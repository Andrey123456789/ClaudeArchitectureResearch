---
name: git-workflow
description: Use when the user asks to perform or prepare a Git operation — branches, worktrees, staging, commits, pushes, PRs, merges, rebases, history inspection or rewriting.
---
<!-- Kind: WF | Scope: repo/meta | Owns: procedure for requested Git operations, user-work protection, commit scope | Loads: workflow invocation; command-guard hook -->
# Git Workflow

Whether a repository-changing operation may run at all: CLAUDE.md § Git Safety — it requires an explicit request, and completing an implementation is not one.

## Safety

- **Never** discard, overwrite, reset, clean or otherwise destroy user work to make a Git operation easier.
- Before a repository-changing operation, **must** inspect the relevant repository state and use the minimum operation required; **must not** silently clean up unrelated working-tree changes.

      git status
      git diff
      git diff --cached

- The command-guard hook pauses repository-changing Git commands. Re-run the command with the trailing comment `# git: user-requested` only when the user explicitly requested that operation.

## Scope

- Before committing, **must** inspect the staged diff and include only the intended logical change; **must not** stage or clean unrelated modified files.

## Branches

Follow an existing branch-naming convention. Without one, clear prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, `chore/` are reasonable defaults. Use meaningful names that describe the work; do not rename an existing user branch merely to satisfy the convention.

## Parallel Work and Worktrees

Parallel implementation streams use separate branches and worktrees (CLAUDE.md § Git Safety). One branch is not checked out in several normal worktrees at once; keep each worktree focused on its branch's concern. Before removing a worktree, verify that required changes are committed or otherwise preserved; do not remove a worktree that contains uncommitted user work.

## Commits

Prefer one logical change per commit; implementation and the tests that protect it belong together in that commit. Avoid artificial tiny commits and avoid combining unrelated fixes or refactors.

### Commit Messages

Follow the repository's existing convention. Without one, Conventional Commits are a useful default:

    feat: add order creation
    fix: prevent duplicate task completion
    refactor: simplify repository query
    test: add order API regression coverage
    docs: document deployment workflow
    chore: update build configuration

Use the body when important motivation, constraints or migration information would otherwise be lost; do not narrate obvious diff details.

## Push

Before pushing: confirm the intended branch; confirm the working and staged state is understood; ensure relevant verification has completed; avoid pushing unrelated local commits. Force-pushing a shared branch needs an explicit request for history rewriting with understood consequences; treat `main`, `master` and other protected/shared branches as non-rewritable.

## Merge and Rebase

Follow the repository/team convention or the user's explicit request rather than personal preference. Inspect local uncommitted work first, and do not stash, reset or discard work automatically to make the operation proceed. Resolve conflicts from the intended combined behavior, not by mechanically choosing "ours" or "theirs", then run relevant verification.

## Pull Requests

Run `verify` before preparing a PR. A PR has a focused purpose without accidental unrelated changes; its description explains what changed, why, how it was verified, and important compatibility or migration notes. Do not claim checks that were not run.

## Destructive Operations

Treat as high-risk: `git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion, rebase of shared history. Perform them only when explicitly requested or clearly required by an approved workflow, and inspect what will be lost or rewritten first.

## Completion

Report the resulting state when useful: branch, commit created, push target, PR preparation status, uncommitted changes that remain.
