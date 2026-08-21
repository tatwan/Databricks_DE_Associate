# Exam Domain 5 — CI/CD & Declarative Automation Bundles (~10%)
# Score 100

## Q1: In the Git-folders workflow, where is a pull request **created and merged**?
- [ ] In the Databricks workspace UI
- [ ] On the job's run page
- [x] In the Git provider (GitHub, GitLab, etc.)
- [ ] Inside the bundle's `databricks.yml` resource file
::time=45

## Q2: Which operations does the **workspace** handle in the Git loop?
- [ ] Approving and completing the code review
- [ ] Creating and merging the pull request itself
- [x] Branch, commit, and push (with a diff view)
- [ ] Tagging the final release in the provider
::time=45

## Q3: The correct order of bundle CLI verbs is…
- [ ] `deploy → validate → run`
- [ ] `run → deploy → validate`
- [ ] `validate → run → deploy`
- [x] `validate → deploy → run`
::time=45

## Q4: `databricks bundle deploy -t dev` does what?
- [ ] Executes the deployed job right away
- [x] Places the resources in the target workspace
- [ ] Checks syntax and references only
- [ ] Creates the pull request in the provider
::time=45

## Q5: `databricks bundle validate` does what?
- [x] Checks syntax and references — nothing changes
- [ ] Deploys the resources to the prod target
- [ ] Runs the deployed job from end to end
- [ ] Merges the feature branch into the main branch
::time=45

## Q6: Which set contains valid top-level mappings commonly used in `databricks.yml`?
- [x] `bundle`, `variables`, `resources`, `targets`
- [ ] `jobs`, `tasks`, `clusters`, `secrets`
- [ ] `dev`, `test`, `stage`, `prod`
- [ ] `name`, `owner`, `schedule`, `notebook`
::time=45

## Q7: How should dev and prod be represented in a well-written bundle?
- [ ] Each environment keeps its own copy of the notebooks
- [ ] Prod uses a completely different YAML file
- [ ] They must be deployed by hand-editing code
- [x] Target overrides with one shared codebase
::time=45

## Q8: "Promotion" from dev to prod means…
- [ ] Copy-pasting notebooks into a prod folder
- [x] Changing the `-t` target, never editing code
- [ ] Rewriting the job by hand in the UI
- [ ] Emailing the built artifact to ops
::time=45

## Q9: A CI pipeline runs on merge to main. The correct end-state action is…
- [ ] It runs `bundle run` before it ever deploys
- [ ] It opens the pull request in the workspace UI
- [x] `bundle deploy -t prod` via a service principal
- [ ] It restarts the cluster by hand after the merge
::time=45

## Q10: Which old-name → current-name mapping is correct?
- [x] Workflows → Lakeflow Jobs; Asset Bundles → Declarative Automation Bundles; Repos → Git folders
- [ ] Workflows → Git folders; Asset Bundles → Lakeflow Connect; Repos → SQL warehouses
- [ ] Workflows → Unity Catalog; Asset Bundles → Delta Sharing; Repos → Lakeflow Jobs
- [ ] Workflows → Auto Loader; Asset Bundles → notebooks; Repos → pipelines
::time=45

## Q11: What does a bundle target with `mode: production` do?
- [ ] It disables retries on every task
- [ ] It deletes the dev target automatically
- [ ] It runs the job immediately after every deploy
- [x] Production-mode deployment validations
::time=45

## Q12: Which pairing correctly separates source control from deployable workspace configuration?
- [ ] Notebooks together with dashboards
- [x] Git folders for source; bundles for deployable resources
- [ ] Compute clusters together with SQL warehouses and pools
- [ ] Catalogs together with their schemas
::time=45
