---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
  - "backend/**/appsettings*.json"
---

> **Policy rule** · Capability: persistence/ef-core · Owns: EF Core usage inside the adapter layer, development seeding, SQL Server provider configuration, persistence mechanisms · Scope: backend · Loading: path (backend code, project files, appsettings)

# Persistence Technology Rules

Stable roles (domain layer, use-case layer, persistence-access contract, commit
boundary, adapter layer, composition root) are bound by the architecture frame in
`docs/architecture.md`. Technique and examples: the `ef-core` skill.

## Technology Boundary

- Persistence-technology types of this implementation are `DbContext` (the
  application's `AppDbContext`), `DbSet<T>`, EF Core LINQ query expressions and
  EF-backed `IQueryable<T>`, `Microsoft.EntityFrameworkCore.*` APIs, and SqlServer
  provider types. The frame's boundary rules keep them inside the adapter layer.
- Inside the adapter layer, use EF Core normally and take advantage of its
  capabilities; do not cripple repository implementations merely to preserve a
  generic abstraction.
- Commit-boundary binding: the commit boundary is implemented over the scoped
  `AppDbContext` and delegates to `DbContext.SaveChangesAsync`; repositories in the
  same use case share that scoped context (registered by `AddDbContext`).

## Development Seeding

- Default: an empty Development database receives a small, deterministic,
  representative seed dataset that covers the meaningful states and relationships
  needed during development (for example newly created, active, completed,
  archived, with and without optional values or relationships, representative
  status values, meaningful boundary states). Do not generate every combination;
  when the required graph is complex, ask for the dataset to be described rather
  than inventing a large generic object graph.
- Development seeding is an adapter-layer/bootstrap concern and may use
  `AppDbContext` directly; it need not go through persistence-access contracts or
  the commit boundary.
- Keep substantial seed construction in a dedicated internal `DbSeeder`
  (adapter layer, `Persistence/Seeding/`) exposed through a narrow initialization
  extension; do not place it in `Program.cs`, `AppDbContext`, entity
  configurations, or migrations.
- Automatic development seeding runs only when the host environment is
  `Development`. Never seed Production automatically, and never use the
  development seeder as test setup.
- The seeder must not call `Database.Migrate()`, `EnsureCreated()`, or otherwise
  create or upgrade the schema; migrations are applied separately before seeding.
- If representative data already exists (checked through one or more root/anchor
  entities), leave it unchanged. Do not use the seeder as automatic
  synchronization, repair, upgrade, overwrite, or recreation of an existing
  Development database; a developer recreates the local database explicitly when
  a fresh dataset is needed.
- Seed entities must preserve current Domain invariants and valid relationships;
  prefer readable deterministic examples over exhaustive or random combinations.

## Provider Configuration

Default: `appsettings.Development.json` provides a usable local Development
connection string (`ConnectionStrings:DefaultConnection`) when it contains no
secret credentials; a suitable Windows default is
`Server=(localdb)\MSSQLLocalDB;Database=<Name>;Trusted_Connection=True;TrustServerCertificate=True;`
(escape the backslash in JSON).
When local SQL Server requires credentials, keep the non-secret structure in
configuration and supply the credential through user-secrets or another approved
local secret mechanism.

## Mechanisms

- Migration mechanism: EF Core migrations in the adapter layer
  (`Persistence/Migrations/`), created from the adapter-layer project with the
  composition-root project as startup project:
  `dotnet ef migrations add <MigrationName> --project <adapter-layer project> --startup-project <composition-root project>`.
- Seeding mechanism: the internal `DbSeeder` invoked from the composition root
  only in Development through the initialization extension.
- Relational testing binding: the EF Core InMemory provider is not relational;
  provider-fidelity tests use the SQL Server provider (LocalDB, or Testcontainers
  when isolated real-provider tests justify it).
- Observable string semantics: string equality, uniqueness, and lookup follow the
  database collation; the product decision is governed by `CLAUDE.md` → Product
  Sources.
