---
paths:
  - "backend/**"
---
<!-- Kind: STD | Scope: backend | Owns: HTTP semantics ownership, status codes, API versioning, OpenAPI accuracy | Loads: path-scoped (backend/**) -->
# Backend HTTP API Standards

## HTTP Semantics Ownership

- HTTP status codes and transport response semantics **must** belong to the Api layer; Application and Domain **must not** return `IActionResult` or ASP.NET Core status codes.

## Status Codes

- Success statuses **must** follow actual HTTP semantics — `200`, `201`, `202` or `204` by outcome: **never** `200` for every outcome, `201` merely because a row was inserted internally, or `202` for work already completed.
- **Default:** a successful collection query with zero matches returns `200` with an empty collection, not `404`.
- **Must** use `401` when authentication is missing or failed and `403` when an authenticated principal is not permitted; returning `404` to hide a protected resource requires a deliberate, consistent security policy.
- **Must** use `409` for a valid request that conflicts with current state and `412` when an explicit HTTP precondition such as `If-Match` fails.

## API Versioning

- **Must not** introduce API versioning merely because an API exists; add it only when published compatibility or coexistence of client generations creates a concrete need (adoption: CLAUDE.md § Decisions).
- Once external clients rely on an API version, breaking contract changes **must not** be made silently: a breaking change requires a new version or another explicitly approved compatibility strategy. Compile success does not establish compatibility.
- **Default:** when explicit versioning is required, one strategy used consistently — URL-segment versioning unless project requirements justify header or query versioning.

## OpenAPI Accuracy

- Swagger/OpenAPI metadata **must** describe the API that actually runs — routes, important response statuses, schemas and authentication behavior — and **must not** document speculative responses.

Workflow: deprecating an externally consumed API version — `architecture-decision` § API Version Deprecation.
Technique: `http-api`, `api-versioning`, `swagger` knowledge skills.
