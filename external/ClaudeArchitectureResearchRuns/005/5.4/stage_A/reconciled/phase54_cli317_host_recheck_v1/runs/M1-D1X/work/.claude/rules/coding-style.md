---
paths:
  - "backend/**/*.cs"
---

> Path rule · Scope: backend · Owns C# conventions, file/namespace and async naming defaults, and style scope discipline

# C# Coding Style

## General Principle

Follow the repository's existing conventions and `.editorconfig`. Prefer modern
C# features when they improve clarity, but do not rewrite working code solely
to use newer syntax. Consistency and readability matter more than maximizing
use of language features.

## Files and Namespaces

For new C# code:

- prefer file-scoped namespaces when consistent with the project;
- by default keep one primary top-level type per file, with the file name
  matching the primary type; small private or nested supporting types may stay
  with the owning type when that improves locality.

Do not reorganize an existing file merely to satisfy a preferred member
ordering.

## Async Naming

Methods returning `Task` or `ValueTask` use the `Async` suffix by default,
following standard .NET conventions and existing interface contracts. Do not
rename framework implementations or established APIs solely to add the suffix
when that would break an existing contract.

## Constructors

Primary constructors are appropriate when dependency injection or simple
initialization remains clear:

```csharp
public sealed class OrderService(
    IOrderRepository orders,
    IUnitOfWork unitOfWork)
{
}
```

Use a regular constructor when validation or initialization is non-trivial,
explicit fields improve readability, the existing codebase consistently uses
that style, or parameter capture would make the class harder to understand. Do
not convert constructors mechanically.

## Records and Classes

Use records when value semantics and immutability are desirable, for example
many DTOs and genuine Value Objects. Use classes when identity, mutable
lifecycle, inheritance, or framework behavior makes class semantics clearer. Do
not turn every DTO or Domain type into a record automatically.

## Visibility and Inheritance

Keep implementation details non-public when they are not part of the project's
public API. Use `sealed` when a type is deliberately not intended for
inheritance and the modifier communicates useful design intent; do not add
`sealed` merely as a speculative JIT optimization.

## Modern Syntax and Type Inference

Use collection expressions, pattern matching, switch expressions,
target-typed construction, and other modern features when they make the code
easier to read; do not prefer newer syntax when the result is less obvious. Use
`var` when the type is obvious from the right-hand side or not important to
understanding the code; use an explicit type when it improves clarity.

## Naming

Use standard .NET naming: PascalCase for types, methods, properties, and public
members; camelCase for parameters and local variables; meaningful names over
abbreviations. Private-field naming follows the repository's established
convention.

## Scope Discipline

Do not perform style-only rewrites outside the requested change unless
explicitly asked. Avoid mixing large formatting or modernization changes with
functional work. Using-directive cleanup of changed files is a `verify` step.
