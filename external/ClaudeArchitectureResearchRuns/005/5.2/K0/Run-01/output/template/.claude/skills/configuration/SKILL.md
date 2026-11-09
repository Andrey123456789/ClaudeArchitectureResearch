---
name: configuration
description: Use when setting up or reviewing application configuration — appsettings, the Options pattern, IOptions/IOptionsSnapshot/IOptionsMonitor, startup validation, user secrets, environment variables, connection strings, managed secret providers, named options.
---
<!-- Kind: KNW | Scope: backend | Owns: .NET configuration technique and examples | Loads: on demand (model-invoked) -->
# Configuration

Standards: `rules/backend/operations.md` § Configuration (typed options, startup validation, local Development connection string) and `rules/common/security.md` § Secrets.

## Provider Precedence

With the normal ASP.NET Core host, configuration commonly layers `appsettings.json`, `appsettings.{Environment}.json`, Development user secrets, environment variables and command-line arguments, later providers overriding earlier ones. Custom providers follow their registration order.

## Options Pattern

```csharp
// Options class with validation attributes
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

// Registration with validation
builder.Services.AddOptions<DatabaseOptions>()
    .BindConfiguration(DatabaseOptions.SectionName)
    .ValidateDataAnnotations()
    .ValidateOnStart(); // Fails at startup if configuration is invalid
```

```json
// appsettings.json
{
  "Database": {
    "ConnectionString": "",
    "MaxRetryCount": 3,
    "CommandTimeoutSeconds": 30
  }
}
```

Numeric values in examples are illustrative, not approved defaults: choose retry counts, timeouts and limits from the actual integration and deployment requirements.

## Injecting Options

```csharp
// IOptions<T> — stable configuration value
public sealed class PricingService(
    IOptions<PricingOptions> options)
{
    private readonly PricingOptions _pricing = options.Value;
}

// IOptionsSnapshot<T> — refreshed for each created scope
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

## Custom Validation (Complex Rules)

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

## External Secret Provider Example: Azure Key Vault

Azure Key Vault is one possible managed secret provider; use the provider that matches the hosting environment, and add Azure-specific dependencies only when the project uses Azure.

```csharp
// Program.cs — add Key Vault as a configuration source
if (builder.Environment.IsProduction())
{
    var keyVaultUri = new Uri(builder.Configuration["KeyVault:Uri"]!);
    builder.Configuration.AddAzureKeyVault(keyVaultUri, new DefaultAzureCredential());
}
```

## Configuration for Multiple Environments

```csharp
// Named options — different configuration per named instance
builder.Services.AddOptions<SmtpOptions>("internal")
    .BindConfiguration("Smtp:Internal");
builder.Services.AddOptions<SmtpOptions>("customer")
    .BindConfiguration("Smtp:Customer");

// Usage
public class EmailService(IOptionsSnapshot<SmtpOptions> options)
{
    public async Task SendInternalEmail(string to, string body)
    {
        var smtp = options.Get("internal");
        // ...
    }
}
```

## Anti-Patterns

### String-Based IConfiguration Access in Services

```csharp
// BAD — stringly typed and scattered configuration access
public sealed class PricingService(IConfiguration configuration)
{
    public decimal GetDiscount()
    {
        return decimal.Parse(
            configuration["Pricing:DefaultDiscount"]!);
    }
}

// GOOD — strongly typed options
public sealed class PricingService(
    IOptions<PricingOptions> options)
{
    public decimal GetDiscount()
    {
        return options.Value.DefaultDiscount;
    }
}
```

### Secrets in appsettings.json

```json
// BAD — committed to source control
{
  "Jwt": { "Key": "super-secret-key" },
  "Database": { "ConnectionString": "Server=prod;Password=secret" }
}

// GOOD — appsettings.json has defaults/structure only
{
  "Jwt": { "Key": "", "Issuer": "myapp", "Audience": "myapp" },
  "Database": { "ConnectionString": "" }
}
// Secrets come from user-secrets (dev) or environment variables / a secret store (deployed)
```

### Skipping Startup Validation

```csharp
// BAD — misconfiguration discovered at runtime
builder.Services.Configure<JwtOptions>(builder.Configuration.GetSection("Jwt"));

// GOOD — fail fast at startup
builder.Services.AddOptions<JwtOptions>()
    .BindConfiguration("Jwt")
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

## Decision Guide

| Scenario | Recommendation |
|---|---|
| Binding configuration to a class | Options pattern with `BindConfiguration` |
| Simple, immutable configuration | `IOptions<T>` |
| Configuration that changes per request | `IOptionsSnapshot<T>` |
| Background service watching configuration | `IOptionsMonitor<T>` |
| Development secrets | `dotnet user-secrets` |
| Production secrets | Environment/platform secret injection or the chosen managed secret store |
| Validating configuration | `ValidateDataAnnotations()` + `ValidateOnStart()` |
| Several configurations of the same type | Named options with `IOptionsSnapshot<T>.Get(name)` |
