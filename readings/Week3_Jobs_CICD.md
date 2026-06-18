# Week 3: Lakeflow Jobs, Orchestration, and CI/CD

**Exam domains:** Productionizing Data Pipelines (Lakeflow Jobs), Implementing CI/CD (new in the May 2026 guide), and partial Troubleshooting & Monitoring.  
**Estimated read time:** 25–35 minutes  
**Running example:** Turning your BrewMart bronze→silver pipeline into a scheduled, repairable, versioned job

## Why This Week Matters

This week covers roughly a **quarter of the exam** (these skills are split across domains in the official weights). The CI/CD domain is brand new — most older practice material completely misses it. These topics also underpin governance and troubleshooting that appear in later weeks.

The shift in thinking: "I can run these cells" → "This pipeline runs itself on a schedule, survives failures, and can be promoted from dev to prod without manual copy/paste."

Two big ideas:
- **Idempotent tasks** (from Week 2) make retries and repair runs safe.
- **Git folders + bundles** separate "version the code" from "declare and promote the entire pipeline."

## Lakeflow Jobs Mental Model

A **job** is the unit of orchestration. It contains one or more **tasks** that form a **DAG** via `depends_on` relationships.

Independent tasks run in parallel. The scheduler only respects declared dependencies.

A job has:
- Tasks (notebook, SQL, dashboard, pipeline, etc.)
- Trigger(s)
- Compute
- Parameters
- Notifications
- Run history

**Task types the exam names explicitly:**
- Notebook
- SQL (query, file, or alert)
- Dashboard (refresh)
- Pipeline (run a Lakeflow Spark Declarative Pipeline)

Other types exist and may appear as distractors (Python wheel, JAR, dbt, for-each, if/else, run-job).

## Control Flow

- **Retries** — per-task max retries + interval. Only for transient failures.
- **Run-if conditions** — run a task on success, failure, or completion of dependencies (e.g., "always send the summary email").
- **If/else condition task** — branch the DAG based on a boolean (often a task value).
- **For-each task** — iterate over a list with controlled concurrency.

**Important distinction:** Retries cannot fix a deterministic bug. That requires a code fix followed by **Repair run**.

## Triggers — Time-Based vs Data-Driven

| Trigger          | Category     | Fires when...                  | Typical stem language                  |
|------------------|--------------|--------------------------------|----------------------------------------|
| Scheduled (cron) | Time-based   | Clock says so                  | "daily at 02:00", SLA language         |
| File arrival     | Data-driven  | New files land in a location   | "unpredictable times", "polling finds nothing" |
| Table update     | Data-driven  | Monitored Delta table commits  | "whenever silver changes"              |
| Continuous       | Always-on    | Job restarts as it finishes    | Streaming-style workloads              |

**Decision rule:** Known cadence + SLA → scheduled. "Whenever data shows up" → file arrival or table update.

**Common trap:** A tight cron (every minute) is still polling. It burns compute on empty runs. File arrival is the lower-latency, lower-cost answer the exam wants.

**Manual (no trigger):** Runs only when you click Run now or trigger via API/CLI. Useful for ad-hoc or externally orchestrated workloads.

## Parameters and Task Values

**Job parameters** are key-value pairs defined at the job level and pushed to every task.

Notebook tasks receive them as **widgets**:
```python
dbutils.widgets.text("target_schema", "lab1_dev")
schema = dbutils.widgets.get("target_schema")
```

**Task values** (`dbutils.jobs.taskValues.set` / `get`) pass small results between tasks (row counts, status flags, etc.). Big data moves through tables, not task values.

Dynamic references: `{{job.parameters.x}}`, `{{tasks.ingest.values.rows}}`.

This is how the same notebook serves dev, test, and prod.

## Monitoring and Repair

Every run is recorded in **run history** with status, duration, trigger source, and per-task timings.

The **matrix view** (runs × tasks) quickly shows which task is degrading or failing repeatedly.

**Repair run** is critical:
- It re-executes only the failed task(s) **and** any downstream tasks that were skipped because of an upstream failure.
- Successful upstream tasks are **never** re-executed.
- You can adjust parameters just for the repair run.

This is why idempotent tasks (COPY INTO, MERGE, etc.) are so valuable — you can safely repair without duplicating work or corrupting state.

**Statuses to know:** Succeeded, Failed, Skipped, Upstream failed, Queued, Running.

## Serverless Jobs Compute

Serverless job compute is the hands-off, auto-optimized option managed by Databricks.

In Free Edition this is what you use. The exam still expects you to know the classic job cluster pattern for comparison.

Lakeflow Jobs can orchestrate multiple task types (notebooks, SQL, dbt, Python wheels, etc.) regardless of whether they run on serverless or classic job clusters.

## CI/CD for Data Engineers

Putting notebooks in Git is only half the story.

**Two layers:**
1. **Git folders** — version control *inside* the workspace (clone, branch, commit, push). Pull requests are created in the external Git provider (GitHub, etc.).
2. **Declarative Automation Bundles** (`databricks.yml`) — declare jobs, pipelines, and other resources as code. Use variables + per-target overrides (targets can also specify a `mode` such as `development` vs `production` to control name prefixes and other behaviors) so the same bundle produces different concrete objects in dev vs prod.

Larger projects often keep individual jobs or pipelines in separate YAML files (for example under a `resources/` folder), but for the exam you only need to recognize the top-level `bundle`, `variables`, `resources`, and `targets` blocks.

**The three CLI verbs (in order):**
1. `databricks bundle validate` — syntax and reference check.
2. `databricks bundle deploy -t <target>` — place/update resources in the workspace.
3. `databricks bundle run -t <target> <job_name>` — execute a deployed job.

In a real CI pipeline, a service principal runs `validate → deploy -t prod` on merge to main.

**Key mental model:** Git folders version the *notebooks*. Bundles version the *orchestration and configuration*.

**Exam Trap**

A very common misconception: “I put my notebook in a Git folder — I’m done with CI/CD.”

Putting notebooks under version control is only half the story. 

- Git folders version *code*.
- Declarative Automation Bundles (`databricks.yml`) version the *full job definition* (tasks, dependencies, schedule, parameters) and control promotion across environments (dev → test → prod).

The pull request is always created in the external Git provider (GitHub, GitLab, etc.), never inside the Databricks workspace. Exam questions love testing this exact boundary.

## BrewMart in Week 3

You will:
- Import the two task notebooks (`ingest_bronze` and `build_silver`).
- Create a 2-task Lakeflow Job with a dependency.
- Add job parameters (`target_schema`, `simulate_failure`).
- Add a paused daily schedule and retries.
- Cause a controlled failure.
- Observe `upstream-failed`.
- Use **Repair run** after fixing the parameter.
- Walk through a Git folder round-trip (branch → edit → commit/push → PR in provider → pull main).
- Read the course `cicd/databricks.yml` to see how the job you built by hand is declared in YAML.

## Exam Focus — High-Yield Patterns

- Trigger selection from scenario wording.
- Repair run vs Run now vs retries (constantly cross-used as distractors).
- Task type matching (SQL refresh → SQL task, BI freshness → dashboard task).
- Parameters → widgets contract.
- Bundle blocks (`bundle`, `variables`, `resources`, `targets`).
- The three CLI verbs and what each does.
- "Where is the pull request created?" → in the Git provider, not the workspace UI.
- Run history for trends; Spark UI for deep dive into one run (Week 4).

## Self-Check Questions

1. Task 4 of 7 failed overnight. You fixed the notebook. What is the most efficient next action, and why?
2. Name the three trigger types mentioned in the exam objective and one scenario keyword for each.
3. What is the difference between a job parameter and a task value? Give one use case for each.
4. In a `databricks.yml`, where does the instruction "in prod, write to schema `sales_prod`" live?
5. A teammate says "I committed my notebook change in the workspace." Has the pull request been created yet? Explain.

## Recommended Documentation

**Primary reading (~45 min)**

- Lakeflow Jobs overview + "Configure and edit tasks"
- Trigger types for Lakeflow Jobs
- Repair a job run; Job run statuses
- Git folders (Databricks Git integration) — the end-to-end workflow
- What are Declarative Automation Bundles? + `databricks.yml` structure reference (focus on high-level blocks)

**Practice targets**
- Rebuild a 2-task job from scratch in under 10 minutes.
- Read a job's JSON view and map the keys back to the bundle YAML.
- (Brave) Run `databricks bundle validate` locally against the course bundle.

## Mini Checklist Before Week 4

- [ ] My job exists with at least three runs in history (success → failed → repaired).
- [ ] I can recite the three CLI verbs in order and the four main blocks of a `databricks.yml`.
- [ ] I can explain where a pull request is actually created.
- [ ] My `sales_silver` is intact — Week 4 will add governance on top of it.

Your pipeline is now a scheduled, observable, repairable asset. Week 4 adds the locks (governance) and the diagnostics (optimization and troubleshooting).
