> Level: 2-technology | Owns: Serilog provider technique (skill-private reference of logging) | Scope: backend | Loads: read by the logging skill only

# Serilog

Serilog is the approved logging provider (project stack); application code
still logs through `ILogger<T>`.

## Principles

1. Two-stage initialization when startup logging matters: a bootstrap logger
   captures failures before DI and configuration exist. Simple applications may
   use host-managed setup without bootstrap logging.
2. `builder.Services.AddSerilog(...)` (integrates with DI via
   `ReadFrom.Services`) instead of `builder.Host.UseSerilog()`.
3. Message templates, not interpolation.
4. Levels, sinks, and overrides live in `appsettings*.json` so they vary per
   environment without redeployment.
5. Keep `Log.Logger` and `LogContext` at composition/provider boundaries.

## Two-stage bootstrap

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
        .Enrich.FromLogContext()
        .Enrich.WithMachineName()          // Serilog.Enrichers.Environment, only if needed
        .Enrich.WithEnvironmentName()
        .Enrich.WithProperty("Application", "MyApp"));

    var app = builder.Build();

    app.UseSerilogRequestLogging(options =>
    {
        options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
        {
            diagnosticContext.Set("RequestHost", httpContext.Request.Host.Value);
            diagnosticContext.Set("UserAgent", httpContext.Request.Headers.UserAgent.ToString());
        };
    });

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

When the static/bootstrap `Log.Logger` is used, flush it on shutdown (as above)
so buffered events are written; purely host-managed logging follows the
provider's lifetime instead.

## Configuration

Configure only the sinks and enrichers the project needs; a Console sink is
enough for a simple local Development baseline. The File/Seq entries and
numeric limits below are illustrative, not approved defaults.

```json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "Microsoft.AspNetCore": "Warning",
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
      },
      { "Name": "File", "Args": { "path": "logs/app-.log", "rollingInterval": "Day" } },
      { "Name": "Seq", "Args": { "serverUrl": "http://localhost:5341" } }
    ],
    "Enrich": ["FromLogContext"],
    "Destructure": [
      { "Name": "ToMaximumDepth", "Args": { "maximumDestructuringDepth": 4 } },
      { "Name": "ToMaximumStringLength", "Args": { "maximumStringLength": 1024 } },
      { "Name": "ToMaximumCollectionCount", "Args": { "maximumCollectionCount": 10 } }
    ]
  }
}
```

`Override` keys are namespace prefixes matched against `SourceContext`; more
specific prefixes win.

## Request logging

```csharp
app.UseSerilogRequestLogging(options =>
{
    options.MessageTemplate =
        "HTTP {RequestMethod} {RequestPath} responded {StatusCode} in {Elapsed:0.0000} ms";

    options.GetLevel = (httpContext, elapsed, ex) =>
        ex is not null || httpContext.Response.StatusCode >= 500
            ? LogEventLevel.Error
            : LogEventLevel.Information;
});
```

One summary event per request replaces the framework's per-request noise.

## Destructuring and LogContext

```csharp
logger.LogInformation("Processing {@SensorInput}", sensorInput); // @ keeps structure
logger.LogInformation("Received {$Data}", data);                  // $ forces ToString()

using (LogContext.PushProperty("CorrelationId", correlationId))
{
    logger.LogInformation("Processing order {OrderId}", orderId);
}
```

`LogContext` requires `.Enrich.FromLogContext()`. Limit destructuring depth,
string length, and collection count, or destructure to selected properties
(`.Destructure.ByTransforming<HttpRequest>(r => new { r.Method, r.Path })`)
instead of whole request objects.

## Optional integrations

Every extra package follows `add-dependency`.

```csharp
// Serilog.Expressions — expression-based filtering and conditional sinks
.Filter.ByExcluding("RequestPath like '/health%'")
.WriteTo.Conditional("@l = 'Error'",
    wt => wt.File("logs/errors-.log", rollingInterval: RollingInterval.Day))

// Serilog.Sinks.OpenTelemetry — OTLP export without the OpenTelemetry SDK
.WriteTo.OpenTelemetry(options =>
{
    options.Endpoint = "http://localhost:4317";
    options.Protocol = OtlpProtocol.Grpc;
    options.ResourceAttributes = new Dictionary<string, object>
    {
        ["service.name"] = "MyApp",
        ["deployment.environment"] = "production"
    };
})

// Elasticsearch: Elastic.Serilog.Sinks (the Serilog.Sinks.Elasticsearch package is deprecated)
.WriteTo.Elasticsearch([new Uri("https://elastic.example.com:9200")], opts =>
    opts.DataStream = new DataStreamName("logs", "myapp"))
```

## Decision guide

| Scenario | Recommendation |
|---|---|
| Provider registration | `AddSerilog()` + configuration |
| General application logging API | `ILogger<T>` (logging skill) |
| Log storage, development | Seq (free single-user) or the Aspire dashboard |
| Log storage, production | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
| Request logging | `UseSerilogRequestLogging()` |
| Scoped properties | `LogContext.PushProperty()` in middleware |
| Filtering | `Serilog.Expressions` |
| High-volume paths | `[LoggerMessage]` source generator |
| Audit trails | `AuditTo` (synchronous; exceptions propagate) |
| Levels per environment | `MinimumLevel.Override` per namespace in appsettings |
