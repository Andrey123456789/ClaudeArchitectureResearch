---
name: configuration
description: >
  Use when binding or validating configuration: appsettings, Options pattern,
  IOptions/IOptionsSnapshot/IOptionsMonitor, ValidateOnStart, user-secrets,
  environment variables, connection strings, secret stores.
---

> Kind: KNW | Scope: backend | Capability: — | Loading: on-demand knowledge

# Configuration

Policy: `.claude/rules/backend/operations.md` (typed options, startup validation), `.claude/rules/common/security.md` (secrets).

## Where IConfiguration belongs

Direct `IConfiguration` access is normal in the composition root, configuration-provider setup, and infrastructure registration; ordinary services consume typed options instead of keys and parsing.

## Provider precedence

With the normal ASP.NET Core host, configuration layers `appsettings.json`, `appsettings.{Environment}.json`, development user secrets, environment variables, and command-line arguments, later providers overriding earlier ones; custom providers follow registration order.

## Options pattern with validation

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
    .ValidateOnStart();   // fails at startup when configuration is invalid
```

Numeric values in examples are illustrative, not approved defaults; choose retry counts, timeouts, and limits from the actual integration and deployment requirements. Complex rules use a validation delegate:

```csharp
builder.Services.AddOptions<JwtOptions>()
    .BindConfiguration("Jwt")
    .Validate(options => !string.IsNullOrEmpty(options.Key) && options.Key.Length >= 32 && options.ExpirationMinutes > 0,
        "JWT key must be at least 32 characters and expiration must be positive")
    .ValidateOnStart();
```

Prefer `AddOptions<T>().BindConfiguration(...).ValidateOnStart()` over `Configure<T>(section)`, which defers misconfiguration to runtime.

## Injecting options

- `IOptions<T>` — stable values read once.
- `IOptionsSnapshot<T>` — recomputed per scope (per request).
- `IOptionsMonitor<T>` — current values over time (`CurrentValue`), for singletons and background services.
- Named options — several configurations of one type: `AddOptions<SmtpOptions>("internal").BindConfiguration("Smtp:Internal")`, read with `IOptionsSnapshot<SmtpOptions>.Get("internal")`.

```csharp
// avoid: stringly typed, scattered configuration access
public sealed class PricingService(IConfiguration configuration)
{
    public decimal GetDiscount() => decimal.Parse(configuration["Pricing:DefaultDiscount"]!);
}

// prefer: typed options
public sealed class PricingService(IOptions<PricingOptions> options)
{
    public decimal GetDiscount() => options.Value.DefaultDiscount;
}
```

## Secrets

`appsettings.json` holds structure and non-secret defaults only (`"Jwt": { "Key": "", "Issuer": "myapp" }`); development secrets come from `dotnet user-secrets`, deployed secrets from environment/platform injection or the chosen managed store. Azure Key Vault is one example, used only when the project actually runs on Azure:

```csharp
if (builder.Environment.IsProduction())
{
    builder.Configuration.AddAzureKeyVault(new Uri(builder.Configuration["KeyVault:Uri"]!), new DefaultAzureCredential());
}
```

## Decision guide

| Scenario | Recommendation |
|---|---|
| Binding config to a class | Options pattern with `BindConfiguration` |
| Simple, immutable config | `IOptions<T>` |
| Config that changes per request | `IOptionsSnapshot<T>` |
| Background service watching config | `IOptionsMonitor<T>` |
| Development secrets | `dotnet user-secrets` |
| Production secrets | Environment/platform injection or chosen managed store |
| Validating config | `ValidateDataAnnotations()` + `ValidateOnStart()` |
| Multiple configs of one type | Named options |
