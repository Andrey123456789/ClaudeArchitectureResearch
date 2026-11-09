> Owns: product-source authority, core and architecture defaults, decision control, challenge duty, development workflow, Git safety | Scope: common | Loads: always (imports docs/technology-stack.md)

# Project Instructions

This repository is a reusable template for ASP.NET Core + Angular applications
based on Clean Architecture.

Approved technology stack, conditional technologies, and repository layout:
@docs/technology-stack.md

Vocabulary: **must / must not** — violation is a defect; **default** — deviation
requires a concrete reason that is reported; **prefer / avoid** — guidance;
**requires approval** — a Reserved decision (see Decision Control).

## Product Sources

`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, optional feature specifications, and
task prompts are product inputs, not instruction layers. They may request a
decision change but must not silently override engineering policy.

- When `SPECIFICATION.md` is non-empty, it is the authoritative source for
  project-specific functional requirements and observable product behavior. An
  empty `SPECIFICATION.md` in the reusable template is intentional.
- Do not silently weaken, contradict, or materially extend approved behavior,
  and do not invent user-visible rules, restrictions, limits, defaults, or
  workflow behavior merely because they seem reasonable.
- If an omitted product detail must be decided and materially affects
  observable product behavior, propose the smallest reasonable option and ask
  for approval.
- Routine internal implementation choices that do not change observable product
  behavior do not require approval.
- String semantics are product behavior when observable. If product sources do
  not define them and the choice materially affects equality, uniqueness,
  lookup, or accepted input, do not silently choose case sensitivity, database
  collation, culture-sensitive vs. ordinal comparison,
  normalization/canonicalization, or automatic trimming — ask for approval.
- When a new behavioral rule is approved, keep the durable source of truth
  synchronized, updating `SPECIFICATION.md` when appropriate.
- `CUSTOM_SETTINGS.md` owns approved project-level tunable product limits and
  defaults (maximum lengths, page sizes, retention periods, numeric thresholds);
  `SPECIFICATION.md` owns behavioral intent. They must not contradict each
  other: if they appear to conflict, stop and ask which source must be corrected.
- Do not silently invent a tunable value that materially changes accepted input
  or observable behavior when no product source defines it: propose the value
  and why it is needed, get approval, record it in `CUSTOM_SETTINGS.md`, then
  run `custom-settings`.
- Never store secrets, environment-specific connection details, package
  versions, HTTP status codes, ports, migration identifiers, or incidental
  implementation constants in `CUSTOM_SETTINGS.md`.

## Core Defaults

- Prefer simple, maintainable solutions; keep architectural complexity
  proportional to current requirements and avoid speculative abstractions.
- Do not introduce frameworks, libraries, infrastructure, or architectural
  patterns without a concrete current need.
- Do not create speculative projects, infrastructure, empty directory trees, or
  generic `Common`/`Helpers`/`Utils` buckets solely to make the repository look
  architectural.
- Keep changes focused on the requested scope and preserve existing behavior
  unless the task or approved specification requires changing it.

## Architecture Defaults

Decision summary — the rules in `.claude/rules/architecture.md` own the details:
Clean Architecture with `Domain`, `Application`, `Infrastructure`, and `Api`
projects; simple domain entities; Application Services as use-case
orchestration; specific repositories with `IUnitOfWork` as the commit boundary;
EF Core as an Infrastructure detail; ASP.NET Core Controllers as the HTTP entry
point; `Program.cs` as the composition root.

Explicitly not adopted (adopting any of these requires approval): CQRS handlers,
MediatR, Kommand, Vertical Slice Architecture or similar mediator-based
organization; event sourcing; microservices; Rich Domain Model or systematic DDD
tactical patterns; a project-wide Result/railway-oriented model; Minimal API
endpoints; multiple `DbContext` persistence boundaries.

## Decision Control

- **Decided** — settled by these instructions, `docs/technology-stack.md`, or
  established project structure (`docs/decisions/` keeps the history and
  rationale). Follow it; do not reopen it without approval.
- **Delegated** — local, reversible, and not materially changing a boundary,
  dependency, accepted convention, public contract, or observable behavior.
  Decide autonomously within the rules.
- **Reserved** — requires explicit approval unless already required by the
  specification or established project structure:
  1. changing an accepted project or architecture decision;
  2. adopting an architectural style or pattern listed as not adopted above;
  3. adding a production project/layer/assembly or changing the project
     reference graph;
  4. changing persistence boundaries or persistence technology;
  5. adding an infrastructure category: messaging, background processing,
     distributed cache, search, external storage, or external identity;
  6. adding a major library/framework or replacing an approved baseline
     technology;
  7. introducing a project-wide convention or abstraction that other code is
     expected to follow;
  8. changing authentication/authorization architecture;
  9. making a breaking public API change or adopting API versioning;
  10. defining product behavior or tunable values that product sources do not
      define (see Product Sources).

When unclear, ask: does it add, remove, or replace a dependency, framework, or
infrastructure capability? Change a project/layer/reference boundary? Establish
a convention other code must follow? Change observable behavior or a public
contract? Become expensive to reverse once other code depends on it? Any "yes"
makes it Reserved.

For a Reserved decision, raise a Decision Request through `architecture-decision`
before implementing it. An explicit user instruction counts as approval, but the
accepted decision must still be recorded there. In an autonomous or headless
run, take only a policy-compliant non-Reserved path and report unresolved
Decision Requests explicitly. Do not ask for approval of routine Delegated
choices already constrained by the specification, approved stack, existing
code, or the rules.

## Challenge Before Implementing

Before implementing a questionable request, identify its material concerns —
for example duplication, poor cohesion, trigger or loading problems, context
cost, conflict with architecture or these instructions, or unnecessary
complexity — and propose an alternative. This does not authorize silently
rewriting or ignoring the user's requirement: state the concern, then follow the
user's decision (Reserved changes still follow Decision Control).

## Development Workflow

1. Before planning or implementing a new application or substantial feature,
   read `SPECIFICATION.md`.
2. Inspect the relevant existing code before making non-trivial changes and
   apply the applicable rules from `.claude/rules/` and skills.
3. For substantial feature work or a newly implemented application, run
   `code-review` before the final `verify`.
4. Before declaring implementation work complete, run `verify` appropriate to
   the scope and risk.

Never weaken, delete, skip, or suppress relevant tests or compiler/analyzer
failures merely to make verification pass.

Run the matching workflow whenever its trigger applies:

| Trigger | Workflow |
|---|---|
| Create or reorganize the solution, add or remove projects | `project-structure` |
| Add, update, or remove a NuGet or npm dependency | `add-dependency` |
| Reserved or unclear architecture/stack/product decision | `architecture-decision` |
| `CUSTOM_SETTINGS.md` changes | `custom-settings` |
| Repair a failing build or failing tests | `build-fix` |
| Any requested Git operation | `git-workflow` |
| Security audit/scan, or a materially security-sensitive change | `security-scan` |
| Review of completed changes | `code-review` (or the `code-reviewer` agent) |
| Before declaring completion | `verify` |

## Git

- Do not commit, push, merge, rebase, reset, force-push, delete branches, or
  perform other repository-changing Git operations unless explicitly requested.
- Never discard, overwrite, reset, clean, or otherwise destroy user work to make
  a Git operation easier.
- Parallel implementation work must use separate branches or worktrees; keep
  unrelated changes out of the current branch.

Maintainers: `.claude/MAP.md` (not auto-loaded) lists every instruction file
with its owner, scope, loading, enforcement, and where new content belongs.
