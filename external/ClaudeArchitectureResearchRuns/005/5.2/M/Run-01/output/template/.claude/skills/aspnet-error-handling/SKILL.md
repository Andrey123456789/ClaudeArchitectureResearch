---
name: aspnet-error-handling
description: >
  Use for ASP.NET Core error handling: IExceptionHandler, ProblemDetails,
  controller outcome mapping, FluentValidation wiring, typed outcomes or
  Result, catch blocks, client cancellation.
---

> Knowledge skill. Owns: error-handling and validation technique and examples · Scope: backend · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/error-handling.md, .claude/rules/api.md

# ASP.NET Core Error Handling

Rules: `error-handling.md` (expected outcomes, central exception handling,
error contracts, validation boundaries, cancellation, logging once) and
`api.md` (status semantics). Status-code reference: `http-api` skill.

## Unexpected Exceptions

Unexpected exceptions — programming defects, unexpected database or
external-service failures, violated assumptions the application cannot handle
locally — propagate to the global handler.

## Global Exception Handler

Treat client-aborted requests separately from unexpected failures:

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

Development diagnostics may show more through development tooling; public API
contracts stay safe.

## Expected Application Outcomes

Expected outcomes are conditions the application understands: the entity does
not exist, a transition is not allowed, a duplicate resource, an optimistic
concurrency conflict, a business operation rejected by a known rule.

For a simple query, `null` may be enough:

```csharp
public Task<OrderDto?> GetByIdAsync(
    Guid id,
    CancellationToken cancellationToken);
```

For a command with several meaningful outcomes, an explicit typed outcome may be
clearer. If the project deliberately adopts a Result pattern, use it
consistently with typed errors rather than arbitrary strings.

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
model-binding failures and produces validation problem responses.
FluentValidation fits rules such as required business input, string or
collection constraints, ranges, cross-property and conditional validation:

```text
API transport/request-contract concern
    -> API boundary validation where appropriate

Application use-case input or straightforward workflow rule
    -> Application validator / Application Service

Non-trivial domain invariant that genuinely belongs to Domain
    -> Domain model
```

Register validators with `FluentValidation.DependencyInjectionExtensions`, and
follow the project's established validation invocation pattern rather than
adding a second competing mechanism. A request can be syntactically valid and
still violate an application or domain rule; enforce a rule in several layers
only when each layer has a distinct reason.

## External Services

Catch an external-service exception locally only to translate it into an
Application-level outcome, add useful context, perform a defined fallback, or
apply an appropriate retry policy at the infrastructure boundary; otherwise let
it propagate. Do not swallow external-service failures.

## Error Logging

Expected outcomes such as `NotFound`, validation failures, or rejected business
operations are not logged as application errors. Logging technique: `logging`
skill.

## Catching Exceptions

Do not write empty catch blocks:

```csharp
try
{
    await service.ProcessAsync(cancellationToken);
}
catch (Exception)
{
}
```

or catch/log/rethrow boilerplate at every layer when the global handler owns
that responsibility:

```csharp
catch (Exception ex)
{
    logger.LogError(ex, "Failed");
    throw;
}
```

## Result Pattern

`Result<T>` is optional. Consider it when an operation has several expected
failure modes, callers benefit from explicit typed outcomes, exception-based
control flow would otherwise be common, and the project will use it
consistently. Avoid it when `null`, `bool`, or a simple typed response is clear,
when it adds wrapper noise around straightforward CRUD, or when it would make
every method return `Result<T>` without need. Adopting it project-wide is a
Reserved decision (CLAUDE.md, Decision Control). Prefer typed errors:

```csharp
public sealed record AppError(
    string Code,
    string Message);
```

## Anti-Patterns

- returning raw exception messages or inconsistent anonymous error objects;
- Application depending on HTTP status codes;
- throwing exceptions for every normal negative branch;
- swallowing exceptions or logging the same failure repeatedly;
- leaking sensitive details through `ProblemDetails`;
- putting business rules only in request validators;
- coupling validation to Minimal API endpoint filters in a Controller-based
  project.

## Decision Guide

| Scenario | Default |
|---|---|
| Invalid HTTP input | Validation problem response |
| Simple query not found | Application returns `null`; API maps to `404` |
| Multiple expected business outcomes | Consider a typed outcome / Result |
| Unexpected exception | Global `IExceptionHandler` |
| API failure contract | `ProblemDetails` |
| Straightforward use-case/workflow rule | Application validation / Application Service |
| Non-trivial invariant genuinely owned by Domain | Domain enforcement |
| Transport validation | API/request validation |
| Recoverable external failure | Handle or translate at the appropriate boundary |
| Unrecoverable external failure | Propagate to centralized handling |
| Client/request cancellation | Propagate cancellation; not a generic 500 |
