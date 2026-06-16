# Databricks notebook source
# MAGIC %md
# MAGIC # Week 3 — Lakeflow Jobs, Orchestration, and CI/CD (Companion Notebook)
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC Week 3's main work happens in the **Jobs & Pipelines UI**, wiring up two task notebooks:
# MAGIC `week3_01_ingest_bronze` and `week3_02_build_silver` (import them first).
# MAGIC This companion notebook: pre-flight checks · the lab's configuration checklist · the stretch SQL gate · post-run verification · a bundle/CLI reference.

# COMMAND ----------

dbutils.widgets.text("user_schema", "lab1_yourname")
USER_SCHEMA = dbutils.widgets.get("user_schema")
spark.sql("USE CATALOG workspace")
spark.sql(f"USE SCHEMA {USER_SCHEMA}")
print(f"Checking workspace.{USER_SCHEMA}")

# COMMAND ----------

# MAGIC %md ## 1 — Pre-flight: is your Week 2 state intact?

# COMMAND ----------

checks = {
    "sales_bronze exists":  spark.catalog.tableExists(f"workspace.{USER_SCHEMA}.sales_bronze"),
    "sales_silver exists":  spark.catalog.tableExists(f"workspace.{USER_SCHEMA}.sales_silver"),
}
try:
    n = len(dbutils.fs.ls(f"/Volumes/workspace/{USER_SCHEMA}/landing/sales_incoming/"))
    checks[f"sales_incoming/ has files ({n})"] = n >= 2
except Exception:
    checks["sales_incoming/ has files"] = False

for k, v in checks.items():
    print(("✅" if v else "❌"), k)

# COMMAND ----------

# MAGIC %md ## 2 — The lab, as a checklist (build this in the Jobs UI)
# MAGIC
# MAGIC ```text
# MAGIC Job: brewmart_daily_<yourname>
# MAGIC ├─ Job parameters: target_schema=<your schema>, simulate_failure=false
# MAGIC ├─ Task 1 ingest_bronze  → notebook week3_01_ingest_bronze · serverless · retries=2
# MAGIC ├─ Task 2 build_silver   → notebook week3_02_build_silver · depends_on=[ingest_bronze]
# MAGIC ├─ Trigger: Scheduled daily 06:00 — PAUSED
# MAGIC └─ Runs: ① success → ② simulate_failure=true → failed (Task 2 = upstream-failed)
# MAGIC          → ③ set false again → REPAIR RUN (only failed path re-executes)
# MAGIC ```
# MAGIC
# MAGIC **Exam anchors while you build:** job parameters arrive in notebooks as **widgets** · independent tasks run in **parallel** · retries fix *transient* failures only · **Repair run** re-executes failed + downstream tasks, never the green ones.

# COMMAND ----------

# MAGIC %md ## 3 — ⭐ Stretch: the data-quality gate (add as Task 3, SQL or notebook task, depends on build_silver)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Fails the task (and so the job) if silver is empty — a pipeline circuit-breaker
# MAGIC SELECT CASE WHEN COUNT(*) = 0
# MAGIC             THEN raise_error('Quality gate: sales_silver is EMPTY')
# MAGIC             ELSE CONCAT('Quality gate passed: ', COUNT(*), ' rows') END AS gate
# MAGIC FROM sales_silver;

# COMMAND ----------

# MAGIC %md ## 4 — Post-run verification (run after your job's 3 runs)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- The newest sales_silver version should have been written BY THE JOB (see operation + job info)
# MAGIC DESCRIBE HISTORY sales_silver;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS silver_rows FROM sales_silver;   -- 22 (or 25 after corrections MERGE)

# COMMAND ----------

# MAGIC %md ## 5 — CI/CD reference card (Declarative Automation Bundles, formerly DABs)
# MAGIC
# MAGIC The course repo's `cicd/databricks.yml` declares THIS job as code. The four blocks:
# MAGIC
# MAGIC | Block | Purpose |
# MAGIC |---|---|
# MAGIC | `bundle` | name of the bundle |
# MAGIC | `variables` | parameterized config (e.g. `target_schema`) |
# MAGIC | `resources` | the jobs/pipelines being declared (tasks, `depends_on`, trigger) |
# MAGIC | `targets` | environments (dev/prod) with **variable overrides** |
# MAGIC
# MAGIC The three CLI verbs — in order, always:
# MAGIC ```bash
# MAGIC databricks bundle validate          # check syntax + references
# MAGIC databricks bundle deploy -t dev     # PLACE resources in the target workspace
# MAGIC databricks bundle run -t dev brewmart_daily    # EXECUTE the deployed job
# MAGIC ```
# MAGIC
# MAGIC **Git folders:** branch / commit / push happen in the workspace UI — **the pull request is created and merged in the provider** (GitHub/GitLab/Azure DevOps).
# MAGIC
# MAGIC **Exam anchors:** `deploy` places, `run` executes · environments = `targets` + overrides · CI runs the same verbs as a service principal on merge.
