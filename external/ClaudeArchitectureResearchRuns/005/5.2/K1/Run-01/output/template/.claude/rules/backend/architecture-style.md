---
paths:
  - "backend/**"
---
Kind: STD | Scope: backend | Capability: architecture/clean-architecture | Loading: path-scoped (backend/**)

# Architecture Style Standards: Clean Architecture

"Persistence-technology types" below means the types of whichever persistence technology the persistence slot selects: its persistence context and set types, query types and expressions, persistence APIs and provider-specific types. The selected persistence module lists them for its implementation. Placement procedures: the architecture workflow facet (decision register → Capability selection).

## Dependency direction

- Dependencies point inward. Domain depends on no other application project. Application depends on Domain. Infrastructure depends on Application and Domain. Api depends on Application and may reference Infrastructure only as required for composition and dependency registration. Inner layers never depend on outer layers, and Domain and Application never reference Infrastructure-specific types. When a feature seems to need an outward reference, reconsider the abstraction boundary instead of adding the reference.

## Domain

- Domain stays independent of the persistence technology, ASP.NET Core, HTTP, persistence and external-service implementation concerns.
- Default: simple domain entities. For CRUD-oriented applications and straightforward workflows, keep entities simple and enforce use-case and workflow rules in Application Services. Validation rules, immutable fields, status transitions or allowed and forbidden edits do not by themselves justify a Rich Domain Model.
- Move behavior into Domain only when non-trivial domain invariants or domain behavior materially benefit from domain-level encapsulation independently of one use case. Otherwise, a Rich Domain Model or DDD tactical patterns require approval, unless the approved specification already requires that design.
- Do not add factory methods, private setters, transition methods, Aggregate Roots, Domain Events, Specifications, Domain Services, systematic Value Objects or similar DDD constructs merely to make a simple model look domain-driven.

## Application

- Default: Application Services are the orchestration mechanism for use cases. They may coordinate Domain objects, repositories, external-service abstractions and the Unit of Work. A service growing too large is a signal to reconsider its responsibilities, not an automatic reason to introduce another pattern.
- Application defines the persistence and external-service abstractions that its use cases require, and keeps infrastructure implementation details out.
- Application must not depend on persistence-technology types (persistence context and set types, persistence APIs, provider-specific types) or on ASP.NET Core transport types.

## Api

- ASP.NET Core Controllers are the default HTTP entry point and stay thin: they bind and validate HTTP input, invoke Application services, and translate application outcomes into HTTP responses.
- Controllers must not contain business logic, access the persistence context or concrete repositories, or construct infrastructure services manually.

## Repositories

- Default: specific repository interfaces that represent cohesive Application use-case persistence needs, defined in Application and implemented in Infrastructure, rather than contracts that mirror every table with generic CRUD. Approved Aggregate Roots are natural repository boundaries. Repositories return materialized entities, collections, projections or explicit result models.
- Repository interfaces must not expose `IQueryable<T>`, persistence-technology types or query expressions, or provider-specific types. Query construction stays in Infrastructure.
- Application must not depend on `IGenericRepository<T>` or any other generic CRUD contract. A generic repository or base class may exist only as an Infrastructure implementation detail that removes genuine duplication, and it must not grow into a replacement for the persistence technology's query capabilities.

## Unit of Work

- Default: `IUnitOfWork` (`Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)`) is the commit boundary of an Application use case. Repositories stage changes and do not commit independently; Application Services decide when an operation is ready to commit.
- Repositories participating in one use case share the same scoped Unit of Work and persistence session. Repositories are injected explicitly into their consumers, and `IUnitOfWork` must not become a repository container or service locator.
- Default: do not introduce explicit transaction APIs until a concrete use case requires transaction control beyond a single `SaveChangesAsync` commit.

## Backend test projects

- Backend test projects must not get broader production-project references than their test scope requires, and they follow the same inward dependency discipline as production code.
