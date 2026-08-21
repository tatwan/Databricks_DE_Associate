# Databricks notebook source
# MAGIC %md
# MAGIC # SOLUTIONS — Week 3 Lab: Parameters, Widgets, `%run`, and Notebook Orchestration
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy · Instructor/self-check copy**
# MAGIC
# MAGIC Complete solutions for `Week3_Params_Widgets_Lab`, with the reasoning a grader would give. Every check cell from the lab passes as-is.
# MAGIC
# MAGIC **Requires:** `week3_helpers` and `week3_child_task` in the same folder.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercise 1 — Widgets
# MAGIC **The one trap:** widgets ALWAYS return strings — `SAMPLE_ROWS` needs an explicit `int(...)` cast. Forgetting the cast is also a classic production bug ("`'5' * 2` is `'55'`").

# COMMAND ----------

dbutils.widgets.text("target_schema", "lab1_yourname")
dbutils.widgets.dropdown("sample_rows", "5", ["5", "10", "20"])

TARGET_SCHEMA = dbutils.widgets.get("target_schema")
SAMPLE_ROWS   = int(dbutils.widgets.get("sample_rows"))     # ← the cast

# COMMAND ----------

# ✅ CHECK — Exercise 1
assert isinstance(TARGET_SCHEMA, str) and len(TARGET_SCHEMA) > 0
assert isinstance(SAMPLE_ROWS, int)
assert SAMPLE_ROWS in (5, 10, 20)
print(f"✅ Exercise 1 passed: schema={TARGET_SCHEMA!r}, rows={SAMPLE_ROWS}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercise 2 — `%run`
# MAGIC **The two rules:** `%run` alone in its cell; path relative to this notebook. Since this solutions notebook lives in `solutions/`, the helpers are one folder up — note the `../notebooks/` path (in the lab itself, which sits next to the helpers, it is just `./week3_helpers`).

# COMMAND ----------

# MAGIC %run ../notebooks/week3_helpers

# COMMAND ----------

from pyspark.sql import functions as F

raw = spark.createDataFrame(
    [("  WEST  ", 240.0), ("north", 120.5), (" South", 89.99)],
    "region STRING, amount DOUBLE",
)

lab_df = add_ingest_metadata(standardize_region(raw))   # clean first, stamp second
display(lab_df)

# COMMAND ----------

# ✅ CHECK — Exercise 2
cols = set(lab_df.columns)
assert "_ingested_at" in cols and "_source_tag" in cols
regions = {r["region"] for r in lab_df.select("region").collect()}
assert regions == {"west", "north", "south"}, f"got {regions}"
print(f"✅ Exercise 2 passed — helpers shared into this session via %run (tag={COURSE_TAG!r})")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercise 3 — `dbutils.notebook.run`
# MAGIC **Grader's notes:** arguments must all be **strings** (`"10"`, not `10`); the child returns ONE string, so `json.loads` unpacks it; a real timeout (not 0) is production hygiene.

# COMMAND ----------

import json

raw_return = dbutils.notebook.run(
    "../notebooks/week3_child_task",     # from the lab's own folder: "./week3_child_task"
    timeout_seconds=300,
    arguments={"region": "south", "min_amount": "10"},
)
child_result = json.loads(raw_return)
print(child_result)

# COMMAND ----------

# ✅ CHECK — Exercise 3
assert isinstance(child_result, dict)
assert child_result["region"] == "south"
assert child_result["qualifying_orders"] == 2, f"got {child_result['qualifying_orders']}"
print(f"✅ Exercise 3 passed: child returned {child_result}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercise 4 — `taskValues`
# MAGIC **Why -1 comes back:** interactively there is **no job context**, so `get` returns the `debugValue`. Inside a real job run, `debugValue` is ignored and the upstream task's actual value arrives. That asymmetry IS the lesson.

# COMMAND ----------

upstream_rows = dbutils.jobs.taskValues.get(
    taskKey="ingest_bronze",
    key="bronze_rows",
    debugValue=-1,
)
print(f"Upstream reported bronze_rows={upstream_rows}")

# COMMAND ----------

# ✅ CHECK — Exercise 4
assert upstream_rows == -1
print("✅ Exercise 4 passed — and you know WHY it's -1 here: no job context, so debugValue is returned")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercise 5 — Which mechanism?
# MAGIC
# MAGIC | # | Scenario | Answer | One-line why |
# MAGIC |---|---|---|---|
# MAGIC | 1 | Job passes `env=prod` to its notebook task | **widgets** | The parameters→widgets contract |
# MAGIC | 2 | Six notebooks share `parse_timestamp()` interactively | **`%run`** | Shared session = shared definitions |
# MAGIC | 3 | Task A's max order id → Task B's scan start | **taskValues** | Small runtime value BETWEEN tasks |
# MAGIC | 4 | Invoke validation notebook with inputs, branch on its answer | **`dbutils.notebook.run`** | Isolated call with parameters + one returned string |
# MAGIC | 5 | Three notebooks nightly, in order, retries, alerts | **job with tasks** | Orchestration belongs to the scheduler, not `%run` chains |

# COMMAND ----------

answers = {
    1: "widgets",
    2: "%run",
    3: "taskValues",
    4: "dbutils.notebook.run",
    5: "job with tasks",
}

# COMMAND ----------

# ✅ CHECK — Exercise 5
expected = {1: "widgets", 2: "%run", 3: "taskvalues", 4: "dbutils.notebook.run", 5: "job with tasks"}
normalized = {k: str(v).lower().replace(" ", "").replace("_", "").replace(".", "").replace("()", "") for k, v in answers.items()}
key_normalized = {k: v.replace(" ", "").replace(".", "") for k, v in expected.items()}
wrong = [k for k in expected if key_normalized[k] not in normalized.get(k, "")]
assert not wrong, f"Rethink scenarios {wrong}"
print("✅ Exercise 5 passed — you can route any exam scenario to its mechanism. Lab complete! 🎉")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Stretch answer
# MAGIC Exercise 4 still returns `-1` inside the job because **nobody ever `set()` a task value under task key `ingest_bronze` / key `bronze_rows`** — the child notebook exits with JSON but sets no task values. Two valid fixes:
# MAGIC 1. Add `dbutils.jobs.taskValues.set(key="bronze_rows", value=n)` to `week3_child_task` **and** name that task `ingest_bronze` in the job, or
# MAGIC 2. Point the `get` at a task key/key pair that actually sets a value (as `week3_01_ingest_bronze` does in the main Week 3 job lab).
# MAGIC
# MAGIC Either way, the principle is the same: **taskValues are addressed by (taskKey, key) — both sides must agree.**
