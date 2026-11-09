---
name: modern-csharp
description: >
  Use when modernizing C# or using C# 14 features: primary constructors, collection
  expressions, records, required members, patterns, field keyword, extension members.
---

> Level: 2 Technology · Owns: modern C# language technique and examples (knowledge) · Scope: backend · Loads: on invocation · Depends on: .claude/rules/2-technology/csharp.md

# Modern C#

Policy owners: follow repository conventions and `.editorconfig`, no mechanical modernization, no style-only rewrites → `.claude/rules/2-technology/csharp.md`; changing `LangVersion` or the target framework → Reserved (CLAUDE.md); measured optimization → `0-core/runtime-principles.md`. Use a feature when it makes code clearer, safer, or simpler. This skill is technique only.

## Primary constructors

```csharp
internal sealed class OrderService(IOrderRepository orders, IUnitOfWork unitOfWork)
{
}
```

Prefer a regular constructor when validation or initialization is non-trivial, explicit fields read better, the codebase uses that style consistently, or parameter capture would obscure the class.

## Collection expressions

```csharp
string[] names = ["Alice", "Bob"];
List<int> ids = [1, 2, 3];
```

Use them when the target type is clear.

## Records and classes

Records fit intentional value semantics: immutable transport DTOs, genuine Value Objects, immutable messages. Entities with identity and lifecycle normally stay classes; classes also fit when inheritance or framework behavior makes class semantics clearer. Avoid `record struct` merely to avoid allocations.

## Required members

```csharp
public required string Name { get; init; }
```

Use `required` when initialization is part of the type's valid construction contract — not as a substitute for constructor or domain validation that protects invariants.

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

Use it to remove an otherwise trivial backing field; keep manual backing fields that already contain clear or substantial logic.

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

Useful when extension properties or grouped extension behavior improve an API; traditional extension methods remain valid.

## Raw string literals

```csharp
var json = """
{
  "enabled": true
}
""";
```

Good for test JSON, templates, and SQL that genuinely belongs in code — not a reason to write raw SQL.

## `var`, visibility, `sealed`

Use `var` when the type is obvious from the right-hand side or unimportant; use an explicit type when it helps. Keep implementation details non-public when they are not part of the project's public API. Use `sealed` when a type is deliberately not designed for inheritance and the modifier communicates intent — not as a speculative JIT optimization. Follow the repository's established private-field naming convention.

## Naming and file layout details

Standard .NET naming: PascalCase for types, methods, properties, and public members; camelCase for parameters and locals; meaningful names over abbreviations (the template's `.editorconfig` reports these as suggestions). Small private or nested supporting types may stay with their owning type when that improves locality. Do not reorganize an existing file merely to satisfy a preferred member ordering.

## Immutability

Prefer immutability when it represents the model naturally; do not force it onto framework models or workflows where controlled mutation is simpler.

## Span and allocation-oriented APIs

`Span<T>`, `ReadOnlySpan<T>`, `stackalloc`, pooling, and similar features are performance tools: use ordinary arrays, strings, and collections by default and introduce these when profiling or a clearly hot path justifies them. For a demonstrated allocation-heavy hot path, spans, `ArrayPool<T>`/`MemoryPool<T>`, source-generated `System.Text.Json` serialization, or preallocated buffers are the usual tools — then measure that the optimization materially improves the relevant workload.

## Compatibility

Confirm the configured language version supports a feature before using it.

## Modernization tasks

When explicitly asked to modernize: preserve behavior, keep the change focused, prefer readability improvements, build and test afterwards, and do not mix architecture refactoring into syntax modernization.
