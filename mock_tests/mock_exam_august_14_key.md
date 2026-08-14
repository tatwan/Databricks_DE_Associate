#  Databricks Certified Data Engineer Associate — August Mock Exam Answer Key & Deep Explanations

**Exam Blueprint Version:** May 4, 2026  
**Total Questions:** 45 Scored Multiple-Choice Items  
**Time Limit:** 90 Minutes  
**Passing Standard:** ~70% (32/45 correct)  

---

## Domain & Topic Weight Distribution

| Section | Domain Name | Exam Weight | Q Count | Question Range | Course Week Focus |
|---|---|:---:|:---:|:---:|:---:|
| **Domain 1** | Databricks Intelligence Platform | ~6% | 3 | Q1 – Q3 | Week 1 |
| **Domain 2** | Data Ingestion & Loading | ~21% | 9 | Q4 – Q12 | Week 2 |
| **Domain 3** | Data Transformation & Modeling | ~22% | 10 | Q13 – Q22 | Week 2 |
| **Domain 4** | Working with Lakeflow Jobs | ~16% | 7 | Q23 – Q29 | Week 3 |
| **Domain 5** | Implementing CI/CD | ~10% | 4 | Q30 – Q33 | Week 3 |
| **Domain 6** | Troubleshooting, Monitoring & Optimization | ~10% | 5 | Q34 – Q38 | Weeks 3–4 |
| **Domain 7** | Governance & Security | ~15% | 7 | Q39 – Q45 | Week 4 |
| **Total** | **All Domains** | **100%** | **45** | **Q1 – Q45** | **Weeks 1–5** |

---

# Section: Domain 1 — Databricks Intelligence Platform

### Q1: Primary Architecture Advantage of the Lakehouse
- **Correct Answer:** **B** — *One governed Delta Lake copy serves BI, streaming, ML, and batch ETL*
- **Exam Mapping:** Domain 1 (Databricks Intelligence Platform) · **Week 1** (`slides/Week1_Lakehouse_Foundations.pptx`, `readings/Week1_Lakehouse_Foundations.md`, `readings/Exam_Review_CheatSheet.md`)
- **Why It's Correct:** The core thesis of the Lakehouse is "one copy, every workload." By adding an ACID transaction layer (Delta Lake) and unified governance (Unity Catalog) on top of open object storage, organizations eliminate copying data into proprietary data warehouses.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Delta Lake does not replace object storage with proprietary formats; it uses open Apache Parquet files and a JSON `_delta_log`.
  - **C is incorrect:** The control plane handles metadata/UI; queries execute in the data plane (compute).
  - **D is incorrect:** The Lakehouse enforces schemas and data types across silver and gold tables.

---

### Q2: Control Plane vs Data Plane Architecture
- **Correct Answer:** **A** — *Unity Catalog metastore, Web UI, and Job orchestration scheduler*
- **Exam Mapping:** Domain 1 (Databricks Intelligence Platform) · **Week 1** (`readings/Week1_Lakehouse_Foundations.md`, `notebooks/Week1_Lakehouse_Fundamentals.py`)
- **Why It's Correct:** The control plane consists of services managed by Databricks in its own cloud account, including the workspace UI, notebook management, cluster manager, job scheduler, and the Unity Catalog central metastore.
- **Distractor & Trap Analysis:**
  - **B is incorrect:** Spark driver and worker nodes run in the data plane.
  - **C is incorrect:** Cloud storage holding Parquet files resides in the customer's cloud storage.
  - **D is incorrect:** Customer VPC/VNet subnets host the customer-managed classic data plane.

---

### Q3: Delta Lake ACID Guarantees & Transaction Log
- **Correct Answer:** **C** — *Readers query the latest committed snapshot recorded in the `_delta_log`*
- **Exam Mapping:** Domain 1 (Databricks Intelligence Platform) · **Week 1** (`readings/Week1_Lakehouse_Foundations.md`, `notebooks/Week1_Lakehouse_Fundamentals.py`)
- **Why It's Correct:** Delta Lake achieves ACID compliance via an ordered JSON transaction log (`_delta_log`). Readers query the latest committed table snapshot from the log and ignore uncommitted Parquet files, eliminating table-level locking.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Cloud storage does not support POSIX table locks. Delta uses optimistic concurrency control (OCC).
  - **B is incorrect:** Delta tables can be petabytes in size; caching tables in driver RAM is impossible.
  - **D is incorrect:** Delta Lake writes only modified Parquet files, not full table directory duplicates.

---

# Section: Domain 2 — Data Ingestion & Loading

### Q4: COPY INTO Idempotency
- **Correct Answer:** **D** — *Loads 0 rows and succeeds because it tracks loaded files in the log*
- **Exam Mapping:** Domain 2 (Data Ingestion & Loading) · **Week 2** (`notebooks/Week2_Ingestion_Transformations.py`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** `COPY INTO` tracks processed files in the target table's transaction log. When rerun on an unchanged source directory, it safely loads 0 rows, raises no error, and produces no duplicates.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** `COPY INTO` does not throw an exception when no new files are found.
  - **B is incorrect:** Unlike `INSERT INTO ... read_files()`, `COPY INTO` does not double-load existing files.
  - **C is incorrect:** `COPY INTO` appends new data; it never truncates or overwrites existing table history.

---

### Q5: Auto Loader Streaming Format
- **Correct Answer:** **A** — *`.format("cloudFiles")`*
- **Exam Mapping:** Domain 2 (Data Ingestion & Loading) · **Week 2** (`notebooks/Week2_Ingestion_Transformations.py`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** Auto Loader is invoked using the Structured Streaming format `"cloudFiles"`. The underlying file format is passed via `.option("cloudFiles.format", "json")`.
- **Distractor & Trap Analysis:**
  - **B is incorrect:** `"autoLoader"` is not a valid Spark option.
  - **C is incorrect:** `"cloudFiles.mode"` is not a recognized configuration.
  - **D is incorrect:** `"deltaStream"` is an invented format name.

---

### Q6: Auto Loader File Discovery at Scale
- **Correct Answer:** **B** — *Set `cloudFiles.useNotifications` to `true` (file notification mode)*
- **Exam Mapping:** Domain 2 (Data Ingestion & Loading) · **Week 2** (`readings/Week2_Ingestion_Transformations.md`, `readings/Exam_Review_CheatSheet.md`)
- **Why It's Correct:** For containers with millions of files, directory listing becomes slow and expensive. Setting `cloudFiles.useNotifications = true` configures event-driven ingestion using cloud messaging services (AWS SNS/SQS, Azure Event Grid, GCP Pub/Sub).
- **Distractor & Trap Analysis:**
  - **A is incorrect:** `spark.sql.shuffle.partitions` controls shuffle partitions, not cloud file discovery.
  - **C is incorrect:** `COPY INTO` relies on directory listing and is slower than Auto Loader at scale.
  - **D is incorrect:** `rescue` is a schema evolution mode (`_rescued_data`), not a file discovery setting.

---

### Q7: Auto Loader Schema Evolution
- **Correct Answer:** **C** — *Throws a schema change exception, updates the schema, and succeeds on restart*
- **Exam Mapping:** Domain 2 (Data Ingestion & Loading) · **Week 2** (`notebooks/Week2_Ingestion_Transformations.py`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** With `addNewColumns` (default), discovering a new column causes the stream to deliberately stop once with an `UnknownFieldException`, update the schema in `cloudFiles.schemaLocation`, and ingest the new column upon restart.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** The stream does not silently discard newly added columns.
  - **B is incorrect:** Deleting checkpoints causes full reprocessing and is never required.
  - **D is incorrect:** New columns evolve the schema; they are not routed to dead-letter queues.

---

### Q8: Data Rescue Mechanism (`_rescued_data`)
- **Correct Answer:** **D** — *Sets the column to `NULL` and captures `"N/A"` in `_rescued_data`*
- **Exam Mapping:** Domain 2 (Data Ingestion & Loading) · **Week 2** (`notebooks/Week2_Ingestion_Transformations.py`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** When a data type mismatch occurs (e.g. text `"N/A"` in a `DOUBLE` column), Auto Loader sets the target column to `NULL` and saves the original unparsed string in `_rescued_data`, preventing pipeline failures.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Default Auto Loader settings prevent batch aborts on type mismatch.
  - **B is incorrect:** Corrupted strings are not coerced to `0.0`.
  - **C is incorrect:** Corrupted rows are preserved with rescued data rather than dropped.

---

### Q9: `availableNow=True` Trigger
- **Correct Answer:** **C** — *`.trigger(availableNow=True)`*
- **Exam Mapping:** Domain 2 (Data Ingestion & Loading) · **Week 2** (`readings/Week2_Ingestion_Transformations.md`, `readings/Exam_Review_CheatSheet.md`)
- **Why It's Correct:** `.trigger(availableNow=True)` processes all available files across micro-batches and then shuts down the stream, allowing streaming pipelines to run economically on batch schedules.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** `.trigger(once=True)` is legacy and processes only a single micro-batch.
  - **B is incorrect:** `processingTime` keeps clusters running 24/7.
  - **D is incorrect:** Continuous triggers are for sub-second streaming on always-on compute.

---

### Q10: Lakeflow Connect Managed Connectors
- **Correct Answer:** **A** — *Lakeflow Connect managed connectors*
- **Exam Mapping:** Domain 2 (Data Ingestion & Loading) · **Week 2** (`slides/Week2_Ingestion_Transformations.pptx`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** For supported SaaS and databases (Salesforce, SQL Server, Postgres), Lakeflow Connect managed connectors provide turnkey CDC, automated schema replication, and serverless ingestion with zero custom code.
- **Distractor & Trap Analysis:**
  - **B is incorrect:** Custom JDBC scripts require manual watermarking and ongoing maintenance.
  - **C is incorrect:** CSV dumps require custom export pipelines.
  - **D is incorrect:** Lakehouse Federation is for federated live queries, not bulk ingestion.

---

### Q11: Nested JSON Transformation (Struct vs Array)
- **Correct Answer:** **A** — *`SELECT contact.city, explode(phones) FROM events_bronze;`*
- **Exam Mapping:** Domain 2 (Data Ingestion & Loading) · **Week 2** (`notebooks/Week2_Ingestion_Transformations.py`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** In Spark SQL, `STRUCT` fields are accessed using dot-notation (`contact.city`), while `ARRAY` elements are unnested into individual rows using `explode(phones)`.
- **Distractor & Trap Analysis:**
  - **B is incorrect:** `explode()` cannot be called on a `STRUCT`.
  - **C is incorrect:** `unwrap()` is not a valid Spark SQL array unnesting function.
  - **D is incorrect:** `split()` is for delimited strings, not struct objects.

---

### Q12: Custom REST API Ingestion
- **Correct Answer:** **D** — *Write the API client in a Python notebook and orchestrate with Lakeflow Jobs*
- **Exam Mapping:** Domain 2 (Data Ingestion & Loading) · **Week 2** (`readings/Week2_Ingestion_Transformations.md`, `readings/Exam_Review_CheatSheet.md`)
- **Why It's Correct:** For internal APIs with custom OAuth2 headers and pagination where no native connector exists, the recommended approach is a Python notebook using `requests` scheduled via Lakeflow Jobs.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Auto Loader reads cloud files, not REST endpoints.
  - **B is incorrect:** `COPY INTO` does not have a `REST_AUTH` option.
  - **C is incorrect:** Lakehouse Federation connects to databases, not arbitrary HTTPS endpoints.

---

# Section: Domain 3 — Data Transformation & Modeling

### Q13: MERGE INTO Statement
- **Correct Answer:** **B** — *`MERGE INTO silver USING stg ON silver.id = stg.id WHEN MATCHED THEN UPDATE...`*
- **Exam Mapping:** Domain 3 (Data Transformation & Modeling) · **Week 2** (`notebooks/Week2_Ingestion_Transformations.py`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** Standard ANSI SQL `MERGE INTO` is the atomic statement in Delta Lake for upserts (`WHEN MATCHED THEN UPDATE` / `WHEN NOT MATCHED THEN INSERT`).
- **Distractor & Trap Analysis:**
  - **A is incorrect:** `UPSERT INTO` does not exist in ANSI SQL or Databricks SQL.
  - **C is incorrect:** `INSERT OVERWRITE` replaces the whole target table.
  - **D is incorrect:** `APPLY CHANGES INTO` is a declarative pipeline construct (DLT), not standalone Delta SQL.

---

### Q14: MERGE Multiple Matches Error Fix
- **Correct Answer:** **C** — *Deduplicate the source dataset on the merge key before running MERGE*
- **Exam Mapping:** Domain 3 (Data Transformation & Modeling) · **Week 2** (`notebooks/Week2_Ingestion_Transformations.py`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** Delta Lake `MERGE` fails if a single target row matches multiple source rows. The only valid fix is deduplicating the source dataset before merging.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Primary keys in Unity Catalog are informational and do not fix source duplicate rows.
  - **B is incorrect:** Altering the join condition alters business logic and does not resolve source duplicates.
  - **D is incorrect:** The issue is source ambiguity, not cluster isolation levels.

---

### Q15: Deduplication to Retain Latest Record
- **Correct Answer:** **D** — *Window function: `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1`*
- **Exam Mapping:** Domain 3 (Data Transformation & Modeling) · **Week 2** (`notebooks/Week2_Ingestion_Transformations.py`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** Partitioning by `customer_id` and ordering by timestamp descending with `ROW_NUMBER()` guarantees that filtering on rank `1` deterministically retains the latest record.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** `df.dropDuplicates(["customer_id"])` keeps an arbitrary row non-deterministically.
  - **B is incorrect:** `SELECT DISTINCT` only removes rows that are identical across every column.
  - **C is incorrect:** `GROUP BY` with `MAX()` cannot return non-aggregated attribute columns without an extra join.

---

### Q16: PySpark DataFrame Positional `union()`
- **Correct Answer:** **A** — *Data is combined positionally, placing `region` values into the `id` column*
- **Exam Mapping:** Domain 3 (Data Transformation & Modeling) · **Week 2** (`notebooks/Week2_Ingestion_Transformations.py`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** In PySpark, `df.union()` aligns columns strictly by position (1st to 1st, 2nd to 2nd). When column orders differ, data is placed into wrong columns silently. Use `unionByName()` to match by name.
- **Distractor & Trap Analysis:**
  - **B is incorrect:** `union()` is positional; only `unionByName()` matches by column name.
  - **C is incorrect:** Compatible types will not raise a schema mismatch exception; they corrupt data silently.
  - **D is incorrect:** `union()` does not perform automatic casting or deduplication.

---

### Q17: Broadcast Join Optimization
- **Correct Answer:** **B** — *Broadcast the 15 MB dimension table (`/*+ BROADCAST */` or `broadcast()`)*
- **Exam Mapping:** Domain 3 (Data Transformation & Modeling) · **Week 2** (`slides/Week2_Ingestion_Transformations.pptx`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** Broadcasting the 15 MB lookup table sends a copy to every executor RAM space, allowing local joins without shuffling the 50 TB fact table across the network.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Increasing shuffle partitions does not eliminate the network shuffle.
  - **C is incorrect:** Repartitioning 50 TB into 10 partitions creates giant 5 TB partitions that will crash executors.
  - **D is incorrect:** `CROSS JOIN` computes a Cartesian product, severely worsening performance.

---

### Q18: INNER vs LEFT JOIN Missing Rows
- **Correct Answer:** **C** — *Sales records with store IDs that did not match the store dimension were dropped*
- **Exam Mapping:** Domain 3 (Data Transformation & Modeling) · **Week 2** (`notebooks/Week2_Ingestion_Transformations.py`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** `INNER JOIN` excludes any left-table rows that do not match the right table. Unmatched store IDs in the fact table were discarded, reducing total aggregated revenue.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** `INNER JOIN` does not change `SUM()` to `AVG()`.
  - **B is incorrect:** `INNER JOIN` does not deduplicate fact transactions.
  - **D is incorrect:** `LEFT JOIN` does not duplicate rows when NULLs are present.

---

### Q19: Quarantine Pattern vs Constraints
- **Correct Answer:** **B** — *Quarantine split: route valid rows to silver, bad rows to a quarantine table*
- **Exam Mapping:** Domain 3 (Data Transformation & Modeling) · **Week 2** (`notebooks/Week2_Ingestion_Transformations.py`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** A quarantine split writes clean rows to silver and bad rows to a quarantine table. This keeps the automated pipeline running while preserving bad records for investigation.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** A `CHECK` constraint fails the entire write transaction when any row violates the rule.
  - **C is incorrect:** Spark does not automatically convert negative numbers to NULL.
  - **D is incorrect:** `VACUUM` cleans up obsolete files; it is not a row-level data quality filter.

---

### Q20: Materialized Views in Gold Layer
- **Correct Answer:** **C** — *A Materialized View (`CREATE MATERIALIZED VIEW`) refreshed hourly*
- **Exam Mapping:** Domain 3 (Data Transformation & Modeling) · **Week 2** (`readings/Week2_Ingestion_Transformations.md`, `readings/Exam_Review_CheatSheet.md`)
- **Why It's Correct:** Materialized Views precompute and persist aggregated results on disk and refresh on a defined schedule, eliminating the heavy cost of recalculating 500M rows on every dashboard view.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Standard views re-execute the full aggregation query on every user access.
  - **B is incorrect:** Temporary views exist only in the current user session.
  - **D is incorrect:** Manually rewriting tables every 5 minutes from notebooks wastes compute.

---

### Q21: `approx_count_distinct` for Fast Metrics
- **Correct Answer:** **C** — *`approx_count_distinct(user_id)`*
- **Exam Mapping:** Domain 3 (Data Transformation & Modeling) · **Week 2** (`slides/Week2_Ingestion_Transformations.pptx`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** `approx_count_distinct()` uses HyperLogLog to estimate distinct values with ~1-5% error in seconds over billions of rows, avoiding the expensive global shuffle of `COUNT(DISTINCT)`.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** `COUNT(DISTINCT)` requires a full network shuffle and exact hash aggregation, failing the 3-second SLA.
  - **B is incorrect:** `DENSE_RANK()` calculates window rankings for each row, not an aggregate count.
  - **D is incorrect:** `summary()` calculates descriptive distribution statistics (mean, stddev, min, max).

---

### Q22: String Splitting in PySpark
- **Correct Answer:** **A** — *`df.withColumn("first_name", F.split(F.col("full_name"), " ")[0])`*
- **Exam Mapping:** Domain 3 (Data Transformation & Modeling) · **Week 2** (`notebooks/Week2_Ingestion_Transformations.py`, `readings/Week2_Ingestion_Transformations.md`)
- **Why It's Correct:** `F.split(col, " ")` splits a string into an array of words; `[0]` accesses the first element.
- **Distractor & Trap Analysis:**
  - **B is incorrect:** `F.substr()` takes integer start and length positions, not a delimiter string.
  - **C is incorrect:** `.slice()` operates on arrays, not string columns.
  - **D is incorrect:** `explode()` converts array elements into new rows rather than creating a column.

---

# Section: Domain 4 — Working with Lakeflow Jobs

### Q23: DAG Parallel Execution
- **Correct Answer:** **D** — *In parallel concurrently as soon as the job starts*
- **Exam Mapping:** Domain 4 (Working with Lakeflow Jobs) · **Week 3** (`slides/Week3_Jobs_CICD.pptx`, `notebooks/Week3_Jobs_Orchestration.py`)
- **Why It's Correct:** Tasks without dependencies in a Lakeflow Job DAG run in parallel concurrently as soon as the job is triggered.
- **Distractor & Trap Analysis:**
  - **A and B are incorrect:** Task execution is determined by DAG dependency edges (`depends_on`), not alphabetical or UI creation order.
  - **C is incorrect:** Parallel tasks can share job clusters or use serverless compute.

---

### Q24: Repair Run on Job Failure
- **Correct Answer:** **A** — *Trigger a "Repair run" on the failed job run*
- **Exam Mapping:** Domain 4 (Working with Lakeflow Jobs) · **Week 3** (`notebooks/Week3_Jobs_Orchestration.py`, `readings/Week3_Jobs_CICD.md`)
- **Why It's Correct:** A "Repair run" re-executes only the failed task and downstream skipped tasks. Already successful tasks (Task 1) are not rerun.
- **Distractor & Trap Analysis:**
  - **B is incorrect:** "Run now" executes the whole DAG from the beginning.
  - **C is incorrect:** Retries only fix transient issues, not deterministic code bugs.
  - **D is incorrect:** Cloning jobs causes configuration drift and orphans run history.

---

### Q25: Sharing Dynamic Values with `taskValues`
- **Correct Answer:** **B** — *Task A calls `taskValues.set()`; Task B calls `taskValues.get()`*
- **Exam Mapping:** Domain 4 (Working with Lakeflow Jobs) · **Week 3** (`notebooks/Week3_Params_Widgets_Demo.py`, `readings/Week3_Jobs_CICD.md`)
- **Why It's Correct:** `dbutils.jobs.taskValues` is the Databricks API for passing runtime values between isolated tasks in a Lakeflow Job run.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** `os.environ` is local to a single OS process and not shared across job tasks.
  - **C is incorrect:** `%run` runs notebooks interactively in one session, not between job tasks.
  - **D is incorrect:** Notebook widgets are for input parameters, not dynamic runtime outputs from other tasks.

---

### Q26: File Arrival Trigger
- **Correct Answer:** **C** — *A File Arrival trigger pointed at the landing storage path*
- **Exam Mapping:** Domain 4 (Working with Lakeflow Jobs) · **Week 3** (`readings/Week3_Jobs_CICD.md`, `readings/Exam_Review_CheatSheet.md`)
- **Why It's Correct:** File Arrival triggers start the job automatically when new files land in cloud storage, eliminating empty polling runs and reducing latency.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** 1-minute cron polling runs 1,440 times/day and wastes compute on empty runs.
  - **B is incorrect:** Continuous triggers are for 24/7 streaming engines.
  - **D is incorrect:** Table update triggers monitor Delta table commits, not raw landing files.

---

### Q27: For-Each Matrix Tasks
- **Correct Answer:** **B** — *A For-each task iterating over a list of region parameters*
- **Exam Mapping:** Domain 4 (Working with Lakeflow Jobs) · **Week 3** (`slides/Week3_Jobs_CICD.pptx`, `readings/Week3_Jobs_CICD.md`)
- **Why It's Correct:** A `For-each` task loops one parameterized task across a list of inputs (e.g. 20 regions) with a configurable concurrency limit.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** If/Else tasks evaluate binary branches, not iterative parameter lists.
  - **C is incorrect:** 20 separate workspace jobs create unmanageable orchestration overhead.
  - **D is incorrect:** Interactive `%run` loops lack task-level retries and DAG monitoring.

---

### Q28: Run-If "All done" Finalizer
- **Correct Answer:** **D** — *`All done`*
- **Exam Mapping:** Domain 4 (Working with Lakeflow Jobs) · **Week 3** (`readings/Week3_Jobs_CICD.md`, `readings/Exam_Review_CheatSheet.md`)
- **Why It's Correct:** Setting "Run if" to `All done` ensures a cleanup or notification task executes regardless of whether upstream tasks succeeded or failed.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** `All succeeded` prevents execution if any upstream task fails.
  - **B is incorrect:** `At least one failed` skips execution on successful runs.
  - **C is incorrect:** `None failed` behaves identically to `All succeeded`.

---

### Q29: Job Parameters to Notebook Widgets
- **Correct Answer:** **A** — *`dbutils.widgets.get("env")`*
- **Exam Mapping:** Domain 4 (Working with Lakeflow Jobs) · **Week 3** (`notebooks/Week3_Params_Widgets_Demo.py`, `readings/Week3_Jobs_CICD.md`)
- **Why It's Correct:** Job parameters configured in Lakeflow Jobs arrive in notebook tasks as widgets and are accessed via `dbutils.widgets.get("param_name")`.
- **Distractor & Trap Analysis:**
  - **B is incorrect:** Parameters are not injected into `spark.conf`.
  - **C is incorrect:** Notebook tasks do not receive parameters in `sys.argv`.
  - **D is incorrect:** `dbutils.jobs.get_parameter` is an invented syntax.

---

# Section: Domain 5 — Implementing CI/CD

### Q30: Git Folders vs Remote Provider Boundary
- **Correct Answer:** **C** — *Reviewing, approving, and merging a Pull Request (PR) into `main`*
- **Exam Mapping:** Domain 5 (Implementing CI/CD) · **Week 3** (`slides/Week3_Jobs_CICD.pptx`, `readings/Week3_Jobs_CICD.md`)
- **Why It's Correct:** Databricks Git folders handle branching, committing, pushing, and pulling. PR review, policy validation, and merging MUST occur on the remote Git provider (GitHub/GitLab).
- **Distractor & Trap Analysis:**
  - **A, B, and D are incorrect:** Branching, committing, and pulling can all be executed directly inside the Databricks Git folders interface.

---

### Q31: Declarative Automation Bundles CLI Lifecycle
- **Correct Answer:** **B** — *`databricks bundle validate` → `databricks bundle deploy` → `databricks bundle run`*
- **Exam Mapping:** Domain 5 (Implementing CI/CD) · **Week 3** (`cicd/databricks.yml`, `readings/Week3_Jobs_CICD.md`)
- **Why It's Correct:** The standard bundle lifecycle sequence is: `validate` (verify syntax) → `deploy` (deploy resources to target) → `run` (execute deployed job).
- **Distractor & Trap Analysis:**
  - **A is incorrect:** A bundle cannot be run before being deployed.
  - **C is incorrect:** `init` creates a new bundle project, not part of regular deployment.
  - **D is incorrect:** `generate` and `execute` are invented commands.

---

### Q32: Multi-Environment Targets in DABs
- **Correct Answer:** **D** — *Use a shared `databricks.yml` with variable overrides in the `targets` block*
- **Exam Mapping:** Domain 5 (Implementing CI/CD) · **Week 3** (`cicd/databricks.yml`, `readings/Week3_Jobs_CICD.md`)
- **Why It's Correct:** A single `databricks.yml` defines the core job resources, and the `targets` block defines environment-specific variable overrides (catalogs, schedules, clusters) for `dev`, `staging`, and `prod`.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Duplicating YAML files across repositories causes configuration drift.
  - **B is incorrect:** Hardcoding environment checks in code violates CI/CD best practices.
  - **C is incorrect:** Manual UI edits get overwritten by future bundle deployments.

---

### Q33: CI/CD Pipeline Authentication
- **Correct Answer:** **A** — *Using a dedicated Service Principal with credentials stored in CI/CD secrets*
- **Exam Mapping:** Domain 5 (Implementing CI/CD) · **Week 3** (`slides/Week3_Jobs_CICD.pptx`, `readings/Week3_Jobs_CICD.md`)
- **Why It's Correct:** Automated CI/CD deployments must authenticate using Service Principals with secrets managed in enterprise vaults (GitHub Secrets, Azure Key Vault), avoiding personal user credentials.
- **Distractor & Trap Analysis:**
  - **B is incorrect:** Personal access tokens break when employees leave and violate security scoping.
  - **C is incorrect:** Hardcoding credentials in YAML files is a critical security vulnerability.
  - **D is incorrect:** Databricks APIs require authentication on all endpoints.

---

# Section: Domain 6 — Troubleshooting, Monitoring & Optimization

### Q34: OPTIMIZE vs VACUUM
- **Correct Answer:** **B** — *`OPTIMIZE` to compact small files, then `VACUUM` to delete unreferenced files*
- **Exam Mapping:** Domain 6 (Troubleshooting, Monitoring & Optimization) · **Week 4** (`notebooks/Week4_Governance_Optimization.py`, `readings/Week4_Governance_Optimization.md`)
- **Why It's Correct:** `OPTIMIZE` compacts small Parquet files into larger ~1 GB files to speed up reads. `VACUUM` deletes unreferenced files older than the retention threshold (e.g. 720 hours = 30 days) to free storage.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Swapping `OPTIMIZE` and `VACUUM` is a classic trap: `VACUUM` does not compact files.
  - **C is incorrect:** `DROP TABLE` deletes the table definition.
  - **D is incorrect:** `RESTORE TABLE` rolls back table versions; it does not compact files.

---

### Q35: Liquid Clustering (`CLUSTER BY`) Advantage
- **Correct Answer:** **C** — *Clustering keys can be altered incrementally with `ALTER TABLE` without a full table rewrite*
- **Exam Mapping:** Domain 6 (Troubleshooting, Monitoring & Optimization) · **Week 4** (`readings/Week4_Governance_Optimization.md`, `readings/Exam_Review_CheatSheet.md`)
- **Why It's Correct:** Liquid Clustering (`CLUSTER BY`) replaces legacy partitioning. Clustering keys can be updated using `ALTER TABLE ... CLUSTER BY` on the fly and apply incrementally without rewriting historical data.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Liquid Clustering works alongside file compaction (`OPTIMIZE`).
  - **B is incorrect:** Liquid Clustering avoids creating rigid nested directory trees.
  - **D is incorrect:** Liquid Clustering manages files in cloud storage, not RAM.

---

### Q36: Spark UI Skew Diagnosis
- **Correct Answer:** **A** — *Data skew on the join/grouping key; fix with broadcast, salting, or null filtering*
- **Exam Mapping:** Domain 6 (Troubleshooting, Monitoring & Optimization) · **Week 4** (`slides/Week4_Governance_Optimization.pptx`, `readings/Week4_Governance_Optimization.md`)
- **Why It's Correct:** When 199 tasks finish in seconds but 1 task takes 42 minutes, it is the classic signature of data skew (one key with millions of rows bottlenecking a single core).
- **Distractor & Trap Analysis:**
  - **B is incorrect:** Driver OOM crashes the whole application during `collect()`, not a single executor task.
  - **C is incorrect:** Node failures trigger task retries on other nodes, not single long tasks.
  - **D is incorrect:** Setting shuffle partitions to 1 forces all work into a single task, worsening runtimes.

---

### Q37: Driver Out-Of-Memory via `collect()`
- **Correct Answer:** **D** — *All distributed data was pulled onto the single driver node's RAM*
- **Exam Mapping:** Domain 6 (Troubleshooting, Monitoring & Optimization) · **Week 4** (`readings/Week4_Governance_Optimization.md`, `readings/Exam_Review_CheatSheet.md`)
- **Why It's Correct:** `collect()` and `toPandas()` pull all distributed data across worker nodes into the single driver node's memory. For large datasets (500 GB), this crashes the driver with an Out-Of-Memory error.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** The crash occurs on the driver, not worker nodes.
  - **B is incorrect:** Storage throttling results in HTTP 503 retries, not memory crashes.
  - **C is incorrect:** Partition counts do not cause driver memory saturation.

---

### Q38: Predictive Optimization Operations
- **Correct Answer:** **A** — *`OPTIMIZE` (compaction) and `VACUUM` (purging obsolete data files)*
- **Exam Mapping:** Domain 6 (Troubleshooting, Monitoring & Optimization) · **Week 4** (`readings/Week4_Governance_Optimization.md`, `readings/Exam_Review_CheatSheet.md`)
- **Why It's Correct:** Predictive Optimization automatically runs `OPTIMIZE` (file compaction) and `VACUUM` (purging stale files) in the background on Unity Catalog managed tables.
- **Distractor & Trap Analysis:**
  - **B is incorrect:** Predictive Optimization is for table maintenance, not SQL query compile-time rewrites.
  - **C is incorrect:** It operates on managed tables; it does not convert external Parquet tables.
  - **D is incorrect:** It does not manage cluster auto-scaling.

---

# Section: Domain 7 — Governance & Security

### Q39: Unity Catalog Privilege Chain
- **Correct Answer:** **C** — *`USE CATALOG` on `finance` and `USE SCHEMA` on `finance.reports`*
- **Exam Mapping:** Domain 7 (Governance & Security) · **Week 4** (`notebooks/Week4_Governance_Optimization.py`, `readings/Week4_Governance_Optimization.md`)
- **Why It's Correct:** Unity Catalog requires a 3-level privilege chain to read a table: `USE CATALOG` (catalog level) + `USE SCHEMA` (schema level) + `SELECT` (table level). Without the `USE` privileges, queries fail with permission denied.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Table-level `ALL PRIVILEGES` still fails without `USE` on the catalog and schema.
  - **B and D are incorrect:** `MODIFY` and `CREATE TABLE` do not resolve traversal permissions.

---

### Q40: Principal Best Practices
- **Correct Answer:** **D** — *Grant permissions to account-level groups rather than individual users*
- **Exam Mapping:** Domain 7 (Governance & Security) · **Week 4** (`notebooks/Week4_Governance_Optimization.py`, `readings/Week4_Governance_Optimization.md`)
- **Why It's Correct:** Granting permissions to groups (synced via SCIM) ensures permissions scale cleanly during employee onboarding and role changes without editing individual table ACLs.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** User-level grants create unmanageable administrative overhead.
  - **B is incorrect:** Sharing credentials violates audit compliance and security policies.
  - **C is incorrect:** Making users owners gives them unrestrained administrative rights over tables.

---

### Q41: Dynamic Column Masking UDFs
- **Correct Answer:** **B** — *Define a SQL UDF checking group membership, then bind it with `ALTER TABLE...SET MASK`*
- **Exam Mapping:** Domain 7 (Governance & Security) · **Week 4** (`notebooks/Week4_Governance_Optimization.py`, `readings/Week4_Governance_Optimization.md`)
- **Why It's Correct:** Dynamic column masking is implemented in two steps: create a SQL UDF checking `is_account_group_member()`, then bind it to the column using `ALTER TABLE table_name ALTER COLUMN col SET MASK udf_name`.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Creating multiple views duplicates logic and leaves base tables exposed.
  - **C is incorrect:** Masking is evaluated at query time; it does not rewrite Parquet files on storage.
  - **D is incorrect:** `DENY` is not supported on Unity Catalog securable objects.

---

### Q42: Row Filters and Table Owners
- **Correct Answer:** **C** — *Only EMEA rows (or no rows), because row filters apply to all queries including table owners*
- **Exam Mapping:** Domain 7 (Governance & Security) · **Week 4** (`notebooks/Week4_Governance_Optimization.py`, `readings/Week4_Governance_Optimization.md`)
- **Why It's Correct:** In Unity Catalog, row filters and column masks apply universally across all query paths. Even the **table owner** is subject to row filter logic.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Table owners do NOT bypass row filters or column masks.
  - **B is incorrect:** Queries do not error; they return only the filtered rows.
  - **D is incorrect:** Queries return structured table rows, not raw metadata files.

---

### Q43: ABAC Tag-Based Column Masking
- **Correct Answer:** **D** — *Attribute-Based Access Control (ABAC) tag-based masking policies*
- **Exam Mapping:** Domain 7 (Governance & Security) · **Week 4** (`slides/Week4_Governance_Optimization.pptx`, `readings/Week4_Governance_Optimization.md`)
- **Why It's Correct:** Unity Catalog ABAC allows attaching tags (e.g. `tag: pii = 'true'`) to columns and applying a single central masking policy that automatically governs all tagged columns across thousands of tables.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Lakehouse Federation connects external databases, not column masking.
  - **B is incorrect:** Static views do not scale across thousands of tables.
  - **C is incorrect:** Delta Sharing is for data sharing across organizations.

---

### Q44: Converting External to Managed Tables
- **Correct Answer:** **B** — *`ALTER TABLE marketing.leads SET MANAGED;`*
- **Exam Mapping:** Domain 7 (Governance & Security) · **Week 4** (`readings/Week4_Governance_Optimization.md`, `readings/Exam_Review_CheatSheet.md`)
- **Why It's Correct:** `ALTER TABLE catalog.schema.table SET MANAGED` transfers lifecycle management of an external table directly to Unity Catalog, enabling `UNDROP` and automated Predictive Optimization.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** `CREATE TABLE AS SELECT` creates a new duplicate table rather than converting in place.
  - **C is incorrect:** `UPDATE TABLE ... SET TYPE` is an invalid SQL command.
  - **D is incorrect:** Dropping an external table deletes metadata only; `UNDROP` cannot recover external tables.

---

### Q45: Automated Data Lineage in Catalog Explorer
- **Correct Answer:** **D** — *Open the Lineage tab on the table in Catalog Explorer or query system tables*
- **Exam Mapping:** Domain 7 (Governance & Security) · **Week 4** (`notebooks/Week4_Governance_Optimization.py`, `readings/Week4_Governance_Optimization.md`)
- **Why It's Correct:** Unity Catalog automatically captures column-level and table-level lineage in real time. Users view the visual graph under the **Lineage** tab in Catalog Explorer or query `system.access.table_lineage`.
- **Distractor & Trap Analysis:**
  - **A is incorrect:** Cluster driver logs contain low-level Spark logs, not end-to-end lineage graphs.
  - **B is incorrect:** The `_delta_log` tracks individual table commits, not cross-table pipeline lineage.
  - **C is incorrect:** `.explain(True)` shows a single query execution plan, not organizational data flow.

---

## Complete Quick-Scoring Key

| Q# | Key | Domain | Course Week | Topic |
|:---:|:---:|:---|:---:|:---|
| **1** | **B** | Domain 1: Platform | Week 1 | Lakehouse Unified Value |
| **2** | **A** | Domain 1: Platform | Week 1 | Control Plane vs Data Plane |
| **3** | **C** | Domain 1: Platform | Week 1 | `_delta_log` & ACID Reads |
| **4** | **D** | Domain 2: Ingestion | Week 2 | COPY INTO Idempotency |
| **5** | **A** | Domain 2: Ingestion | Week 2 | Auto Loader Stream Config |
| **6** | **B** | Domain 2: Ingestion | Week 2 | File Notification Mode |
| **7** | **C** | Domain 2: Ingestion | Week 2 | Auto Loader Schema Evolution |
| **8** | **D** | Domain 2: Ingestion | Week 2 | `_rescued_data` Mechanism |
| **9** | **C** | Domain 2: Ingestion | Week 2 | `availableNow=True` Trigger |
| **10** | **A** | Domain 2: Ingestion | Week 2 | Lakeflow Connect Connectors |
| **11** | **A** | Domain 2: Ingestion | Week 2 | Struct Dot-Notation & Explode |
| **12** | **D** | Domain 2: Ingestion | Week 2 | Custom REST API Ingestion |
| **13** | **B** | Domain 3: Transformation | Week 2 | MERGE INTO Syntax & Semantics |
| **14** | **C** | Domain 3: Transformation | Week 2 | Multiple Matches Error Fix |
| **15** | **D** | Domain 3: Transformation | Week 2 | Latest Row Window Dedup |
| **16** | **A** | Domain 3: Transformation | Week 2 | PySpark Positional `union()` |
| **17** | **B** | Domain 3: Transformation | Week 2 | Broadcast Join Optimization |
| **18** | **C** | Domain 3: Transformation | Week 2 | INNER vs LEFT JOIN Missing Rows |
| **19** | **B** | Domain 3: Transformation | Week 2 | Quarantine Pattern vs Constraints |
| **20** | **C** | Domain 3: Transformation | Week 2 | Materialized Views vs Views |
| **21** | **C** | Domain 3: Transformation | Week 2 | `approx_count_distinct` |
| **22** | **A** | Domain 3: Transformation | Week 2 | String Splitting (`F.split`) |
| **23** | **D** | Domain 4: Lakeflow Jobs | Week 3 | DAG Dependency & Concurrency |
| **24** | **A** | Domain 4: Lakeflow Jobs | Week 3 | Repair Run vs Retries |
| **25** | **B** | Domain 4: Lakeflow Jobs | Week 3 | `dbutils.jobs.taskValues` |
| **26** | **C** | Domain 4: Lakeflow Jobs | Week 3 | File Arrival Triggers |
| **27** | **B** | Domain 4: Lakeflow Jobs | Week 3 | For-Each Parameterization |
| **28** | **D** | Domain 4: Lakeflow Jobs | Week 3 | Run-If "All done" Finalizer |
| **29** | **A** | Domain 4: Lakeflow Jobs | Week 3 | Job Parameters to Widgets |
| **30** | **C** | Domain 5: CI/CD | Week 3 | Git Folders vs Provider PR Boundary |
| **31** | **B** | Domain 5: CI/CD | Week 3 | Bundle CLI: validate→deploy→run |
| **32** | **D** | Domain 5: CI/CD | Week 3 | Multi-Environment Targets in DABs |
| **33** | **A** | Domain 5: CI/CD | Week 3 | Service Principal CI/CD Auth |
| **34** | **B** | Domain 6: Troubleshooting | Weeks 3–4 | OPTIMIZE Compaction & VACUUM |
| **35** | **C** | Domain 6: Troubleshooting | Weeks 3–4 | Liquid Clustering (`CLUSTER BY`) |
| **36** | **A** | Domain 6: Troubleshooting | Weeks 3–4 | Spark UI Skew Detection & Fix |
| **37** | **D** | Domain 6: Troubleshooting | Weeks 3–4 | Driver OOM via `collect()` |
| **38** | **A** | Domain 6: Troubleshooting | Weeks 3–4 | Predictive Optimization |
| **39** | **C** | Domain 7: Governance | Week 4 | USE CATALOG / USE SCHEMA Chain |
| **40** | **D** | Domain 7: Governance | Week 4 | Group-Based Access Governance |
| **41** | **B** | Domain 7: Governance | Week 4 | Dynamic Column Masking UDFs |
| **42** | **C** | Domain 7: Governance | Week 4 | Row Filter Universal Scope |
| **43** | **D** | Domain 7: Governance | Week 4 | ABAC Tag-Based Governance |
| **44** | **B** | Domain 7: Governance | Week 4 | `ALTER TABLE ... SET MANAGED` |
| **45** | **D** | Domain 7: Governance | Week 4 | Automated Lineage & Auditing |
