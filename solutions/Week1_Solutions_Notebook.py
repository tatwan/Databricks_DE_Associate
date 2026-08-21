# Databricks notebook source
# MAGIC %md
# MAGIC # Week 1 — Lab Solutions (Study Copy)
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC This notebook is **markdown only** — nothing runs. For each lab task you get: the task, the solution, and why it works. Copy snippets into *your* lab notebook to try them (your `USER_SCHEMA` widget must be set there).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 4 — Build `sales_raw` with CTAS
# MAGIC
# MAGIC **The task:** convert the landing CSV into a managed Delta table with proper types and a computed `line_total`.
# MAGIC
# MAGIC **Solution:**
# MAGIC ```python
# MAGIC spark.sql(f"""
# MAGIC CREATE OR REPLACE TABLE sales_raw AS
# MAGIC SELECT order_id,
# MAGIC        CAST(order_date AS DATE)   AS order_date,
# MAGIC        customer_id, store, product, category,
# MAGIC        CAST(quantity AS INT)      AS quantity,
# MAGIC        CAST(unit_price AS DOUBLE) AS unit_price,
# MAGIC        CAST(quantity AS INT) * CAST(unit_price AS DOUBLE) AS line_total
# MAGIC FROM read_files('/Volumes/workspace/{USER_SCHEMA}/landing/week1_retail_sales.csv',
# MAGIC                 format => 'csv', header => true)
# MAGIC """)
# MAGIC display(spark.table("sales_raw").limit(5))
# MAGIC ```
# MAGIC
# MAGIC **Why it works:** CTAS creates **and** populates in one statement, and its schema is **inferred from the query** — so every type decision is a `CAST` inside the `SELECT`. No `LOCATION` clause → managed table; no `USING` clause → Delta by default.
# MAGIC
# MAGIC **Common mistakes:**
# MAGIC - Declaring column types in the CTAS: `CREATE TABLE sales_raw (order_date DATE) AS SELECT ...` — **not allowed**; the #1 exam trap for this syntax.
# MAGIC - Forgetting to cast before multiplying: string × string fails or silently misbehaves.
# MAGIC - One source row has a missing `unit_price` → its `line_total` is `NULL`. That's correct: `NULL * anything = NULL`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 5 — Confirm the Table Type and Format
# MAGIC
# MAGIC **The task:** prove from metadata that `sales_raw` is a managed Delta table.
# MAGIC
# MAGIC **Solution:**
# MAGIC ```sql
# MAGIC DESCRIBE EXTENDED sales_raw;
# MAGIC ```
# MAGIC
# MAGIC **Why it works:** the exam's forensic tool. Find three rows: `Type: MANAGED`, `Provider: delta`, and `Location` pointing into Unity Catalog managed storage.
# MAGIC
# MAGIC **The reflex to build:** read `Type`, then predict `DROP` — managed drop deletes data (recoverable briefly via `UNDROP`); external drop removes metadata only.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 6 — Persistent View + Temp View
# MAGIC
# MAGIC **The task:** publish reusable store metrics (`sales_by_store`) and keep a scratch query session-scoped (`my_scratch`).
# MAGIC
# MAGIC **Solution:**
# MAGIC ```sql
# MAGIC CREATE OR REPLACE VIEW sales_by_store AS
# MAGIC SELECT store,
# MAGIC        ROUND(SUM(line_total), 2) AS total_revenue,
# MAGIC        COUNT(DISTINCT order_id)  AS order_count
# MAGIC FROM sales_raw
# MAGIC GROUP BY store;
# MAGIC
# MAGIC CREATE OR REPLACE TEMP VIEW my_scratch AS
# MAGIC SELECT category, SUM(quantity) AS units
# MAGIC FROM sales_raw
# MAGIC GROUP BY category;
# MAGIC
# MAGIC SELECT * FROM sales_by_store ORDER BY total_revenue DESC;
# MAGIC ```
# MAGIC
# MAGIC **Why it works:** both store *query logic*, not data. The persistent view is a governed UC object other authorized users can query; the TEMP view dies with your session and is invisible to everyone else.
# MAGIC
# MAGIC **Expected result:** Atlanta, Chicago, Dallas — plus one `NULL`-store group (dirty data, on purpose; Week 2 fixes it).
# MAGIC
# MAGIC **Common mistake:** `COUNT(*)` instead of `COUNT(DISTINCT order_id)` — counts line items, not orders.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 7 — Break It, Prove the Past, Restore
# MAGIC
# MAGIC **The task:** simulate a bad update, prove the old snapshot still exists, then roll back.
# MAGIC
# MAGIC **Solution (run in this order):**
# MAGIC ```sql
# MAGIC -- 1) the "mistake"
# MAGIC UPDATE sales_raw SET unit_price = 0, line_total = 0;
# MAGIC
# MAGIC -- 2) find the versions
# MAGIC DESCRIBE HISTORY sales_raw;
# MAGIC
# MAGIC -- 3) read the past WITHOUT changing anything
# MAGIC SELECT
# MAGIC   (SELECT ROUND(SUM(line_total), 2) FROM sales_raw VERSION AS OF 0) AS total_v0,
# MAGIC   (SELECT ROUND(SUM(line_total), 2) FROM sales_raw)                 AS total_now;
# MAGIC
# MAGIC -- 4) the undo button
# MAGIC RESTORE TABLE sales_raw TO VERSION AS OF 0;
# MAGIC ```
# MAGIC
# MAGIC **Why it works:** every write is a new Delta version recorded in the transaction log. `VERSION AS OF` **reads** an old snapshot (current data unchanged); `RESTORE` **makes** the old snapshot current again — and the restore itself appears in history as another operation.
# MAGIC
# MAGIC **Expected result:** before restore, `total_now = 0` while `total_v0` holds the real revenue. After restore, they match.
# MAGIC
# MAGIC **Common mistake:** thinking the time-travel query in step 3 repairs the table. It doesn't — it only proves the past is readable. Only `RESTORE` changes current state.

# COMMAND ----------

# MAGIC %md
# MAGIC ## ⭐ Stretch — Data Quality Investigation
# MAGIC
# MAGIC **The task:** the file contains two duplicate rows and two missing values. Build `sales_clean` and count what was removed.
# MAGIC
# MAGIC **Solution:**
# MAGIC ```sql
# MAGIC CREATE OR REPLACE TABLE sales_clean AS
# MAGIC SELECT DISTINCT * FROM sales_raw;
# MAGIC
# MAGIC SELECT (SELECT COUNT(*) FROM sales_raw)  -
# MAGIC        (SELECT COUNT(*) FROM sales_clean) AS rows_removed;   -- expect 2
# MAGIC
# MAGIC -- the NULL line_total order:
# MAGIC SELECT * FROM sales_raw WHERE line_total IS NULL;
# MAGIC ```
# MAGIC
# MAGIC **Why:** `DISTINCT` removes rows identical in every column. The `NULL` `line_total` exists because its `unit_price` is missing and `NULL` arithmetic returns `NULL` — the exact data-quality conversation Week 2 opens with.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC **Week 1 exam anchors:** Delta is the default format · CTAS infers schema (CAST in the SELECT) · managed DROP deletes data · `VERSION AS OF` reads, `RESTORE` rewinds · `/Volumes/<catalog>/<schema>/<volume>/` · temp views are session-scoped.
# MAGIC
# MAGIC Keep your schema, tables, and volume — Week 2 builds on them.
