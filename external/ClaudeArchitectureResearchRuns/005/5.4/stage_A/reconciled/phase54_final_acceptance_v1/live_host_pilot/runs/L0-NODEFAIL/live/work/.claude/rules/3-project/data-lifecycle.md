---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Level: 3 Project · Owns: Development data lifecycle — development seeding and local Development database configuration · Scope: backend · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/0-core/security-principles.md, .claude/rules/1-architecture/persistence-boundary.md, .claude/rules/2-technology/ef-core.md

# Development Data Lifecycle

Keeping the seeder current when the model changes: `development-workflow` → Co-changes. Technique and examples: the `ef-core` skill.

## Development seeding

- For an empty Development database, maintain a small deterministic, representative seed dataset that covers the meaningful states and relationships (default).
- Development seeding is an Infrastructure/bootstrap concern: it may use `AppDbContext` directly and need not go through Application repositories or `IUnitOfWork`.
- Keep substantial seed construction in a dedicated internal `DbSeeder` (for example `Infrastructure/Persistence/Seeding/DbSeeder.cs`), invoked through a narrow Infrastructure initialization extension — not in `Program.cs`, `AppDbContext` configuration, entity configurations, or migrations.
- Automatic development seeding runs only in the Development environment; never seed Production automatically. Tests own their setup and never use the seeder (`0-core/testing-principles.md`).
- The seeder must not call `Database.Migrate()` or `EnsureCreated()` or otherwise create or upgrade the schema; migrations are applied separately before seeding.
- If representative data already exists, leave it unchanged: never use the seeder for automatic synchronization, repair, upgrade, overwrite, or recreation of an existing Development database. A developer who needs the current dataset recreates the local database explicitly.
- Seed entities must preserve current Domain invariants and valid relationships; prefer readable deterministic examples over exhaustive or random combinations.

## Local Development database

- For the SQL Server baseline, `appsettings.Development.json` provides a usable local Development connection string when it contains no secret credentials (default), for example `Server=(localdb)\\MSSQLLocalDB;Database=<Name>;Trusted_Connection=True;TrustServerCertificate=True;`. Credential-bearing local values must come from user-secrets or another approved local secret mechanism.
