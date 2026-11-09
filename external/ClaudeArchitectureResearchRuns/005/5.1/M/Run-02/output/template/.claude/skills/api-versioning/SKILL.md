---
name: api-versioning
description: >
  Use when introducing or evolving API versions: whether to version,
  Asp.Versioning for controllers, URL/header/query strategies, breaking vs.
  compatible changes, deprecation, versioned Swagger documents, version tests.
---

> Owner: API versioning technique and examples (normative policy lives in rules) | Scope: backend | Loads: on demand — knowledge | Enforced: none

# API Versioning

Policy: `.claude/rules/api.md` § Versioning (when to version, no silent breaking
changes, one strategy, no per-version inner models, deprecation obligations).
Adopting versioning is a Reserved decision (`CLAUDE.md` § Decision Control);
package: `docs/technology-stack.md` § Conditional Technologies.

Versioning belongs to the API contract, not to Domain or Application; different
versions may map the same Application result into different HTTP contracts.

## When Versioning Is Useful

- external clients cannot be upgraded atomically with the server;
- several client generations must coexist;
- the API is public or consumed by independent teams;
- breaking contract changes are expected;
- a migration window between contracts is required.

For a small application whose frontend and backend deploy together, explicit
versioning may add little value; do not add `v1` automatically.

## Strategies

URL-segment versioning is clear for many HTTP APIs — the version is visible in
the URI, routing and troubleshooting are easy, and generated documentation is
clear:

```text
/api/v1/orders
/api/v2/orders
```

Header and query-string versioning are valid alternatives when requirements
justify them. Mixing URL, header, and query versioning needs a concrete reason.

## Asp.Versioning Setup

For Controller-based APIs, use the MVC integration (`Asp.Versioning.Mvc`, plus
`Asp.Versioning.Mvc.ApiExplorer` for Swagger grouping):

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

Minimal API version-group examples do not apply to this Controller-based
template.

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

A second contract exposes another controller and version while reusing the same
Application service:

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

## Breaking Changes

Changes that commonly justify a new version: removing a field clients may depend
on, changing a field's meaning or type, changing required input, changing
resource or workflow semantics incompatibly, removing an endpoint, changing
documented HTTP behavior incompatibly. Whether the code compiles says nothing
about compatibility.

## Compatible Changes

Often compatible: adding an optional response field, adding an endpoint, adding
an optional query parameter with backward-compatible behavior, internal changes
that preserve the contract. Consider client-generation behavior when OpenAPI
clients are used — a new enum member can still break generated clients.

## Deprecation

Deprecation is a migration process, not merely an attribute:

```csharp
[ApiVersion("1.0", Deprecated = true)]
```

With `ReportApiVersions = true`, responses advertise supported and deprecated
versions in `api-supported-versions` / `api-deprecated-versions` headers.
Document the replacement version and the removal timeline where consumers will
see them (Swagger description, changelog, consumer communication).

## OpenAPI

Generate separate or clearly grouped Swagger documents for supported versions
when clients need them (`swagger` skill), and keep the documented version aligned
with runtime routing and Controller metadata. Versioning does not change normal
HTTP semantics (`http-api` skill).

## Testing

When versions coexist, test their meaningful differences: version routing,
version-specific response shapes, a deprecated version still operating during its
support period, unsupported-version behavior, and shared Application behavior
staying consistent where intended. Do not duplicate identical tests just because
two versions use the same Application behavior.

## Common Mistakes

- creating a new API version for every implementation change;
- versioning without a compatibility requirement;
- changing an existing version's contract incompatibly.
