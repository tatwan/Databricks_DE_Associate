# Week 2 Overview — Ingestion, Auto Loader, Bronze→Silver Transformations
# Score 100

## Q1: For an unreliable CSV source, why might a bronze table use **STRING columns** plus audit metadata?
- [ ] To minimize the storage footprint of the bronze table files
- [ ] Because Delta tables cannot store numeric or timestamp types
- [ ] Because COPY INTO can only write string columns
- [x] Preserve raw values for validation in silver
::time=45

## Q2: You run the same `COPY INTO` cell twice against an unchanged folder. How many rows load the second time?
> COPY INTO records which files it has loaded in the target's Delta log.
- [ ] Every row is loaded again from scratch
- [ ] Roughly half of the rows reload
- [ ] It raises a duplicate-file error and stops
- [x] Zero rows
::time=45

## Q3: Which single line makes a Spark read stream an **Auto Loader** stream?
```python
(spark.readStream
   .format("cloudFiles")
   .option("cloudFiles.format", "csv")
   .load(path))
```
- [ ] `.option("cloudFiles.format", "csv")`
- [ ] `.trigger(availableNow=True)`
- [x] `.format("cloudFiles")`
- [ ] `.option("header", "true")`
::time=45

## Q4: What is the purpose of Auto Loader's `checkpointLocation`?
- [x] Streaming progress used for exactly-once processing
- [ ] It stores the output table's data and index files
- [ ] It caches the most recent query results
- [ ] It holds the cluster's configuration settings
::time=45

## Q5: What does `trigger(availableNow=True)` do in a streaming write?
- [ ] It runs the stream continuously, forever
- [x] It processes all available files, then stops
- [ ] It disables the checkpoint for this run
- [ ] It processes exactly one file per trigger
::time=45

## Q6: A JSON record has `contact` as a nested object. How do you select the city inside it?
- [ ] `contact['city']`, which works only in Python
- [x] `contact.city` — a dot path into the STRUCT
- [ ] `explode(contact)` to flatten the object
- [ ] `contact -> city` using an arrow operator
::time=45

## Q7: `explode(favorite_categories)` runs on a column that is an ARRAY of 3 elements for one customer. Rows produced for that customer?
- [ ] 1 row
- [ ] 9 rows
- [x] 3 rows
- [ ] 0 rows
::time=45

## Q8: Which pattern keeps only the **latest** record per key (newest by ingest time)?
- [x] `ROW_NUMBER() OVER (PARTITION BY key ORDER BY ts DESC) = 1`
- [ ] `SELECT DISTINCT` on all columns, keeping an arbitrary copy
- [ ] `GROUP BY key` and return any matching row
- [ ] `COALESCE(key, 'latest')` to fill the key
::time=45

## Q9: `COPY INTO` versus `INSERT INTO ... SELECT read_files(...)` on a scheduled daily run — the key difference?
- [ ] They behave identically on a schedule
- [ ] INSERT is the idempotent one; COPY INTO re-inserts every file each run
- [ ] COPY INTO cannot read from a volume path
- [x] COPY INTO skips already-loaded files; the INSERT reloads everything
::time=45

## Q10: A `MERGE` (update matched, insert unmatched) is run twice with the same source. Second-run result?
> Row-level idempotency: matched rows re-update to the same values; nothing new is inserted.
- [ ] Rows are duplicated on the second run
- [x] No material change; the result converges
- [ ] It raises a "multiple matches" error
- [ ] All target rows are deleted
::time=45

## Q11: A write violates a `CHECK (quantity > 0)` constraint on the table. What happens?
- [ ] Only the offending row is silently skipped
- [ ] The constraint is automatically dropped
- [x] The entire write transaction fails
- [ ] The value is coerced to a default
::time=45

## Q12: In a gold aggregation, which join keeps sales from customers **not** in the customer dimension?
- [x] LEFT JOIN, with `COALESCE` for the missing dimension values
- [ ] INNER JOIN, which quietly drops the unmatched fact rows
- [ ] CROSS JOIN of the fact and the dimension
- [ ] SEMI JOIN on the dimension key
::time=45

## Q13: What is the PySpark equivalent of SQL's `WHERE order_id IS NOT NULL`?
- [ ] `.filter(order_id != NULL)`
- [ ] `.dropna(subset="order_id")` to drop the column
- [ ] `.select("order_id").notnull()`
- [x] `.where(col("order_id").isNotNull())`
::time=45

## Q14: Your `MERGE ... ON t.order_id = s.order_id` fails: "a target row matched multiple source rows." Cause and fix?
- [ ] The target already has duplicate order_ids; add a primary key
- [ ] `read_files` cannot be a MERGE source; stage the file first
- [x] Two source rows share an order_id — dedupe the source first
- [ ] The `ON` clause is wrong; match on every column instead
::time=45
