# Week 5 Cumulative Review — Answer Key & Explanations

**Q1 — C: 45 scored multiple-choice questions in 90 minutes, with possible unscored items.** The exam guide allows unidentified unscored items and factors in additional time for them. There is no live notebook lab, free-response section, or take-home capstone; code can still appear for interpretation.

**Q2 — C: `CAST(order_date AS DATE)` in the SELECT.** CTAS takes types from the query, so you cast explicitly. It does not auto-detect, does not accept a separate column list, and `read_files` has no `dateType` option.

**Q3 — D: Lakeflow Connect.** "Zero engineering / managed connectors" is the Lakeflow Connect trigger phrase. Auto Loader and COPY INTO are file-based ingestion you configure; Delta Sharing is for sharing data out.

**Q4 — A: `ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY _ingested_at DESC) = 1`.** `PARTITION BY` restarts the numbering per order and descending time puts the newest row first. Ascending time keeps the oldest, `RANK` can keep ties, and omitting `PARTITION BY` keeps only one row across the whole dataset.

**Q5 — B: Task 2 didn't break — Task 1 failed.** "Upstream failed" is a dependency status, not a bug in Task 2, an OOM, or a run-if skip.

**Q6 — B: `CLUSTER BY (store, order_date)` (Liquid Clustering).** It matches the filter pattern and stays flexible. Partitioning is rigid/legacy, Z-ORDER is a manual re-sort, and the cache is not a layout strategy.

**Q7 — D: A materialized view.** It stores the computed aggregation and refreshes, so repeated reads are cheap. A plain view recomputes each time, a temp view is session-scoped, and a streaming table is for append ingestion.

**Q8 — A: `bundle deploy -t prod` as a service principal.** CI deploys the bundle to prod authenticated as a service principal on merge. The PR is created in the provider (not the workspace), deploy precedes run (not validate after deploy in that framing), and code is not edited per environment — only variable overrides differ.

**Q9 — B: Schema evolution backed by the schema location.** Auto Loader persists inferred schema metadata at `cloudFiles.schemaLocation` and applies the configured evolution behavior when new columns appear. A trigger starts work, a dashboard task refreshes BI, and ownership changes governance rather than schema handling.

**Q10 — C: Ensure no group they're in holds the grant — UC has no DENY.** Unity Catalog has no DENY override, so the real guarantee is that no group the contractor belongs to (and no direct grant) holds SELECT. `DENY SELECT` is the trap — it's legacy hive_metastore only. A blind REVOKE can be re-granted via a group, and changing ownership doesn't block reads.

**Q11 — A: Data skew.** Median 30s with a 28-minute max is the textbook skew signature (one giant partition). Spill, driver OOM, and library conflicts have different symptoms.

**Q12 — D: SQL UNION deduplicates; PySpark union appends by position.** PySpark `DataFrame.union()` behaves like SQL `UNION ALL`; it neither removes duplicates nor matches columns by name. Use `unionByName()` for name-based alignment, and use a join when rows must match on keys.

**Q13 — B: A REST client in a notebook, orchestrated with Lakeflow Jobs.** Unsupported APIs with custom pagination need explicit client logic plus production scheduling and monitoring. COPY INTO reads files, a row filter controls visibility, and a trigger without an ingestion task moves no data.
