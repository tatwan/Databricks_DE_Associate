# Databricks notebook source
# MAGIC %md
# MAGIC # Appendix — PySpark 101 for SQL People
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC **Who this is for:** you are fluent in SQL, and PySpark cells feel like a foreign language. This appendix is a *translation guide*, not a Python course. Every PySpark idea is shown next to the SQL you already know.
# MAGIC
# MAGIC **Standalone by design** — it creates its own tiny dataset, touches none of your lab schemas, and can be run any time: before Week 2, before Week 3, or the night before the exam.
# MAGIC
# MAGIC | Section | You will learn |
# MAGIC |---|---|
# MAGIC | 1 | What `spark` is, and why a DataFrame is just a table |
# MAGIC | 2 | The Rosetta Stone: every SQL clause → its DataFrame method |
# MAGIC | 3 | Crossing the bridge: SQL → PySpark (`spark.sql`) |
# MAGIC | 4 | Crossing back: PySpark → SQL (temp views) |
# MAGIC | 5 | Widgets — parameters for notebooks (and jobs) |
# MAGIC | 6 | The `dbutils` map |
# MAGIC | 7 | Lazy evaluation, actions, and why `collect()` is dangerous |
# MAGIC | 8 | Cheat sheet |

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 — `spark`, and why a DataFrame is just a table
# MAGIC
# MAGIC Every Databricks notebook comes with a ready-made variable called **`spark`** (the SparkSession). Your `%sql` cells secretly use the *same engine* — a `%sql` cell and `spark.sql("...")` do identical work.
# MAGIC
# MAGIC A **DataFrame** is Spark's name for *a table held in a Python variable*: rows, named columns, types. If you can picture a query result, you can picture a DataFrame.
# MAGIC
# MAGIC **Look for:** `display(df)` shows a DataFrame exactly like a SQL result grid.

# COMMAND ----------

# Build a small orders table in Python — no files, no schemas touched.
orders_data = [
    (1, "Kitchen",    "north", 120.50, "2026-01-05"),
    (2, "Appliances", "south",  89.99, "2026-01-06"),
    (3, "Kitchen",    "north",  35.00, "2026-01-06"),
    (4, "Garden",     "west",  240.00, "2026-01-07"),
    (5, "Kitchen",    "south",  15.75, "2026-01-08"),
    (6, "Appliances", "north", 310.20, "2026-01-08"),
]
orders = spark.createDataFrame(
    orders_data,
    "order_id INT, category STRING, region STRING, amount DOUBLE, order_date STRING",
)
display(orders)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 — The Rosetta Stone: SQL clause → DataFrame method
# MAGIC
# MAGIC Each pair below does the same thing. Read the SQL first (you know it), then find each piece in the PySpark line.
# MAGIC
# MAGIC One import unlocks the function library — `F.col`, `F.sum`, `F.when` are the PySpark spellings of column references, aggregates, and CASE WHEN:

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

# MAGIC %md ### SELECT ... WHERE
# MAGIC ```sql
# MAGIC SELECT order_id, amount FROM orders WHERE region = 'north'
# MAGIC ```

# COMMAND ----------

display(
    orders.select("order_id", "amount")
          .filter(F.col("region") == "north")     # .where(...) is an exact synonym
)

# COMMAND ----------

# MAGIC %md ### ORDER BY
# MAGIC ```sql
# MAGIC SELECT * FROM orders ORDER BY amount DESC
# MAGIC ```

# COMMAND ----------

display(orders.orderBy(F.col("amount").desc()))

# COMMAND ----------

# MAGIC %md ### GROUP BY with aggregates
# MAGIC ```sql
# MAGIC SELECT category, COUNT(*) AS n, ROUND(SUM(amount), 2) AS revenue
# MAGIC FROM orders GROUP BY category
# MAGIC ```

# COMMAND ----------

display(
    orders.groupBy("category")
          .agg(F.count("*").alias("n"),
               F.round(F.sum("amount"), 2).alias("revenue"))
)

# COMMAND ----------

# MAGIC %md ### CASE WHEN → `F.when(...).otherwise(...)`
# MAGIC ```sql
# MAGIC SELECT *, CASE WHEN amount >= 100 THEN 'big' ELSE 'small' END AS order_size FROM orders
# MAGIC ```

# COMMAND ----------

display(
    orders.withColumn("order_size",
                      F.when(F.col("amount") >= 100, "big").otherwise("small"))
)

# COMMAND ----------

# MAGIC %md ### CAST → `.cast(...)` — and `withColumn` = "add or replace a column"
# MAGIC ```sql
# MAGIC SELECT *, CAST(order_date AS DATE) AS order_date FROM orders
# MAGIC ```
# MAGIC **Why it matters (exam):** this is the same CAST-in-the-SELECT rule CTAS relies on — types are controlled by casting expressions, in SQL or PySpark alike.

# COMMAND ----------

orders_typed = orders.withColumn("order_date", F.col("order_date").cast("date"))
orders_typed.printSchema()   # order_date is now date, not string

# COMMAND ----------

# MAGIC %md ### JOIN
# MAGIC ```sql
# MAGIC SELECT o.*, r.manager FROM orders o LEFT JOIN regions r ON o.region = r.region
# MAGIC ```
# MAGIC **Why it matters (exam):** the join-type keyword (`"left"`, `"inner"`) carries the same silent-row-loss behavior you learned in Week 2 — `"inner"` drops unmatched rows in PySpark too.

# COMMAND ----------

regions = spark.createDataFrame(
    [("north", "Amina"), ("south", "Piotr")],   # note: no 'west' — watch what LEFT does
    "region STRING, manager STRING",
)
display(orders.join(regions, on="region", how="left"))   # 'west' survives with NULL manager

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 — Crossing the bridge: SQL → PySpark
# MAGIC
# MAGIC `spark.sql("...")` runs any SQL string and hands you the result **as a DataFrame**. This is the single most useful line for a SQL-first engineer: write the logic in SQL, receive it in Python.

# COMMAND ----------

orders.createOrReplaceTempView("orders_v")   # (explained fully in section 4)

df = spark.sql("SELECT category, SUM(amount) AS revenue FROM orders_v GROUP BY category")
display(df)                                   # df is a normal DataFrame — chain more methods if you like

# COMMAND ----------

# MAGIC %md ### Parameterize safely with `args` — not f-strings
# MAGIC `spark.sql` accepts **named parameter markers** (`:name`). This is the safe way to inject values — no string pasting, no injection risk:

# COMMAND ----------

min_amount = 100
df = spark.sql(
    "SELECT * FROM orders_v WHERE amount >= :min_amt",
    args={"min_amt": min_amount},
)
display(df)

# COMMAND ----------

# MAGIC %md ### Pull a single value out of SQL into a Python variable
# MAGIC `.first()[0]` grabs row one, column one — the standard way to get a scalar from SQL into Python:

# COMMAND ----------

total = spark.sql("SELECT SUM(amount) FROM orders_v").first()[0]
print(f"Total revenue as a Python float: {total:.2f}")   # now usable in ifs, prints, api calls...

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4 — Crossing back: PySpark → SQL (temp views)
# MAGIC
# MAGIC `df.createOrReplaceTempView("name")` registers a DataFrame so `%sql` cells can query it. This is how the two languages share data inside one notebook.
# MAGIC
# MAGIC **Why it matters (exam):** a temp view is **session-scoped** — your colleague cannot see it, and it is gone when your session ends. That is the Week 1 quiz question about the "missing" `scratch_results` view.

# COMMAND ----------

big_orders = orders.filter(F.col("amount") >= 100)
big_orders.createOrReplaceTempView("big_orders_v")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Plain SQL against a DataFrame you built in Python one cell ago:
# MAGIC SELECT region, COUNT(*) AS big_order_count
# MAGIC FROM big_orders_v
# MAGIC GROUP BY region

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5 — Widgets: parameters for notebooks (and jobs)
# MAGIC
# MAGIC A **widget** is a named input box at the top of the notebook. Two audiences set them:
# MAGIC 1. **Humans** — type into the box while developing.
# MAGIC 2. **Jobs** — a job parameter named `region` lands in the widget named `region`. `dbutils.widgets.get` cannot tell the difference. **That is the parameters→widgets contract** (Week 3 quiz Q7).

# COMMAND ----------

dbutils.widgets.text("region", "north", "Region to analyze")
dbutils.widgets.dropdown("order_size", "all", ["all", "big", "small"], "Order size")

REGION = dbutils.widgets.get("region")
SIZE   = dbutils.widgets.get("order_size")
print(f"region={REGION!r}  order_size={SIZE!r}")

# COMMAND ----------

# Use the widget value in Python...
display(orders.filter(F.col("region") == REGION))

# ...or pass it into SQL the safe way:
display(spark.sql("SELECT COUNT(*) AS n FROM orders_v WHERE region = :r", args={"r": REGION}))

# COMMAND ----------

# MAGIC %md
# MAGIC In pure `%sql` cells you can reference widgets directly with the `:param` marker syntax:
# MAGIC ```sql
# MAGIC SELECT * FROM orders_v WHERE region = :region
# MAGIC ```
# MAGIC (You may still see the legacy `${region}` syntax in older notebooks — prefer `:region`.)
# MAGIC
# MAGIC Cleanup when experimenting: `dbutils.widgets.remove("region")` or `dbutils.widgets.removeAll()`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6 — The `dbutils` map
# MAGIC
# MAGIC `dbutils` is the Databricks utility belt. Five families cover the exam and daily work:
# MAGIC
# MAGIC | Family | What it does | One-liner you will actually use |
# MAGIC |---|---|---|
# MAGIC | `dbutils.widgets` | Notebook/job parameters | `dbutils.widgets.get("region")` |
# MAGIC | `dbutils.fs` | Browse storage & volumes | `dbutils.fs.ls("/Volumes/workspace/...")` |
# MAGIC | `dbutils.notebook` | Run/exit whole notebooks | `dbutils.notebook.run("./child", 300, {...})` |
# MAGIC | `dbutils.jobs.taskValues` | Pass values BETWEEN job tasks | `taskValues.set(key="n", value=42)` |
# MAGIC | `dbutils.secrets` | Read credentials safely | `dbutils.secrets.get("scope", "api_key")` |
# MAGIC
# MAGIC `dbutils.notebook` and `taskValues` get a full hands-on treatment in **Week3_Params_Widgets_Demo** — here, just place them on the map.

# COMMAND ----------

# dbutils.fs in action — list a volume or sample dataset (adjust the path to one you have):
try:
    display(dbutils.fs.ls("/databricks-datasets/"))
except Exception as e:
    print("No /databricks-datasets in this workspace — point dbutils.fs.ls at any /Volumes path instead.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7 — Lazy evaluation, actions, and the `collect()` trap
# MAGIC
# MAGIC Transformations (`select`, `filter`, `join`, `groupBy`) **do no work** — they build a plan. Work happens only when an **action** demands results:
# MAGIC
# MAGIC | Action | Returns | Safe on big data? |
# MAGIC | --- | --- | --- |
# MAGIC | `display(df)` / `df.show()` | first rows, for your eyes | ✅ yes |
# MAGIC | `df.count()` | one number | ✅ yes |
# MAGIC | `df.first()` / `df.take(n)` | a few rows | ✅ yes |
# MAGIC | `df.collect()` | **every row, into the driver's memory** | ⚠️ **NO** |
# MAGIC
# MAGIC **Why it matters (exam):** `collect()` on a 300-million-row DataFrame kills the session while executors look healthy — that is a **driver OOM** (Week 4 quiz Q8). If you only need to *see* data, `display` it. If you need a value, aggregate first, *then* collect the one-row result.

# COMMAND ----------

plan = orders.filter(F.col("amount") > 50).groupBy("region").count()   # nothing has run yet
print("Plan built, no work done.")
print(plan.collect())   # fine HERE — the aggregated result is 3 rows, not 300 million

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8 — Cheat sheet: keep this open during labs
# MAGIC
# MAGIC | You want to... | SQL | PySpark |
# MAGIC |---|---|---|
# MAGIC | Pick columns | `SELECT a, b` | `.select("a", "b")` |
# MAGIC | Filter rows | `WHERE x > 5` | `.filter(F.col("x") > 5)` |
# MAGIC | New/derived column | `SELECT *, expr AS c` | `.withColumn("c", expr)` |
# MAGIC | Rename | `AS new_name` | `.alias(...)` / `.withColumnRenamed(...)` |
# MAGIC | Change type | `CAST(x AS DATE)` | `.cast("date")` |
# MAGIC | If/else | `CASE WHEN` | `F.when(...).otherwise(...)` |
# MAGIC | Aggregate | `GROUP BY` | `.groupBy(...).agg(...)` |
# MAGIC | Sort | `ORDER BY x DESC` | `.orderBy(F.col("x").desc())` |
# MAGIC | Join | `LEFT JOIN ... ON` | `.join(other, on="k", how="left")` |
# MAGIC | Union (by name!) | `UNION ALL` | `.unionByName(other)` |
# MAGIC | Dedupe | `SELECT DISTINCT` | `.dropDuplicates()` |
# MAGIC | Run SQL from Python | — | `spark.sql("...", args={...})` |
# MAGIC | Query a DataFrame from SQL | — | `df.createOrReplaceTempView("v")` |
# MAGIC | Read a table | `FROM cat.sch.t` | `spark.table("cat.sch.t")` |
# MAGIC | Save a table | `CREATE TABLE ... AS` | `df.write.saveAsTable("cat.sch.t")` |
# MAGIC
# MAGIC **Two habits that prevent 90% of beginner PySpark bugs:**
# MAGIC 1. `from pyspark.sql import functions as F` at the top — then always `F.col`, `F.sum`, `F.when`.
# MAGIC 2. When stuck, fall back across the bridge: build the logic as SQL in `spark.sql(...)`, get it working, translate later (or never — `spark.sql` is production-legitimate).
