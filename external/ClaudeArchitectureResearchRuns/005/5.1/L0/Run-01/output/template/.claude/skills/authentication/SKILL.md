---
name: authentication
description: >
  Use when implementing login, endpoint protection, roles, claims, policies or
  JWT/OIDC/cookie auth: scheme choice, token validation, fallback policy,
  resource authorization, current user, 401/403 tests.
---

> Level: 2 Technology · Owns: authentication and authorization technique · Scope: backend · Loads: on demand (knowledge skill)

# Authentication and Authorization

Policy owners: `.claude/rules/0-core/security-principles.md` (server-side authorization, deliberate anonymous access, fail-safe checks, no custom password/token crypto, effective token validation, enumeration, CSRF, token storage), `.claude/rules/2-technology/aspnet-core.md` (established facilities), `.claude/rules/1-architecture/entry-points.md` (401/403/404 semantics), `.claude/rules/1-architecture/backend-layers.md` (transport types stay out of Application and Domain). Changing the authentication architecture is Reserved.

Authentication establishes who the caller is; authorization decides what the authenticated caller may do.

## Choosing a scheme

| Situation | Typical scheme |
|---|---|
| SPA calling the API | Bearer tokens (JWT) issued by an OpenID Connect provider |
| Server-rendered interactive web app | Cookies |
| Application owns local users and passwords | ASP.NET Core Identity |
| Identity delegated to an external provider | OpenID Connect / OAuth |

Issue custom JWTs only when no existing identity provider owns token issuance for the application.

## Bearer authentication

```csharp
builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = builder.Configuration["Jwt:Authority"];   // metadata supplies issuer and signing keys
        options.Audience = builder.Configuration["Jwt:Audience"];
    });
```

With an authority, issuer and signing keys come from the provider's metadata; issuer, audience, signature and lifetime validation remain enabled by default. Signing keys, certificates and client secrets come from the configuration secret sources (`configuration` skill).

## Endpoint protection

```csharp
builder.Services.AddAuthorizationBuilder()
    .SetFallbackPolicy(new AuthorizationPolicyBuilder().RequireAuthenticatedUser().Build())
    .AddPolicy(Policies.CanManageOrders, policy => policy
        .RequireAuthenticatedUser()
        .RequireClaim("permission", "orders:write"));

[Authorize(Policy = Policies.CanManageOrders)]
[HttpPost]
public async Task<ActionResult<OrderResponse>> Create(...) { ... }

[AllowAnonymous]
[HttpGet("public-catalog")]
public async Task<ActionResult<CatalogResponse>> GetCatalog(...) { ... }
```

With a secure fallback policy, repeating `[Authorize]` on every controller is unnecessary; anonymous endpoints are marked explicitly. Keep policy names in constants (`Policies.CanManageOrders`).

## Roles and policies

Roles fit a genuinely role-oriented model; prefer a policy when several roles or claims represent one capability, and avoid compound role strings scattered through the code.

## Resource-based authorization

For "users edit only their own record", "members update only their projects", "administrators access everything":

```csharp
var result = await authorizationService.AuthorizeAsync(User, project, Operations.Update);
if (!result.Succeeded)
    return Forbid();
```

or explicit Application authorization logic fed by a current-user abstraction.

## 401 versus 403

Authentication/authorization middleware produces `401` (not authenticated) and `403` (authenticated, not permitted) — controllers rarely manufacture them. A deliberate, consistent `404` for hidden resources is a project-level security decision.

## Current user

Controllers may read `User` for purely HTTP concerns:

```csharp
[HttpGet("me")]
public ActionResult<CurrentUserResponse> GetCurrentUser() =>
    Ok(new CurrentUserResponse(User.FindFirstValue(ClaimTypes.NameIdentifier)));
```

When Application use cases repeatedly need caller identity, define a small Application abstraction and implement it at an outer boundary:

```csharp
public interface ICurrentUser            // Application
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}

internal sealed class HttpCurrentUser(IHttpContextAccessor accessor) : ICurrentUser   // Api
{
    public string? UserId => accessor.HttpContext?.User.FindFirstValue(ClaimTypes.NameIdentifier);
    public bool IsAuthenticated => accessor.HttpContext?.User.Identity?.IsAuthenticated ?? false;
}
```

Skip the abstraction when passing an explicit user id is simpler.

## Local accounts with Identity

Use Identity's password hashing, lockout, email confirmation and reset-token providers (`AddIdentityCore<TUser>()` with the EF Core stores). A common anti-enumeration technique: login and password-reset endpoints answer unknown accounts and wrong passwords with the same response shape and timing class.

## Cookies and CSRF

Cookie authentication sends credentials automatically; protect state-changing requests (ASP.NET Core antiforgery, `SameSite` cookies, Angular's `XSRF-TOKEN` cookie/header convention with `withXsrfConfiguration`). Bearer tokens attached explicitly through the `Authorization` header have different CSRF characteristics.

## Token storage in the browser

Options to weigh against the threat model: in-memory tokens with refresh through a backend-for-frontend, `HttpOnly` cookies with CSRF protection, or browser storage APIs (exposed to XSS). Document the choice.

## Testing

Integration cases: unauthenticated → `401`; authenticated without permission → `403`; permitted → success; resource ownership rules; intended anonymous endpoints remain reachable. Test observable behavior, not merely the presence of `[Authorize]`. A test authentication handler (`AddAuthentication("Test").AddScheme<AuthenticationSchemeOptions, TestAuthHandler>("Test", _ => { })` inside `ConfigureTestServices`) keeps tests independent of a real identity provider.

## Review cues

Custom password hashing, disabled token validation, hardcoded signing keys, Angular-only authorization, Application depending on `HttpContext`/`ClaimsPrincipal`/`IHttpContextAccessor`, `401` for forbidden users or `403` for anonymous ones, logged tokens, magic role strings, Identity/JWT issuance/OIDC infrastructure added without need.
