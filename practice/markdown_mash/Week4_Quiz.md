# Week 4 quiz — run in the closing segment, end of class

> Instructor-only. Covers **Week 4** content. End quiz: 8 questions, ~7 minutes, run live.
> The Self-Review Bank below is assigned as homework, not run live.
> The prior-week review quiz is in `Pre_Week4_Quiz.md` (run at 0:00).

---

## END QUIZ — Week 4 Content (run at ~1:50)

# Week 4 Quiz: Governance, Security, and Optimization
# Score 100

## Q1: An analyst group already has USE CATALOG and USE SCHEMA. What additional privilege lets them query (read-only) all current and future tables in the schema?
- [ ] ALL PRIVILEGES on the schema
- [ ] SELECT granted on each table individually
- [x] SELECT granted on the schema
- [ ] MODIFY granted on the schema
::time=25

## Q2: A user receives SELECT on a table through group A. Security must ensure this specific user can never read the table, regardless of group memberships. What should be used?
- [ ] REVOKE SELECT from group A
- [x] DENY SELECT on the table to that user
- [ ] Remove the user from the workspace
- [ ] Drop and recreate the table without grants
::time=25

## Q3: Support agents may see customer emails; everyone else must see masked values — on the same table, with no extra copies. What is the correct implementation?
- [x] Create a SQL function using is_account_group_member and bind it with ALTER TABLE ... SET MASK on the email column
- [ ] Create one view per audience and grant them separately
- [ ] Encrypt the email column and share keys with support
- [ ] GRANT SELECT on the email column only to support agents
::time=30

## Q4: A security team must apply consistent masking to every column tagged pii_email across 3,000 tables, managed centrally. Which capability matches?
- [ ] Per-table mask functions maintained by each data owner
- [x] Unity Catalog ABAC policies driven by tags
- [ ] DENY statements on all 3,000 tables
- [ ] Delta Sharing with masked recipients
::time=30

## Q5: Which clause creates a Delta table with Liquid Clustering on the store column?
- [x] CREATE TABLE sales (...) CLUSTER BY (store)
- [ ] CREATE TABLE sales (...) PARTITIONED BY (store)
- [ ] CREATE TABLE sales (...) ZORDER BY (store)
- [ ] CREATE TABLE sales (...) BUCKETED BY (store)
::time=20

## Q6: In the Spark UI, one stage shows median task time 35 seconds but a maximum task time of 41 minutes, with one task reading far more data than the rest. What is the bottleneck?
- [ ] Disk spill
- [ ] A library conflict
- [x] Data skew
- [ ] Driver out-of-memory
::time=30

## Q7: Which pair correctly matches the maintenance command to its purpose?
- [ ] OPTIMIZE deletes old unreferenced files; VACUUM compacts small files
- [x] OPTIMIZE compacts small files; VACUUM deletes old unreferenced files (and limits time travel)
- [ ] Both commands compact files; VACUUM is just faster
- [ ] VACUUM rewrites the table with new clustering keys
::time=25

## Q8: A notebook calls collect() on a 300-million-row DataFrame and the session dies, while executor metrics show no memory pressure. What happened, and which setting is the (stopgap) lever?
- [x] Driver out-of-memory; spark.driver.memory
- [ ] Executor out-of-memory; spark.executor.memory
- [ ] Disk spill; spark.sql.shuffle.partitions
- [ ] Broadcast failure; spark.sql.autoBroadcastJoinThreshold
::time=30

### End Quiz Answer Key (with explanations)

| # | Answer | Difficulty | Explanation |
|---|--------|-----------|-------------|
| Q1 | SELECT on schema | Easy | Schema-level SELECT inherits to current AND future tables — official sample Q2's pattern. ALL PRIVILEGES over-grants; per-table misses future tables. |
| Q2 | DENY | Easy | DENY overrides any grant including group-inherited; REVOKE only removes one grant. |
| Q3 | Mask function + SET MASK | Applied | The two-step masking pattern; per-audience views are copies-of-logic. |
| Q4 | ABAC | Applied | Scale + tags + central management = ABAC's exact pitch. |
| Q5 | CLUSTER BY | Easy | Liquid Clustering DDL. PARTITIONED BY is legacy; ZORDER is an OPTIMIZE option; BUCKETED is invented. |
| Q6 | Data skew | Applied | Max ≫ median task time with uneven input is the skew signature. |
| Q7 | OPTIMIZE compacts / VACUUM deletes | Tricky | The swapped-purpose distractor is a standard exam trap — and VACUUM trims time travel. |
| Q8 | Driver OOM; driver.memory | Tricky | collect() funnels everything to the driver; healthy executors are the planted clue. Real fix: don't collect. |

---

## SELF-REVIEW BANK — assign as homework with the mock (not run live)

# Week 4 Self-Review
# Score 100

## Q1: Which statement about predictive optimization is correct?
- [ ] It rewrites user queries to use better join strategies
- [ ] It works on external tables registered in any metastore
- [ ] It requires manually scheduled OPTIMIZE jobs to trigger it
- [x] It automatically runs maintenance like OPTIMIZE and VACUUM on Unity Catalog managed tables
::time=20

## Q2: Where does a data engineer view the automatically captured upstream/downstream lineage of a Unity Catalog table?
- [ ] In the _delta_log directory of the table
- [x] In Catalog Explorer on the table's Lineage tab
- [ ] In the cluster event log
- [ ] Lineage requires a third-party scanner to be installed
::time=20

## Q3: A company must give an external partner read access to live data. The partner does not use Databricks — they query from pandas and Power BI. Which approach fits?
- [ ] Databricks-to-Databricks Delta Sharing
- [ ] Nightly CSV exports to an SFTP server
- [x] Delta Sharing via the open sharing protocol
- [ ] Lakehouse Federation pointed at the partner's tools
::time=30

## Q4: Each regional vendor must see only rows where region matches their assignment, enforced for every query path against the single shared table. Which feature is designed for this?
- [ ] A WHERE clause documented in the query style guide
- [ ] Separate schemas per region with copied tables
- [ ] Column masks on the region column
- [x] A row filter function bound with ALTER TABLE ... SET ROW FILTER
::time=30

## Q5: Stage metrics show large values under "Spill (Memory)" and "Spill (Disk)". What does this indicate?
- [x] Data being processed did not fit in executor memory and overflowed to disk
- [ ] The table's files are corrupted and being re-read
- [ ] The shuffle was replaced by a broadcast join
- [ ] The driver is collecting too many results
::time=30

## Q6: A job fails immediately at cluster start, before any Spark stage executes. The event log shows an init script error. What category of failure is this?
- [ ] Data skew in the first stage
- [x] A cluster startup failure — infrastructure, not code
- [ ] An out-of-memory error on the executors
- [ ] A Delta transaction conflict
::time=20

## Q7: Which parameter controls the number of partitions created after a wide transformation such as a join or groupBy?
- [ ] spark.executor.memory
- [ ] spark.sql.autoBroadcastJoinThreshold
- [x] spark.sql.shuffle.partitions
- [ ] spark.driver.memory
::time=20

## Q8: A managed table was dropped by mistake ten minutes ago. What is the fastest recovery?
- [x] UNDROP TABLE — managed drops are recoverable within the retention window
- [ ] Restore from last night's cloud storage backup
- [ ] Recreate the table and reload from source files
- [ ] Nothing — managed drops are instantly unrecoverable
::time=25

## Q9: What is the key difference between Databricks-to-Databricks Delta Sharing and open Delta Sharing?
- [ ] D2D copies the data; open sharing references it
- [ ] Open sharing is faster because it bypasses governance
- [ ] D2D requires the provider to host a REST endpoint manually
- [x] D2D recipients use Unity Catalog natively, while open sharing serves recipients on non-Databricks tools via the protocol
::time=30

### Self-Review Answer Key

| # | Answer | Explanation |
|---|--------|-------------|
| Q1 | Auto-maintenance on UC managed tables | PO automates OPTIMIZE/VACUUM/layout for managed tables only. |
| Q2 | Catalog Explorer Lineage tab | UC captures lineage automatically from query execution. |
| Q3 | Open Delta Sharing | Non-Databricks recipient + live data + no copies = the open protocol. |
| Q4 | Row filter | Row-level security bound to the table applies to every query path. |
| Q5 | Memory overflow to disk | Spill = partitions too large for memory; more partitions or more memory. |
| Q6 | Cluster startup failure | Failure *before any stage* + init script = infrastructure category. |
| Q7 | spark.sql.shuffle.partitions | The post-shuffle partition count knob. |
| Q8 | UNDROP TABLE | "Managed drops are instantly unrecoverable" is FALSE — UNDROP exists (you ran it in demo 2.8). |
| Q9 | D2D = UC native; open = any tool | The two sharing flavors. |

---
