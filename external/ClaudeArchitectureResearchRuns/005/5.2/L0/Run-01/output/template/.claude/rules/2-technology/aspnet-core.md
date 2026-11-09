---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
  - "backend/**/launchSettings.json"
---

> Level: 2 Technology | Owns: ASP.NET Core bindings — Controllers, error contracts, Swagger UI exposure, Identity, Data Protection | Scope: backend | Loads: path | Depends on: 1-architecture/entry-points.md, 1-architecture/outcomes.md, 0-core/security-principles.md

# ASP.NET Core

## Bindings to Architecture Rules

- ASP.NET Core Controllers are the HTTP entry points governed by
  `1-architecture/entry-points.md`.
- `IActionResult`, `ActionResult<T>`, `ProblemDetails`, `StatusCodes`,
  `HttpContext`, `ClaimsPrincipal`, and `IHttpContextAccessor` are web-framework
  transport types in the sense of the Level 1 layer rules.
- The centralized unexpected-failure handler is an `IExceptionHandler`
  registered with `AddProblemDetails()`, `AddExceptionHandler<T>()`, and
  `UseExceptionHandler()`.
- `[Authorize]`, `[AllowAnonymous]`, and global or fallback authorization
  policies are the authorization annotations and policies referred to by the
  Core security principles.
- ASP.NET Core Data Protection is suitable for application-generated protected
  payloads (cookies, temporary protected values); it is not a universal
  database-encryption mechanism.

## Error Contracts

- Default: use `ProblemDetails` for non-validation HTTP failures and
  `ValidationProblemDetails` for request validation failures; keep
  machine-readable error contracts stable and safe.

## Swagger UI

- Default: enable Swagger UI in Development; expose it in other environments
  only when deployment requirements explicitly justify it.

## Authentication

- Do not implement custom token or password security, password hashing, or
  reset-token cryptography when established ASP.NET Core authentication or
  Identity facilities cover the requirement.

Technique: → `http-api`, `aspnet-error-handling`, `swagger`, `authentication`, `health-check` skills.
