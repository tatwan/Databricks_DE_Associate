# Week 3 Overview — Answer Key & Explanations

**Q1 — C: As a widget of the same name.** A job parameter lands in the notebook's widget of the same name; `dbutils.widgets.get` reads it whether a human or the job set it. It is not an env var, a temp view, or a CLI argument.

**Q2 — C: In parallel.** With no dependency edge, independent tasks run at the same time. They are not ordered alphabetically or serially, and missing dependencies do not cause an error.

**Q3 — B: Fix the code, then Repair run.** Retries only help *transient* failures; a deterministic bug fails every retry, so you must fix and repair. More retries, serverless, or a schedule change none address a real bug.

**Q4 — D: Upstream failed.** The downstream task didn't break — its dependency did, so it shows "Upstream failed" (not Failed, Succeeded, or Cancelled).

**Q5 — A: Only the failed tasks plus their downstream tasks.** Repair reruns the failed path and never recomputes the green tasks, which is why it preserves prior compute. It does not restart the whole job or do nothing.

**Q6 — D: Task values.** `taskValues.set/get` carry small runtime results between tasks. Job parameters and widgets carry *config into* tasks, and `%run` inlines code — none pass a result *between* job tasks.

**Q7 — B: File arrival trigger.** It starts a run when data lands, avoiding empty polls and lowering latency. A cron schedule wastes runs, continuous is for always-on streaming, and table-update fires on Delta commits, not file drops.

**Q8 — C: In the Git provider.** Branch, commit, and push happen in the workspace, but the pull request is created and merged in the provider (GitHub/GitLab/Azure DevOps). Not the run page or the YAML.

**Q9 — A: `validate → deploy → run`.** Validate checks syntax/references, deploy places the resources, run executes them. Any order that swaps deploy and run, or runs before deploying, is wrong.

**Q10 — D: Inferred from dataset reads.** The pipeline engine derives the dependency graph from reads such as `spark.read.table(...)`, so table order is declarative rather than manually wired with `depends_on`. The older `dlt.read(...)` form may still run, but current Python guidance uses `from pyspark import pipelines as dp` and standard Spark reads.

**Q11 — B: A constraint fails the write; an expectation applies a warn/drop/fail policy.** Constraints reject the whole write; expectations apply a policy and record pass/fail metrics. They are not identical, expectations don't "always fail," and both concepts are valid on Delta/pipelines.

**Q12 — A: `%run` inlines into the session; a job task runs isolated.** `%run` pastes a notebook's cells into your session (shared variables); a job task runs in its own isolated context and passes data via parameters/task values. `%run` has no retries/schedules.

**Q13 — C: `bundle`, `variables`, `resources`, `targets`.** These are valid, commonly used top-level mappings, but they are not exhaustive; bundle files can also contain mappings such as `include`, `artifacts`, `sync`, `permissions`, and `run_as`. The distractors mix nested keys, invented keys, or catalog objects.
