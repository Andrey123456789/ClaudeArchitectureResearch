---
name: git-workflow
description: >
  Run when asked to branch, use worktrees, stage, commit, push, prepare a PR,
  merge, rebase, inspect history, or run a destructive Git operation.
---

> **Workflow skill** · Owns: Git operation procedure, protection of user work, state-aware minimal operations, focused staging and commits · Scope: repo/meta · Loading: on demand (routed from `CLAUDE.md` → Procedures)

# Git Workflow

## Safety

Repository-changing Git operations happen only when explicitly requested
(`CLAUDE.md` → Git); completing implementation is not such a request.

Never discard, overwrite, reset, clean, or otherwise destroy user work to make a
Git operation easier.

Before a repository-changing operation, inspect the relevant repository state.

Typical checks include:

    git status
    git diff
    git diff --cached

Use the minimum Git operation required for the task, and do not silently clean
unrelated working-tree changes.

## Scope

Keep unrelated changes out of the current operation.

Before committing, inspect the staged diff and ensure it contains only the
intended logical change.

Do not stage unrelated files merely because they are modified.

## Branches

Follow an existing repository branch-naming convention when one exists.

For a repository without an established convention, clear prefixes such as:

    feature/
    fix/
    refactor/
    test/
    docs/
    chore/

are reasonable defaults.

Use meaningful names that describe the work.

Do not rename an existing user branch merely to satisfy this convention.

## Parallel Work and Worktrees

Parallel implementation streams use separate branches or worktrees
(`CLAUDE.md` → Git).

One branch must not be checked out simultaneously in multiple normal worktrees.

Keep each worktree focused on its branch's concern.

Before removing a worktree, verify that required changes are committed or
otherwise safely preserved.

Do not remove a worktree containing uncommitted user work.

## Commits

Prefer one logical change per commit.

Implementation and the tests that protect that implementation normally belong
to the same logical commit.

Do not create artificial tiny commits merely to maximize commit count.

Do not combine unrelated fixes or refactors into one commit.

### Commit Messages

Follow the repository's existing commit-message convention.

When no convention exists, Conventional Commits are a useful default:

    feat: add order creation
    fix: prevent duplicate task completion
    refactor: simplify repository query
    test: add order API regression coverage
    docs: document deployment workflow
    chore: update build configuration

Use the body when important motivation, constraints, or migration information
would otherwise be lost.

Do not narrate obvious diff details unnecessarily.

## Push

Before pushing:

1. confirm the intended branch;
2. confirm the working/staged state is understood;
3. ensure relevant verification has completed;
4. avoid pushing unrelated local commits accidentally.

Never force-push a shared branch unless the user explicitly requests history
rewriting and the consequences are understood.

Treat `main`, `master`, and other protected/shared branches as non-rewritable.

## Merge and Rebase

Do not choose merge versus rebase merely from personal preference.

Follow repository/team convention or the user's explicit request.

Before either operation, inspect local uncommitted work.

Do not automatically stash, reset, or discard work to make an operation proceed.

When conflicts occur, resolve them based on the intended combined behavior, not
by mechanically choosing "ours" or "theirs".

Run relevant verification after conflict resolution.

## Pull Requests

Before preparing a PR, use the `verify` skill.

A PR should have a focused purpose and should not contain accidental unrelated
changes.

A useful PR description normally explains:

    what changed
    why it changed
    how it was verified
    important compatibility/migration notes

Do not claim checks were run if they were not run.

## Destructive Operations

Treat these as high-risk:

    git reset --hard
    git clean
    git push --force
    git push --force-with-lease
    branch deletion
    rebase of shared history

Perform them only when explicitly requested or clearly required by an approved
workflow.

Inspect what will be lost or rewritten before executing them.

## Completion

After Git operations, report the actual resulting state when useful:

    branch
    commit created
    push target
    PR preparation status
    uncommitted changes that remain
