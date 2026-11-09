---
name: logging
description: Application logging technique with ILogger<T>. Use when adding, reviewing, or troubleshooting logs — message templates, log levels, BeginScope, correlation IDs, exception logging, LoggerMessage source generation — and for Serilog setup (AddSerilog, sinks, enrichers, request logging, LogContext) via its reference.
---

> Level: 2-technology · Owns: logging technique; Serilog depth in `references/serilog.md` · Loading: on demand

# Logging

Rules: structured logging and sensitive-data/payload rules (`.claude/rules/0-core/backend-code.md`, `.claude/rules/0-core/security.md`), log-once rule (`.claude/rules/0-core/http-api.md`), Serilog integration rule (`.claude/rules/2-technology/backend-libraries.md`). Serilog-specific setup: `references/serilog.md`.

## Message templates

```csharp
logger.LogInformation("Order {OrderId} created for customer {CustomerId}", orderId, customerId);   // structured
logger.LogInformation($"Order {orderId} created for customer {customerId}");                       // opaque text
```

## Levels

- **Trace/Debug** — detailed troubleshooting diagnostics (still never a safe place for sensitive data).
- **Information** — meaningful application events: a background job completed, an important business operation finished, lifecycle events. Not every method call.
- **Warning** — unexpected or degraded but recovered: fallback used, optional dependency unavailable, unusual handled state.
- **Error** — an operation failed and needs attention. Expected business outcomes such as `NotFound` or validation rejection are normally not errors.
- **Critical** — the application or a major subsystem cannot continue safely.

## Exceptions

Log at the boundary that actually handles or terminates the failure; when rethrowing without meaningful handling, do not add another log. Exception-flow technique: `aspnet-error-handling`.

## Scopes and correlation

```csharp
using (logger.BeginScope(new Dictionary<string, object?> { ["OrderId"] = orderId }))
{
    await ProcessOrderAsync(orderId, cancellationToken);
}
```

Prefer platform trace identifiers when they already correlate requests; add an explicit correlation id only for a concrete integration or operational need, validate or normalize ids accepted from clients, and propagate tracing context across outbound calls with the chosen tracing/HTTP infrastructure.

## Payloads

Log the specific properties needed for operation and diagnosis instead of serialized objects or bodies — this avoids secret/PII exposure, huge events, serialization cost, and fragile schemas. Avoid authorization headers and full request/response bodies containing sensitive data; prefer stable technical identifiers over personal data.

## Performance

Normal `ILogger` structured logging suffices for most code. For measured high-volume hot paths, use source-generated logging:

```csharp
public static partial class OrderLogs
{
    [LoggerMessage(Level = LogLevel.Information, Message = "Order {OrderId} created for {CustomerId}")]
    public static partial void OrderCreated(this ILogger logger, Guid orderId, Guid customerId);
}
```

## Anti-patterns

Interpolated log messages; duplicate exception logging; expected outcomes logged as errors; credentials or secrets in logs; dumping whole objects without review; provider-specific APIs throughout use-case code; logs used as an audit database without an adopted audit design.

## Decision guide

| Scenario | Default |
| --- | --- |
| Logging API | `ILogger<T>` |
| Shared context across entries | `BeginScope` (Serilog: `LogContext`) |
| Unexpected handled exception | log once at the handling boundary |
| Expected business rejection | usually no Error log |
| Provider setup | `references/serilog.md` |
| Measured hot path | `LoggerMessage` source generator |
