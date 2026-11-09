---
name: logging
description: >
  Use for logging: ILogger<T> templates, levels, scopes, correlation, exception
  logging, sensitive data; Serilog setup, sinks, enrichers, request logging.
---
> Level: 2-technology | Owns: logging technique (ILogger and Serilog) | Scope: backend | Loads: on demand (skill)

# Logging

Policy: `hosting.md` (structured `ILogger<T>`), `error-handling.md` (log
unexpected exceptions once), `security.md` (secrets, PII, payloads),
`backend-technologies.md` (Serilog registration). Serilog depth:
`references/serilog.md` — read it when configuring the provider.

## Structured logging

```csharp
logger.LogInformation(
    "Order {OrderId} created for customer {CustomerId}",
    orderId,
    customerId);
```

Not `logger.LogInformation($"Order {orderId} created ...")` — interpolation
destroys the structure. Keep property names stable so logs stay queryable.

## Log levels

- **Trace/Debug** — detailed troubleshooting diagnostics; not a safe place for
  sensitive data.
- **Information** — meaningful application events (a background job completed,
  an important business operation completed, lifecycle events); not every
  method call.
- **Warning** — unexpected or degraded but recovered conditions (fallback used,
  optional dependency unavailable, unusual but handled state).
- **Error** — an operation failed and needs attention. Expected negative
  outcomes (not found, validation rejection) are not errors.
- **Critical** — the application or a major subsystem cannot continue safely.

## Exception logging

Log at the boundary that actually handles or terminates the failure; when
rethrowing without meaningful handling, do not add another log entry.

## Scopes

```csharp
using (logger.BeginScope(new Dictionary<string, object?> { ["OrderId"] = orderId }))
{
    await ProcessOrderAsync(orderId, cancellationToken);
}
```

Providers enrich scopes differently; Serilog `LogContext`: private reference.

## Correlation

Prefer the platform/runtime trace identifiers (`Activity`, `HttpContext.TraceIdentifier`)
when they provide adequate request correlation. Add an explicit correlation
identifier only for an integration or operational requirement, validate or
normalize one received from a client before propagating it, and propagate
tracing context across outbound calls with the project's chosen tracing or HTTP
infrastructure.

## Sensitive data and payloads

Avoid logging authorization headers and full request/response bodies; log the
specific properties needed for operation and diagnosis. This avoids accidental
secret/PII exposure, huge events, serialization cost, and fragile log schemas.

## Performance

Ordinary structured logging is sufficient for most code. For a measured
high-volume hot path, consider source-generated `[LoggerMessage]` methods:

```csharp
public static partial class OrderLogs
{
    [LoggerMessage(Level = LogLevel.Information,
        Message = "Order {OrderId} created for {CustomerId}")]
    public static partial void OrderCreated(this ILogger logger, Guid orderId, Guid customerId);
}
```

## Anti-patterns

String interpolation in log templates; duplicate exception logging; expected
outcomes logged as errors; credentials or secrets in logs; dumping whole objects
without review; provider-specific APIs throughout use-case code; logs used as an
audit database without an adopted audit design.

## Decision guide

| Scenario | Default |
|---|---|
| Application logging API | `ILogger<T>` |
| Shared context across entries | `BeginScope` |
| Unexpected handled exception | Log once at the handling boundary |
| Expected business rejection | No Error log |
| Provider setup, sinks, enrichers | `references/serilog.md` |
| Measured high-volume hot path | `[LoggerMessage]` |
