---
paths:
  - "backend/**/*.cs"
---

> Level: 0 Core | Owns: cache necessity, keys, invalidation, expiration | Scope: backend | Loads: path | Depends on: none

# Caching Principles

- Default: caching is an optimization, not a default architecture requirement.
  Introduce it only for a clear measured or reasoned need, and choose the
  implementation from deployment, consistency, and staleness requirements.
- Cache keys must uniquely represent the cached value and include every
  relevant dimension (identifier, tenant, user, locale, filters); avoid global
  keys for user- or tenant-specific data.
- Invalidate or update cache entries only consistently with successful
  underlying mutations; the cache must not become a second source of truth.
- Every cache entry must have a lifetime or another explicit invalidation
  strategy.

Cache placement across layers: → `1-architecture/backend-layers.md`. Technique: → `caching` skill.
