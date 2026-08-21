# Exam Domain 7 — Governance & Security (~15%)
# Score 100

## Q1: The full privilege chain to read a table is…
- [ ] `SELECT` privilege alone on the table
- [ ] `USE SCHEMA` together with `SELECT`
- [x] `USE CATALOG` + `USE SCHEMA` + `SELECT`
- [ ] `OWN` and `MODIFY` on the table
::time=45

## Q2: A user has `SELECT` but cannot query the table. Most likely cause?
- [ ] Time travel is enabled on the table
- [ ] The table is stored in Delta format
- [x] A missing `USE CATALOG` or `USE SCHEMA` privilege
- [ ] The SQL warehouse serving the query is serverless
::time=45

## Q3: In **Unity Catalog**, `REVOKE` versus `DENY`?
- [ ] They are identical operations on Unity Catalog objects
- [ ] DENY only affects the table's owner principal account
- [ ] REVOKE is unsupported in UC; you must use DENY instead
- [x] `REVOKE` removes a grant; `DENY` is unsupported in UC
::time=45

## Q4: Exam best practice is to grant privileges to…
- [ ] Individual users, one by one
- [x] Groups
- [ ] Service principals exclusively
- [ ] The metastore admin alone
::time=45

## Q5: A column **mask** (or row **filter**) is applied in how many steps?
- [x] Two: create the function, then bind it
- [ ] Three steps: create a view, grant on it, then revoke
- [ ] One step: a single `GRANT`
- [ ] Zero — it is automatic
::time=45

## Q6: You own a table with a mask on `email` but are not in the allowed group. You see…
- [x] Masked values — owners are not exempt
- [ ] Real values, because you are the table owner
- [ ] An error on every query
- [ ] NULLs in the masked column
::time=45

## Q7: Which discriminator is correct?
- [ ] Mask hides rows; a row filter hides a column's values, always
- [ ] ABAC can only ever hide a single specific column
- [ ] Row filters require making a full copy of the table
- [x] Mask columns; filter rows; use ABAC at tag scale
::time=45

## Q8: Which principal should represent a production job that needs table privileges?
- [ ] The metastore administrator's personal account
- [x] A service principal
- [ ] An anonymous workspace visitor
- [ ] The table's storage credential itself
::time=45

## Q9: Which command converts an eligible Unity Catalog external Delta table to a managed table while retaining its table configuration?
- [ ] `OPTIMIZE catalog.schema.table MANAGED`
- [ ] `CONVERT TO DELTA catalog.schema.table`
- [x] `ALTER TABLE catalog.schema.table SET MANAGED`
- [ ] `GRANT MANAGED ON TABLE catalog.schema.table`
::time=45

## Q10: `DROP` on a **managed** vs **external** table?
- [ ] Both managed and external drops delete the underlying data files
- [x] Managed deletes data + metadata; external deletes metadata only
- [ ] Both keep the underlying data files intact
- [ ] Managed keeps its files; external deletes them
::time=45

## Q11: A dropped **managed** table can be recovered with `UNDROP` within the retention window. True or false?
- [x] True
- [ ] False — a managed drop is permanent
::time=45

## Q12: At scale, one masking policy must cover thousands of tables tagged `pii`. The right approach is…
- [ ] A hand-written masking function bound per table
- [ ] One filtered view built for each audience
- [ ] Denying all access to everyone by default
- [x] Tag-driven Unity Catalog ABAC
::time=45

## Q13: Which set lists the Unity Catalog principal types that can receive privileges?
- [x] Users, groups, and service principals
- [ ] Tables, views, and volumes
- [ ] Catalogs, schemas, and functions
- [ ] Clusters, warehouses, and SQL statements
::time=45
