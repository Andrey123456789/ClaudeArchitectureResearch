Kind: KNW | Scope: backend | Capability: — | Loading: private reference of `httpclient-factory`, read when configuring resilience

# Resilience for External Dependencies

Rules: `.claude/rules/backend/integrations.md` (bounded time, safe retries, Retry-After, acceptable fallback, caller cancellation). Package choice: `add-dependency` (Microsoft.Extensions resilience packages; direct Polly only as a documented exception). Resilience policies must match the failure and operation semantics; do not add a mechanism merely because it is available.

## HTTP resilience

`Microsoft.Extensions.Http.Resilience` integrates with `HttpClient`:

```csharp
services.AddHttpClient<CatalogClient>(client =>
{
    client.BaseAddress = catalogUri;
})
.AddStandardResilienceHandler();
```

The standard handler (rate limiter, total timeout, retry, circuit breaker, attempt timeout) fits when its behavior matches the remote API; it is not mandatory for every client. Review its retry behavior carefully for state-changing requests, and avoid stacking handlers with overlapping strategies. The packages are built on Polly v8, but application code uses the Microsoft.Extensions resilience APIs rather than configuring Polly directly. For non-HTTP pipelines use `Microsoft.Extensions.Resilience` (`services.AddResiliencePipeline(...)`).

## Timeouts

A dependency call must not wait indefinitely. Distinguish the attempt timeout from the total-operation timeout, especially with retries, and choose values from actual latency requirements rather than copying numbers from examples.

## Retry

Plausibly transient failures: selected network failures, temporary service unavailability, rate limiting when retry is allowed, transient provider-specific database failures. Not transient: validation errors, authentication and authorization failures, permanent `404` outcomes, deterministic business rejections. Repeat-safety of writes: `integrations.md`.

Before retrying a write, ask: if the first attempt succeeded remotely but the response was lost, what happens when the operation is sent again? If the answer is "a duplicate side effect", automatic retry is unsafe. Use an idempotency mechanism the remote API supports; do not invent a client-side `Idempotency-Key` the service does not honor.

## Retry-After

Honor the server's `Retry-After` when the client policy supports it, instead of an independent aggressive retry schedule against a rate-limited dependency.

## Circuit breaker

Use a circuit breaker when repeated calls to a failing dependency would add load or latency; skip it when there is no meaningful repeated-failure pattern. Give it operational visibility when it matters in production.

## Fallback

Valid fallbacks: stale cached read data where staleness is explicitly acceptable; omitting optional enrichment when its service is unavailable. Invalid: "payment provider unavailable → pretend payment succeeded".

## Hedging

Hedging sends parallel or delayed duplicate attempts. Use it only for operations that are safe to execute several times, typically idempotent reads against interchangeable endpoints, and after measurement; never hedge state-changing operations by default.

## Database operations

Do not wrap normal database access in a generic application-level retry or resilience pipeline. Use the persistence technology's provider-level transient-retry mechanism (persistence knowledge facet); an HTTP retry policy is not appropriate for database operations.

## Message publishing

Retrying publication can produce duplicate delivery. Use idempotent consumers, broker-supported deduplication, an outbox or other mechanisms when the business requirement needs them, and do not claim exactly-once delivery because a retry policy exists.

## Inbound rate limiting

ASP.NET Core rate limiting protects this API from excessive incoming traffic and is separate from outbound resilience. A request rejected by rate limiting gets `429 Too Many Requests`, with `Retry-After` when a useful delay is known (`http-api` skill).

## Cancellation

Pass the caller's `CancellationToken` into the pipeline (`ExecuteAsync(..., cancellationToken)`); cancellation semantics: `integrations.md`.

## Telemetry

Observe retry counts, timeout frequency, circuit state, rate-limit rejections and dependency latency when they matter operationally. Use the telemetry stack the project adopted; resilience handlers do not by themselves require OpenTelemetry.

## Quick reference

| Scenario | Consider |
|---|---|
| Any external I/O | Bounded execution time |
| Safe transient HTTP failure | Retry |
| Unsafe write | No retry unless duplicate-safe |
| `429` from a dependency | Honor `Retry-After` |
| Repeated dependency outage | Circuit breaker |
| Optional data unavailable | Explicit fallback |
| Latency-sensitive idempotent read | Hedging after measurement |
| Database transient faults | Provider-level execution strategy |
| Incoming request rate limiting | ASP.NET Core rate limiter |
