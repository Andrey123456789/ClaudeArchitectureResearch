---
name: logging
description: Use when adding, reviewing or troubleshooting .NET application logging — ILogger<T> message templates, log levels, scopes, correlation, exception logging, sensitive data, LoggerMessage source generation, or Serilog bootstrap, sinks, enrichers and request logging.
---
Kind: KNW | Scope: backend | Capability: — | Loading: on invocation

# Logging

Rules: `.claude/rules/backend/operations.md` (structured logging, Serilog integration), `.claude/rules/common/security.md` (sensitive data and payloads in logs), `.claude/rules/backend/error-handling.md` (log unexpected exceptions once). Serilog configuration depth: `references/serilog.md` (read it when configuring Serilog).

## Structured logging

```csharp
logger.LogInformation(
    "Order {OrderId} created for customer {CustomerId}",
    orderId,
    customerId);
```

Not:

```csharp
logger.LogInformation($"Order {orderId} created for customer {customerId}");
```

Log information that helps diagnose or operate the system, with stable property names so logs stay queryable. Interpolation also allocates the message even when the level is disabled.

## Log levels

Choose levels by operational meaning, not by how unusual an event feels.

- **Trace / Debug**: detailed diagnostics for troubleshooting. A low level is not a privacy control.
- **Information**: meaningful application events (a background job completed, an important business operation completed, a lifecycle event). Do not log every internal method call.
- **Warning**: an unexpected or degraded condition the application recovered from (fallback used, retries exhausted but another path succeeded, optional dependency unavailable, unusual but handled state).
- **Error**: an operation failed and needs investigation. Expected negative business outcomes such as not found or a validation rejection are normally not application errors.
- **Critical**: the application or a major subsystem cannot continue safely.

## Exception logging

Log an exception at the boundary that actually handles or terminates the failure; when rethrowing without meaningful handling, do not add another log entry. Exception flow: `aspnet-error-handling` skill.

## Scopes

Use `ILogger.BeginScope` when several entries share contextual data:

```csharp
using (logger.BeginScope(new Dictionary<string, object?> { ["OrderId"] = orderId }))
{
    await ProcessOrderAsync(orderId, cancellationToken);
}
```

Providers enrich scopes differently; Serilog's `LogContext` is in the Serilog reference.

## Correlation

Prefer the platform's trace identifiers when they already provide adequate request correlation. Add an explicit correlation identifier only when an integration or operational requirement needs one; validate or normalize a correlation identifier accepted from an external client before propagating it. Propagate correlation and tracing context across outbound calls with the project's chosen tracing or HTTP infrastructure.

## What to log instead of payloads

Log the specific properties needed for operation and diagnosis instead of whole objects. This avoids accidental secret or PII exposure, huge events, serialization cost and fragile log schemas. Authorization headers and request or response bodies are typical carriers of data on the never-log list (`.claude/rules/common/security.md` → Sensitive data in logs).

## Performance

Normal structured `ILogger` calls suffice for most code. For a measured high-volume hot path, consider source-generated `[LoggerMessage]` methods (built into Microsoft.Extensions.Logging.Abstractions, generated at compile time, no allocation when the level is disabled):

```csharp
public static partial class OrderLogs
{
    [LoggerMessage(Level = LogLevel.Information, Message = "Order {OrderId} created for {CustomerId}")]
    public static partial void OrderCreated(this ILogger logger, Guid orderId, Guid customerId);
}
```

Do not add source-generated logging everywhere to avoid theoretical allocations.

## Anti-patterns

Review checks; the named standard owns each rule:

- String interpolation in log calls? (`operations.md`)
- The same exception logged at several layers? (`error-handling.md`)
- Expected business outcomes logged as errors?
- Credentials, secrets or whole objects in logs? (`.claude/rules/common/security.md`)
- Provider-specific logging APIs spread through Application code? (`operations.md`)
- Logs used as an audit database without an adopted audit design?
