---
paths:
  - "backend/**/*.cs"
---

> Path rule · Scope: backend · Owns runtime correctness and performance policy: async and cancellation, time, outbound calls, database access efficiency, caching semantics, and measured optimizations

# Runtime and Performance Rules

Layer placement of cache and HTTP technology: `.claude/rules/architecture.md`.
Performance-motivated change procedure: `development-workflow`.

## General Principle

Prefer clear, correct code first. Do not introduce specialized performance
optimizations without a concrete reason; for non-trivial optimizations, prefer
measurement or profiling evidence over assumptions.

## Async and Cancellation

- Use async APIs for asynchronous I/O. Do not block asynchronous code with
  `.Result`, `.Wait()`, or similar sync-over-async patterns.
- Propagate `CancellationToken` through asynchronous operations when
  cancellation is meaningful. Do not add cancellation parameters to purely
  synchronous code without a use case.

## Time

By default use `TimeProvider` for application logic whose behavior depends on
the current time and needs deterministic tests. Do not mechanically replace
every `DateTime` or `DateTimeOffset`; stored timestamps and explicit dates are
not clock dependencies.

## Outbound Calls

- Do not create and dispose a new `HttpClient` per request; use
  `IHttpClientFactory` or another appropriate long-lived client strategy.
- External I/O calls must have a bounded execution time appropriate to the
  operation. Avoid overlapping timeout mechanisms (for example per-attempt and
  total-operation timeouts) whose combined behavior is unclear.
- Retry only when repeating the operation is safe. Do not automatically retry
  state-changing operations without idempotency or another concrete
  duplicate-prevention mechanism.
- When a dependency supplies `Retry-After` or equivalent rate-limit guidance,
  respect it where appropriate; do not retry indefinitely or aggressively.
- Use fallback only when the fallback result is semantically acceptable; do not
  hide correctness failures behind convenient default values.
- Caller cancellation is not a transient dependency failure; do not retry it or
  convert it into repeated outbound attempts.

## Database Access

Keep database work efficient by default: filter and project in the database
when practical, avoid unnecessary round trips and loading significantly more
data than required, watch for N+1 query patterns, and paginate potentially
large result sets.

## Caching

- Caching is an optimization, not a default architectural requirement.
  Introduce it only for a clear measured or reasoned need — measured expensive
  repeated work, high read volume, expensive remote calls — with acceptable
  staleness semantics, and choose the implementation according to deployment,
  consistency, and staleness requirements. Do not cache merely because a value
  is read frequently.
- Every cache entry must have a lifetime or another explicit invalidation
  strategy.
- Cache keys must uniquely represent the cached value and include every
  relevant dimension (identifier, tenant, user when genuinely user-specific,
  locale, query/filter parameters). Avoid global keys for user- or
  tenant-specific data.
- Invalidate or update cache entries only consistently with successful
  underlying mutations; the cache must not become a second source of truth.

## Measured Optimizations

These techniques are valid, but by default introduce them only for a measured
or clearly demonstrated need: compiled queries, `ValueTask<T>`,
`ArrayPool<T>`/`MemoryPool<T>`, manual object pooling, custom serialization
optimizations, aggressive caching, and raw SQL for performance. Do not
sacrifice maintainability for speculative micro-optimization.

## Allocation-Sensitive Code

Prefer ordinary clear .NET code. For demonstrated allocation-heavy hot paths,
consider spans, pooling, source-generated serialization, or preallocated
buffers, and verify that the optimization materially improves the workload.
