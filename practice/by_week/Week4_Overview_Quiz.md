# Week 4 Overview — Governance, Security, Troubleshooting, Optimization
# Score 100

## Q1: A user has `SELECT` on a table but still cannot query it. Most likely cause?
> The read chain is USE CATALOG + USE SCHEMA + SELECT — all three or no access.
- [ ] The table is external, not managed
- [ ] The table has a column mask applied
- [x] A missing `USE CATALOG` or `USE SCHEMA` privilege
- [ ] The SQL warehouse serving the query is stopped
::time=45

## Q2: In **Unity Catalog**, how do `REVOKE` and `DENY` differ?
- [ ] Both DENY and REVOKE override grants inherited via a group
- [ ] DENY blocks all access, while REVOKE only hides columns
- [x] `REVOKE` removes a grant; `DENY` is unsupported in UC
- [ ] They are simply two names for the very same operation
::time=45

## Q3: Exam best practice: privileges should be granted to…
- [ ] Individual users, one at a time
- [x] Groups
- [ ] The metastore admin only
- [ ] Service principals exclusively
::time=45

## Q4: A column mask is bound to `email`. You are the table **owner** but not in the allowed group. You see…
- [x] Masked values — owners are not exempt
- [ ] Real values, because you own the table
- [ ] An error, since owners cannot be masked
- [ ] Only NULLs in the masked column
::time=45

## Q5: What are the two steps to apply a column mask (or row filter)?
- [ ] It is automatic once the column is tagged
- [ ] Three steps: build a view, grant on it, then revoke
- [ ] A single `GRANT` on the column
- [x] Create a policy function, then bind it with `ALTER TABLE`
::time=45

## Q6: One masking policy must apply to every column tagged `pii` across thousands of tables. What should you use?
- [ ] A separate filtered view for each user
- [ ] One manually bound function per column
- [ ] Direct grants to each individual user
- [x] A Unity Catalog ABAC policy driven by tags
::time=45

## Q7: Which layout technique is the current recommendation, with keys changeable later without rewriting the table?
- [ ] Hive-style `PARTITIONED BY` directories
- [x] Liquid Clustering (`CLUSTER BY`)
- [ ] `ZORDER BY`, re-sorted at each OPTIMIZE
- [ ] Bucketing on a hash of the key
::time=45

## Q8: What does `VACUUM` do, and what is its side effect?
- [x] Deletes old files and limits time travel
- [ ] Compacts many small files together but never deletes any data
- [ ] Directly speeds up every query on the table
- [ ] Rebuilds the whole table from scratch
::time=45

## Q9: `UNDROP TABLE` can recover which kind of table within the retention window?
- [ ] An external table whose files were removed
- [ ] A temporary view only
- [x] A managed table, within the retention window
- [ ] A streaming table only
::time=45

## Q10: In a Spark UI stage, **max task time ≫ median task time** points to which problem?
- [ ] Disk spill to local storage
- [x] Data skew
- [ ] A missing table index
- [ ] Driver out-of-memory
::time=45

## Q11: `collect()` or `toPandas()` on a huge DataFrame most directly risks…
- [ ] Executor-side data skew on one partition
- [ ] A shuffle that explodes in size
- [ ] A schema mismatch on read
- [x] Driver out-of-memory
::time=45

## Q12: Where does the Unity Catalog metastore live, and where does **classic** compute run?
- [x] Metastore = control plane; classic compute = the customer's cloud account
- [ ] Both live in the customer's cloud account
- [ ] Both live in the Databricks control plane
- [ ] The metastore runs in the compute plane; classic compute in the control plane
::time=45

## Q13: For a nightly scheduled production job, which compute avoids an always-on interactive cluster's idle time?
- [ ] An always-on all-purpose cluster shared by the team
- [ ] A large shared interactive cluster
- [x] A job cluster — created per run, terminated after
- [ ] A serverless SQL warehouse kept running overnight
::time=45
