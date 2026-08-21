# Exam Domain 3 — Data Transformation & Modeling (~22%)
# Score 100

## Q1: A CTAS statement controls output column types how?
- [ ] Automatically, from the file's extension
- [x] Via `CAST(...)` expressions inside the SELECT
- [ ] From a `(col TYPE, ...)` list before `AS SELECT`
- [ ] It cannot set column types at all
::time=45

## Q2: What does `SELECT DISTINCT` remove?
- [ ] Rows sharing one key but differing elsewhere
- [ ] NULL values in any column
- [ ] The oldest duplicate, keeping the newest
- [x] Rows that are identical across every column
::time=45

## Q3: Arithmetic with a NULL operand (e.g., `quantity * unit_price` when price is NULL) returns…
- [x] NULL
- [ ] 0
- [ ] An error at runtime
- [ ] The non-null operand's value
::time=45

## Q4: Which PySpark expression directly mirrors `COALESCE(store, 'Unknown')`?
- [x] `coalesce(col("store"), lit("Unknown"))`
- [ ] Casts the column; PySpark `.cast()`
- [ ] Deletes rows containing NULLs; PySpark `dropna()`
- [ ] Explodes an array; PySpark `explode()`
::time=45

## Q5: Which join silently **drops** sales whose customer is missing from the dimension?
- [ ] LEFT JOIN, keeping unmatched fact rows
- [x] INNER JOIN
- [ ] FULL OUTER JOIN on both sides
- [ ] RIGHT JOIN favoring the dimension
::time=45

## Q6: A `MERGE` errors with "multiple source rows matched." The fix is to…
- [ ] Add more task retries to the running job
- [ ] Switch the join to an INNER JOIN
- [ ] Drop and recreate the target table first
- [x] Deduplicate the source keys
::time=45

## Q7: Which gold object recomputes fresh every time it is queried, storing no result?
- [ ] A streaming table
- [ ] A materialized view
- [x] A regular view
- [ ] A managed Delta table
::time=45

## Q8: Which object is ideal for **incremental append ingestion**?
- [ ] A temporary session view
- [ ] A regular (recomputed) view
- [x] A streaming table
- [ ] A materialized aggregation view
::time=45

## Q9: In PySpark, what is true of `left_df.union(right_df)`?
- [ ] It removes duplicate rows like SQL `UNION`
- [x] It appends by position without deduplication
- [ ] It joins rows by matching key values
- [ ] It matches columns by name automatically
::time=45

## Q10: Which aggregation counts **unique** customer identifiers in a PySpark DataFrame?
- [ ] `sum("customer_id")`
- [ ] `count("customer_id")`
- [x] `count_distinct("customer_id")`
- [ ] `mean("customer_id")`
::time=45

## Q11: The PySpark mirror of `CAST(quantity AS INT)` is…
- [x] `.withColumn("quantity", col("quantity").cast("int"))`
- [ ] `.select("quantity").cast(IntegerType())`
- [ ] `.astype("quantity", "integer")` (pandas style)
- [ ] `.cast("quantity", "int")`
::time=45

## Q12: A 10-row dimension joined to a large fact table is the classic shape for which optimization?
- [ ] A sort-merge join with more partitions
- [ ] A shuffle-hash join across executors
- [x] A broadcast join (`/*+ BROADCAST(dim) */`)
- [ ] A cross join of both sides
::time=45

## Q13: In current Lakeflow Spark Declarative Pipelines Python, what does `@dp.expect_or_drop("valid_id", "order_id IS NOT NULL")` do?
- [ ] Stops the update as soon as one row fails
- [ ] Keeps failing rows and records only a warning
- [ ] Copies failing rows into a quarantine table automatically
- [x] Drops failing rows and records expectation metrics
::time=45
