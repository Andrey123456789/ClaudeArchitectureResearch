# L1-Restart — controlled refinement from Run-02 (Phase 5.3)

## 0. Authority, purpose and termination

Produce **one strictly better L1 candidate** from the immutable, selected **L1 Run-02** baseline. This is a restart of the refinement implementation, **not** iteration 9, a new architecture, or a continuation of the iteration-8 checker. Make one integrated correction of documented defects and test it against a finite, frozen contract. Avoid a sequence of ever-broader checker patches.

This file supersedes the original root `REFINEMENT_TASK.md` **only in execution ordering, strict P4/P6 interpretation, the bounded test matrix and stopping protocol**. The original `CANDIDATE.md`, `audit/DEFECT_DOSSIER.md`, source inventory, common invariants and baseline design remain authoritative. There is **no** permission to delete/redefine policies, broaden an implementation exception, downgrade a defect, invent a new candidate, or rewrite success criteria after testing.

Terminal status is one of `STRICTLY_BETTER`, `NOT_PROMOTED`, `BLOCKED`. All three are legitimate stopping outcomes. A dirty gate does not authorize unlimited audits. A hook's objection does not authorize repeated self-justification; preserve the truthful result and stop/request owner intervention.

## 1. Starting point: pristine and isolated

Required working folder: an **independent L1-Restart copy** containing the original L1 root metadata, `baseline/`, `source/`, `audit/`, original `CANDIDATE.md` and original `REFINEMENT_TASK.md`, plus these two Restart prompt files. The original L1 iterative workspace must remain untouched. Never inspect/copy implementations from L1 refinement iterations 2–8, L0, M, M1, K0, K1, sibling directories, transcripts or external storage. Lessons relevant to this task are already encoded here.

Read in order:

1. This entire task, `CANDIDATE.md`, `audit/DEFECT_DOSSIER.md` (D1–D17).
2. `audit/BASELINE_SELECTION.md`, `audit/RUN_COMPARISON.md`, `audit/RUN3_DECISION.md`, `audit/EXTERNAL_MECHANICS_NOTES.md`, `audit/evidence/INDEPENDENT_TESTS.md`.
3. `source/inventory.json`, `source/shared-research-invariants.json`, relevant complete `source/v2-baseline/`, and `baseline/{TASK.md,CANDIDATE.md,GENERATION_REPORT.md}`; inspect all original `baseline/template/` files for the source-to-output review.
4. Original `REFINEMENT_TASK.md` for preservation of D1–D17 and original matrix; this Restart contract settles any verification/stop conflicts.

Before editing:

- Assert `output/` is empty/absent (an empty placeholder is fine). **If it holds previous work, stop `BLOCKED`; never silently delete, merge or overwrite.**
- Verify immutable provenance (`MANIFEST.sha256` where available) and initial baseline file inventory; selected Run-02 `baseline/template/` has **85 files**. Do not assume the later 86-file output is the baseline.
- Copy the baseline tree **byte-for-byte** to `output/template/`, verify identity and record one baseline tree hash with a documented deterministic algorithm. Work only under `output/` thereafter.
- `output/.work/` is the sole disposable test/sandbox folder. Create the finite shared harness once, retain it through tests, final confirmation and report, then delete it **last**. Do not reconstruct deleted harness files from dialogue/history.

Immutable: `baseline/`, `source/`, `audit/`, `CANDIDATE.md`, original root tasks and both Restart prompt files. Do not update `MANIFEST.sha256` to disguise changed immutable inputs. Only `output/template/` and `output/REFINEMENT_REPORT.md` are persistent outputs.

## 2. L1 identity and fidelity: non-negotiable

Preserve **0 Core → 1 Architecture → 2 Technology → 3 Project** as the primary stability-first organization: level-first rules, correct Level header/path, allowed same-or-more-stable conformance direction, L-style stratified architecture/project decisions. Level 0/1 own neutral constraints and role/boundary placement; Level 2 / appropriate module facets own concrete techniques; Level 3 owns selected project-specific choices. Do **not** add a K taxonomy/register, M flattening, fifth slot, new instruction level, plugin discovery, meta-framework or another architecture family.

Four **static capability slots only**:

| Slot | Obligation | Selected implementation |
|---|---|---|
| architecture | required **frame** | `clean-architecture` |
| persistence | required **leaf** | `ef-core`, provider `sqlserver` |
| backend-testing | required **leaf** | `nunit` |
| frontend | optional **leaf** (selected initially) | `angular` |

Frame owns layout/placement and architecture-specific patterns; leaves own concrete persistence/test/frontend techniques. Preserve stable facet/role names, selected-only composition, manifests/contracts/ownership, implementation leakage checks and substantive required `binds:` for genuine frame-specific integration. A mutation which deletes the same required binding from **both** manifest and contract must not become a false PASS. Clearing optional frontend in a **test copy** must yield a coherent zero-frontend configuration; retain Angular in the actual output.

Policy gate: reconcile **all 194 inventory records plus GOV-017 and GOV-018 (196 total)** using source-to-output evidence. Zero omitted policies, duplicate authoritative owners, owner changes, `trigger_class` deltas, minimum-scope misses, semantic dilution, missing condition/strength or broken references. A checker claiming 196 is not alone an audit. `SPECIFICATION.md` remains an input, not a new instruction layer. Runtime instruction/code language is English; no research metadata leaks into runtime.

## 3. Strict P4 with an explicit, finite P6 boundary — freeze BEFORE editing

### 3.1 The invariant

Level-0/1 may **refer** to real Level-2+ technique skills but may **not prescribe a concrete non-platform implementation**. This includes selecting, assigning, requiring, defaulting, preferring or otherwise deciding a named technology. Fixed-platform vocabulary and stable architectural roles remain allowed only within the candidate's genuinely predefined boundary; never enlarge that boundary merely to legalize known defects (`IExceptionHandler`, `WebApplicationFactory`, `IActionResult`, ASP.NET Core implementation details, etc.). Move specific technique/binding to owning Level 2/facet and keep neutral policy/role placement at Level 0/1.

**Masking/exempting a technology token is exceptional.** It requires (i) an actual resolved target in permitted Level-2+ skills, (ii) positive recognition of a **pure, non-normative reference/routing construction**, and (iii) neutral directly governing context. Unknown labels, ambiguous governor or referent, and norms that select the referred implementation **do not get the exemption**. Then the existing neutrality rule sees the technology token. Do not rely on an ever-growing vocabulary of forbidden verbs; do not replace a narrow deterministic grammar with general-purpose English or arbitrary Markdown/NLP parsing.

### 3.2 Supported structural boundary

Support these **six existing bounded forms**, within a single immediate governing region: (1) same-line statement, (2) heading governing immediate content, (3) parent/nested list item, (4) list-item continuation, (5) colon lead-in and immediate following content, (6) same-paragraph wrapped continuation. Additionally, process **immediate sibling items** under a common directly governing heading/parent when one explicitly binds a requirement to the sole identified technique (e.g. `this technique`, `the above technique`, `the following technique`). Do not resolve remote pronouns, infer relationships across unrelated sections, or invent an unlimited natural-language parser.

Sibling count/position must not change a pointer's actual governor: a neutral sibling cannot legalize a forbidden selection. A normative sibling such as `Must run unit tests` without an explicit relation to the technique must not contaminate an otherwise valid pure pointer. A sibling such as `Must use this technique for deployment` **does** bind it and forbids masking if the antecedent is unique. More than one possible antecedent is ambiguous: **no exemption**, not arbitrary selection. `;`-separated independent routing clauses and a self-contained, genuinely non-normative parenthesized routing aside have their established bounded independence.

**P6 is a conditional formatting-invariance rule**, not a blanket authorization for all previously successful synthetic fixtures. Reformatting genuinely pure pointers **inside an explicitly neutral recognized governing context** must preserve PASS; reformatting a normative selection must preserve FAIL. Placement under an ambiguous generic governance heading such as `Engineering Discipline` is **not** entitled to PASS simply because another sibling is present. Earlier permissive checker results are diagnostic history, not immutable acceptance requirements. This resolves the P4-versus-P6 conflict **before implementation**.

For example, if `- Technique: \`docker\`.` in an `Engineering Discipline` rule list cannot be positively established as a pure, local, non-normative reference, classify it FAIL regardless of sibling count. A separately labeled neutral technique-reference section or a self-contained pointer with provably neutral local context is a legitimate PASS. This does **not** authorize weakening or deleting the substantive rule list itself. Keep genuine template pointers (e.g. `development-workflow` parenthesized aside, `code-review` routing map and `build-fix` technique footnote if present in the final template) where truly pure; if a normative content change makes a baseline pointer unsafe, relocate its technique selection to Level 2 instead of suppressing the error.

### 3.3 Locked discrimination matrix (real final checker; both L0 and L1)

Build ONE finite fixture matrix before the fix. Run each against an **independently reset temporary template copy** with intact metadata in both `.claude/rules/0-core/engineering.md` and `.claude/rules/1-architecture/frame/boundaries.md` (adapt placement while preserving intended governor). A FAIL counts **only** if the actual neutrality diagnostic identifies the injected Docker/Swagger technology in that eligible rule; incidental parse/reference/test failures do not qualify. A PASS means 0 violations and 0 warnings. **Fixture placement is part of the test:** insert standalone/positive controls in their own explicitly neutral context (or an independent clean reference statement), never accidentally under the existing generic `Engineering Discipline` list; put N14 specifically under that generic list. A negative must retain its normative heading/list governor. In the Markdown table, backslashes escaping inline backticks are formatting only and are NOT fixture characters. Keep the exact expected outcomes below fixed.

| ID | Input / bounded configuration | Verdict |
|---|---|---|
| N01 | `Must use \`docker\` for deployment.` | FAIL |
| N02 | `Selected deployment technology: \`docker\`.` | FAIL |
| N03 | `Selected deployment technology: Technique: \`docker\`.` | FAIL |
| N04 | `### Selected deployment technology` + `- Technique: \`docker\`.` | FAIL |
| N05 | N04 + **one/two neutral siblings**, before or after pointer | FAIL |
| N06 | `- Selected deployment technology:` + nested technique pointer + neutral sibling | FAIL |
| N07 | `### Deployment technique` + `- Technique: \`docker\`.` + `- Must use this technique for deployment.` | FAIL |
| N08 | Neutral parent + pointer + `- Must use the above technique.` | FAIL |
| N09 | Neutral parent + `- Must use the following technique.` + pointer | FAIL |
| N10 | `Technique: \`docker\`. Must use this technique.` | FAIL |
| N11 | `Chosen/Required/Default deployment technology` as governor + technique child | FAIL |
| N12 | `Selected deployment technology: Technique: \`swagger\`.` and sibling-bound obligation with Swagger | FAIL |
| N13 | `Production deployment: Technique: \`docker\`.` when no positive neutral-reference meaning is provable | FAIL |
| N14 | Generic `Engineering Discipline` parent + ambiguous technique child, with or without neutral siblings | FAIL |
| P01 | Bare `Technique: \`docker\`.` with no normative governor | PASS |
| P02 | `See technique: \`docker\`.` in explicitly neutral local context | PASS |
| P03 | `Containers -> \`docker\`.` as a standalone pure routing map entry | PASS |
| P04 | `### Deployment technique` + direct technique pointer | PASS |
| P05 | P04 + one/two genuinely unrelated neutral siblings | PASS |
| P06 | `- Deployment technique:` + nested technique pointer + neutral sibling | PASS |
| P07 | Neutral parent + pointer + `- Must run unit tests.` (unrelated duty) | PASS |
| P08 | `**CI/CD, container, or deployment change** (technique: \`ci-cd\`, \`docker\`)` as a pure parenthetical aside, with independent subsequent instructions | PASS |
| P09 | Genuine `code-review` route-map pointer (only pure technique/reference clauses) | PASS |
| P10 | Genuine trailing `Technique: \`swagger\`, \`http-api\`.` footnote in `build-fix`, where it is a pure reference | PASS |
| P11 | Identical truly neutral pointer with supported heading/list/line-wrap formatting changes | PASS |
| P12 | Legitimate `swagger` pure pointer and independent `;` routing clauses | PASS |

Retain the document's current genuine standalone references when appropriate; use the final template itself for positive controls. **Where a listed pointer is absent from the original baseline, test it as a positive synthetic case, not as an assertion about existing baseline text.**

Metamorphic invariant: adding an unrelated child or moving it above/below the pointer cannot turn a prohibited selection into PASS. Changing neutral formatting within the six supported forms must not turn a genuinely pure pointer into FAIL. Use a small fixed combination of these transforms for Docker and at least one Swagger control (no random fuzzing). Case-insensitive checks, frame-specific API-shaped identifiers and inability to legalize technology through `frame-terms`/`placement-examples` remain in scope. Do not make a negative fixture fail via unrelated corruption.

### 3.4 Honest limitation

This checker is a bounded deterministic guard, **not a proof that no English sentence anywhere can imply a technology requirement**. Report the supported formats and examples of out-of-scope semantics. Separate the mechanical check from the required independent **content audit** of the entire actual Level 0/1 output. Unsupported syntax never justifies claiming a normative technology assignment is acceptable in template content.

## 4. Repair the D1–D17 causes together

Treat this as one program with shared test surfaces, not one defect per follow-up iteration. Use `audit/DEFECT_DOSSIER.md` for exact details and the original task for the full required matrix.

### 4.1 D1–D2: content ownership + neutrality enforcement

Audit all `.claude/rules/0-core/**`, `.claude/rules/1-architecture/**`, applicable frame/role docs and other Level 0/1 instructions. Separate neutral policy/placement from specific Level-2 technique; preserve source owner/trigger/scope and accepted platform boundary. Update the checker to detect concrete framework/API/provider/test/frontend implementation leaks and P4 bypasses **without using an unlimited exception list**. Verify a technology-name leak remains a FAIL after adding labels, nested wrappers, neutral siblings, metadata entries or supported continuation text. Avoid false rejection of true framework-neutral roles.

### 4.2 D3–D5, D11–D13: launcher/root/failure/Windows as one unit

Implement stable root-aware Windows-safe hook launch with supported exec-form `command`/`args` (or evidenced equivalent). Distinguish launcher/config root from active repository/worktree determined via hook `cwd` and Git. Critical dependency/project graph **PreToolUse** fails closed with `onFailure: "block"`/documented equivalent on missing/crashing/timed-out handler and malformed mandatory input. Advisory Post and Stop remain non-blocking as designed. Instruction checker recognizes the **new** configuration, not the obsolete baseline serialization. Manual instructions run checkers from root, nested cwd and linked worktree reliably. Cover normal UTF-8 JSON, BOM JSON and supported BOM-tagged UTF-16LE/BE manifest contents; malformed/odd-length content must fail clearly, not disappear silently.

### 4.3 D6–D10: pre-routing is distinct from actual post-state

Pre-execution classify supported dotnet package/reference changes, npm/pnpm/yarn mutations, options taking a value (`--prefix`, `--workspace`, `--dir`, `--cwd`) and peer override flags regardless of reasonable location. Dotnet project-reference mutation is Reserved and **must be gated before execution**, not merely noticed afterward. Keep unrelated/restore-only commands clean.

Both successful `PostToolUse` and failed `PostToolUseFailure` Bash/PowerShell invocations must inspect actual relevant manifest/project state **regardless of whether command text matched** a known mutation. Model bounded per-worktree state; initial full snapshot is allowed, routine unrelated calls should not re-scan all content. Include first/later HEAD changes (even clean worktrees), same-file rewrite, tracked additions/deletions/renames, valid and invalid project/package mutations, no-change events, excluded directories, root/nested cwd, real linked worktree and its nested cwd, paths with spaces and worktree isolation. Where lightweight XML parsing is implemented, treat equivalent single- and double-quoted XML attributes equivalently; if evaluation of MSBuild properties is out of scope, document it rather than silently allowing known prohibited concrete values.

### 4.4 D14: Stop behavior

Enforce `stop_hook_active`, initial relevant reminder, unchanged-state silence, materially changed same-file reminders, another unchanged-state silence and per-worktree independence. No infinite repeat on identical content. Do not alter a clean Stop state merely to make a test count larger.

### 4.5 D15: four-slot capability integrity

Verify static selected-only modules, slot cardinality, correct frame/leaf manifests/facets, role-based references, ownership of placement vs technique, actual `binds:` obligations including **removing both sides simultaneously**, implementation-name leak negative tests, and optional frontend clearing in a sandbox. Do not replace L1 with a K1-style capability graph. Policy and decision layers remain level-first.

### 4.6 D16–D17: finite reviews after correctness

Review V2 source technique/examples against the result once; restore material content only where demonstrably useful and non-duplicative. Review always-loaded chars (baseline ≈5.09k tokens, chars/4) and maintainability after fixes. No speculative compression loops, generic scaffolding, forced zero coupling or context optimization that weakens triggers or scope. Added files/components require a demonstrated reliability/ownership rationale.

## 5. One finite shared harness; real implementations

Create `output/.work/` once. Have one reusable fixture runner with independent fresh copies of `output/template/`, real scripts/checkers/hooks/settings, a concise fixture ledger (ID, level, expected verdict, actual diagnostics/exit, evidence path). Keep its test definitions/expectations fixed once implementation starts. Do not patch an oracle to turn genuine FAIL into PASS. If **a test oracle itself is demonstrably broken**, record that separately, revert/fix it before beginning the final confirmation, freeze its hash/definitions, and **never** call a changed-oracle audit a continuation of the same unchanged-oracle confirmation. If the final audit is already under way when this occurs, stop BLOCKED and request owner judgment rather than revising evidence mid-audit.

Required independently meaningful groups (use finite table-driven cases, not hundreds of duplications):

1. **P4/P6:** locked Section 3 matrix in both eligible levels; few metamorphic variants; case/API/frame no-legalizing; true pointers. Assert relevant neutrality diagnostic on FAIL.
2. **Structure/integrity:** level/path assignment; illegal reverse conformance; four slots; extra fifth selection/empty required selection; selected facets; broken refs/imports; implementation leakage; missing required `binds:` alone and from both manifest+contract; optional frontend clear in isolated copy; valid project selection remains in final output.
3. **Hook config and dispatch:** exact declared command/args/event matchers; critical PreToolUse fail-closed; missing/crashing/malformed required input; PostToolUse and PostToolUseFailure Bash/PowerShell event wiring; no unintentional blocking Post/Stop.
4. **Pre-command routing:** dotnet package/reference add/remove, npm/pnpm/yarn, global flags taking values, force/legacy-peer flags; positive and negative/restore-only commands.
5. **Worktree/actual-state:** controlled Git repository with **real linked worktree** and `GIT_CEILING_DIRECTORIES` confinement from the first Git test; cwd root/nested/worktree nested, folder with spaces, active-vs-launch root distinction, per-worktree snapshots, first/later HEAD, rewrites, add/delete/rename and relevant partial changes after failed shell commands, harmless unchanged commands, excluded paths.
6. **Encoding and Stop:** JSON stdin normal/BOM/invalid, manifest UTF-8/UTF-16LE/BE where applicable, malformed encodings; Stop first/unchanged/same-file changed/unchanged and `stop_hook_active`.
7. **Source preservation:** genuine source-to-output 196-policy audit incl. owner/trigger/scope/strength, V2 source review, no duplicate owner, language and references/hygiene, minimal justified complexity and always-loaded estimate.

Negative mutations must fail for the **specific intended reason**, not because sandbox setup is broken. A positive should not add warnings. No mock substitute for real generated checker/hook. Do not assert actual live Claude Desktop hook activation from controlled process-level tests. One baseline failure demonstration per group is enough when cheaply reproducible; all crucial acceptance tests target the FINAL output.

**Anti-overfit:** Test a few independent representations of each property, not solely a hand-curated token list. The expected PASS/FAIL table and primary test suite should not be rewritten after implementation. Do not optimize for the number of passing tests, and never force old permissive P6 PASS on an ambiguous context against strict P4.

## 6. Work order, review and stopping discipline

1. **Preflight and plan:** verify isolated Run-02/85-file copy, immutable sources, identify the actual groupings D1–D17. Read legitimate pointer forms before changing the checker. Freeze the matrix and harness expectations. If requirements seem contradictory, apply Section 3 precedence now; escalate another genuine contradiction before editing rather than burying it in an oracle.
2. **Implement integrated changes:** first policy/level placement + P4 design, then hook/root/command/state as a coherent unit, checker/settings together, capability/`binds:` enforcement. Fix related defects together and run affected finite tests as you implement; keep failures diagnostic.
3. **Primary substantive audit:** review final source policies, L1 identity, P4/P6 actual output and fixture matrix, execution/hooks/worktrees/Windows/Stop, capabilities and optional frontend, V2 technique, references and complexity. Repair concrete template defects found here.
4. **Freeze test oracle(s)** and run **one cumulative confirmation audit**. It must include all required Section-5 groups, no incompatible expected PASS/FAIL, fixed test-harness hash/check definitions and final implementation. If a **real output-template defect** is found, allow **one bounded correction** and **one reconfirmation** with the same oracles. If still dirty, status is `BLOCKED` or `NOT_PROMOTED`; don't start another iteration autonomously.
5. **Terminal:** write honest `output/REFINEMENT_REPORT.md`, record final tree hash, count files, sizes and always-loaded text, verify immutable baseline and final deliverables. Delete `output/.work/` **last** and check `output/` contains only `template/` and `REFINEMENT_REPORT.md`. Report-only edits do not require re-running the full audit. STOP.

**Forbidden after completion or BLOCKED:** second/third audit-of-audit, testing the harness with arbitrary new mutants, repeated baseline rereads, checker-origin reconstruction, repeated rehashes without concrete discrepancy, unbounded Markdown fuzzing, web research, live Desktop hook experiments, re-opening completed findings, or attempts to satisfy an obstructive Stop hook by inventing another proof sequence. A Stop-hook objection is a terminal note to the user, not permission to loop.

## 7. Promotion and report requirements

Promote only when:

- Every D1–D15 mandatory repair is evidenced, D16/D17 reviewed; strict P4 controls and P6 conditional invariance meet the frozen Section-3 contract.
- All source-policy 196 records maintain ownership, `trigger_class`, minimum scope and substantive force; no broken refs/duplicated authoritative owners.
- L1 level hierarchy, stability direction, four-slot static capability model, frame/leaf coupling/`binds:`/optional frontend all remain intact.
- Hook configuration, active worktree detection, critical failure semantics, Bash/PowerShell successful/failed actual-state and all documented bounded command/Windows/Stop groups are evidenced; real checkers PASS and negative mutations fail for intended reasons.
- Runtime instructions remain English, standalone, free of research scaffolding; V2 source technique no worse substantively; complexity growth justified; no weakened oracle or trade-off disguised as a strict improvement.
- One unchanged-oracle cumulative confirmation is clean (or one properly scoped reconfirmation following a real template repair).

Report must include: terminal status and why; Run-02 baseline provenance; starting/final file counts and tree hashes; changed/added/deleted file list; D1–D17 disposition; exact P4/P6 grammar supported/unsupported and fixture summary including neutral vs normative sibling; policy 196 owner/trigger/scope/strength metrics; level/stability/selected-slot/facet/binds/front-end controls; hooks/command/post-success/post-failure/worktree/encoding/Stop results; real process vs controlled host semantics; V2 and complexity review; primary and final confirmation results; any unresolved issues and their precise reproduction.

**The desired result is one defensible, final L1 refinement, not a ninth chapter of self-validation. A truthful BLOCKED is better than a fabricated PASS.**
