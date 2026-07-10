# Week 5: Capstone, Mock Review, and Final Exam Readiness

**Exam domains:** All seven (integrated in the capstone + targeted remediation from your mock results)  
**Estimated read time:** 20–30 minutes

## Purpose of This Week

No new content. The goal is **integration under realistic pressure** and **turning diagnostic information (your mock scores) into a focused final-week plan**.

Remember: the May 4, 2026 exam uses seven domains (including the new CI/CD and Troubleshooting/Monitoring/Optimization domains), not the older five-domain structure.

The two halves of the session:
1. **Capstone** (50 minutes) — Build an end-to-end governed, orchestrated slice of the BrewMart lakehouse with returns data.
2. **Mock review** — Autopsy questions from the domains where the cohort (and you) scored lowest.

## The Capstone — What You Are Actually Proving

You will:
- Ingest a new returns feed (bronze) — using idempotent COPY INTO.
- Apply a quality gate that sends unmatched returns to quarantine (silver) — using a rerunnable rebuild and explicit anti-join logic.
- Build a clustered gold table for net revenue (sales − returns).
- Put the final step behind a paused Lakeflow Job.
- Apply least-privilege grants.
- Validate everything with queries (including lineage).

(This single capstone touches Ingestion, Transformation, Lakeflow Jobs, Governance, and Troubleshooting.)

**Critical design decision in the capstone:**
Quarantine vs `WHERE` filter vs constraint.

- A plain `WHERE` silently drops the bad records.
- A `CHECK` constraint aborts the whole write.
- Quarantine keeps the pipeline flowing *and* makes the problematic records visible for later investigation.

The capstone plants a deliberate orphan return (order 2001 does not exist) and a duplicate so you must implement the right pattern.

## Eight Milestones, Three Gates

Use the milestone map from class (also available in the visuals folder).

Pass/fail gates are usually:
- M2 — Bronze loaded with idempotent COPY INTO proof.
- M3 — Silver + quarantine working correctly.
- M5 — Constraint proof (bad insert fails).

M1–M6 is a strong performance. M7–M8 (grants + lineage) are distinction-level.

Time checkpoints are announced in class (example: be on M3 by ~15 min, M5 by ~30–33 min).

## The "Rules Wall" Method for the Mock Review

For every question reviewed:
1. Read the stem aloud.
2. Name the **forcing constraint** (the detail that makes only one answer correct).
3. Eliminate options in order of confidence.
4. Name the *type* of distractor that died (invented syntax, real-feature-wrong-job, old-name bait, over-powered tool).

At the end of the review you should have a short list of reusable rules, not just "I got that one right."

## Coverage Recovery: Objectives That Are Easy to Under-Practice

Before the final seven-line summary, make sure you can answer these without notes. They are explicit in the May 4, 2026 outline but are not all central to the capstone.

### Ingestion and Loading

- Choose among `COPY INTO`, Auto Loader, Lakeflow Connect managed/standard connectors, partner connectors, and notebook-based JDBC/ODBC/REST clients.
- Explain Auto Loader directory listing vs file notification, schema enforcement vs evolution, and `_rescued_data`.
- Choose batch, streaming, or incremental loading from arrival pattern, scale, latency, and governance constraints.
- Ingest nested JSON and explain when to preserve nested structure vs `explode` arrays.

### Transformation and Modeling

- Distinguish inner, left, cross, multi-key, and broadcast joins.
- Manipulate rows and columns: filter, add/drop/rename/split, and explode.
- Deduplicate with `DISTINCT` or a latest-row window; aggregate with count, approximate distinct count, mean, and summary.
- Choose among a view, materialized view, streaming table, and managed table for a Gold object.
- Name what the four tuning settings influence: shuffle partitions, default parallelism, executor/driver memory, and the auto-broadcast threshold.

If any bullet is fuzzy, use the Week 1–2 readings and the two recovery slides in the Week 5 deck before attempting another full mock.

## The Seven Domain One-Liners (Photograph This)

- **Platform (Databricks Intelligence Platform):** One governed Delta copy serves every workload. Choose compute by workload type and interactivity.
- **Ingestion (Data Ingestion and Loading):** Match constraints to the ladder (managed connectors → Auto Loader/COPY INTO → custom). Idempotency is non-negotiable.
- **Transformation (Data Transformation and Modeling):** Bronze absorbs. Silver enforces contracts. MERGE gives idempotent upserts.
- **Jobs (Working with Lakeflow Jobs):** DAG of tasks. Transient failure → retry. Broken but fixable → repair run. Time-based → schedule. Data arrival → file/table trigger.
- **CI/CD (Implementing CI/CD):** Git folders version notebooks. Bundles declare everything. `validate → deploy → run`. PRs are created in the Git provider.
- **Troubleshooting (Troubleshooting, Monitoring, and Optimization):** Before any tasks run → infra/library/startup. During work → skew/shuffle/spill/OOM. Trends live in run history; one run lives in the Spark UI or query profile.
- **Governance (Governance and Security):** Privilege chain = USE CATALOG + USE SCHEMA + SELECT. One table → mask/filter. Fleet → ABAC. Managed tables unlock automation. `DENY` is legacy `hive_metastore`, not Unity Catalog.

These seven sentences are your final-week skeleton. If any line feels fuzzy, go back to that week's reading and lab.

## Final Week Study Plan (Do This)

**Day 1–2:** Your weakest domain  
- Re-read the relevant reading file.  
- Redo that week's lab from a completely blank notebook (no peeking at your old code).  
- Re-read the official exam guide bullets for that domain.

**Day 3–4:** Your second-weakest domain  
- Same treatment.  
- Retake that week's Markdown Mash quiz cold.

**Day 5:** Targeted mock repair  
- Only redo the questions you missed on the full mock.  
- Review your photograph of the rules wall.  
- Read the entire official exam guide outline once, out loud, 30 seconds per bullet.

**Day 6:** Light review or rest  
- Skim the seven one-liners.  
- Run the system check again on the actual exam machine.  
- Prepare ID, workspace, network.

**Day 7:** Exam day  
- 45 scored questions. 90 minutes. ~2 minutes per question.  
- First pass: answer everything you can do in < 90 seconds. Flag the rest.  
- Answer everything (no penalty for guessing).  
- Unscored experimental items may appear — do not let a weird question rattle you.

## Logistics (Book This Week)

- Register at webassessor.com/databricks ($200).
- Choose online proctored (Kryterion) or test center.
- Online requirements: webcam, government ID, clean desk, system check, stable connection, second monitor off.
- Results are typically available promptly after the exam.

Book a date that still gives you 5–7 solid study days after this session.

## Capstone Success Criteria

You have succeeded when all validation queries return the expected numbers and your job run history shows a clean execution.

Expected numbers for the supplied dataset:
- Bronze has **13** rows, including the duplicate.
- Silver has **11** deduplicated valid rows, and quarantine contains order **2001**.
- Net revenue rows exist where net < gross (returns applied).
- A bad insert against a constraint fails with a clear violation message.
- Job completes successfully.
- Grants are visible with `SHOW GRANTS`.
- Lineage graph shows the flow from returns volume through to gold.

## What "Done" Looks Like on Exam Day

You will walk in knowing:
- The mental model (one Delta copy + one UC tree).
- How to choose tools under constraints.
- The exact behavior of the most common DDL/DML and job features.
- How to eliminate answers using forcing constraints and distractor types.
- A calm pacing strategy.

The course has given you the content. Week 5 gives you the integration reps and the diagnostic information. The rest is disciplined retrieval practice in the final week.

Good luck. You are ready.
