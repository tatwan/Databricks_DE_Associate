/* Content model for the Databricks Data Engineer Associate review session. */

const SRC = {
  guide: 'https://www.databricks.com/sites/default/files/2026-03/databricks-certified-data-engineer-associate-exam-guide-may-4-2026.pdf',
  certPage: 'https://www.databricks.com/learn/certification/data-engineer-associate',
  arch: 'https://docs.databricks.com/aws/en/getting-started/high-level-architecture',
  serverless: 'https://docs.databricks.com/aws/en/ldp/concepts/serverless-vs-classic-compute',
  securables: 'https://docs.databricks.com/aws/en/data-governance/unity-catalog/securable-objects',
  volumes: 'https://docs.databricks.com/aws/en/volumes/',
  managed: 'https://docs.databricks.com/aws/en/tables/managed',
  ctas: 'https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-table-using',
  undrop: 'https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-undrop-table',
  restore: 'https://docs.databricks.com/aws/en/sql/language-manual/delta-restore',
  history: 'https://learn.microsoft.com/en-us/azure/databricks/tables/history',
  medallion: 'https://www.databricks.com/blog/what-is-medallion-architecture',
  copyInto: 'https://docs.databricks.com/aws/en/sql/language-manual/delta-copy-into',
  copyStart: 'https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/copy-into/',
  alSchema: 'https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/schema',
  alNotify: 'https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/file-notification-mode',
  alOptions: 'https://learn.microsoft.com/en-us/azure/Databricks/ingestion/cloud-object-storage/auto-loader/options',
  connect: 'https://learn.microsoft.com/en-us/azure/databricks/ingestion/overview',
  connectors: 'https://learn.microsoft.com/en-us/azure/databricks/ingestion/',
  triggers: 'https://docs.databricks.com/aws/en/structured-streaming/triggers',
  aqe: 'https://docs.databricks.com/aws/en/optimizations/aqe',
  optimizeGuide: 'https://www.databricks.com/discover/pages/optimize-data-workloads-guide',
  mvStandalone: 'https://docs.databricks.com/aws/en/ldp/dbsql/materialized',
  mvSchedule: 'https://docs.databricks.com/aws/en/ldp/dbsql/schedule-refreshes',
  jobTriggers: 'https://learn.microsoft.com/en-us/azure/databricks/jobs/triggers',
  tableTrigger: 'https://www.databricks.com/blog/announcing-table-update-triggers-lakeflow-jobs',
  taskValues: 'https://docs.databricks.com/aws/en/jobs/task-values',
  repair: 'https://docs.databricks.com/aws/en/jobs/repair-job-failures',
  expectations: 'https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/ldp-python-ref-expectations',
  gitFolders: 'https://docs.databricks.com/aws/en/repos/git-operations-with-repos',
  bundles: 'https://docs.databricks.com/aws/en/dev-tools/bundles/deployment-modes',
  bundleRef: 'https://docs.databricks.com/aws/en/dev-tools/bundles/reference',
  privileges: 'https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges/',
  privRef: 'https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/privileges-reference',
  deny: 'https://docs.databricks.com/aws/en/sql/language-manual/security-deny',
  masks: 'https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/',
  masksApply: 'https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/manually-apply',
  abac: 'https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/',
  abacVs: 'https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/abac/abac-vs-rls-cm',
  sharing: 'https://learn.microsoft.com/en-us/azure/databricks/delta-sharing/share-data-open',
  sharingHome: 'https://learn.microsoft.com/en-us/azure/databricks/delta-sharing/',
  vacuum: 'https://docs.databricks.com/aws/en/sql/language-manual/delta-vacuum',
  predictive: 'https://docs.databricks.com/aws/en/optimizations/predictive-optimization',
  clustering: 'https://docs.databricks.com/aws/en/tables/clustering',
  clusterBy: 'https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-cluster-by',
  sparkUi: 'https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/',
  skewSpill: 'https://docs.databricks.com/aws/en/optimizations/spark-ui-guide/long-spark-stage-page',
};

/* ---------------------------------------------------------------- exam meta */

const EXAM = {
  questions: 45,
  minutes: 90,
  guideDate: 'May 4, 2026',
  target: 32,
};

/* ------------------------------------------------------------ session plan */

const PLAN = [
  { id: 'open', label: 'Set expectations', min: 5, target: 'top', note: 'Scenario-first answering; approximate domain weighting.' },
  { id: 'd1', label: 'Platform', min: 5, target: 'd1', note: 'Compress to high-yield distinctions only — 6% of the exam.' },
  { id: 'd2', label: 'Ingestion & loading', min: 17, target: 'd2', note: 'COPY INTO vs Auto Loader vs Lakeflow Connect; schema drift.' },
  { id: 'd3', label: 'Transformation & modeling', min: 18, target: 'd3', note: 'MERGE duplicates, dedupe window, join semantics, broadcast.' },
  { id: 'd4', label: 'Lakeflow Jobs', min: 13, target: 'd4', note: 'DAGs, repair runs, triggers, task values, pipelines.' },
  { id: 'd5', label: 'CI/CD', min: 8, target: 'd5', note: 'Git folders plus bundles.' },
  { id: 'd6', label: 'Troubleshooting & optimization', min: 8, target: 'd6', note: 'OPTIMIZE/VACUUM, clustering, skew/spill, OOM triage.' },
  { id: 'd7', label: 'Governance & security', min: 11, target: 'd7', note: 'Privilege chain, DENY, masks/filters, ABAC.' },
  { id: 'quiz', label: 'Retrieval quiz & close', min: 5, target: 'quiz', note: 'Run the scenario drill; name each learner’s next domain.' },
];

/* ---------------------------------------------------------------- domains */

const DOMAINS = [
  /* ============================================================ DOMAIN 1 */
  {
    id: 'd1',
    num: 1,
    title: 'Databricks Data Intelligence Platform',
    weight: 6,
    approxQ: 3,
    week: 'Week 1',
    summary:
      'Lowest-weight domain, so treat it as a rapid refresher. Know the lakehouse premise, where compute actually runs, the Unity Catalog hierarchy, and the managed/external distinction.',
    cards: [
      {
        slide: 3,
        kicker: 'Lakehouse',
        title: 'The lakehouse in three facts',
        blocks: [
          { type: 'points', items: [
            ['One copy, every workload', 'A single governed Delta copy serves ETL, SQL, streaming, and ML — no lake/warehouse split, no duplicate pipelines.'],
            ['Delta is the default table format', 'On Databricks, <code>CREATE TABLE</code> without a <code>USING</code> clause produces a Delta table. Parquet, CSV, and Iceberg require explicit syntax.'],
            ['<code>_delta_log</code> = ACID', 'An ordered transaction log on cloud object storage gives atomic commits and table versioning — no locks, no proprietary storage format.'],
          ]},
          { type: 'code', lang: 'sql', body: 'CREATE TABLE sales (id INT, amount DOUBLE);\n-- Delta, because no USING clause was specified' },
          { type: 'correction', body: 'Original slide said “Delta, <em>always</em>.” Teach it as the normal/default behavior on Databricks unless another provider is specified — not a portable Spark rule.' },
          { type: 'callout', label: 'Remember', body: 'Delta is a <strong>table</strong> format built on the Parquet <strong>file</strong> format. The log is what adds transactions and time travel.' },
        ],
        src: [['CREATE TABLE [USING]', SRC.ctas]],
      },
      {
        slide: 4,
        kicker: 'Architecture',
        title: 'Control plane, data plane, and the serverless trap',
        blocks: [
          { type: 'cols', cols: [
            { head: 'Control plane — Databricks’ account', items: ['Workspace UI and notebook metadata', 'Job scheduling service', 'Unity Catalog metastore'] },
            { head: 'Data plane — where compute runs', items: ['<strong>Classic</strong> compute: clusters run in your cloud account', '<strong>Serverless</strong> compute: runs in Databricks’ account', 'On serverless, Spark knobs such as <code>shuffle.partitions</code> are largely not settable — Databricks manages them'] },
          ]},
          { type: 'callout', label: 'The trap', body: '“Serverless is always cheaper” is <strong>false</strong>. Always simpler, yes. Cost depends on the workload shape.' },
        ],
        src: [['High-level architecture', SRC.arch], ['Serverless vs classic', SRC.serverless]],
      },
      {
        slide: 5,
        kicker: 'Unity Catalog',
        title: 'The object model and its ordering',
        blocks: [
          { type: 'flow', steps: [
            ['Metastore', 'regional · top of the tree'],
            ['Catalog', 'first name part'],
            ['Schema', 'second name part'],
            ['Table · View · Volume', 'third name part'],
          ]},
          { type: 'code', lang: 'sql', body: 'my_catalog.finance.invoices\n-- the middle element is always the schema' },
          { type: 'points', items: [
            ['Volumes', 'Govern non-tabular files (raw CSVs, images, PDFs) inside the same hierarchy. Tables govern tabular data.'],
            ['The workspace is not in the hierarchy', 'Workspaces are assigned to a metastore; they are not a level of the data namespace.'],
          ]},
          { type: 'correction', body: 'Original slide said the metastore is “one per region.” Say instead: a Unity Catalog metastore is <em>regional</em>, and workspaces are assigned to a metastore. Avoid the account-design absolute.' },
        ],
        src: [['Securable objects', SRC.securables], ['Volumes', SRC.volumes]],
      },
      {
        slide: 6,
        kicker: 'Table lifecycle',
        title: 'Managed vs external tables',
        blocks: [
          { type: 'cols', cols: [
            { head: 'Managed — UC owns data + metadata', items: ['<code>DROP TABLE</code> deletes files <em>and</em> metadata', 'Recoverable with <code>UNDROP TABLE</code> while retention allows', 'Eligible for predictive optimization', '<code>DESCRIBE EXTENDED</code> shows <code>Type: MANAGED</code>'] },
            { head: 'External — created with LOCATION', items: ['<code>DROP</code> removes metadata only; files remain in your storage', 'Fits company-owned storage and non-Databricks readers', 'Still governed by UC through an external location', 'Want lifecycle management? Convert external → managed'] },
          ]},
          { type: 'callout', label: 'The tell', body: '<code>CREATE TABLE … LOCATION \'s3://…\'</code> ⇒ external. No <code>LOCATION</code> ⇒ managed.' },
        ],
        src: [['Managed tables', SRC.managed], ['UNDROP', SRC.undrop]],
      },
      {
        slide: 7,
        kicker: 'DDL',
        title: 'CTAS, CASTs, and views',
        blocks: [
          { type: 'points', items: [
            ['CTAS creates and populates in one statement', 'Column types are inferred from the query. A parenthesized column-type list cannot be declared.'],
            ['Need a specific type? <code>CAST</code> inside the SELECT', 'That is the only type-control mechanism CTAS has.'],
            ['TEMP VIEW is session-scoped', 'Colleagues — and your next session — cannot see it. A standard view is a stored query, visible per its grants.'],
            ['<code>IF NOT EXISTS</code> against a populated table', 'No error, no overwrite. The statement is a silent no-op.'],
          ]},
          { type: 'code', lang: 'sql', body: 'CREATE TABLE silver.orders AS\nSELECT id, CAST(order_date AS DATE) AS order_date\nFROM bronze.orders;' },
          { type: 'callout', label: 'Trap', tone: 'warn', body: '<code>CREATE TABLE t (order_date DATE) AS SELECT …</code> is invalid. The parenthesized type list is the classic wrong answer.' },
        ],
        src: [['CREATE TABLE [USING]', SRC.ctas]],
      },
      {
        slide: 8,
        kicker: 'Delta',
        title: 'Time travel and recovery',
        blocks: [
          { type: 'table', head: ['Incident', 'Fastest fix'], rows: [
            ['Read the table as it was at version 3', '<code>SELECT * FROM events VERSION AS OF 3</code>'],
            ['Roll the table back after a bad <code>UPDATE</code>', '<code>RESTORE TABLE events TO VERSION AS OF 3</code>'],
            ['Managed table dropped 10 minutes ago', '<code>UNDROP TABLE</code> — subject to the applicable retention configuration'],
            ['History older than VACUUM retention', 'Gone. VACUUM deleted those files; time travel past it fails'],
            ['Readers while an <code>UPDATE</code> runs', 'They see the last committed version — readers never block'],
          ]},
          { type: 'correction', body: 'Recoverability depends on the applicable table/metadata retention configuration. Do not imply one universal <code>UNDROP</code> window.' },
          { type: 'callout', label: 'Distinguish', body: '<code>VERSION AS OF</code> reads history without changing anything. <code>RESTORE</code> writes a new version.' },
        ],
        src: [['RESTORE', SRC.restore], ['Table history', SRC.history], ['UNDROP', SRC.undrop]],
      },
      {
        slide: 9,
        kicker: 'Compute',
        title: 'Choosing compute',
        blocks: [
          { type: 'table', head: ['Scenario keywords', 'Best fit', 'Why'], rows: [
            ['Ad-hoc SQL + BI dashboards, no Python', 'Serverless SQL warehouse', 'Instant start, auto-scaling, SQL-optimized'],
            ['Nightly unattended production ETL, budget-aware', 'Job compute / serverless jobs', 'Per-run: starts, runs, terminates — no idle cost'],
            ['Interactive multi-language development', 'All-purpose cluster', 'Long-lived, shared, notebooks attach to it'],
            ['Spiky loads; team wants to stop tuning clusters', 'Serverless jobs compute', 'Databricks manages sizing entirely'],
          ]},
          { type: 'callout', label: 'Anti-pattern', tone: 'warn', body: 'An always-on all-purpose cluster for scheduled production jobs — it lingers and bills after the run finishes.' },
        ],
        src: [['Serverless vs classic', SRC.serverless]],
      },
      {
        slide: 10,
        kicker: 'Architecture',
        title: 'Medallion: each layer has a contract',
        optional: true,
        blocks: [
          { type: 'flow', steps: [
            ['Bronze', 'raw, as-arrived · minimal transformation · auditability and reprocessing'],
            ['Silver', 'deduplicated · cast and validated · trustworthy downstream'],
            ['Gold', 'aggregated, business-ready · serves BI and reporting'],
          ]},
          { type: 'points', items: [
            ['Keep fidelity at bronze', 'Preserve nested structures and raw values. Cleaning belongs to silver, aggregation to gold.'],
          ]},
          { type: 'callout', label: 'One line each', body: 'Bronze = replayable history. Silver = clean and conformed. Gold = answers for the business.' },
        ],
        src: [['Medallion architecture', SRC.medallion]],
      },
    ],
  },

  /* ============================================================ DOMAIN 2 */
  {
    id: 'd2',
    num: 2,
    title: 'Data Ingestion & Loading',
    weight: 21,
    approxQ: 9,
    week: 'Week 2',
    summary:
      'One of the two heaviest domains. Nearly every question is a tool-selection scenario: read the constraints, then pick the simplest sufficient loader.',
    cards: [
      {
        slide: 11,
        kicker: 'COPY INTO',
        title: 'The idempotent SQL loader',
        blocks: [
          { type: 'points', items: [
            ['Idempotent by design', 'COPY INTO tracks the files it has loaded and skips them on rerun — running it twice adds no duplicate rows. It skips files loaded previously even if those files were later modified.'],
            ['Pure SQL', 'Fits teams working exclusively in SQL: nightly batches of files from a volume into a Delta table.'],
            ['Incremental, not a reload', '<code>INSERT INTO … read_files</code> and <code>CREATE OR REPLACE TABLE</code> reprocess everything. COPY INTO loads only what is new.'],
          ]},
          { type: 'code', lang: 'sql', body: "COPY INTO sales\nFROM '/Volumes/main/retail/landing/'\nFILEFORMAT = CSV\nFORMAT_OPTIONS ('header' = 'true');" },
          { type: 'callout', label: 'Remember', body: 'Rerun with nothing new ⇒ 0 rows loaded, no error, no duplicates.' },
        ],
        src: [['COPY INTO', SRC.copyInto], ['Get started with COPY INTO', SRC.copyStart]],
      },
      {
        slide: 12,
        kicker: 'Auto Loader',
        title: 'Streaming file ingestion at scale',
        blocks: [
          { type: 'points', items: [
            ['<code>format("cloudFiles")</code> is Auto Loader', 'A Structured Streaming source for files landing in cloud storage.'],
            ['The checkpoint records processed files across runs', 'Checkpoint-based incremental processing that survives restarts. Preserve the checkpoint and do not change source/path semantics unexpectedly.'],
            ['Built for millions of files arriving continuously', 'The scale at which COPY INTO stops being practical.'],
            ['Tens of millions of files?', 'Switch discovery to file notification mode — event-driven beats re-listing directories on both latency and cost.'],
          ]},
          { type: 'code', lang: 'python', body: '(spark.readStream.format("cloudFiles")\n   .option("cloudFiles.format", "json")\n   .option("cloudFiles.schemaLocation", checkpoint_path)\n   .load(source))' },
          { type: 'correction', body: 'Original slide promised “exactly-once ingestion.” Teach it as checkpoint-based incremental processing with restart safety — that is the defensible claim.' },
        ],
        src: [['File notification mode', SRC.alNotify], ['Auto Loader options', SRC.alOptions]],
      },
      {
        slide: 13,
        kicker: 'Schema drift',
        title: 'Evolution and rescue',
        blocks: [
          { type: 'cols', cols: [
            { head: 'New column · addNewColumns (default)', items: ['The stream stops once with a schema-change error', 'The schema location is updated automatically', 'On restart the stream continues with the new column', 'A deliberate stop-and-recover, not a failure to fix'] },
            { head: 'Type mismatch · _rescued_data', items: ['A STRING arrives where the schema expects INT', 'The mismatched value is captured in <code>_rescued_data</code>', 'The row is ingested and the stream keeps running', 'Investigate the rescued column; nothing is silently lost'] },
          ]},
          { type: 'callout', label: 'May 2026 addition', body: '<code>addNewColumnsWithTypeWidening</code> also handles compatible type widening (for example INT → BIGINT) instead of only adding columns. Mention it once so a newer-wording question does not surprise the cohort.' },
          { type: 'callout', label: 'Contrast', body: 'New column = stop once, then succeed. Bad type = rescued, never fatal.' },
        ],
        src: [['Schema inference and evolution', SRC.alSchema]],
      },
      {
        slide: 14,
        kicker: 'Tool selection',
        title: 'Picking the ingestion tool',
        blocks: [
          { type: 'table', head: ['Scenario signature', 'Reach for'], rows: [
            ['~50 CSVs nightly · SQL-only team · safe reruns', '<strong>COPY INTO</strong>'],
            ['Millions of files, continuous, schema drifts', '<strong>Auto Loader</strong> with schema evolution'],
            ['SaaS or database source (Salesforce, SQL Server) · least engineering', '<strong>Lakeflow Connect</strong> managed connector'],
            ['Custom REST API · custom auth · no connector exists', '<strong>Notebook API client</strong> scheduled with Lakeflow Jobs'],
          ]},
          { type: 'callout', label: 'Best beats works', body: 'When two options both function, pick the simplest one that satisfies every stated constraint.' },
        ],
        src: [['What is Lakeflow Connect?', SRC.connect]],
      },
      {
        slide: 15,
        kicker: 'Details',
        title: 'Ingestion details the exam probes',
        blocks: [
          { type: 'points', items: [
            ['<code>trigger(availableNow=True)</code>', 'Process all data available right now, then stop — a streaming read executed as a scheduled batch. No always-on cluster.'],
            ['Connector tiers', 'Managed connectors automate the most operations (least engineering). Standard connectors trade automation for customization through pipeline and streaming APIs.'],
            ['Bronze-as-STRING pattern', 'For unreliable CSV sources, land columns as STRING plus audit metadata. Nothing is rejected at bronze; types are enforced at silver.'],
            ['Recommended starting point', 'The most managed option that supports your source. Drop a tier only when you need the control.'],
          ]},
          { type: 'callout', label: 'Keyword', body: '“Process what is there on a schedule, no continuous cluster” ⇒ <code>availableNow</code> trigger.' },
        ],
        src: [['Trigger intervals', SRC.triggers], ['Connector tiers', SRC.connectors]],
      },
      {
        slide: 16,
        kicker: 'Semi-structured',
        title: 'Nested data: keep it, then navigate it',
        optional: true,
        blocks: [
          { type: 'points', items: [
            ['Store nested types natively', 'Address object → STRUCT column; phone list → ARRAY column. Do not flatten to 40 columns or stringify JSON at bronze.'],
          ]},
          { type: 'table', head: ['Task', 'Expression', 'Returns'], rows: [
            ['Field inside a struct', '<code>contact.city</code>', 'The city value (dot syntax)'],
            ['Array → rows', '<code>explode(favorite_categories)</code>', 'One output row per array element'],
            ['Split a delimited string', "<code>split(full_name, ' ')[0]</code>", 'Element by index — first name'],
          ]},
          { type: 'callout', label: 'Remember', body: 'Dot syntax navigates parsed structs. <code>explode</code> fans arrays into rows — it does not touch structs.' },
        ],
      },
    ],
  },

  /* ============================================================ DOMAIN 3 */
  {
    id: 'd3',
    num: 3,
    title: 'Data Transformation & Modeling',
    weight: 22,
    approxQ: 10,
    week: 'Week 2',
    summary:
      'The heaviest domain. Expect MERGE failures, deduplication choices, join semantics that quietly change totals, and gold-layer serving decisions.',
    cards: [
      {
        slide: 17,
        kicker: 'Upsert',
        title: 'MERGE INTO: the atomic upsert',
        blocks: [
          { type: 'code', lang: 'sql', body: 'MERGE INTO customers t\nUSING updates s ON t.customer_id = s.customer_id\nWHEN MATCHED THEN UPDATE SET *\nWHEN NOT MATCHED THEN INSERT *;' },
          { type: 'points', items: [
            ['One atomic statement', 'Updates matched rows and inserts unmatched ones. “UPSERT INTO” does not exist; <code>APPLY CHANGES</code> is a declarative-pipeline construct.'],
            ['The famous failure', '“A target row matched multiple source rows.” Root cause: duplicate merge keys in the source. Fix: deduplicate the source before merging.'],
          ]},
          { type: 'callout', label: 'Not the fix', tone: 'warn', body: 'Changing <code>WHEN</code> clauses or the <code>ON</code> condition does not resolve ambiguous matches. Only source deduplication does.' },
        ],
      },
      {
        slide: 18,
        kicker: 'Dedup',
        title: 'Deduplication: arbitrary vs latest',
        blocks: [
          { type: 'cols', cols: [
            { head: 'dropDuplicates(["customer_id"])', items: ['Keeps one row per key — which row is not guaranteed', 'Fine when any representative row will do', 'No sorting happens as a side effect'] },
            { head: 'Latest record per key — the window pattern', items: ['<code>ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at DESC)</code>', 'Keep rows where the row number = 1', 'The only pattern that controls <em>which</em> duplicate survives'] },
          ]},
          { type: 'callout', label: 'Keyword', body: '“Most recent record per key” ⇒ window function. Never a bare <code>dropDuplicates</code> or <code>GROUP BY MAX</code>.' },
        ],
      },
      {
        slide: 19,
        kicker: 'Joins & sets',
        title: 'Combining datasets without surprises',
        blocks: [
          { type: 'table', head: ['Operation', 'Behavior', 'Remedy / rule'], rows: [
            ['<code>UNION</code> vs <code>UNION ALL</code>', 'UNION dedupes; UNION ALL keeps duplicates and is cheaper', 'Need duplicates kept? <code>UNION ALL</code>'],
            ['<code>df1.union(df2)</code>', 'Positional — mismatched column order silently mixes data', 'Use <code>unionByName</code> when order differs'],
            ['<code>INNER JOIN</code> to a dimension', 'Rows without a match are silently dropped — totals shrink', '<code>LEFT JOIN</code> plus <code>COALESCE</code> keeps and labels them'],
          ]},
          { type: 'callout', label: 'Diagnosis', body: '“Revenue decreased after switching LEFT → INNER” = unmatched fact rows silently dropped.' },
        ],
      },
      {
        slide: 20,
        kicker: 'Bilingual',
        title: 'PySpark mirrors: read both languages',
        blocks: [
          { type: 'table', head: ['SQL', 'PySpark', 'Note'], rows: [
            ['<code>WHERE order_id IS NOT NULL</code>', '<code>df.filter(col("order_id").isNotNull())</code>', '<code>filter</code> / <code>where</code> are synonyms'],
            ["<code>COALESCE(store, 'Unknown')</code>", '<code>F.coalesce(col("store"), lit("Unknown"))</code>', 'First non-NULL wins'],
            ['<code>CAST(quantity AS INT)</code>', '<code>col("quantity").cast("int")</code>', 'Not <code>astype</code> — that is pandas'],
            ['<code>COUNT(DISTINCT customer_id)</code>', '<code>F.count_distinct("customer_id")</code>', '<code>count()</code> counts non-NULL rows'],
            ['<code>quantity * unit_price</code> with NULL price', 'Same behavior', 'NULL in ⇒ NULL out, both languages'],
          ]},
          { type: 'callout', label: 'Remember', body: '<code>SELECT DISTINCT</code> removes exact duplicate <strong>rows</strong> — every column equal, not just one key.' },
        ],
      },
      {
        slide: 21,
        kicker: 'Performance',
        title: 'Broadcast joins: small table, big win',
        blocks: [
          { type: 'flow', steps: [
            ['Small dimension', 'small enough for executor memory'],
            ['Broadcast', 'hint, or auto via threshold'],
            ['Every executor', 'joins locally'],
            ['No big shuffle', 'the huge fact table never moves'],
          ]},
          { type: 'correction', body: 'Original slide taught a “6 MB dimension” rule. There is no universal exam threshold. Teach it as: broadcast a dimension small enough for executor memory; auto-broadcast depends on <code>spark.sql.autoBroadcastJoinThreshold</code>, or use an explicit broadcast hint.' },
          { type: 'points', items: [
            ['Not the fix', 'Raising <code>spark.sql.shuffle.partitions</code> (it still shuffles), cross joins, or splitting the fact table into <code>UNION ALL</code> branches.'],
          ]},
          { type: 'callout', label: 'Signature', body: '“Small lookup + huge fact + shuffle-heavy join” ⇒ broadcast the small side.' },
        ],
        src: [['Adaptive query execution', SRC.aqe], ['Optimize data workloads', SRC.optimizeGuide]],
      },
      {
        slide: 22,
        kicker: 'Data quality',
        title: 'Constraints are contracts; quarantine keeps flow',
        blocks: [
          { type: 'cols', cols: [
            { head: 'CHECK constraint — all or nothing', items: ['<code>CHECK (quantity > 0)</code> on the table', 'A 1,000-row INSERT with 3 bad rows → the whole INSERT fails', 'No partial writes, no auto-skipping, no NULL conversion', 'Use when bad data must never land'] },
            { head: 'Quarantine split — flow plus visibility', items: ['Route valid rows → silver, invalid rows → a quarantine table', 'The load keeps running', 'Bad rows stay investigable', 'Use when invalid rows must not stop the pipeline'] },
          ]},
          { type: 'callout', label: 'Decide by requirement', body: '“Must not stop the load, but keep bad rows visible” ⇒ quarantine, not constraints.' },
        ],
      },
      {
        slide: 23,
        kicker: 'Gold layer',
        title: 'Serving the business: views, MVs, approximations',
        blocks: [
          { type: 'table', head: ['Need', 'Tool', 'Why'], rows: [
            ['Reusable query logic, always current', 'Standard view', 'Re-executes the query on each read'],
            ['Expensive multi-table aggregate, read constantly, refresh-based freshness is acceptable', 'Materialized view with a refresh strategy', 'Precomputed — dashboard reads are cheap'],
            ['Distinct count over a billion rows, exactness not required', '<code>approx_count_distinct</code>', 'Fast approximate cardinality (HyperLogLog)'],
          ]},
          { type: 'correction', body: 'Original slide said “≤1 h staleness OK.” One hour is not a product constraint — materialized views can refresh manually, on a schedule, or based on source changes. Frame it as “when refresh-based freshness is acceptable.”' },
          { type: 'callout', label: 'Keywords', body: '“Repeatedly runs an expensive aggregation” + “may lag behind the source” ⇒ materialized view.' },
        ],
        src: [['Standalone materialized views', SRC.mvStandalone], ['Schedule refreshes', SRC.mvSchedule]],
      },
    ],
  },

  /* ============================================================ DOMAIN 4 */
  {
    id: 'd4',
    num: 4,
    title: 'Working with Lakeflow Jobs',
    weight: 16,
    approxQ: 7,
    week: 'Week 3',
    summary:
      'Orchestration reasoning: what runs in parallel, what got skipped, which trigger the wording implies, and what a repair run actually re-executes.',
    cards: [
      {
        slide: 24,
        kicker: 'Naming',
        title: 'Names, compute, and go-live',
        blocks: [
          { type: 'points', items: [
            ['Lakeflow Jobs is the orchestration service', '“Databricks Workflows” is the legacy name. Lakeflow Connect is the ingestion family.'],
            ['Jobs run on per-run compute', 'Job clusters or serverless jobs compute — created for the run, terminated after it.'],
            ['Configured but not live yet?', 'Deploy the job with its trigger set to <strong>Paused</strong>. Fully set up, executes nothing until unpaused.'],
          ]},
          { type: 'callout', label: 'Remember', body: '“Fully configured this week, must not run until go-live” ⇒ paused trigger, not a far-future schedule.' },
        ],
        src: [['Schedules and triggers', SRC.jobTriggers]],
      },
      {
        slide: 25,
        kicker: 'DAG',
        title: 'Edges, parallelism, and failure',
        blocks: [
          { type: 'points', items: [
            ['<code>depends_on</code> is the arrow', 'A task runs only after its dependencies succeed. Tasks with no edge between them run in parallel automatically.'],
            ['“Upstream failed”', 'The downstream task was skipped because its dependency failed. The task itself never ran.'],
            ['Retries fix transient failures only', 'A deterministic bug fails every retry. Fix the code, then use <strong>Repair run</strong>.'],
            ['If/else condition task', 'Branches the DAG on a boolean — “full rebuild on the 1st of the month, incremental otherwise.”'],
          ]},
          { type: 'callout', label: 'Classify the failure', body: 'Succeeds on retry ⇒ transient ⇒ retries. Fails every time ⇒ deterministic ⇒ fix, then repair.' },
        ],
        src: [['Repair job failures', SRC.repair]],
      },
      {
        slide: 26,
        kicker: 'Triggers',
        title: 'Let the data start the job',
        blocks: [
          { type: 'table', head: ['Scenario', 'Trigger'], rows: [
            ['Run every night at 02:00', 'Scheduled (cron)'],
            ['Files land in a storage location at unpredictable times', 'File arrival — monitors a UC volume or external location'],
            ['A silver <strong>table</strong> gets new commits from upstream jobs', 'Table update — responds to updates of specified source tables'],
            ['Stream-like, always-on processing', 'Continuous'],
            ['Job must exist but never fire yet', 'Paused'],
          ]},
          { type: 'callout', label: 'Watch the noun', body: 'Files landing ⇒ file arrival. A table being updated ⇒ table update. Do not poll for either.' },
        ],
        src: [['Schedules and triggers', SRC.jobTriggers], ['Table update triggers', SRC.tableTrigger]],
      },
      {
        slide: 27,
        kicker: 'Patterns',
        title: 'Orchestration patterns in the DAG',
        blocks: [
          { type: 'points', items: [
            ['For-each task', 'Iterate one task over a list (regions, stores) with a concurrency limit — not 14 copied tasks or if/else chains.'],
            ['Run-if “All done”', 'A final task such as a status notification runs whether dependencies succeeded or failed.'],
            ['Retries with an interval', 'The first mechanism for intermittent failures that succeed on retry, such as flaky APIs.'],
            ['Named task types', 'A <strong>pipeline</strong> task runs a declarative pipeline inside the DAG; a <strong>dashboard</strong> task refreshes BI after the gold load.'],
          ]},
          { type: 'callout', label: 'Keyword map', body: '“Once per X, up to N in parallel” ⇒ for-each. “Notify regardless of outcome” ⇒ run-if All done.' },
        ],
        src: [['Schedules and triggers', SRC.jobTriggers]],
      },
      {
        slide: 28,
        kicker: 'Pipelines',
        title: 'Inferred order, declared quality',
        blocks: [
          { type: 'points', items: [
            ['Order is inferred', 'The engine reads who-reads-whom: silver reading bronze <em>is</em> the dependency declaration. No <code>depends_on</code> edges.'],
            ['Expectations, three policies', '<code>expect</code> (warn, keep rows) · <code>expect_or_drop</code> (drop rows, record metrics) · <code>expect_or_fail</code> (stop the update).'],
            ['Constraint ≠ expectation', 'A table CHECK constraint aborts the entire write. An expectation is a per-run pipeline policy with metrics.'],
            ['Streaming table', 'The object for incremental append ingestion. A pipeline runs inside a job DAG via the pipeline task type.'],
          ]},
          { type: 'callout', label: 'Old-name bait', tone: 'warn', body: 'DLT → Lakeflow Spark Declarative Pipelines. Current Python API: <code>from pyspark import pipelines as dp</code>.' },
        ],
        src: [['Expectations', SRC.expectations]],
      },
      {
        slide: 29,
        kicker: 'Wiring',
        title: 'Moving values between tasks and notebooks',
        blocks: [
          { type: 'table', head: ['Need', 'Mechanism', 'In code'], rows: [
            ['Job parameter → notebook task', 'Parameters surface as widgets', '<code>dbutils.widgets.get("env")</code>'],
            ['Task A computes a value Task B needs', 'Task values', '<code>dbutils.jobs.taskValues.set / .get</code>'],
            ['Reuse helper functions across notebooks in a session', '<code>%run</code>', '<code>%run ./helpers</code>'],
          ]},
          { type: 'callout', label: 'Scope check', body: '<code>%run</code> shares a session. A job task runs isolated — nothing defined there is shared.' },
        ],
        src: [['Task values', SRC.taskValues]],
      },
      {
        slide: 30,
        kicker: 'Observability',
        title: 'Repair runs and run history',
        blocks: [
          { type: 'points', items: [
            ['Repair run', 'Re-executes the failed task and its downstream tasks only. Already-successful tasks are never re-executed.'],
            ['Runtime creeping up across weeks?', 'The run history matrix — per-task durations compared across runs — is the first evidence: when it began, and which task.'],
            ['Single-run deep dive', 'The Spark UI. It inspects one run and cannot show a trend.'],
          ]},
          { type: 'callout', label: 'Contrast', body: 'Trend across runs ⇒ run history. Depth within one run ⇒ Spark UI.' },
        ],
        src: [['Repair job failures', SRC.repair], ['Spark UI guide', SRC.sparkUi]],
      },
    ],
  },

  /* ============================================================ DOMAIN 5 */
  {
    id: 'd5',
    num: 5,
    title: 'Implementing CI/CD',
    weight: 10,
    approxQ: 4,
    week: 'Week 3',
    summary:
      'Two ideas only: which Git operations happen inside Databricks, and how a bundle promotes one codebase across environments.',
    cards: [
      {
        slide: 31,
        kicker: 'Git',
        title: 'Git folders: what lives where',
        blocks: [
          { type: 'cols', cols: [
            { head: 'In the workspace Git folder', items: ['Create and switch branches', 'Commit changes', 'Push to the remote', 'The daily development loop'] },
            { head: 'Through the Git integration / provider workflow', items: ['Create and manage pull requests', 'Review and approve', 'Merge to main', 'The workspace links out; it does not merge for you'] },
          ]},
          { type: 'correction', body: 'The May 2026 guide explicitly includes creating pull requests using Databricks Git integration. Say “manage branches, commits, and pushes in Git folders; create and manage pull requests through the configured Git integration/provider workflow” rather than “PRs happen only in the Git provider.”' },
          { type: 'callout', label: 'Boundary', body: 'Branch, commit, and push inside Databricks. PR lifecycle through the provider integration (GitHub, GitLab, Azure DevOps).' },
        ],
        src: [['Git folders', SRC.gitFolders], ['Exam guide (May 4, 2026)', SRC.guide]],
      },
      {
        slide: 32,
        kicker: 'Bundles',
        title: 'One codebase, many targets',
        blocks: [
          { type: 'code', lang: 'yaml', body: '# databricks.yml — targets express the environments\ntargets:\n  dev:\n    variables: { schema: dev_analytics }\n  prod:\n    variables: { schema: analytics }\n    mode: production' },
          { type: 'flow', steps: [
            ['databricks bundle validate', 'syntax and references resolve'],
            ['databricks bundle deploy -t dev', 'place resources in the target'],
            ['databricks bundle run -t dev my_job', 'execute the deployed job'],
          ]},
          { type: 'correction', body: 'Use the May 2026 nomenclature: <strong>Declarative Automation Bundles</strong> (formerly Databricks Asset Bundles), and show complete CLI commands rather than bare subcommands.' },
          { type: 'callout', label: 'Promotion', body: 'Merge to main ⇒ CI runs <code>databricks bundle deploy -t prod</code> as a service principal. Nobody clicks Deploy.' },
        ],
        src: [['Bundle deployment modes', SRC.bundles], ['Configuration reference', SRC.bundleRef]],
      },
    ],
  },

  /* ============================================================ DOMAIN 6 */
  {
    id: 'd6',
    num: 6,
    title: 'Troubleshooting, Monitoring & Optimization',
    weight: 10,
    approxQ: 5,
    week: 'Weeks 3–4',
    summary:
      'Read the planted clue in the stem, then name the category. Most questions resolve to file layout, partition sizing, or where the memory pressure actually is.',
    cards: [
      {
        slide: 37,
        kicker: 'Maintenance',
        title: 'OPTIMIZE, VACUUM, and predictive optimization',
        blocks: [
          { type: 'points', items: [
            ['<code>OPTIMIZE</code>', 'Compacts many small files into fewer larger ones — faster reads.'],
            ['<code>VACUUM</code>', 'Deletes old files no longer referenced by the log. Time travel to versions older than the retention window stops working.'],
            ['Predictive optimization', 'Runs OPTIMIZE and VACUUM automatically for Unity Catalog managed tables. It does not rewrite queries and does not cover external tables.'],
          ]},
          { type: 'callout', label: 'Trap', tone: 'warn', body: 'The swapped pairing (“OPTIMIZE deletes, VACUUM compacts”) is the standard wrong answer. A 1-hour VACUUM retention breaks day-old time travel.' },
        ],
        src: [['VACUUM', SRC.vacuum], ['Predictive optimization', SRC.predictive]],
      },
      {
        slide: 38,
        kicker: 'Layout',
        title: 'Liquid clustering: layout without rewrites',
        blocks: [
          { type: 'code', lang: 'sql', body: 'CREATE TABLE sales (...) CLUSTER BY (store);\n\n-- query patterns changed? re-key without a rewrite:\nALTER TABLE sales CLUSTER BY (region, order_date);' },
          { type: 'points', items: [
            ['Incremental re-layout', 'After <code>ALTER … CLUSTER BY</code>, the new layout applies as data is written and optimized. No full rewrite, no re-ingest.'],
            ['Versus the legacy pair', 'Changing <code>PARTITIONED BY</code> means rebuilding the table. <code>ZORDER</code> requires re-running OPTIMIZE over history.'],
          ]},
          { type: 'callout', label: 'Keyword', body: '“Clustering keys no longer fit the queries” ⇒ <code>ALTER TABLE … CLUSTER BY</code>. That is the headline feature.' },
        ],
        src: [['Liquid clustering', SRC.clustering], ['CLUSTER BY clause', SRC.clusterBy]],
      },
      {
        slide: 39,
        kicker: 'Spark UI',
        title: 'Reading skew and spill',
        blocks: [
          { type: 'cols', cols: [
            { head: 'Data skew', items: ['Median task 35 s, max 41 min — max ≫ median', 'One task reads far more data than the rest', 'A few oversized partitions do all the work'] },
            { head: 'Spill', items: ['Large “Spill (Memory)” / “Spill (Disk)” values', 'Partitions too large for executor memory overflow to disk', 'Levers: more and smaller partitions, or more memory'] },
          ]},
          { type: 'points', items: [
            ['<code>spark.sql.shuffle.partitions</code>', 'Sets the partition count after a wide operation. On serverless, knobs like this are largely not settable — Databricks manages them.'],
            ['Query Profile reading order', 'Longest stage first → task-duration distribution → I/O and spill counters.'],
          ]},
        ],
        src: [['Skew and spill', SRC.skewSpill], ['Spark UI guide', SRC.sparkUi]],
      },
      {
        slide: 40,
        kicker: 'Triage',
        title: 'Failure triage: read the clue, name the category',
        blocks: [
          { type: 'table', head: ['Symptom', 'Diagnosis', 'First lever'], rows: [
            ['<code>collect()</code> on 300 M rows kills the session; executors show no pressure', 'Driver OOM — <code>collect()</code> funnels everything to the driver', '<code>spark.driver.memory</code> as a stopgap; the real fix is not collecting'],
            ['Job dies at cluster start, before any Spark stage; init script error in the event log', 'Infrastructure / cluster startup failure — not code', 'Fix the init script or environment'],
            ['<code>ModuleNotFoundError</code> today; the same notebook worked yesterday on another cluster', 'Library not installed on the compute now attached', 'Install the library on this cluster'],
          ]},
          { type: 'callout', label: 'Planted clue', body: '“Executors healthy” points at the driver. “Before any stage” points at infrastructure.' },
        ],
        src: [['Spark UI guide', SRC.sparkUi]],
      },
    ],
  },

  /* ============================================================ DOMAIN 7 */
  {
    id: 'd7',
    num: 7,
    title: 'Governance & Security',
    weight: 15,
    approxQ: 7,
    week: 'Week 4',
    summary:
      'Third-heaviest domain. The privilege chain, the DENY veto, and the choice between masks, row filters, and ABAC carry most of the questions.',
    cards: [
      {
        slide: 33,
        kicker: 'Privileges',
        title: 'The privilege chain — and the veto',
        blocks: [
          { type: 'flow', steps: [
            ['USE CATALOG', 'on the catalog'],
            ['USE SCHEMA', 'on the schema'],
            ['SELECT', 'on the table — or on the schema'],
          ]},
          { type: 'points', items: [
            ['Grant SELECT at the schema', 'Covers all current <em>and</em> future tables. Per-table grants miss tomorrow’s tables; <code>ALL PRIVILEGES</code> over-grants.'],
            ['DENY beats every grant', 'A user inheriting SELECT through a group can still be blocked: DENY on that user wins. <code>REVOKE</code> removes one specific grant; a DENY is removed by revoking that denial.'],
          ]},
          { type: 'callout', label: 'Symptom', body: '“Has SELECT, still gets a permission error” ⇒ missing <code>USE CATALOG</code> / <code>USE SCHEMA</code>.' },
        ],
        src: [['DENY', SRC.deny], ['Manage privileges', SRC.privileges], ['Privileges reference', SRC.privRef]],
      },
      {
        slide: 34,
        kicker: 'Principals',
        title: 'Principals — and who masks apply to',
        blocks: [
          { type: 'points', items: [
            ['Three principal types', 'Users, groups, and service principals. Tables, catalogs, and functions are <em>securables</em>, not principals; clusters and warehouses are neither.'],
            ['Grant to groups', 'Individual grants do not scale and do not survive turnover. The exam’s best-practice answer is the group.'],
            ['Machines get identities too', 'A production job or CI pipeline authenticates as a <strong>service principal</strong>, never as a named person.'],
            ['Owners are not exempt from masks', 'A table owner outside the allowed group sees masked values like everyone else. Ownership administers; it does not bypass policy.'],
          ]},
          { type: 'callout', label: 'Trap', tone: 'warn', body: '“The owner sees the real emails” — false. Masks and filters apply on every query path, to everyone.' },
        ],
        src: [['Row filters and column masks', SRC.masks], ['Securable objects', SRC.securables]],
      },
      {
        slide: 35,
        kicker: 'Fine-grained',
        title: 'Row filters, column masks, ABAC',
        blocks: [
          { type: 'table', head: ['Requirement', 'Feature', 'How it binds'], rows: [
            ['Support sees raw emails; others see masked — same table', 'Column mask', 'SQL function + <code>ALTER TABLE … SET MASK</code>'],
            ['Each vendor sees only its region’s rows, on every query path', 'Row filter', 'Function + <code>ALTER TABLE … SET ROW FILTER</code>'],
            ['Identical masking on every column tagged <code>pii_email</code>, 3,000 tables, managed centrally', 'ABAC policy', 'Tag-driven — no per-table edits'],
          ]},
          { type: 'callout', label: 'Rule-outs', body: '“No extra copies / every query path” eliminates per-audience views. “Thousands of tables, central team” ⇒ ABAC.' },
        ],
        src: [['Apply filters and masks', SRC.masksApply], ['ABAC', SRC.abac], ['ABAC vs RLS/CM', SRC.abacVs]],
      },
      {
        slide: 36,
        kicker: 'Sharing',
        title: 'Delta Sharing and lineage',
        optional: true,
        blocks: [
          { type: 'cols', cols: [
            { head: 'Databricks ↔ Databricks', items: ['The recipient mounts the share in their own Unity Catalog', 'Full UC-native experience'] },
            { head: 'Open sharing protocol', items: ['The recipient is not on Databricks — pandas, Power BI, Spark', 'Live read access through the protocol — no CSV exports, no copies'] },
          ]},
          { type: 'points', items: [
            ['Lineage is automatic', 'UC captures upstream and downstream lineage from query execution. View it on the table’s Lineage tab in Catalog Explorer. No scanner to install.'],
          ]},
          { type: 'callout', label: 'Optional enrichment', body: 'Useful real-world material, but not explicitly named in the May 2026 governance objectives. Cut it first if you are running behind.' },
        ],
        src: [['Open sharing protocol', SRC.sharing], ['Shares, providers, recipients', SRC.sharingHome]],
      },
    ],
  },
];

/* --------------------------------------------------------------- drills */

const DRILLS = [
  { q: 'SQL-only team, nightly new CSV files, reruns must be safe', a: 'COPY INTO', why: 'Idempotent file tracking, pure SQL, no streaming machinery needed.', d: 'd2' },
  { q: 'Millions of files, ongoing ingestion, new columns keep appearing', a: 'Auto Loader with schema evolution', why: 'Checkpointed incremental discovery; addNewColumns handles the drift.', d: 'd2' },
  { q: 'The source has duplicate keys before an upsert', a: 'Deduplicate the source, then MERGE', why: 'Only source dedup resolves “a target row matched multiple source rows.”', d: 'd3' },
  { q: 'Files arrive unpredictably in a UC external location', a: 'Lakeflow Job file-arrival trigger', why: 'The noun is files landing — no polling schedule required.', d: 'd4' },
  { q: 'A user inherits SELECT through a group but must be blocked from one sensitive table', a: 'DENY', why: 'DENY takes precedence over explicit and inherited grants.', d: 'd7' },
  { q: 'Process everything available on a schedule, with no always-on cluster', a: 'trigger(availableNow=True)', why: 'A streaming read executed as a scheduled batch.', d: 'd2' },
  { q: 'Dashboard reruns the same expensive 5-table aggregate all day', a: 'Materialized view with a refresh strategy', why: 'Precomputed results; reads become cheap.', d: 'd3' },
  { q: 'One task runs 41 minutes while the median task runs 35 seconds', a: 'Data skew', why: 'Max ≫ median in the task duration distribution.', d: 'd6' },
  { q: 'Same job, same code, runtime has crept up over six weeks', a: 'Run history matrix', why: 'Only run history shows a trend across runs; the Spark UI is one run deep.', d: 'd6' },
  { q: 'The clustering keys no longer match how the table is queried', a: 'ALTER TABLE … CLUSTER BY', why: 'Liquid clustering re-keys incrementally, with no table rebuild.', d: 'd6' },
  { q: 'Identical masking needed on every column tagged pii_email across 3,000 tables', a: 'ABAC policy', why: 'Tag-driven and centrally managed; no per-table ALTER statements.', d: 'd7' },
  { q: 'Job is fully configured this week but must not execute until go-live', a: 'Paused trigger', why: 'Deployed and complete, executes nothing until unpaused.', d: 'd4' },
];

/* ----------------------------------------------------------------- quiz */

const QUIZ = [
  {
    d: 'd3',
    q: 'A MERGE fails with “a target row matched multiple source rows.” What resolves it?',
    opts: ['Deduplicate the source before merging', 'Add a WHEN NOT MATCHED BY SOURCE clause', 'Tighten the ON condition with an extra predicate', 'Switch the statement to UPSERT INTO'],
    a: 0,
    why: 'The error is caused by duplicate merge keys in the source. Changing WHEN clauses or the ON condition does not resolve ambiguous matches, and UPSERT INTO does not exist.',
  },
  {
    d: 'd2',
    q: 'A SQL-only team loads roughly 50 new CSV files each night from a UC volume and needs reruns to be safe. Best fit?',
    opts: ['Auto Loader in file notification mode', 'COPY INTO', 'CREATE OR REPLACE TABLE from read_files', 'A Lakeflow Connect managed connector'],
    a: 1,
    why: 'COPY INTO is pure SQL and tracks loaded files, so a rerun adds no duplicates. CREATE OR REPLACE reprocesses everything; Auto Loader is more machinery than this scale needs.',
  },
  {
    d: 'd2',
    q: 'An Auto Loader stream using the default schema-evolution mode meets a brand-new column. What happens?',
    opts: ['The new column is silently dropped', 'The stream fails permanently until the schema is edited by hand', 'The stream stops once with a schema-change error, updates the schema location, and continues after restart', 'The values land in _rescued_data and the stream keeps running'],
    a: 2,
    why: 'addNewColumns is a deliberate stop-and-recover. _rescued_data is the type-mismatch behavior, not the new-column behavior.',
  },
  {
    d: 'd7',
    q: 'A user has SELECT on the table but still gets a permission error. Most likely cause?',
    opts: ['Missing USE CATALOG or USE SCHEMA', 'The table is external', 'A row filter is applied', 'The user is not the table owner'],
    a: 0,
    why: 'The privilege chain is USE CATALOG → USE SCHEMA → SELECT. A missing traversal privilege is the classic symptom.',
  },
  {
    d: 'd7',
    q: 'A user inherits SELECT through a group membership but must be blocked from one sensitive table. What do you use?',
    opts: ['REVOKE SELECT from the user', 'DENY SELECT on the table to the user', 'Remove the user from the group', 'Create a per-audience view'],
    a: 1,
    why: 'DENY takes precedence over explicit and inherited grants. REVOKE only removes a grant the user was directly given.',
  },
  {
    d: 'd4',
    q: 'A downstream task shows “upstream failed.” What actually happened?',
    opts: ['The task ran and threw an exception', 'The task was skipped because its dependency failed', 'The task timed out waiting for compute', 'The task retried three times and gave up'],
    a: 1,
    why: 'The task never ran. Its dependency failed, so the DAG skipped it.',
  },
  {
    d: 'd4',
    q: 'A job failed at task 4 of 6. After fixing the bug, what does Repair run re-execute?',
    opts: ['The whole job from task 1', 'Only task 4', 'Task 4 and its downstream tasks', 'Nothing — a new run is required'],
    a: 2,
    why: 'Repair run re-executes the failed task plus everything downstream of it. Already-successful tasks are not re-run.',
  },
  {
    d: 'd6',
    q: 'A table is queried constantly and reads are slow because of thousands of tiny files. Which command addresses it directly?',
    opts: ['VACUUM', 'OPTIMIZE', 'RESTORE', 'ANALYZE TABLE'],
    a: 1,
    why: 'OPTIMIZE compacts small files into fewer larger ones. VACUUM deletes unreferenced files and does not compact — the swapped pairing is the standard distractor.',
  },
  {
    d: 'd6',
    q: 'A notebook calling collect() on 300 million rows kills the session, while executor metrics look healthy. Diagnosis?',
    opts: ['Executor OOM from partition size', 'Driver OOM', 'Cluster startup failure', 'Shuffle spill to disk'],
    a: 1,
    why: 'collect() funnels all results to the driver. “Executors healthy” is the planted clue pointing at the driver.',
  },
  {
    d: 'd3',
    q: 'Reported revenue dropped after a developer changed a LEFT JOIN to an INNER JOIN. Why?',
    opts: ['INNER JOIN deduplicates rows', 'Fact rows with no matching dimension row were silently dropped', 'The join switched to a broadcast join', 'NULL keys were converted to zero'],
    a: 1,
    why: 'INNER JOIN drops non-matching rows without warning. LEFT JOIN plus COALESCE keeps and labels them.',
  },
  {
    d: 'd1',
    q: 'A managed table was dropped by mistake 10 minutes ago. Fastest recovery?',
    opts: ['UNDROP TABLE', 'RESTORE TABLE … TO VERSION AS OF', 'Re-run the ingestion pipeline', 'Recreate the table over the same storage path'],
    a: 0,
    why: 'UNDROP recovers a dropped managed table, subject to the applicable retention configuration. RESTORE reverts versions of a table that still exists.',
  },
  {
    d: 'd5',
    q: 'Which operation is not performed inside the Databricks workspace Git folder UI?',
    opts: ['Creating a branch', 'Committing changes', 'Pushing to the remote', 'Approving and merging a pull request'],
    a: 3,
    why: 'Branch, commit, and push happen in the Git folder. PR review, approval, and merge happen through the configured Git provider integration.',
  },
];
