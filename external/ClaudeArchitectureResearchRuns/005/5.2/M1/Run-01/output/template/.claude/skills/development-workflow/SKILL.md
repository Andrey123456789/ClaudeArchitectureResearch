---
name: development-workflow
description: >
  Run for any implementation task (new application, feature, bug fix,
  refactoring) before editing code: inspect, implement, review, verify, and
  change-specific co-change obligations.
---

> **Workflow skill** · Owns: implementation procedure and change-specific co-change obligations · Scope: common · Loading: on demand (routed from `CLAUDE.md` → Procedures)

# Development Workflow

## 1. Establish Scope and Sources

1. For a new application or substantial feature, read `SPECIFICATION.md` before
   planning or implementing; read `CUSTOM_SETTINGS.md` when settings may apply.
2. Inspect the relevant existing code before making non-trivial changes.
3. Classify consequential choices (`CLAUDE.md` → Decision Control). For a
   Reserved choice, run `architecture-decision` and continue only with compliant
   non-Reserved work.
4. Raise material concerns about the request before implementing it
   (`CLAUDE.md` → Challenge Obligation).

## 2. Load the Governing Rules

Path-scoped rules load when matching files are read or edited. In greenfield
work, or before creating files in an area that has none yet, read the governing
rules explicitly:

| Area | Rules to read |
|---|---|
| backend code | `architecture-style.md`, `persistence-technology.md`, `api.md`, `error-handling.md`, `backend-runtime.md`, `performance.md`, `coding-style.md`, `security.md` |
| backend tests | `testing.md`, `test-framework.md` |
| frontend | `frontend.md`, the frontend rule facet, `security.md` |
| manifests | `dependencies.md` |
| repository structure | `repository-structure.md` |

Use the knowledge skills for technique. Capability facets named by role (for
example "the frontend rule facet") are resolved in `docs/capability-selection.md`. Scaffolding or structural change: run
`project-structure`.

## 3. Implement

Apply the rules, keep the change within the requested scope, and run the routed
workflows when their triggers occur: `add-dependency` before any NuGet/npm
change, `custom-settings` when `CUSTOM_SETTINGS.md` changes.

## 4. Change-Specific Obligations

Apply each item whose trigger occurred:

- **Approved behavioral rule** — when a new behavioral rule is approved, update
  the durable source of truth, including `SPECIFICATION.md` when appropriate.
- **Model change affecting seeded entities** — whenever a Domain or persistence
  change affects entities in the development seed graph (new required or
  removed/renamed properties, changed relationships, new required related
  entities, changed enum/status values, new meaningful states, changed
  invariants), update the maintained development seeder in the same change so a
  recreated Development database is valid and representative for this revision.
  Existing development rows need not be patched.
- **Schema migration** — treat generated migrations as source code: review each
  generated migration before committing it, paying particular attention to
  destructive schema changes, unexpected column recreation, data migrations,
  indexes, foreign keys, and delete behavior. The migration mechanism is the
  persistence capability's (`persistence-technology.md` → Mechanisms).
- **Performance-motivated change** — identify the actual bottleneck or cost,
  preserve observable behavior, use the simplest effective optimization, add or
  preserve tests for the affected behavior, and benchmark or profile when the
  optimization is non-obvious or complex.
- **Bug fix** — default: for a meaningful bug with plausible recurrence, add a
  regression test that fails before the fix and passes after it, unless equivalent
  coverage already exists.
- **API version deprecation** — when deprecating an externally consumed API
  version, mark it deprecated in the versioning metadata, document the
  replacement, communicate a realistic migration and removal timeline, and keep
  the old version working for the promised support period; do not remove it
  without considering the published support contract.
- **CI/CD definitions** — keep pipeline definitions in source control, reproduce
  the repository's supported build/test commands, and never hide build or test
  failures. For the frontend, use scripts that actually exist in `package.json`
  and use `npm ci` when a maintained lockfile supports it; do not invent npm
  scripts or reflexively replace lockfile-based installs.
- **Database migration in deployment** — do not apply production database
  migrations automatically from normal application startup by default; make
  production migration an explicit, visible deployment step using approved
  credentials, and never run Development seeding in Production.

## 5. Review

For substantial feature work or a newly implemented application, run the
`code-review` workflow (through the `code-reviewer` agent when an independent
pass is useful) and fix confirmed findings before final verification.

## 6. Verify

Before declaring implementation work complete, run the `verify` workflow
appropriate to the scope and risk of the change, then report its result.
