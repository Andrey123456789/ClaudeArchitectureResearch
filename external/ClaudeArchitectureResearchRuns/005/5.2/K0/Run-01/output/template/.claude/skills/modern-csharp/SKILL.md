---
name: modern-csharp
description: Use when explicitly modernizing C# code or when a task involves recent C# 14 features — primary constructors, collection expressions, records, required members, pattern matching, the field keyword, extension members, raw string literals, spans.
---
<!-- Kind: KNW | Scope: backend | Owns: modern C# feature technique and examples | Loads: on demand (model-invoked) -->
# Modern C#

Standards and style guidance: `rules/backend/csharp.md` (conventions, prefer/avoid style guidance, optimization discipline). Language version: DEC-PLAT-01. This skill shows the features; use them when they make code clearer, safer or simpler, not to demonstrate newer syntax.

## Primary Constructors

```csharp
internal sealed class OrderService(
    IOrderRepository orders,
    IUnitOfWork unitOfWork)
{
}
```

When to prefer a regular constructor: `rules/backend/csharp.md` § Conventions.

## Collection Expressions

When the target type is clear:

```csharp
string[] names = ["Alice", "Bob"];

List<int> ids = [1, 2, 3];
```

## Records

Good candidates: immutable transport DTOs, genuine Value Objects, immutable messages. Entities with identity and lifecycle normally remain classes unless the model genuinely benefits from record semantics.

## Required Members

When initializing a property is part of the type's valid construction contract:

```csharp
public required string Name { get; init; }
```

`required` does not replace meaningful constructor or domain validation where invariants need protection.

## Pattern Matching

```csharp
return status switch
{
    OrderStatus.New => ...,
    OrderStatus.Completed => ...,
    _ => ...
};
```

Deeply nested patterns that are harder to read than straightforward conditions are a poor trade.

## `field` Keyword

C# 14 field-backed properties:

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

Useful when it removes an otherwise trivial backing field; manual backing fields with clear or substantial logic can stay.

## Extension Members

C# 14 extension-member blocks help when extension properties or grouped extension behavior genuinely improve an API:

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

Traditional extension methods remain valid; converting them solely because the newer syntax exists adds churn.

## Raw String Literals

Readable embedded text — test JSON, templates, SQL that genuinely belongs in code:

```csharp
var json = """
{
  "enabled": true
}
""";
```

Convenient raw strings are no reason to write raw SQL.

## Immutability

Prefer immutability when it represents the model naturally; framework models and workflows where controlled mutation is simpler stay mutable.

## Span and Allocation-Oriented APIs

`Span<T>`, `ReadOnlySpan<T>`, stack allocation and pooling are performance tools for profiled or clearly hot paths; ordinary arrays, strings and collections are the default (`rules/backend/csharp.md` § Optimization Discipline).

## Compatibility

Confirm the project's configured language version supports a feature before using it; changing `LangVersion` or the target framework to use newer syntax is a decision, not a silent edit (DEC-PLAT-01).

## Modernization Tasks

When explicitly asked to modernize code:

1. preserve behavior;
2. keep the change focused;
3. prefer readability improvements;
4. build and test after the change;
5. keep unrelated architecture refactoring out of syntax modernization.

## Anti-Patterns

Avoid newest syntax for its own sake, converting every class to a record, `record struct` merely to avoid allocations, `Span<T>` without a performance reason, deeply nested patterns, mass constructor conversion, and language or framework version changes without approval.
