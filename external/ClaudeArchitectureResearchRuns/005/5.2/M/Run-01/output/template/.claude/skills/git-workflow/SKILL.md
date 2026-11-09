---
name: git-workflow
description: >
  Use for any requested Git operation: status or history, branches, worktrees,
  staging, commits, push, merge, rebase, PR preparation, reset, clean,
  force-push.
---

> Workflow skill. Owns: safe Git procedure — protection of user work, state-aware minimal operations, focused staging and commits, branches, worktrees, push, merge/rebase, PR preparation · Scope: repo/meta · Loads: on invocation · Depends on: CLAUDE.md · Enforced by: .claude/hooks/pre-tool.mjs (confirmation for destructive commands)

# Git Workflow

Repository-changing operations happen only when the user requested them, and
parallel work stays isolated (CLAUDE.md, Git). Completing an implementation is
not a request to commit, push, merge, or rebase.

## Safety

- Never discard, overwrite, reset, clean, or otherwise destroy user work to
  make a Git operation easier.
- Before a repository-changing operation, inspect the relevant repository state
  (`git status`, `git diff`, `git diff --cached`) and use the minimum operation
  required. Do not silently clean unrelated working-tree changes.

## Scope

- Before committing, inspect the staged diff and include only the logical
  requested change; do not stage unrelated files merely because they are
  modified, and do not clean them up.

## Branches

Follow the repository's branch-naming convention. Without one, clear prefixes
such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, and `chore/` are
reasonable. Use names that describe the work, and do not rename an existing user
branch merely to satisfy a convention.

## Parallel Work and Worktrees

- Use a separate branch and worktree per parallel implementation stream; one
  branch must not be checked out in several normal worktrees.
- Keep each worktree focused on its branch's concern.
- Before removing a worktree, verify that required changes are committed or
  otherwise safely preserved; do not remove a worktree that contains
  uncommitted user work.

## Commits

- Prefer one logical change per commit; implementation and the tests that
  protect it belong together. Do not create artificial tiny commits or combine
  unrelated fixes or refactors.
- Follow the repository's commit-message convention. Without one, Conventional
  Commits are a useful default (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`,
  `chore:`). Use the body when motivation, constraints, or migration information
  would otherwise be lost; do not narrate obvious diff details.

## Push

Before pushing: confirm the intended branch, confirm the working and staged
state is understood, ensure relevant verification has completed, and avoid
pushing unrelated local commits. Never force-push a shared branch unless the
user explicitly requests history rewriting and the consequences are understood;
treat `main`, `master`, and other protected or shared branches as
non-rewritable.

## Merge and Rebase

Follow the repository or team convention, or the user's explicit request, not
personal preference. Inspect local uncommitted work first, and do not
automatically stash, reset, or discard work to make the operation proceed.
Resolve conflicts from the intended combined behavior, not by mechanically
choosing "ours" or "theirs", and run relevant verification afterwards.

## Pull Requests

Run `verify` before preparing a PR. Keep the PR focused; describe what changed,
why, how it was verified, and important compatibility or migration notes. Do
not claim checks that were not run.

## Destructive Operations

`git reset --hard`, `git clean`, `git push --force`,
`git push --force-with-lease`, branch deletion, discarding working-tree changes,
and rebasing shared history are high-risk. Perform them only when explicitly
requested or clearly required by an approved workflow, and inspect what will be
lost or rewritten first. The pre-tool hook asks for confirmation before these
commands run.

## Completion

Report the resulting state when useful: branch, commit created, push target,
PR preparation status, and uncommitted changes that remain.
