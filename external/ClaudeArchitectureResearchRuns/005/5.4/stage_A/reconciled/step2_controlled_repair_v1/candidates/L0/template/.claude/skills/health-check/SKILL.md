---
name: health-check
description: >
  Use for ASP.NET Core health endpoints: AddHealthChecks/MapHealthChecks, liveness vs
  readiness, dependency checks, safe payloads, probe exposure, tests.
---

> Level: 2 Technology · Owns: health-check technique and examples (knowledge) · Scope: backend · Loads: on invocation · Depends on: .claude/rules/0-core/runtime-principles.md, .claude/rules/0-core/security-principles.md

# Health Checks

Policy owners: cheap/deterministic checks and liveness vs readiness semantics → `.claude/rules/0-core/runtime-principles.md` → Health checks; safe public responses → `0-core/security-principles.md`. Health checks answer whether the running instance is alive and/or ready to serve traffic. This skill is technique only.

## Basic setup

```csharp
builder.Services.AddHealthChecks();

var app = builder.Build();
app.MapHealthChecks("/health");
```

## Liveness

Liveness asks: *is the process alive enough that a restart is not required?*

```csharp
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false     // no dependency checks
});
```

A temporarily unavailable database or remote API should not restart the application.

## Readiness

Readiness asks: *can this instance currently serve the traffic it is responsible for?*

```csharp
builder.Services
    .AddHealthChecks()
    .AddCheck<DatabaseHealthCheck>("database", tags: ["ready"]);

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

Include only dependencies required for meaningful readiness; an optional external service need not make the whole instance unready. When initialization is asynchronous or slow, keep readiness unhealthy until required startup work completes (for example a startup check that turns healthy once initialization finished); liveness is not the mechanism for this, because failing it triggers restarts.

## Database and external dependencies

A database check performs a lightweight connectivity/availability check — no business queries, large scans, or writes; prefer provider/framework health-check integrations where suitable (for EF Core: `AddDbContextCheck<AppDbContext>()`). Check an external dependency only when its availability is part of what readiness means, and avoid cascades where A's readiness calls B's readiness calls C's.

## Status codes and payloads

Healthy → success status, unhealthy → non-success, configurable through `HealthCheckOptions.ResultStatusCodes`; probe semantics are not business API semantics. Keep probe responses small. If detailed diagnostics are useful to operators, put them on a protected endpoint (network or authorization controls).

## Exposure

Probes are often reached by infrastructure without user authentication. Choose exposure by topology: private/internal network, a dedicated management port, host restrictions (`RequireHost`), or authorization where the probe infrastructure supports it. Prefer the orchestrator's native HTTP probes; container images may lack `curl`/`wget` (`docker` skill).

## Performance

Probes run frequently: avoid expensive queries, long external timeouts, large allocations, full workflows, and Error-level logs for every normal failed probe.

## Testing

When deployment relies on the configuration, test that the live endpoint responds, readiness changes with a required dependency, responses leak nothing sensitive, and optional dependencies behave as intended. Do not test framework behavior the application does not customize.

## Anti-patterns

Health checks as a code-quality grading system; remote dependency chains without operational justification.
