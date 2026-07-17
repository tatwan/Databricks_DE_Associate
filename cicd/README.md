# `cicd/` — the Week 3 Declarative Automation Bundle

This folder holds one file, **`databricks.yml`** — a working teaching example of a **Declarative Automation Bundle** (formerly *Databricks Asset Bundles*, "DABs"). It is used in **Week 3, slides 10–13** and referenced in the CI/CD portion of the exam prep. It is a read-and-discuss artifact for class; deploying it is an optional stretch, not a lab requirement.

## What the file contains, block by block

The exam tests recognition of exactly these four top-level blocks:

| Block | In our file | What it does |
|---|---|---|
| ① `bundle` | `name: brewmart_pipeline` | Names the bundle — the deployable unit |
| ② `variables` | `target_schema` (default `lab1_dev`) | Config knobs referenced as `${var.target_schema}` — environment-specific values without code changes |
| ③ `resources` | one job, `brewmart_daily` | The actual assets: two notebook tasks (`ingest_bronze` → `build_silver`), the `depends_on` DAG edge *as code*, base parameters, a daily trigger that is **PAUSED**, and failure emails |
| ④ `targets` | `dev` (default) and `prod` | The same bundle pointed at different environments — `dev` writes to `lab1_dev`, `prod` overrides `target_schema` to `sales_prod` and sets `mode: production` |

Details worth noticing when you read it in class:

- **The job here is the same job students build by hand in the Week 3 lab.** One clickable (Jobs UI), one shippable (this YAML) — same animal. The base parameters (`target_schema`, `simulate_failure`) are the very widgets the task notebooks read with `dbutils.widgets.get`.
- **`depends_on` in YAML** is the arrow students drew in the UI — the DAG serialized as code.
- **`pause_status: PAUSED`** is the "deploy ready, but must not run until go-live" exam pattern.
- **`mode: production`** hardens the prod target (stable deployment identity and paths, guards against deploy-time drift).
- **Promotion = changing `-t`**, never editing code: `deploy -t dev` vs `deploy -t prod` deploy identical logic with different variable overrides.

## How it is used — the CLI workflow

```bash
databricks bundle validate          # ① check syntax + that references resolve (changes nothing)
databricks bundle deploy -t dev     # ② PLACE the job in the dev workspace
databricks bundle run  -t dev brewmart_daily   # ③ EXECUTE the deployed job
```

Three verbs, always in that order. `deploy` places resources; `run` executes them — distinct steps, and the exam checks that you know which does which.

## How this works in the real world

In production organizations, this file is the center of the deployment story:

1. **The bundle lives in Git** next to the notebooks it deploys (exactly like this repo: `cicd/databricks.yml` referencing `../notebooks/...`). Code and orchestration are versioned together — a PR that changes a notebook can change its schedule in the same review.
2. **Developers work in dev**: branch → edit in a workspace Git folder → `bundle deploy -t dev` to their own environment → test → commit + push → open a PR *in the Git provider*.
3. **CI validates every PR**: a pipeline (GitHub Actions / Azure DevOps / GitLab CI) runs `databricks bundle validate` — cheap, catches broken references before review.
4. **Merge to main = automatic promotion**: the CI pipeline runs `databricks bundle deploy -t prod`, authenticated as a **service principal** (a machine identity — never a named person). Nobody clicks Deploy in the prod workspace; nobody edits prod notebooks by hand.
5. **Environment differences stay in `targets`**: prod's schema, schedule, permissions, and warehouse sizes are target overrides. The code never contains `if env == "prod"`.
6. **Rollback = redeploy a previous commit.** Because the workspace state is generated from Git, the repo is the source of truth — the workspace is a build artifact.

The sentence that compresses all of this (and is worth several exam points verbatim):

> **"A CI pipeline runs `databricks bundle deploy -t prod`, authenticated as a service principal, on every merge to main."**

## Trying it yourself (optional stretch)

Requires the [Databricks CLI](https://docs.databricks.com/dev-tools/cli/) v0.205+ authenticated to your workspace:

```bash
cd cicd/
databricks bundle validate                 # should pass as-is
databricks bundle deploy -t dev            # creates the (paused) job in your workspace
databricks bundle run -t dev brewmart_daily
```

Notes for the course environment: change `email_notifications` to your address; the notebook paths assume the repo's folder layout is preserved in the workspace; Free Edition students may not have CLI access — the file is fully teachable without deploying it.
