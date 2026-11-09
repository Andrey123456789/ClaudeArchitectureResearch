---
name: logging
description: >
  Use when adding, reviewing or configuring logging or Serilog: ILogger<T>
  message templates, levels, scopes, correlation, LoggerMessage, Serilog
  bootstrap, sinks, enrichers, request logging.
---

> Level: 2 Technology · Owns: logging technique (private reference: Serilog) · Scope: backend · Loads: on demand (knowledge skill)

# Logging

Policy owners: `.claude/rules/0-core/logging-principles.md` (sensitive data, payloads, log-once), `.claude/rules/2-technology/csharp.md` (`ILogger<T>` with structured templates), `.claude/rules/2-technology/aspnet-core.md` (Serilog host integration). Serilog configuration depth: `references/serilog.md`.

## Structured templates

```csharp
logger.LogInformation("Order {OrderId} created for customer {CustomerId}", orderId, customerId);   // structured

logger.LogInformation($"Order {orderId} created for customer {customerId}");                       // opaque text
```

Stable property names (`OrderId`, not `orderID` in one place and `Id` in another) keep logs queryable.

## Log levels

| Level | Meaning |
|---|---|
| Trace / Debug | detailed diagnostics for troubleshooting — not a safe place for sensitive data |
| Information | meaningful application events (job completed, important business operation, lifecycle event) — not every method call |
| Warning | unexpected or degraded condition the application recovered from (fallback used, optional dependency unavailable, unusual handled state) |
| Error | an operation failed and needs investigation — expected negative outcomes such as not-found or validation rejection are typically not errors |
| Critical | the application or a major subsystem cannot continue safely |

## Exception logging placement

Log where the failure is handled or terminated (typically the global exception handler). When rethrowing without meaningful handling, add no log of your own. Exception-flow technique: `aspnet-error-handling` skill.

## Scopes

```csharp
using (logger.BeginScope(new Dictionary<string, object?> { ["OrderId"] = orderId }))
{
    await ProcessOrderAsync(orderId, cancellationToken);
}
```

Providers render scopes differently; Serilog's `LogContext` is described in the reference.

## Correlation

Platform trace identifiers (`Activity.Current`, `HttpContext.TraceIdentifier`) usually provide request correlation. Add an explicit correlation id only for an integration or operational requirement; validate or normalize an id accepted from a client before propagating it; propagate tracing context across outbound calls with the project's tracing or HTTP infrastructure.

## Payloads

Log the specific properties needed for operations and diagnosis instead of serializing whole objects — this limits secret and PII exposure, event size, serialization cost and schema fragility.

## High-volume paths

Ordinary `ILogger` calls suffice for most code. For a measured hot path, use source-generated logging:

```csharp
public static partial class OrderLogs
{
    [LoggerMessage(Level = LogLevel.Information, Message = "Order {OrderId} created for {CustomerId}")]
    public static partial void OrderCreated(this ILogger logger, Guid orderId, Guid customerId);
}
```

## Review cues

Interpolated log messages, the same exception logged in several layers, expected outcomes logged as errors, credentials or tokens in logs, whole objects dumped without review, provider-specific APIs spread through Application code, logs used as an audit database without an adopted audit design.

## Decision guide

| Scenario | Typical choice |
|---|---|
| Application logging API | `ILogger<T>` |
| Context shared across entries | `BeginScope` |
| Unexpected handled exception | Log once at the handling boundary |
| Expected business rejection | Usually no Error log |
| Serilog setup, sinks, enrichers | `references/serilog.md` |
| Measured high-volume path | `[LoggerMessage]` |
