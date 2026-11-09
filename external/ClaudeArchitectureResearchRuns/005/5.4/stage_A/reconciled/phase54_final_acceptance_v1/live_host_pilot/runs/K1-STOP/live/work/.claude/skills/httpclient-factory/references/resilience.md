> Kind: KNW | Scope: backend | Capability: — | Loading: read by `httpclient-factory` when resilience is in scope

# Resilience Reference

Policy: `.claude/rules/backend/runtime.md`. Package defaults (Microsoft resilience integration, direct Polly only as a documented exception): `add-dependency`. Resilience mechanisms are added only when failure and operation semantics justify them, and their behavior is observed when it matters operationally.

## HTTP resilience

```csharp
services.AddHttpClient<CatalogClient>(client => client.BaseAddress = catalogUri)
    .AddStandardResilienceHandler();
```

The standard handler fits when its behavior matches the remote API; it is not mandatory for every client. Review its retry behavior carefully for state-changing requests, and do not stack resilience handlers with overlapping strategies. The modern Microsoft packages are built on Polly v8, but application code configures them through the Microsoft.Extensions resilience APIs.

## Timeouts

Distinguish attempt timeout from total operation timeout, especially with retries enabled, and choose values from actual latency requirements rather than copying example numbers.

## Retry

Retry only plausibly transient failures: selected network failures, temporary unavailability, rate limiting when retry is allowed. Never retry validation errors, authentication/authorization failures, permanent `404` outcomes, deterministic business rejections, or non-idempotent operations without duplicate prevention. Before retrying a write ask: *if the first attempt succeeded remotely but the response was lost, what happens when we send it again?* A duplicate side effect means automatic retry is unsafe; use an API-supported idempotency mechanism, and never invent a client-side `Idempotency-Key` the remote service does not support.

## Retry-After

When a dependency returns `Retry-After`, prefer respecting it when the policy supports it; never hammer a rate-limited dependency with an independent aggressive schedule.

## Circuit breaker

Use one when repeated calls to a failing dependency would add load or latency; not for a dependency without a meaningful repeated failure pattern. Give it operational visibility when it matters in production.

## Fallback

Valid: stale cached read data where staleness is explicitly acceptable; optional enrichment omitted when its service is unavailable. Invalid: "payment provider unavailable → pretend payment succeeded".

## Hedging

Hedging issues parallel or delayed duplicate attempts — only for operations safe to execute multiple times, typically idempotent reads against interchangeable endpoints; never for state-changing operations by default.

## Database operations

Do not wrap normal database operations in a generic application-level retry pipeline or apply an HTTP retry policy to them; use the persistence technology's provider-level transient-fault handling (persistence knowledge facet named in the decision register).

## Message publishing

Retrying publication may produce duplicate delivery; use idempotent consumers, broker deduplication, an outbox, or similar mechanisms when the business requires them, and never claim exactly-once delivery merely because a retry policy exists.

## Inbound rate limiting

ASP.NET Core rate limiting protects this API from excessive incoming traffic and is conceptually separate from outbound resilience; a rejected request returns `429` with `Retry-After` when a useful delay is known (`http-api`).

## Cancellation and telemetry

Propagate caller cancellation through pipelines. Observe retry counts, timeout frequency, circuit state, rate-limit rejections, and dependency latency when they matter, using the telemetry stack the project adopted; OpenTelemetry is not required merely because pipelines exist.

## Decision guide

| Scenario | Default consideration |
|---|---|
| External I/O | Bound execution time |
| Safe transient HTTP failure | Consider retry |
| Unsafe write | No retry unless duplicate-safe |
| `429` from dependency | Respect `Retry-After` where appropriate |
| Repeated dependency outage | Consider circuit breaker |
| Optional data unavailable | Consider explicit fallback |
| Latency-sensitive idempotent read | Consider hedging after measurement |
| Database transient faults | Provider-level strategy (persistence facet) |
| Incoming request rate limiting | ASP.NET Core rate limiter |
