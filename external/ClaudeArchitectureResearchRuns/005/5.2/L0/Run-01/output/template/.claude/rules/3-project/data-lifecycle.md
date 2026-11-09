---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Level: 3 Project | Owns: Development database configuration and development seed-data lifecycle | Scope: backend | Loads: path | Depends on: 2-technology/ef-core.md, 0-core/security-principles.md, 0-core/testing-principles.md

# Development Data Lifecycle

## Development Database Configuration

- Default: `appsettings.Development.json` provides a usable local Development
  connection string when it contains no secret credentials (for example
  `Server=(localdb)\\MSSQLLocalDB;Database=<Name>;Trusted_Connection=True;TrustServerCertificate=True;`).
  Credential-bearing local values must be supplied through `dotnet user-secrets`
  or another approved local secret mechanism.

## Development Seeding

- Default: an empty Development database receives a small, deterministic,
  representative seed dataset that covers the meaningful entity states and
  relationships (new, active, completed, archived; with and without optional
  values and relationships; boundary states) without exhaustive combinations.
- Development seeding is an Infrastructure/bootstrap concern; it may use
  `AppDbContext` directly and need not go through Application repositories or
  `IUnitOfWork`.
- Keep substantial seed construction in a dedicated internal `DbSeeder`
  (`Infrastructure/Persistence/Seeding/`) exposed through a narrow
  initialization extension — not in `Program.cs`, `AppDbContext` configuration,
  entity configurations, or migrations.
- Automatic seeding runs only in the `Development` environment; never seed
  Production automatically; tests own their setup and never use the seeder.
- The seeder must not call `Database.Migrate()`, `EnsureCreated()`, or otherwise
  create or upgrade the schema; migrations are applied separately before
  seeding.
- When representative data already exists, leave it unchanged; the seeder is
  not an automatic synchronization, repair, upgrade, overwrite, or recreation
  mechanism for an existing Development database. A developer recreates the
  local database explicitly to obtain a fresh dataset.
- Seed entities must preserve current Domain invariants and valid
  relationships; prefer readable deterministic examples over exhaustive or
  random combinations.

Model or migration changes that affect seeded entities: → `develop` (persistence changes). Seeder example: → `ef-core` skill.
