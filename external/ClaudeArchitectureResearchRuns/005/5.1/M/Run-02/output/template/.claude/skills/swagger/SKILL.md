---
name: swagger
description: >
  Use when setting up or changing Swashbuckle Swagger:
  AddSwaggerGen/UseSwaggerUI, launchSettings, ProducesResponseType metadata,
  ProblemDetails schemas, Bearer security definitions, XML comments, multiple
  documents, generated clients.
---

> Owner: Swagger/Swashbuckle setup and metadata technique (normative policy lives in rules) | Scope: backend | Loads: on demand — knowledge | Enforced: none

# Swagger

Policy: `.claude/rules/api.md` § Swagger (runtime accuracy, environment
exposure). Baseline package: `docs/technology-stack.md` § Backend. Status-code
semantics: `http-api` skill; error contracts: `aspnet-error-handling` skill.

Swashbuckle describes the API with the OpenAPI specification internally; the
developer-facing requirement here is the interactive Swagger UI rather than a
standalone raw OpenAPI endpoint.

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

Keep Swagger configuration in the API/composition layer. A project scaffolded
with `dotnet new webapi` may contain `AddOpenApi()`/`MapOpenApi()` and the
`Microsoft.AspNetCore.OpenApi` package; replace them with this setup.

## Development Launch

Open Swagger directly in the local Development launch profile
(`Properties/launchSettings.json`):

```json
{
  "launchBrowser": true,
  "launchUrl": "swagger"
}
```

The HTTP/HTTPS application URLs must agree with the profile; never point the
launch URL at HTTPS on an HTTP-only port.

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

Determine possible responses from the complete HTTP pipeline, not only explicit
branches in the action: model binding, validation, authentication/authorization,
rate limiting, centralized exception handling, and other middleware can produce
responses too. Typical mismatches to avoid: documenting `201` when the action
returns `200`, or `204` when it returns a body.

## Creation Responses

Document `201 Created` when that is the runtime contract, preferably produced by
`CreatedAtAction` / `CreatedAtRoute` when a canonical resource URL exists.

## Error Responses

When failures use `ProblemDetails` or `ValidationProblemDetails`, describe those
contracts where useful. Keep internal exception types, stack traces, SQL,
connection strings, and paths out of examples and descriptions.

## Authentication Metadata

When the API actually uses Bearer authentication, expose a matching scheme so
authenticated endpoints can be exercised from Swagger UI:

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

Add the matching security requirement for protected operations (globally or per
operation through an operation filter), and keep anonymous endpoints free of it.
The exact model types differ between Swashbuckle major versions; follow the
installed version's documentation. Do not add a scheme merely because an
authentication package is installed.

## Descriptions

Document what helps a consumer understand the contract: important preconditions,
idempotency semantics, pagination and filtering behavior, meaningful response
outcomes. Skip descriptions that merely repeat action or property names.

## XML Documentation

XML comments can document public API contracts when the project chooses them:

```xml
<GenerateDocumentationFile>true</GenerateDocumentationFile>
```

```csharp
builder.Services.AddSwaggerGen(options =>
{
    var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    options.IncludeXmlComments(Path.Combine(AppContext.BaseDirectory, xmlFile));
});
```

Do not add XML comments to every internal type solely for Swagger.

## Multiple Documents

Use several Swagger documents only for a real contract separation, such as API
versions (`api-versioning` skill) or distinct public and internal surfaces.

## Generated Clients

When the contract feeds Angular or other client generation: treat breaking schema
changes seriously, keep response metadata accurate, avoid unstable anonymous
response shapes, use explicit request/response contracts, and review
generated-client changes whenever the contract changes.

## Common Mistakes

- treating Swagger as a substitute for integration tests;
- applying authentication requirements globally to anonymous endpoints;
- anonymous objects as important long-lived contracts;
- a second competing API-documentation stack without a concrete need.

## Verification

When API behavior changes:

1. verify Controller behavior and the relevant integration tests;
2. verify response metadata;
3. start the API when the change affects startup or composition;
4. open the Development Swagger UI and confirm it loads;
5. exercise representative endpoints through Swagger when that is a meaningful
   behavioral check;
6. preserve newly verified behavior in maintained tests
   (`.claude/rules/testing.md` § Regression and Behavioral Verification).
