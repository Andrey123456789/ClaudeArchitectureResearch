> Owns: resilience pipeline technique (standard handler, timeouts, retry, circuit breaker, hedging, fallback, database and messaging considerations, telemetry) | Scope: backend | Loads: private reference of httpclient-factory (read on demand by that skill only)

# Resilience — Technique

Package choice: `docs/technology-stack.md`. Outbound failure semantics (bounded
time, safe retries, Retry-After, acceptable fallback, cancellation):
`.claude/rules/error-handling.md`. Add a resilience mechanism only when the
failure scenario calls for it.

## HTTP Standard Handler

```csharp
services.AddHttpClient<CatalogClient>(client => client.BaseAddress = catalogUri)
    .AddStandardResilienceHandler();
```

Useful when its behavior fits the remote API; not mandatory for every client.
Review its retry behavior for state-changing requests (disable or narrow retries
for unsafe methods).

## Custom Pipeline

```csharp
services.AddHttpClient<CatalogClient>(client => client.BaseAddress = catalogUri)
    .AddResilienceHandler("catalog", pipeline =>
    {
        pipeline.AddTimeout(TimeSpan.FromSeconds(10));          // total operation
        pipeline.AddRetry(new HttpRetryStrategyOptions
        {
            MaxRetryAttempts = 3,
            ShouldRetryAfterHeader = true,                       // honor Retry-After
            BackoffType = DelayBackoffType.Exponential,
        });
        pipeline.AddTimeout(TimeSpan.FromSeconds(2));           // per attempt
    });
```

Values are illustrative; derive them from actual latency requirements.
Distinguish attempt timeout from total timeout when retries are enabled.

## Retry Candidates

Plausibly transient: selected network failures, temporary unavailability, rate
limiting where retry is allowed, transient provider-specific database errors.
Not transient: validation errors, authentication/authorization failures,
permanent `404`, deterministic business rejection. Write safety is governed by
`error-handling.md`; the key question for writes: "If the first attempt
succeeded remotely but the response was lost, what happens when we send it
again?" Do not invent a client-side `Idempotency-Key` unless the remote service
supports that contract.

## Circuit Breaker

Use when repeated calls to a failing dependency would add load or latency; give
it operational visibility when it matters in production. Skip it for
dependencies without a meaningful repeated-failure pattern.

## Fallback Examples

Acceptable: stale cached reads where staleness is explicitly acceptable; omitting
optional enrichment when its service is down. Unacceptable: "payment provider
unavailable → pretend payment succeeded".

## Hedging

Parallel/delayed duplicate attempts — only for operations safe to execute
multiple times, typically idempotent reads against interchangeable endpoints,
and preferably after measurement.

## Database Resilience

Do not wrap normal EF Core operations in a generic application-level resilience
pipeline. Prefer the provider's EF Core execution strategy
(`options.UseSqlServer(cs, sql => sql.EnableRetryOnFailure())`) and follow its
guidance for transactions with retries; HTTP retry policies are not database
policies.

## Message Publishing

Retried publication can produce duplicate delivery. Use idempotent consumers,
broker deduplication, or an outbox when the requirement needs it; a retry policy
never implies exactly-once delivery. (Messaging infrastructure is Reserved.)

## Inbound Rate Limiting

ASP.NET Core rate limiting protects this API from incoming traffic and is
separate from outbound resilience; rejected requests return `429` with
`Retry-After` when known (`http-api`).

## Telemetry

Observe retry counts, timeout frequency, circuit state, rate-limit rejections,
and dependency latency when they matter operationally, using the project's
adopted telemetry stack; resilience handlers do not by themselves require
OpenTelemetry.

## Decision Guide

| Scenario | Consider |
|---|---|
| Safe transient HTTP failure | Retry with backoff |
| `429` from dependency | Retry honoring `Retry-After` |
| Repeated dependency outage | Circuit breaker |
| Optional data unavailable | Explicit fallback |
| Latency-sensitive idempotent read | Hedging after measurement |
| EF transient faults | Provider execution strategy |
| Stacked handlers with overlapping strategies | Consolidate into one pipeline |
