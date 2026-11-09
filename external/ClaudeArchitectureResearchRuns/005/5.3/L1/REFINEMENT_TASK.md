# L1 controlled-refinement task — Iteration 005 / 5.3

## 1. Goal

Produce a **strictly better implementation of Candidate L1** from the immutable selected Run-02 baseline.

This is not a new candidate-generation run and not an architecture redesign. The purpose is to remove confirmed implementation defects and known recurrent cross-candidate enforcement failures so later benchmarks compare L1's architecture rather than accidental generation quality.

This task is intentionally **bounded**. Repair the documented mandatory defect surface, run the documented regression matrix, perform one complete cumulative confirmation audit, write the report, clean temporary evidence, and stop. Do not turn a clean result into an audit-of-audit, mutation-testing campaign, live-hook-engine experiment, repeated baseline proving, or open-ended shell fuzzing exercise.

## 2. Inputs and boundaries

Read completely before editing:

- `CANDIDATE.md`;
- `audit/DEFECT_DOSSIER.md`;
- `audit/BASELINE_SELECTION.md`;
- `audit/RUN_COMPARISON.md`;
- `audit/RUN3_DECISION.md`;
- `audit/EXTERNAL_MECHANICS_NOTES.md`;
- `audit/evidence/INDEPENDENT_TESTS.md`;
- `source/inventory.json`;
- `source/shared-research-invariants.json`;
- the complete `source/v2-baseline/` tree;
- `baseline/TASK.md`;
- `baseline/CANDIDATE.md`;
- the complete immutable `baseline/template/`.

The raw Run-01 template is intentionally absent. Its report is comparative evidence only. Do not reconstruct, obtain, or copy Run-01 implementation files.

Do not modify `baseline/`, `source/`, `audit/`, `CANDIDATE.md`, or this task.

Write only under `output/`.

Use `output/.work/` for temporary audit/test material. **Create the test harness once, keep it until the report and final confirmation are complete, and remove it only at the very end. Do not delete it early and reconstruct it from transcript/session history.**

Do not read sibling architecture/run workspaces, network material, external session/transcript storage, or sources outside this L1 refinement workspace.

## 3. Establish the working copy

Before changing content:

1. verify `output/` is empty except for any explicitly pre-created empty placeholder directory;
2. copy `baseline/template/` exactly to `output/template/`;
3. verify the initial copy is byte-identical to baseline;
4. record one initial tree hash;
5. make all template changes only in `output/template/`.

The immutable comparison point is L1 Run-02.

Do not repeatedly re-hash an unchanged tree merely for stronger evidence. One initial hash and one final hash are sufficient unless a concrete integrity problem appears.

## 4. L1 architecture identity that must not change

The refined template remains L1 only if all of these remain true:

- primary stability hierarchy is `0 Core -> 1 Architecture -> 2 Technology -> 3 Project`;
- rules remain level-first;
- each instruction artifact remains correctly classified by level;
- conformance dependencies point only to the same or a more stable level;
- Levels 0/1 satisfy the actual candidate technology-neutrality rule;
- exactly four capability slots exist:
  - `architecture` required frame;
  - `persistence` required leaf;
  - `backend-testing` required leaf;
  - `frontend` optional leaf;
- selected implementations remain:
  - `architecture/clean-architecture`;
  - `persistence/ef-core`, provider `sqlserver`;
  - `backend-testing/nunit`;
  - `frontend/angular`;
- capability composition remains static;
- contracts/manifests remain maintainer metadata;
- architecture owns placement; leaves own implementation technique;
- stable role vocabulary mediates frame/leaf interaction where possible;
- explicit `binds:` remains where stable roles genuinely cannot express executable frame integration;
- decisions remain L-style and stratified;
- no K Kind taxonomy or K-style single cross-level register;
- no M-style flattening of the level hierarchy;
- no extra capability slots, dynamic plugin discovery, or unrelated meta-layer.

Do not solve enforcement defects by weakening L1, expanding leak exceptions, redefining platform vocabulary, or changing architecture family.

## 5. Mandatory defect set

Repair **every mandatory item D1-D15** in `audit/DEFECT_DOSSIER.md` and complete mandatory review D16. Perform D17 only as a bounded quality review after correctness.

Each claimed repair needs evidence against the final files. Demonstrate a baseline failure once where cheap/useful; do **not** rerun the full baseline suite after every repair.

### 5.1 Level 0/1 neutrality and placement-vs-technique

Audit every Level 0/1 artifact.

For concrete non-platform framework/API/provider/testing/persistence/frontend technique:

- preserve the stable policy at Core/Architecture;
- move concrete implementation technique/binding to Level 2 or the selected capability facet;
- keep project selection/default at Level 3;
- preserve authoritative owner, trigger class, and minimum scope;
- keep frame-owned placement at Level 1 but concrete technology technique out of the frame when roles can express the boundary.

Do not broaden fixed-platform vocabulary to legalize the baseline.

### 5.2 Checker must prove L1, not baseline serialization

Update deterministic checks so they enforce behaviorally correct properties:

- true Level 0/1 neutrality;
- level assignment and conformance direction;
- four-slot static capability composition;
- selected/optional module correctness;
- frame/leaf ownership, facet metadata, leak rules, and required `binds:`;
- imports, paths, references, required workflows/knowledge;
- corrected exec-form hook configuration;
- critical PreToolUse fail-closed property;
- required `PostToolUseFailure` registration.

Use the bounded negative fixtures listed in the dossier. Do not build a mutation-testing framework for the harness.

### 5.3 Hook/root model

Distinguish:

1. **launcher/config root** — stable location used to start generated hook scripts;
2. **active repository/worktree root** — repository Claude is actually operating in, resolved from hook input `cwd` and Git.

Do not use `${CLAUDE_PROJECT_DIR}` as a substitute for active worktree root.

Use a Windows-safe current hook configuration. Prefer exec-form `command` + `args`. Critical PreToolUse policy enforcement must fail closed with supported failure semantics.

### 5.4 Actual-state shell validation

Command-text classification is useful for **pre-execution routing** but is not sufficient for post-change validation.

For Bash/PowerShell post events, validate the **actual resulting active-worktree state** so relevant manifest/project mutations cannot bypass checks merely because command text is unfamiliar.

The bounded supported surface is:

- successful shell calls (`PostToolUse`);
- failed shell calls with partial side effects (`PostToolUseFailure`);
- fresh and later tracking state;
- first and later HEAD transitions;
- same-file rewrites;
- additions, deletions, moves/renames of tracked manifest/project artifacts;
- root cwd, nested cwd, linked worktree, nested worktree cwd;
- Bash and PowerShell.

Prefer bounded per-worktree snapshot/state over a full scan after every unrelated command. One initial full validation/snapshot per worktree is acceptable. State from one worktree must not contaminate another. Deliberately skipped directories must not later become false removals.

### 5.5 Dependency/reference routing

Before mutating commands execute, correctly identify at least:

- dotnet add/remove package forms;
- dotnet add/remove reference forms;
- npm/pnpm/yarn dependency mutations;
- supported global options taking values before the subcommand (`--prefix`, `--workspace`, `--dir`, `--cwd`, equivalents used by the parser);
- peer-dependency bypass flags such as `--force`, `-f`, `--legacy-peer-deps` with reasonable placement.

Restore-only/unrelated commands must not become false positives. Project-reference graph mutation remains Reserved and must not become a silent post-hoc check.

## 6. Build one bounded regression harness

Create controlled sandboxes only under `output/.work/`. Cap Git upward discovery from the first Git test.

**Build the harness once. Keep it until report + final confirmation are finished. Do not delete and reconstruct it from transcript/history.**

Do not attempt to move the already-running Claude Desktop/Code session into `output/template/` or a sandbox merely to observe live hook activation. Hook configuration is session-scoped; such relocation is not an acceptance requirement. Controlled process-level execution of generated settings/scripts plus documented host semantics is sufficient.

## 7. Required behavioral regression matrix

### 7.1 Launch/root/worktree

Test:

- project-root cwd;
- nested backend cwd;
- nested frontend cwd where frontend is enabled;
- real linked Git worktree where launcher root and active root differ;
- nested cwd inside that worktree;
- paths containing spaces;
- manifest/architecture/Stop checks inspect active worktree content, not main checkout;
- per-worktree state does not cross-contaminate worktrees.

### 7.2 Hook input and Windows encoding

Test:

- normal JSON stdin;
- UTF-8 BOM-prefixed JSON stdin;
- empty/malformed required PreToolUse input has intended fail-closed behavior;
- exact generated `command`/`args` shape;
- missing/crashing/timed-out critical PreToolUse demonstrates fail-closed behavior where feasible through controlled tests;
- manifest/project readers handle supported UTF-8 and BOM-tagged UTF-16LE/UTF-16BE where applicable;
- malformed/odd-length encoded manifest input fails visibly/deterministically.

### 7.3 Dependency/reference command matrix

Use table-driven positive and negative cases across:

- npm;
- pnpm;
- yarn;
- dotnet package commands;
- dotnet project-reference add/remove;
- global-option prefixes/values;
- force/legacy-peer flags;
- restore-only and unrelated commands.

### 7.4 Shell actual-state matrix

Use representative tracked `.csproj`, `Directory.Packages.props`, and `package.json` artifacts.

Prove:

- successful Bash mutation detected;
- successful PowerShell mutation detected;
- failed Bash partial mutation detected through `PostToolUseFailure`;
- failed PowerShell partial mutation detected through `PostToolUseFailure`;
- failed shell call with no relevant state change stays quiet;
- arbitrary shell-driven manifest mutation is detected even if command text is not recognized;
- fresh state + first HEAD transition to invalid committed manifest is detected;
- later HEAD transition is detected;
- same-path rewrite is detected;
- tracked manifest deletion is not silent;
- rename/move is not silent;
- unrelated shell command after unchanged state does not trigger noisy repeated full validation;
- skipped paths do not cause false "removed manifest" findings.

### 7.5 Stop/material-state behavior

Prove:

- initial applicable co-change condition reminds;
- `stop_hook_active` prevents loops;
- unchanged relevant state does not repeat endlessly;
- materially changing the same already-modified file can remind again;
- another unchanged Stop is silent;
- worktree A state does not suppress worktree B.

### 7.6 Level/stability structure

Prove:

- representative Level 0/1 concrete technology leak fails;
- allowed fixed-platform/stable-role vocabulary passes;
- rule path and header level agree;
- reverse/illegal conformance dependency fails;
- same-or-more-stable dependency passes;
- no `Kind:` taxonomy or K-style register appears;
- decision stratification remains valid.

### 7.7 Capability/frame-leaf structure

Prove:

- exactly four agreed slots;
- required slots selected, optional frontend zero/one;
- selected modules only ship (static composition);
- architecture is frame; others are leaves;
- module/facet Level/Capability/Facet metadata matches manifests;
- required facet files exist;
- implementation-name leak negative fixture fails;
- a required `binds:` removal fails when frame-specific references remain;
- optional frontend removal procedure produces a clean checker result with no hidden Angular reference;
- external workflows use stable facet/role vocabulary as required;
- placement stays frame-owned and concrete technique stays Technology/leaf-owned.

### 7.8 Policy/V2/standalone structure

Verify:

- all 194 policies + GOV-017/GOV-018;
- owner fidelity;
- `trigger_class` unchanged;
- minimum scope unchanged or broader only when semantically justified;
- semantic strength/conditions preserved;
- no duplicate normative ownership;
- references/imports resolve;
- runtime language/research metadata hygiene;
- `SPECIFICATION.md` remains input rather than instruction layer;
- source-based V2 review completed without restoring duplication.

## 8. Reviews and repair discipline

### 8.1 V2 fidelity

Review the frozen V2 source, not Run-01 implementation. Restore material technique/examples only if useful. Do not optimize for lexical similarity.

### 8.2 Capability quality

Review frame/leaf coupling, role vocabulary, leaks, `binds:`, and optional frontend removal. Do not force zero coupling when executable integration genuinely requires explicit binding.

### 8.3 Efficiency

Baseline always-loaded is approximately 5.09k by chars/4. After correctness, remove only demonstrably redundant routing/decision prose. Do not move policy, weaken routing, or run repeated compaction cycles. New files/layers require concrete ownership/reliability justification.

## 9. Primary repair audit

After implementing mandatory fixes and the test matrix, perform one substantive audit of the actual `output/template/` covering:

1. all 194 policies + two shared invariants;
2. authoritative owner, trigger, minimum scope, strength/conditions;
3. Level assignment/dependency direction;
4. Level 0/1 technology neutrality;
5. four-slot capability conformance;
6. frame/leaf separation, leaks, `binds:`, optional frontend removal;
7. V2 preservation;
8. duplicates/restatements;
9. internal refs/imports;
10. hook/checker behavior and complete documented matrix;
11. Windows/BOM/UTF-16 behavior;
12. nested-cwd/worktree correctness;
13. Stop material-state behavior;
14. standalone/research/language hygiene;
15. always-loaded/context and justified complexity.

Repair every concrete defect this audit finds.

## 10. One cumulative confirmation audit and STOP rule

After repairs, run **one complete cumulative confirmation audit** using the existing harness.

If it finds a concrete template defect or regression:

1. repair that defect;
2. rerun affected focused tests;
3. rerun the cumulative confirmation audit because the template changed.

When one complete cumulative confirmation audit finds **zero concrete template defects**, convergence is established.

Then:

1. finalize `output/REFINEMENT_REPORT.md` from that evidence;
2. verify the report does not claim unsupported results;
3. record one final tree hash;
4. remove `output/.work/`;
5. verify `output/` contains only `template/` and `REFINEMENT_REPORT.md`;
6. **STOP IMMEDIATELY**.

### Explicitly forbidden after a clean confirmation

Do **not** reopen a clean result to:

- mutation-test the test harness;
- prove that the audit can detect planted defects beyond the bounded negative fixtures already required;
- audit the audit;
- verify the verifier;
- rebuild deleted test tooling from transcript/session history;
- repeat full baseline comparisons;
- obtain a stronger narrative proof;
- repeat whole-tree hashes;
- relocate the live Desktop session into a sandbox to observe hooks;
- start open-ended shell-command fuzzing;
- rerun a full template audit because only report prose changed.

A clean required confirmation audit is sufficient evidence of convergence.

## 11. Baseline-comparison budget

Use baseline evidence economically:

- initial byte-identical working-copy check is required;
- reproduce a baseline defect once when it materially demonstrates the repair;
- do not run the entire expensive matrix against baseline after every change;
- final promotion compares result and metrics to baseline, but the full behavioral suite is primarily a gate on the refined output.

The purpose is to prove improvement, not repeatedly prove that baseline is worse.

## 12. Strict cumulative promotion gate

Promote only if all of the following hold simultaneously:

1. every mandatory D1-D15 item is fixed;
2. D16 review completed and real preservation gaps repaired;
3. D17 review completed without harmful optimization;
4. all 196 normalized runtime requirements remain represented;
5. authoritative-owner regressions = 0;
6. `trigger_class` deltas = 0;
7. minimum-scope misses = 0;
8. unresolved broken references = 0;
9. L1 identity is unchanged;
10. Level 0/1 neutrality is materially corrected and mechanically tested;
11. stability dependency direction is mechanically tested;
12. four-slot capability composition, frame/leaf separation, leak rules, `binds:`, and optional-frontend behavior pass;
13. hook launching/root semantics are Windows/nested-cwd/worktree correct;
14. critical PreToolUse is fail-closed;
15. successful and failed shell actual-state validation passes the documented matrix;
16. fresh/later HEAD, rewrite, deletion/move state cases pass;
17. Stop material-state behavior passes without loops;
18. Windows/BOM/encoding cases pass;
19. V2 fidelity is no worse in substance;
20. complexity/context growth is justified;
21. no checker/test/requirement was weakened merely to obtain PASS.

If a proposed edit creates a trade-off with no demonstrated net improvement, revert it.

**A tie is not an improvement.**

## 13. Deliverables

Final `output/` must contain only:

```text
output/
├── template/
└── REFINEMENT_REPORT.md
```

`REFINEMENT_REPORT.md` must include:

- final status: `STRICTLY_BETTER`, `NOT_PROMOTED`, or `BLOCKED`;
- baseline provenance;
- D1-D15 disposition and evidence;
- D16 V2-fidelity review result;
- D17 efficiency review result;
- files added/removed/changed;
- before/after runtime file count and always-loaded estimate;
- owner regression count;
- trigger delta count;
- minimum-scope miss count;
- broken-reference count;
- Level 0/1 neutrality and stability-direction results;
- capability/frame-leaf/leak/`binds:`/optional-frontend results;
- hook/root/worktree matrix summary;
- dependency/reference routing summary;
- successful/failed shell actual-state matrix summary;
- Windows/BOM/UTF-16 summary;
- Stop material-state summary;
- material V2 technique restored or intentionally not restored;
- primary audit result;
- cumulative confirmation-audit result;
- explicit explanation of why the result is strictly better than baseline.

Do not claim `STRICTLY_BETTER` unless the full cumulative gate passes.
