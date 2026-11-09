---
paths:
  - "backend/**"
---

> Level: 1 Architecture · Owns: HTTP entry-point responsibilities, response semantics, API contracts and evolution, operational endpoints · Scope: backend · Loads: path

# Entry Points

## Responsibilities

- **Must** keep HTTP entry points (controllers) thin: bind and validate HTTP input, invoke Application services, and translate application outcomes into HTTP responses.
- **Must not** put business logic in entry points, access the persistence context or concrete repositories from them, consume Infrastructure implementation types directly, or construct infrastructure services manually.
- **Must** keep HTTP status codes and transport response semantics in the Api layer; Application and Domain never return transport result types or HTTP status codes.

## Response semantics

- **Must** choose success statuses by actual HTTP semantics: never `200` for every outcome; `201 Created` only when the operation created an API resource (with `Location` when a stable URI exists) — not merely because a row was inserted; `202 Accepted` only for accepted-but-incomplete work, never for work already completed; `204 No Content` without a body.
- **Default:** a successful collection query with zero matches returns `200` with an empty collection, not `404`.
- **Must** return `401` when authentication is missing or failed and `403` when an authenticated principal is not permitted. Returning `404` to hide protected resources is allowed only as a deliberate, consistently applied security policy.
- **Must** return `409` for a valid request that conflicts with current state, and `412` when an explicit HTTP precondition such as `If-Match` fails.

Detailed status reference (304, 400, 406, 415, 422, 428, 429, 5xx, idempotency, ETags): `http-api` skill.

## Contracts and documentation

- **Must not** duplicate equivalent DTOs across Api and Application merely to create layer-shaped types; introduce transport-specific request/response contracts when separating them from Application models gives a concrete boundary benefit.
- **Must** keep published API documentation true to the API that actually runs — routes, important response statuses (including those produced by binding, validation, authentication/authorization, rate limiting and central error handling), schemas and authentication behavior. Never document speculative responses.

## API evolution

- **Must not** introduce API versioning merely because an API exists; add it when published compatibility or coexisting client generations create a concrete need (adopting versioning is a Reserved decision).
- **Must** avoid silent breaking changes once a version is relied on by external clients: a breaking contract change requires a new version or another explicitly approved compatibility strategy.
- **Default:** when explicit versioning is required, use one strategy consistently; URL-segment versioning (`/api/v1/...`) unless project requirements justify header or query versioning.
- **Must not** create separate Domain or persistence models merely because the external API has multiple versions; isolate version-specific transport contracts at the Api boundary when practical.
- **Must**, when deprecating an externally consumed API version: mark the deprecation in the versioning metadata, document the replacement, communicate a realistic migration and removal timeline, and keep the old version working for the promised support period. Never remove it without considering the published support contract.

## Operational endpoints

- **Must** keep health checks cheap and deterministic; they never become business workflows or perform expensive or data-mutating database work.
- **Must** keep liveness free of external dependencies whose outage could cause restart loops; readiness may depend on capabilities required to serve traffic and reflects startup and dependency availability (unhealthy until required startup work completes).
- **Must not** expose secrets, credentials, connection details, stack traces or unnecessary internal diagnostics through publicly reachable health responses.
