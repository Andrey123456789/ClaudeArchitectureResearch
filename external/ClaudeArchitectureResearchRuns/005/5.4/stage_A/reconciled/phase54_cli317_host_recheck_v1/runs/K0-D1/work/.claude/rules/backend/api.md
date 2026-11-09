---
paths:
  - "backend/**/*.cs"
---

> Kind: STD | Scope: backend | Owner: HTTP API contract — status semantics, error contract format, versioning, OpenAPI/Swagger | Loading: path-scoped

# HTTP API Standard

Controllers as entry point: D-01. Swagger UI: D-07. API versioning: D-15.

See also: `rules/backend/error-handling.md` (exceptions and validation).

## HTTP semantics

- HTTP status codes and transport response semantics belong to the API layer; Application and Domain must not return `IActionResult`, `ProblemDetails` or ASP.NET Core status codes.
- Default: `ProblemDetails` for non-validation HTTP failures and `ValidationProblemDetails` for request validation; keep machine-readable error contracts stable and safe.
- Choose 200/201/202/204 by actual HTTP semantics: do not return 200 for every outcome, 201 merely because a row was inserted internally, or 202 for work that already completed. Keep status behavior consistent across similar endpoints.
- Default: a successful collection query with zero matches returns 200 with an empty collection, not 404.
- Use 401 when authentication is missing or failed and 403 when an authenticated principal is not permitted. Returning 404 to hide a protected resource must be a deliberate, consistent security policy.
- Use 409 for a valid request that conflicts with current state, and 412 when an explicit HTTP precondition such as `If-Match` fails.

## Versioning

- Do not introduce API versioning merely because an API exists; add it only when published compatibility or coexisting client generations create a concrete need.
- Once an API version is relied on by external clients, it must not change incompatibly without compatibility treatment: a breaking contract change requires a new version or another explicitly approved compatibility strategy.
- Default: when explicit versioning is required, use one strategy consistently — URL-segment versioning unless project requirements justify another.
- Do not create separate Domain or persistence models merely because the external API has multiple versions; isolate version-specific transport contracts at the API boundary when practical.

## OpenAPI and Swagger

- Swagger/OpenAPI metadata must describe the API that actually runs — routes, important response statuses, schemas and authentication behavior — and must not document speculative responses.
- Default: Swagger UI is enabled in Development and exposed in other environments only when deployment requirements explicitly justify it.
