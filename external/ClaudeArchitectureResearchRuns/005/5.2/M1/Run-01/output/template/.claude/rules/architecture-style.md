---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
---

> **Policy rule** · Capability: architecture/clean-architecture · Owns: dependency direction, layer responsibilities, repositories and Unit of Work, registration placement, transport-contract placement, test-project references · Scope: backend, backend-tests · Loading: path (backend code and project files)

# Architecture Style Rules

Adopted architecture, stable-role mapping, and patterns not adopted:
`docs/architecture.md`. Reserved architecture changes: `CLAUDE.md` → Decision
Control.

## Dependency Direction

Dependencies must point inward.

- `Domain` depends on no other application project.
- `Application` depends on `Domain`.
- `Infrastructure` depends on `Application` and `Domain`.
- `Api` depends on `Application` and may reference `Infrastructure` only as required for application composition and dependency registration.
- Inner layers must never depend on outer layers.

Do not reference Infrastructure-specific types from Domain or Application. If a
feature seems to require an outward reference, reconsider the abstraction boundary
instead of adding the reference.

## Domain

The Domain layer contains business concepts that are independent of
infrastructure and transport concerns.

Simple domain entities are the default.

- Keep Domain free of persistence technology, ASP.NET Core, HTTP, persistence,
  and external-service implementation concerns.
- For CRUD-oriented applications and straightforward workflows, keep entities
  simple and enforce use-case/workflow rules in Application Services.
- Validation rules, immutable fields, status transitions, or allowed/forbidden
  edits do not by themselves justify a Rich Domain Model.
- Move behavior into Domain entities only when non-trivial domain invariants or
  domain behavior materially benefit from domain-level encapsulation
  independently of a particular application use case.
- Do not add factory methods, private setters, transition methods, Aggregate
  Roots, Domain Events, Specifications, Domain Services, systematic Value
  Objects, or similar DDD constructs merely to make a simple model appear more
  domain-driven.
- Otherwise a Rich Domain Model or DDD tactical pattern is a Reserved decision
  (`CLAUDE.md` → Decision Control) unless the approved project specification
  already requires that design.

## Application

The Application layer coordinates application use cases.

- Use Application Services as the default orchestration mechanism.
- Application Services may coordinate Domain objects, repositories, external-service abstractions, and the Unit of Work.
- Define persistence and external-service abstractions in Application when they are required by application use cases.
- Keep infrastructure implementation details out of Application.
- Do not use persistence-technology types or APIs (the persistence context and
  its entity sets, technology query APIs and expressions, technology-backed
  `IQueryable<T>`, provider-specific types) or ASP.NET Core transport types in
  Application.

## API

ASP.NET Core Controllers are the default HTTP entry point.

Controllers must remain thin:

- bind and validate HTTP input;
- invoke Application services;
- translate application outcomes into HTTP responses.

Controllers must not:

- contain business logic;
- access the persistence context;
- access concrete repositories;
- construct infrastructure services manually.

`Program.cs` is the application composition root and may register Infrastructure implementations.

## Repositories

Repository interfaces are inward-facing persistence contracts.

- Default: use specific repository interfaces that represent actual Application
  use-case persistence needs and cohesive persistence boundaries, rather than
  generic CRUD contracts that blindly mirror every database table.
- When an explicitly approved DDD design contains Aggregate Roots, those
  Aggregate Roots are natural repository-boundary candidates.
- Define repository interfaces in Application.
- Implement repositories in Infrastructure.
- Keep persistence query construction inside Infrastructure.
- Do not expose `IQueryable<T>`, persistence-technology types (the persistence
  context, its entity sets, query expressions), or provider-specific types from
  repository interfaces.
- Return materialized entities, collections, projections, or explicit result models as appropriate.

Example:

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

A generic repository may be used only as an Infrastructure implementation detail when it removes genuine duplication.

- Application code must not depend on `IGenericRepository<T>` or another generic CRUD contract.
- Concrete repositories may reuse an Infrastructure-only `Repository<TEntity>` base class.
- That base class may expose useful protected persistence helpers to concrete
  repositories.
- Do not expand the generic repository into a replacement for the persistence
  technology's query capabilities.
- Use-case-specific queries belong in concrete repository implementations.

## Unit of Work

Default: use `IUnitOfWork` as the commit boundary for an Application use case.

```csharp
public interface IUnitOfWork
{
    Task<int> SaveChangesAsync(
        CancellationToken cancellationToken = default);
}
```

- Infrastructure implements `IUnitOfWork` over the application's scoped
  persistence context.
- Default: repositories stage changes and do not independently call `SaveChangesAsync`.
- Application Services decide when an application operation is ready to commit.
- Repositories participating in the same use case must share the same Unit of Work.
- Repositories are injected explicitly into their consumers.
- `IUnitOfWork` must not act as a repository container or service locator that
  exposes all repositories as properties.
- Repositories participating in the same Unit of Work share the same scoped
  persistence context.
- Do not introduce explicit transaction APIs until a real use case requires transaction control beyond normal `SaveChangesAsync`.

## Persistence Technology

The persistence technology is an Infrastructure implementation detail. How it is
used inside Infrastructure, together with development seeding and its provider
configuration, is owned by the persistence capability's rule facet
(`persistence-technology.md`).

## Registration

Default: keep dependency registration close to the owning layer.

- Application registers Application services and Application-level validation
  (for example `AddApplication()` in `DependencyInjection.cs`); it does not
  register concrete Infrastructure implementations.
- Infrastructure registers persistence, repository, Unit of Work, and external
  adapter implementations (for example `AddInfrastructure(configuration)`).
- Api remains the composition root that composes both.

## Transport Contracts

Do not duplicate equivalent DTOs across Api and Application merely to create
layer-shaped types. Introduce transport-specific request/response contracts in Api
only when separation from Application models provides a concrete boundary benefit.

## Test Projects

Backend test projects must not receive broader production-project references than
their test scope requires; they follow the same inward dependency discipline as the
production architecture. Typical references:

```text
<Name>.Domain.Tests            -> <Name>.Domain                     (optional project)
<Name>.Application.Tests       -> <Name>.Application, <Name>.Domain as needed
<Name>.IntegrationTests        -> <Name>.Api
<Name>.Infrastructure.Tests    -> <Name>.Infrastructure, narrower as required (optional project)
```

Integration tests may exercise Application, Infrastructure, persistence, routing,
DI, and serialization transitively through the API host.
