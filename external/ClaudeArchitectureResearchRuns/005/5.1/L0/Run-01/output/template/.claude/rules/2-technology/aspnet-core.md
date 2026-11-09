---
paths:
  - "backend/**"
---

> Level: 2 Technology · Owns: ASP.NET Core bindings — transport types, error contracts, host composition, auth facilities, integration testing · Scope: backend, backend-tests · Loads: path

# ASP.NET Core

## Bindings for Level 1 boundaries

- Web-transport types are `IActionResult`, `ActionResult<T>`, `ControllerBase`, `IResult`/`Results`, `ProblemDetails`/`ValidationProblemDetails`, `StatusCodes`, `HttpContext`, `IHttpContextAccessor`, `IFormFile` and request `ClaimsPrincipal` access. The Level 1 layer rules keep them in the Api project; Application receives plain values or Application-owned abstractions.
- HTTP entry points are `[ApiController]` controllers deriving from `ControllerBase`.
- The centralized handler for unexpected failures is an `IExceptionHandler` registered with `AddProblemDetails()` / `AddExceptionHandler<T>()` and `UseExceptionHandler()`; it treats a cancellation caused by `HttpContext.RequestAborted` as client cancellation, not as a server failure.
- Established authentication facilities are the ASP.NET Core authentication handlers (JWT bearer, OpenID Connect, cookies) and ASP.NET Core Identity (password hashing, lockout, reset tokens). Use Identity when the application owns local accounts and passwords — not merely because a business entity is named `User`.

## Error contracts

- **Default:** use `ProblemDetails` for non-validation HTTP failures and `ValidationProblemDetails` for request-validation failures; keep the machine-readable contract stable and safe (stable error codes or fields, never raw exception messages).

## Host composition

- **Default:** enable Swagger UI in Development; expose it in other environments only when deployment requirements explicitly justify it.
- **Default:** when Serilog is configured, register it with `builder.Services.AddSerilog(...)` rather than `Host.UseSerilog()`, keep levels, sinks and overrides in environment-aware configuration, and keep application code on `ILogger<T>`.
- **Must not** treat ASP.NET Core Data Protection as a universal database-encryption solution; it suits application-generated protected payloads such as cookies and temporary protected values.

## Integration testing

- **Default:** use `WebApplicationFactory<Program>` integration tests when routing, model binding, middleware, authentication/authorization, dependency injection, repositories, EF Core or database persistence is what the test must prove. The test host uses isolated test resources (for example a `Testing` environment).

Technique: `http-api`, `aspnet-error-handling`, `swagger`, `authentication`, `health-check`, `api-versioning`, `dotnet-testing` skills.
