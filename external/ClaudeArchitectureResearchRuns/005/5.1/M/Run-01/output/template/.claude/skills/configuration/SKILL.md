---
name: configuration
description: >
  Use when binding configuration sections, writing options classes, choosing
  IOptions/IOptionsSnapshot/IOptionsMonitor, validating settings at startup,
  managing user-secrets or environment variables, adding a secret provider, or
  reasoning about appsettings and provider precedence.
---

> Owns: .NET configuration and options technique | Scope: backend | Loads: on demand (knowledge skill)

# Configuration

Policy owners: typed options and startup validation → `.claude/rules/architecture.md`
(Dependency Injection and Configuration); secrets → `.claude/rules/security.md`;
local Development connection string → `.claude/rules/persistence.md`. Approved
product limits belong in `CUSTOM_SETTINGS.md`, not in configuration examples.

## Provider Precedence

With the default ASP.NET Core host, later providers override earlier ones:
`appsettings.json` → `appsettings.{Environment}.json` → user secrets
(Development) → environment variables → command-line arguments. Custom providers
follow their registration order. Direct `IConfiguration` access is normal in
`Program.cs`, provider setup, and Infrastructure registration.

## Options Pattern

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
    .ValidateOnStart();
```

```json
{ "Database": { "ConnectionString": "", "MaxRetryCount": 3 } }
```

Numeric values are illustrative; choose retry counts, timeouts, and limits from
actual integration and deployment requirements.

## Injecting Options

| Type | Use |
|---|---|
| `IOptions<T>` | Stable values read once (singleton-friendly) |
| `IOptionsSnapshot<T>` | Values recomputed per scope; named options via `.Get(name)` |
| `IOptionsMonitor<T>` | Long-lived services observing changes (`CurrentValue`, `OnChange`) |

```csharp
public sealed class PricingService(IOptions<PricingOptions> options)
{
    public decimal GetDiscount() => options.Value.DefaultDiscount;
}
```

Anti-example: a service taking `IConfiguration` and parsing
`configuration["Pricing:DefaultDiscount"]` itself.

## Custom Validation

```csharp
builder.Services.AddOptions<JwtOptions>()
    .BindConfiguration("Jwt")
    .Validate(o => !string.IsNullOrEmpty(o.Authority), "Jwt:Authority is required")
    .ValidateOnStart();
```

For complex rules implement `IValidateOptions<T>`. Registering with
`Configure<T>(section)` alone skips validation until first use.

## Named Options

```csharp
builder.Services.AddOptions<SmtpOptions>("internal").BindConfiguration("Smtp:Internal");
builder.Services.AddOptions<SmtpOptions>("customer").BindConfiguration("Smtp:Customer");

public sealed class EmailService(IOptionsSnapshot<SmtpOptions> options)
{
    public SmtpOptions Internal => options.Get("internal");
}
```

## Secrets

Development: `dotnet user-secrets init` then
`dotnet user-secrets set "Jwt:Key" "<value>"` in the Api project. Deployed
environments: environment variables (`Jwt__Key`) or the hosting platform's
secret store. Committed `appsettings*.json` keep structure and empty
placeholders:

```json
{ "Jwt": { "Key": "", "Issuer": "myapp", "Audience": "myapp" } }
```

Example managed provider (only when the project actually uses Azure):

```csharp
if (builder.Environment.IsProduction())
{
    builder.Configuration.AddAzureKeyVault(
        new Uri(builder.Configuration["KeyVault:Uri"]!), new DefaultAzureCredential());
}
```
