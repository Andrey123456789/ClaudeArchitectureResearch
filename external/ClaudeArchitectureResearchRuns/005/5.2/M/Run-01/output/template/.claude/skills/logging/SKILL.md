---
name: logging
description: >
  Use when writing or reviewing logging: ILogger message templates, levels,
  scopes, correlation, LoggerMessage, and Serilog setup (AddSerilog, sinks,
  enrichers, request logging).
---

> Knowledge skill. Owns: logging technique and examples; Serilog depth through its private reference · Scope: backend · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/error-handling.md, .claude/rules/security.md

# Logging

Rules: `error-handling.md` (structured templates, log exceptions once, Serilog
registration) and `security.md` (sensitive data and payloads). Serilog-specific
configuration, sinks, enrichers, and request logging: read
`references/serilog.md`.

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

Choose levels by operational meaning, not by how unusual an event feels.

- **Trace / Debug** — detailed diagnostics for troubleshooting. Sensitive data
  is not safe merely because the level is Debug or Trace.
- **Information** — normal meaningful events: a background job completed, an
  important business operation completed, a lifecycle event. Do not log every
  internal method call.
- **Warning** — an unexpected or degraded condition the application recovered
  from: a fallback used, a retry sequence exhausted but another path succeeded,
  an optional dependency unavailable, an unusual but handled state.
- **Error** — an operation failed and needs investigation. Expected negative
  business outcomes such as `NotFound` or validation rejection are not
  application errors.
- **Critical** — the application or a major subsystem cannot continue safely.

## Exception Logging

Which boundary logs an exception, and only once: `error-handling.md`. A layer
that rethrows without meaningful handling therefore leaves logging to the
handling boundary. Exception-flow technique: `aspnet-error-handling` skill.

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

Providers may enrich scopes differently; Serilog `LogContext` is covered in the
reference.

## Correlation

Prefer platform/runtime trace identifiers when they already provide adequate
request correlation. Add an explicit correlation identifier only when an
integration or operational requirement needs one; validate or normalize a
correlation identifier accepted from an external client before propagating it.
Propagate tracing context across outbound calls through the project's chosen
tracing or HTTP infrastructure.

## What to Log Instead of Payloads

Log the specific properties needed for operation and diagnosis rather than
whole objects or request bodies. This reduces accidental secret/PII exposure,
huge log events, serialization cost, and fragile log schemas. Avoid
authorization headers and full request/response bodies that carry sensitive
data.

## Performance

Ordinary structured `ILogger` calls are sufficient for most code. For measured
high-volume hot paths, consider source-generated `LoggerMessage` APIs; do not
add them everywhere to avoid theoretical allocations.

## Anti-Patterns

- string interpolation in structured logs;
- duplicate exception logging;
- logging expected business outcomes as errors;
- dumping full objects without review;
- provider-specific APIs throughout Application code;
- using logs as an audit database unless a dedicated audit design was adopted.

## Decision Guide

| Scenario | Default |
|---|---|
| Application logging API | `ILogger<T>` |
| Context shared across entries | `BeginScope` |
| Unexpected handled exception | Log once at the handling boundary |
| Expected business rejection | No Error log |
| Serilog setup | `references/serilog.md` |
| High-volume measured hot path | Consider `LoggerMessage` |
