---
name: authentication
description: >
  Use for login, identity, JWT bearer/OIDC, cookies, ASP.NET Core Identity,
  authorization policies, roles, claims, resource authorization, current-user
  access, or 401/403 behavior.
---

> Knowledge skill · Authentication and authorization technique · Policy: `.claude/rules/security.md` § Authentication and Authorization, `.claude/rules/api.md` § HTTP Semantics · Architecture changes: Reserved (`CLAUDE.md` § Decision Control)

# Authentication and Authorization

Authentication determines who the caller is; authorization determines what an
authenticated caller may do. Prefer policies when authorization logic is more
than a trivial role check, and keep ASP.NET Core transport/authentication types
out of Domain.

## Choosing Authentication

Choose the scheme according to the actual application: Bearer/OIDC for an SPA
calling an API, cookies for server-rendered interactive web applications,
ASP.NET Core Identity when the application owns local users and passwords, an
external OpenID Connect/OAuth provider when identity is delegated.

Do not add ASP.NET Core Identity merely because the application has a business
entity named `User` or supports profile management; use it when the
application owns local identity accounts and credentials and needs Identity's
account-management capabilities. Do not issue custom JWTs when an existing
identity provider already owns token issuance.

## Local User Accounts

When the application owns passwords, use the framework's password hashing,
lockout, reset-token, and related features (ASP.NET Core Identity). Never store
plaintext passwords or authentication secrets in application source.

## Bearer Authentication

A Controller API used by an SPA commonly authenticates access tokens through
Bearer authentication; configure validation according to the issuer that
actually issues the tokens. Signing keys, certificates, and credentials follow
the project's configuration and security rules.

## Authorization

```csharp
[Authorize]
[ApiController]
[Route("api/orders")]
public sealed class OrdersController : ControllerBase
{
}
```

A secure global/fallback policy may make repeating `[Authorize]` unnecessary.
When the project defaults to authenticated access, mark deliberate exceptions:

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

Roles fit when the business authorization model is genuinely role-oriented.
Avoid scattering compound role strings; prefer a policy when several roles or
claims represent one capability.

## Resource-Based Authorization

Some permissions depend on the resource: users edit only their own record,
project members update only their projects, administrators access any record.
Use ASP.NET Core resource authorization or explicit Application authorization
logic where appropriate.

## 401 vs 403

```text
not authenticated / authentication failed
→ 401 Unauthorized

authenticated successfully
but not permitted
→ 403 Forbidden
```

Authentication/authorization middleware generates these responses by default
rather than controllers manufacturing them. A deliberate, consistent `404` for
some forbidden lookups can avoid disclosing existence. Detailed status
semantics: `http-api` skill.

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

When use cases repeatedly need caller identity, define a small Application
abstraction and implement the HTTP-specific adapter at an outer boundary:

```csharp
public interface ICurrentUser
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}
```

Application services do not depend directly on `HttpContext`,
`ClaimsPrincipal`, or `IHttpContextAccessor`. Do not create `ICurrentUser`
when passing an explicit user identifier is simpler.

## Cookies, CSRF, and Tokens

Bearer tokens sent explicitly through the `Authorization` header have different
CSRF characteristics from cookies sent automatically by the browser. Never
commit signing secrets.

## Testing

Test authorization behavior for important protected operations: an
unauthenticated request → `401`; an authenticated caller without permission →
`403`; a permitted caller → expected success; resource-specific ownership rules;
anonymous endpoints remain accessible when intended. Verify observable behavior
rather than the mere presence of `[Authorize]`.

## Review Checks

Check-by-reference against `security.md` § Authentication and Authorization:
custom password hashing; disabled token validation; hardcoded signing keys;
authorization only in the frontend; Application depending on `HttpContext`;
`401` for an authenticated-but-forbidden user or `403` for missing
authentication; logged tokens; scattered role/permission magic strings;
Identity, JWT issuance, or OIDC infrastructure added without an actual need.
