---
name: custom-settings
description: >
  Use when adding, changing, removing, or applying a value in CUSTOM_SETTINGS.md:
  synchronizes validation, persistence, frontend, tests, configuration, and docs.
---

> Level: 3 Project · Owns: tunable-setting synchronization procedure (workflow) · Scope: common · Loads: on invocation (routed from CLAUDE.md; reminded by the project hook) · Depends on: CLAUDE.md, .claude/rules/** (owner reads)

# Custom Settings Synchronization

What belongs in `CUSTOM_SETTINGS.md`, what never does, approval of new values, and specification consistency are owned by CLAUDE.md → Product governance. This workflow owns the synchronization procedure.

## 1. Before changing a value

1. Confirm the value is approved and consistent with `SPECIFICATION.md` (CLAUDE.md → Product governance).
2. Use a stable descriptive setting name and record the value and its purpose in the table.

## 2. Find every affected surface

Search the repository for the old value, the setting name, validators and DTO constraints, Domain/Application checks, database mapping constraints, frontend validation and UI hints, tests and test data, documentation and examples, and configuration that mirrors the setting. Separate occurrences that express the setting from unrelated numeric coincidences.

## 3. Update every affected surface

When a value is added, changed, or removed, update every affected implementation, validation, configuration, test, documentation, and mirrored frontend/backend surface — changing one literal alone does not establish synchronization. Avoid duplicating the literal across layers when a normal single source in code or configuration is appropriate. Backend validation stays authoritative; frontend validation and messages are kept in sync for user experience (`1-architecture/frontend-structure.md`).

## 4. Database impact

When the change affects schema constraints, indexes, column lengths, or other persistence metadata:

- update the EF Core mapping;
- create the appropriate new migration according to the project's migration workflow (`development-workflow` → Co-changes); regenerate or edit an uncommitted migration only when that matches the normal workflow, and do not casually alter existing migrations;
- verify Development seeding remains valid (`3-project/data-lifecycle.md`);
- add or update provider-sensitive persistence or integration tests when needed.

## 5. Verify

1. Search for stale references to the old value.
2. Build the affected backend/frontend projects and run the relevant tests.
3. Verify persistence changes when applicable.
4. Re-check `SPECIFICATION.md` for conflicts.
5. Run `verify`.

Do not declare a setting synchronized because one constant changed.
