# Exam Domain 2 — Data Ingestion & Loading (~21%)
# Score 100

## Q1: `COPY INTO` is run a second time on an unchanged source folder. Result?
- [ ] It reloads every row in the folder again
- [ ] It raises a duplicate-file error and stops
- [x] 0 rows
- [ ] It truncates the table first, then reloads
::time=45

## Q2: Which statement is **NOT** idempotent for scheduled ingestion?
- [ ] `COPY INTO t FROM ...`
- [ ] Auto Loader with a checkpoint
- [ ] `CREATE OR REPLACE TABLE t AS SELECT ...`
- [x] `INSERT INTO t SELECT * FROM read_files(...)`
::time=45

## Q3: What makes a read stream an **Auto Loader** stream?
- [ ] `.trigger(availableNow=True)`
- [x] `.format("cloudFiles")`
- [ ] `.option("header", "true")`
- [ ] `.writeStream` on the query
::time=45

## Q4: The Auto Loader option `cloudFiles.schemaLocation` stores…
- [x] The inferred schema, remembered across runs
- [ ] The output table's data and index files
- [ ] The compute cluster's configuration
- [ ] The pipeline's audit log
::time=45

## Q5: What does the `_rescued_data` column capture in Auto Loader?
- [ ] Rows that were deleted during the load
- [ ] Duplicate rows found across files
- [x] Values that don't fit the inferred schema
- [ ] The timestamp each row was ingested
::time=45

## Q6: A file arrives at unpredictable times; an hourly poll usually finds nothing. Best trigger?
- [ ] A scheduled cron trigger
- [ ] A continuous, always-on stream
- [ ] A manual run only, on demand
- [x] A file arrival trigger
::time=45

## Q7: Which option provides the least operational overhead for a **supported** SaaS or database source?
- [ ] Auto Loader with cloudFiles
- [x] A Lakeflow Connect managed connector
- [ ] COPY INTO on a schedule
- [ ] A MERGE-based upsert
::time=45

## Q8: How do Lakeflow Connect **standard** connectors differ from managed connectors?
- [ ] Standard connectors always require a third-party ingestion product
- [ ] Managed connectors offer more pipeline-code customization
- [x] Standard = more customization; managed = more automation
- [ ] There is no difference between the two connector categories
::time=45

## Q9: A source has no suitable managed connector and exposes a REST API with custom pagination. What is the best fit?
- [ ] COPY INTO pointed directly at the API endpoint
- [x] A REST notebook orchestrated with Lakeflow Jobs
- [ ] A table update trigger without any ingestion code
- [ ] A Unity Catalog row filter on the destination
::time=45

## Q10: `trigger(availableNow=True)` gives you…
- [ ] A stream that runs continuously and never stops on its own
- [x] Process available data, then stop
- [ ] One row processed per trigger interval
- [ ] A cron-scheduled batch job under the hood
::time=45

## Q11: When choosing an ingestion method, what is the recommended starting point?
- [ ] Start with custom REST code for every source
- [ ] Always choose continuous streaming, regardless of latency needs
- [x] The most managed option that meets the requirements
- [ ] Choose the tool with the largest number of configuration settings
::time=45

## Q12: You add one new file to a folder already loaded by COPY INTO, then rerun. What loads?
- [x] Only the new file's rows
- [ ] Every file in the folder, again
- [ ] Nothing at all loads
- [ ] The whole folder is loaded twice
::time=45

## Q13: Which read pattern turns each element of a nested-JSON array into its own row?
- [ ] `array_col.*` to expand every element
- [ ] `flatten_json(array_col)` to unpack it
- [ ] `unnest(array_col)` in SQL
- [x] `explode(array_col)`
::time=45
