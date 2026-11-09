# R01 HQ-06 / PI-012: baseline and impact

**Type:** PROTOCOL plus CLASSIFICATION_ONLY. No candidate template changes.

**Target:** separate semantics and condition, source authority, modality. Equivalent `only when` and `do not unless` under equal authority and scope read the same. A bare negation is not automatically a prohibition. No technique becomes policy without owner evidence. Exact text: `PROTOCOL_PI012_APPROVED_ADDENDUM.md`.

**Source quotes:** frozen A1.3, "An unmarked positive imperative in a knowledge skill or private reference is DEFAULT unless the source says must, never or do not." `METHODOLOGY_NOTE.md` states the tension: "'Cache X only when Y' and 'do not cache X unless Y' have the same truth conditions, yet A1.3 reads one as DEFAULT and the other as MUST_NOT."

**Affected:** records only, all six candidates. 233 unique keys on the two lists, plus 30 same-class keys found by a bounded scan (`PI012_EXTENSION_REVIEW.jsonl`).

**Enforcement paths:** none. The dataset gate is `_tools/roverlay.py`, which reproduces the stored coverage rows of all six candidates exactly (`_scratch/valbase.py` run, 0 differences), so a recomputed cell is comparable to its baseline.

**Regression risks and controls:**

| Risk | Control |
|---|---|
| Bulk relabel by keyword | Each case read at source, blind first; `_rules/R01-HQ06-PI012/BLIND_HASHES.json` logs the blind files before comparison |
| Wording-only split survives | `EQUIV` groups in the suite, with a mutation test |
| Rule over-reach weakens marked prohibitions | Suite asserts marked unconditional prohibitions and approval gates stay binding |
| Unapproved extension to `do not X when Y` | Kept under A1.3, class `TRIGGERED`, alternative visible in sensitivity |
| Coverage moves silently | Recomputed after every accepted correction, and reported in `PI012_SENSITIVITY.md` |

**Shared semantics versus architecture mechanism:** the reading rule applies to source roles, which exist in all six under different file layouts. It does not touch layouts.

**Blind reading limits:** the session had seen the methodology note and examples before the blind pass, and the blind view shows the claim text written by Step 2. Blind lines were revised once before reveal, on the form rule only (`do not X when Y`), and the hash log records the final blind files. After reveal, three lines changed, each stated in `final.dec`.
