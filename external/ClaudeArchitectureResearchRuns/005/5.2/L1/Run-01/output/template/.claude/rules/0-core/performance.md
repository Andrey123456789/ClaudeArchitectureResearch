---
paths:
  - "backend/**/*"
---
> Level: 0-core | Owns: correctness-first performance, async, time, data-access efficiency, caching semantics | Scope: backend | Loads: path (backend files)

# Performance and Caching Rules

## General principle

Default to clear, correct code first. Do not introduce specialized performance
optimizations without a concrete reason; for non-trivial optimizations, prefer
measurement or profiling evidence over assumptions. Do not sacrifice
maintainability for speculative micro-optimization.

## Async and cancellation

- Use async APIs for asynchronous I/O. Do not block asynchronous code with
  `.Result`, `.Wait()`, or similar sync-over-async patterns.
- Propagate `CancellationToken` through asynchronous operations when
  cancellation is meaningful; do not add cancellation parameters to purely
  synchronous code without a use case.

## Time

Default: use `TimeProvider` for application logic whose behavior depends on the
current time and needs deterministic tests. Do not mechanically replace every
`DateTime`/`DateTimeOffset`; stored timestamps and explicit dates are not clock
dependencies.

## Data access

Default: keep database work efficient — filter and project in the database when
practical, avoid unnecessary round trips and loading significantly more data
than required, watch for N+1 query patterns, and paginate potentially large
result sets.

## Measured optimizations

Default: introduce compiled queries, `ValueTask<T>`, `ArrayPool<T>`/`MemoryPool<T>`
or manual pooling, custom serialization optimizations, aggressive caching, and
raw SQL for performance only for a measured or clearly demonstrated need. For a
demonstrated allocation-heavy hot path, consider spans, pooling, source-generated
serialization, or preallocated buffers, and verify the improvement.

## Caching

- Default: caching is an optimization, not an architectural requirement.
  Introduce it only for a clear measured or reasoned need (expensive repeated
  work, high read volume, expensive remote calls) with acceptable staleness
  semantics, and choose the implementation by deployment, consistency, and
  staleness requirements — not merely because a value is read frequently.
- Every cache entry must have a lifetime or another explicit invalidation
  strategy.
- Cache keys must uniquely represent the cached value and include every
  relevant dimension (tenant, user when user-specific, locale, filters); avoid
  global keys for user- or tenant-specific data.
- Invalidate or update cache entries only consistently with successful
  underlying mutations; the cache must not become a second source of truth.

Performance-change procedure: `develop`. Caching technique: `caching`.
