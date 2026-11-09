> Always-loaded project policy. Owns: product-source authority, change discipline, decision control, architecture decisions, Git boundaries, workflow routing · Scope: common, repo/meta · Loads: always; imports docs/technology-stack.md · Depends on: none · Map: .claude/MAP.md

# Project Instructions

This repository is a reusable template for ASP.NET Core + Angular applications
based on Clean Architecture.

@docs/technology-stack.md

## Normative Vocabulary

- **must / must not** — violation is a defect. Plain imperatives (do / do not)
  carry the same force.
- **default** — deviation requires a concrete reason and must be reported.
- **prefer / avoid** — guidance.
- **requires approval** — a Reserved decision (see Decision Control).

## Product Sources

`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, optional feature specifications, and
task prompts are product inputs, not instruction layers. They may request a
change to an engineering decision; that request goes through Decision Control
and never silently overrides these instructions or `.claude/rules/`.

- When `SPECIFICATION.md` is non-empty, it is the authoritative source for
  project-specific functional requirements and observable product behavior.
  An empty `SPECIFICATION.md` in the template is intentional.
- Do not silently weaken, contradict, or materially extend approved behavior,
  and do not invent user-visible behavior, limits, defaults, restrictions, or
  workflows merely because they seem reasonable or are not explicitly forbidden.
- If an omitted product detail must be decided and materially affects
  observable behavior, propose the smallest reasonable option and ask for
  approval.
- Default: routine internal implementation choices that do not change
  observable behavior are Delegated and do not require approval.
- String semantics are product behavior when observable: case sensitivity,
  collation, culture-sensitive vs. ordinal comparison,
  normalization/canonicalization, trimming, uniqueness, and lookup. When the
  approved sources do not define them, ask before choosing; do not let database
  or framework defaults decide them silently.
- `CUSTOM_SETTINGS.md` holds approved project-level tunable product limits and
  defaults (for example maximum lengths, page sizes, retention periods, numeric
  thresholds); `SPECIFICATION.md` owns behavioral intent.
- `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` must not contradict each other.
  If they appear to conflict, stop and ask which source must be corrected.
- Do not silently invent a tunable value that materially changes accepted input
  or observable behavior: propose it, obtain approval, record it in
  `CUSTOM_SETTINGS.md`, and synchronize it (`custom-settings` workflow).
- Do not store secrets, environment-specific connection details, package
  versions, HTTP status codes, ports, migration identifiers, or incidental
  implementation constants in `CUSTOM_SETTINGS.md`.

## Change Discipline

- Default: choose the simplest maintainable solution; keep architectural
  complexity proportional to current requirements and avoid speculative
  abstractions.
- Do not introduce frameworks, libraries, infrastructure, or architectural
  patterns without a concrete current need.
- Keep changes focused on the requested scope and preserve existing behavior
  unless the task or approved specification requires a change.
- Before implementing a questionable request, identify the concrete concern —
  for example duplication, poor cohesion, trigger or loading problems, context
  cost, conflict with an accepted decision, or unnecessary complexity — and
  propose an alternative. The decision stays with the user: do not silently
  rewrite, narrow, or ignore the requirement.

## Decision Control

Classify every consequential choice before acting on it:

- **Decided** — already settled by these instructions, the technology stack,
  accepted decision records, or existing code. Follow it; do not reopen it
  without approval.
- **Delegated** — local, reversible, and does not materially change a boundary,
  dependency, accepted convention, public contract, or observable behavior.
  Decide it yourself; routine choices already constrained by the specification,
  the stack, existing code, or the rules need no approval.
- **Reserved** — changes an accepted architecture, stack, or public-behavior
  decision, or is materially expensive to reverse. Requires approval.

Reserved decisions include at least:

1. changing an accepted project or architecture decision;
2. adopting an architectural style or pattern listed as not adopted below;
3. adding a production project, layer, or assembly, or changing the project
   reference graph;
4. changing persistence boundaries or persistence technology, including
   multiple `DbContext` boundaries;
5. adding an infrastructure category: messaging, background processing,
   distributed caching, search, external storage, or external identity;
6. adding a major library or framework, or replacing an approved baseline
   technology;
7. introducing a project-wide convention or abstraction that other code is
   expected to follow;
8. changing the authentication/authorization architecture;
9. making a breaking public API change or adopting API versioning;
10. defining product behavior or tunable values that the product sources do
    not define.

When the class is unclear, ask: (1) Does it add, remove, or replace a
dependency, framework, or infrastructure capability? (2) Does it change a
project, layer, or reference boundary? (3) Does it establish a convention other
code is expected to follow? (4) Does it change observable behavior or a public
contract? (5) Would it be expensive to reverse once other code depends on it?
Any "yes" makes the decision Reserved.

For a Reserved decision that the specification or the established project
structure does not already require, stop that part of the work and issue a
Decision Request through the `architecture-decision` workflow. An explicit user
instruction counts as approval, but the accepted decision must still be
recorded through that workflow. In an autonomous or headless run, continue only
along a policy-compliant non-Reserved path and report every unresolved Decision
Request explicitly; never make a Reserved decision silently.

## Architecture Decisions

Decision summary for planning. The detailed, path-scoped rules are
`.claude/rules/architecture.md`, `persistence.md`, and `api.md`.

- **Adopted:** Clean Architecture with `Domain`, `Application`,
  `Infrastructure`, and `Api` projects; dependencies point inward; Application
  Services orchestrate use cases; ASP.NET Core Controllers are the HTTP entry
  point; persistence goes through specific repository interfaces and
  `IUnitOfWork`; EF Core stays inside Infrastructure; Domain entities are simple
  by default.
- **Not adopted — adopting any of these requires approval:** CQRS handlers,
  MediatR, Kommand, or similar mediator-based organization; Vertical Slice
  Architecture; Rich Domain Model and DDD tactical patterns (Aggregate Roots,
  Domain Events, Specifications, Domain Services, systematic Value Objects);
  event sourcing; a project-wide Result/railway-oriented model; microservices;
  Minimal API endpoints.
- **Accepted project decisions:** recorded under `docs/decisions/` by the
  `architecture-decision` workflow, which also updates this section or
  `docs/technology-stack.md` when a decision changes a default.

## Workflows

Run the matching workflow skill:

| Situation | Workflow |
|---|---|
| Implementing a feature, bug fix, refactor, or other change | `development-workflow` |
| Creating a solution or changing projects or top-level structure | `project-structure` |
| Adding, updating, or removing a NuGet or npm dependency | `add-dependency` |
| A Reserved decision or a Decision Request | `architecture-decision` |
| Adding, changing, or removing a `CUSTOM_SETTINGS.md` value | `custom-settings` |
| Repairing a failing build or failing tests | `build-fix` |
| Reviewing a diff, PR, or completed change | `code-review` (agent: `code-reviewer`) |
| Checking work before declaring it complete | `verify` |
| Any Git operation | `git-workflow` |
| Security audit or security-sensitive review | `security-scan` |

Path-scoped rules in `.claude/rules/` load with matching files:
`architecture.md`, `persistence.md`, `api.md`, `error-handling.md`,
`performance.md`, and `coding-style.md` (backend code); `testing.md` (backend
tests); `angular.md` (frontend); `security.md` (code, configuration, and
container files); `dependencies.md` (package manifests); `repository-layout.md`
(physical structure). When work needs a rule whose files are not in context
yet — new code, reviews, verification — read that rule file explicitly.

Knowledge skills supply technique on demand and never override rules. Changes
to the instruction system itself are user-invoked (`/template-maintenance`).

## Git

- Do not commit, push, merge, rebase, reset, force-push, delete branches, or
  perform other repository-changing Git operations unless explicitly requested.
- Keep unrelated changes out of the current branch; parallel implementation
  work must use separate branches or worktrees.
