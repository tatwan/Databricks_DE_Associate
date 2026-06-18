# Week 1: Lakehouse Foundations

**Exam domains (May 2026 guide):** 
- Databricks Intelligence Platform (6%) — primary coverage
- Data Transformation and Modeling (22%) — foundations (DDL, CTAS, gold objects, medallion)
- Governance and Security (15%) — foundations (Unity Catalog hierarchy, managed vs external tables, volumes)

**Estimated read time:** 25–35 minutes  
**Running example:** BrewMart retail sales data

## Why This Week Matters

Week 1 establishes the mental model that every later week builds on. The exam's Domain 1 (Platform) and large parts of Domains 3 and 7 are tested using the concepts introduced here: one copy of data in Delta, one governance tree in Unity Catalog, and the difference between managed and external objects.

This week seeds the "Intelligence Platform" and "Governance & Quality" areas that appear across the current 5-domain grouping used in many official prep paths (Intelligence Platform, Development & Ingestion, Data Processing & Transformations, Productionizing Data Pipelines, Governance & Quality). The full 7-domain breakdown with exact weights is in the course curriculum map.

If you cannot confidently answer "what happens when I drop a managed table vs an external table?" or "what does the `_delta_log` actually do?", you will lose easy points on the exam.

## The Data Intelligence Platform Stack

Databricks markets the full platform as the **Data Intelligence Platform**. The core idea is simple but powerful:

**One governed copy of data in open formats serves every workload** (ETL, SQL analytics, BI, ML, streaming, AI).

The layers, from bottom to top:

1. **Cloud object storage** (S3, ADLS, GCS) — cheap, durable, your account.
2. **Open table files** (Parquet + Delta) — the actual data files plus transactional metadata.
3. **Unity Catalog** — the single governance layer (catalog.schema.object).
4. **Compute** — SQL warehouses, serverless notebooks/jobs, or classic clusters.
5. **Workloads** — everything that reads or writes the same tables.

This model eliminates the traditional split between "data lake" (cheap but unreliable) and "data warehouse" (reliable but expensive copies and closed formats).

**See also:** The Data Intelligence Platform Stack diagram (visuals folder).

## Platform Awareness: Control Plane, Data Plane, and Workspace Isolation

A quick but useful distinction for Domain 1 questions:

- **Control plane**: Managed by Databricks (web UI, job scheduler, Unity Catalog metastore, cluster management APIs, billing).
- **Data plane**: Executes in *your* cloud account (the actual compute and your object storage).

In Free Edition you work in a single workspace backed by one metastore. Larger organizations often share a metastore across multiple workspaces while keeping separate data planes for isolation and cost control. This separation is a recurring theme in platform and governance questions.

## Light dbutils in Notebooks

You will encounter `dbutils` in the course notebooks and labs. It is a utility library available inside Databricks notebooks for common tasks:

- `dbutils.widgets` — receive parameters from jobs (used heavily starting Week 1).
- `dbutils.fs` — list, copy, or interact with files on volumes (e.g., checking what landed in `landing/`).
- `dbutils.notebook.exit()` — return small values from one notebook task to another (Week 3 orchestration).

At the Associate level the exam does not require deep mastery of every dbutils module. Focus on the widget and exit patterns that connect jobs to notebooks.

## Delta Lake — Parquet Plus a Transaction Log

A Delta table is not a special engine. It is:
- Data files (usually Parquet)
- A `_delta_log` directory containing ordered JSON commits (and checkpoints)

The log is the source of truth. Readers always see the latest committed snapshot. This single fact gives you:

- **ACID transactions** on object storage
- **Time travel** (`VERSION AS OF` / `TIMESTAMP AS OF`)
- **History / audit** (`DESCRIBE HISTORY`)
- **Schema enforcement** by default (bad writes are rejected)
- **RESTORE TABLE** as an undo button

**Schema evolution** is opt-in (`mergeSchema` or `COPY_OPTIONS`). Enforcement is the safe default.

**Key exam fact:** `CREATE TABLE` without a `USING` clause creates a Delta table. Delta is the default.

**VACUUM** removes old files and therefore limits how far back time travel can reach (default 7 days retention).

### Common Traps
- Thinking "Delta is a database" — it is an open storage format.
- Believing time travel keeps data forever (VACUUM deletes unreferenced files).
- Expecting `CREATE TABLE IF NOT EXISTS` to update an existing table (it is a no-op if the table exists).

## Unity Catalog Hierarchy and Three-Level Names

Every securable object lives under one account-level metastore:

```
metastore
└── catalog (e.g. workspace, samples, main)
    └── schema
        ├── tables
        ├── views
        ├── volumes
        ├── functions
        └── ...
```

You address objects as `catalog.schema.object`. In Free Edition you primarily use the `workspace` catalog.

**Inheritance flows down.** A `GRANT SELECT ON SCHEMA sales TO analysts` gives access to current *and future* tables in that schema.

**Volumes** govern non-tabular files (CSVs, JSON, libraries, images) under the same `catalog.schema.volume` addressing. Query files inside a volume with `read_files()`, not `SELECT * FROM my_volume`.

## Managed vs External Tables

This is one of the highest-yield topics on the exam.

| Aspect                  | Managed (default)                          | External                                      |
|-------------------------|--------------------------------------------|-----------------------------------------------|
| Who controls data files | Unity Catalog                              | You (external location)                       |
| `DROP TABLE`            | Deletes metadata **and** data files        | Deletes metadata only; files remain           |
| `UNDROP TABLE`          | Possible within retention window           | Not applicable                                |
| Automatic optimization  | Eligible (predictive optimization, etc.)   | Not eligible                                  |
| When to choose          | Default recommendation                     | Hard storage requirements, external readers   |

**Exam reflex:** Run `DESCRIBE EXTENDED table_name` and look at the `Type` line. Then predict what `DROP` will do.

Conversion between managed and external is possible (directional operations), though exact syntax details are lower yield than understanding the consequences.

## Creating Tables — CREATE vs CTAS vs CREATE OR REPLACE

- `CREATE TABLE name (col TYPE, ...)` — empty table, explicit schema.
- `CREATE TABLE name AS SELECT ...` (CTAS) — creates **and** populates. Schema is inferred from the `SELECT`. You **cannot** declare column types in the CTAS clause.
- `CREATE OR REPLACE TABLE` — atomic replace that preserves history.
- `CREATE TABLE IF NOT EXISTS` — does nothing if the table already exists.

**Exam rule you must internalize:** Any option that shows `CREATE TABLE ... AS SELECT (col TYPE, ...)` is wrong. Control types inside the `SELECT` with `CAST`.

## The Gold Object Menu

| Object             | Stores data? | Freshness     | Use when...                              |
|--------------------|--------------|---------------|------------------------------------------|
| Table              | Yes          | As written    | Full control + optimization              |
| View               | No           | Always current| Reusable logic, cheap recompute          |
| Materialized View  | Yes          | As of refresh | Expensive aggregation, frequent reads    |
| Streaming Table    | Yes          | Continuous    | Incremental append ingestion             |
| Temp View          | No           | Always current| Scratch work inside one session only     |

**Key question to ask:** "Do I need the data precomputed or always fresh? Who needs to see it?"

A common support ticket ("I have SELECT but can't query") is almost always a missing `USE CATALOG` or `USE SCHEMA` in the privilege chain.

## Medallion Architecture

**Bronze** — raw, as-ingested, minimal transformation. Preserves fidelity and replayability.  
**Silver** — cleaned, typed, deduplicated, constrained. The trustworthy engineering layer.  
**Gold** — aggregated, business-shaped. What BI and consumers use.

This is a *design pattern*, not an enforced feature. The value of bronze is its rawness — do not pre-clean it or you lose the ability to replay history when silver logic changes.

In the BrewMart example:
- Daily sales CSVs land in a volume → bronze (all strings + audit column).
- Corrections and returns are handled with quality decisions.
- Silver enforces contracts.
- Gold serves specific business questions (sales by store, net revenue, etc.).

## Choosing Compute

- **Serverless SQL warehouse** — SQL analytics, BI, dashboards. Instant start, auto-scaling.
- **Serverless notebook / job compute** — Python + SQL without cluster management. Hands-off.
- **Job clusters** (concept) — created per run, terminated after. The production cost winner.
- **All-purpose clusters** (concept) — interactive development, shared by humans. More expensive per job because they linger.

**Rule of thumb:** SQL-only → warehouse. Scheduled production pipelines → job/serverless compute. Interactive development → all-purpose or serverless.

In Free Edition you are limited to serverless. Classic cluster behavior is testable on the exam even if you cannot create them in class.

## Modern Vocabulary (Avoid Old-Name Traps)

The May 2026 exam uses:
- **Lakeflow Jobs** (not Workflows)
- **Lakeflow Spark Declarative Pipelines** (not DLT)
- **Declarative Automation Bundles** (formerly Databricks Asset Bundles)
- **Git folders** (formerly Repos — the guide sometimes still says "Repos")

Know both old and new names, but answer using the current terminology the question stem uses.

## BrewMart in Week 1

You will create:
- Your own schema inside the `workspace` catalog (`lab1_<yourname>`)
- A volume called `landing`
- A managed Delta table `sales_raw` via CTAS (with casts and `line_total`)
- A view (`sales_by_store`) and a temp view
- A deliberate mistake followed by `DESCRIBE HISTORY` + `VERSION AS OF` + `RESTORE TABLE`

Everything you create here is reused in Weeks 2–5. Do not drop your schema or volume.

## Exam Focus — What Gets Tested

- Compute selection scenarios with cost and workload reasoning.
- DDL discrimination (`CREATE` vs `CTAS` vs `OR REPLACE` vs `IF NOT EXISTS`).
- `DROP` semantics for managed vs external (both directions).
- Three-level naming and the `USE CATALOG` + `USE SCHEMA` + `SELECT` chain.
- Purpose of each medallion layer.
- Gold object selection (table / view / MV / streaming table).
- Delta defaults and the role of the transaction log.

**Elimination technique:** Find the forcing constraint in the stem ("single statement", "regardless of whether it exists", "must remain in our storage"). Strike invented syntax first, then real features applied to the wrong situation.

## Self-Check Questions

1. What two capabilities does the `_delta_log` directory provide that plain Parquet cannot?
2. `DESCRIBE EXTENDED` shows `Type: EXTERNAL`. What happens on `DROP TABLE`? What about time travel and predictive optimization?
3. Write the full path (as a string) to a file `returns.csv` inside volume `incoming` in schema `lab1_alex` in catalog `workspace`.
4. Why would you choose a materialized view over a regular view for a dashboard that hits the same aggregation 200 times per hour?
5. A colleague says "I granted myself SELECT on the table but I still can't query it." What is the most likely missing piece?

## Recommended Documentation

**Primary reading (~40 min total)**

- What is a data lakehouse? (Lakehouse architecture overview)
- What is Delta Lake? (Delta Lake overview)
- What is Unity Catalog? — focus on the object-model diagram and three-level names
- Database objects: tables (managed vs. external) and volumes
- What is the medallion lakehouse architecture?

**Optional deeper dive**
- `DESCRIBE HISTORY` and time travel syntax
- `RESTORE TABLE` and `UNDROP TABLE`

## Mini Checklist Before Week 2

- [ ] My `lab1_<name>` schema, `sales_raw` table, and `landing` volume still exist.
- [ ] I can write a CTAS with casts from memory.
- [ ] I can state `DROP` behavior for managed vs external tables without hesitation.
- [ ] I understand when to use a view vs a materialized view vs a temp view.
- [ ] Free Edition login and SQL warehouse still work.

This foundation is deliberately reused. Week 2 will fill the bronze layer with real incremental files and start building trustworthy silver tables on top of what you created today.
