---
name: git-workflow
description: >
  Use when asked to perform or prepare Git operations: branches, worktrees, commits, pushes, merges, rebases, pull requests.
---

> Level: 3 Project | Owns: Git operation procedure, state inspection, user-change protection, focused staging | Scope: repo/meta | Loads: workflow skill (model-invoked; routed from CLAUDE.md) | Depends on: CLAUDE.md

# Git Workflow

Whether a repository-changing operation may happen at all is decided by
CLAUDE.md (Version-Control Safety): only when explicitly requested.

## Safety

- Never discard, overwrite, reset, clean, stash away, or otherwise destroy user
  work to make a Git operation easier.
- Before a repository-changing operation, inspect the relevant state
  (`git status`, `git diff`, `git diff --cached`, current branch, upstream) and
  use the minimum operation required; do not silently clean unrelated
  working-tree changes.
- High-risk operations — `git reset --hard`, `git clean`, `git push --force`,
  `git push --force-with-lease`, branch deletion, rebasing shared history — run
  only when explicitly requested or required by an approved workflow, after
  inspecting what will be lost or rewritten. `main`, `master`, and other shared
  branches are non-rewritable.

## Commits

- Before committing, inspect the staged diff and include only the requested
  logical change; do not stage unrelated modified files.
- Prefer one logical change per commit; implementation and the tests that
  protect it belong together. Do not create artificial tiny commits or combine
  unrelated fixes.
- Follow the repository's commit-message convention; without one, Conventional
  Commits are a useful default (`feat:`, `fix:`, `refactor:`, `test:`,
  `docs:`, `chore:`). Use the body for motivation, constraints, or migration
  notes.

## Branches and Worktrees

- Follow an existing branch-naming convention; otherwise `feature/`, `fix/`,
  `refactor/`, `test/`, `docs/`, `chore/` prefixes with meaningful names. Do not
  rename an existing user branch to satisfy the convention.
- For parallel streams (isolation rule: CLAUDE.md), one branch is never checked
  out in two normal worktrees, and each worktree stays focused on its branch's
  concern. Before removing a worktree, verify its
  changes are committed or preserved; never remove one with uncommitted user
  work.

## Push, Merge, Rebase

- Before pushing: confirm the branch, understand the working and staged state,
  ensure relevant verification completed, and avoid pushing unrelated local
  commits.
- Choose merge or rebase from the repository convention or the user's request,
  not preference. Inspect local uncommitted work first; resolve conflicts by the
  intended combined behavior, not mechanically by "ours" or "theirs"; run
  relevant verification afterward.

## Pull Requests

Run `verify` before preparing a PR. A PR has one focused purpose; describe what
changed, why, how it was verified, and compatibility or migration notes. Do not
claim checks that were not run.

## Report

Report the resulting state when useful: branch, commit created, push target, PR
status, and remaining uncommitted changes.
