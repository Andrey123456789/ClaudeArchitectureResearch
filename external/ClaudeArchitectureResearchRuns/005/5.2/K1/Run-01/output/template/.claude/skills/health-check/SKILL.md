---
name: health-check
description: Use when implementing or reviewing ASP.NET Core health endpoints — AddHealthChecks/MapHealthChecks, liveness versus readiness, tagged dependency checks, status mapping, safe response payloads, probe exposure and health-check tests.
---
Kind: KNW | Scope: backend | Capability: — | Loading: on invocation

# Health Checks

Rules: `.claude/rules/backend/http-api.md` → Health checks (cheap and deterministic, liveness versus readiness, no exposed internals). Health checks answer whether the running application is alive and/or ready to serve traffic; distinguish liveness from readiness when the deployment infrastructure benefits from it.

## Basic setup

```csharp
builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapHealthChecks("/health");
```

## Liveness

Liveness answers: "Is this process alive enough that restarting it is not required?"

```csharp
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false
});
```

The exact probe configuration varies by hosting environment.

## Readiness

Readiness answers: "Can this instance currently serve the traffic it is responsible for?"

```csharp
builder.Services
    .AddHealthChecks()
    .AddCheck<DatabaseHealthCheck>("database", tags: ["ready"]);

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

Include only dependencies required for meaningful readiness; an optional external service should not necessarily make the whole application unready. If initialization is asynchronous or slow, keep readiness unhealthy until the required startup work completes (not liveness, which can cause restart loops).

## Database and external dependencies

A database check performs a lightweight connectivity check through provider or framework health-check integration where suitable, never a business query, table scan or write. Check an external dependency only when its availability matters to readiness, and avoid readiness cascades (service A readiness → service B readiness → ...) without understanding their operational consequences; prefer a lightweight check of the capability actually needed.

## Status codes and response body

Health endpoints return success when healthy and a non-success status when unhealthy according to the configured probe policy (`HealthCheckOptions.ResultStatusCodes`); do not reuse business API status semantics mechanically for orchestrator probes. Keep probe responses small. When operators need diagnostic detail, protect that endpoint with network or authorization controls appropriate to the environment.

## Exposure

Probes often need to be reachable by infrastructure without user authentication. Choose exposure by deployment topology: private or internal network access, a dedicated management port, host restrictions (`RequireHost`), or authorization when the probe infrastructure supports it.

## Performance

Health checks may run frequently. Avoid expensive queries, long external timeouts, large allocations, full business workflows, and Error-level logs for every normal failed probe.

## Testing

Test health configuration when the deployment relies on it: the live endpoint responds when the process is healthy, readiness changes with a required dependency, responses do not leak sensitive details, and optional-dependency behavior matches the intended readiness semantics. Do not build elaborate tests for framework behavior the application does not customize.

## Anti-patterns

Review checks; `http-api.md` owns each rule unless noted:

- Health checks used as a code-quality grading system, or running business transactions, writes or expensive queries?
- Every dependency on liveness?
- Secrets, connection details or stack traces in responses?
- Remote dependency chains without operational justification?
