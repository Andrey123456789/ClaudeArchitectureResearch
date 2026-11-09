---
name: api-versioning
description: >
  Use when considering or evolving API versions: whether versioning is needed,
  Asp.Versioning setup, versioned controllers, breaking vs. compatible
  changes, deprecation.
---

> Knowledge skill. Owns: API versioning technique and examples · Scope: backend · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/api.md, .claude/rules/architecture.md

# API Versioning

Rules: `api.md` (when to version, published-contract compatibility, one
strategy) and `architecture.md` (no per-version Domain or persistence models).
Adopting versioning is Reserved (CLAUDE.md, Decision Control); package choice:
`add-dependency`; deprecation procedure: `development-workflow`. Versioning
belongs to the API contract, not to Domain or Application.

## When Versioning Is Useful

- external clients cannot be upgraded atomically with the server;
- several client generations must coexist;
- the API is public or consumed by independent teams;
- breaking contract changes are expected;
- a migration window between contracts is required.

For a small application whose frontend and backend deploy together, explicit
versioning may add little value (`api.md`, API Versioning).

## URL-Segment Strategy

```text
/api/v1/orders
/api/v2/orders
```

Benefits: the version is visible in the URI, routing and troubleshooting are
easy, generated documentation is clear. Header and query-string versioning are
valid alternatives when requirements justify them.

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
depend on; changing a field's meaning or type; changing required input;
changing resource or workflow semantics incompatibly; removing an endpoint;
changing documented HTTP behavior incompatibly. Whether the code compiles does
not decide compatibility.

## Compatible Changes

Often compatible: adding an optional response field; adding an endpoint; adding
an optional query parameter with backward-compatible behavior; internal changes
that preserve the contract. Consider client-generation behavior when OpenAPI
clients are used.

## OpenAPI

Generate separate or clearly grouped descriptions for supported versions when
clients need them (`swagger` skill), aligned with runtime routing and Controller
metadata (`api.md`, Swagger).

## HTTP Semantics

Versions do not override HTTP semantics (`http-api` skill).

## Testing

When versions coexist, test meaningful differences: version routing,
version-specific response shapes, a deprecated version still operating during
its support period, unsupported-version behavior, and shared Application
behavior staying consistent. Do not duplicate identical tests merely because two
versions share Application behavior.

## Anti-Patterns

- Minimal API version groups in a Controller-based project;
- a new version for every implementation change;
- mixing URL, header, and query versioning without a concrete reason.
