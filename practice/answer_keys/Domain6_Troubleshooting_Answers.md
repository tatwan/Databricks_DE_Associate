# Domain 6 — Troubleshooting, Monitoring & Optimization — Answer Key

**Q1 — C: Data skew.** A max task time far above the median means one partition is oversized. Spill shows in spill counters, driver OOM is driver-side, and "missing statistic" isn't the signature.

**Q2 — B: Broadcast the small side (AQE / rethink the key).** The standard skew remedy. Retries, driver memory, or dropping a table don't address a skewed key.

**Q3 — D: Disk spill.** Spill counters > 0 mean data spilled to disk — fix with more/smaller partitions or more executor memory. Not skew, a shuffle-free plan, or driver OOM.

**Q4 — A: A heavy shuffle.** Large shuffle read/write on a wide op signals shuffle cost — broadcast the small table and prune/filter early. Not a driver crash, library conflict, or constraint error.

**Q5 — A: Driver OOM.** `collect()`/`toPandas()` pull all rows to the driver; executors stay healthy. Not skew, a shuffle blow-up, or a schema mismatch.

**Q6 — C: Cluster startup or a library conflict.** Failures before any task runs are environment issues — init scripts, quota, or import/library conflicts. Skew and spill happen *during* the job; repair-run config is unrelated.

**Q7 — B: Rewrites files for better layout; old files remain until VACUUM.** OPTIMIZE compacts or reclusters data by writing replacement files and marking old ones unreferenced. It does not physically purge those old files; VACUUM does that after retention. It also does not rewrite the schema or refresh a materialized view.

**Q8 — D: Deletes unreferenced files past retention — limits time travel.** VACUUM removes old files (default 7-day retention), bounding time travel. OPTIMIZE compacts; VACUUM doesn't speed queries directly or rebuild stats.

**Q9 — A: Keys are changeable later without a rewrite; handles high cardinality.** That's why Liquid Clustering is recommended over Z-ORDER/partitioning. It doesn't auto-delete files, doesn't eliminate OPTIMIZE, and isn't external-only.

**Q10 — D: OPTIMIZE, VACUUM, and ANALYZE on Unity Catalog managed tables.** Predictive optimization observes eligible managed tables and schedules these maintenance operations when useful. It does not operate on external tables or temporary views and does not apply Z-ORDER to every table.

**Q11 — B: Mostly not settable — Databricks manages them.** On serverless you generally can't set these knobs. They aren't required manually, set in YAML, or governed by row filters.

**Q12 — C: Longest stage → task-duration distribution → I/O and spill.** Read the biggest stage first, then the task distribution, then I/O/spill counters. Random sampling or driver-logs-only is not the method.

**Q13 — A: The job's run history / matrix view.** Cross-run trends live there; the Spark UI inspects a single run. `DESCRIBE DETAIL` and the Git log are unrelated.
