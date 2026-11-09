---
name: development-workflow
description: Use for any non-trivial implementation task (a new application, feature, bug fix, refactor or performance change) to read product inputs, inspect code, classify decisions, implement, review and verify.
---
Kind: WF | Scope: common | Capability: — | Loading: on invocation (routed from CLAUDE.md)

# Development Workflow

Owns the end-to-end procedure for implementation work. Policy stays with its owners: `CLAUDE.md`, the decision register and `.claude/rules/<scope>/`.

## 1. Read the inputs

- For a new application or a substantial feature, read `SPECIFICATION.md` before planning or implementing.
- Read `CUSTOM_SETTINGS.md` when tunable limits or defaults are involved, plus any feature specification and the task prompt.
- Treat these as product inputs. A request in them to change an engineering decision goes through Decision control (`CLAUDE.md`).

## 2. Inspect before changing

- Inspect the relevant existing code before making a non-trivial change, and apply the applicable standards and skills.
- Standards load only when matching files are read. When you plan work before opening those files, read the relevant owners first: `.claude/rules/common/`, `.claude/rules/backend/`, `.claude/rules/backend-tests/`, `.claude/rules/frontend/`.
- For slot concerns (architecture placement, persistence, backend tests, frontend), use the selected module's facets from the decision register: its knowledge facet for technique and `workflow-facet.md` for procedures.

## 3. Classify decisions and challenge

- Classify each decision as Decided, Delegated or Reserved (`CLAUDE.md` → Decision control). For a Reserved decision, run `architecture-decision` and do not implement that part before approval.
- Apply the challenge obligation (`CLAUDE.md` → Engineering defaults) before implementing a questionable request.
- Material product ambiguity, string semantics or a missing tunable value: propose and ask (`CLAUDE.md` → Product behavior, Tunable settings).

## 4. Implement

- Keep the change within the requested scope.
- Structure changes: `project-structure`. Dependency additions or updates: `add-dependency`. `CUSTOM_SETTINGS.md` changes: `custom-settings`.
- Backend placement: the architecture workflow facet.
- Persistence model change (entity, relationship, mapping, schema): whenever Domain or persistence changes affect seeded entities, update the maintained development seeder in the same change. Schema mechanics and migration review: the persistence workflow facet.
- Performance-motivated change: identify the actual bottleneck or cost, preserve observable behavior, use the simplest effective optimization, add or maintain tests for the affected behavior, and benchmark or profile when the optimization is non-obvious or complex.
- A failing build or failing tests: `build-fix`.

## 5. Review

For substantial feature work or a newly implemented application, run the `code-review` workflow (or the `code-reviewer` agent for an independent pass) before the final verification, and fix the findings that matter.

## 6. Verify

Before declaring the implementation complete, run `verify` at the depth that the scope and risk of the change require.

## Stop conditions

Stop and ask the user when:

- a Reserved decision is pending approval;
- `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` conflict;
- material product behavior is ambiguous;
- verification stays red after bounded `build-fix` attempts.

## Output

Summarize what changed, the verification report from `verify`, any deviation from a default with its reason, and every unresolved Decision Request.
