---
name: health-check
description: >
  Use for health endpoints: AddHealthChecks, MapHealthChecks, liveness vs
  readiness, dependency checks, status mapping, safe responses, probe exposure.
---
> Level: 2-technology | Owns: ASP.NET Core health-check technique | Scope: backend | Loads: on demand (skill)

# Health Checks

Policy: `hosting.md` (cheap and deterministic, liveness vs readiness, no
internals in public responses).

## Basic setup

```csharp
builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapHealthChecks("/health");
```

## Liveness

Answers "is the process alive enough that a restart is not required?" — avoid
databases and remote APIs:

```csharp
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false
});
```

## Readiness

Answers "can this instance serve the traffic it is responsible for?":

```csharp
builder.Services
    .AddHealthChecks()
    .AddCheck<DatabaseHealthCheck>("database", tags: ["ready"]);

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

Include only dependencies required for meaningful readiness; an optional
external service need not make the whole instance unready. Keep readiness
unhealthy until required asynchronous startup work completes — never use
liveness for that (restart loops).

## Database and external dependencies

A database check performs a lightweight connectivity check (prefer the
provider's health-check integration) — no business queries, table scans, or
writes. Check an external dependency only when its availability is part of
readiness; avoid readiness cascades (A → B → C) without understanding their
operational effect.

## Status codes and payloads

Healthy returns success and unhealthy a non-success status per the probe
policy (`HealthCheckOptions.ResultStatusCodes`); do not reuse business API
status semantics for probes. Keep probe bodies small; when operators need
detailed output, protect that endpoint.

## Exposure

Infrastructure often needs probes without user authentication. Choose by
topology: internal network access, a management port, host restrictions
(`RequireHost`), or authorization the probe infrastructure supports.

## Performance

Probes run frequently: avoid expensive queries, long external timeouts, large
allocations, business workflows, and Error-level logs for every failed probe.

## Testing

When deployment relies on the configuration: live responds while the process is
healthy, readiness follows a required dependency, responses do not leak
details, optional dependencies behave as intended. Do not test uncustomized
framework behavior.

## Anti-patterns

Health checks as a quality score; writes or business transactions in probes;
every dependency on liveness; expensive queries; secrets or stack traces in
payloads; unjustified remote dependency chains.
