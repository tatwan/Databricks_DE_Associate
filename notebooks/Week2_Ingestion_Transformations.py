# Databricks notebook source
# MAGIC %md
# MAGIC # Week 2 — Ingestion and Bronze→Silver Transformations
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC Free Edition friendly. Requires your Week 1 schema + `landing` volume.
# MAGIC
# MAGIC | Part | Content |
# MAGIC |---|---|
# MAGIC | 1 | Setup |
# MAGIC | 2 | Demo — COPY INTO (idempotency proof), Auto Loader, nested JSON, PySpark mirror |
# MAGIC | 3 | **Your lab** — incremental bronze→silver with MERGE + constraints |
# MAGIC | 4 | Solutions |
# MAGIC
# MAGIC **Files:** upload `week2_sales_day2.csv` into `landing/sales_incoming/` BEFORE Part 2. Keep `week2_sales_day3.csv`, `week2_corrections.csv`, `week2_customers.json` ready.

# COMMAND ----------

dbutils.widgets.text("user_schema", "lab1_yourname")
USER_SCHEMA = dbutils.widgets.get("user_schema")
VOL = f"/Volumes/workspace/{USER_SCHEMA}/landing"

spark.sql("USE CATALOG workspace")
spark.sql(f"USE SCHEMA {USER_SCHEMA}")
print(f"Working in workspace.{USER_SCHEMA} · volume root: {VOL}")

# COMMAND ----------

# MAGIC %md ## Part 2 — Demo
# MAGIC ### 2.1 Bronze target: all strings + audit column (absorb now, type later)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS sales_bronze (
# MAGIC   order_id STRING, order_date STRING, customer_id STRING, store STRING,
# MAGIC   product STRING, category STRING, quantity STRING, unit_price STRING,
# MAGIC   _ingested_at TIMESTAMP
# MAGIC );

# COMMAND ----------

# MAGIC %md ### 2.2 COPY INTO — run this cell, then run it AGAIN. Second run = 0 rows. That word is *idempotent*.

# COMMAND ----------

display(spark.sql(f"""
COPY INTO sales_bronze
FROM (SELECT *, current_timestamp() AS _ingested_at FROM '{VOL}/sales_incoming/')
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true')
"""))

# COMMAND ----------

# MAGIC %md ### 2.3 Now upload `week2_sales_day3.csv` into `sales_incoming/`, then rerun the cell above.
# MAGIC Only the NEW file loads. Incremental ingestion in one SQL statement.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS bronze_rows FROM sales_bronze;  -- 13 after day2, 23 after day3

# COMMAND ----------

# MAGIC %md ### 2.4 Auto Loader — same job, streaming machinery, batch trigger
# MAGIC Anatomy: `cloudFiles` + `schemaLocation` + `checkpointLocation` + `availableNow`.
# MAGIC *(If serverless blocks this in your workspace, read it as exam syntax — that IS the objective.)*

# COMMAND ----------

checkpoint = f"{VOL}/_checkpoints/sales_al"

(spark.readStream
   .format("cloudFiles")
   .option("cloudFiles.format", "csv")
   .option("cloudFiles.schemaLocation", checkpoint)   # remembered schema
   .option("header", "true")
   .load(f"{VOL}/sales_incoming/")
   .writeStream
   .option("checkpointLocation", checkpoint)          # exactly-once bookkeeping
   .trigger(availableNow=True)                        # process new files, then stop
   .toTable(f"workspace.{USER_SCHEMA}.sales_bronze_al")
   .awaitTermination())

df = spark.table(f"workspace.{USER_SCHEMA}.sales_bronze_al")
print("rows:", df.count())
df.printSchema()   # note _rescued_data

# COMMAND ----------

# MAGIC %md ### 2.5 Nested JSON — upload `week2_customers.json` to the volume root first

# COMMAND ----------

display(spark.sql(f"""
SELECT customer_id, name,
       contact.city                 AS city,         -- dot into the STRUCT
       loyalty_tier,
       explode(favorite_categories) AS fav_category  -- one row per ARRAY element
FROM read_files('{VOL}/week2_customers.json', format => 'json')
"""))

# COMMAND ----------

# MAGIC %md ### 2.6 The PySpark mirror — exam-required reading fluency

# COMMAND ----------

from pyspark.sql.functions import col, to_date, round as pround

silver_preview = (
    spark.table("sales_bronze")
      .where(col("order_id").isNotNull())
      .withColumn("order_date", to_date("order_date"))
      .withColumn("quantity",   col("quantity").cast("int"))
      .withColumn("unit_price", col("unit_price").cast("double"))
      .withColumn("line_total", pround(col("quantity") * col("unit_price"), 2))
      .dropDuplicates(["order_id", "order_date", "customer_id"])
)
display(silver_preview.orderBy("order_id"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 3 — LAB: BrewMart's Incremental Bronze→Silver Pipeline
# MAGIC You already built `sales_bronze` incrementally above (Tasks 1–2 ✅).

# COMMAND ----------

# MAGIC %md ### TODO Task 3 — `sales_silver` via CTAS
# MAGIC Cast types · compute `line_total` · drop NULL `order_id` rows · remove exact duplicates.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: CREATE OR REPLACE TABLE sales_silver AS ...

# COMMAND ----------

# MAGIC %md ### TODO Task 4 — Constraints: `order_id` NOT NULL + CHECK quantity > 0

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: two ALTER TABLE statements

# COMMAND ----------

# MAGIC %md ### TODO Task 5 — Upload `week2_corrections.csv` to the volume ROOT, then MERGE into silver
# MAGIC Matched orders → UPDATE; new orders → INSERT.

# COMMAND ----------

# TODO: MERGE INTO sales_silver USING (cleaned read_files of the corrections file) ...

# COMMAND ----------

# MAGIC %md ### Validation

# COMMAND ----------

# MAGIC %sql
# MAGIC -- a) no duplicate order_ids in silver
# MAGIC SELECT order_id, COUNT(*) FROM sales_silver GROUP BY order_id HAVING COUNT(*) > 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- b) corrections applied: 1045 has a store, 1048 has a price, 1059 exists
# MAGIC SELECT order_id, store, unit_price, line_total
# MAGIC FROM sales_silver WHERE order_id IN ('1045','1048','1059') ORDER BY order_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- c) constraint works — this INSERT must FAIL (the error IS the green check)
# MAGIC INSERT INTO sales_silver VALUES
# MAGIC  ('9999', current_date(), 'C999', 'Atlanta', 'Test', 'Test', -1, 10.0, -10.0);

# COMMAND ----------

# MAGIC %md ### ⭐ Stretch
# MAGIC Orders 1033/1034 were *inserted*, not updated — their originals live in Week 1's `sales_raw`, not this bronze. Backfill Week 1 rows into silver, re-MERGE, and verify they become updates. Bonus: rebuild Task 3 in pure PySpark and compare `count()` vs `approx_count_distinct("customer_id")`.

# COMMAND ----------

# MAGIC %md ---
# MAGIC ## Solution
# MAGIC The solution file will be shared by your instructor.
# MAGIC
# MAGIC ✅ Keep your completed schema and tables — the next week builds on them.
