---
name: health-check
description: >
  Use for health endpoints: AddHealthChecks/MapHealthChecks, liveness vs readiness, dependency checks, response safety, probe tests.
---

> Level: 2 Technology | Owns: ASP.NET Core health-check technique | Scope: backend | Loads: knowledge skill (on demand) | Depends on: 0-core/health-principles.md

# Health Check Technique

Policy owners (routing): cheap/deterministic checks, liveness vs. readiness,
safe public output → `0-core/health-principles.md`.

## Basic Setup

```csharp
builder.Services.AddHealthChecks();
var app = builder.Build();
app.MapHealthChecks("/health");
```

## Liveness and Readiness

```csharp
builder.Services.AddHealthChecks()
    .AddCheck<DatabaseHealthCheck>("database", tags: ["ready"]);

app.MapHealthChecks("/health/live", new HealthCheckOptions { Predicate = _ => false });
app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

The semantics come from `0-core/health-principles.md`; the mechanics:

- `Predicate = _ => false` makes `/health/live` report process liveness without
  running registered dependency checks.
- Tag the checks that define readiness (`"ready"`) and leave optional
  dependencies untagged.
- For slow asynchronous initialization, register a check that reads a
  startup-complete flag set by the initialization code.

## Database Checks

`builder.Services.AddHealthChecks().AddDbContextCheck<AppDbContext>(tags: ["ready"]);`
(package `Microsoft.Extensions.Diagnostics.HealthChecks.EntityFrameworkCore`,
added through `add-dependency`) runs a connectivity probe through the context;
a provider-specific check is an alternative.

## External Dependencies

When a dependency defines readiness, check the capability directly rather than
calling the dependency's own readiness endpoint, which chains failures across
services.

## Status and Response Body

Healthy returns success and unhealthy a non-success status per the probe
policy; map statuses through `HealthCheckOptions.ResultStatusCodes` when needed.
Keep probe bodies small; if operators need details, serve them from an endpoint
protected by network or authorization controls.

## Exposure

Probes often run without user authentication; restrict them by private network,
dedicated management port, host filtering, or authorization the probe
infrastructure supports.

## Performance

Probes run frequently, so long external timeouts, large allocations, and
Error-level logs for every normal failed probe add up quickly; keep each check
small.

## Testing

Test configuration the deployment relies on: live responds while healthy,
readiness follows a required dependency, responses leak nothing sensitive,
optional dependencies behave as intended. Do not test uncustomized framework
behavior.
