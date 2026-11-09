---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> **Policy rule** · Owns: dependency-injection usage, typed configuration, structured logging and provider integration, outbound-call bounds and retries, cache correctness and cache boundaries · Scope: backend · Loading: path (backend code and appsettings)

# Backend Runtime Rules

Technique: the `dependency-injection`, `configuration`, `logging`,
`httpclient-factory`, and `caching` skills.

## Dependency Injection

- Default: inject required dependencies through constructors; avoid
  service-locator and property-injection patterns.
- Respect service lifetimes: never capture a shorter-lived dependency inside a
  longer-lived service. When a singleton or hosted service needs scoped work,
  create a scope per operation.

## Configuration

Default: bind structured service configuration to strongly typed options and
validate it at startup (`ValidateOnStart`) when missing or invalid values prevent
correct or secure operation. Avoid scattering string-based `IConfiguration`
lookups through services; direct `IConfiguration` access belongs to the
composition root and infrastructure registration.

## Logging

- Default: application code logs through `ILogger<T>` with structured message
  templates and stable property names; avoid string interpolation that turns
  structured values into opaque text.
- Default: when Serilog is configured, use the DI-integrated `AddSerilog()`
  approach and keep provider configuration (levels, sinks, overrides) in
  environment-aware configuration; application code keeps depending on
  `ILogger<T>`.

## Outbound Calls

- Infrastructure translates remote HTTP responses into Application-facing
  abstractions; do not leak `HttpResponseMessage` or remote transport concerns
  into Application.
- External I/O calls must have a bounded execution time appropriate to the
  operation; avoid overlapping timeout mechanisms (per-attempt vs. total
  operation) whose combined behavior is unclear.
- Retry only when repeating the operation is safe; do not automatically retry
  state-changing operations without idempotency or another concrete
  duplicate-prevention mechanism.
- Default: when a dependency supplies `Retry-After` or equivalent rate-limit
  guidance, respect it where appropriate; never retry indefinitely or
  aggressively.
- Use fallback only when the fallback result is semantically acceptable; do not
  hide correctness failures behind convenient default values.
- Do not classify caller cancellation as a transient dependency failure or turn it
  into repeated outbound attempts.

## Caching

Whether to cache at all: `performance.md`. When caching exists:

- Keep cache technology out of Domain, and do not leak infrastructure cache APIs
  (for example `HybridCache`) into Application without a deliberate boundary
  abstraction.
- Cache keys must uniquely represent the cached value and include every relevant
  dimension (identifier, tenant, user when user-specific, locale, query
  parameters); avoid global keys for user- or tenant-specific data.
- Every cache entry must have a lifetime or another explicit invalidation
  strategy.
- Invalidate or update cache entries only consistently with successful
  underlying mutations; the cache must not become a second source of truth.
