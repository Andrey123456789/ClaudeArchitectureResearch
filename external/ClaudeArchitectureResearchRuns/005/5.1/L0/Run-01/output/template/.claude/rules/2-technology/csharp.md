---
paths:
  - "backend/**/*.cs"
---

> Level: 2 Technology · Owns: C# and .NET runtime conventions · Scope: backend · Loads: path; read explicitly by `verify`

# C# and .NET Conventions

## Style and scope

- **Default:** follow the repository's existing conventions and `.editorconfig`. Use modern C# features when they improve clarity; do not rewrite working code merely to use newer syntax. Consistency and readability outrank use of language features.
- **Default:** for new code, use file-scoped namespaces when consistent with the project; keep one primary top-level type per file with a matching file name (small private or nested supporting types may stay with their owner); give `Task`/`ValueTask`-returning methods the `Async` suffix unless an existing interface or framework contract makes that inappropriate.
- **Must**, for every C# file created or modified by the task, remove unused or redundant `using` directives before completion — including imports already provided by implicit or global usings unless needed for clarity or disambiguation. Verify the changed files instead of assuming tooling removed them, and do not perform an unrelated repository-wide cleanup.
- **Must not** perform style-only rewrites outside the requested change unless explicitly asked; avoid mixing large formatting or modernization changes with functional work.

## Async, cancellation and time

- **Must** use async APIs for asynchronous I/O and never block on them with `.Result`, `.Wait()`, `GetAwaiter().GetResult()` or similar sync-over-async patterns.
- **Must** propagate `CancellationToken` through asynchronous operations when cancellation is meaningful; do not add cancellation parameters to purely synchronous code without a use case.
- **Default:** use `TimeProvider` for application logic that depends on the current time and needs deterministic tests; do not mechanically replace stored or explicit timestamps.

## Runtime services

- **Must not** create and dispose a new `HttpClient` per request; use `IHttpClientFactory` (typed, named or keyed clients) or another appropriate long-lived client strategy.
- **Default:** bind structured service configuration to strongly typed options (`AddOptions<T>().BindConfiguration(...)`) and validate at startup (`ValidateOnStart`) when missing or invalid values prevent correct or secure operation. Avoid scattering string-based `IConfiguration` lookups through services; composition code may use `IConfiguration` directly.
- **Default:** log through `ILogger<T>` with structured message templates and stable property names; avoid string interpolation that turns structured values into opaque text.

Technique: `modern-csharp`, `configuration`, `dependency-injection`, `httpclient-factory`, `logging` skills.
