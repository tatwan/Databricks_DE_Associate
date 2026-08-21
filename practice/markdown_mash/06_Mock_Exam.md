# Mock Exam 2 (25Q) — Instructor Copy

> Instructor-only. This file is ignored by git and should be distributed or launched only when learners are ready to take the timed mock.

# Mock Exam 2 — Databricks Certified Data Engineer Associate

> **Rules:** 25 questions · ~40 minutes · timed · closed-book · one sitting · answer everything.
> Blueprint-weighted to the May 4, 2026 exam guide: Platform 2 · Ingestion 5 · Transformation 6 · Lakeflow Jobs 4 · CI/CD 2 · Troubleshooting/Optimization 3 · Governance 3.
> Shares no questions with Mock Exam 1 (45Q) or Mock Exam 3. Score yourself **per domain** using the answer key's domain map.

# Mock Exam 2: Databricks Data Engineer Associate
# Score 100

## Q1: A team asks whether moving all of their jobs to serverless compute will automatically reduce their bill. What is the most accurate response?
- [ ] Yes — serverless is always cheaper than classic compute
- [x] Not necessarily — serverless is always simpler and hands-off, but cost depends on the workload shape
- [ ] No — serverless always costs more because Databricks manages it
- [ ] Yes, but only for SQL warehouses, never for jobs
::time=55

## Q2: A data engineer runs the following. What is created?
```sql
CREATE TABLE inventory (sku STRING, qty INT);
```
- [ ] An external Parquet table in the workspace root
- [ ] A temporary view visible only in this session
- [x] A managed Delta table (Delta is the default; no LOCATION means managed)
- [ ] A managed Iceberg table
::time=65

## Q3: A SQL-only team loads roughly 100 CSV files from a volume into a Delta table on a nightly schedule and needs reruns to be safe. Which option is the best fit?
- [ ] Auto Loader with file notification mode
- [ ] A Lakeflow Connect managed connector
- [x] COPY INTO with the volume path as the source
- [ ] CREATE OR REPLACE TABLE with read_files every night
::time=55

## Q4: Which single line in this read makes it an Auto Loader stream?
```python
(spark.readStream
   .format("cloudFiles")
   .option("cloudFiles.format", "json")
   .option("cloudFiles.schemaLocation", chk)
   .load(src))
```
- [x] `.format("cloudFiles")`
- [ ] `.option("cloudFiles.format", "json")`
- [ ] `.option("cloudFiles.schemaLocation", chk)`
- [ ] `.load(src)`
::time=65

## Q5: Auto Loader infers a field as INT, but a later file delivers that field as a STRING. With default settings, what happens to those rows?
- [ ] The stream fails permanently until the files are corrected
- [ ] The rows are silently dropped
- [x] The mismatched value is captured in `_rescued_data` and the row is still ingested
- [ ] A new quarantine table is created automatically for the rows
::time=55

## Q6: A team needs tables from an enterprise Salesforce org continuously available in Unity Catalog with the least engineering effort. Which approach fits?
- [ ] Auto Loader pointed at nightly Salesforce CSV exports
- [x] A Lakeflow Connect managed connector for Salesforce
- [ ] COPY INTO reading the Salesforce REST API directly
- [ ] A hand-written JDBC notebook with custom watermark logic
::time=55

## Q7: A customer record has `favorite_categories` as an ARRAY of three values. What does this query return for that customer?
```sql
SELECT customer_id, explode(favorite_categories) AS category
FROM read_files('/Volumes/ws/lab/customers.json', format => 'json');
```
- [ ] One row with the array concatenated into a string
- [x] Three rows — one per array element
- [ ] One row with a struct of the three categories
- [ ] Zero rows, because explode only works on structs
::time=65

## Q8: A `MERGE INTO` fails with "a target row matched multiple source rows." What is the correct fix?
- [x] Deduplicate the source on the merge key before merging
- [ ] Add a second WHEN MATCHED clause to the statement
- [ ] Replace the ON condition with a LIKE comparison
- [ ] Add a primary key constraint to the target table
::time=55

## Q9: A silver build must keep only the most recent record per `order_id` by `updated_at`. Which pattern is correct?
```sql
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY order_id ORDER BY updated_at DESC) AS rn
  FROM updates) WHERE rn = 1;
```
- [x] This is correct — the window function controls which duplicate survives
- [ ] Replace it with `dropDuplicates(["order_id"])`, which keeps the latest row
- [ ] Replace it with `GROUP BY order_id` returning any row
- [ ] Change `DESC` to `ASC` to keep the newest record
::time=65

## Q10: A query must combine two result sets and keep all duplicate rows. Which operator is correct?
- [ ] UNION
- [ ] INTERSECT
- [x] UNION ALL
- [ ] UNION DISTINCT
::time=45

## Q11: A dashboard repeatedly runs an expensive multi-table aggregation, and results may lag the source by up to one hour. Which gold object minimizes read cost while meeting that freshness rule?
- [ ] A standard view over the aggregation query
- [x] A materialized view refreshed on a schedule
- [ ] A temporary view recreated each morning
- [ ] A streaming table fed by the BI tool
::time=55

## Q12: Invalid rows must not stop a silver load, but they must remain visible for later investigation. Which pattern satisfies both requirements?
- [ ] A CHECK constraint on the silver table
- [ ] NOT NULL constraints on every column
- [x] Split the load: valid rows to silver, invalid rows to a quarantine table
- [ ] Lower the table's retention so bad rows expire
::time=55

## Q13: A CTAS must store `order_date` as DATE even though the source column is STRING. Which approach works?
```sql
CREATE TABLE silver.orders AS
SELECT id, ??? AS order_date
FROM bronze.orders;
```
- [ ] Declare `(order_date DATE)` in parentheses after the table name
- [ ] Add a `USING DATE` clause to the CTAS
- [x] Use `CAST(order_date AS DATE)` inside the SELECT
- [ ] CTAS cannot set types; use an empty CREATE TABLE plus INSERT
::time=65

## Q14: In a 6-task run, task 3 failed after tasks 1–2 spent two hours succeeding. The bug is fixed. What does Repair run do?
- [x] Re-executes task 3 and its downstream tasks only
- [ ] Re-executes all six tasks in a fresh run
- [ ] Marks task 3 succeeded without executing it
- [ ] Rolls back tasks 1–2 and restarts the whole job
::time=45

## Q15: Partner files land in cloud storage at unpredictable times, a few times a week. The job runs hourly and usually finds nothing. Which trigger removes the empty runs?
- [x] A file arrival trigger on the storage location
- [ ] A tighter 15-minute schedule
- [ ] A continuous, always-on trigger
- [ ] A manual trigger with an on-call rotation
::time=55

## Q16: The same notebook logic must run for 30 stores, with at most 5 running at once. Which Lakeflow Jobs feature is designed for this?
- [ ] 30 separate jobs sharing one schedule
- [ ] An if/else task per store
- [x] A for-each task over the store list with concurrency 5
- [ ] A single task reading a 30-element widget
::time=55

## Q17: A job parameter `target_schema` must be read inside a notebook task. Which line reads it?
```python
# job parameter 'target_schema' was set on the job
schema = ???
```
- [x] `dbutils.widgets.get("target_schema")`
- [ ] `dbutils.jobs.taskValues.get("target_schema")`
- [ ] `spark.conf.get("job.target_schema")`
- [ ] `os.environ["target_schema"]`
::time=65

## Q18: An engineer wants to confirm a bundle's configuration is syntactically valid and its references resolve, without changing anything. Which command does this?
- [ ] databricks bundle deploy --check
- [x] databricks bundle validate
- [ ] databricks bundle run --dry
- [ ] databricks bundle sync --verify
::time=45

## Q19: A platform team wants production jobs to update the moment code is merged to main, with no manual clicks by anyone. Which design accomplishes this?
- [ ] Engineers click Deploy in the workspace after each merge
- [x] CI runs `bundle deploy -t prod` as a service principal on merge to main
- [ ] A file arrival trigger watches the Git repository
- [ ] Production notebooks are edited directly to match main
::time=65

## Q20: A stage's task summary shows median duration 30 s, 75th percentile 45 s, and maximum 28 minutes. What does this indicate?
- [x] Data skew — one or a few partitions are far larger than the rest
- [ ] Disk spill across all tasks
- [ ] A driver out-of-memory condition
- [ ] Healthy parallelism
::time=55

## Q21: A team sets VACUUM retention to 1 hour on a Delta table. Two days later an analyst tries to query the table as it was yesterday, and the query fails. Why?
- [ ] Nothing — VACUUM only affects storage cost
- [x] Time travel to versions older than the retention window stops working, because their files are deleted
- [ ] Queries speed up because history becomes indexed
- [ ] The transaction log is deleted and the table becomes unreadable
::time=55

## Q22: A notebook calls `collect()` on a 300-million-row DataFrame and the session dies, while executor metrics show no memory pressure. What happened?
- [ ] Executor-side data skew on one oversized partition
- [x] Driver OOM — `collect()` funnels every row to the driver
- [ ] A shuffle stage exploded in output size
- [ ] A schema mismatch on the read path
::time=55

## Q23: A user has been granted SELECT on a table but still receives a permission error when querying it. What is the most likely missing piece?
- [ ] Table ownership must be transferred to the user
- [x] USE CATALOG and USE SCHEMA privileges on the parent objects
- [ ] SELECT must also be granted on the table's view
- [ ] An entry in the table's row filter function
::time=55

## Q24: On one shared customer table, support must see raw emails while everyone else sees masked values, through every query path. Which design fits?
- [x] A column mask function bound to the email column
- [ ] One filtered view for support and a masked copy for everyone else
- [ ] A DENY statement on the table for everyone outside support
- [ ] A row filter on the email column using the support group
::time=55

## Q25: A central security team must enforce identical masking on every column tagged `sensitive_pii` across thousands of tables, without editing each table. Which capability is designed for this?
- [x] ABAC policies that apply masking based on tags
- [ ] A scheduled job that recreates mask functions nightly
- [ ] A per-table mask function bound one table at a time
- [ ] DENY statements generated by a script
::time=55

---

## Answer Key (score by domain)

| # | Answer | Domain | Explanation |
|---|--------|--------|-------------|
| Q1 | Not necessarily; simpler ≠ cheaper | 1. Platform | Serverless is always hands-off; cost depends on workload shape. |
| Q2 | Managed Delta table | 1. Platform | Delta is default; no LOCATION ⇒ managed. |
| Q3 | COPY INTO | 2. Ingestion | SQL-only + modest volume + rerun-safe = the idempotent SQL loader. |
| Q4 | `.format("cloudFiles")` | 2. Ingestion | cloudFiles is the Auto Loader source; the rest are options/actions. |
| Q5 | `_rescued_data`, row kept | 2. Ingestion | Type mismatch is rescued, not dropped or fatal. |
| Q6 | Managed connector | 2. Ingestion | Enterprise SaaS + least engineering = Lakeflow Connect managed. |
| Q7 | Three rows | 2. Ingestion | explode fans an array into one row per element. |
| Q8 | Dedupe the source | 3. Transformation | Multiple source matches per target row are ambiguous by definition. |
| Q9 | Window function correct | 3. Transformation | ROW_NUMBER…DESC = 1 controls which duplicate survives; dropDuplicates does not. |
| Q10 | UNION ALL | 3. Transformation | UNION dedupes; UNION ALL keeps duplicates. |
| Q11 | Materialized view | 3. Transformation | Precomputed reads + scheduled refresh fits "expensive + hourly staleness OK." |
| Q12 | Quarantine split | 3. Transformation | Constraints abort the write; quarantine keeps flow + visibility. |
| Q13 | CAST in SELECT | 3. Transformation | CTAS types are inferred; CAST is the only type-control mechanism. |
| Q14 | Failed + downstream only | 4. Jobs | Repair run's defining semantics; green tasks preserved. |
| Q15 | File arrival trigger | 4. Jobs | Data-driven trigger ends empty polling runs. |
| Q16 | For-each with concurrency | 4. Jobs | Looping one task over a list with a concurrency cap is for-each. |
| Q17 | `dbutils.widgets.get` | 4. Jobs | Job parameters surface to notebook tasks as widgets. |
| Q18 | bundle validate | 5. CI/CD | The pre-deploy syntax/reference check that changes nothing. |
| Q19 | CI deploy as service principal | 5. CI/CD | The canonical automated promotion pattern on merge. |
| Q20 | Data skew | 6. Troubleshooting | Max ≫ median task time is the skew signature. |
| Q21 | Time travel truncated | 6. Troubleshooting | VACUUM deletes unreferenced files; history past retention is gone. |
| Q22 | Driver OOM | 6. Troubleshooting | collect() funnels all rows to the driver; executors stay healthy. |
| Q23 | USE CATALOG + USE SCHEMA | 7. Governance | The privilege chain; SELECT alone can't reach the table. |
| Q24 | Column mask function | 7. Governance | Column-level masking on the shared table, every query path, no copies. |
| Q25 | ABAC | 7. Governance | Tag-driven central policies at fleet scale. |

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
