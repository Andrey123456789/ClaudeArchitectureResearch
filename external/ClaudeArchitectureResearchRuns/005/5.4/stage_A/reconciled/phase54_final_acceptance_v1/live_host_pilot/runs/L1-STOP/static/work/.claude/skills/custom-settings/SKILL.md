---
name: custom-settings
description: Use when adding, changing, removing, reviewing, or applying values in CUSTOM_SETTINGS.md (max lengths, page sizes, retention periods, thresholds). Keeps every affected implementation, validation, configuration, test, documentation, and frontend/backend surface synchronized.
---

> Level: 0-core · Owns: custom-settings synchronization procedure · Loading: on invocation (also triggered by the product-sources hook)

# Custom Settings Synchronization

Governing policy (what belongs in `CUSTOM_SETTINGS.md`, approval of new values, consistency with `SPECIFICATION.md`): `CLAUDE.md` § Product inputs. If the two product files conflict, stop and resolve which one must change before touching implementation.

## When adding a setting (after approval)

1. Record it in `CUSTOM_SETTINGS.md` under a stable descriptive name with its value and purpose.
2. Update the owning code, validation, and configuration.
3. Update tests.
4. Update user/developer documentation when the value is externally relevant.

Avoid copying the same literal across many layers when one source in code or configuration is appropriate. Framework defaults the project has not intentionally overridden do not belong in the file.

## When a value is added, changed, or removed

Identify and update every affected surface — a single changed literal does not establish synchronization. Search for:

- the old value and the setting name;
- validators and DTO/request constraints;
- domain and use-case checks;
- database mapping constraints;
- frontend validation and UI hints;
- tests and test data;
- documentation and examples;
- configuration that mirrors the setting.

Separate occurrences that express the setting from unrelated numeric coincidences; change only affected behavior.

**Persistence impact** — when the change affects schema constraints, indexes, column lengths, or other persistence metadata, run `persistence.workflow` § B.

**Frontend/backend consistency** — backend validation stays authoritative; keep frontend validation and messages synchronized for user experience only.

## Verification

1. Search for stale references to the old value.
2. Build the affected backend and frontend projects.
3. Run the relevant tests.
4. Verify persistence changes when applicable.
5. Re-check `SPECIFICATION.md` for conflicts.
6. Run `verify`.

Report the setting, old → new value, every surface updated, and the `verify` result.
