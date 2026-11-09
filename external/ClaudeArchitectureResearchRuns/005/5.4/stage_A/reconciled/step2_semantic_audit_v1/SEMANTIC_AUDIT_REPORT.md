# Stage A / Step 2: targeted semantic audit report

Experiment 005, Phase 5.4. Audit version `step2-semantic-audit-v1`, date 2026-11-03.

## Decision

**CONDITIONAL_GO for the definitive Step 3 strictness comparison. Audit outcome: `PASS_WITH_OPEN_ISSUES`.**

| Question | Answer |
|---|---|
| May Step 3 be **prepared** now? | **Yes.** Use the effective view and its flags |
| May Step 3 state a **definitive** comparison? | **Only under the conditions below.** Claims free of them may be compared now |
| May **unresolved claims** be used as facts? | **No.** 31 records stay open, and 6 human questions are undecided |

### Conditions on a definitive comparison

1. **Decide `HQ-06` (the PI-012 rule), or report both views.** No ranking on modality or on `MUST_NOT` counts until then.
2. **Keep open questions out of strictness facts.** That covers the 31 open records in `UNRESOLVED_QUEUE.jsonl` and the 7 records under `HQ-03` and `HQ-05`, whose readings are settled but whose policy answer is not. Report all of them as open.
3. **Treat every correction as proposed.** All 103 are `PROPOSED`, none ratified. Show the baseline value wherever a conclusion turns on one.
4. **Compare content, not counts.** Compare extra fragments and read both source lines before stating a difference on a clause. CD, XW and `MIXED` can describe the same clause, and CO can hide small remainders.
5. **Do not take conditions from the `trigger` field.** On 4,617 records it reads as loading context.
6. **Do not state hook or checker runtime behavior as verified.** Nothing was executed.
7. **Do not infer parity from `DIRECT_EVIDENCE` or from `EQUIVALENT_EVIDENCE_PRESENT`.** On 50 rows, equal-strength evidence is only partial links; on 5 rows there is none.

**Why not NO_GO:** nothing read showed broad contamination. No queue item read lost a normative subclause, no dedup was wrong, all 38 overrides held, and no proposal moved a coverage cell.

**Why not plain GO:** the modality rule is undecided, some real questions are policy choices, and label drift exists that was corrected only where it was found.

## Main findings

1. **K1 Swagger UI was misread, and so were comparable records.** `FG-K1-2b15ea3da2` is `CANONICAL_PLUS_DELTA`, not `CANONICAL_ONLY`: the UI step is an additional `DEFAULT` obligation on every API behavior change. The contrast with M1, L0, L1 and K0 was mostly labeling. See `SWAGGER_UI_REVIEW.md`.
2. **Most of the 79 flat negatives were not prohibitions in force.** 55 are corrected (49 need the proposed rule), 22 upheld, 2 unresolved. Coverage does not move either way, but counts of hard prohibitions do. See `METHODOLOGY_NOTE.md`.
3. **The Step 1 queue sample shows no systematic loss.** 48 items were examined and the rest of the broad-narrow stratum was read as a list (76 items in that stratum): no lost subclause, no wrong dedup. The other 4,756 queue items were not reviewed.
4. **Lessons did not always propagate between candidates.** The M review's correction reached M only, and similar cases appeared elsewhere. See `DRIFT_DIAGNOSTIC.md`.
5. **Of 24 future human decisions, 20 are genuine and collapse to 4 questions.** The other 4 were source readings.

## Audit universe

Counts were recomputed from files and all matched the expected figures. 6,402 records and 1,176 coverage rows are preserved with their identities.

| Target | Expected | Found | Outcome |
|---|---:|---:|---|
| PI-012 category N | 79 | 79 | 55 correct, 22 uphold, 2 unresolved |
| Potential overmerges | 33 | 33 | All compound; stored subclauses adequate on 32, 1 local overlay |
| Coverage overrides | 38 | 38 | 35 confirmed, 3 confirmed with a qualifier |
| Strength cells | 5 | 5 | Qualifier retained on all; none `EQUIVALENT`. Disjoint from the 38 |
| Uncertain list | ~91 | 91 | 19 `UNCERTAIN`, 4 uncertain subclause, 33 LOW, 90 review-needed, overlapping |
| Orphans | 21 | 21 | 4 new clause proposals, 2 facets, 1 documented, 3 resolved, 11 duplicates of open questions |
| Future human decisions | 24 | 24 | 20 genuine (4 questions), 4 source readings |
| Independent sample | ≥24 × 5 | 120 | No shortfalls or substitutions |
| M calibration | ≥8 | 8 | All upheld |
| Queue sample | 48 | 48 | 0 lost subclauses, 0 wrong dedups |
| Drift pairs | bounded | 17 | 9 equal semantics read differently, 4 real, 4 not comparable |

The ledger holds 576 cases, unique by case, each with its list memberships. 481 have decisions. 76 were triaged as mentioning Swagger only, and 19 were compared in the drift work.

## Resolved and unresolved

| Record status in the effective view | Count |
|---|---:|
| Not audited, baseline stands (includes the 95 triaged or compared records with no decision) | 6,034 |
| Audited and upheld | 243 |
| Correction proposed | 103 |
| Unresolved, baseline kept | 22 |
| **Total** | **6,402** |

**31 records stay open:** the 22 above, plus 9 corrected records where only a field was fixed and the question remains. The ledger shows 36 `UNRESOLVED` cases because it also counts 14 orphan and queue items that duplicate those questions.

Step 2's own validator was replayed on an isolated copy inside this folder, because it writes to its own directory: 18 of 18 gates pass, and the copy was then deleted (`PREFLIGHT/VALIDATOR_REPLAY.json`). That replay is structural only.

## Corrections

103 proposals, on 103 records. Baseline files are untouched.

| By basis | Count |
|---|---:|
| Source-supported under the frozen protocol | 43 |
| Depends on the PI-012 proposal | 51 |
| Field fix, question stays open | 9 |

| By kind | Count |
|---|---:|
| Modality | 61 |
| Classification | 22 |
| Other field (trigger, remainder kind and similar) | 13 |
| Subclause split or facet | 6 |
| Strength only | 1 |

The 26 label moves below are 22 `Classification` rows plus 4 `Subclause` rows: a move to `MIXED` also adds subclauses, so it is classed there. That is why M shows 0 under `Classification` but has one label move (`FG-M-b00f9a8f1a`).

**Label moves (26):**

| From | To | Count | Records |
|---|---|---:|---|
| `CANONICAL_ONLY` | `CANONICAL_PLUS_DELTA` | 12 | 5 Swagger compounds; `FG-K0-6bc04e6316`, `FG-M1-bbde8b1664`, `FG-M1-b82958affd`, `FG-L1-f79dc1b843`, `FG-L1-51237abb7d`, `FG-K1-8c2a0fe6ef`, `FG-L0-313d81df34` |
| `UNCERTAIN` | `CANONICAL_PLUS_DELTA` | 4 | Swagger UI records in M1, L0, L1, K0 |
| `CANONICAL_ONLY` | `NON_NORMATIVE` | 4 | `FG-M1-2a030a5f1e`, `FG-K1-aeb672431c`, `FG-L0-c21644a775`, `FG-L1-be0e9eb7f6` |
| `CANONICAL_ONLY` | `MIXED` | 4 | `FG-K1-8a61b0db25`, `FG-K0-9146b82c8d`, `FG-M-b00f9a8f1a`, `FG-L1-f7f4433e5e` |
| `CANONICAL_ONLY` | `EXTRA_WORKFLOW` | 1 | `FG-K1-d5a92cb349` |
| `CANONICAL_PLUS_DELTA` | `EXTRA_PRODUCT` | 1 | `FG-L0-29a3230807` |

**Modality moves:** `MUST_NOT` to `DEFAULT` 49; to `SHOULD_NOT` 5; to `NONE` 3; to `MAY` 3; to `MIXED` 1. `MUST` to `DEFAULT` 3. `DEFAULT` to `MUST_NOT` 2 and to `MIXED` 3. `MAY` to `NONE` 1. Most reduce force, because the audit targeted over-strength lines; two raise it. This says nothing about the records not read.

**Strength moves:** `EQUIVALENT` to `WEAKER_THAN_CANONICAL` 43; to `PORTION_EQUIVALENT_WITH_REMAINDER` 6; to `STRONGER_THAN_CANONICAL` 4; to not applicable 4. `WEAKER` to not applicable 5, to `INCOMPARABLE` 1. `STRONGER` to `INCOMPARABLE` 1. `PORTION_EQUIVALENT` to not applicable 1. Not applicable to `PORTION_EQUIVALENT` 4.

| Effective labels | Baseline | Effective view |
|---|---:|---:|
| `CANONICAL_ONLY` | 4180 | 4159 |
| `CANONICAL_PLUS_DELTA` | 438 | 453 |
| `EXTRA_PRODUCT` | 771 | 772 |
| `EXTRA_WORKFLOW` | 319 | 320 |
| `INTERNAL_ARCHITECTURE` | 390 | 390 |
| `MIXED` | 135 | 139 |
| `NON_NORMATIVE` | 150 | 154 |
| `UNCERTAIN` | 19 | 15 |

**Coverage:** all 1,176 rows keep their `status` and `strength_status`, with or without the PI-012 rule. Witness lists change on 92 rows. 8 rows are marked `CONDITIONALLY_SUPPORTED`: the 5 strength cells and 3 qualified overrides. No row needed `REVIEW_REQUIRED`, because recomputation changed no cell and every row keeps its baseline in `audit_overlay.baseline`. The other 1,133 unflagged rows were recomputed, not independently confirmed, and all rows carry `Traceability only. Not parity or compliance.`

## Examples

**A real addition stored as canonical.** `FG-K1-2b15ea3da2`: "open the Development Swagger UI and confirm it loads". Tests, startup and OpenAPI JSON can all pass with no UI opened, so `WF-005`, `WF-006`, `API-016` and `TST-010` hold while this step does not.

**A prohibition that prohibits nothing.** `FG-M1-2a030a5f1e` was CO at `MUST_NOT`. The source says "This is a target structure, not a requirement to create every optional directory or project immediately." It removes an obligation. Creating the directory breaks nothing.

**A stated default stored as a ban.** `FG-L1-159d2e5920`, `FG-K0-c0ccb8af1b`: "is not added by default" at `MUST_NOT`. No new rule is needed to correct these; frozen rule 5 is enough.

**A flat negative upheld.** `FG-M-340debf96e`: "No handler/CQRS/MediatR structures." Elliptical no X has the force of do not. Stays `MUST_NOT`.

**A question left open.** `FG-K0-0ef1e5ed3d`: "Untrusted payloads are not deserialized into arbitrary runtime types." It follows an "Investigate" sentence in a scan layer. It could be a product prohibition or a scan criterion, and the line does not settle which.

**A link that was only topical.** `FG-L0-29a3230807`: "Do not let CI upgrade packages automatically unless the project adopted automated dependency updates." It was CD on `WF-018`, `WF-020` and `GOV-014`, yet no part of it follows from them. Proposed as `EXTRA_PRODUCT`.

**A narrower claim stored as canonical.** `FG-K1-8c2a0fe6ef`: "fit only a measured hot path where compilation/cache lookup overhead is material". `RUN-008` also allows a clearly demonstrated need that was not measured.

## Candidate by candidate

| Candidate | Corrections | Modality | Classification | Other field | Subclause | N upheld / corrected / open | Sample: blind label agrees / modality agrees / corrected | Still open |
|---|---:|---:|---:|---:|---:|---|---|---:|
| M | 12 | 10 | 0 | 1 | 1 | 2 / 8 / 0 | 7 / 5 / 0 of 8 | 5 |
| M1 | 14 | 5 | 5 | 2 | 1 (+1 strength) | 8 / 6 / 0 | 21 / 16 / 2 of 24 | 5 |
| L0 | 15 | 7 | 5 | 3 | 0 | 2 / 6 / 0 | 18 / 17 / 2 of 24 | 4 |
| L1 | 19 | 9 | 5 | 4 | 1 | 0 / 7 / 0 | 20 / 17 / 4 of 24 | 5 |
| K0 | 26 | 20 | 3 | 2 | 1 | 8 / 20 / 2 | 21 / 16 / 0 of 24 | 7 |
| K1 | 17 | 10 | 4 | 1 | 2 | 2 / 8 / 0 | 18 / 20 / 2 of 24 | 5 |

Correction counts reflect which lists a candidate fell into, so they do not rank candidates. A blind disagreement was often a fair C2 alternative and did not imply a correction. These counts are **not an unbiased** error rate or accuracy estimate: the sample is risk-enriched and targeted.

- **M.** The three revised records hold (`FG-M-22cae42396`, `FG-M-1c4fc44b5e`, `FG-M-d0b6a09cce`), and the review's rules have not drifted. Corrections outside the calibration came from PI-012 and from comparing identical text. One label was missed: `FG-M-b00f9a8f1a`. M alone has `HQ-04` flagged, though all six have a headless sentence.
- **M1.** Check-by-reference lists are read correctly, so most flat negatives stand. `FG-M1-bbde8b1664` confused binding implementation with binding a recommendation. Its Swagger compound and UI record move together.
- **L0.** Rule files tag defaults explicitly, which supports reading untagged lines as binding (`FG-L0-3f0ff267b6` upheld). A rule line marked (default) was stored at `MUST` (`FG-L0-3f6d42031c`). The override row `GOV-007` shows equal strength through a partial witness only.
- **L1.** Most sampled corrections of any candidate, across fields, modality and label, including a dropped condition: `FG-L1-56c0d959e5` applies after a framework upgrade and to APIs that can be verified. Peer-bypass carries a real user route, which goes to `HQ-05`.
- **K0.** Holds 30 of the 79, because it often writes rules as present-tense declaratives. That is a style fact. No correction arose in its sample of 24. Its checker on CPM is broader than `DEP-006` (`FG-K0-6bc04e6316`). `API-014` and `API-019` keep their qualifiers.
- **K1.** Besides Swagger, a topical CO link (`FG-K1-d5a92cb349`) and a flattened marked negative (`FG-K1-e64089621e`). `GOV-007`, `API-014` and `API-019` keep their qualifiers. Its `GOV-007` contrast with L0 is partly a coding artifact.

## Results by section

**Uncertain list (91 unique).**

| Status | Count |
|---|---:|
| Stay open | 29 |
| Settled from the text alone | 26 |
| Label settled, hook semantics unverified | 22 |
| LOW, can only be settled by executing the hook | 14 |

The 19 `UNCERTAIN` records split into four questions. Swagger (4) is resolved. Approved workflow (10), pre-mutation invalidation (4) and headless approval (1) stay `UNCERTAIN`. The 4 uncertain subclauses all belong to the approved-workflow question and stay open.

**Coverage overrides.** Each of the 38 was checked clause by clause against named witnesses' source lines. The three qualifiers:

- `M1 WF-020`: impact and context come from a second record.
- `L0 FE-010`: its reactive-forms witness is corrected from `MUST` to `DEFAULT`.
- `L0 GOV-007`: see above.

Witness fields in `COVERAGE_OVERRIDE_REVIEW.jsonl` show stored values, with `corrected_by_audit` marking any that changed.

**Five strength cells.** K0 `API-014`, `API-019`; K1 `GOV-007`, `API-014`, `API-019`. Clause coverage holds on each. The binding witness drops the policy's normally or adds timing, and the skill lines are weaker. None is `EQUIVALENT`. All stay `STRONGER_AND_WEAKER_EVIDENCE`.

**Overmerges.** All 33 are compound, and stored subclauses separate them on 32. One local overlay is proposed: the post-hoc reminder in `FG-M1-e3684cb036`. Sampling produced a second facet (`FG-K1-e64089621e`). No Step 1 group was split.

**Orphans.** 4 new clause proposals, all low impact and separate from the 6,402: output-cache metadata in M and M1, the AAA default in M1, and a scan-scope line in L0.

**Queue.** 48 items from the 4,868 mechanically closed records, 8 per candidate, were examined one by one. Outcomes: relation correct 41, duplicates of open questions 3, label findings 3, sibling holds the remainder 1. Two of the label findings were broad-narrow items with CO on a narrower claim, so the other 64 items of that stratum were read as a list of paired claims, with no per-item decision. That added one correction (`FG-L0-313d81df34`). This is a labeling pattern, not lost content, so no area is blocked. The other 4,756 items stay mechanically recorded and unreviewed, and the absence of systematic loss applies only to the 112 read.

**Drift.** See `DRIFT_DIAGNOSTIC.md`.

## Open items

| Item | Kind | Records | Where |
|---|---|---:|---|
| `HQ-01` Approved workflow and `GOV-015` | Policy | 14 open records (10 Step 2 entries), all six | `HUMAN_DECISION_QUEUE.jsonl` |
| `HQ-02` Pre-mutation invalidation and `RUN-021` | Policy | 4; M, M1, L1, K1 | same |
| `HQ-03` Checker and `DEP-003` exception | Policy | 5, readings settled; M, M1, K1 | same |
| `HQ-04` Headless prompt approval | Policy | 1 flagged; comparable text in all six | same |
| `HQ-05` User confirmation and `DEP-025` | Policy (found here) | 2; M1, L1 | same |
| `HQ-06` PI-012 rule | Methodology | 51 dependent corrections | `METHODOLOGY_NOTE.md` |
| Non-rewritable branches | Source reading; only the authors can settle it | 10; all six | `UNRESOLVED_QUEUE.jsonl` |
| Deserialization line | Source reading | 2; K0 | `UNRESOLVED_QUEUE.jsonl` |

The non-rewritable branches matter for Step 3: do not count these as stricter than `GOV-015` until clarified.

These decisions are not for this audit to make, and they did not block it.

## Limitations

- **Reader independence is partial.** This was a fresh session, but the same model family as the original classifier, working from project memory notes on Step 2's layout.
- **The blind reading was not perfectly blind.**
  - I saw the stored fields of `FG-K1-2b15ea3da2` before writing its blind line, while learning the record schema, and the review had flagged it.
  - Target lists reveal something: the 79 are all `MUST_NOT`.
  - Sample batches kept stratum order, so a label could be guessed from position.
  - **16 of the 103 corrections have no blind line**, including 11 of the 26 label moves: 12 from drift review, 3 from queue review, 1 from a coverage witness (`source_of_decision` prefixes `F_DRIFT`, `E_QUEUE`, `C_COVERAGE`). They were read at source, knowing the stored fields. 11 of these records were outside the frozen targets altogether.
  - The log proves order of writing, not freedom from prior belief.
- **This is a bounded audit.** 6,034 records were not audited and stand as baseline. Counts here are not an unbiased estimate and do not bound errors elsewhere.
- **Corrections found by pattern were not swept.** For example, other do-not-recommend records and other narrower-as-CO records were not surveyed. `CANONICAL_ONLY` counts may still include small remainders.
- **Nothing was executed.** Hooks, checkers and settings were read statically, including host support for `onFailure`, exec-form `args`, and `decision: block`. 573 records rest on such sources (`static_only`).
- **The modality floor stands.** The 79 are not all of the flat negatives. 230 further leads are listed; 24 were read, and 3 of those were not settled.
- **The `trigger` field is weak.** The flag is heuristic. Conditions were repaired only on records corrected here.
- **The union view bounds everything.** This audit did no global extraction. Codex Pass 2 was not read and may add clauses.
- **Some effective-view fields are stale after a correction.** Free-text `rationale` and `canonical_entailment_rationale` on a corrected record still hold Step 2's words. `claim_text` is never changed, even where it overstates the source (for example never, where the source does not say it). The correction row carries the current reasoning.
- **One sample overlap.** `FG-K0-6605dc1187` was sampled while its subclause `/S2` was a PI-012 target, because the exclusion used subclause keys. Kept, not substituted, and it does not affect the frozen plan.
- **The Swagger family regex was overbroad.** It also shaped the hard exclusions, so some Swagger-mentioning records could not be sampled.

## Validation

`VALIDATION_RESULT.json` holds the 14 mechanical gates. `PREFLIGHT/TOOL_TESTS.json` holds 16 tool tests, including that a tampered correction changes the replay and that a false quote fails. A PASS means the checks hold, not that a reading is right. The open items above stand regardless.

```bash
python -B _tools/build.py
```

```bash
python -B _tools/validate.py
```

```bash
python -B _tools/test_tools.py
```

## Files

- **Start here:** this report; `SWAGGER_UI_REVIEW.md`; `METHODOLOGY_NOTE.md`; `DRIFT_DIAGNOSTIC.md`.
- **Decisions:** `AUDIT_LEDGER.jsonl`, `CORRECTION_PROPOSALS.jsonl`, `NEW_CLAUSE_PROPOSALS.jsonl`, `UNRESOLVED_QUEUE.jsonl`, `HUMAN_DECISION_QUEUE.jsonl`, `FHD_REVIEW.jsonl`.
- **List reviews:** `PI012_NEGATIVE_MODALITY_REVIEW.jsonl`, `PI012_SENSITIVITY.json`, `COVERAGE_OVERRIDE_REVIEW.jsonl`, `OVERMERGE_REVIEW.jsonl`, `ORPHAN_REVIEW.jsonl`, `QUEUE_SAMPLE_REVIEW.jsonl`, `QUEUE_BROAD_NARROW_EXTENSION.jsonl`, `SAMPLE_AGREEMENT.json`, `A13_RESIDUAL_LEADS.jsonl`.
- **Effective view (proposed, not a baseline):** `EFFECTIVE_CLASSIFICATIONS.jsonl`, `EFFECTIVE_POLICY_COVERAGE.jsonl`, `EFFECTIVE_VIEW_MANIFEST.json`.
- **Process:** `AUDIT_TARGETS.jsonl`, `SAMPLING_PLAN.json`, `UPSTREAM_MANIFEST.json`, `STATUS.json`, `CHECKPOINTS/`, `PREFLIGHT/`, `_decisions/`, `_tools/`.

## Stop

Step 3 was not started, and no unified architecture or cross-candidate strictness verdict was produced. No candidate, template, hook or Step 2 file was changed. Codex Pass 2 was neither read nor changed.
