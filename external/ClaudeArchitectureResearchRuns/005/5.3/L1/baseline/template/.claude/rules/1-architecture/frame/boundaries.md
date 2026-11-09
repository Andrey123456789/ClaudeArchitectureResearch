---
paths:
  - "backend/**/*"
---

> Level: 1-architecture · Capability: architecture/clean-architecture · Facet: architecture.boundaries · Owns: layer dependency direction and responsibilities, repository and Unit of Work placement, composition, test-project references · Scope: backend (including backend tests) · Loading: path

# Clean Architecture Boundaries

## Dependency direction

Dependencies must point inward: `Domain` references no other application project; `Application` references `Domain`; `Infrastructure` references `Application` and `Domain`; `Api` references `Application` and references `Infrastructure` only for composition and dependency registration. Inner layers never depend on outer layers. If a feature seems to need an outward reference, reconsider the abstraction boundary instead. Mechanical check: `architecture.check`.

## Domain

- Keep Domain free of persistence-implementation, ASP.NET Core, HTTP, and external-service implementation concerns.
- Default: simple domain entities. Straightforward CRUD and workflow rules — validation, immutable fields, status transitions, allowed or forbidden edits — belong in Application Services and do not by themselves justify a Rich Domain Model.
- Move behavior into Domain only when non-trivial domain invariants or behavior materially benefit from domain-level encapsulation independently of one use case; otherwise a Rich Domain Model or DDD tactical pattern requires approval unless the approved specification already requires it.
- Do not add factory methods, private setters, transition methods, Aggregate Roots, Domain Events, Specifications, Domain Services, systematic Value Objects, or similar constructs merely to make a simple model look domain-driven.

## Application

- Default: Application Services orchestrate use cases; they may coordinate Domain objects, repositories, external-service abstractions, and the Unit of Work.
- Define persistence and external-service abstractions in Application when use cases need them; keep implementation details out of Application.
- Application must not use persistence-implementation types or APIs (persistence context and entity-set types, ORM APIs, database-provider types) or ASP.NET Core transport types.
- Do not duplicate equivalent DTOs across Api and Application merely to create layer-shaped types; add transport-specific request/response contracts in Api when separation from Application models gives a concrete boundary benefit.

## Api

- ASP.NET Core Controllers are the default HTTP entry point and stay thin: they bind and validate HTTP input, invoke Application services, and translate outcomes into HTTP responses.
- Controllers must not contain business logic, access the persistence context or concrete repositories, or construct infrastructure services manually.
- Default: `Program.cs` is the composition root and may register Infrastructure implementations.
- Default: keep registration near the owning layer — Application registers Application services, Infrastructure registers persistence and adapters, Api composes them.

## Repositories and Unit of Work

- Default: prefer specific repository interfaces that represent cohesive Application persistence needs rather than generic CRUD contracts mirroring tables. Interfaces live in Application, implementations in Infrastructure.
- Application must not depend on `IGenericRepository<T>` or another generic CRUD contract; a generic repository base class may exist only inside Infrastructure, only to remove real duplication, and never as a replacement for the ORM's query capabilities.
- Default: `IUnitOfWork` (defined in Application) is the normal commit boundary of a use case; repositories stage changes and Application Services decide when to commit.
- Repositories taking part in one use case share the same scoped Unit of Work and persistence context; inject repositories explicitly — `IUnitOfWork` must not become a repository container or service locator.
- Default: do not introduce explicit transaction APIs until a concrete use case needs control beyond a single `IUnitOfWork.SaveChangesAsync` commit.

## Test projects

Do not give a backend test project broader production references than its test scope needs; keep the inward discipline of production projects (typical: `.Application.Tests` → Application and Domain as needed; `.IntegrationTests` → Api; optional `.Domain.Tests` → Domain; optional `.Infrastructure.Tests` → Infrastructure).
