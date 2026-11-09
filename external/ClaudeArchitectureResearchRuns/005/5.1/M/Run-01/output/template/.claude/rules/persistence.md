---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Owns: Development data seeding, EF Core migration handling, production migration policy, local Development database configuration | Scope: backend | Loads: path

# Persistence Rules

Repository, Unit of Work, and EF Core boundary rules: `architecture.md`.
Implementation technique: `ef-core` skill.

## Development Data Seeding

- By default, maintain a small, deterministic, representative seed dataset for
  an empty Development database, covering the meaningful entity states and
  relationships needed to exercise the application. Prefer readable examples
  over exhaustive or random combinations. When the required graph is complex,
  the task should describe it rather than leaving it to be invented.
- Seeding is an Infrastructure/bootstrap concern. It may use `AppDbContext`
  directly and need not go through Application repositories or `IUnitOfWork`.
- Keep substantial seed construction in a dedicated internal `DbSeeder` (or
  equivalent Infrastructure initialization surface) exposed through a narrow
  initialization extension — not in `Program.cs`, `DbContext` configuration,
  entity configurations, or migrations.
- Automatic seeding runs only in the `Development` environment. Never seed
  Production automatically. Tests own their own setup and must not use the
  development seeder.
- The seeder must not call `Database.Migrate()`, `EnsureCreated()`, or otherwise
  create or upgrade schema; migrations are applied separately before seeding.
- If representative data already exists, leave it unchanged. The seeder is not
  an automatic synchronization, repair, upgrade, overwrite, or recreation
  mechanism; developers recreate local databases explicitly when they need a
  fresh dataset.
- Seed entities must preserve current Domain invariants and valid relationships.
- Whenever Domain or persistence changes affect seeded entities (properties,
  relationships, required related entities, enum/status values, invariants),
  update the seeder in the same change, so that recreating the Development
  database at any revision yields valid, representative data.

## Migrations

- EF Core migrations are source code. Review every generated migration before
  committing it, paying particular attention to destructive schema changes,
  unexpected column recreation, data migrations, indexes, foreign keys, and
  delete behavior. When a migration affects seeded entities, review the seeder
  with it.
- Do not apply production migrations automatically from normal application
  startup. Production migration is an explicit deployment operation using
  approved credentials, and Development seeding never runs in Production.

## Local Development Database Configuration

For the SQL Server baseline, `appsettings.Development.json` provides a usable
local Development connection string when it contains no secret credentials.
Credential-bearing local values are supplied through user-secrets or another
approved local secret mechanism, keeping only the non-secret structure in
configuration.
