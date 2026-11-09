> Owner: private reference of the `logging` skill — Serilog provider setup technique | Scope: backend | Loads: read by `logging` only | Enforced: none

# Serilog

Registration and configuration policy: `.claude/rules/coding-style.md`
§ Logging Calls. Baseline package: `Serilog.AspNetCore`; every other sink or
enricher package is optional and goes through the `add-dependency` workflow.

## Host-Managed Setup

For a simple application, normal host-managed setup is enough:

```csharp
builder.Services.AddSerilog((services, lc) => lc
    .ReadFrom.Configuration(builder.Configuration)
    .ReadFrom.Services(services)
    .Enrich.FromLogContext());
```

`AddSerilog()` integrates with DI (`ReadFrom.Services`) and replaces the older
`builder.Host.UseSerilog()` style.

## Two-Stage Bootstrap

Use a bootstrap logger when failures before the DI/configuration pipeline is
available must be captured:

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

`WithMachineName` / `WithEnvironmentName` need the matching enricher packages.
With a static or bootstrap `Log.Logger`, flush it on shutdown (`try`/`finally`
as above) so buffered events reach async sinks; purely host-managed logging
follows the provider's lifetime and needs no static lifecycle code.

## appsettings.json Configuration

The example below deliberately shows several optional sinks and enrichers at
once. File, Seq, OpenTelemetry, and Elasticsearch are not baseline dependencies:
configure only what the project needs (Console is enough for a local Development
baseline). Numeric limits and retention values are illustrative, not approved
defaults.

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

`Override` uses namespace prefixes matched against `SourceContext`; more specific
prefixes win. Put environment-specific levels and sinks in
`appsettings.{Environment}.json`.

## Request Logging

`UseSerilogRequestLogging()` replaces ASP.NET Core's multiple per-request events
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
// Output: Processing {"Latitude": 25, "Longitude": 134}

// $ forces ToString()
logger.LogInformation("Received {$Data}", new[] { 1, 2, 3 });
// Output: Received "System.Int32[]"
```

Bound destructuring of large graphs, or destructure to selected properties:

```csharp
.Destructure.ToMaximumDepth(4)
.Destructure.ToMaximumStringLength(1024)
.Destructure.ToMaximumCollectionCount(10)

// better: only the fields you need
.Destructure.ByTransforming<HttpRequest>(r => new { r.Method, r.Path })
```

## LogContext

```csharp
using (LogContext.PushProperty("CorrelationId", correlationId))
using (LogContext.PushProperty("TenantId", tenantId))
{
    logger.LogInformation("Processing order {OrderId}", orderId);
    // CorrelationId and TenantId are attached to every event in this scope
}
```

Requires `.Enrich.FromLogContext()`. Keep `LogContext` usage at middleware or
composition boundaries.

## OpenTelemetry Sink

Export events to an OTLP backend without the OpenTelemetry SDK
(`Serilog.Sinks.OpenTelemetry`):

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

## Serilog.Expressions

```csharp
// Exclude health-check noise
.Filter.ByExcluding("RequestPath like '/health%'")

// Route errors to a separate file
.WriteTo.Conditional("@l = 'Error'",
    wt => wt.File("logs/errors-.log", rollingInterval: RollingInterval.Day))
```

## Elasticsearch

The `Serilog.Sinks.Elasticsearch` package is deprecated. Use the official
`Elastic.Serilog.Sinks` package, which writes ECS documents to data streams:

```csharp
.WriteTo.Elasticsearch([new Uri("https://elastic.example.com:9200")], opts =>
    opts.DataStream = new DataStreamName("logs", "myapp"))
```

## Sensitive Data Example

```csharp
// Not this
logger.LogInformation("Login: {Email} with password {Password}", email, password);

// A non-sensitive technical identifier instead
logger.LogInformation(
    "Login completed for user {UserId}",
    userId);
```

## Decision Guide

| Scenario | Technique |
|---|---|
| Serilog as provider | `AddSerilog()` + configuration |
| Local Development log viewing | Console; optionally Seq or Aspire Dashboard |
| Production log storage | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
| Request logging | `UseSerilogRequestLogging()` |
| Scoped properties | `LogContext.PushProperty()` in middleware |
| Log filtering | `Serilog.Expressions` |
| Audit trails | `AuditTo` (synchronous; exceptions propagate) |
| Levels by environment | `MinimumLevel.Override` in appsettings |
