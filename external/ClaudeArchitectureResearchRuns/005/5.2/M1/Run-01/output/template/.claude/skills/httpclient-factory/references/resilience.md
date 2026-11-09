> **Private reference** of `httpclient-factory` · Owns: resilience technique — HTTP resilience handlers, timeouts, retry, circuit breaker, fallback, hedging, message publishing, inbound rate limiting, telemetry · Scope: backend · Loading: on demand (read by `httpclient-factory`)

# Resilience

## Rules

Rules: `backend-runtime.md` → Outbound Calls (bounded time, safe retries,
`Retry-After`, fallback semantics, caller cancellation). Package choice
(Microsoft resilience packages; direct Polly only as a documented exception):
`add-dependency`.

1. Resilience policies must match failure and operation semantics.
2. Circuit breakers are useful when repeated dependency failures would otherwise
   consume resources or amplify an outage.
3. Do not add resilience mechanisms merely because they are available.
4. Observe retries/timeouts/circuit behavior when they materially affect
   operations.

## Package Choice

`Microsoft.Extensions.Http.Resilience` and `Microsoft.Extensions.Resilience` are
implemented on Polly v8; configure them through the Microsoft.Extensions
resilience APIs. Package selection: `add-dependency`.

## HTTP Resilience

For `HttpClient`, `Microsoft.Extensions.Http.Resilience` provides standard
resilience integration.

```csharp
services.AddHttpClient<CatalogClient>(client =>
{
    client.BaseAddress = catalogUri;
})
.AddStandardResilienceHandler();
```

The standard handler is useful when its behavior fits the remote API.

It is not mandatory for every HTTP client.

Review retry behavior carefully for state-changing requests.

Detailed HttpClient lifetime/configuration guidance belongs to the
`httpclient-factory` skill.

## Timeouts

A dependency call should not wait indefinitely.

Distinguish:

```text
attempt timeout
```

from:

```text
total operation timeout
```

especially when retries are enabled.

Choose values from actual latency requirements rather than copying arbitrary
numbers from an example.

## Retry

Retry only failures that are plausibly transient.

Possible examples:

- selected network failures;
- temporary service unavailability;
- rate limiting when retry is allowed;
- transient provider-specific database failures.

Usually not transient, so not retried:

- validation errors;
- authentication/authorization failures;
- permanent `404` outcomes;
- deterministic business rejection.

## Retry-After

Rule: `backend-runtime.md` → Outbound Calls. The standard HTTP resilience
handler's retry strategy honors `Retry-After` by default.

## Idempotency

Before retrying a write ask:

```text
If the first attempt succeeded remotely but the response was lost,
what happens when we send the operation again?
```

If the answer is "duplicate side effect", automatic retry is unsafe.

Use an API-supported idempotency mechanism when appropriate.

Do not invent a client-side `Idempotency-Key` unless the remote service actually
supports that contract.

## Circuit Breaker

Use a circuit breaker when repeated calls to a failing dependency would create
additional load or latency.

Do not add a circuit breaker to a dependency that has no meaningful repeated
failure pattern.

A circuit breaker should have operational visibility when it is important in
production.

## Fallback

Fallback must preserve acceptable business semantics.

Valid examples may include:

- stale cached read data where staleness is explicitly acceptable;
- optional enrichment omitted when its service is unavailable.

Bad fallback:

```text
payment provider unavailable
→ pretend payment succeeded
```

## Hedging

Hedging issues parallel or delayed duplicate attempts.

Use it only for operations that are safe to execute multiple times, typically
idempotent reads against interchangeable endpoints.

Do not hedge state-changing operations by default.

## Database Resilience

Database transient-fault handling belongs to the persistence technology's own
mechanism: see the persistence knowledge facet.

## Message Publishing

Retrying message publication requires understanding the broker and delivery
semantics.

A retry may produce duplicate delivery.

Use idempotent consumers, broker-supported deduplication, outbox patterns, or
other mechanisms when the business requirement needs them.

Do not claim exactly-once delivery merely because a retry policy exists.

## Inbound Rate Limiting

ASP.NET Core rate limiting protects this API from excessive incoming traffic.

It is conceptually different from outbound retry/resilience.

When a request is rejected because of rate limiting:

```text
429 Too Many Requests
```

is the normal HTTP response.

Include `Retry-After` when a useful retry delay is known.

Detailed HTTP semantics belong to the `http-api` skill.

## Cancellation

Rule: `backend-runtime.md` → Outbound Calls. Pass the caller's
`CancellationToken` into the pipeline (`ExecuteAsync(callback, cancellationToken)`).

## Telemetry

Observe resilience behavior when it matters operationally.

Useful signals include:

- retry counts;
- timeout frequency;
- circuit state;
- rate-limit rejection;
- dependency latency.

Do not require OpenTelemetry solely because resilience pipelines or handlers
are present.

Use the telemetry stack adopted by the project.

## Anti-Patterns

Avoid:

- retrying every exception;
- retrying every HTTP status;
- circuit breakers added without a failure scenario;
- hedging writes;
- stacked resilience handlers with overlapping strategies;
- unbounded retry/timeout combinations.

## Decision Guide

| Scenario | Default consideration |
|---|---|
| External I/O | Bound execution time |
| Safe transient HTTP failure | Consider retry |
| Unsafe write | No retry unless duplicate-safe |
| `429` from dependency | Respect `Retry-After` where appropriate |
| Repeated dependency outage | Consider circuit breaker |
| Optional data unavailable | Consider explicit fallback |
| Latency-sensitive idempotent read | Consider hedging after measurement |
| Database transient faults | Persistence technology's execution strategy |
| Incoming request rate limiting | ASP.NET Core rate limiter |
