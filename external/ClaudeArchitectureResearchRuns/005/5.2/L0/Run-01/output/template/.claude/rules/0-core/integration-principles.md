---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Level: 0 Core | Owns: outbound dependency-call semantics (time bounds, retry, fallback, cancellation) | Scope: backend | Loads: path | Depends on: none

# Integration Principles

- External I/O calls must have a bounded execution time appropriate to the
  operation; avoid overlapping timeout mechanisms whose combined behavior is
  unclear (for example per-attempt versus total-operation timeouts).
- Retry only when repeating the operation is safe; do not automatically retry
  state-changing operations without idempotency or another concrete
  duplicate-prevention mechanism.
- Default: when a dependency supplies `Retry-After` or equivalent rate-limit
  guidance, respect it where appropriate; do not retry indefinitely or
  aggressively.
- Use a fallback only when its result is semantically acceptable; do not hide
  correctness failures behind convenient default values.
- Do not classify caller cancellation as a transient dependency failure or
  convert it into repeated outbound attempts.

Outbound client technique: → `httpclient-factory` skill.
