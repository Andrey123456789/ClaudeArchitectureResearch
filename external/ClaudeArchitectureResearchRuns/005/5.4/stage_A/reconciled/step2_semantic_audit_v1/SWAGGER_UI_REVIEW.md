# Swagger UI verification: source review (Section A)

All corrections here are **proposed**. The baseline is unchanged. Full evidence is in `AUDIT_LEDGER.jsonl` and `CORRECTION_PROPOSALS.jsonl`.

## Finding

`FG-K1-2b15ea3da2` is not `CANONICAL_ONLY`. It adds an independently falsifiable verification step. The proposed label is `CANONICAL_PLUS_DELTA`, with a workflow remainder, at `DEFAULT`.

- **Source** (`inputs/K1/output/template/.claude/skills/swagger/SKILL.md:70`): "When API behavior changes: verify controller behavior and relevant integration tests, verify response metadata, start the API when startup/composition changed, open the Development Swagger UI and confirm it loads, exercise representative endpoints when that is a meaningful check, and preserve newly verified behavior in maintained tests (`verify`)."
- **Counterexample:** a controller status code changes. Build, integration tests and the OpenAPI JSON check all pass. Startup and composition are untouched. The agent never opens the UI.

| Policy | Holds in the counterexample? | Why |
|---|---|---|
| `WF-005` [MUST] | Yes | Build and relevant tests ran |
| `API-016` [MUST] | Yes | Metadata describes the running API |
| `TST-010` [MUST] | Yes | No probe needs preserving |
| `WF-006` [DEFAULT] | Not triggered | It covers new applications and substantial startup, configuration, persistence or full-stack changes |

The K1 line still asks for the UI step, so full entailment fails.

- **Condition:** the outer trigger, API behavior changes. The step has no when-clause of its own.
- **Modality:** `DEFAULT`. It is an unmarked imperative in a knowledge skill (A1.3), not a `MUST`.
- **Why `CANONICAL_PLUS_DELTA` and not `MIXED`:** every part is one verification duty, and C2 names an extra trigger as `CANONICAL_PLUS_DELTA`. `MIXED` would also be defensible, but it would change nothing downstream.

## Comparable records, candidate by candidate

| | Trigger wording | UI wording | Form | UI step's own condition | Stored: UI record | Stored: compound record | Proposed |
|---|---|---|---|---|---|---|---|
| **M** `swagger:132-140` | When API behavior changes | open ... and confirm it loads | numbered step 4 | none | `268251a6d0` CD | `fd05eef14c` CO; its claim stops at steps 1-3 | CD kept, trigger field repaired; compound upheld |
| **M1** `swagger:117-122` | When API behavior changes | open ... and confirm it loads | run-in | none | `a876ee45ce` UN | `51dccbe9d9` CO | both CD |
| **L0** `swagger:88-90` | heading: Verification after API changes | open only | run-in | none | `084aeff176` UN | `ad2b418693` CO | both CD |
| **L1** `swagger:64` | After API behavior changes | open only | run-in | none | `de692b7c3d` UN | `a48ca2a20d` CO | both CD |
| **K0** `swagger:80-87` | heading: Verification after API changes | Open ... and confirm it loads | numbered step 5 | none | `47988fe869` UN | `9522259b92` CO | both CD |
| **K1** `swagger:70` | When API behavior changes | open ... and confirm it loads | run-in | none | no separate record | `2b15ea3da2` CO | CD |

No candidate states an exception for the UI step.

### Real differences to keep

- **Trigger breadth:** L0 and K0 say API changes. M, M1, L1 and K1 say API behavior changes.
- **Action:** L0 and L1 say open. M, M1, K0 and K1 add confirm it loads.
- **Form:** M and K0 use numbered lists, so no when-clause can reach across items. M1, L0, L1 and K1 use a run-in series.

### Labeling inconsistencies, not source differences

- M and K0 have the same numbered form. M was CD and K0 was UNCERTAIN, with the note that the reach could not be decided from the list.
- K1 and M1 have the same run-in wording. K1 was CO and M1 was UNCERTAIN. `COVERAGE_LIMITATIONS.md` attributes this to K1 having no separate reported record, which is a Step 1 accident, not a text difference.
- The compound records in M1, L0, L1 and K0 were CO on a "conditional reading", yet their claims name the UI step.

## Reach of the condition

Run-in forms leave one alternative reading: start the API on a startup change, then open the UI, so the UI step would apply only then. I did not keep that reading as the main one, for three reasons:

1. Each conditional item carries its own when-clause; the UI item has none.
2. The next item, exercising endpoints when meaningful, also needs a running API. So running the API is not confined to startup changes.
3. `verify` separately covers the UI at startup in all six. The narrow reading would leave this step redundant.

Confidence is HIGH for K0's numbered list and MEDIUM for the run-in forms. The alternative stays recorded in `alternatives` on each record. This is a source reading, so the four `FUTURE_HUMAN_DECISIONS` entries on it are not human policy questions (`FHD_REVIEW.jsonl`). Authors could confirm, but nothing depends on a policy choice.

## The startup smoke clause is separate

Each candidate also lists a UI check in its runtime smoke step, under `WF-006`'s trigger and an as-applicable hedge. All were upheld as CO. K1, L0 and K0 say "Swagger UI loads when the API exposes it"; M says "expected to expose it"; M1 says "reachable when expected"; L1 says "the Development API documentation UI loads when the stack exposes one".

One limit: the list instantiates `WF-006`'s "key composition surfaces" and does not follow from it by strict logic. All six share this form, so it does not separate them. The evidence lists of `FG-M1-b95ccac9b7`, `FG-L0-3ed43fa3b6` and `FG-M-0dcdca28e3` also include the swagger skill range, which belongs to the other clause.

## Modality coding to read with care

Sibling groups on one verify line carry different modality: `FG-M1-ae7b6c7526` MUST and `FG-M1-b95ccac9b7` DEFAULT; `FG-L0-1fbbe47cb4` MUST and `FG-L0-3ed43fa3b6` DEFAULT. M reads its version DEFAULT. Equivalence with `WF-006` is the same on all of them, so a MUST here must not count as stricter in Step 3.

## Downstream cells

| Policy | Effect in the effective view |
|---|---|
| `WF-006` | `strength_status` unchanged in all six. Equal-strength and partial witness lists each grow by one in M1, L0, L1 and K0, from the formerly UNCERTAIN UI records |
| `WF-005`, `API-016`, `TST-010` | `strength_status` and list sizes unchanged. Compound records move from `EQUIVALENT` to `PORTION_EQUIVALENT_WITH_REMAINDER`, which still counts as equal strength for the canonical part |

No coverage cell changes status. The row in `COVERAGE_LIMITATIONS.md` under known reading differences should be read as superseded by this review once the proposals are accepted.

## Scope note

The regex that built the Swagger family (`AUDIT_TARGETS.jsonl`, membership `SWAGGER_A`) matched 104 records. 25 are the comparable records above. A further 3 were decided through other lists. The other 76 mention Swagger UI on an evidence line but are not verification steps. They were triaged from that line alone, with no label review, and are marked `TRIAGED_NOT_A_VERIFICATION_STEP` in the ledger.
