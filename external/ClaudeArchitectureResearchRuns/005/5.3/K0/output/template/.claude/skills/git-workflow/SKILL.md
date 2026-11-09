---
name: git-workflow
description: Use for any Git operation the user asks for — branches, worktrees, staging, commits, push, merge, rebase, PRs, history or destructive operations.
---

> Kind: WF | Scope: repo/meta | Owner: Git operation procedure — state inspection, user-work protection, focused staging and commits | Loading: workflow (model- or user-invoked)

# Git Workflow

Authorization: repository-changing Git operations happen only when explicitly requested, and parallel work uses separate branches or worktrees (CLAUDE.md § Git). Completing an implementation is not a request to commit, push or merge.

Enforced by: the pre-command hook asks the user to confirm Git commands it classifies as repository-changing, unrecognized subcommands included; read-only commands such as `git status`, `git diff` or `git log` run without a prompt. Git run indirectly by scripts or other programs is not classified.

## Safety

- Never discard, overwrite, reset, clean or otherwise destroy user work to make a Git operation easier.
- Before any repository-changing operation, inspect the relevant repository state and use the minimum operation required; never silently clean unrelated working-tree changes.

```bash
git status
git diff
git diff --cached
```

## Scope

- Before committing, inspect the staged diff and include only the logical change that was requested; do not stage unrelated modified files or clean them up.

## Branches

Follow the repository's branch-naming convention. Without one, prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, `chore/` with meaningful names are reasonable defaults. Do not rename an existing user branch to satisfy a convention.

## Parallel work and worktrees

- Keep each worktree focused on its branch's concern; one branch is not checked out in several normal worktrees at once.
- Before removing a worktree, verify that required changes are committed or otherwise preserved; do not remove a worktree that holds uncommitted user work.

## Commits

- Prefer one logical change per commit; implementation and the tests that protect it belong together. Do not create artificial tiny commits or combine unrelated fixes and refactors.
- Follow the repository's commit-message convention. Without one, Conventional Commits are a useful default:

```text
feat: add order creation
fix: prevent duplicate task completion
refactor: simplify repository query
test: add order API regression coverage
docs: document deployment workflow
chore: update build configuration
```

Use the body when important motivation, constraints or migration information would otherwise be lost; do not narrate obvious diff details.

## Push

1. Confirm the intended branch.
2. Confirm the working and staged state is understood.
3. Ensure relevant verification has completed.
4. Avoid pushing unrelated local commits accidentally.

Never force-push a shared branch unless the user explicitly requests history rewriting and the consequences are understood; treat `main`, `master` and other protected or shared branches as non-rewritable.

## Merge and rebase

Follow the repository/team convention or the user's explicit request rather than personal preference. Inspect local uncommitted work first; do not automatically stash, reset or discard work to make the operation proceed. Resolve conflicts from the intended combined behavior, not by mechanically choosing "ours" or "theirs", and run relevant verification afterwards.

## Pull requests

Run `verify` before preparing a PR. A PR has one focused purpose without accidental unrelated changes. Describe what changed, why, how it was verified and any compatibility or migration notes; never claim checks that were not run.

## Destructive operations

`git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion and rebasing shared history are high-risk: run them only when explicitly requested or required by an approved workflow, and inspect what will be lost or rewritten first.

## Report

After Git operations report the resulting state when useful: branch, commit created, push target, PR preparation status, uncommitted changes that remain.
