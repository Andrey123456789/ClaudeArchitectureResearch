---
paths:
  - "backend/**"
---
Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (backend/**)

# Outbound Integration Standards

Technique: `httpclient-factory` knowledge skill (resilience depth in its reference). Package choice for resilience: `add-dependency`.

- Do not create and dispose a new `HttpClient` for every request. Use `IHttpClientFactory` or another appropriate long-lived client strategy.
- Outbound dependency calls must have a bounded execution time appropriate to the operation. Avoid overlapping timeout mechanisms whose combined behavior is unclear, such as unrelated per-attempt and total timeouts.
- Retry only when repeating the operation is safe. Do not automatically retry state-changing operations without idempotency or another concrete duplicate-prevention mechanism.
- Default: respect `Retry-After` or equivalent rate-limit guidance where appropriate. Never retry indefinitely or aggressively.
- Use a fallback only when its result is semantically acceptable. Never hide correctness failures behind convenient default values.
- Do not classify caller cancellation as a transient dependency failure or turn it into repeated outbound attempts.
