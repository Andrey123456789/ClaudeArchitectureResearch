---
paths:
  - "backend/**"
---

> Level: 0 Core · Owns: performance, caching-semantics and external-call principles · Scope: backend · Loads: path

# Runtime Principles

## Performance

- **Default:** write clear, correct code first. Introduce a specialized optimization only for a concrete reason, and base non-trivial optimizations on measurement or profiling rather than assumption.
- **Default:** keep data access efficient — filter and project in the database when practical, avoid unnecessary round trips, over-fetching and N+1 patterns, and paginate potentially large result sets with deterministic ordering.
- **Default:** precompiled queries, `ValueTask`, buffer or object pooling, custom serialization, aggressive caching and raw SQL for performance are introduced only for a measured or clearly demonstrated need.
- **Must**, for a performance-motivated change: identify the actual bottleneck or cost, preserve observable behavior, use the simplest effective optimization, add or keep tests for the affected behavior, and benchmark or profile when the optimization is non-obvious or complex.

## Caching semantics

- **Default:** caching is an optimization, not a default architectural requirement. Introduce it for a clear measured or reasoned need (expensive repeated work, high read volume, expensive remote calls) with acceptable staleness, and choose the implementation from deployment and consistency requirements.
- **Must** give every cache entry a lifetime or another explicit invalidation strategy.
- **Must** build cache keys that uniquely represent the cached value, including every relevant user, tenant, locale and query dimension; never use global keys for user- or tenant-specific data.
- **Must** invalidate or update cache entries only consistently with successfully committed mutations; the cache never becomes a second source of truth.

## External calls

- **Must** bound the execution time of every external I/O call to suit the operation, and avoid overlapping timeout mechanisms whose combined behavior is unclear (distinguish per-attempt from total-operation timeouts).
- **Must** retry only when repeating the operation is safe; never automatically retry a state-changing operation without idempotency or another concrete duplicate-prevention mechanism.
- **Default:** respect `Retry-After` or equivalent rate-limit guidance from a dependency where appropriate; never retry indefinitely or aggressively.
- **Must** use a fallback only when its result is semantically acceptable; never hide a correctness failure behind a convenient default value.
- **Must not** classify caller cancellation as a transient dependency failure or convert it into repeated outbound attempts.
