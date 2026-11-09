---
paths:
  - "backend/**"
---
<!-- Kind: STD | Scope: backend | Owns: caching need, cache keys, expiration, invalidation | Loads: path-scoped (backend/**) -->
# Backend Caching Standards

Cache placement across layers: `rules/backend/architecture.md` § Boundary Leaks. Distributed cache adoption: CLAUDE.md § Decisions.

- **Default:** caching is an optimization, not an architectural requirement — introduce it only for a clear measured or reasoned need (measured expensive repeated work, high read volume, expensive remote calls, acceptable staleness), and choose the implementation by deployment, consistency and staleness requirements. A value being read frequently is not by itself a reason.
- Cache keys **must** uniquely represent the cached value, including every dimension that affects it (entity identifier, tenant, user when genuinely user-specific, locale, relevant query/filter parameters); **never** use global keys for user- or tenant-specific data.
- Every cache entry **must** have a lifetime or another explicit invalidation strategy.
- Cache invalidation and updates **must** follow committed mutation semantics — not before the underlying mutation is known to have succeeded, unless the workflow deliberately accepts that — and cache state **must not** become a second source of truth.

Technique: `caching` knowledge skill.
