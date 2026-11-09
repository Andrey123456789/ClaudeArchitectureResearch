---
name: git-workflow
description: >
  Safe execution of explicitly requested Git operations: branches, worktrees,
  staging, commits, pushes, merges, rebases, pull requests, history. Use when
  the user asks to perform or prepare a Git operation or inspect history.
---

> Kind: WF | Scope: repo/meta | Capability: — | Loading: on-demand workflow

# Git Workflow

Governing policy: `CLAUDE.md` (Git). This workflow owns how a requested operation is carried out.

Enforced by: the pre-command hook asks the user to confirm Git commands it classifies as repository-changing, unrecognized subcommands included; read-only commands such as `git status`, `git diff` or `git log` run without a prompt. The prompt is not authorization: whether the operation may run at all is still decided by `CLAUDE.md` (Git). Git run indirectly by scripts or other programs is not classified.

## Task start

Run the task-start check (`CLAUDE.md` (Git)) with `git status`. Report the identified paths (staged, unstaged, untracked) and the two options; do not stash, reset, clean, or commit them on your own, and commit them only within the scope the user names. The check reads the state before your first change, so files this task changed do not trigger it.

## Safety

- Never discard, overwrite, reset, clean, stash away, or otherwise destroy user work to make a Git operation easier.
- Before any repository-changing operation, inspect the relevant state (`git status`, `git diff`, `git diff --cached`) and use the minimum operation required; never silently clean unrelated working-tree changes.
- Treat `git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion, and rebasing shared history as high-risk: perform them only under the authority in `CLAUDE.md` (Git); a generic approved workflow is not enough. Immediately before executing one, re-check that authority covers this exact operation and target, inspect what will be lost or rewritten, and confirm that changes you did not make are preserved; otherwise stop and report.

## Scope of a commit

Before committing, inspect the staged diff: it must contain only the intended logical change. Never stage or clean unrelated files merely because they are modified. Prefer one logical change per commit, with implementation and the tests that protect it together; do not create artificial tiny commits or combine unrelated fixes and refactors.

## Branches and worktrees

Follow the repository's branch-naming convention; without one, prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, `chore/` are reasonable defaults. Use meaningful names and do not rename an existing user branch to satisfy a convention. One branch must not be checked out in multiple normal worktrees; keep each worktree focused on its branch's concern; before removing a worktree, verify its changes are committed or otherwise preserved, and never remove a worktree containing uncommitted user work.

## Commit messages

Follow the repository's convention; without one, Conventional Commits are a useful default (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`). Use the body for motivation, constraints, or migration notes that would otherwise be lost; do not narrate obvious diff details.

## Push

Before pushing: confirm the intended branch, confirm the working/staged state is understood, ensure relevant verification has completed, and avoid pushing unrelated local commits. Never force-push a shared branch unless the user explicitly requests history rewriting and understands the consequences; treat `main`, `master`, and other protected or shared branches as non-rewritable by default: rewriting one needs an explicit user request naming that branch, which is valid unless another policy forbids it.

## Merge and rebase

Follow the repository/team convention or the user's explicit request rather than personal preference. Inspect local uncommitted work first, and never automatically stash, reset, or discard it to let an operation proceed. Resolve conflicts from the intended combined behavior, not by mechanically choosing "ours" or "theirs", and run relevant verification afterwards.

## Pull requests

Run `verify` before preparing a PR. A PR has a focused purpose without accidental unrelated changes; its description explains what changed, why, how it was verified, and compatibility/migration notes. Never claim checks that were not run.

## Report

Report the resulting state when useful: branch, commit created, push target, PR preparation status, and uncommitted changes that remain.
