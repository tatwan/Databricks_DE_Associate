# Week 3: Orchestration and Delivery — Lakeflow Jobs, Git Folders, and Automation Bundles

> Aligned to the **May 4, 2026** Databricks Certified Data Engineer Associate exam guide.
> Primary exam domains: **Working with Lakeflow Jobs** (16%, full coverage) + **Implementing CI/CD** (10%, full coverage) + **Troubleshooting, Monitoring, and Optimization** (run history / Jobs-UI monitoring objectives — the rest lands in Week 4).
> Together: roughly **a quarter of the exam** lives in this session.

---

## 1. Session Overview

- **Duration:** 2 hours
- **Target audience:** Same cohort; Weeks 1–2 completed
- **Prerequisites:**
  - Week 2 lab objects intact (`sales_bronze`, `sales_silver`, `landing/sales_incoming/` with both day files)
  - The two task notebooks imported into the workspace **before class**: `week3_01_ingest_bronze.py`, `week3_02_build_silver.py` (Workspace → Import)
  - Optional but valuable: a personal GitHub account (for the Git-folders demo segment)
- **Main exam domains covered:**
  - Domain 4: Working with Lakeflow Jobs — tasks, DAGs, control flow, triggers (all objectives)
  - Domain 5: Implementing CI/CD — Git folders workflow, Declarative Automation Bundles, CLI (all objectives; bundles are demo/concept in Free Edition)
  - Domain 6 (partial): run history trends, Jobs UI monitoring, repair-and-rerun
- **Learning objectives.** By the end of this session, learners can:
  1. Describe the Lakeflow Jobs model: job → tasks → DAG, and configure notebook, SQL, dashboard, and pipeline task types with dependencies
  2. Implement control flow: retries, run-if conditions, if/else branching, and for-each looping
  3. Choose and configure trigger types — scheduled (cron), file arrival, table update, continuous — and justify time-based vs. data-driven triggering
  4. Pass job parameters to notebook tasks (parameters → widgets) and between tasks (task values)
  5. Monitor runs: read the run-history matrix, spot duration drift against baselines, and use **repair run** to rerun only failed tasks
  6. Explain serverless jobs compute as the hands-off, auto-optimized option
  7. Work the Git folders flow: clone, branch, commit, push, and where the PR actually happens
  8. Read a `databricks.yml`: bundle, resources, variables, targets — and the CLI verbs `validate`, `deploy`, `run`

---

## 2. Recommended Timing

| Time      | Segment                      | Purpose                     |
| --------- | ---------------------------- | --------------------------- |
| 0:00–0:10 | Warm-up: Week 2 retrieval + "what breaks if we run your lab cells by hand forever?" | Motivate orchestration from felt pain |
| 0:10–0:42 | Concept slides (15 slides)   | Jobs model, control flow, triggers, monitoring, Git folders, bundles |
| 0:42–1:10 | Instructor demo              | Build a 2-task job live: parameters, schedule, failure, repair; Git folder + bundle walkthrough |
| 1:10–1:40 | Hands-on lab                 | Learners productionize their Week 2 pipeline as a job |
| 1:40–1:50 | In-class activity            | "Orchestration triage" decision cards |
| 1:50–2:00 | Markdown Mash quiz + wrap-up | Exam readiness check, homework |

---

## 3. Slide Deck Content

### Slide 1: Recap and Today's Map — From Notebooks to Production

**Key bullets**
- Weeks 1–2: you built a pipeline; this week: it runs itself, survives failures, and ships across environments
- Two full domains today: Lakeflow Jobs (16%) + CI/CD (10%), plus the monitoring objectives of Domain 6
- The CI/CD domain is **new in the May 2026 exam** — almost no older prep material covers it
- One storyline: BrewMart's pipeline → scheduled job → versioned code → promotable bundle

**Speaker notes**
Open with the pain question: "Who wants to run those COPY INTO cells by hand every morning at 6am?" List what manual execution can't give you: schedules, retries, dependency order, alerting, audit, environments. That list IS today's agenda. Stress the CI/CD novelty — anyone studying from a 2024/2025 course has a blind spot exactly here; this session is where our course earns its keep.

**Visual suggestion**
Before/after split: a human at a laptop running cells vs. a DAG with a clock, retry arrows, and a dev→prod conveyor.

**Exam relevance**
Orientation; flags the highest-risk gap (CI/CD) for this audience.

**Common misconception**
"Orchestration is an ops concern, not exam material." It's ~26% of the exam.

---

### Slide 2: Lakeflow Jobs — The Mental Model

**Key bullets**
- **Job** = the unit of orchestration; contains one or more **tasks**; tasks form a **DAG** via dependencies
- Formerly "Workflows"/"Jobs" — exam says **Lakeflow Jobs**; UI: the Jobs & Pipelines section
- A job has: tasks, trigger(s), compute, parameters, notifications, permissions, run history
- ADF translation: job ≈ pipeline; task ≈ activity; trigger ≈ trigger (the reflex transfers well here)

**Speaker notes**
This is the anchor slide — draw the hierarchy live: job at the top, tasks as boxes, arrows as `depends_on`. Make the point that the DAG is *declared*, not coded: you say what depends on what; the scheduler works out execution order and parallelism (independent tasks run concurrently). The ADF mapping is unusually clean for this topic — use it, then drop it.

**Visual suggestion**
A labeled job anatomy diagram: title bar (job), 4 task boxes in a diamond DAG, a clock icon (trigger), bell (notifications), and a sidebar (parameters, compute).

**Exam relevance**
Domain 4's foundation: "Configure common tasks … and their dependencies using Lakeflow Jobs and its DAG-based task graph."

**Common misconception**
That tasks in a job run strictly in sequence. Independent branches run in parallel — sequence comes only from declared dependencies.

---

### Slide 3: Task Types — What a Box in the DAG Can Be

**Key bullets**
- Exam-named four: **notebook**, **SQL** (query/file/alert), **dashboard** (refresh), **pipeline** (run a Lakeflow Spark Declarative Pipeline)
- Others exist (Python script/wheel, JAR, dbt, for-each, if/else, run-job) — recognize on sight
- Mix freely: SQL task → notebook task → dashboard refresh in one DAG
- Each task points at an asset (notebook path, SQL query, pipeline ID) + its own parameters

**Speaker notes**
Drill the exam's four by use case: transformation logic → notebook; warehouse-bound SQL → SQL task; "leadership wants the dashboard fresh after the load" → dashboard task; "the ETL itself is declarative" → pipeline task. The dashboard task surprises ADF folks — refreshing BI is a first-class DAG node here, no webhook hacks. Mention run-job (job calling another job) as the modularization pattern.

**Visual suggestion**
Four cards with icons (notebook/SQL/dashboard/pipeline), each with a one-line "use when…" caption.

**Exam relevance**
Verbatim: "Configure common tasks (notebook, SQL query, dashboard, and pipeline tasks)."

**Common misconception**
"Everything must be a notebook." Choosing the *right* task type is itself an exam question — e.g., a pure SQL refresh on a warehouse should be a SQL task, not a notebook.

---

### Slide 4: Control Flow — Retries, Conditions, Branching, Looping

**Key bullets**
- **Retries:** per-task max retries + retry interval — first defense against transient failures
- **Run-if conditions:** run a task when dependencies succeed / fail / complete-at-all (cleanup & alert patterns)
- **If/else condition task:** branch the DAG on a boolean expression (e.g., a task value)
- **For-each task:** loop a task over a list (e.g., one ingest per region), with controlled concurrency

**Speaker notes**
Map each to the failure/variation it solves: flaky API → retries; "always send the summary email even on failure" → run-if `All done`; "full load on Sundays, incremental otherwise" → if/else; "same logic, 12 regions" → for-each. These are verbatim outline items ("retries and conditional tasks such as branching and looping"). ADF folks know these as activity policies and ForEach — the concepts port directly.

**Visual suggestion**
Mini-DAG gallery: four 3-node sketches, one per mechanism, each annotated with its trigger phrase ("transient failure", "always run", "boolean branch", "iterate list").

**Exam relevance**
Verbatim Domain 4 objective — control-flow scenario questions are near-certain.

**Common misconception**
Retries fix everything. They fix *transient* failures; a deterministic bug fails all retries — that's what repair-and-rerun (after the fix) is for.

---

### Slide 5: Triggers — Time-Based vs. Data-Driven

**Key bullets**
- **Scheduled:** cron/periodic — "run at 02:00 daily"
- **File arrival:** watch a volume/external location — run when new files land
- **Table update:** run when monitored Delta table(s) get new commits
- **Continuous:** keep the job always running (streaming-style); also: manual/run-now
- Decision rule: known cadence + SLA → schedule; "whenever data shows up" → file arrival/table update

**Speaker notes**
The exam asks this as a choice: "Files land unpredictably between 1am and 5am; the team currently polls hourly" → file arrival trigger (less compute, lower latency, no empty runs). "Downstream must refresh when silver changes, whatever the cause" → table update. Make them say the categories: scheduled = time-based; file-arrival/table-update = data-driven. Free Edition: scheduled triggers work; file-arrival is configurable on volumes — verify in rehearsal; table-update/continuous may be constrained — **"Exam concept; verify availability; teach regardless."**

**Visual suggestion**
2×2: rows = time-based / data-driven; columns = mechanism / when-to-choose, with the three trigger icons placed.

**Exam relevance**
Two verbatim objectives: trigger types incl. "(scheduled, file arrival, and table update)" and "Choose between time-based and data-driven triggers based on data availability and pipeline dependencies."

**Common misconception**
Polling with a tight cron *is* event-driven. It isn't — it burns compute on empty runs and still adds latency; that contrast is exactly how the exam frames the question.

---

### Slide 6: Parameters — Jobs Talk to Notebooks via Widgets

**Key bullets**
- **Job parameters:** key-value pairs defined on the job; pushed to all tasks
- Notebook tasks receive them as **widgets**: `dbutils.widgets.get("target_schema")`
- **Task values:** `dbutils.jobs.taskValues.set/get` — pass small results *between* tasks
- Dynamic value references: `{{job.parameters.x}}`, `{{tasks.t.values.y}}`, run metadata like `{{job.start_time}}`

**Speaker notes**
This is how the same notebook serves dev and prod — parameterize the schema, never hardcode. Show the contract: job parameter `target_schema` → widget of the same name in the notebook (our demo notebooks are built exactly this way). Task values answer "Task 2 needs Task 1's row count" — small data only; big data goes through tables, not task values. ADF translation: pipeline parameters and variables — same idea, lighter syntax.

**Visual suggestion**
Data-flow sketch: job parameter box → arrows into two task boxes → widget icons inside notebooks; a thin separate arrow labeled "taskValues" between the tasks.

**Exam relevance**
Parameterization underlies job-configuration questions and is the bridge to bundle variables (Slide 12).

**Common misconception**
Confusing job parameters (configuration, set at job level) with task values (runtime data passed between tasks).

---

### Slide 7: Monitoring — Run History, Baselines, and the Matrix

**Key bullets**
- Every run recorded: status, duration, trigger source, per-task timings — the **run history**
- Matrix view: runs × tasks grid — spot *which task* degraded or fails repeatedly
- Trend reading: compare current duration to historical baseline; growing duration = early warning (data growth? skew? upstream slowness?)
- Notifications on start/success/failure/duration-threshold; job/task statuses: queued, running, succeeded, failed, skipped, upstream-failed

**Speaker notes**
Two Domain 6 objectives live here, verbatim: identifying performance *trends* via run history, and monitoring pipeline health via statuses and the DAG view. Teach the diagnostic flow: notification → run history → matrix (which task?) → task run page (error/logs) → Spark UI if it's a performance issue (Week 4). The `upstream-failed` status matters: the task didn't fail — its dependency did; fix upstream, repair downstream.

**Visual suggestion**
Stylized matrix-view screenshot: green grid with one column going yellow→red over recent runs, annotated "this task, growing duration."

**Exam relevance**
Verbatim Domain 6: "Identify trends in job performance using the Lakeflow Jobs run history view…" and "Use the Lakeflow Jobs UI to monitor pipeline health…".

**Common misconception**
"A failed run must be rerun from scratch." Hold that thought — next slide.

---

### Slide 8: Repair and Rerun — Don't Recompute What Succeeded

**Key bullets**
- **Repair run:** rerun only the **failed and skipped/upstream-failed** tasks of a job run; successful tasks are not re-executed
- Fix the cause first (code, data, config) — then repair; parameters can be adjusted for the repair
- Saves compute AND avoids re-processing side effects of completed tasks
- Idempotent task design (Weeks 2's theme) is what makes repair *safe*

**Speaker notes**
This is a named exam objective ("Deploy a workflow, repair, and rerun a task in case of failure" in the current guide; failure handling persists in the new one). Walk the scenario: 5-task DAG, task 4 fails at 3am; tasks 1–3 took two hours. Repair reruns 4 and 5 only. Connect to Week 2 explicitly: our COPY INTO and MERGE tasks can be repaired fearlessly *because* they're idempotent — sloppy INSERT pipelines are why some teams fear repair. The demo makes this concrete with the `simulate_failure` switch.

**Visual suggestion**
DAG with tasks 1–3 green (locked, "not rerun"), task 4 red → arrow to "Repair run" → tasks 4–5 rerunning blue.

**Exam relevance**
Direct objective; also the practical glue between Domains 4 and 6.

**Common misconception**
Repair re-executes the whole job. It specifically does not — that's "Run now," and choosing between them is a plausible exam distractor pair.

---

### Slide 9: Serverless Jobs — Hands-Off Compute

**Key bullets**
- Serverless jobs compute: no cluster sizing, instant-ish start, auto-scaling/auto-optimized, Databricks-managed
- Named exam objective: "Use serverless for a hands-off, auto-optimized compute managed by Databricks"
- Classic alternative (concept): job clusters — created per run, terminated after; you own the sizing
- Cost mental model: serverless bills for what the run uses; classic bills for what you provisioned

**Speaker notes**
Free Edition forces serverless — for once, the constraint is the exam answer. The selection heuristic: teams without cluster-tuning expertise, spiky/unpredictable workloads, fast iteration → serverless; very steady high-volume workloads with tuned configs → classic job clusters can still win on cost (Week 4 nuance). Call back to Slide 4 of Week 1 — same decision tree, now with a "who manages it" row.

**Visual suggestion**
Two dials: "Control" (classic high, serverless low) vs. "Operational effort" (classic high, serverless near-zero).

**Exam relevance**
Verbatim Domain 4 objective; also feeds Domain 1 compute-selection questions.

**Common misconception**
"Serverless is always cheaper." It's always *simpler*; cost depends on workload shape — exam stems usually reward it for the hands-off property, not a blanket cost claim.

---

### Slide 10: Why CI/CD — From "It Works in My Notebook" to Engineering

**Key bullets**
- Problems: untracked changes, no review, manual copy-to-prod, config drift between environments
- The Databricks answer, two layers: **Git folders** (version control *in* the workspace) + **Declarative Automation Bundles** (deployable definitions of jobs/pipelines/code)
- Goal: same codebase, promoted dev → test → prod with environment-specific config
- New exam domain (10%) — four objectives, all covered in the next three slides

**Speaker notes**
Frame for data engineers, not app developers: the asset being shipped is a *pipeline* — code (notebooks) + orchestration (job definition) + config (schemas, schedules). Git folders version the code; bundles version *everything else too*. ADF/Synapse folks: this is their ARM-template + Git-integration story, but file-based and CLI-driven rather than portal-exported.

**Visual suggestion**
Conveyor belt: dev workspace → PR/review gate → test → prod, with a bundle box riding the belt containing notebook + job + config icons.

**Exam relevance**
Sets up all four Domain 5 objectives.

**Common misconception**
"CI/CD means just putting notebooks in Git." Code versioning is half the story — the job definitions and environment config are the other half (bundles).

---

### Slide 11: Git Folders — The Workspace Git Workflow

**Key bullets**
- Git folder = a cloned repo living in your workspace (formerly "Repos" — exam guide uses both names)
- In the UI you can: clone, **create/switch branches, commit & push, pull**, view diffs
- Pull requests: you push the branch, then **create the PR in the Git provider** (GitHub/GitLab/Azure DevOps) — the workspace links you there
- Typical flow: branch → edit notebooks → commit/push → PR → review/merge → prod folder pulls main

**Speaker notes**
Demo-adjacent slide; keep it procedural. The PR detail is the exam trap worth hammering: the *workspace UI* handles branch/commit/push, but the PR itself is created and merged in the provider. Walk the loop once on the slide, then again live in the demo. Auth note for class: connecting GitHub needs a token/OAuth — that's why it's an instructor demo, with learners optionally following if they prepped accounts. **Free Edition supports Git folders; the external account is the dependency.**

**Visual suggestion**
Circular workflow: branch → edit → commit → push → (provider icon) PR → merge → pull, with a dotted line marking the workspace/provider boundary.

**Exam relevance**
Verbatim Domain 5: "creating and switching between branches in Databricks Repos, committing and pushing changes, and creating pull requests using Databricks Git integration."

**Common misconception**
That PRs are created inside the Databricks UI. The workspace gets you to the provider; review/merge happen there.

---

### Slide 12: Declarative Automation Bundles — Pipelines as Code

**Key bullets**
- A bundle = a folder with **`databricks.yml`** + source files; declares jobs, pipelines, and other resources as YAML
- Key blocks: `bundle` (name), `resources` (the jobs/pipelines), `variables` (parameterized config), `targets` (dev/test/prod environments)
- **Variables + per-target overrides** = same code, different schema/warehouse/schedule per environment
- Formerly **Databricks Asset Bundles (DABs)** — exam says "Declarative Automation Bundles (formerly Databricks Asset Bundles)"

**Speaker notes**
Show the actual `cicd/databricks.yml` from the course repo (it mirrors today's demo job). Read it top to bottom: name → variable `target_schema` → the job with two tasks and a `depends_on` → two targets overriding the variable. That one file answers two exam objectives (structure; environment-specific config via variables/overrides). Note `mode: production` on prod targets. Don't go deeper than reading fluency — the associate exam tests structure recognition and the promotion story, not advanced bundle authoring.

**Visual suggestion**
The YAML file with four colored brackets labeling bundle / variables / resources / targets, and an arrow from each target to a workspace icon (dev, prod).

**Exam relevance**
Verbatim Domain 5: "Identify the structure of Asset Bundles" and "environment-specific configuration using Automation Bundle variables and overrides."

**Common misconception**
"A bundle is a zip of notebooks." It's a *declaration* — the YAML defines resources that the CLI materializes in a workspace; the same bundle produces different concrete jobs per target.

---

### Slide 13: The Bundle Lifecycle — validate, deploy, run

**Key bullets**
- Databricks CLI drives bundles: `databricks bundle validate` → `databricks bundle deploy -t dev` → `databricks bundle run -t dev brewmart_daily`
- `validate` checks syntax/refs; `deploy` creates/updates the resources in the target workspace; `run` executes a deployed job/pipeline
- Promotion = `deploy -t test`, then `-t prod` — no code edits, only target switch
- In CI (e.g., GitHub Actions): the same three verbs, run by a service principal on merge

**Speaker notes**
Three verbs, in order — make the room chant them: validate, deploy, run. The CI sentence matters for the exam objective ("manage … in automated CI/CD workflows"): a pipeline that runs `bundle deploy -t prod` on merge-to-main is the canonical answer shape. **Free Edition: the CLI works, but full multi-target practice needs more workspace freedom — labeled "Exam concept; demo/walkthrough; hands-on optional homework for the brave."** The demo shows the commands and output as a narrated walkthrough or screenshots.

**Visual suggestion**
Three-step pipeline: validate (✓ icon) → deploy (upload icon, branching to dev/test/prod) → run (play icon), with a GitHub Actions ribbon underneath.

**Exam relevance**
Verbatim Domain 5: "Understand the Databricks CLI to validate, deploy, and manage Declarative Automation Bundles … in automated CI/CD workflows."

**Common misconception**
That `deploy` runs the job. Deploy *places* it; `run` (or its trigger) executes it. Validate/deploy/run are distinct exam-testable steps.

---

### Slide 14: How Today Gets Tested

**Key bullets**
- Trigger selection: cadence words → schedule; "whenever files/data arrive" → file arrival / table update
- Failure handling: transient → retries; broken task → fix + **repair run** (only failed/downstream rerun)
- Task-type matching: SQL refresh → SQL task; BI freshness → dashboard task; declarative ETL → pipeline task
- CI/CD: PR location (provider!), bundle block names, the three CLI verbs, variables-per-target

**Speaker notes**
Model one question: "A job's task 3 of 6 failed at 2am due to a bad cast. The engineer fixed the notebook. What's the most efficient next step?" Eliminate "Run now" (recomputes 1–2), "clone the job" (nonsense), "delete the run" (nothing) → **Repair run**. Then a CI/CD one: "Where is the pull request created?" — provider, not workspace. Remind: distractors here love swapping deploy/run and schedule/file-arrival.

**Visual suggestion**
Two mock questions with elimination strikethroughs, same style as Weeks 1–2.

**Exam relevance**
Question-style rehearsal for Domains 4–6.

**Common misconception**
That CI/CD questions require deep DevOps experience — at associate level they're structure-and-vocabulary questions; the slide-13 verbs and slide-12 blocks cover most of it.

---

### Slide 15: Wrap-Up — Your Pipeline Is Now a Product

**Key bullets**
- BrewMart's pipeline: scheduled, parameterized, repairable, versioned, promotable
- You now own: a 2-task job with a schedule, a failure you repaired yourself, and reading fluency in `databricks.yml`
- Homework: trigger docs + bundle skeleton annotation + (optional) CLI try-out
- Next week: governance (GRANTs, masking, ABAC) + optimization (Spark UI, Liquid Clustering) + exam strategy — the last new content before the capstone

**Speaker notes**
Close the loop: Week 1 objects → Week 2 pipeline → Week 3 production unit. Ask each learner to name one thing their old stack made harder than what they did today (and one thing it made easier — honesty builds trust). Preview Week 4 as "the two domains people under-study, plus how to take this exam."

**Visual suggestion**
The course-progress strip; Weeks 1–3 stamped done; Week 4 highlighted with lock + speedometer icons.

**Exam relevance**
Consolidation.

**Common misconception**
—

---

## 4. Instructor Demo

### Demo: BrewMart Goes to Production — A Job, a Failure, a Repair, and a Bundle

**Goal**
Build a real two-task Lakeflow Job live (parameters → widgets, dependency, schedule), force a failure with a parameter switch, fix it, and use **Repair run** to rerun only the failed task. Then connect the same assets to CI/CD: a Git-folder round-trip and a narrated `databricks.yml` walkthrough.

**Setup**
- Free Edition; the two course notebooks imported to your workspace home: `week3_01_ingest_bronze.py`, `week3_02_build_silver.py`
- Your `workspace.week1_demo` schema from prior weeks (the notebooks take `target_schema` as a parameter — point them at `week1_demo`)
- `landing/sales_incoming/` still contains day2+day3 files (COPY INTO will load 0 new rows — *say that out loud; it's the idempotency victory lap*)
- For the Git segment: a GitHub account + a scratch repo + a configured token (set up before class)
- `cicd/databricks.yml` from the course repo open in a side tab

> **Free Edition notes:** Jobs, schedules, parameters, run history, and repair all work on serverless jobs compute. Git folders work with an external provider account. Bundle CLI deployment is **walkthrough/optional** — the exam objective is structure + verbs, fully teachable without a live deploy.

**Part A — Build and run the job (UI, ~12 min)**

Step-by-step instructor script:

1. **Jobs & Pipelines → Create → Job.** Name it `brewmart_daily_<you>`. "One job, soon two tasks, one DAG."
2. **Task 1:** key `ingest_bronze`, type **Notebook**, path → `week3_01_ingest_bronze`, compute → serverless. "Notice what I'm NOT doing: sizing a cluster."
3. **Job parameters** (job level): add `target_schema = week1_demo`, `simulate_failure = false`. "Parameters live on the job; the notebook catches them as widgets — open the notebook and show `dbutils.widgets.get`."
4. **Task 2:** key `build_silver`, type Notebook, path → `week3_02_build_silver`, **Depends on → ingest_bronze**. Point at the DAG canvas: "That arrow is the orchestration."
5. **Run now.** While it runs, open the run page: statuses flowing queued → running → succeeded; click into Task 1's output — `bronze_rows=23`, COPY INTO loaded 0 new files. "Rerunnable by design — Week 2 paying rent."
6. **Schedule:** Add trigger → Scheduled → daily 06:00 → **set it to Paused**. "Real schedule, zero 6am surprises for my demo account. Note the other trigger types in this menu — file arrival is right there; remember the decision rule."
7. **Retries:** on Task 1, set retries = 2 with a short interval. "Transient-failure insurance. What it won't fix: an actual bug — watch."

**Part B — Failure and repair (~8 min)**

8. Edit job parameter `simulate_failure = true`. **Run now.** Task 1 fails (the notebook raises); Task 2 shows **upstream-failed** (skipped). Open the error: the exception message tells us what to do — "in real life this is your stack trace."
9. Read the run history list: one green run, one red run. Matrix view: the red column is Task 1. "Which task, which run, how long — this view answers the exam's monitoring objectives."
10. "The fix": set `simulate_failure = false` (job parameter — and note you can also override parameters *just for the repair*). On the failed run page → **Repair run**. Watch: only `ingest_bronze` and then `build_silver` execute. "Repair reruns failed and downstream tasks — never the already-green ones. With a 2-hour upstream task, this feature is your weekend."

**Part C — Git folder round-trip (~5 min)**

11. Workspace → Git folders → clone your scratch repo. Create branch `week3-demo`. Move/copy a notebook in, **Commit & push** with a message. Show the diff view first: "review-ready changes."
12. Click "Create pull request" → lands in GitHub. "The workspace took me to the provider — the PR is created HERE. That boundary is an exam question." Merge in GitHub, pull `main` in the workspace. Round trip complete.

**Part D — Bundle walkthrough (~5 min, narrated; CLI optional)**

13. Open `cicd/databricks.yml` side by side with the job you just built by hand. "Everything I clicked is declared here: tasks, the depends_on edge, parameters, the schedule. The UI job and the YAML job are the same animal — one is clickable, one is shippable."
14. Read the four blocks aloud (bundle / variables / resources / targets). Highlight: `${var.target_schema}` in the task parameters; `dev` writes to `lab1_dev`, `prod` to `sales_prod`. "Promotion = changing `-t`, not editing code."
15. Show (terminal or screenshots): `databricks bundle validate` ✓ → `databricks bundle deploy -t dev` → `databricks bundle run -t dev brewmart_daily`. "Validate, deploy, run. In CI, GitHub Actions runs these same verbs on merge. That sentence is worth several exam points."

**Expected Results**
- Part A: successful run; DAG with 2 green tasks; Task 1 exit value `bronze_rows=23`; paused daily schedule visible on the job
- Part B: red run with Task 1 `Failed`, Task 2 `Upstream failed`; after repair — repair run shows only the two tasks executing, ending green; run history shows run → failed run → repaired run
- Part C: branch, commit, push visible in GitHub; PR created in provider; main pulled back clean
- Part D: validate output clean; (if run live) a `[dev]`-prefixed job appears in Jobs & Pipelines

**Talking points (thread through)**
- Parameters→widgets is one contract; taskValues is the other (mention, don't demo-deep)
- "Paused schedule" is a pro habit for demos AND for deploying ahead of go-live
- Idempotent tasks are what make retries and repairs *safe* — Week 2's theme is Week 3's foundation
- The YAML mirrors the UI exactly — learn one, you've learned both

**Troubleshooting**
| Problem | Fix |
| --- | --- |
| Notebook task can't find the notebook | Imported into a different folder — re-browse the path in the task config; avoid renaming after wiring. |
| `PERMISSION_DENIED` on COPY INTO inside the job | `target_schema` parameter doesn't match your real schema — check the job parameter value, not the notebook default. |
| Task 1 succeeds but loads 0 rows and Task 2 "looks wrong" | Correct behavior — files already ingested (idempotency). To show fresh loads, upload a copy of day3 with a new filename into `sales_incoming/` first. |
| Repair option greyed out / missing | You're on the job page, not the *failed run's* page — open the specific run, then Repair run. |
| Schedule fires during class | You skipped the Pause step. Pause the trigger; delete stray runs for cleanliness. |
| Git: push rejected / auth fails | Token expired or repo permissions — re-link credentials in Settings → Linked accounts; have screenshots as fallback. |
| CLI auth friction live on stage | Don't debug live — switch to the prepared screenshots; the objective is the three verbs, not your terminal. |
| Serverless job slow to start first run | Cold start; narrate it once ("serverless trade-off: zero management, occasional warmup") — it's a talking point, not a bug. |

---

## 5. Hands-On Lab

### Lab: Schedule It, Break It, Repair It

**Scenario**
BrewMart's ops lead is done with "run the notebook when you remember." Your Week 2 pipeline becomes a scheduled, parameterized, monitored job — and because failures are a *when* not an *if*, you'll cause one on purpose and recover like a professional.

**Business Problem**
Convert the manual bronze→silver pipeline into a Lakeflow Job that runs on a schedule, survives transient errors, fails loudly when broken, and recovers without recomputing successful work.

**Tasks**
1. Import the two course notebooks into your workspace (if not done pre-class)
2. Create job `brewmart_daily_<yourname>` with Task 1 `ingest_bronze` (notebook task, serverless) and job parameters `target_schema = lab1_<yourname>`, `simulate_failure = false`
3. Add Task 2 `build_silver` depending on Task 1; run the job; verify both tasks green and inspect Task 1's exit value
4. Add a **paused** daily schedule at 06:00 and set retries = 2 on Task 1
5. Set `simulate_failure = true`, run, and observe: Task 1 fails (after retries), Task 2 goes upstream-failed
6. Set `simulate_failure = false` and use **Repair run** on the failed run; confirm only the failed path re-executed
7. In the run history, compare the durations of your three runs and find the matrix view

**Starter Code**
*(No SQL starter — the work is job configuration. Notebook code is provided in `notebooks/week3_01_ingest_bronze.py` and `notebooks/week3_02_build_silver.py`. The only edit learners might make:)*

```python
# Optional: in either notebook, change the widget default to your schema
dbutils.widgets.text("target_schema", "lab1_<yourname>")
```

**Expected Solution**
*(Configuration checklist — the lab "solution" is a correctly wired job:)*

```text
Job: brewmart_daily_<yourname>
├─ Job parameters: target_schema=lab1_<yourname>, simulate_failure=false
├─ Task ingest_bronze  → notebook week3_01_ingest_bronze, serverless, retries=2
├─ Task build_silver   → notebook week3_02_build_silver, depends_on=[ingest_bronze]
├─ Trigger: Scheduled daily 06:00 — PAUSED
└─ Run history: success → failure (simulated) → repair (green)
```

**Validation Checks**

```text
□ Run 1: both tasks Succeeded; Task 1 output shows bronze_rows=23
  (0 new files loaded — expected: COPY INTO idempotency)
□ Job page shows the paused 06:00 daily trigger
□ Run 2: ingest_bronze = Failed (with 2 retry attempts visible),
  build_silver = Upstream failed
□ Run 2 after repair: ONLY ingest_bronze + build_silver re-executed;
  run ends Succeeded
□ Run history lists 3 entries with statuses Success / Failed / Success(repaired)
```

```sql
-- And the data proof (run in SQL editor):
SELECT COUNT(*) FROM workspace.lab1_<yourname>.sales_silver;  -- 22 (or 25 post-corrections)
DESCRIBE HISTORY workspace.lab1_<yourname>.sales_silver;
-- newest version written by the job's repair run — note the job info in the history!
```

**Stretch Task**
Add a third task `data_quality_gate`: a **SQL task** (or small notebook) that runs `SELECT CASE WHEN COUNT(*) = 0 THEN raise_error('empty silver!') END FROM sales_silver`, depending on `build_silver`. Then sketch (markdown cell, no build needed) how you'd convert the whole job to a **file arrival trigger** on `sales_incoming/` — what changes, what stays?

**Instructor Notes**
- The #1 stall: job parameter `target_schema` left at someone else's default → permission or not-found errors. It's also the best teachable moment — parameters over hardcoding
- Watch for learners putting `simulate_failure=true` as the *widget default* instead of the job parameter — then repair "doesn't fix it." Exactly the job-parameter-vs-notebook-default lesson
- Retries make the simulated failure take ~2 extra minutes to finally fail — warn them it's not hung; watch the retry counter (this is also why retries don't fix bugs)
- Some learners will try Repair from the job page and report it missing — navigate them to the failed *run* page
- Free Edition concurrency caps: if many learners run simultaneously and queue, narrate it — queued is a status they should recognize
- Fast finishers → stretch task; the file-arrival sketch makes a great 60-second debrief

---

## 6. In-Class Activity

### Activity: "Orchestration Triage" — Decision Cards

**Time needed:** 10 minutes (6 min pairs + 4 min debrief)

**Setup**
Six scenario cards. Fixed options menu: **scheduled trigger · file arrival trigger · table update trigger · task retries · repair run · if/else task · for-each task · SQL task · dashboard task**. Pick exactly one per card.

**Instructions**
"Find the forcing constraint, pick one mechanism, one-sentence justification. Three minutes of arguing per card is the point."

**Scenario cards**
1. A supplier SFTP-drops files into your landing volume at unpredictable times between 01:00–05:00; the current hourly polling job mostly finds nothing
2. Task 4 of 7 failed overnight because of a typo you've now fixed; tasks 1–3 took 90 minutes — what's your *next click*?
3. The same cleansing logic must run for each of 11 country datasets, ideally several in parallel
4. A flaky external API fails roughly one call in twenty, succeeding on the next attempt
5. After the gold table refreshes nightly, the executive dashboard must show fresh numbers before 07:00 — *without* converting the BI tool to query live
6. On the first of the month run a full rebuild; every other day run the incremental path

**Learner deliverable**
Six picks + forcing constraint, posted to chat.

**Debrief answers**
1. **File arrival trigger** — data-driven beats polling: less compute, lower latency
2. **Repair run** — fix applied; only failed + downstream rerun; 90 minutes preserved
3. **For-each task** — iterate a list with controlled concurrency
4. **Task retries** — transient failure is retries' exact job description
5. **Dashboard task** — BI refresh as a first-class DAG node depending on the gold load
6. **If/else task** — boolean branch on date logic; two paths, one job

**Teaching points**
- Cards 1 vs. 4 vs. 2 sort the failure/latency space: *event-driven trigger* vs. *transient-retry* vs. *fix-and-repair* — the exam mixes these as distractors for each other
- Card 5 exists because almost nobody knows dashboard tasks are real — the exam names them
- If pairs argue "retries" on card 2: retries already happened and couldn't fix a typo — deterministic bugs need humans + repair

---

## 7. Live Knowledge Check

The Markdown Mash quiz for this week is kept in the instructor-only private materials and launched live during the session.

Instructor copy: `instructor_private/markdown_mash/Week3_Quiz.md`. This path is intentionally ignored by git so learners do not see the questions or answer key ahead of time.

## 8. Exam Tips for This Week

**What the exam is likely to test**
- Trigger selection from scenario wording (cadence vs. data-arrival vs. table-commit)
- Repair run vs. run now vs. retries — three mechanisms, constantly cross-used as distractors
- Task-type matching (notebook / SQL / dashboard / pipeline) and DAG dependency reasoning
- Parameters → widgets contract; task values for inter-task data
- Bundle structure (bundle/variables/resources/targets), variables + overrides, the three CLI verbs
- Git folders: what's in the workspace UI vs. what's in the provider
- Run history as the trend-diagnosis tool; serverless as the hands-off compute answer

**Keywords to recognize instantly**
`task_key`, `depends_on`, `DAG`, `run-if`, `if/else condition`, `for-each`, `file arrival`, `table update`, `cron`, `repair run`, `upstream failed`, `matrix view`, `dbutils.widgets.get`, `taskValues`, `databricks.yml`, `targets`, `variables`, `bundle validate/deploy/run`, `Git folder`, `pull request`, `serverless`

**Common traps**
- "Repair run re-executes the whole job" — it doesn't; that's Run now
- "Retries will eventually fix it" — not for deterministic bugs
- "A 1-minute cron is event-driven" — it's expensive polling; file arrival is the answer the exam wants
- "PRs are created in the Databricks UI" — provider-side
- "bundle deploy runs the job" — deploy places, run executes
- Old names in options (Workflows, DABs, Repos) used as bait next to current names — both may appear; match what the question's stem uses

**How to eliminate wrong answers**
Classify the failure or need first: transient (→ retries), deterministic-but-fixed (→ repair), data-availability (→ data-driven trigger), time-SLA (→ schedule). For CI/CD: locate the verb's stage — checking (validate), placing (deploy), executing (run). Any option that mixes stages is wrong.

**Memorize**
The three CLI verbs in order; the four bundle blocks; the four exam-named task types; the three trigger types in the objective ("scheduled, file arrival, table update"); repair-run semantics; parameters→widgets.

**Understand conceptually**
Why idempotent tasks make retries/repair safe; why event-driven triggers beat polling; why environment config belongs in target overrides rather than code; why a duration *trend* needs run history while a single slow run needs the Spark UI.

---

## 9. Homework / Self-Study

**Databricks documentation to read (~45 min)**
- Lakeflow Jobs overview + "Configure and edit tasks" (skim the task-type list)
- Trigger types for Lakeflow Jobs (scheduled / file arrival / table update / continuous)
- Repair a job run; Job run statuses
- Git folders (Databricks Git integration) — the end-to-end workflow page
- What are Declarative Automation Bundles? + bundle configuration (`databricks.yml`) reference — read the *structure*, skip advanced mappings
- Exam-guide-recommended Academy courses if available to you: *Deploy Workloads with Lakeflow Jobs*, *DevOps Essentials for Data Engineering*

**Optional notebook/CLI practice (~25 min)**
1. Rebuild today's job from scratch without notes — target: under 10 minutes
2. Add the stretch-task SQL quality gate as a third task
3. Brave-mode (optional): install the Databricks CLI locally, `databricks auth login` to your Free Edition workspace, and run `databricks bundle validate` against the course's `cicd/databricks.yml` (fix the notebook paths first)
4. Read your job's JSON: job page → kebab menu → View JSON — find `task_key`, `depends_on`, and the schedule; it's the bundle's `resources:` block wearing a different coat

**Review questions**
1. Task 3 of 8 failed; you fixed a data file, not code. Repair run or Run now — and why might parameters matter for the repair?
2. Name the three trigger types in the exam objective and one scenario keyword for each.
3. What's the difference between a job parameter and a task value? Give one use for each.
4. In `databricks.yml`, where does "prod writes to a different schema" live?

**Mini checklist before Week 4**
- [ ] My job exists with 3 runs in history (success / failed / repaired)
- [ ] I can recite: validate → deploy → run, and the four bundle blocks
- [ ] I know where a PR is created
- [ ] My `sales_silver` is intact — Week 4's governance lab GRANTs and masks it

---

## 10. Instructor Preparation Checklist

**Before class (day before)**
- [ ] Import both task notebooks into your workspace; run each manually end-to-end against `week1_demo`
- [ ] Build the demo job once in rehearsal, then **delete it** so you build it fresh and fast live (or keep it hidden as backup)
- [ ] Rehearse the failure→repair sequence including the retries delay — time it so you talk through the retry attempts rather than waiting silently
- [ ] Git: confirm token works, scratch repo exists, you can clone/branch/push/PR in under 4 minutes
- [ ] CLI: either confirm `bundle validate` works against your workspace or prepare the screenshot deck (validate ✓, deploy output, run output)
- [ ] Check current Free Edition trigger menu: confirm which trigger types are visible (file arrival on volumes?) and adjust Slide 5's "verify availability" note to what you saw
- [ ] Remind learners (day before): import the two notebooks; optional GitHub account for follow-along

**Workspace objects needed**
- `week1_demo` schema with bronze/silver tables and `landing/sales_incoming/` files (from Weeks 1–2)
- The two imported task notebooks
- A spare copy of `week2_sales_day3.csv` renamed (e.g., `day3_copy.csv`) — your "fresh file" if you want COPY INTO to load >0 rows live
- Scratch GitHub repo + linked credentials
- `cicd/databricks.yml` open in a side tab; screenshot deck for CLI

**Demo rehearsal**
- [ ] Time the four parts: A ≈ 12, B ≈ 8, C ≈ 5, D ≈ 5 — total 30; the lab can absorb 5 minutes of overrun, the quiz cannot
- [ ] Part C is the most failure-prone live (auth) — do it right after a successful rehearsal login, and have the screenshot path ready
- [ ] Decide your Part D mode in advance: live terminal only if rehearsal was clean *today*; otherwise screenshots — no live debugging
- [ ] Screenshot kit: run page with DAG, matrix view with the red column, Repair run dialog, repaired run, GitHub PR page, CLI outputs

**Backup plans**
- **Jobs UI changed/moved (Free Edition iterates fast):** your rehearsal is your map; narrate differences calmly — the *concepts* (task, dependency, trigger, repair) are stable
- **Git segment blocked (auth/network):** teach from screenshots; learners lose nothing hands-on (it was instructor-demo anyway)
- **Repair flow misbehaves:** fall back to demonstrating Run now vs. repair conceptually on the failed-run page, and show the repair dialog screenshot
- **Severe concurrency queueing during lab:** have learners pair up on one job per pair; queued runs become a monitoring teaching moment
- **Total outage:** slides + activity + quiz + DAG-design-on-paper exercise (design the BrewMart job incl. triggers and retries in markdown); job lab moves to homework with the checklist as proof

---

*Next: Week 4 — Governance and Security (Unity Catalog permissions, masking, ABAC) + Troubleshooting and Optimization (Spark UI, Liquid Clustering, predictive optimization) + exam strategy.*
