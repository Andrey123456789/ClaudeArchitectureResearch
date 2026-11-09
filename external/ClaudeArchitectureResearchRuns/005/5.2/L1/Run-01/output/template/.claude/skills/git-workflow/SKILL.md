---
name: git-workflow
description: >
  Run for any requested Git operation: branches, worktrees, staging, commits,
  push, merge, rebase, pull requests, history, destructive commands.
---
> Level: 0-core | Owns: Git operation procedure — safety, scope, branches, worktrees, commits, integration, PRs | Scope: repo/meta | Loads: on demand (skill)

# Git Workflow

Repository-changing operations happen only when the user requested them
(operating policy); finishing implementation is not a request to commit.

## Safety

- Never discard, overwrite, reset, clean, or otherwise destroy user work to make
  a Git operation easier.
- Before a repository-changing operation, inspect the relevant repository state
  (`git status`, `git diff`, `git diff --cached`) and use the minimum operation
  required. Do not silently clean unrelated working-tree changes.

## Scope

Before committing, inspect the staged diff and include only the intended
logical change. Do not stage unrelated files merely because they are modified,
and do not clean them up silently.

## Branches

Follow an existing branch-naming convention. Without one, prefixes such as
`feature/`, `fix/`, `refactor/`, `test/`, `docs/`, `chore/` with meaningful
names are reasonable. Do not rename an existing user branch to satisfy a
convention.

## Parallel work and worktrees

Use separate branches and worktrees for parallel implementation streams. One
branch is never checked out in multiple normal worktrees; keep each worktree on
its branch's concern. Before removing a worktree, verify that required changes
are committed or safely preserved; never remove a worktree containing
uncommitted user work.

## Commits

Prefer one logical change per commit; implementation and the tests that protect
it belong together. Do not create artificial tiny commits or combine unrelated
fixes. Follow the repository's commit-message convention; without one,
Conventional Commits are a useful default (`feat:`, `fix:`, `refactor:`,
`test:`, `docs:`, `chore:`). Use the body for motivation, constraints, or
migration notes that would otherwise be lost.

## Push

Before pushing: confirm the intended branch, understand the working and staged
state, ensure relevant verification completed, and avoid pushing unrelated
local commits. Never force-push a shared branch unless the user explicitly
requests history rewriting and understands the consequences; treat `main`,
`master`, and other protected or shared branches as non-rewritable.

## Merge and rebase

Follow the repository/team convention or the user's explicit request, not
personal preference. Inspect local uncommitted work first; do not stash, reset,
or discard work automatically to let an operation proceed. Resolve conflicts by
the intended combined behavior, not by mechanically choosing "ours" or
"theirs", and run relevant verification afterwards.

## Pull requests

Run `verify` before preparing a PR. Keep the PR focused; describe what changed,
why, how it was verified, and compatibility or migration notes. Never claim
checks that were not run.

## Destructive operations

`git reset --hard`, `git clean`, `git push --force`,
`git push --force-with-lease`, branch deletion, and rebasing shared history are
high-risk: perform them only when explicitly requested or clearly required by
an approved workflow, after inspecting what will be lost or rewritten.

## Completion

Report the resulting state when useful: branch, commit created, push target,
PR preparation status, and remaining uncommitted changes.
