# Week 2: Data Ingestion and Loading + Bronze→Silver Transformations

> Aligned to the **May 4, 2026** Databricks Certified Data Engineer Associate exam guide.
> Primary exam domains: **Data Ingestion and Loading** (~20%, full coverage) + **Data Transformation and Modeling** (~22%, the cleaning/joins/dedup/MERGE/data-quality half).
> Continues the BrewMart storyline — learners need their Week 1 `lab1_<name>` schema, `sales_raw` table, and `landing` volume.

---

## 1. Session Overview

- **Duration:** 2 hours
- **Target audience:** Same cohort; Week 1 completed
- **Prerequisites:**
  - Week 1 lab objects still exist (`workspace.lab1_<name>` schema, `landing` volume, `sales_raw` table)
  - Week 2 files downloaded before class: `week2_sales_day2.csv`, `week2_sales_day3.csv`, `week2_corrections.csv`, `week2_customers.json`
  - Comfort with three-level names and CTAS (Week 1 checklist)
- **Main exam domains covered:**
  - Domain 2: Data Ingestion and Loading — all objectives (COPY INTO and Auto Loader hands-on; Lakeflow Connect and JDBC/REST as decision concepts)
  - Domain 3: Data Transformation and Modeling — cleaning, joins, set operations, dedup, aggregation, MERGE, data quality
- **Learning objectives.** By the end of this session, learners can:
  1. Classify ingestion patterns (batch, streaming, incremental) and map a scenario to the right tool: COPY INTO, Auto Loader, Lakeflow Connect standard/managed connectors, partner connectors, or JDBC/REST in notebooks
  2. Use `COPY INTO` to incrementally load files and explain *why* a rerun loads zero rows (idempotency)
  3. Describe Auto Loader's `cloudFiles` mechanics: schema inference, schema evolution modes, `_rescued_data`, directory listing vs. file notification
  4. Ingest and navigate semi-structured JSON (nested struct access with `:`/dot syntax, `explode()` for arrays)
  5. Build a silver table from bronze: null handling, casting/standardization, deduplication with `ROW_NUMBER()`, in SQL and PySpark
  6. Use joins (inner, left, broadcast, multi-key) and explain `UNION` vs. `UNION ALL`
  7. Apply `MERGE INTO` for idempotent upserts and corrections
  8. Enforce data quality with Delta constraints (`NOT NULL`, `CHECK`) and describe the quarantine pattern and LDP expectations (concept)

---

## 2. Recommended Timing

| Time      | Segment                      | Purpose                     |
| --------- | ---------------------------- | --------------------------- |
| 0:00–0:10 | Warm-up: Week 1 retrieval quiz (5 oral questions) + "what was dirty in our CSV?" | Activate prior knowledge; surface the dupes/NULLs learners found |
| 0:10–0:45 | Concept slides (15 slides)   | Ingestion decision framework, COPY INTO, Auto Loader, JSON, silver-layer transforms, MERGE, data quality |
| 0:45–1:10 | Instructor demo              | Incremental ingestion two ways + nested JSON |
| 1:10–1:40 | Hands-on lab                 | Bronze→silver pipeline with MERGE and constraints |
| 1:40–1:50 | In-class activity            | "Pick the ingestion method" scenario cards |
| 1:50–2:00 | Markdown Mash quiz + wrap-up | Exam readiness check, homework |

---

## 3. Slide Deck Content

### Slide 1: Recap and Today's Map

**Key bullets**
- Week 1 gave us governed objects; today we fill them — continuously
- Two exam domains today: Ingestion (~20%) + the transformation half of the biggest domain (~22%)
- Together: over 40% of your exam is in this session and its homework
- BrewMart storyline continues: daily files now arrive — loading them once isn't the job; loading them *repeatedly and safely* is

**Speaker notes**
Run the 5-question oral retrieval quiz first (DROP semantics, CTAS rule, hierarchy order, time-travel syntax, volume path). Then ask who did the stretch task — let a learner name the duplicates and NULLs in the Week 1 file. That dirty data is today's raw material. Frame the session's question: "How do you load files that keep arriving, without ever double-loading, and how do you turn raw into trustworthy?"

**Visual suggestion**
Course progress strip with Weeks 1–5; today highlighted with the two domain badges and "~40%+" callout.

**Exam relevance**
Orientation; weighting awareness drives study allocation.

**Common misconception**
That ingestion is "just reading files." The exam tests *selection between methods* and *incremental semantics* — not file reading.

---

### Slide 2: The Ingestion Decision Framework

**Key bullets**
- Three patterns: **batch** (load what's there, on demand/schedule), **incremental** (load only what's new), **streaming** (continuous, low latency)
- The Databricks ETL stack, most-managed to most-custom:
  1. **Lakeflow Connect managed connectors** (SaaS/databases: Salesforce, SQL Server, …) — fully managed
  2. **Lakeflow Spark Declarative Pipelines** (declarative ETL incl. Auto Loader under the hood)
  3. **Structured Streaming / custom code** — maximum control
- Plus: `COPY INTO` (SQL incremental file loading), partner connectors (Fivetran etc.), JDBC/REST in notebooks (pull APIs/DBs yourself)
- Exam framing: "Which option is the **most managed** / requires the **least code** / fits **this volume and frequency**?"

**Speaker notes**
This slide is the domain's skeleton — everything after refines one box. Teach learners to rank options on a "managed ↔ custom" axis; many exam questions resolve to "pick the most managed thing that satisfies the constraints." ADF translation: managed connectors ≈ ADF copy activity with built-in linked services; Auto Loader ≈ event-triggered incremental copies; JDBC-in-notebook ≈ self-authored ingestion. Don't deep-dive each box yet.

**Visual suggestion**
Layered pyramid or ladder: managed connectors (top, least code) → declarative pipelines → Auto Loader/COPY INTO → custom streaming/JDBC (bottom, most code), with a "control vs. convenience" double-headed arrow.

**Exam relevance**
Verbatim objective: "Prioritize between Auto Loader, Lakeflow Connect (standard and managed connectors), partner connectors, and other ingestion methods based on … volume, frequency, data types, governance."

**Common misconception**
That one tool is "best." The exam rewards matching constraints to tools, not tool loyalty.

---

### Slide 3: COPY INTO — Incremental Loading in Pure SQL

**Key bullets**
- `COPY INTO target FROM '/Volumes/...' FILEFORMAT = CSV FORMAT_OPTIONS(...) COPY_OPTIONS(...)`
- **Idempotent and retriable:** already-loaded files are tracked and skipped — rerun = 0 new rows
- Target must exist (or `CREATE TABLE IF NOT EXISTS target;` first); `COPY_OPTIONS('mergeSchema'='true')` for evolution
- Sweet spot: scheduled batch loads of **thousands** of files from cloud storage/volumes, SQL-first teams

**Speaker notes**
Live syntax matters here — they'll write it in the lab. Stress the file-tracking semantics: COPY INTO remembers which *files* it loaded (not which rows), which makes the rerun safe. That word "idempotent" is exam gold: same command, run twice, same result. Contrast with `INSERT INTO ... SELECT read_files(...)` from Week 1 — that would double-load. Mention `FORMAT_OPTIONS('header'='true','inferSchema'='true')` for CSV.

**Visual suggestion**
Timeline cartoon: Day 1 — 2 files, COPY INTO loads 2; Day 2 — 1 new file, COPY INTO loads 1 (the 2 old files greyed out with "skipped ✓").

**Exam relevance**
Verbatim objective: "Use the COPY INTO command to incrementally load files from cloud object storage into Unity-Catalog-governed tables."

**Common misconception**
"Rerunning COPY INTO duplicates the data." It doesn't — that's its whole point. (The trap inverts: appending the *same data from a renamed/moved file* WILL load again — tracking is per file.)

---

### Slide 4: Auto Loader — Scalable Incremental File Ingestion

**Key bullets**
- Structured Streaming source: `spark.readStream.format("cloudFiles")` + `cloudFiles.format` option
- Scales to **millions of files**; two discovery modes: **directory listing** (default) and **file notification** (event-driven, for very high volumes)
- **Schema inference** with a persisted schema location; **schema evolution** (default `addNewColumns`: stream stops on new column, picks it up on restart)
- **`_rescued_data`** column captures data that didn't match the schema (type mismatch, extra columns) instead of dropping it
- Batch-style usage: `.trigger(availableNow=True)` — process everything new, then stop

**Speaker notes**
Auto Loader is the heavyweight exam topic in this domain — syntax recognition is explicitly listed. Walk the anatomy: readStream + cloudFiles format + schemaLocation + checkpoint on the write side. Explain checkpoint = exactly-once bookkeeping (which files are done), schemaLocation = remembered schema across runs. The evolution default surprises people: the stream *fails* on a new column by design, then succeeds on restart with the merged schema — in a scheduled job, the retry makes this self-healing. `availableNow` is how "streaming" tech serves batch cadence — incremental without running 24/7.

**Visual suggestion**
Pipeline diagram: files dropping into a volume → Auto Loader box (schema store + checkpoint icons) → bronze Delta table; side panel showing `_rescued_data` catching a malformed value.

**Exam relevance**
Two verbatim objectives: "Classify valid Auto Loader sources and use cases" and "Demonstrate knowledge of Auto Loader syntax" (old guide), carried into the new guide as "Use Auto Loader with schema enforcement and schema evolution in batch modes (directory listing or file notification)."

**Common misconception**
"Auto Loader = always-on expensive streaming." With `availableNow` it runs on a schedule and stops — incremental ≠ continuous.

---

### Slide 5: COPY INTO vs. Auto Loader — The Exam's Favorite Fork

**Key bullets**
- Both: incremental, exactly-once file loading from cloud storage/volumes into Delta
- **COPY INTO:** SQL-native, simple, great for thousands of files, easy scheduled batch
- **Auto Loader:** scales to millions of files, file-notification mode, richer schema evolution + rescue, streaming-capable
- Databricks' own guidance: starting out / SQL-first / moderate volume → COPY INTO; high file volume, evolving schemas, streaming or near-real-time → Auto Loader

**Speaker notes**
Give them the two-question discriminator: (1) How many files / how often? (2) Does schema drift or latency matter? Volume in the millions, notifications, evolving schema, streaming → Auto Loader. SQL simplicity, periodic batch, manageable volume → COPY INTO. Note honestly: Databricks now nudges new pipelines toward Auto Loader / declarative pipelines generally, but COPY INTO remains fully supported and exam-listed — know both.

**Visual suggestion**
Two-column comparison table with rows: language, scale, discovery, schema evolution, typical trigger, exam keywords.

**Exam relevance**
Direct selection questions; both objectives are explicitly listed in Domain 2.

**Common misconception**
Treating them as rivals where one is "deprecated." Both are current; the exam tests *fit*, and several questions are answerable purely by spotting "millions of files" (→ Auto Loader) or "SQL command" (→ COPY INTO).

---

### Slide 6: Lakeflow Connect, Partner Connectors, and DIY (JDBC/REST)

**Key bullets**
- **Lakeflow Connect standard connectors:** built-in connectors for files/queues you configure
- **Lakeflow Connect managed connectors:** fully managed ingestion from enterprise SaaS/databases (e.g., Salesforce, SQL Server) into UC tables — least engineering
- **Partner connectors:** Fivetran & friends — when you've standardized on a partner stack
- **JDBC/ODBC or REST in notebooks:** pull from databases/APIs in code, land in volumes/tables, schedule with Lakeflow Jobs — most control, most maintenance

**Speaker notes**
Pure concept slide — Free Edition can't demo managed connectors (enterprise sources + infrastructure), so label it clearly: **"Exam concept; requires paid workspace for hands-on."** What the exam wants: given a source type and an engineering-effort constraint, pick the layer. "We need Salesforce data and have no engineers to spare" → managed connector. "Internal REST API, custom auth dance" → notebook + REST client + Lakeflow Jobs schedule. ADF folks: managed connectors are their linked-service reflex — tell them that reflex now answers exam questions.

**Visual suggestion**
Source-type matrix: SaaS app / database / cloud files / API → recommended ingestion layer for each.

**Exam relevance**
Verbatim objectives: "Configure Lakeflow Connect to reliably ingest data from diverse enterprise sources" and "Use JDBC/ODBC or REST clients in notebooks … usually orchestrated and scheduled with Lakeflow Jobs."

**Common misconception**
That JDBC-in-a-notebook is bad practice. It's the *right* answer when no connector exists — the exam includes it as a legitimate pattern, orchestrated by Jobs.

> **Exam concept; may require paid workspace or admin access for full hands-on practice** (managed connectors).

---

### Slide 7: Semi-Structured Data — JSON and Nested Fields

**Key bullets**
- JSON lands as columns + nested **structs** and **arrays** — no flattening required to store it
- Navigate structs: `contact:city` (colon syntax on raw JSON strings) or `contact.city` (dot syntax on parsed structs)
- Arrays: `explode(favorite_categories)` → one row per element
- `schema_of_json()` / `from_json()` to parse JSON strings; `read_files` infers JSON schema automatically

**Speaker notes**
Demo this in 20 minutes, so keep the slide tight. Key mental shift for warehouse people: you don't pre-flatten JSON into 14 staging tables — you store nested and query nested. Colon vs. dot trips people: colon digs into raw JSON *strings*, dot digs into properly typed *structs*; after `read_files` parses JSON, you're usually in struct land (dot). `explode` is explicitly named in the exam outline (Domain 3 "exploding arrays").

**Visual suggestion**
A JSON document on the left; arrows mapping `contact.city` to a scalar and `explode(favorite_categories)` fanning one row into three.

**Exam relevance**
Domain 2: "Ingest semi-structured and unstructured data (for example, JSON and nested data)." Domain 3: "exploding arrays."

**Common misconception**
That `explode` flattens structs. It expands *arrays* into rows; struct access is just dot/colon paths.

---

### Slide 8: Schema Enforcement vs. Schema Evolution (Now With Tools Attached)

**Key bullets**
- Enforcement (default): mismatched writes are **rejected** — your table's contract
- Evolution (opt-in): `mergeSchema` on writes, `COPY_OPTIONS('mergeSchema'='true')` on COPY INTO, `addNewColumns` mode in Auto Loader
- Auto Loader's extra safety net: `_rescued_data` — keeps non-conforming values instead of failing or dropping
- Pattern: **evolve in bronze, enforce in silver/gold**

**Speaker notes**
Week 1 introduced the concept; now attach it to each tool. The design pattern matters more than any switch: bronze should absorb drift (evolution + rescue), silver should be a contract (enforcement + constraints). That single sentence answers a family of exam questions. Quick oral check: "New column appears in source files. What happens with default Auto Loader settings?" (Stream fails with the new-column exception, schema location updated, restart succeeds.)

**Visual suggestion**
Two doors into a building: "Bronze door" wide open with a net (_rescued_data) vs. "Silver door" with a bouncer checking IDs (constraints).

**Exam relevance**
Auto Loader schema enforcement/evolution is a verbatim objective; data-quality placement questions lean on the bronze-vs-silver contract idea.

**Common misconception**
"Schema evolution is always on." Enforcement is the default everywhere; evolution is a deliberate opt-in per write/ingest tool.

---

### Slide 9: Bronze → Silver — Cleaning Like the Exam Expects

**Key bullets**
- Standard silver moves: handle NULLs (`COALESCE`, `WHERE x IS NOT NULL`), CAST to proper types, standardize strings (`TRIM`, `INITCAP`), derive columns
- Read bronze → transform → write silver as a **new table** (don't mutate bronze)
- Same logic, two dialects — SQL: `CAST(quantity AS INT)`; PySpark: `col("quantity").cast("int")`
- PySpark basics the exam expects: `select`, `withColumn`, `filter/where`, `withColumnRenamed`, `drop`, `na.fill/na.drop`

**Speaker notes**
The new exam outline says it verbatim: "reading bronze tables with PySpark/SQL, cleaning nulls, standardizing data types, and writing to new silver tables." Show the SQL and PySpark side by side for ONE transformation so the mapping clicks; the lab is SQL-first with a PySpark mirror provided. Remind them: exam code is SQL when possible, Python otherwise — DataFrame method names (`withColumn`, `na.drop`) do appear, so read them fluently even if they write SQL daily.

**Visual suggestion**
Split-screen code card: identical cleaning pipeline in SQL (left) and PySpark (right), arrows pairing equivalent lines.

**Exam relevance**
Verbatim Domain 3 objective; PySpark literacy is required since the May 2026 guide tests DataFrame operations explicitly.

**Common misconception**
NULL arithmetic: `quantity * unit_price` is NULL if either side is NULL — learners expect 0. (They saw this in Week 1's stretch task — call back to it.)

---

### Slide 10: Combining Data — Joins and Set Operations

**Key bullets**
- Inner, left/right, full outer, cross; multi-key joins: `ON a.k1 = b.k1 AND a.k2 = b.k2`
- **Broadcast join:** small table copied to every executor — no shuffle of the big side; Spark auto-broadcasts under `spark.sql.autoBroadcastJoinThreshold` (~10MB default); manual hint `/*+ BROADCAST(dim) */` or `broadcast(df)`
- `UNION` (SQL) removes duplicates; `UNION ALL` keeps everything — in DataFrames, `union()` behaves like SQL's UNION ALL (positional!)
- Left join + `WHERE right.key IS NULL` = anti-join idiom (find non-matches)

**Speaker notes**
Two exam hooks here. First, broadcast joins: the *why* (eliminate the shuffle for small-dim-to-big-fact joins) matters more than syntax; this resurfaces in Week 4's Spark UI session. Second, the UNION trap: SQL `UNION` dedupes, `UNION ALL` doesn't, and PySpark's `df.union()` does NOT dedupe and matches columns *by position* — three facts, one question family. Multi-key joins are listed verbatim in the outline, so show the AND syntax once.

**Visual suggestion**
Broadcast join sketch: tiny dim table duplicated onto three executor boxes holding fact partitions; below it, a UNION vs UNION ALL row-count mini-example (3+3 → 5 vs 6).

**Exam relevance**
Verbatim: "Inner join, left join, broadcast join, multiple keys, cross join, union, and union all."

**Common misconception**
"UNION is just faster UNION ALL." Backwards — UNION pays a dedup cost; UNION ALL is the cheap one. And `df.union()` ≠ SQL UNION.

---

### Slide 11: Deduplication and Aggregation

**Key bullets**
- Full-row dupes: `SELECT DISTINCT` / `df.distinct()` / `df.dropDuplicates()`
- Key-level dupes keeping the right row: `ROW_NUMBER() OVER (PARTITION BY key ORDER BY ts DESC) = 1` (or `dropDuplicates(["key"])` when "any row" is fine)
- Aggregations the exam names: `count`, `count(DISTINCT)`, **`approx_count_distinct`** (fast, approximate — for huge cardinalities), `mean/avg`, `summary()`/`describe()` for profiling
- GROUP BY + agg is identical in spirit across SQL and `df.groupBy(...).agg(...)`

**Speaker notes**
The retired official sample question (the hospital billing one) is exactly this: groupBy + sum + `count_distinct` with correct aliases — walk it if time allows. Teach the dedup decision: DISTINCT for identical rows; ROW_NUMBER when you must control *which* duplicate survives (latest timestamp). `approx_count_distinct` is in the outline by name: know it trades exactness for speed/memory on high-cardinality counts.

**Visual suggestion**
Table with 2 duplicate order rows; two filters shown: DISTINCT (either survives) vs ROW_NUMBER ordered by ingest time (the latest survives, highlighted).

**Exam relevance**
Verbatim: "data deduplication operations and aggregate operations … count, approximate count distinct, and mean, summary." Official sample Q1 tests exactly this pattern.

**Common misconception**
Using `count(DISTINCT patient_id)` when the question asks for distinct *invoices* — the official sample's actual trap. Read which column the business question counts.

---

### Slide 12: MERGE INTO — Upserts and Idempotent Pipelines

**Key bullets**
- One atomic statement: `MERGE INTO tgt USING src ON tgt.id = src.id WHEN MATCHED THEN UPDATE SET * WHEN NOT MATCHED THEN INSERT *`
- The tool for: late corrections, CDC apply, dedup-on-write, slowly changing data
- Idempotent by design: rerunning the same MERGE converges to the same state (matched rows update to identical values; nothing double-inserts)
- Optional clauses: `WHEN MATCHED AND <cond>`, `WHEN NOT MATCHED BY SOURCE THEN DELETE`

**Speaker notes**
Position MERGE as the answer to "the source sent us fixes" — exactly today's lab (corrections file fixing the NULL store and NULL price). Contrast with INSERT (append-only, duplicates on rerun) and UPDATE (can't add new rows). Say "atomic": one transaction, one new table version — check DESCRIBE HISTORY after. The idempotency framing ties the session together: COPY INTO is idempotent at the *file* level, MERGE at the *row* level — that's how professionals build rerunnable pipelines.

**Visual suggestion**
Venn-style: source rows vs target rows — overlap labeled "WHEN MATCHED → UPDATE", source-only labeled "WHEN NOT MATCHED → INSERT", with the corrections-file example rows.

**Exam relevance**
MERGE is core DML (Domain 3 "DDL/DML features"); upsert scenarios are a staple. The idempotency *concept* shows up in pipeline-design questions across domains.

**Common misconception**
"MERGE with multiple source rows matching one target row works fine." It errors (ambiguous update) — dedupe the source first. This is a classic real-world failure and a plausible exam distractor.

---

### Slide 13: Data Quality — Constraints, Quarantine, and Expectations

**Key bullets**
- Delta constraints: `ALTER TABLE t ALTER COLUMN c SET NOT NULL`; `ALTER TABLE t ADD CONSTRAINT chk CHECK (quantity > 0)`
- A violating write **fails the whole transaction** — constraints are contracts, not filters
- Quarantine pattern: route bad rows to a `_quarantine` table (filter + anti-filter), load only good rows — keeps pipelines flowing AND visible
- Lakeflow Spark Declarative Pipelines **expectations**: declarative rules with three policies — warn (keep + log), drop, fail — *concept here, hands-on Week 3 if pipeline features cooperate*

**Speaker notes**
The verbatim objective is "apply data quality checks and validation rules to ensure reliable Silver and Gold datasets." Teach the escalation ladder: validate-with-queries (cheap, manual) → constraints (enforced, all-or-nothing) → quarantine (graceful) → LDP expectations (declarative + metrics). Be explicit that a CHECK violation aborts the entire write — exam distractors claim "only the bad rows are skipped," which is exactly what constraints do NOT do (that's the quarantine pattern's job). Label LDP expectations: **"Exam concept; pipeline features in Free Edition may be limited — syntax shown, depth in Week 3."**

**Visual suggestion**
Ladder graphic with the four rungs (query checks → constraints → quarantine → expectations), each with a one-line "fails how?" annotation.

**Exam relevance**
Direct Domain 3 objective; expectations also appear under Lakeflow pipelines in Domains 2–4 contexts.

**Common misconception**
"A CHECK constraint drops the bad rows." No — it rejects the write. Declarative expectations with a `DROP` policy are the thing that drops rows.

---

### Slide 14: How Today Gets Tested (+ the Tuning-Parameter Cameo)

**Key bullets**
- Selection questions: keywords → tool ("millions of files" → Auto Loader; "SQL command, incremental" → COPY INTO; "Salesforce, minimal engineering" → managed connector)
- Mechanics questions: rerun semantics, `_rescued_data`, UNION vs UNION ALL, MERGE clauses
- Code-reading: PySpark groupBy/agg and join snippets — find the wrong alias/function
- Cameo (full story in Week 4): `spark.sql.shuffle.partitions`, `spark.sql.autoBroadcastJoinThreshold`, executor/driver memory — know they exist and what they influence

**Speaker notes**
Model one elimination live: "A pipeline must load ~200 new CSV files nightly from object storage using SQL. Reruns must be safe." Kill Auto Loader (works, but stem says SQL + modest volume — not *best*), kill INSERT SELECT (not rerun-safe), kill managed connector (files, not SaaS) → COPY INTO. Mention the four tuning parameters by name only — they're listed in this domain in the outline but pedagogically belong with the Spark UI in Week 4; promise the return.

**Visual suggestion**
Keyword→tool matching arrows; small footnote table of the four tuning params with one-word purposes.

**Exam relevance**
Trains the exact question style of Domains 2–3; flags the named tuning parameters so nobody is surprised.

**Common misconception**
Choosing the most *powerful* tool instead of the most *fitting* one. The exam's "best" = simplest thing satisfying every stated constraint.

---

### Slide 15: Wrap-Up — The Idempotency Thread

**Key bullets**
- Today's spine: load incrementally (COPY INTO / Auto Loader), absorb drift in bronze, enforce contracts in silver, upsert with MERGE — every step rerunnable
- You now own: a multi-file bronze, a constrained silver, and a corrections-driven MERGE flow
- Homework: ingestion docs + one PySpark mirror exercise
- Next week: this pipeline gets orchestrated — Lakeflow Jobs, triggers, and CI/CD with Git folders and bundles

**Speaker notes**
Close on the single idea: *a professional pipeline can be run twice without harm.* Ask the room to name where idempotency came from at each step (file tracking, checkpoints, MERGE keys). Tease Week 3: "you'll stop running these cells by hand."

**Visual suggestion**
The bronze→silver→gold flow annotated with the idempotency mechanism at each arrow.

**Exam relevance**
Consolidation; idempotency reasoning recurs in Jobs/troubleshooting questions.

**Common misconception**
—

---

## 4. Instructor Demo

### Demo: One River, Two Intakes — COPY INTO and Auto Loader (plus Nested JSON)

**Goal**
Show incremental, idempotent file ingestion both ways — `COPY INTO` (SQL) and Auto Loader (`cloudFiles`, PySpark, `availableNow`) — proving the zero-rows-on-rerun behavior live, then ingest nested JSON and navigate structs/arrays.

**Setup**
- Free Edition; **notebook** attached to serverless compute (this demo needs Python cells; SQL cells run in the same notebook)
- Week 1 demo schema reused: `workspace.week1_demo` with volume `landing`
- Files staged locally: `week2_sales_day2.csv`, `week2_sales_day3.csv`, `week2_customers.json`
- Create a subfolder structure in the volume via upload UI: `landing/sales_incoming/` (day2 file uploaded **before** class; day3 uploaded **live** mid-demo — that's the dramatic beat)

> **Free Edition note:** Auto Loader on serverless requires the batch-style `availableNow` trigger (continuous streaming options are restricted). That is exactly the mode the exam guide names ("batch modes"), so the constraint *is* the lesson. If `cloudFiles` errors in your workspace, use the documented fallback in Troubleshooting and teach the cell as a walkthrough.

**Notebook Cells**

```sql
-- Cell 1 (SQL): Setup — bronze target table for COPY INTO
USE CATALOG workspace;
USE SCHEMA week1_demo;

CREATE TABLE IF NOT EXISTS sales_bronze_copy (
  order_id    STRING,
  order_date  STRING,
  customer_id STRING,
  store       STRING,
  product     STRING,
  category    STRING,
  quantity    STRING,
  unit_price  STRING,
  _ingested_at TIMESTAMP
);
-- Bronze keeps strings + audit column: absorb now, type later (silver's job)
```

```sql
-- Cell 2 (SQL): First COPY INTO — loads day2 file
COPY INTO sales_bronze_copy
FROM (
  SELECT *, current_timestamp() AS _ingested_at
  FROM '/Volumes/workspace/week1_demo/landing/sales_incoming/'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');

SELECT COUNT(*) AS rows_loaded FROM sales_bronze_copy;
```

```sql
-- Cell 3 (SQL): Rerun the EXACT same command — idempotency proof
COPY INTO sales_bronze_copy
FROM (
  SELECT *, current_timestamp() AS _ingested_at
  FROM '/Volumes/workspace/week1_demo/landing/sales_incoming/'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');
-- num_inserted_rows: 0  ← nothing double-loads
```

```sql
-- Cell 4 (SQL): ⏸️ UI step first — upload week2_sales_day3.csv to sales_incoming/ NOW
-- Then rerun: only the NEW file loads
COPY INTO sales_bronze_copy
FROM (
  SELECT *, current_timestamp() AS _ingested_at
  FROM '/Volumes/workspace/week1_demo/landing/sales_incoming/'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');

SELECT COUNT(*) AS total_rows FROM sales_bronze_copy;  -- day2 + day3 rows
```

```python
# Cell 5 (Python): Auto Loader — same files, streaming machinery, batch trigger
checkpoint = "/Volumes/workspace/week1_demo/landing/_checkpoints/sales_al"

(spark.readStream
   .format("cloudFiles")
   .option("cloudFiles.format", "csv")
   .option("cloudFiles.schemaLocation", checkpoint)   # remembered schema
   .option("header", "true")
   .load("/Volumes/workspace/week1_demo/landing/sales_incoming/")
   .writeStream
   .option("checkpointLocation", checkpoint)          # exactly-once bookkeeping
   .trigger(availableNow=True)                        # process new files, then stop
   .toTable("workspace.week1_demo.sales_bronze_al")
   .awaitTermination()
)
```

```python
# Cell 6 (Python): Inspect Auto Loader's work — note _rescued_data
df = spark.table("workspace.week1_demo.sales_bronze_al")
print(df.count())
df.printSchema()   # all strings + _rescued_data column
display(df.limit(5))
# Rerun Cell 5 now → completes instantly, count unchanged (checkpoint = idempotent)
```

```sql
-- Cell 7 (SQL): Nested JSON — upload week2_customers.json to landing/ first
SELECT * FROM read_files(
  '/Volumes/workspace/week1_demo/landing/week2_customers.json',
  format => 'json'
);
-- contact arrives as a STRUCT, favorite_categories as an ARRAY — no flattening needed
```

```sql
-- Cell 8 (SQL): Navigate structs and explode arrays
SELECT
  customer_id,
  name,
  contact.city                    AS city,        -- dot into the struct
  loyalty_tier,
  explode(favorite_categories)    AS fav_category -- one row per array element
FROM read_files(
  '/Volumes/workspace/week1_demo/landing/week2_customers.json',
  format => 'json'
);
```

```python
# Cell 9 (Python): The same cleaning in PySpark — exam-required dialect
from pyspark.sql.functions import col, to_date, round as pround

silver_preview = (
    spark.table("workspace.week1_demo.sales_bronze_copy")
      .where(col("order_id").isNotNull())
      .withColumn("order_date", to_date("order_date"))
      .withColumn("quantity",   col("quantity").cast("int"))
      .withColumn("unit_price", col("unit_price").cast("double"))
      .withColumn("line_total", pround(col("quantity") * col("unit_price"), 2))
      .dropDuplicates(["order_id", "order_date", "customer_id"])
)
display(silver_preview.orderBy("order_id"))
# Same moves as SQL: filter, cast, derive, dedup — read both dialects fluently
```

**Instructor Script**
1. **Cell 1:** "Bronze table, all strings, plus an audit timestamp. Bronze absorbs; silver enforces — we decided that on the slides, now watch us live it."
2. **Cell 2:** "COPY INTO: target, source path, format, options. It loaded the day-2 file — note the result shows rows inserted and *files* processed. COPY INTO thinks in files."
3. **Cell 3:** "Same command, again. Zero rows. It remembered the file. This word — idempotent — is on your exam and in every production review you'll ever sit."
4. **Cell 4 + UI:** "A new day, a new file — I'm uploading day-3 right now… rerun: ONLY the new file loaded. That's an incremental pipeline in one SQL statement. No watermark table, no file log of our own — compare that to what you maintain in ADF."
5. **Cell 5:** "Same job, Auto Loader edition. Read the anatomy with me: readStream, format cloudFiles, the schema location where it persists what it learned, the checkpoint where it tracks progress, and availableNow — process everything new, then stop. Streaming machinery, batch cadence."
6. **Cell 6:** "Counts match COPY INTO's table. New column in the schema: `_rescued_data` — Auto Loader's safety net for values that don't fit. Rerun Cell 5 — instant, no new rows. Checkpoint = its memory."
7. **Cells 7–8:** "JSON with a nested struct and an array — stored as-is. Dot syntax walks into the struct; explode fans the array into rows. One customer with three favorite categories becomes three rows. That's the exam's 'exploding arrays.'"
8. **Cell 9:** "Everything we'll do in your SQL lab, in PySpark — filter, cast, derive, dropDuplicates. The exam shows Python when SQL can't express it; you need reading fluency, and now you have a Rosetta stone cell."

**Expected Results**
- Cell 2: 13 rows loaded (day2 file, incl. its duplicate row — bronze keeps it!)
- Cell 3: `num_inserted_rows = 0`
- Cell 4: total 23 rows (13 + 10 from day3)
- Cell 5/6: `sales_bronze_al` with 23 rows, schema all strings + `_rescued_data`
- Cell 8: ~10 customers fanning to ~18 rows after explode; `city` as a clean scalar
- Cell 9: typed, deduplicated preview with `line_total` computed (NULL for the order with missing price — call it out)

**Troubleshooting**
| Problem | Fix |
| --- | --- |
| COPY INTO: `UNSUPPORTED_FEATURE` or path error | Confirm the path ends with `/` (directory), files actually sit in `sales_incoming/`, and you're on the `workspace` catalog. |
| Cell 4 loads 0 rows after upload | The file landed in the wrong folder (root of `landing/`). Move/re-upload into `sales_incoming/`. |
| Auto Loader: `cloudFiles` not available / stream fails on serverless | Free Edition serverless evolves — if blocked, teach Cell 5 as a code-reading walkthrough (the syntax IS the exam objective) and show the equivalent result via `read_files`. Keep your rehearsal screenshot. |
| Auto Loader schema-evolution failure on rerun | A new column appeared (e.g., you pointed it at a folder with mixed files): that *is* `addNewColumns` behavior — restart the cell; it succeeds. Narrate it as a feature. |
| `[ROW_LEVEL] DUPLICATE` style MERGE errors later in lab | Source not deduped — exactly the Slide 12 misconception; have them ROW_NUMBER the source. |
| Checkpoint corruption after experiments | Delete the `_checkpoints/sales_al` folder and the `sales_bronze_al` table; rerun Cell 5 fresh. |
| JSON struct fields come back NULL | They used colon syntax on parsed structs or queried before inference finished — use dot syntax on `read_files` output. |

---

## 5. Hands-On Lab

### Lab: BrewMart's Incremental Bronze→Silver Pipeline

**Scenario**
BrewMart's ops team now drops a sales CSV into your landing volume every day or two. Head office also sends an occasional *corrections* file — fixes for orders that arrived with missing stores or prices, plus the odd brand-new late order. Your Week 1 one-shot load won't survive this. Time to build it properly.

**Business Problem**
Build a rerunnable pipeline: incrementally ingest daily files into an append-only bronze table, curate a typed/deduplicated silver table with constraints, and apply corrections via upsert — such that running any step twice never corrupts the data.

**Tasks**
1. In your `lab1_<name>` schema, create a `sales_incoming` folder in your `landing` volume; upload `week2_sales_day2.csv` (only!)
2. Create `sales_bronze` (all STRING columns + `_ingested_at TIMESTAMP`) and load it with `COPY INTO`; rerun to prove 0 rows; then upload `week2_sales_day3.csv` and rerun to load just the new file
3. Create `sales_silver` via CTAS from bronze: cast types, compute `line_total`, drop rows with NULL `order_id`, deduplicate exact duplicates
4. Add constraints to silver: `order_id` NOT NULL and a CHECK that `quantity > 0`
5. Upload `week2_corrections.csv` to `landing/` (NOT `sales_incoming/`) and `MERGE INTO sales_silver` — corrections update matched orders, new orders insert
6. Validate: corrected orders 1033/1034/1045/1048 now have store/price; new order 1059 exists; rerun the MERGE and confirm the table is unchanged (idempotency)

**Starter Code**

```sql
USE CATALOG workspace;
USE SCHEMA lab1_<yourname>;

-- Task 2: bronze table — fill in the column list (all STRING + _ingested_at)
CREATE TABLE IF NOT EXISTS sales_bronze (
  -- your columns here
);

COPY INTO sales_bronze
FROM (
  SELECT *, current_timestamp() AS _ingested_at
  FROM '/Volumes/workspace/lab1_<yourname>/landing/sales_incoming/'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');

-- Task 3: silver via CTAS — casts, line_total, filter NULL ids, dedup
-- CREATE OR REPLACE TABLE sales_silver AS ...

-- Task 4: constraints
-- ALTER TABLE sales_silver ...

-- Task 5: MERGE corrections (read the file with read_files in USING)
-- MERGE INTO sales_silver AS t
-- USING ( ... ) AS s
-- ON ...
-- WHEN MATCHED THEN ...
-- WHEN NOT MATCHED THEN ...
```

**Expected Solution**

```sql
-- Task 2
CREATE TABLE IF NOT EXISTS sales_bronze (
  order_id STRING, order_date STRING, customer_id STRING, store STRING,
  product STRING, category STRING, quantity STRING, unit_price STRING,
  _ingested_at TIMESTAMP
);
-- (COPY INTO as in starter; run → 13 rows, rerun → 0, upload day3, run → 10)

-- Task 3
CREATE OR REPLACE TABLE sales_silver AS
SELECT DISTINCT
  order_id,
  CAST(order_date AS DATE)    AS order_date,
  customer_id,
  store,
  product,
  category,
  CAST(quantity AS INT)       AS quantity,
  CAST(unit_price AS DOUBLE)  AS unit_price,
  ROUND(CAST(quantity AS INT) * CAST(unit_price AS DOUBLE), 2) AS line_total
FROM sales_bronze
WHERE order_id IS NOT NULL;

-- Task 4
ALTER TABLE sales_silver ALTER COLUMN order_id SET NOT NULL;
ALTER TABLE sales_silver ADD CONSTRAINT positive_qty CHECK (quantity > 0);

-- Task 5
MERGE INTO sales_silver AS t
USING (
  SELECT
    order_id,
    CAST(order_date AS DATE)   AS order_date,
    customer_id, store, product, category,
    CAST(quantity AS INT)      AS quantity,
    CAST(unit_price AS DOUBLE) AS unit_price,
    ROUND(CAST(quantity AS INT) * CAST(unit_price AS DOUBLE), 2) AS line_total
  FROM read_files(
    '/Volumes/workspace/lab1_<yourname>/landing/week2_corrections.csv',
    format => 'csv', header => true)
) AS s
ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

**Validation Checks**

```sql
-- 1. Bronze grew in two file-sized steps and never deduped
SELECT COUNT(*) FROM sales_bronze;                      -- 23 (13 + 10)

-- 2. Silver deduped the day2 duplicate (order 1046)
SELECT order_id, COUNT(*) FROM sales_silver GROUP BY order_id HAVING COUNT(*) > 1;  -- 0 rows

-- 3. Corrections applied
SELECT order_id, store, unit_price, line_total
FROM sales_silver WHERE order_id IN ('1045','1048','1059');
-- 1045 → Dallas/89.50 ; 1048 → 52.25 priced ; 1059 → present (inserted)

-- 4. MERGE idempotency: rerun the MERGE, then
DESCRIBE HISTORY sales_silver;
-- second MERGE version shows 0 inserted / matched updates rewrite same values
SELECT COUNT(*) FROM sales_silver;                      -- unchanged

-- 5. Constraint works (expect FAILURE — that's the pass condition)
INSERT INTO sales_silver VALUES
 ('9999', current_date(), 'C999', 'Atlanta', 'Test', 'Test', -1, 10.0, -10.0);
-- DELTA_VIOLATE_CONSTRAINT: positive_qty ✓ (whole write rejected)
```

**Stretch Task**
Orders 1033 and 1034 were corrected in head office's file — but your silver only contains week-2 bronze data, so the MERGE *inserted* them as new rows. Is that correct behavior? Discuss, then fix properly: load your Week 1 `sales_raw` into `sales_bronze`'s lineage (INSERT the Week 1 rows into silver first, then re-MERGE) and verify 1033/1034 became *updates*. Bonus (PySpark): reproduce Task 3 with `dropDuplicates` and `withColumn`, and compare `count()` vs `approx_count_distinct("customer_id")`.

**Instructor Notes**
- The corrections file deliberately contains orders (1033/1034) whose originals live in *Week 1's* table, not in this week's bronze — most learners won't notice the MERGE inserts rather than updates them. Validation 3 passes either way; the stretch task springs the trap. Gold-tier discussion if surfaced in debrief.
- Watch the COPY INTO path: learners who upload day3 into `landing/` root instead of `sales_incoming/` get 0 rows — same failure as the demo, now it's theirs
- The CHECK-constraint validation *intentionally fails* — warn the room before panic sets in ("an error message can be a green check")
- MERGE `UPDATE SET *` / `INSERT *` requires source and target columns to align — learners who added extra columns to silver will need explicit SET lists
- Fast finishers → stretch; the 1033/1034 discussion is worth stealing 2 minutes of wrap-up for

---

## 6. In-Class Activity

### Activity: "Pick the Intake" — Ingestion Method Selection Cards

**Time needed:** 10 minutes (6 min pairs + 4 min debrief)

**Setup**
Six scenario cards on a slide/handout. Options menu fixed at the top: **COPY INTO · Auto Loader · Lakeflow Connect managed connector · Partner connector (Fivetran) · JDBC/REST in a notebook · MERGE INTO**. One option per card; one card's best answer is deliberately arguable.

**Instructions**
"Same rules as last week: pick one, justify in one sentence, exam language. Find the forcing constraint."

**Scenario cards**
1. Marketing wants Salesforce objects synced into Unity Catalog daily; the team has zero spare engineering capacity
2. An IoT platform writes ~2 million small JSON files per day to object storage; schema adds fields quarterly; near-real-time freshness desired
3. Finance drops ~40 CSVs into a volume every night; the team is SQL-only and runs a scheduled query; reruns must be safe
4. You must pull from an internal REST API with custom token auth, nightly, landing results into a bronze table
5. Yesterday's customer dimension arrived with corrected addresses for ~3% of rows plus a handful of brand-new customers — apply to silver
6. The company already licenses Fivetran for 60 SaaS sources and wants one more source added with the same operational model

**Learner deliverable**
Six picks + the forcing constraint word(s) they spotted in each.

**Debrief answers**
1. **Lakeflow Connect managed connector** — SaaS source + "zero engineering" = most managed layer
2. **Auto Loader** — millions of files + schema evolution + near-real-time; file notification mode at that volume
3. **COPY INTO** — SQL-only + scheduled + rerun-safe + modest volume
4. **JDBC/REST in a notebook** (scheduled by Lakeflow Jobs) — no connector fits a custom API
5. **MERGE INTO** — not ingestion at all: an upsert into silver (the "arguable" card — accept reasoned Auto Loader+MERGE pipelines, but the *operation* is MERGE)
6. **Partner connector** — existing partner standardization is itself the constraint

**Teaching points**
- Card 5 is the point of the exercise: exam options mix ingestion tools and DML — recognize when the question is actually about *applying changes*, not *moving files*
- Constraint vocabulary → answer: "zero engineering" (managed), "millions/evolving" (Auto Loader), "SQL + rerun-safe" (COPY INTO), "custom auth" (DIY), "already standardized" (partner)
- If a pair argues well for a non-key answer, reward the reasoning, then show why the exam's "best" is narrower

---

## 7. Markdown Mash Practice Quiz

# Week 2 Quiz: Ingestion and Bronze→Silver Transformations
# Score 100

## Q1: A data engineer runs the same COPY INTO command twice in a row with no new files added. What happens on the second run?
- [ ] The target table doubles in size
- [ ] The command fails with a duplicate-file error
- [x] No new rows are loaded because already-ingested files are skipped
- [ ] The table is truncated and reloaded
  ::time=20

## Q2: Which format keyword identifies Auto Loader in a Structured Streaming read?
- [x] cloudFiles
- [ ] autoLoader
- [ ] deltaStream
- [ ] copyFiles
  ::time=20

## Q3: A query combines two result sets and must keep duplicate rows. Which SQL operator is correct?
- [ ] UNION
- [ ] INTERSECT
- [ ] UNION DISTINCT
- [x] UNION ALL
  ::time=20

## Q4: What is the purpose of the _rescued_data column produced by Auto Loader?
- [ ] It stores the filename and ingestion timestamp of each row
- [x] It captures data that did not match the expected schema instead of dropping it
- [ ] It holds rows quarantined by CHECK constraints
- [ ] It backs up each row before schema evolution
  ::time=20

## Q5: Which SQL command updates matching rows and inserts non-matching rows from a source into a Delta table in a single atomic operation?
- [ ] UPSERT INTO
- [x] MERGE INTO
- [ ] INSERT OVERWRITE
- [ ] APPLY CHANGES
  ::time=20

## Q6: A pipeline must ingest millions of small JSON files arriving continuously in cloud storage, with occasional new fields appearing in the data. Which ingestion method fits best?
- [x] Auto Loader with schema evolution enabled
- [ ] COPY INTO on a nightly schedule
- [ ] A managed Lakeflow Connect connector
- [ ] INSERT INTO with read_files in a loop
  ::time=30

## Q7: A team needs daily Salesforce data in Unity Catalog and wants the most managed solution with minimal engineering effort. What should they use?
- [ ] Auto Loader pointed at Salesforce exports
- [ ] A JDBC connection in a scheduled notebook
- [x] A Lakeflow Connect managed connector
- [ ] COPY INTO from the Salesforce REST API
  ::time=30

## Q8: A silver table must keep only the most recent record per customer_id based on updated_at. Which approach is correct?
- [ ] SELECT DISTINCT customer_id FROM source
- [ ] GROUP BY customer_id with MAX(updated_at) selecting all columns
- [ ] dropDuplicates() with no arguments
- [x] ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) and keep rows where it equals 1
  ::time=30

## Q9: A 6 MB store-dimension table is joined to a 900 GB sales fact table and the join is slow due to shuffling. What should the engineer consider?
- [ ] Converting the join to a cross join
- [x] A broadcast join so the small table is sent to every executor
- [ ] Splitting the fact table into multiple UNION ALL branches
- [ ] Increasing spark.sql.shuffle.partitions to shuffle faster
  ::time=30

## Q10: A column favorite_categories contains arrays like ["Kitchen","Appliances"]. What does explode(favorite_categories) return?
- [ ] One concatenated string per row
- [ ] A struct with one field per category
- [x] One output row per array element
- [ ] The array sorted alphabetically
  ::time=20

## Q11: A nightly job loads ~50 CSV files from a volume into a Delta table. The team works exclusively in SQL and needs safe reruns. Which option is BEST?
- [x] COPY INTO with the volume path as source
- [ ] Auto Loader with file notification mode
- [ ] A Lakeflow Connect managed connector
- [ ] CREATE OR REPLACE TABLE with read_files each night
  ::time=30

## Q12: Auto Loader is running with default schema evolution (addNewColumns). A new column appears in incoming files. What happens?
- [ ] The new column is silently dropped from all rows
- [ ] All new files are routed to _rescued_data permanently
- [ ] The stream continues and the column appears automatically mid-run
- [x] The stream stops with a schema-change error and picks up the new column on restart
  ::time=30

## Q13: A table has CHECK (quantity > 0). A batch INSERT of 1,000 rows includes 3 rows with quantity = -1. What is the result?
- [ ] 997 rows are inserted and 3 are skipped
- [x] The entire INSERT fails and no rows are written
- [ ] 997 rows are inserted and 3 go to _rescued_data
- [ ] The constraint converts the negative values to NULL
  ::time=30

## Q14: Customer records contain a struct column contact with fields email and city. After reading the JSON with read_files, which expression selects the city?
- [ ] contact->city
- [ ] explode(contact).city
- [x] contact.city
- [ ] city FROM LATERAL contact
  ::time=20

---

### Quiz Answer Key (with explanations)

| # | Answer | Difficulty | Explanation |
|---|--------|-----------|-------------|
| Q1 | No new rows | Easy | COPY INTO tracks loaded files; reruns skip them — its defining idempotency feature. |
| Q2 | cloudFiles | Easy | `format("cloudFiles")` is the Auto Loader source; the others are invented. |
| Q3 | UNION ALL | Easy | UNION dedupes; UNION ALL preserves duplicates (cheaper, too). |
| Q4 | Captures non-conforming data | Easy | `_rescued_data` keeps mismatched values rather than dropping/failing. |
| Q5 | MERGE INTO | Easy | The atomic upsert statement. UPSERT INTO doesn't exist; APPLY CHANGES is a declarative-pipeline CDC construct, not the generic SQL answer. |
| Q6 | Auto Loader | Applied | "Millions of files + continuous + evolving schema" are Auto Loader's signature constraints. |
| Q7 | Managed connector | Applied | SaaS source + most-managed requirement → Lakeflow Connect managed connector. |
| Q8 | ROW_NUMBER = 1 | Applied | Only the window-function pattern controls *which* duplicate survives. GROUP BY+MAX can't select all columns consistently; dropDuplicates() without args needs fully identical rows. |
| Q9 | Broadcast join | Applied | Small-dim-to-big-fact under the broadcast threshold eliminates the shuffle of the large side. |
| Q10 | One row per element | Applied | explode fans arrays into rows; it does not touch structs or order. |
| Q11 | COPY INTO | Tricky | Auto Loader also *works* — but "SQL-only + ~50 files + scheduled + rerun-safe" makes COPY INTO the *best* (simplest sufficient) answer. Classic best-fit question. |
| Q12 | Stops, then succeeds on restart | Tricky | addNewColumns fails the stream intentionally; the schema location is updated so the restart proceeds — self-healing under job retries. |
| Q13 | Entire INSERT fails | Tricky | Constraints are transactional contracts: one violation aborts the whole write. Skipping/quarantining requires explicit patterns or expectations with DROP. |
| Q14 | contact.city | Easy | Dot syntax navigates parsed structs (colon syntax is for raw JSON strings). |

Difficulty mix: 6 easy / 5 applied / 3 tricky ≈ 43% / 36% / 21%. Correct answers spread across positions 1–4.

---

## 8. Exam Tips for This Week

**What the exam is likely to test**
- Best-fit ingestion selection with constraint keywords (volume, frequency, SQL-only, SaaS source, engineering effort)
- COPY INTO rerun semantics and syntax shape; Auto Loader anatomy (cloudFiles, schemaLocation, checkpoint, triggers, discovery modes)
- Schema evolution behavior per tool; `_rescued_data`
- DataFrame code reading: joins, groupBy/agg, dropDuplicates, withColumn
- MERGE INTO clause logic and upsert scenarios
- Data-quality mechanics: what constraints do vs. what expectations do

**Keywords to recognize instantly**
`COPY INTO`, `cloudFiles`, `schemaLocation`, `availableNow`, `file notification`, `directory listing`, `_rescued_data`, `mergeSchema`, `addNewColumns`, `Lakeflow Connect`, `managed connector`, `MERGE INTO ... WHEN MATCHED`, `UNION ALL`, `broadcast`, `explode`, `approx_count_distinct`, `CHECK constraint`

**Common traps**
- "Rerunning COPY INTO duplicates data" — false; and its inverse trap: renamed/moved files DO reload
- `df.union()` dedupes — false (and it matches by position, not name)
- "CHECK constraints skip bad rows" — false; whole-write rejection
- Auto Loader framed as continuous-only/expensive — `availableNow` makes it batch
- Picking the most powerful tool over the simplest sufficient one (Q11 pattern)
- MERGE with duplicate source keys "just works" — it errors

**How to eliminate wrong answers**
Find the constraint nouns first: file count, frequency, language, source type, effort budget. Strike every option that violates *any* stated constraint, then pick the most managed/simplest survivor. In code questions, check aliases and the counted column before judging logic — the official samples hide errors there.

**Memorize**
COPY INTO skeleton (FROM path, FILEFORMAT, FORMAT_OPTIONS, COPY_OPTIONS); Auto Loader's four essentials (cloudFiles format, schemaLocation, checkpointLocation, trigger); MERGE skeleton; UNION vs UNION ALL; dot-vs-colon nested access.

**Understand conceptually**
Why file-tracking and checkpoints produce idempotency; bronze-absorbs/silver-enforces; when a broadcast join wins; why constraints are all-or-nothing while quarantine/expectations are graceful.

---

## 9. Homework / Self-Study

**Databricks documentation to read (~45 min)**
- Ingest data into a Databricks lakehouse (overview — the ETL-stack layering)
- COPY INTO (reference + tutorial page)
- What is Auto Loader? + Auto Loader schema inference and evolution
- Lakeflow Connect overview (skim: standard vs. managed connectors)
- MERGE INTO (SQL reference)
- Constraints on Databricks

**Optional notebook practice (~25 min)**
1. From scratch: build a two-file COPY INTO flow in a new schema, proving 0-rows-on-rerun without notes
2. Re-run the demo's Cell 5 Auto Loader against your own `sales_incoming/` folder; inspect the checkpoint folder's contents in the volume UI
3. PySpark mirror: reproduce your lab's Task 3 silver build using only DataFrame methods; finish with `groupBy("store").agg(...)` revenue per store
4. The exam-guide sample Question 1 (hospital billing): solve it before reading the answer

**Review questions**
1. COPY INTO tracks files; Auto Loader tracks files via checkpoints. Name a scenario where each one re-loads data you didn't expect.
2. Your MERGE failed with a multiple-matches error. What happened and what's the fix?
3. Why does the bronze layer keep the duplicate row that silver removes?
4. Write from memory the expression that keeps the latest row per key.

**Mini checklist before Week 3**
- [ ] `sales_bronze`, `sales_silver` exist and validations 1–4 pass
- [ ] I can sketch COPY INTO and Auto Loader skeletons from memory
- [ ] I can state what `WHEN MATCHED` / `WHEN NOT MATCHED` each do
- [ ] My notebook from the lab is saved — Week 3 turns it into a scheduled Job

---

## 10. Instructor Preparation Checklist

**Before class (day before)**
- [ ] Rerun the full demo in a clean state: drop `sales_bronze_copy`, `sales_bronze_al`, delete `_checkpoints/` and `sales_incoming/` contents, re-upload only day2
- [ ] **Test Cell 5 (Auto Loader) on current Free Edition serverless** — this is the one cell with platform risk; if it fails, prepare the walkthrough variant + screenshots from a working run
- [ ] Verify COPY INTO row counts match the script (13 / 0 / 23)
- [ ] Distribute all four Week 2 files to learners; remind them: upload only day2 before the lab
- [ ] Confirm learners' Week 1 schemas survived (spot-check 2–3 accounts or ask in channel)

**Workspace objects needed**
- `workspace.week1_demo` schema + `landing` volume with `sales_incoming/` subfolder (day2 file pre-uploaded)
- Local copies of day3 + customers JSON for the live uploads
- A hidden backup notebook with all demo cells pre-run (your outage insurance)

**Demo rehearsal**
- [ ] Practice the mid-demo upload of day3 — it must land in `sales_incoming/`, not the volume root (the #1 live-demo fumble)
- [ ] Time it: Cells 1–4 ≈ 10 min, Cell 5–6 ≈ 7 min, Cells 7–9 ≈ 8 min; if behind, Cell 9 becomes homework pointer
- [ ] Screenshot for outage kit: COPY INTO result with `num_inserted_rows`, Auto Loader stream result, `_rescued_data` schema, explode output

**Backup plans**
- **Auto Loader blocked on serverless:** teach syntax from the slide + screenshots; emphasize the exam objective is *syntax and use-case knowledge*, fully covered without execution
- **COPY INTO issues:** fall back to `INSERT INTO ... SELECT ... FROM read_files(...)` and *narrate* the idempotency loss — turns the failure into the lesson
- **Upload UI problems:** learners CTAS/COPY from your instructor volume paths (read works across the workspace catalog)
- **Platform outage:** slides + activity + quiz live; demo via rehearsal screenshots; lab assigned as homework with a 15-min catch-up scheduled at the top of Week 3

---

*Next: Week 3 — Lakeflow Jobs, Orchestration, and CI/CD (Git folders + Declarative Automation Bundles).*
