---
name: configuration
description: Use when binding or validating configuration in .NET — appsettings files, the Options pattern, IOptions/IOptionsSnapshot/IOptionsMonitor, ValidateOnStart, named options, user secrets, environment variables, connection strings, provider precedence or managed secret stores.
---
Kind: KNW | Scope: backend | Capability: — | Loading: on invocation

# Configuration

Rules: `.claude/rules/backend/operations.md` (typed, validated options) and `.claude/rules/common/security.md` (secrets). Approved project values belong in `CUSTOM_SETTINGS.md`, not in this guidance.

## Provider precedence

With the normal ASP.NET Core host, configuration commonly layers `appsettings.json`, `appsettings.{Environment}.json`, development user secrets, environment variables and command-line arguments, with later providers overriding earlier ones. Custom providers follow their registration order. Direct `IConfiguration` access is normal in the composition root, configuration-provider setup and infrastructure registration.

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

```json
{
  "Database": {
    "ConnectionString": "",
    "MaxRetryCount": 3
  }
}
```

Numeric values in examples are illustrative, not approved defaults. Choose retry counts, timeouts and limits from the actual integration and deployment requirements.

## Injecting options

```csharp
// IOptions<T>: stable value for the application lifetime
public sealed class PricingService(IOptions<PricingOptions> options)
{
    private readonly PricingOptions _pricing = options.Value;
}

// IOptionsSnapshot<T>: recomputed per scope
public sealed class PricingService(IOptionsSnapshot<PricingOptions> options) { }

// IOptionsMonitor<T>: observe current values over time (singletons, background services)
public sealed class BackgroundWorker(IOptionsMonitor<WorkerOptions> options)
{
    public void DoWork()
    {
        var current = options.CurrentValue;
    }
}
```

## Complex validation

```csharp
builder.Services.AddOptions<JwtOptions>()
    .BindConfiguration("Jwt")
    .Validate(
        options => !string.IsNullOrEmpty(options.Key) && options.Key.Length >= 32 && options.ExpirationMinutes > 0,
        "JWT key must be at least 32 characters and expiration must be positive")
    .ValidateOnStart();
```

`Configure<T>(section)` without validation discovers misconfiguration only at runtime; prefer `AddOptions<T>().BindConfiguration(...).ValidateOnStart()`.

## Named options

```csharp
builder.Services.AddOptions<SmtpOptions>("internal").BindConfiguration("Smtp:Internal");
builder.Services.AddOptions<SmtpOptions>("customer").BindConfiguration("Smtp:Customer");

public sealed class EmailService(IOptionsSnapshot<SmtpOptions> options)
{
    public Task SendInternalEmailAsync(string to, string body)
    {
        var smtp = options.Get("internal");
        // ...
        return Task.CompletedTask;
    }
}
```

## Secrets

- Development: `dotnet user-secrets init`, then `dotnet user-secrets set "ConnectionStrings:DefaultConnection" "<value>"` in the Api project.
- Committed `appsettings.json` keeps structure and non-secret defaults only, for example `{ "Jwt": { "Key": "", "Issuer": "myapp", "Audience": "myapp" } }`.
- Deployed environments: environment variables (`ConnectionStrings__DefaultConnection`) or the managed secret store of the actual hosting platform. Azure Key Vault is one example; add Azure-specific dependencies only when the project actually uses Azure:

```csharp
if (builder.Environment.IsProduction())
{
    var keyVaultUri = new Uri(builder.Configuration["KeyVault:Uri"]!);
    builder.Configuration.AddAzureKeyVault(keyVaultUri, new DefaultAzureCredential());
}
```

## Typed options instead of scattered keys

```csharp
// Stringly typed and scattered configuration access
public sealed class PricingService(IConfiguration configuration)
{
    public decimal GetDiscount() => decimal.Parse(configuration["Pricing:DefaultDiscount"]!);
}

// Strongly typed options
public sealed class PricingService(IOptions<PricingOptions> options)
{
    public decimal GetDiscount() => options.Value.DefaultDiscount;
}
```

## Anti-patterns

Review checks; the named standard owns each rule:

- Services parsing string keys from `IConfiguration` instead of typed options? (`operations.md`)
- Secrets in `appsettings*.json` or other committed files? (`.claude/rules/common/security.md`)
- Required options without startup validation? (`operations.md`)

## Quick reference

| Scenario | Technique |
|---|---|
| Bind a section to a class | `AddOptions<T>().BindConfiguration(...)` |
| Simple, immutable configuration | `IOptions<T>` |
| Configuration that may change per request | `IOptionsSnapshot<T>` |
| Singleton or background service watching values | `IOptionsMonitor<T>` |
| Validate at startup | `ValidateDataAnnotations()` / `Validate(...)` + `ValidateOnStart()` |
| Several configurations of one type | Named options with `IOptionsSnapshot<T>.Get(name)` |
| Development secrets | `dotnet user-secrets` |
| Production secrets | Environment or platform secret injection, chosen managed secret store |
