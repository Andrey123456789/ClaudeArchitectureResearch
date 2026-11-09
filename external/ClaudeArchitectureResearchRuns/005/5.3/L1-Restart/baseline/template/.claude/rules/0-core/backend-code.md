---
paths:
  - "backend/**/*"
---

> Level: 0-core · Owns: backend runtime conventions — performance, async/cancellation, time, outbound calls, caching, configuration, dependency injection, logging style, C# conventions · Scope: backend · Loading: path

# Backend Code Rules

## Clarity and performance

- Default: write clear, correct code first; add specialized optimizations only for a concrete reason, preferring measurement or profiling evidence for non-trivial ones.
- Default: introduce compiled queries, `ValueTask`, pooling, custom serialization, aggressive caching, or raw SQL for performance only for a measured or clearly demonstrated need.
- Default: keep database work efficient — filter and project in the database when practical, avoid unnecessary round trips, over-fetching, and N+1 patterns, and paginate potentially large result sets.

## Async, cancellation, time

- Use async APIs for asynchronous I/O and never block them with `.Result`, `.Wait()`, or similar sync-over-async patterns.
- Propagate `CancellationToken` through asynchronous operations when cancellation is meaningful; do not add cancellation parameters to purely synchronous code without a use case.
- Default: use `TimeProvider` for logic that depends on the current clock and needs deterministic tests; do not mechanically replace stored or explicit timestamps.

## Outbound dependencies

- Never create and dispose a new `HttpClient` per request; use `IHttpClientFactory` or another appropriate long-lived strategy.
- External I/O calls must have a bounded execution time appropriate to the operation; avoid overlapping timeout mechanisms whose combined behavior is unclear.
- Retry only when repeating the operation is safe; never automatically retry state-changing operations without idempotency or another concrete duplicate-prevention mechanism.
- Default: respect `Retry-After` or equivalent rate-limit guidance where appropriate; never retry indefinitely or aggressively.
- Use fallback only when the fallback result is semantically acceptable; never hide correctness failures behind convenient default values.
- Caller cancellation is not a transient dependency failure: never retry it or convert it into repeated outbound attempts.

## Caching

- Default: caching is not a default architectural requirement; introduce it only for a clear measured or reasoned need and choose the implementation by deployment, consistency, and staleness requirements.
- Cache keys must uniquely represent the cached value and include the relevant user, tenant, locale, and query dimensions; never use global keys for user- or tenant-specific data.
- Every cache entry must have a lifetime or another explicit invalidation strategy.
- Invalidate or update cache entries only consistently with successful underlying mutations; the cache is never a second source of truth.

## Configuration, dependency injection, logging

- Default: use strongly typed options for structured service configuration, validated at startup when missing or invalid values prevent correct or secure operation; avoid scattering string-based `IConfiguration` lookups through services.
- Default: use constructor injection for required dependencies; avoid service-locator and property-injection patterns.
- Respect service lifetimes: never capture a shorter-lived dependency inside a longer-lived service.
- Default: log through `ILogger<T>` with structured message templates and stable property names; avoid string interpolation that turns structured values into opaque text.

## C# conventions

- Default: follow the repository's conventions and `.editorconfig`; use modern C# when it improves clarity, but do not mechanically modernize working code.
- Default: for new code prefer file-scoped namespaces when consistent with the project, keep one primary top-level type per matching file, and use the `Async` suffix for `Task`/`ValueTask`-returning methods unless an existing or framework contract makes that inappropriate.
- Do not perform style-only rewrites outside the requested change unless explicitly asked.
