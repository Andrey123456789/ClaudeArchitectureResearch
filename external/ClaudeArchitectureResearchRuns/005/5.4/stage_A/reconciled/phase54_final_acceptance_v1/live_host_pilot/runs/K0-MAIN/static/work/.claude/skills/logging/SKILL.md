---
name: logging
description: Use when adding or reviewing logging — ILogger<T> templates, levels, scopes, correlation, exception logging, sensitive data, LoggerMessage, Serilog setup, sinks and request logging.
---

> Kind: KNW | Scope: backend | Owner: logging technique; Serilog depth in references/serilog.md | Loading: on demand (model-invoked knowledge)

# Logging

Rules: `rules/backend/hosting.md` § Logging, `rules/common/security.md` § Logging and sensitive data, `rules/backend/error-handling.md` (exception logging). Provider: D-06. Serilog configuration depth: `references/serilog.md`.

## Structured logging

```csharp
logger.LogInformation(
    "Order {OrderId} created for customer {CustomerId}",
    orderId,
    customerId);
```

Avoid interpolation, which turns structured values into opaque text and allocates even when the level is disabled:

```csharp
logger.LogInformation(
    $"Order {orderId} created for customer {customerId}");
```

Keep property names stable so logs stay queryable.

## Log levels

Choose levels by operational meaning:

- **Trace/Debug** — detailed diagnostics for troubleshooting; not a safe place for sensitive data.
- **Information** — meaningful application events: a background job completed, an important business operation completed, a lifecycle event. Not every internal method call.
- **Warning** — an unexpected or degraded condition the application recovered from: fallback used, retries exhausted but another path succeeded, optional dependency unavailable, unusual but handled state.
- **Error** — an operation failed and needs investigation. Expected negative outcomes such as `NotFound` or validation rejection are not application errors.
- **Critical** — the application or a major subsystem cannot continue safely.

## Exception logging

Where an exception is logged: `rules/backend/error-handling.md` § Unexpected failures. Exception flow technique: `aspnet-error-handling`.

## Scopes

```csharp
using (logger.BeginScope(
    new Dictionary<string, object?>
    {
        ["OrderId"] = orderId
    }))
{
    await ProcessOrderAsync(orderId, cancellationToken);
}
```

Providers enrich scopes differently; Serilog's `LogContext` is covered in `references/serilog.md`.

## Correlation

Prefer platform/runtime trace identifiers when they already correlate requests adequately. Add an explicit correlation identifier only for an integration or operational requirement; validate or normalize an identifier accepted from an external client before propagating it, and propagate tracing context across outbound calls with the project's chosen tracing or HTTP infrastructure.

## Sensitive data and payloads

Never-log data is defined in `rules/common/security.md`; in practice also keep authorization headers and full request/response bodies out of logs.

```csharp
// Avoid: credentials in a log event
logger.LogInformation("Login: {Email} with password {Password}", email, password);

// Prefer: a non-sensitive technical identifier
logger.LogInformation("Login completed for user {UserId}", userId);
```

Logging specific properties instead of whole objects reduces accidental secret/PII exposure, huge events, serialization cost and fragile log schemas.

## Performance

Normal structured `ILogger` calls suffice for most code. For measured high-volume hot paths, consider source-generated `LoggerMessage` APIs (zero allocations when the level is disabled); not everywhere by default.

```csharp
public static partial class OrderLogs
{
    [LoggerMessage(Level = LogLevel.Information,
        Message = "Order {OrderId} created for {CustomerId}")]
    public static partial void OrderCreated(this ILogger logger, Guid orderId, Guid customerId);
}
```

## Common mistakes

String interpolation in log calls; duplicate exception logging; expected outcomes logged as errors; credentials or secrets in logs; whole objects dumped without review; provider-specific APIs spread through Application code; logs used as an audit database without a dedicated audit design.

## Decision guide

| Scenario | Technique |
|---|---|
| Application logging API | `ILogger<T>` |
| Context shared across log entries | `BeginScope` |
| Unexpected handled exception | Log once at the handling boundary |
| Expected business rejection | No Error log |
| Serilog setup, sinks, enrichers | `references/serilog.md` |
| High-volume measured hot path | `LoggerMessage` source generator |
