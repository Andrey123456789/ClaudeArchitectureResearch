from jdsl import C, D, P  # noqa: F401

P("PST-001",
  dims=["D1 for an empty Development database keep a small deterministic representative seed dataset covering meaningful states and relationships (default)"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each persistence rule: M rules/persistence.md:17-19, M1 rules/persistence-technology.md:38-41, L0 rules/3-project/data-lifecycle.md:15, L1 rules/2-technology/persistence/seeding.md:10, K0 rules/backend/persistence.md:25, K1 rules/backend/persistence.md:24. The state list (new, active, completed, archived, optional values/relationships, boundary states) sits in the rule (L1) or the ef-core skill (M, M1, L0, K0, K1); 'not every combination' appears in all six.")

P("PST-002",
  dims=["D1 Development seeding is an Infrastructure/bootstrap concern and may use AppDbContext directly, without repositories or IUnitOfWork"],
  label="FULL_SEMANTIC_PARITY",
  same="Same permission in each rule: M persistence.md:20-22, M1 persistence-technology.md:42-44, L0 data-lifecycle.md:16, L1 seeding.md:11, K0 persistence.md:26, K1 persistence-technology.md:20. Stored MUST reflects the placement half (it is an Infrastructure concern); the AppDbContext half is a permission in all six alike.")

P("PST-003",
  dims=["D1 substantial seed construction lives in a dedicated internal DbSeeder behind a narrow Infrastructure initialization extension, not in Program.cs, DbContext configuration, entity configurations or migrations"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST with the same four excluded places in each rule: M persistence.md:23-26, M1 persistence-technology.md:45-47, L0 data-lifecycle.md:17, L1 seeding.md:12, K0 persistence.md:27, K1 persistence-technology.md:21.")

P("PST-004",
  dims=["D1 automatic seeding runs only in Development; never seed Production automatically",
        "D2 tests own their setup and do not use the development seeder"],
  label="FULL_SEMANTIC_PARITY",
  same="Both parts in each rule: M persistence.md:27-29, M1 persistence-technology.md:48-50, L0 data-lifecycle.md:18, L1 seeding.md:13 ('Tests never use the seeder'), K0 persistence.md:28, K1 persistence.md:25. v2's C03 source review (WF-019 production-migration exception) holds in all six and does not touch automatic seeding. Delivery skills in L0, L1, K0, K1 repeat 'no automatic production seeding'.")

P("PST-005",
  dims=["D1 the development seeder does not call Database.Migrate(), EnsureCreated() or otherwise create/upgrade schema; migrations are applied separately first"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each rule: M persistence.md:30-32, M1 persistence-technology.md:51-53, L0 data-lifecycle.md:19, L1 seeding.md:14, K0 persistence.md:29, K1 persistence-technology.md:22. ef-core/workflow lines in all six add 'apply migrations to the local Development database first'. No candidate checks a seeder's calls mechanically.")
