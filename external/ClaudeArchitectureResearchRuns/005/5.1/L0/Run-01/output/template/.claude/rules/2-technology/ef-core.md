---
paths:
  - "backend/**"
---

> Level: 2 Technology · Owns: EF Core bindings and migration review · Scope: backend · Loads: path

# EF Core

## Bindings for the Level 1 persistence boundary

- Persistence-framework types are `DbContext` (the application's `AppDbContext`), `DbSet<T>`, EF Core attributes and APIs (`Microsoft.EntityFrameworkCore.*`), `IQueryable<T>` produced by EF Core, EF query expressions, and provider types such as those of `Microsoft.EntityFrameworkCore.SqlServer`. The Level 1 rules keep them inside Infrastructure.
- The shared scoped persistence context of a use case is the scoped `AppDbContext` registered by `AddDbContext`; `IUnitOfWork.SaveChangesAsync` delegates to that same context, so one `SaveChangesAsync` is the normal commit.
- EF Core InMemory is not a relational provider; it never demonstrates relational or SQL Server behavior.

## Migrations

- **Must** treat EF Core migrations as source code: review every generated migration before it is committed, paying particular attention to destructive schema changes, unexpected column recreation, data migrations, indexes, foreign keys and delete behavior.

Technique (configurations, repositories, queries, tracking, migrations commands): `ef-core` skill.
