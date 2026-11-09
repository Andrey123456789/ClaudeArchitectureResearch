---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Path-scoped rule. Owns: repository contracts, generic-repository limits, Unit of Work, transactions, the EF Core boundary, Development seeding, local Development database configuration · Scope: backend · Loads: when backend C# or appsettings files are in context · Depends on: CLAUDE.md, docs/technology-stack.md · Enforced by: .claude/scripts/check-architecture.mjs

# Persistence Rules

Layer boundaries: `architecture.md`. Technique and examples: `ef-core` skill.
Seed-data co-change, migration review, and production database deployment:
`development-workflow`.

## Repositories

- Repository interfaces are inward-facing persistence contracts: define them in
  Application and implement them in Infrastructure.
- Default: specific repository interfaces that represent actual, cohesive
  Application persistence needs rather than table-mirroring generic CRUD
  contracts. When an approved DDD design contains Aggregate Roots, they are the
  natural repository-boundary candidates.
- Repository interfaces must not expose `IQueryable<T>`, `DbSet<T>`,
  `DbContext`, EF Core expressions, or provider-specific types; they return
  materialized entities, collections, projections, or explicit result models.
  LINQ-to-EF query construction stays in Infrastructure.
- Application must not depend on `IGenericRepository<T>` or another generic
  CRUD contract. A generic repository or a `Repository<TEntity>` base class may
  exist only as an Infrastructure implementation detail that removes genuine
  duplication; do not grow it into a replacement for EF Core query
  capabilities. Use-case-specific queries belong in concrete repositories.

## Unit of Work

- Default: `IUnitOfWork` is the commit boundary of an Application use case.
  Repositories stage changes and do not call `SaveChangesAsync` independently;
  Application Services decide when an operation is ready to commit.
  Infrastructure implements `IUnitOfWork` over the application's `DbContext`.
- Repositories participating in one use case must share the same Unit of Work
  and scoped `DbContext`, and are injected explicitly into their consumers.
  `IUnitOfWork` must not become a repository container or service locator that
  exposes repositories as properties.
- Default: no explicit transaction APIs until a concrete use case requires
  transaction control beyond a normal `SaveChangesAsync`.

## EF Core Boundary

- EF Core is an Infrastructure implementation detail: use its full capabilities
  inside Infrastructure, and do not leak EF Core concepts into Application. Do
  not cripple repository implementations merely to preserve a generic
  abstraction.

## Development Seeding

- Default: an empty Development database receives a small, deterministic,
  representative seed dataset covering the meaningful states and relationships
  needed to exercise the application.
- Development seeding is an Infrastructure/bootstrap concern. It may use
  `AppDbContext` directly and need not go through Application repositories or
  `IUnitOfWork`.
- Substantial seed construction lives in a dedicated internal seeder (for
  example `Persistence/Seeding/DbSeeder.cs`) exposed through a narrow
  Infrastructure initialization extension — not in `Program.cs`, `DbContext`
  configuration, entity configurations, or migrations.
- Automatic seeding runs only in the `Development` environment; never seed
  Production automatically. Tests own their setup and must not use the
  development seeder.
- The seeder must not call `Database.Migrate()`, `EnsureCreated()`, or otherwise
  create or upgrade the schema; migrations are applied separately before
  seeding.
- If representative data already exists, leave it unchanged: the seeder must
  not synchronize, repair, upgrade, overwrite, or recreate an existing
  Development database. A developer recreates the local database explicitly
  when a fresh dataset is needed.
- Seed entities must preserve current Domain invariants and valid
  relationships; prefer readable deterministic examples over exhaustive or
  random combinations.

## Local Development Database Configuration

- Default: for the SQL Server baseline, `appsettings.Development.json` provides
  a usable local Development connection string when that connection string
  contains no secret credentials (for example SQL Server LocalDB with
  `Trusted_Connection=True`). Credential-bearing local values must be supplied
  through user-secrets or another approved local secret mechanism.
