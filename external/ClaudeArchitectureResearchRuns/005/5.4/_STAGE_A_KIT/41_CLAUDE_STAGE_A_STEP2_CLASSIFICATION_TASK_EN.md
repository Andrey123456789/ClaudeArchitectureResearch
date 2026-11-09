# Experiment 005 — Phase 5.4 — Stage A / Step 2
## Evidence-based classification of the augmented union (not divergence analysis)

**Research question:** What type of constraint, if any, does each already-extracted claim represent, and to what extent is its *actual normative meaning* entailed by the common 196-policy contract? Do not answer which candidate is stricter than another. Do not edit the candidates.

## 0. Non-negotiable scope and locations

Working root: `C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4`.

Immutable evidence:
- `inputs/{M,M1,L0,L1,K0,K1}/output/template/**` — actual instruction/configuration/checker sources;
- `inputs/<candidate>/source/inventory.json` — 194 V2 policies, grouped under `policygroups[*].policies[*]`;
- `inputs/<candidate>/source/shared-research-invariants.json` — the two research-wide invariants `GOV-017` and `GOV-018`;
- `stage_A/reconciled/step1_union/MERGED_FINDINGS.jsonl` and its provenance/evidence indices;
- `stage_A/reconciled/step1_union_augmented_pass1/AUGMENTED_UNION_VIEW.jsonl` — **the sole enumeration baseline for this step**;
- `stage_A/reconciled/step1_union_augmented_pass1/NEW_CLAUSE_PROPOSALS.jsonl` (26), `EXISTING_GROUP_FACETS.jsonl` (29), `PASS1_REVIEW_LEDGER.jsonl` (152), `UNRESOLVED_REVIEW_QUEUE.jsonl`, and `REVIEW_REPORT.md`;
- `stage_A/primary`, `stage_A/replica`, `stage_A/independent` for resolving original evidence, when needed.

The *latest* union view contains **6,402 input records**, of types `ORIGINAL_GROUP` (6,347), `PROVISIONAL_NEW_CLAUSE` (26), and `PROVISIONAL_FACET_OVERLAY` (29). The last two are **provisional hypotheses**, not automatically valid extra rules. For `ORIGINAL_GROUP`, the claim is `original_group.neutral_claim_text`; the historical `original_labels`, `original_claimed_policy_ids`, and `merge_decisions` are attribution/provenance, not classification truth. The `group_id`, `proposal_id`, or `facet_id` is the stable source key according to record type.

All outputs go to `stage_A/reconciled/step2_classification/` exclusively. Never change `inputs/`, either earlier union, the raw three runs, candidate templates, `_STAGE_A_KIT` except for already supplied prompts, or `stage_A/codex_iterative_search` (which may still be updating independently). **Do not consume unfinished Codex Pass 2 findings or new iterative-search artifacts.** Use only the completed, already reviewed Pass 1 augmentation.

## 1. Exactly what to classify

For **every one of the 6,402 union-view records**, determine:

1. **Normativity:** Is it an obligation/prohibition/preference/default/exception under its actual scope and loading conditions? Or merely an example, observation, explanation, implementation fact or ambiguous text?
2. **Domain:** Does it govern PRODUCT_ENGINEERING, WORKFLOW_ENFORCEMENT (including hooks/checkers that can affect generated work), INSTRUCTION_ARCHITECTURE (candidate rule topology, loading, ownership, manifests, etc.), NON_NORMATIVE or a MIXED domain?
3. **Canonical policy relation:** Is the *full* actionable meaning logically entailed by one or more of the 196 policies, partly entailed with an additional remainder, not entailed, or uncertain? `MATCHED` reported by an earlier agent is **not** enough to establish entailment.
4. **Actual modality and conditions:** preserve MUST / MUST_NOT / SHOULD / DEFAULT / MAY and all triggers, exceptions, timing, negative conditions, scope and enforcement semantics. Never silently strengthen a preference or default into a universal MUST.
5. **Evidence and uncertainty:** Cite the precise immutable source/line or a verifiable provenance link. Explicitly note if the exact quote, complete context, dynamic hook behavior or applicability cannot be established.

A grouped claim may be *compound*. If different subclaims have different semantics, set `classification = MIXED`, enumerate distinguishable subclauses with separate classifications, and mark any possible Step-1 overmerge for subsequent review. Do **not** mutate, split, or renumber the upstream groups here.

For `PROVISIONAL_FACET_OVERLAY`, distinguish **an additional normative obligation** from a **factual clarification of existing hook behavior**. For `PROVISIONAL_NEW_CLAUSE`, independently establish whether it is new relative to the canonical policies; the previous review's word "new" refers only to the union, not to the 196-policy oracle.

## 2. Fixed classification protocol (freeze before processing)

Use these labels in `classification`:

- `CANONICAL_ONLY`: Normative content is fully entailed by identified canonical policy/policies at the same strength, conditions, exceptions, scope and behavior. Different words or file layouts alone do not matter.
- `CANONICAL_PLUS_DELTA`: At least one independently identifiable normative remainder is **not** entailed, even though another part is. Record the canonical portion and the extra remainder *separately*, with a concrete distinguishing scenario.
- `EXTRA_PRODUCT`: Independently actionable product-engineering requirement not entailed by the 196 canonical policies.
- `EXTRA_WORKFLOW`: Additional executable or procedural constraint that can affect work or generated outputs; not entailed by the 196. Keep it separate from product policy and from architecture-topology differences. Merely changing the *mechanism* of enforcing an identical rule is not necessarily an extra requirement.
- `INTERNAL_ARCHITECTURE`: Constraint confined to the candidate's instruction-system architecture (instruction ownership/loading/routing/capability layout, maintenance protocols, etc.). It may be important to evaluate separately, but is **not** automatically an engineering requirement to homogenize.
- `NON_NORMATIVE`: Pure explanation, example, comment, inert illustrative code, factual note, or technical implementation detail with no independently imposed agent/product behavior. Note that actual executable configuration/hook behavior **can** be normative even if expressed in code.
- `MIXED`: Contains two or more independent subclaims with genuinely different classification outcomes. Enumerate the subclauses and their independent evidence/conditions.
- `UNCERTAIN`: Cannot decide normativity, entailment, loading/applicability or exact effect without unsupported assumptions. Document the precise missing fact; do not force a category.

Also store **independent axes**, even where `classification` is sufficient: `normativity = NORMATIVE | NON_NORMATIVE | UNCERTAIN`; `domain = PRODUCT_ENGINEERING | WORKFLOW_ENFORCEMENT | INSTRUCTION_ARCHITECTURE | MIXED | NON_NORMATIVE | UNCERTAIN`; `oracle_relation = FULLY_ENTAILED | PARTIALLY_ENTAILED | NOT_ENTAILED | NOT_APPLICABLE | UNCERTAIN`; `modality`, `scope`, `trigger`, `exceptions` as evidence-supported concise text.

**Atomicity rule:** Two independently falsifiable obligations with distinct scope/action, prohibition, modality, exception or trigger are separate subclaims; synonyms and synonymous restatements with identical permitted behavior are one. Do not keep splitting an obligation merely because a sentence enumerates example implementation techniques. If atomicity is ambiguous, preserve a compound source record and flag it for review rather than fabricating more "new" requirements.

**Canonical entailment test:** A claim is fully entailed only if **every** implementation/behavior satisfying the relevant 196 policies also satisfies that claim, under the same trigger and context. A policy that merely *mentions* the same technology or topic does not entail the more specific instruction. If uncertain, explain why. If claiming `CANONICAL_PLUS_DELTA`, `EXTRA_PRODUCT`, or `EXTRA_WORKFLOW`, give a *discriminating scenario*: a plausible behavior allowed by the canonical policy but prohibited/required differently by this candidate. This must distinguish normative behavior, not merely different prose or file placement. A dynamic effect that has not been executed must not be presented as proven runtime behavior.

**Domain test:** Do NOT throw away a hook/checker solely because it is code, or unify architecture-specific routing/manifest rules as if they are application-development standards. Separate an agent's duties from the tool's enforcement method and the candidate's internal maintenance protocol. Where both occur in one sentence, mark `MIXED`.

**Policy identities:** Preserve exactly 194 V2 IDs plus `GOV-017`/`GOV-018` per candidate; do not silently add `EXTRA-*` as a 197th canonical policy. Record additions as candidate-specific claims, not as adopted common standards. Cross-architecture equivalence/unification is outside this step.

**No policy-making:** Never choose which additional practice all six candidates *should* adopt. Write unresolved normative design choices to a future-decision queue. Do not request user approval to continue the classification; local ambiguity may remain `UNCERTAIN`.

## 3. Calibration before classifying 6,402 records

1. Write `CLASSIFICATION_PROTOCOL.md` summarizing **this frozen decision tree**, not an invented replacement. Store `protocol_version = step2-v1`.
2. Choose **at least 30 evidence-diverse calibration records** sampled across all six candidates, including canonical-only, extra-condition/exception, YAML/JSON/build configuration, hook/checker, workflow skill, internal architecture rule, pure example, and mixed clause. Explicitly include any relevant known ambiguity (e.g. direct Polly exceptions, `WebApplicationFactory` lifecycle, build analyzers, migrations, floating versions) *if present in the actual source and union*. Do not assume their true classification in advance.
3. Save `CALIBRATION.jsonl` with evidence and each proposed outcome. Verify citations against `inputs/` and identify ambiguous wording. Do **not** optimize only toward counts or previous-agent labels. Use `UNCERTAIN` when necessary.
4. Freeze the protocol; perform the full run. If a serious rubric defect surfaces later, record an explicit `PROTOCOL_ISSUE` with evidence for later review; do not silently change definitions mid-run. Calibration is a methodology smoke test, not a claim of independently validated accuracy.

## 4. Processing order and checkpoints

Process candidates **M → M1 → L0 → L1 → K0 → K1**. Each must be processed to completion under the same frozen protocol.

Write append-safe/batch-safe results to `stage_A/reconciled/step2_classification/per_candidate/<candidate>/CLASSIFICATIONS.jsonl`, with checkpoints under `CHECKPOINTS/`. Save atomic small batches (about 50–100 union-view records; smaller if source is complex), hashing completed batch files. A checkpoint is complete **only after** the batch was written, parsed, verified against input keys and marked complete. On resumption inspect actual saved data rather than counting a dialogue claim as a checkpoint.

After each candidate: run structural validation for that candidate, save `CANDIDATE_REPORT.md`, report in this same session succinctly (processed count; by-category counts; canonical coverage; unresolved cases; validator status), and **continue automatically** without confirmation. Never rebuild or overwrite previously completed verified candidates unnecessarily.

## 5. Required record fields

Each classified record should be one JSON object, with at least:

```json
{
  "protocol_version": "step2-v1",
  "candidate": "M",
  "source_key": "FG-M-...",
  "view_record_type": "ORIGINAL_GROUP",
  "classification": "CANONICAL_ONLY",
  "normativity": "NORMATIVE",
  "domain": "PRODUCT_ENGINEERING",
  "oracle_relation": "FULLY_ENTAILED",
  "canonical_policy_ids": ["DEP-020"],
  "modality": "MUST",
  "scope": "precise evidence-backed scope",
  "trigger": "precise evidence-backed condition or NONE",
  "exceptions": "precise exceptions or NONE",
  "rationale": "short factual entailment analysis, citing exact language",
  "evidence_refs": [{"path": "inputs/M/output/template/...", "start_line": 1, "end_line": 1}],
  "canonical_entailment_rationale": "why policy text logically entails entire claim",
  "extra_fragment": null,
  "distinguishing_scenario": null,
  "subclauses": [],
  "review_needed": false,
  "review_reason": null,
  "confidence": "HIGH"
}
```

The sample is a **schema illustration**, not a real DEP-020 decision. Use keys corresponding to source record type: `group_id` for `ORIGINAL_GROUP`, `proposal_id` for `PROVISIONAL_NEW_CLAUSE`, `facet_id` for `PROVISIONAL_FACET_OVERLAY`.

For `CANONICAL_PLUS_DELTA`, `EXTRA_PRODUCT`, or `EXTRA_WORKFLOW` populate `extra_fragment`, `distinguishing_scenario` and authoritative evidence. `CANONICAL_ONLY` requires nonempty valid policy IDs **and** an entailment rationale. For `MIXED`, provide independently described `subclauses` with classification/policy/delta/evidence, and no silent loss of an extra remainder. For `UNCERTAIN` or `review_needed = true`, give `review_reason` with the precise blocker. Other fields may be null where not applicable, but never fabricate evidence or a policy mapping to satisfy the schema.

Evidence references must correspond to the **candidate's immutable inputs**, not to the model's own report. Preserve exact source locations. It is acceptable to cite an immutable provenance index as a navigation aid, but do not treat another agent's conclusion as primary evidence.

## 6. Per-policy coverage and orphan closure

For each candidate, also emit `POLICY_COVERAGE.jsonl` containing **exactly 196 entries**, one for each canonical ID (194 + 2). Each entry must cite which classified source keys substantiate the policy and state `DIRECT_EVIDENCE | PARTIAL_EVIDENCE | NOT_EVIDENCED | UNCERTAIN`. This is *traceability*, **not** a new freeze-readiness/compliance audit: `NOT_EVIDENCED` means no adequate evidence in this classified dataset; do not assert the policy is violated without a separate compliance test.

Revisit the Step-1 orphan/unresolved/review queues and the 17 issues from Pass 1 augmentation. For each potentially normative unresolved fragment, either attach it to a classified source key, create an explicit `ORPHAN_REVIEW_QUEUE.jsonl` entry with evidence, or justify why it is non-normative. Never claim "zero remaining normative orphans" solely because all nonblank source lines are classified. Emit a `COVERAGE_LIMITATIONS.md` explaining that structural coverage does not prove semantic completeness.

## 7. Final deliverables and validation

Under `stage_A/reconciled/step2_classification/` produce:

- `CLASSIFICATION_PROTOCOL.md` (frozen classification criteria and version);
- `CALIBRATION.jsonl`;
- `per_candidate/<candidate>/CLASSIFICATIONS.jsonl` for all six candidates;
- `per_candidate/<candidate>/POLICY_COVERAGE.jsonl` (196 rows each);
- `per_candidate/<candidate>/CANDIDATE_REPORT.md`;
- `CHECKPOINTS/` with verifiable completed batches;
- `CLASSIFICATION_SUMMARY.json` (counts broken down by candidate, class, domain, relation, certainty, evidence quality);
- `ORPHAN_REVIEW_QUEUE.jsonl`, `UNCERTAIN_CLASSIFICATIONS.jsonl`, `POTENTIAL_OVERMERGES.jsonl`, `FUTURE_HUMAN_DECISIONS.jsonl`;
- `COVERAGE_LIMITATIONS.md` and `STEP2_CLASSIFICATION_REPORT.md`;
- `VALIDATION_RESULT.json` and any local validator/report needed to verify IDs, source-key coverage, input SHA-256, unique classification assignments, policy coverage and checkpoint integrity.

**Mechanical acceptance gates:** all 6,402 augmented-view records appear exactly once in classifications, with exact source-key/type/candidate matches (6,347 groups + 26 proposals + 29 facets); all 1,176 per-policy coverage rows appear exactly once; no undefined canonical IDs; no missing evidence on confirmed high-confidence outcomes; no silent drop of a previously recorded provisional proposal, facet or unresolved item; no modifications to immutable input or original findings. A missing item is `FAIL`, not an accepted warning.

**Semantic quality controls:** a sample of confident `CANONICAL_ONLY`, `NON_NORMATIVE`, `INTERNAL_ARCHITECTURE`, and `EXTRA_*` classifications must be challenged against original evidence and counterexamples. Record failed challenges or uncertainties honestly; a purely structural PASS is **not** proof of substantive accuracy. Prefer accurate `UNCERTAIN` over unsupported certainty. Do not derive new engineering-unification decisions from frequency of model votes.

The detailed classification may be costly. Save progress incrementally and resume after usage limits. Do not request user involvement unless continued access to required files is genuinely impossible. Stop after Step 2; do not automatically proceed to cross-candidate strictness comparison, architectural edits, or later Codex-pass integration.
