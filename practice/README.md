# Practice Quizzes — Databricks Certified Data Engineer Associate

Markdown Mash practice quizzes for exam preparation. Every question is single-answer multiple choice (a few true/false). The drills use a deliberately faster **45-second classroom timer**; the current exam has **45 scored multiple-choice questions in 90 minutes** and can also include unidentified unscored items. There is no hands-on coding environment, but learners must interpret SQL and PySpark snippets.

Two ways to practice: by **week** (mirrors the course delivery) or by **exam domain** (mirrors the May 2026 exam blueprint and weights).

## By Week

| Quiz | Focus |
|---|---|
| [Week 1 Overview](by_week/Week1_Overview_Quiz.md) | Lakehouse foundations, Delta, Unity Catalog, tables, views, volumes, time travel |
| [Week 2 Overview](by_week/Week2_Overview_Quiz.md) | Ingestion, Auto Loader, COPY INTO, bronze→silver, MERGE, JSON, dedup, constraints |
| [Week 3 Overview](by_week/Week3_Overview_Quiz.md) | Lakeflow Jobs, orchestration, CI/CD, declarative pipelines |
| [Week 4 Overview](by_week/Week4_Overview_Quiz.md) | Governance, security, troubleshooting, optimization |
| [Week 5 Cumulative Review](by_week/Week5_Cumulative_Review_Quiz.md) | Mixed-domain capstone review + exam strategy |

## By Exam Domain (May 2026 blueprint)

| Quiz | Weight |
|---|---|
| [Domain 1 — Databricks Intelligence Platform](by_domain/Domain1_Platform_Quiz.md) | ~6% |
| [Domain 2 — Data Ingestion & Loading](by_domain/Domain2_Ingestion_Quiz.md) | ~21% |
| [Domain 3 — Data Transformation & Modeling](by_domain/Domain3_Transformation_Quiz.md) | ~22% |
| [Domain 4 — Lakeflow Jobs / Orchestration](by_domain/Domain4_LakeflowJobs_Quiz.md) | ~16% |
| [Domain 5 — CI/CD & Automation Bundles](by_domain/Domain5_CICD_Quiz.md) | ~10% |
| [Domain 6 — Troubleshooting, Monitoring & Optimization](by_domain/Domain6_Troubleshooting_Quiz.md) | ~10% |
| [Domain 7 — Governance & Security](by_domain/Domain7_Governance_Quiz.md) | ~15% |

## Answer Keys & Explanations

Each quiz has a matching key in [`answer_keys/`](answer_keys/) with the correct choice **and why each distractor is wrong** — use it when reviewing results. Weekly: `Week1_Overview_Answers.md` … `Week5_Cumulative_Review_Answers.md`. Domain: `Domain1_Platform_Answers.md` … `Domain7_Governance_Answers.md`.

## Anti-bias note

Correct answers are distributed across A/B/C/D without a repeating rotation or long streaks. Options are kept to comparable length, and the correct choice is not systematically the longest. Do not coach students to guess by position or length; require them to name the rule that makes the answer correct.

The weekly and domain quizzes intentionally overlap. Use **one route for first attempts** and the other for delayed retrieval practice; taking both back-to-back will expose repeated concepts.

## Format notes (Markdown Mash)

- `# Title` then `# Score 100` at the top of each file.
- `## Qn:` per question; `- [x]` marks the correct answer, `- [ ]` the distractors.
- `::time=45` sets the per-question timer (seconds).
- A `> "quote"` line, where present, is a hint or the exam rationale.

Study tip: take the domain quizzes in weight order (Transformation and Ingestion first), score yourself per domain, and revisit the weak areas with the matching week overview.

## Currentness anchors

- [Official exam guide — exam version live from May 4, 2026](https://www.databricks.com/sites/default/files/2026-03/databricks-certified-data-engineer-associate-exam-guide-may-4-2026.pdf)
- [Current Lakeflow Spark Declarative Pipelines Python API](https://docs.databricks.com/aws/en/ldp/developer/python-ref)
- [Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/)
- [Auto Loader](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader)
- [Unity Catalog row filters, column masks, and ABAC](https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/)
- [Predictive optimization](https://docs.databricks.com/aws/en/optimizations/predictive-optimization)

> **Exam-guide conflict to teach explicitly:** the May 2026 outline names `DENY`, but the current SQL reference states that `DENY` is unsupported for Unity Catalog and applies only to `hive_metastore`. The questions use current product behavior and call out the discrepancy in their explanations.
