---
name: modern-csharp
description: >
  Use when modernizing C# or using C# 14 features: primary constructors,
  collection expressions, records, required members, pattern matching, field
  keyword, extension members, raw strings.
---

> Owns: modern C# feature technique and examples (no policy) | Scope: backend | Loads: on demand (knowledge skill)

# Modern C#

Policy owners: conventions, feature choices, and style-change scope —
`.claude/rules/coding-style.md`; allocation-oriented optimization —
`.claude/rules/performance.md`; changing the language version or target
framework — Reserved (CLAUDE.md § Decision Control).

## Primary Constructors

```csharp
internal sealed class OrderService(
    IOrderRepository orders,
    IUnitOfWork unitOfWork)
{
}
```

## Collection Expressions

Use them when the target type is clear:

```csharp
string[] names = ["Alice", "Bob"];

List<int> ids = [1, 2, 3];
```

## Records

Good record candidates include immutable transport DTOs, genuine Value Objects,
and immutable messages. Entities with identity and lifecycle normally remain
classes unless the model genuinely benefits from record semantics.

## Required Members

Use `required` when initializing a property is part of the type's valid
construction contract:

```csharp
public required string Name { get; init; }
```

`required` is not a substitute for constructor or domain validation where
invariants must be protected.

## Pattern Matching

```csharp
return status switch
{
    OrderStatus.New => ...,
    OrderStatus.Completed => ...,
    _ => ...
};
```

Avoid deeply nested patterns that are harder to understand than straightforward
conditions.

## `field` Keyword

C# 14 supports field-backed properties:

```csharp
public string Name
{
    get;
    set => field =
        string.IsNullOrWhiteSpace(value)
            ? throw new ArgumentException("Name is required.")
            : value.Trim();
}
```

Use it to remove an otherwise trivial backing field; do not rewrite manual
backing fields that already contain clear or substantial logic.

## Extension Members

C# 14 supports extension-member blocks, useful when extension properties or
grouped extension behavior genuinely improve an API:

```csharp
public static class OrderExtensions
{
    extension(Order order)
    {
        public bool IsFinished =>
            order.Status == OrderStatus.Completed;
    }
}
```

Traditional extension methods remain valid; do not convert them solely because
the newer syntax exists.

## Raw String Literals

Useful for readable embedded text — test JSON, templates, SQL that genuinely
belongs in code:

```csharp
var json = """
{
  "enabled": true
}
""";
```

Raw string literals do not make raw SQL appropriate by themselves.

## Immutability

Prefer immutability when it represents the model naturally; do not force
immutable representations onto framework models or workflows where controlled
mutation is simpler and clearer.

## Span and Allocation-Oriented APIs

`Span<T>`, `ReadOnlySpan<T>`, stack allocation, and pooling are performance
tools. Use ordinary arrays, strings, and collections by default.

## Compatibility

Before using a language feature, confirm that the project's configured language
version supports it; do not change `LangVersion` or the target framework to use
newer syntax.

## Modernization Tasks

When explicitly asked to modernize code:

1. preserve behavior;
2. keep the change focused;
3. prefer readability improvements;
4. build and test after the change;
5. do not mix unrelated architecture refactoring into syntax modernization.

## Anti-Patterns

Avoid newest syntax for its own sake, `record struct` merely to avoid
allocations, and mass constructor conversion.
