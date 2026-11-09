# Protocol addendum A1 (step2-v1)

Added 2026-11-02 after the independent review of candidate M. `CLASSIFICATION_PROTOCOL.md` is unchanged and its frozen hash still holds. This addendum adds fields, checks and reading rules; it does not redefine any label. Records carry `protocol_version = step2-v1` and `protocol_addendum = A1`. Each rule is logged as a `PI-###` item in `PROTOCOL_ISSUES.jsonl`.

## A1.1 Corrections after a checkpoint

- Checkpointed batch files are never rewritten. A later change is a block in `_decisions/<C>/CORRECTIONS.dec`.
- `_tools/corrections.py` compiles those blocks into two files:
  - `CORRECTIONS.jsonl`: correction ID, finding reference, reason, field-by-field before and after, the full before record, and hashes of both versions.
  - `CORRECTED_RECORDS.jsonl`: the after records.
- Assembly overlays the after records. Each corrected record carries a `correction_history`.
- `CHECKPOINTS/<C>/CORRECTIONS.checkpoint.json` stores the hashes, and assembly refuses a mismatched overlay.

## A1.2 Canonical semantic coverage versus strength equivalence (PI-001, PI-007)

These are separate axes on every record and subclause.

| Field | Values | Meaning |
|---|---|---|
| `canonical_semantic_coverage` | FULL, PARTIAL, NONE | How much of the cited policies the claim expresses |
| `normative_strength_equivalence` | EQUIVALENT, PORTION_EQUIVALENT_WITH_REMAINDER, WEAKER_THAN_CANONICAL, STRONGER_THAN_CANONICAL, INCOMPARABLE, NOT_APPLICABLE | Whether the claim binds as strongly as the policy |
| `strength_links` | Per policy: policy tag, record modality, mechanical relation | Mechanical comparison of the modality class (binding, preference, permission) with the policy tag |
| `strength_resolution` | Code, label, note | The reviewer's reading of any mismatch or non-equivalence |

`CANONICAL_ONLY` with `WEAKER_THAN_CANONICAL` means the claim is entailed by the policy but is not equivalent to it. Reports always show the two groups separately. `per_candidate/<C>/STRENGTH_DIVERGENCES.jsonl` preserves every divergence for Step 3, with the equal-strength owner records per policy.

Resolution codes:

| Code | Label | Use | Effect on equivalence |
|---|---|---|---|
| SL | SECONDARY_LINK_ONLY | The mismatch is only against a secondary cited policy; another cited policy supplies the strength | Equivalent |
| PC | POLICY_CLAUSE_EQUIVALENT | Restates a clause stated inside the policy; the overall tag differs, the permitted behavior does not | Equivalent |
| CK | CHECK_BY_REFERENCE | A review or verification duty that checks compliance; it does not own the policy | Never counts as direct evidence |
| CR | COROLLARY_GUIDANCE | A lower-strength corollary that neither restates nor relaxes the policy | Never counts as direct evidence |
| PM | PERMISSION_WITHIN_POLICY | A MAY statement inside what the policy allows | Weaker or permission |
| AM | ADVISORY_MECHANISM | Hook, checker or configuration reminder | Weaker |
| GR | GUIDANCE_RESTATEMENT | prefer, avoid or technique wording of a stronger policy | Weaker |
| CN | CONDITIONAL_NARROWING | A condition such as 'where practical' that the policy does not have | Weaker |

Build and validator rules:

- A `CANONICAL_ONLY` record can never be STRONGER. Such a claim must be `CANONICAL_PLUS_DELTA` or `EXTRA_*`.
- A mismatch marked SAME without a resolution is a validation error.
- A WEAKER record without a weaker-kind code is a validation error.

`POLICY_COVERAGE.jsonl` adds `strength_status` (EQUIVALENT_EVIDENCE_PRESENT, ONLY_WEAKER_EVIDENCE, ONLY_STRONGER_EVIDENCE, NO_STRENGTH_EVIDENCE) next to the coverage `status`.

## A1.3 Modality of technique text (PI-008)

A reported MUST is not accepted on technique text. An unmarked positive imperative in a knowledge skill or private reference is DEFAULT unless the source says must, never or do not. Workflow-skill steps stay MUST when they are stated as required procedure.

## A1.4 Directional preference wording (PI-006)

Directional comparative wording ('prefer', 'preferable', 'often preferable', 'usually clearer') is a normative preference at SHOULD or DEFAULT, classified by the entailment test. A hedge lowers confidence and is noted; it does not make the text `NON_NORMATIVE`. Wording that states no direction stays `NON_NORMATIVE` under C5 ('useful', 'can', 'may', 'consider' with no outcome, option lists).

## A1.5 Trigger and exceptions (PI-010)

- `trigger_status` and `exceptions_status` take the values REVIEWER, ATTRIBUTED, NOT_APPLICABLE or MISSING. MISSING on a normative record is a validation error.
- Codex-only groups have no reported trigger, so the reviewer must state the condition from the source, or `NONE`.
- `UNKNOWN_NOT_REPORTED` is never carried as a value.

## A1.6 Source-quote verification (PI-009)

Every record carries `source_quote_verification`, computed by re-reading the immutable file for each evidence reference.

- **Reference status:** EXACT_RANGE_MATCH, EXACT_AFTER_WHITESPACE_NORMALIZATION, QUOTE_WITHIN_RANGE, RANGE_CHECKED_NO_QUOTE or FAILED_*.
- **Record fields:** an overall `status`, `primary_anchor_status`, the exact `primary_quote` (truncated for storage) and a hash of the full range.
- **Scope of the check:** it proves the cited text exists at the cited place. It does not prove the reading of that text is right.
- **Validation:** any FAILED status is a validation error.

## A1.7 Failed-challenge guard (PI-011)

- Challenge samples are frozen in `_decisions/<C>/CHALLENGE_SAMPLE.json`, so corrections cannot change what was challenged.
- Every challenge row has a `resolution`: NOT_NEEDED, UPHELD_WITH_FIELD_CORRECTION, RESOLVED_BY_CORRECTION, OPEN_REVIEW_FLAGGED or OPEN_UNRESOLVED.
- OPEN_UNRESOLVED is a validation error, so a failed challenge cannot coexist with a passing candidate report.
- Candidate reports state that mechanical validation does not establish semantic accuracy, and list each failed challenge with its before and after classification.

## A1.8 Challenge sampling

The challenge sample now has seven families of 3 records each: CO_EQUIVALENT, CO_WEAKER, NN, IA, EXTRA, CD and MX. A family with fewer records contributes all it has. M also has a second round drawn from records not used in round 1.
