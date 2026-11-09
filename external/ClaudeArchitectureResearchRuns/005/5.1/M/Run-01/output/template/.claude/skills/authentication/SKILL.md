---
name: authentication
description: >
  Use when implementing login, identity, endpoint protection, permissions,
  roles, claims, JWT bearer or OIDC, ASP.NET Core Identity, cookies,
  authorization policies, resource-based authorization, current-user access,
  or authorization tests.
---

> Owns: ASP.NET Core authentication/authorization technique | Scope: backend | Loads: on demand (knowledge skill)

# Authentication and Authorization

Policy owners: server-side authorization, deliberate anonymous access,
established mechanisms, token validation, enumeration-safe errors, CSRF, token
storage → `.claude/rules/security.md`; `401`/`403`/hiding with `404` →
`.claude/rules/api.md`; keeping `HttpContext` out of Application →
`.claude/rules/architecture.md`. Changing authentication/authorization
architecture is Reserved (`CLAUDE.md`).

Authentication determines who the caller is; authorization determines what the
authenticated caller may do.

## Choosing a Scheme

| Situation | Typical choice |
|---|---|
| Angular SPA calling the API | Bearer/OIDC with an identity provider |
| Server-rendered interactive web app | Cookies |
| Application owns local users and passwords | ASP.NET Core Identity |
| Identity delegated to a provider | External OpenID Connect/OAuth |

A business entity named `User` or profile management does not by itself call for
ASP.NET Core Identity; use it when the application owns credentials and needs
Identity's account management (hashing, lockout, reset tokens). Do not issue
custom JWTs when an existing identity provider already issues tokens.

## Bearer Authentication

```csharp
builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = builder.Configuration["Authentication:Authority"];
        options.Audience = builder.Configuration["Authentication:Audience"];
    });
```

With `Authority`, signing keys and issuer come from the provider's metadata;
configure audience and lifetime validation according to the issuer. Signing
keys, certificates, and credentials are supplied through configuration and the
secret mechanisms in `security.md`.

## Endpoint Protection

```csharp
// Secure fallback: every endpoint requires an authenticated user unless opted out
builder.Services.AddAuthorizationBuilder()
    .SetFallbackPolicy(new AuthorizationPolicyBuilder().RequireAuthenticatedUser().Build());

[AllowAnonymous]
[HttpGet("public-info")]
public ActionResult<PublicInfo> GetPublicInfo() => ...;
```

Or apply `[Authorize]` at controller level when no fallback policy is used.

## Policies and Roles

```csharp
builder.Services.AddAuthorizationBuilder()
    .AddPolicy(Policies.CanManageOrders, policy => policy
        .RequireAuthenticatedUser()
        .RequireClaim("permission", "orders:write"));

[Authorize(Policy = Policies.CanManageOrders)]
[HttpPost]
public async Task<ActionResult<OrderResponse>> Create(...) { ... }
```

Prefer policies for meaningful capabilities and stable constants for policy
names. Roles fit genuinely role-oriented models; wrap compound role sets in a
policy rather than scattering role strings.

## Resource-Based Authorization

```csharp
var result = await authorizationService.AuthorizeAsync(User, order, Policies.CanEditOrder);
if (!result.Succeeded)
    return Forbid();
```

Implement the rule in an `AuthorizationHandler<TRequirement, TResource>` or in
explicit Application authorization logic (for example "members may update only
their projects; administrators may update any").

## Current User

Controllers may read `User` for purely HTTP concerns:

```csharp
var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
```

When Application use cases repeatedly need the caller, define a small
abstraction and implement it at the Api boundary:

```csharp
public interface ICurrentUser
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}
```

Skip it when passing an explicit user identifier is simpler.

## Cookies and CSRF

With cookie authentication, enable antiforgery for state-changing requests
(`builder.Services.AddAntiforgery(o => o.HeaderName = "X-XSRF-TOKEN")` with the
Angular `withXsrfConfiguration` cookie/header pair). Bearer tokens sent
explicitly in the `Authorization` header have different CSRF characteristics.

## Testing

Integration-test observable authorization behavior for important operations:
unauthenticated → `401`; authenticated without permission → `403`; permitted →
success; ownership rules; intended anonymous endpoints stay reachable. Do not
test only the presence of `[Authorize]`.

## Pitfalls

Role/permission magic strings scattered through the codebase; controllers
manually manufacturing `401`/`403` that middleware should produce; adding
Identity, JWT issuance, or OIDC infrastructure without an actual need.
