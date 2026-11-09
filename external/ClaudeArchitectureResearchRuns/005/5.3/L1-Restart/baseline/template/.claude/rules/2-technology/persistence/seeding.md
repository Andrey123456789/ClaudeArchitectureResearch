---
paths:
  - "backend/**/*"
---

> Level: 2-technology · Capability: persistence/ef-core · Facet: persistence.seeding · Owns: Development data seeding · Scope: backend · Loading: path

# Development Seeding

- Default: for an empty Development database, maintain a small, deterministic, representative seed dataset covering the main meaningful states and relationships — new, active, completed, archived; with and without optional values and relationships; meaningful boundary states. Do not generate every combination or random bulk data.
- Development seeding is a persistence-implementation/bootstrap concern: it may use `AppDbContext` directly and need not go through persistence-access contracts or the commit boundary.
- Keep substantial seed construction in a dedicated internal `DbSeeder` exposed through a narrow initialization extension — not in `Program.cs`, `AppDbContext`, entity configurations, or migrations.
- Automatic seeding runs only in the `Development` environment; never seed Production automatically. Tests never use the seeder.
- The seeder must not call `Database.Migrate()` or `EnsureCreated()` or otherwise create or upgrade schema; migrations are applied separately before seeding.
- When representative data already exists (checked through one or more anchor entities), leave it unchanged: the seeder is never an automatic synchronization, repair, upgrade, overwrite, or recreation mechanism. Developers recreate a local database explicitly when they need a fresh dataset.
- Seed entities must preserve current domain invariants and valid relationships; prefer readable, deterministic examples over exhaustive or random combinations.

Co-change procedure: `persistence.workflow`. Example seeder: `ef-core` skill.
