> Owns: product-source governance, core defaults, architecture defaults, decision control, Git boundaries, workflow routing | Scope: common | Loads: always (imports docs/technology-stack.md)

# Project Instructions

This repository is a reusable template for ASP.NET Core + Angular applications
based on Clean Architecture. The approved technology stack is imported here and
is part of these instructions:

@docs/technology-stack.md

## Normative Vocabulary

- **must / must not** — a violation is a defect.
- **default** — deviation needs a concrete reason and must be reported.
- **prefer / avoid** — guidance.
- **requires approval** — a Reserved decision (see Decision Control).

## Product Specification

`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specifications, and task
prompts are product inputs, not instruction layers. They may request an
engineering decision, but they never silently override this file,
`docs/technology-stack.md`, or `.claude/rules/`; such a request goes through
Decision Control.

- When `SPECIFICATION.md` is non-empty, treat it as the authoritative source for
  project-specific functional requirements and observable product behavior. An
  empty `SPECIFICATION.md` in the reusable template is intentional.
- Do not silently weaken, contradict, or materially extend approved behavior,
  and do not invent user-visible rules, restrictions, limits, defaults, or
  workflow behavior merely because they seem reasonable or are not explicitly
  forbidden.
- If an omitted product detail must be decided to implement the requested
  behavior and the decision materially affects observable product behavior,
  propose the smallest reasonable option and ask for approval.
- String comparison semantics that affect observable behavior are product
  behavior, not persistence details. When the approved sources do not define
  them and the choice materially affects equality, uniqueness, lookup, or
  accepted input, do not silently choose case sensitivity, database collation,
  culture-sensitive vs. ordinal comparison, normalization/canonicalization, or
  automatic trimming — ask for approval.

## Custom Settings

- Record approved project-level tunable product limits and defaults (maximum
  lengths, page-size defaults and maximums, retention periods, numeric
  thresholds) in `CUSTOM_SETTINGS.md`; `SPECIFICATION.md` owns behavioral intent
  and `CUSTOM_SETTINGS.md` owns the approved concrete values.
- The two files must not contradict each other. If they appear to conflict,
  stop and ask which source must be corrected rather than choosing one.
- Do not silently invent a value that materially changes accepted input or
  observable behavior when the specification, existing approved behavior, or
  `CUSTOM_SETTINGS.md` does not define it: propose the value with its reason,
  ask for approval, record it in `CUSTOM_SETTINGS.md`, then synchronize it
  through `custom-settings`.
- Never store secrets, environment-specific connection details, package
  versions, HTTP status codes, ports, migration identifiers, or incidental
  implementation constants in `CUSTOM_SETTINGS.md`.

## Core Defaults

- Prefer simple, maintainable solutions over unnecessary abstractions; keep
  architectural complexity proportional to current requirements and avoid
  speculative abstractions.
- Do not introduce frameworks, libraries, infrastructure, or architectural
  patterns without a concrete current need.
- Keep changes focused on the requested scope and preserve existing behavior
  unless the task or approved specification requires changing it.
- Before implementing a questionable request, identify the concrete concern —
  duplication, poor cohesion, unreliable triggering or loading, context cost,
  conflict with accepted architecture or policy, unnecessary complexity — and
  propose an alternative. This never permits silently rewriting or ignoring the
  user's requirement.

## Architecture Defaults

Decision summary for planning; the authoritative rules are the path-scoped files
in `.claude/rules/`.

- Adopted: Clean Architecture with `Domain`, `Application`, `Infrastructure`,
  and `Api` projects; Application Services orchestrate use cases; ASP.NET Core
  Controllers are the HTTP entry point; persistence goes through specific
  repositories and `IUnitOfWork`, implemented with EF Core in Infrastructure;
  Domain entities are simple by default.
- Repository layout: `backend/<Name>.<Layer>/` holds the .NET production
  projects and, beside them, the backend test projects (for example
  `<Name>.Application.Tests`, `<Name>.IntegrationTests`); `frontend/<Name>.Web/`
  holds the Angular workspace including its tests; `docs/` holds maintained
  documentation. Keep these areas separated and do not create a top-level
  `tests/` directory.
- Do not introduce CQRS handlers, MediatR, Kommand, Vertical Slice
  Architecture, or similar mediator-based organization unless explicitly
  approved.
- Also not adopted (adoption is Reserved): Rich Domain Model and DDD tactical
  patterns, event sourcing, microservices, a project-wide Result/railway model,
  Minimal API endpoints as the HTTP model.

## Decision Control

Classify a decision before acting on it:

- **Decided** — settled by the product sources, this file,
  `docs/technology-stack.md`, `.claude/rules/`, an accepted record in
  `docs/decisions/`, or established project structure. Follow it; reopening it
  requires approval.
- **Delegated** — local and reversible, and changes no boundary, dependency,
  accepted convention, public contract, or observable behavior. This includes
  reasonable internal implementation details that do not change observable
  product behavior, and routine local decisions already constrained by the
  specification, approved stack, existing code, or rules. Decide without
  asking.
- **Reserved** — requires explicit approval unless already required by the
  specification or established project structure:
  1. changing an accepted project or architecture decision;
  2. a new architectural style or pattern (Rich Domain Model or DDD tactical
     patterns, CQRS/MediatR/Vertical Slice Architecture, event sourcing,
     microservices);
  3. a new production project, layer, or assembly, a changed project reference
     graph, or an additional `DbContext`/persistence boundary;
  4. changed persistence boundaries or persistence technology;
  5. a new infrastructure category (messaging, background processing,
     distributed caching, search, external storage, external identity);
  6. a major library or framework, or replacing an approved baseline technology;
  7. a project-wide convention or abstraction other code must follow (for
     example a project-wide Result model);
  8. a new or changed authentication/authorization architecture;
  9. a breaking public API change or adopting API versioning;
  10. product behavior or tunable values not defined by the product sources.

Unclear case — any "yes" makes it Reserved: (1) Does it add, remove, or replace
a dependency, framework, or infrastructure capability? (2) Does it change a
project/layer/reference boundary? (3) Does it establish a convention other code
is expected to follow? (4) Does it change observable behavior or a public
contract? (5) Would it be expensive to reverse once other code depends on it?

For a Reserved decision, stop that part of the work and issue a Decision Request
through `architecture-decision`; continue only with compliant non-Reserved work.
An explicit user instruction counts as approval and is recorded through the same
workflow.

In an autonomous or headless run, implement a Reserved change only when the user
explicitly approved that specific change beforehand, naming the change and its
scope; a broad or vague instruction is not approval, and the approval is
recorded through `architecture-decision`. Never make or approve a new Reserved
decision there: on an unexpected Reserved choice, stop that part of the work,
continue only on a policy-compliant non-Reserved path, and report every
unresolved Decision Request in the final report, with a decision log of what was
implemented under which approval.

## Git

- Do not commit, push, merge, rebase, reset, force-push, delete branches, or
  perform other repository-changing Git operations unless the user explicitly
  requested that operation or pre-approved it with a named operation and scope. A
  generic "approved workflow", general task approval, or a workflow step that
  mentions committing is not that authority.
- An explicit request to rewrite a named branch, including `main`, is valid
  unless another policy forbids it.
- Task-start check: before a task that will change files or repository state in
  a Git working tree, check for pre-existing uncommitted changes (staged,
  unstaged, untracked). If any exist, ask and offer only two options: commit the
  identified changes within a scope the user authorizes, or suspend the whole task
  until the user has cleaned up manually. In a headless or noninteractive run
  without an already adequate choice, pause safely: change nothing and report the
  changes found. Changes made during the current task are not this condition.
- Before a destructive Git operation, re-check the authority for it and that
  changes you did not make are preserved; procedure: `git-workflow`.
- Parallel implementation work must use separate branches or worktrees; keep
  unrelated changes out of the current branch.

## Workflow Routing

Workflow skills own procedures, stop conditions, and output shape. Run the one
that matches:

| Situation | Workflow |
| --- | --- |
| Any implementation change, from first inspection to completion gates | `development-workflow` |
| Final verification before declaring work complete | `verify` |
| Code review or an independent second pass | `code-review` (agent: `code-reviewer`) |
| Failing build or tests to repair | `build-fix` |
| Adding, updating, or removing a NuGet/npm dependency | `add-dependency` |
| `CUSTOM_SETTINGS.md` value added, changed, or removed | `custom-settings` |
| New solution or project, or a repository-structure change | `project-structure` |
| Reserved decision or Decision Request | `architecture-decision` |
| Security audit or scan | `security-scan` |
| Any Git operation | `git-workflow` |

Path-scoped rules in `.claude/rules/` load automatically with matching files;
knowledge skills provide technique on demand. Human maintainers: `.claude/MAP.md`.
