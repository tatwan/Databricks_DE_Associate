# Databricks notebook source
# MAGIC %md
# MAGIC # Week 4 — Lab Solutions (Study Copy)
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC Markdown only — nothing runs. Task → solution → why → mistakes. Copy snippets into *your* lab notebook (your schema context must be set there).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 1 — Recreate / Verify `customers`
# MAGIC
# MAGIC **The task:** start the lab from a clean, known state — a `customers` table with real, readable emails and **no** mask or row filter bound yet.
# MAGIC
# MAGIC **Solution:** the lab's **reset / pre-flight cell** already does this. It unbinds any leftover policy, drops the demo functions, and rebuilds the table:
# MAGIC ```sql
# MAGIC ALTER TABLE customers DROP ROW FILTER;                 -- safe no-op if none bound
# MAGIC ALTER TABLE customers ALTER COLUMN email DROP MASK;    -- safe no-op if none bound
# MAGIC DROP FUNCTION IF EXISTS email_mask;
# MAGIC DROP FUNCTION IF EXISTS atlanta_only;
# MAGIC ```
# MAGIC ```python
# MAGIC spark.sql(f"""
# MAGIC   CREATE OR REPLACE TABLE customers AS
# MAGIC   SELECT customer_id, name, loyalty_tier, contact.email AS email, contact.city AS city
# MAGIC   FROM read_files('{VOL}/week2_customers.json', format => 'json')
# MAGIC """)
# MAGIC ```
# MAGIC **Confirm:** `SELECT * FROM customers ORDER BY customer_id` → ~10 rows, emails un-masked.
# MAGIC
# MAGIC **Why it works:** `CREATE OR REPLACE` makes the lab **repeatable** — rerun any time without "it worked on the instructor's notebook but not mine." Dropping the bindings first prevents a stale mask/filter from skewing later validation.
# MAGIC
# MAGIC **Common mistakes:**
# MAGIC - Skipping this and reusing a `customers` that still has a demo mask bound → Task 3's "prove it masks you" check gives a confusing result.
# MAGIC - `week2_customers.json` not in the volume root → re-upload it (Catalog Explorer → your schema → Volumes → landing → Upload).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 2 — Grant Round-Trip on `sales_by_store`
# MAGIC
# MAGIC **The task:** GRANT read access on your Week 1 view to `account users`, verify, then take it back and verify again.
# MAGIC
# MAGIC **Solution:**
# MAGIC ```sql
# MAGIC GRANT SELECT ON VIEW sales_by_store TO `account users`;
# MAGIC SHOW GRANTS ON VIEW sales_by_store;
# MAGIC
# MAGIC REVOKE SELECT ON VIEW sales_by_store FROM `account users`;
# MAGIC SHOW GRANTS ON VIEW sales_by_store;
# MAGIC ```
# MAGIC
# MAGIC **Why it works:** `SHOW GRANTS` is the audit answer — the grant appears, then disappears. Note the **backticks**: the principal name contains a space.
# MAGIC
# MAGIC **The exam context:** to actually query, a user needs the full chain — `USE CATALOG` + `USE SCHEMA` + `SELECT`. And remember the pair: **REVOKE removes one grant** (access may survive via another group); **DENY overrides everything**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 3 — Column Mask on `customers.email`
# MAGIC
# MAGIC **The task:** `brewmart_support` sees real emails; everyone else sees `***@<domain>` — same table, no copies.
# MAGIC
# MAGIC **Solution (always two steps):**
# MAGIC ```sql
# MAGIC -- ① a function that DECIDES
# MAGIC CREATE OR REPLACE FUNCTION email_mask(email STRING)
# MAGIC RETURN CASE WHEN is_account_group_member('brewmart_support') THEN email
# MAGIC             ELSE regexp_replace(email, '^[^@]+', '***') END;
# MAGIC
# MAGIC -- ② an ALTER that BINDS
# MAGIC ALTER TABLE customers ALTER COLUMN email SET MASK email_mask;
# MAGIC
# MAGIC SELECT customer_id, email FROM customers;   -- ***@... for YOU too
# MAGIC ```
# MAGIC
# MAGIC **Why it works:** the mask evaluates per query, per user, at read time — storage is untouched and every access path is covered. **Owners are not exempt** — that's why you see masked values on your own table, and why this beats one-view-per-audience.
# MAGIC
# MAGIC **Common mistakes:**
# MAGIC - Creating the function but forgetting the `ALTER TABLE ... SET MASK` bind ("nothing happened").
# MAGIC - `regexp_replace(email, '^[^@]+', '***')` keeps the domain — replacing the whole value would break the "***@<domain>" requirement.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 4 — Row Filter on `customers.city`
# MAGIC
# MAGIC **The task:** `brewmart_hq` sees all rows; everyone else sees only Atlanta.
# MAGIC
# MAGIC **Solution:**
# MAGIC ```sql
# MAGIC CREATE OR REPLACE FUNCTION hq_or_atlanta(city STRING)
# MAGIC RETURN is_account_group_member('brewmart_hq') OR city = 'Atlanta';
# MAGIC
# MAGIC ALTER TABLE customers SET ROW FILTER hq_or_atlanta ON (city);
# MAGIC
# MAGIC SELECT COUNT(*) FROM customers;   -- fewer rows than 10
# MAGIC ```
# MAGIC
# MAGIC **Why it works:** the boolean function runs per row at query time — `true` means you see the row. Chicago/Dallas rows still exist on disk; they're filtered, not deleted.
# MAGIC
# MAGIC **The decision line (exam):** hide a COLUMN's values → mask · hide ROWS → filter · the same policy across hundreds of tagged tables → **ABAC**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 5 — `sales_gold_daily` with Liquid Clustering
# MAGIC
# MAGIC **The task:** a gold table laid out for its query pattern (`store`, `order_date`), then compacted.
# MAGIC
# MAGIC **Solution:**
# MAGIC ```sql
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
# MAGIC DESCRIBE DETAIL sales_gold_daily;   -- clusteringColumns = [store, order_date]
# MAGIC OPTIMIZE sales_gold_daily;
# MAGIC ```
# MAGIC
# MAGIC **Why it works:** `CLUSTER BY` = **Liquid Clustering**, the current exam answer — keys are changeable later without rewriting the table (`ALTER TABLE ... CLUSTER BY (region)`), unlike legacy `PARTITIONED BY` or Z-ORDER. `OPTIMIZE` compacts small files.
# MAGIC
# MAGIC **Don't panic:** OPTIMIZE metrics are near-zero on our tiny table — there's nothing to compact. On Premium+, **predictive optimization** runs this for you on UC *managed* tables.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 6 — Lineage (UI)
# MAGIC
# MAGIC **The task:** open the lineage of `sales_gold_daily`.
# MAGIC
# MAGIC **Solution:** Catalog Explorer → your schema → `sales_gold_daily` → **Lineage** tab.
# MAGIC
# MAGIC **Expected trace:** volume files → bronze → silver → `sales_gold_daily` (plus the Week 3 job node). Table-level and column-level.
# MAGIC
# MAGIC **Why it matters (exam):** Unity Catalog captures lineage **automatically from actual query execution** — no scanner, no registration. If the graph looks incomplete, it refreshes as query history catches up.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task 7 — Unbind and Prove Control
# MAGIC
# MAGIC **The task:** remove the filter and mask, confirm full visibility returns.
# MAGIC
# MAGIC **Solution:**
# MAGIC ```sql
# MAGIC ALTER TABLE customers DROP ROW FILTER;
# MAGIC ALTER TABLE customers ALTER COLUMN email DROP MASK;
# MAGIC
# MAGIC SELECT COUNT(*) FROM customers;   -- 10 again, emails readable
# MAGIC ```
# MAGIC
# MAGIC **Why it works:** policies unbind as cleanly as they bind — proof that the data was never modified. The mask/filter were pure query-time behavior.

# COMMAND ----------

# MAGIC %md
# MAGIC ## ⭐ Stretch — Second Mask + the ABAC Question
# MAGIC
# MAGIC **The task:** mask `loyalty_tier` as `'REDACTED'` for non-members of `brewmart_marketing`, then answer: at what scale does per-table masking break down?
# MAGIC
# MAGIC **Solution:**
# MAGIC ```sql
# MAGIC CREATE OR REPLACE FUNCTION tier_mask(tier STRING)
# MAGIC RETURN CASE WHEN is_account_group_member('brewmart_marketing') THEN tier
# MAGIC             ELSE 'REDACTED' END;
# MAGIC ALTER TABLE customers ALTER COLUMN loyalty_tier SET MASK tier_mask;
# MAGIC -- unbind after testing:
# MAGIC -- ALTER TABLE customers ALTER COLUMN loyalty_tier DROP MASK;
# MAGIC ```
# MAGIC
# MAGIC **The discussion answer:** per-table masking breaks down when one policy must cover many tables owned by different teams — every new table needs a hand-written function + bind, drift is inevitable, audits can't prove consistency. The replacement is **tag-driven ABAC**: tag the columns (`pii_email`, `pii_tier`), write ONE policy per tag, applied everywhere the tag appears — current *and future* tables.
# MAGIC
# MAGIC **Bonus:** `EXPLAIN SELECT * FROM sales_gold_daily WHERE store = 'Atlanta'` — the pushed filter in the scan node + clustering on `(store, order_date)` means matching files are pruned, not scanned.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC **Week 4 exam anchors:** USE CATALOG + USE SCHEMA + SELECT chain · DENY > GRANT · grant to groups · masks hit owners too · function decides, ALTER binds · ABAC = scale · lineage is automatic · `INFORMATION_SCHEMA` = catalog metadata in plain SQL · `CLUSTER BY` = liquid clustering (replaces Z-ORDER + partitioning) · OPTIMIZE compacts / VACUUM deletes old files and trims time travel · UNDROP recovers managed drops · compute: all-purpose (interactive) vs job cluster (cheapest for scheduled) vs SQL warehouse (SQL/BI) vs serverless · skew = max ≫ median task time · collect()/toPandas() kills the DRIVER.
# MAGIC
# MAGIC Tonight: the 45-question timed mock — one sitting, closed book, score yourself **per domain**.
