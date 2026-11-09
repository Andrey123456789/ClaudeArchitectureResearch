---
name: custom-settings
description: >
  Use when adding, changing, removing, reviewing, or applying a setting in
  CUSTOM_SETTINGS.md, to synchronize every affected implementation, test, and
  documentation surface.
---

> Workflow · Owns the synchronization procedure for `CUSTOM_SETTINGS.md` changes · Policy: `CLAUDE.md` § Product Sources

# Custom Settings Synchronization

What may be stored in `CUSTOM_SETTINGS.md`, its relation to `SPECIFICATION.md`,
and the approval requirement for new values are defined in `CLAUDE.md`
§ Product Sources. If the two product files conflict, resolve the conflict
before changing implementation.

## When Adding a New Setting

After the value is approved:

1. record it in `CUSTOM_SETTINGS.md` with a stable, descriptive setting name;
2. update the owning code, validation, and configuration;
3. update tests;
4. update user or developer documentation when the value is externally
   relevant.

Avoid duplicating the same literal across many layers when a normal single
source in code or configuration is appropriate.

## When CUSTOM_SETTINGS.md Changes

When an approved value is added, changed, or removed, identify and update every
affected surface. Search the repository for:

- the old value and the setting name;
- validators and DTO constraints;
- Domain and Application checks;
- database mapping constraints;
- frontend validation and UI hints;
- tests and test data;
- documentation and examples;
- configuration that mirrors the setting.

Decide which occurrences express the setting and which are unrelated numeric
coincidences; update only affected behavior.

## Database Impact

If the setting affects schema constraints, indexes, column lengths, or other
persistence metadata, run the `persistence-change` workflow § Schema-Affecting
Settings.

## Frontend and Backend Consistency

When frontend and backend expose the same product constraint, backend
validation remains authoritative; keep frontend validation and messages
synchronized for user experience (`.claude/rules/frontend.md` § Forms and
Validation).

## Verification

Before completion:

1. search for stale references to the old value;
2. build the affected backend and frontend projects;
3. run the relevant tests;
4. verify persistence changes when applicable;
5. check `SPECIFICATION.md` for conflicts;
6. run the normal `verify` workflow.

Changing one literal alone does not establish synchronization; do not declare
the setting synchronized merely because one constant changed.
