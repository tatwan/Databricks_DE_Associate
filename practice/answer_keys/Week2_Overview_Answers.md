# Week 2 Overview — Answer Key & Explanations

**Q1 — D: Preserve questionable values for later validation.** For an unreliable text source, a permissive bronze schema can keep malformed values and defer strict typing to silver. This is a design option, not a universal rule: well-governed sources can land with typed schemas. Delta supports numeric types, COPY INTO is not string-only, and storage size is not the motivation.

**Q2 — D: Zero.** COPY INTO is idempotent — it records loaded files in the Delta log and skips them on rerun. It does not reload, partially reload, or error on a repeated file.

**Q3 — C: `.format("cloudFiles")`.** That is the switch that makes it Auto Loader. `cloudFiles.format` names the *file* type, `trigger(availableNow=True)` controls cadence, and `header` is a CSV parsing option — none of them turn on Auto Loader.

**Q4 — A: Exactly-once bookkeeping of processed files.** The checkpoint remembers which files are done so reruns don't reprocess. It is not the output table, a result cache, or cluster config.

**Q5 — B: Process all available files, then stop.** `availableNow=True` uses streaming machinery at a batch cadence. It is not continuous, not one-file-at-a-time, and does not disable the checkpoint.

**Q6 — B: `contact.city` (dot into the STRUCT).** On parsed JSON, a dot path reaches into a nested struct. `explode` is for arrays, not structs; the bracket and arrow forms are not how you read a struct field here.

**Q7 — C: 3 rows.** `explode` emits one row per array element, so a 3-element array becomes 3 rows. Not 1, not 0, and not the product 9.

**Q8 — A: `ROW_NUMBER() OVER (PARTITION BY key ORDER BY ts DESC) = 1`.** This deterministically keeps the newest row per key. `DISTINCT` only removes fully identical rows (arbitrary survivor), `GROUP BY` needs aggregates, and `COALESCE` fills NULLs — none pick "latest."

**Q9 — D: COPY INTO skips loaded files; the INSERT reloads everything.** COPY INTO tracks files and is safe to reschedule; `INSERT ... SELECT read_files(...)` re-inserts the whole folder each run. The idempotency belongs to COPY INTO, and it can read volume paths.

**Q10 — B: Nothing changes further.** MERGE is row-level idempotent: matched rows re-update to identical values and no new rows insert, so it converges. It does not duplicate, delete, or error (unless the *source* has duplicate keys — a different problem).

**Q11 — C: The entire write transaction fails.** A CHECK constraint rejects the whole write; it does not skip only the bad row, drop itself, or coerce values. (Quarantine/expectations are what let a pipeline continue.)

**Q12 — A: LEFT JOIN with COALESCE.** A LEFT JOIN keeps every fact row even when the dimension has no match; `COALESCE` supplies a fallback like 'Unknown'. INNER JOIN silently drops unmatched sales (the classic exam bug); CROSS and SEMI joins don't fit the enrich-and-keep goal.

**Q13 — D: `.where(col("order_id").isNotNull())`.** This mirrors `IS NOT NULL`. `!= NULL` is invalid, `dropna(subset=...)` drops rows (not a filter expression and doesn't "drop the column"), and `.select(...).notnull()` is not valid Spark.

**Q14 — C: Two source rows share an order_id — dedupe the source first.** MERGE cannot let one target row match multiple source rows, so a duplicate key in the *source* (the corrections file) raises "a target row matched multiple source rows." The fix is to dedupe the source (e.g., `ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY ... ) = 1`). It is not about a target key, `read_files` is a valid MERGE source, and matching on every column would break the upsert logic entirely.
