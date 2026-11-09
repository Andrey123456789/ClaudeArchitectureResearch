# Resume instruction — Stage A Step 3 (six-way normative strictness comparison, v1)

Contract: `_STAGE_A_KIT/75_CLAUDE_STAGE_A_STEP3_SIX_WAY_STRICTNESS_TASK_EN.md` (authoritative).
Rubric: `PROTOCOL.md` (frozen; change only by a dated addendum).
Run root: `stage_A/reconciled/step3_six_way_strictness_v1/`. Write nowhere else.
Input (read-only): `stage_A/reconciled/step2_controlled_repair_v3/`.

Trust `STATE.json` and `CHECKPOINTS/`, not chat. Run every tool from the run root as `python -B _tools/<tool>.py`.

## On every resumption

1. `python -B _tools/preflight.py` — must print `PREFLIGHT PASS` including `P17-RESUME-INPUT-INTEGRITY` (inputs unchanged since the fingerprint). If it fails, stop and record the discrepancy.
2. `python -B _tools/judge.py status` — lists batches and per-policy checkpoints.

## Phase P1 (policy comparison), per batch

1. `python -B _tools/dossier.py build <B>` (only if `_dossiers/<B>.md` is missing).
2. Read `_dossiers/<B>.md` side by side; open template files for truncated or conditional owners.
3. Write `_judgments/<B>.py` with the DSL in `_tools/jdsl.py` (P, D, C).
4. `python -B _tools/judge.py check <B>` — gate B. On FAIL, fix the judgment file and re-run; every attempt stays in `VALIDATION_ATTEMPTS/`.

Never redo a batch whose policies all have checkpoints. Never change the rubric silently.
P1 is COMPLETE (196/196). `python -B _tools/state_sync.py` refreshes STATE progress from the checkpoints.

## Phase P2 (extra-obligation inventory), per chunk

1. `python -B _tools/extras.py status` — 14 chunks XC01..XC14 (797 clusters of 1,777 active extra records). Do NOT re-run `build` once decisions exist (cluster ids would shift).
2. Read `_extras/review/<XC>.md`; check sources with grep where a cluster's presence or force is unclear.
3. Write `_extras/decisions/<XC>.py`: `A([...ids or 'Xa-Xb' ranges])` accepts the proposed class; `X(id, CLASS, note, task=..., presence=..., links=[...])` decides. Every GENUINE_EXTRA_NORM needs `X` with a task.
4. `python -B _tools/extras.py check <XC>`; after all chunks, `python -B _tools/extras.py assemble` writes `EXTRA_OBLIGATIONS_SIX_WAY.jsonl`.

## Later phases

P3 `OPEN_DECISIONS_AND_SENSITIVITY.md`; P4 `HOOK_AND_CHECKER_EFFECTIVE_BEHAVIOR.md`; P5 assembly (`POLICY_SIX_WAY_MATRIX.jsonl`, `POLICY_PAIRWISE_DIFFERENCES.jsonl`, `METRIC_LINEAGE_AND_LIMITS.md`); P6 gates C/D/E (`SEMANTIC_CHALLENGE_LOG.jsonl`, `_tools/validate.py`); P7 final report, then STOP.

## Rules

1. Never write outside this folder. Every predecessor tree, the kit and `inputs/` are read-only.
2. No Git command anywhere. No benchmarks, no Step 4, no template edits.
3. Write code with Write/Edit (Bash heredocs mangle backslashes).

## Status: COMPLETE (2026-11-07)

All phases P0–P7 are done; verdict CONDITIONAL_GO (`FINAL_STAGE_A_STEP3_SIX_WAY_COMPARISON_REPORT.md`). Nothing remains to resume. To re-check the outputs read-only: `python -B _tools/preflight.py` then `python -B _tools/validate.py` (each run adds an attempt file under `VALIDATION_ATTEMPTS/` and rewrites `VALIDATION_REPORT.json`). Do not start Step 4 from this folder.
