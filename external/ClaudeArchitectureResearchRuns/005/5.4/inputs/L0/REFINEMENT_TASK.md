# L0 controlled-refinement task — Iteration 005 / 5.3

## 1. Goal

Produce a **strictly better implementation of Candidate L0** from the immutable selected baseline.

This is not a new candidate-generation run and not an architecture redesign. The goal is to remove confirmed implementation defects so later benchmarks compare L0's architecture rather than accidental generation quality.

This task is intentionally **bounded**. Repair the documented defect surface, run the documented regression matrix, perform one complete confirmation audit, write the report, clean temporary evidence, and stop. Do not turn a clean result into an audit-of-audit, mutation-testing campaign, live-hook-engine experiment, or open-ended shell fuzzing exercise.

## 2. Inputs and boundaries

Read completely before editing:

- `CANDIDATE.md`;
- `audit/DEFECT_DOSSIER.md`;
- `audit/BASELINE_SELECTION.md`;
- `audit/RUN_COMPARISON.md`;
- `audit/EXTERNAL_MECHANICS_NOTES.md`;
- `source/inventory.json`;
- `source/shared-research-invariants.json`;
- the complete `source/v2-baseline/` tree;
- `baseline/TASK.md`;
- the complete immutable `baseline/template/`.

Do not modify `baseline/`, `source/`, `audit/`, `CANDIDATE.md`, or this task.

Write only under `output/`.

Use `output/.work/` for temporary audit/test material. Create the test harness once, keep it until the report and final confirmation are complete, and remove it only at the very end. **Do not delete it early and reconstruct it from transcript/session history.**

Do not read sibling architecture/run workspaces, network material, external session/transcript storage, or any source outside this L0 refinement workspace.

## 3. Establish the working copy

Before changing content:

1. verify `output/` is empty except for any explicitly pre-created placeholder directory;
2. copy `baseline/template/` exactly to `output/template/`;
3. verify the initial copy is byte-identical to the baseline;
4. record one initial tree hash;
5. make all proposed template changes only in `output/template/`.

The immutable comparison point is L0 Run-02.

Do not repeatedly re-hash the unchanged tree merely to obtain stronger evidence. One initial hash and one final hash are sufficient unless a concrete integrity problem appears.

## 4. Architecture identity that must not change

The refined template must remain L0:

- primary organization is `0 Core -> 1 Architecture -> 2 Technology -> 3 Project`;
- rules remain level-first;
- a conformance dependency points only to the same or more stable level;
- Levels 0/1 remain technology-neutral under the candidate's fixed-platform interpretation;
- technologies remain embedded, with no replacement-slot system;
- architecture and project decisions remain stratified and separately always-loaded;
- no `Kind:` taxonomy or Kinds × Scopes organization;
- no capability contracts, manifests, slot selection, generic facet lookup, Feature or Task levels;
- product/task inputs remain inputs, not instruction layers.

Do not "solve" an enforcement defect by weakening L0's constraints or turning L0 into M, L1, K0, or K1.

## 5. Mandatory confirmed defect set

Repair **every mandatory item in `audit/DEFECT_DOSSIER.md` (D1-D12)**.

A claimed repair is not sufficient. Each defect needs behavioral evidence against the final files. Demonstrate baseline failure only once where cheap and useful; do **not** repeatedly rerun the entire full suite against baseline after every repair.

### 5.1 Hook/root model

The final design must distinguish:

1. **launcher/config root** — stable location used to start the hook script;
2. **active repository/worktree root** — repository Claude is actually operating in, resolved from hook input `cwd` and Git when needed.

Do not use `${CLAUDE_PROJECT_DIR}` as a substitute for the active worktree root.

Use a current Windows-safe hook configuration. Prefer exec-form `command` + `args` for Node hooks with path placeholders. Critical PreToolUse policy enforcement must fail closed with supported failure semantics.

### 5.2 Actual-state shell validation

Command-text classification is useful for **pre-execution routing**, but it is not sufficient for post-change validation.

For Bash/PowerShell post events, validate the **actual resulting active-worktree state** so relevant manifest/project mutations cannot bypass checks merely because the command text was unfamiliar.

The bounded supported surface is:

- successful shell calls (`PostToolUse`);
- failed shell calls with partial side effects (`PostToolUseFailure`);
- fresh tracking state;
- later tracking state;
- first and later HEAD transitions;
- same-file rewrites;
- tracked manifest additions, deletions, moves/renames when observable by the state model;
- root cwd, nested cwd, linked worktree, nested worktree cwd;
- Bash and PowerShell.

Prefer one bounded per-worktree snapshot/state mechanism over a full repository scan after every unrelated shell command. The first shell observation in a worktree may perform one full manifest validation/snapshot if needed to establish a safe baseline.

State for one worktree must not contaminate another worktree. Skipped directories such as `node_modules`, build output, nested repositories/worktrees, or other deliberately excluded areas must not be falsely reported later as removed tracked manifests.

### 5.3 Dependency-routing behavior

Before a mutating command executes, correctly identify at least:

- `dotnet add/remove [project] package ...` and supported equivalent package forms;
- `dotnet add/remove [project] reference ...` and supported equivalent reference forms;
- npm/pnpm/yarn dependency mutations;
- npm/pnpm/yarn global options that take values before the subcommand (`--prefix`, `--workspace`, `--dir`, `--cwd`, and equivalent supported forms);
- peer-dependency bypass flags such as `--force`, `-f`, `--legacy-peer-deps`, regardless of reasonable placement.

Restore-only commands without dependency mutation must not be falsely treated as package additions.

Project-reference graph mutation is Reserved. Do not allow it to become a silent post-hoc check.

## 6. Required behavioral regression matrix

Create controlled sandboxes only under `output/.work/`. Cap Git upward discovery from the first Git test.

Do not attempt to move the already-running Claude Desktop/Code session into `output/template/` or a sandbox merely to observe the real hook engine. Hook configuration is session-scoped and such relocation is not an acceptance requirement. **Controlled process-level execution of the generated hook scripts/configuration plus the documented host semantics is sufficient for this refinement.**

At minimum test:

### 6.1 Launch/root/worktree

- project-root cwd;
- nested cwd one or more directories below root;
- real linked Git worktree where launcher root and active root differ;
- nested cwd inside that worktree;
- paths containing spaces;
- product input edit routes to the active worktree, not the main checkout;
- manifest scan and Stop co-change scan operate on active worktree content;
- no accidental inspection/mutation of sibling/main checkout when worktree is active.

### 6.2 Hook input and Windows encoding

- normal JSON stdin;
- UTF-8 BOM-prefixed JSON stdin;
- empty/malformed required input has the intended visible/fail-closed behavior;
- exact generated settings `command`/`args` shape;
- missing/crashing/timed-out critical PreToolUse demonstrates fail-closed behavior;
- no POSIX-only launcher assumption;
- manifest/project readers correctly handle the encodings the Windows workflow can create, including UTF-8 and BOM-tagged UTF-16LE/UTF-16BE where applicable;
- malformed/odd-length encoded manifest input fails visibly rather than crashing the hook process unpredictably.

### 6.3 Dependency command matrix

Positive and negative cases across:

- npm;
- pnpm;
- yarn;
- dotnet package commands;
- dotnet project-reference commands;
- global-option prefixes and option values;
- force/legacy-peer bypass flags;
- restore-only commands.

### 6.4 Shell actual-state matrix

Use representative tracked `.csproj`, `Directory.Packages.props`, and `package.json` cases.

Prove:

- successful Bash mutation is detected;
- successful PowerShell mutation is detected;
- failed Bash mutation with partial side effects is detected through `PostToolUseFailure`;
- failed PowerShell mutation with partial side effects is detected through `PostToolUseFailure`;
- failed shell command that changes no relevant state stays quiet;
- arbitrary shell-driven manifest mutation is detected even when command text is not a known dependency command;
- fresh state + first shell/HEAD transition to an invalid committed manifest is detected;
- later HEAD transition is detected;
- same-path manifest rewrite is detected;
- tracked manifest deletion is not silently ignored;
- rename/move does not disappear silently;
- an unrelated shell command after unchanged state does not cause noisy repeated full validation;
- deliberately skipped paths do not create false "removed manifest" findings.

### 6.5 Stop behavior

- initial relevant production change produces the expected reminder;
- `stop_hook_active` prevents loops;
- unchanged relevant working-tree state does not repeat endlessly;
- materially changing the same already-modified file can produce a fresh reminder while the obligation still applies;
- subsequent unchanged repeat is silent.

### 6.6 Structure/checker mutation cases

Use a **small bounded set** of negative fixtures only to prove the structure checker is not blind to the properties it claims to enforce. At minimum:

- remove required PreToolUse fail-closed configuration -> checker fails;
- remove required `PostToolUseFailure` registration -> checker fails;
- introduce a Level 0/1 disallowed concrete technology -> checker fails;
- introduce a reverse level dependency -> checker fails;
- break a required internal reference -> checker fails.

This is not permission to build a mutation-testing framework. Do not run mutation analysis of the test harness or an audit-of-audit campaign.

## 7. Structural/policy regression audit

After repairs, perform one complete substantive audit of the actual `output/template/`.

Verify at minimum:

- 194 inventory policies + 2 shared invariants all retain exactly one authoritative owner;
- trigger-role delta count = 0;
- minimum-scope misses = 0;
- normative strength and conditions are neither weakened nor accidentally strengthened;
- no material V2 technique/example needed for correct use was lost;
- no new duplicate/restated normative ownership;
- all Level headers and directories conform to L0;
- no reverse conformance dependency or dependency cycle;
- Levels 0/1 contain no disallowed concrete technologies;
- architecture/project decision summaries remain separate imports;
- all internal paths, skill names, imports, section pointers, and private references resolve;
- hook/checker behavior matches documentation and generated instructions;
- `SPECIFICATION.md` stays empty unless the baseline already contained product input (it does not);
- no research metadata, run labels, workspace paths, or non-English runtime prose;
- no dependency on files outside `output/template/`.

Update the instruction-structure checker so it validates the **new correct enforcement configuration and behavior**, including exec-form/path/failure-event/fail-closed requirements, rather than preserving the baseline's obsolete serialization assumptions.

## 8. Quality reviews beyond mandatory fixes

These reviews are required **once**, but changes are optional unless they reveal a concrete defect.

### 8.1 Always-loaded efficiency

Run-02 is around 5.0k chars/4 tokens; Run-01 demonstrated that L0 can be around 4.4k. Look for redundant skill/agent descriptions, duplicate routing prose, or verbose imports.

Reduce cost only when the same trigger reliability, policy ownership, decision content, and human usability are preserved. Do not move policies to a weaker trigger merely to save tokens.

### 8.2 V2 preservation

Use the frozen V2 baseline, not Run-01 output, as the source. Systematically review unmatched sections/headings/technique. Restore useful detail only if it materially improves correctness or maintenance. Do not restore prose merely to increase textual similarity.

### 8.3 Structural economy

Run-02 has 71 runtime files. Do not add a file/layer/helper unless ownership, trigger, enforcement reliability, or maintainability clearly justifies it. Prefer repairing the existing enforcement surface over growing a framework around it.

A quality-review observation that produces no concrete defect does **not** reopen the repair loop.

## 9. Bounded verification and convergence protocol

Use this exact flow:

1. establish the working copy and one baseline evidence snapshot;
2. implement the mandatory repairs;
3. run focused tests while repairing;
4. run the complete required behavioral/regression matrix on the final candidate;
5. perform **one complete substantive confirmation audit**;
6. repair any concrete defect that audit finds;
7. because the template changed, rerun the affected tests and then the confirmation audit once more;
8. when one complete confirmation audit finds zero concrete template defects, finalize the report, clean `output/.work/`, and stop.

Important stop rules:

- Do not start another whole audit because the report wording changed but the template did not.
- Do not verify the verifier, audit the audit, or prove that every test can detect an artificial mutant after the required bounded negative fixtures pass.
- Do not perform mutation analysis of test infrastructure.
- Do not reconstruct deleted test tooling from transcript/session logs.
- Do not repeat full baseline suites after each repair; baseline is evidence, not the candidate under promotion.
- Do not require live observation of the generated hooks in the current already-running Desktop session.
- Do not start open-ended shell syntax fuzzing after the documented matrix passes.
- Do not repeat hashes solely to obtain stronger narrative evidence.
- A harness/test defect is not automatically a template defect. Fix the harness, rerun the affected evidence, and continue the bounded protocol.

## 10. Strict promotion gate

The result may be promoted only if it is **demonstrably strictly better** than `baseline/template/`.

All of the following are required:

1. every mandatory D1-D12 defect is fixed;
2. no new binding defect is introduced;
3. candidate identity remains L0;
4. policy coverage, strength, trigger roles, and scopes are not worse;
5. V2 preservation is not worse in substance;
6. all references resolve;
7. deterministic enforcement is more reliable under nested cwd/worktree/Windows/success/failure shell conditions;
8. checker coverage is not weakened to hide defects;
9. complexity/context/file-count regressions are justified by concrete reliability value;
10. the complete documented behavioral matrix passes against the final files.

**A tie is not an improvement. Cosmetic churn is not an improvement.**

If an attempted change is neutral, subjective, or creates a trade-off without a clear net gain, revert that change and keep the baseline behavior.

## 11. Required report

Write `output/REFINEMENT_REPORT.md` containing:

- final status: `STRICTLY_BETTER`, `NOT_PROMOTED`, or `BLOCKED`;
- baseline tree SHA-256 and final tree SHA-256;
- exact files changed;
- D1-D12 disposition with evidence for each;
- behavioral regression matrix summary;
- policy/trigger/scope/neutrality/dependency/reference audit results;
- Level 0/1 neutrality negative/positive test result;
- success/failure shell-event coverage result;
- worktree/nested-cwd/Windows/BOM/UTF-16 results;
- Stop-state regression result;
- always-loaded estimate before/after;
- runtime file count and byte count before/after;
- V2-fidelity review summary;
- attempted changes reverted because they were not demonstrably better;
- any remaining known limitation.

Generate report tables from final evidence where practical, but do not launch a second verification campaign merely to validate report prose. Report-only edits after the final frozen template require only a lightweight consistency check, not another full template audit.

Remove `output/.work/` only after the report and final confirmation are complete.

The intended outcome is `STRICTLY_BETTER`. Do not lower a requirement to obtain that label.

## 12. Final stop condition

The task is finished when:

- the final `output/template/` passes the documented matrix;
- one complete confirmation audit finds zero concrete template defects;
- `output/REFINEMENT_REPORT.md` is complete and internally consistent;
- `output/.work/` is removed;
- `output/` contains only the deliverable template and report.

At that point **stop immediately**. Do not create new tests, mutants, audits, proof layers, or live-session experiments unless a concrete failed gate identified a real template defect before convergence.
