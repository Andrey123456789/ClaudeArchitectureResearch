---
paths:
  - "SPECIFICATION.md"
  - "CUSTOM_SETTINGS.md"
---

> Level: 0 Core · Owns: product-input authority, product ambiguity, string semantics, tunable values · Scope: common · Loads: always (imported by CLAUDE.md)

# Product Governance

## Specification

- When `SPECIFICATION.md` is non-empty, it is the authoritative source for project-specific functional requirements and observable product behavior. An empty `SPECIFICATION.md` in the reusable template is intentional.
- **Must** read `SPECIFICATION.md` before planning or implementing a new application or a substantial feature.
- **Must not** silently weaken, contradict or materially extend approved behavior, and **must not** invent user-visible rules, limits, defaults, restrictions or workflows merely because they seem reasonable or because the specification does not forbid them.
- **Requires approval:** if an omitted product detail must be decided to implement the requested behavior and the decision materially affects observable behavior, propose the smallest reasonable option and ask for approval.
- **Requires approval:** observable string semantics are product behavior. When the approved sources do not define them and the choice materially affects equality, uniqueness, lookup or accepted input, do not silently choose case sensitivity, collation, culture-sensitive versus ordinal comparison, normalization/canonicalization, or automatic trimming — even when the choice would only be expressed through database configuration or framework defaults.
- **Must** update the durable source of truth — including `SPECIFICATION.md` when appropriate — when a new behavioral rule is approved.

## Custom settings

- `CUSTOM_SETTINGS.md` holds approved project-level tunable product limits and defaults (maximum lengths, page-size defaults and maximums, retention periods, numeric thresholds, other stable tunable values). `SPECIFICATION.md` owns behavioral intent; `CUSTOM_SETTINGS.md` owns the approved concrete values.
- **Requires approval:** the two files must not contradict each other. If they appear to conflict, stop and ask which source must be corrected before implementation continues.
- **Requires approval:** do not silently invent a tunable value that materially changes accepted input or observable behavior when the specification, existing approved behavior or `CUSTOM_SETTINGS.md` does not define it. Propose the value with the reason it is needed, ask for approval, record it in `CUSTOM_SETTINGS.md`, then synchronize.
- **Must not** store secrets, environment-specific connection details, package versions, HTTP status codes, ports, migration identifiers or incidental implementation constants in `CUSTOM_SETTINGS.md`.
- **Must**, when an approved value is added, changed or removed, update every affected implementation, validation, configuration, test, documentation and mirrored frontend/backend surface, search for stale references, and run the normal verification workflow. Changing one literal alone does not establish synchronization. Procedure: `custom-settings` workflow.
