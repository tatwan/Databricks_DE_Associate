# Databricks notebook source
# MAGIC %md
# MAGIC # Week 3 (bonus) — Lakeflow Declarative Pipeline: the SAME bronze→silver, declared
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC **Do not run this notebook interactively.** It is the **source for a pipeline**. `pyspark.pipelines` and the `@dp` decorators execute inside a Lakeflow Spark Declarative Pipeline (formerly Delta Live Tables / DLT). You attach this notebook to a pipeline in the **Jobs & Pipelines UI** — see section 6 of the companion notebook.
# MAGIC
# MAGIC **Why this matters:** this is optional platform enrichment, not a named objective in the May 4, 2026 exam outline. It connects the pipeline task type to the current declarative API and shows **expectations** (`@dp.expect...`) versus Week 2's table **constraints**.
# MAGIC
# MAGIC | | Delta table CONSTRAINT (Week 2) | Pipeline EXPECTATION (here) |
# MAGIC |---|---|---|
# MAGIC | Where | `ALTER TABLE ... ADD CONSTRAINT` | `@dp.expect...` decorator |
# MAGIC | Bad row | **fails the whole write** | policy: **warn** / **drop** / **fail** |
# MAGIC | Metrics | none | per-expectation pass/fail counts in the pipeline UI |

# COMMAND ----------

from pyspark import pipelines as dp
from pyspark.sql.functions import current_timestamp

# The pipeline supplies the schema via a pipeline CONFIGURATION value (the declarative
# cousin of a job parameter). Set `target_schema` in the pipeline settings (section 6).
target_schema = spark.conf.get("target_schema")

# COMMAND ----------

# MAGIC %md ## Bronze — streaming table, absorb everything as strings
# MAGIC `@dp.table` declares a streaming table when the function returns a streaming DataFrame. `cloudFiles` supplies Auto Loader; the pipeline owns checkpointing.

# COMMAND ----------

@dp.table(
    name="sales_bronze_dlt",
    comment="Bronze: raw sales, all strings + ingest audit column (declarative)."
)
def sales_bronze_dlt():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .load(f"/Volumes/workspace/{target_schema}/landing/sales_incoming/")
        .withColumn("_ingested_at", current_timestamp())
    )

# COMMAND ----------

# MAGIC %md ## Silver — typed + quality expectations
# MAGIC Two expectations, two policies — the exam's favorite contrast:
# MAGIC - `@dp.expect_or_drop` → **drops** rows failing the rule (bad `order_id` never reaches silver).
# MAGIC - `@dp.expect` → **warns**: the row is **kept**, but the failure is counted in the pipeline UI.
# MAGIC - (`@dp.expect_or_fail` — not used here — would **fail the flow update**.)
# MAGIC
# MAGIC `spark.readStream.table("sales_bronze_dlt")` references the upstream table **by name** — the engine infers bronze→silver order from that reference. You never write `depends_on` inside the pipeline.

# COMMAND ----------

@dp.table(
    name="sales_silver_dlt",
    comment="Silver: typed, deduplicated, quality-checked (declarative)."
)
@dp.expect_or_drop("valid_order_id", "order_id IS NOT NULL")
@dp.expect("positive_quantity", "CAST(quantity AS INT) > 0")
def sales_silver_dlt():
    return (
        spark.readStream.table("sales_bronze_dlt")
        .selectExpr(
            "order_id",
            "CAST(order_date AS DATE)   AS order_date",
            "customer_id",
            "store",
            "product",
            "category",
            "CAST(quantity AS INT)      AS quantity",
            "CAST(unit_price AS DOUBLE) AS unit_price",
            "ROUND(CAST(quantity AS INT) * CAST(unit_price AS DOUBLE), 2) AS line_total",
        )
        .dropDuplicates(["order_id", "order_date", "customer_id"])
    )
