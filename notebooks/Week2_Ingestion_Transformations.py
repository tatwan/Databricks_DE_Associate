# Databricks notebook source
# MAGIC %md
# MAGIC # Week 2 — Ingestion and Bronze→Silver Transformations
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC Free Edition friendly. Requires your Week 1 schema + `landing` volume.
# MAGIC
# MAGIC | Part | Content |
# MAGIC |---|---|
# MAGIC | 1 | Setup |
# MAGIC | 2 | Demo — COPY INTO (idempotency proof), Auto Loader, nested JSON, PySpark mirror, NULL handling + latest-row dedup |
# MAGIC | 3 | **Your lab** — incremental bronze→silver with MERGE + constraints, then a gold join + aggregate |
# MAGIC | 4 | Solutions |
# MAGIC
# MAGIC **Files:** upload `week2_sales_day2.csv` into `landing/sales_incoming/` BEFORE Part 2. Keep `week2_sales_day3.csv`, `week2_corrections.csv`, `week2_customers.json` ready.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 1 — Reconnect to Your Week 1 Workspace
# MAGIC
# MAGIC **Goal:** Point this notebook at the *same* schema and `landing` volume you built in Week 1, so today's bronze and silver tables land beside last week's objects.
# MAGIC
# MAGIC **What happens:** The cell reads your schema name from the widget, switches the default catalog/schema, and builds the `VOL` path string we reuse all session. Nothing is created here — we are just connecting.
# MAGIC
# MAGIC **Before you run it:** Set the `user_schema` widget at the top to the **same** name you used in Week 1 (e.g. `lab1_yourname`). If it is wrong, you will not see your Week 1 tables.
# MAGIC
# MAGIC **Look for:** a printed line `Working in workspace.<your_schema> · volume root: /Volumes/workspace/<your_schema>/landing`.

# COMMAND ----------

dbutils.widgets.text("user_schema", "lab1_yourname")
USER_SCHEMA = dbutils.widgets.get("user_schema")
VOL = f"/Volumes/workspace/{USER_SCHEMA}/landing"

spark.sql("USE CATALOG workspace")
spark.sql(f"USE SCHEMA {USER_SCHEMA}")
print(f"Working in workspace.{USER_SCHEMA} · volume root: {VOL}")

# COMMAND ----------

# MAGIC %md ## Part 2 — Demo
# MAGIC The instructor will walk these cells. For each one: read the Goal, make the Prediction in your head, run it, then check the Look-for. You will reuse every pattern here in the lab.
# MAGIC
# MAGIC ### 2.1 Create the bronze target — all strings + an audit column
# MAGIC
# MAGIC **Goal:** Create an empty bronze table whose columns are **all `STRING`**, plus one `_ingested_at` timestamp. Bronze's job is to *absorb* whatever arrives; we type the data later, in silver.
# MAGIC
# MAGIC **Predict:** Why declare `quantity` and `unit_price` as `STRING` here when they are clearly numbers? (Hint: a malformed value in a typed column would reject the load.)
# MAGIC
# MAGIC **Look for:** the cell succeeds with no rows produced — `CREATE TABLE IF NOT EXISTS` only defines the structure. `IF NOT EXISTS` makes it safe to rerun without wiping data.
# MAGIC
# MAGIC **Why it matters:** "bronze absorbs, silver enforces" is a named exam objective. Keeping bronze all-strings is how you guarantee a bad row never blocks ingestion — you can always replay and fix typing downstream.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS sales_bronze (
# MAGIC   order_id STRING, order_date STRING, customer_id STRING, store STRING,
# MAGIC   product STRING, category STRING, quantity STRING, unit_price STRING,
# MAGIC   _ingested_at TIMESTAMP
# MAGIC );

# COMMAND ----------

# MAGIC %md ### 2.2 COPY INTO — incremental load, then prove it is idempotent
# MAGIC
# MAGIC **Goal:** Load the file(s) sitting in `landing/sales_incoming/` into `sales_bronze` with a single SQL command — then run the **same cell again** and watch it load **0 rows**.
# MAGIC
# MAGIC **Predict:** On the second run, how many rows get inserted? Why? (The `FROM (SELECT *, current_timestamp() ...)` subquery is how we stamp each row with an ingest time as it lands.)
# MAGIC
# MAGIC **Look for:** the result table shows `num_affected_rows` / `num_inserted_rows`. First run > 0; **second run = 0**. That property has a name: *idempotent*.
# MAGIC
# MAGIC **Why it matters:** COPY INTO tracks which **files** it has already loaded, so a scheduled rerun never double-loads. Contrast with `INSERT INTO ... SELECT read_files(...)`, which would re-insert everything every run. This is a top-tested ingestion fact.

# COMMAND ----------

display(spark.sql(f"""
COPY INTO sales_bronze
FROM (SELECT *, current_timestamp() AS _ingested_at FROM '{VOL}/sales_incoming/')
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true')
"""))

# COMMAND ----------

# MAGIC %md ### 2.3 Add a new day's file and prove only the new file loads
# MAGIC
# MAGIC **Goal:** Simulate "tomorrow's data arriving." Upload `week2_sales_day3.csv` into `sales_incoming/` (Catalog Explorer → your schema → Volumes → landing → sales_incoming → Upload), then **rerun the COPY INTO cell (2.2)** and run the count below.
# MAGIC
# MAGIC **Predict:** After uploading day 3 and rerunning, how many of the files in the folder get loaded — all of them, or just the new one?
# MAGIC
# MAGIC **Look for:** the row count grows by only the new file's rows. Expected: **13 rows after day 2, 23 rows after day 3.**
# MAGIC
# MAGIC **Why it matters:** this is incremental ingestion in one statement — exactly the pattern Week 3 will put on a schedule. The old files are skipped because COPY INTO already recorded them (you will see *where* in the next cell).

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS bronze_rows FROM sales_bronze;  -- 13 after day2, 23 after day3

# COMMAND ----------

# MAGIC %md ### 🔬 Under the Hood — Where does COPY INTO remember what it loaded? *(enrichment)*
# MAGIC **Goal:** See that COPY INTO's "already loaded" list is not a side database — it lives in this table's own Delta log.
# MAGIC
# MAGIC **Predict:** When you reran COPY INTO and got 0 rows, *where* did it look to know those files were done?
# MAGIC
# MAGIC **Look for:** an operation named `COPY INTO` in the history with `operationMetrics` — each commit records the files it ingested; a rerun skips paths already named in those commits.
# MAGIC
# MAGIC **One more reveal:** the next cell asks for the table's physical folder. On a **Unity Catalog managed table, the path comes back hidden/empty — by design.** UC brokers all access through the catalog so grants and auditing can never be bypassed via a raw storage path. That "failure" is Week 4's governance story arriving early. (On tables where a path IS exposed, the cell lists `part-*.parquet` + the `_delta_log/` JSON commits — exactly Week 1's picture.)
# MAGIC
# MAGIC **Why it matters:** this is Week 1's lesson made concrete — *the log IS the table's truth*. The exam tests the behavior (idempotent, file-tracked); this is the *why* behind it.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- the ingestion history is recorded in the table itself
# MAGIC DESCRIBE HISTORY sales_bronze;

# COMMAND ----------

# Try to find the table's physical location, then list its _delta_log.
# On UC MANAGED tables the location is hidden (empty) — that is a feature, not a bug.
detail = spark.sql("DESCRIBE DETAIL sales_bronze").collect()[0].asDict()
loc = detail["location"]

if loc:
    print("This 'table' is physically a folder:", loc)
    display(dbutils.fs.ls(loc))                  # part-*.parquet  +  _delta_log/
    print("\nInside _delta_log — the ordered JSON commits that ARE the table:")
    display(dbutils.fs.ls(loc + "/_delta_log"))
    # 00000.json, 00001.json, ... each COPY INTO appended a commit listing the files it ingested.
else:
    print("DESCRIBE DETAIL returned an EMPTY location — Unity Catalog is doing its job.")
    print("Managed-table storage paths are hidden so every read/write goes THROUGH the")
    print("catalog (grants, auditing, lineage) — no raw-path side door. Week 4 builds on this.")
    print("\nThe log is still fully inspectable — through the governed window:")
    hist = (spark.sql("DESCRIBE HISTORY sales_bronze")
                 .select("version", "timestamp", "operation", "operationMetrics")
                 .orderBy("version"))
    display(hist)   # operationMetrics.numFiles / numOutputRows per COPY INTO commit
# Either way: rerun loaded 0 rows because those file paths are already recorded in the log's commits.

# COMMAND ----------

# MAGIC %md ### 🔬 Under the Hood — Delta vs Parquet vs Iceberg: file format vs table format *(enrichment)*
# MAGIC Closing the Week 1 threads now that you can see the files:
# MAGIC
# MAGIC - **Parquet is a _file_ format.** One `part-*.parquet` holds columns + values, compressed. A *folder* of Parquet files has no history, no transactions, no single source of truth.
# MAGIC - **Delta is a _table_ format.** Same Parquet data files underneath — plus the `_delta_log` you just listed. The ordered JSON commits add ACID, time travel, and schema enforcement. *That database icon in Catalog Explorer is physically: Parquet files + a `_delta_log` folder.*
# MAGIC - **Iceberg is another _table_ format** (same idea, different metadata layout). Databricks interoperates with it via **UniForm** (a Delta table exposes Iceberg-readable metadata) and **managed Iceberg tables** in Unity Catalog.
# MAGIC
# MAGIC **Exam line:** Delta is the *default* table format on Databricks (`USING DELTA` is implicit). Iceberg/UniForm is enrichment — good to understand, not a tested objective here.

# COMMAND ----------

# MAGIC %md ### 2.4 Auto Loader — the same load, with streaming machinery
# MAGIC
# MAGIC **Goal:** Do the same incremental file load a second way — with Auto Loader — and learn to read its four essential pieces.
# MAGIC
# MAGIC **Read the anatomy before running** (each maps to a line in the code):
# MAGIC 1. `format("cloudFiles")` — this is what makes it Auto Loader.
# MAGIC 2. `cloudFiles.schemaLocation` — where it **remembers** the schema it inferred.
# MAGIC 3. `checkpointLocation` — its **exactly-once bookkeeping**: which files are already done.
# MAGIC 4. `trigger(availableNow=True)` — process all new files, then **stop** (streaming tech, batch cadence).
# MAGIC
# MAGIC **Predict:** This writes to a *new* table `sales_bronze_al`. After it runs once, what happens if you run it again with no new files?
# MAGIC
# MAGIC **Look for:** a row count matching your COPY INTO table, and a schema that is all strings **plus a `_rescued_data` column** — Auto Loader's safety net for values that do not fit.
# MAGIC
# MAGIC **Why it matters:** Auto Loader is the heavyweight ingestion topic — the exam expects you to *recognize this syntax* and know it scales to millions of files and handles schema drift. *(If serverless blocks the stream in your workspace, read it as exam syntax — recognizing the four pieces is the objective.)*

# COMMAND ----------

checkpoint = f"{VOL}/_checkpoints/sales_al"

(spark.readStream
   .format("cloudFiles")
   .option("cloudFiles.format", "csv")
   .option("cloudFiles.schemaLocation", checkpoint)   # remembered schema
   .option("header", "true")
   .load(f"{VOL}/sales_incoming/")
   .writeStream
   .option("checkpointLocation", checkpoint)          # exactly-once bookkeeping
   .trigger(availableNow=True)                        # process new files, then stop
   .toTable(f"workspace.{USER_SCHEMA}.sales_bronze_al")
   .awaitTermination())

df = spark.table(f"workspace.{USER_SCHEMA}.sales_bronze_al")
print("rows:", df.count())
df.printSchema()   # note _rescued_data

# COMMAND ----------

# MAGIC %md ### 🔬 Under the Hood — Auto Loader's checkpoint is a real folder *(enrichment)*
# MAGIC **Goal:** Open the checkpoint you passed and see the physical "exactly-once memory."
# MAGIC
# MAGIC **Predict:** If you rerun the Auto Loader cell above and it adds 0 rows, what on disk told it those files were already processed?
# MAGIC
# MAGIC **Look for:** `_schemas/` (the inferred schema, remembered), `offsets/` + `commits/` (stream progress), and a `sources/.../rocksdb` index (the files-already-seen list).
# MAGIC
# MAGIC **Why it matters:** "checkpoint = exactly-once" stops being a slogan once you can see the folder. Delete it and the next run reprocesses everything — amnesia.

# COMMAND ----------

print("The checkpoint/schema location is just a directory of files:")
display(dbutils.fs.ls(checkpoint))
# look for _schemas/  offsets/  commits/  metadata  sources/
print("\nThe schema Auto Loader inferred and now remembers across runs:")
display(dbutils.fs.ls(checkpoint + "/_schemas"))

# COMMAND ----------

# MAGIC %md ### 2.5 Semi-structured JSON — read nested data without pre-flattening
# MAGIC
# MAGIC **Goal:** Query a JSON file that has a nested object and an array, and pull them apart with SQL. First upload `week2_customers.json` to the **volume root** (`landing/`, not `sales_incoming/`).
# MAGIC
# MAGIC **Two moves to watch:**
# MAGIC - `contact.city` — a **dot path** reaches *into* a STRUCT (a nested object) on parsed JSON.
# MAGIC - `explode(favorite_categories)` — turns one row with an **ARRAY** into one row *per element*.
# MAGIC
# MAGIC **Predict:** If a customer has 3 favorite categories, how many rows will `explode` produce for that customer?
# MAGIC
# MAGIC **Look for:** one row per (customer × favorite category). A customer with 3 categories becomes 3 rows; the `city` column comes from inside the `contact` struct.
# MAGIC
# MAGIC **Why it matters:** the exam explicitly lists dot-access and `explode`. Mental shift for warehouse folks: you do **not** pre-flatten JSON into staging tables — you query the nested shape directly. (`explode` works on arrays only, not structs.)

# COMMAND ----------

display(spark.sql(f"""
SELECT customer_id, name,
       contact.city                 AS city,         -- dot into the STRUCT
       loyalty_tier,
       explode(favorite_categories) AS fav_category  -- one row per ARRAY element
FROM read_files('{VOL}/week2_customers.json', format => 'json')
"""))

# COMMAND ----------

# MAGIC %md ### 2.6 The PySpark mirror — the same cleaning, read in the other dialect
# MAGIC
# MAGIC **Goal:** See the silver-style cleaning expressed in **PySpark** so you can *read* it on the exam. This is a preview of the cleaning you will write yourself in Task 3 (in SQL).
# MAGIC
# MAGIC **Predict each line before running** — what does each step do to the data?
# MAGIC - `.where(col("order_id").isNotNull())` → drops rows with no order id
# MAGIC - `.withColumn("quantity", col("quantity").cast("int"))` → fixes the type (string → int)
# MAGIC - `.withColumn("line_total", ...)` → derives a new column
# MAGIC - `.dropDuplicates([...])` → removes duplicate rows
# MAGIC
# MAGIC **Look for:** a typed, deduplicated preview. Note this is a **preview only** — it does not create a table (no `.write`/`.saveAsTable`).
# MAGIC
# MAGIC **Why it matters:** the exam shows code "SQL when possible, Python otherwise," so you must read `withColumn`, `where`, and `dropDuplicates` as fluently as `SELECT`, `WHERE`, and `DISTINCT`. Same pipeline, two dialects.
# MAGIC
# MAGIC **Your SQL ↔ PySpark Rosetta stone** (study this table — DataFrame code appears on the exam):
# MAGIC
# MAGIC | Operation | SQL | PySpark |
# MAGIC |---|---|---|
# MAGIC | Filter | `WHERE order_id IS NOT NULL` | `.where(col("order_id").isNotNull())` |
# MAGIC | Cast | `CAST(quantity AS INT)` | `.withColumn("quantity", col("quantity").cast("int"))` |
# MAGIC | Derive | `ROUND(q * p, 2) AS line_total` | `.withColumn("line_total", round(col("q") * col("p"), 2))` |
# MAGIC | Full-row dedup | `SELECT DISTINCT` | `.dropDuplicates()` |
# MAGIC | Dedup by key | `ROW_NUMBER() ... = 1` | `.dropDuplicates(["key"])` (arbitrary survivor!) |
# MAGIC | Fill NULLs | `COALESCE(store, 'Unknown')` | `.fillna({"store": "Unknown"})` |
# MAGIC | Join | `a LEFT JOIN b ON a.k = b.k` | `a.join(b, "k", "left")` |
# MAGIC | Aggregate | `GROUP BY store` + `SUM(x)` | `.groupBy("store").agg(sum("x"))` |
# MAGIC | Distinct count | `COUNT(DISTINCT order_id)` | `countDistinct("order_id")` |
# MAGIC | Append rows | `UNION ALL` | `.union(df)` (by position!) / `.unionByName(df)` |

# COMMAND ----------

from pyspark.sql.functions import col, to_date, round as pround

silver_preview = (
    spark.table("sales_bronze")
      .where(col("order_id").isNotNull())
      .withColumn("order_date", to_date("order_date"))
      .withColumn("quantity",   col("quantity").cast("int"))
      .withColumn("unit_price", col("unit_price").cast("double"))
      .withColumn("line_total", pround(col("quantity") * col("unit_price"), 2))
      .dropDuplicates(["order_id", "order_date", "customer_id"])
)
display(silver_preview.orderBy("order_id"))

# COMMAND ----------

# MAGIC %md ### 2.7 NULL handling and "keep the latest" dedup — two everyday silver moves
# MAGIC
# MAGIC **Goal:** Practice the two cleaning patterns the exam names that we have not run yet: fill a NULL with a fallback (`COALESCE`), and keep only the **latest** copy of each key (`ROW_NUMBER`).
# MAGIC
# MAGIC **The difference that matters:**
# MAGIC - `SELECT DISTINCT` removes rows that are identical in *every* column — either copy survives, they are the same.
# MAGIC - `ROW_NUMBER() OVER (PARTITION BY key ORDER BY ts DESC) = 1` is for rows that share a key but *differ* — **you** choose which one survives (here: the most recently ingested, using our `_ingested_at` audit column).
# MAGIC
# MAGIC **Predict:** Order 1045 arrived with a NULL `store`. What will `COALESCE(store, 'Unknown')` return for it? And in the second query, if an order was loaded twice with different `_ingested_at` stamps, which copy is kept?
# MAGIC
# MAGIC **Look for:** `store_filled` shows `Unknown` where `store` is NULL; the dedup query returns exactly one row per `order_id` — the newest.
# MAGIC
# MAGIC **Why it matters:** the exam lists NULL handling and deduplication explicitly. `COALESCE` (SQL) = `fillna()` / `na.fill()` (PySpark); `WHERE col IS NOT NULL` = `na.drop()` / `.where(col(...).isNotNull())`. And "keep the most recent record per key" is a named question pattern whose answer is always the `ROW_NUMBER ... = 1` shape.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Move 1: COALESCE fills NULLs with a fallback (fillna in PySpark)
# MAGIC SELECT order_id, store, COALESCE(store, 'Unknown') AS store_filled
# MAGIC FROM sales_bronze
# MAGIC WHERE store IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Move 2: keep the LATEST row per order_id, using the audit column
# MAGIC SELECT * FROM (
# MAGIC   SELECT *,
# MAGIC          ROW_NUMBER() OVER (PARTITION BY order_id
# MAGIC                             ORDER BY _ingested_at DESC) AS rn
# MAGIC   FROM sales_bronze
# MAGIC ) WHERE rn = 1
# MAGIC ORDER BY order_id;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 3 — LAB: BrewMart's Incremental Bronze→Silver Pipeline
# MAGIC You already built `sales_bronze` incrementally above (Tasks 1–2 ✅).

# COMMAND ----------

# MAGIC %md ### TODO Task 3 — Build `sales_silver` with a CTAS
# MAGIC
# MAGIC **Goal:** Turn raw, all-string `sales_bronze` into a clean, typed `sales_silver` table in one `CREATE OR REPLACE TABLE ... AS SELECT` statement.
# MAGIC
# MAGIC **Before you code:** Bronze holds everything as `STRING`. Silver is where you *enforce*: cast to real types, compute a derived column, drop unusable rows, and remove duplicates. Build the `SELECT` first, then wrap it in `CREATE OR REPLACE TABLE`.
# MAGIC
# MAGIC **Your task:**
# MAGIC 1. `CREATE OR REPLACE TABLE sales_silver AS SELECT ...` from `sales_bronze`.
# MAGIC 2. Cast `order_date` → `DATE`, `quantity` → `INT`, `unit_price` → `DOUBLE`.
# MAGIC 3. Add `line_total` = rounded `quantity * unit_price` (to 2 decimals).
# MAGIC 4. Drop rows where `order_id IS NULL`.
# MAGIC 5. Remove exact duplicate rows (`SELECT DISTINCT`).
# MAGIC
# MAGIC **Expected result:** `sales_silver` exists with typed columns + `line_total`, no NULL `order_id` rows, and no exact duplicates. (Rows with a missing `unit_price` will have a `NULL` `line_total` — that is correct; NULL arithmetic returns NULL.)
# MAGIC
# MAGIC <details>
# MAGIC <summary>Hint — click to expand</summary>
# MAGIC
# MAGIC - `CAST(col AS TYPE) AS col` controls the output type, e.g. `CAST(quantity AS INT) AS quantity`.
# MAGIC - `ROUND(CAST(quantity AS INT) * CAST(unit_price AS DOUBLE), 2) AS line_total`.
# MAGIC - `SELECT DISTINCT` right after `SELECT` removes full-row duplicates.
# MAGIC - Filter NULLs with `WHERE order_id IS NOT NULL`.
# MAGIC </details>

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Fill in the blanks (____). Keep the columns you want in silver.
# MAGIC --
# MAGIC -- CREATE OR REPLACE TABLE sales_silver AS
# MAGIC -- SELECT DISTINCT
# MAGIC --   order_id,
# MAGIC --   CAST(order_date AS ____)        AS order_date,
# MAGIC --   customer_id, store, product, category,
# MAGIC --   CAST(quantity   AS ____)        AS quantity,
# MAGIC --   CAST(unit_price AS ____)        AS unit_price,
# MAGIC --   ROUND(____ * ____, 2)           AS line_total
# MAGIC -- FROM sales_bronze
# MAGIC -- WHERE ____ ;        -- keep only rows with a real order_id

# COMMAND ----------

# MAGIC %md ### TODO Task 4 — Add constraints so bad data is rejected at write time
# MAGIC
# MAGIC **Goal:** Make `sales_silver` enforce two rules: `order_id` can never be NULL, and `quantity` must be positive.
# MAGIC
# MAGIC **Before you code:** Constraints are silver's "bouncer." A write that violates a constraint **fails the entire transaction** — it does *not* silently skip the bad row. Constraints check writes going forward (INSERT/UPDATE/MERGE); they do not scan rows already in the table.
# MAGIC
# MAGIC **Your task:** Write **two** `ALTER TABLE` statements:
# MAGIC 1. Set `order_id` to `NOT NULL`.
# MAGIC 2. Add a named `CHECK` constraint requiring `quantity > 0`.
# MAGIC
# MAGIC **Expected result:** both statements succeed. (They only succeed if your current silver data already satisfies them — which it will, after Task 3.) You will *prove* the constraint bites in validation cell (c).
# MAGIC
# MAGIC <details>
# MAGIC <summary>Hint — click to expand</summary>
# MAGIC
# MAGIC - NOT NULL uses `ALTER COLUMN`: `ALTER TABLE t ALTER COLUMN col SET NOT NULL;`
# MAGIC - CHECK uses `ADD CONSTRAINT`: `ALTER TABLE t ADD CONSTRAINT name CHECK (condition);`
# MAGIC - A constraint needs a name, e.g. `positive_qty`.
# MAGIC </details>

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Two statements. Fill in the blanks (____).
# MAGIC --
# MAGIC -- ALTER TABLE sales_silver ALTER COLUMN ____ SET NOT NULL;
# MAGIC -- ALTER TABLE sales_silver ADD CONSTRAINT ____ CHECK (____);

# COMMAND ----------

# MAGIC %md ### TODO Task 5 — Apply a corrections file with MERGE (the idempotent upsert)
# MAGIC
# MAGIC **Goal:** A corrections file arrives with fixes to some existing orders **and** a few brand-new orders. Apply it in one atomic `MERGE`: matched orders get **updated**, unmatched orders get **inserted**.
# MAGIC
# MAGIC **Before you code:** First upload `week2_corrections.csv` to the **volume ROOT** (`landing/`, not `sales_incoming/`). The corrections file is raw (all strings), so your `USING` source must clean/cast it to the *same shape* as `sales_silver` before merging — otherwise types will not line up.
# MAGIC
# MAGIC **Your task:**
# MAGIC 1. Read the corrections CSV with `read_files(..., format => 'csv', header => true)`.
# MAGIC 2. In that subquery, cast the columns exactly like Task 3 (so the source matches silver).
# MAGIC 3. `MERGE INTO sales_silver AS t USING (<that subquery>) AS s ON t.order_id = s.order_id`.
# MAGIC 4. `WHEN MATCHED THEN UPDATE SET *` and `WHEN NOT MATCHED THEN INSERT *`.
# MAGIC
# MAGIC **Expected result:** existing orders show the corrected values; the new orders appear as fresh rows. Rerunning the same MERGE changes nothing further — that is *idempotency at the row level*.
# MAGIC
# MAGIC <details>
# MAGIC <summary>Hint — click to expand</summary>
# MAGIC
# MAGIC - This is a Python cell, so wrap the statement in `spark.sql(f""" ... """)` to use the `{VOL}` path variable.
# MAGIC - The `USING` source is a full `SELECT ... FROM read_files('{VOL}/week2_corrections.csv', format => 'csv', header => true)` with the same casts as Task 3.
# MAGIC - `UPDATE SET *` / `INSERT *` copy all matching columns — they require the source columns to match the target.
# MAGIC - **Trap:** if two source rows share one `order_id`, MERGE errors ("multiple source rows matched"). Deduplicate the source first if needed.
# MAGIC </details>

# COMMAND ----------

# Fill in the blanks (____). This is Python, so the f-string lets you use {VOL}.
#
# spark.sql(f"""
# MERGE INTO sales_silver AS t
# USING (
#   SELECT order_id,
#          CAST(order_date AS ____) AS order_date,
#          customer_id, store, product, category,
#          CAST(quantity   AS ____) AS quantity,
#          CAST(unit_price AS ____) AS unit_price,
#          ROUND(____ * ____, 2)    AS line_total
#   FROM read_files('{VOL}/week2_corrections.csv', format => 'csv', header => true)
# ) AS s
# ON t.____ = s.____
# WHEN MATCHED     THEN ____
# WHEN NOT MATCHED THEN ____
# """)

# COMMAND ----------

# MAGIC %md ### 🔬 Under the Hood — What your MERGE did to the Parquet files *(enrichment)*
# MAGIC **Run this AFTER your Task 5 MERGE.**
# MAGIC
# MAGIC **Goal:** See that a MERGE is one atomic commit that rewrites files — the physical reason it creates a new version and is safe to rerun.
# MAGIC
# MAGIC **Predict:** Did MERGE edit rows in place, or rewrite whole files?
# MAGIC
# MAGIC **Look for:** a `MERGE` operation whose `operationMetrics` show rows updated/inserted AND files added/removed. Classic Delta = **copy-on-write**: a changed row rewrites its entire Parquet file.
# MAGIC
# MAGIC **Why it matters:** "new version" and "idempotent" are the same fact seen from storage. (Modern runtimes may use *deletion vectors* — soft-deletes that defer the rewrite to `OPTIMIZE`. The exam tests the behavior, not the mechanism.)

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY sales_silver;     -- find operation = MERGE, then read operationMetrics

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL sales_silver;      -- numFiles = how many Parquet files back the table right now

# COMMAND ----------

# MAGIC %md ### TODO Task 6 — Enrich and serve: join the customer dimension, aggregate to gold
# MAGIC
# MAGIC **Goal:** Close the medallion loop: join `sales_silver` to a customer dimension built from the nested JSON, then aggregate into a gold object a BI team could use.
# MAGIC
# MAGIC **Before you code:** You queried `week2_customers.json` in demo 2.5 but never kept it. A dimension this small (10 rows) joined to a growing fact table is the classic **broadcast join** shape — Spark copies the small side to every executor so the big side never shuffles. It happens automatically under the ~10MB threshold; on the exam, recognize the `/*+ BROADCAST(c) */` hint.
# MAGIC
# MAGIC **Your task:**
# MAGIC 1. CTAS `customers_dim` from `read_files('{VOL}/week2_customers.json', format => 'json')`, keeping `customer_id`, `name`, `loyalty_tier`, and `contact.city AS city` (dot into the struct — no explode needed here).
# MAGIC 2. Create gold view `revenue_by_city_tier`: **LEFT JOIN** `sales_silver s` to `customers_dim c` on `customer_id`, so sales from unknown customers are kept.
# MAGIC 3. Use `COALESCE(c.city, 'Unknown')` for the city (2.7's move — some silver customer_ids are not in the dim).
# MAGIC 4. Group by city and `loyalty_tier`; compute `ROUND(SUM(line_total), 2) AS revenue` and `COUNT(DISTINCT s.order_id) AS orders`.
# MAGIC
# MAGIC **Expected result:** a small city × tier grid, plus an `Unknown` city row — proof your LEFT JOIN kept unmatched sales. An INNER JOIN would have silently dropped them: the exam's favorite join bug.
# MAGIC
# MAGIC *Short on time? Finish this one as homework — it is in the solution review.*
# MAGIC
# MAGIC <details>
# MAGIC <summary>Hint — click to expand</summary>
# MAGIC
# MAGIC - Step 1 is Python (needs `{VOL}`): `spark.sql(f"""CREATE OR REPLACE TABLE customers_dim AS SELECT customer_id, name, loyalty_tier, contact.city AS city FROM read_files('{VOL}/week2_customers.json', format => 'json')""")`
# MAGIC - Step 2 skeleton: `CREATE OR REPLACE VIEW revenue_by_city_tier AS SELECT COALESCE(c.city,'Unknown') AS city, c.loyalty_tier, ... FROM sales_silver s LEFT JOIN customers_dim c ON s.customer_id = c.customer_id GROUP BY ...`
# MAGIC - Why a **view** for gold here? Cheap recompute, always current — Week 1's gold-object menu. A materialized view would fit if this were an expensive aggregation hit constantly.
# MAGIC - PySpark mirror to read: `s.join(c, "customer_id", "left").groupBy("city", "loyalty_tier").agg(round(sum("line_total"), 2).alias("revenue"), countDistinct("order_id").alias("orders"))`
# MAGIC </details>

# COMMAND ----------

# TODO Task 6.1: build customers_dim (Python cell — you need the {VOL} path)
# spark.sql(f""" CREATE OR REPLACE TABLE customers_dim AS SELECT ... """)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO Task 6.2: gold view with LEFT JOIN + COALESCE + aggregates
# MAGIC -- CREATE OR REPLACE VIEW revenue_by_city_tier AS
# MAGIC -- SELECT ...
# MAGIC -- FROM sales_silver s LEFT JOIN customers_dim c ON ...
# MAGIC -- GROUP BY ... ;
# MAGIC -- SELECT * FROM revenue_by_city_tier ORDER BY revenue DESC;

# COMMAND ----------

# MAGIC %md ### Validation

# COMMAND ----------

# MAGIC %sql
# MAGIC -- a) no duplicate order_ids in silver
# MAGIC SELECT order_id, COUNT(*) FROM sales_silver GROUP BY order_id HAVING COUNT(*) > 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- b) corrections applied: 1045 has a store, 1048 has a price, 1059 exists
# MAGIC SELECT order_id, store, unit_price, line_total
# MAGIC FROM sales_silver WHERE order_id IN ('1045','1048','1059') ORDER BY order_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- c) constraint works — this INSERT must FAIL (the error IS the green check)
# MAGIC INSERT INTO sales_silver VALUES
# MAGIC  ('9999', current_date(), 'C999', 'Atlanta', 'Test', 'Test', -1, 10.0, -10.0);

# COMMAND ----------

# MAGIC %sql
# MAGIC -- d) (Task 6) LEFT JOIN kept unmatched sales: expect an 'Unknown' city row
# MAGIC SELECT * FROM revenue_by_city_tier ORDER BY revenue DESC;

# COMMAND ----------

# MAGIC %md ### ⭐ Stretch
# MAGIC Orders 1033/1034 were *inserted*, not updated — their originals live in Week 1's `sales_raw`, not this bronze. Backfill Week 1 rows into silver, re-MERGE, and verify they become updates. Bonus: rebuild Task 3 in pure PySpark and compare `count()` vs `approx_count_distinct("customer_id")`.

# COMMAND ----------

# MAGIC %md ---
# MAGIC ## Solution
# MAGIC The solution file will be shared by your instructor.
# MAGIC
# MAGIC ✅ Keep your completed schema and tables — the next week builds on them.
