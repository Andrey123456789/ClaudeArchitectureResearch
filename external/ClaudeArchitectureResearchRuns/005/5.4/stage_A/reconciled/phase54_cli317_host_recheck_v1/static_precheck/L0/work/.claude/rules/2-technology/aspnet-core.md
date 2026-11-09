---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
  - "backend/**/appsettings*.json"
  - "backend/**/launchSettings.json"
---

> Level: 2 Technology · Owns: ASP.NET Core bindings — entry-point mechanism, transport and error types, central exception handling, Swagger UI exposure, authentication and data-protection facilities · Scope: backend · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/0-core/security-principles.md, .claude/rules/1-architecture/entry-points.md, .claude/rules/1-architecture/outcomes.md

# ASP.NET Core Bindings

Technique: `http-api`, `aspnet-error-handling`, `swagger`, `authentication`, `health-check` skills.

## Entry points

- Api entry points are ASP.NET Core Controllers (approved in `3-project/decisions.md`). Do not create Minimal API endpoint groups unless explicitly requested.
- `IActionResult`, `ActionResult<T>`, `ProblemDetails`, `HttpContext`, `ClaimsPrincipal`, `IHttpContextAccessor`, and `StatusCodes` are web-framework transport types: they stay in Api and never appear in Application or Domain contracts.

## Error contract

- Use `ProblemDetails` for non-validation HTTP failures and `ValidationProblemDetails` for request validation failures; keep their machine-readable fields stable and safe (default).
- Centralized handling of unexpected exceptions uses `IExceptionHandler` with `AddProblemDetails()` / `UseExceptionHandler()`.

## Swagger UI exposure

- Enable Swagger UI in Development by default and expose it in other environments only when deployment requirements explicitly justify it (default).

## Security facilities

- Established authentication facilities are ASP.NET Core authentication handlers and, when the application owns local accounts and passwords, ASP.NET Core Identity (password hashing, lockout, reset tokens).
- ASP.NET Core Data Protection is suitable for application-generated protected payloads such as cookies or temporary protected values; do not treat it as universal database encryption.
