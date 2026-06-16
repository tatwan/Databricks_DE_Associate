# Databricks notebook source
# MAGIC %md
# MAGIC # Task 1: Ingest to Bronze (BrewMart)
# MAGIC Job-parameterized incremental ingestion with COPY INTO.
# MAGIC Job parameters arrive in the notebook as **widgets**.

# COMMAND ----------

# Widgets = how notebook tasks receive job/task parameters
dbutils.widgets.text("target_schema", "lab1_yourname")        # ← override per learner / per environment
dbutils.widgets.text("simulate_failure", "false")             # ← used in class to demo repair-and-rerun

target_schema    = dbutils.widgets.get("target_schema")
simulate_failure = dbutils.widgets.get("simulate_failure")

print(f"target_schema={target_schema}, simulate_failure={simulate_failure}")

# COMMAND ----------

# Controlled failure switch — lets the instructor demo failure + repair safely
if simulate_failure.lower() == "true":
    raise Exception("Simulated ingestion failure (set simulate_failure=false and use Repair run)")

# COMMAND ----------

# Idempotent incremental load (Week 2 logic, now production-shaped)
spark.sql(f"""
  CREATE TABLE IF NOT EXISTS workspace.{target_schema}.sales_bronze (
    order_id STRING, order_date STRING, customer_id STRING, store STRING,
    product STRING, category STRING, quantity STRING, unit_price STRING,
    _ingested_at TIMESTAMP
  )
""")

result = spark.sql(f"""
  COPY INTO workspace.{target_schema}.sales_bronze
  FROM (
    SELECT *, current_timestamp() AS _ingested_at
    FROM '/Volumes/workspace/{target_schema}/landing/sales_incoming/'
  )
  FILEFORMAT = CSV
  FORMAT_OPTIONS ('header' = 'true')
  COPY_OPTIONS ('mergeSchema' = 'true')
""")
display(result)

# COMMAND ----------

row_count = spark.table(f"workspace.{target_schema}.sales_bronze").count()
print(f"Bronze row count: {row_count}")

# Pass a value to downstream tasks / the run UI
dbutils.notebook.exit(f"bronze_rows={row_count}")
