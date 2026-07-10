# Databricks notebook source
# MAGIC %md
# MAGIC # Week 5 Task 1 — Ingest Returns
# MAGIC **Job role:** `ingest_returns`, the first task in `brewmart_returns_<yourname>`.
# MAGIC
# MAGIC Complete this notebook only after M2 works in the capstone. Paste the same rerunnable table-creation and `COPY INTO` logic into the implementation block. The job supplies `target_schema`; do not hardcode your schema.

# COMMAND ----------

dbutils.widgets.text("target_schema", "lab1_yourname")
target_schema = dbutils.widgets.get("target_schema")
source_path = f"/Volumes/workspace/{target_schema}/landing/returns_incoming/"
target_table = f"workspace.{target_schema}.returns_bronze"

print(f"Source: {source_path}")
print(f"Target: {target_table}")

# COMMAND ----------

# MAGIC %md ## Implementation block
# MAGIC Paste your working M2 code below. It must:
# MAGIC
# MAGIC - create `returns_bronze` with all source columns as `STRING` plus `_ingested_at TIMESTAMP`;
# MAGIC - use `COPY INTO` from `source_path` with CSV headers;
# MAGIC - be safe to rerun (the second run inserts zero rows).

# COMMAND ----------

# TODO: paste your tested CREATE TABLE + COPY INTO implementation here.
raise NotImplementedError("Complete Week 5 M2, then paste it into week5_01_ingest_returns.py")

# COMMAND ----------

# Remove the NotImplementedError above before using this notebook as a job task.
bronze_rows = spark.table(target_table).count()
assert bronze_rows == 13, f"Expected 13 bronze rows, found {bronze_rows}"
dbutils.jobs.taskValues.set(key="bronze_rows", value=bronze_rows)
dbutils.notebook.exit(f"bronze_rows={bronze_rows}")
