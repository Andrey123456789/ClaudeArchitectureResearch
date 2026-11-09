---
name: modern-csharp
description: Use when modernizing C# or using C# 14 features — primary constructors, collection expressions, records, required members, patterns, field keyword, extension members, raw strings, spans.
---

> Kind: KNW | Scope: backend | Owner: modern C# language technique with examples | Loading: on demand (model-invoked knowledge)

# Modern C#

Rules: `rules/backend/csharp.md` (conventions, when to modernize, optimization discipline). Language version: D-03.

Use a modern feature when it makes code clearer, safer or simpler — not to demonstrate syntax.

## Primary constructors

```csharp
internal sealed class OrderService(
    IOrderRepository orders,
    IUnitOfWork unitOfWork)
{
}
```

A normal constructor reads better when initialization, validation, field naming or debugging benefit from it.

## Collection expressions

```csharp
string[] names = ["Alice", "Bob"];

List<int> ids = [1, 2, 3];
```

Use them when the target type is clear.

## Records

Good candidates: immutable transport DTOs, genuine Value Objects, immutable messages. Entities with identity and lifecycle usually stay classes.

## Required members

```csharp
public required string Name { get; init; }
```

`required` expresses a construction contract; it does not replace constructor or domain validation where invariants need protection.

## Pattern matching

```csharp
return status switch
{
    OrderStatus.New => ...,
    OrderStatus.Completed => ...,
    _ => ...
};
```

Deeply nested patterns are often harder to read than plain conditions.

## `field` keyword

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

It removes an otherwise trivial backing field; manual backing fields with clear or substantial logic can stay.

## Extension members

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

Useful when extension properties or grouped extension behavior improve an API; traditional extension methods remain valid.

## Raw string literals

```csharp
var json = """
{
  "enabled": true
}
""";
```

Handy for test JSON, templates and SQL that genuinely belongs in code — they are not a reason to write raw SQL.

## Immutability

Model immutability where it is natural; framework models and workflows with controlled mutation often stay simpler mutable.

## Spans and allocation-oriented code

`Span<T>`, `ReadOnlySpan<T>`, stack allocation, pooling, source-generated serialization and preallocated buffers are performance tools for demonstrated allocation-heavy hot paths; verify that the optimization materially improves the workload. Ordinary arrays, strings and collections are the default.

## Compatibility

Confirm the configured language version supports a feature before using it; changing `LangVersion` or the target framework to use newer syntax is a decision, not a silent edit.

## Modernization tasks

When explicitly asked to modernize:

1. preserve behavior;
2. keep the change focused;
3. favor readability improvements;
4. build and test afterwards;
5. keep architecture refactoring out of syntax modernization.

## Common mistakes

Newest syntax for its own sake; every class turned into a record; `record struct` merely to avoid allocations; `Span<T>` without a performance reason; deeply nested patterns; mass constructor conversion; language or framework version changes without approval.
