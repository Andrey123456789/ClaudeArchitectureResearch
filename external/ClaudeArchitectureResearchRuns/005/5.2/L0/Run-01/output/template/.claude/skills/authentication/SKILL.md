---
name: authentication
description: >
  Use for authentication and authorization: Bearer/OIDC, cookies, Identity, policies, roles, resource authorization, current user, CSRF, 401/403 tests.
---

> Level: 2 Technology | Owns: ASP.NET Core authentication and authorization technique | Scope: backend, frontend | Loads: knowledge skill (on demand) | Depends on: 0-core/security-principles.md, 2-technology/aspnet-core.md

# Authentication Technique

Policy owners (routing): server-side authorization, deliberate anonymous
access, token validation, enumeration safety, CSRF, token storage →
`0-core/security-principles.md`; Identity over custom security →
`2-technology/aspnet-core.md`; `401`/`403` semantics →
`1-architecture/entry-points.md`; changing auth architecture is Reserved
(CLAUDE.md).

Authentication establishes who the caller is; authorization decides what the
caller may do. Keep ASP.NET Core authentication types out of Domain.

## Choosing a Scheme

- Bearer/OIDC for an SPA calling an API.
- Cookies for server-rendered interactive web applications.
- ASP.NET Core Identity when the application owns local accounts and
  passwords and needs account management — not merely because a business entity
  is named `User`.
- An external OpenID Connect/OAuth provider when identity is delegated; do not
  issue custom JWTs when an existing provider already issues tokens.

## Local Accounts

With Identity, use its password hashing, lockout, and reset-token features;
never store plaintext passwords or authentication secrets in source.

## Bearer Validation

```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = builder.Configuration["Authentication:Authority"];
        options.Audience = builder.Configuration["Authentication:Audience"];
    });
```

Authority metadata configures issuer and signing keys; signing keys,
certificates, and credentials follow the configuration and secret rules.

## Authorization

```csharp
[Authorize]
[ApiController]
[Route("api/orders")]
public sealed class OrdersController : ControllerBase { }

// Secure default for every endpoint; opt out with [AllowAnonymous]
builder.Services.AddAuthorizationBuilder()
    .SetFallbackPolicy(new AuthorizationPolicyBuilder().RequireAuthenticatedUser().Build())
    .AddPolicy("CanManageOrders", policy => policy
        .RequireAuthenticatedUser()
        .RequireClaim("permission", "orders:write"));
```

```csharp
[Authorize(Policy = AuthorizationPolicies.CanManageOrders)]
[HttpPost]
public async Task<ActionResult<OrderResponse>> Create(...) { ... }
```

Prefer policies for meaningful capabilities and stable constants for policy
names; use roles when the business model is genuinely role-oriented, and
replace scattered compound role strings with a policy.

## Resource-Based Authorization

For "edit only your own record", "members update their projects",
"administrators access any record", use ASP.NET Core resource authorization
(`IAuthorizationService.AuthorizeAsync(User, resource, requirement)`) or
explicit Application authorization logic.

## 401 and 403

Authentication and authorization middleware normally produce `401` and `403`;
controllers rarely need to build them by hand.

## Current User

Controllers may use `User` for purely HTTP-specific needs:

```csharp
var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
```

When Application use cases repeatedly need the caller, define a small
abstraction and implement it at the outer boundary — or simply pass an explicit
user id when that is simpler:

```csharp
public interface ICurrentUser
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}
```

The adapter keeps `HttpContext`, `ClaimsPrincipal`, and `IHttpContextAccessor`
(transport types, `2-technology/aspnet-core.md`) out of Application.

## Cookies, CSRF, Tokens

Cookie-carried credentials need antiforgery protection for state-changing
requests (ASP.NET Core antiforgery; Angular's XSRF cookie/header support on the
client); Bearer tokens in the `Authorization` header have different CSRF
characteristics.

## Testing

Integration-test protected operations: unauthenticated → `401`; authenticated
without permission → `403`; permitted → success; ownership rules; intended
anonymous endpoints stay reachable. Verify observable behavior, not the mere
presence of `[Authorize]`.
