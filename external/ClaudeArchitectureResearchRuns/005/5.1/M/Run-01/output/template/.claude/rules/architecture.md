---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
---

> Owns: Clean Architecture boundaries, project references, repositories, Unit of Work, EF Core boundary, DI composition, configuration binding | Scope: backend, backend-tests (project references) | Loads: path

# Architecture Rules

Adopted and not-adopted architecture, and the approval gate, are in `CLAUDE.md`.

## Dependency Direction

Dependencies must point inward:

- `Domain` depends on no other application project.
- `Application` depends on `Domain`.
- `Infrastructure` depends on `Application` and `Domain`.
- `Api` depends on `Application` and may reference `Infrastructure` only as
  required for application composition and dependency registration.
- Inner layers must never depend on outer layers. If a feature seems to require
  `Domain -> Application/Infrastructure` or `Application -> Infrastructure`,
  reconsider the abstraction boundary instead of adding the reference.

Backend test projects must not receive broader production-project references
than their test scope requires, and they follow the same inward discipline
(for example `Application.Tests -> Application (+ Domain as needed)`;
`IntegrationTests -> Api` for `WebApplicationFactory<Program>`).

## Domain

- Keep Domain free of EF Core, ASP.NET Core, HTTP, persistence, and
  external-service concerns.
- Simple domain entities are the default. For CRUD-oriented applications and
  straightforward workflows, enforce use-case/workflow rules in Application
  Services. Validation rules, immutable fields, status transitions, or
  allowed/forbidden edits do not by themselves justify a Rich Domain Model.
- Move behavior into Domain entities only when non-trivial domain invariants or
  behavior materially benefit from domain-level encapsulation independently of
  a particular use case; otherwise adopting a Rich Domain Model or DDD tactical
  pattern is Reserved (`CLAUDE.md`) unless the approved specification requires it.
- Do not add factory methods, private setters, transition methods, Aggregate
  Roots, Domain Events, Specifications, Domain Services, systematic Value
  Objects, or similar DDD constructs merely to make a simple model appear more
  domain-driven.

## Application

- Application Services are the default use-case orchestration mechanism; they
  coordinate Domain objects, repositories, external-service abstractions, and
  the Unit of Work.
- Define persistence and external-service abstractions in Application when use
  cases require them; keep infrastructure implementation details out.
- Application must not use `DbContext`, `DbSet<T>`, EF Core APIs,
  provider-specific types, or ASP.NET Core transport types.
- A service becoming too large is a signal to reconsider its responsibilities,
  not an automatic reason to introduce another architectural pattern.

## API

ASP.NET Core Controllers are the default HTTP entry point and must stay thin:
bind and validate HTTP input, invoke Application services, and translate
application outcomes into HTTP responses.

Controllers must not contain business logic, access `DbContext` or concrete
repositories, or construct infrastructure services manually.

`Program.cs` is the application composition root and may register
Infrastructure implementations.

Do not duplicate equivalent DTOs across Api and Application merely to create
layer-shaped types; introduce transport-specific request/response contracts in
Api when separation from Application models provides a concrete boundary
benefit.

## Repositories

- Prefer specific repository interfaces that represent actual, cohesive
  Application persistence needs rather than blindly mirroring every table.
  When an approved DDD design has Aggregate Roots, they are natural repository
  boundaries.
- Define repository interfaces in Application; implement them in
  Infrastructure; keep LINQ-to-EF query construction inside Infrastructure.
- Repository interfaces must not expose `IQueryable<T>`, `DbSet<T>`,
  `DbContext`, EF Core expressions, or provider-specific types. Return
  materialized entities, collections, projections, or explicit result models.

## Generic Repository

Application must not depend on `IGenericRepository<T>` or another generic CRUD
contract. A generic repository/base class may exist only as an Infrastructure
implementation detail that removes genuine duplication; do not expand it into a
replacement for EF Core query capabilities. Use-case-specific queries belong in
concrete repositories.

## Unit of Work

- `IUnitOfWork` is the default commit boundary for an Application use case:
  repositories stage changes and Application Services decide when to commit.
- Repositories participating in one use case must share the same scoped Unit of
  Work / `DbContext` and are injected explicitly into their consumers.
- `IUnitOfWork` must not become a repository container or service locator that
  exposes repositories as properties.
- By default, do not introduce explicit transaction APIs until a concrete use
  case requires control beyond normal `SaveChangesAsync`.

## EF Core Boundary

EF Core is an Infrastructure implementation detail: use it normally inside
Infrastructure, but do not leak EF Core concepts into Application. Do not
cripple repository implementations merely to preserve a generic abstraction.
Development seeding and migrations: `persistence.md`.

## Infrastructure Adapters

- Keep cache technology out of Domain, and do not leak infrastructure cache APIs
  into Application without a deliberate boundary abstraction.
- Infrastructure translates remote HTTP responses into Application-facing
  abstractions; do not leak `HttpResponseMessage` or remote transport concerns
  into Application.

## Dependency Injection and Configuration

- Constructor injection is the default for required dependencies; avoid
  service-locator and property-injection patterns.
- Respect service lifetimes: never capture a shorter-lived dependency inside a
  longer-lived service.
- By default, keep registration close to the owning layer: Application registers
  Application services, Infrastructure registers persistence and adapters, and
  Api remains the composition root.
- Prefer strongly typed options for structured service configuration and
  validate at startup settings whose absence or invalid value prevents correct
  or secure operation; avoid scattering string-based `IConfiguration` lookups
  through services (direct access in composition/registration code is normal).

Technique: `ef-core`, `dependency-injection`, `configuration`, `caching`,
`httpclient-factory` skills.
