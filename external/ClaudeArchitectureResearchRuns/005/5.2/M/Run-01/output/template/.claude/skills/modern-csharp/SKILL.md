---
name: modern-csharp
description: >
  Use when modernizing C# or using C# 14 features: primary constructors,
  collection expressions, records, required members, pattern matching, the
  field keyword, extension members, raw strings.
---

> Knowledge skill. Owns: modern C# language-feature technique and examples · Scope: backend · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/coding-style.md

# Modern C#

Rules: `coding-style.md` (follow existing conventions; no mechanical
modernization; style-change scope). Performance-oriented features:
`performance.md`. Use modern features when they make code clearer, safer, or
simpler.

## Primary Constructors

```csharp
internal sealed class OrderService(
    IOrderRepository orders,
    IUnitOfWork unitOfWork)
{
}
```

A regular constructor is clearer when initialization, validation, field naming,
or debugging benefits from it.

## Collection Expressions

```csharp
string[] names = ["Alice", "Bob"];

List<int> ids = [1, 2, 3];
```

Use them when the target type is clear.

## Records

Good candidates: immutable transport DTOs, genuine Value Objects, immutable
messages. Entities with identity and lifecycle stay classes unless the model
genuinely benefits from record semantics.

## Required Members

```csharp
public required string Name { get; init; }
```

`required` expresses that initialization is part of the type's valid
construction contract; it is not a substitute for constructor or domain
validation where invariants must be protected.

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

## `field` Keyword

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

Useful when it removes an otherwise trivial backing field; manual backing fields
with clear or substantial logic can stay.

## Extension Members

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

Useful for extension properties or grouped extension behavior; traditional
extension methods remain valid.

## Raw String Literals

```csharp
var json = """
{
  "enabled": true
}
""";
```

Useful for test JSON, templates, and SQL that genuinely belongs in code — raw
string literals are not a reason to write raw SQL.

## Immutability

Prefer immutability where it represents the model naturally; controlled
mutation is often simpler for framework models and workflows.

## Span and Allocation-Oriented APIs

`Span<T>`, `ReadOnlySpan<T>`, stack allocation, and pooling are performance
tools for profiled or clearly hot paths; ordinary arrays, strings, and
collections are the default.

## Compatibility

Confirm the project's configured language version supports a feature before
using it. Changing `LangVersion` or the target framework to use newer syntax is
not a routine edit: the platform version is a stack decision
(`docs/technology-stack.md`).

## Modernization Tasks

When explicitly asked to modernize code:

1. preserve behavior;
2. keep the change focused;
3. prefer readability improvements;
4. build and test after the change;
5. keep unrelated architecture refactoring out of syntax modernization.

## Anti-Patterns

- newest syntax for its own sake;
- converting every class to a record;
- `record struct` merely to avoid allocations;
- `Span<T>` without a performance reason;
- mass constructor conversion.
