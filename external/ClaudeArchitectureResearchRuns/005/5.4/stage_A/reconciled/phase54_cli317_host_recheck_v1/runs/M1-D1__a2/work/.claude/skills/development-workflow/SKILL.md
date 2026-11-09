---
name: development-workflow
description: >
  Use before non-trivial implementation work (new application, feature, bug
  fix, refactor): read product sources, inspect code and owning rules,
  implement, review, verify.
---

> Workflow · Owns the implementation procedure: reading product sources, inspecting code and owners, bug-fix regression coverage, performance-motivated changes, and review before verification

# Development Workflow

## 1. Read the Product Sources

Before planning or implementing a new application or substantial feature, read
`SPECIFICATION.md` and `CUSTOM_SETTINGS.md`. Their authority and approval
boundaries are defined in `CLAUDE.md` § Product Sources.

## 2. Inspect Before Changing

Inspect the relevant existing code before making a non-trivial change, and
apply the rules and skills that govern the affected areas.

Path rules load automatically when matching files are read. For greenfield
work, or when the affected files have not been opened yet, read the owning rules
explicitly before writing code:

| Area | Rules to read |
|---|---|
| backend code | `.claude/rules/architecture.md`, `persistence-technology.md`, `coding-style.md`, `composition.md`, `error-handling.md`, `api.md`, `performance.md`, `security.md` |
| backend tests | `.claude/rules/testing.md`, `test-framework.md` |
| frontend code | `.claude/rules/frontend.md`, `frontend-framework.md`, `security.md` |
| manifests | `.claude/rules/dependencies.md` |
| new directories or projects | `.claude/rules/physical-structure.md` |

Use knowledge skills for technique in the area being changed.

## 3. Classify Decisions

Classify each consequential choice as Decided, Delegated, or Reserved
(`CLAUDE.md` § Decision Control). For a Reserved choice, raise a Decision
Request through `architecture-decision` and continue only with work that does
not depend on it. Raise material concerns about a questionable request before
implementing it (`CLAUDE.md` § Core Defaults).

## 4. Implement

Route specialized changes to their workflows:

- dependency additions, updates, or removals → `add-dependency`;
- persistence model, mapping, migration, or seed-data changes →
  `persistence-change`;
- `CUSTOM_SETTINGS.md` changes → `custom-settings`;
- new or reorganized projects, or project-reference changes →
  `project-structure`.

For a meaningful bug with plausible recurrence, add a regression test unless
equivalent coverage already exists; the test reproduces the failure before the
fix and passes after it.

For a performance-motivated change:

1. identify the actual bottleneck or cost;
2. preserve observable behavior;
3. prefer the simplest optimization that addresses the problem;
4. add or preserve tests for the behavior affected by the optimization;
5. benchmark or profile when the optimization is non-obvious or complex.

## 5. Review

For substantial feature work or a newly implemented application, run the
`code-review` workflow (or delegate to the read-only `code-reviewer` agent)
before the final verification, and fix the findings that matter.

## 6. Verify

Run the `verify` workflow before declaring the work complete, and report
unresolved Decision Requests together with the verification result.
