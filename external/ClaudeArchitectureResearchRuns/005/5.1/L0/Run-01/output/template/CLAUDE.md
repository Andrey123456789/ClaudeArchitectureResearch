> Level: 0 Core · Owns: entry point — precedence, vocabulary, operating principles, work loop · Scope: common · Loads: always

# Project Instructions

Reusable instruction template for a .NET backend and a TypeScript single-page frontend built on Clean Architecture.

## Instruction levels and precedence

Engineering instructions live in `.claude/rules/`, ordered by stability:

    0 Core  →  1 Architecture  →  2 Technology  →  3 Project
    (most stable)                                (most volatile)

- A more volatile level refines a more stable one and never contradicts it. If instructions at different levels appear to conflict, do not choose silently: follow the more stable level and report the conflict.
- Path-scoped rules load when matching files are read; the modules imported at the end of this file are always loaded; workflows in `.claude/skills/` explicitly read the rule owners they depend on.
- Product inputs — `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specifications and task prompts — are not instruction levels; their authority is defined in product governance. A product or task input may request a change to an engineering decision; it never silently overrides one — the change goes through decision control.
- Maintainer map (not loaded automatically): `.claude/INSTRUCTION-MAP.md`.

## Vocabulary

- **must / must not** — a violation is a defect.
- **default** — deviate only for a concrete reason, and report the deviation.
- **prefer / avoid** — guidance.
- **requires approval** — a Reserved decision (decision control).

## Operating principles

- **Must** keep changes focused on the requested scope and preserve existing behavior unless the task or the approved specification requires changing it.
- **Default:** prefer simple, maintainable solutions; keep architectural complexity proportional to current requirements; avoid speculative abstractions.
- **Must not** introduce frameworks, libraries, infrastructure or architectural patterns without a concrete current need.
- **Must** challenge a questionable request before implementing it: name the concrete concern — duplication, poor cohesion, unreliable triggering or loading, avoidable context cost, conflict with accepted architecture or decisions, unnecessary complexity — and propose an alternative. This never authorizes silently rewriting or ignoring the requirement: the user decides, and Reserved choices go through decision control.

## Work loop

1. **Must** inspect the relevant existing code before a non-trivial change and apply the rules and workflows that govern it.
2. New application or substantial feature: read the product inputs first (product governance).
3. Classify consequential choices before acting (decision control).
4. Route to workflows: scaffolding or structural change → `project-structure`; adding, updating or removing a package → `add-dependency`; `CUSTOM_SETTINGS.md` change → `custom-settings`; Reserved decision → `architecture-decision`; failing build or tests → `build-fix`; security audit → `security-scan`; Git operations → `git-workflow`.
5. **Must** run `code-review` before the final `verify` for substantial feature work or a newly implemented application.
6. **Must** run `verify` before declaring implementation work complete. Completion obligations: `.claude/rules/0-core/completion-contract.md`.

## Always-loaded modules

@.claude/rules/0-core/product-governance.md
@.claude/rules/0-core/decision-control.md
@.claude/rules/0-core/git-safety.md
@.claude/rules/1-architecture/overview.md
@.claude/rules/3-project/decisions.md
