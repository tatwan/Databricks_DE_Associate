# Pre-Week 2 quiz — run at 0:00, before class content starts

> Instructor-only. Reviews **Week 1** content. 5 questions, ~4 minutes.

# Week 2 Starter: Week 1 Review
# Score 100

## Q1: Which sequence correctly orders the Unity Catalog hierarchy from top to bottom?
- [ ] Catalog → metastore → schema → table
- [ ] Metastore → schema → catalog → table
- [ ] Workspace → catalog → table → schema
- [x] Metastore → catalog → schema → table
::time=35

## Q2: A managed table is dropped with DROP TABLE. What happens to its underlying data files?
- [x] They are deleted along with the metadata
- [ ] They remain in storage and must be cleaned up manually
- [ ] They are archived to a backup catalog automatically
- [ ] They are converted to an external table's files
::time=35

## Q3: Which statement about CTAS (CREATE TABLE AS SELECT) is correct?
- [x] The new table's column types are inferred from the query; a column-type list cannot be declared
- [ ] CTAS creates an empty table whose schema must then be populated with INSERT
- [ ] CTAS requires a USING DELTA clause to produce a Delta table
- [ ] CTAS column types are declared in parentheses before AS SELECT
::time=35

## Q4: An analytics team needs ad-hoc SQL queries and BI dashboards with fast startup and automatic scaling, and they write no Python. Which compute fits best?
- [ ] An all-purpose cluster shared by the team
- [ ] A job cluster triggered per dashboard refresh
- [x] A serverless SQL warehouse
- [ ] A single-node GPU cluster
::time=35

## Q5: In a medallion architecture, what is the primary purpose of the bronze layer?
- [ ] Serving aggregated, business-ready metrics to BI tools
- [x] Preserving raw source data with minimal transformation for auditability and reprocessing
- [ ] Storing deduplicated, validated records with enforced types
- [ ] Caching query results for dashboard performance
::time=35

---

### Answer Key

| # | Answer | Checks |
|---|--------|--------|
| Q1 | Metastore → catalog → schema → table | Three-level namespace |
| Q2 | Deleted with metadata | Managed DROP semantics |
| Q3 | Schema inferred; no type list | The CTAS rule |
| Q4 | Serverless SQL warehouse | Compute selection |
| Q5 | Raw, minimally transformed | Medallion layer purpose |
