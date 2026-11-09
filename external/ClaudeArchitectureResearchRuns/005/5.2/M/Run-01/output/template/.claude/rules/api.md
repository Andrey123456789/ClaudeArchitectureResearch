---
paths:
  - "backend/**/*.cs"
---

> Path-scoped rule. Owns: HTTP response semantics, API versioning boundaries, Swagger accuracy and exposure, health endpoints · Scope: backend · Loads: when backend C# files are in context · Depends on: CLAUDE.md, docs/technology-stack.md

# API Rules

Error contracts, exception handling, and validation: `error-handling.md`.
Status-code reference and examples: `http-api` skill; also `api-versioning`,
`swagger`, and `health-check` skills.

## HTTP Semantics

- HTTP status codes and transport response semantics belong to the API layer.
  Application and Domain must not return `IActionResult`, `ProblemDetails`, or
  HTTP status codes; Controllers translate Application outcomes into HTTP
  responses.
- Choose `200`, `201`, `202`, or `204` by the actual HTTP semantics of the
  outcome: do not return `200` for every outcome, `201` merely because a row was
  inserted internally, or `202` for work that already completed. Return `201`
  when the operation creates an API resource, with a `Location` header when a
  stable resource URI exists.
- Default: a successful collection query with zero matches returns `200` with
  an empty collection, not `404`.
- Use `401` when authentication is missing or failed and `403` when an
  authenticated principal is not permitted. Returning `404` to hide a protected
  resource requires a deliberate, consistent security policy.
- Use `409` for a valid request that conflicts with the current state; use
  `412` when an explicit HTTP precondition such as `If-Match` fails.

## API Versioning

- Do not introduce API versioning merely because an API exists; add it only
  when published compatibility needs or coexisting client generations create a
  concrete need (adoption requires approval — CLAUDE.md, Decision Control).
- Once an API version is relied on by external clients, do not break it
  silently: a breaking contract change requires a new version or another
  explicitly approved compatibility strategy.
- Default: when explicit versioning is adopted, use one strategy consistently;
  URL-segment versioning unless project requirements justify another strategy.
- Deprecating or removing a published version follows `development-workflow`.

## Swagger

- Swagger/OpenAPI metadata must describe the API that actually runs: routes,
  important response statuses, schemas, and authentication behavior. Do not
  document speculative responses.
- Default: Swagger UI is enabled in Development; expose it in other
  environments only when a deployment requirement explicitly justifies it.

## Health Checks

- Health checks must stay cheap and deterministic; they must not become
  business workflows or perform expensive or mutating database work.
- Liveness must not depend on external dependencies whose unavailability could
  cause restart loops. Readiness may depend on capabilities required to serve
  traffic and must reflect startup and dependency availability, staying
  unhealthy until required startup work completes.
- Publicly reachable health responses must not expose secrets, credentials,
  connection details, stack traces, or unnecessary internal diagnostics.
