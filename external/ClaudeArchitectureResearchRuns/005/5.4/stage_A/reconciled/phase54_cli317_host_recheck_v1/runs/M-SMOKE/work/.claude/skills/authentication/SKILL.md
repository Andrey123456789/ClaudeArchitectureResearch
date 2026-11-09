---
name: authentication
description: >
  Use when implementing login, identity, or endpoint protection: auth schemes,
  JWT/OIDC, Identity, cookies and CSRF, policies, roles, claims, resource
  authorization, current user, 401/403.
---

> Owns: authentication and authorization technique and examples (no policy) | Scope: backend, frontend | Loads: on demand (knowledge skill)

# Authentication and Authorization

Policy owners: server-side authorization, anonymous access, platform
mechanisms, token validation, CSRF, token storage, and failure detail —
`.claude/rules/security.md`; 401/403/404 semantics — `.claude/rules/api.md`;
transport types out of Application — `.claude/rules/architecture.md`;
authentication architecture changes — Reserved (CLAUDE.md § Decision Control).

Authentication determines who the caller is; authorization determines what an
authenticated caller may do. Prefer policies when authorization logic is more
than a trivial role check.

## Choosing Authentication

Choose the scheme from the actual application:

- Bearer/OIDC for an SPA calling an API;
- cookies for server-rendered interactive web applications;
- ASP.NET Core Identity when the application owns local users and passwords;
- an external OpenID Connect/OAuth provider when identity is delegated.

Do not add ASP.NET Core Identity merely because there is a business entity named
`User` or user/profile management; use it when the application owns local
identity accounts and credentials and needs Identity's account management. Do
not issue custom JWTs when an existing identity provider already owns token
issuance.

## Local User Accounts

When the application owns passwords, use the framework's password hashing,
lockout, reset-token, and related features; never store plaintext passwords or
authentication secrets in application source.

## Bearer Authentication

An Angular SPA calling a Controller API commonly authenticates with Bearer
tokens. Configure validation for the issuer that actually issues the tokens;
signing keys, certificates, and credentials follow the configuration and
security rules.

## Authorization

Endpoints can be secured through a global or fallback authorization policy,
controller or action authorization attributes, or endpoint authorization
configuration; keep the chosen approach explicit and reviewable.

```csharp
[Authorize]
[ApiController]
[Route("api/orders")]
public sealed class OrdersController : ControllerBase
{
}
```

A secure global/fallback policy can make repeated `[Authorize]` unnecessary;
then mark deliberate public endpoints:

```csharp
[AllowAnonymous]
```

## Policy-Based Authorization

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

Roles fit a genuinely role-oriented business authorization model. Avoid
scattering compound role strings; prefer a policy when several roles or claims
represent one business capability.

## Resource-Based Authorization

Some permissions depend on the resource: a user may edit only their own record; a
project member may update only their projects; administrators may access any
record. Use ASP.NET Core resource authorization or explicit Application
authorization logic.

## 401 vs. 403 in Practice

```text
not authenticated / authentication failed -> 401 Unauthorized
authenticated but not permitted           -> 403 Forbidden
```

Authentication/authorization middleware normally generates these responses
rather than controllers manufacturing them manually.

## Current User

Controllers may use `User` when the information is purely HTTP/API-specific:

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
Application abstraction and implement the HTTP-specific adapter at an outer
boundary, so Application never depends on `HttpContext`, `ClaimsPrincipal`, or
`IHttpContextAccessor`:

```csharp
public interface ICurrentUser
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}
```

Do not create `ICurrentUser` when passing an explicit user identifier is
simpler.

## Cookies and CSRF

Bearer tokens sent explicitly through the `Authorization` header have different
CSRF characteristics from cookies that the browser attaches automatically.

## Testing

Test authorization behavior for important protected operations:

- unauthenticated request → `401`;
- authenticated caller without permission → `403`;
- permitted caller → expected success;
- resource-specific ownership rules;
- anonymous endpoint remains accessible when intended.

Verify observable behavior, not merely the presence of `[Authorize]`.

## Anti-Patterns

Avoid hardcoded signing keys, role/permission magic strings scattered through the
codebase, and adding Identity, JWT issuance, or OIDC infrastructure without an
actual need.
