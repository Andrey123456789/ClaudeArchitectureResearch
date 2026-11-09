---
name: health-check
description: Use when implementing or reviewing application health endpoints — AddHealthChecks/MapHealthChecks, liveness vs readiness, dependency and database checks, status mapping, response payloads, endpoint exposure, startup readiness, health-check tests.
---
<!-- Kind: KNW | Scope: backend | Owns: ASP.NET Core health-check technique and examples | Loads: on demand (model-invoked) -->
# Health Checks

Standards: `rules/backend/operations.md` § Health Checks (cheap and deterministic, distinct liveness/readiness semantics, safe public responses).

Health checks answer whether the running application is alive and/or ready to serve traffic. Distinguish liveness from readiness when the deployment infrastructure benefits from it.

## Basic Setup

```csharp
builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapHealthChecks("/health");
```

Use more specific readiness/liveness endpoints when appropriate.

## Liveness

Liveness answers approximately: *is this process alive enough that restarting it is not currently required?* It usually avoids databases and remote APIs.

```csharp
app.MapHealthChecks(
    "/health/live",
    new HealthCheckOptions
    {
        Predicate = _ => false
    });
```

The exact probe configuration varies by hosting environment; a temporarily unavailable external dependency is no reason to restart the application.

## Readiness

Readiness answers approximately: *can this instance currently serve the traffic it is responsible for?* Register readiness checks with tags:

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

Include only dependencies required for meaningful readiness; an optional external service need not make the whole application unready.

## Database Health

A lightweight connectivity/availability check — no expensive business queries, no large table scans, no data modification. Prefer provider/framework health-check integration where suitable.

## External Dependencies

Check an external dependency only when its availability matters to the meaning of readiness. Avoid dependency cascades

```text
service A readiness
→ calls service B readiness
→ calls service C readiness
→ ...
```

without understanding the operational consequences; prefer a lightweight check of the capability the application genuinely needs.

## Status Codes

Health endpoints return success when healthy and a non-success status when unhealthy according to the probe policy; ASP.NET Core maps statuses through `HealthCheckOptions`. Business API status semantics do not apply mechanically to orchestrator probes.

## Response Body

Keep probe responses small. When detailed diagnostics are useful to operators, protect that endpoint with network or authorization controls appropriate to the environment; connection strings, credentials, raw exception details and sensitive infrastructure topology stay out.

## Authentication and Exposure

Health endpoints often need to be reachable by infrastructure without ordinary user authentication. Choose exposure by deployment topology: private/internal network access, a dedicated management port, host restrictions, or authorization where the probe infrastructure supports it.

## Startup Readiness

Semantics: `rules/backend/operations.md` § Health Checks. Implementation: when initialization is asynchronous or slow, let the initialization work set a startup-complete flag that a readiness-tagged check reports, so liveness stays independent of startup.

## Performance

Probes may be called frequently: avoid expensive queries, long external timeouts, large allocations, full business workflows, and Error-level logs for every normal failed probe.

## Testing

Test health configuration when deployment relies on it: the live endpoint responds when the process is healthy; readiness changes with a required dependency; the response leaks nothing sensitive; optional dependency behavior matches the intended readiness semantics. Framework behavior the application does not customize needs no elaborate tests.

## Anti-Patterns

Avoid health checks as a code-quality grading system, database writes or business transactions from probes, every dependency on liveness, expensive queries, secrets in payloads, remote dependency chains without operational justification, and stack traces from health endpoints.
