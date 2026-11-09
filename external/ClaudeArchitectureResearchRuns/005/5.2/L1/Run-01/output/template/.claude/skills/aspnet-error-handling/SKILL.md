---
name: aspnet-error-handling
description: >
  Use for API error handling: IExceptionHandler, ProblemDetails, controller
  outcome mapping, expected outcomes vs exceptions, Result types, validators,
  cancellation.
---
> Level: 2-technology | Owns: ASP.NET Core error-handling technique and examples | Scope: backend | Loads: on demand (skill)

# ASP.NET Core Error Handling

Policy: `error-handling.md` (exception flow, logging once, safe exposure,
cancellation), `http-api.md` (error contracts and status semantics),
`backend-technologies.md` (validation boundaries). Status-code reference:
`http-api` skill.

## Global exception handler

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

Development diagnostics may show more detail through development tooling;
public API contracts stay safe.

## Expected outcomes

Examples: entity not found, transition not allowed, duplicate resource,
optimistic-concurrency conflict, operation rejected by a known rule. A simple
query can return `null`:

```csharp
public Task<OrderDto?> GetByIdAsync(Guid id, CancellationToken cancellationToken);
```

A command with several meaningful outcomes can return an explicit typed
outcome. Categories describe use-case semantics (`Validation`, `NotFound`,
`Conflict`, `BusinessRuleViolation`); the controller maps them to HTTP.

## Controller mapping

```csharp
[ApiController]
[Route("api/orders")]
public sealed class OrdersController(IOrderService orders) : ControllerBase
{
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<OrderResponse>> GetById(
        Guid id,
        CancellationToken cancellationToken)
    {
        var order = await orders.GetByIdAsync(id, cancellationToken);

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

## ProblemDetails contract

A useful error contract contains the HTTP status, a stable machine-readable
error code when clients need one (`extensions["code"]`), a human-readable title,
a safe detail, and a correlation/trace identifier when appropriate. Use
`ValidationProblemDetails` (`errors` dictionary) for request validation.

## Request validation

`[ApiController]` handles model-binding failures and produces validation
problems. Explicit validators fit required business input, string/collection
constraints, ranges, cross-property and conditional rules. Register validators
with FluentValidation.DependencyInjectionExtensions
(`services.AddValidatorsFromAssemblyContaining<CreateOrderRequestValidator>()`)
and invoke them through the project's established pattern (for example
explicitly in the use-case unit, or in a Controller action filter), not
through a second competing mechanism.

```text
transport/request-contract concern → entry-point validation
use-case input or straightforward workflow rule → use-case validator / use-case unit
non-trivial invariant genuinely owned by the domain → domain model
```

A syntactically valid request can still violate a use-case or domain rule; API
validation does not replace business rules.

## External-service failures

Catch locally only to translate into a use-case outcome, add context, perform a
defined fallback, or apply an infrastructure-boundary retry; otherwise let it
propagate. Never swallow it.

## Catching — what not to write

```csharp
try { await service.ProcessAsync(cancellationToken); }
catch (Exception) { }                     // swallowed failure

catch (Exception ex)
{
    logger.LogError(ex, "Failed");        // catch/log/rethrow at every layer
    throw;
}
```

## Result pattern (optional)

Consider `Result<T>` when an operation has several expected failure modes,
callers benefit from typed outcomes, exception-based flow would otherwise be
common, and the project will use it consistently. Avoid it when `null`, `bool`,
or a simple typed response is clear, when it wraps straightforward CRUD in
noise, or when every method would return it without need. If adopted
(project-wide adoption is a Reserved decision), use typed errors:

```csharp
public sealed record AppError(string Code, string Message);
```

## Anti-patterns

Raw exception messages to clients; inconsistent anonymous error objects;
use-case units depending on HTTP status codes; `Result<T>` everywhere;
exceptions for every negative branch; swallowed exceptions; catch/log/rethrow at
every layer; duplicate logging; sensitive details in `ProblemDetails`; business
rules only in request validators; Minimal API endpoint filters in a
Controller-based project.

## Decision guide

| Scenario | Default |
|---|---|
| Invalid HTTP input | Validation problem response |
| Simple query not found | `null` from the use-case unit; controller maps to `404` |
| Multiple expected business outcomes | Typed outcome (or adopted Result) |
| Unexpected exception | Global `IExceptionHandler` |
| API failure contract | `ProblemDetails` |
| Recoverable external failure | Handle or translate at the adapter boundary |
| Unrecoverable external failure | Propagate to centralized handling |
| Client/request cancellation | Propagate; not a generic `500` |
