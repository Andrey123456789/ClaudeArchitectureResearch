---
paths:
  - "backend/**/*"
---

> Level: 0-core · Owns: HTTP response semantics, error contracts, exception and cancellation handling, API versioning policy, health endpoints · Scope: backend · Loading: path

# HTTP API Rules

## Responses

- Default: use problem details (RFC 9457) for non-validation HTTP failures and validation problem details for request validation; keep machine-readable error contracts stable and safe.
- Choose 200/201/202/204 by actual HTTP semantics: never 200 for every outcome, 201 merely because a row was inserted internally, or 202 for work that already completed.
- Default: a successful collection query with zero matches returns 200 with an empty collection, not 404.
- Use 401 when authentication is missing or failed and 403 when an authenticated principal is not permitted; returning 404 to hide protected resources requires a deliberate, consistent security policy.
- Use 409 for a valid request that conflicts with current state and 412 when an explicit HTTP precondition such as `If-Match` fails.

Full status-code reference: `http-api` skill.

## Failures

- Default: unexpected failures propagate to centralized exception handling at the HTTP boundary; avoid repetitive catch/log/rethrow blocks.
- Never expose stack traces, SQL, connection strings, internal paths, secret values, or sensitive exception details in public API errors.
- Do not establish business exceptions as the default architecture, and do not throw and catch exceptions to jump between normal expected branches.
- Log an unexpected exception once, at the boundary that handles it — not again in repository, use-case unit, entry point, and global handler.
- Normal client-request cancellation is not a server failure: never map it to a generic 500 or log it as an unhandled application error.

## Versioning

- Do not introduce API versioning merely because an API exists; add it when published compatibility or coexisting client generations create a concrete need.
- Once external clients rely on an API version, avoid silent breaking changes: a breaking contract change requires a new version or another explicitly approved compatibility strategy.
- Default: when explicit versioning is required, use one strategy consistently — URL-segment versioning unless project requirements justify another.

## Health checks

- Health checks stay cheap and deterministic: never full business workflows, expensive queries, or mutating database work.
- Liveness avoids external dependencies whose outage could cause restart loops; readiness may depend on capabilities required to serve traffic and reflects startup and dependency availability.
- Publicly reachable health responses must not expose secrets, credentials, connection details, stack traces, or unnecessary internal diagnostics.
