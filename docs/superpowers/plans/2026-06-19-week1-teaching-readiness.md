# Week 1 Teaching Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Week 1 student notebook self-explanatory and align the instructor runbook and student handout to a clear two-hour delivery path.

**Architecture:** Preserve the existing course artifacts and working notebook code. Improve the learner experience through Markdown cells that precede executable cells, then make the instructor notes follow the same order with compact delivery cues. Validate slides, reading, and assessment as supporting artifacts and change them only when correctness or delivery readiness requires it.

**Tech Stack:** Databricks source-format notebooks (`.py`), Markdown, Markdown Mash, PowerPoint (`.pptx`), shell-based static checks, official Databricks documentation.

---

## File Map

- `notebooks/Week1_Lakehouse_Fundamentals.py`: learner-facing demo and hands-on lab; primary edit.
- `instructor_private/notes/01_Week1.md`: instructor-only 3:00-5:00 runbook aligned to notebook order.
- `readings/Week1_Lakehouse_Foundations.md`: student handout for independent review.
- `instructor_private/markdown_mash/Week1_Quiz.md`: full assessment; audit only unless a correctness issue is found.
- `slides/Week1_Lakehouse_Foundations.pptx`: presentation; visual and technical audit only unless a blocking issue is found.
- `notebooks/Week2_Ingestion_Transformations.py`: learner-visible solution-message cleanup only.
- `notebooks/Week4_Governance_Optimization.py`: learner-visible solution-message cleanup only.
- `notebooks/Week5_Capstone.py`: learner-visible solution-message cleanup only.

### Task 1: Add learner guidance to the Week 1 notebook

**Files:**
- Modify: `notebooks/Week1_Lakehouse_Fundamentals.py`
- Reference: `instructor_private/notebook_solutions/Week1_Lakehouse_Fundamentals_Solution.py`
- Reference: `datasets/week1_retail_sales.csv`

- [ ] **Step 1: Record the current notebook structure**

Run:

```bash
rg -n '^# COMMAND|^# MAGIC %md|^# MAGIC %sql|TODO|Instructor Solution' notebooks/Week1_Lakehouse_Fundamentals.py
```

Expected: Parts 1-3, seven demo topics, Tasks 4-7, validation, stretch, and the current solution message are visible.

- [ ] **Step 2: Add the notebook learning contract and language rationale**

Update the opening Markdown to describe Part 2 as an instructor-led worked example and Part 3 as the student lab. Add a `Why SQL in this lab?` section before setup containing these points:

```markdown
### Why SQL in this lab?

SQL is the clearest language for today's table, metadata, governance, and query tasks. It is declarative: you describe the result you want, and Databricks plans the execution. These operations are also directly relevant to the certification exam.

- **SQL:** best fit here for DDL, CTAS, metadata inspection, views, and table recovery.
- **Python/PySpark:** useful for reusable program logic, control flow, complex transformations, and orchestration.
- **Scala:** provides direct access to Spark's JVM APIs and appears in some engineering codebases, but it is not needed for today's objectives.

Databricks notebooks can mix languages. This notebook uses Python for the reusable schema setting and SQL for the data-engineering operations.
```

- [ ] **Step 3: Add context before every Part 1 and Part 2 executable cell**

For each executable cell, place learner-facing Markdown immediately before it. Each block must answer `Goal`, `What happens`, and `What to look for`. Include prediction prompts before the DDL, CTAS, UPDATE, time-travel, volume, and view cells. Keep the first examples suitable for live typing and label later repetitive cells as prepared cells the instructor may paste/run.

- [ ] **Step 4: Expand Tasks 4-7 into complete learner instructions**

Each task must include:

```markdown
**Goal:** one observable outcome.

**Before you code:** the relevant concept and input object.

**Your task:** numbered actions with the exact object names to create or inspect.

**Expected result:** concrete rows, metadata, history operations, or matching totals.

<details>
<summary>Hint</summary>

A concept-level hint that does not reveal the full solution.
</details>
```

Task 4 must specify the `/Volumes/workspace/{USER_SCHEMA}/landing/week1_retail_sales.csv` source, required casts, and `line_total`. Task 5 must name `Type` and `Provider` as the metadata fields to find. Task 6 must define the persistent view output and explain temp-view scope. Task 7 must distinguish querying an old version from restoring current state.

- [ ] **Step 5: Make validation and completion criteria explicit**

Explain that successful completion means:

- `sales_raw` is a managed Delta table with `line_total`;
- `sales_by_store` returns three named stores plus the `NULL` store group;
- history includes create/replace, update, and restore operations;
- version 0 and current `line_total` totals match after restore.

Preserve the stretch task and explain that a null operand produces a null arithmetic result.

- [ ] **Step 6: Replace the learner-visible private solution message**

Use exactly:

```markdown
## Solution

The solution file will be shared by your instructor.
```

- [ ] **Step 7: Verify Databricks source cell boundaries and guidance coverage**

Run:

```bash
python3 -m py_compile notebooks/Week1_Lakehouse_Fundamentals.py
rg -n '^# COMMAND' notebooks/Week1_Lakehouse_Fundamentals.py
rg -n -i 'instructor_private|intentionally ignored|git' notebooks/Week1_Lakehouse_Fundamentals.py
```

Expected: compile succeeds; cell delimiters remain intact; the final search returns no learner-visible private-path or git text.

### Task 2: Rebuild the instructor notes as a two-hour runbook

**Files:**
- Modify: `instructor_private/notes/01_Week1.md`
- Reference: `notebooks/Week1_Lakehouse_Fundamentals.py`

- [ ] **Step 1: Replace the timing table with the approved route**

Use the exact segments `3:00-3:10`, `3:10-3:52`, `3:52-4:20`, `4:20-4:47`, and `4:47-5:00`. State that all slides remain available, Part 2 is the only demo, Part 3 is the only lab, and decision cards are optional verbal checks.

- [ ] **Step 2: Add slide pacing cues without rewriting the deck**

Map the 19 actual slides into `Teach`, `Skim`, and `Reference` pacing labels. Keep slide-specific speaker notes as reference material but put the live pacing map before the long slide reference section.

- [ ] **Step 3: Replace the duplicated demo guide with notebook-aligned cue cards**

For every Part 2 cell, use this compact order immediately before its code:

```markdown
#### Step: [Notebook heading]

**Goal:** ...
**Say:** ...
**Delivery:** Type live | Paste/run
**Ask before running:** ...
**Expect:** ...
**Recover:** ...
```

The first namespace and DDL examples should favor live typing. CTAS onward may favor paste/run while still explaining the important line.

- [ ] **Step 4: Clarify the transition into the student lab**

State that Task 4 is started together and Tasks 5-7 continue independently. Add a `4:45 checkpoint` that tells the instructor to stop coding, debrief expected results, and assign unfinished steps for after class.

- [ ] **Step 5: Demote the decision cards to an optional checkpoint**

Retain the managed/external and table/volume scenarios, but label them `Optional: use verbally during slide transitions or when the room needs a reset`. Remove them from the required timing path.

- [ ] **Step 6: Select five live quiz questions**

Use Q1, Q5, Q6, Q7, and Q10 for the live close because they sample Delta default format, volumes, CTAS, temp-view scope, and time travel. State that Q2-Q4 and Q8-Q13 remain self-review.

- [ ] **Step 7: Add a time-pressure fallback**

Add a short `If behind` box: paste rather than type from CTAS onward, skip the optional decision cards, demonstrate Task 4 only, and still reserve the final five minutes for recap and next steps.

### Task 3: Validate and improve the student handout

**Files:**
- Modify if needed: `readings/Week1_Lakehouse_Foundations.md`

- [ ] **Step 1: Verify version-sensitive claims against official Databricks sources**

Check current official documentation for Free Edition limitations, Delta defaults, Unity Catalog hierarchy, managed/external table behavior, volumes, CTAS, views, time travel, restore, and current product names. Record only sources needed to resolve a factual uncertainty; do not add a long bibliography.

- [ ] **Step 2: Add a concise language-choice section**

Mirror the notebook rationale in reading form: SQL for declarative table operations and exam relevance; PySpark/Python for programmatic transformations and orchestration; Scala for JVM-oriented Spark codebases; mixed-language notebooks as a normal Databricks workflow.

- [ ] **Step 3: Align BrewMart expectations with the notebook**

Confirm the object names, volume path, casts, view outputs, recovery sequence, and Week 2 carry-forward instructions match the updated lab.

- [ ] **Step 4: Check independent readability**

Run:

```bash
rg -n '^## |SQL|PySpark|Scala|BrewMart|sales_raw|sales_by_store|VERSION AS OF|RESTORE' readings/Week1_Lakehouse_Foundations.md
```

Expected: the handout contains a scannable concept progression, language rationale, and notebook-aligned review guidance.

### Task 4: Clean learner-visible solution messages in later notebooks

**Files:**
- Modify: `notebooks/Week2_Ingestion_Transformations.py`
- Modify: `notebooks/Week4_Governance_Optimization.py`
- Modify: `notebooks/Week5_Capstone.py`

- [ ] **Step 1: Replace private-path wording**

In each notebook, preserve the solution heading but replace the path and git-ignore sentence with:

```markdown
The solution file will be shared by your instructor.
```

- [ ] **Step 2: Verify the repository-wide learner-facing cleanup**

Run:

```bash
rg -n -i 'instructor solution|instructor_private|intentionally ignored by git' notebooks --glob '*.py'
```

Expected: solution headings may remain; no notebook exposes a private path or git-ignore implementation detail.

### Task 5: Audit the quiz and slide deck

**Files:**
- Modify only if needed: `instructor_private/markdown_mash/Week1_Quiz.md`
- Modify only if blocking: `slides/Week1_Lakehouse_Foundations.pptx`

- [ ] **Step 1: Audit the Markdown Mash quiz**

Verify one correct answer per question, objective alignment, answer-position distribution, longest-answer cues, timing, and consistency with the updated notebook and reading. Preserve all 13 questions unless a correctness issue requires a targeted rewrite.

- [ ] **Step 2: Render and inspect all 19 slides**

Use the presentations skill rendering workflow to produce full-slide previews and a contact sheet in scratch space outside the repository. Check clipping, overflow, contrast, title consistency, speaker notes, and factual alignment. Do not rewrite or restyle a slide that is already sound.

- [ ] **Step 3: Make only blocking slide corrections**

If a factual or render-visible defect exists, use `@oai/artifact-tool` targeted-edit mode, preserve inherited styling, rerender every affected slide, and export back to `slides/Week1_Lakehouse_Foundations.pptx`. If no defect exists, leave the file byte-for-byte unchanged.

### Task 6: Run final cross-artifact validation

**Files:**
- Validate all files listed in the file map.

- [ ] **Step 1: Run structural and whitespace checks**

Run:

```bash
git diff --check
python3 -m py_compile notebooks/Week1_Lakehouse_Fundamentals.py notebooks/Week2_Ingestion_Transformations.py notebooks/Week4_Governance_Optimization.py notebooks/Week5_Capstone.py
```

Expected: no whitespace errors and all Databricks source notebooks compile as Python source.

- [ ] **Step 2: Confirm private implementation wording is absent**

Run:

```bash
rg -n -i 'instructor_private|intentionally ignored by git' notebooks readings
```

Expected: no matches.

- [ ] **Step 3: Review the final diff for scope and alignment**

Run:

```bash
git diff --stat
git diff -- notebooks/Week1_Lakehouse_Fundamentals.py instructor_private/notes/01_Week1.md readings/Week1_Lakehouse_Foundations.md notebooks/Week2_Ingestion_Transformations.py notebooks/Week4_Governance_Optimization.py notebooks/Week5_Capstone.py
```

Expected: Week 1 notebook and instructor notes contain the substantive changes; reading changes are targeted; later notebooks contain only solution-message edits; slide and quiz changes appear only if validation found a real defect.

- [ ] **Step 4: Issue the readiness verdict**

Report `GO`, `GO WITH MINOR FIXES`, or `NOT YET`, summarize verification evidence, and state any environmental limitation that prevented live Databricks execution.
