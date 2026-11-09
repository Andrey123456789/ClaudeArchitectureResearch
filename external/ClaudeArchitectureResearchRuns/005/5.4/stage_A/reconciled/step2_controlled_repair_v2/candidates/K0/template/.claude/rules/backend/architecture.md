---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
---

> Kind: STD | Scope: backend | Owner: Clean Architecture boundaries — layer dependencies, Domain, Application, API layer, repositories, Unit of Work, EF Core boundary, composition | Loading: path-scoped

# Backend Architecture Standard

Architecture: D-01. Not adopted: D-02. Persistence stack: D-04.

Enforced by: `.claude/scripts/check-dependencies.cjs` (project references).

## Dependency direction

- Dependencies must point inward: `Domain` references no other application project; `Application` references `Domain`; `Infrastructure` references `Application` and `Domain`; `Api` references `Application` and may reference `Infrastructure` only for application composition and dependency registration.
- Inner layers must never depend on outer layers, and Domain and Application must not reference Infrastructure-specific types. If a feature seems to need `Domain → Application`, `Domain → Infrastructure` or `Application → Infrastructure`, reconsider the abstraction boundary instead.

## Domain

- Domain must stay independent of EF Core, ASP.NET Core, HTTP, persistence and external-service implementation concerns, including mapping-library concerns.
- Default: simple domain entities; CRUD-oriented and straightforward workflow rules belong in Application Services. Validation rules, immutable fields, status transitions or allowed/forbidden edits do not by themselves justify a Rich Domain Model.
- Move behavior into Domain only when non-trivial domain invariants or behavior materially benefit from domain-level encapsulation independently of a particular use case. Otherwise a Rich Domain Model or DDD tactical pattern requires approval (Reserved, CLAUDE.md § Decisions) unless the approved specification already requires that design.
- Do not add factory methods, private setters, transition methods, Aggregate Roots, Domain Events, Specifications, Domain Services, systematic Value Objects or similar DDD constructs merely to make a simple model appear domain-driven.

## Application

- Default: Application Services orchestrate use cases; they coordinate Domain objects, repositories, external-service abstractions and the Unit of Work. A service growing too large is a signal to reconsider its responsibilities, not a reason to introduce another architectural pattern.
- Define persistence and external-service abstractions in Application when use cases require them, and keep infrastructure implementation details out of Application.
- Application must not use `DbContext`, `DbSet<T>`, EF Core APIs, provider-specific types or ASP.NET Core transport types.

## API layer

- Controllers (D-01) must stay thin: they bind and validate HTTP input, invoke Application services and translate application outcomes into HTTP responses.
- Controllers must not contain business logic, access `DbContext` or concrete repositories, or construct infrastructure services manually.
- Default: `Program.cs` is the composition root and may register Infrastructure implementations; Controllers still do not consume Infrastructure implementation types.
- Do not duplicate equivalent DTOs across API and Application merely to create layer-shaped types; introduce transport-specific request/response contracts when separation from Application models gives a concrete boundary benefit.

## Repositories

- Default: specific repository interfaces that represent actual, cohesive Application persistence needs rather than table-mirroring generic CRUD contracts. Define them in Application and implement them in Infrastructure; in an explicitly approved DDD design, Aggregate Roots are natural repository boundaries.
- Repository interfaces must not expose `IQueryable<T>`, `DbSet<T>`, `DbContext`, EF Core expressions or provider-specific types; LINQ-to-EF query construction stays in Infrastructure. Return materialized entities, collections, projections or explicit result models.
- Application must not depend on `IGenericRepository<T>` or another generic CRUD contract. A generic repository or `Repository<TEntity>` base class may exist only as an Infrastructure implementation detail that removes real duplication; it does not replace EF Core query capabilities, and use-case-specific queries stay in concrete repositories.

## Unit of Work

- Default: `IUnitOfWork` is the commit boundary of an Application use case — repositories stage changes and do not call `SaveChangesAsync` independently; Application Services decide when the operation commits. Infrastructure implements `IUnitOfWork` over the application's `DbContext`.
- Repositories participating in one use case must share the same scoped Unit of Work and `DbContext`. Inject repositories explicitly into their consumers; `IUnitOfWork` must not become a repository container or service locator exposing repositories as properties.
- Default: no explicit transaction APIs until a concrete use case needs control beyond a normal `SaveChangesAsync`.

## EF Core boundary

- EF Core is an Infrastructure implementation detail: use it fully inside Infrastructure, never leak its concepts into Application, and do not cripple repository implementations to preserve a generic abstraction.

## Composition and dependency injection

- Default: constructor injection for required dependencies; avoid service-locator and property-injection patterns.
- Service lifetimes must be valid: never capture a shorter-lived dependency inside a longer-lived service.
- Default: registration stays with the owning layer — Application registers Application services, Infrastructure registers persistence and adapters, `Api` remains the composition root.
