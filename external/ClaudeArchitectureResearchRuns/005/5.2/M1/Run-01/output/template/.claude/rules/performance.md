---
paths:
  - "backend/**/*.cs"
---

> **Policy rule** · Owns: correctness-first optimization, async I/O and cancellation propagation, TimeProvider, HttpClient lifetime, efficient database access, when to cache, measured optimizations · Scope: backend · Loading: path (backend C# files)

# Performance Rules

## General Principle

Default: write clear, correct code first.

Do not introduce specialized performance optimizations without a concrete reason.
Base non-trivial optimizations on measurement or profiling evidence rather than
assumptions.

## Async and Cancellation

- Use async APIs for asynchronous I/O.
- Do not block asynchronous code with `.Result`, `.Wait()`, or similar sync-over-async patterns.
- Propagate `CancellationToken` through asynchronous operations when cancellation is meaningful.
- Do not add cancellation parameters to purely synchronous code without a use case.

## Time

Use `TimeProvider` for application logic whose behavior depends on the current time
and needs to be testable.

Do not mechanically replace every use of `DateTime` or `DateTimeOffset`.
Values representing stored timestamps or explicit dates are not clock dependencies.

## HTTP

Do not create and dispose a new `HttpClient` for every request.

Use `IHttpClientFactory` or another appropriate long-lived client strategy for
outbound HTTP communication.

Outbound-call rules (timeouts, retries, fallback): `backend-runtime.md`;
technique: the `httpclient-factory` skill.

## Database Access

Keep database work efficient by default:

- filter and project in the database when practical;
- avoid unnecessary round trips;
- avoid loading significantly more data than required;
- watch for N+1 query patterns;
- use pagination for potentially large result sets.

Query technique for the selected persistence technology: the persistence
knowledge facet (see `docs/capability-selection.md`).

## Caching

Caching is an optimization, not a default architectural requirement.

Introduce caching when there is a clear reason, such as:

- measured expensive repeated work;
- high read volume;
- expensive remote calls;
- acceptable staleness semantics.

Choose the cache implementation according to the deployment and consistency
requirements.

Do not introduce caching merely because a value is read frequently.

Rules for cache keys, lifetimes, and invalidation: `backend-runtime.md`.

## Measured Optimizations

Default: introduce the following valid techniques only when a measured or clearly
demonstrated need exists:

- compiled queries;
- `ValueTask<T>`;
- `ArrayPool<T>` / `MemoryPool<T>`;
- manual object pooling;
- custom serialization optimizations;
- aggressive caching;
- raw SQL for performance.

Do not sacrifice maintainability for speculative micro-optimization.

## Allocation-Sensitive Code

Prefer ordinary clear .NET code by default.

For demonstrated allocation-heavy hot paths, consider appropriate tools such as
spans, pooling, source-generated serialization, or preallocated buffers.

Verify that the optimization materially improves the relevant workload.

## Performance Changes

The procedure for a performance-motivated change is owned by
`development-workflow` → Change-Specific Obligations.
