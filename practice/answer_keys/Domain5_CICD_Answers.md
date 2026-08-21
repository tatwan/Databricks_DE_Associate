# Domain 5 — CI/CD & Automation Bundles — Answer Key

**Q1 — C: In the Git provider.** Branch/commit/push are in the workspace, but the PR is created and merged in the provider (GitHub/GitLab/Azure DevOps). Not the run page or the YAML.

**Q2 — C: Branch, commit, and push (with a diff view).** The workspace handles these. Creating/merging the PR, review approval, and release tagging happen in the provider.

**Q3 — D: `validate → deploy → run`.** Validate checks configuration, deploy places resources, and run executes them. The other sequences attempt execution before a valid deployment.

**Q4 — B: Places the resources in the target workspace.** Deploy puts the jobs/pipelines into the target. Run executes, validate checks, and PRs are a provider action.

**Q5 — A: Checks syntax and references — nothing changes.** Validate is a dry check. It does not run, deploy, or merge.

**Q6 — A: `bundle`, `variables`, `resources`, `targets`.** These are valid, commonly used top-level mappings. They are not an exhaustive list: bundle configuration can also use mappings such as `include`, `artifacts`, `sync`, `permissions`, and `run_as`. The distractors mix nested keys, target names, or invented fields.

**Q7 — D: Targets override environment-specific settings while promoting the same source code.** A target can override variables, workspace paths, resource settings, permissions, and mode. The key principle is one versioned codebase, not separate notebook copies, separate hand-maintained YAML, or manual code edits.

**Q8 — B: Changing the `-t` target, never editing code.** Promotion switches the deploy target. Copy-pasting, rewriting in the UI, or emailing artifacts are anti-patterns.

**Q9 — C: `bundle deploy -t prod` as a service principal.** CI deploys to prod authenticated as a service principal on merge. Run doesn't precede deploy, the PR isn't in the workspace UI, and no manual cluster restart is needed.

**Q10 — A: Workflows → Lakeflow Jobs; Asset Bundles → Declarative Automation Bundles; Repos → Git folders.** These are the current product names used alongside the older names in some exam and documentation wording. The other mappings connect unrelated products.

**Q11 — D: Applies production validations.** Production mode validates production pipeline settings and can enforce the configured Git branch; Databricks also recommends a service principal for production deployment. It does not disable task retries, delete a target, or automatically run a job after deploy.

**Q12 — B: Git folders version source; bundles define and promote workspace resources.** Git handles code history and review, while bundles package jobs, pipelines, and environment configuration for repeatable deployment. The other pairings are runtime or governance components rather than the two CI/CD responsibilities.
