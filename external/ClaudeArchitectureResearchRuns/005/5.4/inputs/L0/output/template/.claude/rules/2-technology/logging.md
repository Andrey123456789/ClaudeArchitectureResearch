---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Level: 2 Technology · Owns: logging API and provider bindings — `ILogger<T>` structured logging, Serilog integration · Scope: backend · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/0-core/logging-principles.md

# Logging Bindings

Sensitive-data, payload, and log-once principles: `0-core/logging-principles.md`. Technique: the `logging` skill (Serilog depth in its private reference).

- Use `ILogger<T>` with structured message templates and stable property names; avoid string interpolation that turns structured values into opaque text (default).
- When Serilog is configured, use the DI-integrated `builder.Services.AddSerilog(...)` approach (not `UseSerilog()`), keep levels, sinks, and overrides in environment-aware configuration, and keep application code depending on `ILogger<T>` rather than Serilog APIs (default).
