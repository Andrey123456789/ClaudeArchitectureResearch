# Governance & Product

> Shared normalized content pool. Research artifact, not a runtime candidate file.
> Each policy ID must map to exactly one runtime normative owner in every experimental candidate.

Operating policy, product authority, approval boundaries, scope discipline, Git safety.

## GOV-001 — Specification is authoritative

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** always
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Product Specification`

When SPECIFICATION.md is non-empty, treat it as the authoritative source for project-specific functional requirements and observable product behavior.

## GOV-002 — Read specification before substantial work

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Product Specification`

Before planning or implementing a new application or substantial feature, read SPECIFICATION.md.

## GOV-003 — Do not invent product behavior

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** always
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Product Specification`

Do not silently weaken, contradict, materially extend, or invent user-visible behavior, limits, defaults, restrictions, or workflows.

## GOV-004 — Material product ambiguity requires approval

- **Origin:** v2
- **Strength:** REQUIRES_APPROVAL
- **Trigger class:** always
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Product Specification`

If an omitted detail must be decided and materially affects observable product behavior, propose the smallest reasonable option and ask for approval.

## GOV-005 — Internal implementation details are delegated

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** always
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Product Specification`

Routine internal implementation choices that do not change observable behavior do not require approval.

## GOV-006 — String semantics are product behavior

- **Origin:** v2
- **Strength:** REQUIRES_APPROVAL
- **Trigger class:** always
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Product Specification`

Case sensitivity, collation, culture/ordinal comparison, normalization, trimming, uniqueness and lookup semantics are product behavior when observable; do not silently choose them when unspecified.

## GOV-007 — Synchronize durable product sources

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Product Specification`

When a new behavioral rule is approved, update the durable source of truth, including SPECIFICATION.md when appropriate.

## GOV-008 — CUSTOM_SETTINGS owns tunable values

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** always
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Custom Settings`, `templates/v2-baseline/CUSTOM_SETTINGS.md`

Use CUSTOM_SETTINGS.md for approved project-level tunable product limits and defaults; SPECIFICATION.md owns behavioral intent.

## GOV-009 — Specification/settings conflict stops work

- **Origin:** v2
- **Strength:** REQUIRES_APPROVAL
- **Trigger class:** always
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Custom Settings`, `templates/v2-baseline/CUSTOM_SETTINGS.md`

SPECIFICATION.md and CUSTOM_SETTINGS.md must not contradict each other; if they conflict, stop and resolve which source must be corrected.

## GOV-010 — Do not invent tunable values

- **Origin:** v2
- **Strength:** REQUIRES_APPROVAL
- **Trigger class:** always
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Custom Settings`

Do not silently invent a tunable value that materially changes accepted input or observable behavior; propose, approve, record and synchronize it.

## GOV-011 — CUSTOM_SETTINGS exclusions

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** always
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Custom Settings`

Do not store secrets, environment-specific connection details, package versions, HTTP status codes, ports, migration identifiers, or incidental implementation constants in CUSTOM_SETTINGS.md.

## GOV-012 — Prefer proportional simplicity

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** always
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Core Defaults`

Prefer simple maintainable solutions; keep architectural complexity proportional to current requirements and avoid speculative abstractions.

## GOV-013 — No speculative frameworks/infrastructure

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** always
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Core Defaults`

Do not introduce frameworks, libraries, infrastructure, or architectural patterns without a concrete current need.

## GOV-014 — Preserve scope and behavior

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** always
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Core Defaults`

Keep changes focused on requested scope and preserve existing behavior unless the task or approved specification requires change.

## GOV-015 — Git mutations require explicit request

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** always
- **Scope:** repo/meta
- **Source:** `templates/v2-baseline/CLAUDE.md#Git`

Do not commit, push, merge, rebase, reset, force-push, delete branches, or perform other repository-changing Git operations unless explicitly requested.

## GOV-016 — Parallel work isolation

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** always
- **Scope:** repo/meta
- **Source:** `templates/v2-baseline/CLAUDE.md#Git`

Parallel implementation work must use separate branches or worktrees; keep unrelated changes out of the current branch.

## GOV-017 — Decision control protocol

- **Origin:** research_shared
- **Strength:** MUST
- **Trigger class:** always
- **Scope:** common
- **Source:** `research/observations/002-candidate-space-analysis.md#S-06`

Classify decisions as Decided, Delegated, or Reserved; Reserved changes require explicit approval and headless runs must not silently alter architecture.

## GOV-018 — Challenge questionable instructions

- **Origin:** research_shared
- **Strength:** MUST
- **Trigger class:** always
- **Scope:** common
- **Source:** `research/observations/002-candidate-space-analysis.md#S-16`

Before implementing a questionable request, identify concrete concerns such as duplication, cohesion, triggering, context, conflicts, or complexity and propose an alternative.
