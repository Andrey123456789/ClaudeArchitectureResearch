---
paths:
  - "backend/**/*"
---
> Level: 0-core | Owns: C# code conventions and style scope discipline | Scope: backend | Loads: path (backend files)

# C# Coding Conventions

- Default: follow the repository's existing conventions and `.editorconfig`. Use
  modern C# features when they improve clarity, but do not rewrite working code
  solely to use newer syntax. Consistency and readability outweigh maximal use
  of language features.
- Default for new C# code: file-scoped namespaces when consistent with the
  project; one primary top-level type per file, with the file named after it
  (small private or nested supporting types may stay with their owner); the
  `Async` suffix on methods returning `Task`/`ValueTask`, unless an existing
  interface or framework contract makes renaming inappropriate.
- Use standard .NET naming: PascalCase for types, methods, properties, and public
  members; camelCase for parameters and locals; meaningful names over
  abbreviations; private-field naming per the repository's convention.
- Do not perform style-only rewrites outside the requested change unless
  explicitly asked; avoid mixing large formatting or modernization changes with
  functional work.

Language-feature technique: `modern-csharp`. Using-directive cleanup of changed
files is a `verify` step.
