# R25 contract 3.5: all 103 audit corrections

**Type.** CLASSIFICATION_ONLY. No template edit.

**Input.** `step2_semantic_audit_v1/CORRECTION_PROPOSALS.jsonl`, 51 PI-012-dependent, 43 frozen-protocol-supported, 9 partial-field. Output: `CORRECTION_103_ADJUDICATION.jsonl`, `OVERLAY.jsonl`.

**Method.**
- `_tools/cor103.py` re-checks each original quote in the frozen input and finds it again in the working copy.
- A PI-012-dependent row is accepted only if its modality equals the independent R01 reading of that key. Every other row needs an individual decision in `decisions.py`.
- Proposals whose text a template rule changed are restated from current source (`ACCEPT_MODIFIED`) or rejected with a counterexample.

**Result.** 79 `ACCEPT`, 20 `ACCEPT_MODIFIED`, 4 `REJECT`, 0 `UNRESOLVED`.

| Rejected | Superseded by | Why |
|---|---|---|
| `FG-K0-6bc04e6316` | R08 | The remainder the audit found is gone: the checker reads the effective value |
| `FG-M1-159a4ef4c3` | R06 | The confirmation route the proposal rested on is gone |
| `FG-K1-8c2a0fe6ef` | R09 | "Measured only" is gone |
| `FG-L0-313d81df34` | R10 | "No migration automation of any form" is gone |

**Group designations were checked, not assumed.** The 51 and 43 hold. The 9 partial-field rows are now `QUESTION_RESOLVED_BY_R02`, because register item 9.1 settled the question they kept open.

**Atomic pass.** The suite applies accepted rows one at a time and validates the candidate's whole dataset (ids, references, modality, coverage) after each one. Results: `TEST_RESULTS/R25_per_record.jsonl`. These rows touch no template, so hook and checker suites run once at the gate rather than 99 times. The contract allows this faster machine-checkable whole-dataset pass.

**The 31 open records.** Each is checked against the user's decisions in `UNRESOLVED_DECISIONS.jsonl`: HQ-01 14, non-rewritable 10, HQ-02 4, scan line 2, HQ-04 1. The source or the register resolves all 31. The 14 orphan and queue items are recorded as duplicates of the same questions.
