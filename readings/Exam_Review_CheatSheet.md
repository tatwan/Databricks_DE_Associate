# Final Exam Review Cheat Sheet

**Databricks Certified Data Engineer Associate — one-pass concept review**

Aligned to the **May 4, 2026** exam guide. This is the offline companion to `slides/Exam_Prep_Review.pptx`: every rule, syntax pattern, and decision keyword the quizzes and mock exams test, sequenced by the seven exam domains and weighted like the real exam (45 questions · 90 minutes).

**How to use it:** read it in domain order the night before. Flag any line that feels shaky — that domain leads your final-week plan. When a scenario has two options that both work, the exam wants the **simplest sufficient** one.

| # | Domain | Weight | Course week |
|---|--------|--------|-------------|
| 1 | Databricks Intelligence Platform | 6% | Week 1 |
| 2 | Data Ingestion & Loading | 21% | Week 2 |
| 3 | Data Transformation & Modeling | 22% | Week 2 |
| 4 | Working with Lakeflow Jobs | 16% | Week 3 |
| 5 | Implementing CI/CD | 10% | Week 3 |
| 6 | Troubleshooting, Monitoring & Optimization | 10% | Weeks 3–4 |
| 7 | Governance & Security | 15% | Week 4 |

---

## Domain 1 · Platform

- **One copy, every workload.** A single governed Delta copy serves ETL, SQL, streaming, and ML — no lake/warehouse split, no duplicates.
- **Delta is the default.** `CREATE TABLE` with no `USING` clause creates a **Delta** table. Parquet/CSV/Iceberg need explicit syntax. Delta = a *table* format built on the Parquet *file* format; the `_delta_log` adds ACID + time travel.
- **`_delta_log` = ACID.** An ordered transaction log on cloud object storage gives atomic commits and versioning — no locks, no proprietary format. Readers always see the last committed snapshot; they never block during a write.
- **Control plane vs data plane.** Control plane (Databricks-managed): workspace UI, job scheduler, Unity Catalog metastore. Data plane: **classic** compute runs in *your* cloud account; **serverless** runs in *Databricks'* account. On serverless, Spark knobs (`shuffle.partitions`…) are mostly not settable.
- **Serverless trap:** "serverless is always cheaper" is **false**. It is always *simpler / hands-off*; cost depends on the workload.
- **Unity Catalog object model:** `catalog.schema.object` — the middle element is always the **schema**. Order: metastore → catalog → schema → table/view/volume. Volumes govern non-tabular files; tables govern tabular data.
- **Managed vs external:** `LOCATION` present ⇒ external (DROP removes metadata only, files remain). No `LOCATION` ⇒ managed (DROP deletes files + metadata; recoverable with `UNDROP` in the retention window; eligible for predictive optimization).
- **CTAS** creates *and* populates; column types are **inferred**. Control a type with `CAST` inside the SELECT — you **cannot** declare `(col TYPE)` before `AS SELECT` (classic wrong answer).
- **Compute picker:** ad-hoc SQL/BI → serverless SQL warehouse · nightly unattended ETL on a budget → job compute / serverless jobs (per-run, no idle cost) · interactive multi-language dev → all-purpose cluster. Anti-pattern: an always-on all-purpose cluster for scheduled production.
- **Time travel:** `SELECT ... VERSION AS OF n` *reads* the past (changes nothing); `RESTORE TABLE ... TO VERSION AS OF n` *writes* a new version. `UNDROP TABLE` recovers a dropped managed table within retention. History older than `VACUUM` retention is gone.
- **Medallion contracts:** Bronze = raw, replayable history (keep fidelity). Silver = clean, deduplicated, typed, validated. Gold = aggregated, business-ready.

---

## Domain 2 · Ingestion

- **COPY INTO** — the idempotent SQL loader. Tracks every file it loaded (in the target's `_delta_log`) and skips them on rerun. Rerun with nothing new ⇒ **0 rows, no error, no duplicates**. Best for SQL-only teams, thousands of files, scheduled batch. `INSERT ... read_files` and `CREATE OR REPLACE TABLE` reload everything — COPY INTO loads only what's new.
- **Auto Loader** — `format("cloudFiles")`, a Structured Streaming file source. Built for **millions** of files arriving continuously.
  - **Checkpoint** records processed-file progress across runs ⇒ exactly-once, survives restarts. Delete it ⇒ reprocesses everything.
  - **schemaLocation** stores the inferred schema, remembered across runs.
  - **Tens of millions of files?** Switch discovery to **file notification mode** (event-driven) — beats directory listing on latency and cost.
- **Schema drift:** new column (`addNewColumns`, default) ⇒ stream stops **once** with a schema-change error, updates the schema, then **succeeds on restart** (deliberate stop-and-recover). Type mismatch ⇒ value captured in **`_rescued_data`**, row still ingested, never fatal.
- **`trigger(availableNow=True)`** — process everything available now, then **stop**. Streaming tech on a batch schedule; no always-on cluster.
- **Ingestion ladder (most managed → most custom):** Lakeflow Connect **managed** connectors (SaaS/DB like Salesforce, SQL Server — least engineering) → **standard** connectors (more customization, less automation) → Auto Loader / COPY INTO → JDBC/REST in a notebook (custom API + custom auth, scheduled with Lakeflow Jobs). **Start with the most managed option that supports your source.**
- **Nested data:** store natively — address → **STRUCT**, phone list → **ARRAY**. Don't flatten to 40 columns or stringify JSON at bronze. Navigate with dot syntax (`contact.city`); `explode(array_col)` fans an array into one row per element (it does **not** touch structs). Split a delimited string: `split(full_name,' ')[0]`.

### Keyword → tool

| Stem says… | Answer |
|---|---|
| "millions of files" · "evolving schema" · "near-real-time" | Auto Loader (+ file notification at extreme scale) |
| "SQL command" · "nightly batch" · "rerun must be safe" | COPY INTO |
| "Salesforce / SQL Server" · "minimal / zero engineering" | Lakeflow Connect managed connector |
| "custom REST API" · "custom auth" · "no connector" | Notebook client + Lakeflow Jobs schedule |

---

## Domain 3 · Transformation

- **MERGE INTO** — one atomic statement: updates matched rows, inserts unmatched. Rerun converges to the same state (row-level idempotency). `UPSERT INTO` does **not** exist; `APPLY CHANGES` is a declarative-pipeline construct. **Famous failure:** "a target row matched multiple source rows" ⇒ duplicate keys in the **source** ⇒ fix by **deduplicating the source** (not by changing WHEN/ON clauses).
- **Deduplication:** `dropDuplicates(["key"])` keeps *a* row per key — which one is **not** guaranteed. To keep the **latest** row per key, use a window: `ROW_NUMBER() OVER (PARTITION BY key ORDER BY ts DESC) = 1`. `SELECT DISTINCT` removes rows identical across **every** column.
- **Combining datasets:** `UNION` dedupes; `UNION ALL` keeps duplicates (cheaper). `df.union()` is **positional** — mismatched column order silently mixes data; use `unionByName` when order differs. **INNER JOIN** silently drops unmatched fact rows (totals shrink); **LEFT JOIN + COALESCE** keeps and labels them. Diagnosis: "revenue dropped after LEFT → INNER" = unmatched rows dropped.
- **Broadcast join:** small lookup + huge fact + shuffle-heavy join ⇒ broadcast the small side (hint or `autoBroadcastJoinThreshold`, ~10 MB). The big table never shuffles. *Not* the fix: raising `shuffle.partitions`, cross joins, UNION ALL splits.
- **NULL arithmetic:** NULL in ⇒ NULL out (both SQL and PySpark).
- **PySpark mirrors:** `WHERE x IS NOT NULL` → `.filter(col("x").isNotNull())` · `COALESCE(a,'X')` → `F.coalesce(col("a"), lit("X"))` · `CAST(q AS INT)` → `col("q").cast("int")` (**not** `.astype` — that's pandas) · `COUNT(DISTINCT id)` → `F.count_distinct("id")`.
- **Gold objects:** reusable, always-current logic → **standard view** (recomputes each read) · expensive aggregate read constantly, ≤1 h staleness OK → **materialized view** (precomputed, scheduled refresh) · append-only ingestion → **streaming table** · distinct count over a billion rows, exactness not required → **`approx_count_distinct`** (HyperLogLog). Named aggregations to know: `count`, `approx_count_distinct`, `mean`, `summary`.
- **Data quality:** a **CHECK constraint** is all-or-nothing — one bad row fails the **whole** write (no skipping, no NULL coercion). A **quarantine split** routes valid rows to silver and invalid rows to a quarantine table — the load keeps flowing and bad rows stay visible. Declarative-pipeline **expectations** are per-run policies: `expect` (warn, keep) · `expect_or_drop` (drop + metrics) · `expect_or_fail` (stop). "Must not stop the load but keep bad rows visible" ⇒ **quarantine**.

---

## Domain 4 · Lakeflow Jobs

- **Job → tasks → DAG.** `depends_on` is the arrow; a task runs only after its dependencies succeed. Tasks with **no edge** between them run in **parallel** automatically.
- **Task types to know:** notebook · SQL · dashboard · pipeline (runs a declarative pipeline in the DAG). Also recognize: run-job (job calls job), if/else, for-each.
- **Control flow:** **retries** fix *transient* failures only (flaky API) — a deterministic bug fails every retry ⇒ **fix the code, then Repair run**. **Run-if "All done"** = a finalizer that runs whether dependencies succeeded or failed (the always-send-the-status-email pattern). **If/else** branches on a boolean ("full rebuild on the 1st, else incremental"). **For-each** loops one task over a list with a concurrency limit ("14 regions, 4 at a time") — not 14 copied tasks.
- **Triggers:** nightly at 02:00 → **scheduled (cron)** · files land at unpredictable times → **file arrival** (ends empty polling runs) · a monitored Delta table gets new commits → **table update** · always-on → **continuous** · configured but must not run yet → **Paused**. Choose **time-based** for clock SLAs, **data-driven** for availability.
- **Passing values:** job parameter → notebook task arrives as a **widget** (`dbutils.widgets.get("env")`). Task A → Task B runtime value = **task values** (`dbutils.jobs.taskValues.set/.get`). Reuse helper functions in one session = `%run` (shares the session; a job task runs isolated).
- **Repair run** re-executes the failed task **and its downstream only** — already-green tasks are never recomputed.
- **Monitoring:** duration creeping up across weeks ⇒ the **run history matrix** (per-task durations across runs) is the first evidence. Deep dive into one run ⇒ the **Spark UI**. "Upstream failed" = the downstream task was **skipped** because its dependency failed.
- **Serverless jobs:** hands-off, auto-optimized, billed per run — the exam rewards the "Databricks manages sizing" property.

---

## Domain 5 · CI/CD

- **Git folders boundary:** inside the Databricks workspace you **branch, commit, push, pull**. The **pull request is created, reviewed, and merged in the Git provider** (GitHub/GitLab/DevOps) — not in Databricks.
- **Declarative Automation Bundles** (formerly Asset Bundles) package jobs, pipelines, and config as code in `databricks.yml`. Four blocks to recognize: `bundle` (name) · `variables` (config knobs) · `resources` (the jobs) · `targets` (environments).
- **Environments = targets.** dev vs prod differ **only by per-target variable overrides** on one shared codebase — never a separate YAML or duplicated notebooks. **Promotion = changing `-t`, never editing code.**
- **CLI order (memorize): `validate` → `deploy` → `run`.** `validate` checks syntax/references (changes nothing); `deploy -t dev` places resources in the target; `run -t dev job` executes the deployed job.
- **The CI sentence:** on every merge to main, CI runs `databricks bundle deploy -t prod` authenticated as a **service principal** — nobody clicks Deploy. Any answer that swaps deploy/run, or puts the PR in the workspace UI, is wrong.
- **Old-name bait:** Workflows → Lakeflow Jobs · Asset Bundles/DABs → Declarative Automation Bundles · Repos → Git folders.

---

## Domain 6 · Troubleshooting, Monitoring & Optimization

- **OPTIMIZE** compacts many small files into fewer larger ones (faster reads). **VACUUM** deletes old files no longer referenced by the log — and **time travel to versions older than the retention window stops working**. Swapped pairing ("OPTIMIZE deletes, VACUUM compacts") is the standard wrong answer.
- **Predictive optimization** runs `OPTIMIZE` / `VACUUM` / `ANALYZE` automatically — for **Unity Catalog managed tables only**. It is not a query tuner and does not cover external tables.
- **Liquid Clustering:** `CREATE TABLE ... CLUSTER BY (col)`; re-key later with `ALTER TABLE ... CLUSTER BY (new_cols)` — the new layout applies **incrementally, no full rewrite**. Versus legacy: changing `PARTITIONED BY` rebuilds the table; `ZORDER` re-runs OPTIMIZE over history.
- **Spark UI signatures:** **skew** = max task time ≫ median ("median 30 s, max 28 min"); first lever = broadcast the small side / AQE / rethink the key. **Spill** = large `Spill (Memory)`/`Spill (Disk)`; lever = more/smaller partitions or more memory. **Heavy shuffle** = big Shuffle Read/Write on a wide op; lever = broadcast, prune/filter early.
- **Failure triage:** *before any task* (init-script error, cluster start) ⇒ infrastructure. `ModuleNotFoundError` after a compute switch ⇒ **library not installed on this cluster**. `collect()`/`toPandas()` on a huge DataFrame kills the session while executors are healthy ⇒ **driver OOM** (real fix: don't collect).
- **Tuning knobs (know what they influence):** `spark.sql.shuffle.partitions` (partitions after a wide op) · `spark.default.parallelism` · `spark.executor/driver.memory` (spill/OOM) · `spark.sql.autoBroadcastJoinThreshold` (~10 MB). On **serverless** you mostly can't set these — Databricks manages them.
- **Reading order:** longest stage first → task-duration distribution → I/O and spill counters. Trend across runs ⇒ run history; depth within one run ⇒ Spark UI.

---

## Domain 7 · Governance & Security

- **Read chain — all three or no access:** `USE CATALOG` (catalog) + `USE SCHEMA` (schema) + `SELECT` (table or schema). Symptom "has SELECT but still gets a permission error" ⇒ missing `USE CATALOG` / `USE SCHEMA`. Grant `SELECT` at the **schema** to cover current *and* future tables (per-table misses tomorrow's tables; `ALL PRIVILEGES` over-grants).
- **REVOKE vs DENY:** `REVOKE` removes one specific grant (other paths survive). The May 2026 guide *names* `DENY`, but current Unity Catalog behavior is that **DENY is unsupported on UC objects** (legacy `hive_metastore` only) — know both framings.
- **Principals:** users, groups, service principals. **Grant to groups** (scales, survives turnover — the exam's best-practice answer). A production job / CI pipeline authenticates as a **service principal**, never a named person. Tables/catalogs/functions are *securables*, not principals.
- **Masks & filters (two steps: create a function, then bind it):** column **mask** rewrites a column's value per user (`ALTER TABLE ... ALTER COLUMN ... SET MASK`); **row filter** decides row visibility (`ALTER TABLE ... SET ROW FILTER`). Applied **query-time on every path** — storage untouched. **Owners are not exempt**: a table owner outside the allowed group sees masked values like everyone else.
- **ABAC:** tag a column once (e.g., `pii_email`); one tag-driven policy masks every tagged column across thousands of tables, current and future — no per-table edits. "Thousands of tables, central team, no extra copies" ⇒ ABAC.
- **Managed ↔ external operations:** create, modify, delete, and **convert**. External → managed: `ALTER TABLE catalog.schema.table SET MANAGED` (Databricks takes over the files/lifecycle; table keeps its name, grants, history). `UNDROP TABLE` recovers a dropped managed table within retention.
- **Lineage** is automatic — Catalog Explorer → table → **Lineage tab**; no scanner to install. **Audit logs** are queryable via system tables (`system.access.audit`).
- **Awareness only (removed from / not core to the May 2026 exam):** Delta Sharing (zero-copy live sharing — D2D vs open protocol) and Lakehouse Federation (query external DBs through UC, no ingestion). Treat as distractors, not keyed answers.

---

## The eight course-wide traps

1. **DROP semantics swapped** — managed deletes data; external leaves files.
2. **CTAS with a type list** — invented syntax; `CAST` in the SELECT instead.
3. **"COPY INTO reruns duplicate"** — false, it's file-tracked. (`df.union()` dedupes is also false.)
4. **"Repair reruns everything"** — failed + downstream only.
5. **deploy = run / PR in the workspace** — deploy places, run executes; the PR lives in the provider.
6. **DENY on Unity Catalog** — unsupported on UC objects (legacy only). Owners still aren't mask-exempt.
7. **VACUUM for speed** — OPTIMIZE compacts for speed; VACUUM trims storage and limits time travel.
8. **Most powerful ≠ best** — pick the simplest tool that satisfies every stated constraint.

## Exam-day plan

- 45 questions · 90 minutes ≈ **2 minutes each**. Three passes: fast → flagged → sweep. **No penalty for guessing — answer everything.**
- Kill order for distractors: invented syntax → real-feature-wrong-job → violates a stated constraint → winner.
- Score the mock **per domain**; your weakest domain decides what you re-read, not your total.

---

*Companion to `slides/Exam_Prep_Review.pptx`. Verify product names and the DENY / `SET MANAGED` behaviors against the current Databricks docs before your exam — these are the details most likely to drift.*
