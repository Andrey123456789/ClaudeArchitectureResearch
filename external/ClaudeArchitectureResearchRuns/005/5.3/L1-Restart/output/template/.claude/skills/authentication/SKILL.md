---
name: authentication
description: ASP.NET Core authentication and authorization technique. Use when implementing login, identity, JWT bearer/OIDC, cookies, ASP.NET Core Identity, authorization policies, roles, claims, resource-based authorization, current-user access, password security, CSRF, or 401/403 behavior.
---

> Level: 2-technology · Owns: authentication/authorization technique · Loading: on demand

# Authentication and Authorization

Rules: `.claude/rules/0-core/security.md` § Authentication and authorization; 401/403/404 semantics in `.claude/rules/0-core/http-api.md`; changing authentication/authorization architecture or adding external identity is Reserved. Authentication answers who the caller is; authorization answers what that caller may do.

## Choosing a scheme

- Bearer/OIDC for a browser SPA calling an API;
- cookies for server-rendered interactive applications;
- ASP.NET Core Identity when the application owns local accounts and passwords and needs Identity's account management — not merely because a business entity is named `User`;
- an external OpenID Connect/OAuth provider when identity is delegated; do not issue custom JWTs when an existing provider already issues tokens.

## Local accounts

Use the framework's password hashing, lockout, and reset-token facilities; never plaintext passwords or authentication secrets in source.

## Bearer validation

Configure validation for the issuer that actually issues tokens (authority/metadata configuration usually establishes issuer, audience, signing keys, and lifetime). Signing keys, certificates, and credentials follow configuration and secret rules.

## Authorization

```csharp
[Authorize]
[ApiController]
[Route("api/orders")]
public sealed class OrdersController : ControllerBase { }
```

A secure global/fallback policy can make repeated `[Authorize]` unnecessary; mark deliberate public endpoints `[AllowAnonymous]`. Prefer policies for meaningful capabilities:

```csharp
builder.Services.AddAuthorizationBuilder()
    .AddPolicy("CanManageOrders", policy => policy
        .RequireAuthenticatedUser()
        .RequireClaim("permission", "orders:write"));

[Authorize(Policy = "CanManageOrders")]
[HttpPost]
public async Task<ActionResult<OrderResponse>> Create(/* ... */) { /* ... */ }
```

Keep policy names in constants when repeated. Use roles when the business model is genuinely role-oriented; prefer a policy when several roles or claims form one capability; avoid scattered compound role strings.

## Resource-based authorization

Permissions that depend on the resource (own records only, project members only, administrators everywhere) use ASP.NET Core resource authorization or explicit use-case authorization logic — never only frontend guards or hidden buttons.

## 401 vs 403

Authentication/authorization middleware normally produces `401` (not authenticated or authentication failed) and `403` (authenticated, not permitted) rather than controllers manufacturing them. A deliberate `404` for some forbidden lookups must be a consistent policy (`http-api`).

## Current user

Controllers may read `User` for HTTP-specific needs:

```csharp
[Authorize]
[HttpGet("me")]
public ActionResult<CurrentUserResponse> GetCurrentUser() =>
    Ok(new CurrentUserResponse(User.FindFirstValue(ClaimTypes.NameIdentifier)));
```

When use cases repeatedly need caller identity, define a small use-case-layer abstraction and implement the HTTP adapter at an outer boundary; use-case code never depends on `HttpContext`, `ClaimsPrincipal`, or `IHttpContextAccessor`. Passing an explicit user id is fine when simpler.

```csharp
public interface ICurrentUser
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}
```

## Cookies and tokens

Cookie-borne credentials need CSRF protection in the design; Bearer tokens explicitly sent in the `Authorization` header behave differently. Never log access or refresh tokens or commit signing secrets; choose browser token storage by threat model.

## Testing

Integration-test important protected operations: unauthenticated → `401`; authenticated without permission → `403`; permitted → success; ownership rules; intentionally anonymous endpoints stay reachable. Verify behavior, not just attribute presence.

## Anti-patterns

Custom password hashing; disabled token validation; hardcoded signing keys; authorization only in the frontend; use-case code depending on `HttpContext`; `401` for forbidden or `403` for unauthenticated; logged tokens; scattered permission strings; Identity, JWT issuance, or OIDC infrastructure without an actual need.
