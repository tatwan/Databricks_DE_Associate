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

# Note: read_files() is available in SQL from DBR 13+ (all of Free Edition serverless).
# On an older runtime elsewhere you would read JSON via spark.read.json(...) instead.
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
# MAGIC **Why it matters (exam):** grant to **groups**, not individuals (grants to people don't scale — exam answers favor groups). `REVOKE` removes one grant, so access can survive through another group.

# COMMAND ----------

# MAGIC %sql
# MAGIC GRANT SELECT ON TABLE customers TO `account users`;
# MAGIC SHOW GRANTS ON TABLE customers;

# COMMAND ----------

# MAGIC %sql
# MAGIC REVOKE SELECT ON TABLE customers FROM `account users`;
# MAGIC SHOW GRANTS ON TABLE customers;
# MAGIC -- REVOKE removes one grant; another inherited grant may still allow access.

# COMMAND ----------

# MAGIC %md ### 2.2b The exam-guide `DENY` contradiction — know the platform truth
# MAGIC
# MAGIC The May 4, 2026 exam guide names **GRANT, REVOKE, and DENY** under Governance & Security. Current Databricks SQL documentation is explicit: **`DENY` is not supported by Unity Catalog**; it applies only to objects in the legacy `hive_metastore` catalog.
# MAGIC
# MAGIC | Verb | Effect |
# MAGIC |---|---|
# MAGIC | `GRANT` | give a privilege to a principal |
# MAGIC | `REVOKE` | remove **one** grant — access may still survive via another group the user is in |
# MAGIC | `DENY` | legacy `hive_metastore` only; invalid for Unity Catalog objects |
# MAGIC
# MAGIC ```sql
# MAGIC -- Legacy only; do not run this against a Unity Catalog table:
# MAGIC DENY SELECT ON TABLE hive_metastore.legacy.customers TO `contractors`;
# MAGIC ```
# MAGIC
# MAGIC **Unity Catalog answer:** use the privilege chain, group design, `REVOKE`, row filters, column masks, ABAC policies, and workspace bindings. If a question explicitly says the object is in Unity Catalog, `DENY` is not valid SQL for that object. Keep this note because the guide and product reference currently disagree.

# COMMAND ----------

# MAGIC %md ### 2.2c INFORMATION_SCHEMA — read the catalog with plain SQL
# MAGIC **Goal:** see that catalog metadata (tables, columns, privileges) is itself queryable — no special API.
# MAGIC
# MAGIC **Why it matters (exam):** "programmatically list every table in a schema / audit who has which grant" → query `information_schema`, scoped to the current catalog. It is the SQL-standard cousin of Catalog Explorer.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Every table in your schema, straight from catalog metadata
# MAGIC SELECT table_name, table_type
# MAGIC FROM information_schema.tables
# MAGIC WHERE table_schema = current_schema()
# MAGIC ORDER BY table_name;

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

# MAGIC %md ### 2.6b Z-ORDER — the legacy contrast, so you recognize it on the exam
# MAGIC **Goal:** run the *older* data-skipping command once, so `OPTIMIZE ... ZORDER BY` is not just a name.
# MAGIC
# MAGIC **The three layouts the exam contrasts:**
# MAGIC
# MAGIC | Technique | How you set it | Status |
# MAGIC |---|---|---|
# MAGIC | **Liquid Clustering** | `CLUSTER BY (cols)` — changeable later, high-cardinality-safe | **current recommendation** |
# MAGIC | **Z-ORDER** | `OPTIMIZE t ZORDER BY (cols)` — a manual re-sort, redone at each OPTIMIZE | legacy |
# MAGIC | **Hive partitioning** | `PARTITIONED BY (col)` — rigid directories, dies on high cardinality | legacy |
# MAGIC
# MAGIC **Exam rule:** don't combine `CLUSTER BY` with `ZORDER` on the same table — Liquid Clustering *replaces* Z-ORDER. This cell runs on a throwaway copy so it doesn't fight the clustered `sales_gold_daily`.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Z-ORDER shown on a scratch copy (a NON-clustered table) for recognition only
# MAGIC CREATE OR REPLACE TABLE sales_gold_zorder_demo AS SELECT * FROM sales_gold_daily;
# MAGIC OPTIMIZE sales_gold_zorder_demo ZORDER BY (store);
# MAGIC DROP TABLE IF EXISTS sales_gold_zorder_demo;

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

# MAGIC %md ### 2.10b Compute types — which one for which job (Domain 1, exam anchor)
# MAGIC
# MAGIC The guide lists compute *selection* and cost model explicitly. Four things to tell apart:
# MAGIC
# MAGIC | Compute | Runs | Use it for | Cost note |
# MAGIC |---|---|---|---|
# MAGIC | **All-purpose cluster** | interactive, shared by people | notebooks, dev, exploration | most expensive per job — it lingers |
# MAGIC | **Job cluster** | created per run, terminated after | scheduled production jobs | cheapest for production — no idle time |
# MAGIC | **SQL warehouse** | SQL only (Serverless / Pro / Classic) | BI, dashboards, ad-hoc SQL | Serverless = instant start, auto-scale |
# MAGIC | **Serverless (jobs/notebooks)** | Databricks-managed compute | Free Edition; fast start, no cluster to size | pay per use, no infra to manage |
# MAGIC
# MAGIC **Exam rules of thumb:** SQL-only → **SQL warehouse**. Scheduled pipeline → **job cluster / serverless**. Interactive dev → **all-purpose / serverless**. "Cheapest for a nightly job" → **job cluster** (it doesn't idle).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 3 — LAB: Secure and Tune the BrewMart Lakehouse
# MAGIC Analysts must never see raw emails; the vendor sees only their store's rows; gold needs a growth-ready layout.

# COMMAND ----------

# MAGIC %md ### 🔧 Lab reset / pre-flight — run this FIRST (makes the lab repeatable)
# MAGIC **Goal:** guarantee a clean, known starting state no matter what you ran in the demo or in what order.
# MAGIC
# MAGIC **What it does:** unbinds any mask/row filter left on `customers`, drops the demo policy functions, then recreates `customers` fresh from the JSON. Also confirms your Week 1 `sales_by_store` view exists (Task 2 needs it) and recreates a minimal version if it is missing.

# COMMAND ----------

# Unbind policies if present (safe no-ops if they were never set), then rebuild customers
for stmt in [
    "ALTER TABLE customers DROP ROW FILTER",
    "ALTER TABLE customers ALTER COLUMN email DROP MASK",
]:
    try:
        spark.sql(stmt)
    except Exception as e:
        print("skip:", stmt.split(' ', 3)[-1], "→", str(e).split(':')[0])

for fn in ["email_mask", "atlanta_only"]:
    spark.sql(f"DROP FUNCTION IF EXISTS {fn}")

spark.sql(f"""
CREATE OR REPLACE TABLE customers AS
SELECT customer_id, name, loyalty_tier,
       contact.email AS email, contact.city AS city
FROM read_files('{VOL}/week2_customers.json', format => 'json')
""")

# Task 2 grants on the Week 1 view — recreate a minimal one if it did not survive
if not spark.catalog.tableExists(f"workspace.{USER_SCHEMA}.sales_by_store"):
    spark.sql("""
      CREATE OR REPLACE VIEW sales_by_store AS
      SELECT store, ROUND(SUM(line_total),2) AS revenue, COUNT(DISTINCT order_id) AS orders
      FROM sales_silver GROUP BY store
    """)
    print("Recreated sales_by_store from sales_silver.")

print("✅ Reset complete — customers rebuilt, policies cleared, sales_by_store present.")

# COMMAND ----------

# MAGIC %md ### TODO Task 1 — Recreate/verify `customers`
# MAGIC The reset cell above already rebuilt it. Confirm: `SELECT * FROM customers` shows ~10 rows with **real** emails (no mask yet).

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: SELECT to confirm customers exists with readable emails

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
