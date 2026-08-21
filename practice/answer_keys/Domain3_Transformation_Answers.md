# Domain 3 — Data Transformation & Modeling — Answer Key

**Q1 — B: Via `CAST(...)` in the SELECT.** CTAS derives types from the query. The `(col TYPE, ...)` list is invalid with CTAS; types aren't taken from the file extension, and CTAS can absolutely set types.

**Q2 — D: Rows identical across every column.** DISTINCT removes fully-duplicate rows (arbitrary survivor). Rows that share a key but differ need `ROW_NUMBER`, not DISTINCT; it doesn't target NULLs or "oldest."

**Q3 — A: NULL.** Any arithmetic with a NULL operand yields NULL — not 0, not an error, not the other operand.

**Q4 — A: Return the first non-NULL value; PySpark `coalesce(...)`.** SQL `COALESCE` and `pyspark.sql.functions.coalesce` have the same expression semantics. `fillna` can fill NULL values in a DataFrame, but it is not the direct expression equivalent; `dropna`, `cast`, and `explode` perform different operations.

**Q5 — B: INNER JOIN.** An INNER JOIN drops fact rows with no dimension match — the classic silent-loss bug. LEFT/FULL/RIGHT keep rows from one or both sides.

**Q6 — D: Deduplicate the source.** "Multiple source rows matched" means a key appears more than once in the source; dedup it. Retries, an INNER JOIN, or dropping the target don't fix the cause.

**Q7 — C: A regular view.** A plain view recomputes on every query and stores nothing. A materialized view stores results, a streaming table is for append, and a managed Delta table persists data.

**Q8 — C: A streaming table.** Built for incremental append ingestion. Views recompute, materialized views store aggregations, and temp views are session-scoped.

**Q9 — B: Appends without deduplication and matches by position.** PySpark `DataFrame.union` behaves like SQL `UNION ALL`, not SQL `UNION`, and resolves columns by position. Use `unionByName` when names rather than positions should align; a union is not a key-based join.

**Q10 — C: `count_distinct("customer_id")`.** `count` counts non-NULL rows, while `count_distinct` counts unique non-NULL identifiers. `sum` and `mean` are numeric aggregations and do not answer the uniqueness question.

**Q11 — A: `.withColumn("quantity", col("quantity").cast("int"))`.** This mirrors `CAST(quantity AS INT)`. The other forms use invalid or pandas-style methods that aren't Spark DataFrame API.

**Q12 — C: A broadcast join.** A tiny dimension against a big fact table is the broadcast shape — copy the small side to every executor so the big side never shuffles. Sort-merge/shuffle-hash/cross are not the fit.

**Q13 — D: Drops failing rows and records metrics.** `@dp.expect_or_drop` is the current `pyspark.pipelines` API for a drop policy. `@dp.expect` keeps failing rows and warns, `@dp.expect_or_fail` stops the update, and quarantine requires an explicit flow or table design.
