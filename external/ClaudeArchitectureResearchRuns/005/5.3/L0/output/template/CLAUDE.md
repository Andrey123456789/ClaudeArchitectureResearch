> Level: 0 Core · Owns: precedence, product governance, decision control, challenge obligation, simplicity and scope, Git safety, work routing · Scope: common · Loads: always · Depends on: none

# Project Instructions

This repository is a reusable application template. Its instructions are organized by stability:
**0 Core → 1 Architecture → 2 Technology → 3 Project**. More volatile levels build on more stable ones.
The adopted architecture and the project stack are imported below. Maintainers: see `.claude/INSTRUCTION_MAP.md`.

@.claude/rules/1-architecture/overview.md
@.claude/rules/3-project/decisions.md

## Precedence

- Engineering policy lives in this instruction system. A more volatile level may refine a more stable level but must not contradict it; report a contradiction instead of choosing a side.
- `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` are product inputs, as are feature specifications and task prompts. They define product behavior and approved values; they are not instruction layers. They may request an engineering decision change, but they never silently override engineering policy.
- An explicit user instruction may approve a Reserved decision; record the accepted decision with `architecture-decision`.

## Vocabulary

**must / must not** — violation is a defect. **default** — deviation needs a concrete reason and must be reported. **prefer / avoid** — guidance. **requires approval** — Reserved decision.

## Product governance

- When `SPECIFICATION.md` is non-empty, it is authoritative for project-specific functional requirements and observable product behavior. An empty file in the template is intentional.
- Do not silently weaken, contradict, or materially extend approved behavior. Do not invent user-visible behavior, limits, defaults, restrictions, or workflows — also not merely because the specification does not forbid them.
- If an omitted detail must be decided and materially affects observable product behavior, propose the smallest reasonable option and ask for approval. Routine internal implementation choices that do not change observable behavior do not require approval (default).
- String semantics are product behavior when observable: case sensitivity, collation, culture vs. ordinal comparison, normalization/canonicalization, trimming, uniqueness, and lookup. When the product sources do not define them and the choice affects equality, uniqueness, lookup, or accepted input, do not choose silently — ask for approval.
- `CUSTOM_SETTINGS.md` holds approved project-level tunable limits and defaults (for example maximum lengths, page-size defaults and maximums, retention periods, numeric thresholds); `SPECIFICATION.md` owns behavioral intent.
- The two files must not contradict each other. If they conflict, stop and resolve which source must be corrected before continuing.
- Do not silently invent a tunable value that materially changes accepted input or observable behavior: propose it with the reason, ask for approval, record it in `CUSTOM_SETTINGS.md`, and synchronize every affected surface (`custom-settings`).
- Never store secrets, environment-specific connection details, package versions, HTTP status codes, ports, migration identifiers, or incidental implementation constants in `CUSTOM_SETTINGS.md`.

## Decision control

Classify every consequential choice:

- **Decided** — settled by this instruction system, the product inputs, or a recorded decision. Follow it; do not reopen it without approval. A choice already required by the specification or by the established project structure is Decided.
- **Delegated** — local, reversible, and changes no boundary, dependency, accepted convention, public contract, or observable behavior. Decide and proceed; do not ask approval for routine decisions already constrained by product sources, the approved stack, existing code, or these rules.
- **Reserved** — requires explicit approval before it is implemented. Reserved includes at least:
  1. changing an accepted project or architecture decision;
  2. adopting a new architectural style or pattern, for example CQRS, a mediator, Vertical Slice Architecture, event sourcing, microservices, a Rich Domain Model or DDD tactical patterns;
  3. adding a production project/layer/assembly or changing the project reference graph;
  4. changing persistence boundaries (including multiple persistence contexts) or persistence technology;
  5. adding an infrastructure category: messaging, background processing, distributed cache, search, external storage, external identity;
  6. adding a major library/framework or replacing an approved baseline technology;
  7. introducing a project-wide convention or abstraction that other code is expected to follow, for example a project-wide Result model;
  8. changing the authentication/authorization architecture;
  9. making a breaking public API change or adopting API versioning;
  10. defining product behavior or tunable values that the product sources do not define (Product governance above).

Unclear case — any **yes** makes it Reserved: (1) Does it add, remove, or replace a dependency, framework, or infrastructure capability? (2) Does it change a project/layer/reference boundary? (3) Does it establish a convention other code is expected to follow? (4) Does it change observable behavior or a public contract? (5) Would it be expensive to reverse once other code depends on it?

For a Reserved decision, present a **Decision Request** with: Context · Options · Recommendation · Blocked · Proceeding with. Then run `architecture-decision`, which records the outcome.

In an autonomous or headless run, take only a policy-compliant non-Reserved path, never make a Reserved decision silently, and list every unresolved Decision Request explicitly in the final report.

## Challenge questionable requests

Before implementing a questionable request, name the concrete concern — duplication, poor cohesion, trigger or loading problems, context cost, conflict with the architecture or policy, unnecessary complexity — and propose an alternative. This never authorizes silently rewriting or ignoring the user's requirement; the user decides.

## Simplicity and scope

- Prefer simple, maintainable solutions; keep architectural complexity proportional to current requirements and avoid speculative abstractions (default).
- Do not introduce frameworks, libraries, infrastructure, or architectural patterns without a concrete current need.
- Keep changes focused on the requested scope and preserve existing behavior unless the task or the approved specification requires a change.

## Git safety

- Do not commit, push, merge, rebase, reset, force-push, delete branches, or perform any other repository-changing Git operation unless explicitly requested.
- Parallel implementation work must use separate branches or worktrees; keep unrelated changes out of the current branch.

## Work routing

Workflows own their procedures. Run the matching workflow instead of improvising one:

| Situation | Run |
|---|---|
| Implementing a feature, bug fix, or refactor — including its completion (code review for substantial work, then verification) | `development-workflow` |
| Creating or restructuring the solution, projects, or repository layout | `project-structure` |
| Before declaring implementation work complete | `verify` |
| Repairing a failing build or failing tests | `build-fix` |
| Reviewing completed changes | `code-review`, or the `code-reviewer` agent for an independent review |
| Adding, updating, or removing any package dependency | `add-dependency` |
| `CUSTOM_SETTINGS.md` is added to, changed, or applied | `custom-settings` |
| A Reserved decision or Decision Request | `architecture-decision` |
| CI/CD, container, or deployment definitions | `delivery-pipeline` |
| Security audit or review of a security-sensitive change | `security-scan` |
| Any Git operation | `git-workflow` |

Path-scoped rules under `.claude/rules/` load when matching files are read. Workflows explicitly read the rule files they depend on.
