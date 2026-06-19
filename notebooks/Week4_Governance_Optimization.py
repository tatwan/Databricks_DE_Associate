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
# MAGIC | 2 | Demo — grants, column mask, row filter, lineage, CLUSTER BY, query profile |
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

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE TABLE customers AS
SELECT customer_id, name, loyalty_tier,
       contact.email AS email, contact.city AS city
FROM read_files('{VOL}/week2_customers.json', format => 'json')
""")
display(spark.sql("SELECT * FROM customers ORDER BY customer_id"))

# COMMAND ----------

# MAGIC %md ### 2.2 GRANT → SHOW GRANTS → REVOKE (note the backticks — the principal has a space)

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
# MAGIC **Prediction time:** you OWN this table. Will you see real emails after binding? Run and see.

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
# MAGIC Trace: volume files → bronze → silver (+ the Week 3 job node). Nobody registered anything — UC built it from query history.

# COMMAND ----------

# MAGIC %md ### 2.6 Liquid Clustering + OPTIMIZE

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
# MAGIC Vocabulary to spot: scan → aggregate → **exchange** (= shuffle), rows + time per operator.

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
