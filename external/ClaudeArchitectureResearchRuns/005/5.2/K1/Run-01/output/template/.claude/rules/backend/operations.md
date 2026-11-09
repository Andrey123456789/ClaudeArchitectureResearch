---
paths:
  - "backend/**"
  - "**/Dockerfile*"
  - "**/*.dockerfile"
  - "**/docker-compose*.yml"
  - "**/docker-compose*.yaml"
  - "**/compose*.yml"
  - "**/compose*.yaml"
---
Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (backend/**, container files)

# Operations Standards: Logging, Configuration, Containers

Technique: `logging` (Serilog depth in its reference), `configuration` and `docker` knowledge skills.

## Logging

- Default: log through `ILogger<T>` with structured message templates and stable property names. Avoid string interpolation that turns structured values into opaque text.
- Default: when Serilog is configured, use the DI-integrated `AddSerilog()` approach rather than `UseSerilog()`, keep provider configuration (levels, sinks, enrichers) in environment-aware configuration, and keep application code on `ILogger<T>`.

## Configuration

- Default: use strongly typed options for structured service configuration and validate them at startup when missing or invalid values prevent correct or secure operation. Avoid scattering string-based `IConfiguration` lookups through services.

## Containers

- Default: production containers use an appropriate runtime image (the ASP.NET Core runtime image for ASP.NET Core applications), not the SDK image for convenience. Do not switch to root merely to work around a filesystem-permission problem.
