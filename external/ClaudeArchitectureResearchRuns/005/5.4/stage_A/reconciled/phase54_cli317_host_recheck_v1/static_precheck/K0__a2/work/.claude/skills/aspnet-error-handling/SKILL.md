---
name: aspnet-error-handling
description: Use when implementing API error handling — IExceptionHandler, ProblemDetails, outcome mapping, expected outcomes, FluentValidation placement, catching exceptions, client cancellation, Result patterns.
---

> Kind: KNW | Scope: backend | Owner: ASP.NET Core error-handling and validation technique with examples | Loading: on demand (model-invoked knowledge)

# ASP.NET Core Error Handling

Rules: `rules/backend/error-handling.md` (unexpected failures, expected outcomes, validation boundaries, cancellation), `rules/backend/api.md` (error contract, status semantics). Validation library: D-05. Status-code reference: `http-api`.

## Global exception handler

Centralize unexpected failures in an `IExceptionHandler`, handling client-aborted requests (`HttpContext.RequestAborted`) separately (`rules/backend/error-handling.md` § Cancellation).

```csharp
internal sealed class GlobalExceptionHandler(
    ILogger<GlobalExceptionHandler> logger)
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
            httpContext.Response.StatusCode =
                StatusCodes.Status499ClientClosedRequest;

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

Typical unexpected failures: programming defects, unexpected database or external-service failures, violated assumptions the application cannot handle locally. Development diagnostics may show more through development tooling while public contracts stay safe.

## Expected application outcomes

Expected outcomes are conditions the application understands: entity not found, transition not allowed, duplicate resource, optimistic concurrency conflict, operation rejected by a known rule. Choose the simplest representation:

```csharp
public Task<OrderDto?> GetByIdAsync(
    Guid id,
    CancellationToken cancellationToken);
```

For a command with several meaningful outcomes, an explicit typed outcome can be clearer. Outcome categories with Application or business meaning — `Validation`, `NotFound`, `Conflict`, `BusinessRuleViolation` — map to HTTP in the API layer (`rules/backend/error-handling.md` § Expected outcomes).

## Controller mapping

```csharp
[ApiController]
[Route("api/orders")]
public sealed class OrdersController(
    IOrderService orders)
    : ControllerBase
{
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<OrderResponse>> GetById(
        Guid id,
        CancellationToken cancellationToken)
    {
        var order = await orders.GetByIdAsync(
            id,
            cancellationToken);

        if (order is null)
        {
            return Problem(
                statusCode: StatusCodes.Status404NotFound,
                title: "Order not found");
        }

        return Ok(order);
    }
}
```

## ProblemDetails content

A useful error contract may contain the HTTP status, a stable machine-readable error code when clients need one, a human-readable title, a safe detail, and a correlation or trace identifier when appropriate. The human-readable message is not the machine-readable contract.

## Request validation

With `[ApiController]`, ASP.NET Core handles model-binding failures and can produce validation problem responses. FluentValidation expresses explicit rules for required business/application input, string or collection constraints, ranges, cross-property and conditional validation, and other request or use-case rules that read better as validators.

```text
API transport / request-contract concern       -> API boundary validation
Application use-case input or workflow rule    -> Application validator / Application Service
Non-trivial invariant genuinely owned by Domain -> Domain model
```

Register validators with `FluentValidation.DependencyInjectionExtensions`, follow the project's established invocation pattern instead of adding a second competing mechanism, and avoid deprecated automatic-validation integration packages. A request can be syntactically valid and still violate an Application or Domain rule; when a rule is enforced in several layers, each layer has its own reason.

## Catching exceptions

When a layer may catch: `rules/backend/error-handling.md` § Unexpected failures. For external services that typically means translating to an Application outcome, adding context, a defined fallback or an infrastructure-boundary retry policy; otherwise the exception propagates. Swallowing it hides failures.

Avoid:

```csharp
try
{
    await service.ProcessAsync(cancellationToken);
}
catch (Exception)
{
}
```

and catch/log/rethrow boilerplate when the global handler already owns logging:

```csharp
catch (Exception ex)
{
    logger.LogError(ex, "Failed");
    throw;
}
```

Expected outcomes such as `NotFound`, validation failures or rejected business operations are not logged as application errors. Logging technique: `logging`.

## Result pattern

`Result<T>` is optional. Consider it when an operation has several expected failure modes, callers benefit from typed outcomes, exception-based control flow would otherwise be common, and the project will use it consistently. Avoid it when `null`, `bool` or a simple typed response is clear, when it wraps straightforward CRUD in noise, or when every method would return `Result<T>` without need. If adopted, use typed errors rather than string arrays:

```csharp
public sealed record AppError(
    string Code,
    string Message);
```

A project may deliberately use typed exceptions for selected cases; make that a consistent project-level decision.

## Common mistakes

Raw exception messages or inconsistent anonymous error objects returned to clients; Application depending on HTTP status codes; every method returning `Result<T>`; exceptions for every negative branch; swallowed exceptions; catch/log/rethrow at every layer; the same failure logged repeatedly; sensitive details in `ProblemDetails`; business rules only in request validators; validation coupled to Minimal API endpoint filters in a Controller-based project.

## Decision guide

| Scenario | Technique |
|---|---|
| Invalid HTTP input | Validation problem response |
| Simple query not found | Application returns `null`; API maps to `404` |
| Several expected business outcomes | Typed outcome or Result |
| Unexpected exception | Global `IExceptionHandler` |
| API failure contract | `ProblemDetails` |
| Straightforward use-case/workflow rule | Application validator / Application Service |
| Non-trivial invariant owned by Domain | Domain enforcement |
| Recoverable external failure | Handle or translate at the boundary |
| Unrecoverable external failure | Propagate to centralized handling |
| Client cancellation | Propagate; not a generic `500` |
