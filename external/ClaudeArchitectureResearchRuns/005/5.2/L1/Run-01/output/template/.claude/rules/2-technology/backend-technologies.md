---
paths:
  - "backend/**/*"
  - "**/Dockerfile*"
  - "**/*.dockerfile"
  - "**/.dockerignore"
  - "**/docker-compose*.yml"
  - "**/docker-compose*.yaml"
  - "**/compose*.yml"
  - "**/compose*.yaml"
---
> Level: 2-technology | Owns: rules for embedded backend technologies — validation library, API documentation, logging provider, containers | Scope: backend | Loads: path (backend and container files)

# Embedded Backend Technologies

## Validation — FluentValidation

Use FluentValidation for explicit request and use-case validation where rules
need expressing. Keep each rule at its owning boundary: transport and
request-contract concerns at the entry point, use-case input and
straightforward workflow rules in use-case validators or use-case units,
non-trivial invariants the domain genuinely owns in the domain model, and
assumptions about external systems in adapters. Do not move domain invariants
into validators merely because the library is available, and do not duplicate
the same rule mechanically at every layer. Follow the project's established
validation invocation pattern; do not add a deprecated or legacy ASP.NET
automatic-validation integration package unless a concrete requirement
justifies it.

## API documentation — Swashbuckle (Swagger UI)

- Swagger/OpenAPI metadata must describe the API that actually runs — routes,
  important response statuses, schemas, and authentication behavior —
  considering the whole pipeline (binding, validation, authentication,
  exception handling). Do not document speculative responses.
- Default: Swagger UI is enabled in Development; expose it in another
  environment only when deployment requirements explicitly justify it.

## Logging provider — Serilog

Default: register Serilog with `builder.Services.AddSerilog(...)` (not
`UseSerilog()`), keep levels, sinks, and overrides in environment-aware
configuration, and keep direct Serilog APIs (`Log.Logger`, `LogContext`) at
composition and provider boundaries.

## Containers — Docker

Default: production images use the appropriate runtime image (the ASP.NET Core
runtime image for the API), not the SDK image solely for convenience; run as a
non-root user where supported and do not switch to root merely to bypass a
filesystem permission problem.

Technique: `swagger`, `logging`, `docker`.
