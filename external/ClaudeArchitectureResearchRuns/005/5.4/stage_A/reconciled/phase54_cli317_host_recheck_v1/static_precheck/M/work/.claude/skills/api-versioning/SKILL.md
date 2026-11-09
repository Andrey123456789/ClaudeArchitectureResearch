---
name: api-versioning
description: >
  Use when introducing or evolving API versions: whether to version,
  Asp.Versioning setup, URL/header/query strategy, breaking vs. compatible
  changes, deprecation, versioned OpenAPI.
---

> Owns: API versioning technique and examples (no policy) | Scope: backend | Loads: on demand (knowledge skill)

# API Versioning

Policy owners: when to version, compatibility, and strategy —
`.claude/rules/api.md` § API Versioning; inner models not duplicated per version
— `.claude/rules/architecture.md` § Boundary Contracts; adopting versioning —
Reserved (CLAUDE.md § Decision Control); package choice — `add-dependency`;
deprecation obligations — `development-workflow`.

Versioning belongs to the API contract, not to Domain or Application. Compatible
additions normally stay in the current version.

## When Versioning Is Useful

Explicit versioning helps when external clients cannot be upgraded atomically
with the server, multiple client generations must coexist, the API is public or
consumed by independent teams, breaking changes are expected, or a migration
window between contracts is required. For a small application whose frontend and
backend deploy together it may add little value; do not add `v1` automatically.

## Strategy

URL-segment versioning is clear for many HTTP APIs:

```text
/api/v1/orders
/api/v2/orders
```

It keeps the version visible in the URI, simplifies routing and
troubleshooting, and produces clear generated documentation. Header and
query-string versioning are the alternatives; when each may be chosen is owned
by `.claude/rules/api.md` § API Versioning.

## Asp.Versioning Setup

```csharp
builder.Services
    .AddApiVersioning(options =>
    {
        options.ReportApiVersions = true;
        options.ApiVersionReader =
            new UrlSegmentApiVersionReader();
    })
    .AddMvc()
    .AddApiExplorer(options =>
    {
        options.GroupNameFormat = "'v'VVV";
        options.SubstituteApiVersionInUrl = true;
    });
```

## Controller Versions

```csharp
[ApiController]
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/orders")]
public sealed class OrdersV1Controller(
    IOrderService orders)
    : ControllerBase
{
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<OrderResponseV1>> GetById(
        Guid id,
        CancellationToken cancellationToken)
    {
        var order = await orders.GetByIdAsync(
            id,
            cancellationToken);

        if (order is null)
            return NotFound();

        return Ok(OrderResponseV1.From(order));
    }
}
```

A second contract exposes another controller/version:

```csharp
[ApiController]
[ApiVersion("2.0")]
[Route("api/v{version:apiVersion}/orders")]
public sealed class OrdersV2Controller(
    IOrderService orders)
    : ControllerBase
{
}
```

Different API versions may map the same Application result into different HTTP
contracts.

## Breaking Changes

Changes that commonly justify a new version: removing a field clients may depend
on; changing a field's meaning or type; changing required input; changing
resource or workflow semantics incompatibly; removing an endpoint; changing
previously documented HTTP behavior incompatibly.

## Compatible Changes

Often compatible: adding an optional response field; adding an endpoint; adding
an optional query parameter with backward-compatible behavior; internal changes
that preserve the contract. Consider client-generation behavior when OpenAPI
clients are used.

## Deprecation Mechanics

Deprecation is a migration process, not merely an attribute. Mark a version
deprecated in metadata, for example `[ApiVersion("1.0", Deprecated = true)]`,
and with `ReportApiVersions = true` clients receive the supported and deprecated
versions in response headers.

## OpenAPI

Generate separate or clearly grouped OpenAPI descriptions for supported versions
when clients need them (`swagger` skill); the documented version must match
runtime routing and Controller metadata. Version changes do not override normal
HTTP semantics (`http-api` skill).

## Testing

When versions coexist, test meaningful differences: version routing,
version-specific response shape, a deprecated version still operational during
its support period, unsupported-version behavior, and shared Application
behavior staying consistent where intended. Do not duplicate identical tests
because two versions share Application behavior.

## Anti-Patterns

Avoid Minimal API version-group examples in a Controller-based project, creating
a new API version for every implementation change, and mixing URL, header, and
query versioning without a concrete reason.
