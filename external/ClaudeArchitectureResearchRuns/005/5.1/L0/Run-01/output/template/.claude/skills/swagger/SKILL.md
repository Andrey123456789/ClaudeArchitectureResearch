---
name: swagger
description: >
  Use when configuring or reviewing Swagger UI (Swashbuckle): setup, Development
  launch profile, response metadata, ProblemDetails schemas, Bearer security
  definitions, multiple documents, generated clients.
---

> Level: 2 Technology · Owns: Swagger/Swashbuckle technique · Scope: backend · Loads: on demand (knowledge skill)

# Swagger

Policy owners: `.claude/rules/1-architecture/entry-points.md` (documentation matches the running API), `.claude/rules/2-technology/aspnet-core.md` (Development exposure). Swashbuckle is the selected tool; Swagger tooling uses the OpenAPI specification internally, while the developer-facing surface is the interactive UI. Status semantics: `http-api`; error contracts: `aspnet-error-handling`.

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

Keep Swagger configuration in the Api composition layer. Do not add a second documentation stack (for example built-in `AddOpenApi()`/`MapOpenApi()` alongside Swashbuckle) without a concrete need.

## Development launch profile

```json
{
  "launchBrowser": true,
  "launchUrl": "swagger"
}
```

The profile's application URLs must match the real ports — never point a browser launch URL at HTTPS on an HTTP-only port.

## Response metadata

```csharp
[HttpGet("{id:guid}")]
[ProducesResponseType<OrderResponse>(StatusCodes.Status200OK)]
[ProducesResponseType<ProblemDetails>(StatusCodes.Status404NotFound)]
public async Task<ActionResult<OrderResponse>> GetById(Guid id, CancellationToken cancellationToken)
```

Derive the documented statuses from the whole pipeline — model binding, validation, authentication/authorization, rate limiting, central exception handling, middleware — not only from branches in the action. Typical mismatches: `201` documented for an endpoint that returns `200`; `204` documented for one that returns a body. For creation, document `201` with `CreatedAtAction`/`CreatedAtRoute` when a canonical URL exists. Examples and descriptions follow the error-exposure rule in `security-principles.md`.

## Authentication metadata

When the API actually uses Bearer authentication, add a matching security definition so authenticated endpoints can be exercised from the UI:

```csharp
builder.Services.AddSwaggerGen(options =>
{
    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT"
    });
    // Add a security requirement only for endpoints that actually require authentication
    // (an operation filter that checks endpoint metadata), not globally over anonymous endpoints.
});
```

Do not add a scheme merely because an authentication package is installed. The Swashbuckle major version determines the `Microsoft.OpenApi` model API — check the installed version's documentation.

## Descriptions and XML comments

Document what helps a consumer: important preconditions, idempotency, pagination/filtering behavior, meaningful outcomes. Avoid descriptions that repeat names. XML comments (`<GenerateDocumentationFile>` + `options.IncludeXmlComments(...)`) suit public API contracts when the project chooses them — not every internal type.

## Multiple documents

Use several Swagger documents only for a real contract separation (API versions, public vs internal surfaces). Versioning strategy: `api-versioning` skill.

## Generated clients

When Angular or other clients are generated from the document: treat breaking schema changes seriously, keep metadata accurate, avoid anonymous response shapes, use explicit request/response contracts, and review generated-client diffs whenever the contract changes.

## Verification after API changes

1. Controller behavior and relevant integration tests.
2. Response metadata against runtime behavior.
3. Start the API when startup or composition changed and open `/swagger` in Development.
4. Exercise representative endpoints from the UI when that is a meaningful behavioral check — and preserve what it proved as maintained tests.

## Review cues

Metadata that disagrees with runtime responses, Swagger UI exposed publicly without a reason, Swagger used instead of integration tests, global auth requirements on anonymous endpoints, anonymous objects as long-lived contracts.
