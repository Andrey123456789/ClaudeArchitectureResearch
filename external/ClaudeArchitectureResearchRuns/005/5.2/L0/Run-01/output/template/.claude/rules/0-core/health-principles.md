---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Level: 0 Core | Owns: health-endpoint semantics and exposure | Scope: backend | Loads: path | Depends on: none

# Health Principles

- Health checks must remain cheap and deterministic; they must not become full
  business workflows or perform expensive or mutating database work.
- Liveness should avoid external dependencies that could cause restart loops;
  readiness may depend on capabilities required to serve traffic and should
  reflect startup and dependency availability appropriately (for example,
  staying unhealthy while required asynchronous startup work is incomplete).
- Do not expose secrets, credentials, connection details, stack traces, or
  unnecessary internal diagnostics through publicly reachable health responses.

Implementation technique: → `health-check` skill.
