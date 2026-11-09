> Owns: resilience pipeline technique and examples (no policy) | Scope: backend | Loads: private reference, read only by the httpclient-factory skill

# Resilience

Policy owners: bounded execution time, retry safety, Retry-After, fallback
semantics, and caller cancellation — `.claude/rules/error-handling.md`; approved
packages — `docs/technology-stack.md`; package choice and the direct-Polly
exception — `add-dependency`.

## Principles

1. Match resilience policies to the failure and operation semantics.
2. Circuit breakers help when repeated dependency failures would otherwise
   consume resources or amplify an outage.
3. Do not add resilience mechanisms merely because they are available.
4. Observe retries, timeouts, and circuit behavior when they materially affect
   operations.

The Microsoft resilience packages are built on Polly v8, but application code
uses the `Microsoft.Extensions` resilience APIs.

## HTTP Resilience

`Microsoft.Extensions.Http.Resilience` provides standard resilience integration
for `HttpClient`:

```csharp
services.AddHttpClient<CatalogClient>(client =>
{
    client.BaseAddress = catalogUri;
})
.AddStandardResilienceHandler();
```

The standard handler is useful when its behavior fits the remote API; it is not
mandatory for every client. Review its retry behavior carefully for
state-changing requests.

## Timeouts

Distinguish the attempt timeout from the total operation timeout, especially
when retries are enabled. Choose values from actual latency requirements rather
than copying numbers from an example.

## Retry

Plausibly transient failures: selected network failures, temporary service
unavailability, rate limiting when retry is allowed, transient provider-specific
database failures.

Not retried: validation errors, authentication/authorization failures, permanent
`404` outcomes, deterministic business rejections, and non-idempotent operations
without a duplicate-prevention strategy.

When a remote endpoint returns `Retry-After`, let the policy follow the server's
guidance instead of an independent aggressive schedule.

## Idempotency

Before retrying a write, ask:

```text
If the first attempt succeeded remotely but the response was lost,
what happens when we send the operation again?
```

If the answer is "duplicate side effect", automatic retry is unsafe. Use an
API-supported idempotency mechanism when appropriate, and do not invent a
client-side `Idempotency-Key` unless the remote service actually supports that
contract.

## Circuit Breaker

Use one when repeated calls to a failing dependency would create additional load
or latency, not for a dependency without a meaningful repeated-failure pattern.
Give an important production circuit breaker operational visibility.

## Fallback

Valid examples: stale cached read data where staleness is explicitly
acceptable; optional enrichment omitted when its service is unavailable.

Bad fallback:

```text
payment provider unavailable
-> pretend payment succeeded
```

## Hedging

Hedging issues parallel or delayed duplicate attempts. Use it only for
operations that are safe to execute multiple times — typically idempotent reads
against interchangeable endpoints — never for state-changing operations by
default.

## Database Resilience

Do not wrap normal EF Core operations in a generic application-level retry
pipeline by default. When the provider supports transient retry through EF Core
execution strategies or provider configuration, prefer that mechanism, and
handle transaction/retry interaction according to the provider's EF Core
guidance. An HTTP retry policy is not automatically appropriate for database
operations.

## Message Publishing

Retrying publication can produce duplicate delivery. Use idempotent consumers,
broker-supported deduplication, outbox patterns, or other mechanisms when the
business requirement needs them; a retry policy does not provide exactly-once
delivery.

## Inbound Rate Limiting

ASP.NET Core rate limiting protects this API from excessive incoming traffic and
is conceptually different from outbound resilience. A rejected request normally
returns `429 Too Many Requests`, with `Retry-After` when a useful delay is known
(`http-api` skill).

## Cancellation

Propagate cancellation through resilience pipelines so a cancelled caller ends
the pipeline instead of triggering further attempts.

## Telemetry

Useful signals: retry counts, timeout frequency, circuit state, rate-limit
rejections, dependency latency. Do not require OpenTelemetry solely because
resilience handlers are present; use the telemetry stack the project adopted.

## Anti-Patterns

Avoid retrying every exception or HTTP status, circuit breakers without a failure
scenario, hedging writes, generic resilience wrappers around EF Core without
understanding provider behavior, stacked handlers with overlapping strategies,
and unbounded retry/timeout combinations.

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
