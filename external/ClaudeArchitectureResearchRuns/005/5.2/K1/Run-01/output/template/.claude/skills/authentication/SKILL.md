---
name: authentication
description: Use when implementing login, identity, endpoint protection, permissions, roles, claims, JWT bearer or OIDC, cookies, ASP.NET Core Identity, authorization policies, resource authorization, current-user access or 401/403 behavior in ASP.NET Core controller APIs.
---
Kind: KNW | Scope: backend | Capability: — | Loading: on invocation

# Authentication and Authorization

Rules: `.claude/rules/backend/security.md` (deliberate anonymous access, platform mechanisms, token validation, enumeration-safe failures), `.claude/rules/common/security.md` (server-side authorization, secrets), `.claude/rules/frontend/frontend.md` (CSRF, token storage), `.claude/rules/backend/http-api.md` (401/403). Changing authentication or authorization architecture is Reserved. Authentication determines who the caller is; authorization determines what an authenticated caller may do.

## Choosing authentication

- Bearer/OIDC for a single-page application calling an API.
- Cookies for server-rendered interactive web applications.
- ASP.NET Core Identity when the application owns local accounts, credentials and passwords and needs Identity's account-management capabilities, not merely because a business entity is named `User`.
- An external OpenID Connect/OAuth provider when identity is delegated; do not issue custom JWTs when an existing identity provider already owns token issuance.

## Local user accounts

Use Identity's password hashing, lockout, reset-token and related features; never store plaintext passwords or authentication secrets in source.

## Bearer authentication

Configure validation according to the issuer that actually issues the tokens:

```csharp
builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = builder.Configuration["Authentication:Authority"];
        options.Audience = builder.Configuration["Authentication:Audience"];
    });
```

With `Authority`, the handler loads signing keys and issuer metadata from the provider. Signing keys, certificates and credentials follow the configuration and secret rules.

## Endpoint authorization

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
    .SetFallbackPolicy(new AuthorizationPolicyBuilder().RequireAuthenticatedUser().Build());
```

Public endpoints are then marked `[AllowAnonymous]`.

## Policies and roles

Prefer policies for meaningful capabilities, with stable constants for repeated policy names:

```csharp
builder.Services.AddAuthorizationBuilder()
    .AddPolicy("CanManageOrders", policy => policy
        .RequireAuthenticatedUser()
        .RequireClaim("permission", "orders:write"));

[Authorize(Policy = "CanManageOrders")]
[HttpPost]
public async Task<ActionResult<OrderResponse>> Create(...) { ... }
```

Roles fit a genuinely role-oriented business model; prefer a policy when several roles or claims represent one capability, and avoid compound role strings scattered through the code.

## Resource-based authorization

Some permissions depend on the resource (users edit only their own record, project members update only their projects, administrators access any record). Use ASP.NET Core resource authorization (`IAuthorizationService.AuthorizeAsync(User, resource, requirement)`) or explicit Application authorization logic. Frontend checks are UX; the server decides.

## 401 versus 403 in practice

Authentication and authorization middleware normally produce `401` and `403`; controllers rarely need to manufacture them. A deliberate `404` for forbidden resource lookups must be a consistent policy (`http-api.md`).

## Current user

Controllers may use `User` for purely HTTP-specific information:

```csharp
[Authorize]
[HttpGet("me")]
public ActionResult<CurrentUserResponse> GetCurrentUser()
    => Ok(new CurrentUserResponse(User.FindFirstValue(ClaimTypes.NameIdentifier)));
```

When Application use cases repeatedly need the caller's identity, define a small Application abstraction and implement the HTTP adapter at an outer boundary; Application services do not depend on `HttpContext`, `ClaimsPrincipal` or `IHttpContextAccessor`. Passing an explicit user identifier is simpler when it suffices.

```csharp
public interface ICurrentUser
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}
```

## Cookies and CSRF

When browsers send cookies automatically, design CSRF protection (ASP.NET Core antiforgery, SameSite cookies) for state-changing operations. Bearer tokens attached explicitly through the `Authorization` header have different CSRF characteristics.

## Testing

Test observable authorization behavior for important protected operations: unauthenticated request → `401`; authenticated caller without permission → `403`; permitted caller → expected success; resource ownership rules; anonymous endpoints remain accessible when intended. Do not test only that `[Authorize]` is present.

## Anti-patterns

Review checks; the named standard owns each rule:

- Custom password hashing, disabled token validation or hardcoded signing keys? (`backend/security.md`, `common/security.md`)
- Authorization only in the frontend? (`common/security.md`)
- Application depending on `HttpContext`?
- `401` for an authenticated-but-forbidden user, or `403` for missing authentication? (`http-api.md`)
- Logged tokens? (`common/security.md`)
- Permission magic strings scattered through the codebase?
- Identity, JWT issuance or OIDC infrastructure added without an actual need? (`CLAUDE.md` → Decision control)
