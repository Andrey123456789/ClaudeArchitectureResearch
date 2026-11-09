---
name: configuration
description: >
  Use for configuration: appsettings, Options pattern,
  IOptions/IOptionsSnapshot/IOptionsMonitor, ValidateOnStart, user-secrets,
  environment variables, secret stores.
---
> Level: 2-technology | Owns: configuration and secrets technique | Scope: backend | Loads: on demand (skill)

# Configuration

Policy: `hosting.md` (typed options, startup validation), `security.md`
(secrets).

## Provider precedence

With the default ASP.NET Core host, later providers override earlier ones:
`appsettings.json` → `appsettings.{Environment}.json` → user secrets
(Development) → environment variables → command-line arguments. Custom
providers follow their registration order.

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

Numeric values in examples are illustrative, not approved defaults; choose
retry counts, timeouts, and limits from the actual integration and deployment
requirements.

## Choosing the options interface

```csharp
// IOptions<T> — stable configuration value
public sealed class PricingService(IOptions<PricingOptions> options)
{
    private readonly PricingOptions _pricing = options.Value;
}

// IOptionsSnapshot<T> — recomputed for each created scope
public sealed class QuoteService(IOptionsSnapshot<PricingOptions> options)
{
    private readonly PricingOptions _pricing = options.Value;
}

// IOptionsMonitor<T> — observe current values over time (singletons, workers)
public sealed class BackgroundWorker(IOptionsMonitor<WorkerOptions> options)
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
    .Validate(o => !string.IsNullOrEmpty(o.Key) && o.ExpirationMinutes > 0,
        "JWT key is required and expiration must be positive")
    .ValidateOnStart();
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

## Secrets

- Development: `dotnet user-secrets init`, then
  `dotnet user-secrets set "ConnectionStrings:DefaultConnection" "<value>"`.
- Deployed environments: environment-specific injection
  (`ConnectionStrings__DefaultConnection`) or the managed secret store of the
  chosen host. Azure Key Vault is one example — add a provider-specific package
  only when the project actually uses that platform:

```csharp
if (builder.Environment.IsProduction())
{
    builder.Configuration.AddAzureKeyVault(
        new Uri(builder.Configuration["KeyVault:Uri"]!),
        new DefaultAzureCredential());
}
```

Committed files keep structure and non-secret defaults only:

```json
{
  "Jwt": { "Key": "", "Issuer": "myapp", "Audience": "myapp" },
  "ConnectionStrings": { "DefaultConnection": "" }
}
```

## Anti-patterns

```csharp
// String-keyed parsing inside an ordinary service
public sealed class PricingService(IConfiguration configuration)
{
    public decimal GetDiscount()
        => decimal.Parse(configuration["Pricing:DefaultDiscount"]!);
}

// Binding without validation — misconfiguration surfaces at runtime
builder.Services.Configure<JwtOptions>(builder.Configuration.GetSection("Jwt"));
```

## Decision guide

| Scenario | Recommendation |
|---|---|
| Bind a section to a class | `AddOptions<T>().BindConfiguration(...)` |
| Simple immutable configuration | `IOptions<T>` |
| Value that can change per request | `IOptionsSnapshot<T>` |
| Long-running service watching changes | `IOptionsMonitor<T>` |
| Development secrets | `dotnet user-secrets` |
| Production secrets | Platform injection or the chosen managed store |
| Validation | `ValidateDataAnnotations()` + `ValidateOnStart()` |
| Several configurations of one type | Named options |
