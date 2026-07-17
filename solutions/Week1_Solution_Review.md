# Week 1 Solution Review: Your First Governed Mini-Lakehouse

## What You Built

You created a governed Databricks mini-lakehouse for BrewMart sales data:

- A managed Delta table from a CSV file in a Unity Catalog volume.
- A reusable view for store-level revenue.
- A temporary view for exploratory work.
- A Delta recovery drill using history and restore.

The goal was not just to create a table. The goal was to practice the Week 1 exam anchors: three-level names, managed Delta tables, CTAS, views, temp views, time travel, and `RESTORE TABLE`.

## Task 4: Build `sales_raw` with CTAS

### Goal

Read `week1_retail_sales.csv` from your `landing` volume, create a managed Delta table, cast key fields to proper types, and add `line_total`.

### Solution

```python
spark.sql(f"""
CREATE OR REPLACE TABLE sales_raw AS
SELECT order_id,
       CAST(order_date AS DATE)   AS order_date,
       customer_id,
       store,
       product,
       category,
       CAST(quantity AS INT)      AS quantity,
       CAST(unit_price AS DOUBLE) AS unit_price,
       CAST(quantity AS INT) * CAST(unit_price AS DOUBLE) AS line_total
FROM read_files('/Volumes/workspace/{USER_SCHEMA}/landing/week1_retail_sales.csv',
                format => 'csv', header => true)
""")

display(spark.table("sales_raw").limit(5))
```

### Why This Works

`CREATE OR REPLACE TABLE ... AS SELECT` creates and populates the table in one step. The table schema is inferred from the `SELECT` result, so the casts inside the query control the final column types.

Because no external location is specified, the table is managed by Unity Catalog in the active schema.

### Common Mistakes

- Trying to declare column types in the CTAS table name, such as `CREATE TABLE sales_raw (order_date DATE) AS SELECT ...`.
- Forgetting to cast numeric strings before calculating `line_total`.
- Using file paths directly in later analysis instead of creating a reusable table.

### Validation

```sql
DESCRIBE EXTENDED sales_raw;
```

Look for:

- `Type: MANAGED`
- `Provider: delta`
- A managed storage location.

## Task 5: Confirm Managed Delta Metadata

### Goal

Use table metadata to confirm that `sales_raw` is a managed Delta table.

### Solution

```sql
DESCRIBE EXTENDED sales_raw;
```

### Why This Works

`DESCRIBE EXTENDED` exposes the metadata the exam often asks you to interpret: table type, provider, owner, and location.

### Exam Takeaway

If a question asks how to confirm whether a table is managed or external, inspect metadata. Do not guess from the table name.

## Task 6: Create a View and a Temp View

### Goal

Create one reusable governed view and one session-scoped temporary view.

### Solution

```sql
CREATE OR REPLACE VIEW sales_by_store AS
SELECT store,
       ROUND(SUM(line_total), 2) AS total_revenue,
       COUNT(DISTINCT order_id) AS order_count
FROM sales_raw
GROUP BY store;

CREATE OR REPLACE TEMP VIEW my_scratch AS
SELECT category,
       SUM(quantity) AS units
FROM sales_raw
GROUP BY category;

SELECT * FROM sales_by_store ORDER BY total_revenue DESC;
```

### Why This Works

`sales_by_store` is a named object in Unity Catalog and can be reused after the session ends. `my_scratch` is only available in your current session, so it is appropriate for temporary exploration.

### Common Mistakes

- Using a temp view when downstream users need persistent access.
- Creating a table when the logic should stay live over the base table.
- Forgetting that temp views disappear when the session restarts.

### Validation

```sql
SHOW VIEWS;
```

Confirm that `sales_by_store` appears as a persistent view.

## Task 7: Break It, Inspect History, and Restore

### Goal

Practice Delta Lake recovery: make a bad update, inspect history, and restore the previous version.

### Solution

```sql
UPDATE sales_raw SET unit_price = 0;
```

```sql
DESCRIBE HISTORY sales_raw;
```

```sql
RESTORE TABLE sales_raw TO VERSION AS OF 0;

SELECT ROUND(SUM(unit_price), 2) AS prices_are_back
FROM sales_raw;
```

### Why This Works

Every write creates a new Delta table version. `DESCRIBE HISTORY` shows those versions. `RESTORE TABLE` creates another transaction that returns the table to an earlier version.

### Common Mistakes

- Thinking restore deletes history. It does not; restore itself is another version.
- Confusing `VERSION AS OF` with `RESTORE TABLE`. One queries the past; the other changes the current table state.
- Assuming time travel works forever. Old files can be removed by retention and `VACUUM`.

### Final Validation

```sql
SELECT
  (SELECT ROUND(SUM(line_total), 2) FROM sales_raw VERSION AS OF 0) AS v0,
  (SELECT ROUND(SUM(line_total), 2) FROM sales_raw) AS now;
```

Expected result: `v0` and `now` should match after restore.

## Stretch: Data Quality Investigation

```sql
CREATE OR REPLACE TABLE sales_clean AS
SELECT DISTINCT * FROM sales_raw;

SELECT (SELECT COUNT(*) FROM sales_raw)  -
       (SELECT COUNT(*) FROM sales_clean) AS rows_removed;   -- expect 2

SELECT * FROM sales_raw WHERE line_total IS NULL;            -- the missing-price order
```

`DISTINCT` removes rows identical in every column. The `NULL` `line_total` exists because its `unit_price` is missing and `NULL` arithmetic returns `NULL` — the data-quality conversation Week 2 opens with.

## Exam Takeaways

- Delta is the default table format in Databricks.
- CTAS infers schema from the `SELECT`; use `CAST` to control types.
- Managed table metadata can be inspected with `DESCRIBE EXTENDED`.
- Views persist as governed objects; temp views are session-only.
- Delta history and restore are core recovery tools.
- `VERSION AS OF` reads a prior snapshot; `RESTORE TABLE` changes the current table state.
