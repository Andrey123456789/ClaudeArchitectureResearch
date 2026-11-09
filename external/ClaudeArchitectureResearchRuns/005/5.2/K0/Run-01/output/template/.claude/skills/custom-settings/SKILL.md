---
name: custom-settings
description: Use when a CUSTOM_SETTINGS.md value is added, changed, removed, reviewed or applied. Synchronizes implementation, validation, persistence, frontend, tests and documentation with the approved value.
---
<!-- Kind: WF | Scope: common | Owns: custom-settings synchronization procedure and its persistence co-changes | Loads: workflow invocation; post-edit hook reminder -->
# Custom Settings Synchronization

What belongs in `CUSTOM_SETTINGS.md`, what never does, approval of new values and conflicts with `SPECIFICATION.md`: CLAUDE.md § Product Inputs. `CUSTOM_SETTINGS.md` is a product input, not a runtime secret or configuration store.

## Obligation

When an approved value is added, changed or removed, **must** identify and update every affected implementation, validation, configuration, test, documentation and mirrored frontend/backend surface, search for stale references, and run the normal verification workflow. Changing one literal alone does not establish synchronization.

## 1. Confirm Approval and Consistency

- The value is approved, or approval is requested first when it materially changes accepted input or observable behavior.
- `SPECIFICATION.md` does not contradict it; on conflict stop before changing implementation.

## 2. Record the Setting

- Use a stable, descriptive setting name with its value and purpose in the table.
- Typical settings: maximum title/description lengths, page-size defaults and maximums, retention periods, product-level numeric thresholds, other stable tunable limits explicitly approved for the project. Framework defaults the project has not intentionally overridden are not settings.
- Avoid duplicating the same literal across many layers when a single source in code or configuration is appropriate.

## 3. Find Affected Occurrences

Search for: the old value; the setting name; validators and DTO constraints; Domain/Application checks; database mapping constraints; frontend validation and UI hints; tests and test data; documentation and examples; configuration mirroring the setting. Separate occurrences that express the setting from unrelated numeric coincidences, and update only affected behavior. For a new setting also update the owning code/validation/configuration, tests, and user/developer documentation when the value is externally relevant.

## 4. Database Impact

When the change affects schema constraints, indexes, column lengths or other persistence metadata, **must**:

- update the EF Core mapping;
- create the appropriate migration according to the project's migration workflow — regenerate or edit an uncommitted migration only when that matches the normal workflow;
- verify that Development seeding remains valid;
- add or update provider-sensitive persistence or integration tests when needed.

**Must not** casually alter existing migrations when the project requires a new migration.

## 5. Frontend/Backend Consistency

When both sides expose the same constraint, backend validation remains authoritative and frontend validation and messages stay synchronized for user experience (`rules/frontend/angular.md` § Forms and Validation).

## 6. Verify

1. Search for stale references to the old value.
2. Build the affected backend/frontend projects.
3. Run the relevant tests.
4. Verify persistence changes when applicable.
5. Re-check `SPECIFICATION.md` for conflicts.
6. Run `verify`.

## Output

Setting, old → new value, every updated surface, migration created (if any), tests run, remaining conflicts or approvals needed.
