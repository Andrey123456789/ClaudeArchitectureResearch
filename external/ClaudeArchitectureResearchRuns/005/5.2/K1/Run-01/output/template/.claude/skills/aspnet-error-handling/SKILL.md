---
name: aspnet-error-handling
description: Use when implementing or reviewing ASP.NET Core error handling — IExceptionHandler, ProblemDetails/ValidationProblemDetails, controller error mapping, expected application outcomes, FluentValidation wiring, catch blocks, external-service failures, cancellation or an optional Result pattern.
---
Kind: KNW | Scope: backend | Capability: — | Loading: on invocation

# ASP.NET Core Error Handling

Rules: `.claude/rules/backend/error-handling.md` (error contracts, central handling, logging once, cancellation, expected outcomes, validation boundaries). Status-code semantics: `http-api` skill. This skill holds the implementation technique.

## Global exception handler

Unexpected failures (programming defects, unexpected database or external-service failures, violated assumptions) propagate to one `IExceptionHandler`. Treat client-aborted requests separately:

```csharp
internal sealed class GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger)
    : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        if (exception is OperationCanceledException &&
            httpContext.RequestAborted.IsCancellationRequested)
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
```

```csharp
builder.Services.AddProblemDetails();
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();

app.UseExceptionHandler();
```

Development diagnostics may expose more detail through development tooling; the public API contract stays safe.

## Expected application outcomes

Expected outcomes are conditions the application understands: an entity does not exist, a transition is not allowed, a duplicate resource, an optimistic-concurrency conflict, a business operation rejected by a known rule. Choose the simplest representation:

```csharp
public Task<OrderDto?> GetByIdAsync(Guid id, CancellationToken cancellationToken);
```

For a command with several meaningful outcomes, an explicit typed outcome can be clearer. If the project adopts a Result model (a project-wide convention is Reserved), use it consistently with typed errors rather than arbitrary strings:

```csharp
public sealed record AppError(string Code, string Message);
```

Consider a Result type when an operation has several expected failure modes, callers benefit from explicit typed outcomes, and exception-based control flow would otherwise be common. Avoid it when `null`, `bool` or a simple typed response is clear, or when it only adds wrapper noise around straightforward CRUD.

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

A useful error contract may contain the HTTP status, a stable machine-readable error code when clients need one, a human-readable title, a safe detail, and a correlation or trace identifier when appropriate.

## Request validation

- `[ApiController]` handles transport-level concerns such as model-binding failures and can produce validation problem responses.
- FluentValidation expresses explicit request and use-case rules: required business input, string and collection constraints, ranges, cross-property, conditional and other rules that are clearer as validators.
- Register validators with `FluentValidation.DependencyInjectionExtensions` (`services.AddValidatorsFromAssemblyContaining<...>()`). Do not add deprecated or legacy ASP.NET automatic-validation integration packages merely to connect FluentValidation to the pipeline; follow the project's established invocation pattern (for example invoking the validator in the Application service or an explicit controller step) instead of adding a second competing mechanism.

```text
API transport/request-contract concern        -> API boundary validation
Application use-case input or workflow rule   -> Application validator / Application Service
Non-trivial invariant genuinely owned by Domain -> Domain model
```

A request can be syntactically valid and still violate an application or domain rule; API validation does not replace business rules.

## External services

Catch an external-service exception locally only when the layer can do something meaningful: translate it into an Application-level outcome, add useful context, perform a defined fallback, or apply a retry policy at the infrastructure boundary. Otherwise let it propagate to the centralized handler. Never swallow external-service failures.

## Catching exceptions

Do not catch `Exception` simply to continue execution:

```csharp
try
{
    await service.ProcessAsync(cancellationToken);
}
catch (Exception)
{
}
```

Do not write catch/log/rethrow boilerplate at every layer when the global handler already owns that responsibility:

```csharp
catch (Exception ex)
{
    logger.LogError(ex, "Failed");
    throw;
}
```

## Logging and cancellation

Log levels and sensitive data: `logging` skill. Cancellation propagation: `.claude/rules/backend/performance.md`; client cancellation in the handler: the example above.

## Anti-patterns

Review checks; `error-handling.md` owns each rule unless noted:

- Raw exception messages, inconsistent anonymous error objects or internal details returned to clients?
- Application depending on HTTP status codes? (`http-api.md`)
- `Result<T>` forced everywhere, or exceptions thrown for every normal negative branch?
- Swallowed exceptions, catch/log/rethrow at every layer, or the same failure logged repeatedly?
- Business rules only in request validators, or validation coupled to Minimal API endpoint filters in a controller-based project?
