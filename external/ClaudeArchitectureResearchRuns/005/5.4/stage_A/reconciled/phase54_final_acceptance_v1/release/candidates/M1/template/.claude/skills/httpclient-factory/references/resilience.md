> Private reference of `httpclient-factory` · Resilience technique · Policy: `.claude/rules/performance.md` § Outbound Calls · Package choice: `add-dependency` § Choose the Package

# Resilience

Resilience policies match failure and operation semantics. Circuit breakers
help when repeated dependency failures would otherwise consume resources or
amplify an outage. Do not add resilience mechanisms merely because they are
available, and observe retries, timeouts, and circuit behavior when they
materially affect operations.

The Microsoft resilience packages build on Polly v8, but application code uses
the `Microsoft.Extensions` resilience APIs rather than configuring Polly
directly.

## HTTP Resilience

```csharp
services.AddHttpClient<CatalogClient>(client =>
{
    client.BaseAddress = catalogUri;
})
.AddStandardResilienceHandler();
```

The standard handler is useful when its behavior fits the remote API; it is not
mandatory for every client. Review its retry behavior carefully for
state-changing requests. Client lifetime and configuration: `httpclient-factory`.

## Timeouts

Distinguish the attempt timeout from the total operation timeout, especially
when retries are enabled, and choose values from actual latency requirements
rather than copying numbers from an example.

## Retry

Plausibly transient failures: selected network failures, temporary service
unavailability, rate limiting when retry is allowed, transient provider-specific
database failures. Not retried: validation errors, authentication/authorization
failures, permanent `404` outcomes, deterministic business rejection, and
non-idempotent operations without a duplicate-prevention strategy.

## Retry-After

Prefer the server's retry guidance when the client policy supports it, instead
of an independent aggressive schedule against a rate-limited dependency.

## Idempotency

Before retrying a write, ask:

```text
If the first attempt succeeded remotely but the response was lost,
what happens when we send the operation again?
```

If the answer is "duplicate side effect", automatic retry is unsafe. Use an
API-supported idempotency mechanism when appropriate; do not invent a
client-side `Idempotency-Key` unless the remote service supports that contract.

## Circuit Breaker

Use one when repeated calls to a failing dependency create additional load or
latency; not for a dependency without a meaningful repeated-failure pattern.
Give an important production circuit breaker operational visibility.

## Fallback

Acceptable examples: stale cached read data where staleness is explicitly
acceptable, optional enrichment omitted while its service is unavailable.
Unacceptable:

```text
payment provider unavailable
→ pretend payment succeeded
```

## Hedging

Hedging issues parallel or delayed duplicate attempts. Use it only for
operations that are safe to execute multiple times, typically idempotent reads
against interchangeable endpoints; do not hedge state-changing operations.

## Database Resilience

Do not wrap normal persistence operations in a generic application-level retry
pipeline. When the persistence provider supports transient retry through its
execution strategy or provider configuration, prefer that mechanism, and handle
transaction/retry interaction according to the provider's guidance (persistence
knowledge skill). An HTTP retry policy is not automatically appropriate for
database operations.

## Message Publishing

Retrying message publication requires understanding the broker and delivery
semantics; a retry may produce duplicate delivery. Use idempotent consumers,
broker-supported deduplication, outbox patterns, or similar mechanisms when the
business requirement needs them, and do not claim exactly-once delivery because
a retry policy exists.

## Inbound Rate Limiting

ASP.NET Core rate limiting protects this API from excessive incoming traffic
and is different from outbound resilience. A rejected request receives
`429 Too Many Requests`, with `Retry-After` when a useful delay is known
(`http-api` skill).

## Cancellation

Propagate cancellation through resilience pipelines; caller cancellation is not
a transient failure to retry.

## Telemetry

Useful signals: retry counts, timeout frequency, circuit state, rate-limit
rejections, dependency latency. Do not require OpenTelemetry solely because
resilience pipelines exist; use the telemetry stack adopted by the project.

## Review Checks

Check-by-reference against `performance.md` § Outbound Calls: retrying every
exception or HTTP status; retrying unsafe writes without idempotency analysis;
retrying client cancellation; circuit breakers without a failure scenario;
fallback values that conceal incorrect business results; hedged writes; generic
retry wrappers around persistence without understanding provider behavior;
stacked handlers with overlapping strategies; unbounded retry/timeout
combinations.

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
| Persistence transient faults | Prefer the provider's execution strategy |
| Incoming request rate limiting | ASP.NET Core rate limiter |
