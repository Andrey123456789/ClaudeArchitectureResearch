> Kind: OP | Scope: common | Capability: — | Loading: always (project memory)

# Project Operating Policy

@docs/architecture/decision-register.md

Reusable template for an ASP.NET Core backend with an optional SPA frontend. The imported decision register holds the capability selection, approved stack, project defaults, and accepted decisions. Maintainer map: `.claude/MAP.md` (not loaded).

## Normative vocabulary

**must / must not** — a violation is a defect. **Default** — deviation needs a concrete reason and must be reported. **Prefer / avoid** — guidance. **Requires approval** — a Reserved decision (see Decision control).

## Product sources

- When `SPECIFICATION.md` is non-empty (it is intentionally empty in the template), it is the authoritative source for project-specific functional requirements and observable product behavior.
- Must not silently weaken, contradict, or materially extend specified behavior, and must not silently invent user-visible behavior, limits, defaults, restrictions, or workflows, even when they seem reasonable.
- When an omitted detail must be decided and materially affects observable product behavior, propose the smallest reasonable option and ask for approval.
- Default: routine internal implementation choices that do not change observable behavior need no approval.
- Observable string semantics are product behavior: case sensitivity, collation, culture vs. ordinal comparison, normalization, trimming, uniqueness, and lookup. When the product sources do not define them, choosing them requires approval.
- Approved project-level tunable limits and defaults (maximum lengths, page sizes, retention periods, numeric thresholds) must live in `CUSTOM_SETTINGS.md`; it never overrides `SPECIFICATION.md`, which owns behavioral intent.
- The two files must not contradict each other. If they appear to conflict, stop and ask which source must be corrected; never choose one silently.
- Must not silently invent a tunable value that materially changes accepted input or observable behavior: propose it, obtain approval, record it in `CUSTOM_SETTINGS.md`, then synchronize it (`custom-settings`).
- Must not store in `CUSTOM_SETTINGS.md`: secrets, environment-specific connection details, package versions, HTTP status codes, ports, migration identifiers, or incidental implementation constants.
- Product, feature, and task inputs may request a decision change; they must not silently override engineering policy or recorded decisions.

## Decision control

Classify a choice before acting on it:

- **Decided** — recorded in the decision register or a standard, or already required by the specification or established project structure. Follow it; reopening it requires approval.
- **Delegated** — local and reversible, and does not materially change a boundary, dependency, accepted convention, public contract, or observable behavior. Decide and proceed.
- **Reserved** — requires explicit approval before implementation. At least:
  1. changing an accepted project or architecture decision, including a capability selection;
  2. adopting a new architectural style or pattern, e.g. CQRS, a mediator, Vertical Slice Architecture, event sourcing, microservices, a Rich Domain Model or DDD tactical patterns, a project-wide Result model;
  3. adding a production project, layer, or assembly, or changing the project reference graph;
  4. changing persistence boundaries (e.g. multiple persistence contexts) or persistence technology;
  5. adding an infrastructure category: messaging, background processing, distributed cache, search, external storage, external identity;
  6. adding a major library or framework, or replacing approved baseline technology;
  7. introducing a project-wide convention or abstraction that other code is expected to follow;
  8. changing authentication/authorization architecture;
  9. a breaking public API change or adopting API versioning;
  10. defining product behavior or tunable values that the product sources do not define.
- Unclear case — any "yes" makes it Reserved: (1) Does it add, remove, or replace a dependency, framework, or infrastructure capability? (2) Does it change a project/layer/reference boundary? (3) Does it establish a convention other code is expected to follow? (4) Does it change observable behavior or a public contract? (5) Would it be expensive to reverse after other code depends on it?
- Do not escalate routine local decisions already constrained by the specification, the decision register, existing code, or the standards.
- For a Reserved choice, raise a Decision Request through `architecture-decision` and do not implement it before approval. An explicit user instruction counts as approval; the accepted decision must still be recorded through `architecture-decision`.
- In an autonomous or headless run, take only a policy-compliant non-Reserved path, never silently make or alter a Reserved decision, and report every unresolved Decision Request explicitly.

## Engineering defaults

- Default: the simplest maintainable solution, with architectural complexity proportional to current requirements and no speculative abstractions.
- Must not introduce frameworks, libraries, infrastructure, or architectural patterns without a concrete current need.
- Changes must stay within the requested scope and must preserve existing behavior unless the task or the approved specification requires a change.
- Before implementing a questionable request, name the concrete concern (duplication, poor cohesion, trigger or loading problems, context cost, architecture or policy conflict, unnecessary complexity) and propose an alternative. Never silently rewrite or ignore the user's requirement.

## Git

- Must not commit, push, merge, rebase, reset, force-push, delete branches, or run any other repository-changing Git operation unless explicitly requested; requested operations follow `git-workflow`.
- Parallel implementation work must use separate branches or worktrees; keep unrelated changes out of the current branch.

## Workflows and standards

Each workflow owns its procedure, stop conditions, and report shape. Run it instead of improvising:

| When | Run |
|---|---|
| Implementing a feature, fix, refactor, or new application | `development-workflow` |
| Completing implementation work | `verify` |
| Reviewing a diff or completed work (independent review: `code-reviewer` agent) | `code-review` |
| Repairing a failing build or test | `build-fix` |
| Adding, updating, or removing a NuGet or npm package | `add-dependency` |
| Changing `CUSTOM_SETTINGS.md` | `custom-settings` |
| Changing persistence entities, mappings, migrations, or seed data | `persistence-change` |
| Reserved decision, decision record, or capability selection change | `architecture-decision` |
| Creating or restructuring the solution | `project-structure` |
| CI/CD, container, or deployment change | `delivery-change` |
| Security audit or materially security-sensitive change | `security-scan` |
| Requested Git operation | `git-workflow` |

Path-scoped standards in `.claude/rules/<scope>/` load when matching files are read; knowledge skills load on demand. `template-maintenance` (user-invoked only) governs changes to this instruction system.
