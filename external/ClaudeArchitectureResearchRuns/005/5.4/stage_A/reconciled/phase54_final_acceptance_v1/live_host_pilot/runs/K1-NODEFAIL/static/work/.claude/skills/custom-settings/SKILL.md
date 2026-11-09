---
name: custom-settings
description: >
  Synchronize approved tunable product limits and defaults when
  CUSTOM_SETTINGS.md values are added, changed, removed, reviewed, or applied:
  find every affected surface, update persistence when schema-relevant, verify.
  Use for any CUSTOM_SETTINGS.md change.
---

> Kind: WF | Scope: common | Capability: — | Loading: on-demand workflow

# Custom Settings Synchronization

Governing policy: `CLAUDE.md` (Product sources) — what belongs in `CUSTOM_SETTINGS.md`, approval of new values, and specification consistency. This workflow owns propagation.

## 1. Preconditions

- [ ] The value is approved (new values: proposed with a reason and approved first).
- [ ] No conflict with `SPECIFICATION.md`; a conflict stops the workflow until the user decides which source to correct.
- [ ] The value belongs in the file per `CLAUDE.md` (Product sources) and is not merely a framework default the project has not intentionally overridden.

## 2. Record the setting

Record it in `CUSTOM_SETTINGS.md` with a stable descriptive name, its value, and its purpose. Avoid duplicating the same literal across many layers when a single source in code or configuration is appropriate.

## 3. Find every affected surface

When a value is added, changed, or removed, search the repository for the old value, the setting name, validators and DTO constraints, Domain/Application checks, persistence mapping constraints, frontend validation and UI hints, tests and test data, documentation and examples, and configuration that mirrors the setting. Distinguish occurrences that express the setting from unrelated numeric coincidences, and update only affected behavior — but update every affected implementation, validation, configuration, test, documentation, and mirrored frontend/backend surface.

## 4. Persistence impact

When the change affects schema constraints, indexes, column lengths, or other persistence metadata: update the persistence mapping, create the appropriate migration according to the project's migration workflow, verify that Development seeding remains valid, and add or update provider-sensitive persistence or integration tests when provider behavior matters. Do not casually alter existing migrations when the project requires a new one. Run `persistence-change` for the steps and commands.

## 5. Frontend/backend consistency

When both sides expose the same constraint, backend validation stays authoritative; keep frontend validation and messages synchronized for user experience and never rely on them for security or data integrity.

## 6. Verify

Before completion: search for stale references to the old value; build affected backend/frontend projects; run relevant tests; verify persistence changes when applicable; recheck `SPECIFICATION.md` for conflicts; then run `verify`. Changing one literal alone does not establish synchronization.

## Report

List the setting, old → new value, every updated surface, migration created (if any), and the `verify` result.
