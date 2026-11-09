---
name: custom-settings
description: Use when a CUSTOM_SETTINGS.md value is added, changed, removed or applied; synchronizes code, validation, persistence, frontend, tests and docs.
---

> Kind: WF | Scope: common | Owner: custom-settings synchronization procedure | Loading: workflow (model- or user-invoked; routed by the post-edit hook)

# Custom Settings Synchronization

Policy for `CUSTOM_SETTINGS.md` — what it owns, what it must not contain, conflicts with `SPECIFICATION.md`, approval of new values — is in CLAUDE.md § Product sources. This workflow keeps every affected surface synchronized once a value is approved.

## 1. Confirm the value

1. If the value is new or changed and not already defined by the specification or existing approved behavior, confirm it was approved (CLAUDE.md § Product sources); otherwise raise a Decision Request first.
2. Check `SPECIFICATION.md` for conflicts (CLAUDE.md § Product sources).
3. Record the setting with a stable descriptive name and its purpose. Do not record framework defaults the project has not intentionally overridden.

## 2. Find every affected surface

Search the repository for the old value, the setting name, validators and DTO constraints, Domain/Application checks, database mapping constraints, frontend validation and UI hints, tests and test data, documentation and examples, and configuration that mirrors the setting. Separate occurrences that express the setting from unrelated numeric coincidences, and change only affected behavior.

## 3. Update the owning surfaces

Update every affected implementation, validation, configuration, test, documentation and mirrored frontend/backend surface. Prefer one normal source in code or configuration over the same literal duplicated across layers. Where frontend and backend expose the same constraint, backend validation stays authoritative and frontend validation and messages follow it for user experience (`rules/frontend/angular.md` § Errors and forms).

## 4. Database impact

When the change affects schema constraints, indexes, column lengths or other persistence metadata:

1. update the EF Core mapping;
2. create the appropriate migration according to the project's migration workflow — regenerate or edit an uncommitted migration only when that matches the normal workflow, and do not casually alter existing migrations;
3. verify that Development seeding remains valid;
4. update provider-sensitive persistence or integration tests when needed.

## 5. Verify

1. Search for stale references to the old value.
2. Build the affected backend and frontend projects.
3. Run the relevant tests.
4. Verify persistence changes when applicable.
5. Re-check `SPECIFICATION.md` for conflicts.
6. Run `verify`.

Changing one literal alone does not establish synchronization; do not declare the setting synchronized until every affected surface is updated and verified.
