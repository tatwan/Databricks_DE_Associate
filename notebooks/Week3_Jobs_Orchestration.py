# Databricks notebook source
# MAGIC %md
# MAGIC # Week 3 — Lakeflow Jobs, Orchestration, and CI/CD (Companion Notebook)
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC **How this week works (different from Weeks 1–2):** the only notebook *you* run is **this companion**. Every other notebook is run *for* you — by the job you build, or by a pipeline. Import all five, then follow the order below.
# MAGIC
# MAGIC | Order | Notebook | Who runs it | When |
# MAGIC |---|---|---|---|
# MAGIC | **1** | **This companion** (`Week3_Jobs_Orchestration`) | **You, interactively** | Pre-flight (§1) **before** you build the job |
# MAGIC | **2** | `week3_01_ingest_bronze` | **The job** | Task 1 |
# MAGIC | **3** | `week3_02_build_silver` | **The job** | Task 2 — runs **after** Task 1 (`depends_on`) |
# MAGIC | **4** | `week3_03_quality_gate` *(optional stretch)* | **The job** | Task 3 — runs **after** Task 2 |
# MAGIC | **5** | **This companion** again | **You, interactively** | Verification (§4) **after** the job's 3 runs |
# MAGIC | — | `week3_dlt_pipeline` *(bonus)* | **A pipeline**, not this job | Separate exercise — attach it in the **Pipelines UI** (§6). Never run it as a notebook. |
# MAGIC
# MAGIC You may open `week3_01`/`week3_02` and run them once just to *peek* — but their job is to be executed by the scheduler, not by you. The middle of today's lab happens in the **Jobs & Pipelines UI**, guided by the numbered steps in section 2.

# COMMAND ----------

# MAGIC %md
# MAGIC # ⚠️ STOP — read this before you run anything
# MAGIC
# MAGIC This week is different. Most of the lab is **not** in a notebook — it is in the Jobs UI. Follow this map top to bottom:
# MAGIC
# MAGIC | Step | Where | What you do |
# MAGIC |---|---|---|
# MAGIC | **A** | This notebook | Set the `user_schema` widget to **your Week 1–2 schema** (the same `lab1_yourname` you have used all course), then run the pre-flight (section 1). All checks should be ✅. |
# MAGIC | **B** | — | Do **NOT** run `week3_01` / `week3_02` / `week3_03` as your lab, and do **NOT** run `week3_dlt_pipeline` at all — the task notebooks are run *by the job*, the pipeline notebook by *a pipeline*. (Opening one to peek is fine.) |
# MAGIC | **C** | Jobs & Pipelines UI | Build the job using the numbered steps in section 2. |
# MAGIC | **D** | Jobs UI | Run it **three times**: ① success → ② `simulate_failure=true` (watch it fail) → ③ back to `false` + **Repair run**. |
# MAGIC | **E** | This notebook | Return here and run section 4 (post-run verification). |
# MAGIC
# MAGIC **If a pre-flight check is ❌:** your widget is probably not set to your real schema, or you skipped a Week 2 upload. Fix that first — an ❌ here means the job will silently write to the wrong place, not throw an error.
# MAGIC
# MAGIC > All three Week 3 notebooks default their schema widget to `lab1_yourname`. If you never changed it, **all three point at a schema that does not exist** and you will chase phantom failures. Set it now.

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
    checks[f"sales_incoming/ has file(s) ({n})"] = n >= 1   # one file is enough — the job loads whatever is there
except Exception:
    checks["sales_incoming/ has file(s)"] = False

all_green = all(checks.values())
for k, v in checks.items():
    print(("✅" if v else "❌"), k)
print("\n" + ("✅ All green — proceed to build the job (section 2)."
              if all_green else
              "❌ Fix the ❌ rows before building the job. Most common cause: the user_schema widget "
              "above is not set to your real Week 1–2 schema."))

# COMMAND ----------

# MAGIC %md ## 2 — Build the job (numbered, click-by-click in the Jobs & Pipelines UI)
# MAGIC
# MAGIC Do these in order. The **Task key must be typed exactly** as shown — Task 2 reads Task 1's output by that exact key.
# MAGIC
# MAGIC 1. Left nav → **Jobs & Pipelines** → **Create** → **Job**. Name it `brewmart_daily_<yourname>`.
# MAGIC 2. Open the job's **⋯ / Edit parameters** (or the *Job parameters* panel) and add **two job parameters**:
# MAGIC    `target_schema = <your schema>` and `simulate_failure = false`.
# MAGIC 3. **Add task 1** → type **Notebook**:
# MAGIC    - Task key: **`ingest_bronze`** (exactly)
# MAGIC    - Notebook: **Browse → select your imported `week3_01_ingest_bronze`**
# MAGIC    - Compute: **Serverless**
# MAGIC    - Retries: **2**
# MAGIC    - (Job parameters flow in automatically as the notebook's widgets — you do **not** re-enter them here.)
# MAGIC 4. **Add task 2** → type **Notebook**:
# MAGIC    - Task key: **`build_silver`** (exactly)
# MAGIC    - Notebook: **`week3_02_build_silver`**
# MAGIC    - **Depends on: `ingest_bronze`** ← this is what makes it downstream
# MAGIC 5. *(Optional stretch — section 3)* **Add task 3** → Notebook `week3_03_quality_gate`, Task key `quality_gate`, **Depends on: `build_silver`**.
# MAGIC 6. **Schedule**: add a trigger, **Scheduled — daily 06:00**, then **Pause** it (we run manually today).
# MAGIC 7. **Run now** → **run ①**. Wait for green. Open Task 2's output: find `Upstream reported bronze_rows=...`.
# MAGIC 8. Edit the `simulate_failure` job parameter to **`true`** → **Run now** → **run ②**. Task 1 **fails**; Task 2 shows **Upstream failed**.
# MAGIC 9. Set `simulate_failure` back to **`false`**. Open the **failed run's page** → **Repair run** → **run ③**. Only the failed path re-executes; the green task is not recomputed.
# MAGIC
# MAGIC ### Common gotchas
# MAGIC - **Task key typo** → Task 2's `taskValues.get(taskKey="ingest_bronze", ...)` silently returns the default instead of the real count. Type it exactly.
# MAGIC - **Forgot to import all task notebooks** → Browse can't find `week3_02`/`week3_03`. Import first.
# MAGIC - **Repair run is on the RUN page, not the job page.** If you don't see it, you're looking at the job, not the failed run.
# MAGIC - **Retries won't save run ②** — the failure is deterministic; retries only fix *transient* problems. That's the point of the demo.
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

# MAGIC %md ## 3 — ⭐ Stretch: the data-quality gate (add as Task 3 — a NOTEBOOK task, depends on build_silver)
# MAGIC
# MAGIC Wire **`week3_03_quality_gate`** as a third notebook task (Task key `quality_gate`, **Depends on `build_silver`**). It receives `target_schema` as a job parameter and **fully qualifies** the table.
# MAGIC
# MAGIC **⚠️ Why not a bare SQL task?** The SQL below works *here* only because you ran `USE SCHEMA` in section 1. A standalone **SQL job task does not inherit that** — it would run with no default schema and fail (or hit the wrong table). Interactively-safe ≠ job-safe. That gap is itself an exam idea: job tasks are isolated; pass context through parameters, not session state.
# MAGIC
# MAGIC The cell below is the same logic, **fully qualified**, if you only want to *read* it interactively:

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Interactive read only (fully qualified so it is not schema-dependent).
# MAGIC -- To run it INSIDE the job, use the week3_03_quality_gate notebook task instead.
# MAGIC SELECT CASE WHEN COUNT(*) = 0
# MAGIC             THEN raise_error('Quality gate: sales_silver is EMPTY')
# MAGIC             ELSE CONCAT('Quality gate passed: ', COUNT(*), ' rows') END AS gate
# MAGIC FROM IDENTIFIER('workspace.' || :user_schema || '.sales_silver');

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

# COMMAND ----------

# MAGIC %md ## 6 — ⭐ Optional enrichment: the same pipeline, declared
# MAGIC
# MAGIC You just built bronze→silver **imperatively** — you wrote COPY INTO, the CTAS, the task order, and the idempotency. Now see the **declarative** path: you declare tables and quality rules; the engine derives order and incrementality. This enrichment helps you recognize the pipeline task's current implementation style and tell pipeline **expectations** apart from table **constraints**.
# MAGIC
# MAGIC The source is in **`week3_dlt_pipeline`** (the filename keeps the old DLT name for continuity). Do not run it interactively — `pyspark.pipelines` and `@dp` execute inside a pipeline. Build it in the UI:
# MAGIC
# MAGIC 1. **Jobs & Pipelines** → **Create** → **ETL pipeline** (Lakeflow Declarative Pipeline).
# MAGIC 2. **Source code:** Browse → select **`week3_dlt_pipeline`**.
# MAGIC 3. **Default catalog:** `workspace` · **Default schema:** *your schema* (e.g. `lab1_yourname`).
# MAGIC 4. **Configuration** → add a key/value: **`target_schema` = *your schema*** (this is what `spark.conf.get("target_schema")` reads — the declarative cousin of a job parameter).
# MAGIC 5. Leave it in **Development** mode (faster iteration, cluster stays warm; **Production** mode tears compute down between runs and is stricter). Click **Start**.
# MAGIC 6. Watch the **pipeline graph** build `sales_bronze_dlt` → `sales_silver_dlt`. Click `sales_silver_dlt` → **Data quality** tab: see the per-expectation pass/fail counts.
# MAGIC
# MAGIC **Exam anchors:**
# MAGIC
# MAGIC | Concept | Imperative (week3_01/02) | Declarative (this pipeline) |
# MAGIC |---|---|---|
# MAGIC | Order between steps | you set `depends_on` | inferred from `spark.readStream.table("...")` references |
# MAGIC | Bad-row policy | constraint = **fail the write** | `@dp.expect` **warn** · `expect_or_drop` **drop** · `expect_or_fail` **fail** |
# MAGIC | Table kinds | managed Delta tables | **streaming table** (append) vs **materialized view** (recomputed result) |
# MAGIC | Dev vs Prod | job trigger paused/active | pipeline **Development** vs **Production** mode |
# MAGIC
# MAGIC **Current API:** `from pyspark import pipelines as dp`. Legacy `import dlt` code still runs, but current documentation uses `@dp.table`, `@dp.materialized_view`, and `@dp.expect...`. This section is enrichment; the May 4, 2026 outline does not name declarative pipelines as an objective.
