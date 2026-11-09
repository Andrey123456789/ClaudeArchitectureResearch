---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Path rule · Scope: backend · Owns dependency-injection, typed-configuration, and logging-provider policy

# Service Composition Rules

Layer placement of registrations: `.claude/rules/architecture.md` § Layer
Placement. Sensitive data in logs: `.claude/rules/security.md`. Exception
logging: `.claude/rules/error-handling.md`.

## Dependency Injection

- Constructor injection is the default for required dependencies; avoid
  service-locator and property-injection patterns.
- Respect service lifetimes: never capture a shorter-lived dependency inside a
  longer-lived service. A singleton or hosted service that needs scoped work
  creates a scope per operation and resolves a scoped orchestration service.

## Configuration

- Prefer strongly typed options for structured configuration consumed by
  services; avoid scattering string-based `IConfiguration` lookups through
  application services. Direct `IConfiguration` access is appropriate in the
  composition root, configuration-provider setup, and infrastructure
  registration.
- Validate settings at startup when missing or invalid values prevent correct
  or secure operation.

## Logging

- Use `ILogger<T>` with structured message templates and stable property names;
  avoid string interpolation that turns structured values into opaque text.
- When Serilog is configured, use the modern DI-integrated `AddSerilog()`
  approach and keep provider configuration (levels, sinks, overrides) in
  environment-aware configuration. Application code continues to depend on
  `ILogger<T>` rather than Serilog APIs.
