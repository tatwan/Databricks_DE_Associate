# Mock Exam 3 (25Q) — Instructor Copy

> Instructor-only. This file is ignored by git and should be distributed or launched only when learners are ready to take the timed mock.

# Mock Exam 3 — Databricks Certified Data Engineer Associate

> **Rules:** 25 questions · ~40 minutes · timed · closed-book · one sitting · answer everything.
> Blueprint-weighted to the May 4, 2026 exam guide: Platform 2 · Ingestion 5 · Transformation 6 · Lakeflow Jobs 4 · CI/CD 2 · Troubleshooting/Optimization 3 · Governance 3.
> Shares no questions with Mock Exam 1 (45Q) or Mock Exam 2. Score yourself **per domain** using the answer key's domain map.

# Mock Exam 3: Databricks Data Engineer Associate
# Score 100

## Q1: Which set of services runs in the Databricks-managed control plane rather than in the customer's cloud account?
- [ ] The executors that process a job's data
- [x] The workspace UI, the job scheduler, and the Unity Catalog metastore
- [ ] Classic compute clusters and their attached storage
- [ ] The Parquet data files that back Delta tables
::time=55

## Q2: An engineer needs to read a Delta table exactly as it existed at version 3, without changing the current table. Which statement is correct?
```sql
-- read history, change nothing
SELECT * FROM events ???;
```
- [x] `VERSION AS OF 3`
- [ ] `RESTORE TABLE events TO VERSION AS OF 3`
- [ ] `AT VERSION 3`
- [ ] `DESCRIBE HISTORY events VERSION 3`
::time=65

## Q3: A folder already loaded by COPY INTO receives one new file. The command is rerun. What loads?
- [x] Only the new file's rows
- [ ] Every file in the folder, again
- [ ] Nothing at all
- [ ] The entire folder, loaded twice
::time=55

## Q4: In an Auto Loader stream, what does the checkpoint location track, and why does it matter?
- [x] It records processed-file progress across runs, enabling exactly-once ingestion
- [ ] It stores a backup copy of every ingested file
- [ ] It caches query results for faster reads
- [ ] It holds rows rejected by schema enforcement
::time=55

## Q5: An Auto Loader pipeline ingests from a container that will soon hold tens of millions of files, and the team needs low-latency discovery with minimal listing cost. Which configuration should they evaluate?
- [ ] Switching from Auto Loader to COPY INTO
- [ ] Reducing the directory-listing interval to one second
- [x] File notification mode instead of directory listing
- [ ] Splitting the container into 100 folders, one stream each
::time=55

## Q6: Data must be pulled nightly from an internal REST API with custom token authentication and landed in a Unity Catalog table. No connector exists for this API. What is the recommended pattern?
- [ ] Wait for a Lakeflow Connect managed connector to be released
- [ ] Configure Auto Loader with the API URL as the source path
- [x] Write the API client in a notebook and schedule it with Lakeflow Jobs
- [ ] Use Lakehouse Federation to query the API directly
::time=55

## Q7: A JSON feed has customer records with a nested address object and an array of phone numbers. What is the recommended way to store this in a Delta table?
- [ ] Flatten everything into 40 scalar columns at ingestion
- [ ] Store the whole record as a single JSON string column
- [x] Preserve the address as a STRUCT column and phones as an ARRAY column
- [ ] Split the feed into five normalized relational tables in bronze
::time=55

## Q8: A PySpark pipeline calls `df1.union(df2)` where `df2`'s columns are in a different order than `df1`'s. What happens?
```python
result = df1.union(df2)   # column orders differ
```
- [ ] Spark aligns the columns by name automatically
- [ ] The operation fails because the column orders differ
- [x] Values are combined by position, silently mixing data into the wrong columns
- [ ] Duplicate rows are removed after the union
::time=65

## Q9: A gold revenue view was changed from LEFT JOIN to INNER JOIN against the customer dimension, and total revenue dropped. Why?
- [x] Sales rows with no matching customer in the dimension were silently dropped
- [ ] INNER JOIN deduplicates the fact table before aggregating
- [ ] INNER JOIN applies constraints that reject unmatched rows
- [ ] The broadcast threshold excluded some fact rows from the join
::time=55

## Q10: Why would an engineer choose `approx_count_distinct` over `count(DISTINCT ...)` on a billion-row table?
- [x] Faster approximate cardinality for a small bounded error
- [ ] It returns exact results faster by using an index
- [ ] `count(DISTINCT ...)` is deprecated in Spark
- [ ] It automatically deduplicates the underlying table
::time=45

## Q11: A table has `CHECK (quantity > 0)`. A batch INSERT of 1,000 rows includes 3 rows with `quantity = -1`. What is the result?
- [ ] 997 rows are inserted and 3 are skipped
- [x] The entire INSERT fails and no rows are written
- [ ] 997 rows are inserted and 3 go to `_rescued_data`
- [ ] The 3 negative values are converted to NULL
::time=55

## Q12: Which gold-layer object is designed for incremental, append-only ingestion?
- [ ] A temporary session view
- [ ] A regular (recomputed) view
- [x] A streaming table
- [ ] A materialized aggregation view
::time=45

## Q13: Which PySpark expression mirrors SQL's `CAST(quantity AS INT)`?
```python
df = df.withColumn("quantity", ???)
```
- [x] `col("quantity").cast("int")`
- [ ] `col("quantity").astype("int")`
- [ ] `cast("quantity", IntegerType())`
- [ ] `quantity.toInt()`
::time=65

## Q14: During a run, an ingest task must hand a computed row-count to a later validation task. Which mechanism is intended for passing that value between tasks?
- [x] Set it with `taskValues.set` in Task A and read it with `taskValues.get` in Task B
- [ ] Task A writes it to a global Python variable
- [ ] Task B re-runs Task A's notebook with `%run`
- [ ] Task A emails the value to the job owner
::time=65

## Q15: A downstream aggregation job must run whenever a silver Delta table receives new commits from upstream jobs. Which trigger fits best?
- [ ] A scheduled cron trigger
- [ ] A file arrival trigger
- [x] A table update trigger
- [ ] A continuous, always-on trigger
::time=55

## Q16: A job is ready to ship to production now, but company policy says it must not run until the launch date next month. What is the cleanest configuration?
- [ ] Create the job next month instead
- [x] Deploy the job with its trigger set to Paused
- [ ] Set the schedule to a date far in the future and edit it later
- [ ] Remove all permissions so it cannot start
::time=55

## Q17: Two tasks in a job have no `depends_on` edge between them. How do they run?
- [x] In parallel
- [ ] Sequentially, one completing before the next starts
- [ ] In strict alphabetical order of task key
- [ ] The job errors — every task needs a dependency
::time=45

## Q18: Which set of Git operations can a data engineer complete entirely within the Databricks workspace Git folder UI?
- [ ] Creating and merging the pull request
- [ ] Approving another engineer's pull request
- [x] Creating a branch, committing changes, and pushing to the remote
- [ ] Rewriting remote history with a force-push
::time=55

## Q19: In this bundle file, where is the difference between the dev and prod environments expressed?
```yaml
resources:
  jobs:
    brewmart_daily: { tasks: [...] }
targets:
  dev:  { variables: { schema: lab_dev } }
  prod: { mode: production, variables: { schema: sales_prod } }
```
- [x] In the `targets` block, via per-target variable overrides
- [ ] In separate `resources` blocks named dev and prod
- [ ] In the `bundle` block's environment list
- [ ] In a second databricks.yml committed to a prod branch
::time=65

## Q20: Which maintenance command compacts many small files into fewer larger ones to speed up reads?
- [x] OPTIMIZE
- [ ] VACUUM
- [ ] ANALYZE
- [ ] REFRESH
::time=45

## Q21: A large Delta table already uses Liquid Clustering, but the workload's filter columns have shifted. What is needed to re-key it to the new columns?
- [ ] A full table rewrite into a new table
- [ ] Dropping and re-ingesting with new PARTITIONED BY columns
- [ ] An OPTIMIZE ZORDER run over every historical file
- [x] An `ALTER TABLE ... CLUSTER BY` statement; the new layout applies incrementally
::time=65

## Q22: A notebook fails at import with `ModuleNotFoundError` for a library that worked yesterday on a different cluster. What is the most likely cause?
- [ ] The library was deleted from PyPI
- [ ] The notebook's code has a syntax error
- [x] The library is not installed on the compute now attached to the notebook
- [ ] Unity Catalog revoked access to the library
::time=55

## Q23: How do `DROP TABLE` semantics differ between a managed table and an external table?
- [x] Managed deletes both metadata and data files; external deletes metadata only, leaving files in place
- [ ] Both delete the underlying data files immediately
- [ ] Both keep the underlying files; UC never deletes data
- [ ] Managed keeps its files; external deletes its files
::time=55

## Q24: A regulated dataset must live in the company's own storage account and stay directly readable by a non-Databricks tool, while remaining governed in Unity Catalog. Which table type is required?
- [x] An external table on a governed external location
- [ ] A managed table with predictive optimization
- [ ] A streaming table in a declarative pipeline
- [ ] A materialized view over a managed table
::time=55

## Q25: Regional account managers must see only rows for their own region when querying one shared table, enforced no matter which tool they query from. Which mechanism implements this?
- [ ] One filtered view per region with separate grants
- [ ] A column mask on the region column
- [x] A row filter function bound to the table that evaluates group membership
- [ ] A DENY on the table for all non-admin users
::time=55

---

## Answer Key (score by domain)

| # | Answer | Domain | Explanation |
|---|--------|--------|-------------|
| Q1 | UI, scheduler, metastore | 1. Platform | Control plane = Databricks-managed services; classic compute + data run in the customer account. |
| Q2 | VERSION AS OF 3 | 1. Platform | Reads history without changing anything; RESTORE would write a new version. |
| Q3 | Only the new file's rows | 2. Ingestion | COPY INTO tracks loaded files and loads only what is new. |
| Q4 | Processed-file progress | 2. Ingestion | The checkpoint gives exactly-once ingestion across runs. |
| Q5 | File notification mode | 2. Ingestion | Event-driven discovery scales past directory listing at tens of millions of files. |
| Q6 | Notebook + Lakeflow Jobs | 2. Ingestion | The sanctioned DIY pattern when no connector exists. |
| Q7 | STRUCT + ARRAY columns | 2. Ingestion | Delta stores nested types natively; flattening at bronze loses fidelity. |
| Q8 | Positional mixing | 3. Transformation | `df.union` is positional; use `unionByName` when order differs. |
| Q9 | Unmatched rows dropped | 3. Transformation | INNER JOIN keeps only matches; LEFT JOIN + COALESCE keeps and labels them. |
| Q10 | Fast approximate cardinality | 3. Transformation | HyperLogLog trade: speed/memory for a small bounded error. |
| Q11 | Entire INSERT fails | 3. Transformation | A CHECK constraint aborts the whole transaction; no partial write. |
| Q12 | Streaming table | 3. Transformation | The gold object for incremental append ingestion. |
| Q13 | `col("quantity").cast("int")` | 3. Transformation | `.cast` is the PySpark mirror; `.astype` is pandas. |
| Q14 | taskValues set/get | 4. Jobs | The inter-task runtime value-passing API. |
| Q15 | Table update trigger | 4. Jobs | Fires when a monitored Delta table receives new commits. |
| Q16 | Paused trigger | 4. Jobs | Deploy-ahead-of-go-live = configured job, paused schedule. |
| Q17 | In parallel | 4. Jobs | Tasks with no edge between them run in parallel automatically. |
| Q18 | Branch/commit/push | 5. CI/CD | The workspace Git scope; PR creation/merge live in the provider. |
| Q19 | targets + overrides | 5. CI/CD | Environments are targets; differences are variable overrides on one codebase. |
| Q20 | OPTIMIZE | 6. Troubleshooting | OPTIMIZE compacts small files; VACUUM deletes old files. |
| Q21 | ALTER ... CLUSTER BY | 6. Troubleshooting | Liquid clustering keys change without a table rewrite — its headline feature. |
| Q22 | Library missing on this compute | 6. Troubleshooting | Import error after a compute switch = environment/library failure. |
| Q23 | Managed deletes data; external keeps files | 7. Governance | The core managed-vs-external DROP distinction. |
| Q24 | External table | 7. Governance | Own-storage + external-tool readability forces external. |
| Q25 | Row filter | 7. Governance | Row-level security bound to the table covers every query path. |

### Domain scoring grid

| Domain | Questions | Your score |
|--------|-----------|------------|
| 1. Databricks Intelligence Platform | Q1–Q2 (2) | /2 |
| 2. Data Ingestion and Loading | Q3–Q7 (5) | /5 |
| 3. Data Transformation and Modeling | Q8–Q13 (6) | /6 |
| 4. Working with Lakeflow Jobs | Q14–Q17 (4) | /4 |
| 5. Implementing CI/CD | Q18–Q19 (2) | /2 |
| 6. Troubleshooting, Monitoring, and Optimization | Q20–Q22 (3) | /3 |
| 7. Governance and Security | Q23–Q25 (3) | /3 |
| **Total** | **25** | **/25** |

**Interpreting your score:** treat **~70% (18/25)** with no domain below 50% as "on track." Any domain at or below 50% leads your final-week plan.
