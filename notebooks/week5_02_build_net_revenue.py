# Databricks notebook source
# MAGIC %md
# MAGIC # Week 5 Task 2 — Build Silver, Quarantine, and Net Revenue
# MAGIC **Job role:** `build_net_revenue`, depends on `ingest_returns`.
# MAGIC
# MAGIC Complete this notebook only after M3–M4 work in the capstone. Paste the same rerunnable logic into the implementation block. Use fully qualified names so the task does not depend on interactive `USE SCHEMA` state.

# COMMAND ----------

dbutils.widgets.text("target_schema", "lab1_yourname")
target_schema = dbutils.widgets.get("target_schema")
schema_fqn = f"workspace.{target_schema}"

bronze_rows = dbutils.jobs.taskValues.get(
    taskKey="ingest_returns",
    key="bronze_rows",
    default=-1,
    debugValue=13,
)
print(f"Upstream bronze_rows={bronze_rows}")

required_tables = ["sales_silver", "returns_bronze"]
missing = [
    table
    for table in required_tables
    if not spark.catalog.tableExists(f"{schema_fqn}.{table}")
]
if missing:
    raise RuntimeError(f"Missing prerequisites in {schema_fqn}: {', '.join(missing)}")

# COMMAND ----------

# MAGIC %md ## Implementation block
# MAGIC Paste your working M3–M4 code below. It must:
# MAGIC
# MAGIC - rebuild `returns_silver` as 11 typed, deduplicated rows whose orders exist;
# MAGIC - rebuild `returns_quarantine` with orphan order `2001`;
# MAGIC - rebuild `net_revenue_daily` with `CLUSTER BY (store, order_date)`;
# MAGIC - compute returned value using the matching order's `unit_price`.

# COMMAND ----------

# TODO: paste your tested M3 + M4 implementation here.
raise NotImplementedError("Complete Week 5 M3–M4, then paste it into week5_02_build_net_revenue.py")

# COMMAND ----------

# Remove the NotImplementedError above before using this notebook as a job task.
silver_rows = spark.table(f"{schema_fqn}.returns_silver").count()
orphan_orders = {
    row["order_id"]
    for row in spark.table(f"{schema_fqn}.returns_quarantine").select("order_id").distinct().collect()
}
net_gt_gross = spark.sql(f"""
    SELECT COUNT(*) AS n
    FROM {schema_fqn}.net_revenue_daily
    WHERE net_revenue > gross_revenue
""").collect()[0]["n"]

assert silver_rows == 11, f"Expected 11 silver rows, found {silver_rows}"
assert orphan_orders == {"2001"}, f"Expected only orphan 2001, found {orphan_orders}"
assert net_gt_gross == 0, f"Found {net_gt_gross} rows where net exceeds gross"

gold_rows = spark.table(f"{schema_fqn}.net_revenue_daily").count()
dbutils.notebook.exit(f"silver_rows={silver_rows}; gold_rows={gold_rows}")
