---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
---

> Level: 1 Architecture | Owns: layer responsibilities, reference direction, composition root, registration ownership, infrastructure adapter boundaries, test-project references | Scope: backend, backend-tests | Loads: path | Depends on: 1-architecture/overview.md

# Backend Layers

## Dependency Direction

Dependencies must point inward:

- `Domain` depends on no other application project.
- `Application` depends on `Domain`.
- `Infrastructure` depends on `Application` and `Domain`.
- `Api` depends on `Application` and may reference `Infrastructure` only as
  required for composition and dependency registration.
- Inner layers never depend on outer layers. If a feature seems to need an
  outward reference, reconsider the abstraction boundary instead.

Backend test projects must not have broader production-project references than
their test scope requires; they follow the same inward discipline.

## Domain

- Keep Domain independent of persistence frameworks, web and transport
  frameworks, HTTP, and external-service implementation concerns.
- Default: simple domain entities. Straightforward CRUD and workflow rules
  belong in Application Services; validation rules, immutable fields, status
  transitions, or allowed edits do not by themselves justify a Rich Domain
  Model.
- Move behavior into Domain only when non-trivial domain invariants or behavior
  materially benefit from domain-level encapsulation; otherwise a Rich Domain
  Model or DDD tactical pattern requires approval.
- Do not add factories, private setters, transition methods, Aggregate Roots,
  Domain Events, Specifications, Domain Services, systematic Value Objects, or
  similar DDD constructs merely to appear domain-driven.

## Application

- Default: Application Services orchestrate use cases; they coordinate Domain
  objects, repositories, external-service abstractions, and the Unit of Work. A
  large service is a signal to reconsider responsibilities, not a reason to
  adopt another pattern.
- Define persistence and external-service abstractions in Application when use
  cases require them; keep infrastructure implementation details out.
- Application must not depend on persistence-framework types or APIs, database
  provider types, or web-framework transport types.

## Infrastructure Adapters

- Keep cache technology out of Domain, and do not leak infrastructure cache
  APIs into Application without a deliberate boundary abstraction.
- Infrastructure translates remote HTTP responses into Application-facing
  abstractions; do not leak HTTP response objects or remote transport concerns
  into Application.

## Composition

- Default: the Api project's `Program.cs` is the composition root and may
  register Infrastructure implementations.
- Default: keep registration close to the owning layer — Application registers
  Application services, Infrastructure registers persistence and adapters, and
  the Api project composes them.

Technology bindings for "persistence framework" and "web framework": → `2-technology/ef-core.md`, `2-technology/aspnet-core.md`.
