---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
---

> Level: 2 Technology · Owns: EF Core bindings of the persistence boundary · Scope: backend · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/1-architecture/backend-layers.md, .claude/rules/1-architecture/persistence-boundary.md

# EF Core Bindings

EF Core is the persistence framework of the approved stack (`3-project/decisions.md`). The boundary itself is owned by `1-architecture/persistence-boundary.md`; technique is in the `ef-core` skill.

- `DbContext`, `DbSet<T>`, EF Core APIs and LINQ-to-EF expressions, EF attributes and mapping types, and SQL Server provider types are persistence-framework types for the purposes of the Level 1 boundary rules.
- Entity mappings live in Infrastructure as `IEntityTypeConfiguration<T>` classes, keeping persistence configuration out of Domain entities where practical (prefer).
- The Infrastructure implementation of `IUnitOfWork` delegates to the same scoped `DbContext` that the use case's repositories share.
- An Infrastructure-only `Repository<TEntity>` base class may expose protected helpers to concrete repositories; concrete repositories may use the full EF Core API internally.
