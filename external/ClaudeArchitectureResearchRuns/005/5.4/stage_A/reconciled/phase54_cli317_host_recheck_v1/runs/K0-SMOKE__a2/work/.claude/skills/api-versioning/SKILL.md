---
name: api-versioning
description: Use when introducing or evolving API versions or backward compatibility — need for versioning, Asp.Versioning, strategies, breaking vs. compatible changes, deprecation, versioned docs.
---

> Kind: KNW | Scope: backend | Owner: API versioning technique with examples | Loading: on demand (model-invoked knowledge)

# API Versioning

Rules: `rules/backend/api.md` § Versioning. Decision: D-15 (adopting versioning is Reserved).

See also: `add-dependency` § Package-specific choices (package), `development-workflow` § Public API contract change (deprecation procedure).

Versioning belongs to the API contract (`rules/backend/api.md` § Versioning).

## When versioning is useful

External clients cannot upgrade atomically with the server; several client generations need to coexist; the API is public or consumed by independent teams; breaking changes are expected; a migration window between contracts is required. For a small application whose frontend and backend deploy together, explicit versioning often adds little — a `v1` prefix is not automatic.

## Strategies

URL-segment versioning is visible, easy to route and troubleshoot, and documents clearly:

```text
/api/v1/orders
/api/v2/orders
```

Header and query-string versioning are valid alternatives when requirements justify them.

## Asp.Versioning setup for Controllers

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

## Controller versions

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

[ApiController]
[ApiVersion("2.0")]
[Route("api/v{version:apiVersion}/orders")]
public sealed class OrdersV2Controller(
    IOrderService orders)
    : ControllerBase
{
}
```

Different versions map the same Application result into different HTTP contracts.

## Breaking vs. compatible changes

Commonly breaking: removing a field clients may use; changing a field's meaning or type; changing required input; incompatible resource or workflow semantics; removing an endpoint; incompatibly changing documented HTTP behavior. Whether the code compiles does not decide compatibility.

Often compatible, and kept in the current version: an optional response field; a new endpoint; an optional query parameter with backward-compatible behavior; internal changes that preserve the contract. Consider client-generation behavior when OpenAPI clients are used.

## OpenAPI

Generate separate or clearly grouped documents per supported version when clients need them (technique: `swagger`); the documented version matches runtime routing and Controller metadata. Versioning does not change normal HTTP semantics (`http-api`).

## Testing

When versions coexist, test meaningful differences: version routing, version-specific response shapes, a deprecated version still operating during its support period, unsupported-version behavior, shared Application behavior staying consistent. Identical behavior needs no duplicated tests per version.

## Common mistakes

Versioning without a compatibility requirement; Minimal API version-group examples in a Controller project; Domain models duplicated per version; an existing version changed incompatibly; a new version for every implementation change; deprecated versions removed silently; URL, header and query versioning mixed without reason.
