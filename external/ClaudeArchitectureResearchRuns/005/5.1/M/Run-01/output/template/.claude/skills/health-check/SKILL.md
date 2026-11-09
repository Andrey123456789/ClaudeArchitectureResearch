---
name: health-check
description: >
  Use when implementing or reviewing health endpoints: AddHealthChecks and
  MapHealthChecks, liveness vs. readiness endpoints, tagged dependency checks,
  database health checks, status-code mapping, probe exposure, startup
  readiness, or health-check tests.
---

> Owns: ASP.NET Core health-check technique | Scope: backend | Loads: on demand (knowledge skill)

# Health Checks

Policy owners: cheap/deterministic checks, liveness vs. readiness semantics, safe
public output → `.claude/rules/api.md` (Health Checks). Container probe wiring:
`docker`.

Liveness asks "is this process alive enough that restarting it is not
required?"; readiness asks "can this instance serve the traffic it is
responsible for right now?".

## Basic Setup

```csharp
builder.Services.AddHealthChecks();
var app = builder.Build();
app.MapHealthChecks("/health");
```

## Liveness and Readiness Endpoints

```csharp
builder.Services
    .AddHealthChecks()
    .AddCheck<DatabaseHealthCheck>("database", tags: ["ready"]);

app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false                       // process only, no dependencies
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

Include only dependencies required for meaningful readiness; an optional
external service need not make the whole instance unready. Avoid readiness
cascades (A's readiness calling B's calling C's) without understanding the
operational consequences.

## Database Check

For EF Core, `.AddDbContextCheck<AppDbContext>(tags: ["ready"])` or a custom
check calling `Database.CanConnectAsync` gives a lightweight connectivity check
(what checks may do: `api.md`).

## Startup Readiness

When initialization is asynchronous or slow, keep readiness unhealthy until the
required startup work completes (for example a check reading a flag set by the
startup task). Use readiness, not liveness, for this: a failing liveness probe
restarts the process.

## Status Codes and Output

Health endpoints return success when healthy and non-success when unhealthy
according to the probe policy; adjust with `HealthCheckOptions.ResultStatusCodes`
when the orchestrator expects different codes. Keep probe responses small (the
default plain-text status). If operators need details, put a detailed writer on
a protected endpoint (network restriction, management port, host filter, or
authorization the probe infrastructure supports).

## Exposure

Probes often need to bypass normal user authentication; choose exposure from
deployment topology (private network, management port via `RequireHost`, or
authorization) rather than publishing diagnostics publicly.

## Performance

Probes run frequently: avoid expensive queries, long external timeouts, large
allocations, and Error-level logs for every normal failed probe.

## Testing

When deployment relies on health configuration, test that the live endpoint
answers while the process is healthy, readiness follows a required dependency,
responses do not leak details, and optional dependencies behave as intended. Do
not test unmodified framework behavior.
