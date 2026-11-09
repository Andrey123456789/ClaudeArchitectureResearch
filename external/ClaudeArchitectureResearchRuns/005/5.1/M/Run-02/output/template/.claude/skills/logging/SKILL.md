---
name: logging
description: >
  Use when adding or reviewing logging: ILogger<T> message templates, levels,
  scopes, correlation, exception logging, LoggerMessage, or Serilog setup
  (bootstrap logger, AddSerilog, sinks, enrichers, request logging,
  LogContext).
---

> Owner: logging technique; Serilog depth in a private reference (normative policy lives in rules) | Scope: backend | Loads: on demand — knowledge | Enforced: none

# Logging

Policy: `.claude/rules/coding-style.md` § Logging Calls (structured templates,
Serilog registration), `.claude/rules/error-handling.md` § Unexpected Exceptions
(log once), `.claude/rules/security.md` § Logging and Sensitive Data. Serilog
provider setup: `references/serilog.md`.

## Structured Logging

```csharp
logger.LogInformation(
    "Order {OrderId} created for customer {CustomerId}",
    orderId,
    customerId);
```

Not:

```csharp
logger.LogInformation(
    $"Order {orderId} created for customer {customerId}");
```

Stable property names (`OrderId`, `CustomerId`) keep logs queryable across
events. Log what helps diagnose or operate the system.

## Log Levels

Choose levels by operational meaning, not by how unusual an event feels.

- **Trace / Debug** — detailed diagnostics for troubleshooting; the level is not
  a privacy control.
- **Information** — meaningful normal events: a background job completed, an
  important business operation completed, a lifecycle event. Avoid logging every
  internal method call.
- **Warning** — an unexpected or degraded condition the application recovered
  from: fallback used, an optional dependency unavailable, an unusual but handled
  state.
- **Error** — an operation failed and needs investigation. Expected negative
  business outcomes (`NotFound`, validation rejection) are normally not errors.
- **Critical** — the application or a major subsystem cannot continue safely.

## Exception Logging

Log an exception at the boundary that actually handles or terminates the
failure; when rethrowing without meaningful handling, add no duplicate log.
Exception flow: `aspnet-error-handling` skill.

## Scopes

Use `ILogger.BeginScope` when several entries share contextual data:

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

Providers enrich scopes differently; Serilog `LogContext` is covered in
`references/serilog.md`.

## Correlation

- Prefer platform/runtime trace identifiers when they already provide adequate
  request correlation.
- Add an explicit correlation identifier only when an integration or operational
  requirement needs one; validate or normalize identifiers accepted from external
  clients before propagating them.
- Propagate correlation/tracing context across outbound calls with the project's
  chosen tracing or HTTP infrastructure.

## Payload Logging

Log the specific properties needed for operation and diagnosis rather than whole
objects. This avoids accidental secret or PII exposure, huge log events,
serialization cost, and fragile log schemas. Prefer stable technical identifiers
over personal information.

## Performance

Normal `ILogger` structured logging is enough for most code. For measured
high-volume hot paths, consider source-generated `LoggerMessage`:

```csharp
public static partial class OrderLogs
{
    [LoggerMessage(Level = LogLevel.Information,
        Message = "Order {OrderId} created for {CustomerId}")]
    public static partial void OrderCreated(this ILogger logger, Guid orderId, Guid customerId);
}

// Usage
logger.OrderCreated(order.Id, order.CustomerId);
```

Do not add source-generated logging everywhere to avoid theoretical allocations.

## Common Mistakes

- logging expected business outcomes as errors;
- dumping full objects without review;
- provider-specific APIs spread through Application code;
- using logs as an audit database without a dedicated audit design.

## Decision Guide

| Scenario | Technique |
|---|---|
| Application logging API | `ILogger<T>` |
| Context shared across logs | `BeginScope` |
| Unexpected handled exception | Log once at the handling boundary |
| Expected business rejection | Usually no Error log |
| Serilog setup, sinks, enrichers | `references/serilog.md` |
| High-volume measured hot path | `LoggerMessage` source generator |
