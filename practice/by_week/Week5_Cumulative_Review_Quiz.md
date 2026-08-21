# Week 5 Cumulative Review — Capstone & Exam Readiness (Mixed Domains)
# Score 100

## Q1: Which statement accurately describes the current Databricks Certified Data Engineer Associate exam?
- [ ] A live hands-on coding lab inside a notebook
- [ ] 60 free-response written questions
- [x] 45 scored MCQs in 90 minutes; unscored items may appear
- [ ] A take-home capstone project reviewed by a proctor
::time=45

## Q2: A CTAS reads a CSV where every field is text. How do you produce a typed `DATE` column?
- [ ] Declare the column list before `AS SELECT`
- [ ] CTAS auto-detects the date type from the file
- [x] `CAST(order_date AS DATE)` inside the SELECT
- [ ] Use `read_files` with a `dateType => true` option
::time=45

## Q3: Which option has the least operational overhead for a supported SaaS or database source?
- [ ] Auto Loader with cloudFiles
- [ ] COPY INTO on a schedule
- [ ] Delta Sharing configured against the source
- [x] A Lakeflow Connect managed connector
::time=45

## Q4: You must keep the most recent record per `order_id`. Which is correct?
- [x] `ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY _ingested_at DESC) = 1`
- [ ] `ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY _ingested_at ASC) = 1`
- [ ] `RANK() OVER (PARTITION BY order_id ORDER BY _ingested_at DESC) = 1`
- [ ] `ROW_NUMBER() OVER (ORDER BY _ingested_at DESC) = 1`
::time=45

## Q5: A job's Task 2 (`depends_on` Task 1) shows **Upstream failed**. What does that mean?
- [ ] Task 2 has a genuine bug in its own code
- [x] Task 2 didn't break — its dependency (Task 1) failed
- [ ] The cluster ran out of memory mid-task
- [ ] Task 2 was skipped by a run-if condition you configured
::time=45

## Q6: Best layout for a large gold table queried by `WHERE store = ... AND order_date = ...`?
- [ ] `PARTITIONED BY (order_date)` into rigid directories
- [x] `CLUSTER BY (store, order_date)` — Liquid Clustering
- [ ] `ZORDER BY (store)` at every write
- [ ] No layout — rely on the query cache
::time=45

## Q7: Which gold object best serves an expensive aggregation queried 200 times per hour?
> A materialized view stores the computed result and refreshes; a plain view recomputes each time.
- [ ] A temporary session view
- [ ] A regular view that recomputes on every query
- [ ] A streaming table appended to continuously
- [x] A materialized view (stores the computed result)
::time=45

## Q8: A CI pipeline promotes to production on merge to main. Which action is correct?
- [x] `bundle deploy -t prod` via a service principal
- [ ] It creates the pull request in the workspace UI
- [ ] It runs `deploy`, then `validate`, in that order
- [ ] It edits the notebook code separately for each environment
::time=45

## Q9: An Auto Loader source adds a new field. Which feature controls how that new field is handled across runs?
- [ ] A table update trigger
- [x] Configured schema evolution
- [ ] A dashboard refresh task
- [ ] A Unity Catalog ownership transfer
::time=45

## Q10: In **Unity Catalog**, how do you stop a contractor from reading a table?
- [ ] `REVOKE SELECT`, then hope no group re-grants it
- [ ] `DENY SELECT`, which overrides all grants in UC
- [x] Remove every direct and inherited grant
- [ ] `ALTER TABLE ... OWNER TO` a different principal
::time=45

## Q11: A Spark UI stage shows "median 30s, max 28 minutes." The diagnosis is…
- [x] Data skew
- [ ] Disk spill
- [ ] Driver OOM
- [ ] A library conflict
::time=45

## Q12: Which statement correctly compares SQL `UNION` with PySpark `DataFrame.union()`?
- [ ] Both remove duplicates automatically
- [ ] Both match columns by name automatically
- [ ] PySpark `union()` performs a key-based join
- [x] `UNION` deduplicates; `union()` appends by position
::time=45

## Q13: A source is unsupported by managed connectors and requires custom REST pagination. Which design fits best?
- [ ] COPY INTO directly against the HTTPS endpoint
- [x] A REST notebook orchestrated with Lakeflow Jobs
- [ ] A row filter on the destination table
- [ ] A file arrival trigger with no ingestion task
::time=45
