---
name: api-versioning
description: >
  Use when introducing or evolving API versions, judging breaking vs compatible
  changes, or deprecating a version: Asp.Versioning setup, strategies, versioned
  controllers, Swagger groups.
---

> Level: 2 Technology · Owns: API versioning technique · Scope: backend · Loads: on demand (knowledge skill)

# API Versioning

Policy owners: `.claude/rules/1-architecture/entry-points.md` (API evolution: when to version, breaking changes, one strategy, no per-version inner models, deprecation obligations). Adopting versioning is Reserved (decision control); the package is a conditional technology in the project decisions. Version-specific types live at the Api boundary (`entry-points.md`).

## When versioning helps

External clients cannot upgrade atomically with the server; several client generations must coexist; the API is public or consumed by independent teams; breaking changes are expected; a migration window is required. A small application whose frontend and backend deploy together usually gains little — do not add `v1` automatically.

## Strategies

URL segment (`/api/v1/orders`, `/api/v2/orders`) is visible, easy to route and troubleshoot, and documents clearly. Header (`api-version: 2.0`) and query (`?api-version=2.0`) are the alternatives when requirements justify them (one strategy: `entry-points.md`).

## Asp.Versioning setup (controllers)

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

Package: `Asp.Versioning.Mvc` (+ `Asp.Versioning.Mvc.ApiExplorer` for documentation), added through `add-dependency` only after versioning is adopted.

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
public sealed class OrdersV2Controller(IOrderService orders) : ControllerBase
{
}
```

Different versions map the same Application result into different HTTP contracts.

## Breaking versus compatible

Commonly breaking: removing a field clients may use; changing a field's meaning or type; changing required input; incompatible resource or workflow semantics; removing an endpoint; changing documented HTTP behavior. Commonly compatible: an optional response field, a new endpoint, an optional backward-compatible query parameter, internal changes that keep the contract. Compilation success says nothing about compatibility; consider generated-client behavior too.

## Deprecation mechanics

```csharp
[ApiVersion("1.0", Deprecated = true)]
```

With `ReportApiVersions = true`, responses carry `api-supported-versions` and `api-deprecated-versions` headers. Add a sunset policy where supported (`options.Policies.Sunset(1.0).Effective(date).Link("https://.../migration")`), document the replacement version in Swagger descriptions and release notes, and keep integration tests for the deprecated version until its support period ends.

## Documentation

Generate one Swagger document per supported version (`SwaggerDoc("v1", ...)`, `SwaggerDoc("v2", ...)` driven by `IApiVersionDescriptionProvider`) when clients need them; the documented version must match routing and controller metadata (`swagger` skill). Normal HTTP semantics still apply (`http-api`).

## Testing

Test version routing, version-specific response shapes, that a deprecated version still works during its support period, unsupported-version behavior, and that shared Application behavior stays consistent. Do not duplicate identical tests for versions that share the same behavior.

## Review cues

Versioning without a compatibility requirement, Minimal API version-set examples in a controller project, Domain models duplicated per version, incompatible changes inside an existing version, a new version for every implementation change, silent removal of deprecated versions.
