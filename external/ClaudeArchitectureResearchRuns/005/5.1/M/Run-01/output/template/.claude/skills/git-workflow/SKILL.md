---
name: git-workflow
description: >
  Use whenever the user asks to perform or prepare a Git operation: create or
  switch branches/worktrees, stage, commit, push, prepare a PR, merge, rebase,
  or inspect history. Safe, state-aware, minimal Git procedure.
---

> Owns: Git operation procedure, staging/commit focus, branch/commit conventions, destructive-operation handling | Scope: repo/meta | Loads: workflow (CLAUDE.md routing)

# Git Workflow

When Git operations are allowed at all, and the prohibition on destroying user
work, are owned by `CLAUDE.md` (Git). This workflow defines how to perform a
requested operation.

## Before Any Repository-Changing Operation

Inspect the relevant repository state first (`git status`, `git diff`,
`git diff --cached`, current branch, worktrees) and use the minimum operation
required. Never silently clean up unrelated working-tree changes.

## Scope and Staging

Before committing, inspect the staged diff and include only the intended logical
change. Do not stage unrelated modified files merely because they are modified.

## Branches

Follow the repository's branch-naming convention. Without one, prefixes such as
`feature/`, `fix/`, `refactor/`, `test/`, `docs/`, `chore/` with meaningful
names are reasonable. Do not rename an existing user branch to fit a convention.

## Parallel Work and Worktrees

Use a separate branch and worktree per parallel implementation stream; one
branch is never checked out in multiple normal worktrees. Before removing a
worktree, verify that its changes are committed or otherwise preserved
(`CLAUDE.md`, Git).

## Commits

Prefer one logical change per commit; implementation and the tests protecting it
belong together. Avoid artificial tiny commits and do not combine unrelated
fixes or refactors. Follow the repository's commit-message convention; without
one, Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`,
`chore:`) are a useful default. Use the body for motivation, constraints, or
migration notes that would otherwise be lost.

## Push

Before pushing: confirm the intended branch, understand the working/staged
state, ensure relevant verification completed, and avoid pushing unrelated local
commits. Force-push a shared branch only on an explicit history-rewriting
request whose consequences the user understands; treat `main`, `master`, and
other protected/shared branches as non-rewritable.

## Merge and Rebase

Follow the repository convention or the user's explicit request, not personal
preference. Inspect local uncommitted work first and keep it intact
(`CLAUDE.md`, Git). Resolve conflicts from the
intended combined behavior, not by mechanically choosing "ours"/"theirs", then
run relevant verification.

## Pull Requests

Run `verify` before preparing a PR. Keep the PR focused. Describe what changed,
why, how it was verified, and compatibility/migration notes. Never claim checks
ran that did not run.

## Destructive Operations

`git reset --hard`, `git clean`, `git push --force`/`--force-with-lease`, branch
deletion, and rebasing shared history are high-risk: perform them only when
explicitly requested or clearly required by an approved workflow, and inspect
what will be lost or rewritten before executing them. The project settings ask
for confirmation on these commands.

## Completion

Report the resulting state when useful: branch, commit created, push target, PR
preparation status, and uncommitted changes that remain.
