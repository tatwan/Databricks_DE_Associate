# Databricks notebook source
# MAGIC %md
# MAGIC # Week 3 — Lab Solutions (Study Copy)
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC Markdown only — nothing runs. Week 3's "solution" is a correctly **wired job**, not SQL — so this covers: the target configuration, what each run should show, the quality-gate stretch, and the verification queries.

# COMMAND ----------

# MAGIC %md
# MAGIC ## The Job — Target Configuration
# MAGIC
# MAGIC **The task:** turn your Week 2 pipeline into a scheduled, parameterized, repairable Lakeflow Job.
# MAGIC
# MAGIC **Solution (built in the Jobs & Pipelines UI):**
# MAGIC ```text
# MAGIC Job: brewmart_daily_<yourname>
# MAGIC ├─ Job parameters:  target_schema = lab1_<yourname>
# MAGIC │                   simulate_failure = false
# MAGIC ├─ Task 1: ingest_bronze  → notebook week3_01_ingest_bronze · serverless · retries = 2
# MAGIC ├─ Task 2: build_silver   → notebook week3_02_build_silver · depends_on = [ingest_bronze]
# MAGIC ├─ Task 3: quality_gate    → notebook week3_03_quality_gate · depends_on = [build_silver]  (optional stretch)
# MAGIC └─ Trigger: Scheduled, daily 06:00 — PAUSED
# MAGIC ```
# MAGIC
# MAGIC **Why it works:**
# MAGIC - **Job parameters** are pushed to every task and arrive in the notebooks as **widgets** (`dbutils.widgets.get("target_schema")`) — the same notebook serves any learner, or dev vs prod.
# MAGIC - **`depends_on`** is the DAG edge: the scheduler runs `build_silver` only after `ingest_bronze` succeeds. Independent tasks would run in parallel.
# MAGIC - **Paused schedule** = deploy-ready without surprise 6am runs — also the real-world go-live pattern.
# MAGIC - **Retries = 2** covers *transient* failures only. A deterministic bug fails every retry — that's what fix-then-repair is for.
# MAGIC
# MAGIC **Common mistakes:**
# MAGIC - `target_schema` left at another learner's value → permission/not-found errors. Check the **job parameter**, not the notebook's widget default.
# MAGIC - Setting `simulate_failure=true` as the notebook widget default instead of the job parameter — then "repair doesn't fix it" (the job's value wins; that's the lesson).
# MAGIC - Looking for Repair on the *job* page — it lives on the failed **run's** page.

# COMMAND ----------

# MAGIC %md
# MAGIC ## The Three Runs — What Correct Looks Like
# MAGIC
# MAGIC | Run | Setup | Expected result |
# MAGIC |---|---|---|
# MAGIC | 1 | defaults | Both tasks **Succeeded**. Task 1 output: `bronze_rows=23` (0 new files loaded — COPY INTO idempotency). Task 2 output: `Upstream reported bronze_rows=23` — the **task value** flowing between tasks. |
# MAGIC | 2 | `simulate_failure=true` | Task 1 **Failed** after 2 visible retry attempts; Task 2 **Upstream failed** (it didn't break — its dependency did). |
# MAGIC | 3 | set `false` → **Repair run** on run 2's page | Only `ingest_bronze` + `build_silver` re-execute; run ends **Succeeded**. Green tasks are never recomputed. |
# MAGIC
# MAGIC Run history should read: **Success · Failed · Success (repaired)** — and the matrix view shows the red column on Task 1 for run 2.
# MAGIC
# MAGIC **Why repair is safe here:** both tasks are idempotent (COPY INTO tracks files; `CREATE OR REPLACE` rebuilds silver from bronze). Week 2's theme is what makes Week 3's repair fearless.

# COMMAND ----------

# MAGIC %md
# MAGIC ## ⭐ Stretch — The Data-Quality Gate (Task 3)
# MAGIC
# MAGIC **The task:** add a third task that fails the job if silver is empty — a circuit-breaker.
# MAGIC
# MAGIC **Solution:** wire **`week3_03_quality_gate`** as a **notebook task**, Task key `quality_gate`, `depends_on = [build_silver]`. It receives `target_schema` as a job parameter (widget) and **fully qualifies** the table:
# MAGIC ```python
# MAGIC row_count = spark.table(f"workspace.{target_schema}.sales_silver").count()
# MAGIC if row_count == 0:
# MAGIC     raise Exception("Quality gate FAILED: sales_silver is EMPTY")
# MAGIC ```
# MAGIC
# MAGIC **Why a notebook task and not a bare SQL cell?** A standalone SQL task does **not** inherit any interactive `USE SCHEMA`. The unqualified `FROM sales_silver` that works in the companion notebook would run with **no default schema** as a job task and fail (or hit the wrong table). The exam idea: **job tasks are isolated — pass context through parameters, not session state.** (If you *do* want a SQL task, you must fully qualify with the job parameter, e.g. `IDENTIFIER('workspace.' || :target_schema || '.sales_silver')`.)
# MAGIC
# MAGIC **Why it works:** a raised error fails the task, which fails the job and fires notifications — bad data stops the pipeline *loudly* instead of flowing downstream silently.
# MAGIC
# MAGIC **File-arrival sketch (the thinking part):** replace the schedule with a **file arrival trigger** on `landing/sales_incoming/`. What changes: runs start when data lands (no empty runs, lower latency). What stays: everything else — tasks, parameters, retries, repair.

# COMMAND ----------

# MAGIC %md
# MAGIC ## ⭐ Bonus — The Declarative Pipeline (DLT / Lakeflow Spark Declarative Pipelines)
# MAGIC
# MAGIC **The task:** reproduce bronze→silver **declaratively** using `week3_dlt_pipeline`, attached to a Lakeflow Declarative Pipeline (not the job).
# MAGIC
# MAGIC **Solution (in the Pipelines UI):**
# MAGIC ```text
# MAGIC Create → ETL pipeline
# MAGIC ├─ Source code: week3_dlt_pipeline
# MAGIC ├─ Default catalog: workspace · Default schema: lab1_<yourname>
# MAGIC ├─ Configuration: target_schema = lab1_<yourname>   (read via spark.conf.get)
# MAGIC └─ Mode: Development → Start
# MAGIC ```
# MAGIC
# MAGIC **What correct looks like:** the pipeline graph builds `sales_bronze_dlt` → `sales_silver_dlt`; the **Data quality** tab on silver shows the `valid_order_id` (drop) and `positive_quantity` (warn) expectation counts.
# MAGIC
# MAGIC **Why it works — and the exam contrast:**
# MAGIC
# MAGIC | Idea | Imperative job (Tasks 1–3) | Declarative pipeline |
# MAGIC |---|---|---|
# MAGIC | Order | you set `depends_on` | inferred from `dlt.read("...")` |
# MAGIC | Bad rows | `ADD CONSTRAINT` = **fail the write** | `@dlt.expect` **warn** · `expect_or_drop` **drop** · `expect_or_fail` **fail** |
# MAGIC | Table kinds | managed Delta tables | **streaming table** (append) vs **materialized view** (recomputed) |
# MAGIC | Environments | job trigger paused/active | pipeline **Development** vs **Production** mode |
# MAGIC
# MAGIC **One-liner to memorize:** *a constraint fails the write; an expectation applies a policy (warn/drop/fail) and records metrics.* "DLT" was renamed **Lakeflow Spark Declarative Pipelines** — the same `import dlt` code still runs.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verification — Prove the Job Did the Work
# MAGIC
# MAGIC **Run these in your own notebook / SQL editor after the three runs:**
# MAGIC ```sql
# MAGIC -- Newest version written BY THE JOB (see the job/run info in the history output)
# MAGIC DESCRIBE HISTORY sales_silver;
# MAGIC
# MAGIC SELECT COUNT(*) AS silver_rows FROM sales_silver;
# MAGIC -- Expected: 22 (or 25 if your Week 2 corrections MERGE fed this bronze lineage)
# MAGIC ```
# MAGIC
# MAGIC **Why this matters:** `DESCRIBE HISTORY` showing the job as the writer is the audit-trail proof that orchestration — not a human — now runs your pipeline.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC **Week 3 exam anchors:** parameters arrive as **widgets** · task values flow BETWEEN tasks (`taskValues.set/get`; `debugValue` interactively) · retries = transient only · **Repair run** = failed + downstream, never the green tasks · `Upstream failed` = dependency died · triggers: scheduled / file arrival / table update · `validate → deploy → run` · the four bundle blocks (`bundle`/`variables`/`resources`/`targets`) · the PR is created in the Git provider · `%run` inlines into your session; a job task runs isolated · **expectation** (warn/drop/fail + metrics) vs **constraint** (fails the write) · declarative pipeline order is inferred from `dlt.read` references · **Development** vs **Production** pipeline mode.
