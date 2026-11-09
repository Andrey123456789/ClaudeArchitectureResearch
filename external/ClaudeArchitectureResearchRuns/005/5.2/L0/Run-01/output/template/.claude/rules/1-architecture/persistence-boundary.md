---
paths:
  - "backend/**/*.cs"
---

> Level: 1 Architecture | Owns: repository contracts, generic-repository placement, Unit of Work, transaction boundary | Scope: backend | Loads: path | Depends on: 1-architecture/backend-layers.md

# Persistence Boundary

## Repositories

- Default: prefer specific repository interfaces that represent actual,
  cohesive Application persistence needs rather than table-mirroring generic
  CRUD contracts. Define them in Application and implement them in
  Infrastructure.
- Repository interfaces must not expose `IQueryable<T>`, persistence-framework
  context or set types, persistence-framework query expressions, or
  provider-specific types; query construction stays in Infrastructure.
  Return materialized entities, collections, projections, or explicit result
  models.
- Application must not depend on `IGenericRepository<T>` or another generic
  CRUD contract. A generic repository or base class may exist only as an
  Infrastructure implementation detail that removes real duplication; it is not
  a replacement for the persistence framework's query capabilities.

## Unit of Work

- Default: `IUnitOfWork` is the commit boundary of an Application use case.
  Repositories stage changes and do not independently commit; Application
  Services decide when the operation commits.
- Repositories participating in one use case share the same scoped Unit of Work
  and persistence context. `IUnitOfWork` must not become a repository container
  or service locator; repositories are injected explicitly into their consumers.
- Default: do not introduce explicit transaction APIs until a concrete use case
  requires control beyond the normal single `SaveChangesAsync` commit.

Persistence-framework binding: → `2-technology/ef-core.md`. Development data lifecycle: → `3-project/data-lifecycle.md`.
