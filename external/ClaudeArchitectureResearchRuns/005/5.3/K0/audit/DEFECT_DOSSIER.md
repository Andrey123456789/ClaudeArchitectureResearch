# K0 5.3 Defect Dossier — Refactored before refinement

Every item D1-D11 is **MANDATORY**. D12 is a mandatory source-fidelity review and D13 is a bounded quality review.

This dossier incorporates the cross-candidate defects already observed during M/M1/L refinement so K0 can address them in its **first** 5.3 pass rather than through multiple corrective iterations.

The refinement must preserve all frozen policy semantics, trigger classes, minimum scopes, and K0 identity.

## D1 — CRITICAL — Active worktree is not the repository being enforced [MANDATORY]

Run-02 launches `.claude/hooks/hook.cjs` from the original project configuration and derives `PROJECT_DIR` from the hook file location. In a linked worktree, that can inspect the main checkout rather than the active worktree.

Independent reproduction used a real linked worktree with an invalid `.csproj`. `cwd` and `file_path` pointed into the worktree while the launcher came from the main checkout. The hook returned success with no finding; the dependency checker run directly against the worktree found the error.

**Required result:**

- distinguish stable **launcher/config root** from **active repository/worktree root**;
- launch scripts robustly from the configured project root;
- resolve active repository state from hook input `cwd` with bounded upward/Git discovery;
- use the active root for path relativization, Git state, manifest/project validation, instruction validation, co-change checks, and hook state;
- keep state isolated per active worktree;
- prove root, nested cwd, linked worktree, nested worktree cwd, and path-with-spaces behavior.

Do not replace this with `process.cwd()` alone.

## D2 — HIGH — Critical PreToolUse policy can fail open [MANDATORY]

The raw dependency/Git guard lacks explicit fail-closed host semantics. A missing script, crash, malformed required input, or timeout can otherwise allow the mutating action to continue.

**Required result:**

- critical PreToolUse dependency/project-reference/Git-policy enforcement must use supported fail-closed behavior such as `onFailure: "block"`;
- deterministic checker must verify that configuration;
- test missing/crashing target, malformed required input, and timeout/failure where practical;
- do not make PostToolUse/PostToolUseFailure/Stop blocking merely for symmetry after the underlying tool action has already happened.

## D3 — HIGH — Dependency command classification misses legitimate change forms [MANDATORY]

Confirmed Run-02 misses include package removals, dotnet removal forms, and npm/pnpm/yarn global options before the subcommand.

Representative misses:

- `npm uninstall x` / `npm remove x`;
- `pnpm remove x` / `yarn remove x`;
- `dotnet remove Foo.csproj package X`;
- `dotnet package remove X`;
- `npm --prefix frontend install x --force`;
- `npm --workspace app install x --legacy-peer-deps`;
- `pnpm --dir frontend add x --force`;
- `yarn --cwd frontend add x --force`.

**Required result:**

- table-driven parsing of supported add/install/update/remove/uninstall forms;
- skip recognized global options and their values before finding the subcommand;
- support force/legacy-peer bypass flags in reasonable positions;
- support relevant `.cmd`/`.exe` forms on Windows where the runtime supports them;
- preserve restore/read-only cases that should not be routed as dependency selection changes.

Command parsing remains a **pre-routing** mechanism, not the sole post-change detector.

## D4 — HIGH — Project-reference graph mutations bypass pre-execution Reserved routing [MANDATORY]

Confirmed misses include:

- `dotnet add Foo.Api.csproj reference Foo.Domain.csproj`;
- `dotnet remove Foo.Api.csproj reference Foo.Domain.csproj`.

Changing the project-reference graph is Reserved even when the resulting reference is architecturally legal.

**Required result:**

- detect supported add/remove reference forms before execution;
- route/block through the authoritative project-structure/architecture-decision process;
- preserve paths-with-spaces and reasonable option placement;
- validate the resulting graph after actual mutation;
- do not replace the pre-decision gate with a post-hoc architecture check.

## D5 — CRITICAL — Post-change validation is command-text based and misses actual shell side effects [MANDATORY]

Raw Run-02 post-change behavior is incomplete. Bash/PowerShell can alter `.csproj`, `Directory.Packages.props`, `package.json`, or project references through an arbitrary script/program, Git transition, direct file rewrite, deletion, or rename that does not resemble a known dependency command.

The accumulated M/M1 experience also established two essential host/event cases that must be handled in K0's first pass:

- successful tool call -> `PostToolUse`;
- failed tool call with partial filesystem side effects -> `PostToolUseFailure`.

A failed command can leave a mutated manifest behind and must not escape validation simply because the tool outcome is failure.

Fresh-state and HEAD-transition edge cases must also be covered. If the first observed shell action in a worktree changes HEAD to a revision containing an invalid manifest and leaves a clean worktree, relying only on `git status` or a nonexistent previous HEAD snapshot can miss the defect.

**Required result:**

Implement a bounded per-worktree actual-state model covering the documented tracked manifest/project surfaces.

It must detect/validate at least:

- successful Bash/PowerShell mutation;
- failed Bash/PowerShell mutation with partial side effects via `PostToolUseFailure`;
- arbitrary shell mutation whose command text is not recognized;
- first observation in a fresh worktree state;
- first and later HEAD transitions;
- same-path rewrites;
- additions;
- deletions;
- observable rename/move (including delete+add representation);
- project-reference graph changes.

A failed shell call with no relevant state change should remain quiet.

Prefer one initial full tracked-manifest validation/snapshot per worktree, followed by bounded changed-state validation, over a full repository scan after every unrelated shell call.

State must be per-worktree. Deliberately skipped paths (`node_modules`, build output, nested repositories/worktrees, other explicit exclusions) must not later produce false "removed manifest" findings.

## D6 — HIGH — Git safety enforcement is incomplete and broader claims exceed actual coverage [MANDATORY]

K0 OP policy forbids repository-changing Git operations unless explicitly requested/approved, but Run-02's enforcement covers only a subset.

Representative mutation families include:

- index/worktree: `add`, `rm`, `mv`, checkout/switch forms;
- refs: branch/tag creation/deletion, `update-ref`;
- history: reset/revert/cherry-pick/rebase/am forms where applicable;
- patch/application: `apply`, `am`;
- stash/worktree operations;
- other state-changing commands in the supported policy surface.

Read-only forms must not be blocked merely because they begin with `git`.

**Required result:**

- deterministic read-only-vs-mutating classifier aligned with OP policy;
- support reasonable global options such as `git -C`;
- explicit user-request/approval path for mutations where policy allows continuation;
- table-driven positive/negative tests;
- map/documentation claims must match what enforcement actually guarantees.

Do not attempt to enumerate every Git flag ever invented. Cover the documented command families and stop after that matrix is clean.

## D7 — MEDIUM/HIGH — Windows input/content encoding robustness is incomplete [MANDATORY]

Raw Run-02 hook input is not UTF-8-BOM tolerant because it checks a trimmed string but parses the untrimmed one.

Accumulated refinement experience also showed that Windows PowerShell 5.1 can produce BOM-tagged UTF-16 manifest/project files. Reading such files blindly as UTF-8 can create false findings or crashes.

**Required result:**

- normal JSON hook input works;
- one leading UTF-8 BOM on hook JSON is tolerated;
- empty/malformed **required PreToolUse** input remains visible and fail-closed;
- tracked manifest/project readers support normal UTF-8 and applicable BOM-tagged UTF-16LE/UTF-16BE content;
- malformed/odd-length encoded tracked files produce deterministic visible findings rather than uncontrolled crashes;
- do not add PowerShell-specific runtime dependencies solely to parse text.

## D8 — HIGH — Structural checker freezes old hook serialization instead of checking runtime properties [MANDATORY]

Run-02 checker expects the baseline's specific inline launcher shape and rejects the safer exec-form `command: "node"` + `args: [...]` configuration.

**Required result:**

Checker must validate properties rather than old serialization:

- executable/argument-vector shape;
- placeholder/launcher target;
- referenced script existence;
- event matchers;
- required `PreToolUse` fail-closed behavior;
- required `PostToolUseFailure` Bash|PowerShell registration;
- existing PostToolUse/Stop configuration;
- active-root/worktree behavior via behavioral tests, not string inference.

Add a small bounded negative fixture proving removal of `onFailure: "block"` fails and another proving removal of required `PostToolUseFailure` fails.

Do not weaken structural checks merely to accept the repaired settings.

## D9 — MEDIUM — Runtime manual checker commands are cwd-relative [MANDATORY]

Raw runtime instructions contain `node .claude/...` checker commands that can fail after Claude performs `cd`.

**Required result:**

- make every instructed checker invocation reliable from nested cwd and active worktree;
- use one consistent cross-platform root-aware strategy;
- test paths containing spaces;
- do not introduce POSIX-only shell assumptions.

## D10 — MEDIUM — Stop fingerprint is path-set based rather than material-state based [MANDATORY]

Independent reproduction:

1. production file changes without tests -> reminder;
2. same file changes again with the same Git-status path set -> no reminder.

The reminder fingerprint therefore treats materially new work as an unchanged state.

**Required result:**

- first applicable state -> reminder;
- immediate unchanged repeat -> silent;
- materially changed same-path state -> eligible to remind again;
- next unchanged repeat -> silent;
- `stop_hook_active=true` -> no loop;
- bounded deterministic diff/content identity, not external transcript/session state.

## D11 — HIGH — K0 checker does not enforce the binding Kind dependency direction [MANDATORY]

K0 declares the conformance direction:

`WF -> KNW -> STD -> DEC -> OP`

and:

`ENF -> STD / DEC`

while explicit routing pointers may point differently.

Run-02 checks acyclicity but not whether a non-routing source-Kind -> target-Kind edge is legal. An acyclic but directionally invalid dependency can therefore pass.

**Required result:**

- formalize the declared K0 conformance relation without inventing another taxonomy;
- distinguish conformance dependencies from routing pointers;
- preserve skill-private-reference behavior;
- mechanically reject reversed/cross-Kind conformance edges;
- explicitly cover ENF's allowed target Kinds rather than silently omitting ENF from the model.

Bounded fixtures must prove:

- legal `WF -> KNW -> STD -> DEC -> OP` edges pass;
- reversed/cross-Kind edge fails;
- legal `ENF -> STD` and `ENF -> DEC` pass;
- illegal `ENF -> KNW/WF` conformance edge fails;
- allowed routing-pointer exception passes.

## D12 — MANDATORY REVIEW — Compact Run-02 needs source-based V2 technique review

Independent lexical diagnostics show normalized-policy best-match is essentially tied between runs, while Run-02 is substantially less literal relative to V2 sections.

This does **not** prove semantic loss. It does require one fresh source-based review against `source/v2-baseline/`.

For materially weakly represented V2 sections, classify content as:

- normative policy -> must remain through frozen inventory ownership;
- useful technique/example -> restore if practically valuable;
- duplicate/obsolete ownership -> keep omitted;
- irrelevant implementation detail -> keep omitted.

Place restorations by K0 Kind and Scope, not by V2 filename lineage.

Do not reconstruct Run-01 and do not restore wording merely to improve lexical similarity.

Perform this review once. Do not reopen it after a clean final audit merely to accumulate stronger evidence.

## D13 — QUALITY REVIEW — Preserve K0 compactness and one-register design

Run-02 already meets the roughly 5k always-loaded target and is smaller than Run-01.

After correctness is established:

- keep the one DEC register concise;
- do not turn `Affects` into duplicated policy prose;
- do not create files merely to populate taxonomy cells;
- do not add a second decision hierarchy;
- do not add capability contracts/manifests/slots/facets;
- reject new files/layers unless a concrete ownership or reliability problem requires them;
- do not start a second optimization loop once correctness and confirmation are clean.

## Required non-regression invariants

After all repairs:

- all 194 normalized policies plus GOV-017/GOV-018 remain represented;
- authoritative owner regressions = 0;
- trigger-role delta count = 0;
- minimum-scope miss count = 0;
- unresolved broken references = 0;
- seven Kinds remain the responsibility taxonomy;
- declared Scopes remain the applicability taxonomy;
- each applicable artifact has one primary Kind and Scope;
- mechanism/loading still follows Kind;
- STD remains scope-first and path-scoped;
- one always-loaded DEC register remains authoritative;
- decision summaries are not duplicated into STD/KNW/WF;
- `Affects` targets exist and are consistent with decision citations;
- procedures do not become STD;
- authoritative normative policy does not exist only in KNW;
- no `Level:` hierarchy appears;
- no capability contracts/module manifests/selection/facets appear;
- embedded technology wording remains allowed where K0 assigns it to the correct responsibility/scope;
- all JavaScript parses;
- optional empty taxonomy directories are not created for symmetry;
- Windows/BOM/encoding, nested-cwd, linked-worktree, success/failure shell, Git safety, and Stop tests pass.
