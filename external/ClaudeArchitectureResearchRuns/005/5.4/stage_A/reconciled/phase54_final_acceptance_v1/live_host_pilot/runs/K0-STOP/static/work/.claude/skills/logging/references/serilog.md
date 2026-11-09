> Kind: KNW | Scope: backend | Owner: Serilog configuration technique (private to logging) | Loading: read by logging only

# Serilog

Integration rule: `rules/backend/hosting.md` § Logging. Application code keeps using `ILogger<T>`; direct Serilog APIs (`Log.Logger`, `LogContext`) stay at composition or provider-specific boundaries.

## Host-managed setup

```csharp
builder.Services.AddSerilog((services, lc) => lc
    .ReadFrom.Configuration(builder.Configuration)
    .ReadFrom.Services(services)
    .Enrich.FromLogContext());
```

`AddSerilog()` integrates with DI (`ReadFrom.Services`), replacing the older `builder.Host.UseSerilog()`.

## Two-stage bootstrap

Use a bootstrap logger when startup failures before DI/configuration need to be captured; simpler applications can skip it.

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
        .Enrich.WithMachineName()
        .Enrich.WithEnvironmentName()
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
    await Log.CloseAndFlushAsync();
}
```

When the static/bootstrap `Log.Logger` is used, flush it on shutdown (`try`/`finally` with `CloseAndFlushAsync`) so buffered events from asynchronous sinks are written; purely host-managed logging follows the provider's lifetime.

## appsettings configuration

Keep levels, sinks and overrides in configuration so they can differ per environment. The example shows several optional sinks at once — File, Seq and others are not baseline dependencies; a Console sink suffices for a simple local Development baseline, and numeric limits and retention values are illustrative.

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

`Override` keys are namespace prefixes matched against `SourceContext`; more specific prefixes win.

## Request logging

`UseSerilogRequestLogging()` replaces ASP.NET Core's per-request events with one summary event:

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
// Named properties create queryable structured data
logger.LogInformation("Order {OrderId} placed by {CustomerId} for {Total:C}",
    orderId, customerId, total);

// @ preserves object structure
logger.LogInformation("Processing {@SensorInput}", sensorInput);

// $ forces ToString()
logger.LogInformation("Received {$Data}", new[] { 1, 2, 3 });
```

Limit destructuring of large graphs, or transform types to specific properties:

```csharp
.Destructure.ToMaximumDepth(4)
.Destructure.ToMaximumStringLength(1024)
.Destructure.ToMaximumCollectionCount(10)
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

Requires `.Enrich.FromLogContext()`.

## OpenTelemetry export

`Serilog.Sinks.OpenTelemetry` exports to any OTLP backend without the OpenTelemetry SDK:

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

## Filtering with Serilog.Expressions

```csharp
.Filter.ByExcluding("RequestPath like '/health%'")

.WriteTo.Conditional("@l = 'Error'",
    wt => wt.File("logs/errors-.log", rollingInterval: RollingInterval.Day))
```

## Elasticsearch

The `Serilog.Sinks.Elasticsearch` package is deprecated; use the official `Elastic.Serilog.Sinks` package (same `WriteTo.Elasticsearch` name, ECS documents to data streams):

```csharp
.WriteTo.Elasticsearch([new Uri("https://elastic.example.com:9200")], opts =>
    opts.DataStream = new DataStreamName("logs", "myapp"))
```

## Decision guide

| Scenario | Technique |
|---|---|
| Serilog as provider | `AddSerilog()` + configuration |
| Development log storage | Seq (free single-user) or Aspire Dashboard |
| Production log storage | Seq, Elasticsearch (Elastic sink) or an OTLP backend |
| Request logging | `UseSerilogRequestLogging()` |
| Scoped properties | `LogContext.PushProperty()` in middleware |
| Expression-based filtering | `Serilog.Expressions` |
| Audit trail | `AuditTo` (synchronous, exceptions propagate) |
| Levels per environment | `MinimumLevel.Override` in appsettings |
| OpenTelemetry integration | `Serilog.Sinks.OpenTelemetry` |
