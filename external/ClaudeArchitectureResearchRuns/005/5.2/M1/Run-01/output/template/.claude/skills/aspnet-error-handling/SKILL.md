---
name: aspnet-error-handling
description: >
  ASP.NET Core error handling: IExceptionHandler,
  ProblemDetails/ValidationProblemDetails, outcome mapping, Result<T>,
  FluentValidation validators, catch/rethrow, client cancellation.
---

> **Knowledge skill** · Owns: ASP.NET Core error-handling and validation technique and examples · Scope: backend · Loading: on demand

# Error Handling

## Rules

Rules: `error-handling.md` (expected outcomes, exception flow, logging boundary,
HTTP error contracts, cancellation, validation boundaries) and `api.md` (status
semantics). This skill shows how to implement them.

## Unexpected Exceptions

Unexpected exceptions should normally propagate to a global API exception
handler.

Examples include:

- programming defects;
- unexpected database failures;
- unexpected external-service failures;
- violated assumptions that the application cannot handle locally.

## Global Exception Handler

Use ASP.NET Core `IExceptionHandler` for centralized handling.

Treat client-aborted requests separately from unexpected application failures:
detect cancellation caused by `HttpContext.RequestAborted` before logging.

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

## Expected Application Outcomes

Expected outcomes are conditions the application understands and can represent
without treating them as system failures.

Examples include:

- requested entity does not exist;
- requested transition is not allowed;
- duplicate resource;
- optimistic concurrency conflict;
- business operation rejected by a known rule.

Choose the simplest representation that fits the use case.

For a simple query, `null` may be sufficient:

```csharp
public Task<OrderDto?> GetByIdAsync(
    Guid id,
    CancellationToken cancellationToken);
```

For a command with multiple meaningful outcomes, an explicit typed outcome may
be clearer.

If the project adopts a Result pattern, use it consistently and define typed
errors rather than passing arbitrary strings through every layer. Outcome
category naming: `error-handling.md` → Expected Outcomes.

```csharp
public enum OrderOutcomeKind { Success, NotFound, Conflict, BusinessRuleViolation }

public sealed record OrderOutcome(
    OrderOutcomeKind Kind,
    OrderDto? Order = null,
    string? Code = null);
```

## Controller Mapping

Controllers translate Application outcomes into HTTP semantics.

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

The Application service stays free of transport types; the Controller performs
the mapping (`api.md`).

## ProblemDetails

Contract rules: `error-handling.md` → HTTP Errors. A useful error contract may
contain:

- HTTP status;
- stable machine-readable error code when clients need one;
- human-readable title;
- safe detail;
- correlation or trace identifier when appropriate.

Customize it centrally:

```csharp
builder.Services.AddProblemDetails(options =>
{
    options.CustomizeProblemDetails = context =>
        context.ProblemDetails.Extensions["traceId"] =
            context.HttpContext.TraceIdentifier;
});
```

## Request Validation

With `[ApiController]`, ASP.NET Core handles transport-level concerns such as
model-binding failures and can produce validation problem responses.

FluentValidation expresses explicit request and use-case rules for inputs such
as:

- required business/application input;
- string or collection constraints;
- ranges;
- cross-property validation;
- conditional validation;
- other request/use-case rules that are clearer as explicit validators.

Placement of each rule (`error-handling.md` → Validation Boundaries), for
example:

```text
API transport/request-contract concern
    -> API boundary validation where appropriate

Application use-case input or straightforward workflow rule
    -> Application validator / Application Service

Non-trivial domain invariant that genuinely belongs to Domain
    -> Domain model
```

Register validators with `FluentValidation.DependencyInjectionExtensions`
(`services.AddValidatorsFromAssemblyContaining<CreateOrderRequestValidator>()`)
and invoke them explicitly in the established pattern — for example in the
Application service, or in an action filter that returns
`ValidationProblemDetails` — rather than adding a second competing mechanism.	

## Application and Domain Validation

A request can be syntactically valid but still violate an application or domain
rule; API validation does not replace business rules. Keep genuinely non-trivial
domain invariants in Domain when they naturally belong there, and ordinary CRUD,
straightforward workflow/state, and orchestration rules in Application unless the
approved design explicitly chooses a richer Domain model.

## Exceptions for Domain or Application Rules

Rule: `error-handling.md` → Expected Outcomes. When a project deliberately adopts
typed exceptions for selected cases, map them in one place (the exception handler)
rather than in every Controller.

## External Services

Catch an external-service exception locally only when the current layer can do
something meaningful with it, for example:

- translate it into an Application-level outcome;
- add useful context;
- perform a defined fallback;
- apply an appropriate retry policy at the infrastructure boundary.

Otherwise allow it to propagate to the centralized failure handling path rather
than swallowing it.

## Error Logging

Rule: `error-handling.md` → Logging. Log levels, structured logging, correlation,
and sensitive-data handling: the `logging` skill.

## Cancellation

Rules: `error-handling.md` → Cancellation. The global handler above shows how to
recognize a client-aborted request.

## Catching Exceptions

Catch an exception when at least one of these is true:

- you can recover;
- you can translate it into a meaningful abstraction-level outcome;
- you must perform cleanup that cannot be expressed otherwise;
- you need to add useful context and preserve the original exception.

Do not catch `Exception` simply to continue execution.

Do not write:

```csharp
try
{
    await service.ProcessAsync(cancellationToken);
}
catch (Exception)
{
}
```

Do not write catch/log/rethrow boilerplate at every layer:

```csharp
catch (Exception ex)
{
    logger.LogError(ex, "Failed");
    throw;
}
```

when the global handler already owns that responsibility.

## Result Pattern

`Result<T>` is optional.

Consider it when:

- an operation has several expected failure modes;
- callers benefit from explicit typed outcomes;
- exception-based control flow would otherwise be common;
- the project is willing to use the pattern consistently.

Avoid it when:

- `null`, `bool`, or a simple typed response communicates the outcome clearly;
- it creates wrapper noise around straightforward CRUD;
- it causes every method in the codebase to return `Result<T>` without a real
  need.

If introduced, prefer typed errors:

```csharp
public sealed record AppError(
    string Code,
    string Message);
```

Do not make arbitrary string arrays the application's error type.

## HTTP Status Mapping

Use the `http-api` skill for HTTP response semantics, including success
responses, validation, authentication/authorization, conflicts, preconditions,
rate limiting, and upstream failures. This skill owns exception and failure
handling technique and does not repeat the status-code reference.

## Anti-Patterns

Avoid:

- returning inconsistent anonymous error objects;
- forcing every method to return `Result<T>`;
- swallowing exceptions;
- catch/log/rethrow at every layer;
- putting business rules only in request validators;
- coupling validation to Minimal API endpoint filters when Controllers are the
  project's HTTP model.

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
| Client/request cancellation | Propagate cancellation; do not treat as generic 500 |
