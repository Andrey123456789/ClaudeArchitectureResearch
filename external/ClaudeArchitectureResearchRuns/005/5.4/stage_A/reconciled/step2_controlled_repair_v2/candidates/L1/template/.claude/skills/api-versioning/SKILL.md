---
name: api-versioning
description: API versioning technique for ASP.NET Core Controllers with Asp.Versioning. Use when introducing or evolving multiple API contract versions — URL/header/query strategies, breaking vs compatible changes, deprecation, versioned Swagger documents, version routing tests.
---

> Level: 2-technology · Owns: API versioning technique · Loading: on demand

# API Versioning

Rules: when to version, compatibility, and strategy (`.claude/rules/0-core/http-api.md` § Versioning); no duplicated inner models per version (`.claude/rules/1-architecture/roles.md`); adopting versioning is Reserved; package only after adoption (`add-dependency`); deprecation procedure (`development-workflow`). Versioning belongs to the API contract, not the use-case layer or domain model.

## When it pays off

External clients cannot upgrade atomically with the server; several client generations coexist; the API is public or consumed by independent teams; breaking changes are expected; a migration window is required. For a small application whose frontend and backend deploy together, explicit versioning may add little — do not add `v1` automatically.

## Strategy

URL segments (`/api/v1/orders`, `/api/v2/orders`) make the version visible, easy to route and troubleshoot, and clear in generated docs. Header or query-string versioning are valid when requirements justify them.

## Setup (Controller integration)

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
```

A `[ApiVersion("2.0")]` controller maps the same use-case result into a different HTTP contract.

## Breaking vs compatible

Usually breaking: removing a field clients may use, changing a field's meaning or type, changing required input, incompatible resource or workflow semantics, removing an endpoint, incompatible changes to documented HTTP behavior. Usually compatible: optional response fields, new endpoints, optional backward-compatible query parameters, internal changes preserving the contract. Compilation success does not decide compatibility; consider client-generation effects too.

## Documentation and testing

Generate separate or clearly grouped Swagger documents per supported version (`swagger`), matching runtime routing and metadata. Version changes never override normal HTTP semantics (`http-api`). Test meaningful differences: version routing, version-specific shapes, deprecated versions still operating during support, unsupported-version behavior, shared behavior consistent where intended — without duplicating identical tests per version.

## Anti-patterns

Versioning without a compatibility requirement; Minimal API version-group examples in a Controller project; domain models duplicated per version; incompatible edits to an existing version; a new version for every implementation change; silently removing deprecated versions; mixing URL, header, and query versioning without a concrete reason.
