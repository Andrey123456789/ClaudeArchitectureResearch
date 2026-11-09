---
paths:
  - "backend/**/*"
---
> Level: 2-technology | Capability: persistence/ef-core (persistence.rules) | Owns: EF Core role binding, development seeding, SQL Server development configuration | Scope: backend | Loads: path (backend files)

# Data Access — EF Core

## Role binding

- Persistence-technology types of this module: `DbContext` (the application's
  `AppDbContext`), `DbSet<T>`, EF Core APIs and LINQ-to-EF expressions,
  EF-backed `IQueryable<T>`, and SQL Server provider types.
- Commit boundary: the commit-boundary implementation delegates to
  `AppDbContext.SaveChangesAsync`; the scoped `AppDbContext` is the unit of work
  shared by the persistence-access implementations of one use case.
- Persistence-access implementations are EF Core repositories that stage
  changes in the scoped `AppDbContext`.

## Development seeding

- Default: an empty Development database receives a small, deterministic,
  representative seed dataset covering the meaningful states and relationships
  (new, active or in progress, completed, inactive or archived, with and
  without optional values and relationships, meaningful boundary states).
- Development seeding is an adapter/startup-initialization concern: it may use
  `AppDbContext` directly and does not need persistence-access contracts or the
  commit-boundary contract.
- Keep substantial seed construction in a dedicated internal seeder (`DbSeeder`
  under the persistence implementation's `Seeding/` folder), exposed only
  through a narrow initialization extension — never in `Program.cs`,
  `AppDbContext`, entity configurations, or migrations.
- Automatic seeding runs only in the `Development` environment. Never seed
  Production automatically; tests own their setup and never use the
  development seeder.
- The seeder must not call `Database.Migrate()`, `EnsureCreated()`, or otherwise
  create or upgrade schema; migrations are applied separately before seeding.
- When representative data already exists (checked through one or more anchor
  entities), leave it unchanged. The seeder is never an automatic
  synchronization, repair, upgrade, overwrite, or recreation mechanism for an
  existing Development database; developers recreate a local database
  explicitly when they need the current dataset.
- Seed entities must preserve current domain invariants and valid
  relationships; prefer readable deterministic examples over exhaustive or
  random combinations. When the required graph is complex, the task should
  describe the dataset explicitly.

## Development database configuration

Default: `appsettings.Development.json` provides a usable local Development
connection string when it contains no secret credentials (for example SQL Server
LocalDB with `Trusted_Connection=True`). When local SQL Server requires
credentials, keep the non-secret structure in configuration and supply the
credential through user-secrets or another approved local secret mechanism.

Procedures: `persistence.workflow`, `persistence.scaffold`. Technique: `ef-core`.
