---
name: api-versioning
description: >
  Use when an API needs versions or compatibility planning: Asp.Versioning for
  Controllers, URL segments, breaking vs compatible changes, deprecation.
---
> Level: 2-technology | Owns: API versioning technique | Scope: backend | Loads: on demand (skill)

# API Versioning

Policy: `http-api.md` (versioning only for a real compatibility need, no silent
breaking changes, one strategy with URL segments by default),
`role-boundaries.md` (no per-version domain or persistence models). Adopting
versioning is Reserved; adding the package follows `add-dependency`;
deprecation follows `architecture-decision`.

## When versioning is useful

External clients cannot upgrade atomically with the server; several client
generations must coexist; the API is public or consumed by independent teams;
breaking changes are expected; a migration window is required. A small
application deploying frontend and backend together may gain little — do not
add `v1` automatically.

## Strategies

URL segment (`/api/v1/orders`, `/api/v2/orders`) is visible, easy to route and
troubleshoot, and documents clearly. Header and query-string versioning are
valid when requirements justify them; never mix strategies without a concrete
reason.

## Setup (Controllers)

```csharp
builder.Services
    .AddApiVersioning(options =>
    {
        options.ReportApiVersions = true;
        options.ApiVersionReader = new UrlSegmentApiVersionReader();
    })
    .AddMvc()
    .AddApiExplorer(options =>
    {
        options.GroupNameFormat = "'v'VVV";
        options.SubstituteApiVersionInUrl = true;
    });
```

## Versioned controllers

```csharp
[ApiController]
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/orders")]
public sealed class OrdersV1Controller(IOrderService orders) : ControllerBase
{
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<OrderResponseV1>> GetById(Guid id, CancellationToken cancellationToken)
    {
        var order = await orders.GetByIdAsync(id, cancellationToken);
        return order is null ? NotFound() : Ok(OrderResponseV1.From(order));
    }
}

[ApiController]
[ApiVersion("2.0")]
[Route("api/v{version:apiVersion}/orders")]
public sealed class OrdersV2Controller(IOrderService orders) : ControllerBase { }
```

Different versions map the same use-case result into different transport
contracts.

## Breaking vs compatible changes

Commonly breaking: removing a field clients may use; changing a field's meaning
or type; changing required input; incompatible resource or workflow semantics;
removing an endpoint; incompatible change to documented HTTP behavior. Commonly
compatible: an optional response field, a new endpoint, an optional query
parameter with backward-compatible behavior, internal changes preserving the
contract. Consider client-generation effects too.

## Deprecation mechanics

`[ApiVersion("1.0", Deprecated = true)]` marks the version deprecated and, with
`ReportApiVersions`, advertises it in response headers. Pair it with
documentation of the replacement and the support timeline
(`architecture-decision`).

## OpenAPI

Generate separate or clearly grouped documents per supported version when
clients need them (`swagger`); documented versions must match runtime routing
and controller metadata.

## Testing

Test meaningful differences: version routing, version-specific response
shapes, deprecated versions still operational during support, unsupported
version behavior, shared behavior staying consistent. Do not duplicate
identical tests per version.

## Anti-patterns

Versioning without a compatibility requirement; Minimal API version-group
examples in a Controller project; per-version domain models; incompatible
changes to an existing version; a new version for every implementation change;
silently removing deprecated versions; mixed strategies.
