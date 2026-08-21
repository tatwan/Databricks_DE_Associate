# Solution Reviews — Learner-Facing, Post-Lab

Release each week's files **after** learners have attempted the corresponding lab. Do not use as pre-lab starter material — they contain complete solutions, explanations, validation queries, common mistakes, and exam takeaways.

Each week ships in two equivalent formats:

| Format | File pattern | Use it for |
|---|---|---|
| **Markdown review** (source of truth) | `WeekN_Solution_Review.md` | Reading anywhere — GitHub, editor, print |
| **Solution notebook** (markdown-only, nothing executes) | `WeekN_Solutions_Notebook.py` | Import into Databricks (Workspace → Import) and read side-by-side with your lab; code appears as copyable snippets |

Both show, per lab task: **the task as asked → the solution → why it works → common mistakes**.

## Release Timing

| Week | Files | Release after |
|---|---|---|
| 1 | `Week1_Solution_Review.md` · `Week1_Solutions_Notebook.py` | Week 1 lab debrief |
| 2 | `Week2_Solution_Review.md` · `Week2_Solutions_Notebook.py` | Week 2 lab debrief |
| 3 | `Week3_Solution_Review.md` · `Week3_Solutions_Notebook.py` | Week 3 lab debrief |
| 4 | `Week4_Solution_Review.md` · `Week4_Solutions_Notebook.py` | Week 4 lab debrief |
| 5 | `Week5_Capstone_Solution_Review.md` | Week 5 capstone debrief |

Note on Week 3: the "solution" is a correctly wired **Lakeflow Job**, not SQL — its review covers the target job configuration, the three expected runs (success → simulated failure → repair), the quality-gate stretch, and verification queries. `cicd/databricks.yml` is the same job declared as code.
