---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
  - "*.slnx"
---

> Owner: backend Clean Architecture boundaries, layer responsibilities, repository contracts, dependency injection | Scope: backend | Loads: path (backend C# and project files); read explicitly by `project-structure`, `code-review`, `verify`, `build-fix` | Enforced: `.claude/scripts/check-architecture.mjs` (PostToolUse hook and `verify`)

# Architecture Rules

## Dependency Direction

Dependencies must point inward:

- `Domain` references no other application project.
- `Application` references `Domain`.
- `Infrastructure` references `Application` and `Domain`.
- `Api` references `Application` and may reference `Infrastructure` only as
  required for application composition and dependency registration.

Inner layers must never depend on outer layers, and Domain and Application must
not reference Infrastructure-specific types. If a feature seems to need such a
reference, reconsider the abstraction boundary instead of adding it.

## Domain

- Keep Domain free of EF Core, ASP.NET Core, HTTP, persistence, and
  external-service implementation concerns.
- Default: simple domain entities. For CRUD-oriented applications and
  straightforward workflows, keep entities simple and enforce use-case and
  workflow rules in Application Services. Validation rules, immutable fields,
  status transitions, or allowed/forbidden edits do not by themselves justify a
  Rich Domain Model.
- Move behavior into Domain entities only when non-trivial domain invariants or
  behavior materially benefit from domain-level encapsulation independently of a
  particular use case. Otherwise a Rich Domain Model or DDD tactical pattern
  requires approval, unless the approved specification already requires it.
- Do not add factory methods, private setters, transition methods, Aggregate
  Roots, Domain Events, Specifications, Domain Services, systematic Value
  Objects, or similar DDD constructs merely to make a simple model appear more
  domain-driven.

## Application

- Default: Application Services are the orchestration mechanism for use cases;
  they may coordinate Domain objects, repositories, external-service
  abstractions, and the Unit of Work.
- Define persistence and external-service abstractions in Application when use
  cases require them, and keep infrastructure implementation details out of
  Application.
- Application must not use `DbContext`, `DbSet<T>`, EF Core APIs,
  provider-specific types, or ASP.NET Core transport types.
- Keep cache technology out of Domain, and do not leak infrastructure cache APIs
  (for example `HybridCache`) into Application without a deliberate boundary
  abstraction.
- Infrastructure translates remote HTTP responses into Application-facing
  abstractions; do not leak `HttpResponseMessage` or other remote transport
  concerns into Application.
- A service becoming too large is a signal to reconsider its responsibilities,
  not an automatic reason to introduce another architectural pattern.

## API

- ASP.NET Core Controllers are the default HTTP entry point. Controllers bind and
  validate HTTP input, invoke Application services, and translate application
  outcomes into HTTP responses.
- Controllers must not contain business logic, access `DbContext` or concrete
  repositories, or construct infrastructure services manually.
- Default: `Program.cs` is the application composition root and may register
  Infrastructure implementations.
- Do not duplicate equivalent DTOs across API and Application merely to create
  layer-shaped types; introduce transport-specific request/response contracts
  when separation from Application models gives a concrete boundary benefit.

## Repositories

- Default: specific repository interfaces that represent cohesive Application
  persistence needs rather than table-mirroring generic CRUD contracts. When an
  explicitly approved DDD design contains Aggregate Roots, they are natural
  repository boundaries.
- Define repository interfaces in Application and implement them in
  Infrastructure.
- Repository interfaces must not expose `IQueryable<T>`, `DbSet<T>`,
  `DbContext`, EF Core expressions, or provider-specific types; LINQ-to-EF query
  construction stays in Infrastructure. Return materialized entities,
  collections, projections, or explicit result models.
- Application must not depend on `IGenericRepository<T>` or another generic CRUD
  contract. A generic repository base may exist only as an Infrastructure
  implementation detail that removes real duplication; use-case-specific queries
  belong in concrete repositories.

## Dependency Injection

- Default: constructor injection for required dependencies; avoid service-locator
  and property-injection patterns.
- Respect service lifetimes: never capture a shorter-lived dependency inside a
  longer-lived service.
- Default: keep registration close to the owning layer — Application registers
  Application services, Infrastructure registers persistence and adapters, and
  `Api` remains the composition root.
