---
name: modern-csharp
description: >
  Use when applying or reviewing modern C# features or style: primary
  constructors, collection expressions, records, required members, pattern
  matching, field keyword, extension members, raw strings, var, sealed.
---

> Kind: KNW | Scope: backend | Capability: — | Loading: on-demand knowledge

# Modern C#

Policy: `.claude/rules/backend/coding-style.md` (conventions, no mechanical modernization, no unrelated style rewrites), `.claude/rules/backend/runtime.md` (allocation-oriented techniques need evidence). Use modern features when they make code clearer, safer, or simpler; consistency and readability matter more than maximizing language features.

## Primary constructors

Good for simple dependency injection or initialization:

```csharp
internal sealed class OrderService(IOrderRepository orders, IUnitOfWork unitOfWork)
{
}
```

Prefer a regular constructor when validation or initialization is non-trivial, explicit fields improve readability, the codebase consistently uses that style, or parameter capture would obscure the class. Never convert constructors mechanically.

## Collection expressions

```csharp
string[] names = ["Alice", "Bob"];
List<int> ids = [1, 2, 3];
```

Use them when the target type is clear; do not replace existing initializers solely to modernize.

## Records and classes

Records fit intentional value semantics: immutable transport DTOs, genuine Value Objects, immutable messages. Classes fit identity, mutable lifecycle, inheritance, or framework behavior; entities with identity normally stay classes. Do not turn every DTO or Domain type into a record.

## Required members

```csharp
public required string Name { get; init; }
```

Use `required` when initialization is part of the type's valid construction contract — not as a substitute for constructor/domain validation that protects invariants.

## Pattern matching

```csharp
return status switch
{
    OrderStatus.New => ...,
    OrderStatus.Completed => ...,
    _ => ...
};
```

Avoid deeply nested patterns that are harder to read than plain conditions.

## `field` keyword

```csharp
public string Name
{
    get;
    set => field = string.IsNullOrWhiteSpace(value)
        ? throw new ArgumentException("Name is required.")
        : value.Trim();
}
```

Use it to remove an otherwise trivial backing field; do not rewrite backing fields that already contain clear or substantial logic.

## Extension members

```csharp
public static class OrderExtensions
{
    extension(Order order)
    {
        public bool IsFinished => order.Status == OrderStatus.Completed;
    }
}
```

Useful when extension properties or grouped extension behavior genuinely improve an API; traditional extension methods remain valid and need no conversion.

## Raw string literals

```csharp
var json = """
{
  "enabled": true
}
""";
```

Useful for test JSON, templates, and SQL that genuinely belongs in code — never a reason to introduce raw SQL.

## Style conventions

- `var` when the type is obvious or unimportant; an explicit type when it improves clarity; follow the project's convention.
- Standard .NET naming: PascalCase for types, methods, properties, and public members; camelCase for parameters and locals; meaningful names over abbreviations; private-field naming per the repository's convention.
- Keep implementation details non-public when they are not part of the project's public API; use `sealed` to communicate a deliberate "not for inheritance" design, not as a speculative JIT optimization.
- Do not reorganize an existing file merely to satisfy a preferred member ordering.
- Immutability where it represents the model naturally; controlled mutation where framework models or workflows are simpler with it.

## Span and allocation-oriented APIs

`Span<T>`, `ReadOnlySpan<T>`, stack allocation, pooling, and source-generated serialization are performance tools for demonstrated hot paths; ordinary arrays, strings, and collections are the default. Verify that an optimization materially improves the workload.

## Compatibility

Confirm the configured language version supports a feature before using it; never silently change `LangVersion` or the target framework to use newer syntax (a platform change is Reserved).

## Modernization tasks

When explicitly asked to modernize: preserve behavior, keep the change focused, prefer readability improvements, build and test afterwards, and do not mix architecture refactoring into syntax modernization.

## Anti-patterns

Newest syntax for its own sake, every class as a record, `record struct` merely to avoid allocations, `Span<T>` without a performance reason, mass constructor conversion.
