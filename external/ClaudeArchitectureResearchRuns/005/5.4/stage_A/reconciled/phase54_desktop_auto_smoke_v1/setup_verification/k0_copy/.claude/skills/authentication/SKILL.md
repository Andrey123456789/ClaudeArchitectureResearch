---
name: authentication
description: Use when implementing or reviewing authentication/authorization — schemes, JWT bearer/OIDC, Identity, cookies, policies, claims, roles, resource authorization, current user, 401/403 tests.
---

> Kind: KNW | Scope: backend | Owner: authentication and authorization technique with examples | Loading: on demand (model-invoked knowledge)

# Authentication and Authorization

Rules: `rules/backend/security.md` § Authentication and authorization, `rules/common/security.md` § Authorization authority, `rules/frontend/angular.md` § Browser authentication security, `rules/backend/api.md` (401/403). Authentication architecture changes are Reserved (CLAUDE.md § Decisions).

Authentication establishes who the caller is; authorization decides what an authenticated caller may do. Keep ASP.NET Core transport and authentication types out of Domain.

## Choosing authentication

- Bearer/OIDC for an SPA calling an API;
- cookies for server-rendered interactive web applications;
- ASP.NET Core Identity when the application owns local users, credentials and passwords and needs its account-management capabilities;
- an external OpenID Connect/OAuth provider when identity is delegated.

A business entity named `User` or profile management alone does not call for Identity, and an API needing authentication does not call for custom JWT issuance when an existing identity provider issues tokens.

## Local user accounts

When the application owns passwords, rely on Identity's password hashing, lockout, reset tokens and related features (`rules/backend/security.md` § Authentication and authorization; secrets: `rules/common/security.md` § Secrets).

## Bearer authentication

An Angular SPA calling the API commonly sends access tokens validated by Bearer authentication, configured for the issuer that actually issues the tokens (issuer, audience, signature, lifetime). Signing keys, certificates and credentials follow the configuration and secret rules.

## Authorization

```csharp
[Authorize]
[ApiController]
[Route("api/orders")]
public sealed class OrdersController : ControllerBase
{
}
```

With a secure global/fallback policy, public endpoints carry an explicit `[AllowAnonymous]` (`rules/backend/security.md` § Authentication and authorization).

## Policies

Prefer policies for meaningful capabilities, with stable constants for repeated policy names:

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

Roles fit a genuinely role-oriented model; when several roles or claims represent one business capability, a policy avoids scattered compound role strings.

## Resource-based authorization

Some permissions depend on the resource: users editing only their own records, project members updating only their projects, administrators accessing any record. Use ASP.NET Core resource authorization or explicit Application authorization logic.

## 401 vs. 403

```text
not authenticated / authentication failed      -> 401 Unauthorized
authenticated successfully but not permitted   -> 403 Forbidden
```

Authentication/authorization middleware produces these; controllers do not manufacture them. A deliberate `404` for some forbidden lookups hides existence when that is a consistent policy (`http-api`).

## Current user

Controllers may read `User` for purely HTTP/API-specific needs:

```csharp
[Authorize]
[HttpGet("me")]
public ActionResult<CurrentUserResponse> GetCurrentUser()
{
    var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);

    return Ok(new CurrentUserResponse(userId));
}
```

When Application use cases repeatedly need caller identity, define a small abstraction implemented by an HTTP-specific adapter at an outer boundary, so Application services do not depend on `HttpContext`, `ClaimsPrincipal` or `IHttpContextAccessor`. Passing an explicit user identifier is simpler when it suffices.

```csharp
public interface ICurrentUser
{
    string? UserId { get; }
    bool IsAuthenticated { get; }
}
```

## Cookies, CSRF and token storage

Cookies sent automatically by the browser bring CSRF into the design; tokens attached explicitly in the `Authorization` header have different CSRF characteristics. Browser token storage is a threat-model decision; access and refresh tokens and signing secrets stay out of logs and source control.

## Testing

Test observable authorization behavior for important protected operations — unauthenticated → `401`, authenticated without permission → `403`, permitted caller → success, resource ownership rules, intended anonymous endpoints staying reachable — rather than only the presence of `[Authorize]`.

## Common mistakes

Custom password hashing; disabled token validation; hardcoded signing keys; authorization only in Angular; Application depending on `HttpContext`; `401` for an authenticated-but-forbidden user or `403` for missing authentication; logged tokens; scattered role/permission strings; Identity, JWT issuance or OIDC infrastructure without an actual need.
