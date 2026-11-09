# Protocol addendum PI-012 (approved derived addendum A2)

**Status:** approved by the user as `HQ-06` in `_STAGE_A_KIT/62_APPROVED_DECISIONS_AND_GATES_RU.md`. Derived and versioned under this run root. `step2_classification/CLASSIFICATION_PROTOCOL.md`, `PROTOCOL_ADDENDUM_A1.md` and `PROTOCOL_FREEZE.json` are not edited, and their hashes stay checked by the fence. `addendum_id = A2-PI012`, applies only to records in `REPAIRED_CANDIDATE_DERIVED_VIEW`.

**The user's decision, quoted:** «Утвердить уточнённую методику: отдельно оценивать семантику, модальность и авторитетность источника. Логически эквивалентные `only when`/`do not unless` в одинаковом нормативном контексте оценивать одинаково; не превращать технический пример в MUST_NOT по отрицательной форме. Просмотреть все 230 остаточных кандидатов, не объявляя их автоматически ошибками.»

## The three separate questions

Answer each one on its own, in this order. An answer to one never decides another.

| Axis | Question | Stored in |
|---|---|---|
| (i) Semantic constraint and logical condition | Which behaviors does the text exclude or require, and under what condition? | claim, `trigger`, `exceptions` |
| (ii) Normative authority and source role | Who speaks? Always-loaded policy, path rule, required workflow step, knowledge skill, private reference, hook or checker. Is the line an owner or does it check by reference? | `scope`, `strength_resolution`, source role |
| (iii) Modality | What force does it carry, from explicit strength wording and source role? | `modality` |

## Reading rule

1. **Negation is not force.** A negative sentence is a prohibition only if the text tells someone not to do something under its actual scope. A sentence that removes an obligation prohibits nothing (`NONE`, label `NON_NORMATIVE` under C6). A factual negative about how a mechanism behaves prohibits nothing.
2. **Logical equivalence.** `X only when Y`, `do not X unless Y` and `X requires Y` have the same truth conditions. Under equal authority and equal scope they get the same modality. The condition goes in `trigger`, never in the modality token.
3. **Force follows authority and explicit strength wording.**
   - Always-loaded policy, path rules and required workflow steps keep their own frozen reading: the candidate's vocabulary and its explicit tags apply, and an untagged rule line in a file that tags its defaults binds.
   - In a knowledge skill or private reference, an unconditional marked prohibition (`must not`, `never`, unconditional `do not`) keeps its force under A1.3. A permission-granting conditional in any equivalent form (`only when`, `only if`, `do not ... unless`, `do not ... without`) with no `must` or `never` is `DEFAULT`.
   - A triggered prohibition (`do not X when Y`, `do not X if Y`) is logically close, but its condition raises a ban instead of granting a permission, and the approved decision does not name it. It keeps A1.3 force and carries class `TRIGGERED` in `PI012_SENSITIVITY.md`, so the alternative stays visible.
   - `unless explicitly requested` or `unless approved` on a Decided choice is an approval gate (C8), not a technique condition. It keeps binding force.
   - By-reference lines inherit the owner's force, code `CK`, and never count as independent owner evidence.
4. **Technical examples and samples.** A sample, comment in a sample, or illustrative technique is not made `MUST_NOT` by its negative form. It is `DEFAULT` when it prescribes, `NONE` when it only illustrates (C5).
5. **No promotion without an owner.** Private skill technique does not become authoritative policy unless a policy or rule owner is shown. Where a rule owner states the same prohibition, the skill line restates it and the owner holds the force.
6. **Elliptical prohibitions.** `No X.` in imperative position has the force of `do not`, at its stated scope, under rule 3.
7. **Characterizations and anti-pattern nouns.** `not a dumping ground`, a noun under an anti-pattern list with no owner pointer: `SHOULD_NOT`, as for `avoid`.
8. **Security content.** Content that matters for security does not change the rule. A knowledge line on security with a rule owner restates it. Without an owner it stays `DEFAULT`, and the case is listed in `PI012_SENSITIVITY.md` as security-sensitive so a reader can see both values.
9. **Indeterminate stays indeterminate.** When the three questions cannot be answered from source, the outcome is `UNRESOLVED`. It is never forced.

## Label and coverage effect

- No fixed label is redefined. `CANONICAL_ONLY` at `DEFAULT` against a `MUST_NOT` policy stays `CANONICAL_ONLY` with `WEAKER_THAN_CANONICAL` and code `GR` (C1, A1.2). A record that loses its only normative content moves to `NON_NORMATIVE` under C6 and is listed.
- Coverage and strength are recomputed after each accepted correction, never assumed.

## What this does not do

- It does not bulk-relabel by keyword. Each case in `PI012_79_REVIEW.jsonl` and `PI012_230_REVIEW.jsonl` was read at source.
- It does not declare the 230 leads to be errors. They are leads.
- It does not change `A1.3` for unconditional marked prohibitions, or `A1.4`.
- It does not claim the reviewed set is every affected record. See the bounds in `PI012_SENSITIVITY.md`.

## Uncertainty kept

The decision names `only when` and `do not unless` as equivalent but does not spell out which common value applies in knowledge text. This addendum reads «не превращать технический пример в MUST_NOT по отрицательной форме» together with the existing A1.3 default for technique, which gives `DEFAULT` as the common value. The alternative (`MUST_NOT` for both) is the methodology note's option D. It is shown in `PI012_SENSITIVITY.md`, so the choice can be re-examined.
