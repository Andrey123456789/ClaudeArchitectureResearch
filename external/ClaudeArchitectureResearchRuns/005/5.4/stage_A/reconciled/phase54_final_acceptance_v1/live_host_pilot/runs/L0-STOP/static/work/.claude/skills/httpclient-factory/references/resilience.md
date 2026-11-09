> Level: 2 Technology · Owns: resilience configuration technique (private reference of `httpclient-factory`) · Scope: backend · Loads: read by `httpclient-factory` only · Depends on: .claude/skills/httpclient-factory/SKILL.md

# Resilience

Policy owners: bounded execution time, retry safety, Retry-After, fallback semantics, caller cancellation → `.claude/rules/0-core/runtime-principles.md`; package choice and the direct-Polly exception → `add-dependency`; approved conditional packages → `3-project/decisions.md`. Resilience policies must match failure and operation semantics; do not add mechanisms merely because they are available.

## HTTP resilience

```csharp
services.AddHttpClient<CatalogClient>(client => client.BaseAddress = catalogUri)
    .AddStandardResilienceHandler();
```

The standard handler (`Microsoft.Extensions.Http.Resilience`) is useful when its behavior fits the remote API; it is not mandatory for every client. Review its retry behavior carefully for state-changing requests. The Microsoft resilience packages build on Polly v8; application code normally configures them through the Microsoft.Extensions APIs.

## Timeouts

Distinguish the **attempt timeout** from the **total operation timeout**, especially with retries. Choose values from actual latency requirements, not from examples.

## Retry

Plausibly transient: selected network failures, temporary unavailability, rate limiting when retry is allowed, transient provider-specific database failures. Not retried: validation errors, authentication/authorization failures, permanent 404 outcomes, deterministic business rejections, non-idempotent operations without duplicate prevention.

Before retrying a write, ask: *if the first attempt succeeded remotely but the response was lost, what happens when we send it again?* If the answer is "a duplicate side effect", automatic retry is unsafe. Use an idempotency mechanism the remote API actually supports; do not invent a client-side `Idempotency-Key` the service does not honor.

When a dependency returns `Retry-After`, let the retry policy honor it instead of an independent aggressive schedule.

## Circuit breaker

Use one when repeated calls to a failing dependency would add load or latency; skip it when there is no meaningful repeated-failure pattern. Give it operational visibility when it matters in production.

## Fallback

Valid: stale cached read data where staleness is explicitly acceptable; optional enrichment omitted while its service is down. Invalid: *payment provider unavailable → pretend payment succeeded*.

## Hedging

Hedging issues parallel or delayed duplicate attempts — only for operations safe to execute several times, typically idempotent reads against interchangeable endpoints. Do not hedge state-changing operations.

## Database resilience

Do not wrap normal EF Core operations in a generic application-level retry pipeline. Prefer the provider's EF Core execution strategy (for SQL Server, `options.UseSqlServer(cs, sql => sql.EnableRetryOnFailure())`) and follow the provider guidance for transaction/retry interaction. An HTTP retry policy is not a database policy.

## Message publishing

A publish retry may duplicate delivery. Use idempotent consumers, broker deduplication, an outbox, or similar mechanisms when the business requires it; a retry policy does not provide exactly-once delivery.

## Inbound rate limiting

ASP.NET Core rate limiting protects this API from excessive incoming traffic and is separate from outbound resilience; rejected requests get `429` with `Retry-After` when known (`http-api` skill).

## Telemetry

Observe retry counts, timeout frequency, circuit state, rate-limit rejections, and dependency latency when they matter operationally, using the telemetry stack the project adopted; resilience alone does not require OpenTelemetry.

## Anti-patterns

Retrying every exception or status; circuit breakers without a failure scenario; hedged writes; stacked handlers with overlapping strategies.

## Decision guide

| Scenario | Consideration |
|---|---|
| Safe transient HTTP failure | consider retry (standard handler or a configured retry strategy) |
| `429` from dependency | a retry strategy that reads `Retry-After` |
| Repeated dependency outage | consider circuit breaker |
| Optional data unavailable | consider explicit fallback |
| Latency-sensitive idempotent read | consider hedging after measurement |
| EF transient faults | provider/EF execution strategy |
