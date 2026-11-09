> **Always-loaded policy** · Owns: product-source authority, engineering defaults, decision control, challenge obligation, Git boundary, procedure routing · Scope: common, repo/meta · Loading: always (project root)

# Project Instructions

Reusable template for an ASP.NET Core backend with an optional frontend. The
architecture style, persistence technology, backend test framework, and frontend
framework are capability selections recorded in `docs/capability-selection.md`.

Planning-time decisions (always loaded):

@docs/technology-stack.md
@docs/capability-selection.md

## Normative Vocabulary

- **must / must not** — a violation is a defect.
- **default** — deviation requires a concrete reason and must be reported.
- **prefer / avoid** — guidance.
- **requires approval** — a Reserved decision (see Decision Control).

## Product Sources

`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, optional feature specifications, and
task prompts are product/task inputs, not instruction layers. They may request an
engineering decision change, but they never silently override engineering policy;
such a request goes through Decision Control.

- When `SPECIFICATION.md` is non-empty, it is the authoritative source for
  project-specific functional requirements and observable product behavior. An
  empty `SPECIFICATION.md` in the reusable template is intentional.
- Do not silently weaken, contradict, or materially extend approved behavior, and
  do not invent user-visible behavior, rules, limits, defaults, restrictions, or
  workflows merely because they seem reasonable or are not explicitly forbidden.
- If an omitted product detail must be decided and materially affects observable
  product behavior, propose the smallest reasonable option and ask for approval.
- Routine internal implementation details that do not change observable behavior
  do not require approval.
- String semantics are product behavior when observable: case sensitivity,
  database collation, culture-sensitive vs. ordinal comparison,
  normalization/canonicalization, automatic trimming, uniqueness, and lookup. When
  the approved sources do not define them and the choice materially affects
  equality, uniqueness, lookup, or accepted input, do not choose silently — ask for
  approval. This holds even when the choice would be expressed only through
  database configuration or framework defaults.
- `CUSTOM_SETTINGS.md` holds approved project-level tunable product limits and
  defaults (for example maximum lengths, page-size defaults and maximums, retention
  periods, numeric thresholds). `SPECIFICATION.md` owns behavioral intent;
  `CUSTOM_SETTINGS.md` owns the approved concrete values.
- `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` must not contradict each other. If
  they appear to conflict, stop and ask which source must be corrected; do not
  choose one silently.
- Do not silently invent a tunable value that materially changes accepted input or
  observable behavior when the specification, existing approved behavior, or
  `CUSTOM_SETTINGS.md` does not define it. Propose the value with its reason, ask
  for approval, record it in `CUSTOM_SETTINGS.md`, and synchronize it with the
  `custom-settings` workflow.
- Do not store secrets, environment-specific connection details, package
  versions, HTTP status codes, ports, migration identifiers, or incidental
  implementation constants in `CUSTOM_SETTINGS.md`.

## Engineering Defaults

- Default: prefer simple, maintainable solutions; keep architectural complexity
  proportional to current requirements and avoid speculative abstractions.
- Do not introduce frameworks, libraries, infrastructure, or architectural
  patterns without a concrete current need.
- Keep changes focused on the requested scope and preserve existing behavior
  unless the task or the approved specification requires changing it.

## Challenge Obligation

Before implementing a questionable request, identify the concrete concern — for
example duplication, poor cohesion, trigger or loading problems, context cost,
architecture conflict, or unnecessary complexity — and propose an alternative.
This never authorizes silently rewriting or ignoring the user's requirement: state
the concern, then follow the user's decision.

## Decision Control

Classify every consequential choice before acting:

- **Decided** — already settled by the approved sources, the planning-time
  decisions above, existing code, or the rules; follow it and do not reopen it
  without approval.
- **Delegated** — local, reversible, and does not materially change a boundary,
  dependency, accepted convention, public contract, or observable behavior; decide
  it without asking. Do not ask for approval for routine local implementation
  decisions already constrained by these sources.
- **Reserved** — requires explicit approval before it is introduced, unless the
  approved specification or established project structure already requires it.

Reserved decisions include at least:

1. changing an already accepted project or architecture decision, including a
   capability selection or an observable declared capability property;
2. adopting a new architectural style or pattern, for example CQRS, a mediator,
   Vertical Slice Architecture, event sourcing, microservices, a Rich Domain Model
   or systematic DDD tactical patterns, or a project-wide Result/railway model;
3. adding a production project, layer, or assembly, or changing the project
   reference graph;
4. changing persistence boundaries or persistence technology, including multiple
   persistence contexts or a substantially different persistence technology;
5. adding a new infrastructure category such as messaging, background processing,
   distributed caching, search, external storage, or external identity;
6. adding a major library or framework, or replacing an approved baseline
   technology;
7. introducing a project-wide convention or abstraction that other code is
   expected to follow;
8. changing authentication/authorization architecture;
9. making a breaking public API change or adopting API versioning;
10. defining product behavior or tunable values that the product sources do not
    define.

For unclear cases, any "yes" makes the decision Reserved: Does it add, remove, or
replace a dependency, framework, or infrastructure capability? Does it change a
project/layer/reference boundary? Does it establish a convention other code is
expected to follow? Does it change observable behavior or a public contract?
Would it be expensive to reverse after other code depends on it?

A Reserved decision is raised as a Decision Request through the
`architecture-decision` workflow. An explicit user instruction may count as
approval, but the accepted decision must be recorded through that workflow. In an
autonomous or headless run, choose only a policy-compliant non-Reserved path and
report unresolved Decision Requests explicitly; never make a Reserved decision
silently.

## Procedures

Workflows own the multi-step procedures; run them rather than improvising:

- implementation work (new application, feature, bug fix, refactoring) →
  `development-workflow` (it owns the inspect, implement, review, and verify steps);
- before adding, updating, or removing any NuGet or npm dependency → `add-dependency`;
- `CUSTOM_SETTINGS.md` change → `custom-settings`;
- Reserved decision, Decision Request, or ADR → `architecture-decision`;
- repository-changing Git work → `git-workflow`;
- broken build or failing tests → `build-fix`;
- solution scaffolding or structural change → `project-structure`;
- security audit → `security-scan`.

Path-scoped rules in `.claude/rules/` load with matching files. The human map of
the instruction system is `.claude/MAP.md` (not loaded automatically).

## Git

- Do not commit, push, merge, rebase, reset, force-push, delete branches, or
  perform other repository-changing Git operations unless explicitly requested.
- Keep unrelated changes out of the current branch.
- Parallel implementation work must use separate branches or worktrees.
