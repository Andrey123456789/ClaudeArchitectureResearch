---
paths:
  - "backend/**"
---
Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (backend/**)

# C# Coding Style Standards

Language-feature technique: `modern-csharp` knowledge skill. Mechanical formatting and analyzer settings: `.editorconfig` and `Directory.Build.props`. Using-directive cleanup of changed files: `verify`.

- Default: follow the repository's existing conventions and `.editorconfig`. Use modern C# features when they improve clarity, but do not rewrite working code merely to use newer syntax; consistency and readability matter more than maximal use of language features.
- Do not perform style-only rewrites outside the requested change unless explicitly asked. Avoid mixing large formatting or modernization changes with functional work.
- Default for new C# code: use file-scoped namespaces when consistent with the project; keep one primary top-level type per file whose name matches the file (small private or nested supporting types may stay with their owner); use the `Async` suffix for `Task`- and `ValueTask`-returning methods unless an existing or framework contract makes it inappropriate. Do not reorganize an existing file merely for a preferred member ordering.
- Prefer standard .NET naming: PascalCase for types, methods, properties and public members, camelCase for parameters and locals, meaningful names over abbreviations; private-field naming follows the repository convention. Keep implementation details non-public when they are not part of the project's public API, and use `sealed` to communicate design intent rather than as a speculative optimization.
