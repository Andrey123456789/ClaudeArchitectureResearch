---
name: swagger
description: >
  Use for Swagger UI and OpenAPI metadata: Swashbuckle setup, launch settings,
  ProducesResponseType, ProblemDetails docs, Bearer security, generated clients.
---
> Level: 2-technology | Owns: Swashbuckle / Swagger UI technique | Scope: backend | Loads: on demand (skill)

# Swagger

Policy: `backend-technologies.md` (metadata matches runtime; Development
exposure), project stack (Swashbuckle is the baseline). Status semantics:
`http-api`; error contracts: `aspnet-error-handling`. Swagger tooling uses the
OpenAPI specification internally; the developer-facing surface is Swagger UI,
not a standalone raw OpenAPI endpoint — do not make built-in
`AddOpenApi()`/`MapOpenApi()` the default when interactive Swagger testing is
the requirement.

## Basic setup

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

Keep Swagger configuration in the host's composition code.

## Development launch

```json
{
  "launchBrowser": true,
  "launchUrl": "swagger"
}
```

The profile's HTTP/HTTPS application URLs must agree with the launch URL — never
point the browser at HTTPS on an HTTP-only port.

## Response metadata

```csharp
[HttpGet("{id:guid}")]
[ProducesResponseType<OrderResponse>(StatusCodes.Status200OK)]
[ProducesResponseType<ProblemDetails>(StatusCodes.Status404NotFound)]
public async Task<ActionResult<OrderResponse>> GetById(Guid id, CancellationToken cancellationToken)
{
    // ...
}
```

Document `201` only when the endpoint returns `201` (prefer `CreatedAtAction` /
`CreatedAtRoute` with a canonical URL), never `204` for an endpoint with a body,
and only statuses that are part of the real runtime contract. Account for
responses produced outside the action — model binding, validation,
authentication/authorization, rate limiting, centralized exception handling —
without adding speculative entries. Describe `ProblemDetails` /
`ValidationProblemDetails` where useful; never show internal exception types,
stack traces, SQL, connection strings, or file paths in examples.

## Authentication metadata

When the API actually uses authentication, configure the matching security
definition and requirements (for Bearer, an HTTP bearer scheme so protected
endpoints can be exercised from Swagger UI). Do not add a scheme because a
package is installed, and do not apply authentication requirements globally to
anonymous endpoints.

## Descriptions and XML comments

Document what helps consumers: preconditions, idempotency, pagination/filtering
behavior, meaningful outcomes — not restated action or property names. XML
comments are optional for public contracts; do not add them to every internal
type for Swagger's sake.

## Multiple documents

Only for a real contract separation (API versions, public vs internal
surfaces); versioning strategy: `api-versioning`.

## Generated clients

When the contract feeds client generation: treat breaking schema changes
seriously, keep metadata accurate, avoid anonymous response shapes, use explicit
request/response contracts, and review generated-client diffs.

## Verification after API changes

1. Verify controller behavior and relevant integration tests.
2. Verify response metadata.
3. Start the API when startup/composition changed and confirm the Development
   Swagger UI loads.
4. Exercise representative endpoints through Swagger UI when that is a
   meaningful check, then preserve newly verified behavior in maintained tests
   (`verify`).

## Anti-patterns

Metadata that disagrees with runtime responses; public Swagger UI without a
reason; Swagger as a substitute for integration tests; global auth requirements
on anonymous endpoints; anonymous objects as long-lived contracts; a second
competing documentation stack without a concrete need.
