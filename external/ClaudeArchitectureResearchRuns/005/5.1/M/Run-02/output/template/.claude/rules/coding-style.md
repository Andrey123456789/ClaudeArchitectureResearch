---
paths:
  - "backend/**/*.cs"
---

> Owner: C# conventions, file and async naming, using-directive hygiene, style scope discipline, typed configuration, logging call style | Scope: backend | Loads: path (backend C#); read explicitly by `verify` | Enforced: `.editorconfig` (format and naming), `verify` final diff review

# C# Coding Style

Technique for constructors, records, visibility, `var`, and recent language
features: `modern-csharp` skill. Formatting and naming conventions:
`.editorconfig`.

## General Principle

- Default: follow the repository's existing conventions and `.editorconfig`. Use
  modern C# when it improves clarity, but do not rewrite working code solely to
  use newer syntax.
- Do not perform style-only rewrites outside the requested change unless
  explicitly asked; avoid mixing large formatting or modernization changes with
  functional work.

## Files, Namespaces, and Async Naming

- Default for new C# code: file-scoped namespaces when consistent with the
  project; one primary top-level type per file, with the file named after it
  (small private or nested supporting types may stay with their owner); the
  `Async` suffix on `Task`/`ValueTask`-returning methods unless an existing or
  framework contract makes it inappropriate.

## Using Directives

- For every C# file created or modified by the task, remove unused or redundant
  `using` directives before completion, including imports already provided by
  implicit or global usings unless needed for clarity or disambiguation. Do not
  perform an unrelated repository-wide using cleanup, and verify the changed
  files instead of assuming tooling removed every redundant import.

## Configuration

- Default: bind structured configuration consumed by services to strongly typed
  options, and validate settings at startup when missing or invalid values would
  prevent correct or secure operation; avoid scattering string-based
  `IConfiguration` lookups through services (direct `IConfiguration` use in the
  composition root and registration code is fine). Technique: `configuration`
  skill.

## Logging Calls

- Default: log through `ILogger<T>` with structured message templates and stable
  property names; avoid string interpolation that turns structured values into
  opaque text.
- Default: when Serilog is configured, register it with the DI-integrated
  `AddSerilog()` approach and keep levels and sinks in environment-aware
  configuration; Serilog-specific APIs stay at composition and provider
  boundaries. Technique: `logging` skill.
