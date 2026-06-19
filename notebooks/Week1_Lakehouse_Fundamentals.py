# Databricks notebook source
# MAGIC %md
# MAGIC # Week 1 — Lakehouse Foundations: Delta Lake, Unity Catalog, and Table Fundamentals
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC Runs entirely on **Databricks Free Edition** (serverless).
# MAGIC
# MAGIC | Part | Content |
# MAGIC |---|---|
# MAGIC | 1 | Setup (your schema) |
# MAGIC | 2 | Instructor-led example — namespace, DDL, CTAS, time travel, volumes, views |
# MAGIC | 3 | **Your lab** — build the BrewMart mini-lakehouse in the TODO cells |
# MAGIC | 4 | Finish and keep your work for Week 2 |
# MAGIC
# MAGIC Part 2 is a worked example: predict what each cell will do, then follow the instructor's explanation. In Part 3, you apply the same ideas to a new dataset.
# MAGIC
# MAGIC ### Why SQL in this lab?
# MAGIC SQL is the clearest language for today's table, metadata, governance, and query tasks. It is **declarative**: you describe the result you want, and Databricks plans how to execute it. These operations are also directly relevant to the certification exam.
# MAGIC
# MAGIC - **SQL:** best fit here for DDL, CTAS, metadata inspection, views, and table recovery.
# MAGIC - **Python/PySpark:** useful for reusable program logic, control flow, complex transformations, and orchestration.
# MAGIC - **Scala:** provides direct access to Spark's JVM APIs and appears in some engineering codebases, but it is not needed for today's objectives.
# MAGIC
# MAGIC Databricks notebooks can mix languages. This notebook uses Python for the reusable schema setting and SQL for the data-engineering operations.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 1 — Set Up Your Workspace
# MAGIC
# MAGIC **Goal:** Create an isolated schema for your work so your objects do not conflict with another learner's objects.
# MAGIC
# MAGIC **What happens:** The Python cell reads the name from a widget, switches to the writable `workspace` catalog, creates the schema if needed, and makes it the default schema.
# MAGIC
# MAGIC **Before you run it:** Replace `yourname` with a short unique name. Use letters, numbers, and underscores only.
# MAGIC
# MAGIC **Look for:** The final message should show `workspace.<your_schema>`.

# COMMAND ----------

dbutils.widgets.text("user_schema", "lab1_yourname")
USER_SCHEMA = dbutils.widgets.get("user_schema")

spark.sql("USE CATALOG workspace")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {USER_SCHEMA}")
spark.sql(f"USE SCHEMA {USER_SCHEMA}")
print(f"Working in: workspace.{USER_SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 2 — Instructor-Led Example
# MAGIC
# MAGIC The instructor will demonstrate the pattern you will reuse in the BrewMart lab. The early SQL is worth typing; later prepared cells may be pasted so the discussion stays focused on the engineering decisions.
# MAGIC
# MAGIC ### 2.1 Find Objects with the Three-Level Namespace
# MAGIC
# MAGIC **Goal:** Connect Unity Catalog's hierarchy to the object names used in SQL.
# MAGIC
# MAGIC A full object address is `catalog.schema.object`. `SHOW CATALOGS` lists the top level available to you.
# MAGIC
# MAGIC **Predict:** Which two catalogs should be useful today: the writable catalog and the read-only sample catalog?
# MAGIC
# MAGIC **Look for:** `workspace` and `samples` in the result.

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW CATALOGS;

# COMMAND ----------

# MAGIC %md
# MAGIC **Goal:** Read a table without changing the current catalog or schema.
# MAGIC
# MAGIC The fully qualified name `samples.nyctaxi.trips` supplies all three namespace levels, so Databricks knows exactly which table to read.
# MAGIC
# MAGIC **Look for:** Ten taxi rows and the four selected columns. This is a read-only shared sample table.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT trip_distance, fare_amount, pickup_zip, dropoff_zip
# MAGIC FROM samples.nyctaxi.trips
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2.2 Create an Empty Managed Delta Table with DDL
# MAGIC
# MAGIC **Goal:** Define a table schema first, then insert rows.
# MAGIC
# MAGIC `CREATE OR REPLACE TABLE` makes the cell safe to rerun. No `USING` clause and no `LOCATION` are specified, so Databricks creates a **managed Delta table** by default.
# MAGIC
# MAGIC **Predict:** How many rows will the final `SELECT` return, and which column proves that the schema preserved a Boolean type?
# MAGIC
# MAGIC **Look for:** Three rows and `true`/`false` values in `is_airport`.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE trip_zones (
# MAGIC   zip        STRING,
# MAGIC   zone_label STRING,
# MAGIC   is_airport BOOLEAN
# MAGIC );
# MAGIC
# MAGIC INSERT INTO trip_zones VALUES
# MAGIC   ('10001', 'Midtown',   false),
# MAGIC   ('11371', 'LaGuardia', true),
# MAGIC   ('11430', 'JFK',       true);
# MAGIC
# MAGIC SELECT * FROM trip_zones;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2.3 Create and Populate a Table with CTAS
# MAGIC
# MAGIC **Goal:** Build a table from a query in one statement.
# MAGIC
# MAGIC CTAS means `CREATE TABLE AS SELECT`. The output columns and types come from the `SELECT`, so `CAST` is how you control a type. A CTAS statement does not declare a separate column-type list.
# MAGIC
# MAGIC **Predict:** Does `short_trips` start empty, or is it populated as part of the create operation?
# MAGIC
# MAGIC **Look for:** A count greater than zero. The table contains only trips shorter than two miles.
# MAGIC
# MAGIC > **Exam anchor:** Eliminate an answer that combines CTAS with a `(column TYPE, ...)` declaration.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE short_trips AS
# MAGIC SELECT pickup_zip, dropoff_zip,
# MAGIC        CAST(trip_distance AS DOUBLE) AS trip_distance,
# MAGIC        fare_amount
# MAGIC FROM samples.nyctaxi.trips
# MAGIC WHERE trip_distance < 2;
# MAGIC
# MAGIC SELECT COUNT(*) AS short_trip_count FROM short_trips;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2.4 Inspect What Databricks Created
# MAGIC
# MAGIC **Goal:** Confirm table properties from metadata rather than guessing from the SQL.
# MAGIC
# MAGIC `DESCRIBE EXTENDED` returns schema information plus detailed metadata.
# MAGIC
# MAGIC **Look for these three fields:**
# MAGIC - `Type: MANAGED`
# MAGIC - `Provider: delta`
# MAGIC - `Location`: a Unity Catalog-managed storage location
# MAGIC
# MAGIC **Why it matters:** Table type determines who manages the files and what happens to them when the table is dropped.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED short_trips;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2.5 Create a New Delta Version
# MAGIC
# MAGIC **Goal:** Make a controlled change so you can inspect Delta history and compare snapshots.
# MAGIC
# MAGIC The update adds `1.00` to fares for one pickup ZIP code. Delta commits the write as a new table version.
# MAGIC
# MAGIC **Predict:** Will readers see a partly updated table while this operation runs?
# MAGIC
# MAGIC **Look for:** A successful update. Delta transactions are atomic, so readers see a complete committed snapshot.

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE short_trips SET fare_amount = fare_amount + 1.00
# MAGIC WHERE pickup_zip = '10282';

# COMMAND ----------

# MAGIC %md
# MAGIC **Goal:** Read the table's audit trail.
# MAGIC
# MAGIC `DESCRIBE HISTORY` lists versions in reverse chronological order. Find the CTAS operation and the later `UPDATE`.
# MAGIC
# MAGIC **Look for:** Different version numbers, timestamps, and operation names. History describes changes; it does not itself change the table.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY short_trips;

# COMMAND ----------

# MAGIC %md
# MAGIC **Goal:** Compare an older snapshot with the current table without changing either one.
# MAGIC
# MAGIC `VERSION AS OF 0` reads version 0. The second subquery reads the current snapshot.
# MAGIC
# MAGIC **Predict:** Which total should be larger after the update?
# MAGIC
# MAGIC **Look for:** `total_now` should be greater than `total_v0`. Time travel reads the past; `RESTORE TABLE` would make an old snapshot current again.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   (SELECT ROUND(SUM(fare_amount), 2) FROM short_trips VERSION AS OF 0) AS total_v0,
# MAGIC   (SELECT ROUND(SUM(fare_amount), 2) FROM short_trips)                 AS total_now;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2.6 Put Source Files in a Governed Volume
# MAGIC
# MAGIC **Goal:** Create governed storage for a non-tabular source file.
# MAGIC
# MAGIC Tables govern rows and columns. Volumes govern files such as CSV, JSON, images, and libraries. The Python cell uses your widget value to build a fully qualified volume name.
# MAGIC
# MAGIC **Look for:** A printed path in the form `/Volumes/workspace/<your_schema>/landing/`.
# MAGIC
# MAGIC After running the cell, upload `week1_retail_sales.csv` in **Catalog Explorer → workspace → your schema → Volumes → landing → Upload**.

# COMMAND ----------

spark.sql(f"CREATE VOLUME IF NOT EXISTS workspace.{USER_SCHEMA}.landing")
print(f"Upload week1_retail_sales.csv to: /Volumes/workspace/{USER_SCHEMA}/landing/")

# COMMAND ----------

# MAGIC %md
# MAGIC **Goal:** Inspect the CSV in place before creating a table.
# MAGIC
# MAGIC `read_files()` reads files from the volume and returns tabular rows. At this point the CSV is still a file; this query does **not** create a table.
# MAGIC
# MAGIC **Look for:** Five BrewMart rows with column names from the CSV header.
# MAGIC
# MAGIC > If the cell reports that the path does not exist, confirm the upload filename and the printed volume path before continuing.

# COMMAND ----------

# Query the raw file IN PLACE — no table yet
display(spark.sql(f"""
  SELECT * FROM read_files(
    '/Volumes/workspace/{USER_SCHEMA}/landing/week1_retail_sales.csv',
    format => 'csv', header => true)
  LIMIT 5
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2.7 Compare Persistent and Temporary Views
# MAGIC
# MAGIC **Goal:** Choose the right kind of view based on who needs it and how long it must exist.
# MAGIC
# MAGIC `airport_short_trips` is a persistent Unity Catalog view. `scratch_fares` is a session-scoped temporary view.
# MAGIC
# MAGIC **Predict:** Which view could another authorized user query after your notebook session ends?
# MAGIC
# MAGIC **Look for:** Both names in `SHOW VIEWS`; the temporary view is marked as temporary. Its definition disappears with the session.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW airport_short_trips AS
# MAGIC SELECT s.*, z.zone_label
# MAGIC FROM short_trips s JOIN trip_zones z ON s.dropoff_zip = z.zip
# MAGIC WHERE z.is_airport;
# MAGIC
# MAGIC CREATE OR REPLACE TEMP VIEW scratch_fares AS
# MAGIC SELECT pickup_zip, AVG(fare_amount) AS avg_fare FROM short_trips GROUP BY pickup_zip;
# MAGIC
# MAGIC SHOW VIEWS;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 3 — LAB: Your First Governed Mini-Lakehouse (BrewMart)
# MAGIC Sales CSVs arrive by email today. Your job is to make them queryable, governed, and auditable, then prove that a bad update is recoverable.
# MAGIC
# MAGIC You already completed Tasks 1-3 above: create your schema, create the `landing` volume, and upload and inspect the file.
# MAGIC
# MAGIC **Lab workflow:** Start Task 4 with the instructor. Continue Tasks 5-7 independently. Use the validation cell to decide whether you are finished.

# COMMAND ----------

# MAGIC %md
# MAGIC ### TODO Task 4 — Build `sales_raw` with CTAS
# MAGIC
# MAGIC **Goal:** Convert the landing CSV into a managed Delta table with useful data types.
# MAGIC
# MAGIC **Before you code:** The source path is `/Volumes/workspace/{USER_SCHEMA}/landing/week1_retail_sales.csv`. `read_files()` initially reads CSV fields as strings, so the CTAS query must control the output schema.
# MAGIC
# MAGIC **Your task:**
# MAGIC 1. Use `CREATE OR REPLACE TABLE sales_raw AS SELECT`.
# MAGIC 2. Read the CSV with `read_files(..., format => 'csv', header => true)`.
# MAGIC 3. Cast `order_date` to `DATE`, `quantity` to `INT`, and `unit_price` to `DOUBLE`.
# MAGIC 4. Add `line_total` as the cast quantity multiplied by the cast unit price.
# MAGIC 5. Display five rows from the new table.
# MAGIC
# MAGIC **Expected result:** `sales_raw` exists and includes typed columns plus `line_total`. One source row has a missing unit price, so its `line_total` is `NULL`.
# MAGIC
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC Build the `SELECT` first. Put each `CAST` inside the query and give it the desired column alias. Use the Python `USER_SCHEMA` variable to construct the volume path.
# MAGIC </details>

# COMMAND ----------

# TODO: build sales_raw with a CTAS from read_files(...)
# spark.sql(f""" CREATE OR REPLACE TABLE sales_raw AS SELECT ... """)

# COMMAND ----------

# MAGIC %md
# MAGIC ### TODO Task 5 — Confirm the Table Type and Format
# MAGIC
# MAGIC **Goal:** Use metadata to prove that `sales_raw` is a managed Delta table.
# MAGIC
# MAGIC **Your task:** Run the metadata command used in Part 2 and find the `Type` and `Provider` fields.
# MAGIC
# MAGIC **Expected result:** `Type` is `MANAGED` and `Provider` is `delta`.
# MAGIC
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC The command starts with `DESCRIBE` and includes more detail than a basic schema description.
# MAGIC </details>

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: which command shows Type and Provider?

# COMMAND ----------

# MAGIC %md
# MAGIC ### TODO Task 6 — Create a Persistent View and a Temp View
# MAGIC
# MAGIC **Goal:** Publish reusable store metrics and keep a separate exploratory query session-scoped.
# MAGIC
# MAGIC **Your task:**
# MAGIC 1. Create or replace the persistent view `sales_by_store`.
# MAGIC 2. Group by `store`, calculate rounded total revenue from `line_total`, and count distinct orders.
# MAGIC 3. Create or replace a temporary view named `my_scratch` for an exploratory category or product summary.
# MAGIC 4. Query `sales_by_store` and inspect the available views.
# MAGIC
# MAGIC **Expected result:** `sales_by_store` returns Atlanta, Chicago, Dallas, and one `NULL`-store group. `my_scratch` exists only in this notebook session.
# MAGIC
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC Use `SUM(line_total)`, `COUNT(DISTINCT order_id)`, and `GROUP BY store`. A temporary view adds the keyword `TEMP` before `VIEW`.
# MAGIC </details>

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: CREATE OR REPLACE VIEW sales_by_store AS ...
# MAGIC -- TODO: CREATE OR REPLACE TEMP VIEW my_scratch AS ...

# COMMAND ----------

# MAGIC %md
# MAGIC ### TODO Task 7 — Break It, Prove the Past, and Restore
# MAGIC
# MAGIC **Goal:** Demonstrate the difference between reading an old snapshot and restoring it as the current state.
# MAGIC
# MAGIC **Your task:**
# MAGIC 1. Simulate a bad update by setting both `unit_price` and `line_total` to `0` for every row.
# MAGIC 2. Inspect table history and identify the new `UPDATE` version.
# MAGIC 3. Compare the current `line_total` sum with `VERSION AS OF 0`. This query proves the old snapshot still exists but does not repair current data.
# MAGIC 4. Restore `sales_raw` to version 0.
# MAGIC 5. Inspect history again; the restore should appear as another operation.
# MAGIC
# MAGIC **Expected result:** Before restore, the current total is zero while the version 0 total is not. After restore, the totals match again.
# MAGIC
# MAGIC <details>
# MAGIC <summary>Hint</summary>
# MAGIC
# MAGIC Use `UPDATE`, `DESCRIBE HISTORY`, `VERSION AS OF 0`, and `RESTORE TABLE ... TO VERSION AS OF 0` in that order.
# MAGIC </details>

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TODO: your recovery drill here

# COMMAND ----------

# MAGIC %md
# MAGIC ### Validation — Check Your Finished Lakehouse
# MAGIC
# MAGIC You are finished when all four statements are true:
# MAGIC
# MAGIC 1. `sales_raw` is a managed Delta table and contains `line_total`.
# MAGIC 2. `sales_by_store` returns three named stores plus one `NULL`-store group.
# MAGIC 3. History includes the create/replace operation, the deliberate `UPDATE`, and `RESTORE`.
# MAGIC 4. The version 0 and current `line_total` totals match after restore.
# MAGIC
# MAGIC Run the total comparison below. Also rerun your metadata, view, and history queries if you have not confirmed the first three checks.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 1) sales_raw exists with line_total; 2) view returns 3 stores + 1 NULL-store row;
# MAGIC -- 3) history shows CTAS → UPDATE → RESTORE; 4) v0 total == current total
# MAGIC SELECT
# MAGIC   (SELECT ROUND(SUM(line_total),2) FROM sales_raw VERSION AS OF 0) AS v0,
# MAGIC   (SELECT ROUND(SUM(line_total),2) FROM sales_raw)                 AS now;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Stretch — Investigate Data Quality
# MAGIC
# MAGIC The file contains two duplicate rows and two missing values. Build `sales_clean` using `DISTINCT` or `ROW_NUMBER`, then count how many rows were removed.
# MAGIC
# MAGIC Find the order with a `NULL` `line_total`. Explain why: arithmetic with a `NULL` operand returns `NULL`. This is a preview of the data-quality decisions you will make in Week 2.

# COMMAND ----------

# MAGIC %md ---
# MAGIC ## Solution
# MAGIC The solution file will be shared by your instructor.
# MAGIC
# MAGIC Keep your completed schema, volume, tables, and views. Week 2 builds on them.
