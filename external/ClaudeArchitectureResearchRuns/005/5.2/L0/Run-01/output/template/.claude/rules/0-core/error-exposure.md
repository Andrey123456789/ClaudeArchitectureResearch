---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Level: 0 Core | Owns: public failure exposure and cancellation classification | Scope: backend | Loads: path | Depends on: none

# Error Exposure

- Do not expose stack traces, SQL details, connection strings, internal paths,
  secret values, or sensitive exception details in public API errors.
  Development diagnostics may show more through development tooling; public
  contracts stay safe.
- Do not map normal client-request cancellation to a generic `500` response or
  log it as an unhandled application failure.
