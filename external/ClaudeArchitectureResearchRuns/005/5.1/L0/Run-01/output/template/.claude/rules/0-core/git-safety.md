---
paths:
  - ".gitignore"
  - ".gitattributes"
---

> Level: 0 Core · Owns: Git safety · Scope: repo/meta · Loads: always (imported by CLAUDE.md)

# Git Safety

- **Must not** commit, push, merge, rebase, reset, force-push, delete branches, rewrite history or perform any other repository-changing Git operation unless explicitly requested. Completing implementation is not such a request.
- **Must** use separate branches or worktrees for parallel implementation work, and keep unrelated changes out of the current branch.
- **Must not** discard, overwrite, reset, clean, automatically stash or otherwise destroy user work to make a Git operation easier.
- **Must** inspect the relevant repository state (status, working-tree diff, staged diff) before a repository-changing operation and use the minimum operation required; never silently clean unrelated working-tree changes.
- **Must** inspect the staged diff before committing and include only the requested logical change; do not stage or clean unrelated modified files.

Procedures for branches, worktrees, commits, pushes, merges, rebases and pull requests: `git-workflow`.
