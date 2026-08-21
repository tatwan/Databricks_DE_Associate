# Pre-Week 4 quiz — run at 0:00, before class content starts

> Instructor-only. Reviews **Week 3** content. 5 questions, ~4 minutes.

# Week 4 Starter: Week 3 Review
# Score 100

## Q1: A 6-task job run has one failed task and two downstream tasks that were skipped. What does Repair run do?
- [ ] Re-executes all six tasks from the beginning
- [ ] Re-executes only the single failed task and marks the skipped ones as succeeded
- [ ] Creates a copy of the job with the failed task removed
- [x] Re-executes the failed task and its downstream tasks, skipping already-successful ones
::time=25

## Q2: Files land in a volume at unpredictable times; an hourly polling job mostly finds nothing. Which trigger fits best?
- [x] File arrival trigger
- [ ] Scheduled trigger with a 1-minute interval
- [ ] Continuous trigger
- [ ] Manual trigger with email reminders
::time=20

## Q3: Which Databricks CLI sequence correctly takes a bundle from source to a running job?
- [x] validate → deploy → run
- [ ] run → deploy
- [ ] deploy → validate
- [ ] sync → start
::time=20

## Q4: Where is a pull request created and merged for a workspace Git folder?
- [x] In the Git provider (GitHub/GitLab/Azure DevOps)
- [ ] In the Databricks workspace Git folder UI
- [ ] In the Databricks CLI
- [ ] PRs auto-merge on push
::time=20

## Q5: A job defines a job parameter env=prod. How does a notebook task receive it at run time?
- [ ] A global Python variable named env
- [ ] By reading databricks.yml
- [ ] Via spark.conf.get("job.env")
- [x] As a widget, read with dbutils.widgets.get("env")
::time=25

---

### Answer Key

| # | Answer | Checks |
|---|--------|--------|
| Q1 | Failed + downstream only | Repair run semantics |
| Q2 | File arrival | Data-driven beats polling |
| Q3 | validate → deploy → run | The three CLI verbs, in order |
| Q4 | In the provider | The workspace/provider boundary |
| Q5 | Widget | The parameters→widgets contract |
