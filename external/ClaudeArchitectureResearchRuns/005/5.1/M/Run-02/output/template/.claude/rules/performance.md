---
paths:
  - "backend/**/*.cs"
---

> Owner: optimization discipline, async I/O and cancellation propagation, time abstraction, outbound HttpClient lifetime, database access efficiency, caching correctness | Scope: backend | Loads: path (backend C#); read explicitly by `code-review` | Enforced: `code-review` checks

# Performance Rules

Technique: `ef-core`, `caching`, `httpclient-factory`, and `modern-csharp`
skills.

## General Principle

- Default: prefer clear, correct code first. Do not introduce specialized
  optimizations without a concrete reason, and prefer measurement or profiling
  evidence for non-trivial optimization.
- Default: introduce compiled EF queries, `ValueTask<T>`, `ArrayPool<T>` /
  `MemoryPool<T>`, manual object pooling, custom serialization optimizations,
  aggressive caching, and raw SQL for performance only for a measured or clearly
  demonstrated need.

## Async and Cancellation

- Use async APIs for asynchronous I/O, and do not block them with `.Result`,
  `.Wait()`, or similar sync-over-async patterns.
- Propagate `CancellationToken` through asynchronous operations when
  cancellation is meaningful; do not add cancellation parameters to purely
  synchronous code without a use case.

## Time

- Default: use `TimeProvider` for application logic whose behavior depends on the
  current clock and needs deterministic tests; do not mechanically replace
  stored timestamps or explicit dates, which are not clock dependencies.

## Outbound HTTP

- Do not create and dispose a new `HttpClient` per request; use
  `IHttpClientFactory` or another appropriate long-lived client strategy.

## Database Access

- Default: filter and project in the database when practical, avoid unnecessary
  round trips, over-fetching, and N+1 query patterns, and paginate potentially
  large result sets.

## Caching

- Default: caching is an optimization, not an architecture requirement;
  introduce it only for a clear measured or reasoned need, and choose the
  implementation from deployment, consistency, and staleness requirements.
- Cache keys must uniquely represent the cached value and include the relevant
  user, tenant, and context dimensions; do not use global keys for user- or
  tenant-specific data.
- Every cache entry must have a lifetime or another explicit invalidation
  strategy.
- Invalidate or update cache entries only consistently with successful
  underlying mutations; do not make cache state a second source of truth.

## Performance Changes

A performance-motivated change must identify the actual bottleneck, preserve
observable behavior, use the simplest effective optimization, add or keep tests
for the affected behavior, and benchmark or profile non-obvious or complex
optimizations.
