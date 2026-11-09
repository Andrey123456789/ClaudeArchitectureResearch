# C06-REVIEW-SETS: declaration (contract section 2, step A)

Written before any disposition of this change. Data only: no candidate byte changes.

**Scope.** Kit 71 C06, without its sixth reading: the six reviewer readings of v1 report section 6, the 62 `review_needed` records, the 38 coverage cells with no FULL direct witness, and the 42 added claims plus 4 proposals from v1, along with claims added later by C01 to C05. `R22-UNDER-EXTRACTION` is its own change, `C06B-R22-APPLICABILITY`, because it edits the extractor.

**Authority.** Kit 71 C06: for each item record `CONFIRMED`, `CORRECTED`, `QUALIFIED`, `UNRESOLVED` or `NOT_VERIFIED`, and why. "Do not falsely declare the remaining ~6,400 claims fully read." Kit 71 stop rules: no count is closed for its own sake.

## Atomic dispositions

One per flagged record, in `_rules/C06-REVIEW-SETS/review_needed.py`. A disposition changes the flag and records its reason. It moves no classification and no modality. A flag stays on where the question is still open, and the record then says what did not run.

The 38 cells and the added claims are read and reported; they change no record. A cell with no FULL direct witness is never called full parity.

## Executed evidence

v1's flags mostly said hook behavior was read statically. Where the script can run, this change runs it on a disposable copy, with its real input format: malformed, empty and commandless input to the six pre-tool hooks; stop hooks in L1, K0, K1; K0 reference and post-tool hooks; K1 spec forms, removal, bulk update, force, nested wrappers and reference edges; `git check-ignore` in L0, L1.

How a live host applies a decision (`onFailure`, exit code 2, deny, ask, Stop block) stays `NOT_VERIFIED`. No live host ran.

## Readings

- `R02-TASK-SCOPE`, `R02-HEADLESS-DIRTY`: read against `CLAUDE.md` in all six.
- `R04-RECORD-FORGERY`: a fixture record written by the agent is accepted by every checker, and that is reported as a limit. The text must claim no proof of who asked. No proof-of-origin test is passed, and no infrastructure is added.
- `R01-COMMON-VALUE`, `R01-TRIGGERED-CLASS`: closed by C05, with both readings shown in `PI012_SENSITIVITY_V2.md`.

## Negative cases

A flag cleared with no reading fails. An open flag cleared to reach zero fails. A partial cell called full parity fails. A proposal promoted to a shared policy fails. A disposition that changes a field it did not declare fails the per-claim gate.
