---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Owns: Development data seeding and local Development database configuration | Scope: backend | Loads: path-scoped (backend C# and appsettings files)

# Persistence Rules

Repository, Unit of Work, and EF Core boundary rules: `architecture.md`.
Implementation technique and examples: `ef-core` skill. Keeping seed data current
when the model changes: `development-workflow` (persistence step).

## Development Seeding

- By default, maintain a small, deterministic, representative seed dataset for
  an empty Development database, covering the main meaningful states and
  relationships needed to exercise the application.
- Development seeding is an Infrastructure/bootstrap concern: it may use
  `AppDbContext` directly and does not need to go through Application
  repositories or `IUnitOfWork`.
- Keep substantial seed construction in a dedicated internal `DbSeeder` in
  Infrastructure (for example `Persistence/Seeding/`), exposed through a narrow
  initialization extension — not in `Program.cs`, `DbContext` configuration,
  entity configurations, or migrations.
- Automatic development seeding runs only in the `Development` environment.
  Never seed Production automatically. Tests own their own setup and never use
  the development seeder.
- The development seeder must not call `Database.Migrate()`, `EnsureCreated()`,
  or otherwise create or upgrade the schema; migrations are applied separately
  before seeding.
- If representative data already exists, leave it unchanged: do not use the
  seeder as an automatic synchronization, repair, upgrade, overwrite, or
  recreation mechanism for an existing Development database. A developer who
  needs the current dataset recreates the local database explicitly.
- Seed entities must preserve current Domain invariants and valid
  relationships; prefer readable deterministic examples over exhaustive or
  random combinations.

## Development Database Configuration

For the SQL Server baseline, `appsettings.Development.json` provides a usable
local Development connection string when that connection string contains no
secret credentials. Credential-bearing local values are supplied through
user-secrets or another approved local secret mechanism.
