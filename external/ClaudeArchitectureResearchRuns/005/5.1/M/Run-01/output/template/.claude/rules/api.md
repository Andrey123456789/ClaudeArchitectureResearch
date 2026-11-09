---
paths:
  - "backend/**/*.cs"
---

> Owns: HTTP response semantics, public error contracts, Swagger accuracy, API versioning and deprecation, health-check semantics | Scope: backend | Loads: path

# HTTP API Rules

Controller responsibilities: `architecture.md`. Exception/outcome handling:
`error-handling.md`. Full status-code reference and examples: `http-api` skill.

## HTTP Semantics

- HTTP status codes and transport response semantics belong to the Api layer;
  Application and Domain must not return `IActionResult` or ASP.NET Core status
  codes.
- Choose `200`/`201`/`202`/`204` by actual HTTP semantics: do not return `200`
  for every outcome, `201` merely because a row was inserted internally, or
  `202` for work already completed.
- A successful collection query with zero matches returns `200` with an empty
  collection by default, not `404`.
- Use `401` when authentication is missing or failed and `403` when an
  authenticated principal is not permitted. Returning `404` to hide a protected
  resource must be a deliberate, consistent security policy.
- Use `409` for a valid request that conflicts with current state; use `412`
  when an explicit HTTP precondition such as `If-Match` fails.

## Error Contracts

- By default, use `ProblemDetails` for non-validation HTTP failures and
  `ValidationProblemDetails` for request validation; keep machine-readable
  contracts stable and safe, never relying on human-readable exception messages.
- Public API errors must not expose stack traces, SQL, connection strings,
  internal paths, secret values, or sensitive exception details.

## Swagger

- Swagger/OpenAPI metadata must describe the API that actually runs — routes,
  important response statuses (considering the whole pipeline), schemas, and
  authentication behavior. Do not document speculative responses.
- Where Swagger UI is exposed (Development by default) is decided in
  `docs/technology-stack.md`.

## API Versioning

- Do not introduce API versioning merely because an API exists; it is warranted
  only by a real compatibility need such as published contracts or coexisting
  client generations (adopting it is Reserved: `CLAUDE.md`).
- Once a version is relied on by external clients, avoid silent breaking
  changes: a breaking contract change requires a new version or another
  explicitly approved compatibility strategy.
- When explicit versioning is required, use one strategy consistently;
  URL-segment versioning is the default unless requirements justify another.
- Do not create separate Domain or persistence models merely because the API has
  multiple versions; isolate version-specific transport contracts at the Api
  boundary when practical.
- When deprecating an externally consumed version: mark it deprecated in
  versioning metadata, document the replacement, communicate a realistic
  migration/removal timeline, and keep the old version working for the promised
  support period. Never remove it without considering the published support
  contract.

## Health Checks

- Health checks must stay cheap and deterministic; they must not become business
  workflows or perform expensive or mutating database work.
- Liveness avoids external dependencies that could cause restart loops by
  default; readiness may depend on capabilities required to serve traffic and
  reflects startup and dependency availability.
- Publicly reachable health responses must not expose secrets, credentials,
  connection details, stack traces, or unnecessary internal diagnostics.
