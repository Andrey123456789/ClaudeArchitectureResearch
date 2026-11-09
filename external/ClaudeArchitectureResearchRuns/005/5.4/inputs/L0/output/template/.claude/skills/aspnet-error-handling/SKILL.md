---
name: aspnet-error-handling
description: >
  Use when implementing API error handling: IExceptionHandler, ProblemDetails,
  controller outcome mapping, typed outcomes or Result, FluentValidation wiring,
  cancellation.
---

> Level: 2 Technology · Owns: ASP.NET Core error-handling and validation technique (knowledge) · Scope: backend · Loads: on invocation · Depends on: .claude/rules/1-architecture/outcomes.md, .claude/rules/2-technology/aspnet-core.md

# ASP.NET Core Error Handling

Policy owners: expected outcomes, exception use, validation boundaries → `.claude/rules/1-architecture/outcomes.md`; error and type bindings → `2-technology/aspnet-core.md`, `2-technology/fluentvalidation.md`; failure exposure → `0-core/security-principles.md`; log-once and cancellation → `0-core/logging-principles.md`, `0-core/runtime-principles.md`; status semantics → `http-api` skill. This skill is technique only.

## Global exception handler

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
            return true;   // client went away: not an application failure
        }

        logger.LogError(exception,
            "Unhandled exception while processing {Method} {Path}",
            httpContext.Request.Method, httpContext.Request.Path);

        await Results.Problem(
                statusCode: StatusCodes.Status500InternalServerError,
                title: "An unexpected error occurred")
            .ExecuteAsync(httpContext);

        return true;
    }
}

// Program.cs
builder.Services.AddProblemDetails();
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
app.UseExceptionHandler();
```

Typical unexpected failures: programming defects, unexpected database or external-service failures, violated assumptions the application cannot handle locally. Development diagnostics may show more through development tooling; public contracts stay safe.

## Expected outcomes

Examples: entity not found, transition not allowed, duplicate resource, optimistic-concurrency conflict, operation rejected by a known rule.

```csharp
// Simple query: null is enough
public Task<OrderDto?> GetByIdAsync(Guid id, CancellationToken cancellationToken);
```

For a command with several meaningful outcomes, an explicit typed outcome is often clearer. If the project deliberately adopts a Result pattern, use it consistently with typed errors rather than strings:

```csharp
public sealed record AppError(string Code, string Message);
```

Consider a Result when an operation has several expected failure modes, callers benefit from typed outcomes, or exception-based control flow would otherwise be common; avoid it when `null`, `bool`, or a simple typed response is clear, or when it only wraps straightforward CRUD.

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
            return Problem(statusCode: StatusCodes.Status404NotFound, title: "Order not found");

        return Ok(order);
    }
}
```

## Error contract contents

A useful ProblemDetails contract may contain the HTTP status, a stable machine-readable error code when clients need one, a human-readable title, a safe detail, and a correlation/trace identifier when appropriate.

## Request validation wiring

With `[ApiController]`, model-binding and transport-level failures automatically produce validation problem responses. Explicit rules use FluentValidation validators (`2-technology/fluentvalidation.md`), placed by owner:

```text
API transport/request-contract concern      -> Api boundary validation
Application input or straightforward rule   -> Application validator / Application Service
Non-trivial invariant owned by Domain       -> Domain model
```

Register validators with `services.AddValidatorsFromAssemblyContaining<CreateOrderRequestValidator>()` (FluentValidation.DependencyInjectionExtensions) and invoke them through the project's one established mechanism (for example explicitly in the Application Service, or an action filter in Api).

## Catching exceptions

Catch only when you can recover, translate to an abstraction-level outcome, perform cleanup that cannot be expressed otherwise, or add context while preserving the original exception. Avoid:

```csharp
try { await service.ProcessAsync(cancellationToken); }
catch (Exception) { }                       // swallowed failure

catch (Exception ex)
{
    logger.LogError(ex, "Failed");          // catch/log/rethrow at every layer
    throw;
}
```

External-service exceptions may be caught locally to translate them into an Application outcome, add context, apply a defined fallback, or apply an infrastructure retry policy; otherwise let them propagate. Expected outcomes (`NotFound`, validation failures, rejected operations) are normally not logged as errors.

## Decision guide

| Scenario | Technique |
|---|---|
| Invalid HTTP input | `[ApiController]` validation problem response |
| Simple query not found | Application returns `null`; Api maps to 404 |
| Several expected business outcomes | typed outcome or an adopted Result |
| Unexpected exception | `IExceptionHandler` + ProblemDetails |
| Recoverable external failure | handle/translate at the Infrastructure boundary |
| Client/request cancellation | `OperationCanceledException` + `RequestAborted` branch in the handler |

Avoid inconsistent anonymous error objects and validation coupled to Minimal API endpoint filters in a Controller-based project.
