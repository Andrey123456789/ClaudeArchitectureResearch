---
paths:
  - "backend/**/*"
---
> Level: 0-core | Owns: outbound dependency calls — client lifetime, timeouts, retries, fallback, cancellation | Scope: backend | Loads: path (backend files)

# Outbound Call Rules

- Do not create and dispose a new `HttpClient` per request; use
  `IHttpClientFactory` or another appropriate long-lived client strategy.
- External I/O calls must have a bounded execution time appropriate to the
  operation. Avoid overlapping timeout mechanisms (per-attempt vs. total
  operation) whose combined behavior is unclear.
- Retry only when repeating the operation is safe. Do not automatically retry
  state-changing operations without idempotency or another concrete
  duplicate-safety mechanism.
- Default: when a dependency supplies `Retry-After` or equivalent rate-limit
  guidance, respect it where the policy supports it; never retry indefinitely or
  aggressively.
- Use a fallback only when its result is semantically acceptable; never hide a
  correctness failure behind a convenient default value.
- Caller cancellation is not a transient dependency failure: do not classify it
  as one or convert it into repeated outbound attempts.

Technique: `httpclient-factory` (resilience depth in its private reference).
