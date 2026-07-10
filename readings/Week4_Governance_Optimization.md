# Week 4: Governance and Security + Troubleshooting and Optimization

**Exam domains (May 2026 guide):**
- Governance and Security (15%) — full coverage
- Troubleshooting, Monitoring, and Optimization (10%) — the performance half (run-history monitoring was Week 3)


**Estimated read time:** 30–40 minutes  
**Running example:** Securing and tuning the BrewMart silver and gold tables

## Why This Week Matters

These two domains are frequently under-studied. Engineers spend most of their time building pipelines and relatively little time on "who can see the data" and "why is it slow."

Governance questions are word-precise. A single word like `REVOKE` or "managed" vs "external" can flip the answer. Optimization questions reward symptom → metric → first action reasoning more than memorizing tuning parameters.

## The Securable Hierarchy and Principals

```
metastore
└── catalog
    └── schema
        └── table / view / volume / function / ...
```

Privileges inherit **downward**. Granting at the schema level covers current and future objects.

**Principals:**
- Users (people)
- Groups (preferred for most grants — they scale)
- Service principals (machine identities for jobs and CI/CD pipelines)

**Ownership** gives the ability to grant on an object.

## GRANT, REVOKE, and the Privilege Chain

To query a table you normally need the full chain:
`USE CATALOG` + `USE SCHEMA` + `SELECT`

Common privileges include `SELECT`, `MODIFY`, `CREATE TABLE`, `USE CATALOG`, `USE SCHEMA`, `READ VOLUME`, `WRITE VOLUME`, `EXECUTE`.

**Critical distinction:** `REVOKE` removes a grant you previously gave. Other paths (group membership or a grant inherited from another group) may still allow access.

> **Current-doc warning:** The May 4, 2026 exam guide names `DENY`, but the current Databricks SQL reference says `DENY` is **not supported by Unity Catalog**. It applies only to legacy `hive_metastore` objects. For Unity Catalog, use groups and inheritance, `GRANT`/`REVOKE`, row filters, column masks, ABAC policies, and workspace bindings. If the stem explicitly says Unity Catalog, `DENY` is not valid SQL for that object.

**Exam favorite:** "Analysts need read-only access to an entire schema." The best answer is almost always `GRANT SELECT ON SCHEMA ...` rather than per-table grants.

## Managed vs External — Operations Edition

Week 1 introduced the concept. Week 4 adds the operations the exam lists:
- Create, modify, delete
- Convert between managed and external

`UNDROP TABLE` works for managed tables within the retention window.

Predictive optimization and many automatic features are only available for managed tables in Unity Catalog.

**Exam reflex:** if the question mentions automatic Liquid Clustering or Predictive Optimization, the correct answer must use Unity Catalog managed tables, not external tables.

## Column Masks and Row Filters

Both are implemented as SQL UDFs bound directly to the table.

```sql
CREATE FUNCTION email_mask(email STRING)
RETURN CASE 
  WHEN is_account_group_member('support_team') THEN email
  ELSE '***' 
END;

ALTER TABLE customers ALTER COLUMN email SET MASK email_mask;
ALTER TABLE customers SET ROW FILTER store_filter ON (store);
```

**Important properties:**
- Applied at query time for *every* access path (no bypass by querying the base table).
- Storage is untouched.
- Table owners are **not** automatically exempt.

Masks and filters are the right tool for one or a few sensitive tables. For hundreds of tables with the same policy, look at ABAC.

## ABAC (Attribute-Based Access Control)

Tag columns or tables (`pii_email`, `region=EU`), then write **policies** against those tags.

A single policy can apply masking or row filtering everywhere the tag appears — now and in the future.

**Decision framework:**
- One sensitive table → direct mask or row filter.
- Fleet of tables + central security team + consistent rules → ABAC (exam concept level in Free Edition).

ABAC row filters and column masks are evaluated using the session user’s identity, even when data is accessed through views or functions, so there is no shortcut around policies via a view.

## Lineage and Audit Logs

- **Lineage** is captured automatically by Unity Catalog from actual query and job execution (table and column level). View it in Catalog Explorer → table → Lineage tab.
- **Audit logs** live in system tables (`system.access.audit`) and are queryable with SQL.

No third-party scanner or manual registration is required.

## Delta Sharing and Lakehouse Federation (Awareness)

- **Delta Sharing** — zero-copy sharing of live tables (Databricks-to-Databricks or open protocol). Watch egress costs across regions/clouds.
- **Lakehouse Federation** — query external databases through Unity Catalog without ingesting the data.

Both are "data without copying" but in opposite directions. They are helpful platform awareness but lower priority than core GRANT/mask/ABAC topics for the scored governance domain.

## Physical Layout and Maintenance

Tables are files. Query speed is heavily influenced by file layout.

- Many tiny files → high overhead (list + open costs).
- A few very large files → poor parallelism and pruning.

**OPTIMIZE** compacts small files.  
**VACUUM** removes files no longer referenced by any table version (reclaims storage but limits time travel). Default retention: 7 days.

**Common trap:** Swapping the purposes of OPTIMIZE and VACUUM in answers.

### The Recovery Toolkit (you ran all of these)

| Mistake | Recovery |
|---|---|
| Bad UPDATE/DELETE | `RESTORE TABLE t TO VERSION AS OF n` (Week 1) |
| Dropped a **managed** table | `UNDROP TABLE t` — within the retention window |
| Need to *read* the past | `SELECT ... VERSION AS OF n` or `TIMESTAMP AS OF '...'` |
| Time travel "stopped working" for old versions | VACUUM removed those files — bounded by retention |

## Control Plane vs Compute Plane (Domain 1 callback)

- **Control plane** — managed by Databricks: web UI, job scheduler, Unity Catalog metastore, compute-management APIs. Your grants, masks, and lineage are metadata living here.
- **Compute plane** — where code executes and touches data: **classic** compute runs in the customer's cloud account; **serverless** runs in a Databricks-managed environment.

One-line exam answers: classic clusters run in *your* cloud account; serverless runs in *Databricks'* environment; the metastore is control-plane.

## Liquid Clustering

```sql
CREATE TABLE gold_daily (...) CLUSTER BY (store, order_date);

ALTER TABLE gold_daily CLUSTER BY (region);  -- change keys without full rewrite
```

Liquid Clustering replaces the older combination of Hive-style partitioning (rigid directories, high-cardinality disasters) and Z-ORDER (manual, fixed at OPTIMIZE time).

Advantages:
- Choose or change clustering keys without rewriting the entire table.
- Handles high cardinality and skew better.
- `CLUSTER BY AUTO` lets Databricks pick keys from observed query patterns.

This is the current recommended approach named in the May 2026 guide.

## Predictive Optimization

Databricks automatically runs `OPTIMIZE`, `VACUUM`, and `ANALYZE` on eligible **Unity Catalog managed tables** based on actual usage. Automatic clustering-key selection is specifically associated with `CLUSTER BY AUTO`.

It is a major reason to prefer managed tables when possible.

Scope: Premium+ workspaces, managed tables only. It maintains *tables*, not individual queries.

## Reading the Spark UI and Query Profile

Start with the longest stage, then look at the task duration distribution.

- **Skew:** A few tasks take much longer than the median (max ≫ median).
- **Heavy shuffle:** Large Shuffle Read/Write on wide operations (joins, groupBy).
- **Spill:** "Spill (Memory)" or "Spill (Disk)" counters are non-zero.

First remedies:
- Skew → broadcast small side, salting, better keys, AQE.
- Shuffle → prune earlier, broadcast the small table.
- Spill → more partitions (smaller tasks) or more memory.

**Before vs during work:**
- Failure before any tasks → startup, library, init script, capacity (check event log).
- Failure during work → data / memory / code (Spark UI + logs).

## The Four Tuning Parameters (Know What They Influence)

- `spark.sql.shuffle.partitions`
- `spark.default.parallelism`
- `spark.executor.memory` / `spark.driver.memory`
- `spark.sql.autoBroadcastJoinThreshold`

On serverless and with AQE, Databricks does much of this automatically. The exam still wants you to know the direction each knob moves the system.

## BrewMart in Week 4

You will:
- Run a GRANT → SHOW GRANTS → REVOKE round-trip on your Week 1 view.
- Implement a column mask and a row filter on real data — and observe that even the table owner sees masked values.
- Build `sales_gold_daily` with `CLUSTER BY (store, order_date)`, run `OPTIMIZE`, and inspect `DESCRIBE DETAIL`.
- Open the automatic lineage of your gold table in Catalog Explorer.
- Unbind the policies and prove the data was never modified.
- In the demo: read a query profile (find the exchange/shuffle), run the maintenance & recovery drill (`VACUUM`, `DROP`→`UNDROP`, `TIMESTAMP AS OF`), and query the audit log shape (`system.access.audit`).
- Diagnose bottleneck scenarios (skew / spill / startup / driver OOM) in the in-class symptom-card activity.

## Exam Focus — Symptom → Action and Precise Wording

Governance questions love precise privilege language and the managed/external distinction.

Optimization questions love:
- "Max task time much higher than median" → skew.
- "Large shuffle read/write" → broadcast or early pruning.
- "Spill counters > 0" → more partitions.

Predictive optimization questions usually ask which feature removes the need for manually scheduled OPTIMIZE jobs on managed tables.

## Self-Check Questions

1. After a `REVOKE`, a user can still read the table. List two possible reasons and the Unity Catalog mechanisms you would use to correct the access design.
2. Mask vs row filter vs ABAC: give the one-line condition that tells you which to choose.
3. In a stage summary you see one task took 28 minutes while the median task took 12 seconds. What is the symptom and the first remedy you should consider?
4. Why does predictive optimization only apply to managed tables?
5. A job fails with an import error before any tasks start. Where is the first place you look?

## Recommended Documentation

**Primary reading (~35 min)**

- [Unity Catalog privileges and securable objects](https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges)
- [Row filters and column masks](https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks)
- [ABAC overview](https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac)
- [Liquid clustering](https://docs.databricks.com/aws/en/delta/clustering)
- [Predictive optimization](https://docs.databricks.com/aws/en/optimizations/predictive-optimization)
- [Spark UI guide](https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/)

**Practice targets**
- Re-apply a mask and row filter from memory.
- Write GRANT statements for a group and a service principal, then verify with `SHOW GRANTS`.
- Run a filtered query and use `EXPLAIN` or the query profile to see pruning.

## Mini Checklist Before Week 5

- [ ] Timed mock exam completed and scored by domain.
- [ ] Two weakest domains identified.
- [ ] Kryterion system check passed on the machine you will use for the real exam.
- [ ] All BrewMart objects still exist (capstone reuses them).

Governance and optimization close the set of seven domains. Week 5 is about integrating everything under time pressure and turning your mock results into a final-week study plan.
