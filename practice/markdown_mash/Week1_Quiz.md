# Week 1 live Markdown Mash quiz

> Instructor-only. This file is ignored by git and should be launched live during class.

## 7. Markdown Mash Practice Quiz

# Week 1 Quiz: Lakehouse, Delta, and Unity Catalog Foundations
# Score 100

## Q1: A data engineer runs CREATE TABLE sales (id INT, amount DOUBLE) in Databricks without a USING clause. What table format is created?
- [ ] Parquet
- [x] Delta
- [ ] Iceberg
- [ ] CSV-backed external table
::time=20

## Q2: Which sequence correctly orders the Unity Catalog hierarchy from top to bottom?
- [ ] Catalog → metastore → schema → table
- [ ] Metastore → schema → catalog → table
- [ ] Workspace → catalog → table → schema
- [x] Metastore → catalog → schema → table
::time=20

## Q3: A managed table is dropped with DROP TABLE. What happens to its underlying data files?
- [x] They are deleted along with the metadata
- [ ] They remain in storage and must be cleaned up manually
- [ ] They are archived to a backup catalog automatically
- [ ] They are converted to an external table's files
::time=20

## Q4: In the reference my_catalog.finance.invoices, what does finance represent?
- [ ] A catalog
- [ ] A metastore
- [x] A schema
- [ ] A volume
::time=20

## Q5: Which Unity Catalog object is designed to store and govern non-tabular files such as raw CSVs and images?
- [ ] An external table
- [x] A volume
- [ ] A materialized view
- [ ] A Delta share
::time=20

## Q6: A data engineer must create a new Delta table that is immediately populated with the results of a query against an existing table, in a single statement. Which approach should they use?
- [ ] CREATE TABLE followed by COPY INTO
- [ ] CREATE TABLE followed by INSERT INTO ... SELECT
- [ ] CREATE OR REPLACE VIEW wrapping the query
- [x] CREATE TABLE ... AS SELECT (CTAS)
::time=20

## Q7: A colleague says they cannot find the view scratch_results that you created and queried successfully an hour ago. What is the most likely explanation?
- [x] It was created as a TEMP VIEW, so it exists only in your session
- [ ] Views must be refreshed before other users can query them
- [ ] The view was automatically vacuumed after 60 minutes
- [ ] Views are only visible to workspace admins by default
::time=30

## Q8: An analytics team needs to run ad-hoc SQL queries and power BI dashboards with fast startup and automatic scaling, and they write no Python. Which compute is the best fit?
- [ ] An all-purpose cluster shared by the team
- [ ] A job cluster triggered per dashboard refresh
- [x] A serverless SQL warehouse
- [ ] A single-node GPU cluster
::time=30

## Q9: DESCRIBE EXTENDED on a table shows Type: MANAGED. Which statement is true?
- [ ] The data files live in a customer-specified external location
- [x] Unity Catalog governs both the metadata and the data files' storage
- [ ] The table cannot be time traveled
- [ ] DROP TABLE will preserve the data files indefinitely
::time=30

## Q10: After an accidental UPDATE, a data engineer wants to query a Delta table exactly as it was at version 3. Which query is correct?
- [ ] SELECT * FROM events AT VERSION 3
- [ ] SELECT * FROM events.v3
- [ ] RESTORE TABLE events TO VERSION AS OF 3 inside a SELECT
- [x] SELECT * FROM events VERSION AS OF 3
::time=30

## Q11: Which statement about CTAS (CREATE TABLE AS SELECT) is correct?
- [x] The new table's column types are inferred from the query; a column-type list cannot be declared
- [ ] CTAS creates an empty table whose schema must then be populated with INSERT
- [ ] CTAS requires a USING DELTA clause to produce a Delta table
- [ ] CTAS column types are declared in parentheses before AS SELECT
::time=30

## Q12: A table was created with CREATE TABLE ... LOCATION 's3://corp-bucket/data/orders'. The table is then dropped. What is the result?
- [ ] Both metadata and the files at the location are deleted
- [ ] The drop fails because external tables cannot be dropped
- [x] The metadata is removed but the files at the location remain
- [ ] The files are moved into Unity Catalog managed storage
::time=30

## Q13: In a medallion architecture, what is the primary purpose of the bronze layer?
- [ ] Serving aggregated, business-ready metrics to BI tools
- [x] Preserving raw source data with minimal transformation for auditability and reprocessing
- [ ] Storing deduplicated, validated records with enforced types
- [ ] Caching query results for dashboard performance
::time=20

---

### Quiz Answer Key (with explanations)

| # | Answer | Difficulty | Explanation |
|---|--------|-----------|-------------|
| Q1 | Delta | Easy | Delta is the default table format in Databricks; `USING DELTA` is implicit. |
| Q2 | Metastore → catalog → schema → table | Easy | The three-level namespace `catalog.schema.table` sits under one metastore. |
| Q3 | Deleted with metadata | Easy | Managed = UC owns data + metadata; DROP removes both (briefly recoverable with UNDROP). |
| Q4 | Schema | Easy | Middle element of a three-level name is always the schema. |
| Q5 | Volume | Easy | Volumes govern non-tabular/file data; tables govern tabular data. |
| Q6 | CTAS | Applied | Single-statement create-and-populate is the definition of CTAS. COPY INTO and INSERT are two-step. |
| Q7 | TEMP VIEW session scope | Applied | Temp views are session-scoped and invisible to other users/sessions. The other options invent behavior. |
| Q8 | Serverless SQL warehouse | Applied | SQL-only + BI + instant start + autoscaling = SQL warehouse. Clusters are for general code/jobs. |
| Q9 | UC governs metadata + data | Applied | MANAGED means UC-managed storage; drop deletes data; time travel works on all Delta tables. |
| Q10 | VERSION AS OF | Applied | Exact time-travel syntax. RESTORE changes the table; the question asks only to query. |
| Q11 | Schema inferred; no type list | Tricky | The CTAS rule — control types by CASTing in the SELECT. Distractor D is the classic trap. |
| Q12 | Metadata removed, files remain | Tricky | LOCATION ⇒ external table ⇒ DROP is metadata-only. The files become unmanaged residue. |
| Q13 | Raw, minimally transformed | Easy | Bronze = fidelity + replayability; cleaning is silver; aggregation is gold. |

Difficulty mix: 6 easy / 5 applied / 2 tricky ≈ 46% / 38% / 15%. Correct answers distributed across positions 1–4.

---
