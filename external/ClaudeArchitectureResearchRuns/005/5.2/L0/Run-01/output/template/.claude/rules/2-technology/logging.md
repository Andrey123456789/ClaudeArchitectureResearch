---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Level: 2 Technology | Owns: .NET logging API usage and Serilog provider integration | Scope: backend | Loads: path | Depends on: 0-core/logging-principles.md

# Logging Technology

- Default: log through `ILogger<T>` with structured message templates and
  stable property names; avoid string interpolation that turns structured
  values into opaque text.
- Default: configure Serilog through the DI-integrated
  `builder.Services.AddSerilog(...)` API, keep provider configuration (levels,
  sinks, overrides) in environment-aware configuration, and keep application
  code on `ILogger<T>` rather than Serilog APIs.

Technique: → `logging` skill (Serilog depth in its private reference).
