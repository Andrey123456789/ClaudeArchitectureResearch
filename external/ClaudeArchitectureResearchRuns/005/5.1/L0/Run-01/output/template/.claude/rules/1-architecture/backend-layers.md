---
paths:
  - "backend/**"
---

> Level: 1 Architecture · Owns: layer dependency direction, layer responsibilities, composition · Scope: backend, backend-tests · Loads: path; read explicitly by `project-structure`

# Backend Layers

## Dependency direction

- **Must** keep dependencies pointing inward:
  - Domain depends on no other application project;
  - Application depends on Domain;
  - Infrastructure depends on Application and Domain;
  - Api depends on Application and may reference Infrastructure only for composition and dependency registration.

  Inner layers never depend on outer layers, and Domain or Application never reference Infrastructure-specific types. When a feature seems to need an outward reference, reconsider the abstraction boundary instead of adding the reference.
- **Must not** give backend test projects broader production-project references than their test scope requires; tests keep the same inward discipline (Application tests → Application and Domain as needed; integration tests → Api; Domain or Infrastructure tests → their own layer and narrower references).

Mechanical check: `node .claude/scripts/check-architecture.mjs`.

## Domain

- **Must** keep Domain independent of persistence frameworks, web/transport frameworks, HTTP, persistence concerns and external-service implementations.
- **Default:** simple domain entities. CRUD-oriented and straightforward workflow rules — validation rules, immutable fields, status transitions, allowed or forbidden edits — belong in Application Services and do not by themselves justify a Rich Domain Model.
- **Requires approval:** move behavior into Domain entities only when non-trivial domain invariants or behavior materially benefit from domain-level encapsulation independent of a particular use case. Otherwise a Rich Domain Model or DDD tactical pattern is a Reserved decision unless the approved specification already requires it.
- **Must not** add factory methods, private setters, transition methods, aggregate roots, domain events, specifications, domain services, systematic value objects or similar constructs merely to make a simple model look domain-driven.

## Application

- **Default:** Application Services are the orchestration mechanism for use cases; they coordinate Domain objects, repositories, external-service abstractions and the unit of work.
- **Must** define the persistence and external-service abstractions that use cases require in Application, keeping implementation details out.
- **Must not** let Application depend on persistence-framework types or APIs, provider-specific types, or web-transport types.
- **Must** keep cache technology out of Domain, and keep infrastructure cache APIs out of Application unless a deliberate boundary abstraction is introduced.
- **Must** have Infrastructure translate remote HTTP responses into Application-facing abstractions; `HttpResponseMessage` and other remote-transport concerns never leak into Application.

## Composition

- **Default:** constructor injection for required dependencies; avoid service-locator and property-injection patterns.
- **Must** respect service lifetimes: a longer-lived service never captures a shorter-lived dependency (a singleton that needs scoped work creates a scope per operation).
- **Default:** keep registration close to the owning layer — Application registers Application services, Infrastructure registers persistence and adapters.
- **Default:** the Api host's startup (`Program.cs`) is the composition root and may register Infrastructure implementations.
