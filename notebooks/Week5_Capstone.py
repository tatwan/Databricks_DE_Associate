# Databricks notebook source
# MAGIC %md
# MAGIC # Week 5 — CAPSTONE: BrewMart Returns → Net Revenue
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC **50 minutes. Solo. Everything was taught — nothing here is new.**
# MAGIC Finance needs *net* revenue (sales − returns), governed, quality-gated, clustered, scheduled.
# MAGIC
# MAGIC | Milestone | Target time | Gate? |
# MAGIC |---|---|---|
# MAGIC | M1 upload returns file | 0:03 | |
# MAGIC | M2 bronze via COPY INTO (rerun = 0) | 0:08 | ✅ |
# MAGIC | M3 quality-gated silver + quarantine | 0:20 | ✅ |
# MAGIC | M4 clustered net-revenue gold | 0:30 | |
# MAGIC | M5 constraint | 0:33 | ✅ |
# MAGIC | M6 2-task job, paused schedule | 0:41 | |
# MAGIC | M7 view + GRANT | 0:45 | |
# MAGIC | M8 validations + lineage | 0:50 | |
# MAGIC
# MAGIC Stuck >5 min? Hints are at the bottom — they cost nothing but pride.

# COMMAND ----------

dbutils.widgets.text("user_schema", "lab1_yourname")
USER_SCHEMA = dbutils.widgets.get("user_schema")
VOL = f"/Volumes/workspace/{USER_SCHEMA}/landing"
spark.sql("USE CATALOG workspace")
spark.sql(f"USE SCHEMA {USER_SCHEMA}")
print(f"Capstone arena: workspace.{USER_SCHEMA}")

# COMMAND ----------

# MAGIC %md ## M1 — Land it
# MAGIC Create `returns_incoming/` in your landing volume (Catalog Explorer) and upload `week5_returns.csv` there.

# COMMAND ----------

# Pre-flight: file landed?
try:
    files = dbutils.fs.ls(f"{VOL}/returns_incoming/")
    print("✅", [f.name for f in files])
except Exception as e:
    print("❌ returns_incoming/ not found or empty — do M1 first")

# COMMAND ----------

# MAGIC %md ## M2 — TODO: `returns_bronze` (all STRING + `_ingested_at`), COPY INTO, prove rerun = 0

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: CREATE TABLE IF NOT EXISTS returns_bronze (...)

# COMMAND ----------

# TODO: COPY INTO (use VOL + '/returns_incoming/') — run twice, second run loads 0

# COMMAND ----------

# MAGIC %md ## M3 — TODO: quality-gated silver
# MAGIC `returns_silver` = typed + deduped returns whose `order_id` EXISTS in `sales_silver`.
# MAGIC Non-matching rows → `returns_quarantine` (kept visible — NOT dropped).

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: returns_silver

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: returns_quarantine

# COMMAND ----------

# MAGIC %md ## M4 — TODO: `net_revenue_daily` with CLUSTER BY (store, order_date)
# MAGIC Per store/day: gross revenue (sales), returned amount (returned qty × the **order's** unit price), net = gross − returned.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO

# COMMAND ----------

# MAGIC %md ## M5 — TODO: constraint `quantity_returned > 0` on returns_silver; prove a bad INSERT fails

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO

# COMMAND ----------

# MAGIC %md ## M6 — Jobs UI: 2-task job (`ingest_returns` → `build_net_revenue`), **paused** daily schedule, one successful manual run
# MAGIC ## M7 — TODO: view `net_revenue_summary` + GRANT SELECT to `account users` + SHOW GRANTS

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO M7

# COMMAND ----------

# MAGIC %md ## M8 — Validations (all must pass) + open lineage on `net_revenue_daily`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS bronze_rows FROM returns_bronze;            -- 13

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS silver_rows FROM returns_silver;            -- 11

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT order_id FROM returns_quarantine;                       -- 2001 only

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT return_id, COUNT(*) FROM returns_silver
# MAGIC GROUP BY return_id HAVING COUNT(*) > 1;                        -- 0 rows (R007 deduped)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS net_gt_gross
# MAGIC FROM net_revenue_daily WHERE net_revenue > gross_revenue;      -- 0

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL net_revenue_daily;                             -- clusteringColumns = [store, order_date]

# COMMAND ----------

# MAGIC %md ### ⭐ Stretch (markdown answers, no build)
# MAGIC 1. **Returns-rate alert:** any store's daily returned_amount > 20% of gross → someone is told. Which Week 3 pieces, wired how?
# MAGIC 2. Should quarantined rows ever re-enter silver? Which single statement does it once their orders arrive?

# COMMAND ----------

# MAGIC %md ---
# MAGIC ## 🔒 HINTS (scroll only if stuck > 5 min)
# MAGIC - **H-M3:** Week 2, joins slide — the anti-join idiom: two tables from one source, split by `IN` / `NOT IN` against `sales_silver.order_id`.
# MAGIC - **H-M4:** Returns don't know prices. Who does? Join `returns_silver` to `sales_silver` ON order_id, then LEFT JOIN the two daily aggregates.
# MAGIC - **H-M6:** Your Week 3 job is the template — clone the pattern (widgets for `target_schema`), not the work.

# COMMAND ----------

# MAGIC %md ---
# MAGIC ## 🔒 SOLUTIONS (debrief only)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- M2
# MAGIC CREATE TABLE IF NOT EXISTS returns_bronze (
# MAGIC   return_id STRING, order_id STRING, return_date STRING,
# MAGIC   quantity_returned STRING, reason STRING, _ingested_at TIMESTAMP
# MAGIC );

# COMMAND ----------

display(spark.sql(f"""
COPY INTO returns_bronze
FROM (SELECT *, current_timestamp() AS _ingested_at FROM '{VOL}/returns_incoming/')
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true')
"""))

# COMMAND ----------

# MAGIC %sql
# MAGIC -- M3
# MAGIC CREATE OR REPLACE TABLE returns_silver AS
# MAGIC SELECT DISTINCT r.return_id, r.order_id,
# MAGIC        CAST(r.return_date AS DATE)      AS return_date,
# MAGIC        CAST(r.quantity_returned AS INT) AS quantity_returned,
# MAGIC        r.reason
# MAGIC FROM returns_bronze r
# MAGIC WHERE r.order_id IN (SELECT order_id FROM sales_silver);
# MAGIC
# MAGIC CREATE OR REPLACE TABLE returns_quarantine AS
# MAGIC SELECT DISTINCT r.* FROM returns_bronze r
# MAGIC WHERE r.order_id NOT IN (SELECT order_id FROM sales_silver);

# COMMAND ----------

# MAGIC %sql
# MAGIC -- M4
# MAGIC CREATE OR REPLACE TABLE net_revenue_daily
# MAGIC CLUSTER BY (store, order_date)
# MAGIC AS
# MAGIC WITH returned AS (
# MAGIC   SELECT s.store, s.order_date,
# MAGIC          SUM(r.quantity_returned * s.unit_price) AS returned_amount
# MAGIC   FROM returns_silver r JOIN sales_silver s ON r.order_id = s.order_id
# MAGIC   GROUP BY s.store, s.order_date
# MAGIC ),
# MAGIC gross AS (
# MAGIC   SELECT store, order_date, SUM(line_total) AS gross_revenue
# MAGIC   FROM sales_silver WHERE store IS NOT NULL
# MAGIC   GROUP BY store, order_date
# MAGIC )
# MAGIC SELECT g.store, g.order_date, g.gross_revenue,
# MAGIC        COALESCE(rt.returned_amount, 0) AS returned_amount,
# MAGIC        ROUND(g.gross_revenue - COALESCE(rt.returned_amount, 0), 2) AS net_revenue
# MAGIC FROM gross g
# MAGIC LEFT JOIN returned rt ON g.store = rt.store AND g.order_date = rt.order_date;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- M5
# MAGIC ALTER TABLE returns_silver ADD CONSTRAINT positive_return CHECK (quantity_returned > 0);

# COMMAND ----------

# MAGIC %sql
# MAGIC -- M7
# MAGIC CREATE OR REPLACE VIEW net_revenue_summary AS
# MAGIC SELECT store, SUM(net_revenue) AS total_net FROM net_revenue_daily GROUP BY store;
# MAGIC GRANT SELECT ON VIEW net_revenue_summary TO `account users`;
# MAGIC SHOW GRANTS ON VIEW net_revenue_summary;

# COMMAND ----------

# MAGIC %md
# MAGIC 🏁 **Course complete.** Final week: weakest domain first · redo labs from scratch · retake missed mock questions · book the exam at webassessor.com/databricks · 2 minutes per question · flag and move · answer everything.
