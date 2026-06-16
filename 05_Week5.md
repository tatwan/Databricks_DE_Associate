# Week 5: Capstone, Mock-Exam Review, and Final Exam Readiness

> Aligned to the **May 4, 2026** Databricks Certified Data Engineer Associate exam guide.
> Domains: **all seven**, integrated. No new exam content — this session converts knowledge into exam performance.
> Companion assessment: the instructor-only 45-question Markdown Mash mock exam, taken as a timed event after Week 4 and reviewed in class today.

---

## 1. Session Overview

- **Duration:** 2 hours
- **Target audience:** Same cohort; Weeks 1–4 completed; mock exam taken, timed, and self-scored **per domain** before class
- **Prerequisites:**
  - All BrewMart objects intact: `sales_bronze`, `sales_silver`, `customers`, `sales_gold_daily`, `landing` volume, the Week 3 job
  - `week5_returns.csv` downloaded before class
  - Mock domain-score breakdown in hand
- **Main exam domains covered:** All seven, in two modes — *integration* (capstone) and *remediation* (review)
- **Learning objectives.** By the end of this session, learners can:
  1. Build an end-to-end governed, orchestrated lakehouse slice — ingest → quality-gated silver → clustered gold → scheduled job → grants — under time pressure, unassisted
  2. Diagnose their own weak domains from mock results and apply targeted remediation
  3. Execute the elimination method on full-difficulty exam questions at exam pace
  4. Walk into the exam with logistics handled and a final-week study plan

---

## 2. Recommended Timing

| Time      | Segment                      | Purpose                     |
| --------- | ---------------------------- | --------------------------- |
| 0:00–0:05 | Warm-up: domain-score show of hands | Map the cohort's weak spots; calibrate the review |
| 0:05–0:15 | Concept slides (capstone brief + rules) | Frame the integration exercise |
| 0:15–1:05 | **Capstone** (the week's "lab") | All seven domains in one build, 50 minutes |
| 1:05–1:20 | Capstone debrief (the week's "demo": instructor solution walkthrough) | Compare approaches; surface integration mistakes |
| 1:20–1:50 | Mock-exam review by domain (the week's "activity") | Question autopsies on the cohort's worst domains |
| 1:50–2:00 | Final readiness checklist + send-off | Logistics, last-week plan, confidence calibration |

*Structural note: this week the lab IS the capstone, the demo IS the solution walkthrough, and the activity IS the mock review. The weekly quiz is replaced by the instructor-only 45-question mock exam.*

---

## 3. Slide Deck Content

*(Short deck by design — 8 slides; the session is hands-on and discussion-heavy.)*

### Slide 1: Where You Stand

**Key bullets**
- Four weeks, seven domains, ~50 practice questions, one mock — today: integration + repair
- Show of hands per domain: "below 70% on the mock?" — we review the top two or three pain domains
- Typical cohort pattern: CI/CD and Governance lowest (newest + least practiced) — expect company
- Today's two halves: *can you build it* (capstone) and *can you answer it* (review)

**Speaker notes**
Run the show-of-hands honestly and write the counts on screen — the review block's agenda comes from this, live. Normalize imperfect mock scores: the mock is calibration, not verdict; a 60% with a clear domain diagnosis a week out is a passing trajectory. Set the day's tone: no new material, maximum reps.

**Visual suggestion**
Seven domain badges with empty tally boxes to fill in live.

**Exam relevance**
Directs the remaining 90 minutes to the cohort's actual gaps.

**Common misconception**
"A failed mock means postpone." It means *targeted week*, not retreat — domains are repairable in days.

---

### Slide 2: Capstone Brief — BrewMart Returns

**Key bullets**
- New business event: **product returns** arrive as CSVs; finance wants *net* revenue (sales − returns) per store per day
- You will: ingest returns → quality-gate them into silver (quarantine bad ones) → build a clustered net-revenue gold → schedule it → govern it
- 50 minutes, milestone checklist, solution withheld until debrief
- Everything you need was taught in Weeks 1–4; the integration is the exam

**Speaker notes**
Read the business story once, then point at the milestone list (Section 5) and start the clock. Coach style for today: answer "where is X" questions, refuse "how do I X" questions for the first 30 minutes — the struggle is the point. Tell them which milestones are pass/fail gates (M2, M3, M5) vs. stretch (M7, M8).

**Visual suggestion**
The full BrewMart architecture diagram: existing pipeline grayed, today's returns branch highlighted in color, ending in a `net_revenue_daily` gold node.

**Exam relevance**
The exam's scenario questions assume you've *done* this end-to-end at least once. After today, you have.

**Common misconception**
"The capstone needs new commands." Zero new syntax — if you're reaching for something untaught, you've overcomplicated a step.

---

### Slide 3: Capstone Rules and Rubric

**Key bullets**
- Work solo (pairs allowed for those who lost workspace state); validation queries provided per milestone — self-check as you go
- Order matters: M1→M5 are sequential; M6–M8 in any order
- Stuck >5 min on one milestone? Take the hint card (each costs nothing but pride)
- Done = all validation queries green; early finishers take the stretch (returns-rate alerting design)

**Speaker notes**
Hint cards (Section 6 of this doc) keep momentum without giving away solutions — print or post them folded/collapsed. Announce time checkpoints aloud at 15/30/40 minutes with the milestone you *should* be on (M3 / M5 / M6). The room's energy management is your main job for this hour.

**Visual suggestion**
Checklist graphic of the 8 milestones with suggested minute-marks.

**Exam relevance**
Pacing under a clock is itself exam training — same skill, different format.

**Common misconception**
That finishing all 8 milestones is required to "pass." M1–M6 is a strong performance; M7–M8 are the distinction tier.

---

### Slide 4: Review Method — The Question Autopsy

**Key bullets**
- For each reviewed mock question: (1) read stem aloud, (2) name the forcing constraint, (3) kill options in order of confidence, (4) name the distractor *types* that died
- Distractor taxonomy refresher: invented syntax · real-feature-wrong-job · old-name bait · over-powered tool
- You explain, not me: a learner drives each autopsy; I referee
- Goal: turn every miss into a named, reusable rule

**Speaker notes**
This slide is the contract for the 30-minute review block. Learner-driven autopsies are slower but stick — budget ~3 minutes per question, so pick ~8–10 questions max from the weakest domains (use the mock key's domain map to grab them fast). End each autopsy by having the driver state the rule in one sentence ("DENY beats GRANT", "deploy places, run executes") — collect these on a visible "rules wall."

**Visual suggestion**
A four-step autopsy flow diagram + the four distractor "wanted posters" from Week 4.

**Exam relevance**
The method *is* the deliverable — it's what they'll run 45 times on exam day.

**Common misconception**
Reviewing by rereading notes. Misses become learning only when the *elimination path* is reconstructed, not the fact.

---

### Slide 5: Domain Cheat Card — The Seven One-Liners

**Key bullets**
- **Platform:** one copy (Delta) + one governance tree (UC) + right-sized compute (serverless = hands-off)
- **Ingestion:** match the constraint — files@scale→Auto Loader · SQL batch→COPY INTO · SaaS→managed connector · custom→notebook+Jobs
- **Transformation:** bronze absorbs, silver enforces, gold serves; MERGE = idempotent upsert
- **Jobs:** DAG of tasks; transient→retry, broken→fix+repair; time→schedule, data→file-arrival/table-update
- **CI/CD:** Git folders for code, bundles for everything; validate→deploy→run; PR lives in the provider
- **Troubleshooting:** before-work=infra/library, during=skew/spill/OOM; trends→run history, one run→Spark UI
- **Governance:** chain = USE+USE+SELECT; DENY>GRANT; one table→mask/filter, fleet→ABAC; managed unlocks automation

**Speaker notes**
Read all seven aloud, slowly — this is the course in 30 seconds and the last-week revision artifact. Tell learners to photograph this slide; it's their final-review skeleton: if any line feels foggy, that's tonight's docs reading.

**Visual suggestion**
Seven horizontal cards, one per domain, color-matched to the badges used all course.

**Exam relevance**
Compressed retrieval cues for every domain.

**Common misconception**
—

---

### Slide 6: Exam Logistics — No Surprises

**Key bullets**
- Register at webassessor.com/databricks; $200; online proctored (Kryterion) or test center
- Online: system check done?, webcam, government ID, clean desk, no notes/phones, stable network
- 45 scored questions, 90 min, possible unscored extras; results typically prompt
- Reschedule/cancellation windows exist — book a slot that gives you 5–7 more study days

**Speaker notes**
Walk the booking flow on screen if time allows. Push them to book **this week** — a date on the calendar converts studying from "someday" to a plan. Online-proctoring gotchas worth saying: second monitors off, room scan happens, bathroom breaks are restricted — test-center is worth considering for anyone with flaky internet.

**Visual suggestion**
A timeline from today → study days → exam day, with logistics checkpoints flagged.

**Exam relevance**
Administrative failure is the most preventable failure.

**Common misconception**
"I'll book after I feel ready." Readiness follows the booking, rarely the reverse.

---

### Slide 7: Your Final Week Plan

**Key bullets**
- Day 1–2: weakest domain — docs + redo that week's lab from scratch
- Day 3–4: second-weakest — same treatment; redo its quiz cold
- Day 5: re-take the mock's missed questions only; review the rules wall
- Day 6: rest or light review of the seven one-liners; Day 7: exam
- Re-read the official exam guide outline once — it's the test's table of contents

**Speaker notes**
Prescriptive on purpose — decision fatigue kills final weeks. Emphasize *redoing labs from scratch* over rereading: retrieval beats recognition. The official guide re-read matters: any outline bullet they can't speak to for 30 seconds is a flag.

**Visual suggestion**
A 7-day calendar strip with the plan stamped on it.

**Exam relevance**
Spaced, targeted, retrieval-based — the highest-yield week structure.

**Common misconception**
Cramming new material in the last 48 hours. The final days consolidate; they don't expand.

---

### Slide 8: Send-Off

**Key bullets**
- You built a governed lakehouse, productionized it, secured it, tuned it — from a free workspace
- The exam tests vocabulary + judgment; you've drilled both for five weeks
- After you pass: credential via credentials.databricks.com; recert in 2 years; Professional cert is the next ladder rung
- Stay in the course channel — share your result and your exam-day notes (within NDA!) for the cohort behind you

**Speaker notes**
Keep it short and warm. Remind them of the NDA: celebrating is fine, reciting questions isn't. Mention the Professional cert as the horizon for the strong finishers — several will ask. Last words: book it, take it, tell us.

**Visual suggestion**
Course-complete graphic: all five Fridays stamped, the credential badge at the end of the path.

**Exam relevance**
Closure and momentum.

**Common misconception**
—

---

## 4. Instructor Demo

### Demo: Capstone Solution Walkthrough + Three Question Autopsies

**Goal**
Close the capstone with a clean reference solution (15 minutes, after learners attempt it), highlighting the integration decisions; then model the autopsy method on three full-difficulty mock questions before handing the method to learners for the review block.

**Setup**
- Your own completed capstone build in `week1_demo` (built in rehearsal — you'll walk it, not build it live)
- Instructor-only mock exam open; three pre-chosen questions spanning the cohort's likely weak domains (suggested: Q31 targets/bundles, Q39 privilege chain, Q21 constraint-vs-quarantine)

**Walkthrough script (Part 1 — capstone solution, ~15 min)**
1. **The shape first:** show the finished lineage graph — returns volume → bronze → silver (+ quarantine) → net-revenue gold, with the job node. "Architecture before code: this is what M1–M8 built."
2. **M2 — bronze:** "All strings, audit column, COPY INTO. Rerun it — zero rows. You've seen this four weeks running; on the exam this pattern is half of Domain 2."
3. **M3 — the quality gate (the capstone's heart):** walk the anti-join split — returns matching real orders go to silver; orphans (order 2001) land in `returns_quarantine`. "Constraint would have *rejected the batch*; quarantine *keeps the pipeline flowing and the problem visible*. Choosing between those is an exam question and a design review."
4. **M4 — net revenue:** the join of returns to sales for unit prices, then sales-minus-returns per store/day, `CLUSTER BY (store, order_date)`. "Note returns valued at the *order's* price — a business rule encoded in a join."
5. **M5/M6/M7:** constraint on silver; the two-task job (paused schedule — say why again); the grant + mask on `reason`? No — mask on nothing here: grant SELECT on the gold *view*, point out least privilege. "Governance is two statements when the structure is right."
6. **The mistakes I saw:** name 2–3 patterns observed during the hour (typical: quality gate done as a WHERE that silently *drops* orphans with no quarantine; MERGE used where plain INSERT sufficed; clustering on `return_id`). No names, all lessons.

**Walkthrough script (Part 2 — three autopsies, ~8 min, instructor-driven to model the method)**
- For each: stem aloud → "the forcing constraint is…" → eliminate in confidence order → name the distractor types → one-sentence rule for the wall. Then: "Next block, you drive."

**Expected results**
Learners leave with: a validated-or-corrected capstone, the reference pattern for quality gates, and the autopsy method demonstrated three times at full speed.

**Troubleshooting**
| Problem | Fix |
| --- | --- |
| Many learners far behind at debrief time | Walk M1–M4 only; publish M5–M8 of the solution to the channel; protect the review block — it serves the exam more than capstone completion does. |
| Solution walkthrough becomes re-teaching | Time-box per milestone (90s); park concept questions to the review block where they likely map to a mock question anyway. |
| Cohort aced the mock (rare) | Swap review time for "hard mode": the three autopsies become learner-driven cold, plus the stretch alerting-design discussion. |

---

## 5. Hands-On Lab

### Lab (Capstone): BrewMart Returns — Net Revenue, End to End

**Scenario**
Finance discovered that gross revenue overstates performance — customers return products. A returns feed now lands in your volume. Deliver net revenue per store per day: governed, quality-gated, clustered, scheduled. Fifty minutes. Everything was taught; nothing is new.

**Business Problem**
Integrate a second data feed into the existing lakehouse without breaking its guarantees: bad return records must not poison silver (but must stay visible), the gold layer must reflect sales *minus* returns, and the whole flow must run on a schedule with least-privilege access.

**Tasks (milestones — validation query after each)**

1. **M1 — Land it (≈3 min):** upload `week5_returns.csv` to a new `landing/returns_incoming/` folder in your volume
2. **M2 — Bronze (≈5 min):** `returns_bronze` (all STRING + `_ingested_at`), loaded via `COPY INTO`; prove rerun = 0 rows
3. **M3 — Quality-gated silver (≈12 min):** `returns_silver` = typed, deduplicated returns **whose `order_id` exists in `sales_silver`**; non-matching rows go to `returns_quarantine` (not dropped!)
4. **M4 — Gold (≈10 min):** `net_revenue_daily` with `CLUSTER BY (store, order_date)`: per store/day, gross revenue (from sales), returned amount (returned qty × the order's unit price), and net = gross − returned
5. **M5 — Contract (≈3 min):** constraint on `returns_silver`: `quantity_returned > 0`; prove it rejects a bad insert
6. **M6 — Orchestrate (≈8 min):** a 2-task job — `ingest_returns` (notebook or SQL task wrapping M2) → `build_net_revenue` (M4 rebuild), **paused** daily schedule, one successful manual run
7. **M7 — Govern (≈4 min):** a view `net_revenue_summary` over the gold table; `GRANT SELECT` to `account users`; `SHOW GRANTS` to verify
8. **M8 — Prove it (≈5 min):** run all validation queries; open the gold table's lineage and trace back to the returns volume

**Starter Code**

```sql
USE CATALOG workspace;
USE SCHEMA lab1_<yourname>;

-- M2 starter
CREATE TABLE IF NOT EXISTS returns_bronze (
  return_id STRING, order_id STRING, return_date STRING,
  quantity_returned STRING, reason STRING,
  _ingested_at TIMESTAMP
);
-- COPY INTO ... (you know this)

-- M3 hint-shaped starter: two CTAS from the same cleaned CTE-style query,
-- split by whether order_id matches sales_silver
-- (anti-join idiom from Week 2, Slide 10)

-- M4 starter: gross from sales_silver, returned via a join, then the difference
-- M6: reuse the Week 3 notebook pattern (widgets for target_schema)
```

**Expected Solution**

```sql
-- M2
COPY INTO returns_bronze
FROM (SELECT *, current_timestamp() AS _ingested_at
      FROM '/Volumes/workspace/lab1_<yourname>/landing/returns_incoming/')
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');

-- M3
CREATE OR REPLACE TABLE returns_silver AS
SELECT DISTINCT
  r.return_id,
  r.order_id,
  CAST(r.return_date AS DATE)        AS return_date,
  CAST(r.quantity_returned AS INT)   AS quantity_returned,
  r.reason
FROM returns_bronze r
WHERE r.order_id IN (SELECT order_id FROM sales_silver);

CREATE OR REPLACE TABLE returns_quarantine AS
SELECT DISTINCT r.*
FROM returns_bronze r
WHERE r.order_id NOT IN (SELECT order_id FROM sales_silver);

-- M4
CREATE OR REPLACE TABLE net_revenue_daily
CLUSTER BY (store, order_date)
AS
WITH returned AS (
  SELECT s.store, s.order_date,
         SUM(r.quantity_returned * s.unit_price) AS returned_amount
  FROM returns_silver r
  JOIN sales_silver s ON r.order_id = s.order_id
  GROUP BY s.store, s.order_date
),
gross AS (
  SELECT store, order_date, SUM(line_total) AS gross_revenue
  FROM sales_silver
  WHERE store IS NOT NULL
  GROUP BY store, order_date
)
SELECT g.store, g.order_date,
       g.gross_revenue,
       COALESCE(rt.returned_amount, 0)                      AS returned_amount,
       ROUND(g.gross_revenue - COALESCE(rt.returned_amount, 0), 2) AS net_revenue
FROM gross g
LEFT JOIN returned rt
  ON g.store = rt.store AND g.order_date = rt.order_date;

-- M5
ALTER TABLE returns_silver ADD CONSTRAINT positive_return CHECK (quantity_returned > 0);

-- M7
CREATE OR REPLACE VIEW net_revenue_summary AS
SELECT store, SUM(net_revenue) AS total_net FROM net_revenue_daily GROUP BY store;
GRANT SELECT ON VIEW net_revenue_summary TO `account users`;
SHOW GRANTS ON VIEW net_revenue_summary;
```

**Validation Checks**

```sql
-- M2: bronze has 13 rows (incl. the R007 duplicate); rerun COPY INTO → 0 new
SELECT COUNT(*) FROM returns_bronze;                           -- 13

-- M3: silver deduped AND quality-gated; quarantine caught the orphan
SELECT COUNT(*) FROM returns_silver;                           -- 11
SELECT order_id FROM returns_quarantine;                       -- 2001 (no such sale)
SELECT return_id, COUNT(*) FROM returns_silver
GROUP BY return_id HAVING COUNT(*) > 1;                        -- 0 rows (R007 deduped)

-- M4: net never exceeds gross; clustering applied
SELECT COUNT(*) FROM net_revenue_daily WHERE net_revenue > gross_revenue;  -- 0
DESCRIBE DETAIL net_revenue_daily;                             -- clusteringColumns = [store, order_date]

-- M5: constraint rejects (expected FAILURE = pass)
INSERT INTO returns_silver VALUES ('R999','1001',current_date(),-1,'test');

-- M6: job run page shows 2 tasks green; trigger paused
-- M8: lineage tab on net_revenue_daily traces to returns_incoming
```

**Stretch Task**
Design (markdown only, no build): a **returns-rate alert** — when any store's daily returned_amount exceeds 20% of gross, someone should know. Which pieces do you reach for? (Expected sketch: a SQL task or alert on a threshold query, run as a third job task depending on `build_net_revenue`, with an email notification — every component is Week 3 material.) Second stretch: should `returns_quarantine` rows ever *re-enter* silver, and what statement would do it once the order data arrives? (MERGE, after the orphan's order lands.)

**Instructor Notes**
- M3 is where the hour is won or lost: the design decision (quarantine vs. WHERE-drop vs. constraint) is the capstone's pedagogical core — when circulating, ask "where did the orphan go?" and let silence do the teaching
- The R007 duplicate and order 2001 are the planted traps; learners whose silver shows 12–13 rows missed one
- M4's subtlety: returns valued via the join to sales (the order's price) — learners who guess a price column in returns will hit the missing-column wall and re-read; that's intended
- M6 reusers of Week 3 notebooks finish fast; hand-rollers may need the hint card; both paths are valid
- Pairs are fine for the workspace-state unlucky; keep solo where possible — exam conditions
- Hint cards (post collapsed/folded): **H-M3:** "Week 2, Slide 10: the anti-join idiom — two tables from one source, split by IN / NOT IN." **H-M4:** "Returns don't know prices. Who does?" **H-M6:** "Your Week 3 job already does half of this — clone the pattern, not the work."

---

## 6. In-Class Activity

### Activity: Mock-Exam Review — Learner-Driven Question Autopsies

**Time needed:** 30 minutes (the session's review block)

**Setup**
Mock domain-score tallies from the warm-up on screen; the 2–3 weakest domains chosen; 8–10 questions pulled from those domains via the answer key's domain map. The autopsy method (Slide 4) visible. A "rules wall" (whiteboard/shared doc) ready.

**Instructions**
One learner drives each question: stem aloud → forcing constraint → eliminate in confidence order → name distractor types → state the one-sentence rule. Instructor referees, corrects gently, keeps 3-minute pace. Everyone else votes (hands/chat) *before* the driver eliminates — public commitment makes wrong instincts visible and fixable.

**Scenario**
The questions themselves — drawn live from the instructor-only mock exam based on the cohort's actual misses.

**Learner deliverable**
The rules wall: 8–10 one-sentence rules in the cohort's own words, photographed/shared at session end — their collective last-week crib sheet.

**Debrief answer**
Per question, in the mock's answer key (domain-mapped, one-line explanations).

**Teaching points**
- Public voting before elimination surfaces the *distribution* of error — when half the room picks the same wrong option, that distractor type gets named and added to the wall with a star
- Watch for constraint-blindness (answering the question they expected, not the one asked) — the most common pattern at this stage; the fix is the read-aloud discipline itself
- If a question survives elimination with two options standing, teach the tiebreaker: prefer the more *specific-to-the-stem* option over the more *generally true* one

---

## 7. Markdown Mash Practice Quiz

**This week's quiz is the instructor-only full mock exam** (45 questions, blueprint-weighted: 3 Platform / 9 Ingestion / 10 Transformation / 7 Jobs / 4 CI/CD / 5 Troubleshooting / 7 Governance, with a domain-mapped answer key).

Usage:
- **Before class (required):** instructor releases the mock as a timed event (90:00), closed-book, one sitting; learners self-score per domain
- **In class:** the review block autopsies questions from the cohort's weakest domains
- **After class:** retake *missed questions only* on Day 5 of the final-week plan

---

## 8. Exam Tips for This Week

**What the exam is likely to test**
Everything — but your *mock breakdown* now matters more than any generic list. Remediate domains scoring under ~70% first; polish 70–85% domains second; leave 85%+ domains alone until the final-day skim.

**Keywords to recognize instantly**
The seven one-liners (Slide 5) are the compressed keyword map. If any line needs a second read, that domain gets docs time this week.

**Common traps (the course-wide top eight, one last time)**
- DROP semantics swapped (managed vs. external)
- CTAS with a column-type list (invented syntax)
- "Rerunning COPY INTO duplicates data" (false) and `df.union()` dedupes (false)
- Repair run "re-executes everything" (false — failed + downstream only)
- deploy ≠ run; PR lives in the provider
- REVOKE as a blocker (DENY is the blocker); owners exempt from masks (they're not)
- VACUUM for speed / OPTIMIZE for storage (swapped purposes)
- The most powerful tool over the simplest sufficient one

**How to eliminate wrong answers**
The autopsy method, now automatic: forcing constraint → kill invented syntax → kill constraint-violators → prefer stem-specific over generally-true. Two minutes per question; flag and move at 90 seconds of uncertainty.

**Memorize (final pass)**
Privilege chain; CLI verbs; bundle blocks; trigger trio; time-travel syntax; COPY INTO + Auto Loader skeletons; MERGE skeleton; the four tuning parameters; `CLUSTER BY`.

**Understand conceptually (final pass)**
Idempotency end-to-end; bronze-absorbs/silver-enforces; managed-tables-unlock-automation; before/during failure triage; one-table-vs-fleet governance.

---

## 9. Homework / Self-Study

**The final-week plan (from Slide 7) — prescriptive:**
- **Day 1–2:** weakest domain — official docs for that domain's keywords + redo that week's lab from a blank notebook
- **Day 3–4:** second-weakest — same treatment + retake that week's quiz cold (target: 90%+)
- **Day 5:** retake all *missed* mock questions; review the rules wall photo; re-read the official exam-guide outline top to bottom — 30 seconds of explanation per bullet, out loud
- **Day 6:** rest, or the seven one-liners only; prep the exam environment (ID, room, network, system check re-run)
- **Day 7:** exam. Two minutes a question. Flag and move. Answer everything.

**Logistics checklist**
- [ ] Exam booked at webassessor.com/databricks
- [ ] Kryterion system check passed on the actual exam machine
- [ ] ID valid; testing room plan (or test-center directions)
- [ ] Result-sharing plan with the cohort channel (within NDA)

**Optional confidence builders**
- Rebuild the capstone in a fresh schema in under 30 minutes
- The official exam guide's five retired sample questions — all five, with full autopsies, no notes

---

## 10. Instructor Preparation Checklist

**Before class (day before)**
- [ ] Build the complete capstone solution in your workspace; run every validation query; screenshot the lineage graph
- [ ] Verify counts: bronze 13 / silver 11 / quarantine shows order 2001 / net ≤ gross everywhere
- [ ] Distribute `week5_returns.csv` + remind learners: mock taken, scored by domain, breakdown in hand
- [ ] Print/prepare hint cards (H-M3, H-M4, H-M6) and the milestone time-checkpoint list
- [ ] Pre-select 3 autopsy questions for Part 2 of the demo + a shortlist of ~15 review candidates spanning all domains (you'll filter live by the cohort's tallies)
- [ ] Set up the rules wall (whiteboard or shared doc)

**Workspace objects needed**
- Your completed capstone in `week1_demo` (the walkthrough artifact)
- All prior-week objects (the capstone depends on `sales_silver`)
- Screenshot kit: finished lineage graph, job run page, validation outputs

**Demo rehearsal**
- [ ] Time the solution walkthrough at 15 minutes against the finished build — milestone time-boxes of 90 seconds each
- [ ] Rehearse the three autopsies aloud — the modeling quality here determines the review block's quality
- [ ] Prepare your "mistakes I saw" slot structure (you'll fill content live while circulating)

**Backup plans**
- **Learners' prior-week objects missing:** publish a `rebuild_prereqs.sql` script (CTAS sales_silver from the Week 1 CSV + corrections — assemble it from the Week 2 solution) and have victims run it during Slide 2–3; pairs as the fallback
- **Capstone collapses time-wise (cohort-wide):** call it at M4, walk M5–M8 in the debrief, and extend the review block — the review serves the exam more directly
- **Mock not taken by many:** flip the order — run 6–8 instructor-picked autopsies as the "mock highlights" first (cold voting works even unprepared), capstone second with M6–M8 as homework
- **Total outage:** the review block + autopsies + rules wall + final-week planning fill 2 hours fully offline with the mock PDF/printout; capstone becomes the final homework with validation queries as proof

---

*Course complete. Files: `00_Curriculum_Map.md` · Weeks 1–5 · instructor-only mock · `datasets/` · `notebooks/` · `cicd/databricks.yml`.*
