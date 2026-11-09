> Kind: KNW | Scope: backend | Capability: — | Loading: read by `logging` when Serilog configuration is in scope

# Serilog Reference

Serilog is the logging provider (decision register); application code keeps using `ILogger<T>`. Policy: `.claude/rules/backend/operations.md`.

## Principles

1. **Two-stage initialization when startup logging matters** — a bootstrap logger captures failures before DI/configuration is available; simpler applications may use host-managed setup without bootstrap logging.
2. **`builder.Services.AddSerilog()`**, not `builder.Host.UseSerilog()` — integrates with DI via `ReadFrom.Services(services)`.
3. **Message templates, not interpolation** — `{PropertyName}` creates queryable data; `$"..."` breaks structure and allocates even when the level is disabled.
4. **Configuration in appsettings** — levels, sinks, and overrides change per environment without redeployment.
5. **Serilog APIs stay at the edges** — `Log.Logger` and `LogContext` belong to composition and provider-specific boundaries.

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

Baseline integration package: `Serilog.AspNetCore`. A Console sink suffices for a simple local Development baseline; File, Seq, OpenTelemetry, Elasticsearch, and enrichers such as `WithMachineName`/`WithEnvironmentName` are optional — add sinks and enrichers only when the project requires them (`add-dependency`). Numeric limits and retention values in examples are illustrative, not approved defaults.

## appsettings configuration

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
        "Args": { "outputTemplate": "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}" }
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

`Override` keys are namespace prefixes matched against `SourceContext`; more specific prefixes win. A rolling File sink (`"path": "logs/app-.log", "rollingInterval": "Day"`) or a Seq sink (`"serverUrl": "http://localhost:5341"`) is added to `WriteTo` only when needed.

## Request logging

`UseSerilogRequestLogging` replaces per-request framework noise with one summary event:

```csharp
app.UseSerilogRequestLogging(options =>
{
    options.MessageTemplate = "HTTP {RequestMethod} {RequestPath} responded {StatusCode} in {Elapsed:0.0000} ms";
    options.GetLevel = (httpContext, elapsed, ex) =>
        ex is not null || httpContext.Response.StatusCode >= 500 ? LogEventLevel.Error : LogEventLevel.Information;
    options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
        diagnosticContext.Set("RequestHost", httpContext.Request.Host.Value);
});
```

Enrich only with non-sensitive values (`.claude/rules/common/security.md`).

## Destructuring

```csharp
logger.LogInformation("Processing {@SensorInput}", sensorInput);   // @ preserves structure
logger.LogInformation("Received {$Data}", new[] { 1, 2, 3 });       // $ forces ToString()
```

Never destructure large graphs such as `HttpRequest` without limits; configure `Destructure.ToMaximumDepth/StringLength/CollectionCount` or transform to specific properties (`Destructure.ByTransforming<HttpRequest>(r => new { r.Method, r.Path })`).

## LogContext

```csharp
using (LogContext.PushProperty("CorrelationId", correlationId))
using (LogContext.PushProperty("TenantId", tenantId))
{
    logger.LogInformation("Processing order {OrderId}", orderId);
}
```

Requires `.Enrich.FromLogContext()`.

## Optional integrations

- OTLP export without the OpenTelemetry SDK: `Serilog.Sinks.OpenTelemetry` (`.WriteTo.OpenTelemetry(o => { o.Endpoint = "http://localhost:4317"; o.Protocol = OtlpProtocol.Grpc; })`).
- Expression filtering (`Serilog.Expressions`): `.Filter.ByExcluding("RequestPath like '/health%'")`, `.WriteTo.Conditional("@l = 'Error'", wt => wt.File("logs/errors-.log", rollingInterval: RollingInterval.Day))`.
- Elasticsearch: the `Serilog.Sinks.Elasticsearch` package is deprecated; use `Elastic.Serilog.Sinks` (`.WriteTo.Elasticsearch([new Uri("https://elastic.example.com:9200")], opts => opts.DataStream = new DataStreamName("logs", "myapp"))`).
- Audit trails: `AuditTo` (synchronous; exceptions propagate) — only with an adopted audit design.

## Shutdown flush

When the static/bootstrap `Log.Logger` is used, flush it on shutdown (`try { app.Run(); } ... finally { await Log.CloseAndFlushAsync(); }`) so asynchronous sinks do not lose buffered events. Purely host-managed logging follows the provider's lifetime instead.

## Decision guide

| Scenario | Recommendation |
|---|---|
| Provider setup | `AddSerilog()` + configuration |
| Development log storage | Console; Seq or Aspire Dashboard when useful |
| Production log storage | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
| Request logging | `UseSerilogRequestLogging()` |
| Scoped properties | `LogContext.PushProperty()` in middleware |
| Level per environment | `MinimumLevel.Override` in appsettings |
