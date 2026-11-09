---
name: swagger
description: >
  Use when configuring or reviewing Swagger/Swashbuckle: AddSwaggerGen,
  Development-only UI, launchUrl, ProducesResponseType, ProblemDetails
  documentation, Bearer security definitions, XML comments, generated clients.
---

> Kind: KNW | Scope: backend | Capability: — | Loading: on-demand knowledge

# Swagger

Policy: `.claude/rules/backend/api-contracts.md` (documentation matches runtime; environment exposure). Decision: Swashbuckle Swagger UI (decision register). Status-code semantics: `http-api`; error contracts: `aspnet-error-handling`. Swagger tooling uses the OpenAPI specification internally; the developer-facing requirement is the interactive UI, not a standalone raw OpenAPI endpoint.

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

Keep Swagger configuration in the Api/composition layer. Package: `Swashbuckle.AspNetCore` (`add-dependency`).

## Development launch

A launch profile can open Swagger directly (`"launchBrowser": true, "launchUrl": "swagger"`). The actual HTTP/HTTPS application URLs must agree with the profile; never point a browser launch URL to HTTPS on an HTTP-only port.

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

Document only statuses in the endpoint's real runtime contract: never `201` when the endpoint returns `200`, never `204` when it returns a body, no speculative entries because a status is theoretically possible. Consider the complete pipeline — model binding, validation, authentication/authorization, rate limiting, centralized exception handling, other middleware — not only explicit controller branches. For creation endpoints document `201` and prefer `CreatedAtAction`/`CreatedAtRoute` when a canonical URL exists. Describe `ProblemDetails`/`ValidationProblemDetails` where useful, and never expose internal exception types, stack traces, SQL, connection strings, or paths in examples.

## Authentication metadata

When the API uses authentication, configure the matching security definition and requirements (e.g. a Bearer scheme so authenticated endpoints can be exercised in the UI). Do not add a scheme merely because an authentication package is installed, and do not apply authentication requirements globally to anonymous endpoints.

## Descriptions and XML comments

Document what helps a consumer: important preconditions, idempotency semantics, pagination/filtering behavior, meaningful outcomes; avoid descriptions that repeat action or property names. XML comments may document public contracts when the project chooses them; do not add them to every internal type for Swagger.

## Multiple documents

Use several documents only for a real contract separation (API versions, distinct public/internal surfaces); versioning strategy: `api-versioning`.

## Generated clients

When the contract feeds frontend or other client generation: treat breaking schema changes seriously, keep metadata accurate, avoid unstable anonymous response shapes, use explicit request/response contracts, and review generated-client changes when the contract changes.

## Verification

When API behavior changes: verify controller behavior and relevant integration tests, verify response metadata, start the API when startup/composition changed, open the Development Swagger UI and confirm it loads, exercise representative endpoints when that is a meaningful check, and preserve newly verified behavior in maintained tests (`verify`).

## Anti-patterns

Metadata that disagrees with runtime responses, Swagger UI exposed publicly without a reason, Swagger as a substitute for integration tests, anonymous objects as long-lived contracts, and a second competing documentation stack without a concrete need.
