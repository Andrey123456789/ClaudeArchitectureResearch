> Private reference of `logging` · Serilog provider technique · Policy: `.claude/rules/composition.md` § Logging

# Serilog

## Setup Choices

- Use two-stage initialization when startup logging matters: a bootstrap logger
  captures failures before the full DI/configuration pipeline exists. Simpler
  applications may use normal host-managed Serilog setup without bootstrap
  logging.
- Register with `builder.Services.AddSerilog()`, which integrates with DI
  services through `ReadFrom.Services(services)`, rather than the older
  `builder.Host.UseSerilog()`.
- Message templates (`{PropertyName}`) create queryable structured data; string
  interpolation breaks structure and allocates even when the level is disabled.
- Keep log levels, sinks, and overrides in `appsettings` so they can vary per
  environment without redeployment.
- Keep direct Serilog APIs such as `Log.Logger` and `LogContext` at composition
  or provider-specific boundaries.

## Two-Stage Bootstrap Setup

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

The configuration below deliberately shows several optional sinks and
enrichers together. File, Seq, OpenTelemetry, Elasticsearch, and other sinks
are not baseline dependencies: configure only what the project needs — a
Console sink is enough for a simple local baseline. Numeric limits and retention
values are illustrative, not approved defaults.

## appsettings Configuration

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
specific prefixes take precedence. Add an override for the persistence
library's namespace when its query logging is too verbose.

## Request Logging Middleware

Replaces the multiple per-request ASP.NET Core log events with one summary
event:

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

## Structured Logging and Destructuring

```csharp
// Named properties — queryable structured data
logger.LogInformation("Order {OrderId} placed by {CustomerId} for {Total:C}",
    orderId, customerId, total);

// @ preserves object structure as properties
logger.LogInformation("Processing {@SensorInput}", sensorInput);
// Output: Processing {"Latitude": 25, "Longitude": 134}

// $ forces ToString()
logger.LogInformation("Received {$Data}", new[] { 1, 2, 3 });
// Output: Received "System.Int32[]"
```

Limit destructuring (`Destructure.ToMaximumDepth`, `ToMaximumStringLength`,
`ToMaximumCollectionCount`) or destructure specific properties
(`Destructure.ByTransforming<HttpRequest>(r => new { r.Method, r.Path })`);
large object graphs cause memory issues and massive entries.

## Scoped Properties with LogContext

```csharp
using (LogContext.PushProperty("CorrelationId", correlationId))
using (LogContext.PushProperty("TenantId", tenantId))
{
    logger.LogInformation("Processing order {OrderId}", orderId);
}
```

Requires `.Enrich.FromLogContext()` on the logger configuration.

## OpenTelemetry Sink (OTLP Export)

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

Requires the `Serilog.Expressions` package:

```csharp
// Exclude health check noise
.Filter.ByExcluding("RequestPath like '/health%'")

// Route errors to a separate file
.WriteTo.Conditional("@l = 'Error'",
    wt => wt.File("logs/errors-.log", rollingInterval: RollingInterval.Day))
```

## [LoggerMessage] Source Generator for Hot Paths

```csharp
public static partial class OrderLogs
{
    [LoggerMessage(Level = LogLevel.Information,
        Message = "Order {OrderId} created for {CustomerId}")]
    public static partial void OrderCreated(this ILogger logger, Guid orderId, Guid customerId);
}

// Usage
logger.OrderCreated(order.Id, order.CustomerId);
```

## Flushing on Shutdown

When the application uses the static/bootstrap `Log.Logger`, flush it on
shutdown so buffered events from asynchronous sinks (Seq, OTLP, Elasticsearch)
are written:

```csharp
try { app.Run(); }
catch (Exception ex) { Log.Fatal(ex, "Unhandled exception"); }
finally { await Log.CloseAndFlushAsync(); }
```

For purely host-managed logging, follow the configured provider's lifetime
behavior instead of adding static lifecycle code.

## Sensitive Data

```csharp
// BAD — password in logs
logger.LogInformation("Login: {Email} with password {Password}", email, password);

// GOOD — non-sensitive technical identifier
logger.LogInformation(
    "Login completed for user {UserId}",
    userId);
```

## Elasticsearch Sink

The `Serilog.Sinks.Elasticsearch` package is deprecated; use the official
`Elastic.Serilog.Sinks` package, which writes ECS-formatted documents to data
streams:

```csharp
// <PackageReference Include="Elastic.Serilog.Sinks" />
.WriteTo.Elasticsearch([new Uri("https://elastic.example.com:9200")], opts =>
    opts.DataStream = new DataStreamName("logs", "myapp"))
```

## Decision Guide

| Scenario | Recommendation |
|---|---|
| Serilog as provider | `AddSerilog()` + configuration |
| General application logging API | `ILogger<T>` (logging skill) |
| Log storage (development) | Seq (free single-user) or Aspire Dashboard |
| Log storage (production) | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
| Request logging | `UseSerilogRequestLogging()` |
| Scoped properties | `LogContext.PushProperty()` in middleware |
| Log filtering | `Serilog.Expressions` |
| High-performance paths | `[LoggerMessage]` source generator |
| Audit trails | `AuditTo` (synchronous, exceptions propagate) |
| Log levels by environment | `MinimumLevel.Override` per namespace in appsettings |
| OpenTelemetry integration | `Serilog.Sinks.OpenTelemetry` (no SDK dependency) |
