# Databricks Data Engineer Associate

Five-Friday client enablement program for Databricks Certified Data Engineer Associate preparation.

This repository is organized for live instructor-led delivery. Learners should use the slides, notebooks, datasets, practice quizzes, and released solution reviews. Instructor notes, quizzes, mock exams, and private solution notebooks are kept under `instructor_private/` and should not be distributed to learners.

## About the Certification Exam

The course targets the exam version that goes live **May 4, 2026**. Always confirm the current details against the official exam guide before your test date — Databricks updates it whenever the exam changes.

| Fact | Detail |
|---|---|
| Scored questions | 45 multiple-choice (unscored trial items may also appear) |
| Time limit | 90 minutes |
| Registration fee | USD 200 (plus local taxes) |
| Delivery | Online proctored or test center |
| Prerequisite | None required; ~6 months hands-on Databricks experience recommended |
| Validity | 2 years (recertify with the current live exam) |
| Retake policy | 14-day wait after a failed attempt |

### Exam domain / topic distribution

The exam is organized into seven domains. The approximate weights below are the blueprint this course is built to; use them to prioritize study — Ingestion and Transformation together are ~43% of the exam, so they get the most class time. All mock exams and practice quizzes are weighted to match.

| # | Exam domain | Approx. weight | ~Qs of 45 | Key topics | Course week |
|---|-------------|:---:|:---:|-------------|:---:|
| 1 | Databricks Intelligence Platform | ~6% | 3 | Lakehouse value, Delta Lake & `_delta_log`, Unity Catalog object model, control vs data plane, compute selection | 1 |
| 2 | Data Ingestion & Loading | ~21% | 9 | COPY INTO, Auto Loader (`cloudFiles`, checkpoints, schema evolution, `_rescued_data`), Lakeflow Connect, nested/semi-structured data | 2 |
| 3 | Data Transformation & Modeling | ~22% | 10 | Bronze→silver cleaning, joins & broadcast, dedup & window functions, MERGE, aggregations, gold objects, data quality | 2 |
| 4 | Working with Lakeflow Jobs | ~16% | 7 | Jobs/tasks/DAG, triggers, control flow (retries, if/else, for-each), parameters & task values, repair runs | 3 |
| 5 | Implementing CI/CD | ~10% | 4 | Git folders vs provider PRs, Declarative Automation Bundles, `validate → deploy → run`, service-principal promotion | 3 |
| 6 | Troubleshooting, Monitoring & Optimization | ~10% | 5 | Spark UI (skew, spill, shuffle), OPTIMIZE/VACUUM, Liquid Clustering, predictive optimization, failure triage | 3–4 |
| 7 | Governance & Security | ~15% | 7 | Privilege chain & GRANT/REVOKE/DENY, principals, column masks & row filters, ABAC, managed vs external, lineage | 4 |

*Weights are approximate and aligned to the exam-guide section ordering; the official guide lists objectives rather than fixed percentages, and the exact mix can vary by exam form. Re-verify each cohort.*

### Official exam guides & resources

- [Exam guide — version live from May 4, 2026 (PDF)](https://www.databricks.com/sites/default/files/2026-03/databricks-certified-data-engineer-associate-exam-guide-may-4-2026.pdf)
- [Certification overview page](https://www.databricks.com/learn/certification/data-engineer-associate) — always links the latest exam guide
- [Databricks certification hub](https://www.databricks.com/learn/training/certification)
- [Certification & badging FAQ](https://www.databricks.com/learn/certification/faq)

### Where to register

- Register and schedule at **[webassessor.com/databricks](https://webassessor.com/databricks)** (create an account → *Register for an Assessment*).
- Choose online-proctored or a test center. For online, run the [Kryterion system check](https://www.kryterion.com/systemcheck) on the actual machine you'll test on.
- Have a government-issued photo ID and a clean, quiet testing area ready.

## Course Format

| Week | Focus | Main learner artifacts |
|---|---|---|
| 1 | Lakehouse foundations, Delta Lake, Unity Catalog, tables, views, volumes | `slides/Week1_Lakehouse_Foundations.pptx`, `notebooks/Week1_Lakehouse_Fundamentals.py`, `datasets/week1_retail_sales.csv` |
| 2 | Ingestion, Auto Loader, COPY INTO, bronze-to-silver transformations, MERGE | `slides/Week2_Ingestion_Transformations.pptx`, `notebooks/Week2_Ingestion_Transformations.py`, Week 2 datasets |
| 3 | Lakeflow Jobs, orchestration, Git folders, Declarative Automation Bundles | `slides/Week3_Jobs_CICD.pptx`, `notebooks/Week3_Jobs_Orchestration.py`, `notebooks/week3_01_ingest_bronze.py`, `notebooks/week3_02_build_silver.py`, `cicd/databricks.yml` |
| 4 | Governance, security, troubleshooting, optimization, exam strategy | `slides/Week4_Governance_Optimization.pptx`, `notebooks/Week4_Governance_Optimization.py` |
| 5 | Capstone, mock-review debrief, final exam readiness | `slides/Week5_Capstone_ExamReadiness.pptx`, `notebooks/Week5_Capstone.py`, `datasets/week5_returns.csv` |

## Learner Setup

1. Use a Databricks Free Edition workspace unless your instructor provides another workspace.
2. Import the relevant `.py` file from `notebooks/` into Databricks as a notebook.
3. Upload the required CSV or JSON files from `datasets/` when the notebook asks for them.
4. Keep your Week 1 schema and volume through the full course. Later weeks build on earlier objects.
5. For Week 3, import these notebooks:
   - `notebooks/Week3_Jobs_Orchestration.py` — the companion you run interactively (pre-flight + verification)
   - `notebooks/week3_01_ingest_bronze.py` — executed by the job you build (Task 1)
   - `notebooks/week3_02_build_silver.py` — executed by the job you build (Task 2)
   - `notebooks/week3_03_quality_gate.py` — optional stretch task (Task 3, data-quality gate)
   - `notebooks/week3_dlt_pipeline.py` — bonus: source for a Lakeflow Declarative Pipeline (attach in the Pipelines UI; do not run as a notebook)
6. For Week 5, import the capstone plus its two job-task skeletons:
   - `notebooks/Week5_Capstone.py` — the learner workspace and milestone checks
   - `notebooks/week5_01_ingest_returns.py` — paste the tested M2 implementation, then use as job Task 1
   - `notebooks/week5_02_build_net_revenue.py` — paste the tested M3–M4 implementation, then use as dependent job Task 2

## Materials

### Learner-Facing

- `slides/` — weekly PowerPoint decks.
- `notebooks/` — Databricks source-format learner notebooks.
- `datasets/` — small lab datasets used by the notebooks.
- `cicd/` — Databricks bundle example for Week 3.
- `readings/` — supplemental reference material for offline study and exam review (one file per week, plus a final `Exam_Review_CheatSheet.md`). These are always available to learners.
- `practice/` — Markdown Mash practice quizzes with answer keys, organized `by_week/` and `by_domain/` (weighted to the exam blueprint). Always available to learners.
- `solutions/` — post-lab solution review handouts. These should be released only after learners complete the corresponding lab or capstone.


## Solution Review Policy

The files in `solutions/` are released after the relevant lab debrief.

**Solution notebooks (Databricks source format, markdown-only — import and read; nothing executes).** Each shows, per lab task: the task, the solution snippet, why it works, and common mistakes:

| File | Release after |
|---|---|
| `solutions/Week1_Solutions_Notebook.py` | Week 1 lab debrief |
| `solutions/Week2_Solutions_Notebook.py` | Week 2 lab debrief |
| `solutions/Week3_Solutions_Notebook.py` | Week 3 lab debrief (job config + runs + gate + verification) |
| `solutions/Week4_Solutions_Notebook.py` | Week 4 lab debrief |

**Markdown review documents** (same content in plain-Markdown form, for offline reading):

| File | Release after |
|---|---|
| `solutions/Week1_Solution_Review.md` | Week 1 lab debrief |
| `solutions/Week2_Solution_Review.md` | Week 2 lab debrief |
| `solutions/Week3_Solution_Review.md` | Week 3 lab debrief |
| `solutions/Week4_Solution_Review.md` | Week 4 lab debrief |
| `solutions/Week5_Capstone_Solution_Review.md` | Week 5 capstone debrief |
