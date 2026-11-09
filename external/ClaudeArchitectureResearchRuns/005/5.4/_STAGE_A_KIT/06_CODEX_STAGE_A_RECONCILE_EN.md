# Experiment 005 / Phase 5.4 / Stage A — Independent Reconciliation (Codex)

## Prerequisites

Run in a **new session** in `<005>/5.4`. Substitute `{{CANDIDATE}}` with exactly one candidate. The blind independent sweep in `stage_A/independent/{{CANDIDATE}}/blind/` must already be **FINALIZED**, before this session views primary results. Primary extraction must also be complete and validated.

Never rewrite or revise the blind report after reading Claude's findings. Never alter `inputs/`, `5.3`, templates, or either agent's original outputs.

## Procedure

1. Check immutable input hashes, run `py .\_STAGE_A_KIT\05_WORK_QUEUE_AND_PROGRESS.py check --root . --candidate {{CANDIDATE}}` and `py .\_STAGE_A_KIT\03_VALIDATE_STAGE_A.py --candidate {{CANDIDATE}} --root .`. Stop with explicit BLOCKED status if primary outputs are incomplete; do not fill in gaps on its behalf.
2. Compare `BLIND_FINDINGS.jsonl` against Claude's `constraints.jsonl`, `policies.jsonl` and exact `coverage_ranges.jsonl`. Independently reread original quoted file ranges to substantiate or reject each difference. Review at least the primary's extra and uncertain items for evidence errors as well.
3. For every blind finding, issue `CONFIRMED_OMISSION`, `ALREADY_CAPTURED`, `DISPUTED`, or `NEEDS_INVESTIGATION`, citing original file/line evidence and the primary segment/constraint if any. Flag incorrect `NON_NORMATIVE`/`IMPLEMENTATION`/`DUPLICATE` classifications and wrong oracle links. Also challenge primary extras that are not genuinely additional.
4. Pay special attention to constraints entirely outside the 196 or buried in executable configuration. Do not compare architectures or normalize rules: that is Stage B/C.
5. Write results **only** into `stage_A/reconciled/{{CANDIDATE}}/`.

## Deliverables

- `RECONCILIATION.jsonl` — `{ "blind_finding_id":"...", "decision":"CONFIRMED_OMISSION|ALREADY_CAPTURED|DISPUTED|NEEDS_INVESTIGATION", "primary_constraint_ids":["..."], "primary_segment_ids":["..."], "source_path":"output/template/...", "source_start_line":1, "source_end_line":2, "evidence":"verbatim quote", "rationale":"...", "action":"..." }`.
- `ADJUDICATION_BACKLOG.md` — omissions and unresolved disagreements requiring documented Stage A record amendments, plus any unsupported source surface.
- `RECONCILIATION_REPORT.md` — totals, actual validation output, issues resolved vs still open, immutable source verification.

Stage A is complete for a candidate only after each credible omission is separately adjudicated and incorporated into a **versioned correction** of the primary extraction inside 5.4, with no changes to the original blind report or source snapshot. Do not claim no missed rules can exist.
