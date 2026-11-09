---
paths:
  - "backend/**/*"
---

> Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (frontmatter paths)

# C# Coding Style Standard

- Default: follow the repository's existing conventions and `.editorconfig`; use modern C# features when they improve clarity, but do not rewrite working code solely to use newer syntax.
- Default for new C# code: file-scoped namespaces when consistent with the project; one primary top-level type per file with a matching file name (small private or nested supporting types may stay with their owner); the `Async` suffix on `Task`/`ValueTask`-returning methods unless an existing or framework contract makes it inappropriate.
- Must not perform style-only rewrites outside the requested change unless explicitly asked; avoid mixing large formatting or modernization changes with functional work.

Technique: `modern-csharp`. Changed-file import cleanup: `verify`.
