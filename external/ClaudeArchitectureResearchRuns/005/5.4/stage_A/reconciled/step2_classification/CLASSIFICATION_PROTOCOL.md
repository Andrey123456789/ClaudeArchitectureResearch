# Stage A / Step 2 — Classification protocol

`protocol_version = step2-v1` (frozen 2026-11-02, before the full run; calibration in `CALIBRATION.jsonl`)

Source of authority: `_STAGE_A_KIT/41_CLAUDE_STAGE_A_STEP2_CLASSIFICATION_TASK_EN.md` §1–§2. This file summarizes that
fixed decision tree. It does not replace it. The **operational clarifications C1–C15** settle
cases that the task text leaves open. Each clarification that could be read as a change to a
definition is also logged in `PROTOCOL_ISSUES.jsonl` for later human review.

## 1. Inputs and unit of classification

- **Enumeration baseline:** the immutable `step1_union_augmented_pass1/AUGMENTED_UNION_VIEW.jsonl`. It holds 6,402 records:
  - 6,347 `ORIGINAL_GROUP` records, keyed by `group_id`;
  - 26 `PROVISIONAL_NEW_CLAUSE` records, keyed by `proposal_id`;
  - 29 `PROVISIONAL_FACET_OVERLAY` records, keyed by `facet_id`.
- **Claim under classification:**
  - for a group, `original_group.neutral_claim_text`;
  - for a proposal, `proposed_clause_text`;
  - for a facet, `facet_text`.
- **Attributed fields:** historical labels, reported policy IDs, reported modality, trigger and exceptions are attributed provenance. They are shown to the reviewer as leads. They are never accepted as classification truth.
- **Evidence:** every record cites its immutable source ranges under `inputs/<C>/output/template/**`. These come from Step-1 verified occurrences, or from Pass-1 evidence for provisional records. The reviewer may add ranges with `ev:`, and every added range is checked against the file.
- **Oracle:** the 194 V2 policies in `inputs/<C>/source/inventory.json` plus `GOV-017` and `GOV-018` from `shared-research-invariants.json`. All six candidates carry identical inventory files (SHA-256 checked). `intentional_non_oracle_material` (EXC-001..018) is a navigation aid only. It is not a policy and is never cited as entailing anything.

## 2. Decision tree (applied to every record, in this order)

1. **Normativity.** Does the text, read in its loading context, impose a behavior? A behavior here means an obligation, prohibition, preference, default, exception, approval gate, or the effect of executable configuration or a hook/checker.
   - If it does not → `NON_NORMATIVE` (explanation, example, comment, inert illustrative code, factual note, implementation detail with no independent effect).
   - If normativity cannot be decided without unsupported assumptions → `UNCERTAIN`, naming the missing fact.
2. **Atomicity.** Does the record contain two or more independently falsifiable subclaims whose outcomes differ? Subclaims are independent when they differ in action, prohibition, modality, exception or trigger. If so → `MIXED`, with enumerated `subclauses`, each classified separately. Synonymous restatements and example lists are not split. Where atomicity is ambiguous, keep the record compound and set `review_needed`. Possible Step-1 overmerges get `om:` and are written to `POTENTIAL_OVERMERGES.jsonl`. Upstream groups are never mutated.
3. **Domain** of each normative (sub)claim: `PRODUCT_ENGINEERING`, `WORKFLOW_ENFORCEMENT`, `INSTRUCTION_ARCHITECTURE`, or `MIXED` (see C4). If the claim is confined to the instruction-system architecture → `INTERNAL_ARCHITECTURE`.
4. **Canonical entailment test.** A claim is fully entailed only if every behavior satisfying the relevant policies also satisfies the claim, under the same trigger and context. Topic overlap is not entailment, and neither is mentioning the same technology.
   - Fully entailed → `CANONICAL_ONLY`: requires valid policy IDs and an entailment rationale.
   - Entailed part plus an independently identifiable non-entailed normative remainder → `CANONICAL_PLUS_DELTA`. Record the canonical part (policy IDs), the remainder (`extra_fragment`) and a distinguishing scenario.
   - Not entailed, product-engineering → `EXTRA_PRODUCT`, with a distinguishing scenario.
   - Not entailed, executable or procedural constraint on work or outputs → `EXTRA_WORKFLOW`, with a distinguishing scenario.
   - Cannot decide → `UNCERTAIN`.
5. **Modality and conditions.** Preserve the actual MUST / MUST_NOT / SHOULD / SHOULD_NOT / DEFAULT / MAY / REQUIRES_APPROVAL / DECIDED, together with its trigger, exceptions, timing, scope and enforcement semantics. Never strengthen a preference or default into MUST.
6. **Evidence and uncertainty.** Cite exact immutable ranges and state what could not be established: the exact quote, the full context, dynamic hook behavior, or applicability. `confidence` is HIGH, MEDIUM or LOW:
   - HIGH: the text is unambiguous and the entailment judgment needs no assumption;
   - MEDIUM: the judgment rests on a stated reading or an assumption;
   - LOW: the judgment is close to arbitrary and is flagged.

Labels: `CANONICAL_ONLY`, `CANONICAL_PLUS_DELTA`, `EXTRA_PRODUCT`, `EXTRA_WORKFLOW`, `INTERNAL_ARCHITECTURE`, `NON_NORMATIVE`, `MIXED`, `UNCERTAIN` — exactly as defined in task §2.

**Independent axes** are stored for every record:
- `normativity`: NORMATIVE | NON_NORMATIVE | UNCERTAIN;
- `domain`: PRODUCT_ENGINEERING | WORKFLOW_ENFORCEMENT | INSTRUCTION_ARCHITECTURE | MIXED | NON_NORMATIVE | UNCERTAIN;
- `oracle_relation`: FULLY_ENTAILED | PARTIALLY_ENTAILED | NOT_ENTAILED | NOT_APPLICABLE | UNCERTAIN;
- `modality`, `scope`, `trigger`, `exceptions`.

Additional fields:
- `strength_vs_canonical`: SAME | WEAKER | STRONGER | INCOMPARABLE | N/A;
- `canonical_coverage`: FULL or PARTIAL per cited policy;
- `related_policy_ids`: non-entailing context only;
- `canonical_conflict_ids`;
- `facet_assessment` (facets);
- `new_relative_to_oracle` (proposals);
- `field_provenance`: says, for each field, whether a value was decided by the reviewer, taken over from attributed provenance, or computed mechanically.

## 3. Operational clarifications (frozen with v1)

- **C1 — Weaker or partial claims.** `CANONICAL_ONLY` requires the full-entailment test. A claim may be *weaker* than the policy, or cover only part of it, and still be entailed. Example: a policy MUST becomes the claim SHOULD; or the claim names one item of a policy's list. Such a claim is `CANONICAL_ONLY` with `strength_vs_canonical = WEAKER` or with coverage `PARTIAL` (`~`). The weakening is a coverage observation, not an extra requirement. A *stronger* claim is never `CANONICAL_ONLY`. It is `CANONICAL_PLUS_DELTA` (`st=STRONGER`), or `EXTRA_*` when no canonical portion remains. Stronger means, for example, an added condition, a narrower exception, a removed explicit-request exception, DEFAULT becoming MUST, or a broader prohibited set. Logged as PROTOCOL_ISSUE PI-001, because task §2 says "at the same strength".
- **C2 — `CANONICAL_PLUS_DELTA` vs `MIXED`.**
  - `CANONICAL_PLUS_DELTA` applies when the remainder refines the *same* obligation: added specificity of the same action, stronger modality, narrower exception, extra trigger or timing. `extra_fragment_kind` (`k`) records whether the remainder is product, workflow or architecture.
  - `MIXED` applies when the record holds separable subclaims with different actions and different outcomes. Typical cases: an agent duty plus its hook mechanism plus a maintenance protocol; a canonical rule plus instruction routing.
- **C3 — Enforcement mechanisms.**
  - A hook, checker, setting or build configuration that only enforces an *identical* canonical rule, with no additional effect on work, is classified with that rule: `CANONICAL_ONLY`, domain `WORKFLOW_ENFORCEMENT`.
  - Additional executable effects are `EXTRA_WORKFLOW`, or the workflow remainder of a `CANONICAL_PLUS_DELTA`. Examples: blocking or denying behavior the canonical rule permits; marker or re-run protocols; fail-closed gating of all shell calls; stop-time prompts; findings with no explicit-request exception; broader match sets.
  - A narrower enforcement, such as a checker that misses some cases, adds no obligation. It is recorded in the rationale.
- **C4 — Domain assignment.**
  - `PRODUCT_ENGINEERING` covers the product repository's code, configuration, tests, build settings, dependencies and CI/CD pipeline content, plus approval gates whose object is product architecture or technology.
  - `WORKFLOW_ENFORCEMENT` covers the agent's work process — inspection, planning, verification, review, reporting, Git, approval procedure, dependency due diligence — and hooks, checkers and settings that act on the agent's work.
  - `INSTRUCTION_ARCHITECTURE` covers instruction ownership, placement, loading, routing, headers, manifests, capability slots, levels and kinds, instruction-system maintenance, and checkers that validate only the instruction system.
  - For CANONICAL_* records, the tools suggest a default domain from the first cited policy; the reviewer overrides it (`d=`) when the claim's object differs.
- **C5 — Technique and examples.**
  - Text that prescribes a particular way of doing something is normative at its stated or implied strength, usually DEFAULT or SHOULD. This holds for imperatives, and for declaratives used as guidance ("integration tests replace …").
  - Explicitly illustrative content is `NON_NORMATIVE`: "for example", "e.g.", code samples, "useful", "can", option lists. A copy risk (an example embodying an unapproved choice) is noted, not converted into a rule.
- **C6 — Permissions.** MAY or ALLOWED text is normative only when it widens or narrows what the canonical policies permit. A permission the oracle already grants is `CANONICAL_ONLY` (when it is part of a policy's statement) or `NON_NORMATIVE` (when it is merely descriptive).
- **C7 — DEFAULT deviation mechanics.** The oracle's DEFAULT strength does not itself require that a deviation be documented, reported or recorded. A candidate requirement to do so is therefore a non-entailed remainder: `CANONICAL_PLUS_DELTA` with `k=W`, or `EXTRA_WORKFLOW` for the general definition. This applies whether the requirement is stated per rule (for example "direct Polly … document why") or as a general definition. Confidence is at most MEDIUM, because the oracle does not define DEFAULT mechanics.
- **C8 — Strength equivalences.** `DECIDED` ≈ MUST unless an approved decision changes it. `REQUIRES_APPROVAL` ≈ MUST_NOT without explicit approval. Candidate wording with the same approval path is SAME strength.
- **C9 — Loading and placement.** File placement, loading mechanism and path-scoping are not normative differences by themselves. They are recorded in `scope` and `loading_context`. They matter only where the trigger or scope text changes what is permitted.
- **C10 — Host-dependent semantics.** Hook and settings semantics are read statically: exec-form `args`, `onFailure`, PostToolUseFailure, `decision:block`, Stop blocking, exit codes. The classification uses the implemented or declared intent. No runtime effect is asserted. Where the classification depends solely on host support, the record is flagged `review_needed` with confidence ≤ MEDIUM.
- **C11 — Facets.**
  - `fa=AN` (ADDITIONAL_NORMATIVE_OBLIGATION): the facet adds an obligation, permission or blocking effect beyond the target group's text.
  - `fa=FC` (FACTUAL_CLARIFICATION_OF_EXISTING_BEHAVIOR): the facet only clarifies how the existing mechanism behaves. The facet is then normally `NON_NORMATIVE`, with the consequence for the target noted.
- **C12 — Field defaults and provenance.**
  - `trigger` and `exceptions` default to the attributed seed-record text that was displayed to the reviewer (`REPORTED_SEED_ATTRIBUTED`). The reviewer overrides (`t:`/`e:`) when that text is wrong or incomplete.
  - `scope` defaults to the mechanical loading context.
  - `modality` defaults to the reported base token only when all reporting runs agree. Otherwise it must be decided explicitly.
  - These defaults are attributed, not independently re-derived. `field_provenance` says which applies.
- **C13 — Policy coverage** is computed from CANONICAL_* links (record level and subclauses), as traceability, not compliance:
  - `DIRECT_EVIDENCE`: at least one FULL link with confidence ≥ MEDIUM;
  - `PARTIAL_EVIDENCE`: only PARTIAL, WEAKER or LOW-confidence links;
  - `UNCERTAIN`: only links from UNCERTAIN records;
  - `NOT_EVIDENCED`: no link.
  A reviewer override is allowed only with a written note, for example when several partial claims jointly cover a policy.
- **C14 — Scenario discipline.** `EXTRA_*` and `CANONICAL_PLUS_DELTA` need a distinguishing scenario that changes permitted behavior. A scenario that differs only in wording or file layout disqualifies the extra classification.
- **C15 — Conflicts.** A claim that requires something a policy forbids, or forbids something a policy requires or permits, has the policy listed in `canonical_conflict_ids`. It gets a `FUTURE_HUMAN_DECISIONS.jsonl` entry, and is classified by the tree, normally as `CANONICAL_PLUS_DELTA` with `st=STRONGER` or `INCOMPARABLE`, or as `EXTRA_*`. Removing a permission the oracle grants is STRONGER, not a conflict, unless the oracle makes that permission mandatory.

## 4. Process controls

- **Calibration** (≥30 records, all six candidates) is recorded in `CALIBRATION.jsonl` before the full run. The same records are classified again inside the frozen batches, and agreement is reported.
- **Batches.** The frozen batch plan is in `_batches/<C>.json` (≤60 records per batch, ordered by primary source location).
- **Decisions.** Decisions are in `_decisions/<C>/B###.dec` (DSL documented in `_tools/build.py`). Each decision file is compiled into `per_candidate/<C>/batches/B###.jsonl`. A batch is checkpointed in `CHECKPOINTS/<C>/B###.checkpoint.json` only after the compiled file has been written, re-read, parsed, and its keys and types verified against the plan. The checkpoint stores file hashes.
- **Rubric defects** found during the run are appended to `PROTOCOL_ISSUES.jsonl`. Definitions are not changed mid-run.
- **Separation of concerns.** No cross-candidate strictness comparison, no edits to candidates, no unification, and no use of Codex pass ≥ 2 artifacts.
