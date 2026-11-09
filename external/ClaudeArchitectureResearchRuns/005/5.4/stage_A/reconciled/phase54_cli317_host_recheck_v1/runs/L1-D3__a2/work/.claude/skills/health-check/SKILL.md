---
name: health-check
description: ASP.NET Core health-check technique. Use when implementing or reviewing AddHealthChecks/MapHealthChecks, liveness vs readiness endpoints, tagged dependency checks, database health, probe status mapping, health endpoint exposure, or health-check tests.
---

> Level: 2-technology · Owns: health-check technique · Loading: on demand

# Health Checks

Rules: `.claude/rules/0-core/http-api.md` § Health checks. Health checks answer whether the process is alive and whether this instance is ready to serve traffic.

## Setup

```csharp
builder.Services.AddHealthChecks();
var app = builder.Build();
app.MapHealthChecks("/health");
```

## Liveness

"Is the process alive enough that a restart is not needed?" — an endpoint that runs no dependency checks:

```csharp
app.MapHealthChecks("/health/live", new HealthCheckOptions { Predicate = _ => false });
```

## Readiness

"Can this instance serve the traffic it is responsible for?" — tag the checks that matter:

```csharp
builder.Services.AddHealthChecks().AddCheck<DatabaseHealthCheck>("database", tags: ["ready"]);

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

Include only dependencies required for meaningful readiness; an optional external service need not make the whole application unready. Keep readiness unhealthy until required asynchronous startup work completes — never misuse liveness for that (restart loops).

## Dependencies

- Database: a lightweight connectivity check; use provider/framework integrations where suitable.
- External services: only when their availability defines readiness; avoid readiness cascades (A → B → C) without understanding the operational consequences; prefer a lightweight check of the capability actually needed.

## Status codes and payload

Health endpoints return success when healthy and non-success when unhealthy per the probe policy (`HealthCheckOptions.ResultStatusCodes`); do not reuse business API status semantics mechanically. Keep probe responses small; put detailed diagnostics behind network or authorization controls for operators.

## Exposure

Probes often need access without user authentication: use private networks, a management port, host restrictions, or authorization the probe infrastructure supports, chosen by deployment topology. Prefer the orchestrator's native HTTP probes.

## Performance

Probes run frequently: avoid long external timeouts, large allocations, and Error-level logs for every normal failed probe.

## Testing

When deployment relies on health configuration, test that live responds while healthy, readiness follows required dependencies, responses leak nothing sensitive, and optional dependencies behave as intended. Skip elaborate tests for uncustomized framework behavior.

## Anti-patterns

Health checks as a quality grading system; writes or business transactions in probes; every dependency on liveness; expensive queries; secrets or stack traces in payloads; remote dependency chains without operational justification.
