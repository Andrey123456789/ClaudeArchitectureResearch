---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
  - "backend/**/Dockerfile*"
  - "backend/**/.dockerignore"
---

> Kind: STD | Scope: backend | Owner: hosting and operations — configuration binding, logging, health checks, container images | Loading: path-scoped

# Hosting and Operations Standard

Logging provider: D-06. Containers: D-14.

See also: `rules/common/security.md` (sensitive data in logs).

## Configuration

- Default: strongly typed options for structured service configuration, validated at startup when missing or invalid values would prevent correct or secure operation. Avoid scattering string-based `IConfiguration` lookups through services; direct `IConfiguration` access belongs in the composition root, configuration-provider setup and infrastructure registration.

## Logging

- Default: `ILogger<T>` with structured message templates and stable property names; avoid string interpolation that turns structured values into opaque text.
- Default: when Serilog is configured, use the DI-integrated `AddSerilog` approach with provider configuration in environment-aware configuration; application code keeps depending on `ILogger<T>`.

## Health checks

- Health checks must stay cheap and deterministic and must not become business workflows or perform expensive or mutating database work.
- Liveness must not depend on external dependencies whose unavailability would cause restart loops (by default no database or remote API checks); readiness may depend on capabilities required to serve traffic and must reflect startup completion and required-dependency availability.
- Publicly reachable health responses must not expose secrets, credentials, connection details, stack traces or unnecessary internal diagnostics.

## Containers

- Default: production containers use an appropriate runtime image (the ASP.NET Core runtime image for APIs) rather than the SDK image for convenience, and avoid switching to root merely to bypass a filesystem problem.
