---
name: aspnet-error-handling
description: >
  Use when implementing API error handling or validation: IExceptionHandler,
  ProblemDetails, ValidationProblemDetails, outcome-to-HTTP mapping, Result
  types, FluentValidation placement, try/catch, exception logging.
---

> Kind: KNW | Scope: backend | Capability: — | Loading: on-demand knowledge

# ASP.NET Core Error Handling

Policy: `.claude/rules/backend/api.md`. Status-code semantics: `http-api` (this skill does not repeat them).

## Global exception handler

Unexpected exceptions — programming defects, unexpected database or external-service failures, violated assumptions the application cannot handle locally — propagate to one centralized handler. Treat client-aborted requests separately:

```csharp
internal sealed class GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger) : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        if (exception is OperationCanceledException && httpContext.RequestAborted.IsCancellationRequested)
        {
            httpContext.Response.StatusCode = StatusCodes.Status499ClientClosedRequest;
            return true;
        }

        logger.LogError(
            exception,
            "Unhandled exception while processing {Method} {Path}",
            httpContext.Request.Method,
            httpContext.Request.Path);

        await Results.Problem(
                statusCode: StatusCodes.Status500InternalServerError,
                title: "An unexpected error occurred")
            .ExecuteAsync(httpContext);

        return true;
    }
}

// Program.cs
builder.Services.AddProblemDetails();
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
app.UseExceptionHandler();
```

Development diagnostics may expose more detail through development tooling; public contracts stay safe.

## Expected Application outcomes

Expected outcomes are conditions the application understands: entity not found, transition not allowed, duplicate resource, optimistic concurrency conflict, operation rejected by a known rule. Choose the simplest representation:

```csharp
public Task<OrderDto?> GetByIdAsync(Guid id, CancellationToken cancellationToken);   // null is enough for a simple query
```

A command with several meaningful outcomes may use an explicit typed outcome. Name categories by Application/business semantics — `Validation`, `NotFound`, `Conflict`, `BusinessRuleViolation` — not `BadRequest`, `Unprocessable`, `Unauthorized`, `Forbidden`, or `InternalServerError`, and map them to HTTP in the Api layer.

## Controller mapping

```csharp
[ApiController]
[Route("api/orders")]
public sealed class OrdersController(IOrderService orders) : ControllerBase
{
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<OrderResponse>> GetById(Guid id, CancellationToken cancellationToken)
    {
        var order = await orders.GetByIdAsync(id, cancellationToken);

        if (order is null)
        {
            return Problem(statusCode: StatusCodes.Status404NotFound, title: "Order not found");
        }

        return Ok(order);
    }
}
```

## ProblemDetails contents

A useful error contract may contain the HTTP status, a stable machine-readable error code when clients need one, a human-readable title, a safe detail, and a correlation/trace identifier when appropriate. Human-readable exception messages are never the machine-readable contract.

## Validation placement

With `[ApiController]`, ASP.NET Core handles model-binding failures and produces validation problem responses. FluentValidation expresses explicit rules: required business/application input, string or collection constraints, ranges, cross-property and conditional validation.

```text
API transport/request-contract concern        -> API boundary validation
Application use-case input / workflow rule    -> Application validator or Application Service
Non-trivial invariant genuinely owned by Domain -> Domain model
```

Do not move Domain invariants into FluentValidation merely because the library is available, and do not duplicate one rule in several layers unless each has a distinct reason. Register validators with `FluentValidation.DependencyInjectionExtensions`; do not add deprecated/legacy ASP.NET automatic-validation integration packages, and follow the project's established invocation pattern instead of adding a competing one. A syntactically valid request can still violate an Application or Domain rule.

## Exceptions for rules

A project may deliberately use typed exceptions for selected cases, but only as a consistent project-level decision.

## External services

Catch an external-service exception locally only to translate it into an Application-level outcome, add useful context, perform a defined fallback, or apply an infrastructure-level retry policy; otherwise let it propagate. Never swallow external-service failures.

## Catching exceptions

Catch when you can recover, translate into a meaningful abstraction-level outcome, perform cleanup that cannot be expressed otherwise, or add context while preserving the original exception. Never catch `Exception` merely to continue, and avoid:

```csharp
try { await service.ProcessAsync(cancellationToken); }
catch (Exception) { }                       // swallowed failure

catch (Exception ex)
{
    logger.LogError(ex, "Failed");          // catch/log/rethrow at every layer
    throw;
}
```

Expected outcomes (not found, validation failures, rejected business operations) are normally not logged as application errors. Logging technique: `logging`.

## Result pattern (optional)

Consider `Result<T>` when an operation has several expected failure modes, callers benefit from typed outcomes, exception-based control flow would otherwise be common, and the project will use it consistently. Avoid it when `null`, `bool`, or a simple typed response suffices, when it wraps straightforward CRUD in noise, or when it would spread to every method without need (project-wide adoption: `CLAUDE.md`, Decision control). If adopted, use typed errors rather than string arrays:

```csharp
public sealed record AppError(string Code, string Message);
```

## Anti-patterns

Returning raw exception messages, inconsistent anonymous error objects, putting business rules only in request validators, and coupling validation to Minimal API endpoint filters when Controllers are the HTTP model.

## Decision guide

| Scenario | Default |
|---|---|
| Invalid HTTP input | Validation problem response |
| Simple query not found | `null` outcome; Api maps to `404` |
| Multiple expected business outcomes | Typed outcome (or an approved Result model) |
| Unexpected exception | Global `IExceptionHandler` |
| API failure contract | `ProblemDetails` |
| Straightforward use-case/workflow rule | Application validation / Application Service |
| Non-trivial invariant owned by Domain | Domain enforcement |
| Recoverable external failure | Handle or translate at the boundary |
| Unrecoverable external failure | Propagate to centralized handling |
| Client/request cancellation | Propagate; not a generic `500` |
