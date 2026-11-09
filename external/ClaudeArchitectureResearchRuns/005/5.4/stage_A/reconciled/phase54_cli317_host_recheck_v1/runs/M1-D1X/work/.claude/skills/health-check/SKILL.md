---
name: health-check
description: >
  Use for ASP.NET Core health endpoints: AddHealthChecks/MapHealthChecks,
  liveness vs. readiness, dependency checks, status mapping, safe payloads,
  probe exposure.
---

> Knowledge skill · Health-check technique · Policy: `.claude/rules/api.md` § Health Checks

# Health Checks

Health checks answer whether the running application is alive and/or ready to
serve traffic. Distinguish liveness from readiness when the deployment
infrastructure benefits from it.

## Basic Setup

```csharp
builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapHealthChecks("/health");
```

Use more specific readiness and liveness endpoints when appropriate.

## Liveness

Liveness asks: is this process alive enough that restarting it is not
required? A liveness probe usually avoids databases and remote APIs:

```csharp
app.MapHealthChecks(
    "/health/live",
    new HealthCheckOptions
    {
        Predicate = _ => false
    });
```

The exact probe configuration varies by hosting environment.

## Readiness

Readiness asks: can this instance currently serve the traffic it is
responsible for? Register readiness checks with tags:

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

## Startup Readiness

If initialization is asynchronous or takes meaningful time, readiness stays
unhealthy until the required startup work has completed. Do not use liveness for
this; it causes restart loops.

## Database Health

A database check performs a lightweight connectivity/availability check —
no expensive business queries, large scans, or writes. Use provider/framework
health-check integration where suitable.

## External Dependencies

Check an external dependency only when its availability is important to the
meaning of readiness. Avoid readiness cascades where service A's readiness calls
B's, which calls C's, without understanding the operational consequences;
prefer a lightweight check of the capability actually needed.

## Status Codes

Health endpoints return success when healthy and a non-success status when
unhealthy according to the configured probe policy; `HealthCheckOptions` allows
status-code mapping. Do not reuse business API status-code semantics
mechanically for orchestrator probes.

## Response Body

Keep probe responses small. If operators need diagnostic detail, protect that
endpoint with network or authorization controls appropriate to the environment.

## Authentication and Exposure

Health endpoints often need to be reachable by infrastructure without user
authentication. Choose exposure by deployment topology: private/internal
network access, a dedicated management port, host restrictions, or
authorization where the probe infrastructure supports it.

## Performance

Health checks may be called frequently: avoid expensive queries, long external
timeouts, large allocations, full business workflows, and Error-level logs for
every normal failed probe.

## Testing

Test meaningful health configuration when deployment relies on it: the live
endpoint responds when healthy, readiness changes with a required dependency,
responses do not leak sensitive details, optional-dependency behavior matches
the intended semantics. Do not build elaborate tests for framework behavior the
application does not customize.

## Review Checks

Check-by-reference against `api.md` § Health Checks: health checks used as a
code-quality grading system; database writes or business transactions from
probes; every dependency on liveness; expensive queries; secrets or stack traces
in responses; remote dependency chains without operational justification.
