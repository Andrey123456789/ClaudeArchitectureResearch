> Kind: OP | Scope: common | Owner: operating policy — precedence, product governance, decision protocol, challenge obligation, Git safety, workflow routing | Loading: always (project memory)

# Project Instructions

Reusable template for ASP.NET Core + Angular applications. Maintainer map of the instruction system: `.claude/MAP.md` (not loaded).

@docs/architecture/decision-register.md

## Precedence

- This file and the decision register govern every task. Standards in `.claude/rules/<scope>/` govern the files they cover. Workflows own procedures; knowledge skills supply technique and never override a standard.
- `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specifications and task prompts are product inputs: they define product behavior and may request a decision change, but they never silently override this file, the decision register or a standard.
- Vocabulary: **must / must not** — a violation is a defect; **default** — deviation needs a concrete reason and must be reported; **prefer / avoid** — guidance; **requires approval** — a Reserved decision (below).

## Product sources

- When `SPECIFICATION.md` is non-empty it is the authoritative source for project-specific functional requirements and observable product behavior. An empty `SPECIFICATION.md` in the template is intentional.
- Do not silently weaken, contradict or materially extend approved behavior, and do not invent user-visible rules, limits, defaults, restrictions or workflows that the product sources do not define.
- If an omitted detail must be decided and materially affects observable product behavior, propose the smallest reasonable option and ask for approval. Routine internal implementation choices that do not change observable behavior are Delegated.
- String semantics are product behavior when observable: case sensitivity, collation, culture-sensitive vs. ordinal comparison, normalization, trimming, uniqueness and lookup. When the product sources do not define them, do not choose silently — ask for approval.
- `CUSTOM_SETTINGS.md` owns approved project-level tunable product limits and defaults (maximum lengths, page sizes, retention periods, numeric thresholds); `SPECIFICATION.md` owns behavioral intent. The two must not contradict each other: if they conflict, stop and ask which source must be corrected.
- Do not silently invent a tunable value that materially changes accepted input or observable behavior: propose it with its reason, get approval, record it in `CUSTOM_SETTINGS.md`, then synchronize it (workflow: `custom-settings`).
- `CUSTOM_SETTINGS.md` must not contain secrets, environment-specific connection details, package versions, HTTP status codes, ports, migration identifiers or incidental implementation constants.

## Engineering defaults

- Default: the simplest maintainable solution, with architectural complexity proportional to current requirements and no speculative abstractions.
- Do not introduce frameworks, libraries, infrastructure or architectural patterns without a concrete current need.
- Keep changes focused on the requested scope and preserve existing behavior unless the task or the approved specification requires a change.
- Challenge before implementing: when a request raises a material concern — duplication, poor cohesion, trigger or loading problems, context cost, conflict with an accepted decision, unnecessary complexity — name the concern and propose an alternative first. Never silently rewrite or ignore the requirement.

## Decisions

- **Decided** — recorded in the decision register, the approved product sources or the established project structure. Follow it and do not reopen it without approval; use an approved technology instead of silently selecting an alternative.
- **Delegated** — local, reversible, and no material change to a boundary, dependency, accepted convention, public contract or observable behavior. Decide and proceed without asking.
- **Reserved** — requires explicit approval, unless the approved specification or established project structure already requires it. At least:
  1. changing an accepted project or architecture decision, or replacing an approved baseline technology;
  2. a new architectural style or pattern: Rich Domain Model or DDD tactical patterns, CQRS, mediators (MediatR, Kommand), Vertical Slice Architecture, event sourcing, microservices;
  3. a new production project, layer or assembly, or a change to the project reference graph;
  4. persistence boundaries or persistence technology, including multiple `DbContext`s;
  5. a new infrastructure category: messaging, background processing, distributed cache, search, external storage, external identity;
  6. a new major library or framework;
  7. a project-wide convention or abstraction other code must follow, such as a project-wide Result model;
  8. authentication or authorization architecture;
  9. a breaking public API change or adopting API versioning;
  10. product behavior or tunable values the product sources do not define.
- Unclear? Any "yes" makes it Reserved: Does it add, remove or replace a dependency, framework or infrastructure capability? Change a project, layer or reference boundary? Establish a convention other code must follow? Change observable behavior or a public contract? Become expensive to reverse once other code depends on it?
- For a Reserved decision raise a **Decision Request** — Context, Options, Recommendation, Blocked, Proceeding with — and wait. An explicit user instruction counts as approval; record every accepted decision (workflow: `architecture-decision`).
- In an autonomous or headless run, take only a policy-compliant non-Reserved path, never make a Reserved decision silently, and list unresolved Decision Requests in the final report.

## Git

- Do not commit, push, merge, rebase, reset, force-push, delete branches or run any other repository-changing Git operation unless explicitly requested.
- Parallel implementation work must use separate branches or worktrees; keep unrelated changes out of the current branch.

## Workflow routing

Run the matching workflow; it owns the procedure, stop conditions and output, and reads the owners it needs.

| When | Run |
|---|---|
| Planning or implementing a new application, feature, bug fix, refactor or other non-trivial change | `development-workflow` |
| Before declaring any implementation work complete | `verify` |
| Reviewing completed changes, a diff or a PR | `code-review` (agent `code-reviewer`) |
| Repairing a failing build or failing tests | `build-fix` |
| Creating a solution or changing projects or repository structure | `project-structure` |
| Adding, updating or removing a NuGet or npm package | `add-dependency` |
| A `CUSTOM_SETTINGS.md` value is added, changed or removed | `custom-settings` |
| A Reserved decision, or recording or changing an accepted decision | `architecture-decision` |
| Any Git operation | `git-workflow` |
| Security audit or materially security-sensitive change | `security-scan` |
| CI/CD pipeline, container or deployment/migration step | `delivery-pipeline` |
| Changing this instruction system | ask the user to run `/template-maintenance` (never model-invoked) |
