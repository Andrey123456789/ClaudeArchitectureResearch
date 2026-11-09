---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Level: 2 Technology | Owns: .NET async and cancellation, time abstraction, outbound HttpClient lifetime, dependency-injection mechanics, typed configuration | Scope: backend | Loads: path | Depends on: 1-architecture/backend-layers.md

# .NET Runtime Conventions

## Async and Cancellation

- Use async APIs for asynchronous I/O; do not block them with `.Result`,
  `.Wait()`, or similar sync-over-async patterns.
- Propagate `CancellationToken` through asynchronous operations when
  cancellation is meaningful; do not add cancellation parameters to purely
  synchronous code without a use case.

## Time

- Default: use `TimeProvider` for application logic that depends on the current
  clock and needs deterministic tests; do not mechanically replace stored or
  explicit timestamps.

## Outbound HTTP

- Do not create and dispose a new `HttpClient` per request; use
  `IHttpClientFactory` or another appropriate long-lived client strategy.

## Dependency Injection

- Default: use constructor injection for required dependencies; avoid
  service-locator and property-injection patterns.
- Respect service lifetimes; never capture a shorter-lived dependency inside a
  longer-lived service.

## Configuration

- Default: prefer strongly typed options for structured service configuration
  and validate settings at startup when missing or invalid values prevent
  correct or secure operation; avoid scattering string-based `IConfiguration`
  lookups through application services.

Technique: → `dependency-injection`, `configuration`, `httpclient-factory` skills.
