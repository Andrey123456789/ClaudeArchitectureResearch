# Frontend

> Shared normalized content pool. Research artifact, not a runtime candidate file.
> Each policy ID must map to exactly one runtime normative owner in every experimental candidate.

Angular structure, state, HTTP boundary, routing, forms, frontend security and error handling.

## FE-001 — Modern standalone Angular

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/angular/SKILL.md#Core Principles`

Use modern standalone Angular APIs for new code and organize application code primarily by feature.

## FE-002 — Presentation stays focused

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/angular/SKILL.md#Pages and Components`

Keep pages/components focused on presentation and UI orchestration; do not move trivial presentation logic into services merely to shrink components.

## FE-003 — Explicit frontend HTTP boundary

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/angular/SKILL.md#HTTP`

Keep backend communication in explicit feature data-access/services; do not scatter HttpClient calls through presentation components or import backend Domain entities into Angular.

## FE-004 — Signals vs RxJS by semantics

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/angular/SKILL.md#Signals`

Use Signals for naturally synchronous/local UI state and RxJS when asynchronous streams, HTTP composition, cancellation or event pipelines are clearer; avoid mechanical conversions.

## FE-005 — Lazy-load meaningful features

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/angular/SKILL.md#Routing`

Use route-level lazy loading for meaningful features; do not lazy-load every tiny component.

## FE-006 — Prefer simple local state

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/angular/SKILL.md#State Management`

Prefer simple local/component/service state before introducing a state-management library.

## FE-007 — Frontend structure stays feature-oriented

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/angular/SKILL.md#Feature Organization`

Avoid application-wide technical buckets and empty architecture folders; keep feature-specific code within the feature and keep core/shared relatively small.

## FE-008 — Functional interceptors are cross-cutting

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/angular/SKILL.md#HttpClient Configuration`

Prefer functional interceptors for new code and keep interceptor responsibilities cross-cutting; do not put feature business logic in interceptors.

## FE-009 — Frontend understands documented API errors

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/angular/SKILL.md#HTTP Errors`

Frontend code follows the documented API error contract; centralize reusable ProblemDetails parsing when practical and do not infer business behavior from arbitrary human-readable exception messages.

## FE-010 — Frontend validation is UX, backend remains authoritative

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/angular/SKILL.md#Forms`

Use reactive forms for non-trivial forms when useful; frontend validation improves UX but does not replace backend validation or data-integrity/security enforcement.
