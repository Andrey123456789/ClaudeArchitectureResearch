---
paths:
  - "backend/**"
---
<!-- Kind: STD | Scope: backend | Owns: logging usage, typed configuration, local Development database settings, Swagger UI exposure, health checks, container runtime images | Loads: path-scoped (backend/**) -->
# Backend Operations Standards

## Logging

- **Default:** application code logs through `ILogger<T>` (DEC-LOG-01) with structured message templates and stable property names; avoid string interpolation that turns structured values into opaque text.
- **Default:** when Serilog is configured, use the DI-integrated `AddSerilog()` approach and keep provider configuration in environment-aware configuration; application code keeps depending on `ILogger<T>` rather than Serilog APIs.

Sensitive data in logs: `rules/common/security.md`. Exception logging: `rules/backend/error-handling.md`.

## Configuration

- **Default:** strongly typed options for structured service configuration, validated at startup when missing or invalid values prevent correct or secure operation; avoid scattering string-based `IConfiguration` lookups through services (direct `IConfiguration` access is normal in the composition root, provider setup and infrastructure registration).
- **Default:** for the SQL Server baseline (DEC-DATA-01), `appsettings.Development.json` provides a usable local Development connection string when it contains no secret credentials; credential-bearing local values come from user-secrets or another approved local secret mechanism.

## Swagger UI Exposure

- **Default:** Swagger UI (DEC-DOCS-01) is enabled in Development; expose it in other environments only when deployment requirements explicitly justify it.

## Health Checks

- Health checks **must** stay cheap and deterministic; they **must not** become business workflows or perform expensive or mutating database work.
- Liveness and readiness **must** keep distinct dependency semantics: liveness avoids external dependencies whose outages could cause restart loops; readiness may depend on capabilities required to serve traffic and stays unhealthy until required startup work and dependencies are available.
- Publicly reachable health responses **must not** expose secrets, credentials, connection details, stack traces or unnecessary internal diagnostics.

## Containers

- **Default:** production containers use an appropriate runtime image (the ASP.NET runtime image for ASP.NET Core) rather than the SDK image for convenience, and do not switch to root merely to bypass filesystem problems. Whether to containerize: DEC-OPS-01.

Technique: `logging`, `configuration`, `swagger`, `health-check`, `docker` knowledge skills.
