---
name: authentication
description: Use when implementing login, identity, endpoint protection, permissions, roles, claims, JWT bearer/OIDC, ASP.NET Core Identity, cookies, policies, resource authorization, current-user access or 401/403 behavior in the ASP.NET Core API.
---
<!-- Kind: KNW | Scope: backend | Owns: authentication and authorization technique and examples | Loads: on demand (model-invoked) -->
# Authentication and Authorization

Standards: `rules/backend/security.md` (anonymous access, platform mechanisms, Bearer validation, failure detail), `rules/common/security.md` (server authority, secrets, token logging), `rules/frontend/security.md` (CSRF, token storage), `rules/backend/api.md` (401/403). Authentication/authorization architecture changes: CLAUDE.md § Decisions.

Authentication determines who the caller is; authorization determines what an authenticated caller may do. Prefer policies when authorization logic is more than a trivial role check, and keep ASP.NET Core transport/authentication types out of Domain.

## Choosing Authentication

Choose the scheme for the actual application:

- Bearer/OIDC for an SPA calling an API;
- cookies for server-rendered interactive web applications;
- ASP.NET Core Identity when the application owns local users/passwords;
- an external OpenID Connect/OAuth provider when identity is delegated.

A business entity named `User` or profile management is no reason to add Identity; Identity fits when the application owns local accounts, credentials and needs its account-management capabilities. Avoid issuing custom JWTs when an existing identity provider already owns token issuance.

## Local User Accounts

When the application owns passwords, use the framework's password hashing, lockout, reset-token and related security features (ASP.NET Core Identity) — the standard behind this is `rules/backend/security.md` § Authentication and Authorization; secrets: `rules/common/security.md`.

## Bearer Authentication

An Angular SPA calling a Controller API commonly authenticates access tokens through Bearer authentication, configured for the issuer that actually issues the tokens. Signing keys, certificates and credentials follow the configuration and secret standards.

## Authorization

```csharp
[Authorize]
[ApiController]
[Route("api/orders")]
public sealed class OrdersController : ControllerBase
{
}
```

A secure global/fallback policy can make repeating `[Authorize]` unnecessary; anonymous endpoints are then marked deliberately:

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

Use stable constants for policy names that repeat throughout the application.

## Roles

Roles fit a genuinely role-oriented business authorization model. Avoid compound role strings scattered everywhere; prefer a policy when several roles or claims represent one business capability.

## Resource-Based Authorization

Some permissions depend on the resource: a user edits only their own record; a project member updates only their projects; administrators access any record. Use ASP.NET Core resource authorization or explicit Application authorization logic.

## 401 vs 403

```text
not authenticated / authentication failed
→ 401 Unauthorized

authenticated successfully
but not permitted
→ 403 Forbidden
```

Authentication/authorization middleware normally generates these responses rather than controllers manufacturing them. A deliberate `404` for some forbidden lookups (to avoid disclosing existence) is a consistent security policy, not an ad-hoc choice. Detailed status semantics: `http-api` skill.

## Current User

Controllers may use `User` when information is purely HTTP/API-specific:

```csharp
[Authorize]
[HttpGet("me")]
public ActionResult<CurrentUserResponse> GetCurrentUser()
{
    var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);

    return Ok(new CurrentUserResponse(userId));
}
```

When Application use cases repeatedly need caller identity, define a small Application abstraction:

```csharp
public interface ICurrentUser
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}
```

Implement the HTTP-specific adapter at an outer boundary, so Application services do not depend on `HttpContext`, `ClaimsPrincipal` or `IHttpContextAccessor`. Passing an explicit user identifier is simpler when that suffices.

## Cookie Authentication and CSRF

Browser-sent cookie credentials make CSRF part of the design; Bearer tokens explicitly sent in the `Authorization` header have different CSRF characteristics (`rules/frontend/security.md`).

## Token Storage

Client-side token storage follows the application's threat model; signing secrets stay out of source control.

## Authentication Errors

Login endpoints avoid revealing whether an account exists or which credential was wrong when that would help an attacker (`rules/backend/security.md`).

## Testing

Test authorization behavior for important protected operations: unauthenticated request → `401`; authenticated caller without permission → `403`; permitted caller → expected success; resource ownership rules; intended anonymous endpoints stay accessible. Verify observable behavior rather than the mere presence of `[Authorize]`.

## Anti-Patterns

Avoid custom password hashing, disabled token validation, hardcoded signing keys, authorization only in Angular, Application depending on `HttpContext`, `401` for an authenticated-but-forbidden user, `403` for missing authentication, logging tokens, magic role/permission strings scattered through the codebase, and Identity, JWT issuance or OIDC infrastructure without an actual need.
