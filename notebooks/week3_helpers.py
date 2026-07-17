# Databricks notebook source
# MAGIC %md
# MAGIC # Helpers — a notebook designed to be `%run`
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC **Role:** this notebook is *included* by others via `%run ./week3_helpers` — like a SQL `CREATE FUNCTION` script, or a Python `import`. It defines things; it does not *do* things.
# MAGIC
# MAGIC **The key idea:** `%run` executes this notebook **inside the caller's session**. Everything defined here — functions, variables — lands directly in the caller's namespace, as if the caller had typed it.
# MAGIC
# MAGIC **Study check:** notice what this notebook does NOT have — no widgets, no writes, no `dbutils.notebook.exit`. A `%run` target should only define reusable pieces. Side effects belong to the caller.

# COMMAND ----------

from pyspark.sql import functions as F

COURSE_TAG = "creo-dea-week3"   # a shared constant every caller can read after %run


def add_ingest_metadata(df):
    """Stamp a DataFrame with the standard ingestion-audit columns.

    The kind of helper every team writes once and reuses everywhere —
    exactly what the exam means by 'reuse helper functions across notebooks'.
    """
    return (df
            .withColumn("_ingested_at", F.current_timestamp())
            .withColumn("_source_tag", F.lit(COURSE_TAG)))


def standardize_region(df, col_name="region"):
    """Trim + lowercase a region column so joins and filters behave."""
    return df.withColumn(col_name, F.lower(F.trim(F.col(col_name))))


print(f"✅ helpers loaded: add_ingest_metadata, standardize_region, COURSE_TAG={COURSE_TAG!r}")
