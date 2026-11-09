---
name: swagger
description: >
  Use for Swagger UI with Swashbuckle: AddSwaggerGen/UseSwaggerUI, Development
  exposure, launchSettings, ProducesResponseType, ProblemDetails schemas,
  Bearer security definitions, generated clients.
---

> Knowledge skill · Swagger/OpenAPI documentation technique · Policy: `.claude/rules/api.md` § Swagger · Stack decision: `docs/technology-stack.md` § API Documentation

# Swagger

Swagger tooling describes the API with the OpenAPI specification internally;
the developer-facing surface is the interactive Swagger UI rather than a
standalone raw OpenAPI endpoint. Status-code semantics: `http-api` skill; error
contracts: `aspnet-error-handling` skill.

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

Keep Swagger configuration in the API/composition layer. Select the package
version through `add-dependency`.

## Development Launch

For a new local Development API, configure the launch profile so the browser
opens Swagger directly when that helps:

```json
{
  "launchBrowser": true,
  "launchUrl": "swagger"
}
```

The application URLs must agree with the launch profile; do not point a
browser launch URL at HTTPS on an HTTP-only port.

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

Determine possible responses from the complete HTTP pipeline, not only the
explicit branches of the action: model binding, validation,
authentication/authorization, rate limiting, centralized exception handling,
and other middleware can all produce responses. Do not document `201` when the
endpoint returns `200`, or `204` when it returns a body.

## Creation Responses

Document `201 Created` when that is the runtime contract, and prefer
`CreatedAtAction` / `CreatedAtRoute` when a canonical resource URL exists.

## Error Responses

When failures use `ProblemDetails` or `ValidationProblemDetails`, describe those
contracts where useful. Swagger examples and descriptions never show internal
exception types, stack traces, SQL, connection strings, or filesystem paths.

## Authentication Metadata

When the API actually uses authentication, configure the matching security
definition and requirements; for Bearer authentication expose a Bearer scheme so
authenticated endpoints can be exercised through Swagger UI. Do not add a scheme
merely because an authentication package is installed, and do not apply
authentication requirements globally to anonymous endpoints.

## Descriptions

Document what helps a consumer understand the contract — important
preconditions, idempotency semantics, pagination/filtering behavior, meaningful
outcomes — rather than repeating action or property names.

## XML Documentation

XML comments may help public API contracts when the project chooses them; do
not add them to every internal type solely for Swagger generation.

## Multiple Documents

Use multiple Swagger documents only for a real contract separation, such as API
versions or distinct public/internal surfaces (`api-versioning` skill).

## Generated Clients

If the contract feeds frontend or other client generation: treat breaking
schema changes seriously, keep response metadata accurate, avoid unstable
anonymous response shapes, use explicit request/response contracts, and review
generated-client changes when the contract changes.

## Verification

When API behavior changes: verify Controller behavior and relevant integration
tests, verify response metadata, start the API when startup/composition changed,
open the Development Swagger UI and confirm it loads, exercise representative
endpoints through Swagger when that is a meaningful behavioral check, and
preserve newly verified behavior as maintained tests (`verify` § Preserve
Behavioral Verification).

## Review Checks

Check-by-reference against `api.md` § Swagger: metadata that disagrees with
runtime responses; Swagger UI exposed publicly without a reason; Swagger used as
a substitute for integration tests; anonymous objects as long-lived API
contracts; a second competing documentation stack without a concrete need.
