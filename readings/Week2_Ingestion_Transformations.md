# Week 2: Ingestion and Bronze→Silver Transformations

**Exam domains:** Development and Ingestion, Data Processing & Transformations (cleaning, joins, dedup, MERGE, and quality). These align with the 2026 exam’s ingestion and transformation domains.  
**Estimated read time:** 30–40 minutes  
**Running example:** BrewMart daily sales files + corrections file

## Why This Week Matters

Together, Weeks 1 and 2 cover roughly **40%+ of the exam**. The exam heavily tests your ability to choose the right ingestion tool for a set of constraints and to build reliable silver tables on top of raw bronze.

The same skills also underpin later domains on productionizing pipelines (Jobs, CI/CD) and governance, so you’ll see these patterns and the idempotency theme repeated across the course.

The throughline of the entire course appears here: **a professional pipeline can be run twice without harm**.

- COPY INTO is idempotent at the *file* level.
- Auto Loader + checkpoints is idempotent at the *stream* level.
- MERGE is idempotent at the *row* level.

Everything else in later weeks (Jobs, repair, governance) depends on this property. The ingestion and transformation patterns from Weeks 1–2 are foundational to productionizing and governance topics that follow.

## The Ingestion Decision Ladder

Databricks offers a spectrum from most-managed (least code) to most-custom (most control):

1. **Lakeflow Connect managed connectors** — Fully managed ingestion for SaaS and database sources (Salesforce, SQL Server, etc.). It automatically lands data into Delta tables in the lakehouse. "Zero engineering" is the trigger phrase on the exam.
2. **Lakeflow Spark Declarative Pipelines** — declarative ETL that often uses Auto Loader concepts for file ingestion.
3. **Auto Loader** and **COPY INTO** — incremental file ingestion you configure.
4. **Structured Streaming** or **JDBC/REST in notebooks** — maximum control.

**Exam rule:** Given volume, frequency, source type, and engineering budget, pick the *most managed* option that satisfies every stated constraint.

### COPY INTO vs Auto Loader

| Dimension            | COPY INTO                              | Auto Loader                                      |
|----------------------|----------------------------------------|--------------------------------------------------|
| Language             | Pure SQL                               | PySpark Structured Streaming (`cloudFiles`)      |
| Scale                | Thousands of files                     | Millions of files                                |
| Discovery            | Lists source path on every run         | Directory listing (default) or file notification |
| Schema evolution     | `mergeSchema` option                   | Inference + `addNewColumns` + `_rescued_data`    |
| Idempotency          | Tracks files already loaded            | Checkpoint records progress                      |
| Best for             | SQL-first teams, scheduled batch       | High volume, evolving schemas, lower latency     |

**Important prerequisite:** COPY INTO requires the target table to exist before you run the command (use `CREATE TABLE IF NOT EXISTS` first if needed). This is a common exam detail.

**Trigger word test:**
- "SQL command" + "modest number of files" + "rerun-safe" → COPY INTO.
- "Millions of files", "schema drift", "near real-time" → Auto Loader.

**Key Auto Loader concepts:**
- `cloudFiles.format`
- `cloudFiles.schemaLocation` (remembers the schema)
- `checkpointLocation` (exactly-once bookkeeping)
- `.trigger(availableNow=True)` for batch-style use of streaming machinery
- `_rescued_data` column captures values that didn't match the schema instead of dropping or failing the stream
- `cloudFiles.schemaEvolutionMode` controls how new or incompatible columns are handled (for example `addNewColumns` or rescuing data into `_rescued_data`).

## Bronze vs Silver Contract

**Bronze** absorbs. Keep it as raw as possible (all strings + audit columns) so you can always replay.

**Silver** enforces. Here you:
- Cast to correct types
- Handle NULLs (`COALESCE`, filters)
- Standardize strings (`TRIM`, `INITCAP`)
- Deduplicate
- Add constraints (`NOT NULL`, `CHECK`)
- Compute derived columns (`line_total`)

**Pattern:** Read bronze → transform → write a *new* silver table. Never mutate bronze.

The same transformations must be expressible in both SQL and PySpark because the exam shows code in "SQL when possible, Python otherwise."

## Deduplication and the Latest-Row Pattern

- Full-row duplicates → `SELECT DISTINCT` or `dropDuplicates()`
- Keep the latest per key → `ROW_NUMBER() OVER (PARTITION BY key ORDER BY timestamp DESC) = 1`
- "Any row is fine" → `dropDuplicates(["key"])`

`approx_count_distinct` is called out by name in the exam outline for high-cardinality counts where exact is too expensive.

## MERGE INTO — The Idempotent Upsert

`MERGE INTO target USING source ON join_condition WHEN MATCHED THEN UPDATE SET * WHEN NOT MATCHED THEN INSERT *`

Use for:
- Late-arriving corrections
- CDC / slowly changing dimensions
- Deduplication on write

**Idempotency guarantee:** Running the same MERGE again converges to the identical state.

**Critical rule:** If multiple source rows match one target row, the statement fails with an ambiguous-update error. Deduplicate the source first.

## Data Quality Escalation Ladder

1. **Query checks** — cheap, manual, advisory (`WHERE` in your SELECT).
2. **Delta constraints** — `NOT NULL` or `CHECK`. A violating write **fails the entire transaction**. Not a filter. Constraints are enforced at write time (INSERT/UPDATE/MERGE); they do not retroactively scan existing rows.
3. **Quarantine pattern** — route bad rows to a separate table (`_quarantine`). Good rows load. Bad rows stay visible for investigation.
4. **Lakeflow Spark Declarative Pipelines expectations** — declarative rules with policies (warn / drop / fail). Concept only in early weeks.

**Exam trap:** "A CHECK constraint skips the bad rows." No — it rejects the whole write. Quarantine or expectations are what let the pipeline continue.

## Joins, Broadcast, and UNION

- Multi-key joins use `ON a.k1 = b.k1 AND a.k2 = b.k2`.
- **Broadcast join** — small table copied to every executor. Avoids shuffling the large side. Triggered automatically below ~10 MB or with `/*+ BROADCAST(dim) */`.
- `UNION` removes duplicates. `UNION ALL` keeps them.
- PySpark `df.union()` behaves like `UNION ALL` (no dedup, matches by **position**).
- `unionByName()` matches by name.

**Anti-join idiom:** `LEFT JOIN ... WHERE right.key IS NULL`.

## JSON and Nested Data

You do not need to flatten JSON at ingest time.

- After `read_files(..., format => 'json')`, structs are addressable with dot syntax (`contact.city`).
- Colon syntax (`contact:city`) works on raw JSON *strings*.
- `explode(array_col)` turns one row into N rows (one per element).

This is explicitly listed in the exam objectives.

## BrewMart Pipeline in Week 2

You will:
1. Upload daily files into a subfolder of your volume.
2. Use `COPY INTO` into a bronze table (prove rerun loads zero rows).
3. Upload a new day's file and prove only the new file loads.
4. Build `sales_silver` with casts, dedup, and a computed column.
5. Add constraints.
6. Apply a corrections file with `MERGE INTO`.
7. Prove the MERGE is idempotent.
8. Prove that a constraint violation aborts the whole write.

The corrections file deliberately contains both updates to Week 1 data and brand-new rows — this surfaces an important discussion about lineage and when rows become updates vs inserts.

## Exam Focus — High-Yield Decision Points

- "Which ingestion method?" → match volume, SQL vs code, schema drift, latency to the ladder.
- Rerun semantics of COPY INTO and checkpoints.
- `_rescued_data` purpose.
- `df.union()` vs SQL `UNION`.
- MERGE clause behavior and the multiple-matches error.
- Bronze absorbs / silver enforces.
- What constraints actually do vs what quarantine does.

## Self-Check Questions

1. A pipeline must load ~200 new CSV files nightly using only SQL. Reruns must be safe. Which tool? Why not the other incremental option?
2. Your MERGE statement fails with "multiple source rows match". What is the root cause and the fix?
3. Why does the bronze table keep the duplicate row that silver removes?
4. Write (from memory) the expression that keeps only the latest row per `order_id` based on `updated_at`.
5. A new column appears in the source files for an Auto Loader stream using default settings. What happens on the next run?

## Recommended Documentation

**Primary reading (~45 min)**

- Ingest data into a Databricks lakehouse (overview — the ETL stack)
- COPY INTO (reference + tutorial)
- What is Auto Loader? + Auto Loader schema inference and evolution
- Lakeflow Connect overview (skim standard vs managed connectors)
- MERGE INTO (SQL reference)
- Constraints on Databricks

**Practice targets**
- Build a small two-file COPY INTO flow from scratch proving zero rows on rerun.
- Reproduce your silver build in pure PySpark DataFrame API.
- Solve the official exam guide sample question about hospital billing (dedup + aggregation).

## Mini Checklist Before Week 3

- [ ] `sales_bronze` and `sales_silver` exist and pass the validation queries.
- [ ] I can sketch the COPY INTO and Auto Loader command skeletons from memory.
- [ ] I can state what each `WHEN MATCHED` / `WHEN NOT MATCHED` clause does.
- [ ] My lab notebook is saved — Week 3 will turn it into a scheduled Lakeflow Job.

The idempotent pipeline you built this week is the foundation for everything that follows. Week 3 removes the need to click "Run" by hand.
