# Week 4 Overview — Answer Key & Explanations

**Q1 — C: A missing `USE CATALOG` or `USE SCHEMA` privilege.** Reading needs the full chain USE CATALOG + USE SCHEMA + SELECT. Having only SELECT is the classic "I can't query" ticket. Table type, masks, and a stopped warehouse produce different symptoms.

**Q2 — C: REVOKE removes a grant; DENY is legacy hive_metastore only, not UC.** Unity Catalog does **not** support DENY, so there is no "override all grants" — REVOKE removes a grant and access may still persist via another group. The "DENY overrides everything" idea is the exam-guide framing that current UC docs contradict; in UC you manage access with groups, REVOKE, masks/row filters, and ABAC.

**Q3 — B: Groups.** Grants to groups scale and are the exam-preferred answer. Per-user grants don't scale; restricting to admins or service principals only is wrong.

**Q4 — A: Masked values — owners are not automatically exempt.** This table-level mask evaluates the invoking user's group membership, so the owner sees `***` unless the function explicitly allows that identity. Ownership alone does not produce real values, an error, or forced NULLs.

**Q5 — D: Create a function that decides, then `ALTER TABLE ... SET MASK`.** Always two steps — a function returning masked/real value, then binding it to the column (same pattern for row filters with `SET ROW FILTER`). It is not a single GRANT, a three-step view dance, or automatic.

**Q6 — D: A tag-driven Unity Catalog ABAC policy.** ABAC centralizes a row-filter or column-mask policy and applies it to all matching tagged data. Per-user views, per-column manual bindings, and individual grants do not scale to thousands of tables.

**Q7 — B: Liquid Clustering (`CLUSTER BY`).** It is the current recommendation: keys are changeable later without rewriting, and it handles high cardinality. Partitioning and Z-ORDER are the legacy contrast; bucketing is not the answer here.

**Q8 — A: Deletes unreferenced files past retention — limits time travel.** VACUUM removes old files (default 7-day retention), which bounds how far back you can time travel. OPTIMIZE is the one that compacts; VACUUM does not speed queries directly or rebuild the table.

**Q9 — C: A managed table, within the retention window.** UNDROP recovers a dropped *managed* table. External tables never lost their files (nothing to undrop), and temp/streaming-only options are wrong.

**Q10 — B: Data skew.** Max task time far above the median means one partition is huge — skew. Spill shows as spill counters, a "missing index" isn't a Spark concept, and driver OOM is a driver-side symptom.

**Q11 — D: Driver out-of-memory.** `collect()`/`toPandas()` pull all rows to the driver, risking driver OOM while executors stay healthy. It is not skew, a shuffle blow-up, or a schema mismatch.

**Q12 — A: Metastore = control plane; classic compute = the customer's cloud account.** The metastore, scheduler, and UI live in the Databricks-managed control plane; classic compute runs in the customer account (serverless runs in Databricks-managed). The other pairings misplace one or both.

**Q13 — C: A job cluster.** Job clusters spin up per run and terminate after, avoiding idle interactive-compute time. Actual cost still depends on workload and pricing; the exam discriminator here is lifecycle, not a universal price guarantee.
