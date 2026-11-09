---
paths:
  - "backend/**"
---

> Level: 1 Architecture · Owns: repository contracts, unit of work, persistence-framework boundary · Scope: backend · Loads: path; read explicitly by `project-structure`

# Persistence Boundary

## Repositories

- **Default:** define specific repository interfaces in Application that represent cohesive use-case persistence needs, not table-mirroring generic CRUD contracts; implement them in Infrastructure. When an explicitly approved DDD design has aggregate roots, those are natural repository boundaries.
- **Must not** expose `IQueryable<T>`, persistence-framework sets or contexts, framework query expressions or provider-specific types from repository interfaces. Query construction stays in Infrastructure; return materialized entities, collections, projections or explicit result models.
- **Must not** let Application depend on `IGenericRepository<T>` or any other generic CRUD contract. A generic repository base class may exist only as an Infrastructure implementation detail that removes real duplication; use-case-specific queries live in concrete repositories.

```csharp
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken);

    Task AddAsync(Order order, CancellationToken cancellationToken);
}
```

## Unit of Work

- **Default:** `IUnitOfWork` is the commit boundary of an Application use case. Repositories stage changes and do not commit independently; Application Services decide when the operation is ready to commit.
- **Must** let the repositories of one use case share the same scoped unit of work and persistence context; repositories are injected explicitly into their consumers. `IUnitOfWork` **must not** become a repository container or service locator that exposes repositories as properties.
- **Default:** do not introduce explicit transaction APIs until a concrete use case needs control beyond the normal single commit.

```csharp
public interface IUnitOfWork
{
    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
}
```

## Persistence framework

- **Must** treat the persistence framework as an Infrastructure implementation detail: use its capabilities fully inside Infrastructure — do not cripple repository implementations to preserve a generic abstraction — and never leak its concepts into Application.
