> Owner: operating policy, product-source authority, architecture decisions, decision control, workflow routing | Scope: common | Loads: always | Enforced: hooks in `.claude/settings.json`

# Project Instructions

Reusable template for ASP.NET Core + Angular applications based on Clean
Architecture. Maintainers: the instruction map is `.claude/MAP.md` (not loaded
automatically).

## Vocabulary

**must / must not** — violation is a defect. **default** — deviation needs a
concrete reason that you report. **prefer / avoid** — guidance. **requires
approval** — a Reserved decision (see Decision Control below).

## Product Sources

`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, optional feature specifications, and
task prompts are inputs, not instruction layers. They may request a change to an
engineering decision but never silently override these instructions.

- When `SPECIFICATION.md` is non-empty, it is the authoritative source for
  project-specific functional requirements and observable product behavior. An
  empty file in the template is intentional.
- Do not silently weaken, contradict, or materially extend approved behavior,
  and do not invent user-visible rules, restrictions, limits, defaults, or
  workflows merely because they seem reasonable.
- If an omitted product detail must be decided and materially affects observable
  behavior, propose the smallest reasonable option and ask for approval.
- String semantics that affect equality, uniqueness, lookup, or accepted input
  are product behavior, even when expressed through database collation or
  framework defaults: case sensitivity, collation, culture vs. ordinal
  comparison, normalization, trimming. When product sources do not define them,
  ask before choosing.
- When a new behavioral rule is approved, update the durable source of truth,
  including `SPECIFICATION.md` when appropriate.
- `CUSTOM_SETTINGS.md` holds approved project-level tunable limits and defaults
  (maximum lengths, page sizes, retention periods, numeric thresholds);
  `SPECIFICATION.md` owns behavioral intent. The two must not contradict each
  other; if they appear to conflict, stop and ask which source to correct.
- Do not silently invent a tunable value that materially changes accepted input
  or observable behavior: propose it with its reason, get approval, record it in
  `CUSTOM_SETTINGS.md`, then synchronize it through the `custom-settings`
  workflow.
- Never put secrets, environment-specific connection details, package versions,
  HTTP status codes, ports, migration identifiers, or incidental implementation
  constants in `CUSTOM_SETTINGS.md`.

## Core Defaults

- Default: prefer simple, maintainable solutions; keep architectural complexity
  proportional to current requirements and avoid speculative abstractions.
- Do not introduce frameworks, libraries, infrastructure, or architectural
  patterns without a concrete current need.
- Keep changes focused on the requested scope and preserve existing behavior
  unless the task or approved specification requires a change.
- Before implementing a questionable request, name the concrete concern
  (duplication, poor cohesion, trigger or context-cost problems, architecture
  conflict, unnecessary complexity) and propose an alternative. This never
  authorizes silently rewriting or ignoring the user's requirement.

## Architecture Decisions

Decided (summary; normative detail lives in the file named):

- Clean Architecture with `Domain`, `Application`, `Infrastructure`, and `Api`
  projects; dependencies point inward (`.claude/rules/architecture.md`).
- Simple domain entities, Application Services as use-case orchestration, thin
  ASP.NET Core Controllers (`.claude/rules/architecture.md`).
- Specific repository interfaces in Application, EF Core implementations in
  Infrastructure, `IUnitOfWork` as the commit boundary
  (`.claude/rules/architecture.md`, `.claude/rules/persistence.md`).
- Default repository layout: `backend/<Name>.<Layer>/` for production and backend
  test projects, `frontend/<Name>.Web/` for the Angular workspace, `docs/` for
  documentation, each clearly separated; no top-level `tests/` directory.
- Approved stack and conditional technologies: `docs/technology-stack.md`
  (imported at the end of this file). Accepted decisions: `docs/decisions/`.

Not adopted — introducing any of these requires approval:

- CQRS handlers, MediatR, Kommand, Vertical Slice Architecture, or similar
  mediator-based organization; event sourcing; microservices.
- Rich Domain Model and DDD tactical patterns
  (`.claude/rules/architecture.md` § Domain); generic repository contracts in
  Application; Minimal APIs as the endpoint model; a project-wide Result model
  (`.claude/rules/error-handling.md` § Expected Outcomes).

## Decision Control

Classify a consequential choice before acting on it:

- **Decided** — settled by these instructions, `docs/technology-stack.md`, a
  record in `docs/decisions/`, the approved specification, or established project
  structure. Follow it; do not reopen it without approval.
- **Delegated** — local, reversible, and not materially changing a boundary,
  dependency, accepted convention, public contract, or observable behavior.
  Routine internal implementation choices are Delegated and need no approval.
- **Reserved** — requires approval. At least:
  1. changing an accepted project or architecture decision;
  2. adopting anything listed under "Not adopted", or another architectural
     style or pattern;
  3. adding a production project, layer, or assembly, or changing the project
     reference graph;
  4. changing persistence boundaries or technology (including multiple
     `DbContext` boundaries);
  5. adding an infrastructure category: messaging, background processing,
     distributed cache, search, external storage, external identity;
  6. adding a major library or framework, or replacing an approved baseline
     technology;
  7. introducing a project-wide convention or abstraction that other code is
     expected to follow;
  8. changing authentication or authorization architecture;
  9. making a breaking public API change or adopting API versioning;
  10. defining product behavior or tunable values that product sources do not
      define (see Product Sources).

When unsure, any "yes" makes it Reserved: Does it add, remove, or replace a
dependency, framework, or infrastructure capability? Change a project, layer, or
reference boundary? Establish a convention other code is expected to follow?
Change observable behavior or a public contract? Become expensive to reverse once
other code depends on it?

For a Reserved decision, pause that part of the work and present a Decision
Request with **Context**, **Options**, **Recommendation**, **Blocked** (what
waits), and **Proceeding with** (the non-Reserved work that continues), then
follow the `architecture-decision` workflow. An explicit user instruction counts
as approval; record the accepted decision through that workflow. In autonomous or
headless runs, take only a policy-compliant non-Reserved path and report
unresolved Decision Requests explicitly; never make a Reserved decision silently.

## Development Workflow

- Inspect the relevant existing code before non-trivial changes and apply the
  rules and skills that govern it.
- Before planning or implementing a new application or substantial feature, read
  `SPECIFICATION.md`.
- Run the workflow that owns the activity:
  - new solution, project, or structural reorganization → `project-structure`;
  - adding, updating, or removing any NuGet or npm dependency → `add-dependency`;
  - change to `CUSTOM_SETTINGS.md` → `custom-settings`;
  - Reserved decision → `architecture-decision`;
  - broken build or failing tests → `build-fix`;
  - security audit or materially security-sensitive change → `security-scan`;
  - requested Git operation → `git-workflow`.
- For substantial feature work or a newly implemented application, run the
  `code-review` workflow before the final `verify` workflow.
- Before declaring implementation work complete, run the `verify` workflow at the
  depth the scope and risk require.
- Restructuring the instruction system itself (rules, skills, hooks, map) goes
  through the user-invoked `/template-maintenance` workflow.

## Git

- Do not commit, push, merge, rebase, reset, force-push, delete branches, or
  perform other repository-changing Git operations unless explicitly requested.
- Parallel implementation work must use separate branches or worktrees; keep
  unrelated changes out of the current branch.

## Technology Stack

@docs/technology-stack.md
