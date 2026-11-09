---
name: modern-csharp
description: Modern C# 14 technique. Use when explicitly modernizing code or working with primary constructors, collection expressions, records, required members, pattern matching, the field keyword, extension members, raw string literals, var usage, or span-based APIs.
---

> Level: 2-technology · Owns: C# language-feature technique and style guidance · Loading: on demand

# Modern C#

Rules: C# convention and scope rules (`.claude/rules/0-core/backend-code.md` § C# conventions); repository `.editorconfig`. Use a feature when it makes code clearer, safer, or simpler — never to demonstrate newer syntax. Consistency and readability beat maximal feature use.

## Constructors

Primary constructors suit simple dependency injection:

```csharp
internal sealed class OrderService(IOrderRepository orders, IUnitOfWork unitOfWork)
{
}
```

Use a regular constructor when validation or initialization is non-trivial, explicit fields read better, the codebase consistently uses that style, or parameter capture would obscure the class. Never convert constructors mechanically.

## Records and classes

Records fit intentional value semantics: immutable transport DTOs, genuine value objects, immutable messages. Entities with identity and lifecycle stay classes unless record semantics genuinely help; inheritance or framework behavior may also favor classes. Avoid `record struct` merely to dodge allocations.

## Members and syntax

- `required` when initialization is part of the valid-construction contract (`public required string Name { get; init; }`) — not a substitute for invariant validation.
- Collection expressions when the target type is clear (`string[] names = ["Alice", "Bob"];`); do not rewrite existing initializers just to modernize.
- Pattern matching and switch expressions when they clarify branching; avoid deeply nested patterns.
- `field` keyword (C# 14) to remove a trivial backing field:

  ```csharp
  public string Name
  {
      get;
      set => field = string.IsNullOrWhiteSpace(value) ? throw new ArgumentException("Name is required.") : value.Trim();
  }
  ```

- Extension members (C# 14) when extension properties or grouped behavior improve an API; ordinary extension methods remain valid:

  ```csharp
  public static class OrderExtensions
  {
      extension(Order order)
      {
          public bool IsFinished => order.Status == OrderStatus.Completed;
      }
  }
  ```

- Raw string literals for readable embedded text (test JSON, templates, SQL that genuinely belongs in code) — never an excuse for raw SQL.
- `var` when the type is obvious or unimportant; explicit types when they aid understanding; follow the project's convention.

## Style details

- Keep implementation details non-public when they are not part of the project's public API; use `sealed` when it communicates that a type is not designed for inheritance, not as a speculative JIT optimization.
- Standard .NET naming: PascalCase for types, methods, properties, and public members; camelCase for parameters and locals; meaningful names over abbreviations; private-field naming per repository convention.
- Small private or nested supporting types may stay with their owning type when that improves locality; do not reorganize a file only to satisfy a preferred member order.
- Prefer immutability when it models the domain naturally, not where controlled mutation is simpler.

## Performance-oriented features

`Span<T>`, `ReadOnlySpan<T>`, stack allocation, `ArrayPool<T>`/`MemoryPool<T>` pooling, preallocated buffers, and source-generated serialization are performance tools for demonstrated allocation-heavy hot paths — verify they materially help the workload, and never trade maintainability for speculative micro-optimization. Ordinary arrays, strings, and collections are the default.

## Compatibility

Confirm the configured language version supports a feature; changing `LangVersion` or the target framework requires approval.

## Modernization tasks

When explicitly asked to modernize: preserve behavior, keep the change focused, favor readability, build and test afterwards, and do not mix architecture refactoring into syntax modernization.
