# Databricks Certified Data Engineer Associate — August Mock Exam
# Score 100

# Section: Domain 1 — Databricks Intelligence Platform
> Questions 1 to 3 · Exam weight ~6% · Course Week 1

## Q1: What is the primary architecture advantage of a Databricks Lakehouse over separate data lakes and warehouses?
- [ ] A proprietary storage format that replaces open cloud object storage
- [x] One governed Delta Lake copy serves BI, streaming, ML, and batch ETL
- [ ] All SQL queries are compiled into PySpark and run in the control plane
- [ ] Schemas and data types are no longer required for silver and gold tables
::time=65

## Q2: Which component resides entirely in the Databricks-managed control plane rather than the data plane?
- [x] Unity Catalog metastore, Web UI, and Job orchestration scheduler
- [ ] Spark driver nodes and worker executor virtual machine instances
- [ ] Cloud storage containers holding Parquet data files and logs
- [ ] Customer VPC/VNet subnets hosting classic compute clusters
::time=65

## Q3: How does Delta Lake ensure concurrent readers never see uncommitted writes without table locks?
- [ ] By acquiring exclusive table-level locks before writing any files
- [ ] By caching the entire table in driver memory until commits finish
- [x] Readers query the latest committed snapshot recorded in the `_delta_log`
- [ ] By creating a full duplicate copy of the entire table directory on commit
::time=65

# Section: Domain 2 — Data Ingestion & Loading
> Questions 4 to 12 · Exam weight ~21% · Course Week 2

## Q4: `COPY INTO` is run a second time on a folder where no new files were added. What is the result?
- [ ] Fails with a `FileNotFoundException` error because no new files arrived
- [ ] Reloads all existing files and duplicates records in the target table
- [ ] Truncates the target table and leaves it empty with zero records
- [x] Loads 0 rows and succeeds because it tracks loaded files in the log
::time=65

## Q5: Which configuration option identifies a Structured Streaming query as an Auto Loader stream?
- [x] `.format("cloudFiles")`
- [ ] `.option("autoLoader", "true")`
- [ ] `.option("cloudFiles.mode", "stream")`
- [ ] `.format("deltaStream")`
::time=65

## Q6: A container receives millions of files daily. Which setting avoids slow directory listing costs in Auto Loader?
- [ ] Set `spark.sql.shuffle.partitions` to 2000 in cluster settings
- [x] Set `cloudFiles.useNotifications` to `true` (file notification mode)
- [ ] Switch to `COPY INTO` with a 10-second polling cron job schedule
- [ ] Set `cloudFiles.schemaEvolutionMode` to `rescue` to skip file checks
::time=65

## Q7: An Auto Loader stream (`addNewColumns`) encounters a file with a new column. What is the expected behavior?
- [ ] Silently drops the new column and continues processing existing fields
- [ ] Fails permanently and requires deleting the entire checkpoint directory
- [x] Throws a schema change exception, updates the schema, and succeeds on restart
- [ ] Moves all records containing the new column to a dead-letter queue table
::time=65

## Q8: Auto Loader infers a column as `DOUBLE`, but a later file contains `"N/A"`. Where does the unparsed string go?
- [ ] Aborts the entire batch transaction and halts the stream immediately
- [ ] Coerces the string to `0.0` and inserts the row without raising an alert
- [ ] Drops the row entirely from the target Delta table during processing
- [x] Sets the column to `NULL` and captures `"N/A"` in `_rescued_data`
::time=65

## Q9: Which trigger runs an Auto Loader stream as a batch on a schedule, processing all pending files before stopping?
- [ ] `.trigger(once=True)`
- [ ] `.trigger(processingTime="4 hours")`
- [x] `.trigger(availableNow=True)`
- [ ] `.trigger(continuous="1 minute")`
::time=65

## Q10: Which ingestion feature provides turnkey change data capture (CDC) for Salesforce and SQL Server with zero custom code?
- [x] Lakeflow Connect managed connectors
- [ ] Custom Python JDBC scripts on scheduled all-purpose clusters
- [ ] Auto Loader pointed at daily CSV export files in a volume
- [ ] Lakehouse Federation with scheduled CTAS queries
::time=65

## Q11: In bronze JSON data, `contact` is a STRUCT and `phones` is an ARRAY. Which query correctly extracts both?
- [x] `SELECT contact.city, explode(phones) FROM events_bronze;`
- [ ] `SELECT explode(contact).city, flatten(phones) FROM events_bronze;`
- [ ] `SELECT contact['city'], unwrap(phones) FROM events_bronze;`
- [ ] `SELECT split(contact, '.')[0], explode(phones.*) FROM events_bronze;`
::time=65

## Q12: Data must be ingested from a proprietary REST API with custom OAuth2 headers and no pre-built connector. Best approach?
- [ ] Point Auto Loader directly at the HTTPS REST API endpoint with auth tokens
- [ ] Use `COPY INTO` with a custom `REST_AUTH` header option in the query
- [ ] Query the REST API directly using Lakehouse Federation and generic ODBC
- [x] Write the API client in a Python notebook and orchestrate with Lakeflow Jobs
::time=65

# Section: Domain 3 — Data Transformation & Modeling
> Questions 13 to 22 · Exam weight ~22% · Course Week 2

## Q13: Which atomic statement performs an upsert from a staging table `stg` into a target Delta table `silver`?
- [ ] `UPSERT INTO silver USING stg ON silver.id = stg.id WHEN MATCHED UPDATE...`
- [x] `MERGE INTO silver USING stg ON silver.id = stg.id WHEN MATCHED THEN UPDATE...`
- [ ] `INSERT OVERWRITE silver SELECT * FROM stg WHERE id IN (SELECT id FROM silver);`
- [ ] `APPLY CHANGES INTO silver FROM stg KEYS (id) SEQUENCE BY ts;`
::time=65

## Q14: A `MERGE INTO` query fails with: "Cannot perform MERGE because a target row matched multiple source rows." How to fix?
- [ ] Add an enforced PRIMARY KEY constraint to the target table definition
- [ ] Add `AND target.is_active = true` to the `ON` join filter condition
- [x] Deduplicate the source dataset on the merge key before running MERGE
- [ ] Change the cluster transaction isolation level to `READ UNCOMMITTED`
::time=65

## Q15: A table has multiple updates per `customer_id`. Which method guarantees retaining only the latest record?
- [ ] `df.dropDuplicates(["customer_id"])` in PySpark without specifying sort order
- [ ] `SELECT DISTINCT * FROM raw_customers` in SQL across all columns
- [ ] `SELECT customer_id, MAX(updated_at) FROM raw_customers GROUP BY customer_id`
- [x] Window function: `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1`
::time=65

## Q16: DataFrames `df1(id, sales, region)` and `df2(region, id, sales)` are combined with `df1.union(df2)`. What happens?
- [x] Data is combined positionally, placing `region` values into the `id` column
- [ ] PySpark matches columns by name automatically and aligns schemas correctly
- [ ] Fails immediately with a `SchemaMismatchException` error between columns
- [ ] PySpark automatically casts all columns to string and removes duplicates
::time=65

## Q17: A query joins a 50 TB fact table with a 15 MB dimension table, causing massive network shuffle. Best fix?
- [ ] Increase `spark.sql.shuffle.partitions` from 200 to 5000 in cluster settings
- [x] Broadcast the 15 MB dimension table (`/*+ BROADCAST */` or `broadcast()`)
- [ ] Repartition the 50 TB fact table into 10 partitions to reduce network hops
- [ ] Convert the query to a `CROSS JOIN` followed by a `WHERE` filter condition
::time=65

## Q18: Changing a gold query from `LEFT JOIN` to `INNER JOIN` caused total reported sales revenue to drop by 8%. Why?
- [ ] INNER JOIN computes the average revenue instead of the sum for grouped stores
- [ ] INNER JOIN removes duplicate transactions that occurred on the same business day
- [x] Sales records with store IDs that did not match the store dimension were dropped
- [ ] LEFT JOIN duplicates revenue rows whenever NULL values are present in dimensions
::time=65

## Q19: Bad records must not stop a silver pipeline, but must be saved for audit. Which pattern fits?
- [ ] Add a `CHECK (price > 0)` constraint on the silver table to reject bad rows
- [x] Quarantine split: route valid rows to silver, bad rows to a quarantine table
- [ ] Rely on Spark's default casting to coerce negative values to NULL in memory
- [ ] Run Delta Lake `VACUUM` to automatically delete invalid records from storage
::time=65

## Q20: A complex 15-metric aggregation over 500M rows is queried constantly by dashboards (1-hr lag OK). Best object?
- [ ] A standard SQL View (`CREATE VIEW`) that recomputes on every query execution
- [ ] A temporary view (`CREATE TEMPORARY VIEW`) scoped to the active user session
- [x] A Materialized View (`CREATE MATERIALIZED VIEW`) refreshed hourly on a schedule
- [ ] An external Parquet table re-created with CTAS every 5 minutes from a notebook
::time=65

## Q21: An interactive dashboard needs distinct user counts over 2 billion rows in under 3 seconds. Exactness is not required. Use?
- [ ] `COUNT(DISTINCT user_id)` which performs a full global shuffle across all rows
- [ ] `DENSE_RANK() OVER (ORDER BY user_id)` which ranks all rows in the dataset
- [x] `approx_count_distinct(user_id)`
- [ ] `summary(user_id)` which computes mean, standard deviation, and percentiles
::time=65

## Q22: `full_name` contains `"Jane Doe"`. Which PySpark expression extracts `"Jane"` into a new column `first_name`?
- [x] `df.withColumn("first_name", F.split(F.col("full_name"), " ")[0])`
- [ ] `df.withColumn("first_name", F.substr(F.col("full_name"), " "))`
- [ ] `df.withColumn("first_name", F.col("full_name").slice(0, 1))`
- [ ] `df.withColumn("first_name", F.explode(F.col("full_name"))[0])`
::time=65

# Section: Domain 4 — Working with Lakeflow Jobs
> Questions 23 to 29 · Exam weight ~16% · Course Week 3

## Q23: In a Lakeflow Job, `Task_C` depends on `Task_A` and `Task_B`. How will `Task_A` and `Task_B` execute?
- [ ] Sequentially in alphabetical order by task name (`Task_A` then `Task_B`)
- [ ] Sequentially in the exact order they were created in the Lakeflow Jobs UI
- [ ] In parallel only if explicitly assigned to separate all-purpose clusters
- [x] In parallel concurrently as soon as the job starts
::time=65

## Q24: Task 2 of a 5-task job failed due to a fixed bug. Task 1 was green; Tasks 3-5 were skipped. How to finish the run?
- [x] Trigger a "Repair run" on the failed job run
- [ ] Trigger "Run now" to re-execute the entire DAG from Task 1
- [ ] Increase task retry count to 5 and wait for the next scheduled run
- [ ] Clone the job, delete Task 1, and execute the clone
::time=65

## Q25: Task A computes a date string at runtime. Which API passes this value to downstream Task B in the same job run?
- [ ] Task A writes to `os.environ`; Task B reads `os.getenv()` in its OS process
- [x] Task A calls `taskValues.set()`; Task B calls `taskValues.get()`
- [ ] Task A runs `%run TaskB` passing the variable directly in notebook scope
- [ ] Task A calls `widgets.text()`; Task B calls `widgets.get()` for inputs
::time=65

## Q26: Files land in cloud storage at unpredictable times. Which trigger starts the job immediately without empty polling runs?
- [ ] A Scheduled Cron trigger configured to run every 1 minute throughout the day
- [ ] A Continuous trigger running 24/7 on an always-on all-purpose compute cluster
- [x] A File Arrival trigger pointed at the landing storage path
- [ ] A Table Update trigger monitoring commits on `samples.nyctaxi.trips`
::time=65

## Q27: A team needs to run the same task across 20 regions with configurable concurrency. Which task type fits best?
- [ ] An If/Else condition task linked to 20 separate downstream branch tasks
- [x] A For-each task iterating over a list of region parameters
- [ ] A Run-job task calling 20 individual workspace jobs sequentially
- [ ] A Python `%run` loop inside a single interactive notebook script
::time=65

## Q28: A final task must send a status summary email regardless of whether upstream tasks succeeded or failed. Run-if setting?
- [ ] `All succeeded` which requires all upstream dependency tasks to succeed
- [ ] `At least one failed` which triggers only when an upstream error occurs
- [ ] `None failed` which runs when all upstream dependencies complete cleanly
- [x] `All done`
::time=65

## Q29: A Lakeflow Job passes a parameter `env = 'prod'` to a notebook task. How does the notebook read it?
- [x] `dbutils.widgets.get("env")`
- [ ] `spark.conf.get("databricks.jobs.parameters.env")`
- [ ] `sys.argv[1]`
- [ ] `dbutils.jobs.get_parameter("env")`
::time=65

# Section: Domain 5 — Implementing CI/CD
> Questions 30 to 33 · Exam weight ~10% · Course Week 3

## Q30: When using Databricks Git folders with GitHub, which step MUST occur on the remote Git provider?
- [ ] Creating a new feature branch from `main` inside the workspace
- [ ] Committing modified notebook and SQL files with a commit message
- [x] Reviewing, approving, and merging a Pull Request (PR) into `main`
- [ ] Pulling remote changes into the local workspace branch
::time=65

## Q31: Which command sequence represents the standard deployment lifecycle for Declarative Automation Bundles?
- [ ] `databricks bundle run` → `databricks bundle deploy` → `databricks bundle validate`
- [x] `databricks bundle validate` → `databricks bundle deploy` → `databricks bundle run`
- [ ] `databricks bundle deploy` → `databricks bundle validate` → `databricks bundle init`
- [ ] `databricks bundle generate` → `databricks bundle execute`
::time=65

## Q32: How should multi-environment configurations (dev, staging, prod) be managed in Declarative Automation Bundles?
- [ ] Maintain three separate repositories with duplicated YAML configuration files
- [ ] Hardcode `if env == 'prod'` conditional logic inside notebook source files
- [ ] Manually change compute and catalog settings in the workspace UI after deploy
- [x] Use a shared `databricks.yml` with variable overrides in the `targets` block
::time=65

## Q33: How should an automated GitHub Actions CI/CD deployment authenticate with Databricks?
- [x] Using a dedicated Service Principal with credentials stored in CI/CD secrets
- [ ] Using the Personal Access Token (PAT) of the Lead Data Engineer on their account
- [ ] Hardcoding administrator username and password directly inside `databricks.yml`
- [ ] Allowing anonymous unauthenticated deployments over an internal corporate VPN
::time=65

# Section: Domain 6 — Troubleshooting, Monitoring & Optimization
> Questions 34 to 38 · Exam weight ~10% · Course Weeks 3–4

## Q34: A Delta table has thousands of small 1 MB files and old unreferenced data files. Which command pair optimizes it?
- [ ] `VACUUM` to compact small files, then `OPTIMIZE` to delete unreferenced files
- [x] `OPTIMIZE` to compact small files, then `VACUUM` to delete unreferenced files
- [ ] `ALTER TABLE REORGANIZE` followed by `DROP TABLE` to clean table storage
- [ ] `OPTIMIZE` to delete old files, then `RESTORE TABLE` to compact active data
::time=65

## Q35: Why is Liquid Clustering (`CLUSTER BY`) preferred over legacy Hive partitioning (`PARTITIONED BY`)?
- [ ] Liquid Clustering disables file compaction to eliminate write overhead completely
- [ ] Liquid Clustering creates rigid nested directory trees in cloud object storage
- [x] Clustering keys can be altered incrementally with `ALTER TABLE` without a full table rewrite
- [ ] All table data and indexes are stored permanently in RAM rather than object storage
::time=65

## Q36: In the Spark UI, 199 tasks completed in 15 seconds, but 1 task ran for 42 minutes. What issue does this indicate?
- [x] Data skew on the join/grouping key; fix with broadcast, salting, or null filtering
- [ ] Driver Out-Of-Memory error; fix by increasing driver instance memory in settings
- [ ] Worker node hardware failure; fix by switching from spot to on-demand instances
- [ ] Excessive partitions; fix by reducing `spark.sql.shuffle.partitions` value to 1
::time=65

## Q37: Running `df.toPandas()` or `df.collect()` on a 500 GB DataFrame crashed the notebook with a Driver OOM. Why?
- [ ] Worker nodes ran out of RAM processing shuffle partitions across the cluster
- [ ] Cloud storage throttled read operations due to exceeding API request limits
- [ ] Shuffle partition count exceeded 2000 causing task scheduler crashes on nodes
- [x] All distributed data was pulled onto the single driver node's memory space
::time=65

## Q38: What background operations does Unity Catalog Predictive Optimization execute automatically on managed tables?
- [x] `OPTIMIZE` (compaction) and `VACUUM` (purging obsolete data files)
- [ ] Rewriting SQL queries at compile time to inject broadcast join hints automatically
- [ ] Converting external Parquet tables into Unity Catalog managed Delta tables
- [ ] Auto-scaling compute cluster worker nodes based on query queue depth and latency
::time=65

# Section: Domain 7 — Governance & Security
> Questions 39 to 45 · Exam weight ~15% · Course Week 4

## Q39: An analyst has `SELECT` on `finance.reports.sales` but gets `Permission Denied`. What privileges are missing?
- [ ] `ALL PRIVILEGES` on the table `finance.reports.sales` in the metastore
- [ ] `MODIFY` on the schema `finance.reports` to allow execution plan generation
- [x] `USE CATALOG` on `finance` and `USE SCHEMA` on `finance.reports`
- [ ] `CREATE TABLE` on the schema `finance.reports` to permit temporary tables
::time=65

## Q40: What is the recommended best practice for granting object permissions in Unity Catalog?
- [ ] Grant permissions directly to individual user email accounts for audit tracking
- [ ] Share an admin account password among all senior analysts in each business unit
- [ ] Make all analysts the owner of every table they query to bypass permission checks
- [x] Grant permissions to account-level groups rather than individual users
::time=65

## Q41: How is dynamic column masking applied to mask SSNs for non-HR users in Unity Catalog?
- [ ] Create duplicate SQL views per audience with hardcoded string replacement logic
- [x] Define a SQL UDF checking group membership, then bind it with `ALTER TABLE...SET MASK`
- [ ] Run a nightly batch job that physically encrypts Parquet files in cloud storage
- [ ] Apply a `DENY SELECT` statement on the specific column for all non-HR users
::time=65

## Q42: A row filter restricts rows to `region = 'EMEA'`. What rows does the TABLE OWNER see if they are not in the EMEA group?
- [ ] All rows because table owners bypass all row filters and masks automatically
- [ ] Query fails with an `AccessControlException` error for unauthorized table owners
- [x] Only EMEA rows (or no rows), because row filters apply to all queries including table owners
- [ ] Raw Parquet metadata files and directory paths in storage but no tabular data rows
::time=65

## Q43: Which feature applies a central masking policy across thousands of columns tagged `pii = 'true'` automatically?
- [ ] Lakehouse Federation foreign catalogs connected to external databases
- [ ] Static SQL views generated across all schemas using information schema queries
- [ ] Delta Sharing open protocol recipient profiles and external sharing tokens
- [x] Attribute-Based Access Control (ABAC) tag-based masking policies
::time=65

## Q44: Which command converts an external table `marketing.leads` to a managed table in place?
- [ ] `CREATE MANAGED TABLE marketing.leads AS SELECT * FROM marketing.leads;`
- [x] `ALTER TABLE marketing.leads SET MANAGED;`
- [ ] `UPDATE TABLE marketing.leads SET TYPE = 'MANAGED' WHERE table_name = 'leads';`
- [ ] `DROP TABLE marketing.leads;` followed by `UNDROP TABLE marketing.leads;`
::time=65

## Q45: How can a data engineer inspect end-to-end data lineage for a table without installing external agents?
- [ ] Parse Spark execution driver logs across completed cluster runs in the workspace
- [ ] Query raw `_delta_log` JSON commit files in cloud storage with external JSON tools
- [ ] Run `.explain(True)` on DataFrames in an active interactive notebook session
- [x] Open the Lineage tab on the table in Catalog Explorer or query system tables
::time=65
