> Owns: Serilog configuration technique (bootstrap, configuration, sinks, enrichers, request logging, LogContext, filtering) | Scope: backend | Loads: private reference of logging (read on demand by that skill only)

# Serilog — Configuration Technique

Registration style and configuration placement are governed by
`.claude/rules/error-handling.md` (Logging). Only the Console sink is part of the
local baseline; File, Seq, OpenTelemetry, Elasticsearch, and extra enrichers
below are optional examples, and numeric limits are illustrative, not approved
defaults.

## Host-Managed Setup (Simple Applications)

```csharp
builder.Services.AddSerilog((services, lc) => lc
    .ReadFrom.Configuration(builder.Configuration)
    .ReadFrom.Services(services)
    .Enrich.FromLogContext());
```

## Two-Stage Bootstrap (When Startup Logging Matters)

A bootstrap logger captures failures before DI and configuration exist.

```csharp
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Information)
    .Enrich.FromLogContext()
    .WriteTo.Console()
    .CreateBootstrapLogger();

try
{
    Log.Information("Starting application");
    var builder = WebApplication.CreateBuilder(args);

    builder.Services.AddSerilog((services, lc) => lc
        .ReadFrom.Configuration(builder.Configuration)
        .ReadFrom.Services(services)
        .Enrich.FromLogContext()
        .Enrich.WithProperty("Application", "MyApp.Api"));

    var app = builder.Build();
    app.UseSerilogRequestLogging();
    app.Run();
}
catch (Exception ex)
{
    Log.Fatal(ex, "Application terminated unexpectedly");
}
finally
{
    await Log.CloseAndFlushAsync();   // flush static/bootstrap logger, buffered sinks
}
```

For purely host-managed logging, rely on the provider's lifetime handling rather
than adding static lifecycle code.

## appsettings.json

```json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "Microsoft.AspNetCore": "Warning",
        "Microsoft.EntityFrameworkCore": "Warning",
        "Microsoft.Hosting.Lifetime": "Information",
        "System": "Warning"
      }
    },
    "WriteTo": [
      {
        "Name": "Console",
        "Args": {
          "outputTemplate": "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}"
        }
      }
    ],
    "Enrich": [ "FromLogContext" ],
    "Destructure": [
      { "Name": "ToMaximumDepth", "Args": { "maximumDestructuringDepth": 4 } },
      { "Name": "ToMaximumStringLength", "Args": { "maximumStringLength": 1024 } },
      { "Name": "ToMaximumCollectionCount", "Args": { "maximumCollectionCount": 10 } }
    ]
  }
}
```

Override keys are namespace prefixes matched against `SourceContext`; more
specific prefixes win. Optional sinks such as a rolling `File` sink
(`"path": "logs/app-.log", "rollingInterval": "Day"`) or `Seq`
(`"serverUrl": "http://localhost:5341"`) are added only when required.

## Request Logging

`UseSerilogRequestLogging` replaces per-request framework noise with one summary
event:

```csharp
app.UseSerilogRequestLogging(options =>
{
    options.MessageTemplate =
        "HTTP {RequestMethod} {RequestPath} responded {StatusCode} in {Elapsed:0.0000} ms";
    options.GetLevel = (httpContext, elapsed, ex) =>
        ex is not null || httpContext.Response.StatusCode >= 500
            ? LogEventLevel.Error
            : LogEventLevel.Information;
    options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
        diagnosticContext.Set("UserId",
            httpContext.User.FindFirstValue(ClaimTypes.NameIdentifier) ?? "anonymous");
});
```

## Destructuring

```csharp
logger.LogInformation("Processing {@SensorInput}", sensorInput); // structure preserved
logger.LogInformation("Received {$Data}", data);                  // forces ToString()

// Limit or shape destructuring rather than logging large graphs:
.Destructure.ToMaximumDepth(4)
.Destructure.ByTransforming<HttpRequest>(r => new { r.Method, r.Path })
```

## LogContext

```csharp
using (LogContext.PushProperty("CorrelationId", correlationId))
using (LogContext.PushProperty("TenantId", tenantId))
{
    logger.LogInformation("Processing order {OrderId}", orderId);
}
```

Requires `.Enrich.FromLogContext()`. Keep `LogContext` at composition/middleware
boundaries; application code stays on `ILogger<T>`.

## Optional Sinks and Filtering

```csharp
// OTLP export without the OpenTelemetry SDK (Serilog.Sinks.OpenTelemetry)
.WriteTo.OpenTelemetry(options =>
{
    options.Endpoint = "http://localhost:4317";
    options.Protocol = OtlpProtocol.Grpc;
    options.ResourceAttributes = new Dictionary<string, object> { ["service.name"] = "MyApp.Api" };
})

// Serilog.Expressions filtering
.Filter.ByExcluding("RequestPath like '/health%'")
.WriteTo.Conditional("@l = 'Error'", wt => wt.File("logs/errors-.log", rollingInterval: RollingInterval.Day))
```

Elasticsearch: the `Serilog.Sinks.Elasticsearch` package is deprecated; use the
official `Elastic.Serilog.Sinks` package (same `WriteTo.Elasticsearch` method
name, ECS documents to data streams).

## Decision Guide

| Scenario | Technique |
|---|---|
| Simple host-managed logging | `AddSerilog` + `ReadFrom.Configuration` |
| Startup failures must be captured | Two-stage bootstrap logger |
| Development log viewing | Console; Seq or Aspire Dashboard when useful |
| Request summaries | `UseSerilogRequestLogging()` |
| Scoped properties | `LogContext.PushProperty()` in middleware |
| Expression filtering | `Serilog.Expressions` |
| Per-environment levels | `MinimumLevel.Override` in configuration |
| Audit trails | `AuditTo` (synchronous; exceptions propagate) |
