---
name: api-versioning
description: Use when introducing or evolving multiple API contract versions or discussing backward compatibility — when versioning pays off, URL/header/query strategies, Asp.Versioning for Controllers, breaking vs compatible changes, deprecation, OpenAPI grouping, version tests.
---
<!-- Kind: KNW | Scope: backend | Owns: API versioning technique and examples | Loads: on demand (model-invoked) -->
# API Versioning

Standards: `rules/backend/api.md` § API Versioning and `rules/backend/architecture.md` § Boundary Leaks (no per-version Domain models). Adoption: DEC-VER-01 and CLAUDE.md § Decisions. Package: `add-dependency` § Conditional Technology Packages. Deprecation procedure: `architecture-decision` § API Version Deprecation.

Versioning belongs to the API contract, not to Domain or Application. Compatible additions normally stay in the current version.

## When Versioning Is Useful

Explicit versioning is most useful when external clients cannot be upgraded atomically with the server, multiple client generations coexist, the API is public or consumed by independent teams, breaking changes are expected, or a migration window between contracts is required. For a small application whose frontend and backend deploy together it may add little; avoid adding `v1` automatically without a long-lived versioning need.

## Strategy

URL-segment versioning is a clear default for many HTTP APIs:

```text
/api/v1/orders
/api/v2/orders
```

It keeps the version visible in the URI, easy to route and troubleshoot, and clear in generated documentation. Header and query-string versioning are valid alternatives when requirements justify them.

## Asp.Versioning Setup

Controller integration of `Asp.Versioning`:

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

A second contract may expose another controller/version:

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

Different API versions may map the same Application result into different HTTP contracts.

## Breaking Changes

Changes that commonly justify a new version: removing a field clients may depend on; changing a field's meaning or type; changing required input; changing resource or workflow semantics incompatibly; removing an endpoint; changing previously documented HTTP behavior incompatibly.

## Compatible Changes

Often compatible: adding an optional response field; adding an endpoint; adding an optional query parameter with backward-compatible behavior; internal changes that preserve the contract. Consider client-generation behavior too when OpenAPI clients are used.

## OpenAPI

Generate separate or clearly grouped OpenAPI descriptions for supported versions when clients need them (`swagger` skill); the documented version matches runtime routing and controller metadata.

## HTTP Semantics

Version changes do not override normal HTTP semantics (`http-api` skill: status codes, conditional requests, ProblemDetails, idempotency).

## Testing

When versions coexist, test meaningful differences: version routing, version-specific response shape, a deprecated version still operational during its support period, unsupported-version behavior, shared Application behavior consistent where intended. Identical tests duplicated per version add little.

## Anti-Patterns

Avoid versioning without a compatibility requirement, Minimal API version-group examples in a Controller-based project, Domain models duplicated per API version, incompatible changes to an existing version, a new version for every implementation change, silently removing deprecated versions, and mixing URL, header and query versioning without a concrete reason.
