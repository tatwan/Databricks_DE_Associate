# Databricks notebook source
# MAGIC %md
# MAGIC # Week 2 — Lab Solutions (Study Copy)
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC Markdown only — nothing runs. Task → solution → why → mistakes. Copy snippets into *your* lab notebook (where `USER_SCHEMA` and `VOL` are defined).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 3 — Build `sales_silver` with a CTAS
# MAGIC
# MAGIC **The task:** turn all-string `sales_bronze` into a typed, deduplicated `sales_silver` with `line_total`, dropping rows with no `order_id`.
# MAGIC
# MAGIC **Solution:**
# MAGIC ```sql
# MAGIC CREATE OR REPLACE TABLE sales_silver AS
# MAGIC SELECT DISTINCT
# MAGIC   order_id,
# MAGIC   CAST(order_date AS DATE)   AS order_date,
# MAGIC   customer_id, store, product, category,
# MAGIC   CAST(quantity AS INT)      AS quantity,
# MAGIC   CAST(unit_price AS DOUBLE) AS unit_price,
# MAGIC   ROUND(CAST(quantity AS INT) * CAST(unit_price AS DOUBLE), 2) AS line_total
# MAGIC FROM sales_bronze
# MAGIC WHERE order_id IS NOT NULL;
# MAGIC ```
# MAGIC
# MAGIC **Why it works:** bronze absorbs, silver **enforces** — casts fix the types, `WHERE order_id IS NOT NULL` enforces the business key, `SELECT DISTINCT` removes exact-duplicate rows, and the whole thing is a *new* table (never mutate bronze).
# MAGIC
# MAGIC **Common mistakes:**
# MAGIC - Cleaning `sales_bronze` in place — you lose the ability to replay.
# MAGIC - Expecting `line_total` to be `0` where `unit_price` is NULL — it's `NULL` (`NULL` arithmetic), and that's correct at this stage.
# MAGIC - Using `DISTINCT` when the requirement is "latest row wins" — that needs `ROW_NUMBER() OVER (PARTITION BY key ORDER BY ts DESC) = 1` (demo 2.7).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 4 — Add Constraints
# MAGIC
# MAGIC **The task:** enforce that `order_id` is never NULL and `quantity` is positive.
# MAGIC
# MAGIC **Solution:**
# MAGIC ```sql
# MAGIC ALTER TABLE sales_silver ALTER COLUMN order_id SET NOT NULL;
# MAGIC ALTER TABLE sales_silver ADD CONSTRAINT positive_qty CHECK (quantity > 0);
# MAGIC ```
# MAGIC
# MAGIC **Why it works:** constraints are the silver contract, enforced **at write time** — any future INSERT/UPDATE/MERGE that violates them **fails as a whole transaction**. They only bind if existing data already satisfies them (which Task 3 guaranteed).
# MAGIC
# MAGIC **The exam distinction:** a CHECK constraint does **not** skip bad rows — it rejects the entire write. Skipping gracefully is the *quarantine pattern* or declarative *expectations with a DROP policy*.
# MAGIC
# MAGIC **Proof it works:** validation cell (c) inserts `quantity = -1` and **must fail** — the error is the green check.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 5 — Apply Corrections with MERGE
# MAGIC
# MAGIC **The task:** one atomic upsert — corrected orders update, brand-new orders insert.
# MAGIC
# MAGIC **Solution (Python cell, to use the `{VOL}` path):**
# MAGIC ```python
# MAGIC spark.sql(f"""
# MAGIC MERGE INTO sales_silver AS t
# MAGIC USING (
# MAGIC   SELECT order_id,
# MAGIC          CAST(order_date AS DATE)   AS order_date,
# MAGIC          customer_id, store, product, category,
# MAGIC          CAST(quantity AS INT)      AS quantity,
# MAGIC          CAST(unit_price AS DOUBLE) AS unit_price,
# MAGIC          ROUND(CAST(quantity AS INT) * CAST(unit_price AS DOUBLE), 2) AS line_total
# MAGIC   FROM read_files('{VOL}/week2_corrections.csv', format => 'csv', header => true)
# MAGIC ) AS s
# MAGIC ON t.order_id = s.order_id
# MAGIC WHEN MATCHED THEN UPDATE SET *
# MAGIC WHEN NOT MATCHED THEN INSERT *
# MAGIC """)
# MAGIC ```
# MAGIC
# MAGIC **Why it works:** the `USING` subquery cleans/casts the raw corrections to the *same shape as silver* before matching. `WHEN MATCHED → UPDATE SET *`, `WHEN NOT MATCHED → INSERT *`. One transaction, one new table version — rerunning converges to the same state (row-level idempotency).
# MAGIC
# MAGIC **Common mistakes:**
# MAGIC - Skipping the casts in the source → type misalignment with `SET *` / `INSERT *`.
# MAGIC - Duplicate keys in the source → "multiple source rows matched" error; deduplicate the source first.
# MAGIC - Plain `INSERT` instead of MERGE → duplicates on every rerun.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 6 — Join the Customer Dimension, Aggregate to Gold
# MAGIC
# MAGIC **The task:** build `customers_dim` from the nested JSON, LEFT JOIN it to silver, and serve `revenue_by_city_tier`.
# MAGIC
# MAGIC **Solution:**
# MAGIC ```python
# MAGIC spark.sql(f"""
# MAGIC CREATE OR REPLACE TABLE customers_dim AS
# MAGIC SELECT customer_id, name, loyalty_tier, contact.city AS city
# MAGIC FROM read_files('{VOL}/week2_customers.json', format => 'json')
# MAGIC """)
# MAGIC ```
# MAGIC ```sql
# MAGIC CREATE OR REPLACE VIEW revenue_by_city_tier AS
# MAGIC SELECT COALESCE(c.city, 'Unknown')  AS city,
# MAGIC        c.loyalty_tier,
# MAGIC        ROUND(SUM(s.line_total), 2)  AS revenue,
# MAGIC        COUNT(DISTINCT s.order_id)   AS orders
# MAGIC FROM sales_silver s
# MAGIC LEFT JOIN customers_dim c ON s.customer_id = c.customer_id
# MAGIC GROUP BY COALESCE(c.city, 'Unknown'), c.loyalty_tier;
# MAGIC
# MAGIC SELECT * FROM revenue_by_city_tier ORDER BY revenue DESC;
# MAGIC ```
# MAGIC
# MAGIC **Why it works:**
# MAGIC - `contact.city` dot-navigates the STRUCT — nested JSON needs no pre-flattening.
# MAGIC - **LEFT JOIN** keeps sales whose `customer_id` isn't in the dimension; an INNER JOIN would silently drop them and revenue would shrink — the exam's favorite join bug. The `Unknown` city row is your proof.
# MAGIC - A 10-row dimension against a growing fact table is the **broadcast join** shape (automatic under ~10MB; hint: `/*+ BROADCAST(c) */`).
# MAGIC - Gold is a **view**: cheap recompute, always current. An expensive, constantly-hit aggregation would justify a materialized view instead.
# MAGIC
# MAGIC **PySpark mirror (read it fluently — exam shows DataFrame code):**
# MAGIC ```python
# MAGIC (s.join(c, "customer_id", "left")
# MAGIC    .withColumn("city", coalesce(col("city"), lit("Unknown")))
# MAGIC    .groupBy("city", "loyalty_tier")
# MAGIC    .agg(round(sum("line_total"), 2).alias("revenue"),
# MAGIC         countDistinct("order_id").alias("orders")))
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## ⭐ Stretch — Why Orders 1033/1034 Were Inserted, Not Updated
# MAGIC
# MAGIC **What happened:** the corrections file fixes orders whose originals live in **Week 1's `sales_raw`**, not this week's bronze → the MERGE found no match in silver and inserted them. Correct MERGE behavior; incomplete lineage.
# MAGIC
# MAGIC **The fix:** backfill Week 1's rows into silver first, then re-run the MERGE — now they match and become updates:
# MAGIC ```sql
# MAGIC INSERT INTO sales_silver
# MAGIC SELECT r.order_id, r.order_date, r.customer_id, r.store, r.product, r.category,
# MAGIC        r.quantity, r.unit_price, r.line_total
# MAGIC FROM sales_raw r
# MAGIC WHERE r.order_id NOT IN (SELECT order_id FROM sales_silver);
# MAGIC -- then re-run the Task 5 MERGE and check DESCRIBE HISTORY:
# MAGIC -- numTargetRowsUpdated > 0 for 1033/1034 this time.
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC **Week 2 exam anchors:** COPY INTO tracks files (rerun = 0) · Auto Loader = `cloudFiles` + schemaLocation + checkpoint + `availableNow` · `_rescued_data` · dot syntax + `explode` · MERGE = atomic row-level upsert · CHECK rejects the whole write · LEFT JOIN keeps unmatched rows · small dim + big fact = broadcast · `ROW_NUMBER ... = 1` = latest per key.
