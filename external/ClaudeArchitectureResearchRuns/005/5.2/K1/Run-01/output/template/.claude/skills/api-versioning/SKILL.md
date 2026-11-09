---
name: api-versioning
description: Use when introducing or evolving several API contract versions for ASP.NET Core controllers — deciding whether versioning is needed, Asp.Versioning setup, URL/header/query strategies, breaking versus compatible changes, deprecation, OpenAPI per version and version tests.
---
Kind: KNW | Scope: backend | Capability: — | Loading: on invocation

# API Versioning

Rules: `.claude/rules/backend/http-api.md` → Versioning (when to version, no silent breaking changes, one strategy) and `.claude/rules/backend/architecture.md` → API boundary contracts. Adopting versioning is Reserved (`CLAUDE.md` → Decision control); deprecation procedure: `architecture-decision`; package: `add-dependency`. Versioning belongs to the API contract, not to Domain or Application.

## When versioning is useful

Explicit versioning pays off when external clients cannot be upgraded atomically with the server, several client generations must coexist, the API is public or consumed by independent teams, breaking changes are expected, or a migration window between contracts is required. For a small application whose frontend and backend deploy together it may add little value; do not add `v1` automatically without a long-lived versioning need.

## Strategies

URL-segment versioning (`/api/v1/orders`, `/api/v2/orders`) makes the version visible, routing and troubleshooting easy, and generated documentation clear. Header and query-string versioning are valid alternatives when requirements justify them.

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

## Controller versions

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

Different versions may map the same Application result into different HTTP contracts.

## Breaking and compatible changes

Commonly breaking: removing a field clients may depend on, changing a field's meaning or type, changing required input, changing resource or workflow semantics incompatibly, removing an endpoint, changing documented HTTP behavior incompatibly. Compatibility is not determined by whether the code compiles.

Often compatible: adding an optional response field, adding an endpoint, adding an optional query parameter with backward-compatible behavior, internal changes that preserve the contract. Consider client-generation behavior when OpenAPI clients are used.

## Deprecation metadata

```csharp
[ApiVersion("1.0", Deprecated = true)]
```

With `ReportApiVersions = true`, responses advertise supported and deprecated versions. The deprecation process (replacement, timeline, support period) is in `architecture-decision`.

## OpenAPI

Generate separate or clearly grouped documents for the supported versions when clients need them (`swagger` skill). The documented version must match runtime routing and controller metadata. Versioning does not change normal HTTP semantics (`http-api` skill).

## Testing

When versions coexist, test the meaningful differences: version routing, version-specific response shapes, a deprecated version still operating during its support period, unsupported-version behavior, and shared Application behavior staying consistent where intended. Do not duplicate identical tests because two versions share Application behavior.

## Anti-patterns

Review checks; the named standard owns each rule:

- Versioning without a compatibility requirement, or a new version for every implementation change? (`http-api.md`)
- Minimal API version-group examples in a controller-based project?
- Domain models duplicated per API version? (`architecture.md`)
- An existing version's contract changed incompatibly, or a deprecated version silently removed? (`http-api.md`, `architecture-decision`)
- URL, header and query versioning mixed without a concrete reason? (`http-api.md`)
