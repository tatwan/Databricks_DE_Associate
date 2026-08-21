# Domain 2 — Data Ingestion & Loading — Answer Key

**Q1 — C: 0 rows.** COPY INTO tracks loaded files and skips them on rerun (idempotent). It does not reload, error, or truncate.

**Q2 — D: `INSERT INTO t SELECT * FROM read_files(...)`.** This re-inserts the whole source every run. COPY INTO, Auto Loader (checkpoint), and CREATE OR REPLACE are all rerun-safe.

**Q3 — B: `.format("cloudFiles")`.** That is the Auto Loader switch. `availableNow` sets cadence, `header` is a parse option, and `writeStream` just writes the stream.

**Q4 — A: The inferred schema, remembered across runs.** `schemaLocation` persists the inferred schema. It is not the output data, cluster config, or an audit log.

**Q5 — C: Values that don't fit the inferred schema.** `_rescued_data` is Auto Loader's safety net for non-conforming values — not deletes, duplicates, or a timestamp.

**Q6 — D: A file arrival trigger.** It fires when data lands — no empty polls, lower latency. Cron wastes runs, continuous is for always-on streams, and manual defeats automation.

**Q7 — B: Lakeflow Connect.** A managed Lakeflow Connect connector handles source-specific authentication, incremental reads, schema evolution, retries, and pipeline operations for supported sources. Auto Loader and COPY INTO are file-ingestion mechanisms you configure; MERGE is a transformation.

**Q8 — C: Standard connectors offer more customization; managed connectors automate more operations.** Standard connectors can be used through pipeline or streaming APIs when you need control. Managed connectors reduce operational work for supported sources. They are not identical, and "managed" does not mean more custom code.

**Q9 — B: Custom REST code in a notebook, orchestrated with Lakeflow Jobs.** A custom API with pagination needs client logic and scheduling. COPY INTO reads files rather than APIs, a trigger does not perform ingestion by itself, and a row filter controls visibility rather than movement.

**Q10 — B: Streaming machinery, batch cadence.** `availableNow=True` processes all new files then stops. It is not continuous, not one-row-per-trigger, and not literally a cron job.

**Q11 — C: Start with the most managed option that satisfies the requirements.** Databricks recommends beginning with the layer that minimizes operational work, then moving to standard connectors, pipelines, streaming, JDBC, or REST when the source or customization needs require it. Complexity is not a benefit by itself.

**Q12 — A: Only the new file's rows.** COPY INTO loads just the newly added file and skips the ones already recorded. It does not reload everything, load nothing, or double-load.

**Q13 — D: `explode(array_col)`.** `explode` emits one row per array element. `array_col.*`, `flatten_json`, and `unnest` are not the correct construct here.
