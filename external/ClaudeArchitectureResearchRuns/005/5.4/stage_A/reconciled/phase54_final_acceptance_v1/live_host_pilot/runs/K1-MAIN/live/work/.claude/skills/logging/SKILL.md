---
name: logging
description: >
  Use when adding or reviewing logging: ILogger<T> message templates, log
  levels, BeginScope, correlation IDs, exception logging, sensitive data,
  LoggerMessage, Serilog sinks, enrichers, request logging, LogContext.
---

> Kind: KNW | Scope: backend | Capability: — | Loading: on-demand knowledge

# Logging

Policy: `.claude/rules/backend/operations.md` (structured logging, Serilog integration), `.claude/rules/common/security.md` (sensitive data, payloads), `.claude/rules/backend/api.md` (log exceptions once). Serilog-specific setup: `references/serilog.md`.

## Structured logging

```csharp
logger.LogInformation("Order {OrderId} created for customer {CustomerId}", orderId, customerId);   // structured
logger.LogInformation($"Order {orderId} created for customer {customerId}");                    // avoid: opaque text
```

Stable property names keep logs queryable. Log information that helps diagnose or operate the system.

## Levels

- **Trace/Debug** — detailed troubleshooting diagnostics; never assume sensitive data is safe at these levels.
- **Information** — meaningful application events (a background job completed, an important business operation completed, a lifecycle event); not every internal method call.
- **Warning** — an unexpected or degraded condition the application recovered from (fallback used, retries exhausted but another path succeeded, optional dependency unavailable, unusual handled state).
- **Error** — an operation failed and needs investigation. Expected negative outcomes such as `NotFound` or validation rejection are normally not errors.
- **Critical** — the application or a major subsystem cannot continue safely.

Choose levels by operational meaning, not by how unusual an event feels.

## Exception logging

Log an exception at the boundary that actually handles or terminates the failure; when rethrowing without meaningful handling, normally add no duplicate log. Exception flow: `aspnet-error-handling`.

## Scopes and correlation

```csharp
using (logger.BeginScope(new Dictionary<string, object?> { ["OrderId"] = orderId }))
{
    await ProcessOrderAsync(orderId, cancellationToken);
}
```

Providers enrich scopes differently; provider-specific mechanisms such as Serilog `LogContext` are in the reference. Prefer platform trace identifiers when they already correlate requests; add an explicit correlation identifier only for an integration or operational requirement, validate or normalize one accepted from an external client, and propagate tracing context across outbound calls with the project's tracing or HTTP infrastructure.

## Sensitive data and payloads

Avoid logging authorization headers and full request/response bodies that contain sensitive data; log the specific properties needed for operation and diagnosis. This reduces accidental secret/PII exposure, huge events, serialization cost, and fragile log schemas. Do not rely on log level as a privacy control; prefer stable technical identifiers over personal information.

## Performance

Normal structured `ILogger` calls suffice for most code. For measured high-volume hot paths consider source-generated `LoggerMessage`:

```csharp
public static partial class OrderLogs
{
    [LoggerMessage(Level = LogLevel.Information, Message = "Order {OrderId} created for {CustomerId}")]
    public static partial void OrderCreated(this ILogger logger, Guid orderId, Guid customerId);
}
```

Do not add source-generated logging everywhere to avoid theoretical allocations.

## Anti-patterns

String interpolation in log templates, duplicate exception logging, expected business outcomes logged as errors, dumping full objects without review, provider-specific APIs throughout Application code, and using logs as an audit database unless a dedicated audit design was adopted.

## Decision guide

| Scenario | Default |
|---|---|
| Application logging API | `ILogger<T>` |
| Context shared across entries | `BeginScope` |
| Unexpected handled exception | Log once at the handling boundary |
| Expected business rejection | Usually no Error log |
| Serilog provider setup | `references/serilog.md` |
| Measured high-volume hot path | `LoggerMessage` source generator |
