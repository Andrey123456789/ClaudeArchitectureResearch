---
name: logging
description: >
  Use for .NET logging: ILogger message templates, log levels, scopes,
  correlation, exception logging, sensitive data, LoggerMessage, Serilog
  setup, sinks, enrichers, request logging.
---

> Knowledge skill · Logging technique · Policy: `.claude/rules/composition.md` § Logging, `.claude/rules/security.md` § Logging and Sensitive Data, `.claude/rules/error-handling.md` § Exception Logging · Serilog depth: `references/serilog.md`

# Logging

Log information that helps diagnose or operate the system, and choose log
levels by operational meaning, not by how unusual an event feels.

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

## Log Levels

- **Trace / Debug** — detailed diagnostics for troubleshooting (sensitive-data
  rules apply at every level: `security.md`).
- **Information** — normal meaningful events: a background job completed, an
  important business operation completed, a runtime lifecycle event. Avoid
  logging every internal method call.
- **Warning** — an unexpected or degraded condition the application recovered
  from: fallback used, retry sequence exhausted but another path succeeded,
  optional dependency unavailable, unusual but handled state.
- **Error** — an operation failed and needs investigation (which outcomes are
  not errors: `error-handling.md` § Exception Logging).
- **Critical** — the application or a major subsystem cannot continue safely.

## Exception Logging

Log an exception at the boundary that actually handles or terminates the
failure; when rethrowing without meaningful handling, do not add another log.
Exception-flow technique: `aspnet-error-handling` skill.

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

Providers enrich scopes differently; for Serilog `LogContext` see
`references/serilog.md`.

## Correlation

Prefer platform/runtime trace identifiers when they already provide adequate
request correlation. Add an explicit correlation identifier only when an
integration or operational requirement needs one; validate or normalize an
identifier accepted from an external client before propagating it. Propagate
correlation/tracing context across outbound calls with the project's chosen
tracing or HTTP infrastructure.

## Sensitive Data and Payloads

Beyond the never-log list in `security.md`, avoid logging authorization headers
and full request/response bodies that contain sensitive data. Log the specific
properties needed for operation and diagnosis; this reduces accidental
secret/PII exposure, huge log events, serialization cost, and fragile log
schemas.

## Performance

Normal `ILogger` structured logging is sufficient for most code. For measured
high-volume hot paths consider source-generated `LoggerMessage` APIs; do not
add them everywhere to avoid theoretical allocations.

## Review Checks

Check-by-reference against the policy owners above: string interpolation in
structured logs; duplicate exception logging; expected business outcomes logged
as errors; credentials or secrets logged; full objects dumped without review;
provider-specific APIs spread through Application code; logs used as an audit
database without a dedicated audit design.

## Decision Guide

| Scenario | Default |
|---|---|
| Application logging API | `ILogger<T>` |
| Context shared across logs | `BeginScope` |
| Unexpected handled exception | Log once at the handling boundary |
| Expected business rejection | No Error log |
| Serilog provider setup | `references/serilog.md` |
| High-volume measured hot path | Consider `LoggerMessage` |
