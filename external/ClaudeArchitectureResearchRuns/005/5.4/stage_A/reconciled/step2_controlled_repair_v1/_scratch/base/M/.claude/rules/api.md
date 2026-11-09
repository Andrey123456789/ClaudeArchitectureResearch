---
paths:
  - "backend/**/*.cs"
---

> Owns: HTTP status semantics, API versioning, Swagger accuracy and exposure, health endpoints | Scope: backend | Loads: path-scoped (backend C# files)

# API Rules

Error contracts and exception handling: `error-handling.md`. Status-code
reference, headers, and examples: `http-api` skill.

## HTTP Semantics

- HTTP status codes and transport response semantics belong to the API layer.
  Application and Domain must not return `IActionResult` or ASP.NET Core status
  codes.
- Choose `200`/`201`/`202`/`204` according to the actual HTTP semantics: do not
  return `200` for every outcome, `201` merely because a row was inserted
  internally (`201` means the operation created an API resource), or `202` for
  work that already completed synchronously. A `204` response has no body.
- A successful collection query with zero matches returns `200` with an empty
  collection by default, not `404`.
- Use `401` when authentication is missing or failed and `403` when an
  authenticated principal is not permitted. Returning `404` to hide a protected
  resource must be a deliberate, consistent security policy.
- Use `409` for a valid request that conflicts with the current state and `412`
  when an explicit HTTP precondition such as `If-Match` fails.
- Keep status-code behavior consistent across similar endpoints.

## API Versioning

- Do not introduce API versioning merely because an API exists; add it when
  published compatibility or coexistence of client generations creates a
  concrete need. Adopting versioning is a Reserved decision.
- Once an API version is relied on by external clients, avoid silent breaking
  changes: a breaking contract change requires, by default, a new version or
  another explicitly approved compatibility strategy. Do not judge
  compatibility only by whether the code compiles.
- When explicit versioning is required, use one strategy consistently;
  URL-segment versioning (`/api/v1/...`) is the default unless project
  requirements justify header or query-string versioning.
- Deprecating a version: `development-workflow` (API deprecation step).

## Swagger / OpenAPI

- Swagger/OpenAPI metadata must describe the API that actually runs — routes,
  important response statuses (including those produced by binding,
  validation, authentication/authorization, rate limiting, or centralized
  exception handling), schemas, and authentication behavior. Do not document
  speculative responses.
- Enable Swagger UI in Development by default; expose it in other environments
  only when deployment requirements explicitly justify it.

## Health Checks

- Health checks must stay cheap and deterministic; they must not become full
  business workflows or perform expensive or mutating database work.
- Keep liveness and readiness semantics distinct: liveness by default avoids
  external dependencies that could cause restart loops; readiness may depend on
  capabilities required to serve traffic and reflects startup and dependency
  availability (it stays unhealthy until required startup work completes —
  never use liveness for that).
- Publicly reachable health responses must not expose secrets, credentials,
  connection details, stack traces, or unnecessary internal diagnostics.
