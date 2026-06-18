# Databricks Data Engineer Associate

Five-Friday client enablement program for Databricks Certified Data Engineer Associate preparation.

This repository is organized for live instructor-led delivery. Learners should use the slides, notebooks, datasets, and released solution reviews. Instructor notes, quizzes, mock exams, and private solution notebooks are kept under `instructor_private/` and should not be distributed to learners.

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
5. For Week 3, import both task notebooks:
   - `notebooks/week3_01_ingest_bronze.py`
   - `notebooks/week3_02_build_silver.py`

## Materials

### Learner-Facing

- `slides/` — weekly PowerPoint decks.
- `notebooks/` — Databricks source-format learner notebooks.
- `datasets/` — small lab datasets used by the notebooks.
- `cicd/` — Databricks bundle example for Week 3.
- `readings/` — supplemental reference material for offline study and exam review (one file per week). These are always available to learners.
- `solutions/` — post-lab solution review handouts. These should be released only after learners complete the corresponding lab or capstone.

### Instructor-Only

- `instructor_private/notes/` — curriculum map, weekly instructor notes, demo scripts, pacing, facilitation guidance, and mock-exam planning.
- `instructor_private/markdown_mash/` — live quizzes and mock exam.
- `instructor_private/notebook_solutions/` — private Databricks solution notebooks used for instructor debrief and rescue.
- `instructor_private/Databricks_Suggested_Outline.md` — planning reference.

Do not publish or share `instructor_private/` with learners. It contains answer keys, assessment material, and delivery guidance that would weaken the learning experience if seen early.

## Solution Review Policy

The files in `solutions/` will be released them after the relevant lab:

| File | Release after |
|---|---|
| `solutions/Week1_Solution_Review.md` | Week 1 lab debrief |
| `solutions/Week2_Solution_Review.md` | Week 2 lab debrief |
| `solutions/Week4_Solution_Review.md` | Week 4 lab debrief |
| `solutions/Week5_Capstone_Solution_Review.md` | Week 5 capstone debrief |

Week 3 is mostly a Jobs UI exercise. Use the Week 3 task notebooks and `cicd/databricks.yml` as the reference package.

## Notes for Instructors

Before delivery:

- Rehearse each notebook in the target Databricks workspace.
- Confirm which Free Edition features are available for Jobs triggers, Auto Loader, masks, row filters, and lineage.
- Keep screenshots or recorded walkthroughs for any workspace feature that may be unavailable during class.
- Use the mock exam and weekly quizzes from `instructor_private/markdown_mash/` only in controlled delivery.
