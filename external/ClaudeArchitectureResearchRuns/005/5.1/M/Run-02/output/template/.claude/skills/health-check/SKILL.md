---
name: health-check
description: >
  Use when adding or changing health endpoints:
  AddHealthChecks/MapHealthChecks, liveness vs. readiness, tags, database
  checks, startup readiness, status mapping, probe exposure, health-check
  tests.
---

> Owner: health-check implementation technique (normative policy lives in rules) | Scope: backend | Loads: on demand — knowledge | Enforced: none

# Health Checks

Policy: `.claude/rules/api.md` § Health Checks (cheap and deterministic,
liveness vs. readiness semantics, safe public output).

Health checks answer whether the running application is alive and/or ready to
serve traffic. Distinguish liveness from readiness when the deployment
infrastructure benefits from it.

## Basic Setup

```csharp
builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapHealthChecks("/health");
```

## Liveness

Liveness asks roughly: is this process alive enough that restarting it is not
currently required? A liveness probe usually avoids databases and remote APIs:

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

Readiness asks roughly: can this instance currently serve the traffic it is
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
external service need not make the whole application unready.

## Database Health

Use a lightweight connectivity check — provider or framework integration where
suitable, for example EF Core's `AddDbContextCheck<AppDbContext>()`
(`Microsoft.Extensions.Diagnostics.HealthChecks.EntityFrameworkCore`) — rather
than business queries or table scans.

## External Dependencies

Check an external dependency only when its availability is part of what readiness
means, and prefer a lightweight check of the capability actually needed. Avoid
unexamined cascades:

```text
service A readiness
→ calls service B readiness
→ calls service C readiness
→ ...
```

## Startup Readiness

When initialization is asynchronous or slow, keep readiness unhealthy until the
required startup work completes — for example a startup health check that flips
to healthy once an initialization flag is set. Using liveness for this causes
restart loops.

## Status Codes

Health endpoints return success when healthy and a non-success status when
unhealthy according to the probe policy; `HealthCheckOptions.ResultStatusCodes`
customizes the mapping. Business API status semantics do not carry over to
orchestrator probes mechanically.

## Response Body and Exposure

Keep probe responses small. If operators need detailed diagnostics, put them on a
protected endpoint (network restriction, management port, host filtering, or
authorization the probe infrastructure supports):

```csharp
app.MapHealthChecks("/health/details", new HealthCheckOptions
{
    ResponseWriter = WriteDetailedResponseAsync
})
.RequireHost("*:8081")
.RequireAuthorization("Operators");
```

Health endpoints often must be reachable by infrastructure without ordinary user
authentication; choose exposure from the deployment topology.

## Performance

Probes may be called frequently: avoid expensive queries, long external
timeouts, large allocations, and Error-level logs for every normal failed probe.

## Testing

Test health configuration that deployment relies on: the live endpoint responds
when the process is healthy, readiness follows a required dependency, the
response does not leak sensitive details, optional-dependency behavior matches
intended readiness semantics. Skip elaborate tests of framework behavior the
application does not customize.

## Common Mistakes

- using health checks as a code-quality grading system;
- every dependency on liveness;
- remote dependency chains with no operational justification.
