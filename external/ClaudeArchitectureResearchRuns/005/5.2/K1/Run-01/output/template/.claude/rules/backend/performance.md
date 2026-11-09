---
paths:
  - "backend/**"
---
Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (backend/**)

# Performance and Runtime Standards

Caching technique: `caching` knowledge skill. Performance-change procedure: `development-workflow`.

## General

- Default: write clear, correct code first. Introduce specialized performance optimizations only for a concrete reason, and prefer measurement or profiling evidence for non-trivial optimizations.
- Default: compiled queries, `ValueTask<T>`, `ArrayPool<T>`/`MemoryPool<T>` or manual pooling, custom serialization optimizations, aggressive caching and raw SQL for performance are introduced only for a measured or clearly demonstrated need. Do not sacrifice maintainability for speculative micro-optimization.

## Async, cancellation and time

- Use async APIs for asynchronous I/O and never block them with `.Result`, `.Wait()` or similar sync-over-async patterns.
- Propagate `CancellationToken` through asynchronous operations when cancellation is meaningful. Do not add cancellation parameters to purely synchronous code without a use case.
- Default: application logic whose behavior depends on the current clock and needs deterministic tests uses `TimeProvider`. Stored timestamps and explicit dates are not clock dependencies; do not replace every `DateTime` or `DateTimeOffset` mechanically.

## Caching

- Default: caching is an optimization, not a default architecture requirement. Introduce it for a clear measured or reasoned need (expensive repeated work, high read volume, expensive remote calls) with acceptable staleness semantics, and choose the implementation by deployment, consistency and staleness requirements.
- Cache keys must uniquely represent the cached value and include every dimension that affects it, such as identifier, tenant, user, locale and query parameters. Never use global keys for user- or tenant-specific data.
- Every cache entry must have a lifetime or another explicit invalidation strategy.
- Invalidate or update cache entries only in a way that is consistent with successful underlying mutations. The cache must not become a second source of truth.
