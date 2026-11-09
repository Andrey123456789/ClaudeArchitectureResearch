---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
---

> Level: 1 Architecture · Owns: layer dependency direction, Domain and Application responsibilities, infrastructure adapter boundaries, composition and dependency injection · Scope: backend · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/1-architecture/overview.md

# Backend Layers

Concrete framework types for these boundaries are named in `.claude/rules/2-technology/`. Concrete project names: `3-project/layout.md`.

## Dependency direction

Dependencies must point inward:

- Domain depends on no other application project.
- Application depends on Domain.
- Infrastructure depends on Application and Domain.
- Api depends on Application and may reference Infrastructure only as required for composition and dependency registration.
- Inner layers never depend on outer layers; Domain and Application never reference Infrastructure-specific types.

If a feature seems to need an outward reference, reconsider the abstraction boundary instead of adding the reference.

## Domain

- Domain must stay independent of persistence frameworks, web/transport frameworks, HTTP, persistence, and external-service implementation concerns.
- Simple domain entities are the default. For CRUD-oriented applications and straightforward workflows, keep entities simple and enforce use-case and workflow rules in Application Services (default). Validation rules, immutable fields, status transitions, or allowed/forbidden edits do not by themselves justify a Rich Domain Model.
- Move behavior into Domain only when non-trivial domain invariants or behavior materially benefit from domain-level encapsulation independently of a particular use case. Otherwise a Rich Domain Model or DDD tactical pattern requires approval, unless the approved specification already requires that design.
- Do not add factory methods, private setters, transition methods, Aggregate Roots, Domain Events, Specifications, Domain Services, systematic Value Objects, or similar DDD constructs merely to make a simple model look domain-driven.

## Application

- Application Services are the default orchestration mechanism for use cases; they coordinate Domain objects, repositories, external-service abstractions, and the Unit of Work (default). A service growing too large is a signal to reconsider its responsibilities, not an automatic reason to adopt another pattern.
- Define persistence and external-service abstractions in Application when use cases require them; keep infrastructure implementation details out of Application.
- Application must not depend on persistence-framework types or APIs (context, set, or query-expression types of the persistence framework), provider-specific types, or web-framework transport types.

## Infrastructure adapters

- Infrastructure translates remote HTTP responses into the Application-facing abstraction; do not leak `HttpResponseMessage` or other remote-transport concerns into Application.
- Keep cache technology out of Domain, and do not leak infrastructure cache APIs into Application without a deliberate boundary abstraction.

## Composition and dependency injection

- `Program.cs` in Api is the application composition root and may register Infrastructure implementations (default).
- Keep registration close to the owning layer: Application registers Application services, Infrastructure registers persistence and adapters, and Api remains the composition root (default).
- Use constructor injection for required dependencies by default; avoid service-locator and property-injection patterns (default).
- Respect dependency lifetimes: never capture a shorter-lived dependency inside a longer-lived service.
