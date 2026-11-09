---
name: modern-csharp
description: >
  Use when modernizing C# or using C# 14 features: primary constructors,
  collection expressions, records, required members, pattern matching, field
  keyword, extension members, raw strings.
---

> Knowledge skill · Optional language technique · Conventions: `.claude/rules/coding-style.md`

# Modern C#

Use modern language features when they make code clearer, safer, or simpler;
do not modernize code merely to demonstrate newer syntax.

## Primary Constructors

Useful for simple dependency injection:

```csharp
internal sealed class OrderService(
    IOrderRepository orders,
    IUnitOfWork unitOfWork)
{
}
```

Prefer a normal constructor when initialization, validation, field naming, or
debugging is clearer that way.

## Collection Expressions

Use them when the target type is clear:

```csharp
string[] names = ["Alice", "Bob"];

List<int> ids = [1, 2, 3];
```

Do not replace every existing collection initializer solely for modernization.

## Records

Good candidates: immutable transport DTOs, genuine Value Objects, immutable
messages. Entities with identity and lifecycle remain classes unless the model
genuinely benefits from record semantics.

## Required Members

Use `required` when initializing a property is part of the type's valid
construction contract:

```csharp
public required string Name { get; init; }
```

Do not use `required` as a substitute for constructor or domain validation where
invariants must be protected.

## Pattern Matching

Useful when it makes branching clearer:

```csharp
return status switch
{
    OrderStatus.New => ...,
    OrderStatus.Completed => ...,
    _ => ...
};
```

Avoid deeply nested patterns that are harder to read than straightforward
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
backing fields with clear or substantial logic solely to use it.

## Extension Members

C# 14 extension-member blocks help when extension properties or grouped
extension behavior genuinely improve an API:

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

Useful for readable embedded text such as test JSON, templates, or SQL that
genuinely belongs in code:

```csharp
var json = """
{
  "enabled": true
}
""";
```

Raw SQL still follows `.claude/rules/performance.md` and `security.md`.

## Immutability

Prefer immutability when it represents the model naturally; do not force it onto
framework models or workflows where controlled mutation is simpler.

## Span and Allocation-Oriented APIs

`Span<T>`, `ReadOnlySpan<T>`, stack allocation, and pooling are performance
tools. Use ordinary arrays, strings, and collections by default and introduce
these only when profiling or a clearly hot path justifies the complexity
(`performance.md` § Allocation-Sensitive Code).

## Compatibility

Confirm that the project's configured language version supports a feature
before using it. Changing `LangVersion` or the target framework is a stack
decision, not a modernization step.

## Modernization Tasks

When explicitly asked to modernize code: preserve behavior, keep the change
focused, prefer readability improvements, build and test afterward, and do not
mix unrelated architecture refactoring into syntax modernization.

## Avoid

Newest syntax for its own sake; converting every class to a record;
`record struct` merely to avoid allocations; `Span<T>` without a performance
reason; deeply nested patterns; mass constructor conversion.
