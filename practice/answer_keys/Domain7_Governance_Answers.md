# Domain 7 — Governance & Security — Answer Key

**Q1 — C: `USE CATALOG` + `USE SCHEMA` + `SELECT`.** All three are required to read. SELECT alone, USE SCHEMA + SELECT, or OWN/MODIFY are incomplete or wrong.

**Q2 — C: A missing `USE CATALOG` or `USE SCHEMA` privilege.** The classic "I have SELECT but can't query" cause. Table format, time travel, and warehouse type don't block reads this way.

**Q3 — D: REVOKE removes a grant; DENY applies only to legacy hive_metastore.** Unity Catalog does not support DENY, so you cannot "override all grants" on a UC object — REVOKE removes a grant (access may survive via a group). In UC, control access with groups, REVOKE, masks/row filters, and ABAC. (The exam guide still lists DENY; the product reference says it's unsupported on UC — know both.)

**Q4 — B: Groups.** Grant to groups so access scales. Per-user grants don't scale; limiting to service principals or admins only is wrong.

**Q5 — A: Two steps — a function that decides, then `ALTER TABLE ... SET MASK`.** Same two-step pattern for row filters (`SET ROW FILTER`). Not one GRANT, not a three-step view dance, not automatic.

**Q6 — A: Masked values — owners are not exempt.** Masks apply per user regardless of ownership. Not real values, an error, or forced NULLs.

**Q7 — D: Column → mask; rows → filter; many tagged tables → ABAC.** The correct discriminators. The others swap mask/filter, understate ABAC, or wrongly claim filters copy data.

**Q8 — B: A service principal.** A service principal is a machine identity designed for production jobs and CI/CD. Personal admin accounts are not appropriate automation identities, anonymous users cannot hold the required access, and a storage credential is a securable credential rather than the job's principal.

**Q9 — C: `ALTER TABLE ... SET MANAGED`.** For an eligible external Delta table on supported compute, this converts the table to Unity Catalog managed while retaining history and configuration. `CONVERT TO DELTA` changes a non-Delta table's format, OPTIMIZE changes file layout, and GRANT controls privileges.

**Q10 — B: Managed deletes data + metadata; external deletes metadata only.** External files remain after a drop; managed files are removed. "Both delete" / "both keep" / reversed are the distractors.

**Q11 — True.** `UNDROP TABLE` recovers a dropped *managed* table within the retention window — so managed drops are *not* instantly unrecoverable.

**Q12 — D: Tag-driven ABAC.** At scale, tag columns and write one policy per tag, applied to all current and future tagged tables. Per-table functions, per-audience views, and blanket denial don't scale.

**Q13 — A: Users, groups, and service principals.** These are principals that can receive Unity Catalog privileges. Tables, views, volumes, catalogs, schemas, and functions are securable objects; clusters, warehouses, and SQL statements are not principal types.
