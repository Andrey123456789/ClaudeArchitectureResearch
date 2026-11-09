---
paths:
  - "backend/**"
---
<!-- Kind: STD | Scope: backend | Owns: C# conventions and style guidance, async/cancellation, time, optimization discipline | Loads: path-scoped (backend/**) -->
# Backend C# Code Standards

## Conventions

- **Default:** follow the repository's existing conventions and `.editorconfig`; use modern C# when it improves clarity, but do not mechanically modernize working code. Consistency and readability outrank maximal use of language features.
- **Default** for new C# code: file-scoped namespaces when consistent with the project; one primary top-level type per file, with the file named after it (small private or nested supporting types may stay with their owner); the `Async` suffix on `Task`/`ValueTask`-returning methods unless an existing interface or framework contract makes renaming inappropriate.
- **Must not** perform style-only rewrites outside the requested change unless explicitly asked; avoid mixing large formatting or modernization changes with functional work.

Style guidance (prefer/avoid):

- Primary constructors when dependency injection or simple initialization stays clear; a regular constructor when validation or initialization is non-trivial, explicit fields read better, the codebase consistently uses that style, or parameter capture would obscure the class. Avoid mechanical constructor conversion.
- Records when value semantics and immutability are intended (many DTOs, genuine Value Objects); classes when identity, mutable lifecycle, inheritance or framework behavior make class semantics clearer. Avoid turning every DTO or Domain type into a record.
- Keep implementation details non-public when they need not be part of the public API; use `sealed` when it communicates deliberate design intent, not as a speculative JIT optimization.
- Collection expressions, pattern matching, switch expressions and target-typed construction when they read better; `var` when the type is obvious or unimportant, an explicit type when it aids clarity.
- Standard .NET naming: PascalCase for types, methods, properties and public members; camelCase for parameters and locals; meaningful names over abbreviations; private fields follow the repository convention. Avoid reorganizing an existing file merely to satisfy a preferred member ordering.

## Async, Cancellation and Time

- **Must** use async APIs for asynchronous I/O and **must not** block them with `.Result`, `.Wait()` or similar sync-over-async patterns.
- **Must** propagate `CancellationToken` through asynchronous operations when cancellation is meaningful; do not add cancellation parameters to purely synchronous code without a use case.
- **Default:** `TimeProvider` for application logic whose behavior depends on the current clock and needs deterministic tests; do not mechanically replace stored timestamps or explicit dates, which are not clock dependencies.

## Optimization Discipline

- **Default:** clear, correct code first — no specialized performance optimization without a concrete reason, and measurement or profiling evidence for non-trivial optimization.
- **Default:** compiled queries (`EF.CompileQuery` / `EF.CompileAsyncQuery`), `ValueTask<T>`, `ArrayPool<T>` / `MemoryPool<T>` or manual pooling, custom serialization, aggressive caching and raw SQL for performance are introduced only for a measured or clearly demonstrated need. For a demonstrated allocation-heavy hot path, spans, pooling, source-generated serialization or preallocated buffers may apply — verify the improvement on the relevant workload.

Workflow: performance-motivated changes — `development-workflow` § Co-change Obligations; using-directive cleanup of changed files — `verify` § 6.
Technique: `modern-csharp` knowledge skill.
