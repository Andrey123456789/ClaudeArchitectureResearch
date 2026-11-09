---
paths:
  - "backend/**/*.cs"
---

> Owns: C# conventions, using-directive hygiene, style scope discipline | Scope: backend | Loads: path

# C# Coding Style

Mechanical formatting and analyzer severities live in `.editorconfig` and
`Directory.Build.props`; do not restate them here.

## General Principle

Follow the repository's existing conventions and `.editorconfig`. Use modern C#
features when they improve clarity, but do not rewrite working code solely to
use newer syntax. Consistency and readability matter more than maximizing use of
language features. Technique: `modern-csharp` skill.

## Files and Namespaces

- For new code, prefer file-scoped namespaces when consistent with the project.
- Keep one primary top-level type per file, with the file name matching that
  type; small private or nested supporting types may stay with their owner when
  that improves locality.
- Methods returning `Task` or `ValueTask` use the `Async` suffix unless an
  existing or framework contract makes that inappropriate; do not rename
  established APIs solely to add it.

Do not reorganize an existing file merely to satisfy a preferred member order.

## Constructors, Records, and Visibility

- Primary constructors fit dependency injection and simple initialization; use
  a regular constructor when validation or initialization is non-trivial,
  explicit fields read better, or the codebase consistently does so. Do not
  convert constructors mechanically.
- Use records when value semantics and immutability are desirable (many DTOs,
  genuine Value Objects); use classes when identity, mutable lifecycle,
  inheritance, or framework behavior makes class semantics clearer.
- Keep implementation details non-public when they are not part of the public
  API. Use `sealed` to communicate deliberate non-inheritance, not as a
  speculative JIT optimization.
- Use `var` when the type is obvious or unimportant; use an explicit type when
  it improves clarity.

## Naming

Standard .NET naming: PascalCase for types, methods, properties, and public
members; camelCase for parameters and locals; meaningful names over
abbreviations. Private-field naming follows the repository's convention.

## Using Directives

For every C# file created or modified by the current task, remove unused or
redundant `using` directives (including imports already provided by
implicit/global usings, unless needed for clarity or disambiguation) before
completion. Do not perform an unrelated repository-wide using cleanup. Use
compiler/IDE tooling when available, but verify the changed files.

## Scope Discipline

Do not perform style-only rewrites outside the requested change unless
explicitly asked. Avoid mixing large formatting or modernization changes with
functional work.
