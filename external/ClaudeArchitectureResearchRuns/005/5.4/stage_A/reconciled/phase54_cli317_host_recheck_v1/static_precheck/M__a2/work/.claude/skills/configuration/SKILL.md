---
name: configuration
description: >
  Use when binding or validating configuration: appsettings, Options pattern,
  ValidateOnStart, named options, user-secrets, environment variables,
  connection strings, secret providers.
---

> Owns: configuration technique and examples (no policy) | Scope: backend | Loads: on demand (knowledge skill)

# Configuration

Policy owners: typed options and startup validation —
`.claude/rules/architecture.md` § Composition and Dependency Injection; secrets —
`.claude/rules/security.md`; local Development database configuration —
`.claude/rules/persistence.md`.

## Where IConfiguration Belongs

Direct `IConfiguration` access is normal in the composition root,
configuration-provider setup, and infrastructure registration; ordinary
application services receive typed options instead.

## Provider Precedence

With the normal ASP.NET Core host, configuration layers `appsettings.json`,
`appsettings.{Environment}.json`, development user secrets, environment
variables, and command-line arguments, with later providers overriding earlier
ones. Custom providers follow their registration order.

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
    .ValidateOnStart(); // fails at startup if configuration is invalid
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

Numeric values in examples are illustrative, not approved defaults. Choose retry
counts, timeouts, limits, and similar operational values from the actual
integration and deployment requirements.

## Injecting Options

```csharp
// IOptions<T> - stable configuration value
public sealed class PricingService(
    IOptions<PricingOptions> options)
{
    private readonly PricingOptions _pricing = options.Value;
}

// IOptionsSnapshot<T> - refreshed for each created scope
public sealed class PricingService(
    IOptionsSnapshot<PricingOptions> options)
{
    private readonly PricingOptions _pricing = options.Value;
}

// IOptionsMonitor<T> - observe current values over time
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

Azure Key Vault is one possible managed secret provider; use the provider that
matches the hosting environment and add Azure-specific dependencies only when
the project actually uses Azure.

```csharp
// Program.cs - add Key Vault as a configuration source
if (builder.Environment.IsProduction())
{
    var keyVaultUri = new Uri(builder.Configuration["KeyVault:Uri"]!);
    builder.Configuration.AddAzureKeyVault(keyVaultUri, new DefaultAzureCredential());
}
```

## Named Options

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

## Examples of What to Avoid

```csharp
// BAD - stringly typed configuration access inside a service
public sealed class PricingService(IConfiguration configuration)
{
    public decimal GetDiscount()
    {
        return decimal.Parse(
            configuration["Pricing:DefaultDiscount"]!);
    }
}

// GOOD - strongly typed options
public sealed class PricingService(
    IOptions<PricingOptions> options)
{
    public decimal GetDiscount()
    {
        return options.Value.DefaultDiscount;
    }
}
```

```json
// BAD - secrets committed to source control
{
  "Jwt": { "Key": "super-secret-key" },
  "Database": { "ConnectionString": "Server=prod;Password=secret" }
}

// GOOD - appsettings.json holds defaults and structure only
{
  "Jwt": { "Key": "", "Issuer": "myapp", "Audience": "myapp" },
  "Database": { "ConnectionString": "" }
}
// Secrets come from user-secrets (development) or environment
// variables / a managed secret store (deployed environments).
```

```csharp
// BAD - misconfiguration discovered at runtime
builder.Services.Configure<JwtOptions>(builder.Configuration.GetSection("Jwt"));

// GOOD - fail fast at startup
builder.Services.AddOptions<JwtOptions>()
    .BindConfiguration("Jwt")
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

## Decision Guide

| Scenario | Recommendation |
|----------|---------------|
| Binding config to a class | Options pattern with `BindConfiguration` |
| Simple, immutable config | `IOptions<T>` |
| Config that changes per request | `IOptionsSnapshot<T>` |
| Background service watching config | `IOptionsMonitor<T>` |
| Development secrets | `dotnet user-secrets` |
| Production secrets | Environment/platform secret injection or chosen managed store |
| Validating config | `ValidateDataAnnotations()` + `ValidateOnStart()` |
| Multiple configs of the same type | Named options with `IOptionsSnapshot<T>.Get(name)` |
