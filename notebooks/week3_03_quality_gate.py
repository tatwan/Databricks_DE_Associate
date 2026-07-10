# Databricks notebook source
# MAGIC %md
# MAGIC # Task 3 (stretch): Data-Quality Gate (BrewMart)
# MAGIC **Role in the DAG:** final task, `depends_on` `build_silver`. The job — not a human — runs this notebook.
# MAGIC
# MAGIC ## What a "quality gate" is, and why pipelines have one
# MAGIC A quality gate is a **circuit-breaker task** at the end of a pipeline. Its only job is to check an invariant that *must* hold — here, "silver is not empty" — and to **fail loudly** if it doesn't. Failing on purpose sounds strange until you picture the alternative: an upstream glitch produces an empty `sales_silver`, every downstream dashboard silently shows zero revenue, and nobody notices for a week. A gate turns that silent-wrong into a loud-stopped: the task goes red, the job fails, notifications fire, and bad data never gets certified as good.
# MAGIC
# MAGIC This is the same instinct as Week 2's `CHECK` constraint (reject bad rows at write time) and the declarative-pipeline **expectations** you'll meet in the bonus — three layers of the same idea: *stop bad data early, on purpose.*
# MAGIC
# MAGIC ## Why this is a NOTEBOOK task, not a bare SQL cell (important)
# MAGIC A standalone SQL task does **not** inherit any `USE SCHEMA` you ran interactively somewhere else — every job task runs in its **own isolated context** with no default schema. So an unqualified `FROM sales_silver` would fail (or hit the wrong table) once it's wired into the job. The safe, repeatable pattern is the one Task 1 and Task 2 already use: receive the schema as a **job parameter** (which arrives as a widget) and **fully qualify** the table name. That contract — *pass context through parameters, not session state* — is itself an exam idea.
# MAGIC
# MAGIC **Why it matters (exam):** questions describe a task that "works when I run it by hand but fails in the job." The answer is almost always missing context — an unset schema, a path that assumed the interactive session. Parameterize it.

# COMMAND ----------

# MAGIC %md ### Receive the schema as a job parameter (widget)
# MAGIC **Goal:** get the target schema the same way Tasks 1 and 2 do — so this task, too, serves any learner or environment unchanged.
# MAGIC
# MAGIC **Look for:** the printed fully-qualified table name. Interactively you see the widget default; inside the job you see the job parameter's value.

# COMMAND ----------

dbutils.widgets.text("target_schema", "lab1_yourname")
target_schema = dbutils.widgets.get("target_schema")
print(f"Quality gate checking workspace.{target_schema}.sales_silver")

# COMMAND ----------

# MAGIC %md ### The gate
# MAGIC **Goal:** pass when silver has rows; **raise** (fail the task, and so the job) when it is empty.
# MAGIC
# MAGIC **Look for:** in a healthy run, the printed row count and a clean exit. If you ever see this task go red, the job did its job — it refused to certify an empty silver.

# COMMAND ----------

row_count = spark.table(f"workspace.{target_schema}.sales_silver").count()

if row_count == 0:
    raise Exception("Quality gate FAILED: sales_silver is EMPTY — stopping the pipeline")

print(f"Quality gate PASSED: sales_silver has {row_count} rows")
dbutils.notebook.exit(f"quality_gate=passed rows={row_count}")
