# Experiment 005 / Phase 5.4 / Stage A / Step 3
## Evidence-based six-way normative strictness comparison (v1)

**Status:** User-authorized Step 3. **Working directory:** `C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4`.

**Purpose:** Compare the *actual, effective normative behavior* of six independently designed Markdown instruction architectures — **M, M1, L0, L1, K0, K1** — on the canonical 196-policy universe, and identify true candidate-specific additions and behavioral asymmetries. Produce an auditable comparison suitable for deciding whether the research can freeze its candidate baseline and proceed to later experiments. Do **not** rank architectures as better at programming or generate benchmark applications.

**Output directory, created by this task only:**
`stage_A/reconciled/step3_six_way_strictness_v1/`

## 0. Precedence and non-negotiable rules

1. This document defines Step 3's **analysis procedure**, not new engineering policies. Respect already approved user decisions from Step 2 v1/v2/v3 and the frozen canonical oracle. Never treat analyst preference or frequency of a recommendation as a new shared requirement.
2. **Read-only predecessors**: frozen `inputs/`, `stage_A/primary/`, `stage_A/replica/`, `stage_A/independent/`, `stage_A/codex_iterative_search/`, `stage_A/reconciled/step1_union_augmented_pass1/`, `step2_controlled_repair_v1/`, `step2_controlled_repair_v2/` and **the entire** `step2_controlled_repair_v3/` including its six candidates, datasets, and manifests. Never edit those trees or move their files.
3. Write *only* within `step3_six_way_strictness_v1/`. No mutating Git operations, automatic commits, template edits, harmonization, new rule enforcement, or unauthorized policy changes. If a clear defect is found, document it and a minimal proposed remediation instead of editing v3.
4. **No Step 4**, no application/code-generation benchmarks, no winner selection, no trial of a unified architecture. A possible narrowly isolated hook/host **pilot** is distinct from a benchmark and must meet the isolation requirements below; otherwise record NOT_RUN.
5. Keep all research artifacts, reports, JSON and Markdown **in English**. Session updates may be concise.
6. Do not infer full semantic parity from identical `coverage.status`, `strength_status`, a matching witness line, or passing tests. Do not calculate a strictness ranking from raw `MUST_NOT` counts or modality tokens. Source meaning, actual scope, conditionality and enforcement matter.
7. Every concrete Step 3 claim must be traceable to the final **v3 candidate** and, where relevant, the canonical policy, Step 2 claim identifier, and v3 metric lineage. Unverified facts must be labeled UNVERIFIED, not reconstructed from memory.

## 1. Mandatory preflight — fail safely

Before any interpretation or new output except the task's resume scaffolding:

- Read, in full, `stage_A/reconciled/step2_controlled_repair_v3/FINAL_PASS2_PASS3_INTEGRATION_AND_PARITY_REPORT.md`, `STATE.json`, `RESUME.md`, `EVIDENCE_LIMITS.md`, `UNRESOLVED_AND_USER_DECISION_QUEUE.jsonl`, `V3_METRIC_IMPACT.md`, `V3_METRIC_CROSSWALK.json`, `DATASET_MANIFEST.json`, `V3_FINAL_MANIFEST.json`, and the final audit and regression tallies. Read the original canonical 196-policy specification and the approved rules from v3's references.
- Verify v3 `STATE.status` is COMPLETE, that all nine checkpoints are present, that there are exactly 448 expected candidate template files, and that file hashes match the **v3 final manifest**. Verify 196 canonical policy IDs per candidate, 1,176 policy coverage cells, and the v3 classification record universe without discarding inactive/history rows. Confirm the provenance of Codex Pass 1 integration and the completed Passes 2 and 3, but **do not adjudicate them again**.
- Verify the reported v3 final outcomes against artifacts (expected in the supplied final report: 3,416 suite PASS / 0 FAIL / 32 NOT_RUN; 263 cold audit PASS / 0 FAIL / 35 NOT_RUN / 9 FINDING). These are inherited evidence, not new Step 3 test results.
- Record the v3 hashes and comparison inputs in `UPSTREAM_FINGERPRINT.json` and run a **read-only** input-integrity verification on later resumptions.
- Do not confuse the absent v1/v2 *convenience ZIP* with a missing source tree. If the tree and manifest agree, document the missing ZIP as an environment note rather than blocking the study.
- If v3 is not complete, or required source data is absent or genuinely corrupted: record exact discrepancies in `PREFLIGHT_REPORT.md` and STOP with `BLOCKED`. Do not recreate v3 or guess its content.

## 2. Resume and checkpoint protocol

Immediately create `STATE.json`, `RESUME.md`, `PROTOCOL.md` under the **Step 3 output only**. Record all inputs, evidence and open decisions. Partition the 196-policy universe into durable source-grounded batches, with individual per-policy checkpoints and a completed/uncompleted manifest. After each policy, extra-obligation cluster and gate, persist records atomically. On a rate-limit interruption leave the next exact command and first unfinished unit in `RESUME.md` and return without claiming completion.

After resumption, verify checkpoints and hashes; do not restart from policy 1 or silently change the comparison rubric. A model context compaction is **not** a reason to redo completed batches. Do not erase previous failed check attempts; retain the history and corrected final PASS.

## 3. Operational definitions: compare behavior, not wording

For each atomic normative dimension of each policy, review:

- **Requirement content**: what concrete behavior is demanded, forbidden, preferred or permitted.
- **Deontic force**: MUST / MUST_NOT / SHOULD / SHOULD_NOT / DEFAULT / MAY / conditional / compound, based on source meaning rather than text fragments.
- **Scope and applicability**: language/platform, task type, file path, development phase, triggers, explicit conditions, exceptions, approval boundaries. Distinguish a file-loading `trigger` from a normative applicability condition.
- **Effective delivery/reachability**: root/always-on instructions, delegated skills, references, hooks and checkers. A separate knowledge skill's technique example is not automatically an always-active policy. A source line that cannot reliably reach the agent is an enforcement/reachability difference, not automatically a normative-text difference.
- **Enforcement**: prompt advice versus mechanically executed checks, and how hook outcomes are interpreted by the live host. State static expectations separately from verified host behavior.
- **Evidence and counterexamples**: exact current v3 path, line range, claim keys, policy IDs, source excerpt, and a minimal identical hypothetical task showing whether an effective behavioral difference would occur.
- **Canonical compliance vs comparative strictness**: report these on *different axes*. A policy can be stronger in a dimension but not higher-quality, more compliant or more productive. Do not infer benchmark performance from textual strictness.

Use comparison labels at the **atomic dimension** level:
`SAME`, `A_STRONGER`, `B_STRONGER`, `INCOMPARABLE`, `NOT_APPLICABLE`, `UNVERIFIED`.
For six-way policy summaries use: `FULL_SEMANTIC_PARITY`, `PARTIAL_PARITY_WITH_DELTA`, `MEANINGFUL_DIVERGENCE`, `CONTEXT_DEPENDENT`, `UNVERIFIED`.

A condition/exception in one candidate may reverse which is more restrictive on different tasks. Record those task scopes rather than forcing a single total order. Distinguish true normative variance, delivery/reachability variance, enforced behavioral variance, candidate-specific technique, harmless paraphrase, and uncertainty.

## 4. Full canonical comparison (196 policies × six candidates)

For **all 196 canonical policy IDs**, create one six-way source-backed record. For each of the six candidates, identify current v3 normative owners, full relevant subclauses, conditions, exceptions, force, delivery mechanism and available checker evidence. Reconcile the record with `REPAIRED_CLASSIFICATIONS.jsonl`, `REPAIRED_POLICY_COVERAGE.jsonl`, `POLICY_PARITY_MATRIX.jsonl`, the Step 2 per-candidate divergences, and all overlays/crosswalks. Do not silently copy earlier labels as new Step 3 findings.

Review every policy group across the six candidates **side by side**. If individual cells cannot receive a substantive source reading, identify exactly which remain mechanical-only and withhold definitive parity for those cells. Clearly count:
(a) fully source-compared cells,
(b) partially compared cells,
(c) mechanical-witness-only cells,
(d) unverified cells.
Preserve the full 1,176-cell index even when a policy is wholly equivalent.

Specifically challenge the five `STRONGER_AND_WEAKER_EVIDENCE` policy cells and all relevant 38 partial/override witnesses; do not regard an equal-strength fragment as equivalent to the *entire* rule. Check source changes in 104 v3 files relative to frozen originals and all changes since v2 at the point they bear on a comparison.

For every material six-way difference, produce the full set of relevant **15 candidate-pair relationships** or an explicitly documented `NOT_APPLICABLE`/`UNVERIFIED` entry; do not manufacture comparisons just to fill a grid. Include identical-task counterexamples for genuine, testable differences. For policies that are genuinely same, record concise source-based justification (not just a matching label).

## 5. Candidate-specific EXTRA requirements

Build a separate, deduplicated **extra-obligation inventory** from the current v3 classifications including `EXTRA_PRODUCT`, `EXTRA_WORKFLOW`, `CANONICAL_PLUS_DELTA` remainders and `MIXED` extras, and the Codex Pass 1–3 adjudication layers. Separate true obligations from examples, implementation defaults, technical techniques and architecture-specific organizational descriptions.

For each real extra, show presence/absence and effective force across all six architectures; classify it as:
- genuine extra norm likely to affect a comparable task;
- architecture-specific legitimate divergence;
- identical norm with different packaging/reachability;
- redundant, derived, or non-normative;
- unresolved or decision-dependent.

Do **not** adopt extras as additional common oracle policies merely because five candidates have one and the sixth does not. In particular handle the L0 raw-HTML scan issue (Q-01) without silently editing any architecture.

## 6. Previously open issues and metric sensitivity

Process the v3 `UNRESOLVED_AND_USER_DECISION_QUEUE.jsonl` **Q-01 through Q-13** individually. Distinguish RESOLVED, OBSERVATION, ENVIRONMENT, NOT_RUN and true USER_DECISION entries; no blanket reopening of already fixed issues. For each real user decision:
- state the narrow factual difference and actual impact on study tasks;
- offer the minimal sensible options and a reasoned recommendation;
- calculate whether each option changes a Step 3 conclusion or later benchmark comparability;
- leave it undecided if user authorization is missing.

Pay special attention to: Q-01 raw-HTML scan; Q-02 blank PreToolUse command; Q-03 event/tool mismatch; Q-04 K0 Git false-positive; Q-06 the unreviewed `do not`/soft-modality class; Q-08 live-host semantics; Q-11 no-SDK behavior; Q-12 central-file naming; and Q-07 the bounded three-of-six Codex strategy coverage. Preserve uncertainty and context.

For PI-012/HQ-06 and Q-06, **do not rank** candidates using raw modality counts. Where a conclusion depends on alternative defensible readings, provide both readings and a sensitivity table; avoid declaring disputed syntax alone evidence of stronger policy. If necessary perform bounded source rereads only for findings that materially affect comparisons; record the remaining unreviewed universe without hiding it.

Maintain a metric lineage table from v2 to v3 to Step 3. Distinguish 6,498 v3 classification records, the 1,176 policy cells, and directly observed behavior. Never mix counts from different universes. Explicitly document the v3 report's 44-run suite total and distinguish early failed attempts from the successful final suite replay. Validate all table totals and each claimed delta.

## 7. Minimal pilot / static vs live evidence

Step 3 is an evidence comparison, **not** the practical benchmark phase. Do not silently promote static hook/checker simulations to verified Claude Code host behavior. For Git `ask`/`deny`, malformed payload, exit 2, `onFailure`, headless behavior, or checker loading, if a **safe, isolated temporary host probe** is feasible under existing authorization and does not mutate source/benchmark repositories, you may design and execute the minimum necessary test and retain the raw evidence. Otherwise provide an exact manual reproduction procedure and mark the host behavior NOT_RUN.

Do not issue actual mutating Git commands against research repos, trigger live network/registry/database services, or create application benchmarks as part of this step. No forced upgrades, packages or paid tokens. Preserve original differences in hook budgets and explicit instructions separately from observed behavior.

## 8. Quality gates and self-challenge

A. **Preflight gate:** all hashes and counts match; the frozen v3 input is untouched.
B. **Per-batch structural gate:** every canonical policy ID is covered once for each candidate, every claim key and v3 current evidence ref resolves, no duplicate or missing ID, correct semantic record schema, all counters add up.
C. **Semantic challenge gate:** challenge every recorded *material difference* with evidence from both sides, applicable exceptions and a counterexample; challenge every comparison that could overturn a user decision or the claimed fairness of later benchmarks. A fresh-session or different-model reviewer is valuable but do not misrepresent a same-family self-audit as independent confirmation.
D. **Metric and provenance gate:** policy-cell and dataset counts reconcile with final v3 outputs; direct changes, indirect changes and limitations remain distinct; Pass 1, Pass 2 and Pass 3 provenance intact; no reapplication of Codex edits.
E. **Final cold audit:** reread final output artifacts independently of intermediate PASS labels; recompute row counts, hash input snapshots, verify source anchors and decision crosswalks, run a reproducible validation script and save both successful and failed attempts. Clearly report what was actually source-read versus mechanically verified.

No corrections to candidate source files are authorized. If Step 3 uncovers a contradiction, document an exact source-grounded change proposal and its expected impact; defer the one-logical-rule-at-a-time full regression procedure to a separately approved repair task. Never silently revise v3 and pretend Step 3 only compared it.

## 9. Required deliverables

Under the Step 3 output folder, produce at least:

1. `STATE.json` and `RESUME.md` — durable progress, hashes and next executable step.
2. `PROTOCOL.md` and `UPSTREAM_FINGERPRINT.json` — frozen comparison rubric, sources and versions.
3. `POLICY_SIX_WAY_MATRIX.jsonl` — exactly 196 policy-level six-way records, each with source-grounded candidate data and audited cell status; plus a 1,176-cell index if not embedded.
4. `POLICY_PAIRWISE_DIFFERENCES.jsonl` — source-grounded meaningful candidate pairs and counterexamples, with unverified paths explicitly identified.
5. `EXTRA_OBLIGATIONS_SIX_WAY.jsonl` — deduplicated extra obligations and candidate presence/force/delivery.
6. `HOOK_AND_CHECKER_EFFECTIVE_BEHAVIOR.md` — textual policy versus static enforcement versus real host evidence and NOT_RUN.
7. `OPEN_DECISIONS_AND_SENSITIVITY.md` — Q-01 to Q-13 disposition and impact of alternative readings, with precise recommendations only where necessary.
8. `METRIC_LINEAGE_AND_LIMITS.md` — v2→v3→Step 3 record counts, coverage cells, evidence levels and conclusions that cannot be made.
9. `VALIDATION_REPORT.json` plus stored failed/successful attempts; reproducible read-only validators under `_tools/` in Step 3 only.
10. `FINAL_STAGE_A_STEP3_SIX_WAY_COMPARISON_REPORT.md` — scope, method, complete results, defensible comparisons, exceptions, scientific limitations, user decision queue and **GO / CONDITIONAL_GO / NO_GO** for candidate freeze and *later* practical experiments.

All reports must distinguish *verified* from *hypothesized*, normative strictness from enforcement reachability, and architectural differences from defects. Do not present a single global ranking unless a defensible, predeclared comparison metric and coverage standard support it; otherwise report a partial order and scenario-specific differences.

## 10. Stop and handoff

Work autonomously through Step 3 without asking for approval to restate decisions already made. If a genuinely new user policy decision would be necessary, leave it **OPEN** and continue analyzing unaffected rows; explain exactly what the decision blocks. Keep checkpoints current before a quota cutoff. At completion state which evidence is not verified, whether a user decision is required before freeze, and the exact output folder for independent review. **STOP.** Do not initiate Step 4, unify templates, generate C# applications or modify any predecessor.
