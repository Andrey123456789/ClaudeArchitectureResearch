---
name: modern-csharp
description: >
  Use when modernizing C# or using C# 14 features: primary constructors,
  collection expressions, records, required members, patterns, field keyword,
  extension members.
---
> Level: 2-technology | Owns: C# language-feature and low-level style technique | Scope: backend | Loads: on demand (skill)

# Modern C#

Policy: `coding.md` (follow conventions, no mechanical modernization, no
unrelated style rewrites). Use a feature when it makes code clearer, safer, or
simpler — not to demonstrate syntax. Confirm the project's language version
supports a feature; changing `LangVersion` or the target framework is not a
side effect of using syntax.

## Primary constructors

```csharp
internal sealed class OrderService(
    IOrderRepository orders,
    TimeProvider clock)
{
}
```

Good for simple dependency injection. Use a regular constructor when
validation/initialization is non-trivial, explicit fields read better, the
codebase consistently uses that style, or parameter capture would obscure the
class. Do not convert constructors mechanically.

## Collection expressions

```csharp
string[] names = ["Alice", "Bob"];
List<int> ids = [1, 2, 3];
```

Use when the target type is clear; do not rewrite existing initializers solely
for modernization.

## Records and classes

Records fit intentional value semantics: immutable transport DTOs, genuine
value objects, immutable messages. Entities with identity and lifecycle stay
classes; not every DTO or domain type becomes a record; avoid `record struct`
merely to avoid allocations.

## Required members

```csharp
public required string Name { get; init; }
```

Use `required` when initialization is part of the valid construction contract —
not as a substitute for invariant-protecting validation.

## Pattern matching

```csharp
return status switch
{
    OrderStatus.New => ...,
    OrderStatus.Completed => ...,
    _ => ...
};
```

Avoid deeply nested patterns that read worse than plain conditions.

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

Use it to remove a trivial backing field; do not rewrite backing fields that
already hold clear or substantial logic.

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

Useful for extension properties or grouped extension behavior; traditional
extension methods remain valid.

## Raw string literals

```csharp
var json = """
{
  "enabled": true
}
""";
```

Useful for test JSON, templates, and SQL that genuinely belongs in code — not a
reason to write raw SQL.

## Style details

- `var` when the type is obvious or unimportant; an explicit type when it
  improves clarity; follow the project's convention.
- Keep implementation details non-public when they are not part of the public
  API; use `sealed` when a type is deliberately not designed for inheritance,
  not as a speculative JIT optimization.
- Use collection expressions, switch expressions, target-typed `new`, and
  similar features when they make code easier to read.
- Prefer immutability where it models the domain naturally; do not force it on
  framework models or workflows where controlled mutation is clearer.

## Span and allocation-oriented APIs

`Span<T>`, `ReadOnlySpan<T>`, `stackalloc`, and pooling are performance tools
for profiled hot paths (`performance.md`); use ordinary arrays, strings, and
collections by default.

## Modernization tasks

When explicitly asked to modernize: preserve behavior, keep the change focused,
prefer readability improvements, build and test afterwards, and keep
architecture refactoring out of syntax modernization.
