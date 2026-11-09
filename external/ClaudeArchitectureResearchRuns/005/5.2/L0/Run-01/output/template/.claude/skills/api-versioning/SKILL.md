---
name: api-versioning
description: >
  Use when introducing or evolving API versions: Asp.Versioning setup, versioned controllers, breaking changes, deprecation, OpenAPI groups.
---

> Level: 2 Technology | Owns: Asp.Versioning technique | Scope: backend | Loads: knowledge skill (on demand) | Depends on: 1-architecture/entry-points.md

# API Versioning Technique

Policy owners (routing): when versioning is warranted, breaking-change
treatment, one consistent strategy, no duplicated inner models →
`1-architecture/entry-points.md`; adopting versioning is Reserved (CLAUDE.md);
package choice → `add-dependency`; deprecation procedure → `develop`.

## When Versioning Helps

External clients that cannot upgrade with the server, coexisting client
generations, public or cross-team APIs, expected breaking changes, required
migration windows. A small application whose frontend and backend deploy
together usually gains little; do not add `v1` automatically.

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

## Versioned Controllers

```csharp
[ApiController]
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/orders")]
public sealed class OrdersV1Controller(IOrderService orders) : ControllerBase
{
    [HttpGet("{id:guid}")]
    public async Task<ActionResult<OrderResponseV1>> GetById(Guid id, CancellationToken ct)
    {
        var order = await orders.GetByIdAsync(id, ct);
        return order is null ? NotFound() : Ok(OrderResponseV1.From(order));
    }
}

[ApiController]
[ApiVersion("2.0")]
[Route("api/v{version:apiVersion}/orders")]
public sealed class OrdersV2Controller(IOrderService orders) : ControllerBase { }
```

Different versions map the same Application result into different HTTP
contracts. URL segments (`/api/v1/orders`) are visible, easy to route and
troubleshoot, and document clearly; header or query versioning is valid when
requirements justify it.

## Breaking vs. Compatible Changes

Usually breaking: removing a field clients may use, changing a field's meaning
or type, changing required input, incompatible resource or workflow semantics,
removing an endpoint, incompatible changes to documented HTTP behavior.
Usually compatible: optional response fields, new endpoints, optional query
parameters with backward-compatible behavior, internal changes. Compiling code
does not prove compatibility; consider generated clients too.

## Deprecation Metadata

```csharp
[ApiVersion("1.0", Deprecated = true)]
```

With `ReportApiVersions = true`, responses advertise supported and deprecated
versions in headers.

## OpenAPI

Generate separate or clearly grouped documents per supported version when
clients need them (`swagger` skill); the documented version must match routing
and Controller metadata. Versioning does not change HTTP semantics (`http-api`).

## Testing

Test version routing, version-specific shapes, a deprecated version still
working during its support period, unsupported-version behavior, and shared
behavior staying consistent — without duplicating identical tests per version.

## Avoid

Minimal API version-group examples in a Controller project, new versions for
every implementation change, and mixing URL, header, and query versioning
without a concrete reason.
