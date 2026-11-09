---
name: modern-csharp
description: >
  Use when explicitly modernizing C# code or when a task involves recent C#
  features: primary constructors, collection expressions, records, required
  members, pattern matching, the field keyword, extension members, raw string
  literals, or span-based APIs.
---

> Owns: modern C# language-feature technique | Scope: backend | Loads: on demand (knowledge skill)

# Modern C#

Policy owners: conventions and scope discipline → `.claude/rules/coding-style.md`;
allocation-oriented optimization → `.claude/rules/performance.md`. Changing
`LangVersion` or the target framework requires approval (`CLAUDE.md`). Use a
feature when it makes code clearer, safer, or simpler — not to demonstrate
syntax. Confirm the configured language version supports it first.

## Primary Constructors

```csharp
internal sealed class OrderService(IOrderRepository orders, IUnitOfWork unitOfWork)
{
}
```

Prefer a normal constructor when initialization, validation, field naming, or
debugging reads better that way.

## Collection Expressions

```csharp
string[] names = ["Alice", "Bob"];
List<int> ids = [1, 2, 3];
```

## Records

Good candidates: immutable transport DTOs, genuine Value Objects, immutable
messages. Entities with identity and lifecycle normally stay classes; avoid
`record struct` merely to avoid allocations.

## Required Members

```csharp
public required string Name { get; init; }
```

Use when initialization is part of the type's valid construction contract; it
does not replace constructor/domain validation that protects invariants.

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

Use it to remove a trivial backing field; leave backing fields with substantial
logic alone.

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

Traditional extension methods remain valid; do not convert them just because
the new syntax exists.

## Raw String Literals

```csharp
var json = """
{
  "enabled": true
}
""";
```

Useful for test JSON, templates, and SQL that genuinely belongs in code (raw SQL
still follows `performance.md` and `security.md`).

## Immutability and Spans

Prefer immutability where it models the domain naturally, but not where
controlled mutation is simpler. `Span<T>`, `ReadOnlySpan<T>`, `stackalloc`, and
pooling are performance tools for profiled hot paths; ordinary arrays, strings,
and collections are the default.

## Modernization Tasks

When explicitly asked to modernize: preserve behavior, keep the change focused,
prefer readability gains, build and test afterwards, and do not mix unrelated
architecture refactoring into syntax modernization.
