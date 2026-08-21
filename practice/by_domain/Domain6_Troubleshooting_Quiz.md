# Exam Domain 6 — Troubleshooting, Monitoring & Optimization (~10%)
# Score 100

## Q1: In a Spark UI stage, **max task time ≫ median task time** signals…
- [ ] Disk spill to local storage
- [ ] Driver out-of-memory
- [x] Data skew
- [ ] A missing table statistic
::time=45

## Q2: First remedy for data skew on a join?
- [ ] Add more task retries and rerun the failed stage
- [x] Broadcast the small side, use AQE, or rethink the key
- [ ] Raise only the driver memory, leaving partitions as-is
- [ ] Drop the smaller table and reload it from the source
::time=45

## Q3: A stage reports substantial `Spill (Disk)`. What happened?
- [ ] Data skew concentrated on a single large partition
- [ ] A shuffle-free plan that needs no exchange step
- [ ] Driver out-of-memory from collecting results locally
- [x] Execution spilled intermediate data to disk
::time=45

## Q4: Big Shuffle Read/Write on a wide op (join, groupBy) indicates…
- [x] A heavy shuffle — broadcast the small table, filter early
- [ ] A driver crash caused by collecting too much data
- [ ] A library import conflict raised before execution starts
- [ ] A CHECK constraint violation blocking the write
::time=45

## Q5: `collect()` or `toPandas()` on a huge DataFrame most directly causes…
- [x] Driver OOM, while the executors stay healthy
- [ ] Executor-side skew on one oversized partition
- [ ] A shuffle stage that explodes in output size
- [ ] A schema mismatch detected on the read path
::time=45

## Q6: A failure that happens **before any task starts** is usually…
- [ ] Data skew concentrated on one very large partition
- [ ] Disk spill written to local disk during a wide op
- [x] Startup or library configuration
- [ ] A repair-run misconfiguration on the job
::time=45

## Q7: `OPTIMIZE` does what?
- [ ] Deletes old unreferenced files from storage
- [x] Rewrites files for compaction or clustering
- [ ] Refreshes a downstream materialized view
- [ ] Rewrites the table's schema and column types
::time=45

## Q8: `VACUUM` does what, and what is the side effect?
- [ ] Compacts many small files together without deleting anything
- [ ] Rebuilds only the table's column statistics
- [ ] Directly speeds up every query that runs against the table
- [x] Deletes unreferenced files past retention — limits time travel
::time=45

## Q9: Liquid Clustering (`CLUSTER BY`) is preferred over Z-ORDER and partitioning because…
- [x] Changeable keys and high-cardinality support
- [ ] It deletes old unreferenced files from storage automatically
- [ ] It removes the need to ever run OPTIMIZE on the table
- [ ] It works only on external tables, never managed ones
::time=45

## Q10: **Predictive optimization** can automatically run which maintenance on eligible tables?
- [ ] OPTIMIZE, VACUUM, and ANALYZE on external tables
- [ ] Cache refreshes and ANALYZE on temporary views
- [ ] Z-ORDER and VACUUM on every Delta table
- [x] OPTIMIZE, VACUUM, and ANALYZE on Unity Catalog managed tables
::time=45

## Q11: On **serverless** compute, Spark tuning knobs like `spark.sql.shuffle.partitions` are…
- [ ] Required to be set by hand before every run
- [x] Mostly not settable — Databricks manages them
- [ ] Configured inside the bundle's YAML file
- [ ] Controlled indirectly through row filters
::time=45

## Q12: Recommended reading order when diagnosing a slow query in the Query Profile?
- [ ] Spill counters first, then the table's schema
- [ ] A random sample of individual task logs and metrics
- [x] Longest stage → task spread → I/O and spill
- [ ] Only the driver logs, read from top to bottom
::time=45

## Q13: Where do you diagnose a duration **trend across runs** (not a single run)?
- [x] The job's run history and matrix view
- [ ] The Spark UI of a single individual run
- [ ] `DESCRIBE DETAIL` output on the table
- [ ] The Git provider's commit and merge history
::time=45
