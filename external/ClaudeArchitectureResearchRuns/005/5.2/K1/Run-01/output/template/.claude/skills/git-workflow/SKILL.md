---
name: git-workflow
description: Use when the user asks to perform or prepare Git operations such as branches, worktrees, staging, commits, pushes, PRs, merges, rebases, history inspection or destructive operations.
---
Kind: WF | Scope: repo/meta | Capability: — | Loading: on invocation (routed from CLAUDE.md)

# Git Workflow

When repository-changing Git operations are allowed at all: `CLAUDE.md` → Git (only when explicitly requested; never merely because implementation is complete).

## Safety

- Never discard, overwrite, reset, clean or otherwise destroy user work to make a Git operation easier.
- Before a repository-changing operation, inspect the relevant repository state (`git status`, `git diff`, `git diff --cached`) and use the minimum operation required. Do not silently clean up unrelated working-tree changes.

## Staging and commits

- Before committing, inspect the staged diff and include only the requested logical change. Do not stage unrelated modified files merely because they are modified.
- Prefer one logical change per commit; implementation and the tests that protect it belong to the same commit. Do not create artificially tiny commits or combine unrelated fixes and refactors.
- Follow the repository's commit-message convention. Without one, Conventional Commits are a useful default (`feat: add order creation`, `fix: prevent duplicate task completion`, `refactor:`, `test:`, `docs:`, `chore:`). Use the body when motivation, constraints or migration information would otherwise be lost; do not narrate obvious diff details.

## Branches and worktrees

- Follow an existing branch-naming convention. Without one, prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/` and `chore/` are reasonable defaults with meaningful names. Do not rename an existing user branch to satisfy a convention.
- Parallel implementation streams get their own branches or worktrees (`CLAUDE.md` → Git). One branch must not be checked out in several normal worktrees at once; keep each worktree focused on its branch's concern.
- Before removing a worktree, verify that required changes are committed or otherwise safely preserved; never remove a worktree that contains uncommitted user work.

## Push

Before pushing: confirm the intended branch, confirm the working and staged state is understood, make sure relevant verification has completed, and avoid pushing unrelated local commits. Never force-push a shared branch unless the user explicitly requests history rewriting and understands the consequences; treat `main`, `master` and other protected or shared branches as non-rewritable.

## Merge and rebase

Follow the repository or team convention or the user's explicit request rather than personal preference. Inspect local uncommitted work first, and do not automatically stash, reset or discard work to make the operation proceed. Resolve conflicts from the intended combined behavior, not by mechanically choosing "ours" or "theirs", and run relevant verification afterwards.

## Pull requests

Run `verify` before preparing a PR. A PR has a focused purpose and no accidental unrelated changes. Its description explains what changed, why, how it was verified, and important compatibility or migration notes. Never claim checks that were not run.

## Destructive operations

`git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion and rebasing shared history are high-risk. Perform them only when explicitly requested or clearly required by an approved workflow, and inspect what will be lost or rewritten first.

## Completion

Report the resulting state when useful: branch, commit created, push target, PR preparation status, and uncommitted changes that remain.
