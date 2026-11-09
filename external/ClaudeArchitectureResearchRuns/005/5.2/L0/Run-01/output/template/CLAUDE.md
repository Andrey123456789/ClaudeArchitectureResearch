> Level: 0 Core | Owns: precedence, product governance, scope and simplicity, challenge obligation, decision control, version-control safety, work routing | Scope: common | Loads: always (project memory) | Depends on: none

# Project Instructions

This repository is a reusable template for a layered web application: a .NET
backend under `backend/<Name>.<Layer>/` and a TypeScript frontend under
`frontend/<Name>.Web/`.

Vocabulary: **must / must not** — violation is a defect; **default** — deviation
needs a concrete reason and must be reported; **prefer / avoid** — guidance;
**requires approval** — a Reserved decision (see Decision Control).

## Instruction System

Engineering policy lives in `.claude/rules/`, organized by stability:
`0-core` → `1-architecture` → `2-technology` → `3-project`. A more volatile level
may depend on a more stable level, never the reverse. Path-scoped rules load
when matching files are read; workflows explicitly read the owners they need.
Workflows (procedures) and knowledge skills (technique) never override rules.
Maintainer map (not loaded): `.claude/INSTRUCTION_MAP.md`.

## Precedence

1. Approval boundaries and decision control in this file.
2. Engineering policy in `.claude/rules/`. A conflict between levels is a
   template defect: report it instead of choosing silently.
3. Product inputs — `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature
   specifications, task prompts — define what to build. They may request a
   change to an engineering decision, but must not silently override
   engineering policy; such a request is a Decision Request.

An explicit user instruction can approve a Reserved decision; the accepted
decision is then recorded through `architecture-decision`.

## Product Governance

- When `SPECIFICATION.md` is non-empty, it is the authoritative source for
  project-specific functional requirements and observable product behavior
  (an empty file in the reusable template is intentional).
- Do not silently weaken, contradict, or materially extend approved behavior,
  and do not silently invent user-visible rules, limits, defaults, restrictions,
  or workflows — not even when they seem reasonable.
- If an omitted product detail must be decided and the decision materially
  affects observable behavior, propose the smallest reasonable option and ask
  for approval.
- Routine internal implementation choices that do not change observable
  behavior are Delegated and do not require approval.
- String semantics are product behavior when observable: case sensitivity,
  collation, culture-sensitive vs. ordinal comparison, normalization or
  canonicalization, trimming, uniqueness, and lookup semantics. When product
  sources do not define them and the choice matters, do not choose silently —
  ask for approval, even when the choice would be expressed only through
  database or framework configuration.
- `CUSTOM_SETTINGS.md` owns approved project-level tunable limits and defaults
  (maximum lengths, page sizes, retention periods, numeric thresholds);
  `SPECIFICATION.md` owns behavioral intent.
- `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` must not contradict each other.
  If they conflict, stop and resolve which source must be corrected before
  implementation continues.
- Do not silently invent a tunable value that materially changes accepted input
  or observable behavior: propose it, get approval, record it in
  `CUSTOM_SETTINGS.md`, and synchronize it (run `custom-settings`).
- Do not store secrets, environment-specific connection details, package
  versions, HTTP status codes, ports, migration identifiers, or incidental
  implementation constants in `CUSTOM_SETTINGS.md`.

## Scope and Simplicity

- Keep changes focused on the requested scope and preserve existing behavior
  unless the task or approved specification requires a change.
- Default: prefer simple, maintainable solutions; keep architectural complexity
  proportional to current requirements; avoid speculative abstractions.
- Do not introduce frameworks, libraries, infrastructure, or architectural
  patterns without a concrete current need.

## Challenge Obligation

Before implementing a questionable request, identify the concrete concern —
duplication, poor cohesion, trigger or loading problems, context cost, conflict
with accepted architecture or product sources, unnecessary complexity — and
propose an alternative. Do not silently rewrite or ignore the requirement.

## Decision Control

- **Decided** — settled by these rules, the decision summaries below, or a
  recorded accepted decision. Follow it; do not reopen it without approval.
- **Delegated** — local and reversible, and does not materially change a
  boundary, dependency, accepted convention, public contract, or observable
  behavior. Decide and proceed.
- **Reserved** — requires approval. Reserved decisions include at least:
  1. changing an accepted project or architecture decision;
  2. adopting a new architectural style or pattern;
  3. adding a production project, layer, or assembly, or changing the project
     reference graph;
  4. changing persistence boundaries or persistence technology;
  5. adding an infrastructure category (messaging, background processing,
     distributed cache, search, external storage, external identity);
  6. adding a major library or framework, or replacing a baseline technology;
  7. introducing a project-wide convention or abstraction other code must follow;
  8. changing authentication or authorization architecture;
  9. making a breaking public API change or adopting API versioning;
  10. defining product behavior or tunable values not defined by product sources.

For an unclear case, ask: (1) does it add, remove, or replace a dependency,
framework, or infrastructure capability? (2) does it change a project, layer, or
reference boundary? (3) does it establish a convention other code is expected to
follow? (4) does it change observable behavior or a public contract? (5) would it
be expensive to reverse once other code depends on it? Any yes makes it Reserved.

For a Reserved decision, do not implement it; issue a Decision Request through
`architecture-decision`. In an autonomous or headless run, take only a
policy-compliant non-Reserved path and report every unresolved Decision Request
explicitly.

## Version-Control Safety

- Do not commit, push, merge, rebase, reset, force-push, delete branches, or
  perform other repository-changing version-control operations unless
  explicitly requested.
- Parallel implementation work must use separate branches or worktrees; keep
  unrelated changes out of the current branch.

## Work Routing

- Implementation work (feature, bug fix, new application): run `develop`. It
  owns the development procedure, review, and completion through `verify`.
- New solution or structural change: `project-structure`.
- Failing build or tests: `build-fix`.
- Adding or updating a package: `add-dependency`.
- `CUSTOM_SETTINGS.md` change: `custom-settings`.
- Reserved decision: `architecture-decision`.
- Branches, commits, pushes, merges, pull requests: `git-workflow`.
- Security audit or security-sensitive change: `security-scan`.
- Independent review: the `code-reviewer` agent (runs `code-review`).
- Technology technique: knowledge skills, loaded on demand by description.

## Decision Summaries (always loaded)

@.claude/rules/1-architecture/overview.md
@.claude/rules/3-project/decisions.md
