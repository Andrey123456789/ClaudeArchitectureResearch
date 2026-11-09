> Level: 2-technology · Owns: resilience pipeline technique (private reference of `httpclient-factory`) · Loading: read by `httpclient-factory`

# Resilience

Rules: outbound-dependency rules (`.claude/rules/0-core/backend-code.md`). Package choice (Microsoft resilience packages by default; direct Polly only as a documented exception; deprecated Polly integrations never): `add-dependency`. The Microsoft packages are built on Polly v8, but application code normally configures them through the `Microsoft.Extensions` resilience APIs.

## HTTP pipelines

```csharp
services.AddHttpClient<CatalogClient>(client => client.BaseAddress = catalogUri)
    .AddStandardResilienceHandler();
```

The standard handler helps when its behavior fits the remote API; it is not mandatory, and its retry behavior needs review for state-changing requests. Avoid stacking handlers with overlapping strategies.

## Strategies

- **Timeouts** — set attempt and total-operation timeouts from real latency requirements, not example numbers.
- **Retry** — plausibly transient failures only: selected network failures, temporary unavailability, rate limiting when retry is allowed, transient provider-specific database failures. Never validation errors, authentication/authorization failures, permanent `404`, deterministic business rejection, or non-idempotent operations without duplicate prevention. Ask: if the first attempt succeeded remotely but the response was lost, what does a resend do? Do not invent a client-side `Idempotency-Key` unless the remote service supports it.
- **Retry-After** — prefer the server's guidance when the policy supports it instead of an independent aggressive schedule.
- **Circuit breaker** — when repeated calls to a failing dependency add load or latency; give it operational visibility in production; skip it without a repeated-failure scenario.
- **Fallback** — acceptable examples: stale cached read data where staleness is explicitly fine, optional enrichment omitted when its service is down. Unacceptable: "payment provider unavailable → pretend payment succeeded".
- **Hedging** — parallel or delayed duplicate attempts, only for operations safe to run several times (typically idempotent reads against interchangeable endpoints); never writes by default.
- **Inbound rate limiting** — ASP.NET Core rate limiting protects this API and is separate from outbound resilience; rejected requests get `429` with `Retry-After` when useful (`http-api`).

## Database operations

Do not wrap normal ORM operations in a generic application-level retry pipeline; prefer the provider's own execution strategy and handle transaction/retry interaction per the persistence knowledge skill. HTTP retry policies are not database policies.

## Messaging

Retrying publication can duplicate delivery; use idempotent consumers, broker deduplication, or an outbox when the business needs it, and never claim exactly-once delivery because a retry exists.

## Telemetry

Observe retry counts, timeout frequency, circuit state, rate-limit rejections, and dependency latency where operationally important, using the telemetry stack the project adopted; resilience alone does not require OpenTelemetry.

## Decision guide

| Scenario | Consider |
| --- | --- |
| External I/O | bounded execution time |
| Safe transient HTTP failure | retry |
| Unsafe write | no retry unless duplicate-safe |
| `429` from dependency | honor `Retry-After` |
| Repeated dependency outage | circuit breaker |
| Optional data unavailable | explicit fallback |
| Latency-sensitive idempotent read | hedging after measurement |
| Database transient faults | provider execution strategy |
| Incoming rate limiting | ASP.NET Core rate limiter |
