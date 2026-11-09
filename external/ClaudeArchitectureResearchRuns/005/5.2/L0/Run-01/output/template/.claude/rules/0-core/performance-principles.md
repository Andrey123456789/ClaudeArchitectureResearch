---
paths:
  - "backend/**/*.cs"
---

> Level: 0 Core | Owns: correctness-first optimization and efficient data access | Scope: backend | Loads: path | Depends on: none

# Performance Principles

- Default: prefer clear, correct code first. Do not introduce specialized
  optimizations without a concrete reason; for non-trivial optimizations,
  prefer measurement or profiling evidence over assumptions.
- Default: keep database work efficient — filter and project in the database
  when practical, avoid unnecessary round trips, over-fetching, and N+1
  patterns, and paginate potentially large result sets.
- Default: introduce compiled queries, `ValueTask`, pooling, custom
  serialization, aggressive caching, or raw SQL for performance only for a
  measured or clearly demonstrated need.

Performance-motivated changes: → `develop` (performance changes).
