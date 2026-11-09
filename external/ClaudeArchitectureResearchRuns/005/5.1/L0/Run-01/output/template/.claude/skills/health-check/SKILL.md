---
name: health-check
description: >
  Use when implementing or reviewing health endpoints or orchestrator probes:
  liveness vs readiness, tagged dependency checks, database checks, startup
  readiness, safe responses.
---

> Level: 2 Technology · Owns: health-check implementation technique · Scope: backend · Loads: on demand (knowledge skill)

# Health Checks

Policy owners: `.claude/rules/1-architecture/entry-points.md` (Operational endpoints: cheap and deterministic, liveness vs readiness semantics, no internals in public responses). Distinguish liveness from readiness when the deployment platform benefits from it.

## Basic setup

```csharp
builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapHealthChecks("/health");
```

## Liveness

Answers roughly: *is this process alive enough that a restart is not needed?*

```csharp
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false                      // no dependency checks: process responsiveness only
});
```

The exact probe configuration depends on the hosting environment.

## Readiness

Answers roughly: *can this instance serve the traffic it is responsible for?*

```csharp
builder.Services
    .AddHealthChecks()
    .AddCheck<DatabaseHealthCheck>("database", tags: ["ready"]);

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

Include only dependencies that define readiness; an optional external service does not necessarily make the whole application unready.

## Database checks

A lightweight connectivity check fits the cost limits in `entry-points.md`: for EF Core, `AddDbContextCheck<AppDbContext>()` (`Microsoft.Extensions.Diagnostics.HealthChecks.EntityFrameworkCore`) runs `CanConnectAsync`. Prefer provider or framework integrations where suitable.

## External dependencies

Check an external dependency only when its availability is part of readiness's meaning. Avoid readiness cascades (A calls B's readiness, which calls C's…) without understanding the operational consequences; check the capability the application genuinely needs.

## Startup readiness

When initialization is asynchronous or slow, a startup-gate check flipped by a hosted service keeps readiness unhealthy until it completes (liveness is not the mechanism for this — `entry-points.md`).

## Status codes and responses

Health endpoints return success when healthy and a non-success status when unhealthy under the configured probe policy (`HealthCheckOptions.ResultStatusCodes` maps statuses). Probe semantics are not business API semantics. Keep public probe responses small (the default plain-text writer); if operators need detail, serve a richer `ResponseWriter` on an endpoint protected by network or authorization controls, and check its content against the exposure rule in `entry-points.md`.

## Exposure

Probes are often reached by infrastructure without user authentication. Choose exposure from the deployment topology: private network, dedicated management port (`RequireHost("*:8081")`), host restrictions, or authorization where the probe infrastructure supports it.

## Performance

Probes run often: avoid expensive queries, long external timeouts, large allocations, business workflows, and Error-level logs for every routine failed probe.

## Testing

When deployment relies on the configuration: live endpoint responds while the process is healthy; readiness follows a required dependency; responses leak nothing sensitive; optional-dependency behavior matches intent. Do not test un-customized framework behavior.
