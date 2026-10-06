# Workflows & Delivery

> Shared normalized content pool. Research artifact, not a runtime candidate file.
> Each policy ID must map to exactly one runtime normative owner in every experimental candidate.

Review, verification, completion, reporting and workflow behavior.

## WF-001 — Inspect existing code before non-trivial change

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Development Workflow`

Inspect relevant existing code before making non-trivial changes and apply applicable rules/skills.

## WF-002 — Review substantial work before final verification

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Development Workflow`

For substantial feature work or a newly implemented application, run the code-review workflow before final verify.

## WF-003 — Verification required before completion

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/CLAUDE.md#Development Workflow`, `templates/v2-baseline/.claude/skills/verify/SKILL.md`

Before declaring implementation complete, run the verify workflow appropriate to the scope and risk.

## WF-004 — Verification starts with final diff/scope

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/skills/verify/SKILL.md#Inspect the Change`

Review the final changed-file set/diff, confirm scope, remove accidental artifacts/secrets, and determine affected repository areas before choosing checks.

## WF-005 — Build/test affected areas externally

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/skills/verify/SKILL.md#Build`

Build affected projects and run relevant tests; a build failure means implementation is not complete and new relevant failures must be investigated.

## WF-006 — Runtime smoke for substantial composition changes

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/skills/verify/SKILL.md#Runtime Smoke Verification for New Applications`

For new runnable applications or substantial startup/configuration/persistence/full-stack changes, verify intended Development startup and key composition surfaces.

## WF-007 — Architecture/security/dependency checks are risk-scoped

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/skills/verify/SKILL.md#Architecture Check`

Run architecture, formatting/analyzer, dependency and security checks when relevant to the change rather than indiscriminately.

## WF-008 — Fix and retry until green or blocked

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/skills/verify/SKILL.md#Fix-and-Retry`

When verification fails, make the smallest appropriate fix and rerun affected checks until green or genuine user input is required; do not hide known failures.

## WF-009 — Report actual verification state

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/skills/verify/SKILL.md#Reporting`

Report what was actually run using PASS/NOT RUN/NOT APPLICABLE; never imply an unchecked area passed.

## WF-010 — Code reviewer is independent and read-only

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/agents/code-reviewer.md#Role`

The code-reviewer performs an independent read-only review and uses code-review as the canonical procedure rather than redefining policy.

## WF-011 — Review prioritizes defects over style

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/agents/code-reviewer.md#Review Priorities`

Prioritize correctness, security, data integrity, architecture, concurrency/integration, meaningful tests, maintainability and credible performance; do not elevate style preferences above defects.

## WF-012 — Do not manufacture review findings

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/agents/code-reviewer.md#Output`

Do not invent findings to populate categories; when no meaningful findings exist, say so and state important unverifiable areas.
