---
paths:
  - "backend/**"
---
<!-- Kind: STD | Scope: backend | Owns: outbound HTTP client lifetime, timeouts, retries, Retry-After, fallback, caller cancellation | Loads: path-scoped (backend/**) -->
# Backend Outbound HTTP and Resilience Standards

Resilience packages: DEC-RES-01. Transport boundary toward Application: `rules/backend/architecture.md` § Boundary Leaks.

- **Must not** create and dispose a new `HttpClient` per request; use `IHttpClientFactory` or another appropriate long-lived client strategy.
- External I/O calls **must** have a bounded execution time appropriate to the operation; avoid overlapping timeout mechanisms (for example per-attempt and total-operation timeouts) whose combined behavior is unclear.
- Retries **must** happen only when repeating the operation is safe; **never** retry state-changing operations automatically without idempotency or another concrete duplicate-safety mechanism.
- **Default:** respect `Retry-After` or equivalent rate-limit guidance where appropriate; do not retry indefinitely or aggressively.
- Fallback **must** be used only when its result is semantically acceptable; **never** hide correctness failures behind convenient default values.
- Caller cancellation **must not** be classified as a transient dependency failure or converted into repeated outbound attempts.

Technique: `httpclient-factory` knowledge skill (includes the resilience reference).
