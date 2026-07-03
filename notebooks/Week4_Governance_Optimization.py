# Databricks notebook source
# MAGIC %md
# MAGIC # Week 4 — Governance & Security + Troubleshooting & Optimization
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC Requires: Week 2 `sales_silver` + `week2_customers.json` in your landing volume.
# MAGIC
# MAGIC | Part | Content |
# MAGIC |---|---|
# MAGIC | 1 | Setup |
# MAGIC | 2 | Demo — grants, column mask, row filter, lineage, CLUSTER BY, query profile, VACUUM/UNDROP/time-travel drill, audit logs |
# MAGIC | 3 | **Your lab** — secure and tune BrewMart (TODO cells) |
# MAGIC | 4 | Solutions |

# COMMAND ----------

dbutils.widgets.text("user_schema", "lab1_yourname")
USER_SCHEMA = dbutils.widgets.get("user_schema")
VOL = f"/Volumes/workspace/{USER_SCHEMA}/landing"
spark.sql("USE CATALOG workspace")
spark.sql(f"USE SCHEMA {USER_SCHEMA}")
print(f"Working in workspace.{USER_SCHEMA}")

# COMMAND ----------

# MAGIC %md ## Part 2 — Demo
# MAGIC ### 2.1 A table worth protecting
# MAGIC
# MAGIC **Goal:** build the table we will govern — customer PII (emails, cities) from the Week 2 JSON.
# MAGIC
# MAGIC **Look for:** ~10 customers with **real, readable emails**. Remember what you see now; by 2.3 the same query will behave differently.
# MAGIC
# MAGIC **Why it matters:** every governance feature today answers one question about this table: *who may see what, without making copies?* Views-per-audience make copies of logic; masks and filters put the policy inside the one table.

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE TABLE customers AS
SELECT customer_id, name, loyalty_tier,
       contact.email AS email, contact.city AS city
FROM read_files('{VOL}/week2_customers.json', format => 'json')
""")
display(spark.sql("SELECT * FROM customers ORDER BY customer_id"))

# COMMAND ----------

# MAGIC %md ### 2.2 GRANT → SHOW GRANTS → REVOKE
# MAGIC
# MAGIC **Goal:** run the basic access-control loop and read its audit answer (`SHOW GRANTS`).
# MAGIC
# MAGIC **The chain to remember:** reading a table normally needs **three** privileges — `USE CATALOG` + `USE SCHEMA` + `SELECT`. The classic support ticket "I have SELECT but can't query" is a missing `USE` privilege.
# MAGIC
# MAGIC **Look for:** the grant appears in `SHOW GRANTS`, then disappears after `REVOKE`. Note the backticks: `` `account users` `` — the principal name has a space.
# MAGIC
# MAGIC **Why it matters (exam):** grant to **groups**, not individuals (grants to people don't scale — exam answers favor groups). And know the difference: **REVOKE removes one grant** (access may survive via another group); **DENY overrides everything**, even group-inherited grants.

# COMMAND ----------

# MAGIC %sql
# MAGIC GRANT SELECT ON TABLE customers TO `account users`;
# MAGIC SHOW GRANTS ON TABLE customers;

# COMMAND ----------

# MAGIC %sql
# MAGIC REVOKE SELECT ON TABLE customers FROM `account users`;
# MAGIC SHOW GRANTS ON TABLE customers;
# MAGIC -- Remember: REVOKE removes A grant; DENY overrides ALL grants. Different tools.

# COMMAND ----------

# MAGIC %md ### 2.3 Column mask — two steps: a function that decides, an ALTER that binds
# MAGIC
# MAGIC **Goal:** hide email addresses from everyone outside `support_team` — inside the table itself, with zero copies.
# MAGIC
# MAGIC **The pattern (always two steps):** ① `CREATE FUNCTION` that returns the masked or real value depending on `is_account_group_member(...)` → ② `ALTER TABLE ... SET MASK` binds it to the column.
# MAGIC
# MAGIC **Predict:** you OWN this table. Will you see real emails after binding? Run and see.
# MAGIC
# MAGIC **Look for:** `***@...` in your own results. **Owners are not exempt** — the mask evaluates per query, per user, and storage is untouched. That's why this beats 15 filtered views: one table, no bypass path.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE FUNCTION email_mask(email STRING)
# MAGIC RETURN CASE
# MAGIC   WHEN is_account_group_member('support_team') THEN email
# MAGIC   ELSE regexp_replace(email, '^[^@]+', '***')
# MAGIC END;
# MAGIC
# MAGIC ALTER TABLE customers ALTER COLUMN email SET MASK email_mask;
# MAGIC
# MAGIC SELECT customer_id, name, email FROM customers ORDER BY customer_id;
# MAGIC -- Owner or not: you're not in support_team → ***@... · Masks don't care about your title.

# COMMAND ----------

# MAGIC %md ### 2.4 Row filter — the function returns true → you see the row
# MAGIC
# MAGIC **Goal:** restrict which ROWS are visible, same two-step pattern: a boolean function + `ALTER TABLE ... SET ROW FILTER ... ON (col)`.
# MAGIC
# MAGIC **Predict:** you are not in `all_regions`. How many of the ~10 customers will the next SELECT return?
# MAGIC
# MAGIC **Look for:** only Atlanta rows. The Chicago/Dallas rows still exist on disk — filtering happens at query time, on every access path.
# MAGIC
# MAGIC **Mask vs filter vs ABAC — the one-line discriminators:** hide a COLUMN's values → mask · hide ROWS → filter · same policy across hundreds of tagged tables, managed centrally → ABAC (concept: tag once, policy per tag, applied everywhere current and future).

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE FUNCTION atlanta_only(city STRING)
# MAGIC RETURN is_account_group_member('all_regions') OR city = 'Atlanta';
# MAGIC
# MAGIC ALTER TABLE customers SET ROW FILTER atlanta_only ON (city);
# MAGIC
# MAGIC SELECT customer_id, name, city, email FROM customers;
# MAGIC -- Row count drops. Chicago/Dallas rows still exist on disk — filtered at query time.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Policies unbind as cleanly as they bind
# MAGIC ALTER TABLE customers DROP ROW FILTER;
# MAGIC ALTER TABLE customers ALTER COLUMN email DROP MASK;
# MAGIC SELECT COUNT(*) AS all_rows_back FROM customers;

# COMMAND ----------

# MAGIC %md ### 2.5 Lineage (UI) — Catalog Explorer → your schema → `sales_silver` → **Lineage** tab
# MAGIC
# MAGIC **Goal:** see the lineage UC has been building for you all course, automatically.
# MAGIC
# MAGIC **Look for:** volume files → bronze → silver (+ the Week 3 job node). Table-level AND column-level.
# MAGIC
# MAGIC **Why it matters (exam):** nobody registered anything — UC captures lineage **automatically from actual query execution**. "Lineage requires a third-party scanner" is a planted wrong answer. Use cases: impact analysis, root cause, compliance.

# COMMAND ----------

# MAGIC %md ### 2.6 Liquid Clustering + OPTIMIZE
# MAGIC
# MAGIC **Goal:** create a gold table whose physical layout matches how it will be queried (`WHERE store = ... AND order_date = ...`), then compact it.
# MAGIC
# MAGIC **Why `CLUSTER BY` and not `PARTITIONED BY`:** Liquid Clustering is the current exam answer — keys are changeable later without rewriting the table (`ALTER TABLE ... CLUSTER BY (other_col)`), and it handles high cardinality. Hive-style partitioning (rigid directories) and Z-ORDER (manual re-sorts at OPTIMIZE time) are the legacy contrast.
# MAGIC
# MAGIC **Look for:** `clusteringColumns` in `DESCRIBE DETAIL`. OPTIMIZE metrics will be near-zero on our tiny table — not broken; there's nothing to compact. On Premium+, **predictive optimization** runs OPTIMIZE/VACUUM for you on **UC managed tables** — a big reason managed is the recommendation.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE sales_gold_daily
# MAGIC CLUSTER BY (store, order_date)
# MAGIC AS
# MAGIC SELECT store, order_date,
# MAGIC        ROUND(SUM(line_total), 2) AS revenue,
# MAGIC        COUNT(DISTINCT order_id)  AS orders
# MAGIC FROM sales_silver
# MAGIC WHERE store IS NOT NULL
# MAGIC GROUP BY store, order_date;
# MAGIC
# MAGIC DESCRIBE DETAIL sales_gold_daily;   -- find clusteringColumns

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE sales_gold_daily;
# MAGIC -- Tiny table → near-zero metrics; on Premium, predictive optimization runs this for you, unasked.

# COMMAND ----------

# MAGIC %md ### 2.7 A query worth profiling (guaranteed shuffle) — then open **Query Profile** via Query History
# MAGIC
# MAGIC **Goal:** run a query with a real shuffle, then read its anatomy in **Query History → this query → Query Profile** (serverless's friendlier rendering of the Spark UI).
# MAGIC
# MAGIC **Vocabulary to spot:** scan → aggregate → **exchange** (exchange = shuffle), with rows and time per operator.
# MAGIC
# MAGIC **Why it matters (exam):** the exam DESCRIBES a Spark UI and wants the diagnosis word. Symptom signatures: max task time ≫ median = **skew** (remedy: broadcast the small side / AQE) · big Shuffle Read/Write on a join or groupBy = **heavy shuffle** (broadcast, prune early) · Spill counters > 0 = **spill** (more partitions or more memory). Reading order: longest stage → task duration distribution → I/O and spill counters.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT t.pickup_zip,
# MAGIC        COUNT(*)                              AS trips,
# MAGIC        APPROX_COUNT_DISTINCT(t.dropoff_zip)  AS distinct_dropoffs,
# MAGIC        AVG(t.fare_amount)                    AS avg_fare
# MAGIC FROM samples.nyctaxi.trips t
# MAGIC GROUP BY t.pickup_zip
# MAGIC ORDER BY trips DESC;

# COMMAND ----------

# MAGIC %md ### 2.8 Maintenance & recovery drill — VACUUM, UNDROP, TIMESTAMP AS OF
# MAGIC
# MAGIC **Goal:** run the three table-lifecycle commands you have only *heard about* so far, and lock in what each one does.
# MAGIC
# MAGIC | Command | Does | Does NOT |
# MAGIC |---|---|---|
# MAGIC | `OPTIMIZE` | compacts small files | delete anything |
# MAGIC | `VACUUM` | deletes unreferenced old files (default retention: 7 days) | speed up queries directly — and it **limits time travel** |
# MAGIC | `UNDROP TABLE` | recovers a dropped **managed** table within the retention window | help external tables (their files never left) |
# MAGIC
# MAGIC **Predict:** our tables are days old at most. How many files will VACUUM actually delete?
# MAGIC
# MAGIC **Look for:** VACUUM succeeds and removes ~nothing (everything is inside retention) — the *command shape* is the exam target. The swapped-purpose distractor ("OPTIMIZE deletes old files") should now be un-fallable-for.

# COMMAND ----------

# MAGIC %sql
# MAGIC VACUUM sales_gold_daily;   -- deletes files no longer referenced AND older than retention (7 days)
# MAGIC -- Deep sync with Week 1: vacuumed files = unreachable versions = bounded time travel.

# COMMAND ----------

# MAGIC %md **The undo pair, both directions:** Week 1 you recovered from a bad UPDATE with `RESTORE`. Now recover from a bad DROP with `UNDROP` — and read the past precisely with `TIMESTAMP AS OF` (the sibling of `VERSION AS OF` you have not run yet).

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Drop → recover a scratch MANAGED table (external tables: DROP is metadata-only, no UNDROP needed)
# MAGIC CREATE OR REPLACE TABLE scratch_undrop_demo AS SELECT 1 AS id;
# MAGIC DROP TABLE scratch_undrop_demo;
# MAGIC UNDROP TABLE scratch_undrop_demo;
# MAGIC SELECT * FROM scratch_undrop_demo;   -- back from the dead (within the retention window)

# COMMAND ----------

# Time travel by TIMESTAMP: grab the latest commit time from history, then query "as of" that moment
ts = spark.sql("DESCRIBE HISTORY sales_gold_daily") \
          .selectExpr("max(timestamp) AS ts").collect()[0]["ts"]
print(f"Querying sales_gold_daily as of {ts}")
display(spark.sql(f"SELECT * FROM sales_gold_daily TIMESTAMP AS OF '{ts}'"))
# VERSION AS OF n = by version number · TIMESTAMP AS OF '...' = by moment in time. Same feature, two addresses.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Cleanup the scratch table
# MAGIC DROP TABLE IF EXISTS scratch_undrop_demo;

# COMMAND ----------

# MAGIC %md ### 2.9 Audit logs — who did what, when *(may be restricted in Free Edition)*
# MAGIC
# MAGIC **Goal:** see the audit answer shape: audit events live in **system tables**, queryable with plain SQL — no external logging stack.
# MAGIC
# MAGIC **Look for:** recent events with your identity. If Free Edition blocks `system.access.audit`, the *answer shape* below is still the exam target — read it, don't skip it.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- The audit answer shape (exam target even if restricted in your workspace):
# MAGIC SELECT user_identity, action_name, request_params, event_time
# MAGIC FROM system.access.audit
# MAGIC WHERE event_date = current_date()
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %md ### 2.10 Platform callback — control plane vs compute plane (Domain 1, 2 minutes)
# MAGIC
# MAGIC A Week 1 idea worth locking in before the mock, because today's features straddle it:
# MAGIC
# MAGIC - **Control plane** — managed by Databricks: the web UI, job scheduler, Unity Catalog metastore, compute-management APIs. Your GRANTs, masks, and lineage live *here* (metadata).
# MAGIC - **Compute plane** — where your code executes and touches data. **Classic** compute runs in *your* cloud account; **serverless** runs in a Databricks-managed environment (what Free Edition uses).
# MAGIC
# MAGIC **Exam shapes:** "Where do classic clusters run?" → the customer's cloud account. "Where does serverless run?" → Databricks-managed. "Where is the metastore?" → control plane. One sentence each — cheap points.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 3 — LAB: Secure and Tune the BrewMart Lakehouse
# MAGIC Analysts must never see raw emails; the vendor sees only their store's rows; gold needs a growth-ready layout.
# MAGIC ✅ Task 1 (customers table) was built in the demo — recreate it here if you skipped Part 2.

# COMMAND ----------

# MAGIC %md ### TODO Task 2 — Grant round-trip on your Week 1 view
# MAGIC GRANT SELECT on `sales_by_store` to `account users` → SHOW GRANTS → REVOKE → SHOW GRANTS.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO

# COMMAND ----------

# MAGIC %md ### TODO Task 3 — Mask `customers.email`: `brewmart_support` sees real, others see `***@<domain>`

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: CREATE FUNCTION + ALTER TABLE ... SET MASK ... then SELECT to prove it hits YOU too

# COMMAND ----------

# MAGIC %md ### TODO Task 4 — Row filter on `customers.city`: `brewmart_hq` sees all, others only 'Atlanta'

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: CREATE FUNCTION + ALTER TABLE ... SET ROW FILTER ... ON (city)

# COMMAND ----------

# MAGIC %md ### TODO Task 5 — `sales_gold_daily` with CLUSTER BY (store, order_date) + OPTIMIZE
# MAGIC *(Done in demo — rebuild from memory without scrolling up. That's the exam rep.)*

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO

# COMMAND ----------

# MAGIC %md ### TODO Task 6 — Open lineage on `sales_gold_daily` (UI)
# MAGIC Do this before cleanup so the graph still reflects the governed objects you just created.

# COMMAND ----------

# MAGIC %md ### Validation before cleanup

# COMMAND ----------

# MAGIC %sql
# MAGIC -- While mask is bound: 0 leaked emails
# MAGIC SELECT COUNT(*) AS leaked FROM customers WHERE email NOT LIKE '***%';

# COMMAND ----------

# MAGIC %sql
# MAGIC -- While filter is bound: only Atlanta
# MAGIC SELECT DISTINCT city FROM customers;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Clustering in place
# MAGIC DESCRIBE DETAIL sales_gold_daily;

# COMMAND ----------

# MAGIC %md ### TODO Task 7 — drop the filter + mask, confirm full visibility

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO Task 7

# COMMAND ----------

# MAGIC %sql
# MAGIC -- After cleanup: all customer rows should be visible again
# MAGIC SELECT COUNT(*) AS all_rows_after_cleanup FROM customers;

# COMMAND ----------

# MAGIC %md ### ⭐ Stretch
# MAGIC Second mask: `loyalty_tier` → `'REDACTED'` for non-members of `brewmart_marketing`. Then one paragraph: at what scale does per-table masking break down, and what replaces it? *(Expected: tag-driven ABAC policies.)* Bonus: `EXPLAIN SELECT * FROM sales_gold_daily WHERE store='Atlanta'` — find pruning evidence.

# COMMAND ----------

# MAGIC %md ---
# MAGIC ## Solution
# MAGIC The solution file will be shared by your instructor.
# MAGIC
# MAGIC ✅ Keep your completed schema and tables — the next week builds on them.
