> Level: 2 Technology · Owns: Serilog configuration technique (private reference of `logging`) · Scope: backend · Loads: read by `logging` only

# Serilog

Integration policy: `.claude/rules/2-technology/aspnet-core.md` (Host composition). Application code keeps using `ILogger<T>`; direct Serilog APIs (`Log.Logger`, `LogContext`) stay at composition or provider-specific boundaries.

## Host setup

Two-stage initialization captures startup failures before configuration and DI are available. Simpler applications may use host-managed setup alone.

```csharp
using Serilog;

Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Information)
    .Enrich.FromLogContext()
    .WriteTo.Console()
    .CreateBootstrapLogger();                         // stage 1: bootstrap logger

try
{
    Log.Information("Starting application");

    var builder = WebApplication.CreateBuilder(args);

    builder.Services.AddSerilog((services, lc) => lc  // stage 2: full logger with DI and configuration
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
    await Log.CloseAndFlushAsync();                   // flush buffered events of the static logger
}
```

`WithMachineName`/`WithEnvironmentName` enrichers need `Serilog.Enrichers.Environment`; add enrichers and sinks only when the project needs them.

## Configuration (appsettings)

Only the Console sink is a local baseline. File, Seq, OpenTelemetry or Elasticsearch sinks are optional; numeric limits below are illustrative, not approved defaults.

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

`Override` keys are namespace prefixes matched against `SourceContext`; more specific prefixes win.

## Request logging

`UseSerilogRequestLogging` replaces several per-request framework events with one summary event:

```csharp
app.UseSerilogRequestLogging(options =>
{
    options.MessageTemplate = "HTTP {RequestMethod} {RequestPath} responded {StatusCode} in {Elapsed:0.0000} ms";
    options.GetLevel = (httpContext, elapsed, ex) =>
        ex is not null || httpContext.Response.StatusCode >= 500
            ? LogEventLevel.Error
            : LogEventLevel.Information;
    options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
        diagnosticContext.Set("UserId",
            httpContext.User.FindFirstValue(ClaimTypes.NameIdentifier) ?? "anonymous");
});
```

## Destructuring and LogContext

```csharp
logger.LogInformation("Processing {@SensorInput}", sensorInput);   // @ keeps structure
logger.LogInformation("Received {$Data}", data);                    // $ forces ToString()

using (LogContext.PushProperty("TenantId", tenantId))               // requires Enrich.FromLogContext()
{
    logger.LogInformation("Processing order {OrderId}", orderId);
}
```

Destructure specific shapes instead of whole framework objects: `.Destructure.ByTransforming<HttpRequest>(r => new { r.Method, r.Path })`.

## Optional sinks and filters

```csharp
.WriteTo.OpenTelemetry(options =>                                   // Serilog.Sinks.OpenTelemetry
{
    options.Endpoint = "http://localhost:4317";
    options.Protocol = OtlpProtocol.Grpc;
})

.Filter.ByExcluding("RequestPath like '/health%'")                  // Serilog.Expressions
.WriteTo.Conditional("@l = 'Error'", wt => wt.File("logs/errors-.log", rollingInterval: RollingInterval.Day))
```

The `Serilog.Sinks.Elasticsearch` package is deprecated; Elasticsearch output uses `Elastic.Serilog.Sinks`:

```csharp
.WriteTo.Elasticsearch([new Uri("https://elastic.example.com:9200")], opts =>
    opts.DataStream = new DataStreamName("logs", "myapp"))
```

## Decision guide

| Scenario | Typical choice |
|---|---|
| Register the provider | `builder.Services.AddSerilog(...)` + configuration |
| Local development storage | Console; Seq or the Aspire dashboard when useful |
| Production storage | Seq, Elasticsearch (`Elastic.Serilog.Sinks`) or an OTLP backend |
| Request logging | `UseSerilogRequestLogging()` |
| Scoped properties | `LogContext.PushProperty` (often in middleware) |
| Expression filtering | `Serilog.Expressions` |
| Audit trail | `AuditTo` (synchronous, exceptions propagate) — only with an adopted audit design |
| Levels per environment | `MinimumLevel.Override` in environment-specific appsettings |
