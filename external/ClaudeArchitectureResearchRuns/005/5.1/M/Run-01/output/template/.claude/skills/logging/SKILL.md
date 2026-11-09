---
name: logging
description: >
  Use when adding, reviewing, or troubleshooting application logging: ILogger
  message templates, log levels, scopes, correlation, exception logging
  placement, LoggerMessage source generation, or Serilog setup (bootstrap,
  sinks, enrichers, request logging, LogContext) via its reference.
---

> Owns: logging technique (ILogger and Serilog) | Scope: backend | Loads: on demand (knowledge skill); private reference references/serilog.md

# Logging

Policy owners: log-once, structured templates, Serilog registration →
`.claude/rules/error-handling.md` (Logging); secrets, PII, and payload logging →
`.claude/rules/security.md`; provider choice → `docs/technology-stack.md`.
Serilog configuration technique: `references/serilog.md`.

## Message Templates

```csharp
logger.LogInformation(
    "Order {OrderId} created for customer {CustomerId}", orderId, customerId);

// Avoid: interpolation flattens properties into text
logger.LogInformation($"Order {orderId} created for customer {customerId}");
```

Keep property names stable (`OrderId`, not `Id` here and `OrderID` there) so
logs remain queryable.

## Choosing Levels

| Level | Use for |
|---|---|
| Trace / Debug | Detailed troubleshooting diagnostics (level is no privacy control: `security.md`) |
| Information | Meaningful application events: job completed, important business operation completed, lifecycle events — not every method call |
| Warning | Unexpected or degraded but recovered: fallback used, optional dependency unavailable, unusual handled state |
| Error | An operation failed and needs attention; expected rejections (not found, validation) are not errors |
| Critical | The application or a major subsystem cannot continue safely |

## Where Exceptions Are Logged

The boundary that handles or terminates the failure logs it — usually the global
exception handler for unexpected API failures. When rethrowing without
meaningful handling, add no log. Exception flow: `aspnet-error-handling`.

## Scopes

```csharp
using (logger.BeginScope(new Dictionary<string, object?> { ["OrderId"] = orderId }))
{
    await ProcessOrderAsync(orderId, cancellationToken);
}
```

Providers enrich scopes differently; Serilog `LogContext` is in the reference.

## Correlation

Prefer platform trace identifiers (`Activity.Current`, `HttpContext.TraceIdentifier`)
when they already correlate requests. Add an explicit correlation identifier only
for an integration or operational requirement; validate or normalize one
received from an external client before propagating it. Propagate tracing
context on outbound calls through the project's chosen tracing/HTTP
infrastructure.

## Hot Paths

Ordinary structured `ILogger` calls are sufficient for most code. For measured
high-volume paths, use source-generated logging:

```csharp
public static partial class OrderLogs
{
    [LoggerMessage(Level = LogLevel.Information, Message = "Order {OrderId} created for {CustomerId}")]
    public static partial void OrderCreated(this ILogger logger, Guid orderId, Guid customerId);
}
```

Do not add it everywhere to avoid theoretical allocations.

## Pitfalls

Provider-specific APIs scattered through Application code; dumping full objects
without review; using logs as an audit database without a dedicated audit design.
