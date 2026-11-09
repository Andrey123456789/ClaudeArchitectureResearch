---
name: aspnet-error-handling
description: ASP.NET Core error-handling technique. Use when implementing or reviewing IExceptionHandler, ProblemDetails/ValidationProblemDetails responses, controller outcome mapping, expected use-case outcomes, FluentValidation validators, try/catch placement, client-cancellation handling, or an optional Result<T> pattern.
---

> Level: 2-technology · Owns: exception, validation, and outcome-mapping technique · Loading: on demand

# ASP.NET Core Error Handling

Rules: `.claude/rules/0-core/http-api.md` § Failures, the role boundary rules (HTTP semantics at the entry point, expected outcomes), and the validation rule in `.claude/rules/2-technology/backend-libraries.md`. Status semantics: `http-api`. This skill adds technique only.

## Global exception handler

```csharp
internal sealed class GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger) : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(HttpContext httpContext, Exception exception, CancellationToken cancellationToken)
    {
        if (exception is OperationCanceledException && httpContext.RequestAborted.IsCancellationRequested)
        {
            httpContext.Response.StatusCode = StatusCodes.Status499ClientClosedRequest;
            return true;
        }

        logger.LogError(exception, "Unhandled exception while processing {Method} {Path}",
            httpContext.Request.Method, httpContext.Request.Path);

        await Results.Problem(statusCode: StatusCodes.Status500InternalServerError,
            title: "An unexpected error occurred").ExecuteAsync(httpContext);
        return true;
    }
}

// Program.cs
builder.Services.AddProblemDetails();
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
app.UseExceptionHandler();
```

Typical unexpected failures: programming defects, unexpected database or external-service failures, violated assumptions the code cannot handle locally. Development tooling may show more detail; the public contract stays safe.

## Expected outcomes

Examples: entity not found, transition not allowed, duplicate resource, optimistic-concurrency conflict, operation rejected by a known rule. Pick the simplest representation — `null` for a simple query (`Task<OrderDto?> GetByIdAsync(...)`), an explicit typed outcome for a command with several meaningful results.

## Controller mapping

```csharp
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
```

## ProblemDetails contract

A useful error contract carries the HTTP status, a stable machine-readable error code when clients need one, a human-readable title, a safe detail, and a correlation/trace identifier when appropriate.

## Validation technique

- With `[ApiController]`, model-binding failures produce validation problem responses automatically.
- FluentValidation fits required application input, string/collection constraints, ranges, cross-property and conditional rules. Register validators with `FluentValidation.DependencyInjectionExtensions`; follow the project's established invocation pattern instead of adding a competing mechanism, and do not add deprecated automatic-validation integration packages.
- A syntactically valid request can still violate a use-case or domain rule; ordinary CRUD and workflow rules stay in the use-case layer unless an approved design chose a richer domain model.

```text
transport/request-contract concern      -> entry-point validation
use-case input or workflow rule         -> use-case validator / use-case unit
non-trivial domain-owned invariant      -> domain model
```

## Catching exceptions

Catch only to recover, translate into a meaningful abstraction-level outcome, perform a defined fallback, add context while preserving the original exception, or run required cleanup. For external services, translate or retry at the implementation-layer boundary when meaningful; otherwise let the failure propagate. Never swallow:

```csharp
try { await service.ProcessAsync(cancellationToken); }
catch (Exception) { }                                  // never

catch (Exception ex) { logger.LogError(ex, "Failed"); throw; }   // redundant when the global handler logs
```

Expected outcomes (`NotFound`, validation failures, rejected operations) are normally not logged as errors.

## Optional Result pattern

Consider `Result<T>` when an operation has several expected failure modes, callers benefit from typed outcomes, exception-based flow would otherwise be common, and the project will use it consistently (adopting it project-wide is Reserved). Avoid it when `null`, `bool`, or a simple typed response is clear or it only wraps straightforward CRUD. If adopted, use typed errors: `public sealed record AppError(string Code, string Message);` — never arbitrary string arrays.

## Anti-patterns

Raw exception messages to clients; inconsistent anonymous error objects; use-case code depending on HTTP status codes; `Result<T>` everywhere; exceptions for every negative branch; swallowed exceptions; catch/log/rethrow at every layer; duplicate logging; sensitive data in `ProblemDetails`; business rules only in request validators; Minimal API endpoint filters for validation in a Controller project.

## Decision guide

| Scenario | Default |
| --- | --- |
| Invalid HTTP input | validation problem response |
| Simple query not found | use-case `null` outcome; entry point maps to `404` |
| Several expected business outcomes | typed outcome (Result only if adopted) |
| Unexpected exception | global `IExceptionHandler` |
| API failure contract | `ProblemDetails` |
| Recoverable external failure | handle or translate at the adapter boundary |
| Unrecoverable external failure | propagate to centralized handling |
| Client/request cancellation | propagate; not a generic `500` |
