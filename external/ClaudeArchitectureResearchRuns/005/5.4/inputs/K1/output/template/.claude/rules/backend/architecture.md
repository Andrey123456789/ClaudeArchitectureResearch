---
paths:
  - "backend/**/*"
---

> Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (frontmatter paths)

# Backend Architecture Standard (role level)

Applies to the backend roles named in the decision register (Domain, Application, Infrastructure, Api). The selected architecture frame adds its own style rules in `architecture-style.md`.

## HTTP entry points

- ASP.NET Core Controllers are the default HTTP entry point and must stay thin: bind and validate HTTP input, invoke Application services, and translate Application outcomes into HTTP responses.
- Controllers must not contain business logic, access the database context or concrete repositories, or construct infrastructure services manually.

## Dependency injection

- Default: constructor injection for required dependencies; avoid service-locator and property-injection patterns.
- Dependency lifetimes must be valid: never capture a shorter-lived dependency inside a longer-lived service.

## Technical boundaries

- Cache technology must stay out of Domain, and infrastructure cache APIs must not leak into Application without a deliberate boundary abstraction.
- Infrastructure translates remote HTTP responses into Application-facing abstractions; `HttpResponseMessage` and other remote transport concerns must not leak into Application.

Technique: `dependency-injection`, `caching`, `httpclient-factory`.
