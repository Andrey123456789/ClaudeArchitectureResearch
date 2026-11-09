# K0 controlled-refinement task — Iteration 005 / 5.3

## 1. Goal

Produce a **strictly better implementation of Candidate K0** from the immutable selected Run-02 baseline.

This is not a new candidate-generation run and not an architecture redesign. The purpose is to remove confirmed implementation defects so later benchmarks compare K0's architecture rather than accidental raw-generation quality.

This task is intentionally **bounded**. Repair the documented defect surface, run the documented regression matrix, perform one complete cumulative confirmation audit, write the report, clean temporary evidence, and stop.

Do **not** turn a clean result into:

- audit-of-audit;
- verifier-of-verifier work;
- a mutation-testing campaign against the test harness;
- repeated convergence demonstrations;
- live-session hook relocation experiments;
- open-ended Git/shell-command fuzzing;
- repeated baseline proving after the documented defect has already been demonstrated.

Once the documented matrix passes and one complete confirmation audit finds zero concrete template defects, convergence is established.

**A tie is not an improvement.**

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

The Run-01 template is intentionally absent. Do not seek, reconstruct, or infer its files. Its report/comparison evidence may establish that a stronger behavior is feasible, but it is not a source to copy from.

Do not modify `baseline/`, `source/`, `audit/`, `CANDIDATE.md`, or this task.

Write only under `output/`.

Use `output/.work/` for temporary audit/test material. Create the test harness **once**, keep it until the report and final confirmation are complete, and delete it only at the very end. Do not delete it early and reconstruct it from transcript/session history.

Do not read sibling candidate/run workspaces, external repositories, network material, or external session/transcript storage.

## 3. Establish the working copy

Before changing content:

1. verify `output/` is empty except for an explicitly pre-created empty directory;
2. copy `baseline/template/` exactly to `output/template/`;
3. verify the initial working copy is byte-identical to the baseline;
4. record one initial tree hash;
5. make all template changes only in `output/template/`.

The immutable comparison point is K0 Run-02.

Do not repeatedly hash an unchanged tree merely to obtain stronger evidence. One initial hash and one final hash are sufficient unless a concrete integrity defect appears.

## 4. K0 identity — non-negotiable

The refined result remains K0 only if all of the following remain true:

- responsibility is classified by the seven Kinds `OP`, `DEC`, `STD`, `KNW`, `WF`, `ENF`, `IN`;
- applicability uses the declared Scopes `common`, `backend`, `backend-tests`, `frontend`, `delivery`, `repo/meta`;
- each applicable instruction artifact has one primary Kind and one Scope;
- Kind determines mechanism/loading;
- OP and DEC remain always-loaded;
- exactly one always-loaded decision register remains authoritative;
- STD remains path-scoped and organized by Scope;
- KNW remains technique/examples, not authoritative normative ownership;
- WF remains procedure/steps/stop conditions/output;
- ENF remains deterministic enforcement/assets;
- IN remains product input and cannot override engineering policy;
- decision entries retain stable IDs, concise summary, `Details in`, and `Affects` semantics;
- decision summaries are not duplicated as separate policy manuals;
- technology remains embedded in the appropriate Kinds;
- no capability contracts, module manifests, slot selection, generic facet lookup, or replacement mechanism appears;
- no `Level:` hierarchy or `0-core/1-architecture` structure appears;
- no file exists merely to populate a Kind × Scope cell.

Do not make K0 look like M, L0, L1, or K1 while fixing it.

## 5. Mandatory defect set

Resolve **D1-D11** in `audit/DEFECT_DOSSIER.md`.

Complete the mandatory D12 V2-fidelity review and D13 compactness review. If either review reveals a concrete defect, repair it before confirmation.

A claimed repair is not sufficient. Each mandatory defect needs behavioral or structural evidence against the final files. Demonstrate a baseline failure only once where cheap and useful; do not rerun the entire baseline suite after every repair.

### 5.1 Hook/root model

The final design must distinguish:

1. **launcher/config root** — stable location used to launch the hook script;
2. **active repository/worktree root** — repository Claude is actually operating in, resolved from hook input `cwd` and Git when needed.

Do not use `${CLAUDE_PROJECT_DIR}` as a substitute for the active worktree root.

Prefer the current cross-platform exec-form hook configuration (`command` + `args`) for Node hooks with path placeholders. Critical policy PreToolUse enforcement must fail closed with supported host failure semantics.

Every repository-sensitive operation must use the active root:

- path relativization;
- Git state/safety checks;
- manifest/project graph validation;
- co-change checks;
- instruction validation when the active worktree's instruction system is changed;
- hook state persistence.

### 5.2 Command-text pre-routing vs actual-state post-validation

Command classification is useful for **pre-execution routing**. It is not sufficient for **post-execution validation**.

PreToolUse must correctly route/block known dependency, project-reference, and repository-changing Git commands.

After Bash/PowerShell calls, validate the **actual resulting active-worktree state** so a mutation cannot bypass checks merely because command text was unfamiliar.

The bounded supported post-change surface includes:

- successful shell calls (`PostToolUse`);
- failed shell calls with partial side effects (`PostToolUseFailure`);
- fresh tracking state and later tracking state;
- first and later HEAD transitions;
- same-file rewrites;
- tracked manifest additions, deletions, and observable moves/renames;
- root cwd, nested cwd, linked worktree, nested worktree cwd;
- Bash and PowerShell.

Prefer one bounded **per-worktree** snapshot/state mechanism over a full repository scan after every unrelated shell call. On first shell observation in a worktree, one full tracked-manifest validation/snapshot is acceptable to establish a safe baseline.

State for one worktree must not contaminate another. Deliberately skipped directories such as `node_modules`, build output, nested repositories/worktrees, and other excluded areas must not later be falsely reported as removed tracked manifests.

### 5.3 Dependency/project-reference routing

Before execution, correctly identify at least:

- npm/pnpm/yarn dependency add/install/update/remove/uninstall forms;
- supported global options before subcommands, including options that consume values (`--prefix`, `--workspace`, `--dir`, `--cwd`, and supported equivalents);
- force / legacy-peer dependency bypass flags regardless of reasonable placement;
- dotnet/NuGet package add/update/remove forms;
- dotnet project-reference add/remove forms, including common option placement and paths with spaces;
- restore/read-only forms that must not be misclassified as dependency selection changes.

Project-reference graph mutation is Reserved. A structurally legal new reference is still a graph decision and must not become a silent post-hoc check.

### 5.4 Git-safety routing

K0's OP Git policy must match deterministic enforcement.

Build one compact table-driven classifier that distinguishes representative read-only Git operations from repository-changing operations, including reasonable global options such as `git -C`.

Cover representative mutating families including index/worktree/ref/history changes, branch/tag/worktree/stash operations, patch/application operations, and other supported repository mutations. Do not rely solely on a partial static permission-pattern list while the map claims broader protection.

Do not block a read-only command merely because it begins with `git`.

### 5.5 K0 structure checker

Refactor `check-instructions` as needed so it checks properties rather than the baseline's old serialization.

It must enforce at least:

- Kind/Scope header and location rules;
- mechanism/loading per Kind;
- STD scope/path consistency;
- one-register DEC integrity;
- `Details in` / `Affects` existence and consistency;
- no decision-summary restatement into STD/KNW/WF;
- no procedures in STD;
- no bare authoritative normative ownership only in KNW;
- skill-private reference boundaries;
- legal **Kind conformance dependency direction**, not merely acyclicity;
- routing-pointer exceptions only where explicitly allowed;
- `ENF -> STD / DEC` conformance behavior as declared by K0;
- no Levels/capability machinery;
- current hook executable/args/script existence/event matcher/failure-mode configuration;
- required `PostToolUseFailure` registration;
- human-map coverage.

### 5.6 Root-aware manual tools

Every runtime instruction that tells Claude to run repository checkers/tools must remain valid after `cd` and inside linked worktrees.

Use one consistent cross-platform root-aware invocation strategy. Do not require POSIX-only shell syntax.

### 5.7 Windows/input robustness

Preserve normal JSON hook input and make required input robust to a UTF-8 BOM.

Manifest/project readers must correctly handle the Windows encodings the workflow can plausibly create, including UTF-8 and BOM-tagged UTF-16LE/UTF-16BE where applicable.

Malformed or odd-length encoded tracked manifest input must fail visibly/deterministically rather than crash unpredictably.

### 5.8 Stop reminder state

Preserve loop suppression while making reminder identity sensitive to materially changed relevant working-tree state, not only the same path set/reminder IDs.

Required behavior:

1. first applicable state -> reminder;
2. immediate unchanged repeat -> silent;
3. materially change the same relevant file again -> reminder may fire again;
4. another unchanged repeat -> silent;
5. `stop_hook_active=true` -> no loop.

Do not use external transcript/session state.

## 6. Required bounded behavioral matrix

Create controlled sandboxes only under `output/.work/`. Cap upward Git discovery from the first Git sandbox test.

Do **not** move the already-running Claude Desktop/Code session into `output/template/` or a sandbox to observe a different hook configuration. Hook configuration is session-scoped. Controlled process-level execution of the generated hooks/configuration plus documented host semantics is sufficient for this refinement.

### 6.1 Launch/root/worktree

Test at minimum:

- project root;
- nested backend cwd;
- nested frontend cwd;
- real linked Git worktree root;
- nested cwd inside the worktree;
- paths containing spaces;
- Bash matcher;
- PowerShell matcher;
- active-worktree manifest/Git/co-change checks do not inspect the main checkout by mistake.

### 6.2 Input/failure/encoding

Test:

- normal JSON stdin;
- UTF-8 BOM-prefixed JSON stdin;
- empty/malformed required PreToolUse input -> visible fail-closed behavior;
- missing/crashing critical PreToolUse target -> fail closed;
- timeout/failure semantics where practical;
- UTF-8 and applicable UTF-16LE/UTF-16BE tracked manifest content;
- malformed/odd-length encoded manifest input -> deterministic visible finding, not uncontrolled crash.

### 6.3 Dependency/project-reference matrix

Use table-driven cases across:

- npm;
- pnpm;
- yarn;
- dotnet/NuGet package commands;
- dotnet project-reference add/remove;
- global options and option values;
- force/legacy-peer bypass flags;
- paths with spaces;
- restore/read-only/unrelated commands that must remain allowed.

### 6.4 Git-safety matrix

Test representative:

- read-only commands;
- index mutations;
- worktree mutations;
- ref/branch/tag mutations;
- history/reset/revert/cherry-pick/rebase-like mutations where supported;
- stash/worktree operations;
- patch/application forms;
- `git -C` and reasonable global-option placement;
- explicit user-request/approved path where policy allows continuation.

The suite should demonstrate the policy boundary, not enumerate every Git flag ever invented.

### 6.5 Actual-state shell matrix

Use representative tracked `.csproj`, `Directory.Packages.props`, and `package.json` cases.

Prove:

- successful Bash mutation detected;
- successful PowerShell mutation detected;
- failed Bash mutation with partial side effects detected through `PostToolUseFailure`;
- failed PowerShell mutation with partial side effects detected through `PostToolUseFailure`;
- failed shell command with no relevant state change stays quiet;
- arbitrary shell-driven manifest mutation detected even if command text is unknown;
- fresh state + first shell/HEAD transition to invalid committed manifest detected;
- later HEAD transition detected;
- same-path manifest rewrite detected;
- tracked manifest deletion not silently ignored;
- rename/move not silently lost;
- unchanged unrelated shell command does not cause noisy repeated validation;
- deliberately skipped paths do not create false removed-manifest findings.

### 6.6 Stop matrix

Test the five-state sequence in Section 5.8, plus representative production/test/schema/seed obligations already present in K0.

### 6.7 K0 structural negative/positive fixtures

Use a **small bounded set** of fixtures to prove the checker is not blind. This is not permission to build a general mutation-testing framework.

At minimum:

- legal `WF -> KNW`, `KNW -> STD`, `STD -> DEC`, `DEC -> OP` conformance edges -> PASS;
- illegal/reversed/cross-Kind conformance edge -> FAIL;
- legal `ENF -> STD` and `ENF -> DEC` -> PASS;
- illegal `ENF -> KNW/WF` conformance edge -> FAIL;
- explicit routing pointer that is allowed to point differently -> PASS;
- wrong Kind/mechanism placement -> FAIL;
- broken `Affects` target -> FAIL;
- decision restatement violation -> FAIL;
- procedure in STD -> FAIL;
- authoritative norm only in KNW -> FAIL;
- forbidden `Level:` or capability machinery -> FAIL;
- missing critical `onFailure: "block"` -> FAIL;
- missing required `PostToolUseFailure` registration -> FAIL;
- broken internal reference -> FAIL.

After these documented fixtures pass, do **not** start open-ended checker mutation analysis.

## 7. Source-based V2 fidelity review

Run-02 is compact and lexically farther from V2 than Run-01. Review `source/v2-baseline/` directly.

For each materially weakly represented section:

1. identify its responsibility;
2. classify it as normative policy, useful technique/example, duplicate/obsolete ownership, or irrelevant implementation detail;
3. preserve every accepted normative requirement through the frozen inventory owner;
4. restore useful technique/examples only when they improve practical guidance;
5. place restored content according to K0 Kind and Scope, not V2 filename lineage;
6. do not restore text merely to improve lexical similarity;
7. do not reconstruct the absent Run-01 template.

This review is performed once. After the final V2/policy audit is clean, do not reopen it merely to search for stronger prose evidence.

## 8. K0-specific architecture review

Explicitly verify:

- a maintainer can place a new item by Kind then Scope without a hidden second taxonomy;
- Kind predicts loading/mechanism;
- every STD `paths:` matches its Scope;
- one DEC register remains authoritative;
- every decision citation has consistent `Affects` coverage and every target exists;
- routing pointers are distinguishable from conformance dependencies;
- conformance dependencies follow K0's allowed Kind direction, including ENF rules;
- embedded technologies may appear in multiple Kinds only because each artifact owns a different responsibility;
- no replacement/capability abstraction was introduced.

## 9. Efficiency review

Run-02 already meets the roughly 5k always-loaded target and is smaller than Run-01.

Correctness comes first. Once correctness is established:

- remove only demonstrably redundant routing/description prose;
- keep the single decision register concise;
- do not increase always-loaded surface without a concrete reliability/policy reason;
- do not add files to make the taxonomy visually symmetric;
- do not create a second optimization cycle after the mandatory audit is clean.

If a correctness fix increases size, document the cost and why it is justified.

## 10. Primary substantive audit

After repairs, audit the actual final files in `output/template/`.

Cover:

1. all 194 inventory policies plus GOV-017/GOV-018;
2. authoritative owner;
3. trigger role;
4. minimum scope;
5. semantic strength/conditions;
6. duplication/restatement;
7. V2 technique preservation review;
8. Kind/Scope assignment and mechanism;
9. Kind conformance direction and routing exceptions;
10. DEC register / `Details in` / `Affects` integrity;
11. STD/KNW/WF responsibility boundaries;
12. hook/root/worktree/failure/encoding behavior;
13. dependency/reference/Git routing;
14. actual-state post-change matrix;
15. Stop material-state behavior;
16. internal references/imports;
17. Windows/nested-cwd/worktree behavior;
18. research metadata / English-only hygiene;
19. always-loaded surface and justified complexity;
20. standalone output.

Repair every concrete defect found.

## 11. Confirmation and bounded convergence

After the primary audit and repairs, run **one complete cumulative confirmation audit** over the final template.

If the confirmation audit finds a concrete template defect:

1. repair it;
2. rerun directly affected tests;
3. rerun the complete confirmation audit because the template changed.

When one complete confirmation audit finds **zero concrete template defects**:

1. update `output/REFINEMENT_REPORT.md`;
2. record one final tree hash;
3. remove `output/.work/`;
4. verify `output/` contains only `template/` and `REFINEMENT_REPORT.md`;
5. **STOP IMMEDIATELY**.

A clean confirmation result is sufficient evidence of convergence under this protocol.

Do **not** then:

- ask whether the tests themselves need mutation analysis;
- restore deleted test tooling from transcript;
- build an audit-of-audit;
- rerun the entire baseline repeatedly;
- repeat hashes for reassurance;
- perform live hook-engine relocation experiments;
- expand the supported shell/Git matrix without a concrete failed documented requirement;
- continue because more evidence might be narratively stronger.

## 12. Strict promotion gate

Promote only if all are true:

- D1-D11 repaired;
- D12 completed and any real V2 gap repaired;
- D13 completed without unnecessary expansion;
- all 194 policies + GOV-017/GOV-018 represented;
- owner regressions = 0;
- trigger-role deltas = 0;
- minimum-scope misses = 0;
- unresolved broken references = 0;
- K0 identity unchanged;
- exactly one DEC register remains authoritative;
- Kind still determines mechanism/loading;
- Kind conformance direction is mechanically enforced;
- Git policy and deterministic Git enforcement agree on the documented supported surface;
- active-worktree, successful-shell, failed-shell, first/later HEAD, delete/move, encoding, and Stop cases pass;
- no checker was weakened merely to achieve PASS;
- complexity growth is justified by a concrete correctness/maintainability gain.

If a proposed edit produces a trade-off with no demonstrated net improvement, revert it.

**A tie is not an improvement.**

## 13. Deliverables

Produce only:

```text
output/
├── template/
└── REFINEMENT_REPORT.md
```

`REFINEMENT_REPORT.md` must include:

- final status: `STRICTLY_BETTER`, `NOT_PROMOTED`, or `BLOCKED`;
- selected baseline provenance;
- D1-D11 disposition with evidence;
- D12 V2-fidelity review result;
- D13 efficiency review result;
- files added/removed/changed;
- policy/invariant coverage;
- owner regression count;
- trigger-role delta count;
- minimum-scope miss count;
- broken-reference count;
- K0 structural result, including Kind dependency-direction fixtures;
- decision register / `Affects` result;
- dependency/reference/Git classifier summary;
- successful/failed shell actual-state matrix summary;
- worktree/nested-cwd/encoding/Stop results;
- before/after always-loaded estimate;
- before/after runtime file count;
- material V2 technique restored or intentionally omitted;
- primary-audit result;
- cumulative confirmation-audit result;
- final tree hash;
- explicit explanation of why the result is strictly better than the immutable baseline.

Do not claim `STRICTLY_BETTER` unless the strict promotion gate actually passes.
