---
paths:
  - "backend/**"
---
<!-- Kind: STD | Scope: backend | Owns: layer dependencies, layer responsibilities, composition and DI, boundary leaks | Loads: path-scoped (backend/**) -->
# Backend Architecture Standards

Architecture style: DEC-ARCH-01. Patterns not adopted: DEC-ARCH-02. Approval for consequential changes: CLAUDE.md § Decisions.

## Dependency Direction

Dependencies **must** point inward:

- `Domain` depends on no other application project.
- `Application` depends on `Domain`.
- `Infrastructure` depends on `Application` and `Domain`.
- `Api` depends on `Application` and may reference `Infrastructure` only as required for application composition and dependency registration.
- Inner layers **must never** depend on outer layers; Domain and Application **must not** reference Infrastructure-specific types.

When a feature seems to need an outward reference, reconsider the abstraction boundary instead of adding the reference.

## Domain

- Domain **must** stay independent of EF Core, ASP.NET Core, HTTP, persistence and external-service implementation concerns.
- **Default:** simple domain entities; straightforward CRUD and workflow rules belong in Application Services. Validation rules, immutable fields, status transitions or allowed/forbidden edits do not by themselves justify a Rich Domain Model.
- Move behavior into Domain only when non-trivial domain invariants or behavior materially benefit from domain-level encapsulation independently of a particular use case. Otherwise a Rich Domain Model or DDD tactical pattern **requires approval**, unless the approved specification already requires that design.
- **Must not** add factory methods, private setters, transition methods, Aggregate Roots, Domain Events, Specifications, Domain Services, systematic Value Objects or similar DDD constructs merely to make a simple model appear domain-driven.

## Application

- **Default:** Application Services orchestrate use cases; they may coordinate Domain objects, repositories, external-service abstractions and the Unit of Work. A service growing too large is a signal to reconsider its responsibilities, not an automatic reason to adopt another pattern (DEC-ARCH-02).
- Application **must** define the persistence and external-service abstractions its use cases require, and keep infrastructure implementation details out.
- Application **must not** depend on `DbContext`, `DbSet<T>`, EF Core APIs, provider-specific types or ASP.NET Core transport types.

## API

- Controllers (DEC-PLAT-01) **must** stay thin: bind and validate HTTP input, invoke Application services, translate application outcomes into HTTP responses.
- Controllers **must not** contain business logic, access `DbContext` or concrete repositories, construct infrastructure services manually, or consume Infrastructure implementation types.
- **Default:** `Program.cs` is the application composition root and may register Infrastructure implementations.

## Composition and Dependency Injection

- **Default:** constructor injection for required dependencies; avoid service-locator and property-injection patterns.
- Dependency lifetimes **must** be respected: **never** capture a shorter-lived dependency inside a longer-lived service.
- **Default:** registration stays close to the owning layer — Application registers Application services, Infrastructure registers persistence and infrastructure adapters, and Api remains the composition root.

## Boundary Leaks

- Cache technology **must** stay out of Domain, and infrastructure cache APIs **must not** leak into Application without a deliberate boundary abstraction.
- Infrastructure **must** translate remote HTTP responses into Application-facing abstractions; `HttpResponseMessage` and other remote transport concerns **must not** leak into Application.
- **Must not** create separate Domain or persistence models merely because the external API has several versions; isolate version-specific transport contracts at the API boundary when practical.
- **Must not** duplicate equivalent DTOs across Api and Application merely to create layer-shaped types; introduce transport-specific request/response contracts when separation from Application models gives a concrete boundary benefit.

Technique: `dependency-injection`, `caching`, `httpclient-factory`, `api-versioning` knowledge skills.
