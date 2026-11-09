---
name: health-check
description: >
  Use for health endpoints: AddHealthChecks/MapHealthChecks, liveness vs.
  readiness, database and dependency checks, probe exposure, startup
  readiness.
---

> Knowledge skill. Owns: health-check technique and examples · Scope: backend · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/api.md

# Health Checks

Rules: `api.md` (Health Checks — cheap and deterministic, liveness vs.
readiness, safe public responses). Health checks answer whether the running
application is alive and/or ready to serve traffic; distinguish liveness from
readiness when the deployment infrastructure benefits from it.

## Basic Setup

```csharp
builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapHealthChecks("/health");
```

## Liveness

Liveness asks roughly: is the process alive enough that restarting it is not
required? A liveness probe usually checks no databases or remote APIs:

```csharp
app.MapHealthChecks(
    "/health/live",
    new HealthCheckOptions
    {
        Predicate = _ => false
    });
```

Probe configuration varies by hosting environment.

## Readiness

Readiness asks roughly: can this instance serve the traffic it is responsible
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

A lightweight connectivity/availability check, ideally through
provider/framework health-check integration — no business queries, table scans,
or data modification.

## External Dependencies

Check an external dependency only when its availability is part of what
readiness means, and avoid unexamined cascades:

```text
service A readiness
-> calls service B readiness
-> calls service C readiness
-> ...
```

Prefer a lightweight check of the capability the application genuinely needs.

## Status Codes

Health endpoints return success when healthy and a non-success status when
unhealthy according to the probe policy; ASP.NET Core maps statuses through
`HealthCheckOptions`. Do not reuse business API status-code semantics
mechanically for orchestrator probes.

## Response Body and Exposure

Keep probe responses small. When operators need diagnostic detail, protect that
endpoint with network or authorization controls. Probes often must be reachable
without user authentication; choose exposure by topology — private/internal
network access, a dedicated management port, host restrictions, or
authorization where the probe infrastructure supports it.

## Startup Readiness

When initialization is asynchronous or slow, keep readiness unhealthy until
required startup work completes; using liveness for this can cause restart
loops.

## Performance

Health checks may run frequently: avoid expensive queries, long external
timeouts, large allocations, business workflows, and Error-level logs for every
failed probe that is expected during routine operation.

## Testing

Test health configuration that deployment relies on: the live endpoint responds
when the process is healthy; readiness changes with a required dependency; the
response does not leak sensitive details; optional dependencies behave as
intended. Skip elaborate tests of framework behavior the application does not
customize.

## Anti-Patterns

- health checks used as a code-quality grading system;
- database writes or business transactions from probes;
- every dependency on liveness;
- remote dependency chains without operational justification;
- application stack traces in health responses.
