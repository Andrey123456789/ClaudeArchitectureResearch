---
name: configuration
description: .NET configuration technique. Use for appsettings, the Options pattern, IOptions vs IOptionsSnapshot vs IOptionsMonitor, ValidateOnStart, user secrets, environment variables, connection strings, config binding, named options, or external secret providers.
---

> Level: 2-technology · Owns: configuration and options technique · Loading: on demand

# Configuration

Rules: typed-options rule (`.claude/rules/0-core/backend-code.md`), secrets and fail-visibly rules (`.claude/rules/0-core/security.md`). Direct `IConfiguration` access is normal in the composition root, configuration-provider setup, and infrastructure registration; the problem is ordinary services parsing keys.

## Provider precedence

With the default ASP.NET Core host, later providers override earlier ones: `appsettings.json`, `appsettings.{Environment}.json`, user secrets (Development), environment variables, command-line arguments. Custom providers follow registration order.

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
    .ValidateOnStart();
```

Numbers in examples are illustrative, not approved defaults — derive retry counts, timeouts, and limits from the real integration and deployment.

Complex rules:

```csharp
builder.Services.AddOptions<JwtOptions>()
    .BindConfiguration("Jwt")
    .Validate(o => !string.IsNullOrEmpty(o.Authority), "Jwt:Authority is required")
    .ValidateOnStart();
```

## Injecting options

| Need | Use |
| --- | --- |
| stable value | `IOptions<T>` |
| refreshed per scope/request | `IOptionsSnapshot<T>` |
| observe changes over time (background services) | `IOptionsMonitor<T>.CurrentValue` |
| several configurations of one type | named options: `AddOptions<SmtpOptions>("internal").BindConfiguration("Smtp:Internal")`, then `IOptionsSnapshot<T>.Get("internal")` |

```csharp
public sealed class PricingService(IOptions<PricingOptions> options)
{
    public decimal GetDiscount() => options.Value.DefaultDiscount;   // instead of decimal.Parse(configuration["Pricing:DefaultDiscount"]!)
}
```

## Secrets

`appsettings.json` holds structure and non-secret defaults only (`"Jwt": { "Key": "", "Issuer": "myapp" }`). Development values come from `dotnet user-secrets`; deployed environments use environment/platform injection or the chosen managed store. A managed provider is added only for the platform actually used, for example:

```csharp
if (builder.Environment.IsProduction())
{
    builder.Configuration.AddAzureKeyVault(new Uri(builder.Configuration["KeyVault:Uri"]!), new DefaultAzureCredential());
}
```

## Anti-patterns

Services reading string keys from `IConfiguration`; secrets in committed settings files; `Configure<T>(section)` without validation for settings the app cannot run without; copying example numbers into production configuration.
