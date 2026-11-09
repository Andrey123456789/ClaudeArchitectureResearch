---
paths:
  - "**/*"
---
> Level: 0-core | Owns: normative vocabulary, engineering defaults, challenge duty, Git boundary | Scope: common | Loads: always (imported by CLAUDE.md)

# Operating Policy

## Normative vocabulary

- **must / must not** — a violation is a defect.
- **default** — deviation requires a concrete reason and must be reported.
- **prefer / avoid** — guidance.
- **requires approval** — a Reserved decision (see decision control).

## Engineering defaults

- Default to simple, maintainable solutions over unnecessary abstractions; keep
  architectural complexity proportional to current requirements and avoid
  speculative abstractions.
- Do not introduce frameworks, libraries, infrastructure, or architectural
  patterns without a concrete current need.
- Keep changes focused on the requested scope and preserve existing behavior
  unless the task or the approved specification requires a change.

## Challenge questionable requests

Before implementing a questionable request, identify the concrete concern —
duplication, poor cohesion, trigger or loading problems, context cost, conflict
with architecture or policy, unnecessary complexity — and propose an
alternative. This never authorizes silently rewriting or ignoring the
requirement: implement the request as asked within policy, or stop with a
Decision Request when it needs approval.

## Git boundary

- Do not commit, push, merge, rebase, reset, force-push, delete branches, or
  perform other repository-changing Git operations unless explicitly requested.
  Procedure: `git-workflow`.
- Parallel implementation work must use separate branches or worktrees; keep
  unrelated changes out of the current branch.
