---
name: custom-settings
description: >
  Use when adding, changing, removing, reviewing, or applying a value in
  CUSTOM_SETTINGS.md. Propagates the approved value to every affected
  implementation, validation, persistence, frontend, test, configuration, and
  documentation surface, then verifies.
---

> Owns: custom-setting synchronization procedure, schema-impact co-changes | Scope: common | Loads: workflow (CLAUDE.md routing; hook reminder on CUSTOM_SETTINGS.md edits)

# Custom Settings Synchronization

What belongs in `CUSTOM_SETTINGS.md`, approval of new values, and conflicts with
`SPECIFICATION.md` are governed by `CLAUDE.md` (Product Sources). This workflow
applies an approved value everywhere it matters.

## 1. Preconditions

- [ ] The value is approved, or already defined by the specification or existing
      approved behavior (otherwise stop and ask — CLAUDE.md, Product Sources).
- [ ] The entry is a tunable product value, not a secret, connection detail,
      package version, status code, port, migration identifier, or incidental
      constant.
- [ ] `SPECIFICATION.md` does not contradict it (on conflict: stop and resolve
      which source must change before touching implementation).

## 2. Record

Record the setting in `CUSTOM_SETTINGS.md` with a stable descriptive name, value,
and purpose. Avoid duplicating the same literal across many layers when a
normal single source in code or configuration is appropriate.

## 3. Find Every Affected Surface

When a value is added, changed, or removed, identify and update every affected
surface. Search the repository for:

- the old value and the setting name;
- validators and DTO constraints;
- Domain/Application checks;
- database mapping constraints;
- frontend validation and UI hints (backend validation stays authoritative;
  frontend mirrors it for user experience);
- tests and test data;
- configuration that mirrors the setting;
- user/developer documentation and examples.

Separate genuine occurrences from unrelated numeric coincidences, and update only
affected behavior.

## 4. Database Impact

If the change affects schema constraints, indexes, column lengths, or other
persistence metadata, read `.claude/rules/persistence.md`, then:

1. update the EF Core mapping;
2. create the appropriate migration according to the project's migration
   workflow (regenerate or edit an uncommitted migration only when that matches
   the normal workflow; do not casually alter existing migrations);
3. review the migration and verify Development seeding remains valid
   (`persistence.md`);
4. add or update provider-sensitive persistence/integration tests when needed.

## 5. Verify

1. Search again for stale references to the old value — changing one literal
   alone does not establish synchronization.
2. Build affected backend/frontend projects and run relevant tests.
3. Verify persistence changes when applicable.
4. Re-check `SPECIFICATION.md` for conflicts.
5. Run the normal `verify` workflow.

Report the setting, old/new value, every surface updated, and verification
results.
