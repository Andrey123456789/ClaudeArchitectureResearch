---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
---

> Capability: architecture/clean-architecture · Path rule · Scope: backend · Owns layer dependencies, use-case orchestration, entry points, repositories, the commit boundary, layer placement, and test-project references

# Architecture Rules

The role names used by other instructions map to these layers in
`docs/capabilities/architecture.md`. Persistence-technology specifics are in
`.claude/rules/persistence-technology.md`.

## Dependency Direction

Dependencies must point inward.

- `Domain` depends on no other application project.
- `Application` depends on `Domain`.
- `Infrastructure` depends on `Application` and `Domain`.
- `Api` depends on `Application` and may reference `Infrastructure` only as
  required for application composition and dependency registration.
- Inner layers must never depend on outer layers. Do not reference
  Infrastructure-specific types from Domain or Application.

## Domain

The Domain layer contains business concepts independent of infrastructure and
transport concerns. Simple domain entities are the default.

- Keep Domain independent of the persistence technology, ASP.NET Core, HTTP,
  persistence, and external-service implementation concerns.
- For CRUD-oriented applications and straightforward workflows, keep entities
  simple and enforce use-case and workflow rules in Application Services.
  Validation rules, immutable fields, status transitions, or allowed/forbidden
  edits do not by themselves justify a Rich Domain Model.
- Move behavior into Domain entities only when non-trivial domain invariants or
  behavior materially benefit from domain-level encapsulation independently of
  a particular use case. Otherwise a Rich Domain Model or DDD tactical pattern
  requires explicit approval, unless the approved specification already
  requires that design.
- Do not add factory methods, private setters, transition methods, Aggregate
  Roots, Domain Events, Specifications, Domain Services, systematic Value
  Objects, or similar DDD constructs merely to make a simple model appear more
  domain-driven.

## Application

- Application Services are the default orchestration mechanism for use cases.
  They may coordinate Domain objects, repositories, external-service
  abstractions, and the Unit of Work.
- Define persistence and external-service abstractions in Application when use
  cases require them; keep infrastructure implementation details out of
  Application.
- Application must not depend on persistence-technology types or on ASP.NET
  Core transport types.
- A service becoming too large is a signal to reconsider its responsibilities,
  not an automatic reason to introduce another architectural pattern.

## API

ASP.NET Core Controllers are the default HTTP entry point. Controllers must
remain thin: they bind and validate HTTP input, invoke Application services,
and translate application outcomes into HTTP responses.

Controllers must not contain business logic, access the persistence session or
concrete repositories, or construct infrastructure services manually.

By default `Program.cs` is the application composition root and may register
Infrastructure implementations; Controllers do not consume Infrastructure
implementation types directly.

## Repositories

Repository interfaces are inward-facing persistence contracts.

- Prefer specific repository interfaces that represent actual, cohesive
  Application use-case persistence needs rather than table-mirroring generic
  CRUD contracts. When an explicitly approved DDD design contains Aggregate
  Roots, they are natural repository-boundary candidates.
- Define repository interfaces in Application and implement them in
  Infrastructure; query construction stays inside Infrastructure.
- Repository interfaces must not expose `IQueryable<T>`, persistence-technology
  types or query expressions, or provider-specific types. Return materialized
  entities, collections, projections, or explicit result models as appropriate.

```csharp
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(
        Guid id,
        CancellationToken cancellationToken);

    Task AddAsync(
        Order order,
        CancellationToken cancellationToken);
}
```

## Generic Repository

Application must not depend on `IGenericRepository<T>` or another generic CRUD
contract. A generic repository or `Repository<TEntity>` base class may exist
only as an Infrastructure implementation detail that removes genuine
duplication; it may expose protected helpers to concrete repositories, but it
must not become a replacement for the persistence technology's query
capabilities. Use-case-specific queries belong in concrete repositories.

## Unit of Work

`IUnitOfWork` is the default commit boundary for an Application use case.

```csharp
public interface IUnitOfWork
{
    Task<int> SaveChangesAsync(
        CancellationToken cancellationToken = default);
}
```

- Infrastructure implements `IUnitOfWork` over the scoped persistence session.
- Repositories stage changes and do not independently commit; Application
  Services decide when an application operation is ready to commit.
- Repositories participating in one use case must share the same scoped Unit of
  Work and persistence session. Inject repositories explicitly into their
  consumers.
- `IUnitOfWork` must not act as a repository container or service locator that
  exposes repositories as properties.

## Layer Placement

- Keep cache technology out of Domain, and do not leak infrastructure cache APIs
  into Application without a deliberate boundary abstraction.
- Infrastructure translates remote HTTP responses into Application-facing
  abstractions; do not leak `HttpResponseMessage` or remote transport concerns
  into Application contracts unless the Application explicitly models HTTP.
- By default keep dependency registration close to the owning layer:
  Application registers Application services, Infrastructure registers
  persistence and adapters, and Api remains the composition root.
- Do not create separate Domain or persistence models merely because the
  external API has multiple versions; isolate version-specific transport
  contracts at the API boundary when practical.
- Do not duplicate equivalent DTOs across Api and Application merely to create
  layer-shaped types; introduce transport-specific request/response contracts
  when separation from Application models provides a concrete boundary benefit.

## Test Project References

Do not give backend test projects broader production-project references than
their test scope requires; apply the same inward dependency discipline as the
production architecture.
