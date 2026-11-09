> Level: 2-technology · Owns: Serilog provider technique (private reference of `logging`) · Loading: read by `logging`

# Serilog

Integration rule (`AddSerilog`, environment-aware configuration, application code on `ILogger<T>`): `.claude/rules/2-technology/backend-libraries.md`. Keep direct Serilog APIs (`Log.Logger`, `LogContext`) at composition or provider-specific boundaries.

## Setup

Two-stage bootstrap is worthwhile when startup failures must be logged before DI and configuration exist; simpler applications can use host-managed setup only.

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
    await Log.CloseAndFlushAsync();
}
```

Flush the static/bootstrap logger on shutdown when it is used (async sinks lose buffered events otherwise); purely host-managed logging follows the provider's lifetime instead.

## Configuration

Configure only the sinks and enrichers the project needs; a Console sink is enough for a simple local Development baseline. File, Seq, OpenTelemetry, or Elasticsearch sinks are options, not baseline dependencies, and numeric limits below are illustrative.

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
      { "Name": "Console", "Args": { "outputTemplate": "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}" } }
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

`UseSerilogRequestLogging` replaces per-request framework noise with one summary event:

```csharp
app.UseSerilogRequestLogging(options =>
{
    options.MessageTemplate = "HTTP {RequestMethod} {RequestPath} responded {StatusCode} in {Elapsed:0.0000} ms";
    options.GetLevel = (httpContext, elapsed, ex) =>
        ex is not null || httpContext.Response.StatusCode >= 500 ? LogEventLevel.Error : LogEventLevel.Information;
    options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
    {
        diagnosticContext.Set("RequestHost", httpContext.Request.Host.Value);
        diagnosticContext.Set("UserId", httpContext.User.FindFirstValue(ClaimTypes.NameIdentifier) ?? "anonymous");
    };
});
```

`EnrichDiagnosticContext` adds request-level properties to the single summary event; prefer stable technical identifiers over personal data. Process-wide enrichers such as `.Enrich.WithMachineName()`, `.Enrich.WithEnvironmentName()` (`Serilog.Enrichers.Environment`), or `.Enrich.WithProperty("Application", "<Name>.Api")` belong in the logger configuration and are added only when an operational need exists.

## Structure and context

- `{@Value}` destructures an object, `{$Value}` forces `ToString()`; prefer destructuring to selected properties (`.Destructure.ByTransforming<HttpRequest>(r => new { r.Method, r.Path })`) and keep destructuring limits configured.
- `using (LogContext.PushProperty("TenantId", tenantId)) { ... }` attaches properties to every event in scope; requires `Enrich.FromLogContext()`.
- `Serilog.Expressions` enables filters such as `.Filter.ByExcluding("RequestPath like '/health%'")` and conditional sinks.

## Sinks to avoid

The `Serilog.Sinks.Elasticsearch` package is deprecated; use `Elastic.Serilog.Sinks` when Elasticsearch is the chosen log store. OTLP export is available through `Serilog.Sinks.OpenTelemetry` without the OpenTelemetry SDK.

## Decision guide

| Scenario | Option |
| --- | --- |
| Provider setup | `AddSerilog()` + configuration |
| Local log storage when needed | Seq (free single-user) or the Aspire Dashboard |
| Production log storage | Seq, Elasticsearch (`Elastic.Serilog.Sinks`), or an OTLP backend |
| Request logging | `UseSerilogRequestLogging()` |
| Scoped properties | `LogContext.PushProperty()` in middleware |
| Filtering | `Serilog.Expressions` |
| Audit trails (only with an adopted audit design) | `AuditTo` (synchronous; exceptions propagate) |
| Levels per environment | `MinimumLevel.Override` per namespace in configuration |
