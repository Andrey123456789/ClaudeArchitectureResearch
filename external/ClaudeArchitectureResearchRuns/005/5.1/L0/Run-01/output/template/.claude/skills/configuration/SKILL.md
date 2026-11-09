---
name: configuration
description: >
  Use when binding configuration, adding settings or connection strings, or
  handling secrets: Options pattern, IOptions variants, ValidateOnStart,
  appsettings layering, user-secrets, environment variables.
---

> Level: 2 Technology · Owns: configuration technique · Scope: backend · Loads: on demand (knowledge skill)

# Configuration

Policy owners: `.claude/rules/2-technology/csharp.md` (typed options, startup validation), `.claude/rules/0-core/security-principles.md` (secrets, failing visibly on missing security configuration). Tunable product values are not configuration-only decisions — they live in `CUSTOM_SETTINGS.md` (product governance).

## Provider precedence

With the default ASP.NET Core host, later providers override earlier ones: `appsettings.json` → `appsettings.{Environment}.json` → user secrets (Development) → environment variables → command-line arguments. Custom providers follow their registration order. Direct `IConfiguration` access is normal in `Program.cs`, composition code and provider setup.

## Options pattern

```csharp
public sealed class DatabaseOptions
{
    public const string SectionName = "Database";

    [Required]
    public required string ConnectionString { get; init; }

    [Range(1, 100)]
    public int MaxRetryCount { get; init; } = 3;
}

builder.Services.AddOptions<DatabaseOptions>()
    .BindConfiguration(DatabaseOptions.SectionName)
    .ValidateDataAnnotations()
    .ValidateOnStart();                                // fails at startup when invalid
```

Numbers in examples are illustrative. Choose retry counts, timeouts and limits from the real integration and deployment requirements.

## Consuming options

```csharp
public sealed class PricingService(IOptions<PricingOptions> options)          // stable value
public sealed class PricingService(IOptionsSnapshot<PricingOptions> options)  // re-read per scope
public sealed class Worker(IOptionsMonitor<WorkerOptions> options)            // observe changes over time
```

## Complex validation

```csharp
builder.Services.AddOptions<JwtOptions>()
    .BindConfiguration("Jwt")
    .Validate(o => !string.IsNullOrEmpty(o.Authority) && !string.IsNullOrEmpty(o.Audience),
        "Jwt:Authority and Jwt:Audience are required")
    .ValidateOnStart();
```

For reusable rules implement `IValidateOptions<T>`.

## Secrets

- Development: `dotnet user-secrets init` (adds a `UserSecretsId`, which is not a secret) and `dotnet user-secrets set "ConnectionStrings:DefaultConnection" "..."` in the Api project.
- Deployed environments: environment variables injected by the platform (`ConnectionStrings__DefaultConnection`), or the platform's managed secret store. Example for Azure (only when the project actually uses Azure):

```csharp
if (builder.Environment.IsProduction())
{
    builder.Configuration.AddAzureKeyVault(
        new Uri(builder.Configuration["KeyVault:Uri"]!),
        new DefaultAzureCredential());
}
```

Committed `appsettings.json` holds structure and non-secret defaults only:

```json
{
  "Jwt": { "Authority": "", "Audience": "myapp" },
  "ConnectionStrings": { "DefaultConnection": "" }
}
```

## Named options

```csharp
builder.Services.AddOptions<SmtpOptions>("internal").BindConfiguration("Smtp:Internal");
builder.Services.AddOptions<SmtpOptions>("customer").BindConfiguration("Smtp:Customer");

public sealed class EmailService(IOptionsSnapshot<SmtpOptions> options)
{
    private SmtpOptions Internal => options.Get("internal");
}
```

## Review cues

Services parsing `configuration["Section:Key"]` strings, `Configure<T>` without startup validation for required settings, secrets in committed files, Azure-specific dependencies in a project not hosted on Azure.

## Decision guide

| Scenario | Typical choice |
|---|---|
| Bind a section to a class | `AddOptions<T>().BindConfiguration(...)` |
| Simple immutable configuration | `IOptions<T>` |
| Per-request refreshed values | `IOptionsSnapshot<T>` |
| Background service watching changes | `IOptionsMonitor<T>` |
| Development secrets | `dotnet user-secrets` |
| Production secrets | Platform secret injection or the chosen managed store |
| Validation | `ValidateDataAnnotations()` / `Validate(...)` + `ValidateOnStart()` |
| Several configurations of one type | Named options |
