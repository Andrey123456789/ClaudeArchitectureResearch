---
name: git-workflow
description: Use when the user asks to perform or prepare Git operations — create or switch branches or worktrees, stage, commit, push, prepare a PR, merge, rebase, or inspect history. Safe, minimal, state-aware procedure.
---

> Level: 0-core · Owns: Git operation procedure — state inspection, minimal operations, protection of user work, focused staging · Loading: on invocation

# Git Workflow

Whether a repository-changing operation may happen at all is governed by `CLAUDE.md` § Git (explicit request only; parallel work on separate branches/worktrees).

## Safety

- Never discard, overwrite, reset, clean, stash away, or otherwise destroy user work to make a Git operation easier.
- Before any repository-changing operation, inspect the relevant state (`git status`, `git diff`, `git diff --cached`, current branch, upstream) and use the minimum operation that achieves the request; never silently clean unrelated working-tree changes.
- High-risk operations — `git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion, rebasing shared history — run only when explicitly requested or required by an approved workflow, and only after inspecting what will be lost or rewritten. Treat `main`, `master`, and other protected or shared branches as non-rewritable.

## Scope and commits

- Before committing, inspect the staged diff and include only the requested logical change; never stage unrelated modified files merely because they are modified.
- Prefer one logical change per commit; implementation and the tests protecting it normally belong together. No artificial micro-commits, no unrelated fixes bundled together.
- Follow the repository's commit-message convention; otherwise Conventional Commits are a useful default (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`). Use the body for motivation, constraints, or migration notes; do not narrate the obvious diff.

## Branches and worktrees

- Follow an existing branch-naming convention; otherwise prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, `chore/` are reasonable. Do not rename an existing user branch to fit.
- One branch is never checked out in several normal worktrees at once; keep each worktree focused on its branch.
- Before removing a worktree, confirm its changes are committed or otherwise preserved; never remove a worktree holding uncommitted user work.

## Push, merge, rebase

- Before pushing: confirm the intended branch, understand the working/staged state, ensure relevant verification completed, and avoid pushing unrelated local commits.
- Choose merge or rebase by repository convention or the user's request, not preference. Inspect uncommitted work first; never stash, reset, or discard automatically to let the operation proceed.
- Resolve conflicts by the intended combined behavior, not by mechanically taking "ours" or "theirs"; run relevant verification afterwards.

## Pull requests

Run `verify` before preparing a PR. Keep the PR focused; describe what changed, why, how it was verified, and compatibility or migration notes. Never claim checks that were not run.

## Report

When useful, report the resulting state: branch, commit created, push target, PR status, and uncommitted changes that remain.
