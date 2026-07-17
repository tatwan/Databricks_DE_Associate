# Week 2 Solution Review: Incremental Bronze to Silver Pipeline

## What You Built

You extended the BrewMart pipeline from raw ingestion to a trusted silver table:

- Incremental loading into `sales_bronze`.
- A typed and deduplicated `sales_silver` table.
- Constraints that enforce the silver contract.
- A `MERGE INTO` operation for corrections and upserts.

The central idea is idempotency. Professional pipelines should be safe to rerun.

## Task 3: Build `sales_silver`

### Goal

Create a clean silver table from `sales_bronze`: cast types, calculate `line_total`, remove rows with missing `order_id`, and remove exact duplicates.

### Solution

```sql
CREATE OR REPLACE TABLE sales_silver AS
SELECT DISTINCT
  order_id,
  CAST(order_date AS DATE)   AS order_date,
  customer_id,
  store,
  product,
  category,
  CAST(quantity AS INT)      AS quantity,
  CAST(unit_price AS DOUBLE) AS unit_price,
  ROUND(CAST(quantity AS INT) * CAST(unit_price AS DOUBLE), 2) AS line_total
FROM sales_bronze
WHERE order_id IS NOT NULL;
```

### Why This Works

Bronze preserves source data with minimal assumptions. Silver applies the data contract:

- Business key exists.
- Dates and numbers are correctly typed.
- Duplicate raw rows are removed.
- Derived values are created consistently.

### Common Mistakes

- Cleaning `sales_bronze` directly instead of writing a new silver table.
- Forgetting that `NULL * value` produces `NULL`.
- Using `DISTINCT` when the business requirement is “latest row wins.” For latest-row logic, use a window function such as `ROW_NUMBER()`.

### Validation

```sql
SELECT order_id, COUNT(*)
FROM sales_silver
GROUP BY order_id
HAVING COUNT(*) > 1;
```

Expected result: no rows.

## Task 4: Add Constraints

### Goal

Enforce that every silver row has an `order_id` and a positive quantity.

### Solution

```sql
ALTER TABLE sales_silver ALTER COLUMN order_id SET NOT NULL;

ALTER TABLE sales_silver
ADD CONSTRAINT positive_qty CHECK (quantity > 0);
```

### Why This Works

Constraints turn expectations into table-level enforcement. If a future write violates the contract, Databricks rejects the write instead of silently corrupting silver data.

### Common Mistakes

- Expecting a constraint to quarantine only bad rows. A constraint violation fails the write.
- Adding constraints before cleaning existing bad data.
- Using constraints in bronze, where controlled schema drift may still be expected.

### Validation

```sql
INSERT INTO sales_silver VALUES
 ('9999', current_date(), 'C999', 'Atlanta', 'Test', 'Test', -1, 10.0, -10.0);
```

Expected result: this insert should fail. The failure is the green check.

## Task 5: Apply Corrections with `MERGE INTO`

### Goal

Load `week2_corrections.csv` and apply updates or inserts into `sales_silver`.

### Solution

```python
spark.sql(f"""
MERGE INTO sales_silver AS t
USING (
  SELECT order_id,
         CAST(order_date AS DATE)   AS order_date,
         customer_id,
         store,
         product,
         category,
         CAST(quantity AS INT)      AS quantity,
         CAST(unit_price AS DOUBLE) AS unit_price,
         ROUND(CAST(quantity AS INT) * CAST(unit_price AS DOUBLE), 2) AS line_total
  FROM read_files('{VOL}/week2_corrections.csv', format => 'csv', header => true)
) AS s
ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
""")
```

### Why This Works

`MERGE INTO` is the Delta Lake upsert pattern:

- Matching keys update existing rows.
- New keys insert new rows.
- The operation is atomic.
- Rerunning the same corrections converges to the same state.

### Reading the MERGE, clause by clause

Use this to walk the class through the statement:

- **`spark.sql(f"""...""")`** — it is an f-string only so `{VOL}` (your landing-volume path) is substituted before the SQL runs. That is the one reason this is a Python cell and not a `%sql` cell.
- **`MERGE INTO sales_silver AS t`** — the table being changed, aliased `t` (target).
- **`USING ( SELECT ... FROM read_files(...) ) AS s`** — the incoming data, aliased `s` (source). `read_files` reads the raw CSV **in place** — no staging table. The corrections file is all strings, so the `SELECT` casts and derives every column (`order_date`→`DATE`, `quantity`→`INT`, `unit_price`→`DOUBLE`, recompute `line_total`) so the source has the **exact same shape as silver**.
- **`ON t.order_id = s.order_id`** — the match key. This is how MERGE decides, row by row, "is this correction already an order in silver?"
- **`WHEN MATCHED THEN UPDATE SET *`** — order_ids that already exist in silver: overwrite every column with the corrected values (e.g., 1045 gains a store, 1048 gains a price).
- **`WHEN NOT MATCHED THEN INSERT *`** — order_ids not in silver: insert them as new rows (e.g., 1059).
- **Why `*` works:** `SET *` / `INSERT *` copy columns **by name**, which is exactly why the source had to be pre-cast to silver's schema. If the shapes did not line up, the `*` forms would fail or misalign — the casting is load-bearing, not cosmetic.

One-line summary for the class: *match on `order_id`; if it exists, correct it; if it's new, add it — one atomic, rerun-safe transaction, with the source pre-cast to silver's schema so `UPDATE SET *`/`INSERT *` align.*

### Common Mistakes

- Using plain `INSERT`, which duplicates correction rows on rerun.
- Forgetting to cast source columns before the merge.
- Merging from a source that has duplicate keys. A target row cannot safely match multiple source rows.
- Using `UPDATE` alone, which cannot insert new orders.

### Validation

```sql
SELECT order_id, store, unit_price, line_total
FROM sales_silver
WHERE order_id IN ('1045','1048','1059')
ORDER BY order_id;
```

Expected result:

- `1045` has a corrected store.
- `1048` has a corrected unit price.
- `1059` exists as an inserted row.

## Task 6: Join the Customer Dimension and Aggregate to Gold

### Goal

Build `customers_dim` from the nested JSON, LEFT JOIN it to `sales_silver`, and serve a gold aggregate (`revenue_by_city_tier`).

### Solution

```python
spark.sql(f"""
CREATE OR REPLACE TABLE customers_dim AS
SELECT customer_id, name, loyalty_tier, contact.city AS city
FROM read_files('{VOL}/week2_customers.json', format => 'json')
""")
```

```sql
CREATE OR REPLACE VIEW revenue_by_city_tier AS
SELECT COALESCE(c.city, 'Unknown')  AS city,
       c.loyalty_tier,
       ROUND(SUM(s.line_total), 2)  AS revenue,
       COUNT(DISTINCT s.order_id)   AS orders
FROM sales_silver s
LEFT JOIN customers_dim c ON s.customer_id = c.customer_id
GROUP BY COALESCE(c.city, 'Unknown'), c.loyalty_tier;
```

PySpark mirror (read it fluently — the exam shows DataFrame code):

```python
(s.join(c, "customer_id", "left")
   .withColumn("city", coalesce(col("city"), lit("Unknown")))
   .groupBy("city", "loyalty_tier")
   .agg(round(sum("line_total"), 2).alias("revenue"),
        countDistinct("order_id").alias("orders")))
```

### Why This Works

- `contact.city` dot-navigates the STRUCT — nested JSON needs no pre-flattening.
- **LEFT JOIN** keeps sales whose `customer_id` is missing from the dimension; an INNER JOIN would silently drop them and your revenue would shrink — the classic join bug the exam probes.
- `COALESCE(c.city, 'Unknown')` labels those unmatched rows instead of leaving NULL groups.
- A 10-row dimension joined to a growing fact is the **broadcast join** shape: Spark ships the small table to every executor, so the big side never shuffles (automatic under ~10MB; hint syntax `/*+ BROADCAST(c) */`).
- Gold is a **view** here: cheap recompute, always current. If this aggregation were expensive and hit constantly, a materialized view would trade freshness for read speed.

### Common Mistakes

- INNER JOIN dropping unmatched sales (compare row totals to detect it).
- `COUNT(*)` instead of `COUNT(DISTINCT order_id)` — counts line items, not orders.
- Grouping by the raw `c.city` while selecting the COALESCEd value.

## Stretch: Why Orders 1033/1034 Were Inserted, Not Updated

The corrections file fixes orders whose originals live in **Week 1's `sales_raw`**, not this week's bronze — so the MERGE found no match in silver and inserted them. Correct MERGE behavior; incomplete lineage.

The fix — backfill Week 1's rows into silver, then re-run the MERGE (they now match and become updates):

```sql
INSERT INTO sales_silver
SELECT r.order_id, r.order_date, r.customer_id, r.store, r.product, r.category,
       r.quantity, r.unit_price, r.line_total
FROM sales_raw r
WHERE r.order_id NOT IN (SELECT order_id FROM sales_silver);
-- re-run the Task 5 MERGE, then DESCRIBE HISTORY:
-- numTargetRowsUpdated > 0 for 1033/1034 this time.
```

## Exam Takeaways

- `COPY INTO` is idempotent at the file level.
- Auto Loader uses `cloudFiles`, schema tracking, checkpoints, and `availableNow` for batch-style incremental loading.
- Silver tables are where cleaning, casting, deduplication, and validation happen.
- Constraints reject invalid writes; quarantine patterns preserve bad rows for investigation.
- `MERGE INTO` is the right pattern for corrections, change data capture, and upserts.
- `UNION` vs. `UNION ALL`, broadcast joins, `explode`, and `approx_count_distinct` are all fair game for transformation questions.
