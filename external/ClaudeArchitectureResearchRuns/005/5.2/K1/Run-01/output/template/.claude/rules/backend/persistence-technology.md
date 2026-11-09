---
paths:
  - "backend/**"
---
Kind: STD | Scope: backend | Capability: persistence/ef-core | Loading: path-scoped (backend/**)

# Persistence Technology Standards: EF Core with SQL Server

## Role bindings

- Persistence-technology types (kept out of Domain and Application by `architecture-style.md`): `DbContext` and `AppDbContext`, `DbSet<T>`, EF Core APIs and query expressions, `IQueryable<T>` backed by EF Core, and SQL Server provider types.
- Persistence session: the scoped `AppDbContext`. The Infrastructure `IUnitOfWork` implementation delegates `SaveChangesAsync` to it, and all repositories of one use case share it.
- Provider-fidelity target: SQL Server. EF Core InMemory or another provider is not this provider.
- Persistence area: `Infrastructure/Persistence/`; its internal layout is in the persistence workflow facet.

## EF Core boundary

- EF Core is an Infrastructure implementation detail. Inside Infrastructure, use EF Core fully and take advantage of its capabilities, without crippling repository implementations to preserve a generic abstraction, but do not leak EF Core concepts into Application.

## Development seeding

- Development seeding is an Infrastructure/bootstrap concern. It may use `AppDbContext` directly and does not need Application repositories or `IUnitOfWork`.
- Keep substantial seed construction in a dedicated internal `DbSeeder` (`Persistence/Seeding/DbSeeder.cs`) exposed through a narrow Infrastructure initialization extension, not in `Program.cs`, `AppDbContext`, entity configurations or migrations.
- The development seeder must not call `Database.Migrate()` or `EnsureCreated()` or otherwise create or upgrade the schema. Migrations are applied separately before seeding.

## Development database configuration

- Default: `appsettings.Development.json` provides a usable local Development connection string when it contains no secret credentials, for example LocalDB with `Trusted_Connection=True`. Credential-bearing local values come from user-secrets or another approved local secret mechanism.
