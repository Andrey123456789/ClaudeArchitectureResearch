---
name: health-check
description: >
  Health endpoints: AddHealthChecks, MapHealthChecks, liveness vs. readiness,
  tags, database and dependency checks, status mapping, safe payloads,
  orchestrator probes.
---

> **Knowledge skill** · Owns: health-check technique and examples · Scope: backend · Loading: on demand

# Health Checks

## Rules

Rules: `api.md` → Health Checks (cheap and deterministic, liveness vs. readiness,
safe public responses). Health checks answer whether the running application is
alive and/or ready to serve traffic; distinguish liveness from readiness when the
deployment infrastructure benefits from it.

## Basic Setup

```csharp
builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapHealthChecks("/health");
```

Use more specific readiness/liveness endpoints when appropriate.

## Liveness

Liveness answers approximately:

> Is this application process alive enough that restarting it is not currently
> required?

A liveness probe should usually avoid dependencies such as databases and remote
APIs.

Example:

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

Readiness answers approximately:

> Can this instance currently serve the traffic for which it is responsible?

Register readiness checks with tags:

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

Include only dependencies required for meaningful readiness.

An optional external service should not necessarily make the whole application
unready.

## Database Health

A database health check performs a lightweight connectivity/availability check
(`api.md` → Health Checks); use provider/framework health-check integration where
suitable.

## External Dependencies

Check an external dependency only when its availability is important to the
meaning of readiness.

Avoid building a dependency cascade where:

```text
service A readiness
→ calls service B readiness
→ calls service C readiness
→ ...
```

without understanding the operational consequences.

Prefer a lightweight check of the capability the application genuinely needs.

## Status Codes

Health endpoints normally return success when considered healthy and a
non-success status when unhealthy according to the configured probe policy.

ASP.NET Core allows status-code mapping through `HealthCheckOptions`.

Do not reuse normal business API status-code semantics mechanically for
orchestrator probes.

## Response Body

Keep probe responses small.

Public content limits: `api.md` → Health Checks. If diagnostic details are useful
for operators, serve them from a separate endpoint protected by network or
authorization controls appropriate to the environment.

## Authentication and Exposure

Health endpoints often need to be reachable by infrastructure without ordinary
user authentication.

Choose exposure according to deployment topology.

Possible approaches include:

- private/internal network access;
- dedicated management port;
- host restrictions;
- authorization where the probe infrastructure supports it.

Do not blindly put public unauthenticated diagnostic details on the internet.

## Startup Readiness

Rule: `api.md` → Health Checks. Implement it with a readiness check that reports
unhealthy until the startup work signals completion (for example a singleton
flag set by the hosted service that performs initialization); never use liveness
for this, because that causes restart loops.

## Performance

Health checks may be called frequently.

Avoid:

- expensive queries;
- long external timeouts;
- large object allocation;
- full business workflows;
- writing logs at Error level for every normal failed probe.

## Testing

Test meaningful health configuration when deployment relies on it.

Useful cases include:

- live endpoint responds when the process is healthy;
- readiness changes according to a required dependency;
- response does not leak sensitive details;
- optional dependency behavior matches intended readiness semantics.

Do not create elaborate tests for framework behavior that the application does
not customize.

## Anti-Patterns

Avoid:

- using health checks as a code-quality grading system;
- every dependency on liveness;
- remote dependency chains with no operational justification.
