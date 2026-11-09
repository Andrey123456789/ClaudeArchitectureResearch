---
paths:
  - "backend/**/*"
---

> Kind: STD | Scope: backend | Capability: persistence/ef-core | Loading: path-scoped (frontmatter paths)

# Persistence Technology — EF Core (variant: sqlserver)

Binds to the architecture frame: EF Core lives in the Infrastructure role and implements the Application persistence and commit-boundary contracts.

## Boundary

- EF Core is an Infrastructure implementation detail. Use its full capabilities inside Infrastructure, but EF Core concepts — `DbContext`, `DbSet<T>`, EF Core APIs, `IQueryable<T>` backed by EF Core, and provider-specific types — must not leak into Application.
- Infrastructure implements `IUnitOfWork` by delegating to the shared scoped `AppDbContext`.
- Default: no explicit transaction APIs until a concrete use case requires transaction control beyond a single `SaveChangesAsync`.

## Development seeding mechanism

- Development seeding is an Infrastructure/bootstrap concern and may use `AppDbContext` directly; it need not go through Application repositories or `IUnitOfWork`.
- Substantial seed construction lives in a dedicated internal `DbSeeder` (`Persistence/Seeding/` in Infrastructure), exposed through a narrow Infrastructure initialization extension — never in `Program.cs`, `AppDbContext` configuration, entity configurations, or migrations.
- The development seeder must not call `Database.Migrate()`, `EnsureCreated()`, or otherwise create or upgrade the schema; migrations are applied separately before seeding.

## Variant: sqlserver

- Default: `appsettings.Development.json` provides a usable local Development connection string when it contains no secret credentials; credential-bearing local values come from user-secrets or another approved local secret mechanism.

Technique: `ef-core`. Procedure: `persistence-change`. Enforced by: `.claude/scripts/facets/persistence-technology.cjs`.
