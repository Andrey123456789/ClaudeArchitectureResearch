---
name: logging
description: >
  Use when adding or reviewing logging: ILogger<T> message templates, levels, scopes,
  correlation, exception logging, LoggerMessage, Serilog setup and sinks.
---

> Level: 2 Technology · Owns: logging technique and examples (knowledge) · Scope: backend · Loads: on invocation · Depends on: .claude/rules/0-core/logging-principles.md, .claude/rules/2-technology/logging.md

# Logging

Policy owners: never-log data, payload logging, log-once → `.claude/rules/0-core/logging-principles.md`; `ILogger<T>` templates and Serilog integration → `2-technology/logging.md`; exception flow → `1-architecture/outcomes.md`. Serilog-specific depth: `references/serilog.md`. This skill is technique only.

## Structured logging

```csharp
logger.LogInformation(
    "Order {OrderId} created for customer {CustomerId}",
    orderId,
    customerId);

// Avoid — interpolation turns structured values into opaque text
logger.LogInformation($"Order {orderId} created for customer {customerId}");
```

Keep property names stable so logs remain queryable.

## Log levels

Choose levels by operational meaning:

- **Trace / Debug** — detailed troubleshooting diagnostics (not a safe place for sensitive data).
- **Information** — normal meaningful events: a background job completed, an important business operation completed, a lifecycle event. Do not log every method call.
- **Warning** — an unexpected or degraded condition the application recovered from: fallback used, optional dependency unavailable, unusual but handled state.
- **Error** — an operation failed and needs attention. Expected negative outcomes such as `NotFound` or validation rejection are normally not errors.
- **Critical** — the application or a major subsystem cannot continue safely.

## Exceptions

Log at the boundary that actually handles or terminates the failure; when rethrowing without meaningful handling, normally do not add another log entry.

## Scopes

```csharp
using (logger.BeginScope(new Dictionary<string, object?> { ["OrderId"] = orderId }))
{
    await ProcessOrderAsync(orderId, cancellationToken);
}
```

Providers enrich scopes differently; Serilog `LogContext`: `references/serilog.md`.

## Correlation

Prefer the platform/runtime trace identifiers when they already provide adequate request correlation. Add an explicit correlation identifier only for an integration or operational requirement; validate or normalize identifiers accepted from external clients before propagating them; propagate tracing context across outbound calls with the project's chosen tracing or HTTP infrastructure.

## What to log instead of payloads

Log the specific properties needed for operation and diagnosis (identifiers, counts, states, durations). This avoids accidental secret/PII exposure, huge events, serialization cost, and fragile log schemas. Avoid logging authorization headers and full request/response bodies.

## Hot paths

Normal structured logging is sufficient for most code. For a measured high-volume path, use source-generated logging:

```csharp
public static partial class OrderLogs
{
    [LoggerMessage(Level = LogLevel.Information, Message = "Order {OrderId} created for {CustomerId}")]
    public static partial void OrderCreated(this ILogger logger, Guid orderId, Guid customerId);
}

logger.OrderCreated(order.Id, order.CustomerId);
```

Do not add it everywhere to avoid theoretical allocations.

## Anti-patterns

Logging expected business outcomes as errors; logs used as an audit database without an adopted audit design.

## Decision guide

| Scenario | Technique |
|---|---|
| Application logging API | `ILogger<T>` |
| Context shared across entries | `BeginScope` |
| Unexpected handled exception | `logger.LogError(exception, template, ...)` in the handler that owns it |
| Expected business rejection | usually no Error entry |
| Serilog setup, sinks, enrichers | `references/serilog.md` |
| Measured high-volume path | `[LoggerMessage]` |
