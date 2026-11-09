---
name: logging
description: >
  Logging: ILogger<T> message templates, levels, BeginScope, correlation,
  exception logging, LoggerMessage, Serilog setup (AddSerilog, sinks, enrichers,
  request logging).
---

> **Knowledge skill** · Owns: logging technique and examples (Serilog depth in `references/serilog.md`) · Scope: backend · Loading: on demand

# Logging

## Rules

Rules: `backend-runtime.md` → Logging (structured `ILogger<T>` logging, Serilog
integration), `error-handling.md` → Logging (log an unexpected exception once),
and `security.md` → Logging and Sensitive Data. This skill shows how to apply
them.

Log information that helps diagnose or operate the system, and choose log levels
by operational meaning, not by how unusual an event feels.

## Structured Logging

```csharp
logger.LogInformation(
    "Order {OrderId} created for customer {CustomerId}",
    orderId,
    customerId);
```

Avoid:

```csharp
logger.LogInformation(
    $"Order {orderId} created for customer {customerId}");
```

Stable property names keep logs queryable.

## Log Levels

### Trace / Debug

Detailed diagnostic information primarily useful during troubleshooting.

Do not assume sensitive data is safe simply because the level is Debug or Trace.

### Information

Normal meaningful application events.

Examples:

- a background job completed;
- an important business operation completed;
- a deployment/runtime lifecycle event occurred.

Avoid logging every internal method call.

### Warning

An unexpected or degraded condition from which the application recovered.

Examples:

- fallback used;
- retry sequence exhausted but another path succeeded;
- optional dependency unavailable;
- unusual but handled state.

### Error

An operation failed and requires investigation or meaningful attention.

Expected negative business outcomes such as `NotFound` or validation rejection
are normally not application errors.

### Critical

The application or a major subsystem cannot continue safely.

## Exception Logging

Log an exception at the boundary that actually handles or terminates the failure
(`error-handling.md` → Logging); when rethrowing without meaningful handling, add
no duplicate log. Exception-flow technique: the `aspnet-error-handling` skill.

## Scopes

Use `ILogger.BeginScope` when several log entries need shared contextual data.

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

Logging providers may enrich these scopes differently.

For provider-specific mechanisms such as Serilog `LogContext`, see
`references/serilog.md`.

## Correlation

Prefer platform/runtime trace identifiers when they already provide adequate
request correlation.

Add an explicit correlation identifier only when an integration or operational
requirement needs one.

When a correlation identifier is accepted from an external client, validate or
normalize it before propagating it.

Propagate correlation/tracing context across outbound calls using the project's
chosen tracing or HTTP infrastructure.

## Sensitive Data

Rules: `security.md` → Logging and Sensitive Data. Values that commonly slip in:
authorization headers, full request/response bodies, and token-bearing URLs.

## Payload Logging

Rule: `security.md` → Logging and Sensitive Data. Logging specific properties
instead of whole objects avoids accidental secret/PII exposure, huge log events,
serialization cost, and fragile log schemas.

## Performance

Normal `ILogger` structured logging is sufficient for most code.

For measured high-volume logging hot paths, consider source-generated
`LoggerMessage` APIs.

Do not add source-generated logging everywhere merely to avoid theoretical
allocations.

## Provider-Specific Configuration

Application code depends on `ILogger<T>` (`backend-runtime.md`). For Serilog,
read `references/serilog.md` for:

- bootstrap configuration;
- sinks;
- enrichers;
- request logging;
- provider-specific filtering;
- `LogContext`.

## Anti-Patterns

Avoid:

- logging expected business outcomes as errors;
- dumping full objects without review;
- putting provider-specific APIs throughout Application code;
- using logs as an audit database unless a dedicated audit design has been adopted.

## Decision Guide

| Scenario | Default |
|---|---|
| Application logging API | `ILogger<T>` |
| Context shared across logs | `BeginScope` |
| Unexpected handled exception | Log once at handling boundary |
| Expected business rejection | Usually no Error log |
| Provider-specific Serilog setup | `references/serilog.md` |
| High-volume measured hot path | Consider `LoggerMessage` |
