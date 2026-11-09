---
name: custom-settings
description: >
  Run when a CUSTOM_SETTINGS.md value is added, changed, removed, or applied:
  synchronize code, validation, persistence, tests, docs, and frontend, then
  verify.
---

> **Workflow skill** · Owns: custom-settings synchronization procedure, schema-affecting setting co-changes · Scope: common, backend · Loading: on demand (routed from `CLAUDE.md` → Procedures; reminded by the settings-change hook)

# Custom Settings Synchronization

## Purpose

Keep approved tunable values consistent everywhere they take effect. The authority
of `CUSTOM_SETTINGS.md`, its relationship to `SPECIFICATION.md`, the conflict
stop, the approval of new values, and what must not be stored there are governed
by `CLAUDE.md` → Product Sources. If the two product files conflict, resolve the
inconsistency before changing implementation.

## What Belongs Here

Stable tunable product values explicitly approved for the project, such as
maximum title/description lengths, page-size defaults and maximums, retention
periods, and product-level numeric thresholds. Also keep out framework defaults
that the project has not intentionally overridden.

## When Adding a New Setting

Obtain approval first when `CLAUDE.md` → Product Sources requires it. After
approval:

1. record the setting in `CUSTOM_SETTINGS.md`;
2. use a stable descriptive setting name;
3. update the owning code/validation/configuration;
4. update tests;
5. update user/developer documentation when the value is externally relevant.

Avoid duplicating the same literal across many layers when a normal single source
in code/configuration is appropriate.

## When CUSTOM_SETTINGS.md Changes

When an approved value is added, changed, or removed, identify and update every
affected implementation, validation, configuration, test, documentation, and
mirrored frontend/backend surface. Search the repository for:

- the old value;
- the setting name;
- validators and DTO constraints;
- Domain/Application checks;
- database mapping constraints;
- frontend validation/UI hints;
- tests and test data;
- documentation and examples;
- configuration that mirrors the setting.

Determine which occurrences express the setting and which are unrelated numeric
coincidences. Update only affected behavior.

## Database Impact

If a changed setting affects schema constraints, indexes, column lengths, or other
persistence metadata:

- update the persistence mapping;
- create a new migration through the persistence capability's migration mechanism
  (`persistence-technology.md` → Mechanisms) when the changed setting requires a
  schema change;
- regenerate or edit an uncommitted migration only when that matches the
  project's normal migration workflow, and do not casually alter existing
  migrations when the project requires a new migration;
- verify that Development seeding remains valid;
- add or update provider-sensitive persistence or integration tests when provider
  behavior matters.

## Frontend / Backend Consistency

When both frontend and backend expose the same product constraint, keep frontend
validation and messages synchronized for user experience; the backend remains the
authoritative enforcement (`frontend.md` → Forms and Validation).

## Verification

Before completion:

1. search for stale references to the old value;
2. build affected backend/frontend projects;
3. run relevant tests;
4. verify persistence changes when applicable;
5. check `SPECIFICATION.md` for conflicts;
6. run the normal `verify` workflow.

Changing one literal alone does not establish synchronization; do not declare the
setting synchronized until every affected surface has been checked.
