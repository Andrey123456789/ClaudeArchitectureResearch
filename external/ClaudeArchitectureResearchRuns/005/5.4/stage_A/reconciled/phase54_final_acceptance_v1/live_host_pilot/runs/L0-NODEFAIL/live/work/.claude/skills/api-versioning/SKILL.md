---
name: api-versioning
description: >
  Use when considering or evolving API versions: Asp.Versioning setup, URL/header
  strategies, breaking vs compatible changes, deprecation, versioned Swagger
  documents.
---

> Level: 2 Technology · Owns: API versioning technique and examples (knowledge) · Scope: backend · Loads: on invocation · Depends on: .claude/rules/1-architecture/entry-points.md

# API Versioning

Policy owners: when versioning is justified, breaking-change treatment, one consistent strategy (URL segment by default), no per-version inner models → `.claude/rules/1-architecture/entry-points.md` → Versioning; adopting versioning is Reserved (CLAUDE.md → Decision control); the package binding → `add-dependency`; deprecation procedure → `architecture-decision`. Versioning belongs to the API contract, not to Domain or Application. This skill is technique only.

## When versioning is useful

External clients that cannot upgrade atomically with the server; several client generations coexisting; a public API or independent consumer teams; expected breaking changes; a required migration window. For a small application whose frontend and backend deploy together, explicit versioning may add little value — do not add `v1` automatically.

## Strategies

```text
/api/v1/orders        URL segment — visible, easy to route and troubleshoot, clear docs
api-version header    header strategy
?api-version=1.0      query-string strategy
```

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
        if (order is null)
            return NotFound();

        return Ok(OrderResponseV1.From(order));
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

## Breaking vs compatible

Commonly breaking: removing a field clients may use; changing a field's meaning or type; changing required input; incompatible resource or workflow semantics; removing an endpoint; incompatible changes to documented HTTP behavior. Compilation success says nothing about compatibility. Often compatible: an optional response field, a new endpoint, an optional backward-compatible query parameter, internal changes that keep the contract. Consider client-generation behavior when OpenAPI clients are used.

## Deprecation metadata

```csharp
[ApiVersion("1.0", Deprecated = true)]
```

`ReportApiVersions = true` advertises supported and deprecated versions in response headers. The full deprecation sequence is in `architecture-decision`.

## Documentation

Generate separate or clearly grouped Swagger documents per supported version when clients need them (`swagger` skill); the documented version must match routing and controller metadata. Versions never override normal HTTP semantics (`http-api` skill).

## Testing

Test meaningful differences: version routing, version-specific response shape, a deprecated version still working during its support period, unsupported-version behavior, shared behavior consistent where intended. Do not duplicate identical tests per version.

## Anti-patterns

Minimal API version groups in a Controller project; a new version for every implementation change.
