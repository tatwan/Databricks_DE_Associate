# Week 4: Governance and Security + Troubleshooting and Optimization (+ Exam Strategy)

> Aligned to the **May 4, 2026** Databricks Certified Data Engineer Associate exam guide.
> Primary exam domains: **Governance and Security** (15%, full coverage) + **Troubleshooting, Monitoring, and Optimization** (10%, the performance half — run-history monitoring was Week 3).
> Last new content of the course. Ends with exam strategy; the instructor releases the full mock as a timed event before Week 5 and reviews it in class.

---

## 1. Session Overview

- **Duration:** 2 hours
- **Target audience:** Same cohort; Weeks 1–3 completed
- **Prerequisites:**
  - Week 2–3 objects intact: `sales_silver` in `lab1_<name>`, `week2_customers.json` still in the landing volume
  - Comfort with `DESCRIBE EXTENDED` and three-level names (used constantly today)
- **Main exam domains covered:**
  - Domain 7: Governance and Security — managed/external operations, GRANT/REVOKE/DENY, principals, row filters and column masks, ABAC, plus carry-over governance topics (lineage, audit logs, Delta Sharing, Lakehouse Federation)
  - Domain 6: Troubleshooting, Monitoring, and Optimization — Spark UI bottlenecks (skew/shuffle/spill), Liquid Clustering, predictive optimization, cluster/library/OOM diagnosis, tuning parameters (returning from Week 2's cameo)
- **Learning objectives.** By the end of this session, learners can:
  1. Apply `GRANT`, `REVOKE`, and `DENY` to principals (users, groups, service principals) at the right level of the securable hierarchy, and explain the USE CATALOG → USE SCHEMA → SELECT privilege chain
  2. Perform managed/external table operations and describe conversion between them
  3. Implement column masks and row filters with SQL UDFs, and explain when ABAC policies are the better answer
  4. Locate lineage in Catalog Explorer and state where audit logs live; describe Delta Sharing types and Lakehouse Federation use cases
  5. Read Spark UI / query-profile symptoms: skew, shuffle, spill — and name the first remedy for each
  6. Explain Liquid Clustering (`CLUSTER BY`) vs. partitioning/Z-order, and what predictive optimization automates
  7. Diagnose cluster startup failures, library conflicts, and OOM errors from their signatures
  8. Execute an exam plan: pacing, flagging, elimination, and SQL-first reading

---

## 2. Recommended Timing

| Time      | Segment                      | Purpose                     |
| --------- | ---------------------------- | --------------------------- |
| 0:00–0:08 | Warm-up: Week 3 retrieval (CLI verbs, repair semantics, trigger types) | Activate; these reappear in today's quiz |
| 0:08–0:45 | Concept slides (16 slides)   | Governance stack, masking/ABAC, sharing, Spark UI, clustering, exam strategy |
| 0:45–1:10 | Instructor demo              | GRANTs live, mask + row filter on real data, lineage, CLUSTER BY + query profile |
| 1:10–1:40 | Hands-on lab                 | Secure and optimize the BrewMart lakehouse |
| 1:40–1:50 | In-class activity            | "Diagnose the bottleneck" symptom cards |
| 1:50–2:00 | Markdown Mash quiz + mock-exam assignment | Exam readiness; schedule the instructor-released timed mock |

---

## 3. Slide Deck Content

### Slide 1: Recap and Today's Map — Lock It Down, Speed It Up

**Key bullets**
- Weeks 1–3 built and productionized a pipeline; today: who may see what (governance) and why is it slow (optimization)
- Domain 7 (15%) + the rest of Domain 6 (10%) — today closes all seven exam domains
- These are the two most *under-studied* domains: engineers practice pipelines, not permissions
- Tonight: the full 45-question timed mock goes home with you

**Speaker notes**
Quick Week 3 retrieval first (validate/deploy/run; what repair reruns; the three trigger types). Then reframe: everything so far assumed you could see all the data — real organizations don't work that way, and neither does the exam. Sell the stakes: governance questions are word-precise (GRANT vs DENY, managed vs external) — easy points if studied, coin-flips if not.

**Visual suggestion**
Course strip with all 7 domain badges now colored; a padlock + speedometer icon pair for today.

**Exam relevance**
Closes the blueprint; flags the under-studied domains.

**Common misconception**
"Governance is an admin's job, not an engineer's exam topic." It's 15% of *your* exam.

---

### Slide 2: The Securable Hierarchy and the Principals

**Key bullets**
- Securables: metastore → catalog → schema → table/view/volume/function/model (+ external locations, shares, connections)
- Privileges **inherit downward**: a grant on a catalog flows to its schemas and tables
- Principals: **users** (people), **groups** (memberships — grant to these!), **service principals** (machine identities for jobs/CI)
- Ownership matters: the owner (or higher-level admin) can grant; `GRANT` requires authority over the object

**Speaker notes**
Re-draw the Week 1 tree, now with locks on every node. Inheritance is the load-bearing idea: granting SELECT on a *schema* covers all current and future tables in it — exactly the official sample-question pattern. Hammer the group habit: grants to individuals don't scale and exam answers favor groups. Service principals get a full sentence: they're what your Week 3 CI/CD story authenticates as — jobs in prod should run as service principals, not as Dave.

**Visual suggestion**
The UC tree with a lock per level and an inheritance arrow flowing down; three principal cards (user/group/service principal) with one-line "use for."

**Exam relevance**
Verbatim: "applying GRANT, REVOKE, and DENY privileges to principals (users, groups, and service principals) at appropriate levels of the security hierarchy."

**Common misconception**
That granting on a table is the "safest default." Level choice is a design decision — schema-level grants with inheritance are often the intended exam answer for team access.

---

### Slide 3: GRANT, REVOKE, DENY — and the Privilege Chain

**Key bullets**
- `GRANT SELECT ON SCHEMA s TO group;` / `REVOKE SELECT ON ...` / `SHOW GRANTS ON ...`
- To query a table you need the **chain**: `USE CATALOG` + `USE SCHEMA` + `SELECT`
- Common privileges: SELECT, MODIFY, CREATE TABLE, USE CATALOG/SCHEMA, EXECUTE, READ/WRITE VOLUME, ALL PRIVILEGES
- **DENY** explicitly blocks — it wins over any GRANT (even via group membership); REVOKE merely removes a prior grant

**Speaker notes**
Run the official sample question live (analysts need read-only on a schema; they already have USE on catalog+schema): `GRANT SELECT ON SCHEMA sales_data TO analysts` — and explain why `ALL PRIVILEGES` (over-grant), `INSERT` (write), and the per-table option (unnecessary; schema-level inherits) lose. The DENY/REVOKE distinction is pure exam: REVOKE undoes *your* grant; DENY overrides *everything* including group-inherited access. The chain explains the classic support ticket: "I have SELECT but can't query" → missing USE CATALOG/SCHEMA.

**Visual suggestion**
A door with three locks labeled USE CATALOG / USE SCHEMA / SELECT; a side box showing GRANT (+), REVOKE (–), DENY (⛔ trumps all).

**Exam relevance**
Verbatim objective; the GRANT-on-schema pattern is literally official sample Question 2.

**Common misconception**
"REVOKE and DENY do the same thing." A user can still see data after a REVOKE (via another group's grant); DENY closes that path.

---

### Slide 4: Managed vs. External — The Operations Edition

**Key bullets**
- Week 1 gave the concept; the exam objective adds **operations**: create, modify, delete, **convert**
- DROP managed = data gone (recoverable ~briefly: `UNDROP TABLE`); DROP external = metadata only
- Conversion exists: external→managed (and managed→external) via `ALTER TABLE ... SET MANAGED`-style operations / rebuild patterns — know that it's *possible and directional*, not the exact syntax
- Why Databricks pushes managed: predictive optimization, automatic layout/lifecycle, faster defaults

**Speaker notes**
Mostly reinforcement — quiz the room cold on DROP semantics both ways; they should be instant by now. New material: `UNDROP TABLE` (managed tables are recoverable within a retention window) and the existence of conversion. Be honest about depth: the associate exam wants you to know conversion is possible and what changes (who manages the files); memorizing evolving syntax is low-yield. The "why managed" list connects to Slide 11 (predictive optimization is managed-tables-only) — plant that seed now.

**Visual suggestion**
The Week 1 side-by-side panel, now with two new arrows: UNDROP (managed, clock icon) and a convert arrow between the panels.

**Exam relevance**
Verbatim: "Differentiate between managed and external tables … perform basic operations (create, modify, delete, and convert between managed and external tables)."

**Common misconception**
"Managed table drops are instantly unrecoverable." UNDROP exists within the retention window — a tested nuance precisely because it surprises people.

---

### Slide 5: Column Masks and Row Filters — Security Inside the Table

**Key bullets**
- Both are SQL UDFs bound to a table — policy lives with the data, applies to every query path
- **Column mask:** function rewrites a column's value per user — `ALTER TABLE t ALTER COLUMN email SET MASK mask_fn;`
- **Row filter:** boolean function decides row visibility — `ALTER TABLE t SET ROW FILTER filter_fn ON (store);`
- Inside the functions: `is_account_group_member('group')` branches by audience; non-members see masked/filtered results

**Speaker notes**
The pattern is two steps, always: CREATE FUNCTION, then ALTER TABLE to bind it. Walk one mask example line by line (the demo repeats it on real data): members of `support_team` see real emails, everyone else sees `***@domain`. Then the row filter: returns true → row visible. Sell the architectural point the exam rewards: this beats making 15 filtered views because there's *one* table and the policy can't be bypassed by querying the base object. Note who's exempt: nobody by default — even owners see masked data unless the function says otherwise (great demo moment).

**Visual suggestion**
One table, two users querying: user A (in group) sees full rows/emails; user B sees fewer rows and starred emails — same `SELECT *`.

**Exam relevance**
Verbatim: "Understand column-level masking and row-level security to restrict data visibility based on user groups."

**Common misconception**
"Masking changes the stored data." It rewrites at *query time*; storage is untouched — and table owners are NOT automatically exempt.

---

### Slide 6: ABAC — Governance That Scales by Tags

**Key bullets**
- Problem: 4,000 tables with PII columns — per-table masks don't scale
- **ABAC (attribute-based access control):** tag data (`pii_email`, `region=EU`), write **policies** against tags, applied centrally
- Policies deliver row filtering and column masking automatically wherever the tag appears
- Mental model: masks/filters = per-table mechanism; ABAC = fleet-wide policy engine using the same machinery

**Speaker notes**
Keep it conceptual and honest: **"Exam concept; requires admin/advanced workspace — concept only in this course."** The exam objective is "understand," and the discriminator question is scale: one sensitive table → mask/filter directly; "hundreds of tables, central security team, consistent policy" → ABAC. Tags + policies + inheritance down the hierarchy is the whole story at associate level. Fabric/Purview folks will recognize sensitivity-label thinking — the reflex maps well.

**Visual suggestion**
Many table icons, three tagged `PII`; one policy box with arrows fanning to all tagged tables: "tag once, police everywhere."

**Exam relevance**
Verbatim: "Understand Unity Catalog ABAC policies to centrally control row-level filtering and column masking for sensitive data."

**Common misconception**
ABAC as a *third* unrelated mechanism. It's the central management layer that applies the same row-filter/column-mask effects — by tag instead of by table.

> **Exam concept; may require paid workspace or admin access for full hands-on practice.**

---

### Slide 7: Lineage and Audit Logs — Who Made It, Who Touched It

**Key bullets**
- **Lineage:** UC captures table- and column-level lineage automatically across SQL, notebooks, jobs, pipelines — Catalog Explorer → table → Lineage tab
- Use cases: impact analysis ("what breaks if I change silver?"), root cause ("where did this bad column come from?"), compliance
- **Audit logs:** who did what, when — delivered via **system tables** (`system.access.audit`) queryable in SQL
- Lineage = data flow; audit = user actions; both UC-native

**Speaker notes**
Demo shows lineage live on `sales_silver` — three weeks of pipeline history drawn automatically; no agent, no manual registration (that's the differentiator vs. their Purview experience). For audit logs, the exam's old-guide objective was "identify how audit logs are stored" — the answer shape: system tables in the `system` catalog, queryable with plain SQL (`system.access.audit`). **Free Edition: system-table access may be restricted — show the query shape on the slide regardless.**

**Visual suggestion**
Split: left, a lineage graph (volume → bronze → silver → view, with a job node); right, a 3-row mock of `system.access.audit` (user, action, object, time).

**Exam relevance**
Both named in the current guide's governance section ("Use lineage features in Unity Catalog", "Identify how audit logs are stored") — carried as governance knowledge into the new exam.

**Common misconception**
That lineage needs manual registration or a scanner. UC builds it from actual query execution automatically.

---

### Slide 8: Delta Sharing and Lakehouse Federation — Data Beyond the Workspace

**Key bullets**
- **Delta Sharing:** open protocol to share live data **without copying**; two flavors — **Databricks-to-Databricks** (recipient has UC: easy, governed, full features) and **open sharing** (recipient uses the protocol from any tool: pandas, Power BI, Spark)
- Provider creates a **share** (tables added to it) → grants a **recipient** access; recipient queries live data
- Cost nuance: cross-region/cross-cloud sharing can incur egress — a named exam consideration
- **Lakehouse Federation:** query *external* databases (Postgres, Snowflake, SQL Server…) through UC **without ingesting** — connection + foreign catalog; great for exploration/light access, not for heavy repeated ETL

**Speaker notes**
Two "data without copying" features — opposite directions: Sharing exports your tables outward; Federation imports queryability inward. Exam discriminators: "share with a partner who doesn't use Databricks" → open sharing; "both sides on Databricks" → D2D; "query the operational Postgres without building a pipeline" → Federation. The egress-cost point is verbatim in the guide ("Analyze the cost considerations of data sharing across clouds") — one sentence: same-region sharing is cheap; cross-cloud moves bytes and bills. **Both: "Exam concept; admin setup required — concept only."**

**Visual suggestion**
Compass diagram: your metastore in the center; Delta Sharing arrows pointing out (to a Databricks logo and a generic-tools logo); a Federation arrow pointing in from external DB icons.

**Exam relevance**
Four named guide objectives: Delta Sharing usage, advantages/limitations, D2D vs. external types, cross-cloud cost; plus "Identify use cases of Lakehouse Federation."

**Common misconception**
"Delta Sharing emails a copy of the data." No copy — recipients read the live table via the protocol; that's the entire advantage (and why egress matters).

> **Exam concept; may require paid workspace or admin access for full hands-on practice.**

---

### Slide 9: The Optimization Story Starts With Files

**Key bullets**
- A Delta table's speed is largely its **file layout**: many tiny files = slow (open/list overhead); a few giant files = poor pruning/parallelism
- **OPTIMIZE table** — compacts small files into well-sized ones
- **VACUUM table** — deletes files no longer referenced (old versions) past retention; reclaims storage, *limits time travel*
- Reading questions: streaming/frequent small appends → small-files problem → OPTIMIZE

**Speaker notes**
Bridge from governance to performance with the physical truth: tables are files (Week 1's `_delta_log` slide pays off). Explain *why* small files hurt — per-file overhead and scheduling, not row count. VACUUM closes the loop opened in Week 1: this is the command that bounds time travel; default retention 7 days, and shortening it has consequences. Both commands are exam-recognizable even where automation (next two slides) runs them for you.

**Visual suggestion**
Two shelves: one crammed with 500 tiny boxes vs. one with 8 medium boxes; OPTIMIZE arrow between them; a trash chute labeled VACUUM with a "time travel horizon" warning sign.

**Exam relevance**
Foundation for Liquid Clustering and predictive optimization questions; VACUUM/time-travel interaction is classic exam bait.

**Common misconception**
"VACUUM makes queries faster." It reclaims storage and trims history; OPTIMIZE is the query-speed command. Swapping them is a standard distractor.

---

### Slide 10: Liquid Clustering — Layout Without the Partition Pain

**Key bullets**
- `CREATE TABLE t (...) CLUSTER BY (store, order_date)` — clusters data by columns for file-skipping
- Replaces both **Hive-style partitioning** (rigid directories; cardinality traps; can't change cheaply) and **Z-ORDER** (requires manual re-runs, fixed at OPTIMIZE time)
- Liquid advantages: choose/change keys without rewriting the table (`ALTER TABLE ... CLUSTER BY`), handles high-cardinality and skew, incremental
- `CLUSTER BY AUTO` — let Databricks pick keys from query patterns (ties into predictive optimization)

**Speaker notes**
This is the modern answer the May 2026 guide names (the older partitioning/Z-order obsession is legacy context). Give partitioning two sentences of respect — it still appears in older codebases and as a distractor: partitioning by a high-cardinality column (like order_id) is the famous anti-pattern that creates the small-files problem. Then the pitch: liquid clustering gets the file-skipping benefit with none of the directory rigidity, and keys are *changeable*. Exam discriminator: any stem featuring "evolving query patterns," "high cardinality," or "without rewriting" → Liquid Clustering.

**Visual suggestion**
Three-column timeline: Partitioning (rigid folders) → Z-ORDER (manual re-sort cycles) → Liquid Clustering (fluid clusters, swap-keys arrow), with a "current exam answer" stamp on the third.

**Exam relevance**
Verbatim Domain 6: "Understand the features of Liquid Clustering and predictive optimization."

**Common misconception**
"Liquid clustering is just Z-order renamed." Different machinery and contract: incremental, key-changeable, no manual OPTIMIZE ZORDER cycles.

---

### Slide 11: Predictive Optimization — Maintenance on Autopilot

**Key bullets**
- Databricks runs **OPTIMIZE / VACUUM / layout decisions automatically** based on observed usage — no schedules to write
- Works on **Unity Catalog managed tables** (a big reason "managed" is the recommendation)
- AI-driven: prioritizes tables where maintenance yields real query/cost benefit
- Requires Premium+ — **"Exam concept; not exercisable in Free Edition"**

**Speaker notes**
Short slide, high yield. The exam shape: "Which feature removes the need for manually scheduled OPTIMIZE jobs?" → predictive optimization. Connect the threads: managed tables (Slide 4) + liquid clustering AUTO (Slide 10) + this = the "Databricks runs your table maintenance" story — that's the Data Intelligence Platform pitch from Week 1, Slide 3, now concrete. Be precise on scope: managed tables, UC, paid tiers.

**Visual suggestion**
A robot with a wrench standing over a tables shelf; checklist items OPTIMIZE/VACUUM/clustering being ticked automatically; a "managed tables only" gate.

**Exam relevance**
Named in the same Domain 6 objective as Liquid Clustering; also reinforces Domain 1 ("enable features that simplify data layout decisions").

**Common misconception**
"Predictive optimization tunes my queries." It maintains *tables* (layout, files, history) — query tuning is still Spark's and your job.

---

### Slide 12: Reading the Spark UI — Skew, Shuffle, Spill

**Key bullets**
- Entry: job/query → stages → tasks; start with the longest stage and its **task-duration distribution**
- **Skew:** a few tasks run far longer (uneven key distribution) — max ≫ median task time
- **Shuffle:** wide ops (joins, groupBy) move data between executors — big "Shuffle Read/Write" = expensive boundary
- **Spill:** memory overflow written to disk ("Spill (Memory/Disk)" metrics) — partitions too big / memory too small
- Remedies map: skew → better keys/broadcast/AQE; shuffle → broadcast small side, prune early; spill → more partitions or memory

**Speaker notes**
Teach it as symptom → metric → first remedy, three rows, that's the slide. The exam gives you a described Spark UI ("one task took 40 minutes, the median was 2") and wants the word: *skew*. Connect to Week 2's broadcast join: that was shuffle-avoidance — now they see what it avoided. In serverless-first environments learners may use the **query profile** view (SQL warehouse) more than the classic Spark UI; same concepts, friendlier rendering — the demo uses it. Stage-level metrics is the verbatim objective phrase.

**Visual suggestion**
Three mini bar charts of task durations: skew (one giant bar), healthy, and a spill panel with memory overflowing into a disk icon; remedy arrows under each.

**Exam relevance**
Verbatim: "Identify common performance bottlenecks such as data skew, shuffling, and disk spilling by interpreting stage-level metrics in the Spark UI."

**Common misconception**
"Shuffle is a bug to eliminate entirely." Wide operations *require* shuffles; the skill is minimizing and right-sizing them, not zeroing them.

---

### Slide 13: The Four Tuning Parameters (Week 2's Cameo, Promoted)

**Key bullets**
- `spark.sql.shuffle.partitions` — number of partitions *after* a shuffle (too few → huge partitions/spill; too many → tiny-task overhead)
- `spark.default.parallelism` — default parallelism for low-level RDD ops
- `spark.executor.memory` / `spark.driver.memory` — memory per executor / driver (spill & OOM lever)
- `spark.sql.autoBroadcastJoinThreshold` — max table size Spark auto-broadcasts (~10MB default)
- Modern reality: AQE and serverless tune much of this — the exam wants you to know **what each knob influences**

**Speaker notes**
These four are listed by name in the exam outline — that makes them memorization targets. One line each, tied to the previous slide's symptoms: spill → shuffle.partitions or executor.memory; missed broadcast → autoBroadcastJoinThreshold; driver OOM on a big collect → driver.memory. Then the honest caveat: on serverless you mostly *can't* set these — Databricks does — which is itself an exam-friendly fact (serverless = auto-optimized). "Re-measure after changing" is in the objective wording: tuning is empirical, not faith-based.

**Visual suggestion**
Four labeled dials, each wired to the symptom it treats (spill, parallelism, OOM, broadcast).

**Exam relevance**
Verbatim Domain 3 objective: "Understand the basic tuning parameters … and re-measure the performance."

**Common misconception**
"Crank shuffle partitions higher = faster." Each setting has a too-far failure mode; the exam tests the *direction* of the trade-off, not magic numbers.

---

### Slide 14: When It Won't Even Start — Clusters, Libraries, OOM

**Key bullets**
- **Cluster startup failures:** cloud capacity, permissions/quota, bad init scripts — check the cluster **event log**; signature: failure *before any task runs*
- **Library conflicts:** install errors or version clashes (e.g., two pandas pins) — signature: import/`ModuleNotFound`/resolver errors at session start; fix: align versions, prefer notebook-scoped installs
- **Driver vs. executor OOM:** driver OOM ← big `collect()`/`toPandas()`; executor OOM ← oversized partitions, skew, giant joins
- Triage question #1: did it fail **before** work started (infra/library) or **during** (data/memory)?

**Speaker notes**
The exam objective is verbatim: "Diagnose cluster startup failures, library conflicts, and out-of-memory issues." Teach the before/during split as the master key — it sorts nearly every troubleshooting stem. Give each failure its one-line signature and its first place to look (event log / library UI & error text / Spark UI + stderr). The driver-vs-executor OOM distinction is the subtlest: `collect()` pulling 50M rows kills the *driver* — a question shape they should recognize instantly. Free Edition note: learners won't see classic cluster failures on serverless — **concept slide, real exam points.**

**Visual suggestion**
Decision tree: "Failed before any task?" → infra (capacity/init/library) vs. "Failed mid-job?" → data/memory (skew/spill/OOM), with the three exam failure types placed on the branches.

**Exam relevance**
Verbatim Domain 6 objective — typically 1–2 questions.

**Common misconception**
Treating every failure as a code bug. Startup and library failures happen before your code runs — rereading the notebook won't find them.

---

### Slide 15: Exam Strategy — How to Take This Exam

**Key bullets**
- 45 scored questions / 90 minutes = **2 min/question**; first pass fast, flag and move on (unscored experimental items may also appear — don't let a bizarre question rattle you)
- Read the stem for the **forcing constraint** (you've drilled this for 4 weeks); kill invented syntax first, then misapplied-real-features
- Code is SQL when possible, Python otherwise — read PySpark calmly: find the aliases, the counted column, the join keys
- No test aides; online proctored or test center; passing is scaled — answer everything (no penalty for guessing)

**Speaker notes**
Make the math vivid: at 2 minutes each, a question that's eaten 4 minutes owes you two flags. Recommend the three-pass method: pass 1 answer everything answerable in <90s; pass 2 the flagged; pass 3 sanity-sweep. Remind them of the distractor taxonomy they've now seen in 4 quizzes: invented syntax, real-feature-wrong-job, old-name bait, over-powered tool. Logistics: Kryterion online proctoring needs a webcam, clean desk, system check beforehand — do the system check this week, not exam morning.

**Visual suggestion**
A 90-minute clock split into three passes; the four distractor types as "wanted posters."

**Exam relevance**
Direct — strategy is worth several questions' margin for a prepared candidate.

**Common misconception**
"Hard questions early mean I'm failing." Question order is random and some items are unscored — early difficulty signals nothing.

---

### Slide 16: Wrap-Up — All Seven Domains Closed

**Key bullets**
- You can now: govern it (GRANT/mask/filter), share it (Delta Sharing), diagnose it (Spark UI), and maintain it (clustering/PO)
- Tonight: the full 45-question, 90-minute mock — take it **timed, closed-book, one sitting**
- Bring your domain-level score breakdown to Week 5; the capstone and review target *your* weak areas
- Week 5: end-to-end capstone + mock review + final readiness checklist

**Speaker notes**
Set mock rules explicitly: simulate the real thing — timer on, notes away, no pausing; the score matters less than the per-domain diagnosis. Collect a quick pulse: which domain do they *feel* weakest in (usually CI/CD or governance) — tell them Week 5's review flexes toward the room's actual results. End on momentum: every exam topic has now been taught; what remains is integration and reps.

**Visual suggestion**
Seven domain badges all stamped ✓; a mock-exam ticket graphic with "timed · closed-book · one sitting" rules.

**Exam relevance**
Launches the most predictive prep activity of the course.

**Common misconception**
—

---

## 4. Instructor Demo

### Demo: Lock It, Mask It, Trace It, Cluster It

**Goal**
Make governance and optimization tangible on the BrewMart data: live GRANT/REVOKE with SHOW GRANTS, a column mask and a row filter that visibly change query results *for the owner*, automatic lineage across three weeks of pipeline, and Liquid Clustering + a query-profile read.

**Setup**
- Free Edition; SQL editor or notebook on serverless
- `workspace.week1_demo` objects from Weeks 1–3 (esp. `sales_bronze_copy`/`sales_silver` equivalents); `week2_customers.json` in the `landing` volume
- A second browser tab with Catalog Explorer open (for grants UI + lineage)

> **Free Edition notes:** GRANT/REVOKE/SHOW GRANTS work on objects you own (grant to the `account users` group — it exists in every workspace). Row filters and column masks are standard UC SQL — verified in rehearsal; if your workspace blocks them, the cells double as exam-syntax walkthrough (the objective is "understand"). Lineage works in Catalog Explorer. ABAC, Delta Sharing, predictive optimization remain concept-only.

**Notebook Cells**

```sql
-- Cell 1: A table worth protecting — customers with emails
USE CATALOG workspace;
USE SCHEMA week1_demo;

CREATE OR REPLACE TABLE customers AS
SELECT customer_id, name, loyalty_tier,
       contact.email AS email,
       contact.city  AS city
FROM read_files(
  '/Volumes/workspace/week1_demo/landing/week2_customers.json',
  format => 'json');

SELECT * FROM customers ORDER BY customer_id;
```

```sql
-- Cell 2: Grants — give, inspect, take away
GRANT SELECT ON TABLE customers TO `account users`;

SHOW GRANTS ON TABLE customers;

REVOKE SELECT ON TABLE customers FROM `account users`;
SHOW GRANTS ON TABLE customers;
-- UI moment: Catalog Explorer → customers → Permissions tab = same operations, clickable
```

```sql
-- Cell 3: Column mask — two steps: function, then bind
CREATE OR REPLACE FUNCTION email_mask(email STRING)
RETURN CASE
  WHEN is_account_group_member('support_team') THEN email      -- members see real value
  ELSE regexp_replace(email, '^[^@]+', '***')                  -- everyone else: ***@domain
END;

ALTER TABLE customers ALTER COLUMN email SET MASK email_mask;

SELECT customer_id, name, email FROM customers ORDER BY customer_id;
-- We are NOT in support_team → even as OWNER we see ***@example.com
```

```sql
-- Cell 4: Row filter — boolean function, then bind
CREATE OR REPLACE FUNCTION atlanta_only(city STRING)
RETURN is_account_group_member('all_regions') OR city = 'Atlanta';

ALTER TABLE customers SET ROW FILTER atlanta_only ON (city);

SELECT customer_id, name, city, email FROM customers;
-- Row count drops: only Atlanta customers visible (we're not in all_regions)
```

```sql
-- Cell 5: Policies are removable, auditable objects
ALTER TABLE customers DROP ROW FILTER;
ALTER TABLE customers ALTER COLUMN email DROP MASK;
SELECT COUNT(*) AS all_rows_back FROM customers;
```

```sql
-- Cell 6: ⏸️ UI — Lineage (no code)
-- Catalog Explorer → week1_demo → sales_silver (or your silver table) → Lineage tab
-- Walk upstream: silver ← bronze ← volume files; note the JOB node from Week 3.
-- Click a column → column-level lineage.
```

```sql
-- Cell 7: Liquid Clustering — layout as a one-liner
CREATE OR REPLACE TABLE sales_gold_daily
CLUSTER BY (store, order_date)
AS
SELECT store, order_date,
       ROUND(SUM(line_total), 2) AS revenue,
       COUNT(DISTINCT order_id)  AS orders
FROM sales_silver
GROUP BY store, order_date;

DESCRIBE DETAIL sales_gold_daily;     -- see clusteringColumns
OPTIMIZE sales_gold_daily;            -- manual trigger today; predictive optimization's job on paid tiers
```

```sql
-- Cell 8: A query worth profiling (intentionally shuffly)
SELECT t.pickup_zip,
       COUNT(*)                          AS trips,
       APPROX_COUNT_DISTINCT(t.dropoff_zip) AS distinct_dropoffs,
       AVG(t.fare_amount)                AS avg_fare
FROM samples.nyctaxi.trips t
GROUP BY t.pickup_zip
ORDER BY trips DESC;
-- ⏸️ UI: open Query Profile (SQL editor → query history → this query → profile)
-- Find: the aggregation's shuffle, rows per operator, time per stage.
```

**Instructor Script**
1. **Cell 1:** "Real names, real emails — the kind of table that gets a company fined. Today it gets governed."
2. **Cell 2:** "GRANT to a group — `account users` is everyone in this workspace. SHOW GRANTS is your audit answer in one command. REVOKE removes my grant — and notice what it *couldn't* remove: a grant someone else made via another group. That's DENY's job, and that distinction is an exam question."
3. **Cell 3:** "Two steps, always: a function that decides, an ALTER that binds. Run the select — I am the OWNER of this table and I see starred emails. Masks don't care about your title; the function is the law. If I were in `support_team`, I'd see the real thing — same query, different user, different answer."
4. **Cell 4:** "Same trick for rows: the function returns true, you see the row. Ten customers became four — the Chicago and Dallas rows still exist on disk; they're filtered at query time. One table, many audiences, zero copies."
5. **Cell 5:** "Policies unbind as cleanly as they bind. Everything's back. In a big org you wouldn't hand-craft these per table — you'd tag columns PII and let an ABAC policy apply this everywhere. Same machinery, central trigger — that's the slide-6 story and that's all the exam needs."
6. **Cell 6 (UI):** "I never registered anything — UC drew this from actual query history. There's our Week 3 job feeding silver. Impact analysis: click downstream before you change a column. Purview users: notice nobody ran a scanner."
7. **Cell 7:** "CLUSTER BY at creation — that's liquid clustering. DESCRIBE DETAIL shows the clustering columns. No directories, no partition column to regret next quarter — and ALTER TABLE can change the keys later without rewriting. OPTIMIZE compacts now; on Premium, predictive optimization would do this for me, unasked."
8. **Cell 8:** "A groupBy over millions of taxi rows — a guaranteed shuffle. Open the profile: here's the scan, here's the exchange — that word means shuffle — rows in, rows out, time per operator. On the exam you won't click this UI; you'll read a description of it. The vocabulary you just saw — stage, shuffle, task times — is the vocabulary of those questions."

**Expected Results**
- Cell 1: 10 customers with real emails/cities
- Cell 2: grants list showing `account users` with SELECT, then without
- Cell 3: all emails rendered `***@example.com` *for you, the owner*
- Cell 4: only Atlanta customers (4 rows: C001, C002, C014 + any other Atlanta) — count visibly drops
- Cell 5: full 10 rows back
- Cell 6: lineage graph spanning volume → bronze → silver (+ job node)
- Cell 7: `clusteringColumns: ["store","order_date"]` in DESCRIBE DETAIL; OPTIMIZE returns a metrics row
- Cell 8: result set + a query profile showing scan→aggregate→exchange operators with timings

**Troubleshooting**
| Problem | Fix |
| --- | --- |
| `GRANT ... TO account users` syntax error | Backticks required: `` `account users` `` (space in principal name). |
| Mask/row-filter ALTER not permitted | Workspace tier/feature gap — switch to walkthrough mode: the syntax on screen IS the exam content; show rehearsal screenshots of the masked results. |
| Mask shows real emails to you | You're in a group named `support_team` (unlikely) — or the function edited differently; re-check the CASE branches. |
| Row filter hides ALL rows | The filter column was bound wrong: `ON (city)` must reference the city column; re-bind. |
| Lineage tab empty | Lineage builds from query activity; if the schema is fresh, run the Week 2/3 pipeline once and revisit; or show lineage on your most-used table instead. |
| `CLUSTER BY` rejected | Rare on current serverless; fall back to creating the table plain and showing the CLUSTER BY syntax + `ALTER TABLE ... CLUSTER BY (store)` discussion. |
| Query profile hard to find | SQL editor → Query history (left rail) → click the query → "Query profile." Rehearse the click-path; UI moves. |
| OPTIMIZE returns zero-effect metrics | Tiny table — nothing to compact; say so ("optimization is for real data volumes") and move on. |

---

## 5. Hands-On Lab

### Lab: Secure and Tune the BrewMart Lakehouse

**Scenario**
BrewMart hired analysts and signed a support vendor. Legal's requirements: analysts query curated data but **never see raw customer emails**; the vendor's accounts see **only their assigned store's rows**. Meanwhile the gold layer needs a layout that survives growth. You're the engineer; ship it.

**Business Problem**
Apply least-privilege access, PII masking, and row-level security to existing tables — and create a growth-ready gold table with Liquid Clustering — using only SQL.

**Tasks**
1. Build `customers` in your `lab1_<name>` schema from the customers JSON (id, name, loyalty_tier, email, city)
2. Grant `account users` SELECT on your `sales_by_store` view (Week 1); verify with `SHOW GRANTS`; then REVOKE and re-verify
3. Create + bind a column mask on `customers.email`: members of `brewmart_support` see real emails, all others see `***@<domain>`; prove it works by querying as yourself
4. Create + bind a row filter on `customers.city`: members of `brewmart_hq` see all rows, others only `'Atlanta'`; verify the row count drops
5. Create `sales_gold_daily` (revenue + orders per store per day from `sales_silver`) with `CLUSTER BY (store, order_date)`; confirm via `DESCRIBE DETAIL`; run `OPTIMIZE`
6. Open the **lineage** of `sales_gold_daily` in Catalog Explorer — screenshot or describe the upstream chain
7. Cleanup proof-of-control: DROP the row filter and mask, confirm full visibility returns

**Starter Code**

```sql
USE CATALOG workspace;
USE SCHEMA lab1_<yourname>;

-- Task 1
CREATE OR REPLACE TABLE customers AS
SELECT customer_id, name, loyalty_tier,
       contact.email AS email,
       contact.city  AS city
FROM read_files(
  '/Volumes/workspace/lab1_<yourname>/landing/week2_customers.json',
  format => 'json');

-- Task 2: GRANT / SHOW GRANTS / REVOKE  (your turn)

-- Task 3: mask function skeleton
CREATE OR REPLACE FUNCTION email_mask(email STRING)
RETURN CASE
  WHEN is_account_group_member('<which group?>') THEN email
  ELSE  -- mask expression here
END;
-- then: ALTER TABLE ... ALTER COLUMN ... SET MASK ...;

-- Task 4: row filter skeleton
-- CREATE OR REPLACE FUNCTION ... RETURN ... ;
-- ALTER TABLE ... SET ROW FILTER ... ON (...);

-- Task 5: gold with CLUSTER BY  (your turn)
```

**Expected Solution**

```sql
-- Task 2
GRANT SELECT ON VIEW sales_by_store TO `account users`;
SHOW GRANTS ON VIEW sales_by_store;
REVOKE SELECT ON VIEW sales_by_store FROM `account users`;
SHOW GRANTS ON VIEW sales_by_store;

-- Task 3
CREATE OR REPLACE FUNCTION email_mask(email STRING)
RETURN CASE
  WHEN is_account_group_member('brewmart_support') THEN email
  ELSE regexp_replace(email, '^[^@]+', '***')
END;

ALTER TABLE customers ALTER COLUMN email SET MASK email_mask;
SELECT customer_id, email FROM customers;          -- ***@... for you

-- Task 4
CREATE OR REPLACE FUNCTION hq_or_atlanta(city STRING)
RETURN is_account_group_member('brewmart_hq') OR city = 'Atlanta';

ALTER TABLE customers SET ROW FILTER hq_or_atlanta ON (city);
SELECT COUNT(*) FROM customers;                    -- fewer rows than 10

-- Task 5
CREATE OR REPLACE TABLE sales_gold_daily
CLUSTER BY (store, order_date)
AS
SELECT store, order_date,
       ROUND(SUM(line_total), 2) AS revenue,
       COUNT(DISTINCT order_id)  AS orders
FROM sales_silver
WHERE store IS NOT NULL
GROUP BY store, order_date;

DESCRIBE DETAIL sales_gold_daily;                  -- clusteringColumns populated
OPTIMIZE sales_gold_daily;

-- Task 7
ALTER TABLE customers DROP ROW FILTER;
ALTER TABLE customers ALTER COLUMN email DROP MASK;
SELECT COUNT(*) FROM customers;                    -- 10 again, emails visible
```

**Validation Checks**

```sql
-- 1. Mask active: zero real emails visible to you
SELECT COUNT(*) AS leaked
FROM customers WHERE email NOT LIKE '***%';        -- 0 while mask is bound

-- 2. Row filter active: only Atlanta
SELECT DISTINCT city FROM customers;               -- Atlanta (1 row) while bound

-- 3. Grants round-trip: final SHOW GRANTS has no account-users SELECT
SHOW GRANTS ON VIEW sales_by_store;

-- 4. Clustering in place
DESCRIBE DETAIL sales_gold_daily;                  -- clusteringColumns = [store, order_date]

-- 5. After Task 7 cleanup: full visibility restored
SELECT COUNT(*) FROM customers;                    -- 10
```

**Stretch Task**
Loyalty masking, exam-style: bind a *second* mask so `loyalty_tier` shows real values only to `brewmart_marketing`, others see `'REDACTED'`. Then answer in one paragraph: at what point (how many tables/columns) does this per-table approach break down, and what would you propose instead? (Expected answer: tag-driven ABAC policies.) Bonus: run `EXPLAIN SELECT * FROM sales_gold_daily WHERE store = 'Atlanta'` and find evidence of file pruning.

**Instructor Notes**
- The "aha" to engineer: learners expect to see real emails because *they own the table* — the moment the mask hits them too is when RLS/masking clicks. Don't pre-spoil it
- Backticks around `account users` and function-vs-binding confusion (editing the function ≠ rebinding; CREATE OR REPLACE FUNCTION updates behavior live — actually demonstrate if asked) are the top syntax stalls
- If masks/filters are blocked in the current Free Edition build, pivot: learners write the statements, you confirm syntax correctness against the solution, and the demo screenshots stand in as expected output — note it as "Exam concept; syntax fluency achieved"
- `sales_gold_daily` from ~25 silver rows produces trivially small files — OPTIMIZE metrics will be near-zero; pre-empt the "is it broken?" question
- Keep 2 minutes of debrief for the stretch's ABAC paragraph — it cements Slide 6

---

## 6. In-Class Activity

### Activity: "Diagnose the Bottleneck" — Symptom Cards

**Time needed:** 10 minutes (6 min pairs + 4 min debrief)

**Setup**
Six symptom cards. Options menu: **data skew · disk spill · excessive shuffle / missed broadcast · driver OOM · cluster startup failure · library conflict · small-files problem**. Pick one diagnosis + one first remedy per card.

**Instructions**
"You're on call. One diagnosis, one first move, ten words of justification. The metrics in the card are your only evidence."

**Scenario cards**
1. Stage 7: median task 40s, max task 38min; one partition processed 12GB while others got 200MB
2. Job fails at 06:00 before any task starts; event log: "init script exited with non-zero status"; no Spark stages exist
3. Stage metrics show "Spill (Disk): 48GB"; tasks complete but the stage takes 6× its baseline
4. Notebook fails at `import great_expectations`: ModuleNotFoundError — but it worked yesterday on another cluster
5. A `display(df.toPandas())` on a 200M-row result kills the session; executors look healthy in metrics
6. A streaming bronze table now has 400,000 files of ~50KB each; every downstream query is slowing week over week

**Learner deliverable**
Six diagnosis+remedy pairs posted to chat.

**Debrief answers**
1. **Data skew** — uneven key distribution; remedy: broadcast the small side / AQE skew handling / salt or rethink the key
2. **Cluster startup failure** — infra, not code (failed *before* tasks); remedy: fix/remove the init script, check event log
3. **Disk spill** — partitions exceed memory; remedy: raise `spark.sql.shuffle.partitions` (smaller partitions) or executor memory
4. **Library conflict / missing library** — environment, not code; remedy: install/pin the library for *this* compute (notebook-scoped install)
5. **Driver OOM** — `toPandas()` pulls everything to the driver; remedy: don't collect — aggregate/limit first (or raise driver memory as a stopgap)
6. **Small-files problem** — streaming micro-batches; remedy: OPTIMIZE (and liquid clustering / predictive optimization going forward)

**Teaching points**
- The master key from Slide 14: *failed before work started* (cards 2, 4) vs. *failed/slowed during* (1, 3, 5, 6) — apply it first, every time
- Card 5's trap is "executors look healthy" — that's the tell it's the *driver*; exam questions plant exactly this clue
- Card 6 links Domain 6 back to OPTIMIZE/clustering — diagnosis questions sometimes want a *maintenance* answer, not a tuning answer

---

## 7. Live Knowledge Check

The Markdown Mash quiz for this week is kept in the instructor-only private materials and launched live during the session.

Instructor copy: `instructor_private/markdown_mash/Week4_Quiz.md`. This path is intentionally ignored by git so learners do not see the questions or answer key ahead of time.

## 8. Exam Tips for This Week

**What the exam is likely to test**
- GRANT-level selection (schema vs. table) and the USE chain; DENY vs. REVOKE
- Managed/external operations incl. UNDROP and the existence of conversion
- Mask vs. row filter vs. ABAC — matching scale and shape of the requirement to the mechanism
- Delta Sharing types + cross-cloud cost; Federation use cases (query-in-place, no ingestion)
- Spark UI symptom vocabulary: skew / shuffle / spill signatures and first remedies
- Liquid Clustering vs. partitioning/Z-order; what predictive optimization automates and where it works
- The four tuning parameters by name and direction; the three failure categories (startup/library/OOM)

**Keywords to recognize instantly**
`GRANT/REVOKE/DENY`, `SHOW GRANTS`, `USE CATALOG`, `service principal`, `is_account_group_member`, `SET MASK`, `SET ROW FILTER`, `ABAC`, `tag`, `lineage`, `system.access.audit`, `Delta Sharing`, `share/recipient`, `open sharing protocol`, `Lakehouse Federation`, `foreign catalog`, `OPTIMIZE`, `VACUUM`, `CLUSTER BY`, `liquid clustering`, `predictive optimization`, `skew`, `spill`, `shuffle`, `spark.sql.shuffle.partitions`, `init script`, `collect()`

**Common traps**
- "REVOKE guarantees no access" — other grant paths survive; DENY is the blocker
- "Table owners always see unmasked data" — masks apply to owners too unless the function exempts them
- "VACUUM speeds up queries" / "OPTIMIZE reclaims storage" — swapped purposes
- "Partition by the highest-cardinality column for speed" — the classic anti-pattern; liquid clustering is the modern answer
- "Predictive optimization works everywhere" — UC *managed* tables, paid tiers
- "Executor settings fix driver OOM" — collect()/toPandas() failures are driver-side
- Delta Sharing "sends a copy" — it's zero-copy live access; that's the advantage *and* why egress costs exist

**How to eliminate wrong answers**
Governance: match the *scale* (one table → mask/filter; fleet+tags → ABAC) and the *direction* (data out → Sharing; queries out to external DB → Federation). Performance: classify before/during failure first, then match the metric named in the stem (max≫median → skew; spill counters → memory; before-any-stage → infra). Any option pairing a real feature with the wrong scope (PO on external tables, DENY as a grant) dies immediately.

**Memorize**
The privilege chain (USE CATALOG + USE SCHEMA + SELECT); DENY > GRANT; the two-step mask/filter pattern; `CLUSTER BY` syntax; the four tuning parameters; the three failure signatures; D2D vs. open sharing.

**Understand conceptually**
Why policy-in-the-table beats per-audience views; why tags scale governance; why shuffles exist and when broadcast avoids them; why small files happen and which features fight them; why managed tables unlock automation.

---

## 9. Homework / Self-Study

**Primary assignment: THE MOCK EXAM (90 min, required)**
- 45 questions, timed, closed-book, one sitting — simulate Kryterion conditions
- Source: the Week 5 mock provided by the instructor (built to the domain blueprint: 3 platform / 9 ingestion / 10 transformation / 7 jobs / 4 CI/CD / 5 troubleshooting / 7 governance)
- Score yourself **per domain** and bring the breakdown to Week 5 — the review session flexes to the cohort's weak areas
- Also run the official Kryterion system check on the machine you'll test with

**Databricks documentation to read (~35 min)**
- Unity Catalog privileges and securable objects (the privilege table)
- Row filters and column masks
- ABAC overview (skim — concept level)
- Delta Sharing: "What is Delta Sharing?" (the two sharing types)
- Liquid clustering for Delta tables; Predictive optimization
- Spark UI guide — the skew/spill diagnosis sections

**Optional notebook practice (~20 min)**
1. Re-bind your lab's mask and filter from memory — target: no syntax peeking
2. Write the GRANT statements for: a BI group needing read on your whole schema; a service principal needing MODIFY on one table — then SHOW GRANTS to verify
3. `EXPLAIN` a filtered query against `sales_gold_daily` and find pruning evidence

**Review questions**
1. A user can still read a table after you ran REVOKE. List two possible reasons and the definitive fix.
2. Mask, row filter, ABAC: give the one-line trigger condition for choosing each.
3. Spill vs. skew: which metric distinguishes them in a stage summary?
4. Why does predictive optimization require *managed* tables?

**Mini checklist before Week 5**
- [ ] Mock exam done, timed, scored by domain
- [ ] My weakest two domains identified (bring them!)
- [ ] Kryterion system check passed on my exam machine
- [ ] Lab cleanup NOT done — the capstone reuses the BrewMart objects

---

## 10. Instructor Preparation Checklist

**Before class (day before)**
- [ ] **Rehearse Cells 3–4 (mask + row filter) on current Free Edition** — this is the week's platform-risk item; capture screenshots of masked output and reduced row count for fallback
- [ ] Verify `` GRANT ... TO `account users` `` works in your workspace and that SHOW GRANTS displays cleanly
- [ ] Check the lineage tab renders for your silver table (it needs prior query/job activity — run the Week 3 job once if the graph looks thin)
- [ ] Rehearse the query-profile click-path on a `samples.nyctaxi.trips` aggregation; screenshot the profile
- [ ] Test `CLUSTER BY` + `DESCRIBE DETAIL` + `OPTIMIZE` end-to-end
- [ ] Prepare and distribute the 45-question mock exam package (released at end of class) with per-domain answer key
- [ ] Remind learners: customers JSON must still be in their landing volume

**Workspace objects needed**
- `week1_demo` schema with silver-equivalent table + `landing/week2_customers.json`
- Catalog Explorer pinned tabs: table permissions page, lineage tab
- Screenshot kit: masked emails result, filtered rows result, lineage graph, query profile, DESCRIBE DETAIL with clusteringColumns

**Demo rehearsal**
- [ ] Time: Cells 1–2 ≈ 5 min, 3–5 ≈ 8 min (the heart — don't rush the owner-sees-masked moment), 6 ≈ 3 min, 7–8 ≈ 7 min
- [ ] Practice narrating the mask reveal WITHOUT spoiling it — ask the room "whose emails will I see?" before running Cell 3
- [ ] Decide the Cell 8 vehicle: query profile on the SQL warehouse is the reliable Free Edition path; classic Spark UI only if your rehearsal found it accessible

**Backup plans**
- **Masks/filters blocked:** walkthrough mode — learners write syntax, screenshots show results; exam objective ("understand") fully met; say so explicitly to defuse frustration
- **Lineage empty/slow:** use your most-queried table, or the screenshot; the click-path is the learnable
- **Query profile UI moved:** your rehearsal screenshots; the *vocabulary* (stage, exchange/shuffle, task distribution) is the exam content, not the clicks
- **Total outage:** the entire session is unusually slide-teachable — run slides + activity + quiz live, assign demo+lab as guided homework with your screenshot pack, and start Week 5 with a 15-minute governance lab catch-up
- **Time crunch:** Slide 8 (Sharing/Federation) and Slide 14 compress to 90 seconds each with their tables; protect the mask demo and exam-strategy slide above all

---

*Next: Week 5 — Capstone (end-to-end BrewMart pipeline under exam conditions) + full mock-exam review by domain + final readiness checklist.*
