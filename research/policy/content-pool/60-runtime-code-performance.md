# Runtime, Code & Performance

> Shared normalized content pool. Research artifact, not a runtime candidate file.
> Each policy ID must map to exactly one runtime normative owner in every experimental candidate.

C# conventions, async/cancellation, time, outbound HTTP, caching and measured optimization.

## RUN-001 — Correctness and clarity before optimization

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/performance.md#General Principle`

Prefer clear correct code first; do not introduce specialized optimizations without a concrete reason and prefer measurement/profiling for non-trivial optimization.

## RUN-002 — Use async I/O without sync-over-async

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/performance.md#Async and Cancellation`

Use async APIs for asynchronous I/O and do not block them with .Result, .Wait(), or similar sync-over-async patterns.

## RUN-003 — Propagate cancellation when meaningful

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/performance.md#Async and Cancellation`, `templates/v2-baseline/.claude/skills/error-handling/SKILL.md#Cancellation`

Propagate CancellationToken through asynchronous operations when cancellation is meaningful; do not add cancellation parameters to purely synchronous code without a use case.

## RUN-004 — Use TimeProvider for testable current-time logic

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/performance.md#Time`

Use TimeProvider for application logic that depends on the current clock and needs deterministic testing; do not mechanically replace explicit/stored timestamps.

## RUN-005 — Use managed outbound HttpClient lifetime

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/performance.md#HTTP`

Do not create/dispose a new HttpClient per request; use IHttpClientFactory or another appropriate long-lived strategy.

## RUN-006 — Database access is efficient by default

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/performance.md#Database Access`

Filter/project in the database when practical, avoid unnecessary round trips/over-fetching/N+1 patterns, and paginate potentially large result sets.

## RUN-007 — Caching requires concrete semantics/need

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/performance.md#Caching`

Caching is not a default architecture requirement; introduce it only for a clear measured/reasoned need and choose implementation according to deployment, consistency and staleness requirements.

## RUN-008 — Advanced optimizations require evidence

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/performance.md#Measured Optimizations`

Compiled queries, ValueTask, pooling, custom serialization, aggressive caching and raw SQL should normally be introduced only for a measured or clearly demonstrated need.

## RUN-009 — Follow existing C# conventions

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/coding-style.md#General Principle`

Follow repository conventions and .editorconfig; use modern C# when it improves clarity, but do not mechanically modernize working code.

## RUN-010 — Changed C# files have clean imports

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/coding-style.md#Using Directives`

For C# files created or modified by the task, remove unused/redundant usings while avoiding unrelated repository-wide cleanup.

## RUN-011 — No unrelated style rewrites

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/coding-style.md#Scope Discipline`

Do not perform style-only rewrites outside the requested change unless explicitly asked.

## RUN-012 — Performance changes preserve behavior

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/performance.md#Performance Changes`

A performance-motivated change identifies the bottleneck, preserves behavior, uses the simplest effective optimization, maintains tests, and benchmarks/profiles non-obvious complex optimizations.
