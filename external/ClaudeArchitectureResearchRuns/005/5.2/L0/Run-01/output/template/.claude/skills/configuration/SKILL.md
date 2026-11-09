---
name: configuration
description: >
  Use for .NET configuration: Options pattern, startup validation, IOptions variants, appsettings layering, user secrets, secret providers.
---

> Level: 2 Technology | Owns: .NET configuration technique | Scope: backend | Loads: knowledge skill (on demand) | Depends on: 2-technology/dotnet-runtime.md, 0-core/security-principles.md

# Configuration Technique

Policy owners (routing): typed and validated options →
`2-technology/dotnet-runtime.md`; secrets → `0-core/security-principles.md`;
Development connection string → `3-project/data-lifecycle.md`; tunable product
values → `CUSTOM_SETTINGS.md` (not runtime configuration).

Direct `IConfiguration` access is normal in `Program.cs`, configuration-provider
setup, and infrastructure registration; ordinary services consume options.

## Options Pattern

```csharp
public sealed class DatabaseOptions
{
    public const string SectionName = "Database";

    [Required]
    public required string ConnectionString { get; init; }

    [Range(1, 60)]
    public int CommandTimeoutSeconds { get; init; } = 30;
}

builder.Services.AddOptions<DatabaseOptions>()
    .BindConfiguration(DatabaseOptions.SectionName)
    .ValidateDataAnnotations()
    .ValidateOnStart();   // fail at startup, not on first use
```

Numbers in examples are illustrative; choose timeouts, retry counts, and limits
from the actual integration and deployment requirements.

## Complex Validation

```csharp
builder.Services.AddOptions<JwtOptions>()
    .BindConfiguration("Jwt")
    .Validate(o => !string.IsNullOrEmpty(o.Key) && o.Key.Length >= 32 && o.ExpirationMinutes > 0,
        "JWT key must be at least 32 characters and expiration must be positive")
    .ValidateOnStart();
```

## Consuming Options

| Need | Type |
|---|---|
| Stable value | `IOptions<T>` |
| Refreshed per scope (request) | `IOptionsSnapshot<T>` |
| Observed over time (singletons, background services) | `IOptionsMonitor<T>` (`CurrentValue`) |
| Several instances of one type | Named options: `AddOptions<SmtpOptions>("internal").BindConfiguration("Smtp:Internal")`, then `IOptionsSnapshot<T>.Get("internal")` |

## Provider Precedence

With the default ASP.NET Core host, later providers override earlier ones:
`appsettings.json` → `appsettings.{Environment}.json` → user secrets
(Development) → environment variables → command-line arguments. Custom providers
follow their registration order. Environment variables use `__` for nesting
(`ConnectionStrings__DefaultConnection`).

## Secrets

- Development: `dotnet user-secrets init` and
  `dotnet user-secrets set "Jwt:Key" "<value>"` in the Api project.
- Deployed: environment or platform secret injection, or a managed store chosen
  by the project. Example for Azure only when the project uses Azure:

```csharp
if (builder.Environment.IsProduction())
{
    builder.Configuration.AddAzureKeyVault(
        new Uri(builder.Configuration["KeyVault:Uri"]!), new DefaultAzureCredential());
}
```

`appsettings.json` holds structure and non-secret defaults only:

```json
{ "Jwt": { "Key": "", "Issuer": "myapp", "Audience": "myapp" } }
```

## Avoid

```csharp
// Stringly typed, scattered parsing inside a service
decimal.Parse(configuration["Pricing:DefaultDiscount"]!);

// Binding without startup validation — misconfiguration found at runtime
builder.Services.Configure<JwtOptions>(builder.Configuration.GetSection("Jwt"));
```
