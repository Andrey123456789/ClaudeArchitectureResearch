---
name: swagger
description: >
  Use for Swagger UI with Swashbuckle: setup, launch profile,
  ProducesResponseType metadata, ProblemDetails schemas, Bearer security
  definitions, generated clients.
---

> Knowledge skill. Owns: Swagger/Swashbuckle technique and examples · Scope: backend · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/api.md

# Swagger

Decision: Swashbuckle Swagger UI is the Development interactive surface
(`docs/technology-stack.md`). Rules: `api.md` (documentation matches runtime;
environment exposure). Status semantics: `http-api` skill; error contracts:
`aspnet-error-handling` skill. Swagger tooling uses the OpenAPI specification
internally; the developer-facing requirement is the interactive UI, not a raw
OpenAPI endpoint.

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

Keep Swagger configuration in the Api/composition layer.

## Development Launch

For a new local API, a launch profile can open Swagger directly:

```json
{
  "launchBrowser": true,
  "launchUrl": "swagger"
}
```

The application URLs must agree with the launch profile; do not point a browser
launch URL to HTTPS on an HTTP-only port.

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

When determining an endpoint's real responses, consider the whole pipeline —
model binding, validation, authentication/authorization, rate limiting,
centralized exception handling, other middleware — not only the action's
explicit branches. Examples of drift: documenting `201` when the endpoint
returns `200`, or `204` when it returns a body.

## Creation Responses

Document `201 Created` when that is the runtime contract, and prefer
`CreatedAtAction` / `CreatedAtRoute` when a canonical resource URL exists.

## Error Responses

When runtime failures use `ProblemDetails` or `ValidationProblemDetails`,
describe those contracts where useful. Keep Swagger examples and descriptions
free of internal exception types, stack traces, SQL, connection strings, and
filesystem paths (error exposure: `error-handling.md`).

## Authentication Metadata

When the API actually uses authentication, configure the matching security
definition and requirements — for Bearer authentication, a Bearer scheme so
authenticated endpoints can be exercised from the UI. Do not add a scheme merely
because an authentication package is installed, and do not apply authentication
requirements globally to anonymous endpoints.

## Descriptions

Document what helps a consumer: important preconditions, idempotency
semantics, pagination and filtering behavior, meaningful response outcomes.
Avoid descriptions that only repeat action or property names. XML comments may
document public contracts when the project chooses them; do not add them to
every internal type for Swagger's sake.

## Multiple Documents

Use several Swagger documents only for a real contract separation, such as API
versions (`api-versioning` skill) or distinct public/internal surfaces.

## Generated Clients

When the contract feeds Angular or other client generation: treat breaking
schema changes seriously, keep response metadata accurate, avoid unstable
anonymous response shapes, use explicit request/response contracts, and review
generated-client changes when the contract changes.

## Anti-Patterns

- Swagger UI exposed publicly without a reason;
- Swagger treated as a substitute for integration tests;
- anonymous objects as important long-lived contracts;
- a second competing API-documentation stack without a concrete need.

## Verification

When API behavior changes: verify Controller behavior and the relevant
integration tests; verify response metadata; start the API when startup or
composition changed; open the Development Swagger UI and confirm it loads;
exercise representative endpoints through Swagger when that is a meaningful
check — and preserve newly verified behavior as maintained tests (`verify`).
