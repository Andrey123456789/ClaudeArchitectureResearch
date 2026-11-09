# V3-D02-MODALITY86: declaration

Written before any change of this rule. Authority: kit 74 Part A.6 ("individually source-review those 86 flagged records ..., correct proved modality errors with per-rule gates, and retain unresolved ones with explicit evidence"). Data only.

**Review.** All 86 records of v2 `MARKED_NEVER_SOFT_MODALITY.jsonl` were read at source (`_adjudication/modality86/SHEET.md`, `review.py`), under Step 2 addendum A1.3 (a knowledge or reference text is DEFAULT unless the source says must, never or do not) and the v2 C07 marked-form precedent. Result: 84 UPHELD with a stated reason code, 1 QUALIFIED (L1 304 catalogue line, borderline), 1 CORRECTED. Deliverable: `MARKED_NEVER_86_REVIEW.jsonl`.

**Correction (one).** `FG-M-8b2c02178e` (M `rules/angular.md`: "Do not introduce NgModules for ordinary feature development unless an integration or legacy dependency genuinely requires them."): modality DEFAULT -> MUST_NOT. The record holds only that marked ban; no default marker governs it; M1 stores the same sentence MUST_NOT; the record was already STRONGER than FE-001. Classification CANONICAL_PLUS_DELTA, the FE-001 link and the STRONGER equivalence are unchanged, so no coverage or strength cell moves.

**Not changed.** The 84 upheld and 1 qualified records. v2's class file stays as v2 wrote it (`NOT_VERIFIED`); the v3 review is a separate file.

**Regression adaptation.** v2 `C07_PARITY_CLOSE.py` requires the stored class file to equal the class recomputed on the current view; after a correction the corrected record leaves the recomputed class. The test now recomputes the class on v2's view (the view that produced the file) and additionally requires every one of its records to have a v3 review row. Negative test: this change's suite mutation that drops a review row.
