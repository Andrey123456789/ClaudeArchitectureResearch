---
paths:
  - "backend/**/*"
---
> Level: 0-core | Owns: dependency injection, logging API, configuration, health checks | Scope: backend | Loads: path (backend files)

# Hosting and Composition Rules

## Dependency injection

- Default: constructor injection for required dependencies; avoid
  service-locator and property-injection patterns.
- Respect service lifetimes: never capture a shorter-lived dependency inside a
  longer-lived service. When a singleton or hosted service needs scoped work,
  create a scope per operation.

## Logging

Default: log through `ILogger<T>` with structured message templates and stable
property names; avoid string interpolation that turns structured values into
opaque text.

## Configuration

Default: bind structured service configuration to strongly typed options and
validate at startup the settings whose absence or invalid value prevents correct
or secure operation. Avoid scattering string-based `IConfiguration` lookups
through services; direct `IConfiguration` access belongs to the composition
root, configuration-provider setup, and adapter registration.

## Health checks

- Health checks must stay cheap and deterministic; they must not become business
  workflows or perform expensive or mutating database work.
- Liveness must not depend on external dependencies whose temporary
  unavailability would cause restart loops. Readiness may depend on the
  capabilities required to serve traffic and must reflect startup and
  dependency availability (unhealthy until required startup work completes).
- Publicly reachable health responses must not expose secrets, credentials,
  connection details, stack traces, or unnecessary internal diagnostics.

Technique: `dependency-injection`, `logging`, `configuration`, `health-check`.
