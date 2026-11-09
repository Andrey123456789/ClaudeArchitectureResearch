---
paths:
  - "backend/**/*.cs"
---

> Kind: STD | Scope: backend | Owner: C# code conventions, async and cancellation, time, optimization discipline | Loading: path-scoped

# C# Standard

Platform and language version: D-03.

Enforced by: `.editorconfig` (formatting and naming checks).

## Conventions

- Default: follow the repository's existing conventions and `.editorconfig`; use modern C# when it improves clarity, but do not mechanically modernize working code. Consistency and readability matter more than using every language feature.
- Do not perform style-only rewrites outside the requested change unless explicitly asked; avoid mixing large formatting or modernization changes with functional work.
- Default for new code: file-scoped namespaces when consistent with the project; one primary top-level type per file, with the file named after it (small private or nested supporting types may stay with their owner); the `Async` suffix on `Task`/`ValueTask`-returning methods unless an existing or framework contract makes it inappropriate. Do not reorganize an existing file merely to satisfy a preferred member ordering.
- Prefer primary constructors for simple dependency injection or initialization, and a regular constructor when validation or initialization is non-trivial, explicit fields read better, or the codebase consistently uses that style; do not convert constructors mechanically.
- Prefer records where value semantics and immutability are intended (many DTOs, genuine Value Objects) and classes where identity, mutable lifecycle, inheritance or framework behavior matters; do not turn every DTO or Domain type into a record.
- Keep implementation details non-public unless they belong to the project's public API; use `sealed` when it communicates deliberate design intent, not as a speculative optimization.
- Prefer `var` when the type is obvious from the right-hand side or unimportant, and an explicit type when it aids understanding. Use standard .NET naming (PascalCase for types and members, camelCase for parameters and locals, meaningful names over abbreviations); private-field naming follows the repository's convention.

## Async and cancellation

- Use async APIs for asynchronous I/O and never block them with `.Result`, `.Wait()` or similar sync-over-async patterns.
- Propagate `CancellationToken` through asynchronous operations when cancellation is meaningful; do not add cancellation parameters to purely synchronous code without a use case.

## Time

- Default: use `TimeProvider` for application logic whose behavior depends on the current clock and needs deterministic tests. Stored timestamps and explicit dates are not clock dependencies; do not replace every `DateTime`/`DateTimeOffset` mechanically.

## Optimization

- Default: clear, correct code first. Do not introduce specialized optimizations without a concrete reason, and prefer measurement or profiling evidence for non-trivial optimization.
- Default: compiled queries, `ValueTask<T>`, `ArrayPool<T>`/`MemoryPool<T>` and manual pooling, custom serialization, aggressive caching and raw SQL for performance are introduced only for a measured or clearly demonstrated need.
