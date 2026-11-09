---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
---

> Owns: backend layer boundaries, project references, repositories and Unit of Work, EF Core boundary, composition and dependency injection | Scope: backend, backend-tests | Loads: path-scoped (backend C# and project files)

# Architecture Rules

Adopted architecture and Reserved decisions: CLAUDE.md § Architecture Defaults
and § Decision Control. Persistence seeding: `persistence.md`. HTTP semantics:
`api.md`.

## Dependency Direction

Dependencies must point inward:

- `Domain` depends on no other application project.
- `Application` depends on `Domain`.
- `Infrastructure` depends on `Application` and `Domain`.
- `Api` depends on `Application` and may reference `Infrastructure` only as
  required for application composition and dependency registration.
- Inner layers never depend on outer layers; Domain and Application never
  reference Infrastructure-specific types.

If a feature seems to require an outward reference, reconsider the abstraction
boundary instead of adding the reference.

## Project References

Production graph: `Domain` → none; `Application` → `Domain`;
`Infrastructure` → `Application`, `Domain`; `Api` → `Application`,
`Infrastructure`. Never add `Domain` → `Application`/`Infrastructure` or
`Application` → `Infrastructure`.

Do not give backend test projects broader production-project references than
their test scope requires; they keep the same inward discipline:

- `<Name>.Domain.Tests` (optional) → `Domain`;
- `<Name>.Application.Tests` → `Application`, and `Domain` as needed;
- `<Name>.IntegrationTests` → `Api` (for `WebApplicationFactory<Program>`);
- `<Name>.Infrastructure.Tests` (optional) → `Infrastructure`, narrower
  references as required.

Project references are checked by `.claude/scripts/check-manifests.mjs`, which
the manifest hook runs automatically.

## Domain

- Keep Domain free of EF Core, ASP.NET Core, HTTP, persistence, and
  external-service implementation concerns.
- Simple domain entities are the default. For CRUD-oriented applications and
  straightforward workflows, enforce use-case and workflow rules in Application
  Services. Validation rules, immutable fields, status transitions, or
  allowed/forbidden edits do not by themselves justify a Rich Domain Model.
- Move behavior into Domain entities only when non-trivial domain invariants or
  domain behavior materially benefit from domain-level encapsulation
  independently of a particular use case. Otherwise a Rich Domain Model or DDD
  tactical pattern requires explicit approval, unless the approved
  specification already requires that design.
- Do not add factory methods, private setters, transition methods, Aggregate
  Roots, Domain Events, Specifications, Domain Services, systematic Value
  Objects, or similar DDD constructs merely to make a simple model appear more
  domain-driven.

## Application

- Application Services are the default orchestration mechanism for use cases.
  They may coordinate Domain objects, repositories, external-service
  abstractions, and the Unit of Work. A service becoming too large is a signal
  to reconsider its responsibilities, not a reason to introduce another
  architectural pattern.
- Define persistence and external-service abstractions in Application when
  application use cases require them; keep infrastructure implementation
  details out of Application.
- Application must not use `DbContext`, `DbSet<T>`, EF Core APIs,
  provider-specific types, or ASP.NET Core transport types.

## API

- ASP.NET Core Controllers are the default HTTP entry point and stay thin: they
  bind and validate HTTP input, invoke Application services, and translate
  application outcomes into HTTP responses. Do not create Minimal API endpoint
  groups unless explicitly requested.
- Controllers must not contain business logic, access `DbContext` or concrete
  repositories, or construct infrastructure services manually.
- `Program.cs` is the application composition root and may register
  Infrastructure implementations; Controllers do not consume Infrastructure
  implementation types directly.

## Repositories

- Prefer specific repository interfaces that represent actual, cohesive
  Application persistence needs over generic CRUD contracts that mirror every
  table. When an approved DDD design contains Aggregate Roots, they are natural
  repository-boundary candidates. Define repository interfaces in Application
  and implement them in Infrastructure.
- Repository interfaces must not expose `IQueryable<T>`, `DbSet<T>`,
  `DbContext`, EF Core expressions, or provider-specific types; LINQ-to-EF query
  construction stays in Infrastructure. Return materialized entities,
  collections, projections, or explicit result models as appropriate.

## Generic Repository

Application must not depend on `IGenericRepository<T>` or another generic CRUD
contract. A generic repository or `Repository<TEntity>` base class (which may
expose protected persistence helpers) may exist only as an Infrastructure
implementation detail that removes genuine duplication. Do not expand it into a
replacement for EF Core query capabilities; use-case-specific queries belong in
concrete repository implementations.

## Unit of Work

- `IUnitOfWork` (`SaveChangesAsync`) is the default commit boundary for an
  Application use case: repositories stage changes and do not independently
  call `SaveChangesAsync`, and Application Services decide when an operation is
  ready to commit. Infrastructure implements `IUnitOfWork` with the
  application's `DbContext`.
- Repositories participating in one use case must share the same Unit of Work
  and the same scoped `DbContext`. Repositories are injected explicitly into
  their consumers; `IUnitOfWork` must not act as a repository container or
  service locator exposing repositories as properties.
- Do not introduce explicit transaction APIs until a concrete use case requires
  transaction control beyond normal `SaveChangesAsync`.

## EF Core Boundary

EF Core is an Infrastructure implementation detail: use it normally, with its
full capabilities, inside Infrastructure, and do not leak EF Core concepts into
Application. The repository boundary keeps persistence concerns out of
Application; it does not hide EF Core from Infrastructure, so do not cripple
repository implementations merely to preserve a generic abstraction.

## Composition and Dependency Injection

- Use constructor injection for required dependencies by default; avoid
  service-locator and property-injection patterns.
- Respect dependency lifetimes: never capture a shorter-lived dependency (for
  example a scoped service) inside a longer-lived service.
- Keep registration close to the owning layer: Application registers
  Application services, Infrastructure registers persistence and adapters, and
  Api remains the composition root.
- Prefer strongly typed options for structured service configuration, validate
  settings at startup when missing or invalid values prevent correct or secure
  operation, and avoid scattering string-based `IConfiguration` lookups through
  services (direct `IConfiguration` access belongs to composition and
  registration code).
- When Serilog is configured, use by default the modern DI-integrated
  `builder.Services.AddSerilog(...)` approach rather than `UseSerilog`, keep
  provider configuration (levels, sinks, overrides) in environment-aware
  configuration, and keep application code depending on `ILogger<T>`.

## Boundary Contracts

- Keep cache technology out of Domain, and do not leak infrastructure cache
  APIs into Application without a deliberate boundary abstraction.
- Infrastructure translates remote HTTP responses into Application-facing
  abstractions; do not leak `HttpResponseMessage` or remote transport concerns
  into Application.
- Do not create separate Domain or persistence models merely because the
  external API has multiple versions; isolate version-specific transport
  contracts at the API boundary when practical.
- Do not duplicate equivalent DTOs across Api and Application merely to create
  layer-shaped types; introduce transport-specific request/response contracts
  when separation from Application models provides a concrete boundary benefit.
