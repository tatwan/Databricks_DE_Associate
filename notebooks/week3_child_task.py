# Databricks notebook source
# MAGIC %md
# MAGIC # Child Task — a notebook designed to be called by `dbutils.notebook.run`
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC **Role:** a parent notebook calls this one with `dbutils.notebook.run("./week3_child_task", 300, {"region": "north", "min_amount": "50"})`.
# MAGIC
# MAGIC **Contrast with `%run` (this is the exam discriminator):**
# MAGIC
# MAGIC | | `%run ./week3_helpers` | `dbutils.notebook.run("./week3_child_task", ...)` |
# MAGIC |---|---|---|
# MAGIC | Session | **Shared** — definitions land in the caller | **Isolated** — child sees nothing of the parent |
# MAGIC | Input | none (it just executes inline) | a `{param: value}` dict → arrives as **widgets** |
# MAGIC | Output | everything it defined | **one string**, via `dbutils.notebook.exit(...)` |
# MAGIC | Feels like | `import` / running a SQL script | calling a stored procedure |
# MAGIC
# MAGIC **Study check as you read:** find the three stages — ① receive parameters (widgets) → ② do the work → ③ `dbutils.notebook.exit` a string. That same shape is how a *job task* consumes job parameters — which is why widgets are the parameters→widgets contract.

# COMMAND ----------

# MAGIC %md ### ① Receive parameters — they arrive as widgets
# MAGIC The parent's `{"region": "north", "min_amount": "50"}` lands in widgets of the **same names**. Note: values always arrive as **strings** — cast what you need to cast.

# COMMAND ----------

dbutils.widgets.text("region", "north")
dbutils.widgets.text("min_amount", "0")

region     = dbutils.widgets.get("region")
min_amount = float(dbutils.widgets.get("min_amount"))   # widgets are strings — cast!
print(f"Child received: region={region!r}, min_amount={min_amount}")

# COMMAND ----------

# MAGIC %md ### ② Do the work
# MAGIC A self-contained mini-dataset keeps this runnable anywhere — the *pattern* is what you are studying, not the data.

# COMMAND ----------

from pyspark.sql import functions as F

sales = spark.createDataFrame(
    [("north", 120.5), ("north", 35.0), ("south", 89.99),
     ("west", 240.0), ("north", 310.2), ("south", 15.75)],
    "region STRING, amount DOUBLE",
)

result = (sales
          .filter((F.col("region") == region) & (F.col("amount") >= min_amount))
          .agg(F.count("*").alias("n"), F.round(F.sum("amount"), 2).alias("revenue"))
          .first())

n, revenue = result["n"], result["revenue"] or 0.0
print(f"Computed: {n} qualifying orders, revenue={revenue}")

# COMMAND ----------

# MAGIC %md ### ③ Return ONE string with `dbutils.notebook.exit`
# MAGIC The parent gets back exactly one string — so the convention is to pack results as JSON. `exit()` also **stops this notebook here**: cells after it never run when called via `dbutils.notebook.run`.

# COMMAND ----------

import json

dbutils.notebook.exit(json.dumps({
    "region": region,
    "qualifying_orders": n,
    "revenue": revenue,
}))

# COMMAND ----------

# MAGIC %md
# MAGIC ⚠️ If you are reading this cell after *running the notebook interactively*, note that `exit()` above ended execution — this cell only renders, it never runs in a `dbutils.notebook.run` call.
