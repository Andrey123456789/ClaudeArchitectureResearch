---
name: git-workflow
description: >
  Use when asked to perform or prepare Git operations: branches, worktrees, staging,
  commits, push, pull requests, merge, rebase, history, destructive commands.
---

> Level: 0 Core · Owns: Git operation procedure — state inspection, focused staging and commits, branches, worktrees, push, merge/rebase, PRs (workflow) · Scope: repo/meta · Loads: on invocation · Depends on: CLAUDE.md

# Git Workflow

When repository-changing Git operations are allowed at all, and parallel-work isolation, are owned by CLAUDE.md → Git safety.

## Task start

Run the task-start check (CLAUDE.md → Git safety) with `git status`. Report the identified paths (staged, unstaged, untracked) and the two options; do not stash, reset, clean, or commit them on your own, and commit them only within the scope the user names. The check reads the state before your first change, so files this task changed do not trigger it.

## Safety

- Never discard, overwrite, reset, clean, or otherwise destroy user work to make a Git operation easier.
- Before any repository-changing operation, inspect the relevant repository state (`git status`, `git diff`, `git diff --cached`) and use the minimum operation required. Do not silently clean up unrelated working-tree changes.

## Staging and commits

- Before committing, inspect the staged diff and include only the requested logical change; do not stage unrelated modified files merely because they are modified.
- Prefer one logical change per commit; implementation and the tests that protect it normally belong together. Do not create artificial tiny commits or combine unrelated fixes.
- Follow the repository's commit-message convention; without one, Conventional Commits are a useful default (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`). Use the body for motivation, constraints, or migration notes that would otherwise be lost.

## Branches and worktrees

- Follow an existing branch-naming convention; otherwise prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, `chore/` with meaningful names are reasonable defaults. Do not rename an existing user branch to satisfy a convention.
- Use separate branches and worktrees for parallel implementation streams; one branch is not checked out in several normal worktrees at once; keep each worktree focused on its branch.
- Before removing a worktree, verify its changes are committed or otherwise preserved; never remove a worktree containing uncommitted user work.

## Push

Before pushing: confirm the intended branch, understand the working/staged state, ensure relevant verification completed, and avoid pushing unrelated local commits. Never force-push a shared branch unless the user explicitly requests history rewriting and understands the consequences; treat `main`, `master`, and other protected or shared branches as non-rewritable by default: rewriting one needs an explicit user request naming that branch, which is valid unless another policy forbids it.

## Merge and rebase

Follow the repository/team convention or the user's explicit request rather than personal preference. Inspect local uncommitted work first; do not automatically stash, reset, or discard it. Resolve conflicts from the intended combined behavior, not by mechanically choosing "ours" or "theirs", and run relevant verification afterwards.

## Pull requests

Run `verify` before preparing a PR. A PR has a focused purpose; its description explains what changed, why, how it was verified, and compatibility/migration notes. Never claim checks that were not run.

## Destructive operations

`git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion, and rebasing shared history are high-risk: perform them only under the authority in CLAUDE.md → Git safety; a generic approved workflow is not enough. Immediately before executing one, re-check that authority covers this exact operation and target, inspect what will be lost or rewritten, and confirm that changes you did not make are preserved; otherwise stop and report.

## Report

Report the resulting state when useful: branch, commit created, push target, PR status, remaining uncommitted changes.
