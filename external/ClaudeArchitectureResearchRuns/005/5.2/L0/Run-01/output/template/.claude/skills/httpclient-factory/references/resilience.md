> Level: 2 Technology | Owns: Microsoft.Extensions resilience technique (private to `httpclient-factory`) | Scope: backend | Loads: on demand by `httpclient-factory` | Depends on: 0-core/integration-principles.md

# Resilience

Add a resilience mechanism only when the dependency's failure behavior needs it;
retry and circuit breakers are not required for every external call, but a time
bound is.

## HTTP Pipeline

```csharp
services.AddHttpClient<CatalogClient>(client => client.BaseAddress = catalogUri)
    .AddStandardResilienceHandler();
```

The standard handler (rate limiter, total timeout, retry, circuit breaker,
attempt timeout) fits many read-heavy APIs; review its retry behavior for
state-changing requests and customize or replace it when it does not fit.
Microsoft.Extensions resilience is built on Polly v8; configure it through the
Microsoft.Extensions APIs rather than direct Polly APIs.

## Timeouts

Distinguish the attempt timeout from the total operation timeout, especially
with retries, and choose values from real latency requirements rather than
examples.

## Retry

Plausibly transient: selected network failures, temporary unavailability, rate
limiting when retry is permitted, transient provider database failures. Not
transient: validation errors, authentication/authorization failures, permanent
`404`, deterministic business rejection.

Before retrying a write, ask: *if the first attempt succeeded remotely but the
response was lost, what does a second attempt do?* If the answer is a duplicate
side effect, use an idempotency mechanism the remote API actually supports —
do not invent a client-side `Idempotency-Key` the server ignores. A `PUT` or
`DELETE` is not operationally safe to repeat merely because the HTTP method is
defined as idempotent; check what the remote implementation actually does.

## Circuit Breaker

Use one when repeated calls to a failing dependency add load or latency; give
it operational visibility when it matters in production.

## Fallback

Acceptable: stale cached reads where staleness is explicitly allowed, optional
enrichment omitted. Unacceptable: "payment provider unavailable → pretend the
payment succeeded".

## Hedging

Parallel or delayed duplicate attempts; only for operations safe to execute
several times (idempotent reads against interchangeable endpoints), after
measurement.

## Database and Messaging

Do not wrap EF Core operations in a generic application retry pipeline; use the
provider's EF Core execution strategy (e.g. `EnableRetryOnFailure`) and follow
its transaction guidance. Message-publication retries can duplicate delivery —
use idempotent consumers, broker deduplication, or an outbox when the business
needs it; a retry policy does not provide exactly-once delivery.

## Inbound Rate Limiting

ASP.NET Core rate limiting protects this API from incoming traffic and is
separate from outbound resilience; rejected requests return `429` with
`Retry-After` when known.

## Telemetry

Observe retry counts, timeout frequency, circuit state, rate-limit rejections,
and dependency latency when they matter, using the project's telemetry stack.

## Avoid

Retrying every exception or status, stacked handlers with overlapping
strategies, unbounded retry/timeout combinations, and circuit breakers without a
failure scenario.
