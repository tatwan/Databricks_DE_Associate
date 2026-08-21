# Databricks Data Engineer Associate — Kahoot Master Review
# Score 100

# Section: Round 1 — Lakehouse Foundations & Object Model
> Core concepts on storage, ACID transactions, Unity Catalog namespaces, and table lifecycles.

## Q1: Which component provides ACID transactions and time travel on top of Parquet files?
- [ ] Cloud object storage lifecycle management policies
- [x] Delta transaction log (_delta_log) commit files
- [ ] Parquet file footer metadata dictionaries
- [ ] Unity Catalog schema metadata caching logs
::time=45

## Q2: What happens to the underlying data files when an external table is dropped with `DROP TABLE`?
- [x] Data files remain intact in external cloud storage
- [ ] Data files are permanently deleted immediately
- [ ] Data files are moved to a temporary trash folder
- [ ] Data files are archived to cold storage tiers
::time=45

## Q3: What is the correct 3-level namespace structure used to reference a table in Unity Catalog?
- [ ] workspace.schema.table
- [ ] metastore.catalog.table
- [ ] catalog.database.metastore
- [x] catalog.schema.table
::time=45

## Q4: Which statement creates a CTAS table whose `id` output column is typed as `INT`?
- [ ] CREATE TABLE t (id INT) AS SELECT id FROM src
- [ ] CREATE TABLE t AS SELECT id::INT FROM src TYPE
- [x] CREATE TABLE t AS SELECT CAST(id AS INT) AS id FROM src
- [ ] CREATE TABLE t SET SCHEMA (id INT) AS SELECT * FROM src
::time=45

## Q5: How can you recover a Unity Catalog managed table that was accidentally deleted with `DROP TABLE`?
- [ ] Re-run the original CREATE TABLE statement pointing to the previous storage path
- [ ] Restore the underlying cloud storage container snapshot from the cloud portal
- [x] Execute UNDROP TABLE catalog.schema.table within the applicable retention period
- [ ] Query the table using RESTORE TABLE catalog.schema.table TO VERSION AS OF 0
::time=45

# Section: Round 2 — Data Ingestion & Loading
> Auto Loader, COPY INTO, Lakeflow Connect, and handling nested formats.

## Q6: What happens when `COPY INTO` is rerun on a directory where no new files have arrived?
- [ ] It raises a fatal duplicate file error
- [ ] It re-appends the most recent batch
- [ ] It prompts to drop the target table
- [x] It safely loads 0 rows with no duplicates
::time=45

## Q7: By default, when Auto Loader encounters data that does not match the expected schema, where can it preserve the unexpected values?
- [x] In the _rescued_data column
- [ ] In a dead-letter cloud bucket
- [ ] In the cluster driver log files
- [ ] In a temporary quarantine table
::time=45

## Q8: For very large cloud-storage directories, which Auto Loader approach avoids repeatedly listing all files and uses event-driven discovery?
- [ ] Directory listing crawler mode
- [x] File-events / notification-based discovery
- [ ] Batch catalog metadata sweep mode
- [ ] Polling schema registry mode
::time=45

## Q9: Which setting enables an Auto Loader stream to ingest all currently available files and shut down?
- [ ] .trigger(once=True)
- [ ] .trigger(continuous="1 min")
- [ ] .trigger(batchMode=True)
- [x] .trigger(availableNow=True)
::time=45

## Q10: Which connector provides a fully managed, low-code ingestion path for SaaS sources like Salesforce?
- [x] Lakeflow Connect managed connectors
- [ ] PySpark JDBC custom notebook scripts
- [ ] Direct Delta Sharing external feeds
- [ ] Cloud storage Auto Loader directory crawlers
::time=45

## Q11: Which PySpark function expands an ARRAY column into one new row per array element?
- [ ] flatten()
- [ ] split()
- [x] explode()
- [ ] unwrap()
::time=45

# Section: Round 3 — Transformations, Modeling & Data Quality
> MERGE INTO, window deduplication, join strategies, declarative pipeline expectations, and aggregations.

## Q12: If `MERGE INTO` fails with "a target row matched multiple source rows", what is the root cause?
- [ ] The target table has too many small data files
- [x] The source dataset contains duplicate join keys
- [ ] The MATCHED condition was omitted in the query
- [ ] The target table has clustering enabled on keys
::time=45

## Q13: Which technique guarantees keeping strictly the latest record per customer ID?
- [ ] df.dropDuplicates(["customer_id"])
- [ ] SELECT DISTINCT * FROM customers
- [x] ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY ts DESC) = 1
- [ ] SELECT customer_id, MAX(*) FROM customers
::time=45

## Q14: How does `df.union()` combine two PySpark DataFrames with matching schemas?
- [x] By column position, regardless of column names
- [ ] By column name, aligning matching column labels
- [ ] By automatically deduplicating identical rows
- [ ] By rejecting queries if column order differs
::time=45

## Q15: When joining a 15 MB lookup table with a 500 GB fact table, which optimization prevents heavy shuffle?
- [ ] Increasing spark.sql.shuffle.partitions
- [ ] Converting the join into a full cross join
- [ ] Splitting the fact table into mini-batches
- [x] Applying a broadcast join hint to the small table
::time=45

## Q16: In Lakeflow Declarative Pipelines, which expectation policy logs invalid rows in metrics but drops them from the output table?
- [ ] @dp.expect(...)
- [x] @dp.expect_or_drop(...)
- [ ] @dp.expect_or_fail(...)
- [ ] @dp.expect_or_quarantine(...)
::time=45

## Q17: If a row violates a `CHECK (amount > 0)` table constraint during an append, what happens?
- [ ] The bad row is replaced with NULL values
- [ ] The bad row is silently dropped and skipped
- [ ] The bad row is routed to a quarantine table
- [x] The entire transaction fails and writes nothing
::time=45

## Q18: Which aggregation function provides memory-efficient approximate distinct counts across billions of rows?
- [x] approx_count_distinct()
- [ ] count_distinct_estimate()
- [ ] hyper_log_count()
- [ ] dense_count_distinct()
::time=45

# Section: Round 4 — Lakeflow Jobs & Orchestration
> DAG dependencies, control flow, triggers, task values, and repair runs.

## Q19: In a Lakeflow Job DAG with no dependency edges between Task A and Task B, how do they execute?
- [ ] Sequentially in alphabetical order
- [ ] Task B waits for Task A to finish
- [x] Both tasks execute in parallel
- [ ] The scheduler prompts the user to pick
::time=45

## Q20: After fixing a code bug on a failed task in a 5-task DAG, how should you rerun the job efficiently?
- [ ] Trigger a full rerun of the entire job DAG
- [ ] Clone the DAG and run only the fixed single task
- [ ] Increase retry counts in job settings
- [x] Use Repair Run to execute only failed and downstream tasks
::time=45

## Q21: How does a downstream task retrieve a dynamic runtime value published by an upstream task?
- [ ] dbutils.widgets.get("key")
- [x] dbutils.jobs.taskValues.get("upstream_task", "key")
- [ ] spark.conf.get("spark.task.key")
- [ ] os.environ.get("JOB_TASK_VALUE_key")
::time=45

## Q22: Which trigger type starts a Lakeflow Job automatically as soon as new data is committed to a monitored Delta table?
- [ ] File arrival trigger
- [x] Table update trigger
- [ ] Scheduled cron trigger
- [ ] Continuous streaming trigger
::time=45

## Q23: Which Lakeflow Job task type executes a single parameterized task repeatedly over an array of items with a concurrency limit?
- [x] For-each task
- [ ] Run-job task
- [ ] If/else task
- [ ] Condition task
::time=45

## Q24: In Lakeflow Jobs, which Run-if condition ensures a cleanup or alert task runs regardless of whether upstream tasks succeeded or failed?
- [ ] All succeeded
- [ ] At least one failed
- [x] All done
- [ ] None failed
::time=45

# Section: Round 5 — CI/CD & Automation Bundles
> Declarative Automation Bundles (DABs), CLI workflows, environments, and Git provider boundaries.

## Q25: What is the correct Databricks CLI command sequence for Declarative Automation Bundles?
- [x] validate -> deploy -> run
- [ ] deploy -> validate -> run
- [ ] init -> run -> deploy
- [ ] build -> publish -> run
::time=45

## Q26: Where should pull requests (PRs) be reviewed and merged when using Databricks Git folders?
- [ ] Inside the Databricks Workspace Git UI
- [ ] In the Unity Catalog access control tab
- [x] In the external Git provider (e.g., GitHub, GitLab)
- [ ] In the Lakeflow Jobs configuration panel
::time=45

## Q27: In a `databricks.yml` bundle file, how should development and production environments be configured without duplicating code?
- [ ] By maintaining two completely separate bundle repositories
- [ ] By defining custom branches directly inside the YAML root
- [ ] By copying all task definitions into environment folders
- [x] By defining targets with environment-specific variable overrides
::time=45

## Q28: Which identity should authenticate automated CI/CD deployment pipelines deploying bundles to production?
- [ ] The workspace account administrator
- [x] A dedicated service principal
- [ ] The lead data engineer's personal user token
- [ ] The cluster creator's group identity
::time=45

# Section: Round 6 — Troubleshooting, Monitoring & Optimization
> OPTIMIZE, VACUUM, Liquid Clustering, Spark UI metrics, and memory diagnostics.

## Q29: What is the key functional difference between `OPTIMIZE` and `VACUUM` on Delta tables?
- [ ] OPTIMIZE removes old log versions; VACUUM changes data types
- [ ] OPTIMIZE purges deleted rows; VACUUM reindexes clustered keys
- [ ] OPTIMIZE deletes unreferenced files; VACUUM compacts small files
- [x] OPTIMIZE compacts small files; VACUUM deletes unreferenced files
::time=45

## Q30: In the Spark UI, what symptom indicates severe data skew in a stage?
- [x] Max task duration is substantially larger than median task duration
- [ ] All tasks finish within seconds but GC time exceeds 90%
- [ ] Executor memory drops to zero before jobs are scheduled
- [ ] Shuffle write records are evenly divided across all tasks
::time=45

## Q31: What is the primary cause when calling `df.collect()` crashes a notebook session while worker nodes remain completely healthy?
- [ ] Network partition between executor nodes
- [x] Driver out-of-memory (OOM) exception
- [ ] Delta transaction log concurrency conflict
- [ ] Cluster auto-termination timeout reached
::time=45

## Q32: In the Spark UI, what metric indicates that intermediate shuffle data exceeded RAM and was written to disk?
- [ ] Peak Execution Memory
- [ ] Shuffle Read Records
- [x] Spill (Memory) and Spill (Disk)
- [ ] Garbage Collection (GC) Time
::time=45

## Q33: How does Liquid Clustering (`CLUSTER BY`) differ from traditional Hive table partitioning?
- [x] Cluster keys can be redefined without requiring an immediate full rewrite of existing data
- [ ] Cluster keys require an immediate full rewrite of all historical table files on cloud storage
- [ ] It requires pre-creating physical subdirectories partitioned by date and region paths
- [ ] It is strictly limited to single integer columns and cannot cluster across multiple columns
::time=45

## Q34: Which feature enables automatic layout optimization on Unity Catalog managed tables without manual scripts?
- [ ] Liquid Clustering
- [ ] Adaptive Query Execution
- [ ] Auto Loader File Discovery
- [x] Predictive Optimization
::time=45

# Section: Round 7 — Governance & Security
> Unity Catalog 3-level permission chains, row filters, column masks, ABAC, and conversion.

## Q35: To query `sales.orders.transactions`, what minimum Unity Catalog privileges are required?
- [ ] SELECT on table only
- [ ] ALL PRIVILEGES on catalog and schema
- [x] USE CATALOG, USE SCHEMA, and SELECT on table
- [ ] MODIFY on schema and READ on table
::time=45

## Q36: What is the best practice principal type for assigning table permissions in Unity Catalog?
- [ ] Individual user accounts
- [x] Account-level groups
- [ ] Workspace cluster owners
- [ ] Table creator service credentials
::time=45

## Q37: Which Unity Catalog feature restricts row visibility for regional analysts based on their group membership?
- [x] Row filter applied via SET ROW FILTER
- [ ] Column mask applied via SET MASK
- [ ] Schema-level DENY statement
- [ ] Storage credential isolation policy
::time=45

## Q38: How can you dynamically mask sensitive columns without modifying underlying storage files?
- [ ] Create a separate replica table with encrypted string columns
- [ ] Run a scheduled PySpark job that overwrites raw table values
- [ ] Restrict access using standard schema-level DENY statements
- [x] Apply a column mask using ALTER TABLE ... ALTER COLUMN ... SET MASK
::time=45

## Q39: Which governance approach automatically enforces masking across thousands of tables by tagging columns rather than editing each table?
- [ ] Role-Based Access Control (RBAC)
- [x] Attribute-Based Access Control (ABAC)
- [ ] Discretionary Access Control (DAC)
- [ ] Mandatory Metastore Access Control (MAC)
::time=45

## Q40: Which statement correctly converts an existing external table to a Unity Catalog managed table?
- [ ] CREATE OR REPLACE TABLE catalog.schema.table AS SELECT *
- [ ] ALTER TABLE catalog.schema.table DROP LOCATION
- [x] ALTER TABLE catalog.schema.table SET MANAGED
- [ ] ALTER TABLE catalog.schema.table CONVERT TO MANAGED
::time=45
