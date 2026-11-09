# PI-012: reading flat negatives (proposed rule)

**Status: proposal, not applied to the frozen protocol.** `CLASSIFICATION_PROTOCOL.md` and Addendum A1 are unchanged. Every correction that depends on this rule is marked `PROPOSED_PENDING_METHODOLOGY_PI012`. The decision is `HQ-06` in `HUMAN_DECISION_QUEUE.jsonl`.

## The problem

A1.3 reads an unmarked positive imperative in a knowledge skill or private reference as `DEFAULT`, "unless the source says must, never or do not". It does not say how to read a negative with none of those words: "Not retried:", "not a dumping ground", "does not appear in Application contracts", "only when". Step 2 left 79 such records at `MUST_NOT`. Several stored notes state the working rule outright ("declarative 'are not' keeps the strength"), and that is the rule PI-012 leaves open.

The marker test also has a tension. "Cache X only when Y" and "do not cache X unless Y" have the same truth conditions, yet A1.3 reads one as `DEFAULT` and the other as `MUST_NOT`. So this needs a stated rule, not a case-by-case judgment.

## Proposed rule

Answer two questions separately.

**1. Is it normative?** Mere negation is not automatically a command. Ask whether the text tells someone what to do or not do, under its actual scope. A sentence that removes an obligation prohibits nothing.

**2. What modality?** It depends on the form and on the source role. The rule applies only where A1.3 applies: knowledge skills and private references. Rule files, workflow steps, CLAUDE.md, and checkers keep their own reading. L0's rule files tag defaults explicitly, for example, so an untagged line there binds.

Always keep the actor, scope, trigger and exceptions. An `only when` condition belongs in `trigger`, not in the modality.

| Form | Example from source | Normative? | Reading | Outcome in the 79 | Needs this rule? |
|---|---|---|---|---|---|
| Elliptical prohibition | "No handler/CQRS/MediatR structures." | Yes | `MUST_NOT` at stated scope; "No X." has the force of "do not" | 11 upheld | No |
| By reference | list headed "Check-by-reference against `performance.md`"; a line pointing to its owner | Yes | Inherits the owner's force; not independent owner evidence | 9 upheld | No |
| Exception denied | "`appsettings.Development.json` is not exempt" | Yes, a scope statement | Follows the policy whose exception it denies | 2 upheld | No |
| Only-when | "`Middleware` — only when custom middleware exists." | Yes, a conditional rule | `DEFAULT`, with the condition in `trigger` | 30 corrected | Yes |
| Negative declarative | "`HybridCache` itself does not appear in Application contracts." | Yes | `DEFAULT` | 6 corrected | Yes |
| Label over a list | "Not retried: validation errors, ..." | Yes | `DEFAULT` | 6 corrected | Yes |
| Contrastive not | "not one test per trivial `Add`/`Get` method" | Yes | `DEFAULT` | 2 corrected | Yes |
| Characterization | "not a dumping ground" | Advisory | `SHOULD_NOT` | 3 corrected | Yes |
| Anti-pattern list, no owner pointer | noun phrase under Anti-patterns | Yes | `SHOULD_NOT`, as for avoid | 1 corrected | Yes |
| Comment in a sample | "# only when the project adopted formatting..." | Yes, weakly | `DEFAULT`; non-normative is the alternative | 1 corrected | Yes |
| Explicit default | "is not added by default" | Yes | `DEFAULT` under frozen rule 5 | 3 corrected | No |
| Evaluative | "not worth adding" | Yes | `SHOULD_NOT` under A1.4 | 1 corrected | No |
| Positive imperative | "Keep Docker concerns out" | Yes | `DEFAULT` under A1.3 itself | 1 corrected | No |
| Removes an obligation | "not a requirement to create every optional directory" | No | `NON_NORMATIVE` under C6 | 1 corrected | No |
| Cannot be told apart | "Untrusted payloads are not deserialized into arbitrary runtime types." after an investigate line | Unsettled | Stays open | 2 unresolved | n/a |

**Result for the 79:** 55 `CORRECT` (49 need this rule, 6 do not), 22 `UPHOLD`, 2 `UNRESOLVED`. Suggested modality: 49 `DEFAULT`, 5 `SHOULD_NOT`, 1 `NONE`, with 24 remaining `MUST_NOT`. One label changes (`FG-M1-2a030a5f1e`, CO to NN). Every row is in `PI012_NEGATIVE_MODALITY_REVIEW.jsonl`.

## Compatibility with the frozen protocol

- **C1 and A1.2:** a record read at `DEFAULT` against a `MUST_NOT` policy stays `CANONICAL_ONLY`, marked `WEAKER_THAN_CANONICAL` with code `GR`. No fixed label is redefined.
- **C5:** prescriptive technique stays normative at its implied strength. The rule refines "implied strength"; it does not change what counts as technique.
- **C6:** applied as written to text that only removes an obligation.
- **A1.3:** this extends a test that names positive imperatives to flat negatives. That is why it is an amendment and not a reading of the existing text, and why dependent corrections stay `PROPOSED`.
- **C8, C10, C15:** unaffected.

The rule binds records only through the overlay. Nothing is applied retroactively to the baseline.

## What "weaker" means in practice

The reading changes the force of the line, not what the candidate requires overall. Scenario: an agent creates a `Middleware` folder before custom middleware exists, with a stated reason.

- **At `MUST_NOT`,** that line is broken regardless of the reason.
- **At `DEFAULT`,** that line allows a reasoned deviation.
- **Either way,** `ARC-027` still applies where its owner rule states it.

For the 8 `EXTRA_PRODUCT` records there is no canonical owner to fall back on, so the difference is sharper. A `GET` that retries a validation error once breaks "Not retried:" at `MUST_NOT`, and is a reasoned deviation at `DEFAULT`.

## Alternative readings

| Option | Rule | Effect |
|---|---|---|
| **A. Do not accept** | Flat negatives stay `MUST_NOT` | 49 records of the 79 stay at the stored strength, plus `FG-K1-0e4de41164/S1` and `FG-M-fb58b46139` |
| **B. Accept as proposed** | The table above | The effective view |
| **C. Accept in part** | Keep security-content lines binding, because their content is a security condition | The lines most affected: `FG-L1-a0b4d693e7`, `FG-K0-345276aafe`, `FG-K0-0cf8d7ed7b`, `FG-K1-c7d26b5b93` stay `MUST_NOT` |
| **D. Marker equivalence** | "Only when" counts as "do not unless", always `MUST_NOT` | 30 only-when records stay; the other forms follow B |

## Sensitivity for Step 3

**Coverage: nothing moves.** Under A and B alike, all 1,176 rows keep the same `status` and `strength_status`. Each affected policy has an equal-strength owner elsewhere. `EFFECTIVE_POLICY_COVERAGE.jsonl` carries `strength_status_without_pi012` per row, and the check is mechanical.

**Modality counts do move.** `MUST_NOT` records by candidate (from `PI012_SENSITIVITY.json`):

| Candidate | Baseline | Effective view, rule not accepted | Effective view, rule accepted | Of the 79 |
|---|---:|---:|---:|---:|
| M | 195 | 194 | 186 | 10 |
| M1 | 223 | 222 | 217 | 14 |
| L0 | 173 | 173 | 167 | 8 |
| L1 | 194 | 190 | 185 | 7 |
| K0 | 168 | 166 | 149 | 30 |
| K1 | 205 | 204 | 196 | 10 |

The middle column differs from baseline because of corrections that do not need the rule. These are label counts for a sensitivity check, not a strictness comparison.

**Conclusions that would change:**

- **Any count or ranking of mandatory prohibitions.** K0 holds 30 of the 79 because it often states rules as present-tense declaratives. That is a style fact, and it would otherwise read as strictness.
- **Any statement about hard extras.** 8 `EXTRA_PRODUCT` records move from `MUST_NOT` to `DEFAULT` under the rule: M 2, M1 1, L0 1, K0 3, K1 1, L1 0. Six of them are the "Not retried" lists and the 304 line.

**Conclusions that would not change:** policy traceability, per-policy strength status, and every label except the one recorded above.

**Recommendation for Step 3:** compare semantic content first. Where a claim's force matters, read the source line and report the form. Do not rank on modality tokens until `HQ-06` is decided, or report both views.

## The 79 are a floor

The A1.3 scan skips a record when a must-like word appears anywhere in its evidence. So:

- Reading outside the list found more of the same: `FG-K1-0e4de41164/S1`, `FG-M-fb58b46139`, `FG-M-cf0b72f861`. It also found records where "does not require" was stored as a prohibition: `FG-L0-c21644a775`, `FG-L1-be0e9eb7f6`, `FG-L1-96c278fc07`, `FG-K1-05e649abd6`.
- `A13_RESIDUAL_LEADS.jsonl` lists 230 knowledge-text records at `MUST` or `MUST_NOT` where the sentence closest to the claim has no must-like word. This is a heuristic: most of the 24 I read had a marker in a neighbouring sentence or were check-by-reference items. Leads are flagged `modality_lead_a13` in the effective view. They are not findings.
