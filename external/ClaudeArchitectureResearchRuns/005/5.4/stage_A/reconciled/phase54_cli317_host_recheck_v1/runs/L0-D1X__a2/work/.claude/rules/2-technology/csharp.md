---
paths:
  - "backend/**/*.cs"
---

> Level: 2 Technology · Owns: C# and .NET conventions — style scope, files and naming, async and cancellation, time, outbound HTTP client lifetime, typed configuration · Scope: backend · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/0-core/runtime-principles.md

# C# and .NET Conventions

Mechanical formatting lives in `.editorconfig`. Technique: `modern-csharp`, `configuration`, `httpclient-factory`, `dependency-injection` skills. Import cleanup of changed files: `verify`.

## Style

- Follow the repository's existing conventions and `.editorconfig`. Use modern C# when it improves clarity, but do not mechanically modernize working code (default).
- Do not perform style-only rewrites outside the requested change unless explicitly asked; avoid mixing large formatting or modernization changes with functional work.
- For new code, prefer file-scoped namespaces when consistent with the project, normally keep one primary top-level type per file with a matching file name, and use the `Async` suffix for `Task`/`ValueTask`-returning methods unless an existing or framework contract makes that inappropriate (default).

## Async and cancellation

- Use async APIs for asynchronous I/O and never block them with `.Result`, `.Wait()`, or similar sync-over-async patterns.
- Propagate `CancellationToken` through asynchronous operations when cancellation is meaningful; do not add cancellation parameters to purely synchronous code without a use case.

## Time

- Use `TimeProvider` for application logic that depends on the current clock and needs deterministic testing; do not mechanically replace explicit or stored timestamps (default).

## Outbound HTTP

- Never create and dispose a new `HttpClient` per request; use `IHttpClientFactory` or another appropriate long-lived client strategy.

## Configuration

- Prefer strongly typed options for structured service configuration and validate settings at startup when missing or invalid values prevent correct or secure operation; avoid scattering string-based `IConfiguration` lookups through services (default).
