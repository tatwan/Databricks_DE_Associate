# Week 3 Overview — Lakeflow Jobs, Orchestration, CI/CD, Declarative Pipelines
# Score 100

## Q1: How does a notebook task receive a job parameter?
- [ ] As an OS environment variable
- [ ] Through a shared temporary view
- [x] As a widget of the same name (`dbutils.widgets.get`)
- [ ] As a positional argument passed on the command line
::time=45

## Q2: Two tasks in a job have no `depends_on` edge between them. How do they run?
- [ ] The job errors — every task needs a dependency
- [ ] Sequentially, one completing before the next starts
- [x] In parallel
- [ ] Strictly in alphabetical order of task key
::time=45

## Q3: A task with 2 retries fails on a **deterministic** bug every time. What actually fixes it?
> Retries cure only *transient* failures. A real bug needs a fix, then a Repair run.
- [ ] Raise the retry count to 10 or more
- [x] Fix the code, then trigger a Repair run
- [ ] Switch the task to serverless compute
- [ ] Add a schedule so it runs again later
::time=45

## Q4: In a run where Task 1 failed, what status does its downstream Task 2 show?
- [ ] Cancelled by the user
- [ ] Succeeded
- [ ] Failed
- [x] Upstream failed
::time=45

## Q5: What does a **Repair run** re-execute?
- [x] Only the failed tasks plus their downstream tasks
- [ ] The entire job again, starting from the first task
- [ ] Only the very first task in the DAG
- [ ] Nothing — it just resends notifications
::time=45

## Q6: Which mechanism passes a small runtime **result** (like a row count) between two tasks?
- [ ] Job parameters set on the job
- [ ] Notebook widgets read at the top
- [ ] A `%run` include of a shared helper notebook
- [x] Task values (`taskValues.set` / `taskValues.get`)
::time=45

## Q7: A file lands at unpredictable times; an hourly schedule mostly finds nothing. Best trigger?
- [ ] A scheduled cron trigger
- [x] A file arrival trigger
- [ ] A continuous, always-on trigger
- [ ] A table update trigger
::time=45

## Q8: Where is a pull request **created and merged** in the Git-folders workflow?
- [ ] In the Databricks workspace UI
- [ ] On the job's run page
- [x] In the Git provider (GitHub, GitLab, Azure DevOps)
- [ ] Inside the bundle's `databricks.yml` definition file
::time=45

## Q9: What is the correct order of Declarative Automation Bundle CLI verbs?
- [x] `validate → deploy → run`
- [ ] `deploy → validate → run`
- [ ] `run → deploy → validate`
- [ ] `validate → run → deploy`
::time=45

## Q10: In a current Lakeflow Spark Declarative Pipeline, how is the order between bronze and silver determined?
- [ ] You wire `depends_on` between the tables by hand
- [ ] Alphabetically by table name
- [ ] By file modification timestamp
- [x] From dataset read dependencies
::time=45

## Q11: What is the difference between a table **CONSTRAINT** and a pipeline **EXPECTATION**?
- [ ] They are identical mechanisms
- [x] Constraint fails; expectation applies a policy
- [ ] An expectation always fails the update, while a constraint merely warns
- [ ] Only expectations work on Delta tables
::time=45

## Q12: `%run ./helper` versus wiring a notebook as a **job task** — which is true?
- [x] `%run` shares a session; job tasks are isolated
- [ ] Both run in complete isolation from each other
- [ ] `%run` supports retries, schedules, and repair runs too
- [ ] A job task shares all variables with its caller
::time=45

## Q13: Which set contains valid top-level mappings commonly used in `databricks.yml`?
- [ ] `jobs`, `tasks`, `clusters`, `secrets`
- [ ] `name`, `env`, `deploy`, `run`
- [x] `bundle`, `variables`, `resources`, `targets`
- [ ] `catalog`, `schema`, `volume`, `table`
::time=45
