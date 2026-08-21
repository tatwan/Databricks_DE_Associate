# Domain 1 — Databricks Intelligence Platform — Answer Key

**Q1 — B: Web UI, job scheduler, Unity Catalog metastore.** These managed services are the control plane. Data files and executors are the compute plane; it is not "only warehouses" or "nothing."

**Q2 — D: The customer's own cloud account.** Classic compute runs in the customer account (VPC/subscription). Not the control plane, a laptop, or the metastore.

**Q3 — A: A Databricks-managed environment.** Serverless runs in Databricks-managed infrastructure (what Free Edition uses). Not the customer account, on-prem, or a Git provider.

**Q4 — A: A job cluster.** It is created per run and terminated after, so it avoids the idle cost of a long-running interactive cluster. This does not claim that one compute product is universally cheapest; actual cost depends on workload and pricing.

**Q5 — B: A SQL warehouse.** Warehouses (serverless/pro/classic) serve SQL, BI, and dashboards. All-purpose and job clusters are general compute; the driver isn't a BI engine.

**Q6 — D: "Serverless is always cheaper."** Serverless is always *simpler*, but cost depends on workload shape — the "always cheaper" claim is the trap. The other three are true statements about serverless.

**Q7 — C: `catalog.schema.table`.** The UC namespace is catalog → schema → table. The others invert levels or add wrong ones.

**Q8 — C: Interactive development and shared notebook work.** All-purpose clusters are for interactive/dev use. They are not the cheapest for production, not SQL-only, and don't host the metastore.

**Q9 — A: A service principal.** Machine identity for jobs/CI. Personal accounts, admin passwords, and anonymous tokens are not the pattern.

**Q10 — D: Delta is a table format; Parquet is a file format.** Delta = Parquet data files + a transaction log. The reversed and "both the same" options are wrong.

**Q11 — B: Delta Lake.** Delta Lake adds a transaction log, ACID behavior, and versioned table state on top of cloud files. A SQL warehouse is compute, Unity Catalog is governance, and a Git folder versions source code.

**Q12 — C: Delta.** Delta is the implicit default (`USING DELTA`). Parquet, Iceberg, and CSV require explicit handling.
