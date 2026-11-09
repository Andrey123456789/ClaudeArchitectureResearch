---
paths:
  - "backend/**"
  - "**/Dockerfile*"
  - "**/docker-compose*.yml"
  - "**/docker-compose*.yaml"
  - "**/compose*.yml"
  - "**/compose*.yaml"
  - ".github/workflows/**"
  - "**/*pipeline*.yml"
  - "**/*pipeline*.yaml"
---

> Level: 3 Project · Owns: Development database configuration, development seeding, settings-driven schema changes, production migration · Scope: backend, delivery · Loads: path; read explicitly by `verify`, `custom-settings`, `project-structure`

# Development Data Lifecycle

## Local Development database

- **Default:** `appsettings.Development.json` in the Api project provides a usable local Development connection string when it contains no secret credentials (on Windows, for example `Server=(localdb)\MSSQLLocalDB;Database=<Name>;Trusted_Connection=True;TrustServerCertificate=True;` under `ConnectionStrings:DefaultConnection`, with the backslash escaped in JSON). When local SQL Server needs credentials, keep the non-secret structure in configuration and supply the secret through `dotnet user-secrets` or another approved local secret mechanism.

## Development seeding

- **Default:** for an empty Development database, maintain a small, deterministic, representative seed dataset that covers the meaningful states and relationships — new, active/in progress, completed, archived; with and without optional values and relationships; representative status values and boundary states — without generating every combination. When the needed graph is complex, ask for an explicit dataset description instead of inventing a large generic object graph.
- **Must** treat seeding as an Infrastructure/bootstrap concern: the seeder may use `AppDbContext` directly and need not go through Application repositories or `IUnitOfWork`.
- **Must** keep substantial seed construction in a dedicated internal `DbSeeder` (`Infrastructure/Persistence/Seeding/`) behind a narrow Infrastructure initialization extension — not in `Program.cs`, `AppDbContext`, entity configurations or migrations.
- **Must not** seed automatically outside the `Development` environment; never seed Production automatically; tests use their own setup, never the development seeder.
- **Must not** let the seeder call `Database.Migrate()`, `EnsureCreated()` or otherwise create or upgrade the schema; migrations are applied separately before seeding.
- **Must not** use the seeder to synchronize, repair, upgrade, overwrite or recreate an existing Development database: when representative data already exists (checked through anchor entities), leave it unchanged. Developers recreate the local database explicitly when they need the current dataset.
- **Must** construct seed entities that satisfy the current Domain invariants and valid relationships; prefer readable deterministic examples over exhaustive or random combinations.
- **Must** update the maintained seeder in the same change whenever a Domain or persistence change affects seeded entities (new required or removed/renamed properties, changed relationships, enum or status values, states, invariants), including when a migration changes the seeded graph. Recreating the Development database at any revision yields valid, representative data.

## Settings-driven schema changes

- **Must**, when a `CUSTOM_SETTINGS.md` change affects schema constraints, indexes, column lengths or other persistence metadata: update the EF Core mapping; create the appropriate migration according to the project's migration workflow (a new migration when the schema must change; regenerate or edit only an uncommitted migration when that is the normal workflow); verify Development seeding remains valid; and update provider-sensitive persistence or integration tests when needed. Do not casually alter existing migrations.

## Production

- **Must not** apply production database migrations automatically from normal application startup. Production migration is an explicit deployment or operational step using approved credentials (generated migration scripts are often preferable), and Development seeding never runs in Production.

Technique: `ef-core` skill (seeder and migration mechanics).
