# Week 4 Solution Review: Secure and Tune the BrewMart Lakehouse

## What You Built

You secured and optimized the BrewMart lakehouse:

- Granted and revoked access to a view.
- Added a column mask to protect email addresses.
- Added a row filter to restrict visible customer rows.
- Built a clustered gold table.
- Practiced cleanup and validation.

Week 4 is about precision. Governance questions often hinge on one word: `GRANT`, `REVOKE`, `DENY`, mask, filter, managed, external, or ABAC.

## Task 1: Recreate / Verify `customers`

### Goal

Start the lab from a clean, known state: a `customers` table with real, readable emails and no mask or row filter bound yet.

### Solution

The lab's reset / pre-flight cell handles this. It unbinds any leftover policy, drops the demo functions, then rebuilds the table from the Week 2 JSON:

```sql
ALTER TABLE customers DROP ROW FILTER;              -- safe no-op if none bound
ALTER TABLE customers ALTER COLUMN email DROP MASK; -- safe no-op if none bound
DROP FUNCTION IF EXISTS email_mask;
DROP FUNCTION IF EXISTS atlanta_only;
```

```python
spark.sql(f"""
  CREATE OR REPLACE TABLE customers AS
  SELECT customer_id, name, loyalty_tier, contact.email AS email, contact.city AS city
  FROM read_files('{VOL}/week2_customers.json', format => 'json')
""")
```

Confirm with `SELECT * FROM customers ORDER BY customer_id` — about 10 rows, emails un-masked.

### Why This Works

`CREATE OR REPLACE` makes the lab repeatable — you can rerun it any time without the "worked on the instructor's screen but not mine" problem. Dropping the bindings first prevents a stale mask or filter from skewing later validation.

### Common Mistakes

- Reusing a `customers` table that still has a demo mask bound, which makes Task 3's proof step confusing.
- `week2_customers.json` missing from the volume root — re-upload it before running the reset cell.

## Task 2: Grant Round-Trip on `sales_by_store`

### Goal

Grant read access to a view, verify the grant, revoke it, and verify again.

### Solution

```sql
GRANT SELECT ON VIEW sales_by_store TO `account users`;
SHOW GRANTS ON VIEW sales_by_store;
```

```sql
REVOKE SELECT ON VIEW sales_by_store FROM `account users`;
SHOW GRANTS ON VIEW sales_by_store;
```

### Why This Works

`GRANT` adds a permission. `SHOW GRANTS` confirms current access. `REVOKE` removes a grant, but it does not necessarily block access if another group still grants the same privilege.

### Common Mistakes

- Confusing `REVOKE` with `DENY`.
- Forgetting backticks around principals with spaces, such as `account users`.
- Granting too much, such as `ALL PRIVILEGES`, when read-only access is enough.

### Exam Takeaway

To query a table or view, a principal usually needs the privilege chain: `USE CATALOG`, `USE SCHEMA`, and object-level access such as `SELECT`.

## Task 3: Mask `customers.email`

### Goal

Allow `brewmart_support` to see real email values while everyone else sees masked values.

### Solution

```sql
CREATE OR REPLACE FUNCTION email_mask(email STRING)
RETURN CASE
  WHEN is_account_group_member('brewmart_support') THEN email
  ELSE regexp_replace(email, '^[^@]+', '***')
END;

ALTER TABLE customers ALTER COLUMN email SET MASK email_mask;

SELECT customer_id, email
FROM customers;
```

### Why This Works

A column mask is a function bound to a column. It runs at query time and changes what the user sees without changing the stored value.

### Common Mistakes

- Creating separate copies of the table for each audience.
- Assuming table owners automatically bypass masks.
- Masking with a view when the requirement says every query path must be protected.

### Validation

```sql
SELECT COUNT(*) AS leaked
FROM customers
WHERE email NOT LIKE '***%';
```

Expected result for non-support users: `0`.

## Task 4: Add a Row Filter

### Goal

Allow `brewmart_hq` to see all cities while other users see only Atlanta rows.

### Solution

```sql
CREATE OR REPLACE FUNCTION hq_or_atlanta(city STRING)
RETURN is_account_group_member('brewmart_hq') OR city = 'Atlanta';

ALTER TABLE customers SET ROW FILTER hq_or_atlanta ON (city);

SELECT COUNT(*) AS visible_rows
FROM customers;
```

### Why This Works

A row filter function returns `true` for rows the querying user can see. Rows that return `false` are hidden at query time.

### Common Mistakes

- Using a column mask when the requirement is row-level visibility.
- Relying on a `WHERE` clause in user queries instead of enforcing the policy on the table.
- Building one filtered view per audience when a bound row filter is simpler and harder to bypass.

### Validation

```sql
SELECT DISTINCT city
FROM customers;
```

Expected result for non-HQ users: only `Atlanta`.

## Task 5: Build and Optimize `sales_gold_daily`

### Goal

Create a gold table clustered by store and order date, then run `OPTIMIZE`.

### Solution

```sql
CREATE OR REPLACE TABLE sales_gold_daily
CLUSTER BY (store, order_date)
AS
SELECT store,
       order_date,
       ROUND(SUM(line_total), 2) AS revenue,
       COUNT(DISTINCT order_id)  AS orders
FROM sales_silver
WHERE store IS NOT NULL
GROUP BY store, order_date;

OPTIMIZE sales_gold_daily;

DESCRIBE DETAIL sales_gold_daily;
```

### Why This Works

Gold tables are business-shaped. `CLUSTER BY` applies Liquid Clustering so Databricks can organize data for common query patterns without rigid partition directories.

`OPTIMIZE` compacts small files. It is different from `VACUUM`, which removes old unreferenced files and affects time travel.

### Common Mistakes

- Using `PARTITIONED BY` as the default answer for modern Databricks layout questions.
- Confusing `OPTIMIZE` with `VACUUM`.
- Clustering on columns that are not common filters or grouping keys.

### Validation

```sql
DESCRIBE DETAIL sales_gold_daily;
```

Look for clustering metadata that includes `store` and `order_date`.

## Task 6: Inspect Lineage

### Goal

Use Catalog Explorer to inspect lineage for `sales_gold_daily`.

### Expected Path

Open:

```text
Catalog Explorer → workspace → your schema → sales_gold_daily → Lineage
```

Expected trace:

```text
landing volume/files → bronze/silver tables → sales_gold_daily
```

### Why This Matters

Lineage supports impact analysis and troubleshooting. If lineage is delayed, wait for query history to refresh or use the instructor screenshot pack.

## Task 7: Cleanup Mask and Row Filter

### Goal

Remove the policies after the lab so the Week 5 capstone starts from a clean state.

### Solution

```sql
ALTER TABLE customers DROP ROW FILTER;

ALTER TABLE customers ALTER COLUMN email DROP MASK;

SELECT COUNT(*) AS all_back
FROM customers;
```

### Why This Works

Mask and row-filter policies are bound to the table. Dropping the binding removes the query-time transformation or row restriction.

### Common Mistakes

- Leaving masks or filters bound before Week 5 and confusing later validation results.
- Dropping the function before dropping the table binding.
- Forgetting to validate that all rows are visible again.

## Stretch: Second Mask + the ABAC Question

```sql
CREATE OR REPLACE FUNCTION tier_mask(tier STRING)
RETURN CASE WHEN is_account_group_member('brewmart_marketing') THEN tier
            ELSE 'REDACTED' END;
ALTER TABLE customers ALTER COLUMN loyalty_tier SET MASK tier_mask;
-- unbind after testing:
-- ALTER TABLE customers ALTER COLUMN loyalty_tier DROP MASK;
```

**The discussion answer:** per-table masking breaks down when one policy must cover many tables owned by different teams — every new table needs a hand-written function and bind, drift is inevitable, and audits cannot prove consistency. The replacement is **tag-driven ABAC**: tag the columns (`pii_email`, `pii_tier`), write one policy per tag, and it applies everywhere the tag appears — current and future tables.

**Bonus:** `EXPLAIN SELECT * FROM sales_gold_daily WHERE store = 'Atlanta'` — the pushed filter in the scan node plus clustering on `(store, order_date)` means matching files are pruned rather than scanned.

## Exam Takeaways

- `DENY` blocks access even if a user gets access through another group.
- `REVOKE` removes a grant but does not necessarily block all paths.
- Column masks protect values; row filters protect rows.
- ABAC is the scale pattern for centrally applied tag-driven masking and filtering.
- `INFORMATION_SCHEMA` exposes catalog metadata (tables, columns, grants) as plain, queryable SQL.
- Compute selection: all-purpose = interactive/dev, job cluster = cheapest for scheduled jobs, SQL warehouse = SQL/BI, serverless = Databricks-managed instant compute.
- Liquid Clustering is current exam vocabulary; Z-order and traditional partitioning are mostly legacy contrast.
- Spark UI symptoms map to causes: max task time much greater than median means skew; spill means memory pressure; import errors before execution often mean library or compute setup issues.
