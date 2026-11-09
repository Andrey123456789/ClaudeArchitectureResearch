# Blind reread

## Design

A seeded stratified draw (seed 20261104): 2 records per label group per candidate, 48 in all, from records no earlier review read. The groups are equal-sized, so these counts cannot be scaled to a population rate.

The first draw listed records in stratum order, and the reader knew that order, so a record's position gave away its stored group. It was viewed but not read. It is kept as `_rules/C07-PARITY-CLOSE/BLIND_PLAN_BURNED.json`, and its records were excluded from this shuffled draw.

The reader is the same model family that wrote the labels, and it sees the claim text, so this is a weak check. The reading was written and hashed before the comparison (`edfb264bf14969c70792ef320dd8584f0d905e4f6db1f52941ca92b5c7ffc014`). The hash proves the order of writing, not freedom from prior belief.

## Result

| Outcome | Records |
|---|---:|
| Agreed on group and force | 30 |
| Disagreed on group only | 10 |
| Disagreed on group and force | 8 |

Each disagreement was read at source with the stored fields and the policy text (`BLIND_REREAD_ADJUDICATION.jsonl`):

| Result | Records |
|---|---:|
| CORRECTED | 1 |
| QUALIFIED | 2 |
| STORED_UPHELD | 15 |

Most group disagreements are limits of the reading: the reader did not have the policy text, so it could not tell `CANONICAL_ONLY` from `CANONICAL_PLUS_DELTA`, or see that no policy covered a line.

## What it found

The same marked ban, "Never place frontend tests under `backend/`", was stored as `MUST_NOT` in M1, L1 and K0 and as `DEFAULT` in L0 and K1, with no text difference behind it. No coverage cell shows this. `C07-N1` to `C07-N3` correct the three records. M has no such ban: its text only says the workspace holds its tests, and that real difference stays.

## An open class it points to

`MARKED_NEVER_SOFT_MODALITY.jsonl` lists 86 active normative records whose claim says "never" or "must not" while their modality is a soft one. They were found by a word match and were not read one by one. Many are compounds such as "positive step; never X", and some are descriptions such as "never verifies". They stay as stored, with status `NOT_VERIFIED`. The contract asks for no sweep of this class, and relabeling by word match would be the mechanical closing it forbids.

If all were stored as `MUST_NOT`:

| Candidate | `MUST_NOT` now | Listed |
|---|---:|---:|
| M | 181 | 8 |
| M1 | 211 | 9 |
| L0 | 163 | 15 |
| L1 | 179 | 20 |
| K0 | 151 | 13 |
| K1 | 194 | 21 |

- Coverage or strength cells moved: 0. Coverage does not read modality, so this zero is true by construction and is not evidence of agreement.
- Records that would read `SAME` with a modality above the policy and no resolution code: 36.

**Consequence for Step 3:** do not use raw `MUST_NOT` counts as a strictness measure between candidates. Label counts carry this noise. Coverage and strength cells do not depend on it.
