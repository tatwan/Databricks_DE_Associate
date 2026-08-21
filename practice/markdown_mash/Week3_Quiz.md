# Week 3 quiz — run in the closing segment, end of class

> Instructor-only. Covers **Week 3** content. End quiz: 8 questions, ~7 minutes, run live.
> The Self-Review Bank below is assigned as homework, not run live.
> The prior-week review quiz is in `Pre_Week3_Quiz.md` (run at 0:00).

---

## END QUIZ — Week 3 Content (run at ~1:50)

# Week 3 Quiz: Lakeflow Jobs, Orchestration, and CI/CD
# Score 100

## Q1: A 6-task job run has one failed task and two downstream tasks that were skipped. What does Repair run do?
- [ ] Re-executes all six tasks from the beginning
- [ ] Re-executes only the single failed task and marks the skipped ones as succeeded
- [ ] Creates a copy of the job with the failed task removed
- [x] Re-executes the failed task and its downstream tasks, skipping already-successful ones
::time=25

## Q2: Which trigger type starts a job run when new data files land in a monitored storage location?
- [x] File arrival trigger
- [ ] Scheduled trigger with a 1-minute interval
- [ ] Continuous trigger
- [ ] Table update trigger
::time=20

## Q3: A silver table is updated by several upstream jobs at unpredictable times. A downstream aggregation job must run whenever the silver table receives new data. Which trigger fits best?
- [ ] A scheduled trigger every five minutes
- [ ] A file arrival trigger on the landing volume
- [x] A table update trigger on the silver table
- [ ] A continuous trigger on the aggregation job
::time=30

## Q4: The same transformation notebook must run once per region for 14 regions, up to 4 in parallel. Which mechanism should be used?
- [ ] Fourteen copies of the task with manual dependencies
- [ ] A run-if condition on each regional task
- [ ] An if/else condition task evaluating the region list
- [x] A for-each task iterating the region list with concurrency set to 4
::time=30

## Q5: A team must deploy the same job to dev and prod, where prod writes to a different schema and uses a different schedule. What is the bundle-native way to do this?
- [ ] Maintain two separate databricks.yml files in two repositories
- [ ] Edit the YAML manually before each prod deployment
- [x] Define targets with variable overrides for schema and schedule
- [ ] Use the workspace UI to clone the dev job into prod monthly
::time=30

## Q6: Which Databricks CLI sequence correctly takes a bundle from source to a running job in the dev environment?
- [x] databricks bundle validate → databricks bundle deploy -t dev → databricks bundle run -t dev my_job
- [ ] databricks bundle run -t dev my_job → databricks bundle deploy -t dev
- [ ] databricks bundle deploy -t dev → databricks bundle validate
- [ ] databricks jobs create → databricks bundle sync → databricks bundle start
::time=30

## Q7: A job defines a job parameter env=prod. How does a notebook task receive this value at run time?
- [ ] Through a global Python variable named env injected into the session
- [ ] By reading the job's databricks.yml from the workspace
- [ ] Via spark.conf.get("job.env") on the cluster
- [x] As a widget, read with dbutils.widgets.get("env")
::time=30

## Q8: A data engineer working in a workspace Git folder has committed and pushed a feature branch. Where is the pull request created and merged?
- [x] In the Git provider (GitHub/GitLab/Azure DevOps); the workspace links out to it
- [ ] In the Databricks workspace Git folder UI
- [ ] In the Databricks CLI with databricks repos merge
- [ ] PRs are unnecessary; pushing the branch auto-merges to main
::time=25

### End Quiz Answer Key (with explanations)

| # | Answer | Difficulty | Explanation |
|---|--------|-----------|-------------|
| Q1 | Failed + downstream only | Easy | Repair run's defining behavior — successful tasks are never re-executed. |
| Q2 | File arrival | Easy | Watches a storage location; the data-driven alternative to polling. |
| Q3 | Table update trigger | Applied | The dependency is on a *table's* commits, not files or clock time. |
| Q4 | For-each | Applied | Iterate a list with a concurrency setting — verbatim "looping" objective. |
| Q5 | Targets + variable overrides | Applied | The bundle-native promotion pattern — same code, per-target config. |
| Q6 | validate → deploy → run | Applied | The canonical CLI order; deploy places resources, run executes them. |
| Q7 | Widget | Tricky | Job parameters surface in notebook tasks as widgets — the parameters→widgets contract. |
| Q8 | In the provider | Easy | The workspace gets you to the PR; creation/review/merge happen in GitHub/GitLab/DevOps. |

---

## SELF-REVIEW BANK — assign as homework (not run live)

# Week 3 Self-Review
# Score 100

## Q1: What is the current Databricks name for the workflow/job orchestration service?
- [ ] Databricks Workflows
- [x] Lakeflow Jobs
- [ ] Delta Orchestrator
- [ ] Lakeflow Connect
::time=20

## Q2: Which file defines a Declarative Automation Bundle?
- [ ] bundle.json
- [ ] workflow.yml
- [x] databricks.yml
- [ ] deploy.yaml
::time=20

## Q3: Which set of Git operations can be performed directly inside the Databricks workspace Git folder UI?
- [ ] Only viewing files; all Git operations require the provider website
- [x] Creating branches, switching branches, committing, and pushing changes
- [ ] Merging pull requests and deleting remote repositories
- [ ] Rebasing and cherry-picking across forks
::time=20

## Q4: After a nightly gold-table load, leadership's dashboard must display current data. Which job design is most appropriate?
- [x] Add a dashboard task that depends on the gold-load task
- [ ] Schedule a second job that emails the dashboard as a PDF
- [ ] Convert the dashboard to query the bronze layer directly
- [ ] Add a notebook task that calls the BI tool's screenshot API
::time=30

## Q5: A task calling an external API fails intermittently (about 5% of calls) and succeeds when retried. What is the FIRST mechanism to configure?
- [ ] An if/else task that checks API health before calling
- [x] Task retries with a retry interval
- [ ] A repair run after each failure
- [ ] A continuous trigger so failures restart automatically
::time=30

## Q6: A small team spends hours each sprint tuning job-cluster sizes for unpredictable, spiky workloads and wants to stop managing compute entirely. Which option best fits?
- [ ] A large all-purpose cluster shared by all jobs
- [x] Serverless jobs compute
- [ ] A pool of pre-warmed job clusters with fixed sizes
- [ ] Single-node clusters for every task
::time=30

## Q7: Over three weeks, a job's nightly run time has grown from 20 to 55 minutes with no code changes. Which feature provides the FIRST evidence for diagnosing this trend?
- [ ] The Spark UI of the most recent run only
- [ ] The job's email notification settings
- [x] The run history view comparing durations across runs (matrix view per task)
- [ ] DESCRIBE HISTORY on the target table
::time=30

## Q8: A team wants to reuse a set of helper functions (config loaders, common casts) across several notebooks in the same session. Which mechanism is designed for this?
- [x] %run ./helpers at the top of each notebook
- [ ] A job task that runs the helpers notebook first
- [ ] dbutils.jobs.taskValues.set for each function
- [ ] Copy-pasting the functions into each notebook
::time=25

### Self-Review Answer Key

| # | Answer | Explanation |
|---|--------|-------------|
| Q1 | Lakeflow Jobs | Current name; "Workflows" is legacy, Lakeflow Connect is ingestion. |
| Q2 | databricks.yml | The bundle's root configuration file. |
| Q3 | Branch/commit/push | The workspace UI covers the daily Git loop; PR merge lives in the provider. |
| Q4 | Dashboard task | BI refresh as a DAG node depending on the load — an exam-named task type. |
| Q5 | Retries | Intermittent + succeeds-on-retry = transient; retries are the first line. |
| Q6 | Serverless | "Stop managing compute" + spiky = serverless's exam-stated value. |
| Q7 | Run history / matrix | A *trend* needs runs compared over time; Spark UI inspects one run. |
| Q8 | %run | Inlines the helper notebook into the same session, sharing definitions. A job task runs in isolation — nothing is shared. |

---
