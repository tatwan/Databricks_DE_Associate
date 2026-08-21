# Exam Domain 4 — Lakeflow Jobs / Orchestration (~16%)
# Score 100

## Q1: A job is the unit of orchestration. What are its **tasks**?
- [ ] The individual compute nodes in the cluster
- [ ] The schedule entries that trigger the job
- [x] The boxes in the DAG, each pointing at an asset
- [ ] The catalog objects the job reads from
::time=45

## Q2: `depends_on` between two tasks represents…
- [ ] A per-task retry-and-interval policy
- [x] A DAG edge — downstream runs only after upstream succeeds
- [ ] A cluster shared between the two tasks
- [ ] A parameter mapping automatically passed between the two tasks
::time=45

## Q3: Independent tasks (no edge between them) run…
- [ ] In strict alphabetical order
- [ ] One after another, sequentially
- [ ] Not at all — the job errors out
- [x] In parallel
::time=45

## Q4: Task **retries** fix which kind of failure?
- [x] Transient failures (flaky API, network blip)
- [ ] Deterministic logic bugs in the task code
- [ ] Schema mismatches on write
- [ ] Permission and access errors
::time=45

## Q5: A **Repair run** re-executes…
- [x] Failed tasks plus their downstream tasks
- [ ] The whole job again from the very first task
- [ ] Only the last task in the DAG
- [ ] Nothing — it only resends alerts
::time=45

## Q6: A dashboard must refresh only after its upstream SQL transformation succeeds. Which task should be downstream in the DAG?
- [ ] A file arrival trigger
- [ ] A for-each task
- [x] A dashboard task
- [ ] A repair run
::time=45

## Q7: A job parameter arrives in a notebook task as…
- [ ] An environment variable
- [ ] A task value set upstream
- [ ] A `%run` include
- [x] A widget of the same name
::time=45

## Q8: Which mechanism carries small runtime data **between** tasks?
- [ ] Job parameters configured on the job
- [x] Task values (`taskValues.set` / `taskValues.get`)
- [ ] Notebook widgets read at the top of the notebook
- [ ] Email notifications sent on completion
::time=45

## Q9: "Same logic for 14 regions, 4 in parallel." Which task type?
- [x] A for-each task
- [ ] An if/else conditional branch task
- [ ] A run-job task that calls another job
- [ ] A dashboard-refresh task node
::time=45

## Q10: "Full rebuild on the 1st of the month, incremental otherwise." Which task type?
- [ ] A for-each loop over regions
- [ ] A plain SQL query task
- [ ] A pipeline (DLT) task
- [x] An if/else conditional task
::time=45

## Q11: A duration **trend** across many runs is best diagnosed where?
- [ ] The Spark UI drilldown of a single run
- [x] The job's run history / matrix view
- [ ] `DESCRIBE HISTORY` on the table
- [ ] The Git provider's commit log
::time=45

## Q12: Which trigger fires when a monitored Delta table receives new commits?
- [ ] A file arrival trigger
- [ ] A scheduled cron trigger
- [x] A table update trigger
- [ ] A continuous, always-on trigger
::time=45

## Q13: "Deploy ready, but must not run until go-live." Configure the job how?
- [x] Deploy with the trigger paused
- [ ] Delete the schedule entirely
- [ ] Set the retry count to zero
- [ ] Switch to a continuous trigger
::time=45
