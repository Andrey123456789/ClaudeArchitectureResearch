# C07-PARITY-CLOSE: declaration (contract section 2, step A)

Written before any disposition of this change. Data only: no candidate byte changes.

**Scope.** Kit 71 C07: reconcile `R13-TEST-PRIORITY`, `R19-CI-RULE-SPREAD` and `R20-DESER-FORMS` with the earlier fixes, recalculate derived counts, and check that nothing widened. Also the recommended targeted blind reread from kit 71 C06, which reads records no earlier review touched.

## Decisions

- **R13: `NO_CHANGE_VERIFIED`.** The prioritize sentence appears in M, K0 and K1. `TST-011` holds in all six through their testing rules. Kit 62 8.7: repair classification, not text, when semantics match. Re-checked on current bytes.
- **R19: `NO_CHANGE_VERIFIED`.** The CI update rule stays in all six, labelled out of practical evaluation scope. Kit 62 8.7 keeps it. CI/CD stays out of practical benchmarks.
- **R20: a data qualifier, modality unchanged.** All six deserialization lines sit in a private scan layer. M, M1, L0 and K1 mark them, K0 is an audit criterion (C05), and L1 is a list item. A qualifier says this form difference is not a strictness fact. Their stated applicability stays as it is: the M, M1, L0 and K1 lines state no condition, so writing "during a scan" into the condition would be invented precision. Delivery is already in `delivery_context`.

## Checks

The dataset counts are recomputed, not assumed from v1's 6,448. The four proposals stay proposals. No local database migration duty spread beyond K1's own text. No total in a v2 output mixes frozen and current anchors or counts `MIXED` or a partial witness as equality.

The 103 corrections and 31 original open records are reassessed only where a v2 change touched the record. The list is computed, and each overlap is read.

## Blind reread

A seeded stratified sample from records no earlier review read: 2 per label group per candidate. It is falsification, not an error rate: strata are equal-sized, and the reader is the same model family that wrote the labels and sees the claim text. A disagreement is read at source. It then becomes one claim disposition through the per-claim gate, or stays `UNRESOLVED` with both readings.

## Negative cases

A qualifier that moves a modality fails. A proposal promoted to a policy fails. A reading written after the comparison fails: its hash is logged first. A hand-typed count that differs from the recomputed one fails.

## Added after the blind reread

The comparison found one defect class, so this change gained three dispositions it did not start with. The same marked ban, "Never place frontend tests under `backend/`", is stored as `MUST_NOT` in M1, L1 and K0 and as `DEFAULT` in L0 and K1, with no text difference behind it. `C07-N1` to `C07-N3` correct those three records, one at a time, through the per-claim gate. M has no such ban and stays as it is.

A word match lists the wider class: normative records whose claim says "never" or "must not" at a soft modality. They stay as stored, with status `NOT_VERIFIED` and a sensitivity table. Relabeling by word match is the mechanical closing kit 71 forbids, and the match cannot tell a marked ban from a description.
