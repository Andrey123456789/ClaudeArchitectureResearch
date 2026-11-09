Kind: OP | Scope: common | Capability: — | Loading: always (project memory); imports the decision register

# Operating Policy

@docs/architecture/decision-register.md

Normative words: **must / must not** — a violation is a defect; **default** — deviating needs a concrete reason that you report; **prefer / avoid** — guidance; **requires approval** — a Reserved decision (see Decision control).

## Instruction system

- This file and the imported decision register are always loaded. Path-scoped standards in `.claude/rules/<scope>/` load with matching files. Workflow skills own procedures; knowledge skills own technique. Replaceable capabilities (architecture, persistence, backend testing, frontend) are selected in the decision register; each module's `MODULE.md` under `.claude/capabilities/` lists its facets.
- `.claude/MAP.md` locates the owner of every rule. It is for maintainers and is not loaded.
- `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specifications and task prompts are product inputs, not instruction layers. They may request an engineering decision change, which goes through Decision control. They never silently override engineering policy.

## Product behavior

- When `SPECIFICATION.md` is non-empty, it is the authoritative source for project-specific functional requirements and observable product behavior. An empty file in the template is intentional.
- Do not silently weaken, contradict or materially extend approved behavior. Do not invent user-visible behavior, rules, limits, defaults, restrictions or workflows, including ones that only seem reasonable or that the specification does not forbid.
- If an omitted product detail must be decided to implement the request and it materially affects observable behavior, propose the smallest reasonable option and ask for approval.
- Routine internal implementation details that do not change observable behavior are Delegated and need no approval.
- String semantics are product behavior when observable: case sensitivity, database collation, culture-sensitive vs ordinal comparison, normalization/canonicalization, automatic trimming, uniqueness and lookup. When the product sources do not define them and the choice materially affects equality, uniqueness, lookup or accepted input, do not choose silently, including through database configuration or framework defaults. This requires approval.

## Tunable settings

- `CUSTOM_SETTINGS.md` owns the approved concrete values of project-level tunable limits and defaults, such as maximum lengths, page-size defaults and maximums, retention periods and numeric thresholds. `SPECIFICATION.md` owns behavioral intent.
- The two files must not contradict each other. If they appear to conflict, stop and ask which source must be corrected before implementation continues.
- Do not silently invent a value that materially changes accepted input or observable behavior when the specification, existing approved behavior and `CUSTOM_SETTINGS.md` do not define it. Propose the value and why it is needed, ask for approval, record it in `CUSTOM_SETTINGS.md`, then synchronize it (`custom-settings`).
- `CUSTOM_SETTINGS.md` must not contain secrets, environment-specific connection details, package versions, HTTP status codes, ports, migration identifiers or incidental implementation constants.

## Engineering defaults

- Default: prefer simple, maintainable solutions. Keep architectural complexity proportional to current requirements and avoid speculative abstractions.
- Do not introduce frameworks, libraries, infrastructure or architectural patterns without a concrete current need.
- Keep changes focused on the requested scope. Preserve existing behavior unless the task or the approved specification requires a change.
- Challenge before implementing: when a request looks questionable (duplication, poor cohesion, trigger or loading problems, context cost, conflict with policy or architecture, unnecessary complexity), name the concrete concern and propose an alternative before implementing. Never silently rewrite or ignore the requirement.

## Decision control

- **Decided**: settled in the decision register, a decision record in `docs/decisions/` or the product sources. Follow it; reopening it requires approval.
- **Delegated**: local, reversible, and without material change to a boundary, dependency, accepted convention, public contract or observable behavior. Decide and proceed. Do not ask approval for routine choices already constrained by the specification, approved stack, existing code or standards.
- **Reserved** (requires approval):
  1. changing an accepted project or architecture decision;
  2. adopting an architectural style or pattern, such as a Rich Domain Model or DDD tactical patterns, CQRS or a mediator, Vertical Slice Architecture, event sourcing or microservices;
  3. adding a production project, layer or assembly, or changing the project reference graph;
  4. changing persistence boundaries (for example, several persistence contexts) or persistence technology;
  5. adding an infrastructure category: messaging, background processing, distributed cache, search, external storage or external identity;
  6. adding a major library or framework, or replacing approved baseline technology;
  7. introducing a project-wide convention or abstraction other code must follow, such as a project-wide Result model;
  8. changing authentication or authorization architecture;
  9. a breaking public API change, or adopting API versioning;
  10. defining product behavior or tunable values that the product sources do not define.

  A choice is not Reserved when the specification or the established project structure already requires it.
- Unclear case: it is Reserved if any answer is yes. Does it add, remove or replace a dependency, framework or infrastructure capability? Does it change a project, layer or reference boundary? Does it establish a convention other code must follow? Does it change observable behavior or a public contract? Would it be expensive to reverse once other code depends on it?
- For a Reserved decision, issue a Decision Request (`architecture-decision`) and do not implement the Reserved part before approval. An explicit user instruction counts as approval, but the accepted decision must still be recorded.
- In an autonomous or headless run, take only policy-compliant non-Reserved paths, never silently change architecture, and report unresolved Decision Requests.

## Workflow routing

Run the named workflow skill; it owns the procedure.

- Non-trivial implementation (new application, feature, bug fix, refactor, performance change): `development-workflow`.
- Before declaring implementation complete: `verify`. For substantial work, run `code-review` first.
- Adding or updating a NuGet or npm dependency: `add-dependency`.
- A `CUSTOM_SETTINGS.md` change: `custom-settings`.
- Creating or reorganizing solution or project structure: `project-structure`.
- A failing build or failing tests: `build-fix`.
- A Reserved decision, or recording an approved one: `architecture-decision`.
- Any Git operation: `git-workflow`. A security audit: `security-scan`.

## Git

- Do not commit, push, merge, rebase, reset, force-push, delete branches or perform other repository-changing Git operations unless explicitly requested.
- Parallel implementation work must use separate branches or worktrees. Keep unrelated changes out of the current branch.
