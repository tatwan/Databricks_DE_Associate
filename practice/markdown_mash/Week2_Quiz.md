# Week 2 quiz — run in the closing segment, end of class

> Instructor-only. Covers **Week 2** content. End quiz: 8 questions, ~7 minutes, run live.
> The Self-Review Bank below is assigned as homework, not run live.
> The prior-week review quiz is in `Pre_Week2_Quiz.md` (run at 0:00).

---

## END QUIZ — Week 2 Content (run at ~1:50)

# Week 2 Quiz: Ingestion and Bronze→Silver Transformations
# Score 100

## Q1: A data engineer runs the same COPY INTO command twice in a row with no new files added. What happens on the second run?
- [ ] The target table doubles in size
- [ ] The command fails with a duplicate-file error
- [x] No new rows are loaded because already-ingested files are skipped
- [ ] The table is truncated and reloaded
::time=35

## Q2: Which format keyword identifies Auto Loader in a Structured Streaming read?
- [x] cloudFiles
- [ ] autoLoader
- [ ] deltaStream
- [ ] copyFiles
::time=35

## Q3: What is the purpose of the _rescued_data column produced by Auto Loader?
- [ ] It stores the filename and ingestion timestamp of each row
- [x] It captures data that did not match the expected schema instead of dropping it
- [ ] It holds rows quarantined by CHECK constraints
- [ ] It backs up each row before schema evolution
::time=35

## Q4: Which SQL command updates matching rows and inserts non-matching rows from a source into a Delta table in a single atomic operation?
- [ ] UPSERT INTO
- [x] MERGE INTO
- [ ] INSERT OVERWRITE
- [ ] APPLY CHANGES
::time=35

## Q5: A silver table must keep only the most recent record per customer_id based on updated_at. Which approach is correct?
- [ ] SELECT DISTINCT customer_id FROM source
- [ ] GROUP BY customer_id with MAX(updated_at) selecting all columns
- [ ] dropDuplicates() with no arguments
- [x] ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) and keep rows where it equals 1
::time=35

## Q6: A 6 MB store-dimension table is joined to a 900 GB sales fact table and the join is slow due to shuffling. What should the engineer consider?
- [ ] Converting the join to a cross join
- [x] A broadcast join so the small table is sent to every executor
- [ ] Splitting the fact table into multiple UNION ALL branches
- [ ] Increasing spark.sql.shuffle.partitions to shuffle faster
::time=35

## Q7: A nightly job loads ~50 CSV files from a volume into a Delta table. The team works exclusively in SQL and needs safe reruns. Which option is BEST?
- [x] COPY INTO with the volume path as source
- [ ] Auto Loader with file notification mode
- [ ] A Lakeflow Connect managed connector
- [ ] CREATE OR REPLACE TABLE with read_files each night
::time=35

## Q8: A table has CHECK (quantity > 0). A batch INSERT of 1,000 rows includes 3 rows with quantity = -1. What is the result?
- [ ] 997 rows are inserted and 3 are skipped
- [x] The entire INSERT fails and no rows are written
- [ ] 997 rows are inserted and 3 go to _rescued_data
- [ ] The constraint converts the negative values to NULL
::time=35

### End Quiz Answer Key (with explanations)

| # | Answer | Difficulty | Explanation |
|---|--------|-----------|-------------|
| Q1 | No new rows | Easy | COPY INTO tracks loaded files; reruns skip them — its defining idempotency feature. |
| Q2 | cloudFiles | Easy | `format("cloudFiles")` is the Auto Loader source; the others are invented. |
| Q3 | Captures non-conforming data | Easy | `_rescued_data` keeps mismatched values rather than dropping/failing. |
| Q4 | MERGE INTO | Easy | The atomic upsert statement. UPSERT INTO doesn't exist; APPLY CHANGES is a declarative-pipeline CDC construct. |
| Q5 | ROW_NUMBER = 1 | Applied | Only the window-function pattern controls *which* duplicate survives. |
| Q6 | Broadcast join | Applied | Small-dim-to-big-fact under the broadcast threshold eliminates the shuffle of the large side. |
| Q7 | COPY INTO | Tricky | Auto Loader also *works* — but "SQL-only + ~50 files + scheduled + rerun-safe" makes COPY INTO the *best* (simplest sufficient) answer. |
| Q8 | Entire INSERT fails | Tricky | Constraints are transactional contracts: one violation aborts the whole write. Skipping/quarantining requires explicit patterns or expectations with DROP. |

---

## SELF-REVIEW BANK — assign as homework (not run live)

# Week 2 Self-Review
# Score 100

## Q1: A query combines two result sets and must keep duplicate rows. Which SQL operator is correct?
- [ ] UNION
- [ ] INTERSECT
- [ ] UNION DISTINCT
- [x] UNION ALL
::time=20

## Q2: A pipeline must ingest millions of small JSON files arriving continuously in cloud storage, with occasional new fields appearing in the data. Which ingestion method fits best?
- [x] Auto Loader with schema evolution enabled
- [ ] COPY INTO on a nightly schedule
- [ ] A managed Lakeflow Connect connector
- [ ] INSERT INTO with read_files in a loop
::time=30

## Q3: A team needs daily Salesforce data in Unity Catalog and wants the most managed solution with minimal engineering effort. What should they use?
- [ ] Auto Loader pointed at Salesforce exports
- [ ] A JDBC connection in a scheduled notebook
- [x] A Lakeflow Connect managed connector
- [ ] COPY INTO from the Salesforce REST API
::time=30

## Q4: A column favorite_categories contains arrays like ["Kitchen","Appliances"]. What does explode(favorite_categories) return?
- [ ] One concatenated string per row
- [ ] A struct with one field per category
- [x] One output row per array element
- [ ] The array sorted alphabetically
::time=20

## Q5: Auto Loader is running with default schema evolution (addNewColumns). A new column appears in incoming files. What happens?
- [ ] The new column is silently dropped from all rows
- [ ] All new files are routed to _rescued_data permanently
- [ ] The stream continues and the column appears automatically mid-run
- [x] The stream stops with a schema-change error and picks up the new column on restart
::time=30

## Q6: Customer records contain a struct column contact with fields email and city. After reading the JSON with read_files, which expression selects the city?
- [ ] contact->city
- [ ] explode(contact).city
- [x] contact.city
- [ ] city FROM LATERAL contact
::time=20

## Q7: A gold revenue view was changed from LEFT JOIN to INNER JOIN against the customer dimension, and total revenue decreased. Why?
- [ ] INNER JOIN deduplicates the fact table before aggregating
- [x] Sales rows with no matching customer_id in the dimension were silently dropped
- [ ] INNER JOIN applies constraints that reject unmatched rows
- [ ] The broadcast threshold excluded some fact rows from the join
::time=30

### Self-Review Answer Key

| # | Answer | Explanation |
|---|--------|-------------|
| Q1 | UNION ALL | UNION dedupes; UNION ALL preserves duplicates (cheaper, too). |
| Q2 | Auto Loader | "Millions of files + continuous + evolving schema" are Auto Loader's signature constraints. |
| Q3 | Managed connector | SaaS source + most-managed requirement → Lakeflow Connect managed connector. |
| Q4 | One row per element | explode fans arrays into rows; it does not touch structs or order. |
| Q5 | Stops, then succeeds on restart | addNewColumns fails the stream intentionally; the schema location is updated so the restart proceeds. |
| Q6 | contact.city | Dot syntax navigates parsed structs (colon syntax is for raw JSON strings). |
| Q7 | Unmatched rows dropped | INNER JOIN keeps only matches — the exam's favorite silent join bug. LEFT JOIN + COALESCE keeps and labels them. |

---
