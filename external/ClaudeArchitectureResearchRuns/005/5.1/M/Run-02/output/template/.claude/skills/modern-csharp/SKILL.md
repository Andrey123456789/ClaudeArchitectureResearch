---
name: modern-csharp
description: >
  Use when modernizing C# or applying C# 14 features (primary constructors,
  collection expressions, records, required members, patterns, field keyword,
  extension members, raw strings, Span) or choosing constructor, record, var,
  or visibility style.
---

> Owner: modern C# language technique and low-level style guidance (normative policy lives in rules) | Scope: backend | Loads: on demand — knowledge | Enforced: `.editorconfig` suggestions

# Modern C#

Policy: `.claude/rules/coding-style.md` (repository conventions first, no
mechanical modernization, style scope discipline). Use a feature when it makes
the code clearer, safer, or simpler — not to demonstrate newer syntax.

## Primary Constructors

Useful for simple dependency injection or simple initialization:

```csharp
internal sealed class OrderService(
    IOrderRepository orders,
    IUnitOfWork unitOfWork)
{
}
```

Prefer a regular constructor when validation or initialization is non-trivial,
explicit fields read better, the codebase consistently uses that style, or
parameter capture would make the class harder to understand. Do not convert
existing constructors mechanically.

## Records and Classes

Records fit when value semantics and immutability are intentional: many
immutable transport DTOs, genuine Value Objects, immutable messages. Classes fit
when identity, a mutable lifecycle, inheritance, or framework behavior make class
semantics clearer — entities normally stay classes. Not every DTO or Domain type
should become a record, and `record struct` is not an allocation trick.

## Visibility and Inheritance

Keep implementation details non-public when they are not part of the project's
public API (`internal` repositories, configurations, handlers). Use `sealed` when
a type is deliberately not designed for inheritance and the modifier
communicates that intent — not as a speculative JIT optimization.

## Collection Expressions

```csharp
string[] names = ["Alice", "Bob"];

List<int> ids = [1, 2, 3];
```

Use them when the target type is clear; do not rewrite existing initializers just
to modernize.

## Required Members

```csharp
public required string Name { get; init; }
```

Use `required` when initializing the property is part of the type's valid
construction contract, not as a substitute for constructor or domain validation
that protects invariants.

## Pattern Matching

```csharp
return status switch
{
    OrderStatus.New => ...,
    OrderStatus.Completed => ...,
    _ => ...
};
```

Pattern matching, switch expressions, and target-typed `new` help when they make
branching clearer; deeply nested patterns that are harder to read than plain
conditions do not.

## `field` Keyword

C# 14 field-backed properties remove a trivial backing field:

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

Keep manual backing fields that already contain clear or substantial logic.
(Trimming input like this is an observable product decision —
`CLAUDE.md` § Product Sources.)

## Extension Members

C# 14 extension blocks help when extension properties or grouped extension
behavior genuinely improve an API:

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

Traditional extension methods remain valid; do not convert them because newer
syntax exists.

## Raw String Literals

```csharp
var json = """
{
  "enabled": true
}
""";
```

Readable for test JSON, templates, and SQL that genuinely belongs in code — which
does not make raw SQL itself more appropriate.

## `var`

Use `var` when the type is obvious from the right-hand side or unimportant to
understanding; use an explicit type when it improves clarity. Follow the
project's convention.

## Naming

PascalCase for types, methods, properties, and public members; camelCase for
parameters and locals; meaningful names over abbreviations; interfaces prefixed
with `I`. Private-field naming follows the repository's established convention.
`.editorconfig` encodes these as suggestions.

## Immutability

Prefer immutability when it represents the model naturally; controlled mutation
is simpler for framework models and many workflows.

## Span and Allocation-Oriented APIs

`Span<T>`, `ReadOnlySpan<T>`, `stackalloc`, pooling, source-generated
serialization, and preallocated buffers are performance tools for demonstrated
allocation-heavy hot paths (`.claude/rules/performance.md` § General
Principle). Use ordinary arrays, strings, and collections by default, and verify
that an optimization materially improves the workload.

## Compatibility

Confirm the configured language version supports a feature before using it.
`LangVersion` and the target framework are stack decisions
(`docs/technology-stack.md` § Backend), not a modernization step.

## Modernization Tasks

When explicitly asked to modernize:

1. preserve behavior;
2. keep the change focused and prefer readability improvements;
3. build and test afterwards;
4. keep unrelated architecture refactoring out of syntax modernization.
