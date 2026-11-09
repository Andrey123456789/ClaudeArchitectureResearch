---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
---

> Level: 1 Architecture · Owns: repository contracts, Unit of Work commit boundary, persistence-framework boundary · Scope: backend · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/1-architecture/backend-layers.md

# Persistence Boundary

Which concrete types count as persistence-framework types is defined in `.claude/rules/2-technology/`.

## Persistence framework

- The persistence framework is an Infrastructure implementation detail. Use it normally inside Infrastructure and take advantage of its capabilities, but do not leak its concepts into Application.
- Do not cripple repository implementations merely to preserve a generic abstraction; the repository boundary keeps persistence concerns out of Application, it does not hide the framework from Infrastructure.

## Repositories

- Repository interfaces are inward-facing contracts defined in Application and implemented in Infrastructure.
- Prefer specific repository interfaces that represent actual cohesive Application persistence needs rather than table-mirroring generic CRUD contracts (default). When an explicitly approved DDD design has Aggregate Roots, they are natural repository-boundary candidates.
- Repository interfaces must not expose `IQueryable<T>`, persistence-framework context, set, or query-expression types, or provider-specific types; query construction stays in Infrastructure. Return materialized entities, collections, projections, or explicit result models.
- Application must not depend on `IGenericRepository<T>` or any other generic CRUD contract. A generic repository or base class may exist only as an Infrastructure implementation detail that removes real duplication; use-case-specific queries belong in concrete repositories.

## Unit of Work

- `IUnitOfWork` is the normal commit boundary of an Application use case: repositories stage changes, and Application Services decide when to commit (default).
- Repositories participating in one use case must share the same scoped Unit of Work and persistence context. Repositories are injected explicitly into their consumers; `IUnitOfWork` must not become a repository container or service locator.
- Do not introduce explicit transaction APIs until a concrete use case requires control beyond the normal single save/commit (default).
