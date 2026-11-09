---
paths:
  - "**/*"
---
> Level: 0-core | Owns: authority of product inputs and approval of product behavior and tunable values | Scope: common | Loads: always (imported by CLAUDE.md)

# Product Governance

`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, optional feature specifications, and
task prompts are product/task inputs, not instruction layers. An input may
request an engineering decision change; it must not silently override
engineering policy — handle the request through decision control.

## Specification

- When `SPECIFICATION.md` is non-empty, it is the authoritative source for
  project-specific functional requirements and observable product behavior. An
  empty `SPECIFICATION.md` in the template is intentional.
- Do not silently weaken, contradict, or materially extend approved behavior.
  Do not invent user-visible behavior, limits, defaults, restrictions, or
  workflows merely because they seem reasonable or are not explicitly forbidden.
- If an omitted detail must be decided to implement the request and materially
  affects observable product behavior, propose the smallest reasonable option
  and ask for approval.
- String semantics are product behavior when observable: case sensitivity,
  collation, culture-sensitive vs. ordinal comparison, normalization or
  canonicalization, automatic trimming, uniqueness, and lookup semantics. When
  approved sources do not define them and the choice materially affects
  equality, uniqueness, lookup, or accepted input, do not choose silently —
  including through database configuration or framework defaults (the selected
  persistence implementation declares its default comparison semantics in the
  capability selection); ask for approval.

## Custom settings

- `CUSTOM_SETTINGS.md` holds approved project-level tunable product limits and
  defaults (maximum lengths, page-size defaults and maximums, retention periods,
  numeric thresholds); `SPECIFICATION.md` owns behavioral intent.
- `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` must not contradict each other. If
  they appear to conflict, stop and ask which source must be corrected instead
  of choosing one.
- Do not silently invent a tunable value that materially changes accepted input
  or observable behavior when the specification, existing approved behavior, or
  `CUSTOM_SETTINGS.md` does not define it: propose the value with its reason,
  ask for approval, record it in `CUSTOM_SETTINGS.md`, then synchronize the
  affected surfaces (`custom-settings`).
- Do not store secrets, environment-specific connection details, package
  versions, HTTP status codes, ports, migration identifiers, or incidental
  implementation constants in `CUSTOM_SETTINGS.md`.
