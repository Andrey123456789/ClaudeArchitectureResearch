---
paths:
  - "backend/**/*.cs"
---

> Owns: optimization discipline, async and cancellation, time abstraction, HttpClient lifetime, database efficiency, caching semantics | Scope: backend | Loads: path-scoped (backend C# files)

# Performance Rules

Procedure for performance-motivated changes: `development-workflow`.

## General Principle

Prefer clear, correct code first. Do not introduce specialized performance
optimizations without a concrete reason; for non-trivial optimizations, prefer
measurement or profiling evidence over assumptions.

## Async and Cancellation

- Use async APIs for asynchronous I/O and never block them with `.Result`,
  `.Wait()`, or similar sync-over-async patterns.
- Propagate `CancellationToken` through asynchronous operations when
  cancellation is meaningful; do not add cancellation parameters to purely
  synchronous code without a use case.

## Time

Use `TimeProvider` for application logic whose behavior depends on the current
clock and needs deterministic testing. Do not mechanically replace every
`DateTime` or `DateTimeOffset`: stored timestamps and explicit dates are not
clock dependencies.

## Outbound HTTP

Do not create and dispose a new `HttpClient` per request; use
`IHttpClientFactory` or another appropriate long-lived client strategy.
Timeouts and retries: `error-handling.md`. Client technique:
`httpclient-factory` skill.

## Database Access

Keep database work efficient by default: filter and project in the database
when practical, avoid unnecessary round trips, over-fetching, and N+1 query
patterns, and paginate potentially large result sets. EF Core technique:
`ef-core` skill.

## Caching

- Caching is an optimization, not a default architectural requirement.
  Introduce it only for a clear measured or reasoned need (expensive repeated
  work, high read volume, expensive remote calls, acceptable staleness), and
  choose the implementation from the deployment, consistency, and staleness
  requirements — not merely because a value is read frequently.
- Cache keys must uniquely represent the cached value and include every
  relevant dimension (identifier, tenant, user, locale, query parameters); do
  not use global keys for user- or tenant-specific data.
- Invalidate or update cache entries only in a way consistent with successful
  underlying mutations; the cache must not become a second source of truth.
- Every cache entry must have a lifetime or another explicit invalidation
  strategy.

## Measured Optimizations

By default, introduce these only for a measured or clearly demonstrated need:
`EF.CompileQuery`/`EF.CompileAsyncQuery`, `ValueTask<T>`,
`ArrayPool<T>`/`MemoryPool<T>`, manual object pooling, custom serialization
optimizations, aggressive caching, and raw SQL for performance. Do not sacrifice
maintainability for speculative micro-optimization.

For demonstrated allocation-heavy hot paths, spans, pooling, source-generated
serialization, or preallocated buffers are appropriate tools; verify that the
optimization materially improves the relevant workload.
