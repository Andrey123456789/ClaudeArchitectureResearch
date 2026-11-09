---
name: authentication
description: >
  Use for login, identity, and endpoint protection: JWT bearer/OIDC, ASP.NET
  Core Identity, cookies and CSRF, authorization policies, claims, roles,
  resource authorization, current user, 401/403.
---

> Knowledge skill. Owns: authentication and authorization technique and examples · Scope: backend, frontend · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/security.md, .claude/rules/api.md

# Authentication and Authorization

Rules: `security.md` (server-side authorization, deliberate anonymous access,
platform authentication mechanisms, token validation, failure detail, CSRF,
token storage, secrets) and `api.md` (401/403/404 semantics). Changing the
authentication/authorization architecture or adding external identity is
Reserved (CLAUDE.md, Decision Control). Authentication determines who the
caller is; authorization determines what an authenticated caller may do.

## Choosing Authentication

Choose the scheme according to the actual application:

- Bearer/OIDC for an SPA calling an API;
- cookies for server-rendered interactive web applications;
- ASP.NET Core Identity when the application owns local users and passwords;
- an external OpenID Connect/OAuth provider when identity is delegated.

A business entity named `User` or profile management does not by itself call
for ASP.NET Core Identity; Identity fits when the application owns local
accounts and credentials and needs its account-management capabilities. When an
existing identity provider already issues tokens, the API validates them rather
than issuing custom JWTs.

## Local User Accounts

When the application owns passwords, rely on the framework's password hashing,
lockout, reset-token, and related features (platform-mechanism rule:
`security.md`).

## Bearer Authentication

Configure validation according to the issuer that actually issues tokens.
Signing keys, certificates, and credentials follow the configuration and
secrets rules.

## Authorization

```csharp
[Authorize]
[ApiController]
[Route("api/orders")]
public sealed class OrdersController : ControllerBase
{
}
```

With a secure global/fallback policy, repeating `[Authorize]` is unnecessary and
`[AllowAnonymous]` marks the deliberate exceptions.

## Policy-Based Authorization

Prefer policies when authorization is more than a trivial role check:

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

Roles fit a genuinely role-oriented business model. Avoid scattering compound
role strings; a policy can express one capability backed by several roles or
claims.

## Resource-Based Authorization

Some permissions depend on the resource — a user edits only their own record,
a project member updates only their projects, administrators access any record.
Use ASP.NET Core resource authorization or explicit Application authorization
logic.

## 401 vs 403

```text
not authenticated / authentication failed -> 401 Unauthorized
authenticated but not permitted           -> 403 Forbidden
```

Authentication and authorization middleware produce these responses in most
cases, rather than controllers manufacturing them.

## Current User

Controllers may use `User` for purely HTTP-specific information:

```csharp
[Authorize]
[HttpGet("me")]
public ActionResult<CurrentUserResponse> GetCurrentUser()
{
    var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);

    return Ok(new CurrentUserResponse(userId));
}
```

When use cases repeatedly need caller identity, define a small Application
abstraction and implement the HTTP-specific adapter at an outer boundary, so
Application services do not depend on `HttpContext`, `ClaimsPrincipal`, or
`IHttpContextAccessor`:

```csharp
public interface ICurrentUser
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}
```

Passing an explicit user identifier is simpler when it suffices.

## Cookies and Bearer Tokens

Bearer tokens sent explicitly in the `Authorization` header have different CSRF
characteristics than cookies sent automatically by the browser (CSRF rule:
`security.md`, Browser Credentials).

## Testing

Test authorization behavior for important protected operations:

- unauthenticated request → `401`;
- authenticated caller without permission → `403`;
- permitted caller → expected success;
- resource-specific ownership rules;
- intended anonymous endpoints remain accessible.

Verify observable behavior, not only the presence of `[Authorize]`.

## Anti-Patterns

- hardcoded signing keys;
- Application depending on `HttpContext`;
- role or permission magic strings scattered through the codebase;
- adding Identity, JWT issuance, or OIDC infrastructure without an actual need.
