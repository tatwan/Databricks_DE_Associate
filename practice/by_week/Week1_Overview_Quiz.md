# Week 1 Overview — Lakehouse Foundations, Delta Lake, Unity Catalog
# Score 100

## Q1: In Unity Catalog, what is the correct order of the three-level namespace?
- [ ] `schema.catalog.table`
- [ ] `database.schema.catalog`
- [x] `catalog.schema.table`
- [ ] `table.schema.catalog`
::time=45

## Q2: You run `CREATE TABLE trip_zones (...)` with no `USING` clause and no `LOCATION`. What is created?
> On Databricks, Delta is the default format, and without a LOCATION the table is managed.
- [ ] A temporary view
- [ ] An external Delta table
- [ ] An external Parquet table
- [x] A managed Delta table
::time=45

## Q3: What determines the columns and types of a table built with CTAS (`CREATE TABLE ... AS SELECT`)?
- [ ] It creates an empty table you must INSERT into afterward
- [ ] It requires a separate `(column TYPE, ...)` list before the query
- [ ] It can only read from external files, not from tables
- [x] They come from the SELECT query (use `CAST` to control a type)
::time=45

## Q4: Which command reveals a table's `Type` (MANAGED/EXTERNAL) and `Provider` (delta)?
- [ ] `SHOW TABLES IN` the schema
- [x] `DESCRIBE EXTENDED` on the table
- [ ] `DESCRIBE HISTORY` on the table
- [ ] `SHOW TBLPROPERTIES` on the table
::time=45

## Q5: When you `DROP` a table, how do **managed** and **external** tables differ?
- [x] Managed deletes data + metadata; external deletes metadata only
- [ ] Both delete their files as soon as the table is dropped
- [ ] Managed keeps its files; external deletes its files immediately
- [ ] Both keep their files, because Unity Catalog never deletes data
::time=45

## Q6: You need to read a Delta table as it existed at version 0, without changing it. Which clause?
- [x] `SELECT * FROM t VERSION AS OF 0`
- [ ] `RESTORE TABLE t TO VERSION AS OF 0`
- [ ] `DESCRIBE HISTORY t VERSION 0`
- [ ] `ROLLBACK TABLE t TO 0`
::time=45

## Q7: A bad `UPDATE` corrupted your table. You want to make an old snapshot the **current** state again.
> Time travel *reads* the past; RESTORE *makes* an old version current.
- [ ] `SELECT * FROM t VERSION AS OF 0`
- [x] `RESTORE TABLE t TO VERSION AS OF 0`
- [ ] `UNDROP TABLE t`
- [ ] `VACUUM t`
::time=45

## Q8: In Unity Catalog, which object governs **non-tabular files** such as CSV, JSON, and images?
- [ ] Catalogs
- [ ] Schemas
- [x] Volumes
- [ ] Tables
::time=45

## Q9: Which object can another authorized user query **after your notebook session ends**?
- [x] A persistent view created with `CREATE VIEW`
- [ ] A temporary view created with `CREATE TEMP VIEW`
- [ ] A DataFrame stored in a Python variable in your notebook
- [ ] A widget value set at the top of the notebook
::time=45

## Q10: What is the relationship between Delta and Parquet?
- [ ] Delta is a newer file format that replaces Parquet entirely
- [ ] Parquet is the table format; Delta is a compression codec
- [ ] They are unrelated storage technologies
- [x] Delta is a table format: Parquet files plus a `_delta_log`
::time=45

## Q11: What does `read_files('/Volumes/.../file.csv', format => 'csv', header => true)` do?
- [ ] It permanently registers a new managed table in the catalog
- [x] Rows only; no table is created
- [ ] It moves the file into the table's managed storage location
- [ ] It works only on JSON files, not CSV
::time=45

## Q12: `CREATE TABLE IF NOT EXISTS sales (...)` runs against a table that already exists with data. Result?
- [ ] The existing table is overwritten and its rows are cleared
- [ ] An error is raised because the table already exists
- [x] Nothing changes — it is a safe no-op
- [ ] Only the schema is altered to match the new definition
::time=45

## Q13: Delta transactions are atomic. While an `UPDATE` runs, what do concurrent readers see?
- [ ] Rows updating in real time as the write proceeds
- [ ] An error until the write commits
- [ ] An empty table during the write
- [x] The last committed snapshot — never a partial update
::time=45
