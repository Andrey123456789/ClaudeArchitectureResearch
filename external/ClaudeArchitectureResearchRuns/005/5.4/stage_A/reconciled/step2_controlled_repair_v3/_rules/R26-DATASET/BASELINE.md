# R26 contract 4: repaired derived view

**Type.** CLASSIFICATION_ONLY. No template edit. The frozen baseline stays as it is: `FROZEN_BASELINE_REFERENCE` is `step2_classification/per_candidate/*`.

**Replay.** `python -B _tools/dataset.py` builds the view in this order: baseline, R01 overlay, R15, R17, R19, R20 overlays, accepted R25 rows, claim updates (`updates.py`), added claims, R21 proposals, derived applicability, current evidence mapping, coverage recomputed from active rows. Same inputs give the same bytes, apart from the manifest timestamp.

**Crosswalk statuses** in `ORIGINAL_TO_REPAIRED_CLAIMS.jsonl`:

| Status | Meaning |
|---|---|
| `UNCHANGED` | Evidence lines unchanged |
| `MOVED` | Same text at other lines |
| `REWORDED_CONTEXT` | A cited range changed, and the claim was read and still holds on the current text |
| `REWORDED` | The claim itself was restated from current source; `claim_text_original` keeps the old text |
| `REMOVED` | The source no longer holds the claim; the row stays with `active: false` and coverage skips it |
| `ADDED` | A new independent claim under a new id (`REP-*`, `NCP-*`) |

`SPLIT` was not needed. Old ids are never reused.

**Read of changed records.** Every record citing a changed range was read: claim against the current line. The first plan restated too few. That read found 32 more that needed it:
- 12 version rules that now accept a recorded exception,
- 6 dependency-marker rules, because the marker does not reach force forms,
- 4 high-risk Git lines still saying "approved workflow",
- 10 Swagger lines still carrying the old reach question.

The remaining `REWORDED_CONTEXT` records share a range with an edit but keep their meaning.

**What is not claimed.** Coverage rows are traceability, not parity. Records outside the changed ranges were not re-read here. Applicability fields are derived (see R22).
