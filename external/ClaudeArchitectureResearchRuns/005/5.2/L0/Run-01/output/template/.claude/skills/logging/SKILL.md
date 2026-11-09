---
name: logging
description: >
  Use for .NET logging: ILogger templates, levels, scopes, correlation, LoggerMessage, and Serilog setup, sinks, enrichers, request logging.
---

> Level: 2 Technology | Owns: ILogger and Serilog technique | Scope: backend | Loads: knowledge skill (on demand) | Depends on: 0-core/logging-principles.md, 2-technology/logging.md

# Logging Technique

Policy owners (routing): sensitive data and payloads →
`0-core/logging-principles.md`; `ILogger<T>` and Serilog integration →
`2-technology/logging.md`; log-once boundary → `1-architecture/outcomes.md`.
Serilog depth: read `references/serilog.md` when configuring the provider.

## Message Templates

```csharp
logger.LogInformation(
    "Order {OrderId} created for customer {CustomerId}", orderId, customerId);

// Avoid: interpolation flattens structure and allocates even when disabled
logger.LogInformation($"Order {orderId} created for customer {customerId}");
```

Use stable property names so logs stay queryable.

## Levels

- **Trace/Debug** — troubleshooting detail; not a safe place for sensitive data.
- **Information** — meaningful events (job completed, important business
  operation, lifecycle); not every method call.
- **Warning** — unexpected or degraded but recovered (fallback used, optional
  dependency unavailable, unusual handled state).
- **Error** — an operation failed and needs attention; expected business
  rejections (`NotFound`, validation) are normally not errors.
- **Critical** — the application or a major subsystem cannot continue safely.

## Scopes and Correlation

```csharp
using (logger.BeginScope(new Dictionary<string, object?> { ["OrderId"] = orderId }))
{
    await ProcessOrderAsync(orderId, cancellationToken);
}
```

Prefer the platform's trace identifiers for request correlation; add an
explicit correlation id only for an integration or operational need, validate
or normalize one received from a client, and propagate context across outbound
calls with the project's tracing or HTTP infrastructure.

## Hot Paths

Normal structured logging is enough for most code. For a measured high-volume
path, use source-generated logging:

```csharp
public static partial class OrderLogs
{
    [LoggerMessage(Level = LogLevel.Information, Message = "Order {OrderId} created for {CustomerId}")]
    public static partial void OrderCreated(this ILogger logger, Guid orderId, Guid customerId);
}
```

## Avoid

Error-level logs for expected outcomes, dumping
whole objects without review, provider-specific APIs throughout Application
code, and using logs as an audit database without an adopted audit design.
