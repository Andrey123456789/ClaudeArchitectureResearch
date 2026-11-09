---
paths:
  - "backend/**/*.cs"
---

> Kind: STD | Scope: backend | Owner: outbound dependencies — HttpClient lifetime, transport boundary, time limits, retry, fallback, cancellation | Loading: path-scoped

# Outbound Integration Standard

Resilience packages: D-12.

- Never create and dispose a new `HttpClient` per request; use `IHttpClientFactory` or another appropriate long-lived client strategy.
- Infrastructure translates remote HTTP responses into Application-facing abstractions; `HttpResponseMessage` and other remote transport concerns must not leak into Application.
- External I/O calls must have a bounded execution time appropriate to the operation; avoid overlapping timeout mechanisms whose combined behavior is unclear.
- Retry only when repeating the operation is safe; never retry state-changing operations automatically without idempotency or another concrete duplicate-prevention mechanism.
- Default: when a dependency supplies `Retry-After` or equivalent rate-limit guidance, respect it where appropriate, and never retry indefinitely or aggressively.
- Use a fallback only when its result is semantically acceptable; never hide a correctness failure behind a convenient default value.
- Caller cancellation is not a transient dependency failure: do not classify it as one or turn it into repeated outbound attempts.
