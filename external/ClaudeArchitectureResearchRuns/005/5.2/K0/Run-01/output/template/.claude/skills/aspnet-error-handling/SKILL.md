---
name: aspnet-error-handling
description: Use when implementing or reviewing API error handling — IExceptionHandler, ProblemDetails/ValidationProblemDetails responses, controller error mapping, expected application outcomes, FluentValidation placement, exception catching, error logging, client cancellation, optional Result types.
---
<!-- Kind: KNW | Scope: backend | Owns: ASP.NET Core error-handling and validation technique | Loads: on demand (model-invoked) -->
# ASP.NET Core Error Handling

Standards: `rules/backend/error-handling.md` (error contracts, exception flow, expected outcomes, validation boundaries, cancellation) and `rules/common/security.md`. HTTP status semantics: `http-api` skill. This skill owns technique and examples.

## Unexpected Exceptions

Typical unexpected failures that propagate to the global handler: programming defects, unexpected database failures, unexpected external-service failures, violated assumptions the application cannot handle locally.

## Global Exception Handler

Centralized handling with ASP.NET Core `IExceptionHandler`, treating client-aborted requests separately from unexpected failures:

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

Registration in API composition:

```csharp
builder.Services.AddProblemDetails();
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();

app.UseExceptionHandler();
```

Development diagnostics may show more through development tooling, but public API contracts stay safe.

## Expected Application Outcomes

Expected outcomes are conditions the application understands and represents without treating them as system failures: entity not found, transition not allowed, duplicate resource, optimistic concurrency conflict, operation rejected by a known rule. Choose the simplest representation; for a simple query `null` may be enough:

```csharp
public Task<OrderDto?> GetByIdAsync(
    Guid id,
    CancellationToken cancellationToken);
```

For a command with several meaningful outcomes an explicit typed outcome may be clearer. Name Application outcome categories by Application semantics — `Validation`, `NotFound`, `Conflict`, `BusinessRuleViolation` — and map them to HTTP in the Api layer.

## Controller Mapping

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

## ProblemDetails

A useful error contract may contain the HTTP status, a stable machine-readable error code when clients need one, a human-readable title, a safe detail, and a correlation or trace identifier when appropriate.

## Request Validation

With `[ApiController]`, ASP.NET Core handles transport-level concerns such as model-binding failures and can produce validation problem responses. FluentValidation (DEC-VAL-01) expresses explicit rules for inputs such as required business/application input, string or collection constraints, ranges, cross-property and conditional validation:

```text
API transport/request-contract concern
    -> API boundary validation where appropriate

Application use-case input or straightforward workflow rule
    -> Application validator / Application Service

Non-trivial domain invariant that genuinely belongs to Domain
    -> Domain model
```

Register validators with `FluentValidation.DependencyInjectionExtensions` where appropriate. Avoid deprecated or legacy ASP.NET automatic-validation integration packages, and follow the project's established validation invocation pattern rather than adding a second competing mechanism.

## Application and Domain Validation

A request can be syntactically valid and still violate an application or domain rule, so request validation and business-rule checks are separate pieces of code. Where each rule lives: `rules/backend/error-handling.md` § Validation Boundaries and `rules/backend/architecture.md` § Domain.

## Exceptions for Domain or Application Rules

A project may deliberately use typed exceptions for selected cases as a consistent project-level decision; it is not the default architecture.

## External Services

Catch an external-service exception locally only when the layer can do something meaningful: translate it into an Application-level outcome, add useful context, perform a defined fallback, or apply an appropriate retry policy at the infrastructure boundary. Otherwise let it propagate to centralized handling; avoid swallowing external-service failures.

## Error Logging

Expected outcomes such as `NotFound`, validation failures or rejected business operations are normally not logged as application errors. Log levels, structured logging and correlation: `logging` skill.

## Catching Exceptions

When a catch is justified: `rules/backend/error-handling.md` § Exception Flow. Two shapes to avoid — catching `Exception` simply to continue:

```csharp
try
{
    await service.ProcessAsync(cancellationToken);
}
catch (Exception)
{
}
```

and catch/log/rethrow boilerplate at every layer when the global handler already owns that responsibility:

```csharp
catch (Exception ex)
{
    logger.LogError(ex, "Failed");
    throw;
}
```

## Result Pattern

`Result<T>` is optional. Consider it when an operation has several expected failure modes, callers benefit from explicit typed outcomes, exception-based control flow would otherwise be common, and the project is willing to use it consistently. Avoid it when `null`, `bool` or a simple typed response communicates the outcome, when it adds wrapper noise around straightforward CRUD, or when every method would return `Result<T>` without need. A project-wide Result model is a Reserved decision (CLAUDE.md § Decisions). If introduced, prefer typed errors over arbitrary string arrays:

```csharp
public sealed record AppError(
    string Code,
    string Message);
```

## Cancellation

Propagate `CancellationToken` through asynchronous operations; a request cancelled by the client is not an internal server error (`rules/backend/error-handling.md` § Cancellation Outcomes).

## Anti-Patterns

Avoid returning raw exception messages or inconsistent anonymous error objects, Application code depending on HTTP status codes, forcing every method to return `Result<T>`, exceptions for every normal negative branch, swallowed exceptions, catch/log/rethrow at every layer, repeated logging of the same failure, sensitive details in `ProblemDetails`, business rules only in request validators, and Minimal API endpoint filters for validation in a Controller-based project.

## Decision Guide

| Scenario | Default |
|---|---|
| Invalid HTTP input | Validation problem response |
| Simple query not found | Explicit Application outcome, often `null`; Api maps to `404` |
| Multiple expected business outcomes | Consider a typed outcome / Result |
| Unexpected exception | Global `IExceptionHandler` |
| API failure contract | `ProblemDetails` |
| Straightforward use-case/workflow rule | Application validation / Application Service |
| Non-trivial invariant genuinely owned by Domain | Domain enforcement |
| Transport validation | API/request validation |
| Recoverable external failure | Handle or translate at the appropriate boundary |
| Unrecoverable external failure | Propagate to centralized handling |
| Client/request cancellation | Propagate cancellation; not a generic 500 |
