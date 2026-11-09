> Kind: KNW | Scope: backend | Owner: resilience pipeline technique (private to httpclient-factory) | Loading: read by httpclient-factory only

# Resilience

Rules: `rules/backend/integrations.md`. Packages: D-12. See also: `add-dependency` § Package-specific choices (package choice and the Polly exception).

Resilience policies match failure and operation semantics; add a mechanism only for an identified failure scenario, and observe retries, timeouts and circuit state when they matter operationally. The Microsoft packages are built on Polly v8, but application code uses the `Microsoft.Extensions` resilience APIs.

## HTTP resilience

```csharp
services.AddHttpClient<CatalogClient>(client =>
{
    client.BaseAddress = catalogUri;
})
.AddStandardResilienceHandler();
```

The standard handler is useful when its behavior fits the remote API; it is not mandatory for every client. Review its retry behavior carefully for state-changing requests, and avoid stacking handlers with overlapping strategies.

## Timeouts

Distinguish attempt timeout from total operation timeout, especially with retries enabled. Choose values from actual latency requirements, not from examples.

## Retry

Plausibly transient failures: selected network failures, temporary unavailability, rate limiting where retry is allowed, transient provider-specific database failures. Not retried: validation errors, authentication/authorization failures, permanent `404`, deterministic business rejection, non-idempotent operations without duplicate prevention.

Before retrying a write, ask: if the first attempt succeeded remotely but the response was lost, what happens when the operation is sent again? If the answer is a duplicate side effect, automatic retry is unsafe. Use an idempotency mechanism the remote API actually supports — a client-side `Idempotency-Key` helps only when the remote service implements that contract.

## Retry-After

Prefer the server's retry guidance when the policy supports it instead of an independent aggressive schedule against a rate-limited dependency.

## Circuit breaker

Useful when repeated calls to a failing dependency would add load or latency; pointless without a meaningful repeated-failure pattern. Give it operational visibility when it matters in production.

## Fallback

Acceptable fallbacks: stale cached read data where staleness is explicitly acceptable; optional enrichment omitted when its service is unavailable. Unacceptable: "payment provider unavailable → pretend payment succeeded".

## Hedging

Hedging sends parallel or delayed duplicate attempts; use it only for operations safe to execute multiple times, typically idempotent reads against interchangeable endpoints — not writes.

## Database resilience

Do not wrap normal EF Core operations in a generic application-level retry pipeline. When the provider supports transient retry through EF Core execution strategies or provider configuration, prefer that, and handle transaction/retry interaction according to the provider's EF Core guidance. HTTP retry policies are not database policies.

## Message publishing

Retrying publication can duplicate delivery; use idempotent consumers, broker deduplication, outbox patterns or similar when the business requirement needs them. A retry policy does not make delivery exactly-once.

## Inbound rate limiting

ASP.NET Core rate limiting protects this API from excessive incoming traffic and is separate from outbound resilience; rejected requests get `429` with `Retry-After` when a useful delay is known (`http-api`).

## Cancellation

Propagate caller cancellation through resilience pipelines; it is not a transient failure to retry.

## Telemetry

Useful signals: retry counts, timeout frequency, circuit state, rate-limit rejections, dependency latency. Use the telemetry stack the project adopted; resilience handlers alone do not justify adding OpenTelemetry.

## Decision guide

| Scenario | Consideration |
|---|---|
| External I/O | Bounded execution time |
| Safe transient HTTP failure | Consider retry |
| Unsafe write | No retry unless duplicate-safe |
| `429` from dependency | Honor `Retry-After` where appropriate |
| Repeated dependency outage | Consider circuit breaker |
| Optional data unavailable | Consider explicit fallback |
| Latency-sensitive idempotent read | Consider hedging after measurement |
| EF transient faults | Provider/EF execution strategy |
| Incoming request rate limiting | ASP.NET Core rate limiter |
