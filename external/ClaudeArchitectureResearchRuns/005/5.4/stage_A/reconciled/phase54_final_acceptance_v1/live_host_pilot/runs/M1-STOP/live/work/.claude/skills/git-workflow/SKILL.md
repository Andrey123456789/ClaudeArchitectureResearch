---
name: git-workflow
description: >
  Use for any Git operation: branches, worktrees, staging, commits, push,
  merge, rebase, pull requests, or history inspection.
---

> Workflow · Owns the Git operation procedure: state inspection, minimal operations, user-work protection, and focused commits · Boundary: `CLAUDE.md` § Git

# Git Workflow

Enforced by: the pre-command hook asks the user to confirm Git commands it classifies as repository-changing, unrecognized subcommands included; read-only commands such as `git status`, `git diff` or `git log` run without a prompt. The prompt is not authorization: whether the operation may run at all is still decided by `CLAUDE.md` § Git. Git run indirectly by scripts or other programs is not classified.

## Task Start

Run the task-start check (`CLAUDE.md` § Git) with `git status`. Report the
identified paths (staged, unstaged, untracked) and the two options; do not
stash, reset, clean, or commit them on your own, and commit them only within the
scope the user names. The check reads the state before your first change, so
files this task changed do not trigger it.

## Safety

Perform a repository-changing Git operation only under the authority in
`CLAUDE.md` § Git — never merely because implementation is complete.

- Never discard, overwrite, reset, clean, or otherwise destroy user work to make
  a Git operation easier.
- Before a repository-changing operation, inspect the relevant repository
  state, typically:

  ```text
  git status
  git diff
  git diff --cached
  ```

- Use the minimum Git operation required for the task, and do not silently
  clean up unrelated working-tree changes.

## Scope

Before committing, inspect the staged diff and include only the intended
logical change. Do not stage unrelated files merely because they are modified.

## Branches

Follow an existing branch-naming convention when one exists. Otherwise clear
prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, and
`chore/` are reasonable defaults. Use meaningful names, and do not rename an
existing user branch merely to satisfy this convention.

## Parallel Work and Worktrees

Parallel implementation streams use separate branches or worktrees
(`CLAUDE.md` § Git). One branch must not be checked out simultaneously in
multiple normal worktrees. Keep each worktree focused on its branch's concern.
Before removing a worktree, verify that required changes are committed or
otherwise safely preserved; do not remove a worktree that contains uncommitted
user work.

## Commits

Prefer one logical change per commit; implementation and the tests that protect
it belong to the same commit by default. Do not create artificial tiny commits or
combine unrelated fixes or refactors.

Follow the repository's commit-message convention. When none exists,
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

Before pushing: confirm the intended branch, confirm the working and staged
state is understood, ensure relevant verification has completed, and avoid
pushing unrelated local commits. Never force-push a shared branch unless the
user explicitly requests history rewriting and the consequences are understood;
treat `main`, `master`, and other protected or shared branches as
non-rewritable by default: rewriting one needs an explicit user request naming
that branch, which is valid unless another policy forbids it.

## Merge and Rebase

Follow the repository/team convention or the user's explicit request rather
than personal preference. Before either operation, inspect local uncommitted
work; do not automatically stash, reset, or discard work to make the operation
proceed. Resolve conflicts from the intended combined behavior, not by
mechanically choosing "ours" or "theirs", and run relevant verification after
resolution.

## Pull Requests

Before preparing a PR, run `verify`. A PR has a focused purpose without
accidental unrelated changes. A useful description explains what changed, why,
how it was verified, and important compatibility or migration notes. Do not
claim checks were run if they were not.

## Destructive Operations

Treat these as high-risk: `git reset --hard`, `git clean`, `git push --force`,
`git push --force-with-lease`, branch deletion, and rebasing shared history.
Perform them only under the authority in `CLAUDE.md` § Git; a generic approved workflow is not
enough. Immediately before executing one, re-check that authority covers this
exact operation and target, inspect what will be lost or rewritten, and confirm
that changes you did not make are preserved; otherwise stop and report.

## Completion

After Git operations, report the actual resulting state when useful: branch,
commit created, push target, PR preparation status, and uncommitted changes
that remain.
