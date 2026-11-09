---
paths:
  - "backend/**/*.cs"
---

> Level: 0 Core · Owns: technology-neutral runtime principles (optimization, data access efficiency, caching, external calls, cancellation, health checks) · Scope: backend · Loads: path rule · Depends on: CLAUDE.md

# Runtime Principles

Language and runtime bindings (async, cancellation tokens, time, outbound HTTP clients) live in `.claude/rules/2-technology/`. Technique: `caching`, `httpclient-factory`, `health-check` skills. Steps for performance-motivated changes: `development-workflow`.

## Optimization

- Prefer clear, correct code first. Do not introduce specialized optimizations without a concrete reason, and prefer measurement or profiling evidence over assumptions for non-trivial optimization (default).
- Introduce advanced techniques — precompiled queries, specialized async return types, pooling, custom serialization, aggressive caching, raw SQL for performance — only for a measured or clearly demonstrated need (default).
- Keep database access efficient by default: filter and project in the database when practical, avoid unnecessary round trips, over-fetching, and N+1 patterns, and paginate potentially large result sets (default).

## Caching

- Caching is not a default architecture requirement. Introduce it only for a clear measured or reasoned need, and choose the implementation by deployment, consistency, and staleness requirements (default).
- Cache keys must uniquely represent the cached value and include every relevant user, tenant, and context dimension; avoid global keys for user- or tenant-specific data.
- Invalidate or update cache entries only in a way consistent with successful underlying mutations; the cache must not become a second source of truth. The strategy must account for the transaction isolation level, concurrent reads and refills, commit and rollback order, a crash between commit and invalidation, retries, and the staleness the application documents as tolerated. Invalidating after commit is not by itself atomic across the database and the cache. Invalidating before the mutation is not ruled out when correctness for those semantics is shown.
- Every cache entry must have a lifetime or another explicit invalidation strategy.

## External calls

- External I/O calls must have a bounded execution time appropriate to the operation; avoid overlapping timeout mechanisms whose combined behavior is unclear.
- Retry only when repeating the operation is safe; never automatically retry state-changing operations without idempotency or another concrete duplicate-safety mechanism.
- When a dependency supplies `Retry-After` or equivalent rate-limit guidance, respect it where appropriate; do not retry indefinitely or aggressively (default).
- Use a fallback only when the fallback result is semantically acceptable; never hide correctness failures behind convenient default values.

## Cancellation

- Caller cancellation is not a transient dependency failure: do not classify it as one or convert it into repeated outbound attempts.
- Normal client-request cancellation is not a server failure: do not map it to a generic 500 response or log it as an unhandled application failure.

## Health checks

- Health checks must stay cheap and deterministic; they must not become business workflows or perform expensive or mutating database work.
- Liveness and readiness must keep distinct dependency semantics: liveness avoids external dependencies that could cause restart loops (default); readiness may depend on the capabilities required to serve traffic and reflects startup and dependency availability.
