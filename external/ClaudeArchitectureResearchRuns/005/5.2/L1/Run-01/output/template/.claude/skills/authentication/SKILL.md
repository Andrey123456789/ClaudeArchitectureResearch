---
name: authentication
description: >
  Use for login, identity, or endpoint protection: JWT bearer and OIDC, cookies
  and CSRF, ASP.NET Core Identity, policies, claims, roles, resource
  authorization, 401/403.
---
> Level: 2-technology | Owns: ASP.NET Core authentication and authorization technique | Scope: backend, frontend | Loads: on demand (skill)

# Authentication and Authorization

Policy: `security.md` (server authorization, deliberate anonymous access,
platform mechanisms, token validation, enumeration, CSRF, token storage),
`http-api.md` (401/403 semantics). Changing the authentication or
authorization architecture is Reserved.

Authentication determines who the caller is; authorization determines what an
authenticated caller may do.

## Choosing authentication

- Bearer/OIDC for a browser frontend calling the API;
- cookies for server-rendered interactive web applications;
- ASP.NET Core Identity when the application owns local accounts and passwords
  and needs Identity's account management;
- an external OpenID Connect/OAuth provider when identity is delegated.

Do not add Identity merely because a business entity is called `User`, and do
not issue custom JWTs when an existing identity provider owns token issuance.
For local accounts use Identity's password hashing, lockout, and reset tokens.

## Bearer authentication

```csharp
builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = builder.Configuration["Authentication:Authority"];
        options.Audience = builder.Configuration["Authentication:Audience"];
    });
```

With `Authority`, signing keys and issuer come from the provider metadata.
Signing keys, certificates, and secrets follow the configuration and security
rules.

## Authorization

```csharp
[Authorize]
[ApiController]
[Route("api/orders")]
public sealed class OrdersController : ControllerBase { }
```

A secure fallback policy can make repeated `[Authorize]` unnecessary:

```csharp
builder.Services.AddAuthorizationBuilder()
    .SetFallbackPolicy(new AuthorizationPolicyBuilder()
        .RequireAuthenticatedUser()
        .Build());
```

Then mark deliberate public endpoints with `[AllowAnonymous]`.

## Policies and roles

```csharp
builder.Services.AddAuthorizationBuilder()
    .AddPolicy("CanManageOrders", policy => policy
        .RequireAuthenticatedUser()
        .RequireClaim("permission", "orders:write"));

[Authorize(Policy = "CanManageOrders")]
[HttpPost]
public async Task<ActionResult<OrderResponse>> Create(...) { ... }
```

Prefer policies when logic exceeds a trivial role check or when several roles
or claims represent one capability; use constants for repeated policy names;
avoid compound role strings scattered through the code.

## Resource-based authorization

For "edit only your own record" or "members only" rules, use
`IAuthorizationService.AuthorizeAsync(User, resource, requirement)` with an
`AuthorizationHandler<TRequirement, TResource>`, or explicit use-case
authorization logic.

## 401 vs 403

```text
not authenticated / authentication failed → 401
authenticated but not permitted           → 403
```

Let authentication/authorization middleware produce these responses. A
deliberate `404` for some forbidden lookups must be a consistent policy.

## Current user

Controllers may use `User` for purely HTTP-specific information:

```csharp
var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
```

When use cases repeatedly need caller identity, define a small use-case-side
contract implemented by an outer adapter — use-case code never depends on
`HttpContext`, `ClaimsPrincipal`, or `IHttpContextAccessor`. Skip the
abstraction when passing an explicit user identifier is simpler.

```csharp
public interface ICurrentUser
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}
```

## Cookies and CSRF

With cookie authentication, use ASP.NET Core antiforgery for state-changing
requests (the frontend sends the antiforgery token in a header); explicit
`Authorization: Bearer` headers have different CSRF characteristics.

## Testing

Integration tests for important protected operations: unauthenticated → `401`;
authenticated without permission → `403`; permitted → success; ownership
rules; intended anonymous endpoints stay reachable. Test observable behavior,
not the presence of `[Authorize]`.

## Anti-patterns

Custom password hashing; disabled token validation; hardcoded signing keys;
authorization only in the frontend; use-case code depending on `HttpContext`;
`401` for forbidden or `403` for unauthenticated callers; logged tokens;
scattered role/permission magic strings; Identity, JWT issuance, or OIDC
infrastructure without an actual need.
