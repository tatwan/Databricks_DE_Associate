# Databricks notebook source
# MAGIC %md
# MAGIC # Task 2: Build Silver (BrewMart)
# MAGIC **Role in the DAG:** downstream task — the scheduler starts it **only after `ingest_bronze` succeeds** (`depends_on`). If Task 1 fails, this task never runs and shows **Upstream failed** — a status, not a bug.
# MAGIC
# MAGIC The transformation is Week 2's silver build, unchanged. What's new is *how it participates in a pipeline*: parameterized target, a task value read from upstream, and an idempotent rebuild that makes Repair run safe.

# COMMAND ----------

dbutils.widgets.text("target_schema", "lab1_yourname")
target_schema = dbutils.widgets.get("target_schema")

# COMMAND ----------

# MAGIC %md ### Read the upstream task's TASK VALUE
# MAGIC **Goal:** receive runtime data from `ingest_bronze` — not configuration (that's what job parameters are for), but a *result* produced during this run.
# MAGIC
# MAGIC **Predict:** what value prints when you run this cell interactively, outside a job?
# MAGIC
# MAGIC **Look for:** inside a job → the real row count Task 1 set. Interactively → `debugValue` (0), because there is no upstream task. That's exactly what `debugValue` is for.
# MAGIC
# MAGIC **Why it matters (exam):** parameters carry config INTO tasks (as widgets); task values carry small results BETWEEN tasks; big data moves through tables. Three lanes — questions mix them up on purpose.

# COMMAND ----------

# Read the upstream task's TASK VALUE (set by ingest_bronze).
# debugValue is used when you run this notebook interactively (outside a job).
bronze_rows = dbutils.jobs.taskValues.get(
    taskKey="ingest_bronze", key="bronze_rows", default=-1, debugValue=0)
print(f"Upstream reported bronze_rows={bronze_rows}")
# Exam contract: job PARAMETERS carry config into tasks (as widgets);
# TASK VALUES carry small runtime results BETWEEN tasks. Big data goes through tables.

# COMMAND ----------

# MAGIC %md ### Idempotent rebuild — why Repair run is fearless here
# MAGIC **Goal:** rebuild silver from bronze so that running this task once, twice, or via a repair always converges to the same correct table.
# MAGIC
# MAGIC **Why `CREATE OR REPLACE` and not `INSERT`:** an INSERT-based task would duplicate rows every rerun. `CREATE OR REPLACE ... AS SELECT` derives silver *entirely from bronze*, atomically, keeping history. Rerun-safe by construction.
# MAGIC
# MAGIC **Look for (after a job run):** `DESCRIBE HISTORY sales_silver` — the newest version's metadata shows it was written **by the job**, not by a person.

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
