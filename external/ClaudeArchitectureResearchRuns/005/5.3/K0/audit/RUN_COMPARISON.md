# K0 Run-01 vs Run-02

## Structural variance

Independent tree comparison:

- Run-01 runtime files: 66;
- Run-02 runtime files: 62;
- common runtime paths: 55;
- union runtime paths: 73;
- whole-tree path Jaccard: **0.753**;
- byte-identical common files: 1 (`SPECIFICATION.md`);
- STD rule-path Jaccard: **0.611**;
- skill-name Jaccard: **1.000** (all 29 skill entry points agree).

Rule decomposition differs, but not radically:

Run-01-only rule paths include:

- `common/structure.md`;
- `backend/outbound-http.md`;
- `backend/operations.md`;
- `frontend/security.md`.

Run-02 instead consolidates/reorganizes into:

- `common/repository-layout.md`;
- `backend/integrations.md`;
- `backend/hosting.md`;
- frontend security obligations inside `frontend/angular.md`.

## Architecture agreement

Despite implementation variance, both runs independently agree on the defining K0 architecture:

1. Kind is the primary responsibility classification.
2. Scope is the placement/applicability classification.
3. OP/DEC are always-loaded.
4. STD is path-scoped and organized by Scope.
5. KNW is on-demand technique.
6. WF is procedural.
7. ENF is hooks/scripts/assets.
8. IN remains product input, not engineering policy.
9. One decision register carries decisions plus `Details in` / `Affects`.
10. Technologies are embedded across Kinds rather than hidden behind capability slots.
11. No `Level:` hierarchy exists.
12. No capability contract/module/slot structure exists.

Thus the two runs are different implementations of K0, not competing interpretations of what K0 means.

## Run-01 strengths

Run-01 provides useful evidence for the quality ceiling:

- broader dependency command recognition, including removals;
- repository-changing Git command recognition;
- higher V2 textual/technique preservation;
- BOM-tolerant hook input parsing.

Its largest runtime weakness is more fundamental: every hook is launched with a current-directory-relative path (`node .claude/hooks/...`). After Claude performs an ordinary `cd`, the hook may fail before its own root-resolution logic can run. Its root resolver also checks `CLAUDE_PROJECT_DIR` before hook-input `cwd`, so an active worktree can be shadowed by the original checkout.

## Run-02 strengths

Run-02 is smaller, meets the ~5k always-loaded target, consolidates responsibilities more effectively, and avoids the immediate nested-cwd launcher failure by locating the hook through the original project root.

Its main weaknesses are concentrated in enforcement and fidelity review rather than in the K0 topology itself. Those are repairable without redesigning the candidate.
