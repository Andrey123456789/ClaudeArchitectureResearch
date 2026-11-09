---
name: swagger
description: Use when configuring or reviewing Swagger UI and OpenAPI metadata for ASP.NET Core controllers with Swashbuckle — AddSwaggerGen, Development-only UI, launch profiles, ProducesResponseType metadata, ProblemDetails, Bearer security definitions, multiple documents or generated clients.
---
Kind: KNW | Scope: backend | Capability: — | Loading: on invocation

# Swagger

Rules: `.claude/rules/backend/http-api.md` → API documentation (metadata matches runtime behavior, environment-aware exposure). Stack decision: decision register (Swashbuckle Swagger UI). Status semantics: `http-api` skill; error contracts: `aspnet-error-handling` skill. Swagger tooling uses the OpenAPI specification internally; the developer-facing surface is the interactive Swagger UI, not a standalone raw OpenAPI endpoint.

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

Keep Swagger configuration in the Api composition layer. Package versions: `add-dependency`.

## Development launch

For a new local API, let the launch profile open Swagger when that helps:

```json
{
  "launchBrowser": true,
  "launchUrl": "swagger"
}
```

The application URLs must agree with the profile; do not point the launch URL at HTTPS on an HTTP-only port.

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

Determine the possible responses from the whole pipeline (model binding, validation, authentication and authorization, rate limiting, centralized exception handling, middleware), not only from branches in the action. For creation, document `201 Created` when that is the runtime contract and prefer `CreatedAtAction`/`CreatedAtRoute` when a canonical resource URL exists. When failures use `ProblemDetails`/`ValidationProblemDetails`, describe those contracts where useful, without internal exception types, stack traces, SQL, connection strings or file paths in examples or descriptions.

## Authentication metadata

When the API actually uses authentication, configure the matching security definition and requirements; for Bearer authentication, expose a Bearer scheme so authenticated endpoints can be exercised from Swagger UI. Do not add a scheme merely because an authentication package is installed, and do not apply authentication requirements globally to anonymous endpoints.

## Descriptions and XML comments

Document what helps a consumer: important preconditions, idempotency semantics, pagination and filtering behavior, meaningful outcomes. Avoid descriptions that repeat action or property names. XML comments may help public contracts when the project chooses them; do not add them to every internal type for Swagger's sake.

## Multiple documents

Use several Swagger documents only for a real contract separation, such as API versions or distinct public and internal surfaces. Versioning strategy: `api-versioning` skill.

## Generated clients

When the contract drives frontend or other client generation: treat breaking schema changes seriously, keep response metadata accurate, avoid unstable anonymous response shapes, use explicit request and response contracts, and review generated-client changes when the contract changes.

## Verification

When API behavior changes: verify controller behavior and the relevant integration tests, verify the response metadata, start the API when startup or composition changed, open the Development Swagger UI and confirm it loads, exercise representative endpoints when that is a meaningful check, and preserve newly verified behavior as maintained tests (`verify` → step 4).

## Anti-patterns

Review checks; the named standard owns each rule:

- Metadata that disagrees with runtime responses, or speculative response codes? (`http-api.md`)
- Swagger UI exposed publicly without a requirement? (`http-api.md`)
- Swagger used as a substitute for integration tests?
- Anonymous objects as long-lived API contracts?
- A second competing documentation stack without a concrete need? (decision register)
