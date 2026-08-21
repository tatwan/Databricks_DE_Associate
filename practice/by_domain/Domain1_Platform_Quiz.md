# Exam Domain 1 — Databricks Intelligence Platform (~6%)
# Score 100

## Q1: Which components live in the **control plane**?
- [ ] Your data files and the executors that process them
- [x] The web UI, job scheduler, and Unity Catalog metastore
- [ ] Only the SQL warehouses you create
- [ ] Nothing — it all runs in the customer's cloud account
::time=45

## Q2: Where does **classic** compute run?
- [ ] In the Databricks-managed control plane
- [ ] On the user's local laptop
- [ ] Inside the Unity Catalog metastore
- [x] In the customer's own cloud account
::time=45

## Q3: Where does **serverless** compute run?
- [x] In a Databricks-managed environment
- [ ] In the customer's cloud account
- [ ] On on-premises hardware only
- [ ] Inside the Git provider
::time=45

## Q4: Which compute avoids paying for an interactive cluster that sits idle between **scheduled nightly runs**?
- [x] A per-run job cluster
- [ ] A shared interactive cluster
- [ ] An all-purpose cluster left running all day
- [ ] A dedicated GPU cluster kept warm overnight
::time=45

## Q5: Which compute is intended for **SQL, BI, and dashboards**?
- [ ] An all-purpose interactive cluster used for dev
- [x] A SQL warehouse (serverless / pro / classic)
- [ ] A job cluster created per run
- [ ] The notebook driver process
::time=45

## Q6: "Use serverless for hands-off, auto-optimized compute." Which claim is the exam **trap**?
- [ ] Databricks handles all provisioning, scaling, and optimization
- [ ] You are billed only for the compute a run uses
- [ ] Serverless is simpler to operate day to day
- [x] "Serverless is always cheaper"
::time=45

## Q7: What is the correct three-level object address in Unity Catalog?
- [ ] `schema.table.column`
- [ ] `workspace.database.table`
- [x] `catalog.schema.table`
- [ ] `metastore.catalog.schema`
::time=45

## Q8: An **all-purpose cluster** is best suited to…
- [ ] The cheapest option for scheduled production runs
- [ ] SQL-only dashboards and BI queries
- [x] Interactive development and shared notebook work
- [ ] Hosting the Unity Catalog metastore
::time=45

## Q9: Which identity does a production job or CI process use to authenticate?
- [x] A service principal
- [ ] A personal user account
- [ ] The metastore admin's password
- [ ] An anonymous access token
::time=45

## Q10: Which is a **table format**, and which is a **file format**?
- [ ] Parquet is the table format; Delta is a file format
- [ ] Both are file formats layered together
- [ ] Both are table formats with no underlying data files
- [x] Delta is a table format; Parquet is a file format
::time=45

## Q11: Which platform layer adds ACID transactions and version history to files in cloud object storage?
- [ ] A SQL warehouse
- [x] Delta Lake
- [ ] Unity Catalog
- [ ] A Git folder
::time=45

## Q12: On Databricks, which table format is the **default** (implicit `USING`)?
- [ ] Parquet
- [ ] Iceberg
- [x] Delta
- [ ] CSV
::time=45
