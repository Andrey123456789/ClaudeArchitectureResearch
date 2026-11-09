---
paths:
  - "backend/**"
---
Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (backend/**)

# Backend Architecture Standards (role level)

The layer roles Domain, Application, Infrastructure and Api come from the selected architecture frame (decision register). The frame's own dependency, placement and boundary rules are in `.claude/rules/backend/architecture-style.md`.

## Composition and dependency injection

- Default: `Program.cs` in the Api project is the application composition root and may register Infrastructure implementations.
- Default: use constructor injection for required dependencies. Avoid service-locator and property-injection patterns.
- Dependency lifetimes must be valid: never capture a shorter-lived dependency (for example a scoped service) inside a longer-lived service (for example a singleton).
- Default: keep registration next to the owning layer. Application registers Application services, Infrastructure registers persistence and adapters, and Api composes them.

## Infrastructure concerns stay out of inner layers

- Cache technology stays out of Domain, and infrastructure cache APIs do not leak into Application without a deliberate boundary abstraction.
- Infrastructure translates remote HTTP responses into Application-facing abstractions. `HttpResponseMessage` and other remote transport concerns do not leak into Application.

## API boundary contracts

- Do not create separate Domain or persistence models merely because the external API has several versions. Isolate version-specific transport contracts at the API boundary when practical.
- Do not duplicate equivalent DTOs across Api and Application merely to create layer-shaped types. Introduce transport-specific request and response contracts when separation from Application models gives a concrete boundary benefit.
