---
name: aspnet-error-handling
description: >
  Use when implementing ASP.NET Core error handling: IExceptionHandler,
  ProblemDetails, outcome-to-HTTP mapping, Result types, FluentValidation
  wiring, exception catching, cancellation.
---

> Owns: error-handling and validation implementation technique (no policy) | Scope: backend | Loads: on demand (knowledge skill)

# ASP.NET Core Error Handling

Policy owners: error contracts, exception flow, expected outcomes, validation
boundaries, failure logging, cancellation, and dependency failures —
`.claude/rules/error-handling.md`; status codes — `.claude/rules/api.md` and the
`http-api` skill.

## What Counts as Unexpected

Programming defects, unexpected database failures, unexpected external-service
failures, and violated assumptions the application cannot handle locally
propagate to the global exception handler.

## Global Exception Handler

Treat client-aborted requests separately from unexpected failures. A
cancellation caused by `HttpContext.RequestAborted` is neither an unhandled
application error nor a `500`.

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

Development diagnostics may expose more information through development
tooling, but public API contracts stay safe.

## Expected Application Outcomes

Expected outcomes are conditions the application understands without treating
them as system failures: the requested entity does not exist; a transition is
not allowed; a duplicate resource; an optimistic concurrency conflict; a business
operation rejected by a known rule.

For a simple query, `null` may be sufficient:

```csharp
public Task<OrderDto?> GetByIdAsync(
    Guid id,
    CancellationToken cancellationToken);
```

For a command with several meaningful outcomes, an explicit typed outcome may be
clearer. If the project deliberately adopts a Result pattern (a project-wide
convention — Reserved), use it consistently with typed errors rather than
arbitrary strings passed through every layer.

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

A useful error contract may contain: the HTTP status; a stable machine-readable
error code when clients need one; a human-readable title; a safe detail; a
correlation or trace identifier when appropriate.

## Request Validation

With `[ApiController]`, ASP.NET Core handles transport-level concerns such as
model-binding failures and can produce validation problem responses.
FluentValidation fits rules that read more clearly as explicit validators:
required business/application input, string or collection constraints, ranges,
cross-property and conditional validation.

```text
API transport/request-contract concern
    -> API boundary validation where appropriate

Application use-case input or straightforward workflow rule
    -> Application validator / Application Service

Non-trivial domain invariant that genuinely belongs to Domain
    -> Domain model
```

Register validators with `FluentValidation.DependencyInjectionExtensions`
(`services.AddValidatorsFromAssemblyContaining<...>()`), and follow the
project's established validation invocation pattern rather than adding a second
competing mechanism. Do not add a deprecated automatic-validation integration
package to connect FluentValidation to the pipeline.

A request can be syntactically valid and still violate an application or domain
rule; API validation does not replace business rules. Ordinary CRUD,
straightforward workflow/state, and orchestration rules stay in Application
unless an approved design chooses a richer Domain model.

## Typed Exceptions

A project may deliberately use typed exceptions for selected cases; make that a
consistent project-level decision rather than a per-feature habit.

## External Services

Catch an external-service exception locally only when the layer can do something
meaningful — translate it into an Application outcome, add useful context,
perform a defined fallback, or apply an appropriate retry policy at the
infrastructure boundary. Otherwise let it propagate to centralized handling; do
not swallow it.

## Catching Exceptions

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

and do not write catch/log/rethrow boilerplate at every layer when the global
handler owns that responsibility:

```csharp
catch (Exception ex)
{
    logger.LogError(ex, "Failed");
    throw;
}
```

## Result Pattern

`Result<T>` helps when an operation has several expected failure modes, callers
benefit from explicit typed outcomes, exception-based control flow would
otherwise be common, and the project uses it consistently. It hurts when `null`,
`bool`, or a simple typed response is clear, when it adds wrapper noise around
straightforward CRUD, or when every method starts returning `Result<T>` without
need. If introduced, prefer typed errors:

```csharp
public sealed record AppError(
    string Code,
    string Message);
```

## Anti-Patterns

Avoid returning inconsistent anonymous error objects, coupling validation to
Minimal API endpoint filters in a Controller-based project, and putting business
rules only in request validators.

## Decision Guide

The policy behind these defaults is owned by `.claude/rules/error-handling.md`.

| Scenario | Default technique |
|---|---|
| Invalid HTTP input | Validation problem response |
| Simple query not found | `null` outcome; API maps to `404` |
| Multiple expected business outcomes | Typed outcome (Result only if adopted) |
| Unexpected exception | Global `IExceptionHandler` |
| API failure contract | `ProblemDetails` |
| Straightforward use-case/workflow rule | Application validator / Application Service |
| Non-trivial invariant genuinely owned by Domain | Domain enforcement |
| Recoverable external failure | Handle or translate at the owning boundary |
| Unrecoverable external failure | Propagate to centralized handling |
| Client/request cancellation | Propagate; handle as shown above, not as `500` |
