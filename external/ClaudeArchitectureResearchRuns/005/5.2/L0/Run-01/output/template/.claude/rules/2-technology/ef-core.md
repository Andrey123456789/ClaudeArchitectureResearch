---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
---

> Level: 2 Technology | Owns: EF Core placement and its bindings to the persistence boundary | Scope: backend | Loads: path | Depends on: 1-architecture/backend-layers.md, 1-architecture/persistence-boundary.md

# EF Core

- EF Core is an Infrastructure implementation detail. Use it normally inside
  Infrastructure — do not cripple repository implementations to preserve a
  generic abstraction — but do not leak EF Core concepts into Application.

## Bindings to Architecture Rules

- `DbContext`, `DbSet<T>`, EF Core APIs and LINQ-to-EF query expressions, and
  `Microsoft.EntityFrameworkCore.SqlServer` provider types are the
  persistence-framework and provider types that the Level 1 layer and
  repository rules keep out of Domain, Application, and repository contracts.
- The scoped `DbContext` is the persistence context shared by the repositories
  and the `IUnitOfWork` implementation of one use case; `SaveChangesAsync` is
  the normal commit.
- Each additional `DbContext` is an additional persistence boundary under the
  consequential architecture gate.

Technique (configuration, queries, migrations, transactions): → `ef-core` skill.
