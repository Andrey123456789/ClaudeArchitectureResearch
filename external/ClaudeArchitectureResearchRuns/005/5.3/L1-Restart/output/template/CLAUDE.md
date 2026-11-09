> Level: 0-core · Owns: operating policy — product inputs, engineering defaults, decision control, challenge duty, workflow routing, Git safety · Scope: common · Loading: always (entry point)

# Project Instructions

Reusable instruction template for a .NET web backend with an optional browser frontend. Maintainer map (not loaded): `.claude/INSTRUCTION_MAP.md`.

Always-loaded decisions (adopted architecture, approved stack, capability selection):

@.claude/rules/1-architecture/frame/adopted-style.md
@.claude/rules/3-project/decisions.md
@.claude/rules/3-project/frontend-stack.md

## Product inputs

`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specifications, and task prompts are inputs, not instruction layers. They may request a decision change; they never silently override engineering policy.

- When `SPECIFICATION.md` is non-empty, it is authoritative for project-specific functional requirements and observable product behavior. An empty file in the template is intentional.
- Do not silently weaken, contradict, or materially extend approved behavior, and do not invent user-visible behavior, limits, defaults, restrictions, or workflows because they seem reasonable or were not forbidden.
- If an omitted detail must be decided and it materially affects observable behavior, propose the smallest reasonable option and ask for approval. Routine internal implementation choices that do not change observable behavior do not require approval.
- String semantics are product behavior when observable: case sensitivity, collation, culture vs. ordinal comparison, normalization/canonicalization, trimming, uniqueness, and lookup. When approved sources do not define them, ask for approval before choosing — including choices made implicitly through database or framework defaults.
- `CUSTOM_SETTINGS.md` holds approved project-level tunable limits and defaults (maximum lengths, page sizes, retention periods, numeric thresholds); `SPECIFICATION.md` owns behavioral intent. They must not contradict each other: if they appear to conflict, stop and ask which source must be corrected.
- Do not silently invent a tunable value that materially changes accepted input or observable behavior: propose it with a reason, get approval, record it in `CUSTOM_SETTINGS.md`, then synchronize (`custom-settings`).
- Never store secrets, environment-specific connection details, package versions, HTTP status codes, ports, migration identifiers, or incidental implementation constants in `CUSTOM_SETTINGS.md`.

## Engineering defaults

- Default: prefer simple, maintainable solutions; keep architectural complexity proportional to current requirements; avoid speculative abstractions.
- Do not introduce frameworks, libraries, infrastructure, or architectural patterns without a concrete current need.
- Keep changes focused on the requested scope and preserve existing behavior unless the task or approved specification requires a change.

## Decision control

- **Decided** — settled by the imported decision files, approved product sources, or recorded decisions: follow it; reopening requires approval.
- **Delegated** — local, reversible, and does not materially change a boundary, dependency, accepted convention, public contract, or observable behavior: decide and proceed.
- **Reserved** — requires approval: changing an accepted project/architecture decision; adopting a new architectural style or pattern (Rich Domain Model or DDD tactical patterns, CQRS, mediator-based organization, Vertical Slice Architecture, event sourcing, a project-wide Result model, microservices); adding a production project/layer or changing the project reference graph; changing persistence boundaries (for example several persistence contexts) or persistence technology; adding an infrastructure category (messaging, background processing, distributed cache, search, external storage, external identity); adding a major library/framework or replacing approved baseline technology; introducing a project-wide convention or abstraction; changing authentication/authorization architecture; a breaking public API change or adopting API versioning; defining product behavior or tunable values not defined by product sources; changing a capability selection (also requires an ADR).
- Unclear case: any "yes" makes it Reserved — does it add, remove, or replace a dependency, framework, or infrastructure capability? change a project/layer/reference boundary? establish a convention other code must follow? change observable behavior or a public contract? become expensive to reverse once other code depends on it?
- For a Reserved decision, send a Decision Request (Context, Options, Recommendation, Blocked, Proceeding with) and continue only with non-Reserved work. Do not ask for approval for routine choices already constrained by the specification, approved stack, existing code, or rules.
- An explicit user instruction counts as approval; record the accepted decision with `architecture-decision`. In autonomous/headless runs, take only a policy-compliant non-Reserved path and report unresolved Decision Requests explicitly.

## Challenge before implementing

Before implementing a questionable request, name the concrete concerns — duplication, poor cohesion, trigger or loading problems, context cost, architecture conflict, unnecessary complexity — and propose an alternative. This never authorizes silently rewriting or ignoring the user's requirement.

## Workflow routing

- Any implementation work (feature, bug fix, refactor, performance, CI/CD or deployment change): run `development-workflow`; it owns the steps. Work is not complete until its `verify` step has run.
- Dependency add/update/remove → `add-dependency` · `CUSTOM_SETTINGS.md` change → `custom-settings` · solution/project structure → `project-structure` · accepted Reserved decision → `architecture-decision` · failing build/tests → `build-fix` · review → `code-review` (independent: `code-reviewer` agent) · security audit → `security-scan` · Git operations → `git-workflow`.
- Rules in `.claude/rules/` load with matching paths. A `<slot>.<facet>` reference resolves through the capability selection in the decisions file.

## Git

- Do not commit, push, merge, rebase, reset, force-push, delete branches, or perform other repository-changing Git operations unless explicitly requested.
- Parallel implementation work must use separate branches or worktrees; keep unrelated changes out of the current branch.
