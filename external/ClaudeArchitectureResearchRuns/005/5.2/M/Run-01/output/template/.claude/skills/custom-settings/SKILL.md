---
name: custom-settings
description: >
  Use when a CUSTOM_SETTINGS.md value is added, changed, removed, or applied
  (lengths, page sizes, retention, thresholds); propagates it across code,
  persistence, frontend, tests, docs.
---

> Workflow skill. Owns: the settings synchronization procedure — propagation across affected surfaces, schema-affecting settings, verification of synchronization · Scope: common · Loads: on invocation; routed by CLAUDE.md and the product-input hook · Depends on: CLAUDE.md, .claude/rules/

# Custom Settings Synchronization

What `CUSTOM_SETTINGS.md` may contain, its relation to `SPECIFICATION.md`, and
the approval requirement for new values: CLAUDE.md (Product Sources). Resolve a
conflict between the two sources before changing implementation.

## When Adding a New Setting

After the value is approved:

1. record it in `CUSTOM_SETTINGS.md` with a stable descriptive name and its
   purpose;
2. update the owning code, validation, and configuration;
3. update tests;
4. update user or developer documentation when the value is externally
   relevant.

Avoid duplicating the same literal across many layers when a single source in
code or configuration is appropriate.

## When a Setting Changes or Is Removed

An added, changed, or removed approved value must reach every affected
implementation, validation, configuration, test, documentation, and mirrored
frontend/backend surface. Search the repository for:

- the old value and the setting name;
- validators and DTO constraints;
- Domain and Application checks;
- database mapping constraints;
- frontend validation and UI hints;
- tests and test data;
- documentation and examples;
- configuration that mirrors the setting.

Separate occurrences that express the setting from unrelated numeric
coincidences, and update only the affected behavior. Changing one literal alone
does not establish synchronization.

## Database Impact

When a changed setting affects schema constraints, indexes, column lengths, or
other persistence metadata:

- update the EF Core mapping;
- create the appropriate migration according to the project's migration
  workflow (regenerate or edit an uncommitted migration only when that matches
  the normal workflow; do not casually alter existing migrations);
- verify that Development seeding remains valid;
- add or update provider-sensitive persistence or integration tests when
  provider behavior matters.

## Frontend and Backend Consistency

When both sides expose the same constraint, keep frontend validation and
messages synchronized with the backend; the backend stays authoritative
(`angular.md`, Forms).

## Verification

Before completion:

1. search for stale references to the old value;
2. build the affected backend and frontend projects;
3. run the relevant tests;
4. verify persistence changes when applicable;
5. check `SPECIFICATION.md` for conflicts;
6. run the normal `verify` workflow.
