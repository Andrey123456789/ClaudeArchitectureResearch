---
name: modern-csharp
description: >
  Use when modernizing C# or using C# 14 features: primary constructors, collection expressions, records, required, field keyword, extension members.
---

> Level: 2 Technology | Owns: modern C# language technique | Scope: backend | Loads: knowledge skill (on demand) | Depends on: 2-technology/csharp.md

# Modern C# Technique

Policy owners (routing): conventions and modernization scope →
`2-technology/csharp.md`; optimization evidence →
`0-core/performance-principles.md`; changing language or framework versions is
Reserved (`3-project/decisions.md`).

Use a feature when it makes code clearer, safer, or simpler; follow the
project's established conventions.

## Primary Constructors

```csharp
internal sealed class OrderService(IOrderRepository orders, IUnitOfWork unitOfWork)
{
}
```

Good for simple dependency injection. Use a regular constructor when
validation or initialization is non-trivial, explicit fields read better, the
codebase uses that style, or parameter capture would obscure the class.

## Collection Expressions

```csharp
string[] names = ["Alice", "Bob"];
List<int> ids = [1, 2, 3];
```

## Records and Classes

Records suit immutable transport DTOs, genuine Value Objects, and immutable
messages. Entities with identity and lifecycle remain classes unless record
semantics genuinely help; do not convert every DTO or entity, and avoid
`record struct` merely to dodge allocations.

## Required Members

```csharp
public required string Name { get; init; }
```

Use when initialization is part of valid construction — not as a substitute for
constructor or domain validation that protects invariants.

## Pattern Matching

```csharp
return status switch
{
    OrderStatus.New => ...,
    OrderStatus.Completed => ...,
    _ => ...
};
```

Avoid deeply nested patterns that are harder to read than plain conditions.

## `field` Keyword (C# 14)

```csharp
public string Name
{
    get;
    set => field = string.IsNullOrWhiteSpace(value)
        ? throw new ArgumentException("Name is required.")
        : value.Trim();
}
```

Removes a trivial backing field; leave substantial manual backing-field logic
as it is.

## Extension Members (C# 14)

```csharp
public static class OrderExtensions
{
    extension(Order order)
    {
        public bool IsFinished => order.Status == OrderStatus.Completed;
    }
}
```

Useful for extension properties or grouped extension behavior; classic
extension methods remain valid.

## Raw String Literals

```csharp
var json = """
{
  "enabled": true
}
""";
```

Good for test JSON, templates, and SQL that genuinely belongs in code — not a
reason to write raw SQL.

## Other Choices

- `var` when the type is obvious or unimportant; explicit types when they help.
- `sealed` when the type deliberately is not designed for inheritance, not as a
  speculative JIT optimization; keep implementation details non-public.
- Prefer immutability where it models the domain naturally; allow controlled
  mutation where frameworks or workflows need it.
- `Span<T>`, `ReadOnlySpan<T>`, `stackalloc`, pooling, source-generated
  serialization, and preallocated buffers are performance tools for profiled,
  allocation-heavy hot paths; use ordinary arrays, strings, and collections by
  default, and verify that an optimization materially improves the workload.
- Confirm the configured `LangVersion` supports a feature before using it.

## Modernization Tasks

When asked to modernize: preserve behavior, keep the change focused, prefer
readability gains, build and test afterwards, and keep architecture refactoring
out of the syntax change.
