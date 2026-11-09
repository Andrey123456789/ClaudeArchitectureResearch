# PI-012 sensitivity on the v2 view

Recomputed from `REPAIRED_CLASSIFICATIONS.jsonl`, the v1 review files and `PI012_EXTRA_21_REVIEW.jsonl`. Label and modality counts of active top-level records, not a strictness comparison. `PI012_SENSITIVITY.md` is v1's file, kept as written.

## `R01-COMMON-VALUE`: the two readings of unmarked `only when` in knowledge text

- **Approved addendum (kept):** `only when` and `do not ... unless` without `must` or `never` are `DEFAULT` in a knowledge skill. Consequence: an agent may deviate with a concrete, reported reason, as the vocabulary of each candidate says.
- **Option D (shown, not imposed):** both forms stay binding. Consequence: the same lines become violations if not followed, including technique lines with no owner.

No source was found that contradicts the approved reading, so it stands. No coverage or strength cell moves under either reading.

| Candidate | `MUST_NOT` now | Option D adds | Triggered forms reading `only when` would remove |
|---|---:|---:|---:|
| M | 181 | 10 | 3 |
| M1 | 211 | 7 | 2 |
| L0 | 163 | 6 | 4 |
| L1 | 179 | 11 | 3 |
| K0 | 151 | 7 | 0 |
| K1 | 194 | 11 | 4 |

## `R01-TRIGGERED-CLASS`: the 21 leads

All 21 were read individually (`PI012_EXTRA_21_REVIEW.jsonl`). Kinds: AUDIT_RESTRAINT 3, CONDITIONAL_HARD 17, TRUE_BAN 1. Decisions: CHANGE 1, KEEP 20.

One lead (`FG-M1-14b23b94ae`) is a scan artifact: the `when` belongs to the next clause. The three scan restraints on `TokenValidationParameters` are addressed to the auditor and create no product prohibition.

## Not strictness facts

- Docker exclusion clause: L0, L1 store it as its own `MUST_NOT` record; M, M1, K1 hold the same clause inside a compound stored `DEFAULT`; K0 says "Keep". Record granularity.
- Custom JWT line: M, M1, L0, L1 `MUST_NOT`; K0, K1 inside a compound stored `DEFAULT`. `SEC-016` is owned elsewhere in both.
- `EnsureSuccessStatusCode` line: K0 writes "too blunt" where five write "do not". A real wording difference.
- Scrutor line: K0 writes "not worth adding" where five write "do not". A real wording difference.
- Deserialization line: all six sit in a scan layer; see `REVIEWER_SIX_READINGS.md`.

## Bounds

The scan is the same heuristic as v1: the closest sentence on knowledge-only records. A sentence it does not pick is missed. These 21 are a bound, not a census of the form.
