---
paths:
  - "backend/**"
---
Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (backend/**)

# HTTP API Standards

Status-code technique and examples: `http-api` knowledge skill. Versioning technique: `api-versioning`. Documentation technique: `swagger`. Health-check technique: `health-check`.

## Layer ownership

- HTTP status codes and transport response semantics belong to the Api layer. Application and Domain must not return `IActionResult` or ASP.NET Core status codes.

## Status semantics

- Choose 200, 201, 202 or 204 by the actual HTTP semantics of the outcome. Do not return 200 for every outcome, 201 merely because a row was inserted internally, or 202 for work that has already completed.
- Default: a successful collection query with zero matches returns 200 with an empty collection, not 404.
- Use 401 when authentication is missing or failed and 403 when an authenticated principal is not permitted. Returning 404 to hide a protected resource requires a deliberate and consistent security policy.
- Use 409 for a valid request that conflicts with the current state, and 412 when an explicit HTTP precondition such as `If-Match` fails.

## Versioning

- Do not introduce API versioning merely because an API exists. Add it when published compatibility or coexisting client generations create a concrete need.
- Once an API version is relied on by external clients, do not break it silently. A breaking contract change requires a new version or another explicitly approved compatibility strategy.
- Default: when explicit versioning is required, use one strategy consistently, with URL-segment versioning unless project requirements justify another strategy.

## API documentation

- Swagger/OpenAPI metadata must describe the API that actually runs: routes, important response statuses (including those produced by binding, validation, authentication, authorization, rate limiting and centralized exception handling), schemas and authentication behavior. Do not document speculative responses.
- Default: configure Swagger UI environment-aware. It is enabled in Development, and enabling it in another environment needs an explicit deployment requirement.

## Health checks

- Health checks must stay cheap and deterministic. They must not become business workflows or perform expensive or mutating database work.
- Liveness avoids external dependencies whose outage could cause restart loops. Readiness may depend on the capabilities required to serve traffic and reflects startup and dependency availability.
- Publicly reachable health responses must not expose secrets, credentials, connection details, stack traces or unnecessary internal diagnostics.
