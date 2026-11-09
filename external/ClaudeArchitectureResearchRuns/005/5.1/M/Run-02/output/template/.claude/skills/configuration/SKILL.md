---
name: configuration
description: >
  Use when binding or validating configuration: appsettings layering,
  IOptions/IOptionsSnapshot/IOptionsMonitor, ValidateOnStart, named options,
  connection strings, user-secrets, environment variables, managed secret
  providers.
---

> Owner: configuration and options technique (normative policy lives in rules) | Scope: backend | Loads: on demand — knowledge | Enforced: none

# Configuration

Policy: `.claude/rules/coding-style.md` § Configuration (typed options, startup
validation), `.claude/rules/security.md` § Secrets and § Failure Behavior.

## Provider Precedence

With the normal ASP.NET Core host, configuration layers `appsettings.json`,
`appsettings.{Environment}.json`, user secrets (Development), environment
variables, and command-line arguments; later providers override earlier ones.
Custom providers follow their registration order. Environment variables use `__`
for nesting (`ConnectionStrings__DefaultConnection`).

## Options Pattern

```csharp
public sealed class DatabaseOptions
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
    .ValidateOnStart(); // fails at startup if configuration is invalid
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

Numbers in examples are illustrative, not approved defaults; choose retry counts,
timeouts, and limits from the actual integration and deployment requirements.
Product-level tunable values belong in `CUSTOM_SETTINGS.md`, not here.

## Injecting Options

```csharp
// IOptions<T> — stable configuration value
public sealed class PricingService(
    IOptions<PricingOptions> options)
{
    private readonly PricingOptions _pricing = options.Value;
}

// IOptionsSnapshot<T> — recomputed for each created scope
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

## Custom Validation

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

For larger rule sets, implement `IValidateOptions<T>`.

## Named Options

```csharp
builder.Services.AddOptions<SmtpOptions>("internal")
    .BindConfiguration("Smtp:Internal");
builder.Services.AddOptions<SmtpOptions>("customer")
    .BindConfiguration("Smtp:Customer");

public sealed class EmailService(IOptionsSnapshot<SmtpOptions> options)
{
    public async Task SendInternalEmailAsync(string to, string body)
    {
        var smtp = options.Get("internal");
        // ...
    }
}
```

## Secrets

Development:

```bash
dotnet user-secrets init --project backend/MyApp.Api
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "<value>" --project backend/MyApp.Api
```

Deployed environments: environment-specific secret injection or the managed
secret store of the chosen platform. Azure Key Vault is one example; add
provider-specific packages only when the project uses that platform:

```csharp
if (builder.Environment.IsProduction())
{
    var keyVaultUri = new Uri(builder.Configuration["KeyVault:Uri"]!);
    builder.Configuration.AddAzureKeyVault(keyVaultUri, new DefaultAzureCredential());
}
```

Committed `appsettings.json` holds structure and non-secret defaults only:

```json
{
  "Jwt": { "Key": "", "Issuer": "myapp", "Audience": "myapp" },
  "Database": { "ConnectionString": "" }
}
```

## Where IConfiguration Belongs

Direct `IConfiguration` access is normal in `Program.cs`, composition code, and
infrastructure registration. The problem is ordinary services depending on keys
and parsing:

```csharp
// Avoid — stringly typed, scattered access
public sealed class PricingService(IConfiguration configuration)
{
    public decimal GetDiscount()
    {
        return decimal.Parse(
            configuration["Pricing:DefaultDiscount"]!);
    }
}

// Prefer — strongly typed options
public sealed class PricingService(
    IOptions<PricingOptions> options)
{
    public decimal GetDiscount()
    {
        return options.Value.DefaultDiscount;
    }
}
```

## Startup Validation

```csharp
// Misconfiguration discovered only at runtime
builder.Services.Configure<JwtOptions>(builder.Configuration.GetSection("Jwt"));

// Fails fast at startup
builder.Services.AddOptions<JwtOptions>()
    .BindConfiguration("Jwt")
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

## Decision Guide

| Scenario | Technique |
|---|---|
| Binding config to a class | Options pattern with `BindConfiguration` |
| Simple, immutable config | `IOptions<T>` |
| Config that may change per request | `IOptionsSnapshot<T>` |
| Background service watching config | `IOptionsMonitor<T>` |
| Development secrets | `dotnet user-secrets` |
| Production secrets | Platform secret injection or the chosen managed store |
| Validating config | `ValidateDataAnnotations()` + `ValidateOnStart()` |
| Several configs of one type | Named options with `IOptionsSnapshot<T>.Get(name)` |
