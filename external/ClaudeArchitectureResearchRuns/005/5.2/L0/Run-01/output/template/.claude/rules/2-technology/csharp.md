---
paths:
  - "backend/**/*.cs"
---

> Level: 2 Technology | Owns: C# conventions, file and async naming, style scope discipline | Scope: backend | Loads: path | Depends on: none

# C# Conventions

- Default: follow the repository's conventions and `.editorconfig`; use modern
  C# when it improves clarity, but do not mechanically modernize working code.
- Do not perform style-only rewrites outside the requested change unless
  explicitly asked; avoid mixing large formatting or modernization changes with
  functional work.
- Default: for new C# code, prefer file-scoped namespaces when consistent with
  the project, keep one primary top-level type per file with a matching file
  name, and use the `Async` suffix for `Task`/`ValueTask`-returning methods
  unless an existing or framework contract makes that inappropriate.

Technique: → `modern-csharp` skill. Unused `using` cleanup: → `verify`.
