---
paths:
  - "backend/**/*"
---

> Level: 2-technology · Owns: ASP.NET Core and .NET API bindings of the technology-neutral backend rules — entry-point mechanism, error-contract types, exception handling, async, time, outbound HTTP, logging, configuration, authentication facilities, secrets · Scope: backend · Loading: path

# Backend Platform Bindings

These bind the technology-neutral Core and Architecture backend rules to concrete ASP.NET Core and .NET APIs. The owning rule keeps the obligation and its strength; a binding names the mechanism and adds no separate policy.

## Entry point (frame boundaries, role rules)

- Entry-point mechanism: ASP.NET Core Controllers (decided stack), as controller classes in a `Controllers/` folder of the entry-point project; do not create Minimal API endpoint groups unless explicitly requested.
- Transport result types that stay at the entry point: `IActionResult`, `ActionResult<T>`, `IResult`, and status-code constants.
- Remote transport responses that the implementation layer translates: `HttpResponseMessage` and its headers and status.

## HTTP error contract and failures (`.claude/rules/0-core/http-api.md`)

- Problem-details responses: `ProblemDetails` for non-validation failures and `ValidationProblemDetails` for request validation, registered with `AddProblemDetails()`; `[ApiController]` produces the automatic validation response.
- Centralized exception handling: an `IExceptionHandler` implementation registered with `AddExceptionHandler<T>()` and `UseExceptionHandler()`.
- Client cancellation surfaces as `OperationCanceledException` with `HttpContext.RequestAborted` signaled.

## Runtime code (`.claude/rules/0-core/backend-code.md`)

- Sync-over-async: `.Result`, `.Wait()`, `.GetAwaiter().GetResult()`. Asynchronous return types for the `Async` suffix: `Task`, `Task<T>`, `ValueTask`, `ValueTask<T>`; `ValueTask` is the allocation-reducing return type.
- Cancellation tokens: `CancellationToken` parameters; at the entry point, `HttpContext.RequestAborted` (bound automatically for controller actions).
- Time abstraction: `TimeProvider` (inject `TimeProvider.System`; tests use `FakeTimeProvider`).
- Factory-managed long-lived client strategy: `IHttpClientFactory` with typed or named clients (`AddHttpClient`); a client instance per request means `new HttpClient()` in request-scoped code.
- Logging abstraction: `ILogger<T>` with message templates.
- Strongly typed options: `IOptions<T>` bound with `AddOptions<T>().Bind(...)`, validated with `ValidateDataAnnotations()` or `Validate(...)` and `ValidateOnStart()`; scattered string lookups mean `IConfiguration["..."]`.

## Security (`.claude/rules/0-core/security.md`)

- Established authentication and identity facilities: ASP.NET Core authentication handlers (JWT bearer, OpenID Connect, cookies) and ASP.NET Core Identity (password hashing, reset and confirmation tokens).
- Application payload-protection API: ASP.NET Core Data Protection (short-lived application payloads).
- Local development secrets: `dotnet user-secrets`.

Technique: `aspnet-error-handling`, `http-api`, `httpclient-factory`, `logging`, `configuration`, `authentication` skills.
