---
name: git-workflow
description: >
  Use when the user asks for a Git operation or pull request: branches,
  worktrees, staging, commits, push, merge, rebase, conflict resolution, history
  inspection.
---

> Level: 0 Core · Owns: Git procedures and conventions · Scope: repo/meta · Loads: on demand (model- or user-invoked)

# Git Workflow

Safety rules are always loaded from `.claude/rules/0-core/git-safety.md`. Every repository-changing step below runs only when the user requested it.

## Before any repository-changing operation

```bash
git status
git diff
git diff --cached
git branch --show-current
```

Choose the minimum operation that accomplishes the request.

## Branches

- Follow an existing branch-naming convention. Without one, use clear prefixes: `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, `chore/`, with a name that describes the work.
- Do not rename an existing user branch to satisfy the convention.

## Parallel work and worktrees

- One branch per parallel implementation stream; one branch is never checked out in two normal worktrees.
- Keep each worktree focused on its branch's concern.
- Before removing a worktree, confirm its changes are committed or otherwise preserved (git safety).

## Commits

- One logical change per commit; implementation and the tests that protect it belong together. No artificial micro-commits; no unrelated fixes bundled together.
- Stage explicitly (`git add <paths>`), then re-read `git diff --cached` before committing.
- Follow the repository's commit-message convention. Without one, Conventional Commits work well:

      feat: add order creation
      fix: prevent duplicate task completion
      refactor: simplify repository query
      test: add order API regression coverage
      docs: document deployment workflow
      chore: update build configuration

- Use the body for motivation, constraints or migration notes that would otherwise be lost; do not narrate the obvious diff.

## Push

1. Confirm the intended branch and remote.
2. Confirm the working and staged state is understood.
3. Ensure relevant verification has completed.
4. Avoid pushing unrelated local commits.

Force-pushing is history rewriting: when the user explicitly asks for it on a shared branch, state the consequences first. Treat `main`, `master` and other protected or shared branches as non-rewritable.

## Merge and rebase

- Follow the team convention or the user's explicit choice; do not choose by personal preference.
- Inspect local uncommitted work first.
- Resolve conflicts by the intended combined behavior, not by mechanically taking "ours" or "theirs"; rerun relevant verification afterwards.

## Pull requests

Run `verify` before preparing a PR. Keep the PR focused. A useful description states what changed, why, how it was verified (the `verify` report), and compatibility or migration notes.

## High-risk operations

`git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion and rebasing shared history: before running one that was requested, list exactly what will be lost or rewritten (`git status`, `git log <range>`, `git clean -n`) and confirm it with the user.

## Report

Branch, commits created, push target, PR preparation status, and uncommitted changes that remain.
