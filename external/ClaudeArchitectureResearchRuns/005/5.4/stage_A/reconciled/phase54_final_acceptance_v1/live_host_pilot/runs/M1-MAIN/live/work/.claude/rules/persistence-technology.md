---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
  - "backend/**/appsettings*.json"
---

> Capability: persistence/ef-core · Path rule · Scope: backend · Owns the persistence-technology boundary, transactions, development seeding, and local database configuration

# Persistence Technology Rules: EF Core

Roles (adapter layer, use-case layer, core model, commit boundary) are mapped
in `docs/capabilities/architecture.md`. Change procedures for mappings,
migrations, and seed data: `persistence-change` workflow.

## Technology Boundary

- EF Core is an adapter-layer implementation detail. Inside the adapter layer,
  use EF Core directly and take advantage of its capabilities; do not cripple
  repository implementations merely to preserve a generic abstraction.
- Do not leak EF Core concepts into the use-case layer. For the architecture
  rules, the persistence-technology types are `DbContext` (including
  `AppDbContext`), `DbSet<T>`, EF Core APIs, `IQueryable<T>` backed by EF Core,
  EF query expressions, and provider-specific types. The persistence session is
  the scoped `AppDbContext` shared by the repositories and the Unit of Work of
  one use case.
- The repository boundary keeps persistence concerns out of the use-case layer;
  it does not hide EF Core from the adapter layer.

## Transactions

A single `SaveChangesAsync` call is the normal transaction boundary for one use
case. Do not introduce explicit transaction APIs until a concrete use case
requires control beyond normal `SaveChangesAsync`.

## Development Seeding

- By default, maintain a small, deterministic, representative seed dataset for
  an empty Development database that covers the main meaningful states and
  relationships; prefer readable deterministic examples over exhaustive or
  random combinations.
- Development seeding is an adapter-layer bootstrap concern and may use
  `AppDbContext` directly; it does not need to go through repositories or the
  Unit of Work.
- Keep substantial seed construction in a dedicated internal `DbSeeder` exposed
  through a narrow adapter-layer initialization extension, not in `Program.cs`,
  `AppDbContext` configuration, entity configurations, or migrations.
- Automatic development seeding runs only in the `Development` environment.
  Never seed Production automatically. Tests own their own setup and do not use
  the development seeder.
- The development seeder must not call `Database.Migrate()`, `EnsureCreated()`,
  or otherwise create or upgrade the schema; migrations are applied separately
  before seeding.
- If representative data already exists, leave it unchanged. Do not use the
  seeder for automatic synchronization, repair, upgrade, overwrite, or
  recreation of an existing Development database; developers recreate a local
  database explicitly when they need the current dataset.
- Seed entities must preserve the current Domain invariants and valid
  relationships.

## Relational Testing Binding

For the provider-fidelity rule in `.claude/rules/testing.md` § Database Tests,
the actual provider is SQL Server, and EF Core InMemory counts as a different,
non-relational provider.

## Local Development Database (provider variant: SQL Server)

`appsettings.Development.json` should provide a usable local Development
connection string when that connection string contains no secret credentials
(for example LocalDB with integrated security). When local SQL Server requires
credentials, keep the non-secret structure in configuration and supply the
secret value through user-secrets or another approved local secret mechanism.
