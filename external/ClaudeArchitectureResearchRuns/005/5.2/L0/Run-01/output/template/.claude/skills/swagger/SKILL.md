---
name: swagger
description: >
  Use for Swagger UI with Swashbuckle: setup, launch profile, ProducesResponseType metadata, ProblemDetails docs, Bearer schemes, generated clients.
---

> Level: 2 Technology | Owns: Swashbuckle/Swagger technique | Scope: backend | Loads: knowledge skill (on demand) | Depends on: 1-architecture/entry-points.md, 2-technology/aspnet-core.md

# Swagger Technique

Policy owners (routing): documentation must match runtime →
`1-architecture/entry-points.md`; environment exposure →
`2-technology/aspnet-core.md`; Swashbuckle selection →
`3-project/decisions.md`; status semantics → `http-api`; error contracts →
`aspnet-error-handling`.

Swashbuckle produces an OpenAPI document internally; the developer-facing
template surface is the interactive Swagger UI, not a raw OpenAPI endpoint, so
do not make `AddOpenApi()`/`MapOpenApi()` the default.

## Setup

```csharp
builder.Services.AddControllers();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.MapControllers();
```

Keep Swagger configuration in the Api/composition layer.

## Development Launch Profile

```json
{ "launchBrowser": true, "launchUrl": "swagger" }
```

Profile URLs must match the actual HTTP/HTTPS ports; never point the launch URL
at HTTPS on an HTTP-only port.

## Response Metadata

```csharp
[HttpGet("{id:guid}")]
[ProducesResponseType<OrderResponse>(StatusCodes.Status200OK)]
[ProducesResponseType<ProblemDetails>(StatusCodes.Status404NotFound)]
public async Task<ActionResult<OrderResponse>> GetById(Guid id, CancellationToken cancellationToken)
```

Derive the documented statuses from the whole pipeline — model binding,
validation, authentication/authorization, rate limiting, centralized exception
handling, middleware — not only the action's explicit branches. Document `201`
only when the endpoint returns `201` (prefer `CreatedAtAction`/`CreatedAtRoute`
when a canonical URL exists) and `204` only when it has no body. Describe
`ProblemDetails`/`ValidationProblemDetails` where useful, without exposing
exception types, stack traces, SQL, connection strings, or paths in examples.

## Authentication Metadata

When the API really uses Bearer authentication, add a matching security
definition and requirements so authenticated endpoints can be exercised from
Swagger UI; do not add a scheme merely because an auth package is installed,
and do not apply authentication requirements globally to anonymous endpoints.

## Descriptions and XML Comments

Document what helps consumers — preconditions, idempotency, pagination and
filtering, meaningful outcomes — not restated names. Use XML comments for public
contracts when the project chooses them, not on every internal type.

## Multiple Documents and Clients

Split documents only for real contract separation (versions, public vs.
internal); versioning strategy lives in `api-versioning`. When clients are
generated from the contract, treat breaking schema changes seriously, keep
metadata accurate, use explicit request/response contracts instead of
anonymous shapes, and review generated-client diffs.

## Verification

When API behavior changes: verify Controller behavior and integration tests,
check response metadata, start the API when composition changed, open the
Development Swagger UI, exercise representative endpoints when it is a
meaningful check, and preserve newly verified behavior as tests (`verify`).
Swagger is not a substitute for integration tests.
