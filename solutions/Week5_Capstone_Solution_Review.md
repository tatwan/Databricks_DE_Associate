# Week 5 Capstone Solution Review: BrewMart Returns to Net Revenue

## What You Built

The capstone integrates all seven course domains:

- Ingest returns into bronze.
- Quality-gate returns into silver or quarantine.
- Build a clustered gold table for net revenue.
- Add a constraint.
- Design a two-task job.
- Govern the summary view.
- Validate row counts, deduplication, business rules, and lineage.

The business rule matters: returns do not carry prices, so returned amount must come from the original sales order.

## M2: Build `returns_bronze`

### Goal

Create an all-string bronze table and load `week5_returns.csv` from the `returns_incoming` folder with `COPY INTO`.

### Solution

```sql
CREATE TABLE IF NOT EXISTS returns_bronze (
  return_id STRING,
  order_id STRING,
  return_date STRING,
  quantity_returned STRING,
  reason STRING,
  _ingested_at TIMESTAMP
);
```

```python
display(spark.sql(f"""
COPY INTO returns_bronze
FROM (SELECT *, current_timestamp() AS _ingested_at FROM '{VOL}/returns_incoming/')
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true')
"""))
```

### Why This Works

Bronze is intentionally permissive: store the incoming feed, preserve source shape, and add an audit column. `COPY INTO` tracks loaded files, so rerunning the command should not duplicate rows from the same file.

### Validation

```sql
SELECT COUNT(*) AS bronze_rows
FROM returns_bronze;
```

Expected result: `13`.

## M3: Build `returns_silver` and `returns_quarantine`

### Goal

Split returns into valid rows and quarantined rows:

- Valid rows have an `order_id` that exists in `sales_silver`.
- Non-matching rows stay visible in `returns_quarantine`.

### Solution

```sql
CREATE OR REPLACE TABLE returns_silver AS
SELECT DISTINCT
  r.return_id,
  r.order_id,
  CAST(r.return_date AS DATE)      AS return_date,
  CAST(r.quantity_returned AS INT) AS quantity_returned,
  r.reason
FROM returns_bronze r
WHERE r.order_id IN (SELECT order_id FROM sales_silver);

CREATE OR REPLACE TABLE returns_quarantine AS
SELECT DISTINCT r.*
FROM returns_bronze r
WHERE r.order_id NOT IN (SELECT order_id FROM sales_silver);
```

### Why This Works

This is the quality-gate pattern. Invalid rows do not poison silver, but they are not silently dropped. They remain visible for investigation.

### Common Mistakes

- Using a `WHERE` clause that drops bad rows with no quarantine.
- Adding a constraint too early and blocking the entire load.
- Forgeting `DISTINCT`, which leaves duplicate return IDs.

### Validation

```sql
SELECT COUNT(*) AS silver_rows
FROM returns_silver;
```

Expected result: `11`.

```sql
SELECT order_id
FROM returns_quarantine;
```

Expected result: `2001` only.

## M4: Build `net_revenue_daily`

### Goal

Calculate daily net revenue per store:

```text
net revenue = gross sales revenue - returned amount
```

Returned amount is calculated using the original order's `unit_price`.

### Solution

```sql
CREATE OR REPLACE TABLE net_revenue_daily
CLUSTER BY (store, order_date)
AS
WITH returned AS (
  SELECT s.store,
         s.order_date,
         SUM(r.quantity_returned * s.unit_price) AS returned_amount
  FROM returns_silver r
  JOIN sales_silver s ON r.order_id = s.order_id
  GROUP BY s.store, s.order_date
),
gross AS (
  SELECT store,
         order_date,
         SUM(line_total) AS gross_revenue
  FROM sales_silver
  WHERE store IS NOT NULL
  GROUP BY store, order_date
)
SELECT g.store,
       g.order_date,
       g.gross_revenue,
       COALESCE(rt.returned_amount, 0) AS returned_amount,
       ROUND(g.gross_revenue - COALESCE(rt.returned_amount, 0), 2) AS net_revenue
FROM gross g
LEFT JOIN returned rt
  ON g.store = rt.store
 AND g.order_date = rt.order_date;
```

### Why This Works

The `returned` CTE joins returns to original sales because returns do not include price. The `gross` CTE calculates original revenue. The final query keeps all gross-revenue days and subtracts returns when present.

### Common Mistakes

- Multiplying returned quantity by a missing price from the returns file.
- Using an inner join from gross to returns, which drops days with no returns.
- Forgetting `COALESCE`, which creates `NULL` net revenue for days without returns.
- Clustering on `return_id` instead of business query columns.

### Validation

```sql
SELECT COUNT(*) AS net_gt_gross
FROM net_revenue_daily
WHERE net_revenue > gross_revenue;
```

Expected result: `0`.

## M5: Add and Prove the Constraint

### Goal

Enforce that returned quantity must be positive.

### Solution

```sql
ALTER TABLE returns_silver
ADD CONSTRAINT positive_return CHECK (quantity_returned > 0);
```

### Proof

```python
try:
    spark.sql("""
      INSERT INTO returns_silver VALUES
      ('BAD_RETURN', '1001', current_date(), -1, 'constraint test')
    """)
    raise AssertionError("M5 proof failed: bad return insert was accepted")
except Exception as exc:
    print("M5 proof passed: constraint rejected the bad insert")
    print(str(exc).splitlines()[0])
```

### Why This Works

Constraints are enforced by the table. Bad writes fail. This is different from quarantine, where bad rows are intentionally routed to a separate table.

## M6: Create the Two-Task Job

### Goal

Productionize the capstone pipeline as a small Lakeflow Job.

### Jobs UI Checklist

```text
Job: brewmart_returns_<yourname>
├─ Task 1: ingest_returns
│  └─ notebook or SQL task wrapping M2
├─ Task 2: build_net_revenue
│  └─ notebook or SQL task wrapping M4
│  └─ depends on ingest_returns
├─ Schedule: daily
├─ Schedule status: Paused
└─ Manual run: one successful test run
```

### Why This Works

The first task loads new returns. The second task rebuilds the gold output after ingestion succeeds. The paused schedule allows production configuration before go-live.

### Exam Takeaway

Use a paused trigger when a job should be fully configured but not yet run automatically.

## M7: Govern the Summary View

### Goal

Expose summarized net revenue with least-privilege read access.

### Solution

```sql
CREATE OR REPLACE VIEW net_revenue_summary AS
SELECT store,
       SUM(net_revenue) AS total_net
FROM net_revenue_daily
GROUP BY store;

GRANT SELECT ON VIEW net_revenue_summary TO `account users`;

SHOW GRANTS ON VIEW net_revenue_summary;
```

### Why This Works

The view exposes a business-ready summary without granting direct access to every intermediate table. `GRANT SELECT` is enough for read-only access to the view.

### Common Mistakes

- Granting access to raw or silver tables when the business only needs the summary.
- Forgetting backticks around `account users`.
- Granting `ALL PRIVILEGES` for read-only needs.

## M8: Final Validation

Run these checks before calling the capstone complete.

```sql
SELECT COUNT(*) AS bronze_rows FROM returns_bronze;
```

Expected: `13`.

```sql
SELECT COUNT(*) AS silver_rows FROM returns_silver;
```

Expected: `11`.

```sql
SELECT order_id FROM returns_quarantine;
```

Expected: `2001` only.

```sql
SELECT return_id, COUNT(*) AS duplicate_count
FROM returns_silver
GROUP BY return_id
HAVING COUNT(*) > 1;
```

Expected: no rows.

```sql
SELECT COUNT(*) AS net_gt_gross
FROM net_revenue_daily
WHERE net_revenue > gross_revenue;
```

Expected: `0`.

```sql
DESCRIBE DETAIL net_revenue_daily;
```

Expected: clustering metadata includes `store` and `order_date`.

## Exam Takeaways

- Bronze absorbs raw files; silver enforces trust; gold serves business use cases.
- Quarantine is the right pattern when invalid rows must stay visible.
- `COPY INTO` is safe to rerun for already-loaded files.
- `MERGE INTO` is the pattern for reprocessing quarantined rows once the missing key appears.
- `CLUSTER BY` is the modern layout pattern for query pruning.
- Jobs should model dependencies explicitly with tasks and DAG edges.
- Governance should expose the least data needed for the use case.
