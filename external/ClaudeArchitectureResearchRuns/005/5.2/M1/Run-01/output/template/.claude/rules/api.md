---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
  - "backend/**/Properties/launchSettings.json"
---

> **Policy rule** · Owns: HTTP status semantics, API versioning, Swagger accuracy and exposure, health endpoints · Scope: backend · Loading: path (backend code and API configuration)

# HTTP API Rules

Technique and the full status-code reference: the `http-api`, `api-versioning`,
`swagger`, and `health-check` skills. Error contracts: `error-handling.md`.

## HTTP Semantics

- HTTP status codes and transport response semantics belong to the API layer.
  Application and Domain must not return `IActionResult` or ASP.NET Core status
  codes.
- Choose `200`/`201`/`202`/`204` by actual HTTP semantics: do not return `200` for
  every outcome, `201` merely because a row was inserted internally (only when the
  HTTP operation created an API resource), or `202` for work that already
  completed synchronously.
- Default: a successful collection query with zero matches returns `200` with an
  empty collection, not `404`.
- Use `401` when authentication is missing or failed and `403` when an
  authenticated principal is not permitted. Returning `404` to hide a protected
  resource requires a deliberate, consistent security policy.
- Use `409` for a valid request that conflicts with current state; use `412` when
  an explicit HTTP precondition such as `If-Match` fails.

## API Versioning

- Do not introduce API versioning merely because an API exists; add it when
  published compatibility or coexistence of client generations creates a concrete
  need (adopting it is Reserved).
- Once an API version is relied on by external clients, avoid silent breaking
  changes; a breaking contract change requires a new version or another explicitly
  approved compatibility strategy.
- Default: when explicit versioning is required, use one strategy consistently;
  URL-segment versioning is the default unless project requirements justify
  another.
- Do not create separate Domain or persistence models merely because the external
  API has multiple versions; isolate version-specific transport contracts at the
  API boundary when practical.

## Swagger

- Swagger/OpenAPI metadata must describe the API that actually runs — routes,
  important response statuses (including those produced by binding, validation,
  authentication/authorization, and middleware), schemas, and authentication
  behavior. Do not document speculative responses.
- Default: map Swagger UI only inside the Development environment check
  (`app.Environment.IsDevelopment()`); mapping it for another environment needs
  the deployment justification required by `docs/technology-stack.md` → API
  Documentation.

## Health Checks

- Health checks must stay cheap and deterministic; they must not become business
  workflows or perform expensive or mutating database work.
- Liveness avoids external dependencies that could cause restart loops;
  readiness may depend on capabilities required to serve traffic and reflects
  startup and dependency availability (unready until required startup work
  completes).
- Do not expose secrets, credentials, connection details, stack traces, or
  unnecessary internal diagnostics through publicly reachable health responses.
