# L1 5.3 Defect Dossier — Refactored Before First Execution

This dossier combines the original independent L1 audit with recurrent cross-candidate defects discovered while refining M and M1. Items marked **MANDATORY** are part of the first L1 5.3 pass so known failures are not rediscovered through later corrective iterations.

Do not weaken L1 or broaden its architecture to make these checks pass.

## D1 — CRITICAL — Core/Architecture technology neutrality is violated [MANDATORY]

Candidate L1 inherits the L0 stability rule: Core and Architecture must not contain concrete non-platform technology implementation vocabulary beyond the candidate's fixed-platform vocabulary.

Run-02 contains concrete implementation/API vocabulary in Level 0/1. Confirmed examples include:

- Core HTTP: `IExceptionHandler` and concrete problem-details implementation types;
- Core security: ASP.NET Core authentication/Identity/Data Protection implementation technique;
- Core testing: `WebApplicationFactory`;
- Architecture roles/boundaries: `IActionResult`, ASP.NET Core transport/controller technique;
- architecture frame text that mixes role placement with concrete framework technique.

**Required result:** audit every Level 0/1 artifact. Preserve the policy and its trigger/scope, but move concrete implementation technique/binding to Level 2 or the appropriate capability facet. Keep frame-owned placement at Level 1. Do not redefine the platform vocabulary merely to make existing text pass.

## D2 — HIGH — Neutrality checker validates an incomplete approximation [MANDATORY]

The baseline `NON_PLATFORM_TOKENS` deny-list misses known concrete implementation vocabulary, so the checker can report PASS while D1 is violated.

**Required result:** enforce the actual inherited L0/L1 boundary, not a convenient partial deny-list. Include bounded positive/negative fixtures proving:

- actual fixed-platform vocabulary and stable architecture-role vocabulary are accepted;
- representative backend/frontend/persistence/testing implementation vocabulary in Level 0/1 is rejected;
- the checker cannot be made green by merely omitting one token from a hand-maintained list.

## D3 — CRITICAL — Hook launchers are current-directory fragile [MANDATORY]

Baseline hooks use current-directory-relative strings such as `node .claude/hooks/...`; after normal `cd`, the script may not start.

**Required result:** use a root-stable, Windows-safe launcher. Prefer exec-form `command` + `args`; the launcher must work from root, nested cwd, linked worktree, nested worktree cwd, and paths containing spaces.

## D4 — HIGH — Launcher/config root and active worktree root are conflated [MANDATORY]

`${CLAUDE_PROJECT_DIR}` identifies the session-start project root; hook input `cwd` follows Claude/worktrees.

**Required result:** distinguish stable launcher/config root from active repository/worktree root. Repository state, manifests, architecture checks, Stop state, and per-worktree state must resolve from hook input `cwd` and Git. Tests must prove the main checkout is not inspected/mutated when a linked worktree is active.

## D5 — HIGH — Critical PreToolUse can fail open [MANDATORY]

The dependency/reference guard is policy-critical but the baseline does not request supported fail-closed behavior.

**Required result:** critical PreToolUse must use `onFailure: "block"` or an equally strong supported mechanism. Missing script, crash, malformed required input, and timeout must not silently allow the command. Do not make post/Stop hooks blocking merely for symmetry.

## D6 — HIGH — npm/pnpm/yarn global options bypass dependency routing [MANDATORY]

Confirmed examples include npm `--prefix`/`--workspace`, pnpm `--dir`, yarn `--cwd`, and force/legacy-peer forms before the mutation subcommand.

**Required result:** parse supported global options that consume values, package add/remove/update/install forms, and force/legacy-peer flags with table-driven tests. Restore-only/unrelated commands must not become false positives.

## D7 — HIGH — dotnet project-reference mutations bypass PreToolUse [MANDATORY]

`dotnet add ... reference ...` and `dotnet remove ... reference ...` are Reserved project-graph decisions but baseline routing can miss them.

**Required result:** detect and route/block them before execution through the authoritative L1 decision/architecture process. Post-change architecture validation must still verify actual resulting state.

## D8 — HIGH — Post-change shell validation relies too much on command text [MANDATORY]

Baseline PostToolUse coverage does not reliably validate Bash/PowerShell mutations, and command classification alone cannot detect arbitrary scripts/commands that modify `.csproj`, `Directory.Packages.props`, `package.json`, or project references.

**Required result:** after successful Bash/PowerShell calls, compare a bounded per-worktree manifest/project state and validate what actually changed. Keep command-text parsing for pre-routing and explanatory context, but not as the sole detector. Avoid a full repository scan after every unrelated shell call once safe state is established.

## D9 — HIGH — Failed shell calls with partial side effects require PostToolUseFailure coverage [MANDATORY]

A Bash/PowerShell call can modify repository files and then fail. Successful `PostToolUse` is not the event for that outcome.

**Required result:** register and handle `PostToolUseFailure` for Bash|PowerShell. Inspect actual resulting active-worktree state and run the same relevant deterministic validation. Failed shell calls that changed no relevant state should stay quiet. Do not try to block an already completed failed tool call.

## D10 — HIGH — Fresh-state HEAD transitions, later HEAD transitions, rewrites, deletions, and moves need persistent actual-state tracking [MANDATORY]

Without bounded per-worktree state, related mutations can be missed:

- first observed shell event changes HEAD to a revision containing invalid committed manifests while worktree ends clean;
- later HEAD transitions change manifests;
- same-path rewrite leaves the path set unchanged;
- deletion disappears from file-by-file validation;
- rename/move appears as delete + add.

**Required result:** maintain bounded state per active worktree. One initial full manifest validation/snapshot per worktree is acceptable. Later observations should compare relevant content/HEAD state and validate affected artifacts. Deletions/moves must be visible/routed. Skipped directories (for example `node_modules`, build output, nested repositories/worktrees, dot-private areas if deliberately excluded) must not later become false "removed manifest" findings.

## D11 — HIGH — Instruction checker freezes obsolete hook serialization [MANDATORY]

The baseline checker expects a shell-form `node <script>.mjs` string and rejects `$`, so it would reject a correct exec-form launcher.

**Required result:** checker validates executable + args, placeholder use as data, script existence, required matchers/events, critical `onFailure`, and the required `PostToolUseFailure` registration. Active-root semantics are proved behaviorally, not inferred from command text.

## D12 — MEDIUM — Root-relative manual checker commands fail after `cd` [MANDATORY]

Runtime instructions tell Claude to run `node .claude/scripts/...` from an assumed root.

**Required result:** manual checker invocation is reliable from nested directories and active worktrees using one consistent cross-platform root-aware strategy.

## D13 — MEDIUM/HIGH — Windows input/content encoding robustness is incomplete [MANDATORY]

Cross-candidate testing showed practical Windows failure modes around BOM-prefixed hook input and PowerShell 5.1-produced text.

**Required result:**

- normal JSON stdin works;
- UTF-8 BOM-prefixed JSON works;
- empty/malformed required PreToolUse input remains fail-closed;
- relevant manifest/project readers handle supported UTF-8 and BOM-tagged UTF-16LE/UTF-16BE where applicable;
- malformed/odd-length encoded files fail visibly/deterministically instead of crashing unpredictably.

## D14 — MEDIUM/HIGH — Stop deduplication must track material state, not only path sets [MANDATORY]

A Stop fingerprint based only on changed paths/reminder IDs can suppress a legitimate reminder after the same already-modified file changes again.

**Required result:** reminder deduplication must distinguish materially different relevant working-tree states while keeping unchanged-state suppression and `stop_hook_active` loop prevention. Required sequence: remind -> unchanged silent -> same-path material change can remind -> unchanged silent.

## D15 — HIGH — Capability/frame-leaf invariants need bounded mechanical proof [MANDATORY]

L1 combines stability levels with replaceable capabilities. Refinement must not preserve the files while weakening the actual replacement boundary.

**Required result:** mechanically verify at least:

- exactly four slots: architecture, persistence, backend-testing, optional frontend;
- one selected implementation per required slot and zero/one optional frontend;
- architecture remains the frame;
- static composition only; no extra modules/slots/dynamic discovery;
- module facets declare correct Level/Capability/Facet ownership;
- external workflows use facet/role vocabulary rather than selected implementation names where required;
- implementation-name leak rules still work;
- required `binds:` coupling is enforced where module content actually depends on the frame; removing a required bind is a negative test;
- optional frontend can be cleared with the documented finite edits and no broken references/hidden Angular dependency;
- "placement belongs to the frame; technique belongs to the leaf" remains true after neutrality repairs.

Do not optimize for zero coupling; preserve explicit `binds:` when executable frame-specific integration genuinely needs it.

## D16 — MEDIUM — Run-02 is more compressed than Run-01; V2 technique needs a source-based review [MANDATORY REVIEW]

Independent lexical diagnostics showed lower literal V2 coverage in Run-02. This is not proof of semantic loss.

**Required result:** review `source/v2-baseline/` directly. Restore genuinely useful technique/examples only when they materially improve guidance. Do not reconstruct Run-01, restore duplication, or optimize for lexical similarity.

## D17 — LOW/MEDIUM — Always-loaded surface is slightly above the design target [QUALITY REVIEW]

Run-02 is around 5.09k tokens by chars/4, close to the ~5k target.

**Required result:** after correctness, remove only demonstrably redundant routing/decision prose if safe. Do not move policy between trigger classes or trade routing reliability for token savings. This review must not become a repeated optimization loop.

## Required non-regression guards

After refinement:

- all 194 inventory policies + GOV-017/GOV-018 remain represented;
- authoritative-owner regressions = 0;
- `trigger_class` deltas = 0;
- minimum-scope misses = 0;
- broken references = 0;
- primary hierarchy remains `0 Core -> 1 Architecture -> 2 Technology -> 3 Project`;
- conformance dependency direction remains same-or-more-stable only;
- Levels 0/1 satisfy actual technology-neutrality rules;
- exactly four static capability slots remain;
- architecture remains frame; leaves remain leaves;
- no Kinds × Scopes, K-style register, M-style flattening, extra slots, or dynamic plugin system;
- L-style stratified decisions remain;
- selected implementations remain clean-architecture / ef-core(sqlserver) / nunit / angular unless optional frontend is temporarily cleared only inside a test sandbox;
- optional frontend removal remains clean;
- all JavaScript parses;
- deterministic checkers and the documented behavior matrix pass;
- `SPECIFICATION.md` remains an input, not an instruction layer;
- runtime content remains English and free of research metadata.

## Bounded negative checker fixtures

Use a small bounded set, not a mutation-testing campaign. At minimum prove the checker rejects:

1. representative concrete technology inserted into Level 0/1;
2. a reverse/illegal level dependency;
3. a broken internal reference;
4. missing critical `onFailure: "block"`;
5. missing required `PostToolUseFailure` registration;
6. invalid capability selection/extra slot;
7. removed required `binds:` where a selected module still contains frame-specific references;
8. implementation-name leakage outside allowed capability/selection surfaces.

Passing these fixtures is enough to show the central predicates are live. Do not escalate into audit-of-audit or broad mutation analysis after the required matrix passes.
