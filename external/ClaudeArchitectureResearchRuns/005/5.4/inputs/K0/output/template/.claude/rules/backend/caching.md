---
paths:
  - "backend/**/*.cs"
---

> Kind: STD | Scope: backend | Owner: caching — need, boundaries, keys, lifetime, invalidation | Loading: path-scoped

# Caching Standard

Distributed caching is Reserved (CLAUDE.md § Decisions).

- Default: caching is an optimization, not an architecture requirement. Introduce it only for a clear measured or reasoned need — expensive repeated work, high read volume, expensive remote calls with acceptable staleness — and choose the implementation by deployment, consistency and staleness requirements, never merely because a value is read often.
- Cache technology must stay out of Domain, and infrastructure cache APIs must not leak into Application without a deliberate boundary abstraction.
- Cache keys must uniquely represent the cached value and include every relevant dimension (identifier, tenant, user when user-specific, locale, query parameters); avoid global keys for user- or tenant-specific data.
- Every cache entry must have a lifetime or another explicit invalidation strategy.
- Invalidate or update cache entries consistently with successful underlying mutations; the cache must never become a second source of truth.
