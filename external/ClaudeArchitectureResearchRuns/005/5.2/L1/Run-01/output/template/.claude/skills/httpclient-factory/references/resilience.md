> Level: 2-technology | Owns: resilience technique (skill-private reference of httpclient-factory) | Scope: backend | Loads: read by the httpclient-factory skill only

# Resilience

Package choice is part of `add-dependency`; retry safety, fallback, and
cancellation rules are in `outbound-calls.md`.

## Principles

Policies match failure and operation semantics; circuit breakers help when
repeated dependency failures would consume resources or amplify an outage;
mechanisms are added for a failure scenario, not because they exist; retries,
timeouts, and circuit state are observed when they matter operationally.

## HTTP resilience

```csharp
services.AddHttpClient<CatalogClient>(client =>
{
    client.BaseAddress = catalogUri;
})
.AddStandardResilienceHandler();
```

The standard handler (Microsoft.Extensions.Http.Resilience) is useful when its
behavior fits the remote API; it is not mandatory for every client. Review its
retry behavior for state-changing requests. These packages are built on Polly
v8; configure them through the Microsoft.Extensions resilience APIs rather than
direct Polly APIs.

## Timeouts

Distinguish attempt timeout from total-operation timeout, especially with
retries enabled. Take values from actual latency requirements, not examples.

## Retry

Plausibly transient: selected network failures, temporary unavailability, rate
limiting when retry is allowed, transient provider-specific database failures.
Not transient (no retry): validation errors, authentication/authorization
failures, permanent `404` outcomes, deterministic business rejections. Writes:
see the retry-safety rule in `outbound-calls.md`.

Idempotency question before retrying a write: *if the first attempt succeeded
remotely but the response was lost, what happens when we send it again?* If the
answer is a duplicate side effect, automatic retry is unsafe. Do not invent a
client-side `Idempotency-Key` unless the remote service supports that contract.

## Retry-After

Prefer the server's retry guidance when the policy supports it; never hammer a
rate-limited dependency with an independent aggressive schedule.

## Circuit breaker

Use one when repeated calls to a failing dependency add load or latency; give
important breakers operational visibility.

## Fallback

Acceptable: stale cached read data where staleness is explicitly acceptable;
optional enrichment omitted while its service is down. Unacceptable: "payment
provider unavailable → pretend payment succeeded".

## Hedging

Parallel or delayed duplicate attempts — only for operations safe to execute
multiple times (typically idempotent reads against interchangeable endpoints),
after measurement. Never hedge state-changing operations by default.

## Database resilience

Do not wrap ordinary data-access calls in a generic application-level
resilience pipeline. Prefer the persistence implementation's provider execution
strategy for transient database faults, and follow its guidance for
transaction/retry interaction (`persistence.knowledge`). An HTTP retry policy is
not a database policy.

## Message publishing

Retrying publication can duplicate delivery; use idempotent consumers,
broker-supported deduplication, or an outbox when the requirement needs it.
A retry policy does not make delivery exactly-once.

## Inbound rate limiting

ASP.NET Core rate limiting protects this API from excessive incoming traffic —
a different concern from outbound resilience. Rejections return `429` with
`Retry-After` when a useful delay is known (`http-api`).

## Cancellation and telemetry

Propagate cancellation through pipelines. Useful signals: retry counts,
timeout frequency, circuit state, rate-limit rejections, dependency latency.
Resilience pipelines do not by themselves require OpenTelemetry; use the
project's telemetry stack.

## Anti-patterns

Retrying every exception or status; retrying unsafe writes or client
cancellation; breakers without a failure scenario; fallbacks that hide wrong
results; hedged writes; generic retry wrappers around data access; stacked
handlers with overlapping strategies; unbounded retry/timeout combinations.

## Decision guide

| Scenario | Default consideration |
|---|---|
| External I/O | Bounded execution time |
| Safe transient HTTP failure | Consider retry |
| Unsafe write | No retry unless duplicate-safe |
| `429` from dependency | Respect `Retry-After` where appropriate |
| Repeated dependency outage | Consider a circuit breaker |
| Optional data unavailable | Consider an explicit fallback |
| Latency-sensitive idempotent read | Consider hedging after measurement |
| Transient database faults | Provider execution strategy |
| Incoming request rate limiting | ASP.NET Core rate limiter |
