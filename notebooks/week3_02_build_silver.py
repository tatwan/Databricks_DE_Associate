# Databricks notebook source
# MAGIC %md
# MAGIC # Task 2: Build Silver (BrewMart)
# MAGIC Runs only after Task 1 succeeds (DAG dependency).
# MAGIC Rebuilds the typed, deduplicated silver table — idempotent by design.

# COMMAND ----------

dbutils.widgets.text("target_schema", "lab1_yourname")
target_schema = dbutils.widgets.get("target_schema")

# COMMAND ----------

spark.sql(f"""
  CREATE OR REPLACE TABLE workspace.{target_schema}.sales_silver AS
  SELECT DISTINCT
    order_id,
    CAST(order_date AS DATE)    AS order_date,
    customer_id,
    store,
    product,
    category,
    CAST(quantity AS INT)       AS quantity,
    CAST(unit_price AS DOUBLE)  AS unit_price,
    ROUND(CAST(quantity AS INT) * CAST(unit_price AS DOUBLE), 2) AS line_total
  FROM workspace.{target_schema}.sales_bronze
  WHERE order_id IS NOT NULL
""")

# COMMAND ----------

silver_count = spark.table(f"workspace.{target_schema}.sales_silver").count()
revenue = spark.sql(f"""
  SELECT ROUND(SUM(line_total), 2) AS total
  FROM workspace.{target_schema}.sales_silver
""").collect()[0]["total"]

print(f"Silver rows: {silver_count} | Total revenue: {revenue}")
dbutils.notebook.exit(f"silver_rows={silver_count}")
