> Level: 2 Technology | Owns: Serilog configuration technique (private to `logging`) | Scope: backend | Loads: on demand by `logging` | Depends on: 2-technology/logging.md

# Serilog

Sinks, enrichers, and numeric limits below are illustrative; configure only
what the project needs. A Console sink is enough for a simple local Development
baseline. File, Seq, OpenTelemetry, and Elasticsearch sinks are not baseline
dependencies.

## Host Setup

Simple applications use host-managed setup:

```csharp
builder.Services.AddSerilog((services, lc) => lc
    .ReadFrom.Configuration(builder.Configuration)
    .ReadFrom.Services(services)
    .Enrich.FromLogContext());
```

Use two-stage bootstrap when startup failures must be captured before DI and
configuration are available:

```csharp
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Information)
    .Enrich.FromLogContext()
    .WriteTo.Console()
    .CreateBootstrapLogger();

try
{
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
    await Log.CloseAndFlushAsync();   // flush buffered async sinks
}
```

`AddSerilog()` replaces the older `builder.Host.UseSerilog()`.

## Configuration

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
      { "Name": "Console",
        "Args": { "outputTemplate": "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}" } }
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

`Override` keys are namespace prefixes matched against `SourceContext`; more
specific prefixes win.

## Request Logging

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

Replaces several per-request framework events with one summary event.

## Destructuring and LogContext

```csharp
logger.LogInformation("Processing {@SensorInput}", sensorInput);   // structure preserved
logger.LogInformation("Received {$Data}", data);                    // ToString()

using (LogContext.PushProperty("TenantId", tenantId))               // needs Enrich.FromLogContext()
{
    logger.LogInformation("Processing order {OrderId}", orderId);
}
```

Prefer `.Destructure.ByTransforming<HttpRequest>(r => new { r.Method, r.Path })`
or explicit properties over destructuring large graphs. Keep `Log.Logger` and
`LogContext` at composition or provider-specific boundaries.

## Optional Sinks and Filtering

- OTLP export: `Serilog.Sinks.OpenTelemetry` (`.WriteTo.OpenTelemetry(...)`).
- Elasticsearch: use `Elastic.Serilog.Sinks`; the `Serilog.Sinks.Elasticsearch`
  package is deprecated.
- `Serilog.Expressions` filtering, e.g.
  `.Filter.ByExcluding("RequestPath like '/health%'")`.
- Audit trails: `AuditTo` (synchronous; exceptions propagate).
