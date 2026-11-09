# Iteration 005 / 5.3 / M1 controlled refinement task

## 1. Mission

Refine the selected **M1 / Run-02** template into a demonstrably better implementation of the **same M1 architecture**.

The immutable baseline is `baseline/template/`. The frozen architecture contract is `CANDIDATE.md`. The frozen policy/source corpus is `source/`. The independent audit findings are under `audit/`.

You are not redesigning M1. You are repairing and normalizing one M1 implementation so that later benchmarks compare architectures rather than accidental generation defects.

## 2. Output boundary

- Do not edit `baseline/`, `source/`, `audit/`, `CANDIDATE.md`, `README.md`, `PROVENANCE.json`, `REFINEMENT_TASK.md`, or `GOAL_PROMPT.txt`.
- Start by copying `baseline/template/` exactly to `output/template/`.
- Edit only `output/template/` plus the required `output/REFINEMENT_REPORT.md` and temporary material under `output/.work/`.
- Remove `output/.work/` before completion.
- Do not read parent or sibling candidate directories. Everything needed is inside this M1 workspace.

## 3. Binding inputs and priority

Read completely before making changes:

1. `REFINEMENT_TASK.md`;
2. `CANDIDATE.md`;
3. `audit/DEFECT_DOSSIER.md`;
4. `audit/BASELINE_SELECTION.md`;
5. `audit/RUN_COMPARISON.md`;
6. `audit/RUN3_DECISION.md`;
7. `audit/EXTERNAL_MECHANICS_NOTES.md`;
8. `source/inventory.json`;
9. `source/shared-research-invariants.json`;
10. the complete `source/v2-baseline/` tree;
11. the complete immutable `baseline/template/` and `baseline/GENERATION_REPORT.md`.

Conflict order:

- frozen policy/source requirements and `CANDIDATE.md` identity are binding;
- this refinement task and confirmed audit defects specify required repairs;
- the old generated report is evidence, not authority;
- do not weaken a source/candidate rule to make the baseline easier to pass.

## 4. Architecture identity that must not change

The result must remain recognizably **M1 = M + exactly four replaceable capability slots**.

Required slots:

1. `architecture/clean-architecture` — required frame;
2. `persistence/ef-core` — required leaf, provider `sqlserver`;
3. `backend-testing/nunit` — required leaf;
4. `frontend/angular` — optional leaf.

Preserve:

- static composition;
- frame/leaf rule: **placement belongs to the frame; technique belongs to the leaf**;
- flat M-style topical rules outside capability metadata;
- V2 lineage for non-capability content;
- one authoritative owner per normative policy;
- role/facet references outside implementation-owned content;
- maintainer-only contracts/manifests except when capability maintenance needs them.

Forbidden drift:

- no new capability slots;
- no dynamic plugin discovery or runtime selection;
- no Stability-first level hierarchy or `Level:` classification;
- no Kinds × Scopes organization or `Kind:` taxonomy;
- no K/L-style decision meta-architecture;
- no global technology-neutral rewrite of unrelated M content;
- no gratuitous directory/file layer added only for symmetry.

## 5. Mandatory confirmed repairs

Every confirmed defect D1–D8 in `audit/DEFECT_DOSSIER.md` must be fixed. Do not mark a defect resolved from prose alone; add deterministic evidence/tests where technically possible.

### 5.1 D1 — active-worktree correctness

Implement a clear two-root model:

- **launcher root** locates the checked-in hook scripts;
- **active root** is derived from hook-input `cwd` and represents the repository/worktree Claude is currently operating in.

Parse hook JSON before choosing the active root. Repository reads/writes/checks, path containment, manifest discovery, architecture checks, Git status, changed-file enumeration, stop-hook state, and capability enforcement must act on the active root.

Do not silently redirect a worktree operation back to the original checkout.

Create tests that use an actual temporary Git worktree inside `output/.work/` and prove:

- invalid manifest in worktree is detected;
- equivalent valid worktree state passes;
- nested cwd inside worktree still maps to the worktree root;
- main-checkout state does not mask or substitute for worktree state;
- path-escape protections remain intact.

### 5.2 D2 + D5 — robust modern hook launch + checker support

Prefer current Claude Code exec form for project-path hooks:

```json
{
  "type": "command",
  "command": "node",
  "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.js"]
}
```

Use an equivalently robust solution only if you can demonstrate it is strictly better for this template.

Update `check-instructions` so it validates the actual selected hook schema rather than hardcoding the old shell-form string. It must verify expected event/matcher coverage, script existence, argument/path structure, and critical failure behavior.

Test launch behavior with:

- project-root cwd;
- nested cwd;
- a path containing spaces;
- active Git worktree;
- Windows-compatible invocation assumptions.

### 5.3 D3 — dependency command parsing

Replace regex assumptions that require the package-manager subcommand immediately after executable name.

Correctly classify normal package mutations with global options before the subcommand, including representative forms for:

- npm `--prefix`, `--workspace`;
- pnpm `--dir`, `--filter`;
- yarn `--cwd`;
- ordinary install/add/remove/update forms;
- force/legacy-peer-deps policy;
- checked/approved markers only when they genuinely correspond to the same command intent.

Use table-driven tests with both positive and negative cases. Avoid false positives on ordinary non-mutating commands. Keep PreToolUse classification and PostToolUse `changesManifests` behavior consistent by sharing parsing/classification logic where practical.

### 5.4 D4 — project-reference mutations before execution

Detect `dotnet add/remove ... reference ...` before mutation. Route it to the existing architecture/project-reference decision owner, not falsely to the NuGet-package workflow.

The pre-check must make clear what the model has to read/do before reissuing the command. The post-check must validate resulting architecture/project references.

Test add/remove with explicit project operands and currently supported shorthand forms.

### 5.5 D6 — root-safe manual checker execution

Audit every workflow/MAP/instruction that runs `.claude/scripts/*` manually. It must remain correct after Claude runs `cd` and inside an active worktree.

Prefer a concise convention that resolves or moves to the active repository/worktree root rather than duplicating absolute paths everywhere.

### 5.6 D7 — Stop-hook state identity

Replace the `{files,messages}`-only fingerprint with a deterministic identity of the relevant actual change state. A changed content state using the same file names must be eligible to trigger a new reminder; an unchanged state must not loop.

Keep state scoped to the active Git worktree/repository. `stop_hook_active` remains part of the loop-prevention design.

Add tests for:

- unchanged state repeated stop -> no duplicate loop;
- same file set with modified content -> reminder can re-trigger;
- two worktrees with equivalent file names -> no cross-worktree suppression.

### 5.7 D8 — fail closed for critical PreToolUse failure

A broken critical pre-enforcement script must not silently permit the protected mutation. Use supported fail-closed hook behavior (current Claude Code supports `onFailure: "block"`) for critical PreToolUse checks.

Do not apply fail-closed mechanically to observational/post/Stop hooks where it is ineffective or counterproductive.

Add a controlled test proving that a missing/crashing critical PreToolUse script blocks rather than allows the command.

## 6. Mandatory quality gates beyond confirmed defects

### 6.1 V2-fidelity review

R1 retained considerably more literal V2 technique/examples than R2. Treat this only as a diagnostic signal.

Systematically compare the complete V2 baseline against `output/template/` after the repairs. For every materially useful section/example/technique:

- preserve it if still applicable;
- restore it if R2 dropped useful semantics or operational technique;
- leave it condensed if the same meaning is already present;
- do not restore duplicate normative restatements or research-only material.

Record material restorations in the report.

### 6.2 Capability coupling review

Review R2 persistence's declared `binds` to the architecture frame. Replace avoidable concrete frame names with stable architecture-role vocabulary where that improves true substitutability without making commands/examples vague or unusable.

Do **not** force `binds` to zero. Keep and explain explicit coupling that is genuinely required.

### 6.3 Complexity/context discipline

The baseline is already slightly above the rough 5k always-loaded target (~5.57k) but within the TASK's reliability-first rule.

- Do not move frozen always-trigger policy out of always-loaded context to reduce tokens.
- Do not add new meta layers for convenience.
- Do not increase always-loaded context, total files, or maintenance concepts unless a mandatory repair needs it and the report explains the tradeoff.
- Opportunistic simplification is allowed only when it is provably semantics-preserving.

## 7. Full regression audit

After repairs, perform a primary audit over the actual output files. At minimum verify:

- all 194 inventory policies and both shared invariants are preserved;
- trigger-role deltas = 0;
- minimum-scope gaps = 0;
- semantic strength/conditions are not weakened;
- one authoritative normative owner; no accidental restatement copies;
- complete V2 preservation review as defined above;
- exactly four capability slots and only one selected implementation per required slot / zero-or-one for optional frontend;
- contracts/manifests/facets/selection agree;
- no unselected implementation enters runtime;
- implementation leak checks pass;
- frame/leaf dependency direction and declared `binds` are coherent;
- all internal references resolve;
- rule path coverage is correct;
- Windows-compatible hook/checker behavior;
- actual active-worktree behavior and nested-cwd behavior;
- command-routing test matrix;
- Stop-hook no-loop + changed-state re-trigger behavior;
- output contains no research labels/benchmark metadata;
- all technical content is English;
- `SPECIFICATION.md` remains a product input;
- output is standalone under `output/template/`.

Repair every concrete defect found, then run one complete confirmation audit. Repeat only if that confirmation finds a concrete template defect. A zero-defect confirmation is the convergence point.

## 8. Strict promotion comparison against the immutable baseline

After convergence, compare `output/template/` with `baseline/template/`.

The refined version may be promoted only if it is **STRICTLY_BETTER**. This requires all of the following:

1. every confirmed D1–D8 defect is fixed with evidence;
2. no new binding defect is introduced;
3. policy coverage/strength/trigger/scope are no worse;
4. M1 identity is unchanged;
5. V2 useful technique/detail is no worse;
6. broken references remain zero;
7. active-worktree, nested-cwd, Windows, dependency-routing, and failure-mode behavior is strictly stronger;
8. any increase in context/files/complexity is justified by a necessary reliability repair and is proportionate;
9. no baseline behavior is lost merely to satisfy a checker;
10. the result is at least as understandable and maintainable for a human.

A **tie is not an improvement**. Cosmetic churn is not an improvement. Rewriting wording without fixing a defect is not an improvement.

If a proposed edit does not survive this gate, revert that edit and keep the baseline behavior.

## 9. Required report

Create `output/REFINEMENT_REPORT.md` containing:

- final status: `STRICTLY_BETTER`, `NOT_PROMOTED`, or `BLOCKED`;
- baseline identity and hashes;
- concise old-vs-new tree/context metrics;
- D1–D8 table: defect, fix, test evidence, result;
- Q1–Q3 review results;
- policy/trigger/scope/semantic audit results;
- capability identity/conformance results;
- worktree/nested-cwd/Windows test matrix;
- dependency-command test matrix;
- Stop-hook state tests;
- V2 material restorations, if any;
- intentional baseline behavior retained;
- any rejected refinement ideas and why;
- final zero-defect confirmation result;
- explicit explanation of why the promoted output is strictly better rather than merely different.

Do not self-approve from the generated checker alone. Treat generated checkers as evidence that must agree with direct inspection and behavioral tests.

## 10. Completion condition

The intended result is `STRICTLY_BETTER`. Work autonomously through repair/audit cycles until every resolvable defect is fixed and the promotion gate passes.

Use `BLOCKED` only for a genuine contradiction or missing required source that cannot be resolved from this workspace. Do not use `NOT_PROMOTED` merely because a repair is difficult; first attempt to repair all confirmed defects. `NOT_PROMOTED` is appropriate only if the best valid repair cannot be proven better than the immutable baseline without regression.

Once the full confirmation audit has zero concrete defects and the strict promotion comparison passes, remove `output/.work/`, finalize `REFINEMENT_REPORT.md`, and stop.
