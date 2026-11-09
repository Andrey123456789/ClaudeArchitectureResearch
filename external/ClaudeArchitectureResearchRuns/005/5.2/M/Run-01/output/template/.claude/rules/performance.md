---
paths:
  - "backend/**/*.cs"
---

> Path-scoped rule. Owns: optimization discipline, async I/O, cancellation propagation, the time abstraction, HttpClient lifetime, database-access efficiency, caching semantics · Scope: backend · Loads: when backend C# files are in context · Depends on: CLAUDE.md

# Performance Rules

Performance-motivated changes follow `development-workflow`. Technique:
`ef-core`, `caching`, and `httpclient-factory` skills.

## General Principle

- Default: clear, correct code first. Do not introduce specialized performance
  optimizations without a concrete reason; prefer measurement or profiling
  evidence over assumptions for non-trivial optimizations.

## Async and Cancellation

- Use async APIs for asynchronous I/O; do not block asynchronous code with
  `.Result`, `.Wait()`, or similar sync-over-async patterns.
- Propagate `CancellationToken` through asynchronous operations when
  cancellation is meaningful; do not add cancellation parameters to purely
  synchronous code without a use case.

## Time

- Default: use `TimeProvider` for application logic whose behavior depends on
  the current time and must be deterministically testable. Do not mechanically
  replace every `DateTime` or `DateTimeOffset`: stored timestamps and explicit
  dates are not clock dependencies.

## HTTP Clients

- Do not create and dispose a new `HttpClient` per request; use
  `IHttpClientFactory` or another appropriate long-lived client strategy.

## Database Access

- Default: filter and project in the database when practical, avoid
  unnecessary round trips, over-fetching, and N+1 query patterns, and paginate
  potentially large result sets.

## Caching

- Default: caching is an optimization, not an architectural requirement.
  Introduce it only for a clear measured or reasoned need — measured expensive
  repeated work, high read volume, expensive remote calls — with acceptable
  staleness semantics, and choose the implementation by deployment,
  consistency, and staleness requirements. Frequent reads alone are not a
  reason.
- Cache keys must uniquely represent the cached value and include every
  dimension that affects it (identifier, tenant, user when user-specific,
  locale, relevant query parameters); do not use global keys for user- or
  tenant-specific data.
- Every cache entry must have a lifetime or another explicit invalidation
  strategy.
- Invalidate or update cache entries only consistently with successful
  underlying mutations; the cache must not become a second source of truth.

## Measured Optimizations

- Default: introduce `EF.CompileQuery` / `EF.CompileAsyncQuery`, `ValueTask<T>`,
  `ArrayPool<T>` / `MemoryPool<T>`, manual object pooling, custom serialization
  optimizations, aggressive caching, or raw SQL for performance only for a
  measured or clearly demonstrated need. Do not sacrifice maintainability for
  speculative micro-optimization.

## Allocation-Sensitive Code

- Prefer ordinary clear .NET code. For demonstrated allocation-heavy hot paths,
  consider spans, pooling, source-generated serialization, or preallocated
  buffers, and verify that the optimization materially improves the workload.
