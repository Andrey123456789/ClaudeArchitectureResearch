---
paths:
  - "backend/**/*.cs"
---

> Owns: C# conventions, file and async naming, language-feature choices, logging-call style, style-change scope | Scope: backend | Loads: path-scoped (backend C# files)

# C# Coding Style

Formatting and naming are also configured in `.editorconfig`. Examples of
recent language features: `modern-csharp` skill.

## General Principle

Follow the repository's existing conventions and `.editorconfig`. Use modern C#
features when they improve clarity, but do not rewrite working code solely to
use newer syntax. Consistency and readability matter more than maximizing use of
language features.

## Files, Namespaces, and Async Naming

For new C# code, prefer file-scoped namespaces when consistent with the
project, keep one primary top-level type per file by default with the file name
matching that type (small private or nested supporting types may stay with the
owning type), and use the `Async` suffix for methods returning `Task` or
`ValueTask` unless an existing interface or framework contract makes it
inappropriate. Do not rename established APIs solely to add the suffix, and do
not reorganize an existing file merely to satisfy a preferred member ordering.

## Language Feature Choices

- Primary constructors fit dependency injection or simple initialization that
  stays clear. Use a regular constructor when validation or initialization is
  non-trivial, explicit fields improve readability, the codebase consistently
  uses that style, or parameter capture would make the class harder to
  understand. Do not convert constructors mechanically.
- Use records when value semantics and immutability are desirable (many DTOs,
  genuine Value Objects); use classes when identity, mutable lifecycle,
  inheritance, or framework behavior makes class semantics clearer. Do not turn
  every DTO or Domain type into a record.
- Keep implementation details non-public when they are not part of the
  project's public API. Use `sealed` when the type is deliberately not meant for
  inheritance and the modifier communicates that intent, not as a speculative
  JIT optimization.
- Use collection expressions, pattern matching, switch expressions,
  target-typed construction, and other modern features when they make code
  easier to read — not when the result is less obvious.
- Use `var` when the type is obvious from the right-hand side or unimportant to
  understanding the code; use an explicit type when it improves clarity.
- Use standard .NET naming: PascalCase for types, methods, properties, and public
  members; camelCase for parameters and locals; meaningful names over
  abbreviations. Private-field naming follows the repository's established
  convention.

## Logging Calls

Use `ILogger<T>` with structured message templates and stable property names;
avoid string interpolation that turns structured values into opaque text.

## Scope Discipline

Do not perform style-only rewrites outside the requested change unless
explicitly asked, and avoid mixing large formatting or modernization changes
with functional work. Removing unused `using` directives from changed files is a
`verify` step.
