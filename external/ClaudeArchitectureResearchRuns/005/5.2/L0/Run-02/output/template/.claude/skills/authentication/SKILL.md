---
name: authentication
description: >
  Use for login, identity, JWT bearer/OIDC, ASP.NET Core Identity, cookies, policies,
  roles, claims, resource authorization, current user, 401/403, CSRF, token storage.
---

> Level: 2 Technology · Owns: ASP.NET Core authentication and authorization technique and examples (knowledge) · Scope: backend, frontend · Loads: on invocation · Depends on: .claude/rules/0-core/security-principles.md, .claude/rules/2-technology/aspnet-core.md

# Authentication and Authorization

Policy owners: server-side authorization, deliberate anonymous access, platform mechanisms instead of custom crypto, token validation, enumeration, CSRF, token storage → `.claude/rules/0-core/security-principles.md`; ASP.NET Core facilities → `2-technology/aspnet-core.md`; 401/403/404 semantics → `1-architecture/entry-points.md`; transport types out of Application → same; a new authentication architecture → Reserved (CLAUDE.md). Authentication determines who the caller is; authorization determines what an authenticated caller may do. This skill is technique only.

## Choosing a scheme

- Bearer/OIDC for an SPA calling an API;
- cookies for server-rendered interactive applications;
- ASP.NET Core Identity when the application owns local accounts, passwords, and needs account management — not merely because a business entity is called `User`;
- an external OpenID Connect/OAuth provider when identity is delegated — do not issue custom JWTs when that provider already issues tokens.

## Local accounts

With ASP.NET Core Identity use its password hashing, lockout, reset-token, and related features (credential rules: `security-principles.md`).

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

Authority/metadata configuration lets the handler validate issuer, signature, and lifetime; set additional `TokenValidationParameters` only when the actual issuer requires it. Signing keys and credentials follow the configuration/secrets rules.

## Authorization

```csharp
[Authorize]
[ApiController]
[Route("api/orders")]
public sealed class OrdersController : ControllerBase
{
}
```

A secure fallback policy can make repeated `[Authorize]` unnecessary; mark deliberately public endpoints with `[AllowAnonymous]`:

```csharp
builder.Services.AddAuthorizationBuilder()
    .SetFallbackPolicy(new AuthorizationPolicyBuilder().RequireAuthenticatedUser().Build());
```

## Policies

```csharp
builder.Services.AddAuthorizationBuilder()
    .AddPolicy("CanManageOrders", policy => policy
        .RequireAuthenticatedUser()
        .RequireClaim("permission", "orders:write"));

[Authorize(Policy = "CanManageOrders")]
[HttpPost]
public async Task<ActionResult<OrderResponse>> Create(/* ... */) { /* ... */ }
```

Prefer policies when authorization is more than a trivial role check, and keep policy names in stable constants when they repeat. Use roles when the business model is genuinely role-oriented; prefer one policy over compound role strings scattered through the code.

## Resource-based authorization

Examples: users edit only their own records; project members update only their projects; administrators access any record. Use `IAuthorizationService.AuthorizeAsync(User, resource, requirement)` with an `AuthorizationHandler<TRequirement, TResource>`, or explicit Application authorization logic where appropriate.

## 401 and 403 in practice

The status semantics are owned by `entry-points.md`. In practice the authentication/authorization middleware produces 401 and 403 (challenge and forbid) instead of controllers manufacturing them.

## Current user

Controllers may read `User` for purely API-level information:

```csharp
[Authorize]
[HttpGet("me")]
public ActionResult<CurrentUserResponse> GetCurrentUser() =>
    Ok(new CurrentUserResponse(User.FindFirstValue(ClaimTypes.NameIdentifier)));
```

When use cases repeatedly need the caller's identity, define a small Application abstraction and implement the HTTP adapter at an outer boundary, keeping `HttpContext`, `ClaimsPrincipal`, and `IHttpContextAccessor` in Api (transport types — `aspnet-core.md`):

```csharp
public interface ICurrentUser
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}
```

Skip the abstraction when passing an explicit user identifier is simpler.

## Cookies, CSRF, and token storage

Cookie-carried credentials need antiforgery protection for state-changing requests (ASP.NET Core antiforgery; Angular's `HttpClient` XSRF support with a matching cookie/header name). Bearer tokens sent explicitly in the `Authorization` header have different CSRF characteristics. Choose browser token storage per the application's threat model.

## Testing

Integration cases: unauthenticated → 401; authenticated without permission → 403; permitted → success; resource ownership rules; intended anonymous endpoints stay reachable. Verify observable behavior, not just the presence of `[Authorize]`.

## Anti-patterns

Role/permission magic strings scattered through the codebase.
