# Databricks notebook source
# MAGIC %md
# MAGIC # Week 3 LAB — Parameters, Widgets, `%run`, and Notebook Orchestration
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC You just watched the demo (`Week3_Params_Widgets_Demo`). Now it is your turn — five exercises, each one mechanism. Replace every `# TODO` and run the cell; each exercise has a ✅ check cell that tells you if you got it right.
# MAGIC
# MAGIC **Rules of the road:**
# MAGIC - Work top to bottom — later exercises reuse earlier results.
# MAGIC - Stuck > 5 minutes? Peek at ONE line of `solutions/Week3_Params_Widgets_Lab_Solutions`, then come back.
# MAGIC - Keep `week3_helpers` and `week3_child_task` in the same folder as this notebook.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercise 1 — Widgets (config INTO the notebook)
# MAGIC
# MAGIC Create two widgets and read them into correctly-typed Python variables:
# MAGIC 1. A **text** widget `target_schema`, default `"lab1_yourname"`.
# MAGIC 2. A **dropdown** widget `sample_rows` with default `"5"` and choices `"5"`, `"10"`, `"20"`.
# MAGIC 3. Read them into `TARGET_SCHEMA` (string) and `SAMPLE_ROWS` (**int** — remember what widgets always return!).

# COMMAND ----------

# TODO: create the two widgets

# TODO: read them — TARGET_SCHEMA as str, SAMPLE_ROWS as int
TARGET_SCHEMA = None
SAMPLE_ROWS   = None

# COMMAND ----------

# ✅ CHECK — Exercise 1
assert isinstance(TARGET_SCHEMA, str) and len(TARGET_SCHEMA) > 0, "TARGET_SCHEMA should be a non-empty string"
assert isinstance(SAMPLE_ROWS, int), "SAMPLE_ROWS must be an int — widgets return strings, cast it!"
assert SAMPLE_ROWS in (5, 10, 20), "SAMPLE_ROWS should come from the dropdown choices"
print(f"✅ Exercise 1 passed: schema={TARGET_SCHEMA!r}, rows={SAMPLE_ROWS}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercise 2 — `%run` (share helpers in this session)
# MAGIC
# MAGIC 1. In the next cell, `%run` the helpers notebook (remember the two rules: alone in the cell, relative path).
# MAGIC 2. Then build the DataFrame below and use **both** helper functions on it: standardize the region, then stamp the ingest metadata.

# COMMAND ----------

# TODO: %run the helpers notebook (this cell must contain ONLY the %run line)

# COMMAND ----------

from pyspark.sql import functions as F

raw = spark.createDataFrame(
    [("  WEST  ", 240.0), ("north", 120.5), (" South", 89.99)],
    "region STRING, amount DOUBLE",
)

# TODO: apply standardize_region, then add_ingest_metadata; save as `lab_df`
lab_df = None

display(lab_df)

# COMMAND ----------

# ✅ CHECK — Exercise 2
cols = set(lab_df.columns)
assert "_ingested_at" in cols and "_source_tag" in cols, "Did you apply add_ingest_metadata?"
regions = {r["region"] for r in lab_df.select("region").collect()}
assert regions == {"west", "north", "south"}, f"Regions should be trimmed + lowercased, got {regions}"
print(f"✅ Exercise 2 passed — helpers shared into this session via %run (tag={COURSE_TAG!r})")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercise 3 — `dbutils.notebook.run` (call a notebook like a function)
# MAGIC
# MAGIC Call `week3_child_task` for the **south** region with `min_amount` **10**, timeout 300 seconds. Parse its JSON return into a dict called `child_result`.
# MAGIC
# MAGIC *Remember: every value in the arguments dict must be a string.*

# COMMAND ----------

import json

# TODO: call the child notebook and parse its return
raw_return   = None
child_result = None

print(child_result)

# COMMAND ----------

# ✅ CHECK — Exercise 3
assert isinstance(child_result, dict), "Parse the returned JSON string with json.loads"
assert child_result["region"] == "south", "Call it for the SOUTH region"
assert child_result["qualifying_orders"] == 2, f"Expected 2 south orders ≥ $10, got {child_result['qualifying_orders']}"
print(f"✅ Exercise 3 passed: child returned {child_result}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercise 4 — `taskValues` (runtime data BETWEEN job tasks)
# MAGIC
# MAGIC Pretend this notebook is a **downstream task** in a job where an upstream task with task key `ingest_bronze` set a value under the key `bronze_rows`.
# MAGIC
# MAGIC Read that value into `upstream_rows`, providing a `debugValue` of `-1` so the cell also works here, interactively.

# COMMAND ----------

# TODO: read the task value (taskKey="ingest_bronze", key="bronze_rows", debugValue=-1)
upstream_rows = None

print(f"Upstream reported bronze_rows={upstream_rows}")

# COMMAND ----------

# ✅ CHECK — Exercise 4
assert upstream_rows == -1, "Interactively you should receive the debugValue (-1) — in a real job you'd get the upstream value"
print("✅ Exercise 4 passed — and you know WHY it's -1 here: no job context, so debugValue is returned")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercise 5 — Which mechanism? (no code — commit before you check)
# MAGIC
# MAGIC For each scenario, write your answer in the cell below, THEN run the check cell:
# MAGIC
# MAGIC 1. A job must pass `env=prod` into its notebook task.
# MAGIC 2. Six notebooks need the same `parse_timestamp()` function during interactive development.
# MAGIC 3. Task A computes yesterday's max order id; Task B must start its scan there.
# MAGIC 4. A notebook must invoke a validation notebook with 3 inputs and branch on its pass/fail answer.
# MAGIC 5. Three notebooks must run in order, nightly, with retries and email alerts.

# COMMAND ----------

answers = {
    1: "?",   # e.g. "widgets", "%run", "taskValues", "dbutils.notebook.run", "job with tasks"
    2: "?",
    3: "?",
    4: "?",
    5: "?",
}

# COMMAND ----------

# ✅ CHECK — Exercise 5
expected = {1: "widgets", 2: "%run", 3: "taskvalues", 4: "dbutils.notebook.run", 5: "job with tasks"}
normalized = {k: str(v).lower().replace(" ", "").replace("_", "").replace(".", "").replace("()", "") for k, v in answers.items()}
key_normalized = {k: v.replace(" ", "").replace(".", "") for k, v in expected.items()}
wrong = [k for k in expected if key_normalized[k] not in normalized.get(k, "")]
assert not wrong, f"Rethink scenarios {wrong} — reread §6 of the demo notebook"
print("✅ Exercise 5 passed — you can route any exam scenario to its mechanism. Lab complete! 🎉")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Stretch (optional, Jobs UI — 10 min)
# MAGIC Wire this into a real job and watch the mechanisms switch from debug to live:
# MAGIC 1. Create a job with **two tasks**: Task 1 = `week3_child_task` (task key `ingest_bronze`), Task 2 = this lab notebook, `depends_on` Task 1.
# MAGIC 2. Add job parameter `target_schema` = anything — watch Exercise 1 receive it as the widget value.
# MAGIC 3. Run it. Exercise 4 still returns -1 — *why?* (Hint: which task key did we ask for, and did the child ever `taskValues.set` under `bronze_rows`? Fix either side and re-run.)
