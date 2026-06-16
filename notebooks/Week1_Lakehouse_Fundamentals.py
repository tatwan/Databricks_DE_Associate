# Databricks notebook source
# MAGIC %md
# MAGIC # Week 1 — Lakehouse Foundations: Delta Lake, Unity Catalog, and Table Fundamentals
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC Runs entirely on **Databricks Free Edition** (serverless).
# MAGIC
# MAGIC | Part | Content |
# MAGIC |---|---|
# MAGIC | 1 | Setup (your schema) |
# MAGIC | 2 | Instructor demo — namespace, DDL, CTAS, time travel, volumes, views |
# MAGIC | 3 | **Your lab** — BrewMart mini-lakehouse (TODO cells) |
# MAGIC | 4 | Solutions (no peeking until you've tried) |

# COMMAND ----------

# MAGIC %md ## Part 1 — Setup
# MAGIC Set your schema name once. Every cell below uses it — no other edits needed.

# COMMAND ----------

dbutils.widgets.text("user_schema", "lab1_yourname")
USER_SCHEMA = dbutils.widgets.get("user_schema")

spark.sql("USE CATALOG workspace")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {USER_SCHEMA}")
spark.sql(f"USE SCHEMA {USER_SCHEMA}")
print(f"Working in: workspace.{USER_SCHEMA}")

# COMMAND ----------

# MAGIC %md ## Part 2 — Demo
# MAGIC ### 2.1 The three-level namespace: `catalog.schema.object`

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW CATALOGS;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT trip_distance, fare_amount, pickup_zip, dropoff_zip
# MAGIC FROM samples.nyctaxi.trips
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md ### 2.2 DDL — empty managed Delta table (Delta is the DEFAULT format)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE trip_zones (
# MAGIC   zip        STRING,
# MAGIC   zone_label STRING,
# MAGIC   is_airport BOOLEAN
# MAGIC );
# MAGIC
# MAGIC INSERT INTO trip_zones VALUES
# MAGIC   ('10001', 'Midtown',   false),
# MAGIC   ('11371', 'LaGuardia', true),
# MAGIC   ('11430', 'JFK',       true);
# MAGIC
# MAGIC SELECT * FROM trip_zones;

# COMMAND ----------

# MAGIC %md ### 2.3 CTAS — create AND populate; schema inferred from the query
# MAGIC ⚠️ Exam rule: a CTAS cannot declare a column-type list — control types with `CAST` in the SELECT.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE short_trips AS
# MAGIC SELECT pickup_zip, dropoff_zip,
# MAGIC        CAST(trip_distance AS DOUBLE) AS trip_distance,
# MAGIC        fare_amount
# MAGIC FROM samples.nyctaxi.trips
# MAGIC WHERE trip_distance < 2;
# MAGIC
# MAGIC SELECT COUNT(*) AS short_trip_count FROM short_trips;

# COMMAND ----------

# MAGIC %md ### 2.4 Read metadata like the exam does
# MAGIC Find: **Type: MANAGED · Provider: delta · Location: UC-managed storage**

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED short_trips;

# COMMAND ----------

# MAGIC %md ### 2.5 Every write = a version → history, time travel, RESTORE

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE short_trips SET fare_amount = fare_amount + 1.00
# MAGIC WHERE pickup_zip = '10282';

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY short_trips;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   (SELECT ROUND(SUM(fare_amount), 2) FROM short_trips VERSION AS OF 0) AS total_v0,
# MAGIC   (SELECT ROUND(SUM(fare_amount), 2) FROM short_trips)                 AS total_now;

# COMMAND ----------

# MAGIC %md ### 2.6 Volumes — governed storage for FILES
# MAGIC After running the next cell: **Catalog Explorer → workspace → your schema → Volumes → landing → Upload** `week1_retail_sales.csv`

# COMMAND ----------

spark.sql(f"CREATE VOLUME IF NOT EXISTS workspace.{USER_SCHEMA}.landing")
print(f"Upload week1_retail_sales.csv to: /Volumes/workspace/{USER_SCHEMA}/landing/")

# COMMAND ----------

# Query the raw file IN PLACE — no table yet
display(spark.sql(f"""
  SELECT * FROM read_files(
    '/Volumes/workspace/{USER_SCHEMA}/landing/week1_retail_sales.csv',
    format => 'csv', header => true)
  LIMIT 5
"""))

# COMMAND ----------

# MAGIC %md ### 2.7 Views vs temp views — persistence and visibility

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW airport_short_trips AS
# MAGIC SELECT s.*, z.zone_label
# MAGIC FROM short_trips s JOIN trip_zones z ON s.dropoff_zip = z.zip
# MAGIC WHERE z.is_airport;
# MAGIC
# MAGIC CREATE OR REPLACE TEMP VIEW scratch_fares AS
# MAGIC SELECT pickup_zip, AVG(fare_amount) AS avg_fare FROM short_trips GROUP BY pickup_zip;
# MAGIC
# MAGIC SHOW VIEWS;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 3 — LAB: Your First Governed Mini-Lakehouse (BrewMart)
# MAGIC Sales CSVs arrive by email today. Make them queryable, governed, auditable — and prove bad updates are recoverable.
# MAGIC
# MAGIC ✅ You already did Tasks 1–3 above (schema, volume, upload + inspect).

# COMMAND ----------

# MAGIC %md ### TODO Task 4 — `sales_raw` via CTAS
# MAGIC Cast `order_date` to DATE, `quantity` to INT, `unit_price` to DOUBLE; add `line_total` = quantity × unit_price.

# COMMAND ----------

# TODO: build sales_raw with a CTAS from read_files(...)
# spark.sql(f""" CREATE OR REPLACE TABLE sales_raw AS SELECT ... """)

# COMMAND ----------

# MAGIC %md ### TODO Task 5 — Confirm it's a MANAGED Delta table

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: which command shows Type and Provider?

# COMMAND ----------

# MAGIC %md ### TODO Task 6 — One VIEW (`sales_by_store`: revenue + order count per store) and one TEMP VIEW (anything exploratory)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: CREATE OR REPLACE VIEW sales_by_store AS ...
# MAGIC -- TODO: CREATE OR REPLACE TEMP VIEW my_scratch AS ...

# COMMAND ----------

# MAGIC %md ### TODO Task 7 — Break it, prove the past, RESTORE
# MAGIC 1. UPDATE all unit prices to 0 (the "mistake") · 2. DESCRIBE HISTORY · 3. query `VERSION AS OF 0` · 4. RESTORE

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: your recovery drill here

# COMMAND ----------

# MAGIC %md ### Validation — all four must pass

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 1) sales_raw exists with line_total; 2) view returns 3 stores + 1 NULL-store row;
# MAGIC -- 3) history shows CTAS → UPDATE → RESTORE; 4) v0 total == current total
# MAGIC SELECT
# MAGIC   (SELECT ROUND(SUM(line_total),2) FROM sales_raw VERSION AS OF 0) AS v0,
# MAGIC   (SELECT ROUND(SUM(line_total),2) FROM sales_raw)                 AS now;

# COMMAND ----------

# MAGIC %md
# MAGIC ### ⭐ Stretch
# MAGIC The file holds 2 duplicate rows and 2 NULLs. Build `sales_clean` (dedup via DISTINCT or ROW_NUMBER) and count dropped rows. Which order has a NULL `line_total` — and why? (NULL arithmetic — Week 2 preview.)

# COMMAND ----------

# MAGIC %md ---
# MAGIC ## Instructor Solution
# MAGIC The completed solution is kept in `instructor_private/notebook_solutions/Week1_Lakehouse_Fundamentals_Solution.py` and is intentionally ignored by git.
# MAGIC
# MAGIC ✅ Keep your completed schema and tables — the next week builds on them.
