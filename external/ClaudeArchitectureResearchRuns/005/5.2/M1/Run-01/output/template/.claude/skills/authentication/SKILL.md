---
name: authentication
description: >
  Authentication/authorization for the API: JWT bearer/OIDC, Identity, cookies
  and CSRF, [Authorize], fallback and resource policies, current user, token
  storage, 401/403.
---

> **Knowledge skill** · Owns: authentication/authorization technique and examples · Scope: backend, frontend · Loading: on demand

# Authentication and Authorization

## Rules

Rules: `security.md` → Authentication and Authorization, Browser Credentials and
Tokens, Fail-Safe Security Checks; `api.md` → HTTP Semantics (`401`/`403`).
Changing authentication/authorization architecture is Reserved.

1. Authentication determines who the caller is.
2. Authorization determines what an authenticated caller may do.
3. Prefer policies when authorization logic is more than a trivial role check.
4. Keep ASP.NET Core transport/authentication types out of Domain.

## Choosing Authentication

Choose the scheme according to the actual application.

Common options include:

- Bearer/OIDC for an SPA calling an API;
- cookies for server-rendered interactive web applications;
- ASP.NET Core Identity when the application owns local users/passwords;
- an external OpenID Connect/OAuth provider when identity is delegated.

Do not add ASP.NET Core Identity merely because the application contains a
business entity named `User` or supports user/profile management.

Use ASP.NET Core Identity when the application owns local identity accounts,
credentials/passwords, and needs Identity's account-management capabilities.

Do not issue custom JWTs merely because the API needs authentication if an
existing identity provider already owns token issuance.

## Local User Accounts

When the application owns passwords, use ASP.NET Core Identity's password
hashing, lockout, reset-token, and related security features (`security.md` →
Authentication and Authorization).

## Bearer Authentication

A Controller API used by a browser SPA commonly authenticates access tokens
through Bearer authentication.

Configure token validation according to the issuer that actually issues tokens
(`security.md` → Authentication and Authorization):

```csharp
builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = builder.Configuration["Authentication:Authority"];
        options.Audience = builder.Configuration["Authentication:Audience"];
    });
```

With an authority, issuer and signing keys come from the provider's metadata.

Secrets, signing keys, certificates, and credentials must follow the project's
configuration/security rules.

## Authorization

Use `[Authorize]` or project-wide authorization policy as appropriate.

```csharp
[Authorize]
[ApiController]
[Route("api/orders")]
public sealed class OrdersController : ControllerBase
{
}
```

A secure global/fallback policy may make repeating `[Authorize]` unnecessary.

Anonymous access should be deliberate:

```csharp
[AllowAnonymous]
```

when the project otherwise defaults to authenticated access.

## Policy-Based Authorization

Prefer policies for meaningful capabilities.

```csharp
builder.Services.AddAuthorizationBuilder()
    .AddPolicy(
        "CanManageOrders",
        policy => policy
            .RequireAuthenticatedUser()
            .RequireClaim("permission", "orders:write"));
```

```csharp
[Authorize(Policy = "CanManageOrders")]
[HttpPost]
public async Task<ActionResult<OrderResponse>> Create(...)
{
    ...
}
```

Use stable constants for policy names when repeated throughout the application.

## Roles

Roles are appropriate when the business authorization model is genuinely
role-oriented.

Avoid scattering compound role strings everywhere.

Prefer a policy when several roles or claims represent one business capability.

## Resource-Based Authorization

Some permissions depend on the actual resource.

Examples:

- user may edit only their own record;
- project member may update only projects they belong to;
- administrators may access any record.

Use ASP.NET Core resource authorization or explicit Application authorization
logic where appropriate.

Client-side checks are UX; server-side checks are security (`security.md`).

## 401 vs 403

Semantics: `api.md` → HTTP Semantics. Authentication/authorization middleware
should normally generate these responses rather than controllers manually
manufacturing them. Detailed HTTP status semantics belong to the `http-api`
skill.

## Current User

Controllers may use `User` when information is purely HTTP/API-specific.

```csharp
[Authorize]
[HttpGet("me")]
public ActionResult<CurrentUserResponse> GetCurrentUser()
{
    var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);

    return Ok(new CurrentUserResponse(userId));
}
```

When Application use cases repeatedly require caller identity, define a small
Application abstraction such as:

```csharp
public interface ICurrentUser
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}
```

Implement the HTTP-specific adapter at an outer boundary.

Do not make Application services depend directly on `HttpContext`,
`ClaimsPrincipal`, or `IHttpContextAccessor`.

Do not create `ICurrentUser` if passing an explicit user identifier is simpler.

## Cookie Authentication and CSRF

Rule: `security.md` → Browser Credentials and Tokens. ASP.NET Core antiforgery
(`AddAntiforgery`, a header-based token for SPA requests) is the usual mechanism
when cookies carry authentication.

## Token Storage

Rule: `security.md` → Browser Credentials and Tokens; signing secrets follow
`security.md` → Secrets.

## Authentication Errors

Rule: `security.md` → Authentication and Authorization. Return the same generic
failure for an unknown user and a wrong password.

## Testing

Test authorization behavior for important protected operations.

Useful integration cases include:

- unauthenticated request → `401`;
- authenticated caller without permission → `403`;
- permitted caller → expected success;
- resource-specific ownership rules;
- anonymous endpoint remains accessible when intended.

Do not test only the presence of `[Authorize]`; verify actual observable behavior.

## Anti-Patterns

Avoid:

- hardcoded signing keys;
- Application depending on `HttpContext`;
- role/permission magic strings scattered throughout the codebase;
- adding Identity, JWT issuance, or OIDC infrastructure without an actual need.
