# Pre-Week 3 quiz — run at 0:00, before class content starts

> Instructor-only. Reviews **Week 2** content. 5 questions, ~4 minutes.

# Week 3 Starter: Week 2 Review
# Score 100

## Q1: A query combines two result sets and must keep duplicate rows. Which SQL operator is correct?
- [ ] UNION
- [ ] INTERSECT
- [ ] UNION DISTINCT
- [x] UNION ALL
::time=35

## Q2: A pipeline must ingest millions of small JSON files arriving continuously, with occasional new fields. Which ingestion method fits best?
- [x] Auto Loader with schema evolution enabled
- [ ] COPY INTO on a nightly schedule
- [ ] A managed Lakeflow Connect connector
- [ ] INSERT INTO with read_files in a loop
::time=35

## Q3: A team needs daily Salesforce data in Unity Catalog with minimal engineering effort. What should they use?
- [ ] Auto Loader pointed at Salesforce exports
- [ ] A JDBC connection in a scheduled notebook
- [x] A Lakeflow Connect managed connector
- [ ] COPY INTO from the Salesforce REST API
::time=35

## Q4: A MERGE INTO fails with a "multiple source rows matched" error. What is the root cause?
- [ ] The target table has duplicate keys
- [x] The source has more than one row for the same join key — deduplicate the source first
- [ ] The WHEN NOT MATCHED clause is missing
- [ ] The source and target schemas do not align
::time=35

## Q5: A column favorite_categories contains arrays like ["Kitchen","Appliances"]. What does explode(favorite_categories) return?
- [ ] One concatenated string per row
- [ ] A struct with one field per category
- [x] One output row per array element
- [ ] The array sorted alphabetically
::time=35

---

### Answer Key

| # | Answer | Checks |
|---|--------|--------|
| Q1 | UNION ALL | UNION dedupes; UNION ALL keeps duplicates |
| Q2 | Auto Loader | Millions of files + drift = Auto Loader's signature |
| Q3 | Managed connector | SaaS + zero engineering → most managed layer |
| Q4 | Duplicate source keys | The famous MERGE failure — dedupe the source |
| Q5 | One row per element | explode fans arrays into rows |
