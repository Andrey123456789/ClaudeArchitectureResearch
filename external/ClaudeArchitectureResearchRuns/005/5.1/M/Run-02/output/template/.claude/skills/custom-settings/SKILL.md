---
name: custom-settings
description: >
  Use when adding, changing, removing, or applying a value in
  CUSTOM_SETTINGS.md. Propagates it to every implementation, validation,
  schema, frontend, test, and documentation surface and checks for stale
  references.
---

> Owner: custom-settings synchronization procedure, including schema-affecting settings | Scope: common | Loads: on demand — workflow (routed by `CLAUDE.md` and the PostToolUse hook on `CUSTOM_SETTINGS.md`) | Enforced: PostToolUse hook reminder, Stop hook reminder

# Custom Settings Synchronization

What belongs in `CUSTOM_SETTINGS.md`, its relation to `SPECIFICATION.md`, and the
approval needed for new values: `CLAUDE.md` § Product Sources. Resolve any
conflict with `SPECIFICATION.md` before changing implementation.

## Propagation Obligation

When an approved `CUSTOM_SETTINGS.md` value is added, changed, or removed,
identify and update every affected implementation, validation, configuration,
test, documentation, and mirrored frontend/backend surface, search for stale
references, and run the normal verification workflow. Changing one literal alone
does not establish synchronization.

## Adding a Setting

After the value is approved:

1. record it in `CUSTOM_SETTINGS.md` with a stable, descriptive setting name;
2. update the owning code, validation, and configuration;
3. update tests;
4. update user or developer documentation when the value is externally
   relevant.

Prefer one normal source in code or configuration over the same literal repeated
across many layers.

## When a Setting Changes

Search the repository for:

- the old value and the setting name;
- validators and DTO constraints;
- Domain and Application checks;
- database mapping constraints;
- frontend validation and UI hints;
- tests and test data;
- documentation and examples;
- configuration that mirrors the setting.

Separate occurrences that express the setting from unrelated numeric
coincidences, and update only affected behavior.

## Database Impact

When a change affects schema constraints, indexes, column lengths, or other
persistence metadata, read `.claude/rules/persistence.md`, then:

- update the EF Core mapping;
- create the appropriate migration according to the project's migration
  workflow — a new migration when the schema change requires one; regenerate or
  edit an uncommitted migration only when that matches the normal workflow; do
  not casually alter existing migrations;
- verify Development seeding remains valid;
- add or update provider-sensitive persistence or integration tests when needed.

## Frontend and Backend Consistency

When frontend and backend expose the same constraint, keep frontend validation
and messages synchronized for user experience; backend validation stays
authoritative (`.claude/rules/angular.md` § Routing and Forms).

## Verification

Before completion:

1. search for stale references to the old value;
2. build the affected backend and frontend projects;
3. run relevant tests;
4. verify persistence changes when applicable;
5. re-check `SPECIFICATION.md` for conflicts;
6. run the `verify` workflow.

## Output

```text
Setting:            <name>  <old> -> <new>
Updated surfaces:   <files grouped by layer>
Schema/migration:   <migration name> / NOT APPLICABLE
Stale references:   none / <list>
Verification:       <verify report>
```
