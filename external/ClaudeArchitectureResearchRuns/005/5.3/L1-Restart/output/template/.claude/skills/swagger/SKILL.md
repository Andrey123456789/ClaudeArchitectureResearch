---
name: swagger
description: Swashbuckle Swagger UI technique for ASP.NET Core Controllers. Use when configuring AddSwaggerGen/UseSwaggerUI, launch profiles that open /swagger, ProducesResponseType metadata, ProblemDetails schemas, Bearer security definitions, XML comments, multiple documents, or generated-client contracts.
---

> Level: 2-technology · Owns: Swagger/OpenAPI documentation technique · Loading: on demand

# Swagger

Rules: documentation truthfulness and environment exposure (`.claude/rules/2-technology/backend-libraries.md`); Swagger UI baseline (decisions file). Status semantics: `http-api`; error contracts: `aspnet-error-handling`. Swashbuckle uses OpenAPI internally; the developer-facing requirement is the interactive UI, not a standalone raw OpenAPI endpoint.

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

Keep Swagger configuration in the entry-point/composition code. Do not make `AddOpenApi()`/`MapOpenApi()` the default when the requirement is Swagger UI testing.

## Launch profile

```json
{ "launchBrowser": true, "launchUrl": "swagger" }
```

Keep application URLs consistent with the profile — never a launch URL pointing to HTTPS on an HTTP-only port.

## Response metadata

```csharp
[HttpGet("{id:guid}")]
[ProducesResponseType<OrderResponse>(StatusCodes.Status200OK)]
[ProducesResponseType<ProblemDetails>(StatusCodes.Status404NotFound)]
public async Task<ActionResult<OrderResponse>> GetById(Guid id, CancellationToken cancellationToken) { /* ... */ }
```

Consider the whole pipeline when listing responses — model binding, validation, authentication/authorization, rate limiting, centralized exception handling, other middleware — not only explicit action branches. Document `201` with `CreatedAtAction`/`CreatedAtRoute` when a canonical URL exists; never `201` for an endpoint returning `200` or `204` for one returning a body. Describe `ProblemDetails`/`ValidationProblemDetails` where useful, without internal exception types, stack traces, SQL, connection strings, or paths in examples.

## Authentication metadata

When the API really uses authentication, add the matching security definition and requirements (a Bearer scheme so authenticated endpoints can be exercised from the UI). Do not add a scheme merely because a package is installed, and do not apply requirements globally to anonymous endpoints.

## Descriptions, XML comments, documents

Describe what helps consumers: preconditions, idempotency, pagination/filtering, meaningful outcomes — not restated names. XML comments are optional for public contracts. Use multiple documents only for a real contract separation (API versions — see `api-versioning` — or public vs internal surfaces).

## Generated clients

When the contract feeds client generation: treat breaking schema changes seriously, keep metadata accurate, avoid anonymous response shapes, use explicit request/response contracts, review generated-client diffs.

## Verification

After API behavior changes: verify controller behavior and integration tests, check response metadata, start the API when startup/composition changed, open the Development Swagger UI, exercise representative endpoints when meaningful, and preserve newly verified behavior as tests (`verify` step 4).

## Anti-patterns

Metadata disagreeing with runtime; public Swagger UI without a reason; Swagger as a substitute for integration tests; global auth requirements on anonymous endpoints; anonymous objects as long-lived contracts; a second competing documentation stack without need.
