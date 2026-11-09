---
paths:
  - "backend/**/*"
  - "**/Dockerfile*"
---

> Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (frontmatter paths)

# Operational Concerns Standard: Health, Logging, Configuration, Containers

## Health checks

- Health checks must stay cheap and deterministic; they must not become business workflows or perform expensive or mutating database work.
- Liveness must avoid external dependencies whose unavailability could cause restart loops; readiness may depend on capabilities required to serve traffic and must reflect startup and dependency availability.
- Publicly reachable health responses must not expose secrets, credentials, connection details, stack traces, or unnecessary internal diagnostics.

## Logging

- Default: `ILogger<T>` with structured message templates and stable property names; avoid string interpolation that turns structured values into opaque text.
- Default: when Serilog is configured, use the DI-integrated `AddSerilog` approach and keep provider configuration in environment-aware configuration; application code continues to depend on `ILogger<T>`.

## Configuration

- Default: strongly typed options for structured service configuration, validated at startup when missing or invalid values prevent correct or secure operation; avoid scattering string-based `IConfiguration` lookups through services.

## Containers

- Default: production containers use an appropriate runtime image, not the SDK image for convenience, and do not switch to root merely to bypass filesystem problems.

Technique: `health-check`, `logging`, `configuration`, `docker`.
