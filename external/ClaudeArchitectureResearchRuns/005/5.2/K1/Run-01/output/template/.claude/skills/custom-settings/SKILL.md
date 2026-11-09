---
name: custom-settings
description: Use when adding, changing, removing, reviewing or applying a value in CUSTOM_SETTINGS.md (maximum lengths, page sizes, retention periods, thresholds) to keep code, validation, persistence, frontend, tests and docs synchronized.
---
Kind: WF | Scope: common | Capability: — | Loading: on invocation (routed from CLAUDE.md; a hook reminds on CUSTOM_SETTINGS.md edits)

# Custom Settings Synchronization

What belongs in `CUSTOM_SETTINGS.md`, approval of new values and conflict handling with `SPECIFICATION.md`: `CLAUDE.md` → Tunable settings. This workflow owns the synchronization procedure.

## Synchronization obligation

When an approved `CUSTOM_SETTINGS.md` value is added, changed or removed, identify and update every affected implementation, validation, configuration, test, documentation and mirrored frontend/backend surface, search for stale references, and run the normal `verify` workflow. Changing one literal alone does not establish synchronization.

## 1. Classify the value

- Confirm it is an approved project-level tunable limit or default. Framework defaults the project has not intentionally overridden are not settings.
- Check `SPECIFICATION.md` for conflicts first; a conflict stops the work (`CLAUDE.md` → Tunable settings).

## 2. Record the setting

After approval:

1. record the setting in `CUSTOM_SETTINGS.md` with a stable, descriptive name, its value and its purpose;
2. update the owning code, validation and configuration;
3. update the tests;
4. update user or developer documentation when the value is externally relevant.

Avoid duplicating the same literal across many layers when a single source in code or configuration is appropriate.

## 3. Find every affected surface

Search the repository for the old value, the setting name, validators and DTO constraints, Domain and Application checks, persistence mapping constraints, frontend validation and UI hints, tests and test data, documentation and examples, and configuration that mirrors the setting. Separate occurrences that express the setting from unrelated numeric coincidences, and update only affected behavior.

## 4. Database impact

When the setting affects schema constraints, indexes, column lengths or other persistence metadata, follow the persistence workflow facet → Schema-affecting `CUSTOM_SETTINGS.md` change.

## 5. Frontend and backend consistency

When both frontend and backend expose the same constraint, keep the frontend validation and messages synchronized with the backend for user experience; the backend stays authoritative (`.claude/rules/frontend/frontend.md` → Backend communication).

## 6. Verify

1. Search for stale references to the old value.
2. Build the affected backend and frontend projects.
3. Run the relevant tests.
4. Verify persistence changes when applicable.
5. Check `SPECIFICATION.md` for conflicts.
6. Run `verify`.
