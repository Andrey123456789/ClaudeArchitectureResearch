> Private reference of the httpclient-factory skill. Owns: resilience technique and examples — pipelines, retry, circuit breaker, fallback, hedging, database and messaging retries, telemetry · Scope: backend · Loads: read by the httpclient-factory skill when resilience behavior is designed or reviewed · Depends on: .claude/skills/httpclient-factory/SKILL.md

# Resilience

Rules: `.claude/rules/error-handling.md` (Outbound Dependencies). Package
choice: `add-dependency` (Package choices). Resilience mechanisms are added only
when the failure and operation semantics call for them, not because they are
available.

## HTTP Resilience

`Microsoft.Extensions.Http.Resilience` integrates with `HttpClient`:

```csharp
services.AddHttpClient<CatalogClient>(client =>
{
    client.BaseAddress = catalogUri;
})
.AddStandardResilienceHandler();
```

The standard handler is useful when its behavior fits the remote API; it is
not mandatory for every client. Review its retry behavior carefully for
state-changing requests. The Microsoft packages are built on Polly v8, but
application code uses the `Microsoft.Extensions` resilience APIs rather than
configuring Polly directly.

## Timeouts

```text
attempt timeout   -> limits one try
total timeout     -> limits the whole operation, including retries
```

Choose values from actual latency requirements, not from examples.

## Retry

Retry safety rule: `error-handling.md`. Plausibly transient failures include
selected network failures, temporary service unavailability, rate limiting when
retry is allowed, and transient provider-specific database failures. Not
transient: validation errors, authentication/authorization failures, permanent
`404` outcomes, and deterministic business rejections.

## Retry-After

Rule: `error-handling.md`. Configure the retry strategy to use the server's
`Retry-After` value where it supports it, rather than an independent fixed
schedule.

## Idempotency Question

Before retrying a write, ask:

```text
If the first attempt succeeded remotely but the response was lost,
what happens when we send the operation again?
```

If the answer is "duplicate side effect", automatic retry is unsafe. Use an
API-supported idempotency mechanism when appropriate; do not invent a client-side
`Idempotency-Key` unless the remote service supports that contract.

## Circuit Breaker

Use a circuit breaker when repeated calls to a failing dependency would add load
or latency, not for a dependency without a meaningful repeated-failure pattern.
Give it operational visibility when it matters in production.

## Fallback

Examples for the fallback rule (`error-handling.md`). Acceptable: stale cached
read data where staleness is explicitly acceptable, or optional enrichment
omitted when its service is unavailable. Unacceptable:

```text
payment provider unavailable
-> pretend payment succeeded
```

## Hedging

Hedging issues parallel or delayed duplicate attempts. Use it only for
operations that are safe to execute several times, typically idempotent reads
against interchangeable endpoints; state-changing operations fall under the
retry-safety rule in `.claude/rules/error-handling.md`.

## Database Resilience

Do not wrap normal EF Core operations in a generic application-level retry
pipeline. When the provider supports transient retry through EF Core execution
strategies or provider configuration, prefer that mechanism, and handle
transaction/retry interaction according to the provider's EF Core guidance. An
HTTP retry policy is not automatically appropriate for database operations.

## Message Publishing

Retrying publication can produce duplicate delivery. Use idempotent consumers,
broker-supported deduplication, outbox patterns, or other mechanisms when the
business requirement needs them; a retry policy does not provide exactly-once
delivery.

## Inbound Rate Limiting

ASP.NET Core rate limiting protects this API from excessive incoming traffic and
is separate from outbound resilience. A rate-limited request receives
`429 Too Many Requests`, with `Retry-After` when a useful delay is known
(`http-api` skill).

## Cancellation

Pass the caller's `CancellationToken` through resilience pipelines (cancellation
and retries: `error-handling.md`).

## Telemetry

Observe retry counts, timeout frequency, circuit state, rate-limit rejections,
and dependency latency when they matter operationally, using the telemetry
stack the project adopted. Resilience handlers do not by themselves require
OpenTelemetry.

## Anti-Patterns

- retrying every exception or every HTTP status;
- circuit breakers without a failure scenario;
- fallback values that conceal incorrect business results;
- hedging writes;
- generic retry wrappers around EF Core without understanding provider behavior;
- stacked resilience handlers with overlapping strategies;
- unbounded retry/timeout combinations.

## Decision Guide

| Scenario | Default consideration |
|---|---|
| External I/O | Bound execution time |
| Safe transient HTTP failure | Consider retry |
| Unsafe write | No retry unless duplicate-safe |
| `429` from dependency | Honor `Retry-After` where appropriate |
| Repeated dependency outage | Consider circuit breaker |
| Optional data unavailable | Consider explicit fallback |
| Latency-sensitive idempotent read | Consider hedging after measurement |
| EF transient faults | Provider/EF execution strategy |
| Incoming request rate limiting | ASP.NET Core rate limiter |
