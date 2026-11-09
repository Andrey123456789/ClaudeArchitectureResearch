---
paths:
  - "backend/**/*"
---

> Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (frontmatter paths)

# Runtime Behavior and Performance Standard

## Optimization

- Default: clear, correct code first; no specialized optimization without a concrete reason, and measurement or profiling evidence for non-trivial optimizations.
- Default: compiled queries, `ValueTask`, pooling, custom serialization, aggressive caching, and raw SQL for performance are introduced only for a measured or clearly demonstrated need.

## Async, cancellation, and time

- Use async APIs for asynchronous I/O; never block them with `.Result`, `.Wait()`, or similar sync-over-async patterns.
- Propagate `CancellationToken` through asynchronous operations when cancellation is meaningful; do not add cancellation parameters to purely synchronous code without a use case.
- Default: `TimeProvider` for logic that depends on the current clock and needs deterministic tests; do not mechanically replace explicit or stored timestamps.

## Database access

- Default: filter and project in the database when practical, avoid unnecessary round trips, over-fetching, and N+1 patterns, and paginate potentially large result sets.

## Outbound calls

- Never create and dispose a new `HttpClient` per request; use `IHttpClientFactory` or another appropriate long-lived client strategy.
- External I/O calls must have a bounded execution time appropriate to the operation; avoid overlapping timeout mechanisms whose combined behavior is unclear.
- Retry only when repeating the operation is safe; never automatically retry state-changing operations without idempotency or another concrete safety mechanism.
- Default: respect `Retry-After` or equivalent rate-limit guidance where appropriate; never retry indefinitely or aggressively.
- Use a fallback only when its result is semantically acceptable; never hide correctness failures behind convenient default values.
- Caller cancellation is not a transient failure: never retry it or convert it into repeated outbound attempts.

## Caching

- Default: no caching without a clear measured or reasoned need; choose the implementation according to deployment, consistency, and staleness requirements.
- Cache keys must uniquely represent the cached value, including relevant user, tenant, and context dimensions; no global keys for user- or tenant-specific data.
- Every cache entry must have a lifetime or another explicit invalidation strategy.
- Invalidate or update cache entries only consistently with successful underlying mutations; the cache must never become a second source of truth.

Technique: `httpclient-factory`, `caching`, `modern-csharp`. Performance-change procedure: `development-workflow`.
