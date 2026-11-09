---
name: health-check
description: >
  Use when adding or reviewing health endpoints: AddHealthChecks,
  MapHealthChecks, liveness vs readiness, tagged checks, database checks, probe
  status codes, safe payloads, startup readiness.
---

> Kind: KNW | Scope: backend | Capability: — | Loading: on-demand knowledge

# Health Checks

Policy: `.claude/rules/backend/operations.md` (cheap and deterministic checks, liveness vs. readiness, safe public responses). Health checks answer whether the running application is alive and/or ready to serve traffic; distinguish liveness from readiness when deployment infrastructure benefits from it.

## Basic setup

```csharp
builder.Services.AddHealthChecks();
var app = builder.Build();
app.MapHealthChecks("/health");
```

## Liveness

*Is the process alive enough that restarting it is not required?* A liveness endpoint usually checks no dependencies:

```csharp
app.MapHealthChecks("/health/live", new HealthCheckOptions { Predicate = _ => false });
```

Exact probe configuration varies by hosting environment; never make the application restart because a dependency is temporarily unavailable.

## Readiness

*Can this instance currently serve the traffic it is responsible for?*

```csharp
builder.Services.AddHealthChecks().AddCheck<DatabaseHealthCheck>("database", tags: ["ready"]);

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

Include only dependencies required for meaningful readiness; an optional external service need not make the whole application unready. If initialization is asynchronous or slow, keep readiness unhealthy until required startup work completes — never use liveness for this, it causes restart loops.

## Database and external dependencies

A database check performs a lightweight connectivity/availability check (provider or framework health-check integration where suitable) — no business queries, large scans, or data modification. Check an external dependency only when its availability matters to readiness, and avoid readiness cascades (A → B readiness → C readiness ...) without understanding the operational consequences; prefer a lightweight check of the capability actually needed.

## Status codes and payloads

Healthy → success, unhealthy → non-success per the configured probe policy (`HealthCheckOptions.ResultStatusCodes` maps statuses); do not reuse business API status semantics mechanically for probes. Keep probe responses small; protect operator-facing detailed diagnostics with network or authorization controls instead of exposing connection strings, credentials, raw exceptions, or infrastructure topology.

## Exposure

Probes often must be reachable by infrastructure without user authentication. Choose exposure by topology: private network access, a dedicated management port, host restrictions, or authorization the probe infrastructure supports.

## Performance

Probes run frequently: avoid expensive queries, long external timeouts, large allocations, full workflows, and Error-level logs for every normal failed probe.

## Testing

Test health configuration the deployment relies on: live endpoint responds when healthy, readiness follows a required dependency, responses do not leak sensitive details, optional-dependency behavior matches the intended semantics. Do not test framework behavior the application does not customize.

## Anti-patterns

Health checks as a code-quality grading system, database writes or business transactions from probes, every dependency on liveness, remote dependency chains without operational justification, stack traces from health endpoints.
