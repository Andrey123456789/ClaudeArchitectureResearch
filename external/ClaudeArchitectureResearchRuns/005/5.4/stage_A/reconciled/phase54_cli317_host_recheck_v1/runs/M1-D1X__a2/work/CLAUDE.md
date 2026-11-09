> Always-loaded operating policy · Owns product-source authority, core defaults, decision control, the Git boundary, and workflow routing · Human map: `.claude/MAP.md` (not auto-loaded)

# Project Instructions

Reusable template for an ASP.NET Core backend with an optional web frontend.
The decision records imported at the end define the adopted architecture, the
approved stack, and the selected capability implementations.

## Product Sources

`SPECIFICATION.md` is the authoritative source for project-specific functional
requirements and observable product behavior when it is non-empty (an empty
file in the reusable template is intentional).

- Do not silently weaken, contradict, or materially extend approved behavior,
  and do not invent user-visible behavior, rules, restrictions, limits,
  defaults, or workflows merely because they seem reasonable or are not
  explicitly forbidden.
- If an omitted detail must be decided and materially affects observable
  product behavior, propose the smallest reasonable option and ask for
  approval. Routine internal implementation choices that do not change
  observable behavior need no approval.
- Observable string semantics are product behavior: case sensitivity,
  collation, culture vs. ordinal comparison, normalization, trimming,
  uniqueness, and lookup. When the approved sources do not define them and the
  choice materially affects equality, uniqueness, lookup, or accepted input,
  ask for approval instead of choosing silently (persistence default:
  `docs/capability-selection.md`).

`CUSTOM_SETTINGS.md` holds approved project-level tunable product limits and
defaults (maximum lengths, page sizes, retention periods, numeric thresholds);
`SPECIFICATION.md` owns behavioral intent.

- The two files must not contradict each other; if they appear to conflict,
  stop and ask which source must be corrected.
- Do not silently invent a tunable value that materially changes accepted input
  or observable behavior when no product source or approved behavior defines
  it: propose it with its reason, get approval, record it, and synchronize it
  (`custom-settings` workflow).
- Never store secrets, environment-specific connection details, package
  versions, HTTP status codes, ports, migration identifiers, incidental
  implementation constants, or framework defaults the project has not
  intentionally overridden in `CUSTOM_SETTINGS.md`.

Product and task inputs are inputs, not instruction layers: they may request an
engineering decision change but never silently override engineering policy; a
conflicting request becomes a Decision Request.

## Core Defaults

- Prefer simple, maintainable solutions; keep architectural complexity
  proportional to current requirements and avoid speculative abstractions.
- Do not introduce frameworks, libraries, infrastructure, or architectural
  patterns without a concrete current need.
- Keep changes focused on the requested scope and preserve existing behavior
  unless the task or the approved specification requires a change.
- Before implementing a questionable request, identify material concerns —
  duplication, poor cohesion, trigger or loading problems, context cost,
  architecture or policy conflict, unnecessary complexity — and propose an
  alternative. This never authorizes silently rewriting or ignoring the user's
  requirement.

## Decision Control

- **Decided** — settled by these instructions, the imported decision records,
  the approved specification, established project structure, or an accepted
  ADR. Follow it; do not reopen it without approval.
- **Delegated** — local, reversible, and not materially changing a boundary,
  dependency, accepted convention, public contract, or observable behavior.
  Decide it yourself.
- **Reserved** — requires explicit approval. It includes at least:
  1. changing an accepted project or architecture decision, including a
     capability selection;
  2. adopting a new architectural style or pattern — for example CQRS, a
     mediator, Vertical Slice Architecture, event sourcing, microservices, a
     Rich Domain Model or systematic DDD tactical patterns, a project-wide
     Result model;
  3. adding a production project, layer, or assembly, or changing the project
     reference graph;
  4. changing persistence boundaries (including multiple persistence contexts)
     or persistence technology;
  5. adding an infrastructure category: messaging, background processing,
     distributed caching, search, external storage, external identity;
  6. adding a major library or framework, or replacing an approved baseline
     technology;
  7. introducing a project-wide convention or abstraction other code must
     follow;
  8. changing the authentication/authorization architecture;
  9. making a breaking public API change or adopting API versioning;
  10. defining product behavior or tunable values not defined by product
      sources.

For an unclear case, any "yes" makes it Reserved: (1) does it add, remove, or
replace a dependency, framework, or infrastructure capability? (2) does it
change a project, layer, or reference boundary? (3) does it establish a
convention other code is expected to follow? (4) does it change observable
behavior or a public contract? (5) would it be expensive to reverse once other
code depends on it?

Raise a Reserved decision as a Decision Request (Context, Options,
Recommendation, Blocked, Proceeding with) through `architecture-decision`. An
explicit user instruction may count as approval but must be recorded there.

In an autonomous or headless run, implement a Reserved change only when the user
explicitly approved that specific change beforehand, naming the change and its
scope; a broad or vague instruction is not approval, and the approval is
recorded through `architecture-decision`. Never make or approve a new Reserved
decision there: on an unexpected Reserved choice, stop that part of the work,
continue only on a policy-compliant non-Reserved path, and report every
unresolved Decision Request in the final report, with a decision log of what was
implemented under which approval.

## Git

Do not commit, push, merge, rebase, reset, force-push, delete branches, or
perform other repository-changing Git operations unless the user explicitly
requested that operation or pre-approved it with a named operation and scope. A
generic "approved workflow", general task approval, or a workflow step that
mentions committing is not that authority.

An explicit request to rewrite a named branch, including `main`, is valid unless
another policy forbids it.

Task-start check: before a task that will change files or repository state in a
Git working tree, check for pre-existing uncommitted changes (staged, unstaged,
untracked). If any exist, ask and offer only two options: commit the identified
changes within a scope the user authorizes, or suspend the whole task until the
user has cleaned up manually. In a headless or noninteractive run without an
already adequate choice, pause safely: change nothing and report the changes
found. Changes made during the current task are not this condition.

Before a destructive Git operation, re-check the authority for it and that
changes you did not make are preserved; procedure: `git-workflow`.

Parallel implementation work must use separate branches or worktrees; keep
unrelated changes out of the current branch.

## Workflow Routing

| When | Run |
|---|---|
| planning or implementing a new application, feature, bug fix, refactor, or other non-trivial change | `development-workflow` |
| creating a solution or adding, removing, or reorganizing projects | `project-structure` |
| adding, updating, or removing a NuGet or npm dependency | `add-dependency` |
| a possibly Reserved decision, an approval, or a capability-selection change | `architecture-decision` |
| `CUSTOM_SETTINGS.md` changes | `custom-settings` |
| persistence model, mapping, migration, or seed-data changes | `persistence-change` |
| reviewing completed changes, a diff, or a PR | `code-review` (read-only: `code-reviewer` agent) |
| a build failure or failing tests | `build-fix` |
| before declaring implementation work complete | `verify` |
| any Git operation | `git-workflow` |
| a security audit or security-sensitive review | `security-scan` |
| changing the instruction system itself | ask the user to run `/template-maintenance` |

## Planning-Time Decisions

@docs/technology-stack.md
@docs/capability-selection.md
@docs/capabilities/architecture.md
@docs/capabilities/persistence.md
@docs/capabilities/backend-testing.md
@docs/capabilities/frontend.md
