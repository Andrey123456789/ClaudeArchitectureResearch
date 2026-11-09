---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
---

> Path-scoped rule. Owns: backend dependency direction, layer responsibilities, Controller boundaries, transport-model boundaries, composition and configuration defaults · Scope: backend, backend-tests · Loads: when backend C# or project files are in context · Depends on: CLAUDE.md, docs/technology-stack.md · Enforced by: .claude/scripts/check-manifests.mjs (project references), .claude/scripts/check-architecture.mjs (source boundaries)

# Architecture Rules

Repositories, Unit of Work, the EF Core boundary, and seeding: `persistence.md`.
HTTP response semantics: `api.md`. Technique: `dependency-injection` and
`configuration` skills.

## Dependency Direction

Dependencies must point inward.

- `Domain` depends on no other application project.
- `Application` depends on `Domain`.
- `Infrastructure` depends on `Application` and `Domain`.
- `Api` depends on `Application` and may reference `Infrastructure` only as
  required for application composition and dependency registration.
- Inner layers must never depend on outer layers. Do not reference
  Infrastructure-specific types from Domain or Application.
- If a feature seems to require `Domain -> Application`,
  `Domain -> Infrastructure`, or `Application -> Infrastructure`, reconsider the
  abstraction boundary instead of adding the reference.
- Backend test projects must not reference more production projects than their
  test scope requires and follow the same inward discipline: for example
  `<Name>.Domain.Tests -> Domain`, `<Name>.Application.Tests -> Application`
  (and `Domain` as needed), `<Name>.IntegrationTests -> Api`.

## Domain

- Keep Domain free of EF Core, ASP.NET Core, HTTP, persistence, and
  external-service concerns.
- Default: simple domain entities. For CRUD-oriented applications and
  straightforward workflows, enforce use-case and workflow rules in Application
  Services. Validation rules, immutable fields, status transitions, or
  allowed/forbidden edits do not by themselves justify a Rich Domain Model.
- Move behavior into Domain entities only when non-trivial domain invariants or
  domain behavior materially benefit from domain-level encapsulation
  independently of a particular use case. Otherwise a Rich Domain Model or a
  DDD tactical pattern requires approval, unless the approved specification
  already requires that design.
- Do not add factory methods, private setters, transition methods, Aggregate
  Roots, Domain Events, Specifications, Domain Services, systematic Value
  Objects, or similar DDD constructs merely to make a simple model appear more
  domain-driven.

## Application

- Default: Application Services are the orchestration mechanism for use cases.
  They may coordinate Domain objects, repositories, external-service
  abstractions, and the Unit of Work. A service becoming too large is a signal
  to reconsider its responsibilities, not an automatic reason to introduce
  another architectural pattern.
- Define persistence and external-service abstractions in Application when use
  cases require them; keep infrastructure implementation details out of
  Application.
- Application must not depend on `DbContext`, `DbSet<T>`, EF Core APIs,
  provider-specific types, or ASP.NET Core transport types.
- Keep cache technology out of Domain, and do not leak infrastructure cache
  APIs (for example `HybridCache` or `IDistributedCache`) into Application
  without a deliberate boundary abstraction.
- Infrastructure translates remote HTTP responses into Application-facing
  abstractions; do not leak `HttpResponseMessage` or other remote-transport
  concerns into Application unless the Application explicitly models HTTP.

## API

- ASP.NET Core Controllers are the HTTP entry point and must stay thin: they
  bind and validate HTTP input, invoke Application services, and translate
  Application outcomes into HTTP responses.
- Controllers must not contain business logic, access `DbContext` or concrete
  repositories, or construct infrastructure services manually.
- Default: `Program.cs` is the application composition root and may register
  Infrastructure implementations; Controllers do not consume Infrastructure
  implementation types.
- Do not duplicate equivalent DTOs across Api and Application merely to create
  layer-shaped types; introduce transport-specific request/response contracts
  when separating them from Application models provides a concrete boundary
  benefit.
- Do not create separate Domain or persistence models merely because the
  external API has several versions; isolate version-specific transport
  contracts at the API boundary when practical.

## Composition and Configuration

- Default: constructor injection for required dependencies; avoid
  service-locator and property-injection patterns.
- Respect dependency lifetimes: never capture a shorter-lived dependency inside
  a longer-lived service.
- Default: keep registration close to the owning layer — Application registers
  Application services, Infrastructure registers persistence and adapters, and
  Api remains the composition root.
- Default: strongly typed options for structured service configuration,
  validated at startup when missing or invalid values prevent correct or secure
  operation. Avoid scattering string-based `IConfiguration` lookups through
  services; direct `IConfiguration` access belongs to the composition root,
  configuration-provider setup, and infrastructure registration.
