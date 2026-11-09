---
name: custom-settings
description: >
  Use when a CUSTOM_SETTINGS.md value is added, changed, removed, applied, or
  reviewed: propagate it to code, validation, persistence, frontend, tests, and
  documentation.
---

> Owns: settings synchronization procedure and its database-impact steps | Scope: common | Loads: workflow (routed from CLAUDE.md; reminded by the file-change hook)

# Custom Settings Synchronization

What belongs in `CUSTOM_SETTINGS.md`, approval of new values, and conflicts with
`SPECIFICATION.md` are governed by CLAUDE.md § Custom Settings. Resolve any
conflict before changing implementation. Framework defaults the project has not
intentionally overridden are not settings. Before editing an affected surface,
read the `.claude/rules/*.md` files whose `paths` match it (for example
`persistence.md` and `architecture.md` for persistence metadata, `angular.md` for
frontend validation).

## Adding a Setting (after approval)

1. Record it in `CUSTOM_SETTINGS.md` with a stable descriptive name, its value,
   and its purpose.
2. Update the owning code, validation, and configuration. Prefer one normal
   source in code or configuration over duplicating the literal across layers.
3. Update tests.
4. Update user or developer documentation when the value is externally
   relevant.

## When a Value Changes or Is Removed

When an approved value is added, changed, or removed, identify and update every
affected implementation, validation, configuration, test, documentation, and
mirrored frontend/backend surface. Changing one literal alone does not
establish synchronization.

Search the repository for:

- the old value and the setting name;
- validators and DTO constraints;
- Domain/Application checks;
- database mapping constraints;
- frontend validation and UI hints;
- tests and test data;
- documentation and examples;
- configuration that mirrors the setting.

Separate occurrences that express the setting from unrelated numeric
coincidences, and update only affected behavior.

## Database Impact

When the change affects schema constraints, indexes, column lengths, or other
persistence metadata:

- update the EF Core mapping;
- create the appropriate migration according to the project's migration
  workflow — regenerate or edit an uncommitted migration only when that matches
  the normal workflow, and do not casually alter existing migrations;
- verify that Development seeding remains valid;
- add or update provider-sensitive persistence or integration tests when
  provider behavior matters.

## Frontend / Backend Consistency

When frontend and backend expose the same constraint, backend validation stays
authoritative; keep frontend validation and messages synchronized for the user
experience (`.claude/rules/angular.md`).

## Verification

1. Search for stale references to the old value.
2. Build affected backend and frontend projects.
3. Run relevant tests.
4. Verify persistence changes when applicable.
5. Check `SPECIFICATION.md` for conflicts.
6. Run the normal `verify` workflow.

Do not declare the setting synchronized merely because one constant changed.
