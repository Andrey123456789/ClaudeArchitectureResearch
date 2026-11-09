# L0 Run-01 vs Run-02 comparison

## Architecture identity

The two runs agree on the defining L0 architecture:

- `0 Core -> 1 Architecture -> 2 Technology -> 3 Project`;
- product/task inputs outside the hierarchy;
- level-first rules;
- more volatile conformance dependencies only toward same/more-stable levels;
- technology neutrality in Levels 0/1;
- embedded concrete technologies rather than replaceable capabilities;
- two stratified always-loaded decision summaries;
- no `Kind:` taxonomy, capability slots, contracts, module manifests, or feature/task levels.

This agreement is more important than path-level file identity.

## Structural variance

The implementations are not near-clones:

- whole-template path Jaccard: **59 common / 90 union = 0.656**;
- rule-path Jaccard: **17 / 34 = 0.500**;
- skill-directory Jaccard: **27 / 30 = 0.900**.

The rule divergence is mostly module granularity and placement permitted by L0. Run-01 has ten Core rule modules; Run-02 consolidates them into five and adds explicit Project `layout` and `package-management` modules. Run-02 also separates `development-workflow` and `delivery-pipeline`, while Run-01 uses `develop` for the main development procedure.

## Independent quality findings

### Run-01 strengths

- Lower always-loaded estimate (~4.4k vs ~5.0k).
- PreToolUse proactively routes package and project-reference mutations.
- Exact launcher survives a nested cwd when `CLAUDE_PROJECT_DIR` is set.
- Very extensive V2 preservation audit and semantic-strength repair.

### Run-01 weaknesses

- Level-1 concrete technology leakage remained despite self-reporting neutrality: `ProblemDetails` and an Angular-named routing pointer.
- BOM-prefixed JSON causes its hook input parser to fail.
- It anchors operational checks to `CLAUDE_PROJECT_DIR`, so a simulated worktree edit can be ignored because the active worktree is outside the original checkout root.
- npm/pnpm/yarn global options with values bypass its dependency classifier.
- Critical PreToolUse failure is not configured fail-closed.

### Run-02 strengths

- Clean Levels 0/1 under an independent concrete-technology scan.
- BOM-prefixed hook JSON is handled correctly.
- Fewer files and a coherent consolidated level structure.
- Better separation of the development workflow from delivery-pipeline procedure.
- Strong duplicate/restatement cleanup and explicit L0 structural checker.

### Run-02 weaknesses

- Exact hook launcher is cwd-relative and fails after Claude changes into a nested directory.
- Its current root model relies on the hook script location rather than the hook input `cwd`; this is fragile for the required combination of nested cwd and worktrees.
- PreToolUse only blocks peer-dependency bypass flags; it does not pre-route ordinary package/reference mutations.
- `dotnet add ... reference ...` can pass both pre- and post-bash silently when the resulting reference is otherwise structurally allowed, even though project-reference graph changes are Reserved.
- npm/pnpm/yarn global options such as `--prefix`, `--dir`, and `--cwd` can hide package/force mutations from both pre/post classifiers.
- No critical PreToolUse handler has `onFailure: block`.
- The structure checker hardcodes the old shell-form hook command and rejects the safer exec-form configuration.
- Stop reminder fingerprinting ignores content changes when the modified-file/status set stays the same.

## Selection

Run-02 is the better refinement baseline because its L0 architecture is cleaner and its remaining problems are concentrated in deterministic enforcement, which can be repaired without changing L0's architectural identity.
