---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Owner: Unit of Work, EF Core boundary inside Infrastructure, development seeding, migrations, Development database configuration | Scope: backend | Loads: path (backend C# and appsettings); read explicitly by `verify`, `code-review`, `project-structure`, `custom-settings` | Enforced: Stop hook seed/migration co-change reminder

# Persistence Rules

## Unit of Work

- Default: `IUnitOfWork` is the commit boundary for an Application use case;
  repositories stage changes and do not independently call `SaveChangesAsync`,
  and Application Services decide when an operation is ready to commit.
- Repositories participating in one use case must share the same scoped Unit of
  Work and `DbContext`, and are injected explicitly into their consumers.
  `IUnitOfWork` must not act as a repository container or service locator that
  exposes repositories as properties.
- Default: do not introduce explicit transaction APIs until a concrete use case
  requires control beyond a normal `SaveChangesAsync`.

## EF Core Boundary

- Inside Infrastructure, use EF Core normally and take advantage of its
  capabilities; do not cripple repository implementations to preserve a generic
  abstraction. The repository boundary keeps EF Core concepts out of Application
  (`.claude/rules/architecture.md` § Application); it does not hide EF Core from
  Infrastructure.

## Development Seeding

- Default: an empty Development database receives a small, deterministic,
  representative seed dataset covering the meaningful states and relationships
  needed to exercise the application.
- Development seeding is an Infrastructure/bootstrap concern and may use
  `AppDbContext` directly; it does not need Application repositories or
  `IUnitOfWork`.
- Keep substantial seed construction in a dedicated internal seeder (for example
  `Persistence/Seeding/DbSeeder.cs`) behind a narrow Infrastructure
  initialization extension — not in `Program.cs`, `AppDbContext`, entity
  configurations, or migrations.
- Automatic seeding runs only in the `Development` environment; never seed
  Production automatically. Test data: `.claude/rules/testing.md` § Isolation
  and Test Data.
- The seeder must not call `Database.Migrate()`, `EnsureCreated()`, or otherwise
  create or upgrade the schema; migrations are applied separately before seeding.
- If representative data already exists, leave it unchanged: the seeder is not a
  synchronization, repair, upgrade, overwrite, or recreation mechanism for an
  existing Development database. A developer who needs the current dataset
  recreates the local database explicitly.
- Seed entities must preserve current Domain invariants and valid relationships;
  prefer readable deterministic examples over exhaustive or random combinations.
- Whenever a Domain or persistence change affects seeded entities, update the
  seeder in the same change, so that recreating the Development database at any
  revision yields valid, representative data.

## Migrations

- Treat EF Core migrations as source code: review generated migrations before
  committing them, paying particular attention to destructive schema changes,
  unexpected column recreation, data migrations, indexes, foreign keys, and
  delete behavior.
- Normal application startup must not apply production database migrations
  automatically; production migration is an explicit deployment or operational
  step, run at a controlled point with the project's approved credentials and
  migration strategy.

## Development Database Configuration

- Default: for the SQL Server baseline, `appsettings.Development.json` provides a
  usable local Development connection string when it contains no secret
  credentials; credential-bearing local values come from user-secrets or another
  approved local secret mechanism.
