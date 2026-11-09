> Level: 2 Technology · Owns: resilience pipeline technique (private reference of `httpclient-factory`) · Scope: backend · Loads: read by `httpclient-factory` only

# Resilience

Policy owners: `.claude/rules/0-core/runtime-principles.md` (bounded time, retry safety, Retry-After, fallback, cancellation). Package choice — including when a direct Polly reference is acceptable — is a conditional-technology entry in the project decisions. `Microsoft.Extensions.Http.Resilience` (for `HttpClient`) and `Microsoft.Extensions.Resilience` (other pipelines) are built on Polly v8; the examples below use their APIs.

Resilience mechanisms are added for an observed failure scenario, not because they are available.

## HttpClient

```csharp
services.AddHttpClient<CatalogClient>(client => client.BaseAddress = catalogUri)
    .AddStandardResilienceHandler();
```

The standard handler (rate limiter, total timeout, retry, circuit breaker, attempt timeout) fits when its behavior matches the remote API. Tune or replace it rather than stacking a second handler with overlapping strategies:

```csharp
services.AddHttpClient<CatalogClient>(...)
    .AddResilienceHandler("catalog", builder =>
    {
        builder.AddTimeout(TimeSpan.FromSeconds(10));                 // total
        builder.AddRetry(new HttpRetryStrategyOptions
        {
            MaxRetryAttempts = 3,
            BackoffType = DelayBackoffType.Exponential,
            UseJitter = true,
            ShouldHandle = args => ValueTask.FromResult(
                HttpClientResiliencePredicates.IsTransient(args.Outcome))
        });
        builder.AddTimeout(TimeSpan.FromSeconds(2));                  // per attempt
    });
```

Values are illustrative; derive them from the dependency's latency and the caller's budget. For non-idempotent methods, disable retries for unsafe verbs (`options.Retry.DisableForUnsafeHttpMethods()` on the standard handler) unless an idempotency mechanism exists.

## Timeouts

Distinguish the **attempt** timeout from the **total operation** timeout, especially with retries enabled; the total budget bounds all attempts and delays together.

## Retry

Plausibly transient: selected network failures, temporary unavailability, rate limiting when retry is allowed, transient provider-specific database failures. Not retried: validation errors, authentication/authorization failures, permanent `404`, deterministic business rejection, non-idempotent operations without duplicate prevention.

Idempotency question before retrying a write: *if the first attempt succeeded remotely but the response was lost, what does sending it again do?* "Duplicate side effect" means automatic retry is unsafe. Use an idempotency mechanism only when the remote service actually supports it — do not invent a client-side `Idempotency-Key` contract.

## Retry-After

The HTTP retry strategy honors `Retry-After` by default in `Microsoft.Extensions.Http.Resilience`; do not override it with an independent aggressive schedule.

## Circuit breaker

Useful when repeated calls to a failing dependency add load or latency; give it operational visibility when it matters in production. Not for dependencies without a meaningful repeated-failure pattern.

## Fallback

Acceptable: stale cached read data where staleness is explicitly acceptable; omitting optional enrichment when its service is down. Unacceptable: "payment provider unavailable → pretend payment succeeded".

## Hedging

Parallel or delayed duplicate attempts — only for operations safe to execute multiple times, typically idempotent reads against interchangeable endpoints, and usually after measurement. Never for writes by default.

## Database resilience

Do not wrap normal EF Core operations in a generic application-level resilience pipeline. Prefer the provider's execution strategy (`UseSqlServer(..., o => o.EnableRetryOnFailure())`) and follow EF Core guidance for transactions under retrying strategies. HTTP retry policies are not database policies.

## Message publishing

Retrying publication can duplicate delivery. Use idempotent consumers, broker deduplication or an outbox when the business requires it; a retry policy never implies exactly-once delivery. (Messaging infrastructure itself is a Reserved decision.)

## Inbound rate limiting

ASP.NET Core rate limiting protects this API from excessive incoming traffic — a different concern from outbound resilience. Rejections return `429` with `Retry-After` when a useful delay is known (`http-api`).

## Telemetry

Observe retry counts, timeout frequency, circuit state, rate-limit rejections and dependency latency when they matter operationally, using the telemetry stack the project already has; resilience handlers do not require adopting OpenTelemetry.

## Decision guide

| Scenario | Typical consideration |
|---|---|
| External I/O | Bounded time budget |
| Safe transient HTTP failure | Retry with backoff and jitter |
| Unsafe write | No retry unless duplicate-safe |
| `429` from a dependency | Honor `Retry-After` |
| Repeated dependency outage | Circuit breaker |
| Optional data unavailable | Explicit fallback |
| Latency-sensitive idempotent read | Hedging after measurement |
| EF Core transient faults | Provider execution strategy |
| Incoming traffic limits | ASP.NET Core rate limiter |
