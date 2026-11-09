---
name: custom-settings
description: >
  Use when a CUSTOM_SETTINGS.md value is added, changed, removed, or applied: synchronize code, validation, persistence, frontend, tests, docs.
---

> Level: 0 Core | Owns: settings-synchronization procedure, schema-affecting settings co-change | Scope: common | Loads: workflow skill (model-invoked; routed from CLAUDE.md and the post-edit hook) | Depends on: CLAUDE.md

# Custom Settings Synchronization

`CUSTOM_SETTINGS.md` ownership, approval, conflict, and exclusion rules are in
CLAUDE.md (Product Governance). This workflow keeps the implementation
synchronized with the approved values.

## 1. Check the Change

1. Confirm the value is approved; a new value that materially changes accepted
   input or observable behavior needs approval first (CLAUDE.md).
2. Confirm it belongs in `CUSTOM_SETTINGS.md` (CLAUDE.md exclusions).
3. Check `SPECIFICATION.md` for a conflict; if one exists, stop and resolve which
   source is corrected.

## 2. Record the Setting

Record it in the `CUSTOM_SETTINGS.md` table with a stable descriptive name,
value, and purpose. Prefer one normal source in code or configuration over
repeating the literal across layers.

## 3. Find Every Affected Surface

When a value is added, changed, or removed, identify and update every affected
implementation, validation, configuration, test, documentation, and mirrored
frontend/backend surface. Search for:

- the old value and the setting name;
- validators and request/DTO constraints;
- Domain and Application checks;
- persistence mapping constraints (lengths, precision, indexes);
- frontend validation and UI hints;
- tests and test data;
- documentation and examples;
- configuration that mirrors the setting.

Separate real occurrences of the setting from unrelated numeric coincidences,
and update only affected behavior. When frontend and backend expose the same
constraint, update both together (validation authority:
→ `1-architecture/frontend-structure.md`).

## 4. Persistence Impact

When the change affects schema constraints, indexes, column lengths, or other
persistence metadata: update the persistence mapping, create the appropriate
migration according to the project's migration workflow, verify that
Development seeding remains valid, and update provider-sensitive persistence or
integration tests when needed. Do not casually alter existing migrations;
regenerate or edit an uncommitted migration only when that matches the
project's normal workflow.

## 5. Verify

1. Search again for stale references to the old value.
2. Build the affected backend and frontend projects and run relevant tests.
3. Verify persistence changes when applicable.
4. Re-check `SPECIFICATION.md` for conflicts.
5. Run `verify`.

Changing one literal does not establish synchronization; do not declare the
setting synchronized until every affected surface is updated and verified.
