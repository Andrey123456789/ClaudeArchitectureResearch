---
name: aspnet-error-handling
description: >
  Use when implementing API errors, exception flow or validation:
  IExceptionHandler, ProblemDetails, outcome-to-HTTP mapping, typed outcomes or
  Result, FluentValidation wiring, safe catching.
---

> Level: 2 Technology · Owns: error-handling and validation technique · Scope: backend · Loads: on demand (knowledge skill)

# ASP.NET Core Error Handling

Policy owners: `.claude/rules/1-architecture/outcomes.md` (expected outcomes, central handling, validation boundaries, cancellation), `.claude/rules/2-technology/aspnet-core.md` (problem-details contracts, handler binding), `.claude/rules/0-core/logging-principles.md` (log once), `.claude/rules/0-core/security-principles.md` (error exposure). HTTP status choice: `http-api` skill.

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
            return true;                                   // client went away: no error log, no 500
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

Development diagnostics may show more detail through development tooling; the public contract stays safe.

## Expected outcomes

Typical failures the application understands: entity not found, transition not allowed, duplicate resource, optimistic-concurrency conflict, operation rejected by a known rule.

```csharp
// Simple query: null is enough
public Task<OrderDto?> GetByIdAsync(Guid id, CancellationToken cancellationToken);

// Command with several meaningful outcomes: an explicit typed outcome
public abstract record CancelOrderOutcome
{
    public sealed record Cancelled : CancelOrderOutcome;
    public sealed record NotFound : CancelOrderOutcome;
    public sealed record Conflict(string Reason) : CancelOrderOutcome;
}
```

If the project deliberately adopts a Result pattern, use it consistently with typed errors rather than strings:

```csharp
public sealed record AppError(string Code, string Message);
```

Consider a Result type when an operation has several expected failure modes, callers benefit from explicit typed outcomes, and the project will apply it consistently. Avoid it when `null`, `bool` or a simple typed response is clear, or when it wraps straightforward CRUD in noise.

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

    [HttpPost("{id:guid}/cancel")]
    public async Task<IActionResult> Cancel(Guid id, CancellationToken cancellationToken)
    {
        var outcome = await orders.CancelAsync(id, cancellationToken);

        return outcome switch
        {
            CancelOrderOutcome.Cancelled => NoContent(),
            CancelOrderOutcome.NotFound => Problem(statusCode: StatusCodes.Status404NotFound, title: "Order not found"),
            CancelOrderOutcome.Conflict c => Problem(statusCode: StatusCodes.Status409Conflict, title: "Order cannot be cancelled", detail: c.Reason),
            _ => throw new UnreachableException()
        };
    }
}
```

## Problem-details contract

A useful error body contains the HTTP status, a stable machine-readable error code when clients need one (an extension member such as `code`), a human-readable title, a safe detail, and a trace or correlation identifier when appropriate (`traceId` is added by `AddProblemDetails`).

## Request validation with FluentValidation

`[ApiController]` already turns model-binding failures into validation problem responses. Explicit validators fit required business input, string/collection constraints, ranges, cross-property and conditional rules.

```csharp
public sealed class CreateOrderRequestValidator : AbstractValidator<CreateOrderRequest>
{
    public CreateOrderRequestValidator()
    {
        RuleFor(x => x.CustomerId).NotEmpty();
        RuleFor(x => x.Lines).NotEmpty();
    }
}

// Application/DependencyInjection.cs
services.AddValidatorsFromAssemblyContaining<CreateOrderRequestValidator>();
```

Invoke validators explicitly where the project's pattern places them (controller or Application service) and map failures to `ValidationProblemDetails`:

```csharp
var validation = await validator.ValidateAsync(request, cancellationToken);
if (!validation.IsValid)
    return ValidationProblem(new ValidationProblemDetails(validation.ToDictionary()));
```

Use `FluentValidation.DependencyInjectionExtensions` for registration; the deprecated `FluentValidation.AspNetCore` automatic pipeline integration is not used. Keep one invocation pattern — do not add a second competing mechanism, and do not couple validation to Minimal API endpoint filters in a controller-based API.

## Catching exceptions

Catch only to recover, translate into the current layer's outcome, run a defined fallback, add context while preserving the original (`throw new X("context", ex)` or `throw;`), or clean up. Patterns to avoid:

```csharp
try { await service.ProcessAsync(cancellationToken); }
catch (Exception) { }                                // swallowed

catch (Exception ex) { logger.LogError(ex, "Failed"); throw; }   // log-and-rethrow at every layer
```

External-service exceptions: translate them into an Application outcome, add context, apply a defined fallback or an infrastructure-level retry policy — otherwise let them reach central handling.

## Decision guide

| Scenario | Typical approach |
|---|---|
| Invalid HTTP input | Validation problem response |
| Simple query, not found | `null` from Application; API maps to `404` |
| Several expected business outcomes | Typed outcome (or the project's adopted Result) |
| Unexpected exception | Global `IExceptionHandler` |
| API failure contract | `ProblemDetails` |
| Straightforward use-case rule | Application validator or Application Service |
| Non-trivial invariant owned by Domain | Domain enforcement |
| Recoverable external failure | Handle or translate at the Infrastructure boundary |
| Client cancellation | Propagate the token; handler returns without logging an error |
