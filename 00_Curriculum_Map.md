# Curriculum Map — Databricks Certified Data Engineer Associate

**Exam version:** May 4, 2026 guide (current live version, verified June 16, 2026)
**Source of truth:** [Official Exam Guide PDF](https://www.databricks.com/sites/default/files/2026-05/databricks-certified-data-engineer-associate-exam-guide-may-2026-000.pdf) | [Certification page](https://www.databricks.com/learn/certification/data-engineer-associate)

## Verified Exam Facts

- 45 scored multiple-choice questions, 90 minutes, $200, online or test center
- Code shown in **SQL when possible, Python otherwise** — but the new outline explicitly tests PySpark DataFrame operations
- 7 domains with official weights: Platform 6%, Ingestion 21%, Transformation 22%, Jobs 16%, CI/CD 10%, Troubleshooting 10%, Governance 15%
- Recommended self-paced prep: Data Ingestion with Lakeflow Connect; Deploy Workloads with Lakeflow Jobs; Build Data Pipelines with Lakeflow Spark Declarative Pipelines; Data Management and Governance with Unity Catalog; DevOps Essentials for Data Engineering; Data Interoperability with Unity Catalog

## Official Domain Weights

The May 2026 exam guide publishes the following domain weights:

| Exam Domain | Official Weight |
| ----------- | --------------- |
| 1. Databricks Intelligence Platform | 6% |
| 2. Data Ingestion and Loading | 21% |
| 3. Data Transformation and Modeling | 22% |
| 4. Working with Lakeflow Jobs | 16% |
| 5. Implementing CI/CD | 10% |
| 6. Troubleshooting, Monitoring, and Optimization | 10% |
| 7. Governance and Security | 15% |

## Domain → Week Mapping

| Exam Domain | Official Weight | Covered In Week | Notes |
| ----------- | --------------- | --------------- | ----- |
| 1. Databricks Intelligence Platform | 6% | Week 1 | Lakehouse architecture, Delta Lake, Unity Catalog hierarchy, compute selection (serverless vs. classic, SQL warehouse vs. all-purpose). Bridge from learners' intro training. Fully hands-on in Free Edition. |
| 2. Data Ingestion and Loading | 21% | Week 2 | COPY INTO and Auto Loader hands-on via managed volumes. Lakeflow Connect standard/managed connectors and JDBC/REST patterns = concept + decision-framework only ("which ingestion method?" questions). Schema enforcement/evolution and JSON/nested data are testable. |
| 3. Data Transformation and Modeling | 22% | Weeks 1–2 | Week 1: DDL/DML, CTAS, managed vs. external, views vs. materialized views vs. streaming tables (gold objects), medallion overview. Week 2: cleaning nulls, casting, joins (incl. broadcast), union vs. union all, explode, dedup, aggregations, MERGE INTO, data quality checks, basic Spark tuning params. PySpark needed here, not just SQL. |
| 4. Working with Lakeflow Jobs | 16% | Week 3 | Jobs, tasks, DAGs, task types (notebook/SQL/dashboard/pipeline), retries, conditional/branching/looping control flow, trigger types (scheduled, file arrival, table update), time-based vs. data-driven. Hands-on in Free Edition for basic jobs; advanced triggers concept-labeled. |
| 5. Implementing CI/CD | 10% | Week 3 | Git folders (branch/commit/push/PR workflow), Declarative Automation Bundles (formerly Databricks Asset Bundles): structure, variables/overrides, dev→test→prod promotion, Databricks CLI validate/deploy. Mostly demo + concept in Free Edition — label as "Exam concept; full hands-on needs CLI/external Git setup." NEW domain — not in older prep material. |
| 6. Troubleshooting, Monitoring, and Optimization | 10% | Weeks 3–4 | Week 3: run history, Jobs UI monitoring, repair-and-rerun, failure diagnosis. Week 4: Spark UI (skew, shuffle, spill), Liquid Clustering, predictive optimization (concept — Premium feature), cluster startup/library/OOM diagnosis. |
| 7. Governance and Security | 15% | Week 4 (seeded Week 1) | Managed vs. external tables (incl. conversion), GRANT/REVOKE/DENY on the securable hierarchy, principals incl. service principals, row-level security and column masking, ABAC policies (concept), Delta Sharing, lineage, audit logs, Lakehouse Federation. Limited admin hands-on in Free Edition — syntax-level demos + scenario labs. |
| All domains | 100% | Week 5 (optional) | Capstone end-to-end pipeline + full 45-question timed mock weighted to domain importance + remediation by domain. If running 4 weeks only: schedule the instructor-controlled mock event after Week 4. |

## Key Differences vs. Your Draft Structure

1. **CI/CD is now an explicit exam domain (10%)** — added to Week 3. Your draft didn't include it.
2. **Z-order/partitioning de-emphasized** — the new guide names **Liquid Clustering and predictive optimization** instead. Teach partitioning only as legacy contrast.
3. **More PySpark than older exam versions** — DataFrame joins, aggregations, dedup, and tuning parameters are explicitly listed. Course stays SQL-first but Week 2 must include real PySpark.
4. **Current terminology required:** Lakeflow Jobs (not "Workflows"), Lakeflow Connect, Lakeflow Spark Declarative Pipelines (not "DLT"), Declarative Automation Bundles (formerly DABs), Git folders (not "Repos" — though the guide itself still says "Databricks Repos" in the CI/CD section, so teach both names).
5. **Delta Sharing, lineage, audit logs, Lakehouse Federation** appear in the *current* (pre-May-2026) guide's governance section and remain fair game conceptually — keep light coverage in Week 4.

## Free Edition Feasibility Tiers

| Tier | Topics |
| ---- | ------ |
| Fully hands-on | Notebooks, SQL, PySpark, managed tables/volumes, Delta, medallion transforms, MERGE, views/MVs, basic Jobs, run history |
| Conditional hands-on | COPY INTO, Auto Loader, Lakeflow Spark Declarative Pipelines, schedules, Git folders, simple GRANTs |
| Concept/demo only | Lakeflow Connect managed connectors, external tables/locations, ABAC, row filters/column masks (admin), predictive optimization, multi-env bundle deployment, Delta Sharing admin |
