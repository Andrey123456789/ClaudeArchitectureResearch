---
name: custom-settings
description: >
  Use whenever CUSTOM_SETTINGS.md changes or a new tunable limit or default is
  needed: approval check, recording, propagation to validation, mapping,
  frontend, tests and docs.
---

> Level: 3 Project · Owns: settings-synchronization procedure · Scope: common · Loads: on demand (model- or user-invoked; routed by the post-edit hook)

# Custom Settings

## Read first

- Product governance (always loaded) — what belongs in `CUSTOM_SETTINGS.md`, approval of new values, conflicts with `SPECIFICATION.md`, and the synchronization obligation this procedure fulfils.
- `.claude/rules/3-project/data-lifecycle.md` (Settings-driven schema changes) — when a value affects persistence metadata.

## 1. Check the source of truth

1. Read the changed or proposed setting and the relevant parts of `SPECIFICATION.md`.
2. An apparent conflict between the two is resolved under product governance before any implementation step.
3. A value that is not yet approved goes through approval first (product governance), with the reason it is needed.

## 2. Record the setting

Use a stable, descriptive setting name, the approved value and its purpose in the table. Typical entries: maximum title/description lengths, page-size defaults and maximums, retention periods, product-level numeric thresholds. Framework defaults the project has not intentionally overridden do not belong here.

## 3. Find every affected surface

Search the repository for:

- the old value and the setting name;
- validators and DTO/request constraints;
- Domain and Application checks;
- EF Core mapping constraints (lengths, precision, indexes);
- frontend validation, form hints and messages;
- tests and test data;
- documentation and examples;
- configuration that mirrors the setting.

Separate occurrences that express the setting from unrelated numeric coincidences; update only the affected behavior. Prefer one normal source in code or configuration over duplicating the literal across many layers.

## 4. Persistence impact

When the setting changes schema constraints, indexes, column lengths or other persistence metadata, follow `data-lifecycle.md` (Settings-driven schema changes) and the `ef-core` skill for migration mechanics.

## 5. Frontend and backend consistency

Update the mirrored frontend validation and messages together with the backend constraint (`frontend-structure.md`).

## 6. Verify

1. Search again for stale references to the old value.
2. Build the affected backend and frontend projects.
3. Run relevant tests; verify persistence changes when applicable.
4. Re-check `SPECIFICATION.md` for conflicts.
5. Run the `verify` workflow.

## Report

Setting, old → new value, approval reference, surfaces updated (code, validation, mapping/migration, frontend, tests, docs), stale-reference search result, verification summary.
