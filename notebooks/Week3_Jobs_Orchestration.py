# Databricks notebook source
# MAGIC %md
# MAGIC # Week 3 — Lakeflow Jobs, Orchestration, and CI/CD (Companion Notebook)
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC **How this week works (different from Weeks 1–2):**
# MAGIC
# MAGIC | Notebook | Who runs it | How |
# MAGIC |---|---|---|
# MAGIC | **This companion** | You, interactively | Pre-flight before the lab · verification after |
# MAGIC | `week3_01_ingest_bronze` | **The job** | Wired as Task 1 in the Jobs UI |
# MAGIC | `week3_02_build_silver` | **The job** | Wired as Task 2, `depends_on` Task 1 |
# MAGIC
# MAGIC Import all three first. You may open the two task notebooks and run them once to sanity-check — but their *point* is to be executed by the scheduler, not by you. The middle of today's lab happens in the **Jobs & Pipelines UI**, guided by the checklist in section 2.

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
# MAGIC
# MAGIC **New this week in the task notebooks:** Task 1 also publishes its row count as a **task value** (`dbutils.jobs.taskValues.set`), and Task 2 reads it (`taskValues.get`). After your first successful run, open Task 2's output and find `Upstream reported bronze_rows=...` — that is runtime data flowing BETWEEN tasks, distinct from job parameters (config flowing INTO tasks).

# COMMAND ----------

# MAGIC %md ## 2b — Notebook composition: `%run` vs a job task (exam discriminator)
# MAGIC
# MAGIC Databricks notebooks support **magic commands**: `%sql`, `%python`, `%md`, `%run` (you have used the first three all course).
# MAGIC
# MAGIC Two ways to "run another notebook" — the exam expects you to tell them apart:
# MAGIC
# MAGIC | | `%run ./helper_notebook` | Job task (or `dbutils.notebook.run`) |
# MAGIC |---|---|---|
# MAGIC | Runs where? | **Inline, same session** — as if its cells were pasted here | **Isolated run** — own state, own results |
# MAGIC | Variables/functions defined there | **Available here afterward** | NOT shared — pass data via parameters/task values/tables |
# MAGIC | Use for | Shared setup/helper functions (config, common imports) | Orchestration: dependencies, retries, schedules, repair |
# MAGIC | Returns | Nothing (it's inclusion, not a call) | Exit value / task values |
# MAGIC
# MAGIC **Exam answer shape:** "Reuse helper functions across notebooks" → `%run`. "Run notebooks in order with retries and a schedule" → a **job with tasks** — not a driver notebook full of `%run` calls.
# MAGIC
# MAGIC > Note: `%run` must be alone in its cell, and the path is relative to this notebook.

# COMMAND ----------

# MAGIC %md ## 2c — Your `dbutils` map so far (exam quick-reference)
# MAGIC
# MAGIC You have now used every `dbutils` module the associate exam cares about:
# MAGIC
# MAGIC | Call | What it does | You used it in |
# MAGIC |---|---|---|
# MAGIC | `dbutils.widgets.text/get` | Receive parameters (from a human OR a job) | Every week |
# MAGIC | `dbutils.fs.ls(path)` | List files in volumes/storage | Week 2 under-the-hood; pre-flight above |
# MAGIC | `dbutils.notebook.exit(str)` | End the notebook, surface one string as task output | Task notebooks |
# MAGIC | `dbutils.jobs.taskValues.set/get` | Pass small results BETWEEN tasks | Task notebooks (new) |
# MAGIC | `%run ./nb` *(magic, not dbutils)* | Inline another notebook into this session | Section 2b |
# MAGIC
# MAGIC That's the depth the exam expects — widget and exit/taskValues patterns that connect jobs to notebooks.

# COMMAND ----------

# MAGIC %md ## 2d — Reading a run page like the exam does
# MAGIC
# MAGIC After each of your three runs, open the run and find these — this is Domain 6 material:
# MAGIC
# MAGIC - **Statuses to recognize:** `Queued` · `Running` · `Succeeded` · `Failed` · `Skipped` · **`Upstream failed`** (the task didn't break — its dependency did).
# MAGIC - **Task output:** click a task → its `notebook.exit` string and logs. Task 2 should print `Upstream reported bronze_rows=...`.
# MAGIC - **Run history (job page):** one row per run — status, duration, trigger source. A duration *trend* across runs is diagnosed HERE, not in the Spark UI (which inspects a single run — Week 4).
# MAGIC - **Matrix view:** runs × tasks grid — spot *which task* degrades or fails repeatedly.
# MAGIC - **Repair run:** lives on the **failed run's page** (not the job page). It re-executes failed + downstream tasks only; green tasks are never recomputed.
# MAGIC
# MAGIC **Diagnostic flow to memorize:** notification → run history → matrix (which task?) → task page (error) → Spark UI (if performance).

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
# MAGIC **The two layers, one sentence each:** Git folders version the *code* (notebooks); bundles version the *pipeline definition* — tasks, dependencies, schedule, parameters — and promote it across environments. "I put my notebooks in Git" is only half of CI/CD.
# MAGIC
# MAGIC **Also recognize:** `mode: production` on a prod target (stricter deploy behavior, no dev name-prefixes) · larger projects split resources into a `resources/` folder of YAML files — the exam only needs the four top-level blocks.
# MAGIC
# MAGIC **Exam anchors:** `deploy` places, `run` executes · environments = `targets` + overrides · CI runs the same verbs as a service principal on merge.
# MAGIC
# MAGIC **Try it (2 min):** open your job → kebab menu → **View JSON**. Find `task_key`, `depends_on`, and the schedule — it's the bundle's `resources:` block wearing a different coat. Learn one, you've learned both.
