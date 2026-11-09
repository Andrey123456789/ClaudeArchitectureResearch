---
name: aspnet-error-handling
description: >
  Use for ASP.NET Core error handling: IExceptionHandler, ProblemDetails, outcome mapping, Result pattern, FluentValidation wiring, cancellation.
---

> Level: 2 Technology | Owns: ASP.NET Core error-handling and validation technique | Scope: backend | Loads: knowledge skill (on demand) | Depends on: 1-architecture/outcomes.md, 2-technology/aspnet-core.md

# ASP.NET Core Error Handling Technique

Policy owners (routing): outcomes, exception flow, logging boundary, validation
boundaries → `1-architecture/outcomes.md`; public error exposure and
cancellation → `0-core/error-exposure.md`; error contracts and handler binding →
`2-technology/aspnet-core.md`; status semantics → `http-api` skill.

## Global Exception Handler

```csharp
internal sealed class GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger)
    : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext, Exception exception, CancellationToken cancellationToken)
    {
        if (exception is OperationCanceledException &&
            httpContext.RequestAborted.IsCancellationRequested)
        {
            httpContext.Response.StatusCode = StatusCodes.Status499ClientClosedRequest;
            return true;   // client went away: not an application failure
        }

        logger.LogError(exception, "Unhandled exception while processing {Method} {Path}",
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

## Expected Outcomes

A simple query may return `null`; a command with several meaningful outcomes
may return a typed outcome. Name categories by Application semantics and map
them to HTTP in the Controller:

```csharp
[HttpGet("{id:guid}")]
public async Task<ActionResult<OrderResponse>> GetById(Guid id, CancellationToken ct)
{
    var order = await orders.GetByIdAsync(id, ct);
    if (order is null)
        return Problem(statusCode: StatusCodes.Status404NotFound, title: "Order not found");
    return Ok(order);
}
```

If the project deliberately adopts a Result pattern (a project-wide convention
is Reserved), use it consistently with typed errors rather than string arrays:

```csharp
public sealed record AppError(string Code, string Message);
```

Consider it when operations have several expected failure modes and callers
benefit from explicit outcomes; avoid it when `null`, `bool`, or a simple typed
response is clear or when it adds wrapper noise to plain CRUD.

## ProblemDetails Contract

A useful error body contains the HTTP status, a stable machine-readable code
when clients need one, a human-readable title, safe detail, and a trace or
correlation identifier when appropriate. Return consistent contracts, never
ad-hoc anonymous error objects.

## Validation Wiring

- `[ApiController]` produces validation problem responses for binding and
  transport failures automatically.
- FluentValidation fits required input, string/collection constraints, ranges,
  cross-property and conditional rules. Register validators with
  `FluentValidation.DependencyInjectionExtensions`
  (`services.AddValidatorsFromAssemblyContaining<CreateOrderRequestValidator>()`)
  and invoke them through the project's one established pattern (for example
  explicitly in the Application Service). Avoid deprecated or legacy ASP.NET
  automatic-validation integration packages and Minimal API endpoint filters in
  a Controller-based project.
- Validators cover request and use-case rules; Domain invariants stay where
  `1-architecture/outcomes.md` places them.

## Catching Exceptions

Catch when you can recover, translate into a meaningful outcome, perform
required cleanup, or add context while preserving the original exception.
Otherwise let it propagate. Avoid:

```csharp
try { await service.ProcessAsync(ct); } catch (Exception) { }          // swallowed
catch (Exception ex) { logger.LogError(ex, "Failed"); throw; }          // log-and-rethrow per layer
```

External-service exceptions are caught locally only to translate, add context,
fall back, or apply an infrastructure-level retry policy — never swallowed.

## Decision Guide

| Scenario | Technique |
|---|---|
| Invalid HTTP input | Validation problem response |
| Simple query not found | `null` outcome → Controller maps to `404` |
| Several expected business outcomes | Typed outcome (or adopted Result) |
| Unexpected exception | Global `IExceptionHandler` |
| Recoverable external failure | Translate at the Infrastructure boundary |
| Client cancellation | Propagate; handler returns without error logging |
