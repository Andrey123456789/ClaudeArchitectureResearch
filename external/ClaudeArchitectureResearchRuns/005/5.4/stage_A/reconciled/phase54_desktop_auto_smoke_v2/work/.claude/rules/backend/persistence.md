---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Kind: STD | Scope: backend | Owner: persistence behavior — database access efficiency, Development database configuration, development seeding | Loading: path-scoped

# Persistence Standard

Persistence stack: D-04.

See also: `rules/backend/architecture.md` (repositories, Unit of Work, EF Core boundary), `rules/backend/security.md` (raw SQL safety).

## Database access

- Default: filter and project in the database when practical, avoid unnecessary round trips, over-fetching and N+1 patterns, and paginate potentially large result sets.

## Development database configuration

- Default: for the SQL Server baseline, `appsettings.Development.json` provides a usable local Development connection string when it contains no secret credentials. Credential-bearing local values must come from user-secrets or another approved local secret mechanism (`rules/common/security.md` § Secrets).

## Development seeding

- Default: an empty Development database receives a small, deterministic, representative seed dataset that covers the meaningful entity states and relationships.
- Development seeding is an Infrastructure/bootstrap concern: it may use `AppDbContext` directly and does not need Application repositories or `IUnitOfWork`.
- Keep substantial seed construction in a dedicated internal seeder (for example `Persistence/Seeding/DbSeeder.cs`) behind a narrow Infrastructure initialization extension — not in `Program.cs`, `DbContext` configuration, entity configurations or migrations.
- Automatic development seeding must run only in the Development environment; never seed Production automatically. The development seeder is never test setup (`rules/backend-tests/testing.md` § Isolation and data).
- The seeder must not call `Database.Migrate()` or `EnsureCreated()` or otherwise create or upgrade schema; migrations are applied separately before seeding.
- When representative data already exists, leave it unchanged: the seeder must not synchronize, repair, upgrade, overwrite or recreate an existing Development database. Developers recreate a local database explicitly when they need a fresh dataset.
- Seed entities must preserve current Domain invariants and valid relationships. Prefer readable, deterministic examples over exhaustive or random combinations.
