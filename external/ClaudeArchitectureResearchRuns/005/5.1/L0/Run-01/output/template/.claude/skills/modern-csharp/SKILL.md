---
name: modern-csharp
description: >
  Use when explicitly modernizing C# or applying C# 14 features: primary
  constructors, collection expressions, records, required members, pattern
  matching, field keyword, extension members.
---

> Level: 2 Technology · Owns: modern C# technique · Scope: backend · Loads: on demand (knowledge skill)

# Modern C#

Policy owners: `.claude/rules/2-technology/csharp.md` (conventions, scope discipline), `.claude/rules/0-core/runtime-principles.md` (measured optimization). Use a feature when it makes the code clearer, safer or simpler — not to demonstrate syntax.

## Primary constructors

```csharp
internal sealed class OrderService(IOrderRepository orders, IUnitOfWork unitOfWork)
{
}
```

Good for simple dependency injection. Prefer a regular constructor when validation or initialization is non-trivial, explicit fields read better, the codebase uses that style, or parameter capture would obscure the class. Do not convert constructors mechanically.

## Collection expressions

```csharp
string[] names = ["Alice", "Bob"];
List<int> ids = [1, 2, 3];
```

Use when the target type is clear; existing initializers need not be rewritten.

## Records and classes

Records fit intentional value semantics: immutable transport DTOs, genuine value objects, immutable messages. Entities with identity and lifecycle remain classes unless record semantics genuinely help. Not every DTO or Domain type becomes a record.

## Required members

```csharp
public required string Name { get; init; }
```

For initialization that is part of the type's construction contract — not a substitute for constructor or Domain validation that protects invariants.

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

## `field` keyword (C# 14)

```csharp
public string Name
{
    get;
    set => field = string.IsNullOrWhiteSpace(value)
        ? throw new ArgumentException("Name is required.")
        : value.Trim();
}
```

Use it to remove a trivial backing field; leave manual backing fields with substantial logic alone.

## Extension members (C# 14)

```csharp
public static class OrderExtensions
{
    extension(Order order)
    {
        public bool IsFinished => order.Status == OrderStatus.Completed;
    }
}
```

Useful for extension properties or grouped extension behavior; traditional extension methods remain valid.

## Raw string literals

```csharp
var json = """
{
  "enabled": true
}
""";
```

Handy for test JSON, templates and SQL that genuinely belongs in code — never a reason to write raw SQL.

## `var`, visibility, `sealed`

`var` when the type is obvious or unimportant, an explicit type when it helps the reader; follow the project's convention. Keep implementation details non-public. Use `sealed` when a type is deliberately not designed for inheritance and the modifier communicates intent — not as a speculative JIT optimization.

## Immutability

Prefer immutability when it models the concept naturally; do not force it onto framework models or workflows where controlled mutation is simpler.

## Span and allocation-oriented APIs

`Span<T>`, `ReadOnlySpan<T>`, `stackalloc` and pooling are performance tools for profiled hot paths; ordinary arrays, strings and collections are the default.

## Compatibility

Confirm the configured language version supports a feature; changing `LangVersion` or the target framework to use newer syntax is a decision, not a side effect.

## Modernization tasks (when explicitly requested)

1. Preserve behavior.
2. Keep the change focused; no architecture refactoring mixed in.
3. Prefer readability improvements.
4. Build and test afterwards.

## Review cues

Newest syntax for its own sake, every class turned into a record, `record struct` only to avoid allocations, `Span<T>` without a performance reason, deeply nested patterns, mass constructor conversion.
