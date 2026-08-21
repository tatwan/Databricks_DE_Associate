# Domain 4 — Lakeflow Jobs / Orchestration — Answer Key

**Q1 — C: The boxes in the DAG, each pointing at an asset.** Tasks are the DAG nodes (notebook, SQL, pipeline, etc.). Not cluster nodes, schedule entries, or catalog objects.

**Q2 — B: A DAG edge.** `depends_on` orders execution: the downstream task runs only after its upstream succeeds. It is not retries, a shared cluster, or a parameter map.

**Q3 — D: In parallel.** With no dependency edge, tasks run concurrently. Not alphabetical, not sequential, and no error.

**Q4 — A: Transient failures.** Retries cure flaky/temporary issues. Deterministic bugs, schema mismatches, and permission errors fail every retry.

**Q5 — A: Failed tasks plus their downstream tasks.** Repair reruns only the failed path; green tasks are never recomputed. Not the whole job, not the last task, not nothing.

**Q6 — C: A dashboard task.** A dashboard task is a DAG node that refreshes a dashboard and can depend on an upstream SQL task. A trigger starts a job, a for-each task loops over inputs, and a repair run reruns an unsuccessful path.

**Q7 — D: A widget of the same name.** Job parameters land in same-named widgets. Not env vars, task values, or `%run`.

**Q8 — B: Task values.** `taskValues.set/get` carry small results between tasks. Parameters/widgets carry config *into* tasks; notifications don't pass data.

**Q9 — A: A for-each task with controlled concurrency.** "Same logic, N items, K in parallel" = for-each with a concurrency limit. If/else branches, run-job calls a job, dashboard refreshes a dashboard.

**Q10 — D: An if/else conditional task.** Branch on a boolean (day of month). Not a loop, a SQL task, or a pipeline task.

**Q11 — B: The job's run history / matrix view.** Trends across runs are seen there; the Spark UI inspects one run. `DESCRIBE HISTORY` and the Git log are unrelated.

**Q12 — C: A table update trigger.** Fires on new Delta commits to a monitored table. File arrival fires on files, cron on time, continuous is always-on.

**Q13 — A: Deploy with the trigger paused.** Deploy-ready without surprise runs — the real go-live pattern. Deleting the schedule loses it, zero retries and continuous don't address "don't run yet."
