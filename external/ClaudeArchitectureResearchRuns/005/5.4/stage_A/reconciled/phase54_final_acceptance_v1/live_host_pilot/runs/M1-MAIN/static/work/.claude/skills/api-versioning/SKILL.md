---
name: api-versioning
description: >
  Use when adding or evolving API versions: Asp.Versioning, URL/header/query
  strategy, [ApiVersion] controllers, breaking vs. compatible changes,
  deprecation, versioned OpenAPI documents.
---

> Knowledge skill · API versioning technique · Policy: `.claude/rules/api.md` § API Versioning, `.claude/rules/architecture.md` § Layer Placement · Deprecation procedure: `architecture-decision` § Public API Version Deprecation · Package: `add-dependency`

# API Versioning

Versioning belongs to the API contract, not to Domain or Application. Compatible
additions stay in the current version.

## When Versioning Is Useful

Explicit versioning is most useful when external clients cannot be upgraded
atomically with the server, several client generations must coexist, the API
is public or consumed by independent teams, breaking changes are expected, or a
migration window between contracts is required. For a small application whose
frontend and backend deploy together it may add little value; do not add `v1`
automatically.

## Strategy

URL-segment versioning is visible in the URI, easy to route and troubleshoot,
and produces clear documentation:

```text
/api/v1/orders
/api/v2/orders
```

Header and query-string versioning are valid alternatives when project
requirements justify them.

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

Different versions may map the same Application result into different HTTP
contracts.

## Breaking Changes

Changes that commonly justify a new version: removing a field clients may
depend on, changing a field's meaning or type, changing required input,
changing resource or workflow semantics incompatibly, removing an endpoint,
changing documented HTTP behavior incompatibly. Do not judge compatibility only
by whether the code compiles.

## Compatible Changes

Often compatible: adding an optional response field, a new endpoint, an
optional query parameter with backward-compatible behavior, or internal changes
that preserve the contract. Consider client-generation behavior when OpenAPI
clients are used.

## OpenAPI

Generate separate or clearly grouped documents for supported versions when
clients need them (`swagger` skill); the documented version must match runtime
routing and Controller metadata.

## HTTP Semantics

Version changes do not override normal HTTP semantics (`http-api` skill).

## Testing

When versions coexist, test meaningful differences: version routing,
version-specific response shape, a deprecated version still operational during
its support period, unsupported-version behavior, and shared Application
behavior staying consistent where intended. Do not duplicate identical tests
merely because two versions share Application behavior.

## Review Checks

Check-by-reference against `api.md` § API Versioning: versioning without a
compatibility requirement; Minimal API version-group examples in a
Controller-based project; Domain models duplicated per version; an existing
version's contract changed incompatibly; a new version for every implementation
change; deprecated versions removed silently; URL, header, and query versioning
mixed without a concrete reason.
