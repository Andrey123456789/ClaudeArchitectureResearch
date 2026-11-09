Kind: KNW | Scope: backend | Capability: — | Loading: private reference of `logging`, read when configuring Serilog

# Serilog Configuration

Integration rule (`AddSerilog()`, environment-aware configuration, application code on `ILogger<T>`): `.claude/rules/backend/operations.md`.

## Bootstrap logging

Use two-stage initialization when startup logging matters: a bootstrap logger captures failures before the DI and configuration pipeline exists. Simpler applications may use plain host-managed Serilog setup without bootstrap logging.

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
        .ReadFrom.Services(services)   // DI integration of the modern AddSerilog API
        .Enrich.FromLogContext()
        .Enrich.WithMachineName()       // optional enricher packages, only when needed
        .Enrich.WithEnvironmentName()
        .Enrich.WithProperty("Application", "MyApp.Api"));

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

When the application uses the static or bootstrap `Log.Logger`, flush it on shutdown as above so asynchronous sinks do not lose buffered events. For purely host-managed logging, follow the provider's lifetime behavior instead of adding static Serilog lifecycle code.

## Configuration in appsettings

Configure only the sinks and enrichers the project needs; a Console sink is enough for a simple local Development baseline. File, Seq, OpenTelemetry, Elasticsearch and other sinks in this reference are examples, not baseline dependencies, and numeric limits or retention values are illustrative, not approved defaults.

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
      }
    ],
    "Enrich": ["FromLogContext"]
  }
}
```

`Override` keys are namespace prefixes matched against `SourceContext`; more specific prefixes win. Library-specific categories (for example the persistence technology's command logging) are tuned the same way; see the relevant knowledge skill.

Optional sink examples, each requiring its own package through `add-dependency`:

```json
{ "Name": "File", "Args": { "path": "logs/app-.log", "rollingInterval": "Day", "retainedFileCountLimit": 30 } }
{ "Name": "Seq", "Args": { "serverUrl": "http://localhost:5341" } }
```

## Request logging

`UseSerilogRequestLogging()` replaces ASP.NET Core's multiple per-request events with one summary event:

```csharp
app.UseSerilogRequestLogging(options =>
{
    options.MessageTemplate =
        "HTTP {RequestMethod} {RequestPath} responded {StatusCode} in {Elapsed:0.0000} ms";

    options.GetLevel = (httpContext, elapsed, ex) => ex is not null
        ? LogEventLevel.Error
        : httpContext.Response.StatusCode >= 500
            ? LogEventLevel.Error
            : LogEventLevel.Information;
});
```

Enrich the diagnostic context only with non-sensitive values (`.claude/rules/common/security.md`).

## Destructuring

```csharp
logger.LogInformation("Processing {@SensorInput}", sensorInput); // structure preserved
logger.LogInformation("Received {$Data}", new[] { 1, 2, 3 });   // ToString()
```

Never destructure large framework objects such as `HttpContext.Request`. Limit destructuring (`Destructure.ToMaximumDepth(4)`, `ToMaximumStringLength(1024)`, `ToMaximumCollectionCount(10)`) or transform types to the properties you need (`Destructure.ByTransforming<HttpRequest>(r => new { r.Method, r.Path })`).

## LogContext

```csharp
using (LogContext.PushProperty("CorrelationId", correlationId))
using (LogContext.PushProperty("TenantId", tenantId))
{
    logger.LogInformation("Processing order {OrderId}", orderId);
}
```

Requires `.Enrich.FromLogContext()`. Keep `LogContext` and other direct Serilog APIs at composition or middleware boundaries.

## Filtering and export

- `Serilog.Expressions`: `.Filter.ByExcluding("RequestPath like '/health%'")`, `.WriteTo.Conditional("@l = 'Error'", wt => wt.File("logs/errors-.log", rollingInterval: RollingInterval.Day))`.
- OTLP export without the OpenTelemetry SDK, through `Serilog.Sinks.OpenTelemetry`:

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
- Elasticsearch: the `Serilog.Sinks.Elasticsearch` package is deprecated; use the official `Elastic.Serilog.Sinks` package, which writes ECS-formatted documents to data streams:

  ```csharp
  .WriteTo.Elasticsearch([new Uri("https://elastic.example.com:9200")], opts =>
      opts.DataStream = new DataStreamName("logs", "myapp"))
  ```

## Quick reference

| Need | Technique |
|---|---|
| Startup failures before DI | Bootstrap logger |
| Log storage in development | Seq or the Aspire Dashboard |
| Log storage in production | Seq, Elasticsearch (Elastic sink) or an OTLP backend |
| Per-request summary | `UseSerilogRequestLogging()` |
| Scoped properties | `LogContext.PushProperty()` in middleware |
| Expression-based filtering | `Serilog.Expressions` |
| Audit trail | `AuditTo` (synchronous; exceptions propagate) |
| Levels per environment | `MinimumLevel.Override` in environment-specific appsettings |
