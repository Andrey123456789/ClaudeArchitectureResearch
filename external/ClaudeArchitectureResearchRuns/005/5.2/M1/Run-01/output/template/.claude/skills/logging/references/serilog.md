> **Private reference** of `logging` · Owns: Serilog configuration technique — bootstrap, appsettings, sinks, enrichers, request logging, destructuring, LogContext, expressions · Scope: backend · Loading: on demand (read by `logging`)

# Serilog

## Rules

Serilog integration rule (`AddSerilog()`, environment-aware configuration,
application code on `ILogger<T>`): `backend-runtime.md` → Logging. Keep direct
Serilog APIs such as `Log.Logger` and `LogContext` at composition and
provider-specific boundaries.

Use two-stage initialization when startup logging matters: a bootstrap logger
captures failures before the full DI/configuration pipeline is available. Simpler
applications may use normal host-managed Serilog setup without bootstrap logging.
`AddSerilog()` integrates with DI services through `ReadFrom.Services(services)`.

## Patterns

### Two-Stage Bootstrap Setup

```csharp
using Serilog;

// Stage 1: Bootstrap logger — captures startup errors before DI
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Information)
    .Enrich.FromLogContext()
    .WriteTo.Console()
    .CreateBootstrapLogger();

try
{
    Log.Information("Starting application");

    var builder = WebApplication.CreateBuilder(args);

    // Stage 2: Full logger with DI and configuration
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

The following configuration intentionally demonstrates several optional sinks
and enrichers in one example.

Do not treat File, Seq, OpenTelemetry, Elasticsearch, or other sinks/enrichers
shown in this skill as baseline dependencies.

For a new application, configure only the sinks and enrichers required by the
actual project. A Console sink is sufficient for a simple local Development
baseline unless additional log storage or export is required.

Numeric limits and retention values in examples are illustrative, not
template-approved defaults.

### appsettings.json Configuration

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

Override section uses namespace prefixes matched against `SourceContext`. More specific prefixes take precedence.

### Request Logging Middleware

Replaces the multiple per-request log events from ASP.NET Core with a single summary event.

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

### Structured Logging and Destructuring

```csharp
// Named properties — creates queryable structured data
logger.LogInformation("Order {OrderId} placed by {CustomerId} for {Total:C}",
    orderId, customerId, total);

// @ operator preserves object structure as properties
logger.LogInformation("Processing {@SensorInput}", sensorInput);
// Output: Processing {"Latitude": 25, "Longitude": 134}

// $ operator forces ToString()
logger.LogInformation("Received {$Data}", new[] { 1, 2, 3 });
// Output: Received "System.Int32[]"
```

### Scoped Properties with LogContext

```csharp
using (LogContext.PushProperty("CorrelationId", correlationId))
using (LogContext.PushProperty("TenantId", tenantId))
{
    logger.LogInformation("Processing order {OrderId}", orderId);
    // CorrelationId and TenantId attached to ALL log events in this scope
}
```

Requires `.Enrich.FromLogContext()` on the logger configuration.

### OpenTelemetry Sink (OTLP Export)

Export Serilog events directly to any OTLP backend without the OpenTelemetry SDK:

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

### Serilog.Expressions for Filtering

Requires the `Serilog.Expressions` package.

```csharp
// Exclude health check noise
.Filter.ByExcluding("RequestPath like '/health%'")

// Route errors to a separate file
.WriteTo.Conditional("@l = 'Error'",
    wt => wt.File("logs/errors-.log", rollingInterval: RollingInterval.Day))
```

### [LoggerMessage] Source Generator for Hot Paths

Built into `Microsoft.Extensions.Logging.Abstractions` — compile-time generated, zero allocations when the level is disabled.

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

## Anti-patterns

### Message Templates

Rule: `backend-runtime.md` → Logging. String interpolation also allocates even
when the level is disabled.

```csharp
// BAD — breaks structured logging, allocates even when level is disabled
logger.LogInformation($"Order {orderId} created for {customerId}");

// GOOD — message template with named parameters
logger.LogInformation("Order {OrderId} created for {CustomerId}", orderId, customerId);
```

### Flush Bootstrap/Static Serilog on Shutdown

When the application uses Serilog's static/bootstrap `Log.Logger`, flush it on
shutdown so buffered events can be written.

For purely host-managed logging, follow the lifetime behavior of the configured
provider rather than adding static Serilog lifecycle code unnecessarily.

```csharp
// BAD — async sinks (Seq, OTLP, Elasticsearch) lose buffered events
app.Run();

// GOOD — wrap in try/finally
try { app.Run(); }
catch (Exception ex) { Log.Fatal(ex, "Unhandled exception"); }
finally { await Log.CloseAndFlushAsync(); }
```

### Sensitive Data

Rule: `security.md` → Logging and Sensitive Data. Prefer a non-sensitive technical
identifier:

```csharp
// BAD — passwords and tokens in logs
logger.LogInformation("Login: {Email} with password {Password}", email, password);

// GOOD — non-sensitive technical identifier
logger.LogInformation(
    "Login completed for user {UserId}",
    userId);
```

### Don't Destructure Without Limits

```csharp
// BAD — large object graphs cause memory issues and massive log entries
logger.LogInformation("Request: {@Request}", httpContext.Request);

// GOOD — configure destructuring limits
.Destructure.ToMaximumDepth(4)
.Destructure.ToMaximumStringLength(1024)
.Destructure.ToMaximumCollectionCount(10)

// BETTER — destructure to specific properties
.Destructure.ByTransforming<HttpRequest>(r => new { r.Method, r.Path })
```

### Don't Use the Deprecated Elasticsearch Sink

```csharp
// BAD — the Serilog.Sinks.Elasticsearch PACKAGE is deprecated
// <PackageReference Include="Serilog.Sinks.Elasticsearch" />
.WriteTo.Elasticsearch("http://localhost:9200")

// GOOD — same method name, but from the official Elastic.Serilog.Sinks
// package, which writes ECS-formatted documents to data streams
// <PackageReference Include="Elastic.Serilog.Sinks" />
.WriteTo.Elasticsearch([new Uri("https://elastic.example.com:9200")], opts =>
    opts.DataStream = new DataStreamName("logs", "myapp"))
```

## Decision Guide

| Scenario | Recommendation |
|----------|---------------|
| Project chooses Serilog as provider | `AddSerilog()` + configuration |
| General application logging API | `ILogger<T>`; follow the `logging` skill |
| Log storage (development) | Seq (free single-user) or Aspire Dashboard |
| Log storage (production) | Seq, Elasticsearch (Elastic sink), or OTLP backend |
| Request logging | `UseSerilogRequestLogging()` (replaces per-request noise) |
| Scoped properties | `LogContext.PushProperty()` in middleware |
| Log filtering | `Serilog.Expressions` for expression-based filtering |
| High-performance paths | `[LoggerMessage]` source generator |
| Audit trails | `AuditTo` (synchronous, exceptions propagate) |
| Log levels by environment | `MinimumLevel.Override` per namespace in appsettings |
| OpenTelemetry integration | `Serilog.Sinks.OpenTelemetry` (no SDK dependency) |
