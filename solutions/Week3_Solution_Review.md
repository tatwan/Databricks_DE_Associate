# Week 3 Solution Review: Schedule It, Break It, Repair It
**Databricks Certified Data Engineer Associate · Creo Academy**

Week 3's "solution" is a correctly **wired job**, not SQL — so this covers: the target configuration, what each run should show, the quality-gate stretch, and the verification queries.
## The Job — Target Configuration

**The task:** turn your Week 2 pipeline into a scheduled, parameterized, repairable Lakeflow Job.

**Solution (built in the Jobs & Pipelines UI):**
```text
Job: brewmart_daily_<yourname>
├─ Job parameters:  target_schema = lab1_<yourname>
│                   simulate_failure = false
├─ Task 1: ingest_bronze  → notebook week3_01_ingest_bronze · serverless · retries = 2
├─ Task 2: build_silver   → notebook week3_02_build_silver · depends_on = [ingest_bronze]
├─ Task 3: quality_gate    → notebook week3_03_quality_gate · depends_on = [build_silver]  (optional stretch)
└─ Trigger: Scheduled, daily 06:00 — PAUSED
```

**Why it works:**
- **Job parameters** are pushed to every task and arrive in the notebooks as **widgets** (`dbutils.widgets.get("target_schema")`) — the same notebook serves any learner, or dev vs prod.
- **`depends_on`** is the DAG edge: the scheduler runs `build_silver` only after `ingest_bronze` succeeds. Independent tasks would run in parallel.
- **Paused schedule** = deploy-ready without surprise 6am runs — also the real-world go-live pattern.
- **Retries = 2** covers *transient* failures only. A deterministic bug fails every retry — that's what fix-then-repair is for.

**Common mistakes:**
- `target_schema` left at another learner's value → permission/not-found errors. Check the **job parameter**, not the notebook's widget default.
- Setting `simulate_failure=true` as the notebook widget default instead of the job parameter — then "repair doesn't fix it" (the job's value wins; that's the lesson).
- Looking for Repair on the *job* page — it lives on the failed **run's** page.
## The Three Runs — What Correct Looks Like

| Run | Setup | Expected result |
|---|---|---|
| 1 | defaults | Both tasks **Succeeded**. Task 1 output: `bronze_rows=23` (0 new files loaded — COPY INTO idempotency). Task 2 output: `Upstream reported bronze_rows=23` — the **task value** flowing between tasks. |
| 2 | `simulate_failure=true` | Task 1 **Failed** after 2 visible retry attempts; Task 2 **Upstream failed** (it didn't break — its dependency did). |
| 3 | set `false` → **Repair run** on run 2's page | Only `ingest_bronze` + `build_silver` re-execute; run ends **Succeeded**. Green tasks are never recomputed. |

Run history should read: **Success · Failed · Success (repaired)** — and the matrix view shows the red column on Task 1 for run 2.

**Why repair is safe here:** both tasks are idempotent (COPY INTO tracks files; `CREATE OR REPLACE` rebuilds silver from bronze). Week 2's theme is what makes Week 3's repair fearless.
## ⭐ Stretch — The Data-Quality Gate (Task 3)

**The task:** add a third task that fails the job if silver is empty — a circuit-breaker.

**Solution:** wire **`week3_03_quality_gate`** as a **notebook task**, Task key `quality_gate`, `depends_on = [build_silver]`. It receives `target_schema` as a job parameter (widget) and **fully qualifies** the table:
```python
row_count = spark.table(f"workspace.{target_schema}.sales_silver").count()
if row_count == 0:
    raise Exception("Quality gate FAILED: sales_silver is EMPTY")
```

**Why a notebook task, not a bare SQL cell?** A standalone SQL task does **not** inherit any interactive `USE SCHEMA` — the unqualified `FROM sales_silver` that works in the companion would run with no default schema and fail. The exam idea: **job tasks are isolated; pass context through parameters, not session state.** (A SQL task can work only if fully qualified, e.g. `IDENTIFIER('workspace.' || :target_schema || '.sales_silver')`.)

**Why it works:** a raised error fails the task, which fails the job and fires notifications — bad data stops the pipeline *loudly* instead of flowing downstream silently.

**File-arrival sketch (the thinking part):** replace the schedule with a **file arrival trigger** on `landing/sales_incoming/`. What changes: runs start when data lands (no empty runs, lower latency). What stays: everything else — tasks, parameters, retries, repair.

## ⭐ Bonus — The Declarative Pipeline (DLT / Lakeflow Spark Declarative Pipelines)

**The task:** reproduce bronze→silver **declaratively** with `week3_dlt_pipeline`, attached to a Lakeflow Declarative Pipeline (not the job).

**Solution (Pipelines UI):**
```text
Create → ETL pipeline
├─ Source code: week3_dlt_pipeline
├─ Default catalog: workspace · Default schema: lab1_<yourname>
├─ Configuration: target_schema = lab1_<yourname>   (read via spark.conf.get)
└─ Mode: Development → Start
```

**What correct looks like:** the pipeline graph builds `sales_bronze_dlt` → `sales_silver_dlt`; the **Data quality** tab on silver shows the `valid_order_id` (drop) and `positive_quantity` (warn) expectation counts.

**Why it works — and the exam contrast:**

| Idea | Imperative job (Tasks 1–3) | Declarative pipeline |
|---|---|---|
| Order | you set `depends_on` | inferred from `dlt.read("...")` |
| Bad rows | `ADD CONSTRAINT` = **fail the write** | `@dlt.expect` **warn** · `expect_or_drop` **drop** · `expect_or_fail` **fail** |
| Table kinds | managed Delta tables | **streaming table** (append) vs **materialized view** (recomputed) |
| Environments | job trigger paused/active | pipeline **Development** vs **Production** mode |

**One-liner:** *a constraint fails the write; an expectation applies a policy (warn/drop/fail) and records metrics.* "DLT" was renamed **Lakeflow Spark Declarative Pipelines** — the same `import dlt` code still runs.
## Verification — Prove the Job Did the Work

**Run these in your own notebook / SQL editor after the three runs:**
```sql
-- Newest version written BY THE JOB (see the job/run info in the history output)
DESCRIBE HISTORY sales_silver;

SELECT COUNT(*) AS silver_rows FROM sales_silver;
-- Expected: 22 (or 25 if your Week 2 corrections MERGE fed this bronze lineage)
```

**Why this matters:** `DESCRIBE HISTORY` showing the job as the writer is the audit-trail proof that orchestration — not a human — now runs your pipeline.
---
**Week 3 exam anchors:** parameters arrive as **widgets** · task values flow BETWEEN tasks (`taskValues.set/get`; `debugValue` interactively) · retries = transient only · **Repair run** = failed + downstream, never the green tasks · `Upstream failed` = dependency died · triggers: scheduled / file arrival / table update · `validate → deploy → run` · the four bundle blocks (`bundle`/`variables`/`resources`/`targets`) · the PR is created in the Git provider · `%run` inlines into your session; a job task runs isolated · **expectation** (warn/drop/fail + metrics) vs **constraint** (fails the write) · declarative pipeline order is inferred from `dlt.read` references · **Development** vs **Production** pipeline mode.
