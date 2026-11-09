---
paths:
  - "backend/**/*"
---

> Level: 2-technology · Capability: persistence/ef-core · Facet: persistence.access · Owns: EF Core confinement, repository-contract leak rule, commit-boundary and relational-fidelity bindings · Scope: backend · Loading: path

# EF Core Persistence Access

- EF Core is an implementation-layer detail: use its full capabilities inside the persistence implementation, but never leak EF Core concepts into the use-case layer. Do not cripple repository implementations to preserve a generic abstraction.
- Persistence-access contracts must not expose `IQueryable<T>`, `DbSet<T>`, `DbContext`, EF Core expressions, or provider-specific types; LINQ-to-EF query construction stays in the persistence implementation, and contracts return materialized entities, collections, projections, or explicit result models.

## Bindings

These bind role-level rules to this module; they add no separate policy.

- Persistence context: the scoped `AppDbContext`, shared by every repository taking part in one use case. Persistence-implementation types: `DbContext`, `DbSet<T>`, EF Core APIs, EF-backed `IQueryable<T>`, SQL Server provider types.
- Commit boundary: the commit-boundary implementation delegates to `AppDbContext.SaveChangesAsync`; staged changes are the tracked changes of the shared context.
- Relational fidelity: the actual provider is SQL Server. EF Core InMemory, SQLite, or another provider does not establish SQL Server behavior.

Technique: `ef-core`. Procedures: `persistence.workflow`.
