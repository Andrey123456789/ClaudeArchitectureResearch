---
name: modern-csharp
description: Use when explicitly modernizing C# code or choosing among C# 14 features — primary constructors, collection expressions, records, required members, pattern matching, the field keyword, extension members, raw strings, var, immutability, Span-based APIs.
---
Kind: KNW | Scope: backend | Capability: — | Loading: on invocation

# Modern C#

Rules: `.claude/rules/backend/coding-style.md` (follow existing conventions, no mechanical modernization, no unrelated style rewrites). Use a feature when it makes code clearer, safer or simpler, not to demonstrate newer syntax. Before using a feature, confirm the project's language version supports it; changing `LangVersion` or the target framework requires approval.

## Primary constructors

Good for simple dependency injection or initialization:

```csharp
internal sealed class OrderService(IOrderRepository orders, IUnitOfWork unitOfWork)
{
}
```

Prefer a regular constructor when validation or initialization is non-trivial, explicit fields read better, the codebase consistently uses that style, or captured parameters would make the class harder to follow. Do not convert constructors mechanically.

## Records and classes

Records fit when value semantics and immutability are intended: many DTOs, genuine Value Objects, immutable messages. Classes fit identity, mutable lifecycle, inheritance or framework behavior; entities with identity normally stay classes. Do not turn every DTO or Domain type into a record, and do not use `record struct` merely to avoid allocations.

## Collection expressions

```csharp
string[] names = ["Alice", "Bob"];
List<int> ids = [1, 2, 3];
```

Use them when the target type is clear; do not replace existing initializers merely to modernize.

## Required members

```csharp
public required string Name { get; init; }
```

Use `required` when initializing the property is part of the type's valid construction contract, not as a substitute for constructor or domain validation that protects invariants.

## Pattern matching and switch expressions

```csharp
return status switch
{
    OrderStatus.New => ...,
    OrderStatus.Completed => ...,
    _ => ...
};
```

Avoid deeply nested patterns that are harder to read than straightforward conditions.

## The `field` keyword

```csharp
public string Name
{
    get;
    set => field = string.IsNullOrWhiteSpace(value)
        ? throw new ArgumentException("Name is required.")
        : value.Trim();
}
```

Use it to remove an otherwise trivial backing field; do not rewrite backing fields with substantial logic just to use it.

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

Useful for extension properties or grouped extension behavior; traditional extension methods remain valid and need no conversion.

## Raw string literals

```csharp
var json = """
{
  "enabled": true
}
""";
```

Useful for test JSON, templates and SQL that genuinely belongs in code; convenient raw strings are not a reason to write raw SQL.

## Other choices

- `var`: when the type is obvious from the right-hand side or not important; an explicit type when it improves clarity; follow the project's convention.
- Target-typed `new`, pattern matching and other modern syntax: when the result is easier to read, not when it becomes less obvious.
- Immutability: prefer it when it represents the model naturally; do not force it onto framework models or workflows where controlled mutation is simpler.
- `Span<T>`, `ReadOnlySpan<T>`, `stackalloc`, pooling: performance tools for profiled or clearly hot paths (`.claude/rules/backend/performance.md`); ordinary arrays, strings and collections by default. For a demonstrated allocation-heavy hot path, consider spans, pooling, source-generated serialization or preallocated buffers, and verify that the optimization materially improves the relevant workload.

## Modernization tasks

When explicitly asked to modernize: preserve behavior, keep the change focused, prefer readability improvements, build and test afterwards, and do not mix unrelated architecture refactoring into syntax modernization.
