# Databricks notebook source
# MAGIC %md
# MAGIC # Week 3 — Parameters, Widgets, `%run`, and Notebook Orchestration (Demo + Study Guide)
# MAGIC **Databricks Certified Data Engineer Associate · Creo Academy**
# MAGIC
# MAGIC The Week 3 slides *name* five mechanisms for moving values around; this notebook is where you actually **run** all five. Use it live in class or as a self-study guide before the exam — every section is written to be read on its own.
# MAGIC
# MAGIC | § | Mechanism | Question it answers |
# MAGIC |---|---|---|
# MAGIC | 1 | **Widgets** | How does config get INTO a notebook? |
# MAGIC | 2 | **Job parameters → widgets** | How does a *job* pass config to a notebook task? |
# MAGIC | 3 | **`%run`** | How do notebooks SHARE functions in one session? |
# MAGIC | 4 | **`dbutils.notebook.run`** | How does a notebook CALL another like a function? |
# MAGIC | 5 | **`taskValues`** | How does runtime data flow BETWEEN job tasks? |
# MAGIC | 6 | Decision table + exam answer shapes | Which one when? |
# MAGIC
# MAGIC **Prerequisites:** none — every section builds its own data. Import `week3_helpers` and `week3_child_task` into the **same folder** as this notebook (`%run` and `notebook.run` use relative paths).

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 — Widgets: config INTO a notebook
# MAGIC
# MAGIC A widget is a named input at the top of the notebook. Create it once, read it anywhere. Four types exist (`text`, `dropdown`, `combobox`, `multiselect`) — `text` and `dropdown` cover nearly everything.
# MAGIC
# MAGIC **Look for:** after running this cell, the input boxes appear at the top of the notebook. Change one and re-run the *read* cell — the code picks up your change without editing a single line. That is the whole point: **code stays fixed, config moves.**

# COMMAND ----------

dbutils.widgets.text("env", "dev", "Environment")
dbutils.widgets.dropdown("write_mode", "append", ["append", "overwrite"], "Write mode")

# COMMAND ----------

env        = dbutils.widgets.get("env")
write_mode = dbutils.widgets.get("write_mode")
print(f"env={env!r}  write_mode={write_mode!r}")

# ⚠️ Widgets ALWAYS return strings. "true" is a non-empty string == truthy. Cast explicitly:
dbutils.widgets.text("batch_size", "500")
batch_size = int(dbutils.widgets.get("batch_size"))     # ← the cast is not optional
print(f"batch_size={batch_size} (type {type(batch_size).__name__})")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 — Job parameters → widgets: THE contract
# MAGIC
# MAGIC When this notebook runs as a **job task**, a job parameter named `env` lands in the widget named `env`. Same `dbutils.widgets.get("env")`, no code change — the notebook cannot tell whether a human or the scheduler set the value.
# MAGIC
# MAGIC **Try it (5 minutes, Jobs UI):**
# MAGIC 1. Jobs & Pipelines → Create job → single notebook task pointing at THIS notebook.
# MAGIC 2. Add job parameter `env` = `prod`.
# MAGIC 3. Run it, open the task output: this cell prints `env='prod'` — the job's value, not the widget default.
# MAGIC
# MAGIC **Why it matters (exam):** *"A job defines parameter env=prod. How does a notebook task receive it?"* → **as a widget, read with `dbutils.widgets.get("env")`** — not a global variable, not `spark.conf`, not reading `databricks.yml`.

# COMMAND ----------

print(f"Right now env={dbutils.widgets.get('env')!r} — interactively that's the widget; in a job it's the job parameter.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 — `%run`: share definitions in ONE session
# MAGIC
# MAGIC `%run ./week3_helpers` executes the helpers notebook **inside this session** — its functions and variables land here as if you had typed them. Think `import`, or running a `CREATE FUNCTION` script.
# MAGIC
# MAGIC Two rules the exam checks:
# MAGIC - `%run` must be **alone in its cell** (nothing else, not even a comment on the same line).
# MAGIC - The path is **relative to this notebook**.

# COMMAND ----------

# MAGIC %run ./week3_helpers

# COMMAND ----------

# Proof of the shared session: use a function and a constant DEFINED IN THE OTHER NOTEBOOK.
from pyspark.sql import functions as F

demo = spark.createDataFrame([("  North ", 12.5), ("SOUTH", 7.0)], "region STRING, amount DOUBLE")

cleaned = standardize_region(demo)          # defined in week3_helpers
stamped = add_ingest_metadata(cleaned)      # defined in week3_helpers
print(f"COURSE_TAG (a variable from the helpers notebook): {COURSE_TAG!r}")
display(stamped)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4 — `dbutils.notebook.run`: call a notebook like a function
# MAGIC
# MAGIC Where `%run` *includes*, `dbutils.notebook.run` **calls**: the child runs in an **isolated session**, receives a dict of parameters (arriving as its widgets), and returns **one string** via `dbutils.notebook.exit`.
# MAGIC
# MAGIC **Look for in the output:** the returned string is JSON we chose to pack — parse it and the parent can act on the child's result. Also click the *Notebook job* link Databricks prints — the child ran as its own ephemeral run.

# COMMAND ----------

import json

raw = dbutils.notebook.run(
    "./week3_child_task",          # relative path, like %run
    timeout_seconds=300,           # 0 = no timeout; always set one in production
    arguments={"region": "north", "min_amount": "50"},   # values must be strings
)

result = json.loads(raw)
print(f"Child returned: {result}")
print(f"→ north revenue over $50: ${result['revenue']}")

# COMMAND ----------

# Isolation, proven: COURSE_TAG exists HERE (via %run). The child could NOT see it —
# it received only what we passed in `arguments`. Parent variables never leak into the child.
print(f"Parent still has COURSE_TAG={COURSE_TAG!r}; the child never saw it.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5 — `taskValues`: runtime data BETWEEN job tasks
# MAGIC
# MAGIC Job parameters carry **config INTO** tasks. `taskValues` carry **results BETWEEN** tasks: Task A `set()`s a small value (a row count, a watermark); a downstream Task B `get()`s it by naming A's task key.
# MAGIC
# MAGIC ```python
# MAGIC # In task "ingest_bronze":
# MAGIC dbutils.jobs.taskValues.set(key="bronze_rows", value=1042)
# MAGIC
# MAGIC # In a DOWNSTREAM task:
# MAGIC n = dbutils.jobs.taskValues.get(taskKey="ingest_bronze", key="bronze_rows")
# MAGIC ```
# MAGIC
# MAGIC Interactively there is no job context, so `get` needs a `debugValue` — that is how you develop the downstream notebook before the job exists. **You saw this live in the Week 3 job lab**: `week3_01` sets `bronze_rows`, `week3_02` reads it.
# MAGIC
# MAGIC Keep task values **small** (counts, flags, paths) — big data moves through **tables**, not task values.

# COMMAND ----------

# set() is a no-op outside a job — safe to run here:
dbutils.jobs.taskValues.set(key="bronze_rows", value=1042)

# get() interactively REQUIRES debugValue (without it: error). In a real job run, debugValue is ignored:
n = dbutils.jobs.taskValues.get(taskKey="ingest_bronze", key="bronze_rows", debugValue=999)
print(f"bronze_rows={n}  ← 999 here (debugValue); the real value when running inside a job")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6 — Which one when? (the decision table to memorize)
# MAGIC
# MAGIC | Scenario keyword | Mechanism | Why |
# MAGIC |---|---|---|
# MAGIC | "Reuse helper functions across notebooks **in the same session**" | `%run` | Shared session — definitions land in the caller |
# MAGIC | "Job parameter → notebook task" | **widgets** (`dbutils.widgets.get`) | The parameters→widgets contract |
# MAGIC | "Call a notebook with inputs and get a result back" | `dbutils.notebook.run` + `notebook.exit` | Isolated call, one string returned |
# MAGIC | "Task A computes a value Task B needs **at run time**" | `taskValues` set/get | The inter-task value API |
# MAGIC | "Run notebooks in order, with retries, on a schedule" | **A job with tasks** | Orchestration is the scheduler's job — not a driver notebook full of `%run` |
# MAGIC
# MAGIC **Exam answer shapes:**
# MAGIC - *Notebook can't see a variable after calling another notebook with `dbutils.notebook.run`* → correct; sessions are isolated. Use `%run` if sharing was the goal.
# MAGIC - *`%run` used but function "not defined"* → `%run` not alone in the cell, or wrong relative path.
# MAGIC - *Widget value arithmetic fails* → widgets return **strings**; cast first.
# MAGIC - *Pass a DataFrame between tasks with taskValues* → wrong; write a **table**, pass the name/count instead.
# MAGIC
# MAGIC **Next step:** do the exercises in `Week3_Params_Widgets_Lab` — then check yourself against `solutions/Week3_Params_Widgets_Lab_Solutions`.
