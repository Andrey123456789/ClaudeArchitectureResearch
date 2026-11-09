---
name: logging
description: >
  Use when adding or reviewing logging: ILogger message templates, levels,
  scopes, correlation, exception logging, LoggerMessage, and Serilog setup,
  sinks, enrichers, request logging.
---

> Owns: logging technique and examples (no policy); private reference references/serilog.md | Scope: backend | Loads: on demand (knowledge skill)

# Logging

Policy owners: logging-call style — `.claude/rules/coding-style.md`;
log-once for exceptions and expected outcomes — `.claude/rules/error-handling.md`;
sensitive data and payload logging — `.claude/rules/security.md`; Serilog
registration — `.claude/rules/architecture.md`. For Serilog configuration
technique read `references/serilog.md`.

Log information that helps diagnose or operate the system, and choose levels by
operational meaning, not by how unusual an event feels.

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

- **Trace / Debug** — detailed diagnostics mainly useful while troubleshooting.
  Debug or Trace does not make sensitive data safe.
- **Information** — normal meaningful events: a background job completed, an
  important business operation completed, a runtime lifecycle event. Avoid
  logging every internal method call.
- **Warning** — an unexpected or degraded condition the application recovered
  from: fallback used, a retry sequence exhausted but another path succeeded, an
  optional dependency unavailable, an unusual but handled state.
- **Error** — an operation failed and needs investigation or attention.
- **Critical** — the application or a major subsystem cannot continue safely.

## Exception Logging

Log an exception where the failure is actually handled or terminated. When
rethrowing without meaningful handling, do not add another log entry.

## Scopes

Use `ILogger.BeginScope` when several entries need shared context:

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

Providers may enrich scopes differently; for Serilog `LogContext` see
`references/serilog.md`.

## Correlation

Prefer platform/runtime trace identifiers when they already provide adequate
request correlation. Add an explicit correlation identifier only when an
integration or operational requirement needs one; validate or normalize an
identifier accepted from an external client before propagating it. Propagate
correlation/tracing context across outbound calls with the project's chosen
tracing or HTTP infrastructure.

## Sensitive Data in Practice

Besides credentials and secrets, watch for authorization headers and full
request/response bodies. Logging the specific properties needed for operation
and diagnosis instead of whole objects reduces accidental secret/PII exposure,
huge log events, serialization cost, and fragile log schemas.

## Performance

Normal structured `ILogger` logging is sufficient for most code. For measured
high-volume logging hot paths, consider source-generated `LoggerMessage` APIs
(example in `references/serilog.md`); do not add them everywhere to avoid
theoretical allocations.

## Anti-Patterns

Avoid putting provider-specific APIs throughout Application code, dumping full
objects without review, and using logs as an audit database unless a dedicated
audit design has been adopted.

## Decision Guide

| Scenario | Default |
|---|---|
| Application logging API | `ILogger<T>` |
| Context shared across logs | `BeginScope` |
| Unexpected handled exception | Log once at the handling boundary |
| Expected business rejection | No Error log |
| Serilog setup, sinks, enrichers | `references/serilog.md` |
| High-volume measured hot path | Consider `LoggerMessage` |
