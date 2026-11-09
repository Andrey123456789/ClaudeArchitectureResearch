---
paths:
  - "backend/**/*"
---

> Level: 2-technology · Owns: usage rules for approved non-slot backend libraries (FluentValidation, Swagger, Serilog, container images) and bindings of technology-neutral Core/Architecture terms to ASP.NET Core and .NET APIs · Scope: backend (including backend tests) · Loading: path

# Backend Technology Rules

- Use FluentValidation for explicit request and use-case validation where appropriate, and keep each rule at its owning boundary: transport/request concerns at the entry point, use-case and straightforward workflow rules in the use-case layer, genuine domain invariants in the domain model, assumptions about external systems in the implementation layer when they matter. Do not move domain invariants into validators or duplicate one rule mechanically across layers.
- Swagger/OpenAPI metadata must describe the API that actually runs — routes, important response statuses (including those produced by the pipeline), schemas, and authentication behavior; never document speculative responses.
- Default: enable Swagger UI in Development; exposure in other environments follows the Swagger decision in the decisions file.
- Default: when Serilog is configured, use the DI-integrated `AddSerilog` approach with provider configuration in environment-aware configuration; application code keeps depending on `ILogger<T>`.
- Default: production containers use an appropriate runtime image rather than the SDK image for convenience, and do not switch to root merely to bypass filesystem permission problems.

## Platform bindings

These bind technology-neutral Core and Architecture rules to the ASP.NET Core and .NET APIs; they add no separate policy.

| Neutral term (rule) | Binding |
| --- | --- |
| entry-point code in Api (frame boundaries and layout) | ASP.NET Core controllers (`ControllerBase` with `[ApiController]`) in the Api project's `Controllers/` folder; do not create Minimal API endpoint groups unless explicitly requested |
| web-framework result, request, and status types (role and frame rules) | `IActionResult`, `ActionResult<T>`, `IResult`, `StatusCodes`, `HttpContext`, `ProblemDetails`, and other ASP.NET Core transport types |
| problem details / validation problem details (HTTP API rules) | `ProblemDetails` / `ValidationProblemDetails`, registered with `AddProblemDetails()`; `[ApiController]` returns validation problems for model-binding failures |
| centralized exception handling (HTTP API rules) | an `IExceptionHandler` registered with `AddExceptionHandler<T>()` and `UseExceptionHandler()` |
| platform authentication and account-management facilities (security rules) | ASP.NET Core authentication handlers and authorization policies; ASP.NET Core Identity for application-owned accounts (password hashing, lockout, reset tokens) |
| data-protection mechanism for application payloads (security rules) | ASP.NET Core Data Protection (`IDataProtectionProvider`) |
| in-memory test host for host integration tests (backend test rules) | `WebApplicationFactory<Program>` from `Microsoft.AspNetCore.Mvc.Testing` |
| HTTP client factory (backend code rules) | `IHttpClientFactory` |
| category-typed logging abstraction (backend code rules) | `ILogger<T>` |
| string-based configuration lookups / typed options (backend code rules) | `IConfiguration` / the options pattern (`IOptions<T>`, `ValidateOnStart()`) |

Technique: `aspnet-error-handling`, `authentication`, `swagger`, `logging`, `httpclient-factory`, `configuration`, `docker` skills.
