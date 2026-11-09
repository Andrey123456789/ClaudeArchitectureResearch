---
name: authentication
description: >
  Use when implementing login or endpoint protection: JWT bearer, OIDC,
  cookies, ASP.NET Core Identity, [Authorize] and fallback policies, policy,
  role, claim, or resource authorization, ICurrentUser, 401/403, CSRF, token
  storage, auth tests.
---

> Owner: authentication and authorization technique (normative policy lives in rules) | Scope: backend | Loads: on demand — knowledge | Enforced: none

# Authentication and Authorization

Policy: `.claude/rules/security.md` § Authentication and Authorization and
§ Browser Credentials, `.claude/rules/api.md` § HTTP Semantics (401/403). Adding
or changing authentication architecture is a Reserved decision
(`CLAUDE.md` § Decision Control).

Authentication determines who the caller is; authorization determines what an
authenticated caller may do. Keep ASP.NET Core transport and authentication types
out of Domain and Application.

## Choosing Authentication

Choose the scheme from the actual application:

- Bearer/OIDC for an SPA calling an API;
- cookies for server-rendered interactive web applications;
- ASP.NET Core Identity when the application owns local users and passwords;
- an external OpenID Connect/OAuth provider when identity is delegated.

A business entity named `User` or profile management does not by itself call for
Identity; use Identity when the application owns local accounts and credentials
and needs its account-management capabilities. When an identity provider already
issues tokens, do not issue custom JWTs.

## Local User Accounts

With ASP.NET Core Identity, use its password hashing, lockout, reset-token, and
related features rather than plaintext storage, custom hashing, or invented reset
tokens, and keep authentication secrets out of source.

## Bearer Authentication

Configure validation for the issuer that actually issues the tokens; with an
authority, metadata supplies signing keys and the issuer:

```csharp
builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = builder.Configuration["Authentication:Authority"];
        options.Audience = builder.Configuration["Authentication:Audience"];
    });
```

Signing keys, certificates, and credentials come from configuration and secret
mechanisms (`configuration` skill).

## Authorization

```csharp
[Authorize]
[ApiController]
[Route("api/orders")]
public sealed class OrdersController : ControllerBase
{
}
```

A secure fallback policy can make repeated `[Authorize]` unnecessary:

```csharp
builder.Services.AddAuthorizationBuilder()
    .SetFallbackPolicy(new AuthorizationPolicyBuilder()
        .RequireAuthenticatedUser()
        .Build());
```

Mark deliberately public endpoints with `[AllowAnonymous]`.

## Policy-Based Authorization

Prefer policies for meaningful capabilities and anything beyond a trivial role
check:

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

Use stable constants for policy names repeated across the application.

## Roles

Roles fit a genuinely role-oriented business model. Avoid compound role strings
scattered through the code; prefer a policy when several roles or claims
represent one business capability.

## Resource-Based Authorization

Some permissions depend on the resource: users may edit only their own records,
project members may update only their projects, administrators may access any
record. Use ASP.NET Core resource authorization (`IAuthorizationService` with a
requirement and handler) or explicit Application authorization logic:

```csharp
var result = await authorizationService.AuthorizeAsync(
    User, order, OrderOperations.Edit);

if (!result.Succeeded)
{
    return Forbid();
}
```

## 401 vs. 403

```text
not authenticated / authentication failed
→ 401 Unauthorized

authenticated successfully
but not permitted
→ 403 Forbidden
```

Authentication and authorization middleware normally produce these responses
rather than controllers manufacturing them. A deliberate `404` for forbidden
lookups (hiding existence) is a project-wide security policy decision.

## Current User

Controllers may use `User` for purely HTTP/API-specific information:

```csharp
[Authorize]
[HttpGet("me")]
public ActionResult<CurrentUserResponse> GetCurrentUser()
{
    var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);

    return Ok(new CurrentUserResponse(userId));
}
```

When Application use cases repeatedly need caller identity, define a small
Application abstraction and implement the HTTP adapter at an outer boundary:

```csharp
public interface ICurrentUser
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}
```

This keeps `HttpContext`, `ClaimsPrincipal`, and `IHttpContextAccessor` out of
Application services (`.claude/rules/architecture.md` § Application). Passing an explicit user identifier is simpler when that
suffices.

## Cookie Authentication and CSRF

Bearer tokens sent explicitly in the `Authorization` header have different CSRF
characteristics from cookies sent automatically by the browser. For cookie-based
APIs, ASP.NET Core antiforgery (`AddAntiforgery`, a header token the Angular
client reads and echoes) is one standard approach.

## Token Storage

Weigh browser storage options (memory, session storage, cookies with
`HttpOnly`/`SameSite`, a backend-for-frontend) against the application's threat
model, and keep signing secrets out of source control.

## Authentication Errors

Login endpoints return the same generic failure for unknown accounts and wrong
passwords where account enumeration matters, and avoid detail that helps an
attacker distinguish secrets or account state.

## Testing

Test authorization behavior for important protected operations, typically in
integration tests:

- unauthenticated request → `401`;
- authenticated caller without permission → `403`;
- permitted caller → expected success;
- resource-specific ownership rules;
- intended anonymous endpoints remain accessible.

Verify observable behavior rather than the mere presence of `[Authorize]`.

## Common Mistakes

- hardcoded signing keys;
- Application code depending on `HttpContext`;
- role or permission magic strings scattered through the codebase;
- adding Identity, JWT issuance, or OIDC infrastructure without an actual need.
