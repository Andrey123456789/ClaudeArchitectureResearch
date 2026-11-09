---
name: swagger
description: >
  Use when configuring Swashbuckle Swagger UI, launch profiles that open
  /swagger, ProducesResponseType metadata, ProblemDetails or Bearer security
  schemes in Swagger, XML comments, multiple Swagger documents, or API contracts
  used for client generation.
---

> Owns: Swashbuckle/Swagger configuration technique | Scope: backend | Loads: on demand (knowledge skill)

# Swagger

Policy owners: documentation must match runtime behavior →
`.claude/rules/api.md` (Swagger); Swashbuckle as the baseline and where the UI is
exposed → `docs/technology-stack.md`. Status semantics: `http-api`. Error contracts:
`aspnet-error-handling`.

Swagger tooling uses the OpenAPI specification internally; the developer-facing
baseline is the interactive Swagger UI rather than a standalone raw document
endpoint.

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

## Development Launch Profile

```json
{
  "profiles": {
    "https": {
      "commandName": "Project",
      "launchBrowser": true,
      "launchUrl": "swagger",
      "applicationUrl": "https://localhost:7001;http://localhost:5001",
      "environmentVariables": { "ASPNETCORE_ENVIRONMENT": "Development" }
    }
  }
}
```

The application URLs must agree with the launch profile; never point a browser
launch at HTTPS on an HTTP-only port.

## Response Metadata

```csharp
[HttpGet("{id:guid}")]
[ProducesResponseType<OrderResponse>(StatusCodes.Status200OK)]
[ProducesResponseType<ProblemDetails>(StatusCodes.Status404NotFound)]
public async Task<ActionResult<OrderResponse>> GetById(Guid id, CancellationToken cancellationToken)
```

When listing possible responses, consider the whole pipeline — model binding,
validation (`ValidationProblemDetails`), authentication/authorization, rate
limiting, centralized exception handling — not only explicit branches. For
creation endpoints returning `201`, prefer `CreatedAtAction`/`CreatedAtRoute`.
Keep examples and descriptions free of internal exception types, stack traces,
SQL, connection strings, and paths.

## Bearer Authentication in Swagger UI

Only when the API actually uses Bearer authentication:

```csharp
builder.Services.AddSwaggerGen(options =>
{
    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT",
    });
    // Add the requirement only to operations that require authentication
    // (for example via an IOperationFilter checking [Authorize]/[AllowAnonymous]).
});
```

Do not apply authentication requirements globally to anonymous endpoints.

## Descriptions and XML Comments

Describe what helps a consumer: preconditions, idempotency, pagination/filtering
behavior, meaningful outcomes — not restated names. XML comments are optional
for public contracts; do not add them to every internal type just for Swagger.

## Multiple Documents

Only for a real contract separation (API versions, public vs. internal
surfaces). Versioning strategy: `api-versioning`.

## Generated Clients

When the contract feeds Angular or other client generation: use explicit
request/response contracts (no anonymous shapes), keep metadata accurate, treat
breaking schema changes seriously, and review generated-client diffs.

## Verification After API Changes

1. Verify Controller behavior and relevant integration tests.
2. Verify response metadata against the runtime pipeline.
3. Start the API when startup/composition changed; open the Development Swagger
   UI and confirm it loads.
4. Exercise representative endpoints when that is a meaningful behavioral
   check, and preserve newly verified behavior as tests (`verify`).

Swagger is not a substitute for integration tests, and a second competing
API-documentation stack needs a concrete reason.
