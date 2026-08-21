# Week 1 Overview — Answer Key & Explanations

**Q1 — C: `catalog.schema.table`.** Unity Catalog's hierarchy is catalog → schema → table. The other orders invert the levels; "database" is the legacy term for schema and never comes first.

**Q2 — D: A managed Delta table.** No `USING` means Delta (the default format); no `LOCATION` means Unity Catalog manages the storage, i.e., managed. It would be *external* only if you specified a `LOCATION`, and *Parquet* only with an explicit `USING PARQUET`.

**Q3 — D: Columns/types come from the SELECT.** CTAS derives the schema from the query, so you control types with `CAST(...)`. The trap answer is the one that pairs CTAS with a separate `(column TYPE, ...)` list — that is invalid syntax. CTAS also populates the table, so "empty table" is wrong.

**Q4 — B: `DESCRIBE EXTENDED`.** It returns schema plus detailed metadata including `Type` and `Provider`. `SHOW TABLES` only lists names; `DESCRIBE HISTORY` shows versions/operations; `SHOW TBLPROPERTIES` shows properties, not the table type.

**Q5 — A: Managed deletes data + metadata; external deletes metadata only.** Dropping a managed table removes its files; dropping an external table leaves the files in your external location (only the catalog entry goes). "Both keep" and "both delete" are the classic distractors.

**Q6 — A: `SELECT ... VERSION AS OF 0`.** Time travel *reads* an old snapshot without modifying the table. `RESTORE` would change the current state; `UNDROP`/`VACUUM` are unrelated (recover a dropped table / delete old files).

**Q7 — B: `RESTORE TABLE t TO VERSION AS OF 0`.** To make an old version the live table again you restore it. `VERSION AS OF` only reads the past. `UNDROP` recovers a *dropped* table, not a bad update; `VACUUM` deletes files.

**Q8 — C: Volumes.** Volumes govern non-tabular files (CSV, JSON, images, libraries). Tables govern rows/columns; catalogs and schemas are namespace levels, not file stores.

**Q9 — A: A persistent view (`CREATE VIEW`).** A persistent UC view survives the session and is queryable by authorized users. A `TEMP VIEW`, a Python variable, and a widget value all disappear when the session ends.

**Q10 — D: Delta is a table format (Parquet files + `_delta_log`).** Delta stores the same Parquet data files plus an ordered JSON transaction log that adds ACID, time travel, and schema enforcement. Delta does not replace Parquet and is not a codec.

**Q11 — B: Reads in place, no table created.** `read_files(...)` returns rows from the file for inspection; you still need a CTAS or COPY INTO to persist a table. It neither registers a table nor moves files, and it supports CSV, JSON, and more.

**Q12 — C: Nothing changes — safe no-op.** `IF NOT EXISTS` skips creation when the table exists; it does not overwrite, error, or alter the schema. (Use `CREATE OR REPLACE` when you *do* want to redefine.)

**Q13 — D: The last committed snapshot.** Delta writes are atomic, so readers always see a complete committed version, never a half-applied update. They are not blocked and do not see an empty table.
