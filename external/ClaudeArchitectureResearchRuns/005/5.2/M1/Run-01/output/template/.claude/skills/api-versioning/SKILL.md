---
name: api-versioning
description: >
  API versioning for Controllers: Asp.Versioning setup, URL/header/query
  strategy, [ApiVersion], breaking vs. compatible changes, deprecation,
  versioned Swagger documents.
---

> **Knowledge skill** · Owns: API versioning technique and examples · Scope: backend · Loading: on demand

# API Versioning

## Rules

Rules: `api.md` → API Versioning (when to version, compatibility, one strategy,
no duplicated inner models). Adopting versioning is Reserved (`CLAUDE.md` →
Decision Control); the package is added through `add-dependency`; deprecation is
a `development-workflow` obligation.

Explicit versioning is justified when contract stability and backward
compatibility outweigh its complexity; compatible additions normally remain in the
current version, and versioning belongs to the API contract, not Domain or
Application.

## When Versioning Is Useful

Explicit API versioning is most useful when:

- external clients cannot be upgraded atomically with the server;
- multiple client generations must coexist;
- the API is public or consumed by independent teams;
- breaking contract changes are expected;
- a migration window between contracts is required.

For a small application where frontend and backend are deployed together,
explicit API versioning may provide little value.

Do not add `v1` automatically without considering whether the project actually
needs a long-lived versioning contract.

## Strategy

URL-segment versioning (the default strategy, `api.md` → API Versioning) looks
like:

```text
/api/v1/orders
/api/v2/orders
```

Benefits include:

- visible version in the URI;
- easy routing and troubleshooting;
- clear generated documentation.

Header and query-string versioning are valid alternatives when project
requirements justify them.

## Asp.Versioning Setup

For Controller-based APIs, use the Controller integration of `Asp.Versioning`.

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

Different API versions may map the same Application result into different HTTP
contracts.

## Breaking Changes

Changes that commonly justify a new API version include:

- removing a field clients may depend on;
- changing a field's meaning or type;
- changing required input;
- changing resource or workflow semantics incompatibly;
- removing an endpoint;
- changing previously documented HTTP behavior incompatibly.

Do not determine breaking compatibility solely from whether the code compiles.

## Compatible Changes

Changes that are often compatible include:

- adding an optional response field;
- adding a new endpoint;
- adding an optional query parameter with backward-compatible behavior;
- internal implementation changes that preserve the API contract.

Client-generation behavior should also be considered when OpenAPI clients are
used.

## Deprecation

Deprecation is a migration process, not merely an attribute; the obligation is in
`development-workflow` → Change-Specific Obligations. Mark the version in
metadata:

```csharp
[ApiVersion("1.0", Deprecated = true)]
```

With `ReportApiVersions = true`, responses advertise supported and deprecated
versions in the `api-supported-versions` / `api-deprecated-versions` headers.

## OpenAPI

Generate separate or clearly grouped OpenAPI descriptions for supported versions
when clients need them.

Follow the `swagger` skill for Swagger/OpenAPI documentation details.

The documented version must match runtime routing and Controller metadata.

## HTTP Semantics

Version changes do not override normal HTTP semantics.

Follow the `http-api` skill for status codes, conditional requests,
ProblemDetails, idempotency, and other HTTP behavior.

## Testing

When multiple versions coexist, test meaningful differences between them.

Useful cases include:

- version routing;
- version-specific response shape;
- deprecated version remains operational during support period;
- unsupported version behavior;
- shared Application behavior remains consistent where intended.

Do not duplicate identical tests merely because two versions use the same
Application behavior.

## Anti-Patterns

Avoid:

- Minimal API version-group examples in a Controller-based project;
- creating a new API version for every implementation change;
- mixing URL, header, and query versioning without a concrete reason.
