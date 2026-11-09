---
name: development-workflow
description: Use for implementation work — a feature, bug fix, refactor, performance change or new application. Reads product inputs, inspects code, classifies decisions, applies co-change obligations, then runs review and verification.
---
<!-- Kind: WF | Scope: common | Owns: implementation procedure, co-change obligations, completion gates | Loads: workflow invocation (routed by CLAUDE.md) -->
# Development Workflow

## 1. Read Product Inputs

- For a new application or substantial feature, **must** read `SPECIFICATION.md` before planning or implementing. Read `CUSTOM_SETTINGS.md` when limits or defaults are involved, and any feature specification supplied with the task.
- Handle gaps and conflicts per CLAUDE.md § Product Inputs; do not introduce product behavior merely because the specification does not forbid it.

## 2. Inspect Before Changing

- Before a non-trivial change, **must** inspect the relevant existing code and apply the applicable standards and knowledge. Standards for a scope load when its files are read; when planning before any matching file is open, read `.claude/rules/<scope>/*.md` explicitly.

## 3. Classify Decisions and Challenge

- Classify each consequential choice per CLAUDE.md § Decisions; Reserved or unclear → `architecture-decision`. Raise concerns per CLAUDE.md § Challenge Before Implementing before building a questionable request.
- Route specialized work: packages → `add-dependency`; projects, references, structure → `project-structure`; `CUSTOM_SETTINGS.md` values → `custom-settings`; pipelines and deployment → `delivery-pipeline`.

## 4. Implement

Implement in small, reviewable steps within the requested scope, following the standards of every touched scope.

### Co-change Obligations

- **Seed data:** whenever a Domain or persistence change affects seeded entities, **must** update the maintained development seeder in the same change — for example new required properties, removed or renamed properties, changed relationships, new required related entities, changed enum/status values, new meaningful states or changed invariants. The goal: recreating the Development database at any revision yields valid, representative seed data; already seeded rows of an existing database need not be patched.
- **Migrations:** **must** treat EF Core migrations as source code and review every generated migration before committing it, paying particular attention to destructive schema changes, unexpected column recreation, data migrations, indexes, foreign keys and delete behavior. When a migration changes entities represented in the seed data, review the seeder in the same change.
- **Bug fixes:** **default:** for a meaningful bug whose recurrence is plausible, add a regression test that reproduces the failure before the fix and passes after it, unless equivalent coverage already exists.
- **Performance-motivated changes:** **must** identify the actual bottleneck or cost, preserve observable behavior, use the simplest effective optimization, add or maintain tests for behavior the optimization affects, and benchmark or profile when the optimization is non-obvious or complex.

## 5. Record Approved Behavior

- When a new behavioral rule is approved, **must** update the durable source of truth — `SPECIFICATION.md` when appropriate; tunable values through `custom-settings`; engineering decisions through `architecture-decision`.

## 6. Review

- For substantial feature work or a newly implemented application, **must** run `code-review` (or delegate to the `code-reviewer` agent) before the final verification, and address its findings.

## 7. Verify

- Before declaring implementation complete, **must** run `verify` at the depth appropriate to the change's scope and risk.

## Stop Conditions

Stop and ask when a Reserved decision lacks approval, product sources conflict, or the correct behavior cannot be determined from the inputs; in autonomous runs continue only with the non-Reserved remainder (CLAUDE.md § Decisions).

## Output

What changed; decisions taken (Decided or Delegated) and approvals obtained; open Decision Requests; review outcome; the `verify` report.
