---
name: health-check
description: >
  Use when implementing health endpoints: AddHealthChecks/MapHealthChecks,
  liveness vs. readiness, dependency and database checks, status mapping, safe
  responses, probe exposure, tests.
---

> Owns: health-check technique and examples (no policy) | Scope: backend | Loads: on demand (knowledge skill)

# Health Checks

Policy owners: cheap/deterministic checks, liveness vs. readiness semantics, and
safe public output — `.claude/rules/api.md` § Health Checks.

Health checks answer whether the running application is alive and/or ready to
serve traffic. Distinguish liveness from readiness when the deployment
infrastructure benefits from it.

## Basic Setup

```csharp
builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapHealthChecks("/health");
```

Use more specific readiness/liveness endpoints when appropriate.

## Liveness

Liveness asks: is the process alive enough that a restart is not currently
required?

```csharp
app.MapHealthChecks(
    "/health/live",
    new HealthCheckOptions
    {
        Predicate = _ => false
    });
```

The exact probe configuration may vary by hosting environment.

## Readiness

Readiness asks: can this instance currently serve the traffic it is responsible
for? Register readiness checks with tags:

```csharp
builder.Services
    .AddHealthChecks()
    .AddCheck<DatabaseHealthCheck>(
        "database",
        tags: ["ready"]);
```

```csharp
app.MapHealthChecks(
    "/health/ready",
    new HealthCheckOptions
    {
        Predicate = check => check.Tags.Contains("ready")
    });
```

Include only dependencies required for meaningful readiness; an optional
external service does not necessarily make the whole application unready.

## Database Health

A lightweight connectivity/availability check — no expensive business queries,
large scans, or data modification. Use provider/framework health-check
integration where suitable.

## External Dependencies

Check an external dependency only when its availability matters to the meaning
of readiness. Avoid readiness cascades (service A readiness → calls service B
readiness → calls service C …) without understanding the operational
consequences; prefer a lightweight check of the capability actually needed.

## Status Codes

Health endpoints return success when healthy and a non-success status when
unhealthy according to the configured probe policy; `HealthCheckOptions` allows
status-code mapping. Do not reuse business API status semantics mechanically for
orchestrator probes.

## Response Body

Keep probe responses small. When operators need detailed diagnostics, protect
that endpoint with network or authorization controls appropriate to the
environment.

## Exposure

Health endpoints often must be reachable by infrastructure without ordinary user
authentication. Choose exposure from the deployment topology: private/internal
network access, a dedicated management port, host restrictions, or authorization
where the probe infrastructure supports it.

## Startup Readiness

If initialization is asynchronous or slow, keep readiness unhealthy until the
required startup work has completed.

## Performance

Health checks may run frequently. Avoid expensive queries, long external
timeouts, large allocations, full business workflows, and Error-level logs for
every normal failed probe.

## Testing

Test meaningful health configuration when deployment relies on it: the live
endpoint responds when the process is healthy; readiness changes with a required
dependency; the response leaks no sensitive details; optional-dependency
behavior matches the intended readiness semantics. Do not build elaborate tests
for framework behavior the application does not customize.

## Anti-Patterns

Avoid using health checks as a code-quality grading system and remote dependency
chains without operational justification.
