# R12 item 8.7 K1 local migrations: baseline and impact

**Target.** Remove only a truly additional mandatory local database mutation. Keep schema migration generation and review, schema before seed, and validation (PST-005, 006, 009, 010). If removal would lose a canonical duty, keep the duty and say why.

**Original.** K1 `persistence-change:45`: "5. Apply locally (`dotnet ef database update ...`), or drop and recreate the local database when a fresh dataset is needed." As a numbered step it applies in every model or mapping change, including one with no migration.

**Neighbor check.** PST-005 says migrations are applied separately before seeding: an order, not a duty to change a local database. PST-009 says create the migration and verify seeding remains valid. WF-006 sets a default startup smoke. None requires changing a local database in every scenario. The register notes this is not fully derived from PST-005 and PST-006, so a negative test is required: included.

**Kept on purpose.** Section A step 5 (initial setup applies the first migration, since startup seeding needs a schema) and section C (start against a freshly recreated Development database when seeding or the schema changed), because that is the validation duty the register tells us to keep.

**Parity.** M1 and L1 keep their own explicit "apply to a Development database" verification lines under their workflow. They are validation lines, not step-level mutation in every scenario, and the register names K1 only.
