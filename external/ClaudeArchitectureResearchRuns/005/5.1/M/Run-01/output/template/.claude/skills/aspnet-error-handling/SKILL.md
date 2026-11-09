---
name: aspnet-error-handling
description: >
  Use when implementing IExceptionHandler, ProblemDetails responses, controller
  error mapping, expected application outcomes or an optional Result type,
  FluentValidation validators and their registration, or exception catching in
  ASP.NET Core code.
---

> Owns: ASP.NET Core exception-handling, outcome, and validation technique | Scope: backend | Loads: on demand (knowledge skill)

# ASP.NET Core Error Handling

Policy owners: outcomes, exception flow, validation boundaries, cancellation,
logging once → `.claude/rules/error-handling.md`; status semantics and public
error contracts → `.claude/rules/api.md`. Status-code reference: `http-api`.

## Global Exception Handler

```csharp
internal sealed class GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger)
    : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext, Exception exception, CancellationToken cancellationToken)
    {
        // Client aborted the request: not a server failure.
        if (exception is OperationCanceledException &&
            httpContext.RequestAborted.IsCancellationRequested)
        {
            httpContext.Response.StatusCode = StatusCodes.Status499ClientClosedRequest;
            return true;
        }

        logger.LogError(exception,
            "Unhandled exception while processing {Method} {Path}",
            httpContext.Request.Method, httpContext.Request.Path);

        await Results.Problem(
                statusCode: StatusCodes.Status500InternalServerError,
                title: "An unexpected error occurred")
            .ExecuteAsync(httpContext);

        return true;
    }
}
```

```csharp
builder.Services.AddProblemDetails();
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
app.UseExceptionHandler();
```

Development diagnostics may show more through development tooling; the public
contract stays safe.

## Expected Outcomes

Simple query: `null` is often enough.

```csharp
Task<OrderDto?> GetByIdAsync(Guid id, CancellationToken cancellationToken);
```

Command with several meaningful outcomes: an explicit typed outcome.

```csharp
public enum CancelOrderOutcome { Cancelled, NotFound, AlreadyCompleted }
```

## Controller Mapping

```csharp
[HttpGet("{id:guid}")]
public async Task<ActionResult<OrderResponse>> GetById(Guid id, CancellationToken cancellationToken)
{
    var order = await orders.GetByIdAsync(id, cancellationToken);
    if (order is null)
        return Problem(statusCode: StatusCodes.Status404NotFound, title: "Order not found");

    return Ok(order);
}
```

## ProblemDetails Content

A useful contract may carry: status, a stable machine-readable error code when
clients need one (for example in `extensions["code"]`), a human-readable title,
a safe detail, and a trace/correlation identifier.

## Optional Result Pattern

Consider `Result<T>` when an operation has several expected failure modes,
callers benefit from typed outcomes, and the project will use it consistently
(project-wide adoption is Reserved). Avoid it when `null`, `bool`, or a small
typed response is clear, or when it only wraps straightforward CRUD. If adopted,
use typed errors rather than string arrays:

```csharp
public sealed record AppError(string Code, string Message);
```

## Request Validation

`[ApiController]` handles model-binding failures and produces validation problem
responses. Use FluentValidation for explicit request/use-case rules (required
input, string/collection constraints, ranges, cross-property and conditional
rules), registered with `FluentValidation.DependencyInjectionExtensions`:

```csharp
services.AddValidatorsFromAssemblyContaining<CreateOrderRequestValidator>();
```

Follow the project's established invocation pattern (for example validating in
the Application service or a controller helper) rather than adding a competing
mechanism or a legacy automatic-validation package. Do not couple validation to
Minimal API endpoint filters in a Controller-based project.

## Catching Exceptions

Valid reasons to catch: recover; translate into a meaningful outcome at this
abstraction level; required cleanup; add context while preserving the original
exception; a defined fallback or infrastructure-boundary retry. Anti-examples:

```csharp
try { await service.ProcessAsync(cancellationToken); }
catch (Exception) { }                       // swallows the failure

catch (Exception ex)
{
    logger.LogError(ex, "Failed");          // duplicate logging when the global
    throw;                                  // handler already owns it
}
```

Typed exceptions for selected cases are a deliberate, consistent project-level
choice (`error-handling.md`).
External-service exceptions are caught locally only when this layer can do
something meaningful; otherwise they propagate to centralized handling.

## Decision Guide

| Need | Mechanism |
|---|---|
| Binding/model-state failure | `[ApiController]` automatic `ValidationProblemDetails` |
| Explicit request/use-case validator | FluentValidation `AbstractValidator<T>` + `AddValidatorsFromAssemblyContaining` |
| Simple query not found | `null` result → `Problem(statusCode: 404)` in the Controller |
| Several expected business outcomes | Typed outcome enum/record, or the adopted Result type |
| Centralized unexpected-failure handling | `IExceptionHandler` + `AddProblemDetails()` + `UseExceptionHandler()` |
| Client-aborted request detection | `OperationCanceledException` + `HttpContext.RequestAborted` |
