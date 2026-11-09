---
name: authentication
description: >
  Use when implementing login or authorization: JWT bearer/OIDC validation,
  ASP.NET Core Identity, cookies and CSRF, policies, roles, claims,
  resource-based authorization, current user, 401 vs 403.
---

> Kind: KNW | Scope: backend | Capability: — | Loading: on-demand knowledge

# Authentication and Authorization

Policy: `.claude/rules/backend/security.md`, `.claude/rules/common/security.md`, `.claude/rules/frontend/security.md`. A new authentication/authorization architecture is Reserved (`CLAUDE.md`). Authentication determines who the caller is; authorization determines what an authenticated caller may do. Keep ASP.NET Core transport/authentication types out of Domain. Status semantics (401, 403, deliberate 404): `http-api`.

## Choosing authentication

Choose the scheme by the actual application: Bearer/OIDC for a SPA calling an API; cookies for server-rendered interactive web applications; ASP.NET Core Identity when the application owns local users, credentials, and needs account management; an external OpenID Connect/OAuth provider when identity is delegated. A business entity named `User` or profile management does not justify Identity, and do not issue custom JWTs when an existing identity provider owns token issuance.

## Local user accounts

When the application owns passwords, use Identity's password hashing, lockout, reset tokens, and related features; never store plaintext passwords or authentication secrets in source.

## Bearer authentication

Configure token validation for the issuer that actually issues tokens (authority/metadata configuration usually establishes issuer, audience, signature, and lifetime validation). Signing keys, certificates, and credentials follow the configuration/security rules.

## Authorization

```csharp
[Authorize]
[ApiController]
[Route("api/orders")]
public sealed class OrdersController : ControllerBase
{
}
```

A secure global/fallback policy can make repeating `[Authorize]` unnecessary; with an authenticated-by-default policy, mark public endpoints with `[AllowAnonymous]`.

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

Roles fit a genuinely role-oriented model; prefer a policy when several roles or claims represent one capability, and avoid scattered compound role strings.

## Resource-based authorization

Some permissions depend on the resource (users edit only their own records, members update only their projects, administrators access everything). Use ASP.NET Core resource authorization or explicit Application authorization logic; client-side checks are UX.

## 401 vs 403

```text
not authenticated / authentication failed   -> 401
authenticated but not permitted             -> 403
```

Authentication/authorization middleware normally produces these responses rather than controllers manufacturing them.

## Current user

Controllers may read `User` for purely HTTP-specific information:

```csharp
[Authorize]
[HttpGet("me")]
public ActionResult<CurrentUserResponse> GetCurrentUser() =>
    Ok(new CurrentUserResponse(User.FindFirstValue(ClaimTypes.NameIdentifier)));
```

When use cases repeatedly need caller identity, define a small Application abstraction and implement the HTTP adapter at an outer boundary; Application services never depend on `HttpContext`, `ClaimsPrincipal`, or `IHttpContextAccessor`. Skip `ICurrentUser` when passing an explicit user identifier is simpler.

```csharp
public interface ICurrentUser
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}
```

## Cookies, CSRF, and token storage

CSRF and token-storage rules: `.claude/rules/frontend/security.md`. Technique for cookie authentication: ASP.NET Core antiforgery (`AddAntiforgery`, token validation on state-changing endpoints) paired with the SPA's matching XSRF header handling. Signing secrets follow the configuration and secret rules.

## Testing

Test authorization behavior of important protected operations: unauthenticated → 401; authenticated without permission → 403; permitted → expected success; resource ownership rules; intended anonymous endpoints remain accessible. Verify observable behavior, not merely the presence of `[Authorize]`.

## Anti-patterns

Hardcoded signing keys, authorization only in the frontend, Application depending on `HttpContext`, 401 for authenticated-but-forbidden or 403 for missing authentication, role/permission magic strings throughout the codebase, adding Identity, JWT issuance, or OIDC infrastructure without an actual need.
