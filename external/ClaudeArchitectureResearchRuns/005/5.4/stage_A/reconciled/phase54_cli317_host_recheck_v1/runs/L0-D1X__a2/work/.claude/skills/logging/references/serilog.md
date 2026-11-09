> Level: 2 Technology · Owns: Serilog configuration technique (private reference of `logging`) · Scope: backend · Loads: read by `logging` only · Depends on: .claude/skills/logging/SKILL.md

# Serilog

Integration policy (DI-integrated `AddSerilog`, environment-aware configuration, application code on `ILogger<T>`) is owned by `.claude/rules/2-technology/logging.md`; the baseline package and sink choice by `3-project/decisions.md`. This reference is technique.

## Host setup

Use two-stage initialization when startup logging matters: a bootstrap logger captures failures before DI/configuration is available. Simpler applications may use host-managed setup without bootstrap logging.

```csharp
using Serilog;

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
        .Enrich.FromLogContext());

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
    await Log.CloseAndFlushAsync();
}
```

When the static/bootstrap `Log.Logger` is used, flush it on shutdown (as above) so buffered events — especially from async sinks such as Seq or OTLP — are written. With purely host-managed logging, follow the provider's lifetime instead of adding static lifecycle code.

## Configuration

An example `appsettings*.json` section. It deliberately shows several optional sinks; File, Seq, OpenTelemetry, and Elasticsearch are not baseline dependencies, and the numbers are illustrative, not approved defaults:

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
      { "Name": "Console", "Args": { "outputTemplate": "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}" } },
      { "Name": "File", "Args": { "path": "logs/app-.log", "rollingInterval": "Day", "retainedFileCountLimit": 30 } },
      { "Name": "Seq", "Args": { "serverUrl": "http://localhost:5341" } }
    ],
    "Enrich": ["FromLogContext", "WithMachineName", "WithEnvironmentName"],
    "Destructure": [
      { "Name": "ToMaximumDepth", "Args": { "maximumDestructuringDepth": 4 } },
      { "Name": "ToMaximumStringLength", "Args": { "maximumStringLength": 1024 } },
      { "Name": "ToMaximumCollectionCount", "Args": { "maximumCollectionCount": 10 } }
    ]
  }
}
```

`Override` keys are namespace prefixes matched against `SourceContext`; more specific prefixes win.

## Request logging

`UseSerilogRequestLogging()` replaces ASP.NET Core's per-request events with one summary event:

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
        diagnosticContext.Set("RequestHost", httpContext.Request.Host.Value);
});
```

## Destructuring and LogContext

```csharp
logger.LogInformation("Processing {@SensorInput}", sensorInput);   // @ keeps structure
logger.LogInformation("Received {$Data}", new[] { 1, 2, 3 });       // $ forces ToString()

using (LogContext.PushProperty("CorrelationId", correlationId))
{
    logger.LogInformation("Processing order {OrderId}", orderId);
}
```

`LogContext` requires `.Enrich.FromLogContext()`. Keep `Log.Logger` and `LogContext` at composition/provider-specific boundaries. Avoid destructuring large graphs such as `HttpRequest`; configure destructuring limits or transform to specific properties (`.Destructure.ByTransforming<HttpRequest>(r => new { r.Method, r.Path })`).

## Optional integrations

OTLP export with `Serilog.Sinks.OpenTelemetry` (no OpenTelemetry SDK dependency):

```csharp
.WriteTo.OpenTelemetry(options =>
{
    options.Endpoint = "http://localhost:4317";
    options.Protocol = OtlpProtocol.Grpc;
    options.ResourceAttributes = new Dictionary<string, object>
    {
        ["service.name"] = "MyApp.Api",
        ["deployment.environment"] = "production"
    };
})
```

Expression-based filtering with `Serilog.Expressions`:

```csharp
// Exclude health-check noise
.Filter.ByExcluding("RequestPath like '/health%'")

// Route errors to a separate file
.WriteTo.Conditional("@l = 'Error'",
    wt => wt.File("logs/errors-.log", rollingInterval: RollingInterval.Day))
```

Elasticsearch: the `Serilog.Sinks.Elasticsearch` package is deprecated; the official `Elastic.Serilog.Sinks` package uses the same method name and writes ECS-formatted documents to data streams:

```csharp
// <PackageReference Include="Elastic.Serilog.Sinks" />
.WriteTo.Elasticsearch([new Uri("https://elastic.example.com:9200")], opts =>
    opts.DataStream = new DataStreamName("logs", "myapp"))
```

Audit trails that must not lose events can use `AuditTo` (synchronous; exceptions propagate).

## Decision guide

| Scenario | Technique |
|---|---|
| Serilog as provider | `AddSerilog()` + configuration |
| Development log storage | Seq or the Aspire Dashboard |
| Production log storage | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
| Request logging | `UseSerilogRequestLogging()` |
| Scoped properties | `LogContext.PushProperty()` in middleware |
| Level per environment | `MinimumLevel.Override` in appsettings |
