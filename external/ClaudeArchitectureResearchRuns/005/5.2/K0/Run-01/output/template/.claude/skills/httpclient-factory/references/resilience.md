<!-- Kind: KNW | Scope: backend | Owns: resilience technique for external dependencies (private to httpclient-factory) | Loads: read by httpclient-factory -->
# Resilience

Standards: `rules/backend/outbound-http.md` (bounded time, retry safety, Retry-After, fallback semantics, caller cancellation). Packages: DEC-RES-01; package choice and the direct-Polly exception: `add-dependency` § Conditional Technology Packages.

## Core Practices

1. Resilience policies match failure and operation semantics.
2. Circuit breakers help when repeated dependency failures would otherwise consume resources or amplify an outage.
3. Resilience mechanisms are added for a failure scenario, not because they are available.
4. Retries, timeouts and circuit behavior are observed when they materially affect operations.

The Microsoft resilience packages are implemented on Polly v8; application code normally uses the `Microsoft.Extensions` resilience APIs rather than configuring Polly directly.

## HTTP Resilience

`Microsoft.Extensions.Http.Resilience` provides the standard handler:

```csharp
services.AddHttpClient<CatalogClient>(client =>
{
    client.BaseAddress = catalogUri;
})
.AddStandardResilienceHandler();
```

The standard handler is useful when its behavior fits the remote API; it is not mandatory for every client. Review its retry behavior carefully for state-changing requests. Client lifetime and configuration: the `httpclient-factory` skill.

## Timeouts

Bounded execution time (`rules/backend/outbound-http.md`) has two distinct limits. Distinguish

```text
attempt timeout
```

from

```text
total operation timeout
```

especially when retries are enabled, and choose values from actual latency requirements rather than copying example numbers.

## Retry

Plausibly transient failures: selected network failures, temporary service unavailability, rate limiting when retry is allowed, transient provider-specific database failures. Not retried: validation errors, authentication/authorization failures, permanent `404` outcomes, deterministic business rejection, non-idempotent operations without a duplicate-prevention strategy.

## Retry-After

When a remote endpoint returns `Retry-After`, prefer a client policy that respects it over an independent aggressive retry schedule against a rate-limited dependency.

## Idempotency

Before retrying a write ask:

```text
If the first attempt succeeded remotely but the response was lost,
what happens when we send the operation again?
```

If the answer is "duplicate side effect", automatic retry is unsafe. Use an API-supported idempotency mechanism when appropriate; do not invent a client-side `Idempotency-Key` unless the remote service supports that contract.

## Circuit Breaker

Use one when repeated calls to a failing dependency would add load or latency, not for a dependency without a meaningful repeated-failure pattern. Give an important production circuit breaker operational visibility.

## Fallback

Acceptable fallbacks include stale cached read data where staleness is explicitly acceptable, and optional enrichment omitted when its service is unavailable. A bad fallback:

```text
payment provider unavailable
→ pretend payment succeeded
```

## Hedging

Hedging issues parallel or delayed duplicate attempts — only for operations safe to execute several times, typically idempotent reads against interchangeable endpoints; not for state-changing operations by default.

## Database Resilience

Avoid wrapping normal EF Core operations in a generic application-level retry pipeline. When the provider supports transient retry through EF Core execution strategies/provider configuration, prefer that, and handle transaction/retry interaction according to the provider's EF Core guidance. An HTTP retry policy is not automatically appropriate for database operations.

## Message Publishing

Retrying publication requires understanding the broker and delivery semantics: a retry may duplicate delivery. Use idempotent consumers, broker deduplication, outbox patterns or similar when the business requirement needs them; a retry policy does not make delivery exactly-once.

## Inbound Rate Limiting

ASP.NET Core rate limiting protects this API from excessive incoming traffic — conceptually different from outbound resilience. A rejected request is `429 Too Many Requests`, with `Retry-After` when a useful delay is known (`http-api` skill).

## Cancellation

Pass the caller's token through the pipeline (`ResiliencePipeline.ExecuteAsync(..., cancellationToken)`) so cancellation stops pending attempts; how caller cancellation is classified: `rules/backend/outbound-http.md`.

## Telemetry

Useful signals: retry counts, timeout frequency, circuit state, rate-limit rejections, dependency latency. Use the telemetry stack the project adopted; resilience pipelines alone do not require OpenTelemetry.

## Anti-Patterns

Avoid retrying every exception or every HTTP status, retrying unsafe writes without idempotency analysis, retrying client cancellation, circuit breakers without a failure scenario, fallback values that conceal incorrect business results, hedging writes, generic retry wrappers around EF Core without understanding provider behavior, stacked handlers with overlapping strategies, and unbounded retry/timeout combinations.

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
| EF transient faults | Provider/EF execution strategy |
| Incoming request rate limiting | ASP.NET Core rate limiter |
