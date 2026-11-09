---
name: api-versioning
description: >
  Use when introducing or evolving API versions: Asp.Versioning setup,
  URL/header/query versioning, breaking vs compatible changes, deprecation,
  versioned Swagger documents, version tests.
---

> Kind: KNW | Scope: backend | Capability: — | Loading: on-demand knowledge

# API Versioning

Policy: `.claude/rules/backend/api-contracts.md`. Adopting versioning is Reserved (`architecture-decision`); its package is added through `add-dependency`; deprecation steps: `development-workflow`. Versioning belongs to the API contract, not to Domain or Application.

## When versioning is useful

External clients that cannot upgrade atomically with the server; coexisting client generations; public APIs or independent consuming teams; expected breaking changes; a required migration window. For a small application whose frontend and backend deploy together, explicit versioning may add little value — do not add `v1` automatically.

## Strategy

URL-segment versioning (`/api/v1/orders`, `/api/v2/orders`) is a clear default: visible version, easy routing and troubleshooting, clear generated documentation. Header and query-string versioning are valid when requirements justify them; do not mix strategies without a concrete reason.

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

[ApiController]
[ApiVersion("2.0")]
[Route("api/v{version:apiVersion}/orders")]
public sealed class OrdersV2Controller(IOrderService orders) : ControllerBase
{
}
```

Different versions map the same Application result into different HTTP contracts.

## Breaking vs compatible changes

Commonly breaking: removing a field clients may depend on, changing a field's meaning or type, changing required input, incompatible resource or workflow semantics, removing an endpoint, incompatible changes to documented HTTP behavior. Compilation success does not decide compatibility. Often compatible: an optional response field, a new endpoint, an optional backward-compatible query parameter, internal changes preserving the contract. Consider client-generation behavior when OpenAPI clients are used.

## Deprecation

Deprecation is a migration process, not merely an attribute: `[ApiVersion("1.0", Deprecated = true)]` with `ReportApiVersions` advertises it; document the replacement, the migration period, and the removal timing (procedure: `development-workflow`).

## OpenAPI

Generate separate or clearly grouped documents per supported version when clients need them (`swagger`); the documented version must match runtime routing and controller metadata. Version changes never override normal HTTP semantics (`http-api`).

## Testing

When versions coexist, test meaningful differences: version routing, version-specific response shapes, deprecated versions still operational during the support period, unsupported-version behavior, shared Application behavior consistent where intended. Do not duplicate identical tests per version.

## Anti-patterns

Minimal API version-group examples in a Controller-based project, a new version for every implementation change, silently removing deprecated versions.
