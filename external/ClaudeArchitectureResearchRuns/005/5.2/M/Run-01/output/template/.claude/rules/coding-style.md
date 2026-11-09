---
paths:
  - "backend/**/*.cs"
---

> Path-scoped rule. Owns: C# conventions, file and naming conventions, style-change scope discipline · Scope: backend · Loads: when backend C# files are in context · Depends on: CLAUDE.md · Enforced by: .editorconfig

# C# Coding Style

Unused `using` directives in changed files are handled by `verify`.
Language-feature technique: `modern-csharp` skill.

## General Principle

- Default: follow the repository's existing conventions and `.editorconfig`.
  Use modern C# features when they improve clarity, but do not rewrite working
  code solely to use newer syntax. Consistency and readability matter more than
  maximizing the use of language features.

## Files, Namespaces, and Async Naming

- Default for new C# code: file-scoped namespaces when consistent with the
  project; one primary top-level type per file, with the file named after that
  type (small private or nested supporting types may stay with their owning
  type when that improves locality); the `Async` suffix on methods returning
  `Task` or `ValueTask`, unless an existing interface or framework contract makes
  the suffix inappropriate.
- Do not rename framework implementations or established APIs solely to add the
  suffix, and do not reorganize an existing file merely to satisfy a preferred
  member ordering.

## Constructors

- Primary constructors are appropriate when dependency injection or simple
  initialization remains clear.
- Prefer a regular constructor when validation or initialization is
  non-trivial, explicit fields improve readability, the codebase consistently
  uses that style, or primary-constructor parameter capture would make the class
  harder to understand.
- Do not convert constructors mechanically.

## Records and Classes

- Use records when value semantics and immutability are desirable, for example
  many DTOs and genuine Value Objects; use classes when identity, mutable
  lifecycle, inheritance, or framework behavior makes class semantics clearer.
- Do not turn every DTO or Domain type into a record automatically.

## Visibility and Inheritance

- Keep implementation details non-public when they are not part of the
  project's public API.
- Use `sealed` when a type is deliberately not intended for inheritance and the
  modifier communicates useful intent; do not add it merely as a speculative JIT
  optimization.

## Modern Syntax and Type Inference

- Use collection expressions, pattern matching, switch expressions,
  target-typed construction, and similar features when they make code easier to
  read; avoid newer syntax when the result is less obvious.
- Use `var` when the type is obvious from the right-hand side or not important
  to understanding the code; use an explicit type when it improves clarity.

## Naming

- Use standard .NET naming: PascalCase for types, methods, properties, and
  public members; camelCase for parameters and locals; meaningful names over
  abbreviations. Private-field naming follows the repository's established
  convention.

## Scope Discipline

- Do not perform style-only rewrites outside the requested change unless
  explicitly asked; avoid mixing large formatting or modernization changes with
  functional work.
