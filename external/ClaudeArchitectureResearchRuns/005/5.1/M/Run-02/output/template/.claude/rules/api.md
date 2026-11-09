---
paths:
  - "backend/**/*.cs"
---

> Owner: HTTP status semantics, API versioning and deprecation, Swagger accuracy and exposure, health endpoints | Scope: backend | Loads: path (backend C#); read explicitly by `code-review` | Enforced: `code-review` and `verify` checks

# HTTP API Rules

Technique and the full status-code reference: `http-api`, `api-versioning`,
`swagger`, and `health-check` skills.

## HTTP Semantics

- HTTP status codes and transport response semantics belong to the API layer;
  Application and Domain must not return `IActionResult`, `ProblemDetails`, or
  ASP.NET Core status codes.
- Choose `200`, `201`, `202`, or `204` by the actual HTTP semantics of the
  outcome: not `200` for every outcome, not `201` merely because a row was
  inserted internally, not `202` for work that has already completed.
- Default: a successful collection query with zero matches returns `200` with an
  empty collection, not `404`.
- Use `401` when authentication is missing or failed and `403` when an
  authenticated principal is not permitted. Returning `404` to hide a protected
  resource requires a deliberate, consistently applied security policy.
- Use `409` for a valid request that conflicts with current state, and `412` when
  an explicit HTTP precondition such as `If-Match` fails.

## Versioning

- Do not introduce API versioning merely because an API exists; add it only when
  published compatibility or coexisting client generations create a concrete
  need.
- Once external clients rely on an API version, do not break it silently: a
  breaking contract change requires a new version or another explicitly approved
  compatibility strategy.
- Default: when explicit versioning is required, use one strategy consistently;
  URL-segment versioning unless project requirements justify another.
- Do not create separate Domain or persistence models merely because the API has
  several versions; isolate version-specific transport contracts at the API
  boundary when practical.
- When deprecating an externally consumed version, mark it deprecated in the
  versioning metadata, document the replacement, communicate a realistic
  migration and removal timeline, and keep it working for the promised support
  period; do not remove it without considering its published support contract.

## Swagger

- Swagger/OpenAPI metadata must describe the API that actually runs — routes,
  important response statuses, schemas, and authentication behavior — and must
  not document speculative responses.
- Default: enable Swagger UI in Development; expose it in other environments only
  when deployment requirements explicitly justify it.

## Health Checks

- Health checks must stay cheap and deterministic: no full business workflows,
  expensive queries, or database writes.
- Liveness must avoid external dependencies whose unavailability could cause
  restart loops; readiness may depend on capabilities required to serve traffic
  and reflects required dependency and startup availability.
- Publicly reachable health responses must not expose secrets, credentials,
  connection details, stack traces, or unnecessary internal diagnostics.
