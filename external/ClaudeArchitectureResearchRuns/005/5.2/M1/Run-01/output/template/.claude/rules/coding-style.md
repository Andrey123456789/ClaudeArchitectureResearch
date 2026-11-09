---
paths:
  - "backend/**/*.cs"
---

> **Policy rule** · Owns: C# conventions, file/namespace and async naming conventions, style-scope discipline · Scope: backend · Loading: path (backend C# files)

# C# Coding Style

## General Principle

Follow the repository's existing conventions and `.editorconfig`.

Default: use modern C# features when they improve clarity, but do not rewrite
working code solely to use newer syntax.

Consistency and readability are more important than maximizing use of language
features.

## Files and Namespaces

- Default: use file-scoped namespaces for new files when consistent with the
  project.
- Default: keep one primary top-level type per file, in a file named after that
  type.
- Small private or nested supporting types may remain with the owning type when
  that improves locality.

Do not reorganize an existing file merely to satisfy a preferred member ordering.

## Constructors

Primary constructors are appropriate when dependency injection or simple
initialization remains clear.

```csharp
public sealed class OrderService(
    IOrderRepository orders,
    IUnitOfWork unitOfWork)
{
}
```

Use a regular constructor when:

- validation or initialization is non-trivial;
- explicit fields improve readability;
- the existing codebase uses that style consistently;
- primary-constructor parameter capture would make the class harder to understand.

Do not convert constructors mechanically.

## Records and Classes

Use records when value semantics and immutability are desirable, for example
many DTOs and genuine Value Objects.

Use classes when identity, mutable lifecycle, inheritance, or framework behavior
makes class semantics clearer.

Do not turn every DTO or Domain type into a record automatically.

## Visibility and Inheritance

Keep implementation details non-public when they do not need to form part of
the project's public API.

Use `sealed` when the type is deliberately not intended for inheritance and the
modifier communicates useful design intent.

Do not add `sealed` merely as a speculative JIT optimization.

## Modern Syntax

Use collection expressions, pattern matching, switch expressions, target-typed
construction, and other modern C# features when they make the code easier to
read.

Do not prefer newer syntax when the resulting code is less obvious.

## Type Inference

Use `var` when the type is obvious from the right-hand side or the exact type is
not important to understanding the code.

Use an explicit type when it improves clarity.

## Async Naming

Default: methods returning `Task` or `ValueTask` use the `Async` suffix, following
standard .NET conventions and existing interface contracts.

Do not rename framework implementations or established APIs solely to add the
suffix when doing so would break an existing contract.

## Naming

Use standard .NET naming conventions:

- PascalCase for types, methods, properties, and public members;
- camelCase for parameters and local variables;
- meaningful names over abbreviations.

Private-field naming follows the repository's established convention.

## Using Directives

Cleaning unused or redundant `using` directives in C# files created or modified
by the task is a completion check owned by `verify` → Final Diff Review.

## Scope Discipline

Do not perform style-only rewrites outside the requested change unless explicitly
asked.

Avoid mixing large formatting or modernization changes with functional work.
