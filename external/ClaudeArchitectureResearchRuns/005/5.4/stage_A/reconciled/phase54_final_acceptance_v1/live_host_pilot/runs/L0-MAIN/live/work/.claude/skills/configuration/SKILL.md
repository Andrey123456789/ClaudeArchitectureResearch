---
name: configuration
description: >
  Use for .NET configuration: appsettings, Options pattern, IOptions/Snapshot/Monitor,
  startup validation, user secrets, environment variables, connection strings.
---

> Level: 2 Technology · Owns: .NET configuration technique and examples (knowledge) · Scope: backend · Loads: on invocation · Depends on: .claude/rules/2-technology/csharp.md, .claude/rules/0-core/security-principles.md

# Configuration

Policy owners: typed options and startup validation → `.claude/rules/2-technology/csharp.md`; secrets → `0-core/security-principles.md`; required security configuration failing visibly → same file; local Development database → `3-project/data-lifecycle.md`; tunable product values → `CUSTOM_SETTINGS.md` (not runtime configuration). This skill is technique only.

Direct `IConfiguration` access is normal in `Program.cs`, configuration-provider setup, and infrastructure registration; the problem is ordinary services parsing configuration keys.

## Provider precedence

With the default ASP.NET Core host, later providers override earlier ones: `appsettings.json` → `appsettings.{Environment}.json` → user secrets (Development) → environment variables → command-line arguments. Custom providers follow their registration order.

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
    .ValidateOnStart();           // fails at startup instead of at first use
```

Numbers in examples are illustrative, not approved defaults; choose retry counts, timeouts, and limits from the actual integration and deployment.

## Injecting options

```csharp
public sealed class PricingService(IOptions<PricingOptions> options)          // stable value
public sealed class PricingService(IOptionsSnapshot<PricingOptions> options)  // refreshed per scope
public sealed class BackgroundWorker(IOptionsMonitor<WorkerOptions> options)  // observe changes
{
    public void DoWork() { var current = options.CurrentValue; }
}
```

## Custom validation

```csharp
builder.Services.AddOptions<JwtOptions>()
    .BindConfiguration("Jwt")
    .Validate(o => !string.IsNullOrEmpty(o.Authority), "Jwt:Authority is required")
    .ValidateOnStart();
```

## Secrets in practice

```bash
dotnet user-secrets init --project backend/MyApp.Api
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "<local value>" --project backend/MyApp.Api
```

`appsettings.json` keeps structure and non-secret defaults only:

```json
{
  "Jwt": { "Authority": "", "Audience": "myapp" },
  "ConnectionStrings": { "DefaultConnection": "" }
}
```

Deployed environments inject values through environment variables (`ConnectionStrings__DefaultConnection`) or the managed secret store of the actual host. Example of one managed provider — use it only when the project runs on Azure:

```csharp
if (builder.Environment.IsProduction())
{
    builder.Configuration.AddAzureKeyVault(
        new Uri(builder.Configuration["KeyVault:Uri"]!), new DefaultAzureCredential());
}
```

## Named options

```csharp
builder.Services.AddOptions<SmtpOptions>("internal").BindConfiguration("Smtp:Internal");
builder.Services.AddOptions<SmtpOptions>("customer").BindConfiguration("Smtp:Customer");

public sealed class EmailService(IOptionsSnapshot<SmtpOptions> options)
{
    public Task SendInternalAsync(string to, string body)
    {
        var smtp = options.Get("internal");
        // ...
        return Task.CompletedTask;
    }
}
```

## Anti-patterns

```csharp
// Avoid — stringly typed, scattered configuration access in a service
public sealed class PricingService(IConfiguration configuration)
{
    public decimal GetDiscount() => decimal.Parse(configuration["Pricing:DefaultDiscount"]!);
}

// Avoid — misconfiguration discovered only at runtime
builder.Services.Configure<JwtOptions>(builder.Configuration.GetSection("Jwt"));
```

## Decision guide

| Scenario | Technique |
|---|---|
| Bind a section to a class | `AddOptions<T>().BindConfiguration()` |
| Simple immutable configuration | `IOptions<T>` |
| Value that may change per request | `IOptionsSnapshot<T>` |
| Background service watching changes | `IOptionsMonitor<T>` |
| Development secrets | `dotnet user-secrets` |
| Production secrets | environment/platform injection or the chosen managed store |
| Validation | `ValidateDataAnnotations()` + `ValidateOnStart()` |
| Several configurations of one type | named options + `IOptionsSnapshot<T>.Get(name)` |
