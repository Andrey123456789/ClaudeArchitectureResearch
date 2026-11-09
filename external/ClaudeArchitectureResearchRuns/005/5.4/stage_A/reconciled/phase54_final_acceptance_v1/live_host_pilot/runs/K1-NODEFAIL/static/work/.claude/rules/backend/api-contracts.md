---
paths:
  - "backend/**/*"
---

> Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (frontmatter paths)

# API Contract Evolution and Documentation Standard

## Versioning

- Must not introduce API versioning merely because an API exists; add it only when published compatibility or coexistence of client generations creates a concrete need (adopting versioning: Reserved, `CLAUDE.md`).
- Once an API version is relied on by external clients, it must not change incompatibly in silence: a breaking contract change requires a new version or another explicitly approved compatibility strategy.
- Default when explicit versioning is required: one strategy used consistently, URL-segment versioning unless project requirements justify another.
- Must not create separate Domain or persistence models merely because the external API has multiple versions; isolate version-specific transport contracts at the Api boundary when practical.

## Documentation

- Swagger/OpenAPI metadata must describe the API that actually runs: routes, important response statuses, schemas, and authentication behavior. Never document speculative responses.
- Default: Swagger UI is enabled in the Development environment and exposed in other environments only when a deployment requirement explicitly justifies it.

Technique: `api-versioning`, `swagger`. Version deprecation procedure: `development-workflow`.
