---
name: git-workflow
description: >
  Use when the user asks for a Git operation: branch or worktree, stage,
  commit, push, PR, merge, rebase, stash, reset, clean, branch deletion, or
  history inspection. Safe, state-aware procedure.
---

> Owner: Git operation safety procedure — state inspection, minimal operations, preservation of user work, focused staging and commits | Scope: repo/meta | Loads: on demand — workflow (routed by `CLAUDE.md` § Git and by the PreToolUse hook) | Enforced: PreToolUse hook pauses repository-changing and destructive Git commands once per command

# Git Workflow

When Git operations are allowed at all, and parallel-work isolation:
`CLAUDE.md` § Git.

## Safety

- Never discard, overwrite, reset, clean, or otherwise destroy user work to make
  a Git operation easier.
- Before a repository-changing operation, inspect the relevant state and use the
  minimum operation the task requires; do not silently clean unrelated
  working-tree changes. Typical checks:

```bash
git status
git diff
git diff --cached
```

## Scope

Before committing, inspect the staged diff and include only the intended logical
change; do not stage or clean up unrelated modified files merely because they are
modified.

## Branches

Follow the repository's branch-naming convention when one exists. Without one,
`feature/`, `fix/`, `refactor/`, `test/`, `docs/`, and `chore/` prefixes with a
meaningful description are reasonable. Do not rename an existing user branch to
satisfy a convention.

## Parallel Work and Worktrees

- One branch cannot be checked out in two normal worktrees at once.
- Keep each worktree focused on its branch's concern.
- Before removing a worktree, verify its changes are committed or otherwise
  preserved; never remove a worktree that contains uncommitted user work.

## Commits

Prefer one logical change per commit; implementation and the tests that protect
it normally belong together. Do not create artificial tiny commits or combine
unrelated fixes and refactors.

Follow the repository's commit-message convention. Without one, Conventional
Commits are a useful default:

```text
feat: add order creation
fix: prevent duplicate task completion
refactor: simplify repository query
test: add order API regression coverage
docs: document deployment workflow
chore: update build configuration
```

Use the body for motivation, constraints, or migration notes that would
otherwise be lost; do not narrate obvious diff details.

## Push

Before pushing:

1. confirm the intended branch;
2. confirm the working and staged state is understood;
3. ensure relevant verification has completed;
4. avoid pushing unrelated local commits by accident.

Never force-push a shared branch unless the user explicitly requests history
rewriting and understands the consequences. Treat `main`, `master`, and other
protected or shared branches as non-rewritable.

## Merge and Rebase

Choose merge or rebase from repository or team convention or the user's explicit
request, not personal preference. Inspect local uncommitted work first, and do
not stash, reset, or discard work automatically to make the operation proceed.
Resolve conflicts from the intended combined behavior rather than mechanically
choosing "ours" or "theirs", then run relevant verification.

## Pull Requests

Run the `verify` workflow before preparing a PR. A PR has a focused purpose and no
accidental unrelated changes. A useful description covers what changed, why, how
it was verified, and compatibility or migration notes. Never claim checks that
were not run.

## Destructive Operations

High-risk: `git reset --hard`, `git clean`, `git push --force`,
`git push --force-with-lease`, branch deletion, `git checkout -- <path>` /
`git restore <path>`, `git stash drop` / `clear`, rebasing shared history. Run
them only when explicitly requested or clearly required by an approved workflow,
after inspecting exactly what will be lost or rewritten.

The PreToolUse hook pauses these and other repository-changing commands once per
command and session; re-run the same command only after confirming it was
explicitly requested.

## Completion

Report the resulting state when useful: branch, commit created, push target, PR
preparation status, and uncommitted changes that remain.
