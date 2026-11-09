---
name: aspnet-error-handling
description: >
  Use when implementing IExceptionHandler, ProblemDetails or
  ValidationProblemDetails, FluentValidation validators, typed outcomes or a
  Result type, external-service exception handling, or outcome-to-HTTP mapping
  in ASP.NET Core.
---

> Owner: ASP.NET Core error-handling and validation technique (normative policy lives in rules) | Scope: backend | Loads: on demand — knowledge | Enforced: none

# ASP.NET Core Error Handling

Policy: `.claude/rules/error-handling.md` (expected outcomes, central handling,
error contracts, validation boundaries, cancellation, logging once). Status-code
choice: `http-api` skill.

## Global Exception Handler

Handle unexpected failures centrally with `IExceptionHandler`. Treat
client-aborted requests separately from application failures:

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

Typical unexpected failures: programming defects, unexpected database or
external-service failures, violated assumptions the application cannot handle
locally. Development diagnostics may show more detail through development
tooling; the public contract stays safe.

## Expected Application Outcomes

Examples: requested entity does not exist, transition not allowed, duplicate
resource, optimistic concurrency conflict, operation rejected by a known rule.

For a simple query, `null` may be enough:

```csharp
public Task<OrderDto?> GetByIdAsync(
    Guid id,
    CancellationToken cancellationToken);
```

For a command with several meaningful outcomes, an explicit typed outcome may be
clearer. Name outcome categories by Application semantics — `Validation`,
`NotFound`, `Conflict`, `BusinessRuleViolation` — and map them to HTTP in the API
layer.

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

## ProblemDetails Content

A useful error contract may contain the HTTP status, a stable machine-readable
error code when clients need one, a human-readable title, a safe detail, and a
correlation or trace identifier when appropriate. Return consistent
`ProblemDetails` rather than ad-hoc anonymous error objects.

## Request Validation

With `[ApiController]`, ASP.NET Core handles model-binding failures and produces
validation problem responses. Use FluentValidation for rules that are clearer as
explicit validators: required business input, string or collection constraints,
ranges, cross-property and conditional validation.

```text
API transport/request-contract concern
    -> API boundary validation where appropriate

Application use-case input or straightforward workflow rule
    -> Application validator / Application Service

Non-trivial domain invariant that genuinely belongs to Domain
    -> Domain model
```

Register validators with `FluentValidation.DependencyInjectionExtensions`, for
example `services.AddValidatorsFromAssemblyContaining<CreateOrderRequestValidator>()`.
Invoke validators through the project's established pattern (for example
explicitly in the Application Service or a controller action filter) rather than
adding a second competing mechanism, and avoid Minimal API endpoint filters in a
Controller-based project.

A request can be syntactically valid and still violate an application or domain
rule; API validation does not replace business rules.

## Selected Typed Exceptions

A project may deliberately use typed exceptions for selected cases; make that a
consistent project-level choice rather than an ad-hoc habit.

## External Services

Catch an external-service exception locally only when the current layer can do
something meaningful: translate it into an Application-level outcome, add useful
context, perform a defined fallback, or apply an appropriate retry at the
infrastructure boundary. Otherwise let it propagate to centralized handling
rather than swallowing it.

## Catching Exceptions

Avoid both of these:

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

The first hides failures; the second duplicates logging the global handler
already owns.

## Error Logging

Expected outcomes such as `NotFound`, validation failures, or rejected business
operations are normally not logged as application errors. Log levels, message
templates, and correlation: `logging` skill.

## Optional Result Pattern

`Result<T>` may help when an operation has several expected failure modes,
callers benefit from typed outcomes, exception-based control flow would otherwise
be common, and the project will use it consistently. It hurts when `null`,
`bool`, or a simple typed response is clear enough, or when it wraps
straightforward CRUD in noise. A project-wide Result model is a Reserved decision
(`CLAUDE.md` § Decision Control). If adopted, prefer typed errors over string
arrays:

```csharp
public sealed record AppError(
    string Code,
    string Message);
```

## Decision Guide

| Scenario | Technique |
|---|---|
| Invalid HTTP input | Validation problem response |
| Simple query not found | `null` from Application; API maps to `404` |
| Multiple expected business outcomes | Typed outcome (or adopted Result) |
| Unexpected exception | Global `IExceptionHandler` |
| API failure contract | `ProblemDetails` |
| Straightforward use-case/workflow rule | Application validator / Application Service |
| Non-trivial invariant owned by Domain | Domain enforcement |
| Recoverable external failure | Handle or translate at the infrastructure boundary |
| Unrecoverable external failure | Propagate to centralized handling |
| Client/request cancellation | Propagate; not a generic `500` |
