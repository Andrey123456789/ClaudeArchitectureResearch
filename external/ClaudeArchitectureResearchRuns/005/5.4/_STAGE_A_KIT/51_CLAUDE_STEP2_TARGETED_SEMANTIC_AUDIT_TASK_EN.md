# Experiment 005 / Phase 5.4 / Stage A / Step 2 — Independent targeted semantic audit (v1)

## 0. Mission and boundaries

Perform an **independent, evidence-driven quality audit** of the completed Stage A / Step 2 classification. Step 2 is structurally complete (6,402 classified records; 1,176 candidate-policy coverage rows; previous validator reported 18/18 PASS), but semantic acceptance is **conditional**. Investigate the concrete risks below, propose narrowly scoped, fully traceable corrections, and provide an auditable corrected **derived** view suitable for a later Step 3 review. **Do not start Step 3** and do not issue cross-candidate parity verdicts.

This is a **bounded semantic QA task**, not another full extraction or blanket reclassification of 6,402 records. The audit must be capable of returning `PASS_WITH_OPEN_ISSUES` if a policy choice or ambiguous source cannot be resolved, rather than forcing an answer. Do not describe sampling results as an accuracy rate or as mathematical proof of semantic completeness.

Work from `C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4`, with this task file under `_STAGE_A_KIT/`.

### Read these inputs first (read-only)

1. `_STAGE_A_KIT/52_STEP2_INDEPENDENT_REVIEW_EN.md` — the independent review and its specific defects. Use as an *issue lead*, not as an infallible adjudication. Verify against the sources.
2. `_STAGE_A_KIT/41_CLAUDE_STAGE_A_STEP2_CLASSIFICATION_TASK_EN.md` — the original task's authoritative criteria.
3. `stage_A/reconciled/step2_classification/CLASSIFICATION_PROTOCOL.md`, `PROTOCOL_ADDENDUM_A1.md`, `PROTOCOL_ISSUES.jsonl`, `PROTOCOL_FREEZE.json`.
4. `stage_A/reconciled/step2_classification/STEP2_CLASSIFICATION_REPORT.md`, `COVERAGE_LIMITATIONS.md`, `VALIDATION_RESULT.json`.
5. `stage_A/reconciled/step2_classification/per_candidate/<C>/CLASSIFICATIONS.jsonl` and `POLICY_COVERAGE.jsonl` for C in `M,M1,L0,L1,K0,K1`; `UNCERTAIN_CLASSIFICATIONS.jsonl`, `POTENTIAL_OVERMERGES.jsonl`, `ORPHAN_REVIEW_QUEUE.jsonl`, `FUTURE_HUMAN_DECISIONS.jsonl`, `STEP1_QUEUE_DISPOSITIONS.jsonl`, `_decisions/A13_AUDIT_FINDINGS.jsonl`.
6. Frozen source evidence under `inputs/<C>/output/template/`; candidate `inputs/<C>/source/inventory.json` (194 V2 policies) and shared GOV-017/GOV-018 in `inputs/`. Consult original augmented-union provenance whenever needed to resolve an unclear group.

**Never** treat earlier classification fields, original audit labels, an automation's result, or the independent review's conclusion as intrinsically correct. Re-read exact source lines and the relevant **full** canonical policy text; reason from the words, trigger, exceptions, timing, strength, actor and loading context. Distinguish instruction-system architecture from product-engineering and agent-workflow duties. Do not presume comparable clauses in different candidates have identical semantics. For code-based rules, static analysis is not proof of executable runtime behavior.

### Strict write fence and independence

Write **only** inside `stage_A/reconciled/step2_semantic_audit_v1/` (create it if absent). Treat the entire existing `step2_classification/` folder, all earlier Stage A/5.3 evidence, all `inputs/` candidate files, and the concurrent Codex search as immutable. Do not edit the original protocol or 6,402 classifications; do not change candidate architectures, create a unified architecture, run another global source extraction, or consume Codex Pass 2 outputs. Do not write outside the output folder except for the user copying this kit into `_STAGE_A_KIT/`.

Use a **fresh Claude Code session** to reduce continuity bias from the original classifier. Work autonomously, write restartable checkpoints and resume from validated outputs. Avoid stopping for approval for matters resolvable from source; put actual policy choices into the decision queue. Read source and independently articulate a counterexample **before** accepting or rejecting the original classification. If the existing frozen protocol contains a tension, record a proposed amendment and effect analysis; do not silently redefine it.

## 1. Preflight: verify the audit universe

- Verify the completed Step 2 input exists and has exactly 6,402 unique classification keys, 1,176 unique candidate-policy rows, and six candidates (M 1,003; M1 1,113; L0 972; L1 1,037; K0 1,077; K1 1,200). Recompute from files, not reports. Check that the upstream input hash manifest and immutable source paths still match; rerun the **existing** Step 2 validator **read-only** without running its `build` mode or causing changes to upstream files. If its validator writes to source, instead run it in an isolated copy inside your output folder and describe the isolation. Do not overwrite Step 2 `VALIDATION_RESULT.json`.
- Enumerate the *actual* audit targets from the files, track overlaps in a single `AUDIT_TARGETS.jsonl`, and compare counts to the expected reference counts below. Report discrepancies rather than manufacturing records.
- Freeze a reproducible independent sampling plan **before** auditing the samples; record selection criteria, deterministic seed, IDs and per-candidate/category counts in `SAMPLING_PLAN.json`.

## 2. Required source-grounded review work

### A. Known counterexample: Swagger UI

- First investigate **K1** record `FG-K1-2b15ea3da2` with exact evidence `inputs/K1/output/template/.claude/skills/swagger/SKILL.md:70` and all associated source ranges. Current label is `CANONICAL_ONLY` with `FULLY_ENTAILED`, `SAME`, `DEFAULT`. Source directs opening Development Swagger UI and verifying that it loads after API behavior changes. Evaluate the exact canonical policies `WF-006`, `WF-005`, `API-016`, `TST-010` and a counterexample where startup, OpenAPI JSON and tests pass without opening the UI. Determine whether the action is an independently falsifiable additional workflow obligation, its condition and modality, and whether `CANONICAL_PLUS_DELTA`, `MIXED`, or another label is warranted.
- Source-review comparable Swagger verification records in **M, M1, L0, L1, K0**, especially those currently marked `UNCERTAIN` regarding the scope of the condition. Do not impose uniform labels if actual texts differ. For every candidate, record evidence, trigger, exception and the reason any apparent contrast is real or merely a labeling inconsistency.
- Inspect `COVERAGE_LIMITATIONS.md`'s explicit cross-candidate Swagger reading difference. Flag any downstream canonical coverage cells or affected comparative interpretations.

### B. PI-012: all documented 79 flat negatives

- Enumerate **all 79 category `N`** entries in `step2_classification/_decisions/A13_AUDIT_FINDINGS.jsonl` (expect count 79; reconcile if different). Re-read each exact source and its necessary context. For each decide whether its language actually creates a `MUST_NOT` prohibition, conveys a recommendation, default, scope description, descriptive fact, conditional rule, or cannot reliably be distinguished. Examples: “Not retried”, “not a dumping ground”, “does not appear in Application contracts”, “only when”. Mere negation is **not automatically** a command.
- Prepare a coherent, source-aware normalization proposal for negative declaratives, consistent with positive declaratives, imperatives, and the already frozen C1–C15 criteria. Separate reading of **normativity** from reading of **modality**. Explicitly preserve scope, actor, trigger and exceptions. Document an independently falsifiable scenario for anything marked stronger/weaker than before.
- For each of 79: `UPHOLD`, `CORRECT`, or `UNRESOLVED`, with old vs suggested fields and reason. **Do not force** a resolution of policy-governance ambiguity. Report separate counts for outcome and impact on strength/coverage. If a broadly aggregated group masks different negative subclauses, propose a `MIXED` subclause overlay.
- Treat the normalization as a **proposed interpretation** where it would amend the frozen protocol; do not silently apply a protocol change retroactively. Include sensitivity analysis for Step 3 (which strictness conclusions would change if the proposed rule is accepted vs not accepted).

### C. Whole targeted risk inventory (account for every item, overlaps allowed)

Individually triage these known risk lists. A low-risk entry may be resolved by concise evidence-grounded justification; every entry must receive an explicit outcome, source link and audit status:

1. **33** entries in `POTENTIAL_OVERMERGES.jsonl`: decide whether different independently falsifiable claims were merged; propose group-local `subclauses` or facet overlay, retaining original keys and provenance. Don't split or mutate upstream Step 1 groups.
2. **38** policy-coverage rows with a nonempty `reviewer_override_note`: verify the union of witnesses actually covers each **clause** of the canonical policy, with matching triggers, scope, exceptions and normative strength. `DIRECT_EVIDENCE` is traceability, not parity. Explicitly re-evaluate K0 `API-014`,`API-019`, and K1 `GOV-007`,`API-014`,`API-019` (five `STRONGER_AND_WEAKER_EVIDENCE` cells); never infer `EQUIVALENT` from their overall coverage status.
3. **19** records labeled `UNCERTAIN` and **4** with uncertain subclauses: independently reassess; retain `UNRESOLVED` when evidence cannot settle the question.
4. **All entries** in `UNCERTAIN_CLASSIFICATIONS.jsonl` (expected ~91 unique rows, including the 33 LOW-confidence and 90 review-needed flags, **not additive**): source-review and explain which uncertainty can be resolved without user choice. Use a set union to prevent duplicate work.
5. **21** entries in `ORPHAN_REVIEW_QUEUE.jsonl`: decide whether each includes a missing normative action, a facet of an existing record, a nonnormative example, or remains an explicitly documented orphan. Do not secretly add unrelated extractions; report any proposed new clause separately.
6. **24** entries in `FUTURE_HUMAN_DECISIONS.jsonl`: verify these are genuine human policy decisions rather than resolvable source interpretations; deduplicate by underlying question. **Do not** decide how stringent the six architectures ought to be. Preserve approvals/exceptions as unresolved where warranted.

A claim that is repeated in several lists is one audit case with multiple target-list memberships. Cross-reference all memberships. Escalate and resolve systematic inconsistencies discovered while doing these checks.

### D. Independent semantic reading of the five candidates not previously externally reviewed

The original classifier processed M1, L0, L1, K0, K1 without a fresh independent semantic reader. In **each** of these five candidates freeze a source-key-based, deterministically selected set of **at least 24 additional records** not already targeted by section C where availability permits, across the following strata:

- 4 `CANONICAL_PLUS_DELTA` (include both strength and exception-related deltas where available);
- 4 `EXTRA_PRODUCT`;
- 4 `EXTRA_WORKFLOW`;
- 4 `MIXED` (or all if fewer than four);
- 3 `CANONICAL_ONLY` (prioritize a weaker-strength/partial-coverage example);
- 2 `NON_NORMATIVE` (do not filter out MEDIUM confidence);
- 2 `INTERNAL_ARCHITECTURE`;
- 1 `UNCERTAIN` if not already audited; otherwise select a `DEFAULT`/`SHOULD` borderline case.

For M, do a **minimum 8-record calibration spot-check**, including revised records `FG-M-22cae42396`, `FG-M-1c4fc44b5e`, `FG-M-d0b6a09cce` and at least five extra cases, to ensure the review's decision rule has not drifted. Avoid a much larger reread of M unless evidence indicates a systemic issue.

Use a stable SHA-256-sort selection over source keys within the strata, frozen **before** opening the source for the selected sample; record shortfalls and substitutions. For each selected record, first make an independent reading of its actual source and canonical policies; only then compare with the stored fields. Require a **distinguishing counterexample** for `CANONICAL_PLUS_DELTA` or `EXTRA_*`, or a positive entailment argument for `CANONICAL_ONLY`. Explicitly assess `MIXED`/atomicity, normative strength, exceptions, scope, trigger, and architecture-internal vs product/workflow distinctions. Record both agreements and disagreements. Never claim this non-random, risk-enriched audit supplies an unbiased statistical error rate.

### E. Coverage of the 4,868 mechanically accounted Step 1 queue records

Do **not** pretend these were individually adjudicated. Without a 4,868-item brute-force review, predefine and independently examine **48** queue items (at least eight per candidate) from the mechanically closed items in `STEP1_QUEUE_DISPOSITIONS.jsonl`: include attribution disagreements, related-but-distinct claims, broad/narrow differences, and different normative strengths. Select with a documented deterministic/risk-stratified rule, and track overlap with earlier targets. Record whether this review discovers evidence of **systematic** lost normative subclauses or incorrect deduplication. If repeated failures suggest broad contamination, enlarge only the affected stratum and flag Step 3 as blocked for that area; don't silently declare the entire queue reviewed.

### F. Consistency/drift diagnostic

Examine label-use drift without treating raw label counts as inherent architecture differences: `MIXED` counts M 6 → K1 40; `INTERNAL_ARCHITECTURE` M 47 → K1 91. Select a bounded set of same-type/source-role/related-policy examples across at least three candidate pairs and compare **classification criteria**, not candidate quality. Note where source differences warrant different labels versus where equivalent semantics were read differently. This is diagnostic **normalization**, not Step 3 six-way strictness ranking. Do not impose architecture-mechanism parity.

## 3. Evidence, decisions, and suggested correction overlays

For every audited claim, record:
- candidate and stable original key, audit reason/membership, exact source path + line range + verified quote, relevant **full** canonical policy IDs and text/ranges, previous classification fields, independent classification fields, actor/behavior/trigger/scope/exception/timing/modality/enforcement, entailment test or counterexample, original-vs-proposed determination, confidence, and explicit remaining ambiguity;
- decision `UPHOLD`, `CORRECT`, `UNRESOLVED`, `NOT_A_SEPARATE_CLAUSE`, `OVERMERGE_FACET`, or `EVIDENCE_CONFLICT`, with a short concrete rationale;
- if changed, an atomic `before/after` record and source-fingerprint. A correction must be independently re-playable; no silent overwrites, inferred source lines, or unsupported additional policy IDs.

Maintain the **original** 6,402 group/proposal/facet identities. Newly identified subclauses are local overlays; an unsurfaced orphan becomes a `NEW_CLAUSE_PROPOSAL` with provenance and does not masquerade as one of the immutable 6,402.

Do not automatically change one candidate's rule merely because another candidate is stricter. Do not unify candidate requirements, decide human governance, or change any template, hook or enforcement script. Never treat the 26 Pass-1 provisional proposals as independently approved policy additions.

Produce a complete **derived** effective classification view after proposed, source-supported corrections, but keep the baseline unchanged. It must preserve every original record exactly once; express all suggested changes via the overlay and record unresolved alternatives without forcing a new label. Apply the overlay deterministically, with a manifest linking baseline hashes and overlay hashes. Recompute any impacted coverage/strength descriptors; where independent confirmation is insufficient, retain the old row marked `REVIEW_REQUIRED` rather than assert parity. Explicitly mark `PROPOSED`, not `RATIFIED`, on all corrections that depend on a methodology amendment or pending human decision.

## 4. Deliverables, checkpoints, acceptance gates

Write all outputs under `stage_A/reconciled/step2_semantic_audit_v1/`:

- `STATUS.json` and `CHECKPOINTS/` (phase, candidate/target, counts, input hashes; restartable).
- `AUDIT_TARGETS.jsonl`, `SAMPLING_PLAN.json`, `AUDIT_LEDGER.jsonl` (full targeted-universe accounting and decisions).
- `CORRECTION_PROPOSALS.jsonl` with before/after provenance; `NEW_CLAUSE_PROPOSALS.jsonl` if genuinely missing obligations are seen; `UNRESOLVED_QUEUE.jsonl` and `HUMAN_DECISION_QUEUE.jsonl` (only justified open issues).
- `PI012_NEGATIVE_MODALITY_REVIEW.jsonl` (all actual category N entries) and `METHODOLOGY_NOTE.md` (normalization proposal, protocol compatibility, alternative interpretations and sensitivity).
- `COVERAGE_OVERRIDE_REVIEW.jsonl` (all actual override rows, including five special strength cases); `OVERMERGE_REVIEW.jsonl` (all 33); `ORPHAN_REVIEW.jsonl` (all 21); `QUEUE_SAMPLE_REVIEW.jsonl` (the 48 queue items); `DRIFT_DIAGNOSTIC.md`.
- `EFFECTIVE_CLASSIFICATIONS.jsonl` with all **6,402** original identities and applied suggested corrections clearly distinguished from baseline; `EFFECTIVE_POLICY_COVERAGE.jsonl` with **1,176** candidate-policy identities and accurate flags for unresolved/conditionally supported coverage; `EFFECTIVE_VIEW_MANIFEST.json` holding precise fingerprints and overlay protocol. The effective view is a **proposed QA overlay**, not a newly frozen baseline.
- `VALIDATION_RESULT.json` and reproducible validator/helper scripts inside `_tools/` (scripts must verify source ranges, original counts, unique IDs, target-list accounting, hash preservation, override lineage, overlay consistency, reference existence, and any affected coverage cells). Test the scripts.
- `SEMANTIC_AUDIT_REPORT.md` summarizing candidate-by-candidate findings, resolved vs unresolved counts, corrections by class/modality/strength, examples with quotations, limitations, and an explicit **GO / CONDITIONAL_GO / NO_GO for starting Step 3's definitive strictness comparison**. Distinguish permission to **prepare** Step 3 from permission to use unresolved claims as facts.

Run gates:

1. `ALL_UPSTREAM_INPUTS_UNCHANGED` by SHA-256 for the candidate input files and Step 2 baseline (never change it).
2. `AUDIT_TARGETS_EXHAUSTIVELY_ACCOUNTED` (79 N, 33 possible overmerges, 38 override coverage rows, all uncertain/flagged cases, 21 orphans and 24 human-decision entries; exact expected counts corroborated from input).
3. `INDEPENDENT_SAMPLE_FROZEN_AND_READ` (five ≥24-record samples and M's limited calibration, with substitutions noted).
4. `ALL_QUOTES_SOURCE_VERIFIED` for *each* substantive reclassification or new claim.
5. `NO_SILENT_RECLASSIFICATION`, `BASELINE_6402_1176_IDENTITIES_PRESERVED`, `OVERLAY_REPLAYABLE` and `UNCERTAIN_NOT_FORCED`.
6. `NO_PASS2_IMPORTED`, `NO_SOURCE_TEMPLATE_OR_ORIGINAL_STEP2_WRITES`, `NO_STEP3_OR_UNIFICATION`, and honest `LIMITATIONS_REPORTED`.

A failed gate must yield `BLOCKED` or `PASS_WITH_OPEN_ISSUES`, not be waived by a manually typed PASS. If time/token limits interrupt execution, save a clear resumable checkpoint; do not claim completion prematurely. Do not ask the user to make a governance choice merely to continue semantic review.

## 5. Execution order and finish

Preflight and sampling freeze → A (Swagger) → B (79 negatives) → C (risk lists, de-duplicated) → D (five-candidate semantic sample + M calibration) → E (48 Step-1 queue checks) → F (drift) → proposed overlays → validation → final report. After each phase, save state and present a concise in-session status. Continue autonomously to completion. **Stop before Step 3**.
