> Private reference of the logging skill. Owns: Serilog configuration technique and examples · Scope: backend · Loads: read by the logging skill when Serilog is configured or changed · Depends on: .claude/skills/logging/SKILL.md

# Serilog

Serilog registration rule (`AddSerilog`, environment-aware configuration,
`ILogger<T>` in application code): `.claude/rules/error-handling.md`, Logging.

## Bootstrap Logging

Two-stage initialization helps when startup logging matters: a bootstrap logger
captures failures before the DI/configuration pipeline exists. Simpler
applications may use host-managed Serilog without a bootstrap logger.

```csharp
using Serilog;

// Stage 1: bootstrap logger — captures startup errors before DI
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Information)
    .Enrich.FromLogContext()
    .WriteTo.Console()
    .CreateBootstrapLogger();

try
{
    Log.Information("Starting application");

    var builder = WebApplication.CreateBuilder(args);

    // Stage 2: full logger with DI and configuration
    builder.Services.AddSerilog((services, lc) => lc
        .ReadFrom.Configuration(builder.Configuration)
        .ReadFrom.Services(services)
        .Enrich.FromLogContext()
        .Enrich.WithMachineName()
        .Enrich.WithEnvironmentName()
        .Enrich.WithProperty("Application", "MyApp.Api"));

    var app = builder.Build();

    app.UseSerilogRequestLogging(options =>
    {
        options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
        {
            diagnosticContext.Set("RequestHost", httpContext.Request.Host.Value);
            diagnosticContext.Set("UserAgent",
                httpContext.Request.Headers.UserAgent.ToString());
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

`ReadFrom.Services(services)` is why `builder.Services.AddSerilog()` is used
instead of `builder.Host.UseSerilog()`.

## Configuration

The example below deliberately shows several optional sinks and enrichers. File,
Seq, OpenTelemetry, Elasticsearch, and similar sinks are not baseline
dependencies: configure only what the project needs (a Console sink suffices for
local Development). Numeric limits and retention values are illustrative, not
approved defaults.

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
      },
      {
        "Name": "File",
        "Args": {
          "path": "logs/app-.log",
          "rollingInterval": "Day",
          "retainedFileCountLimit": 30,
          "fileSizeLimitBytes": 104857600
        }
      },
      {
        "Name": "Seq",
        "Args": { "serverUrl": "http://localhost:5341" }
      }
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

`Override` uses namespace prefixes matched against `SourceContext`; more
specific prefixes take precedence.

## Request Logging

`UseSerilogRequestLogging` replaces ASP.NET Core's multiple per-request events
with one summary event:

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

    options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
    {
        diagnosticContext.Set("UserId",
            httpContext.User.FindFirstValue(ClaimTypes.NameIdentifier) ?? "anonymous");
    };
});
```

## Destructuring

```csharp
// Named properties — queryable structured data
logger.LogInformation("Order {OrderId} placed by {CustomerId} for {Total:C}",
    orderId, customerId, total);

// @ preserves object structure as properties
logger.LogInformation("Processing {@SensorInput}", sensorInput);

// $ forces ToString()
logger.LogInformation("Received {$Data}", new[] { 1, 2, 3 });
```

Destructure with limits, or better, to specific properties:

```csharp
.Destructure.ToMaximumDepth(4)
.Destructure.ToMaximumStringLength(1024)
.Destructure.ToMaximumCollectionCount(10)

.Destructure.ByTransforming<HttpRequest>(r => new { r.Method, r.Path })
```

Avoid destructuring whole `HttpRequest` objects or other large graphs (payload
rule: `.claude/rules/security.md`).

## LogContext

```csharp
using (LogContext.PushProperty("CorrelationId", correlationId))
using (LogContext.PushProperty("TenantId", tenantId))
{
    logger.LogInformation("Processing order {OrderId}", orderId);
}
```

Requires `.Enrich.FromLogContext()`; keep `LogContext` use at middleware or
composition boundaries.

## OpenTelemetry Sink

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

## Serilog.Expressions Filtering

Requires the `Serilog.Expressions` package.

```csharp
.Filter.ByExcluding("RequestPath like '/health%'")

.WriteTo.Conditional("@l = 'Error'",
    wt => wt.File("logs/errors-.log", rollingInterval: RollingInterval.Day))
```

## Flushing on Shutdown

When the application uses the static/bootstrap `Log.Logger`, flush it on
shutdown so buffered events (Seq, OTLP, Elasticsearch sinks) are written:

```csharp
try { app.Run(); }
catch (Exception ex) { Log.Fatal(ex, "Unhandled exception"); }
finally { await Log.CloseAndFlushAsync(); }
```

Purely host-managed logging follows the configured provider's lifetime instead.

## Elasticsearch

The `Serilog.Sinks.Elasticsearch` package is deprecated. The official
`Elastic.Serilog.Sinks` package provides the same `WriteTo.Elasticsearch`
method name and writes ECS-formatted documents to data streams:

```csharp
.WriteTo.Elasticsearch([new Uri("https://elastic.example.com:9200")], opts =>
    opts.DataStream = new DataStreamName("logs", "myapp"))
```

## Decision Guide

| Scenario | Recommendation |
|---|---|
| Project uses Serilog as provider | `AddSerilog()` + configuration |
| Log storage (development) | Seq (free single-user) or Aspire Dashboard |
| Log storage (production) | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
| Request logging | `UseSerilogRequestLogging()` |
| Scoped properties | `LogContext.PushProperty()` in middleware |
| Log filtering | `Serilog.Expressions` |
| High-performance paths | `[LoggerMessage]` source generator |
| Audit trails | `AuditTo` (synchronous, exceptions propagate) |
| Log levels by environment | `MinimumLevel.Override` per namespace in appsettings |
| OpenTelemetry integration | `Serilog.Sinks.OpenTelemetry` |
