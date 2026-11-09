---
name: swagger
description: >
  Use when configuring Swagger/OpenAPI for Controllers: Swashbuckle setup,
  Development UI, launch settings, response metadata, ProblemDetails
  documentation, Bearer definitions, generated clients.
---

> Owns: Swagger/OpenAPI technique and examples (no policy) | Scope: backend | Loads: on demand (knowledge skill)

# Swagger

Policy owners: the Swashbuckle/Swagger UI baseline — `docs/technology-stack.md`;
documentation accuracy and environment exposure — `.claude/rules/api.md`;
status-code semantics — `http-api` skill; error contracts —
`.claude/rules/error-handling.md`.

Swagger tooling describes the API with the OpenAPI specification internally;
the developer-facing requirement here is the interactive Swagger UI, not a
standalone raw OpenAPI endpoint.

## Package

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

Keep Swagger configuration in the API/composition layer.

## Development Launch

For a new local Development API, configure the launch profile so the browser
opens Swagger directly when that helps:

```json
{
  "launchBrowser": true,
  "launchUrl": "swagger"
}
```

The application's HTTP/HTTPS URLs must agree with the launch profile; do not
point the launch URL at HTTPS on an HTTP-only port.

## Controller Response Metadata

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

Do not document `201` when the endpoint returns `200`, or `204` when it returns
a body. When determining possible responses, consider the whole pipeline —
model binding, validation, authentication/authorization, rate limiting,
centralized exception handling, other middleware — not only explicit branches in
the action; but do not add an entry merely because a status is theoretically
possible.

## Creation Responses

Document `201 Created` when that is the runtime contract, and prefer
`CreatedAtAction`/`CreatedAtRoute` when a canonical resource URL exists.

## Error Responses

When runtime failures use `ProblemDetails` or `ValidationProblemDetails`,
describe those contracts where useful. Do not put internal exception types,
stack traces, SQL, connection strings, file paths, or other implementation
details in Swagger examples or descriptions.

## Authentication Metadata

When the API actually uses authentication, configure the matching security
definition and requirements; for Bearer authentication expose a Bearer scheme so
authenticated endpoints can be exercised from Swagger UI. Do not add a scheme
merely because an authentication package is installed, and do not apply
authentication requirements globally to anonymous endpoints.

## Descriptions

Document what helps a consumer understand the contract — important
preconditions, idempotency semantics, pagination/filtering behavior, meaningful
outcomes. Avoid descriptions that repeat action or property names.

## XML Documentation

XML comments may help public API contracts when the project chooses them; do not
add them to every internal type solely for Swagger.

## Multiple Documents

Use multiple Swagger documents only for a real contract separation, such as API
versions or distinct public/internal surfaces (`api-versioning` skill).

## Generated Clients

When the contract feeds Angular or other client generation: treat breaking
schema changes seriously, keep response metadata accurate, avoid unstable
anonymous response shapes, use explicit request/response contracts, and review
generated-client changes when the contract changes.

## Anti-Patterns

Avoid treating Swagger as a substitute for integration tests, using anonymous
objects as important long-lived contracts, and adding a second competing
API-documentation stack without a concrete need.

## Verification

When API behavior changes:

1. verify Controller behavior and relevant integration tests;
2. verify response metadata;
3. start the API when the change affects startup/composition;
4. open the Development Swagger UI and confirm it loads;
5. exercise representative endpoints through Swagger when that is a meaningful
   behavioral check;
6. preserve newly verified behavior in maintained tests (`verify` step 4).
