---
name: swagger
description: Use when configuring or reviewing Swagger UI/OpenAPI for Controllers — Swashbuckle setup, launch profile, ProducesResponseType, ProblemDetails, Bearer schemes, generated-client contracts.
---

> Kind: KNW | Scope: backend | Owner: Swagger/OpenAPI technique with examples | Loading: on demand (model-invoked knowledge)

# Swagger

Rules: `rules/backend/api.md` § OpenAPI and Swagger. Decision: D-07. Status semantics: `http-api`; error contracts: `aspnet-error-handling`.

Swashbuckle describes the API with the OpenAPI specification internally; the developer-facing surface here is the interactive Swagger UI, not a standalone raw OpenAPI endpoint.

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

Keep Swagger configuration in the API/composition layer. The built-in `AddOpenApi()`/`MapOpenApi()` is not a replacement when the requirement is interactive Swagger UI testing.

## Development launch

```json
{
  "launchBrowser": true,
  "launchUrl": "swagger"
}
```

Keep the application URLs and the launch profile in agreement — a browser launch URL pointing to HTTPS on an HTTP-only port fails.

## Response metadata

```csharp
[HttpGet("{id:guid}")]
[ProducesResponseType<OrderResponse>(StatusCodes.Status200OK)]
[ProducesResponseType<ProblemDetails>(StatusCodes.Status404NotFound)]
public async Task<ActionResult<OrderResponse>> GetById(
    Guid id,
    CancellationToken cancellationToken)
{
    // ...
}
```

Accuracy rule: `rules/backend/api.md` § OpenAPI and Swagger — for example, not `201` for an endpoint that returns `200`, not `204` for one that returns a body. Possible responses come from the whole pipeline: model binding, validation, authentication/authorization, rate limiting, centralized exception handling and other middleware, not only explicit action branches; a status that is merely theoretically possible is not documented. For creation, document `201 Created` with `CreatedAtAction`/`CreatedAtRoute` when a canonical URL exists.

## Error responses

When failures use `ProblemDetails`/`ValidationProblemDetails`, describe those contracts where useful. Keep internal exception types, stack traces, SQL, connection strings and filesystem paths out of Swagger examples and descriptions (`rules/backend/error-handling.md` § Unexpected failures).

## Authentication metadata

When the API actually uses authentication, configure the matching security definition and requirements — for Bearer authentication, a Bearer scheme so protected endpoints can be exercised from Swagger UI. An installed authentication package alone is no reason to add a scheme, and global requirements are not applied to anonymous endpoints.

## Descriptions and XML comments

Document what helps consumers: important preconditions, idempotency semantics, pagination/filtering behavior, meaningful outcomes — not descriptions that repeat action or property names. XML comments can help public contracts when the project chooses them; they are not needed on every internal type.

## Multiple documents

Use several Swagger documents only for a real contract separation, such as API versions (`api-versioning`) or distinct public/internal surfaces.

## Generated clients

When the contract drives Angular or other client generation: treat breaking schema changes seriously, keep response metadata accurate, avoid unstable anonymous response shapes, use explicit request/response contracts and review generated-client changes when the contract changes.

## Verification after API changes

1. Verify Controller behavior.
2. Verify the relevant integration tests.
3. Verify the response metadata.
4. Start the API when the change affects startup or composition.
5. Open the Development Swagger UI and confirm it loads.
6. Exercise representative endpoints through Swagger when that is a meaningful behavioral check, and preserve newly verified behavior in maintained tests (`verify` § 4).

## Common mistakes

Metadata that disagrees with runtime responses; Swagger UI exposed publicly without a reason; Swagger treated as a substitute for integration tests; global authentication requirements on anonymous endpoints; anonymous objects as long-lived contracts; a second competing documentation stack without a concrete need.
