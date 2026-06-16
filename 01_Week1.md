# Week 1: Lakehouse Foundations — Delta Lake, Unity Catalog, and Table Fundamentals

> Aligned to the **May 4, 2026** Databricks Certified Data Engineer Associate exam guide.
> Primary exam domains: **Databricks Intelligence Platform** (full coverage) + **Data Transformation and Modeling** (DDL/table-object foundations) + **Governance and Security** (managed vs. external, seeded here, deepened in Week 4).

---

## 1. Session Overview

- **Duration:** 2 hours
- **Target audience:** Working data engineers from ADF / Synapse / Fabric / SQL warehousing backgrounds who have completed Databricks Fundamentals and Getting Started with Data Engineering
- **Prerequisites:**
  - A Databricks Free Edition account, logged in successfully before class
  - Comfort with SQL (joins, DDL, DML)
  - Conceptual familiarity with notebooks
- **Main exam domains covered:**
  - Domain 1: Databricks Intelligence Platform (~6–10%)
  - Domain 3: Data Transformation and Modeling — DDL features, gold-object types (partial)
  - Domain 7: Governance and Security — managed vs. external tables (introduced)
- **Learning objectives.** By the end of this session, learners can:
  1. Explain the lakehouse architecture and how the Data Intelligence Platform layers (cloud storage → Delta Lake → Unity Catalog → compute → workloads) fit together
  2. Describe what Delta Lake adds on top of Parquet (transaction log, ACID, time travel, schema enforcement)
  3. Navigate the Unity Catalog hierarchy and address any object with `catalog.schema.object`
  4. Create managed tables with `CREATE TABLE` and `CTAS`, and explain when each is appropriate
  5. Distinguish managed vs. external tables and predict what `DROP TABLE` does to each
  6. Distinguish views, temp views, materialized views, and streaming tables
  7. Create a volume, upload a file, and query it with `read_files()`
  8. Choose the right compute for a workload (serverless SQL warehouse vs. serverless notebook compute vs. classic/job clusters — conceptually)

---

## 2. Recommended Timing

| Time      | Segment                      | Purpose                     |
| --------- | ---------------------------- | --------------------------- |
| 0:00–0:10 | Warm-up: "Translate your stack" + exam orientation | Activate prior ADF/Synapse/Fabric knowledge; set exam expectations |
| 0:10–0:45 | Concept slides (15 slides)   | Lakehouse, Delta, UC hierarchy, table types, compute |
| 0:45–1:10 | Instructor demo              | Samples → managed table → CTAS → time travel → volume |
| 1:10–1:40 | Hands-on lab                 | Learners build their first governed tables from a CSV |
| 1:40–1:50 | In-class activity            | "Managed or external? Table or volume?" decision cards |
| 1:50–2:00 | Markdown Mash quiz + wrap-up | Exam readiness check, homework assignment |

---

## 3. Slide Deck Content

### Slide 1: Welcome — What This Exam Actually Tests

**Key bullets**
- Databricks Certified Data Engineer Associate: 45 scored questions, 90 minutes, multiple choice, $200
- 7 domains (May 2026 guide): Platform, Ingestion, Transformation & Modeling, Lakeflow Jobs, CI/CD, Troubleshooting/Optimization, Governance & Security
- Code is shown in **SQL when possible, Python otherwise** — you need both
- This course: 5 Fridays, each anchored to specific domains

**Speaker notes**
Open by setting the contract: this is not a beginner course, it's a certification bridge. Tell them the exam changed on May 4, 2026 — most online prep material targets the older 5-domain version, so warn them off stale Udemy dumps. Emphasize pace: 2 minutes per question on exam day. Show the domain list and point to where each lands in our 5 weeks.

**Visual suggestion**
A 5-week timeline strip with the 7 exam domains color-coded onto the weeks (use the curriculum map table).

**Exam relevance**
Orientation — knowing the blueprint is the highest-leverage study act.

**Common misconception**
Learners assume old practice exams are valid. The May 2026 version added CI/CD and reorganized everything; old question banks miss entire domains.

---

### Slide 2: Translating Your Azure Vocabulary

**Key bullets**
- ADF pipeline → Lakeflow Jobs (orchestration) / Lakeflow Connect (ingestion)
- Synapse dedicated SQL pool → SQL warehouse on Delta tables (no separate warehouse engine)
- Fabric OneLake + shortcuts → Unity Catalog + external locations
- Fabric Lakehouse/Warehouse split → one lakehouse, one format (Delta), one governance layer

**Speaker notes**
Spend two minutes max — this slide buys trust, not exam points. Key message: in Databricks there is no engine/storage split to manage; storage is open Parquet+Delta in your cloud account, and every workload (SQL, Python, streaming, BI) hits the same tables. Fabric people will find Delta familiar — Fabric uses Delta too — so their instincts transfer well. Warn ADF people: orchestration here is code-adjacent (jobs, tasks), not drag-and-drop activities.

**Visual suggestion**
Two-column mapping table: "What you say today" → "What Databricks calls it."

**Exam relevance**
None directly — but it prevents learners from answering with Azure mental models, the #1 source of wrong answers for this audience.

**Common misconception**
"Databricks SQL warehouse is a separate copy of the data, like a dedicated pool." It isn't — it's compute over the same Delta tables.

---

### Slide 3: The Lakehouse and the Data Intelligence Platform

**Key bullets**
- Lakehouse = data lake economics + warehouse reliability/performance, one copy of data
- Stack: cloud object storage → open formats (Parquet + Delta) → Unity Catalog governance → compute → workloads (ETL, SQL/BI, ML, streaming, AI)
- "Data Intelligence Platform" = lakehouse + AI-powered layer (Databricks IQ, predictive optimization, assistant)
- Open formats prevent lock-in: your tables are readable by external engines

**Speaker notes**
This is the exam's Domain 1 core. Have learners articulate *why* the lakehouse exists: warehouses gave ACID and performance but closed formats and expensive copies; lakes gave cheap open storage but no reliability. Delta on object storage closes the gap. Name the layers from bottom up and keep returning to this diagram all course. Mention that the exam's current branding is "Data Intelligence Platform" — if a question says that, it means the whole platform.

**Visual suggestion**
Layered architecture diagram, bottom-up: object storage → Delta Lake → Unity Catalog → compute (SQL warehouses, serverless, clusters) → workload icons.

**Exam relevance**
Direct: "Explain the value of the Data Intelligence Platform" and "core components: architecture, Delta Lake, Unity Catalog" are named objectives.

**Common misconception**
That the lakehouse is a marketing wrapper around a data lake. The differentiator is the transactional metadata layer (Delta) + unified governance (UC) — be ready to say what's *technically* different.

---

### Slide 4: Compute — Picking the Right Engine for the Job

**Key bullets**
- Serverless SQL warehouse: SQL analytics, BI, dashboards — instant start, auto-scaling
- Serverless notebook/job compute: Python/SQL notebooks and jobs without cluster management
- Classic compute (concept): all-purpose clusters (interactive, shareable, more expensive per job) vs. job clusters (created per run, terminated after, cheaper for production)
- Rule of thumb: SQL-only → warehouse; production pipeline → job compute; interactive development → all-purpose or serverless

**Speaker notes**
The exam loves "which compute should they use?" questions. Teach the decision logic: workload type (SQL vs. general code), interactivity (human vs. scheduled), and cost (job clusters terminate; all-purpose linger). Be explicit about what learners will see in class: **Free Edition is serverless-only** — one 2X-Small SQL warehouse and serverless notebook compute; you cannot create classic clusters. So cluster configuration is "exam concept; requires a paid workspace for hands-on." Serverless itself is exam-relevant: hands-off, auto-optimized, Databricks-managed.

**Visual suggestion**
Decision tree: "SQL only?" → warehouse; "Scheduled production job?" → job compute; "Interactive dev?" → all-purpose/serverless. Annotate each node with cost behavior.

**Exam relevance**
Named objective: "select the most suitable compute option for each workload use case" including "characteristics, limitations, and cost models." Serverless appears again in Domain 4 ("use serverless for hands-off, auto-optimized compute").

**Common misconception**
"All-purpose clusters are for production because they're always on." Reverse: job clusters are the production pattern precisely because they terminate; all-purpose is for humans.

> **Exam concept; may require paid workspace or admin access for full hands-on practice** (cluster creation/configuration UI).

---

### Slide 5: Delta Lake — What It Actually Is

**Key bullets**
- Delta table = Parquet data files + `_delta_log` transaction log (JSON commits + checkpoints)
- The log is the source of truth: readers get the latest committed snapshot — ACID on object storage
- Default table format in Databricks; `USING DELTA` is implicit
- Open source format — not proprietary to Databricks

**Speaker notes**
Demystify: a Delta table is just files. The magic is the ordered transaction log that records every add/remove of data files. That's what gives atomic writes, consistent reads, and the version history we'll use for time travel. Connect to their world: this is what Fabric tables use under OneLake too. Stress "Delta is the default" — on the exam, `CREATE TABLE` with no `USING` clause makes a Delta table.

**Visual suggestion**
Folder-structure sketch: table directory containing `part-*.parquet` files and `_delta_log/00000.json, 00001.json...`, with arrows showing a commit appending to the log.

**Exam relevance**
Delta Lake is a named "core component" in Domain 1, and DDL/DML behavior questions in Domain 3 assume you know Delta is default.

**Common misconception**
"Delta is a database engine or a Databricks-only format." It's an open storage format/protocol; compute engines (including non-Databricks ones) read it.

---

### Slide 6: Delta Superpowers — History, Time Travel, Schema Enforcement

**Key bullets**
- Every write = new table version; `DESCRIBE HISTORY` shows the audit trail
- Time travel: `SELECT ... VERSION AS OF n` / `TIMESTAMP AS OF '...'`; `RESTORE TABLE` to roll back
- Schema enforcement: writes with mismatched schema are rejected by default
- Schema evolution: opt-in (e.g., `mergeSchema`) — enforcement is the default, evolution is the choice

**Speaker notes**
Run the logic chain: because the log records every version, you can query the past, audit changes, and roll back mistakes. Schema enforcement is the warehouse-grade safety they're used to from Synapse — bad-schema writes fail instead of silently corrupting. Make the enforcement-vs-evolution distinction crisp now; it returns in Week 2 with Auto Loader. Mention `VACUUM` removes old files and therefore limits how far back time travel reaches (one sentence — depth comes in Week 4).

**Visual suggestion**
Version timeline: v0 CREATE → v1 INSERT → v2 UPDATE, with a query arrow pointing back at v1 labeled "VERSION AS OF 1."

**Exam relevance**
DDL/DML feature identification (Domain 3) and troubleshooting questions often hinge on history/time-travel syntax.

**Common misconception**
"Time travel keeps data forever." It's bounded by retention and `VACUUM`; vacuumed versions are gone.

---

### Slide 7: Unity Catalog — One Governance Layer, Three-Level Names

**Key bullets**
- Hierarchy: metastore → **catalog** → **schema** → securable objects (tables, views, volumes, functions, models)
- Every object addressed as `catalog.schema.object` — the three-level namespace
- One metastore per region/account governs all workspaces; in Free Edition you get one metastore, one workspace, and a `workspace` catalog
- UC adds: centralized access control (GRANT/REVOKE), auditing, lineage, discovery

**Speaker notes**
This is the single most reused mental model in the course — every demo, lab, and half the exam questions use three-level names. Compare to their world: catalog ≈ database server/Fabric workspace-ish, schema ≈ database/schema, but the comparison is loose — what matters is the *path*. Show the Catalog Explorer live if time allows. Tell them: in our Free Edition labs, everything lives in `workspace.<your_schema>`. The `samples` catalog is read-only shared data.

**Visual suggestion**
Tree diagram: Metastore → catalogs (`workspace`, `samples`) → schemas → leaf icons for table/view/volume/function.

**Exam relevance**
Named in Domain 1 (core component) and Domain 7 (privilege hierarchy levels). Questions test which level a privilege or object lives at.

**Common misconception**
Confusing *metastore* with the legacy *Hive metastore*, and thinking each workspace has its own isolated catalog of data. UC is account-level; workspaces share it.

---

### Slide 8: Managed vs. External Tables

**Key bullets**
- **Managed:** UC controls both metadata *and* data files in UC-managed storage; `DROP TABLE` deletes data (recoverable briefly via `UNDROP`)
- **External:** UC controls metadata only; data lives at an external location you specify; `DROP TABLE` removes metadata, files remain
- Managed is the Databricks default and recommendation (enables predictive optimization & faster defaults)
- External is for: data shared with non-Databricks tools, existing data estates, hard storage-location requirements

**Speaker notes**
This is a guaranteed exam topic and the #1 "gotcha" for warehouse people. Drill the DROP behavior both directions with a quick oral quiz. Explain *why* managed is recommended: when Databricks owns layout it can optimize automatically. ADF/Synapse external-table instincts transfer well here. Note that the exam also mentions *converting* between managed and external — know it's possible and not just a flag flip (typically involves recreating or `ALTER ... SET LOCATION` patterns; details Week 4). In Free Edition, external locations aren't available — external tables are **"Exam concept; requires paid workspace/admin for hands-on."**

**Visual suggestion**
Side-by-side panel: two tables, arrows to "UC-managed storage" vs. "your storage path," with a DROP TABLE bomb icon showing what survives in each.

**Exam relevance**
Explicit Domain 7 objective: "Differentiate between managed and external tables… create, modify, delete, convert." Also drives `DESCRIBE EXTENDED` interpretation questions.

**Common misconception**
"External tables are safer because Databricks can't touch my data." Cuts both ways — you also lose automatic optimization and lifecycle management, and orphaned files become your problem.

---

### Slide 9: Volumes — Governed Storage for Files

**Key bullets**
- Volume = UC-governed storage for **non-tabular** data (CSV/JSON landing files, images, libraries)
- Tables = tabular data; volumes = everything else; same `catalog.schema.volume` addressing
- Path access: `/Volumes/<catalog>/<schema>/<volume>/...`
- Managed volumes work in Free Edition — our labs stage files here

**Speaker notes**
Volumes are how Databricks killed the "random files in DBFS" anti-pattern: file storage now has the same governance as tables. The exam's ingestion domain assumes files land somewhere governed — volumes are that somewhere. Show the path convention and say it out loud: slash-Volumes-catalog-schema-volume. In the demo they'll upload a CSV to a volume and query it in place.

**Visual suggestion**
Two buckets labeled "Tabular → Table" and "Non-tabular → Volume," both hanging off the same schema node in the UC tree.

**Exam relevance**
Volumes appear in ingestion scenarios (Domain 2: "import data from local files") and the governance hierarchy (Domain 7).

**Common misconception**
Treating a volume like a table ("SELECT * FROM my_volume"). You query *files in* a volume with `read_files()` or load them into a table — the volume itself isn't queryable.

---

### Slide 10: Creating Tables — CREATE TABLE and CTAS

**Key bullets**
- `CREATE TABLE t (col TYPE, ...)` — empty table, explicit schema
- `CREATE TABLE t AS SELECT ...` (CTAS) — creates *and* populates; schema **inferred from the query**, no column list allowed (column *names* may be aliased)
- `CREATE OR REPLACE TABLE` — replaces atomically, history preserved (still time-travelable)
- `CREATE TABLE IF NOT EXISTS` — no-op if exists; does NOT update an existing table

**Speaker notes**
Straight exam syntax. The retired official sample questions test exactly this: "create an empty Delta table regardless of whether it exists" → `CREATE OR REPLACE TABLE` with explicit columns. Drill the CTAS rule: schema comes from the SELECT — you cannot declare column types in a CTAS column list. If you need type control with CTAS, CAST in the SELECT. Also contrast OR REPLACE vs. DROP+CREATE: OR REPLACE is atomic and keeps history.

**Visual suggestion**
Three code cards side by side (CREATE / CTAS / CREATE OR REPLACE) with a one-line "when to use" caption under each.

**Exam relevance**
Domain 3 "Identify DDL/DML features" — among the most directly tested syntax on the exam (two of five official sample questions).

**Common misconception**
That `CREATE TABLE IF NOT EXISTS` "refreshes" the table or that CTAS accepts `(col TYPE)` declarations. Both wrong.

---

### Slide 11: Views, Temp Views, Materialized Views, Streaming Tables

**Key bullets**
- **View:** stored query, re-computed at read time, persisted in UC, shareable, governable
- **Temp view:** session-scoped, vanishes when the session ends, invisible to others
- **Materialized view:** *precomputed* results, refreshed on a schedule/incrementally — for BI performance
- **Streaming table:** continuously/incrementally ingests append-only sources — for pipelines
- Gold-layer menu: table (full control) / view (always fresh, compute at read) / MV (fast reads, refresh lag) / streaming table (incremental ingest)

**Speaker notes**
The first three are classic SQL knowledge; the exam twist is choosing among all four for a gold-layer scenario (named Domain 3 objective). Give the decision heuristics: dashboard hit many times an hour on expensive aggregation → MV; logic wrapper, always-current → view; scratch object inside one notebook session → temp view; incremental append ingestion → streaming table. Note MVs and streaming tables are created via SQL but refreshed by managed infrastructure (Lakeflow/serverless) — light hands-on in Free Edition, full story in Week 2.

**Visual suggestion**
2×2-ish comparison table: freshness at read, query cost at read, persistence/sharing, typical use.

**Exam relevance**
Verbatim objective: "Understand the difference between, and how to build, Gold layer objects such as materialized views, views, streaming tables, and tables."

**Common misconception**
"A view stores data." It stores a query. And the reverse for MVs — learners forget MVs can serve **stale** data between refreshes.

---

### Slide 12: Medallion Architecture — Bronze, Silver, Gold

**Key bullets**
- **Bronze:** raw, as-ingested, minimal transformation — preserves source fidelity and replayability
- **Silver:** cleaned, deduplicated, typed, conformed — the trustworthy engineering layer
- **Gold:** aggregated, business-shaped — feeds BI, ML, and consumers
- A design pattern (recommended), not an enforced feature — layers are just schemas/tables you organize

**Speaker notes**
Frame it as progressive refinement with replayability: if silver logic was wrong, you rebuild from bronze without re-extracting from sources. Map to their experience: staging → conformed → presentation in a warehouse. The exam asks for the *purpose of each layer* (named objective). Tell them this is the course spine — Week 2 builds bronze→silver→gold for real.

**Visual suggestion**
Left-to-right flow: source systems → Bronze (🥉 raw) → Silver (🥈 clean) → Gold (🥇 aggregated) → BI/ML icons. One-line label per layer stating its contract.

**Exam relevance**
Verbatim Domain 3 objective: "Describe the three layers of the Medallion Architecture and explain the purpose of each layer."

**Common misconception**
"Bronze should be cleaned a little so it's usable." No — bronze's value *is* its rawness. Cleansing belongs in silver; pre-cleaning bronze destroys your replay/audit story.

---

### Slide 13: The Modern Databricks Vocabulary (Don't Get Tricked by Old Names)

**Key bullets**
- Workflows → **Lakeflow Jobs** | DLT → **Lakeflow Spark Declarative Pipelines** | new: **Lakeflow Connect** (ingestion connectors)
- Databricks Asset Bundles (DABs) → **Declarative Automation Bundles** (exam says "formerly Databricks Asset Bundles")
- Repos → **Git folders** (the exam guide still says "Databricks Repos" — know both)
- Old blogs/courses use stale names; the exam uses current ones

**Speaker notes**
Two minutes of pure exam insurance. Most third-party prep content predates the rename wave; learners must map old↔new instantly or they'll misread questions. Read each pair aloud. This also previews Weeks 2–3 so the names won't be foreign.

**Visual suggestion**
Two-column "Then → Now" table with the four renames.

**Exam relevance**
The May 2026 guide uses Lakeflow/Automation Bundle terminology throughout — recognizing it is prerequisite to parsing questions.

**Common misconception**
Thinking the renames are different products. Same capabilities, evolved names (with feature growth).

---

### Slide 14: How Week 1 Topics Get Tested

**Key bullets**
- Recall: default format (Delta), UC hierarchy order, DROP semantics
- Syntax: CREATE/CTAS/OR REPLACE variants, `VERSION AS OF`, three-level names
- Scenario: "Which compute…", "Which gold object…", "What happens to the files when…"
- Elimination skill: distractors are usually *real* features applied to the wrong situation

**Speaker notes**
Walk one retired official question live (the `CREATE OR REPLACE TABLE` one from the exam guide) and model the elimination: option C is CTAS misuse, option D invents syntax (`WITH COLUMNS`), option B fails the "regardless of whether it exists" requirement — A stands. Teach this elimination rhythm; we repeat it every week.

**Visual suggestion**
Screenshot-style mock question with the four options and strike-through annotations.

**Exam relevance**
Meta-skill; the quiz at the end of class mirrors this style.

**Common misconception**
That exam distractors are obviously wrong. They're plausible — usually correct syntax for a *different* task.

---

### Slide 15: Wrap-Up and What's Next

**Key bullets**
- Today: platform, Delta, UC names, tables/views, medallion — the vocabulary of everything that follows
- Homework: docs reading + practice notebook (15–20 min)
- Next week: ingestion — COPY INTO, Auto Loader, Lakeflow Connect, and building bronze→silver for real
- Bring questions about anything that felt Azure-shaped

**Speaker notes**
Recap the three anchors: one copy of data in Delta, one governance tree in UC, one design pattern (medallion). Assign homework explicitly and tell them the Week 2 lab builds directly on today's schema and volume — don't delete them.

**Visual suggestion**
Three-icon summary (Delta log, UC tree, medallion flow) + homework checklist.

**Exam relevance**
Consolidation.

**Common misconception**
—

---

## 4. Instructor Demo

### Demo: From Sample Data to Governed Delta Tables (and Back in Time)

**Goal**
Prove the Week 1 concepts live: three-level namespace navigation, managed table creation via DDL and CTAS, `DESCRIBE EXTENDED` interpretation, Delta versioning + time travel, and volumes as governed file storage. Everything runs on Databricks Free Edition serverless compute.

**Setup**
- Free Edition workspace, logged in; a SQL editor tab or a notebook attached to serverless compute (SQL warehouse for SQL-only, or serverless notebook compute)
- Uses the read-only `samples` catalog (`samples.nyctaxi.trips`) — available in Free Edition
- Creates schema `week1_demo` inside the `workspace` catalog
- `datasets/week1_retail_sales.csv` downloaded locally (for the volume-upload step)

**Notebook Cells**

```sql
-- Cell 1: Orientation — the three-level namespace
-- Browse what governance gives us for free
SHOW CATALOGS;
SHOW SCHEMAS IN samples;

-- Query shared sample data with a fully qualified name
SELECT trip_distance, fare_amount, pickup_zip, dropoff_zip
FROM samples.nyctaxi.trips
LIMIT 10;
```

```sql
-- Cell 2: Create our working schema (in the workspace catalog)
CREATE SCHEMA IF NOT EXISTS workspace.week1_demo;
USE CATALOG workspace;
USE SCHEMA week1_demo;
```

```sql
-- Cell 3: DDL — an empty managed Delta table with explicit schema
CREATE OR REPLACE TABLE trip_zones (
  zip          STRING,
  zone_label   STRING,
  is_airport   BOOLEAN
);

INSERT INTO trip_zones VALUES
  ('10001', 'Midtown',  false),
  ('11371', 'LaGuardia', true),
  ('11430', 'JFK',       true);

SELECT * FROM trip_zones;
```

```sql
-- Cell 4: CTAS — create AND populate in one statement, schema inferred
CREATE OR REPLACE TABLE short_trips AS
SELECT
  pickup_zip,
  dropoff_zip,
  CAST(trip_distance AS DOUBLE) AS trip_distance,
  fare_amount
FROM samples.nyctaxi.trips
WHERE trip_distance < 2;

SELECT COUNT(*) AS short_trip_count FROM short_trips;
```

```sql
-- Cell 5: What did we actually make? Read DESCRIBE EXTENDED like the exam does
DESCRIBE EXTENDED short_trips;
-- Point out: Type = MANAGED, Provider = delta, Location = UC-managed storage
```

```sql
-- Cell 6: Delta versioning — every write is a version
UPDATE short_trips SET fare_amount = fare_amount + 1.00
WHERE pickup_zip = '10282';

DESCRIBE HISTORY short_trips;
```

```sql
-- Cell 7: Time travel — query the table as it was BEFORE the update
SELECT
  (SELECT ROUND(SUM(fare_amount), 2) FROM short_trips VERSION AS OF 0) AS total_v0,
  (SELECT ROUND(SUM(fare_amount), 2) FROM short_trips)                 AS total_now;
```

```sql
-- Cell 8: Volumes — governed storage for FILES
CREATE VOLUME IF NOT EXISTS workspace.week1_demo.landing;
-- ⏸️ UI step: Catalog Explorer → workspace → week1_demo → Volumes → landing
--    → Upload file → week1_retail_sales.csv
```

```sql
-- Cell 9: Query the raw file in place — no table yet
SELECT * FROM read_files(
  '/Volumes/workspace/week1_demo/landing/week1_retail_sales.csv',
  format => 'csv',
  header => true
)
LIMIT 5;
```

```sql
-- Cell 10: Views vs temp views
CREATE OR REPLACE VIEW airport_short_trips AS
SELECT s.*, z.zone_label
FROM short_trips s
JOIN trip_zones z ON s.dropoff_zip = z.zip
WHERE z.is_airport;

CREATE OR REPLACE TEMP VIEW scratch_fares AS
SELECT pickup_zip, AVG(fare_amount) AS avg_fare
FROM short_trips GROUP BY pickup_zip;

SHOW VIEWS IN week1_demo;
-- Note: the temp view appears with isTemporary=true and lives only in THIS session
```

**Instructor Script**
1. **Cell 1:** "Before we create anything, look what governance already gives us — catalogs I can browse, sample data I can query by its full address: `samples.nyctaxi.trips`. Catalog, dot, schema, dot, table. Say that pattern in your head every time — a third of exam questions contain one of these names."
2. **Cell 2:** "In Free Edition our writable catalog is `workspace`. I create a schema — that's level two of the hierarchy. `USE` statements just set defaults so I can type short names."
3. **Cell 3:** "Classic DDL — explicit columns, empty table. Notice what I did NOT write: `USING DELTA`. Delta is the default. This is exam-tested syntax — `CREATE OR REPLACE` means I can rerun this cell endlessly: idempotent, atomic, and the old versions stay in history."
4. **Cell 4:** "CTAS — schema comes from the query. Watch the CAST: that's how you control types in a CTAS, because a CTAS cannot take a column-type list. If an exam option shows `CREATE TABLE x AS SELECT` with `(col TYPE)` declarations — eliminate it."
5. **Cell 5:** "DESCRIBE EXTENDED is the exam's favorite forensic tool. Find three rows with me: **Type: MANAGED**, **Provider: delta**, and the **Location** pointing into UC-managed storage. If I dropped this table, those files go too. If Type said EXTERNAL, the files would survive a drop."
6. **Cells 6–7:** "One UPDATE — and DESCRIBE HISTORY shows a new version with operation, timestamp, and user: a free audit trail. Time travel: `VERSION AS OF 0` reads the original. Totals differ — the past is intact. Restoring is one command: `RESTORE TABLE`."
7. **Cell 8 + UI:** "Files need a governed home too — that's a volume. Watch the upload in Catalog Explorer." (Do the upload live; narrate the `/Volumes/workspace/week1_demo/landing/` path.)
8. **Cell 9:** "`read_files` queries the CSV *in place* — no table created. Next week this exact pattern becomes the front door of our ingestion pipeline."
9. **Cell 10:** "Two views: the permanent one is a governed UC object my teammates can query; the TEMP view dies with my session. If a colleague says 'I can't see your view' — first question: was it TEMP?"

**Expected Results**
- Cell 1: catalog list incl. `samples` and `workspace`; 10 taxi rows
- Cell 3: 3-row zones table
- Cell 4: a count in the tens of thousands (sample data varies)
- Cell 5: metadata rows showing `MANAGED`, `delta`, a UC storage location
- Cell 6: history with `CREATE OR REPLACE TABLE AS SELECT` (v0) and `UPDATE` (v1)
- Cell 7: `total_v0` < `total_now` (the +1.00 fares)
- Cell 9: 5 CSV rows with headers as columns
- Cell 10: `airport_short_trips` (permanent) and `scratch_fares` (isTemporary=true)

**Troubleshooting**
| Problem | Fix |
| --- | --- |
| `PERMISSION_DENIED` creating schema | You're not in the `workspace` catalog — Free Edition users have create rights on `workspace`, not on `samples` or `system`. Run `USE CATALOG workspace`. |
| `TABLE_OR_VIEW_NOT_FOUND: samples.nyctaxi.trips` | Catalog Explorer → confirm `samples` exists; occasionally delayed on brand-new accounts. Fallback: skip to Cell 3 and use `trip_zones` + the CSV for everything. |
| Cell 7 shows equal totals | The UPDATE matched no rows (zip not in sample slice). Pick a pickup_zip visible in Cell 4's data and rerun Cells 6–7. |
| `read_files` path error | Path is case-sensitive and must start `/Volumes/`. Copy the exact path from Catalog Explorer (kebab menu → Copy volume path). |
| Warehouse cold start (~30–60s) | Start the SQL warehouse before class; keep it warm by running Cell 1 at 0:40. |
| Temp view "not found" later in class | Session restarted — expected behavior; turn it into a teaching moment. |

---

## 5. Hands-On Lab

### Lab: Your First Governed Mini-Lakehouse

**Scenario**
You've just joined BrewMart, a small retail chain selling coffee equipment. Sales exports arrive as CSV files. Today you'll stand up the first governed slice of their lakehouse: a landing volume, a raw table, and the first curated objects — exactly the objects you learned to distinguish this session.

**Business Problem**
Sales data currently lives in emailed CSVs. Leadership wants it queryable, governed, and auditable in Databricks, with a reusable "sales by store" object the BI team can hit — and proof that accidental bad updates can be rolled back.

**Tasks**
1. Create your own schema `workspace.lab1_<yourname>` and a volume named `landing` inside it
2. Upload `week1_retail_sales.csv` to the volume (Catalog Explorer → your volume → Upload)
3. Query the file in place with `read_files()` to inspect it (how many rows? spot anything dirty?)
4. Create a managed Delta table `sales_raw` from the file using CTAS, casting `order_date` to DATE and computing `line_total` = quantity × unit_price
5. Run `DESCRIBE EXTENDED sales_raw` — confirm it is MANAGED and Delta
6. Create a **view** `sales_by_store` (total revenue + order count per store) and a **temp view** `my_scratch` (any exploratory query)
7. Simulate a mistake: UPDATE all unit prices to 0 — then prove recovery with `DESCRIBE HISTORY` and a `VERSION AS OF` query, and fix the table with `RESTORE TABLE`

**Starter Code**

```sql
-- Task 1: your schema + volume  (replace <yourname>)
CREATE SCHEMA IF NOT EXISTS workspace.lab1_<yourname>;
USE CATALOG workspace;
USE SCHEMA lab1_<yourname>;
CREATE VOLUME IF NOT EXISTS landing;

-- Task 2: upload week1_retail_sales.csv via Catalog Explorer UI

-- Task 3: inspect the raw file (fill in the path)
SELECT * FROM read_files(
  '/Volumes/workspace/lab1_<yourname>/landing/week1_retail_sales.csv',
  format => 'csv',
  header => true
);

-- Task 4: CREATE TABLE sales_raw AS SELECT ... (your turn)

-- Task 6: CREATE VIEW / CREATE TEMP VIEW (your turn)

-- Task 7: break it, inspect history, time-travel, RESTORE (your turn)
```

**Expected Solution**

```sql
-- Task 4
CREATE OR REPLACE TABLE sales_raw AS
SELECT
  order_id,
  CAST(order_date AS DATE)            AS order_date,
  customer_id,
  store,
  product,
  category,
  CAST(quantity AS INT)               AS quantity,
  CAST(unit_price AS DOUBLE)          AS unit_price,
  CAST(quantity AS INT) * CAST(unit_price AS DOUBLE) AS line_total
FROM read_files(
  '/Volumes/workspace/lab1_<yourname>/landing/week1_retail_sales.csv',
  format => 'csv',
  header => true
);

-- Task 5
DESCRIBE EXTENDED sales_raw;   -- Type: MANAGED, Provider: delta

-- Task 6
CREATE OR REPLACE VIEW sales_by_store AS
SELECT store,
       ROUND(SUM(line_total), 2) AS total_revenue,
       COUNT(DISTINCT order_id)  AS order_count
FROM sales_raw
GROUP BY store;

CREATE OR REPLACE TEMP VIEW my_scratch AS
SELECT category, SUM(quantity) AS units
FROM sales_raw
GROUP BY category;

-- Task 7
UPDATE sales_raw SET unit_price = 0;                 -- the "mistake"
DESCRIBE HISTORY sales_raw;                          -- find the UPDATE version
SELECT ROUND(SUM(line_total),2) FROM sales_raw VERSION AS OF 0;  -- the past is intact
RESTORE TABLE sales_raw TO VERSION AS OF 0;          -- roll back
SELECT ROUND(SUM(unit_price),2) FROM sales_raw;      -- prices are back
```

**Validation Checks**

```sql
-- 1. Raw file row count (expect 38 data rows, including 2 duplicate rows)
SELECT COUNT(*) FROM read_files(
  '/Volumes/workspace/lab1_<yourname>/landing/week1_retail_sales.csv',
  format => 'csv', header => true);

-- 2. Table is managed Delta
DESCRIBE EXTENDED sales_raw;     -- Type = MANAGED, Provider = delta

-- 3. View works and shows 3 stores + 1 null-store row
SELECT * FROM sales_by_store ORDER BY total_revenue DESC;

-- 4. History shows: CTAS (v0) → UPDATE (v1) → RESTORE (v2)
DESCRIBE HISTORY sales_raw;

-- 5. After RESTORE, revenue matches v0
SELECT
  (SELECT ROUND(SUM(line_total),2) FROM sales_raw VERSION AS OF 0) AS v0,
  (SELECT ROUND(SUM(line_total),2) FROM sales_raw)                 AS now;
-- v0 = now ✓
```

**Stretch Task**
The file contains two fully duplicated rows and some NULLs (a missing store, a missing unit_price). Create `sales_clean` with duplicates removed (`SELECT DISTINCT` or `ROW_NUMBER()`), then count how many rows were dropped. Bonus: which order has a NULL `line_total`, and why? (NULL arithmetic — Week 2 preview.)

**Instructor Notes**
- The two most common stalls: forgetting to replace `<yourname>` (schema name collision errors) and mistyping the volume path — show "Copy volume path" in Catalog Explorer early
- Watch for learners writing `CREATE TABLE sales_raw (order_id INT, ...) AS SELECT` — perfect moment to reinforce the CTAS rule from Slide 10
- If uploads misbehave for anyone, unblock them fast: have them CTAS directly from *your* demo volume path (read access works across the workspace catalog by default in Free Edition) — governance teaching moment
- The NULL store row in `sales_by_store` surprises people — leave it; Week 2 opens with exactly this data-quality conversation
- Fast finishers: send them to the stretch task rather than ahead in the deck

---

## 6. In-Class Activity

### Activity: "Right Object, Right Job" — Decision Cards

**Time needed:** 10 minutes (6 min in pairs + 4 min debrief)

**Setup**
Slide or handout with 6 mini-scenarios. Pairs decide: which object/feature fits, and one sentence why. No coding.

**Instructions**
"For each scenario, pick exactly one: managed table, external table, volume, view, temp view, or materialized view. You have 6 minutes. Be ready to defend your pick in exam language."

**Scenario cards**
1. Vendor drops 2GB of raw JSON log files daily; they must be governed but aren't queryable as-is yet
2. The finance team's dashboard re-runs an expensive 40M-row aggregation every 5 minutes; results only need hourly freshness
3. A regulated dataset must physically live in the company's own storage account, readable by a non-Databricks tool
4. You need a quick lookup of "today's weird orders" while debugging in your notebook this afternoon — nobody else needs it
5. Analysts keep rewriting the same 30-line join+filter; results must always reflect current data; reads are cheap
6. A new pipeline's curated output: queried by many teams, optimized automatically by Databricks, lifecycle fully managed

**Learner deliverable**
Each pair writes their six picks (one word each) in chat or on paper.

**Debrief answers**
1. **Volume** — non-tabular raw files under UC governance
2. **Materialized view** — precomputed; hourly staleness is acceptable, read cost matters
3. **External table** — storage-location requirement + external-tool access
4. **Temp view** — session-scoped scratch, no governance footprint
5. **View** — saved logic, always-current, cheap recompute
6. **Managed table** — the default; Databricks owns layout and optimization

**Teaching points**
- Exam questions are exactly these cards with more words — train the reflex: *find the constraint that forces the answer* ("must live in our storage" → external; "nobody else needs it" → temp)
- #2 vs #5 is the high-value contrast: MV trades freshness for read speed; view trades read cost for freshness
- Anyone answering #1 with "bronze table" is half right — the *files* land in a volume; loading them *into* a bronze table is Week 2

---

## 7. Markdown Mash Practice Quiz

# Week 1 Quiz: Lakehouse, Delta, and Unity Catalog Foundations
# Score 100

## Q1: A data engineer runs CREATE TABLE sales (id INT, amount DOUBLE) in Databricks without a USING clause. What table format is created?
- [ ] Parquet
- [x] Delta
- [ ] Iceberg
- [ ] CSV-backed external table
  ::time=20

## Q2: Which sequence correctly orders the Unity Catalog hierarchy from top to bottom?
- [ ] Catalog → metastore → schema → table
- [ ] Metastore → schema → catalog → table
- [ ] Workspace → catalog → table → schema
- [x] Metastore → catalog → schema → table
  ::time=20

## Q3: A managed table is dropped with DROP TABLE. What happens to its underlying data files?
- [x] They are deleted along with the metadata
- [ ] They remain in storage and must be cleaned up manually
- [ ] They are archived to a backup catalog automatically
- [ ] They are converted to an external table's files
  ::time=20

## Q4: In the reference my_catalog.finance.invoices, what does finance represent?
- [ ] A catalog
- [ ] A metastore
- [x] A schema
- [ ] A volume
  ::time=20

## Q5: Which Unity Catalog object is designed to store and govern non-tabular files such as raw CSVs and images?
- [ ] An external table
- [x] A volume
- [ ] A materialized view
- [ ] A Delta share
  ::time=20

## Q6: A data engineer must create a new Delta table that is immediately populated with the results of a query against an existing table, in a single statement. Which approach should they use?
- [ ] CREATE TABLE followed by COPY INTO
- [ ] CREATE TABLE followed by INSERT INTO ... SELECT
- [ ] CREATE OR REPLACE VIEW wrapping the query
- [x] CREATE TABLE ... AS SELECT (CTAS)
  ::time=20

## Q7: A colleague says they cannot find the view scratch_results that you created and queried successfully an hour ago. What is the most likely explanation?
- [x] It was created as a TEMP VIEW, so it exists only in your session
- [ ] Views must be refreshed before other users can query them
- [ ] The view was automatically vacuumed after 60 minutes
- [ ] Views are only visible to workspace admins by default
  ::time=30

## Q8: An analytics team needs to run ad-hoc SQL queries and power BI dashboards with fast startup and automatic scaling, and they write no Python. Which compute is the best fit?
- [ ] An all-purpose cluster shared by the team
- [ ] A job cluster triggered per dashboard refresh
- [x] A serverless SQL warehouse
- [ ] A single-node GPU cluster
  ::time=30

## Q9: DESCRIBE EXTENDED on a table shows Type: MANAGED. Which statement is true?
- [ ] The data files live in a customer-specified external location
- [x] Unity Catalog governs both the metadata and the data files' storage
- [ ] The table cannot be time traveled
- [ ] DROP TABLE will preserve the data files indefinitely
  ::time=30

## Q10: After an accidental UPDATE, a data engineer wants to query a Delta table exactly as it was at version 3. Which query is correct?
- [ ] SELECT * FROM events AT VERSION 3
- [ ] SELECT * FROM events.v3
- [ ] RESTORE TABLE events TO VERSION AS OF 3 inside a SELECT
- [x] SELECT * FROM events VERSION AS OF 3
  ::time=30

## Q11: Which statement about CTAS (CREATE TABLE AS SELECT) is correct?
- [x] The new table's column types are inferred from the query; a column-type list cannot be declared
- [ ] CTAS creates an empty table whose schema must then be populated with INSERT
- [ ] CTAS requires a USING DELTA clause to produce a Delta table
- [ ] CTAS column types are declared in parentheses before AS SELECT
  ::time=30

## Q12: A table was created with CREATE TABLE ... LOCATION 's3://corp-bucket/data/orders'. The table is then dropped. What is the result?
- [ ] Both metadata and the files at the location are deleted
- [ ] The drop fails because external tables cannot be dropped
- [x] The metadata is removed but the files at the location remain
- [ ] The files are moved into Unity Catalog managed storage
  ::time=30

## Q13: In a medallion architecture, what is the primary purpose of the bronze layer?
- [ ] Serving aggregated, business-ready metrics to BI tools
- [x] Preserving raw source data with minimal transformation for auditability and reprocessing
- [ ] Storing deduplicated, validated records with enforced types
- [ ] Caching query results for dashboard performance
  ::time=20

---

### Quiz Answer Key (with explanations)

| # | Answer | Difficulty | Explanation |
|---|--------|-----------|-------------|
| Q1 | Delta | Easy | Delta is the default table format in Databricks; `USING DELTA` is implicit. |
| Q2 | Metastore → catalog → schema → table | Easy | The three-level namespace `catalog.schema.table` sits under one metastore. |
| Q3 | Deleted with metadata | Easy | Managed = UC owns data + metadata; DROP removes both (briefly recoverable with UNDROP). |
| Q4 | Schema | Easy | Middle element of a three-level name is always the schema. |
| Q5 | Volume | Easy | Volumes govern non-tabular/file data; tables govern tabular data. |
| Q6 | CTAS | Applied | Single-statement create-and-populate is the definition of CTAS. COPY INTO and INSERT are two-step. |
| Q7 | TEMP VIEW session scope | Applied | Temp views are session-scoped and invisible to other users/sessions. The other options invent behavior. |
| Q8 | Serverless SQL warehouse | Applied | SQL-only + BI + instant start + autoscaling = SQL warehouse. Clusters are for general code/jobs. |
| Q9 | UC governs metadata + data | Applied | MANAGED means UC-managed storage; drop deletes data; time travel works on all Delta tables. |
| Q10 | VERSION AS OF | Applied | Exact time-travel syntax. RESTORE changes the table; the question asks only to query. |
| Q11 | Schema inferred; no type list | Tricky | The CTAS rule — control types by CASTing in the SELECT. Distractor D is the classic trap. |
| Q12 | Metadata removed, files remain | Tricky | LOCATION ⇒ external table ⇒ DROP is metadata-only. The files become unmanaged residue. |
| Q13 | Raw, minimally transformed | Easy | Bronze = fidelity + replayability; cleaning is silver; aggregation is gold. |

Difficulty mix: 6 easy / 5 applied / 2 tricky ≈ 46% / 38% / 15%. Correct answers distributed across positions 1–4.

---

## 8. Exam Tips for This Week

**What the exam is likely to test**
- Compute selection scenarios (warehouse vs. all-purpose vs. job vs. serverless) with cost reasoning
- DDL syntax discrimination: CREATE vs. CTAS vs. CREATE OR REPLACE vs. IF NOT EXISTS
- DROP semantics for managed vs. external tables (both directions)
- UC hierarchy levels and three-level naming
- Purpose of each medallion layer, stated abstractly
- Gold-object selection: table vs. view vs. materialized view vs. streaming table

**Keywords to recognize instantly**
`metastore`, `three-level namespace`, `managed/external`, `volume`, `_delta_log`, `DESCRIBE EXTENDED/HISTORY`, `VERSION AS OF` / `TIMESTAMP AS OF`, `RESTORE`, `serverless`, `Data Intelligence Platform`, `bronze/silver/gold`

**Common traps**
- Options that bolt a column-type list onto CTAS, or invent syntax like `WITH COLUMNS` or `USING DELTA` as a CTAS requirement
- "IF NOT EXISTS updates the table if it exists" — it does nothing if it exists
- Swapped DROP behavior (claiming external drops delete files, or managed drops preserve them)
- "All-purpose clusters for production jobs" — job clusters/job compute is the production answer on cost grounds
- Old terminology in your head vs. new terminology on the exam (Slide 13 table)

**How to eliminate wrong answers**
First locate the *forcing constraint* in the stem ("single statement," "regardless of whether it exists," "must remain in our storage account," "no one else needs it"). Usually exactly one option satisfies it; two options will be real features misapplied, and one will be invented syntax. Kill the invented syntax first.

**Memorize**
The UC hierarchy order; DROP semantics both ways; time-travel syntax (`VERSION AS OF n`, `TIMESTAMP AS OF '...'`); `/Volumes/<catalog>/<schema>/<volume>/` path shape; Delta = default format.

**Understand conceptually**
Why the transaction log enables ACID + time travel; why managed tables enable automatic optimization; why bronze stays raw; the freshness-vs-read-cost tradeoff between views and MVs.

---

## 9. Homework / Self-Study

**Databricks documentation to read (~40 min)**
- What is a data lakehouse? (docs → Lakehouse architecture)
- What is Delta Lake? (docs → Delta Lake overview)
- What is Unity Catalog? — focus on the object-model diagram
- Database objects: tables (managed vs. external) and volumes
- What is the medallion lakehouse architecture?

**Optional notebook practice (~20 min)**
1. Recreate the demo from a blank notebook *without looking* — schema, DDL table, CTAS from `samples.nyctaxi.trips`, one UPDATE, one time-travel query
2. Run `DESCRIBE DETAIL` on your table and compare its output to `DESCRIBE EXTENDED`
3. Try `DROP TABLE` then `UNDROP TABLE` on a scratch managed table

**Review questions (answer from memory, then verify)**
1. What two things does the `_delta_log` directory enable that plain Parquet cannot do?
2. You see `Type: EXTERNAL` in DESCRIBE EXTENDED. List two operational consequences.
3. When would a materialized view be the *wrong* choice even though reads are frequent?
4. Write the full path to a file `a.json` in volume `raw` in schema `iot` in catalog `prod`.

**Mini checklist before Week 2**
- [ ] My `lab1_<name>` schema, `sales_raw` table, and `landing` volume still exist (Week 2 builds on them)
- [ ] I can write a CTAS with casts from memory
- [ ] I can state DROP behavior for managed vs. external without hesitating
- [ ] Free Edition login works and the SQL warehouse starts

---

## 10. Instructor Preparation Checklist

**Before class (day before)**
- [ ] Log into your Free Edition workspace; confirm `samples.nyctaxi.trips` is queryable
- [ ] Pre-run the entire demo top to bottom in a clean schema; fix any drift (Free Edition evolves — verify `read_files` and `RESTORE` still behave as scripted)
- [ ] Confirm the `UPDATE` in Cell 6 actually matches rows (check a pickup_zip present in your sample slice; adjust the literal if needed)
- [ ] Drop/recreate `week1_demo` so DESCRIBE HISTORY is clean for class
- [ ] Distribute `datasets/week1_retail_sales.csv` to learners (LMS/email/repo link) with the instruction "download before class"
- [ ] Verify learners' accounts: send a "log in and run SELECT 1" pre-class task; chase non-responders

**Workspace objects needed**
- Schema `workspace.week1_demo` (created live in demo — have it pre-created in a hidden backup notebook in case of time pressure)
- Volume `workspace.week1_demo.landing`
- Local copy of `week1_retail_sales.csv` for the live upload

**Demo rehearsal**
- [ ] Rehearse the Catalog Explorer upload click-path — it's the only UI-dependent step and the UI moves; know the current location of "Upload to volume" and "Copy volume path"
- [ ] Time the demo: target 22 min talking + 3 min buffer; Cells 1–5 are cuttable to summary if running long, Cells 6–9 are not (history/time-travel/volume are the heart)
- [ ] Prepare the Slide 14 walkthrough of official sample Question 4 (CREATE OR REPLACE) with elimination annotations

**Backup plans**
- **Warehouse won't start / capacity issues:** switch to serverless notebook compute (attach notebook, same SQL runs); the demo is engine-agnostic
- **Sample catalog missing:** run everything from the CSV — CTAS `sales_raw` first, then do versioning/time-travel on it instead of `short_trips`
- **Upload UI broken:** fallback cell that builds `sales_raw` with `CREATE TABLE ... ; INSERT INTO ... VALUES`(keep a prepared INSERT script with ~10 rows); volumes become talk-through with screenshots
- **Total platform outage (rare):** teach slides + activity, run the quiz, swap demo/lab to a recorded screencast (record your rehearsal!) and assign the lab as homework — the Week 2 session starts with a 15-min lab catch-up
- **Screenshots to capture during rehearsal:** Catalog Explorer tree, volume upload dialog, DESCRIBE EXTENDED output, DESCRIBE HISTORY output — your outage insurance

---

*Next: Week 2 — Data Ingestion and Loading (COPY INTO, Auto Loader, Lakeflow Connect, bronze→silver).*
