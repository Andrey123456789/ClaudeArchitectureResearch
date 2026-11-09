---
name: api-versioning
description: >
  Use when evaluating whether an API needs versioning, configuring
  Asp.Versioning for Controllers, adding a v2 controller, judging breaking vs.
  compatible contract changes, deprecating a version, or grouping versions in
  Swagger.
---

> Owns: API versioning technique (Asp.Versioning setup, version controllers, compatibility analysis, deprecation mechanics) | Scope: backend | Loads: on demand (knowledge skill)

# API Versioning

Policy owners: when versioning is warranted, breaking changes, strategy,
inner-model reuse, deprecation obligations → `.claude/rules/api.md` (API
Versioning); adopting versioning is Reserved (`CLAUDE.md`); the package is a
conditional technology (`docs/technology-stack.md`). Versioning belongs to the
API contract, not to Domain or Application.

## When Versioning Helps

Signals: external clients cannot upgrade atomically with the server; several
client generations coexist; the API is public or consumed by independent teams;
breaking changes are expected; a migration window is required. A small
application whose frontend and backend deploy together usually gains little
(when versioning is warranted: `api.md`).

## Strategies

URL segment (`/api/v1/orders`) is visible, easy to route and troubleshoot, and
documents clearly. Header or query-string versioning are alternatives when
requirements justify them. Do not mix strategies without a concrete reason.

## Asp.Versioning Setup (Controllers)

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

Install the package through `add-dependency` (timing:
`docs/technology-stack.md`). Do not use
Minimal API version-group examples in a Controller-based project.

## Version Controllers

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

Both versions map the same Application result into different HTTP contracts.

## Breaking vs. Compatible

Usually breaking: removing a field clients may depend on; changing a field's
meaning or type; changing required input; incompatible resource/workflow
semantics; removing an endpoint; incompatible change to documented HTTP
behavior. Usually compatible: adding an optional response field, a new endpoint,
an optional query parameter with backward-compatible behavior, internal changes
preserving the contract. Compilation success says nothing about compatibility;
consider generated-client behavior too.

## Deprecation Mechanics

```csharp
[ApiVersion("1.0", Deprecated = true)]
```

With `ReportApiVersions = true`, responses advertise supported and deprecated
versions (`api-supported-versions`, `api-deprecated-versions` headers). Pair the
metadata with documented replacement, migration guidance, and a communicated
removal timeline.

## OpenAPI

Generate one Swagger document per supported version when clients need them
(`swagger`), matching runtime routing and Controller metadata.

## Testing

Test meaningful differences: version routing, version-specific response shapes,
deprecated versions still operational during support, unsupported-version
behavior, shared Application behavior consistent where intended. Do not
duplicate identical tests per version.
