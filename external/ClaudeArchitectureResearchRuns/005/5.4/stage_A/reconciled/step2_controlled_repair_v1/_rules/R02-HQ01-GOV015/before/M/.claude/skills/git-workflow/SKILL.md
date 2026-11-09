---
name: git-workflow
description: >
  Use when the user asks for a Git operation: branches, worktrees, staging,
  commits, push, merge, rebase, pull requests, history inspection, or
  destructive operations.
---

> Owns: Git operation procedure, user-work protection, commit scope | Scope: repo/meta | Loads: workflow (routed from CLAUDE.md)

# Git Workflow

Which operations require an explicit request, and branch/worktree isolation for
parallel work: CLAUDE.md § Git. Completing an implementation is not a request to
commit, push, merge, or rewrite history.

## Safety

- Never discard, overwrite, reset, clean, or otherwise destroy user work to make
  a Git operation easier.
- Before a repository-changing operation, inspect the relevant repository state
  (`git status`, `git diff`, `git diff --cached`) and use the minimum operation
  required. Do not silently clean up unrelated working-tree changes.

## Scope

Before committing, inspect the staged diff and include only the intended
logical change. Do not stage unrelated files merely because they are modified,
and keep unrelated changes out of the current operation.

## Branches

Follow the repository's branch-naming convention when one exists. Otherwise,
clear prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, and
`chore/` are reasonable defaults. Use meaningful names that describe the work,
and do not rename an existing user branch merely to satisfy this convention.

## Parallel Work and Worktrees

- One branch must not be checked out simultaneously in multiple normal
  worktrees.
- Keep each worktree focused on its branch's concern.
- Before removing a worktree, verify that required changes are committed or
  otherwise safely preserved; never remove a worktree containing uncommitted
  user work.

## Commits

- Prefer one logical change per commit; implementation and the tests that
  protect it belong in the same logical commit.
- Do not create artificial tiny commits, and do not combine unrelated fixes or
  refactors into one commit.
- Follow the repository's commit-message convention. Without one,
  Conventional Commits are a useful default:

  ```text
  feat: add order creation
  fix: prevent duplicate task completion
  refactor: simplify repository query
  test: add order API regression coverage
  docs: document deployment workflow
  chore: update build configuration
  ```

  Use the body when important motivation, constraints, or migration information
  would otherwise be lost; do not narrate obvious diff details.

## Push

Before pushing:

1. confirm the intended branch;
2. confirm the working and staged state is understood;
3. ensure relevant verification has completed;
4. avoid pushing unrelated local commits accidentally.

Never force-push a shared branch unless the user explicitly requests history
rewriting and the consequences are understood. Treat `main`, `master`, and
other protected or shared branches as non-rewritable.

## Merge and Rebase

Follow repository/team convention or the user's explicit request rather than
personal preference. Before either operation, inspect local uncommitted work,
and do not automatically stash, reset, or discard work to make it proceed.
Resolve conflicts from the intended combined behavior, not by mechanically
choosing "ours" or "theirs", then run relevant verification.

## Pull Requests

Run `verify` before preparing a PR. A PR has a focused purpose without
accidental unrelated changes, and its description explains what changed, why,
how it was verified, and important compatibility or migration notes. Do not
claim checks were run if they were not.

## Destructive Operations

Treat `git reset --hard`, `git clean`, `git push --force`,
`git push --force-with-lease`, branch deletion, and rebase of shared history as
high-risk. Perform them only when explicitly requested or clearly required by an
approved workflow, and inspect what will be lost or rewritten before executing
them.

## Completion

After Git operations, report the resulting state when useful: branch, commit
created, push target, PR preparation status, and uncommitted changes that
remain.
