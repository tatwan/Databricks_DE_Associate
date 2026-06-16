# Databricks Certified Data Engineer Associate Client Enablement Curriculum

A five-Friday, ten-hour program is the strongest fit for the current **Databricks Certified Data Engineer Associate** exam. The official May 2026 exam guide shows a broad associate-level scope across seven domains, with the heaviest weighting in **Data Transformation and Modeling**, **Data Ingestion and Loading**, **Lakeflow Jobs**, and **Governance and Security**. The exam itself is **45 scored multiple-choice questions in 90 minutes**, and Databricks states that exam code is presented in **SQL when possible** and **Python otherwise**. citeturn6view0turn5view2

Your client’s starting point is also well aligned with Databricks’ own role-based learning pathway: **Databricks Fundamentals** followed by **Get Started with Data Engineering on Databricks**, before deeper role-specific enablement. That means your role should be to provide the **associate bridge and certification-focused deep dive**, not to reteach generic platform orientation from scratch. citeturn13view0 fileciteturn0file0

## Recommended program shape

The official exam-domain weighting strongly favors a **five-session design** over a four-session one. In practice, four Fridays can work only if you move a meaningful amount of content into homework and accept that some topics become demo-only rather than truly hands-on. With five Fridays, you can give each major chunk of the exam its own cognitive “home” instead of forcing orchestration, CI/CD, governance, and optimization into a rushed final session. citeturn6view0

| Official exam domain | Weight | What that means for your course |
|---|---:|---|
| Databricks Data Intelligence Platform | 6% | Keep this as a short bridge, not a full week |
| Data Ingestion and Loading | 21% | Give this a full Friday |
| Data Transformation and Modeling | 22% | Give this a full Friday |
| Working with Lakeflow Jobs | 16% | Major coverage, not a side topic |
| Implementing CI/CD | 10% | Teach current workflow and deployment concepts explicitly |
| Troubleshooting, Monitoring, and Optimization | 10% | Reserve dedicated time near the end |
| Governance and Security | 15% | Treat as exam-critical, not optional |

The table above is derived from the official May 2026 Databricks exam guide. citeturn6view0

My recommendation is therefore:

**Best option:** **Five Fridays, two hours each**.  
**Compressed option:** **Four Fridays** only if you assign mandatory homework between sessions, merge the platform bridge into the ingestion session, and move the full mock exam to asynchronous practice.

## Design principles for this audience

Because your learners are already working data engineers—many from **ADF, Synapse, or Fabric** backgrounds—your course should be built as a **concept translation and Databricks deep dive**, not a beginner bootcamp. The biggest curriculum mistake would be over-spending time on general data engineering theory they already know, instead of helping them master **Databricks-specific patterns, current terminology, and exam-style feature selection**. The official exam guide itself is very explicit that the exam now covers **Lakeflow Jobs**, **CI/CD**, **Unity Catalog governance**, and **troubleshooting/optimization**, in addition to core ETL. citeturn6view0

Use **current Databricks terminology** throughout. A lot of older content online uses stale names, and that will confuse learners on the current exam. Databricks now documents **Git folders** as the workspace Git integration feature, **Declarative Automation Bundles** as the current name for what used to be Databricks Asset Bundles, **Lakeflow Jobs** for workflow orchestration, and **Lakeflow Spark Declarative Pipelines** for declarative batch and streaming pipelines in SQL or Python. citeturn16view0turn16view1turn17view0turn17view1

Use **Unity Catalog + Medallion architecture** as the spine of the course. Databricks describes Unity Catalog as the unified governance layer beneath data interactions in the workspace, and Databricks explicitly recommends the medallion architecture as a best-practice pattern for bronze, silver, and gold data products. That combination gives you a clean structure for slides, demos, labs, and exam scenarios. citeturn27view2turn30view0

For the weekly teaching rhythm, I would keep every Friday consistent:

- **10 minutes**: retrieval quiz and previous-week recap  
- **35 minutes**: exam-focused concept slides  
- **30 minutes**: instructor demo  
- **30 minutes**: guided hands-on lab  
- **15 minutes**: exam-style questions and debrief  

That rhythm is not from the official docs; it is the instructional design I would use to make a two-hour format feel steady, adult-friendly, and certification-oriented.

## Weekly curriculum blueprint

### Bridge and platform foundations

**Slides.** Cover the **current exam structure**, the Databricks **Data Intelligence Platform** view of the platform, compute choices, Delta Lake basics, Unity Catalog object hierarchy, managed versus external assets, volumes, and the medallion pattern. This is also the place to normalize the current naming model: Git folders, Lakeflow Jobs, Declarative Automation Bundles, and Lakeflow Spark Declarative Pipelines. Emphasize that **Delta is the default table format** in Databricks, that **Unity Catalog is automatically enabled for workspaces created after November 8, 2023**, and that Databricks positions **managed tables** as the default and recommended table type. citeturn5view2turn6view0turn25view0turn27view2turn22view1turn32view0

**Demo.** Use official getting-started assets: query `samples.nyctaxi.trips`, create a managed table in the workspace catalog, create a managed volume, and upload a small CSV or JSON file into that volume. Databricks’ tutorials explicitly use sample Unity Catalog tables, first-table creation, grants, and volume creation/upload workflows, which makes this a very clean and supportable first session for Free Edition. citeturn18view2turn18view1turn34view0turn35view0

**Lab.** Have each learner create one managed table and one managed volume in the default schema, then read the uploaded file through both SQL and PySpark from a `/Volumes/<catalog>/<schema>/<volume>/...` path. This gives them immediate hands-on exposure to the `catalog.schema.object` mental model that will keep showing up throughout the exam. It also front-loads the distinction between **tables** for tabular data and **volumes** for non-tabular or staged file data. citeturn22view2turn33view0turn35view1

**Practice and homework.** Finish with an 8-question quiz on compute selection, Delta versus files, Unity Catalog hierarchy, managed versus external, and current Databricks terminology. For homework, assign the exam-guide-aligned self-paced items around **Unity Catalog interoperability** and **data governance**. The May 2026 exam guide explicitly recommends **Data Interoperability with Unity Catalog** and **Get Started with Data Governance on Databricks** among its related preparation resources. citeturn6view0

### Ingestion and loading patterns

**Slides.** Focus this session on the exam’s **21% Data Ingestion and Loading** domain. Teach the decision logic between **batch**, **streaming**, and **incremental** ingestion, and then map that to **COPY INTO**, **Auto Loader**, **Lakeflow Connect standard connectors**, **Lakeflow Connect managed connectors**, and notebook-based JDBC/REST ingestion patterns. Databricks’ current docs are especially useful here because they now describe the “layers of the ETL stack” and explicitly position **managed connectors** as the most automated layer, **Lakeflow Spark Declarative Pipelines** as the middle layer, and **Structured Streaming** as the most customizable layer. citeturn6view0turn23view0turn24view0turn28view0turn28view1

**Demo.** The best Free Edition-compatible demo is a **volume-based ingestion pattern**. Upload files to a managed volume, create a Delta target table, run `COPY INTO`, then rerun it after adding a second file so learners can see the official Databricks behavior: `COPY INTO` is **retriable and idempotent**, and already-loaded files are skipped on later runs. If your workspace supports it, show an Auto Loader notebook or a basic Lakeflow pipeline afterward as the “next maturity step.” citeturn23view0turn35view0turn24view0turn31view1

**Lab.** Give learners a bronze-table ingestion exercise. The simplest version is: upload two small files into a volume, load the first into a target Delta table, then add the second and rerun the ingestion. A slightly more advanced variant is to use semi-structured data and ask learners to reason about schema evolution, rescue behavior, or the difference between notebook ingestion and Lakeflow-style declarative ingestion. Databricks’ current getting-started and ingestion docs support both of these moves cleanly. citeturn23view0turn24view0turn33view1turn35view0

**Practice and homework.** End with 10 exam-style questions that force **feature selection**, not just definitions. Good question stems here are “Which ingestion method is best?” and “Which option is the most managed?” For homework, assign the exam-guide-recommended **Data Ingestion with Lakeflow Connect** content. citeturn6view0turn28view0turn28view1

### Transformation and modeling

**Slides.** This should be the most technically dense Friday, because **Data Transformation and Modeling** is the largest domain at **22%**. Organize it around the medallion flow: bronze to silver to gold. Cover null handling, casting, joins, broadcast-join awareness, `union` versus `union all`, exploding arrays, deduplication, aggregates, basic tuning settings, `MERGE INTO`, and the choice between **views**, **materialized views**, **streaming tables**, and regular tables. The exam guide explicitly calls out these operations, and Databricks’ medallion and Delta documentation provides the architectural narrative around them. citeturn6view0turn30view0turn25view0turn25view1turn17view1

**Demo.** Use either the **official song-data pipeline tutorial** or a small taxi-style dataset to show a practical bronze-silver-gold flow. The strongest live sequence is: land raw data, clean/cast/deduplicate into silver, then aggregate into a gold object for reporting. If pipeline features are available, also show a small **data quality expectation** example, since the Lakeflow tutorial explicitly uses data-quality rules and materialized views. citeturn15view0turn18view2turn30view0

**Lab.** Ask learners to create a silver table from a raw or bronze source, then a gold object that supports a realistic analytics question. Include at least one join, one deduplication step, and one aggregate. For the capstone task inside the lab, use **`MERGE INTO`** so they practice upsert logic and understand that it is a Delta-table operation. citeturn25view1turn30view0

**Practice and homework.** This is where I would use the largest weekly quiz, around **10 to 12 questions**, because transformation/modeling is both large on the exam and a foundation for the rest of the course. For homework, assign the exam-guide-recommended **Build Data Pipelines with Lakeflow Spark Declarative pipeline** content. citeturn6view0

### Orchestration and delivery workflows

**Slides.** Center this Friday on **Lakeflow Jobs** and **CI/CD**, which together represent **26%** of the exam. Teach the Lakeflow Jobs mental model of **jobs, tasks, triggers, and DAGs**, including common task types, schedules, branching, looping, and run history. Then move into the delivery layer: **Git folders** for workspace Git workflows and **Declarative Automation Bundles** for packaging and promoting jobs, pipelines, and other workspace resources across environments. citeturn17view0turn16view0turn16view1turn6view0

**Demo.** If your Free workspace exposes Jobs and scheduling, use a notebook task with parameters and a simple schedule, then inspect run history. Databricks’ Free Edition page explicitly highlights designing ETL workflows, scheduled runs, schema drift/data quality handling, and run history, so that is a reasonable demonstration target. If Git integration is available, show branch switching and a simple commit inside a Git folder. For DABs, a lightweight demo is enough: show a small `databricks.yml` and explain how the CLI validates, deploys, and runs bundles. citeturn9view0turn17view0turn16view0turn16view1

**Lab.** Make this a **scenario-first lab**, even if the workspace can do part of it hands-on. Have learners design a small DAG on paper or in markdown, choose between time-based and event-based triggers, and identify the right task types. If scheduling is available, let them also create one small notebook job. Then have them annotate a minimal bundle skeleton or CI/CD checklist. That balance matches the exam reality: candidates need to understand both the UI workflow and the deployment model. citeturn17view0turn16view1

**Practice and homework.** Use 8 to 10 questions focused on workflow reasoning, trigger choice, Git operations, and bundle-based promotion. The exam guide explicitly recommends **Deploy Workloads with Lakeflow Jobs** and **DevOps Essentials for Data Engineering** as preparation resources, so those are ideal between-session assignments. citeturn6view0

### Governance, optimization, and final rehearsal

**Slides.** Use the final Friday for the last two major exam areas: **Governance and Security** and **Troubleshooting, Monitoring, and Optimization**. Cover **managed versus external tables**, privilege hierarchy, `GRANT`/`REVOKE`/`DENY`, table-level **row filters and column masks**, **ABAC** concepts, Spark UI reading for skew/spill, **Liquid Clustering**, and **predictive optimization**. Also include a short exam strategy slide set at the end: pacing, elimination, and how to interpret SQL-first question stems. citeturn22view1turn22view0turn22view2turn21view1turn21view0turn27view1turn26view0turn27view0turn5view2turn6view0

**Demo.** In the workspace, show Catalog Explorer privileges and at least one simple `GRANT` example. If your environment supports it, demonstrate a basic row filter or column mask on a toy table; otherwise, teach the syntax and logic from slides. Then show how to open the Spark UI and what Databricks tells you to inspect first: timeline, longest stage, skew, spill, and I/O behavior. End with a brief syntax-level demonstration of `CLUSTER BY` and a conceptual explanation of predictive optimization. citeturn22view2turn21view1turn27view1turn26view0turn27view0

**Lab.** Make this a mixed **case-study and timed-practice** session. Good lab prompts here are: choose managed versus external; write the correct grants; identify whether ABAC or table-level masks are the better fit; interpret a Spark UI symptom; decide whether liquid clustering or traditional partitioning is the better answer; explain whether predictive optimization applies. The last 25 to 30 minutes should be a timed mini-mock. citeturn22view0turn22view1turn22view2turn21view0turn21view1turn27view1turn26view0turn27view0

**Practice and homework.** Release the full 45-question mock after this session, followed by a remediation list by domain. Databricks’ own sample questions in the exam guide are useful, but Databricks also explicitly says those questions are **retired from a previous version** and are meant to illustrate objectives, not predict the current live exam. citeturn6view0

## Free Edition hands-on strategy

Databricks’ official Free Edition page is encouraging for your use case. Databricks says Free Edition lets users work with professional tools, notebooks, dashboards, ETL workflows, scheduled runs, schema drift and data quality scenarios, run history, and free Databricks Academy training. In other words, it is absolutely suitable for **associate-level learning** as long as you design labs around **core platform behavior**, not enterprise-only plumbing. citeturn8view0turn9view0

The most important design choice is to use **managed Unity Catalog tables and managed volumes** as your default lab substrate. Databricks documents volumes as the recommended governed staging area for non-tabular data and explicitly names ingestion use cases like **Auto Loader**, **COPY INTO**, and **CTAS**. Databricks also documents that, in automatically enabled Unity Catalog workspaces, workspace users receive `USE CATALOG`, `USE SCHEMA`, `CREATE TABLE`, and `CREATE VOLUME` on the default schema of the workspace catalog. That combination is exactly what makes a Free Edition-friendly lab design possible. citeturn33view0turn34view0turn35view0turn22view2

I would separate your lab design into three tiers:

| Delivery tier | Topics |
|---|---|
| **Fully hands-on** | notebooks, SQL/Python, managed tables, managed volumes, Unity Catalog object model, Delta basics, medallion transformations, query/visualize exercises |
| **Conditional hands-on** | `COPY INTO`, Auto Loader, Lakeflow Spark Declarative Pipelines, notebook jobs, schedules, run history |
| **Demo or scenario only unless the workspace supports more** | Lakeflow Connect managed connectors, external tables, ABAC administration at scale, predictive optimization, multi-environment DAB deployment |

That tiering follows the documented prerequisites for these features. `COPY INTO` for cloud storage requires configured data access; the Lakeflow pipeline tutorial requires Unity Catalog plus compute and permissions; external tables require an external location; predictive optimization requires **Premium plan or above**; and Lakeflow Connect managed connectors depend on enterprise sources plus serverless-managed pipeline infrastructure. citeturn23view0turn15view0turn22view0turn27view0turn28view1

A practical safeguard is to build **every lab with a fallback path**. For example, your primary ingestion lab can use **volume upload + `COPY INTO`**, while the fallback lab uses **upload + `spark.read` + Delta write**. Your primary orchestration lab can use **Jobs** if present, while the fallback uses a scenario worksheet plus run-history screenshots. That way, Free Edition becomes an enabler instead of a risk. citeturn23view0turn35view0turn35view1turn17view0

## Practice and exam readiness plan

Build your mock exams to the **official domain weighting**, not to whatever topic felt most fun to teach. For a full **45-question** mock, a very good blueprint is the following:

| Domain | Approximate question count |
|---|---:|
| Databricks Data Intelligence Platform | 3 |
| Data Ingestion and Loading | 9 |
| Data Transformation and Modeling | 10 |
| Working with Lakeflow Jobs | 7 |
| Implementing CI/CD | 4 |
| Troubleshooting, Monitoring, and Optimization | 5 |
| Governance and Security | 7 |

This distribution is a practical rounding of the official exam percentages from the May 2026 guide. citeturn6view0

The official sample questions in the exam guide are useful, but only in the right way. Databricks says those questions are **retired from a previous version of the exam** and are included to show objective alignment. That means you should use them as **templates for question style**, not as a study bank to memorize. citeturn6view0

Because Databricks states that the live exam presents data-manipulation code in **SQL when possible** and **Python otherwise**, your practice material should follow the same ratio. In real course design terms, that means: make your slide examples mostly SQL-first, make your labs bilingual where possible, and make your quizzes slightly more SQL-heavy than PySpark-heavy. Since the exam is 45 questions in 90 minutes, teach learners to operate at roughly **two minutes per question** and to flag ambiguous questions rather than over-investing early. citeturn5view2turn6view0

For homework and remediation, lean on the exam guide’s recommended training list and the free training/Academy access that Databricks exposes through Free Edition and its training pages. The May 2026 exam guide explicitly recommends **Data Ingestion with Lakeflow Connect**, **Deploy Workloads with Lakeflow Jobs**, **DevOps Essentials for Data Engineering**, **Data Interoperability with Unity Catalog**, **Build Data Pipelines with Lakeflow Spark Declarative pipeline**, and **Get Started with Data Governance on Databricks**. Databricks’ own Free Edition and training pages also point learners to free self-paced Academy resources. citeturn6view0turn9view0turn13view0

The bottom line is that you do **not** need to build a full 2-day Databricks course to get this audience ready. What you need is a **five-Friday associate bridge**: current terminology, exam-weighted coverage, SQL-first practice, Free Edition-friendly labs built on managed tables and volumes, and a disciplined mock-exam cadence. If you design to that pattern, your course will feel purposeful, modern, and tightly aligned to the **May 2026** Databricks Certified Data Engineer Associate exam. citeturn6view0turn5view2turn9view0