# Databricks notebook source
# MAGIC %md
# MAGIC # Task 1: Ingest to Bronze (BrewMart)
# MAGIC **Role in the DAG:** first task of the `brewmart_daily` job. The job — not a human — runs this notebook.
# MAGIC
# MAGIC This is Week 2's COPY INTO logic, now **production-shaped**. Three changes to notice as you read:
# MAGIC 1. **No hardcoded schema** — the target arrives as a job parameter (widget). Same notebook serves dev and prod.
# MAGIC 2. **Fully qualified names** (`workspace.<schema>.table`) — a job task cannot rely on someone having clicked `USE SCHEMA` first.
# MAGIC 3. **Results are published** for the run UI and downstream tasks (last cell).
# MAGIC
# MAGIC You may run it once interactively to sanity-check (set the widget to your schema) — but its home is the Jobs UI.

# COMMAND ----------

# MAGIC %md ### Receive job parameters as widgets
# MAGIC **Goal:** see the parameters→widgets contract in real code.
# MAGIC
# MAGIC When a job runs this notebook, the job parameter `target_schema` lands in the widget **of the same name** — `dbutils.widgets.get` doesn't care whether a human or a job set it. That is the whole contract.
# MAGIC
# MAGIC **Look for:** the printed values. Interactively you get the widget defaults; inside a job you get the job's parameter values — same code, no edits.
# MAGIC
# MAGIC **Why it matters (exam):** "How does a notebook task receive a job parameter?" → *as a widget*. And parameterizing the schema is why one notebook can serve dev → test → prod.

# COMMAND ----------

# Widgets = how notebook tasks receive job/task parameters
dbutils.widgets.text("target_schema", "lab1_yourname")        # ← override per learner / per environment
dbutils.widgets.text("simulate_failure", "false")             # ← used in class to demo repair-and-rerun

target_schema    = dbutils.widgets.get("target_schema")
simulate_failure = dbutils.widgets.get("simulate_failure")

print(f"target_schema={target_schema}, simulate_failure={simulate_failure}")

# COMMAND ----------

# MAGIC %md ### The controlled failure switch
# MAGIC **Goal:** give ourselves a safe way to make this task fail on demand — so we can practice diagnosis and **Repair run** on a failure we control.
# MAGIC
# MAGIC **Predict:** with `simulate_failure=true`, this task fails every attempt. Will the retries you configured on the task fix it?
# MAGIC
# MAGIC **Look for:** nothing (it passes silently while the parameter is `false`). When triggered: the task fails, retries fail too — retries fix *transient* problems, and this failure is deterministic. Downstream `build_silver` shows **Upstream failed**: it didn't break; its dependency did.

# COMMAND ----------

# Controlled failure switch — lets the instructor demo failure + repair safely
if simulate_failure.lower() == "true":
    raise Exception("Simulated ingestion failure (set simulate_failure=false and use Repair run)")

# COMMAND ----------

# MAGIC %md ### The idempotent load — why this task is safe to retry and repair
# MAGIC **Goal:** run Week 2's COPY INTO unchanged and understand why it makes orchestration *safe*.
# MAGIC
# MAGIC **Predict:** your `sales_incoming/` files were already loaded in Week 2. How many rows will this task insert?
# MAGIC
# MAGIC **Look for:** `num_inserted_rows = 0` on an unchanged folder. Not a bug — the victory lap. COPY INTO tracks files, so the scheduler can run this daily, retry it, or repair it, and it never double-loads.
# MAGIC
# MAGIC **Why it matters (exam):** idempotent tasks are what make retries and Repair run *safe*. Pipelines built on plain `INSERT` are why some teams fear reruns.

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

# MAGIC %md ### Publish results downstream — two mechanisms, know both
# MAGIC **Goal:** hand this task's outcome to (a) the run UI and (b) the next task.
# MAGIC
# MAGIC - `dbutils.jobs.taskValues.set(key, value)` → structured value a **downstream task** reads with `taskValues.get`. For small results only (counts, flags); big data flows through tables.
# MAGIC - `dbutils.notebook.exit(string)` → one string shown as this task's **output** in the run UI, and ends the notebook.
# MAGIC
# MAGIC **Look for (after a job run):** open Task 1's run page — the exit string is its output; open Task 2's output — it prints the task value it received.

# COMMAND ----------

row_count = spark.table(f"workspace.{target_schema}.sales_bronze").count()
print(f"Bronze row count: {row_count}")

# Two ways to hand results downstream — know BOTH for the exam:
# 1) Task values: structured, read by a downstream task via taskValues.get
dbutils.jobs.taskValues.set(key="bronze_rows", value=row_count)

# 2) notebook.exit: one string, shown in the run UI as the task's output
dbutils.notebook.exit(f"bronze_rows={row_count}")
