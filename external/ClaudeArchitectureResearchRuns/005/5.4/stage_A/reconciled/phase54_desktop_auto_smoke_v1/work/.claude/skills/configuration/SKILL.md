---
name: configuration
description: Use when setting up or reviewing configuration — appsettings, Options pattern, IOptions/IOptionsSnapshot/IOptionsMonitor, startup validation, user secrets, environment variables, secret stores.
---

> Kind: KNW | Scope: backend | Owner: configuration and options technique with examples | Loading: on demand (model-invoked knowledge)

# Configuration

Rules: `rules/backend/hosting.md` § Configuration, `rules/common/security.md` § Secrets and § Failure behavior.

## Provider precedence

With the normal ASP.NET Core host, configuration commonly layers `appsettings.json`, `appsettings.{Environment}.json`, development user secrets, environment variables and command-line arguments, later providers overriding earlier ones. Custom providers follow their registration order. Where direct `IConfiguration` access belongs: `rules/backend/hosting.md` § Configuration.

## Options pattern

```csharp
public class DatabaseOptions
{
    public const string SectionName = "Database";

    [Required]
    public required string ConnectionString { get; init; }

    [Range(1, 100)]
    public int MaxRetryCount { get; init; } = 3;

    [Range(1, 60)]
    public int CommandTimeoutSeconds { get; init; } = 30;
}

builder.Services.AddOptions<DatabaseOptions>()
    .BindConfiguration(DatabaseOptions.SectionName)
    .ValidateDataAnnotations()
    .ValidateOnStart(); // fails at startup when configuration is invalid
```

```json
{
  "Database": {
    "ConnectionString": "",
    "MaxRetryCount": 3,
    "CommandTimeoutSeconds": 30
  }
}
```

Numbers in examples are illustrative; choose retry counts, timeouts and limits from the actual integration and deployment requirements.

## Injecting options

```csharp
// IOptions<T> — stable value
public sealed class PricingService(
    IOptions<PricingOptions> options)
{
    private readonly PricingOptions _pricing = options.Value;
}

// IOptionsSnapshot<T> — refreshed for each scope
public sealed class PricingService(
    IOptionsSnapshot<PricingOptions> options)
{
    private readonly PricingOptions _pricing = options.Value;
}

// IOptionsMonitor<T> — observes current values over time
public sealed class BackgroundWorker(
    IOptionsMonitor<WorkerOptions> options)
{
    public void DoWork()
    {
        var current = options.CurrentValue;
    }
}
```

## Custom validation

```csharp
builder.Services.AddOptions<JwtOptions>()
    .BindConfiguration("Jwt")
    .Validate(options =>
    {
        if (string.IsNullOrEmpty(options.Key) || options.Key.Length < 32)
            return false;
        if (options.ExpirationMinutes <= 0)
            return false;
        return true;
    }, "JWT key must be at least 32 characters and expiration must be positive")
    .ValidateOnStart();
```

`Configure<T>(section)` without validation only discovers misconfiguration at runtime; `AddOptions<T>().BindConfiguration(...).ValidateOnStart()` fails fast.

## Named options

```csharp
builder.Services.AddOptions<SmtpOptions>("internal")
    .BindConfiguration("Smtp:Internal");
builder.Services.AddOptions<SmtpOptions>("customer")
    .BindConfiguration("Smtp:Customer");

public class EmailService(IOptionsSnapshot<SmtpOptions> options)
{
    public async Task SendInternalEmail(string to, string body)
    {
        var smtp = options.Get("internal");
        // ...
    }
}
```

## Typed access instead of string lookups

```csharp
// Stringly typed and scattered
public sealed class PricingService(IConfiguration configuration)
{
    public decimal GetDiscount()
    {
        return decimal.Parse(
            configuration["Pricing:DefaultDiscount"]!);
    }
}

// Strongly typed
public sealed class PricingService(
    IOptions<PricingOptions> options)
{
    public decimal GetDiscount()
    {
        return options.Value.DefaultDiscount;
    }
}
```

## Secrets

`appsettings.json` holds structure and non-secret defaults (`rules/common/security.md` § Secrets); values come from user-secrets in development and from environment variables or a managed store in deployed environments:

```json
{
  "Jwt": { "Key": "", "Issuer": "myapp", "Audience": "myapp" },
  "Database": { "ConnectionString": "" }
}
```

Azure Key Vault is one possible managed provider — add Azure-specific packages only when the project actually runs on Azure:

```csharp
if (builder.Environment.IsProduction())
{
    var keyVaultUri = new Uri(builder.Configuration["KeyVault:Uri"]!);
    builder.Configuration.AddAzureKeyVault(keyVaultUri, new DefaultAzureCredential());
}
```

## Decision guide

| Scenario | Technique |
|---|---|
| Binding configuration to a class | Options pattern with `BindConfiguration` |
| Simple immutable configuration | `IOptions<T>` |
| Configuration that changes per request | `IOptionsSnapshot<T>` |
| Background service watching configuration | `IOptionsMonitor<T>` |
| Development secrets | `dotnet user-secrets` |
| Deployed secrets | Environment/platform injection or chosen managed store |
| Validating configuration | `ValidateDataAnnotations()` + `ValidateOnStart()` |
| Several configurations of one type | Named options with `IOptionsSnapshot<T>.Get(name)` |
