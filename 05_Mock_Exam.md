# Full Mock Exam — Databricks Certified Data Engineer Associate

> **Rules:** 45 questions · 90 minutes · timed · closed-book · one sitting · answer everything.
> Blueprint-weighted to the May 4, 2026 exam guide: Platform 3 · Ingestion 9 · Transformation 10 · Lakeflow Jobs 7 · CI/CD 4 · Troubleshooting/Optimization 5 · Governance 7.
> Score yourself **per domain** using the answer key's domain map. Bring the breakdown to Week 5.

# Mock Exam: Databricks Data Engineer Associate
# Score 100

## Q1: What is the primary architectural value of the Databricks Data Intelligence Platform compared to maintaining a separate data lake and data warehouse?
- [ ] It stores all data in a proprietary high-performance format
- [x] One copy of data in open formats serves SQL, ETL, streaming, and ML workloads under unified governance
- [ ] It eliminates the need for data governance entirely
- [ ] It replaces cloud object storage with managed databases
  ::time=30

## Q2: A nightly production ETL pipeline must run unattended on a budget. The team is choosing between an always-on all-purpose cluster and per-run compute. Which option fits best?
- [ ] An all-purpose cluster shared with the analytics team
- [ ] A SQL warehouse kept running 24/7
- [ ] A GPU cluster to finish faster
- [x] Job compute created per run and terminated on completion (or serverless jobs compute)
  ::time=30

## Q3: What enables Delta Lake to provide ACID transactions on top of cloud object storage?
- [x] An ordered transaction log that records every change as a new table version
- [ ] Row-level locks held in a central database
- [ ] Storing all data in memory until commit
- [ ] Replacing Parquet files with a proprietary binary format
  ::time=20

## Q4: Which statement correctly loads new CSV files from a volume into an existing Delta table, skipping files already ingested?
- [ ] INSERT INTO sales SELECT * FROM read_files('/Volumes/c/s/v/files/', format => 'csv')
- [ ] CREATE OR REPLACE TABLE sales AS SELECT * FROM csv.`/Volumes/c/s/v/files/`
- [x] COPY INTO sales FROM '/Volumes/c/s/v/files/' FILEFORMAT = CSV FORMAT_OPTIONS ('header' = 'true')
- [ ] MERGE INTO sales USING read_files('/Volumes/c/s/v/files/') ON true WHEN NOT MATCHED THEN INSERT *
  ::time=30

## Q5: What is the purpose of the checkpoint location in an Auto Loader stream?
- [x] It persists ingestion progress so each file is processed exactly once across runs
- [ ] It stores a backup copy of every ingested file
- [ ] It caches query results for faster reads
- [ ] It holds rows rejected by schema enforcement
  ::time=20

## Q6: An Auto Loader pipeline ingests from a container that will soon receive tens of millions of files, and the team needs new files discovered with minimal latency and listing cost. Which configuration should they evaluate?
- [ ] Switching from Auto Loader to COPY INTO
- [ ] Reducing the trigger interval of directory listing to one second
- [ ] Splitting the container into 100 folders with one stream each
- [x] File notification mode instead of directory listing
  ::time=30

## Q7: A team wants tables from an on-premises SQL Server continuously available in Unity Catalog with the least custom engineering. Which option fits?
- [ ] A nightly JDBC notebook with hand-written watermark logic
- [x] A Lakeflow Connect managed connector for SQL Server
- [ ] COPY INTO pointed at database export files
- [ ] Auto Loader reading the database's transaction log
  ::time=30

## Q8: Why is COPY INTO described as idempotent?
- [ ] It validates schema before every load
- [ ] It locks the target table during the load
- [x] It tracks which files have been loaded and skips them on subsequent runs
- [ ] It wraps each file in a separate transaction
  ::time=20

## Q9: During Auto Loader ingestion with schema inference, a field arrives as a STRING in some files where the inferred schema expects INT. With default settings, where does the mismatched data go?
- [ ] The stream fails permanently until the files are fixed
- [x] Into the _rescued_data column for those rows
- [ ] Into a separate quarantine table created automatically
- [ ] It is silently dropped
  ::time=30

## Q10: Data must be pulled nightly from an internal REST API that uses custom token authentication, then landed in a Unity Catalog table. No connector exists for this API. What is the recommended pattern?
- [ ] Wait for a Lakeflow Connect managed connector to be released
- [ ] Configure Auto Loader with the API URL as the source path
- [ ] Use Lakehouse Federation to query the API directly
- [x] Write the API client in a notebook and schedule it with Lakeflow Jobs
  ::time=30

## Q11: An Auto Loader stream using addNewColumns schema evolution encounters files containing a brand-new column. What is the expected behavior?
- [x] The stream fails with a schema-change error, updates the tracked schema, and succeeds on restart
- [ ] The stream continues and the column appears in-flight without interruption
- [ ] The new column is permanently ignored
- [ ] All subsequent files are quarantined until the schema is manually edited
  ::time=30

## Q12: A JSON feed contains customer records with a nested address object and an array of phone numbers. What is the recommended way to store this in a Delta table?
- [ ] Flatten everything into 40 scalar columns at ingestion
- [ ] Store the whole record as one JSON string column
- [x] Preserve the address as a STRUCT column and phones as an ARRAY column
- [ ] Split the feed into five normalized relational tables in bronze
  ::time=30

## Q13: In a medallion architecture, which layer applies deduplication, type casting, and validation to produce trustworthy datasets for downstream use?
- [ ] Bronze
- [x] Silver
- [ ] Gold
- [ ] Landing
  ::time=20

## Q14: A data engineer needs a CTAS statement where order_date is stored as DATE even though the source column is STRING. Which approach is correct?
- [ ] Declare (order_date DATE) in parentheses after the table name
- [ ] Add a USING DATE clause to the CTAS
- [ ] CTAS cannot control types; an empty CREATE TABLE plus INSERT is required
- [x] CAST(order_date AS DATE) inside the SELECT clause
  ::time=20

## Q15: A MERGE INTO fails with an error stating a target row matched multiple source rows. What is the correct fix?
- [x] Deduplicate the source on the merge key before merging
- [ ] Replace WHEN MATCHED THEN UPDATE with INSERT
- [ ] Add a second WHEN MATCHED clause
- [ ] Switch the ON condition to a LIKE comparison
  ::time=30

## Q16: A PySpark pipeline calls df1.union(df2) where df2's columns are in a different order than df1's. What happens?
- [ ] Spark aligns columns by name automatically
- [ ] The operation fails because column order differs
- [x] Values are combined by position, silently mixing data into wrong columns
- [ ] Duplicate rows are removed after the union
  ::time=30

## Q17: What does df.dropDuplicates(["customer_id"]) guarantee?
- [ ] The most recently updated row per customer_id is kept
- [x] One row per customer_id is kept, but which row is not guaranteed
- [ ] Rows are only removed when every column matches
- [ ] The DataFrame is sorted by customer_id after deduplication
  ::time=30

## Q18: A silver table needs first_name and last_name derived from a full_name column formatted as "First Last". Which expression pattern applies?
- [ ] explode(full_name) into two rows
- [ ] full_name.first and full_name.last struct access
- [ ] A row filter function on full_name
- [x] split(full_name, ' ') and selecting elements [0] and [1]
  ::time=30

## Q19: Why would a data engineer choose approx_count_distinct over count(DISTINCT ...) on a billion-row table?
- [x] It is significantly faster and uses less memory, at the cost of a small bounded error
- [ ] It returns exact results faster by using an index
- [ ] count(DISTINCT ...) is deprecated in Spark
- [ ] It automatically deduplicates the underlying table
  ::time=20

## Q20: A BI dashboard repeatedly runs an expensive multi-table aggregation. Results may lag the source by up to one hour. Which gold-layer object minimizes read cost while meeting the freshness requirement?
- [ ] A standard view over the aggregation query
- [ ] A temp view created by the nightly job
- [x] A materialized view refreshed on a schedule
- [ ] A streaming table fed by the BI tool
  ::time=30

## Q21: Invalid rows must not stop a silver load, but they must remain visible for investigation. Which pattern satisfies this?
- [ ] A CHECK constraint on the silver table
- [x] Split the load: valid rows to silver, invalid rows to a quarantine table
- [ ] NOT NULL constraints on every column
- [ ] Lower the table's retention period so bad rows expire
  ::time=30

## Q22: A join between a 4 MB lookup table and a 2 TB fact table is producing massive shuffles. Which change directly addresses this?
- [ ] Convert the join to a UNION ALL
- [ ] Repartition the fact table by the lookup key first
- [ ] Increase spark.driver.memory
- [x] Broadcast the lookup table (hint or autoBroadcastJoinThreshold)
  ::time=30

## Q23: Files from a partner land in cloud storage at unpredictable times, several times per week. The job that processes them currently runs hourly and usually finds nothing. Which trigger eliminates the empty runs?
- [x] A file arrival trigger on the storage location
- [ ] A tighter 15-minute schedule
- [ ] A continuous trigger
- [ ] A manual trigger with an on-call rotation
  ::time=30

## Q24: A final task must send a status notification whether the pipeline succeeded or failed. How should it be configured?
- [ ] As the first task in the DAG so it always runs
- [ ] With maximum retries so failure cannot skip it
- [x] With a run-if condition of "All done" on its dependencies
- [ ] As a separate job triggered by a schedule one hour later
  ::time=30

## Q25: In a 6-task run, task 3 failed after tasks 1–2 spent two hours succeeding. The bug is fixed. What does Repair run do when invoked on this run?
- [ ] Re-executes all six tasks in a new run
- [x] Re-executes task 3 and its downstream tasks only
- [ ] Marks task 3 as succeeded without executing it
- [ ] Rolls back the writes of tasks 1–2 and restarts
  ::time=20

## Q26: The same notebook logic must run for 30 store locations with at most 5 concurrent executions. Which Lakeflow Jobs feature is designed for this?
- [ ] 30 separate jobs sharing one schedule
- [ ] An if/else task per store
- [ ] A single task with a 30-element widget
- [x] A for-each task over the store list with concurrency 5
  ::time=30

## Q27: Task A computes a watermark value that Task B needs at run time. What is the intended mechanism?
- [x] Task A sets it with dbutils.jobs.taskValues.set and Task B reads it with taskValues.get
- [ ] Task A writes it to a global Python variable
- [ ] Task B re-runs Task A's notebook with %run
- [ ] Task A emails the value to the job owner
  ::time=30

## Q28: A job must execute a Lakeflow Spark Declarative Pipeline as one step of a larger DAG. Which task type is appropriate?
- [ ] A notebook task that imports the pipeline's source files
- [ ] A SQL task running REFRESH PIPELINE
- [x] A pipeline task referencing the pipeline
- [ ] A dashboard task bound to the pipeline's output
  ::time=20

## Q29: A new job must be fully configured in production this week but must not execute until go-live next month. What is the cleanest setup?
- [ ] Create the job next month
- [x] Deploy the job with its trigger set to Paused
- [ ] Set the schedule to a date far in the future and edit it later
- [ ] Remove all permissions so it cannot start
  ::time=30

## Q30: Which Git workflow steps can a data engineer complete entirely within the Databricks workspace Git folder UI?
- [ ] Creating the pull request and merging it
- [ ] Rewriting remote history with force-push
- [ ] Approving another engineer's pull request
- [x] Creating a branch, committing changes, and pushing to the remote
  ::time=20

## Q31: In a databricks.yml, where is the difference between the dev and prod deployment environments expressed?
- [x] In the targets block, with per-target variable overrides
- [ ] In separate resources blocks named dev and prod
- [ ] In the bundle block's environment list
- [ ] In a second databricks.yml committed to a prod branch
  ::time=30

## Q32: Before deploying a bundle, an engineer wants to confirm the configuration is syntactically correct and references resolve. Which command does this?
- [ ] databricks bundle run --dry
- [ ] databricks bundle deploy --check
- [x] databricks bundle validate
- [ ] databricks bundle sync --verify
  ::time=20

## Q33: An organization wants every merge to the main branch to automatically update production jobs. Which design accomplishes this?
- [ ] Engineers manually click Deploy in the workspace after each merge
- [x] A CI pipeline runs databricks bundle deploy -t prod, authenticated as a service principal, on merge
- [ ] A file arrival trigger watches the Git repository
- [ ] Production notebooks are edited directly to match main
  ::time=30

## Q34: A job that historically ran in 25 minutes has taken 70+ minutes for the past five nights. Which tool provides the first evidence of when the regression began and which task is responsible?
- [ ] The Spark UI of last night's run
- [ ] DESCRIBE HISTORY on the output table
- [x] The job's run history with per-task durations across runs
- [ ] The cluster event log
  ::time=30

## Q35: In a stage's task summary, the median task duration is 30 seconds, the 75th percentile is 45 seconds, and the maximum is 28 minutes. What does this indicate?
- [x] Data skew — one or a few partitions are far larger than the rest
- [ ] Disk spill across all tasks
- [ ] A driver out-of-memory condition
- [ ] Healthy parallelism
  ::time=30

## Q36: Query patterns on a large table have changed, and the current clustering keys no longer help. With Liquid Clustering, what does changing the keys require?
- [ ] A full table rewrite into a new table
- [ ] Dropping and re-ingesting the table with new PARTITIONED BY columns
- [ ] An OPTIMIZE ZORDER run on every historical file
- [x] An ALTER TABLE ... CLUSTER BY statement; new layout applies incrementally
  ::time=30

## Q37: A team runs VACUUM with a 1-hour retention on a table where analysts rely on time travel for day-old comparisons. What is the consequence?
- [ ] Nothing; VACUUM only affects storage costs
- [x] Time travel to versions older than the retention window stops working because their files are deleted
- [ ] Queries become faster because history is indexed
- [ ] The transaction log is deleted and the table becomes unreadable
  ::time=30

## Q38: A notebook fails at import with ModuleNotFoundError for a library that worked yesterday on a different cluster. What is the most likely cause?
- [ ] The library was deleted from PyPI
- [ ] The notebook's code has a syntax error
- [x] The library is not installed on the compute now attached to the notebook
- [ ] Unity Catalog revoked access to the library
  ::time=20

## Q39: A user has been granted SELECT on a table but receives a permission error when querying it. What is the most likely missing piece?
- [ ] SELECT must also be granted on the table's view
- [x] USE CATALOG and USE SCHEMA privileges on the parent objects
- [ ] Table ownership
- [ ] An entry in the table's row filter function
  ::time=20

## Q40: A regulated dataset must reside in the company's own storage account and remain directly readable by a non-Databricks tool, while still being governed in Unity Catalog. Which table type is required?
- [x] An external table on an external location
- [ ] A managed table with predictive optimization
- [ ] A streaming table in a declarative pipeline
- [ ] A materialized view over a managed table
  ::time=30

## Q41: A managed table was dropped by mistake ten minutes ago. What is the immediate recovery option?
- [ ] Restore the files from the cloud provider's recycle bin
- [ ] CREATE TABLE ... VERSION AS OF the dropped table
- [ ] Managed table drops are unrecoverable
- [x] UNDROP TABLE within the retention window
  ::time=30

## Q42: Regional account managers must see only rows for their own region when querying a shared table, enforced no matter which tool they query from. Which mechanism implements this?
- [ ] One filtered view per region with separate grants
- [ ] A column mask on the region column
- [x] A row filter function bound to the table evaluating group membership
- [ ] A DENY on the table for all non-admin users
  ::time=30

## Q43: A central security team must enforce identical masking on every column tagged sensitive_pii across thousands of tables, without editing each table. Which Unity Catalog capability is designed for this?
- [x] ABAC policies that apply masking based on tags
- [ ] A scheduled job that re-creates mask functions nightly
- [ ] Delta Sharing with masked recipients
- [ ] DENY statements generated by a script
  ::time=30

## Q44: What is the key advantage of Delta Sharing over delivering nightly data extracts to a partner?
- [ ] Extracts are blocked by Unity Catalog
- [ ] Delta Sharing physically copies data into the recipient's account for speed
- [ ] Delta Sharing requires the recipient to license Databricks
- [x] Recipients query live data without copies, with access governed and revocable by the provider
  ::time=30

## Q45: Where can a data engineer query the record of user actions (such as grants and table access) in a Unity Catalog-enabled workspace?
- [ ] In the _delta_log folder of each table
- [x] In system tables such as system.access.audit
- [ ] In the SQL warehouse query profile
- [ ] In the workspace trash folder
  ::time=30

---

## Answer Key (score by domain)

| # | Answer | Domain | Explanation |
|---|--------|--------|-------------|
| Q1 | One copy, open formats, unified governance | 1. Platform | The lakehouse value proposition: no warehouse/lake split, no copies. |
| Q2 | Job compute / serverless jobs | 1. Platform | Per-run compute terminates with the run; all-purpose lingers and costs. |
| Q3 | Transaction log | 1. Platform | `_delta_log` ordered commits = ACID + versioning on object storage. |
| Q4 | COPY INTO | 2. Ingestion | The incremental, file-tracking SQL loader; INSERT/CTAS reload everything. |
| Q5 | Exactly-once progress tracking | 2. Ingestion | The checkpoint records processed files/offsets across runs. |
| Q6 | File notification mode | 2. Ingestion | Event-driven discovery scales past directory listing at tens of millions of files. |
| Q7 | Managed connector | 2. Ingestion | Enterprise DB + least engineering = Lakeflow Connect managed connector. |
| Q8 | File tracking | 2. Ingestion | Idempotency = loaded files are remembered and skipped. |
| Q9 | _rescued_data | 2. Ingestion | Type-mismatched values are rescued, not dropped, not fatal. |
| Q10 | Notebook + Lakeflow Jobs | 2. Ingestion | The exam-sanctioned DIY pattern when no connector exists. |
| Q11 | Fail, update schema, succeed on restart | 2. Ingestion | addNewColumns' deliberate stop-and-recover contract. |
| Q12 | STRUCT + ARRAY columns | 2. Ingestion | Delta stores nested types natively; flattening at bronze loses fidelity. |
| Q13 | Silver | 3. Transformation | Clean/conform/validate is silver's contract. |
| Q14 | CAST in SELECT | 3. Transformation | CTAS schema is inferred; CASTs are the type-control mechanism. |
| Q15 | Dedupe the source | 3. Transformation | Multiple source matches per target row are ambiguous by definition. |
| Q16 | Positional mixing | 3. Transformation | df.union is positional; use unionByName when order differs. |
| Q17 | Arbitrary row per key | 3. Transformation | Subset dropDuplicates keeps *a* row; "latest" needs a window function. |
| Q18 | split + elements | 3. Transformation | The outline's "splitting columns" objective. |
| Q19 | Fast approximate cardinality | 3. Transformation | HyperLogLog trade: speed/memory vs. small bounded error. |
| Q20 | Materialized view | 3. Transformation | Precomputed reads + scheduled refresh fits "expensive + hourly staleness OK." |
| Q21 | Quarantine split | 3. Transformation | Constraints abort the write; quarantine keeps flow + visibility. |
| Q22 | Broadcast | 3. Transformation | Small-to-huge join: ship the small table, skip the big shuffle. |
| Q23 | File arrival trigger | 4. Jobs | Data-driven trigger ends empty polling runs. |
| Q24 | Run-if "All done" | 4. Jobs | Conditional execution for always-run finalizers. |
| Q25 | Failed + downstream only | 4. Jobs | Repair run's defining semantics. |
| Q26 | For-each with concurrency | 4. Jobs | Looping a task over a list is for-each's purpose. |
| Q27 | taskValues set/get | 4. Jobs | The inter-task value-passing API. |
| Q28 | Pipeline task | 4. Jobs | Declarative pipelines run in a DAG via the pipeline task type. |
| Q29 | Paused trigger | 4. Jobs | Deploy-ahead-of-go-live = configured job, paused schedule. |
| Q30 | Branch/commit/push | 5. CI/CD | The workspace UI's Git scope; PR creation/merge live in the provider. |
| Q31 | targets + overrides | 5. CI/CD | Environments are targets; differences are variable overrides. |
| Q32 | bundle validate | 5. CI/CD | The pre-deploy syntax/reference check. |
| Q33 | CI deploy as service principal | 5. CI/CD | The canonical automated promotion pattern on merge. |
| Q34 | Run history per-task durations | 6. Troubleshooting | Trends across runs = run history; single-run depth = Spark UI. |
| Q35 | Data skew | 6. Troubleshooting | Max ≫ median task time is the skew signature. |
| Q36 | ALTER ... CLUSTER BY | 6. Troubleshooting | Liquid clustering keys change without table rewrite — its headline feature. |
| Q37 | Time travel truncated | 6. Troubleshooting | VACUUM deletes unreferenced files; history older than retention is gone. |
| Q38 | Library missing on this compute | 6. Troubleshooting | Environment failure signature: import error after compute switch. |
| Q39 | USE CATALOG + USE SCHEMA | 7. Governance | The privilege chain; SELECT alone can't reach the table. |
| Q40 | External table | 7. Governance | Own-storage + external-tool readability forces external. |
| Q41 | UNDROP | 7. Governance | Managed drops are recoverable within the retention window. |
| Q42 | Row filter | 7. Governance | Row-level security bound to the table covers every query path. |
| Q43 | ABAC | 7. Governance | Tag-driven central policies at fleet scale. |
| Q44 | Zero-copy governed live access | 7. Governance | Delta Sharing's advantage: live, revocable, no extracts. |
| Q45 | system.access.audit | 7. Governance | Audit logs surface as queryable system tables. |

### Domain scoring grid

| Domain | Questions | Your score |
|--------|-----------|------------|
| 1. Databricks Intelligence Platform | Q1–Q3 (3) | /3 |
| 2. Data Ingestion and Loading | Q4–Q12 (9) | /9 |
| 3. Data Transformation and Modeling | Q13–Q22 (10) | /10 |
| 4. Working with Lakeflow Jobs | Q23–Q29 (7) | /7 |
| 5. Implementing CI/CD | Q30–Q33 (4) | /4 |
| 6. Troubleshooting, Monitoring, and Optimization | Q34–Q38 (5) | /5 |
| 7. Governance and Security | Q39–Q45 (7) | /7 |
| **Total** | **45** | **/45** |

**Interpreting your score:** the real exam's passing bar is scaled, but as a working rule treat **32+/45 (~70%)** with no domain below 50% as "on track." Any domain at or below 50% → that domain leads your final-week plan (see Week 5, Slide 7).
