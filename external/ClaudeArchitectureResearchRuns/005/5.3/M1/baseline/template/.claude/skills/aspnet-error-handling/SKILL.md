---
name: aspnet-error-handling
description: >
  Use for ASP.NET Core error handling: IExceptionHandler,
  ProblemDetails/ValidationProblemDetails, outcome-to-HTTP mapping, Result
  pattern, FluentValidation validators, catch blocks, cancellation.
---

> Knowledge skill · Error-handling technique and examples · Policy: `.claude/rules/error-handling.md`, HTTP semantics: `.claude/rules/api.md`

# ASP.NET Core Error Handling

## Unexpected Exceptions

Typical unexpected failures — programming defects, unexpected database or
external-service failures, violated assumptions the application cannot handle
locally — propagate to the global exception handler.

## Global Exception Handler

The handler below treats client-aborted requests (`HttpContext.RequestAborted`)
separately, as `error-handling.md` § Cancellation requires.

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

Register it in API composition:

```csharp
builder.Services.AddProblemDetails();
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();

app.UseExceptionHandler();
```

Development diagnostics may expose more through development tooling, but
public API contracts stay safe.

## Expected Application Outcomes

For a simple query, `null` may be enough:

```csharp
public Task<OrderDto?> GetByIdAsync(
    Guid id,
    CancellationToken cancellationToken);
```

For a command with several meaningful outcomes, an explicit typed outcome may
be clearer. Map Application categories to HTTP in the API layer.

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

## ProblemDetails Contents

A useful error contract may contain the HTTP status, a stable machine-readable
error code when clients need one, a human-readable title, a safe detail, and a
correlation or trace identifier when appropriate.

## Request Validation

With `[ApiController]`, ASP.NET Core handles transport-level concerns such as
model-binding failures and can produce validation problem responses.
FluentValidation fits rules such as required business input, string or
collection constraints, ranges, cross-property and conditional validation, and
other request/use-case rules that read better as explicit validators.

```text
API transport/request-contract concern
    -> API boundary validation where appropriate

Application use-case input or straightforward workflow rule
    -> Application validator / Application Service

Non-trivial domain invariant that genuinely belongs to Domain
    -> Domain model
```

Register validators with `FluentValidation.DependencyInjectionExtensions` and
follow the project's established validation invocation pattern rather than
adding a second competing mechanism.

## Application and Domain Validation

API validation does not replace business rules: a request can be syntactically
valid yet violate an application or domain rule. Keep ordinary CRUD rules,
straightforward workflow/state rules, and orchestration rules in Application
unless the approved design explicitly chooses a richer Domain model.

## External Services

Catch an external-service exception locally only when the layer can translate
it into an Application-level outcome, add useful context, perform a defined
fallback, or apply an appropriate retry policy at the infrastructure boundary;
otherwise let it propagate to centralized handling. Do not swallow
external-service failures.

## Catching Exceptions

Avoid both of these shapes:

```csharp
try
{
    await service.ProcessAsync(cancellationToken);
}
catch (Exception)
{
}
```

```csharp
catch (Exception ex)
{
    logger.LogError(ex, "Failed");
    throw;
}
```

The second is redundant when the global handler already logs the failure.

## Result Pattern

`Result<T>` is optional. Consider it when an operation has several expected
failure modes, callers benefit from explicit typed outcomes, exception-based
control flow would otherwise be common, and the project is willing to use the
pattern consistently. Avoid it when `null`, `bool`, or a simple typed response
is clear, when it adds wrapper noise around straightforward CRUD, or when it
would make every method return `Result<T>` without need. If adopted
(project-wide adoption is Reserved), prefer typed errors over string arrays:

```csharp
public sealed record AppError(
    string Code,
    string Message);
```

## Review Checks

Check-by-reference against `error-handling.md`: raw exception messages returned
to clients; inconsistent anonymous error objects; Application depending on HTTP
status codes; every method forced to return `Result<T>`; exceptions for every
negative branch; swallowed exceptions; catch/log/rethrow at every layer;
repeated logging; sensitive details in `ProblemDetails`; business rules only in
request validators; Minimal API endpoint filters used for validation in a
Controller-based project.

## Decision Guide

| Scenario | Default |
|---|---|
| Invalid HTTP input | Validation problem response |
| Simple query not found | Explicit Application outcome, often `null`; API maps to `404` |
| Multiple expected business outcomes | Consider typed outcome / Result |
| Unexpected exception | Global `IExceptionHandler` |
| API failure contract | `ProblemDetails` |
| Straightforward use-case/workflow rule | Application validation / Application Service |
| Non-trivial invariant genuinely owned by Domain | Domain enforcement |
| Transport validation | API/request validation |
| Recoverable external failure | Handle or translate at the appropriate boundary |
| Unrecoverable external failure | Propagate to centralized handling |
| Client/request cancellation | Propagate cancellation; not a generic 500 |
