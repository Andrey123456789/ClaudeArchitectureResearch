---
paths:
  - "backend/**/*.cs"
  - "backend/**/launchSettings.json"
---

> Path rule · Scope: backend · Owns HTTP status semantics, API versioning, Swagger accuracy and exposure, and health-check policy

# HTTP API Rules

Error contracts and exception mapping: `.claude/rules/error-handling.md`.
Status-code reference and examples: `http-api` skill.

## HTTP Semantics

- HTTP status codes and transport response semantics belong to the API layer.
  Application and Domain must not return `IActionResult` or ASP.NET Core status
  codes.
- Choose `200`, `201`, `202`, or `204` according to the actual HTTP semantics of
  the outcome. Do not return `200` for every outcome, `201` merely because a row
  was inserted internally (`201` means a new API resource, with `Location` when
  a stable resource URI exists), or `202` for work that already completed.
- By default, a successful collection query with zero matches returns `200`
  with an empty collection, not `404`.
- Use `401` when authentication is missing or failed and `403` when an
  authenticated principal is not permitted. Returning `404` to hide protected
  resources requires a deliberate, consistent security policy.
- Use `409` for a valid request that conflicts with the current state; use
  `412` when an explicit HTTP precondition such as `If-Match` fails.

## API Versioning

- Do not introduce API versioning merely because an API exists; add it when
  published compatibility or coexisting client generations create a concrete
  need. Adopting versioning is Reserved.
- Once an API version is relied on by external clients, avoid silent breaking
  changes; a breaking contract change requires a new version or another
  explicitly approved compatibility strategy.
- When explicit versioning is required, use one strategy consistently;
  URL-segment versioning is the default unless project requirements justify
  another strategy.
- Deprecating or removing a published version: `architecture-decision`
  workflow § Public API Version Deprecation.

## Swagger

- Swagger/OpenAPI metadata must describe the API that actually runs — routes,
  important response statuses, schemas, and authentication behavior. Do not
  document speculative responses.
- Enable Swagger UI in Development by default; expose it in other environments
  only when deployment requirements explicitly justify it.

## Health Checks

- Health checks must remain cheap and deterministic. They must not become full
  business workflows and must not perform expensive or mutating database work.
- Liveness must not depend on external dependencies whose unavailability could
  cause restart loops; readiness may depend on the capabilities required to
  serve traffic and must reflect startup and dependency availability
  appropriately.
- Do not expose secrets, credentials, connection details, stack traces, or
  unnecessary internal diagnostics through publicly reachable health responses.
