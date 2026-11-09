> Owner: private reference of the `httpclient-factory` skill — resilience pipeline technique | Scope: backend | Loads: read by `httpclient-factory` only | Enforced: none

# Resilience

Policy: `.claude/rules/error-handling.md` § External Dependency Failures
(bounded time, safe retries, `Retry-After`, acceptable fallback) and § Cancellation.
Packages (`Microsoft.Extensions.Http.Resilience`,
`Microsoft.Extensions.Resilience`; no deprecated Polly integration packages;
direct Polly only as a documented exception): `docs/technology-stack.md`
§ Conditional Technologies.

Match each resilience mechanism to the failure and operation semantics, add one
only for a concrete failure scenario, and observe its behavior when it matters
operationally. The Microsoft packages are built on Polly v8; configure them
through the Microsoft.Extensions resilience APIs rather than direct Polly APIs.

## HTTP Resilience

```csharp
services.AddHttpClient<CatalogClient>(client =>
{
    client.BaseAddress = catalogUri;
})
.AddStandardResilienceHandler();
```

The standard handler combines rate limiting, total timeout, retry, circuit
breaker, and per-attempt timeout. It fits when its behavior suits the remote API;
it is not mandatory for every client. Review its retry behavior for
state-changing requests, and tune or disable retries per client:

```csharp
.AddStandardResilienceHandler(options =>
{
    options.Retry.DisableForUnsafeHttpMethods();
    options.AttemptTimeout.Timeout = TimeSpan.FromSeconds(2);
    options.TotalRequestTimeout.Timeout = TimeSpan.FromSeconds(10);
});
```

Values are illustrative; derive them from actual latency requirements.

## Timeouts

Distinguish the **attempt timeout** from the **total operation timeout**,
especially when retries are enabled: the total must cover all attempts and
delays. Avoid stacking `HttpClient.Timeout`, a pipeline timeout, and a manual
`CancellationTokenSource` timeout with unclear combined behavior.

## Retry

Plausibly transient: selected network failures, temporary unavailability
(`503`), rate limiting when retry is allowed, transient provider-specific
database failures.

Not transient: validation errors, authentication/authorization failures,
permanent `404` outcomes, deterministic business rejections, and caller
cancellation.

## Retry-After

Prefer the server's retry guidance when the policy supports it; do not hammer a
rate-limited dependency with an independent aggressive schedule.

## Idempotency

Before retrying a write, ask:

```text
If the first attempt succeeded remotely but the response was lost,
what happens when we send the operation again?
```

If the answer is "duplicate side effect", automatic retry is unsafe. Use an
API-supported idempotency mechanism when appropriate; do not invent a client-side
`Idempotency-Key` unless the remote service supports that contract.

## Circuit Breaker

Use one when repeated calls to a failing dependency would add load or latency,
not for a dependency without a meaningful repeated-failure pattern. Give an
important production circuit breaker operational visibility.

## Fallback

Acceptable examples: stale cached read data where staleness is explicitly
acceptable; optional enrichment omitted while its service is unavailable.

Unacceptable:

```text
payment provider unavailable
→ pretend payment succeeded
```

## Hedging

Hedging issues parallel or delayed duplicate attempts. Use it only for operations
that are safe to execute multiple times — typically idempotent reads against
interchangeable endpoints — and measure first. Hedging a state-changing operation
duplicates its side effects (`.claude/rules/error-handling.md` § External
Dependency Failures).

## Database Resilience

Do not wrap normal EF Core operations in a generic application-level retry
pipeline. Prefer the provider's EF Core execution strategy:

```csharp
options.UseSqlServer(
    connectionString,
    sql => sql.EnableRetryOnFailure());
```

Handle transaction/retry interaction according to the provider's EF Core
guidance (`ef-core` skill § Transactions). An HTTP retry policy is not a
database retry policy.

## Message Publishing

Retrying publication can produce duplicate delivery. Use idempotent consumers,
broker deduplication, outbox patterns, or similar mechanisms when the business
requirement needs them (adding messaging infrastructure is a Reserved decision).
A retry policy does not give exactly-once delivery.

## Inbound Rate Limiting

ASP.NET Core rate limiting protects this API from excessive incoming traffic; it
is a different concern from outbound resilience. Rejected requests get `429` with
`Retry-After` when useful (`http-api` skill).

## Telemetry

Useful signals: retry counts, timeout frequency, circuit state, rate-limit
rejections, dependency latency. Use the telemetry stack the project already
adopted; resilience handlers alone do not justify adding OpenTelemetry.

## Common Mistakes

- retrying every exception or every HTTP status;
- circuit breakers without a failure scenario;
- stacked resilience handlers with overlapping strategies;
- generic retry wrappers around EF Core that ignore provider behavior;
- unbounded retry/timeout combinations.

## Decision Guide

| Scenario | Consider |
|---|---|
| External I/O | Bounded execution time |
| Safe transient HTTP failure | Retry |
| Unsafe write | No retry unless duplicate-safe |
| `429` from dependency | Honor `Retry-After` |
| Repeated dependency outage | Circuit breaker |
| Optional data unavailable | Explicit fallback |
| Latency-sensitive idempotent read | Hedging, after measurement |
| EF transient faults | Provider/EF execution strategy |
| Incoming request rate limiting | ASP.NET Core rate limiter |
