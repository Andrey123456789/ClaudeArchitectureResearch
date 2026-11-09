---
name: swagger
description: >
  Use when configuring Swashbuckle Swagger UI: AddSwaggerGen/UseSwaggerUI, launch
  profile, ProducesResponseType metadata, ProblemDetails docs, Bearer definitions.
---

> Level: 2 Technology · Owns: Swagger/OpenAPI documentation technique and examples (knowledge) · Scope: backend · Loads: on invocation · Depends on: .claude/rules/1-architecture/entry-points.md, .claude/rules/2-technology/aspnet-core.md

# Swagger

Policy owners: documentation must match runtime → `.claude/rules/1-architecture/entry-points.md` → Documentation truth; Swagger UI exposure → `2-technology/aspnet-core.md`; Swashbuckle as baseline → `3-project/decisions.md`; status semantics → `http-api` skill; error contract → `aspnet-error-handling` skill. Swagger tooling uses the OpenAPI specification internally; the developer-facing baseline is interactive Swagger UI, not a standalone raw OpenAPI endpoint. This skill is technique only.

## Basic setup

```csharp
builder.Services.AddControllers();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();      // served at /swagger
}

app.MapControllers();
```

Keep Swagger configuration in Api/composition. Built-in `AddOpenApi()` / `MapOpenApi()` is not the template default when the requirement is Swagger UI.

## Development launch

```json
{
  "launchBrowser": true,
  "launchUrl": "swagger"
}
```

The launch profile's URLs must agree with the configured HTTP/HTTPS ports — never a browser launch URL pointing to HTTPS on an HTTP-only port.

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

When determining real responses consider the whole pipeline — model binding, validation, authentication/authorization, rate limiting, centralized exception handling, other middleware — not only explicit branches in the action. Document `201 Created` (with `CreatedAtAction`/`CreatedAtRoute` when a canonical URL exists) only when that is the runtime contract; never `204` for an endpoint that returns a body. Describe ProblemDetails/ValidationProblemDetails contracts where useful; examples and descriptions never show exception types, stack traces, SQL, connection strings, or paths.

## Authentication metadata

When the API actually uses Bearer authentication, add a matching security definition and requirements so authenticated endpoints can be exercised from Swagger UI:

```csharp
builder.Services.AddSwaggerGen(options =>
{
    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT"
    });
});
```

Do not add a scheme merely because an authentication package is installed, and do not apply authentication requirements globally to anonymous endpoints.

## Descriptions and XML comments

Document what helps a consumer: important preconditions, idempotency semantics, pagination/filtering behavior, meaningful outcomes; avoid descriptions that repeat names. XML comments suit public API contracts when the project chooses them — not every internal type.

## Multiple documents

Use several Swagger documents only for a real contract separation (API versions, public vs internal surfaces); versioning strategy belongs to the `api-versioning` skill.

## Generated clients

When the contract feeds Angular or other client generation: treat breaking schema changes seriously, keep response metadata accurate, avoid unstable anonymous response shapes, use explicit request/response contracts, and review generated-client changes.

## Verification after API changes

Verify controller behavior and integration tests, verify the response metadata, start the API when startup/composition changed, open the Development Swagger UI, exercise representative endpoints when that is a meaningful check — and preserve newly verified behavior as `verify` step 4 requires.

## Anti-patterns

Swagger as a substitute for integration tests; anonymous objects as long-lived contracts; a second competing documentation stack without a concrete need.
