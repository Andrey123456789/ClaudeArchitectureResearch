---
name: health-check
description: Use when implementing or reviewing health endpoints — liveness vs. readiness, dependency checks, status mapping, safe payloads, probe exposure, startup readiness.
---

> Kind: KNW | Scope: backend | Owner: health-check technique with examples | Loading: on demand (model-invoked knowledge)

# Health Checks

Rules: `rules/backend/hosting.md` § Health checks.

Health checks answer whether the running application is alive and/or ready to serve traffic. Distinguish liveness from readiness when the deployment infrastructure benefits from it.

## Basic setup

```csharp
builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapHealthChecks("/health");
```

## Liveness

Liveness asks roughly: is the process alive enough that a restart is not required? Dependency rules for liveness and readiness: `rules/backend/hosting.md` § Health checks.

```csharp
app.MapHealthChecks(
    "/health/live",
    new HealthCheckOptions
    {
        Predicate = _ => false
    });
```

## Readiness

Readiness asks: can this instance currently serve the traffic it is responsible for? Tag the checks that define it, and include only dependencies required for meaningful readiness — an optional external service need not make the whole application unready.

```csharp
builder.Services
    .AddHealthChecks()
    .AddCheck<DatabaseHealthCheck>(
        "database",
        tags: ["ready"]);

app.MapHealthChecks(
    "/health/ready",
    new HealthCheckOptions
    {
        Predicate = check => check.Tags.Contains("ready")
    });
```

When initialization is asynchronous or slow, keep readiness unhealthy until required startup work completes; using liveness for this causes restart loops.

## Database and external dependencies

A database check is a lightweight connectivity/availability check (`rules/backend/hosting.md` § Health checks); provider integrations help. Check an external dependency only when its availability defines readiness, prefer a lightweight check of the needed capability, and avoid readiness chains (service A → B → C) without understanding their operational consequences.

## Status codes and payloads

Health endpoints return success when healthy and a non-success status when unhealthy under the probe policy; `HealthCheckOptions` maps statuses. Business API status semantics do not transfer mechanically to orchestrator probes. Keep probe responses small; operator-level diagnostic detail goes behind network or authorization controls appropriate to the environment.

## Exposure

Probes usually need to be reachable by infrastructure without user authentication. Options: private/internal network access, a dedicated management port, host restrictions, authorization when the probe infrastructure supports it. Detailed diagnostics are not published unauthenticated on the internet.

## Performance

Probes run frequently: avoid expensive queries, long external timeouts, large allocations, business workflows and Error-level logs for every normal failed probe.

## Testing

When deployment relies on health configuration, test that the live endpoint responds while the process is healthy, readiness follows a required dependency, responses leak nothing sensitive, and optional dependencies behave as intended. Uncustomized framework behavior needs no elaborate tests.

## Common mistakes

Health checks as a code-quality grading system; database writes or business transactions from probes; every dependency on liveness; expensive queries; secrets or stack traces in payloads; remote dependency chains without operational justification.
