---
name: logging
description: Use when adding, reviewing or troubleshooting application logging — ILogger message templates, log levels, scopes, correlation, exception logging placement, payload and sensitive-data choices, LoggerMessage hot paths; includes the Serilog setup reference (bootstrap, sinks, enrichers, request logging).
---
<!-- Kind: KNW | Scope: backend | Owns: logging technique; Serilog setup reference | Loads: on demand (model-invoked) -->
# Logging

Standards: `rules/backend/operations.md` § Logging (ILogger templates, Serilog integration), `rules/common/security.md` § Logging and Sensitive Data, `rules/backend/error-handling.md` (log unexpected exceptions once). Provider decision: DEC-LOG-01. Serilog setup: `references/serilog.md`.

Log information that helps diagnose or operate the system, and choose levels by operational meaning rather than by how unusual an event feels.

## Structured Logging

```csharp
logger.LogInformation(
    "Order {OrderId} created for customer {CustomerId}",
    orderId,
    customerId);
```

instead of

```csharp
logger.LogInformation(
    $"Order {orderId} created for customer {customerId}");
```

Stable property names keep logs queryable.

## Log Levels

- **Trace / Debug** — detailed diagnostics mainly for troubleshooting; the level does not make sensitive data safe.
- **Information** — normal meaningful events: a background job completed, an important business operation completed, a runtime lifecycle event. Avoid logging every internal method call.
- **Warning** — an unexpected or degraded condition the application recovered from: fallback used, retries exhausted but another path succeeded, optional dependency unavailable, unusual but handled state.
- **Error** — an operation failed and needs investigation. Expected negative outcomes such as `NotFound` or validation rejection are normally not errors.
- **Critical** — the application or a major subsystem cannot continue safely.

## Exception Logging

Log an exception at the boundary that actually handles or terminates the failure; when rethrowing without meaningful handling, normally add no log. Exception flow: `aspnet-error-handling` skill.

## Scopes

`ILogger.BeginScope` shares contextual data across several entries:

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

Providers enrich scopes differently; Serilog `LogContext` is in `references/serilog.md`.

## Correlation

Prefer platform/runtime trace identifiers when they already provide adequate request correlation; add an explicit correlation identifier only for an integration or operational requirement. Validate or normalize a correlation identifier accepted from an external client before propagating it, and propagate tracing context across outbound calls with the project's tracing or HTTP infrastructure.

## Sensitive Data and Payloads

Beyond the prohibited values in the security standard, avoid authorization headers and full request/response bodies containing sensitive data. Log the specific properties needed for operation and diagnosis instead of serializing objects — that also avoids huge events, serialization cost and fragile log schemas.

## Performance

Normal structured `ILogger` logging is sufficient for most code. For measured high-volume hot paths consider source-generated `LoggerMessage` APIs (example in `references/serilog.md`); avoid adding them everywhere for theoretical allocations.

## Provider-Specific Configuration

Application code depends on `ILogger<T>`, not on Serilog or another provider. Bootstrap configuration, sinks, enrichers, request logging, provider-specific filtering and `LogContext` are provider concerns: `references/serilog.md`.

## Anti-Patterns

Avoid string interpolation in structured logs, duplicate exception logging, expected business outcomes logged as errors, credentials or secrets in logs, dumping full objects without review, provider-specific APIs throughout Application code, and using logs as an audit database unless a dedicated audit design was adopted.

## Decision Guide

| Scenario | Default |
|---|---|
| Application logging API | `ILogger<T>` |
| Context shared across logs | `BeginScope` |
| Unexpected handled exception | Log once at the handling boundary |
| Expected business rejection | Usually no Error log |
| Provider-specific Serilog setup | `references/serilog.md` |
| High-volume measured hot path | Consider `LoggerMessage` |
