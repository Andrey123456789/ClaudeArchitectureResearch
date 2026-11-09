---
name: swagger
description: Use when setting up or reviewing Swagger UI and API documentation for Controller APIs — Swashbuckle setup, Development launch profile, ProducesResponseType metadata, ProblemDetails schemas, Bearer security definitions, descriptions, XML comments, multiple documents, generated clients.
---
<!-- Kind: KNW | Scope: backend | Owns: Swashbuckle/OpenAPI documentation technique | Loads: on demand (model-invoked) -->
# Swagger

Decision: DEC-DOCS-01. Standards: `rules/backend/api.md` § OpenAPI Accuracy and `rules/backend/operations.md` § Swagger UI Exposure. Status semantics: `http-api`; error behavior: `aspnet-error-handling`.

Swagger tooling describes the API with the OpenAPI specification internally; the developer-facing surface in this template is the interactive Swagger UI, not a standalone raw OpenAPI endpoint.

## Baseline Package

`Swashbuckle.AspNetCore`, version selected through `add-dependency`.

## Basic Setup

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

Keep Swagger configuration in the Api/composition layer, and avoid making built-in `AddOpenApi()` / `MapOpenApi()` the default when the requirement is Swagger UI.

## Development Launch

For a new local API, a launch profile that opens Swagger directly improves the developer experience:

```json
{
  "launchBrowser": true,
  "launchUrl": "swagger"
}
```

The actual HTTP/HTTPS application URLs agree with the launch profile — no browser launch URL pointing to HTTPS on an HTTP-only port.

## Controller Response Metadata

Document important response types when useful, kept in sync with runtime behavior:

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

`201` documented for an endpoint that returns `200`, or `204` for one that returns a body, are typical mismatches. Possible responses come from the complete pipeline — model binding, validation, authentication/authorization, rate limiting, centralized exception handling, other middleware — not only explicit branches in the action; avoid speculative `ProducesResponseType` entries for merely theoretical statuses.

## Creation Responses

Document `201 Created` when that is the runtime contract, preferring `CreatedAtAction` / `CreatedAtRoute` when a canonical resource URL exists.

## Error Responses

When runtime failures use `ProblemDetails` or `ValidationProblemDetails`, describe those contracts where useful; keep internal exception types, stack traces, SQL, connection strings and file paths out of examples and descriptions.

## Authentication Metadata

When the API actually uses authentication, configure the matching security definition and requirements — for Bearer authentication an appropriate Bearer scheme so authenticated endpoints can be exercised in Swagger UI. An installed authentication package alone is not a reason to add a scheme, and anonymous endpoints keep anonymous metadata.

## Descriptions

Document what helps a consumer understand the contract — important preconditions, idempotency semantics, pagination/filtering behavior, meaningful outcomes — rather than repeating action or property names.

## XML Documentation

XML comments may help public API contracts when the project chooses them; adding them to every internal type solely for Swagger is unnecessary.

## Multiple Documents

Multiple Swagger documents only for a real contract separation, such as API versions or distinct public/internal surfaces (versioning: `api-versioning` skill).

## Generated Clients

When the contract feeds Angular or other client generation: treat breaking schema changes seriously, keep response metadata accurate, avoid unstable anonymous response shapes, use explicit request/response contracts, and review generated-client changes when the contract changes.

## Anti-Patterns

Avoid metadata that disagrees with runtime responses, Swagger UI exposed publicly without a reason, Swagger as a substitute for integration tests, authentication requirements applied globally to anonymous endpoints, anonymous objects as long-lived contracts, and a second competing documentation stack without a concrete need.

## Checks After API Changes

Confirm controller behavior and integration tests, verify response metadata, start the API when startup/composition changed, and open the Development Swagger UI to confirm it loads (`verify` § 3, Runtime Smoke Verification).
