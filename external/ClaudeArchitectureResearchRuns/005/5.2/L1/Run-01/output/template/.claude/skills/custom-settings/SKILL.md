---
name: custom-settings
description: >
  Run when a CUSTOM_SETTINGS.md value is added, changed, removed, or applied:
  synchronize code, validation, persistence, frontend, tests, and docs.
---
> Level: 0-core | Owns: custom-settings synchronization procedure | Scope: common | Loads: on demand (skill; hook reminder on CUSTOM_SETTINGS.md edits)

# Custom Settings Synchronization

What belongs in `CUSTOM_SETTINGS.md`, the approval requirement for new values,
and the specification/settings conflict rule are owned by product governance
(always loaded). This workflow keeps an approved value synchronized.

## Adding a setting (after approval)

1. Record it in `CUSTOM_SETTINGS.md` with a stable, descriptive name, value, and
   purpose.
2. Update the owning code, validation, and configuration.
3. Update tests.
4. Update user or developer documentation when the value is externally
   relevant.

Prefer one source for the value in code or configuration over duplicating the
same literal across many layers.

## Synchronizing a change, addition, or removal

When an approved value is added, changed, or removed, identify and update every
affected surface. Search the repository for the old value, the setting name,
validators and DTO constraints, domain and use-case checks, persistence mapping
constraints, frontend validation and UI hints, tests and test data,
documentation and examples, and configuration that mirrors the setting.
Distinguish occurrences that express the setting from unrelated numeric
coincidences, and update only the affected behavior. Changing one literal alone
does not establish synchronization.

## Persistence impact

When the change affects schema constraints, indexes, column lengths, or other
persistence metadata: update the persistence mapping and create the migration
according to `persistence.workflow` (edit or regenerate only an uncommitted
migration when that matches the project's migration workflow — never alter an
existing migration casually), verify that Development seeding remains valid,
and add or update provider-sensitive persistence or integration tests when
provider behavior matters.

## Frontend and backend consistency

When both sides expose the same constraint, the backend validation stays
authoritative; keep frontend validation and messages synchronized for user
experience.

## Verification

1. Search for stale references to the old value and name.
2. Build the affected backend and frontend projects.
3. Run the relevant tests.
4. Verify persistence changes when applicable.
5. Check `SPECIFICATION.md` for conflicts.
6. Run the normal `verify` workflow.
