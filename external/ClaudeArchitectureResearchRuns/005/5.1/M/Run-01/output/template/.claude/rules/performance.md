---
paths:
  - "backend/**/*.cs"
---

> Owns: async/cancellation, time abstraction, HttpClient lifetime, database efficiency, caching semantics, measured optimization, performance-change procedure | Scope: backend | Loads: path

# Performance Rules

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

By default, use `TimeProvider` for application logic whose behavior depends on
the current time and must be deterministically testable. Do not mechanically
replace every `DateTime`/`DateTimeOffset`: stored timestamps and explicit dates
are not clock dependencies.

## Outbound HTTP

Do not create and dispose a new `HttpClient` per request; use
`IHttpClientFactory` or another appropriate long-lived client strategy.
Timeout/retry semantics: `error-handling.md`. Technique: `httpclient-factory`.

## Database Access

By default: filter and project in the database when practical, avoid
unnecessary round trips and over-fetching, watch for N+1 query patterns, and
paginate potentially large result sets. Technique: `ef-core`.

## Caching

- Caching is an optimization, not a default architectural requirement. Introduce
  it only for a clear measured or reasoned need (expensive repeated work, high
  read volume, expensive remote calls) with acceptable staleness semantics, and
  choose the implementation from deployment and consistency requirements. Do not
  cache merely because a value is read frequently.
- Cache keys must uniquely represent the cached value and include every relevant
  dimension (identifier, tenant, user when user-specific, locale, query
  parameters); never use global keys for user- or tenant-specific data.
- Every cache entry must have a lifetime or another explicit invalidation
  strategy.
- Invalidate or update entries only consistently with successful underlying
  mutations; the cache must never become a second source of truth.

Cache boundary placement: `architecture.md`. Technique: `caching`.

## Measured Optimizations

By default, introduce these only for a measured or clearly demonstrated need:
`EF.CompileQuery`/`EF.CompileAsyncQuery`, `ValueTask<T>`,
`ArrayPool<T>`/`MemoryPool<T>`, manual object pooling, custom serialization
optimizations, aggressive caching, and raw SQL for performance. For demonstrated
allocation-heavy hot paths, spans, pooling, source-generated serialization, or
preallocated buffers may be appropriate; verify they materially help. Do not
sacrifice maintainability for speculative micro-optimization.

## Performance Changes

A performance-motivated change must:

1. identify the actual bottleneck or cost;
2. preserve observable behavior;
3. use the simplest optimization that addresses the problem;
4. add or preserve tests for behavior affected by the optimization;
5. benchmark or profile when the optimization is non-obvious or complex.
