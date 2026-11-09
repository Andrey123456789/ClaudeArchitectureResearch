# RESUME — CLI 2.1.317 live hook compatibility recheck (phase54_cli317_host_recheck_v1)

**Status: see `STATE.json` (`status`, `units`, `next_unit`).** Trust `STATE.json` and the files on disk, not chat memory. The recheck is designed to stop after delivering its evidence; it does not start Phase 5.5 or benchmarks.

Run every tool with `python -B` and absolute paths. Do not `cd` into a predecessor or release folder: that caused incident INC-01 (`CLI317_RECHECK_REPORT.md` section 6).

## Units and where the evidence lives

| Unit | Evidence | Never redo |
|---|---|---|
| S0 baseline and incident | `_baseline/` | `protect_snapshot.py snapshot` (refuses to overwrite) |
| S1 CLI identity | `cli_identity/`, `CLI_VERSION_AND_HASH.md` | — |
| S2 design | `DESIGN_AND_EXPECTATIONS.md` (hash in `STATE.json`), `DESIGN_AMENDMENTS.md` (append-only), `static_precheck/` | editing the design after a run |
| S3 failure cases, attempt 1 | `runs/<CASE>/`, `SEQUENTIAL_RUN_LOG.txt` | a live case is never re-run in place; `recheck.py` refuses existing folders |
| S4 smoke, attempt 1 | `runs/<C>-SMOKE/` | same |
| S5 investigation and attempt 2 | `runs/<CASE>__a2/`, `SEQUENTIAL_RUN_LOG_ATTEMPT2.txt`, Amendment A2 | same |
| S6 matrix and reports | `CLI317_RECHECK_MATRIX.jsonl`, `RECHECK_TOTALS.json`, `RAW_EVIDENCE_AUDIT.json`, `*.md` | — (`build_matrix.py` and `audit_raw.py` are re-runnable and read only the evidence) |
| S7 final validation | `VALIDATION_REPORT.json`, `FILE_MANIFEST.json`, `_baseline/PROTECTED_VERIFY_FINAL.json` | — |

## Re-check commands

```bash
python -B "C:/Projects/AI Learning/ClaudeArchitectureResearchRuns/005/5.4/stage_A/reconciled/phase54_cli317_host_recheck_v1/_tools/state.py" show
```

```bash
python -B "C:/Projects/AI Learning/ClaudeArchitectureResearchRuns/005/5.4/stage_A/reconciled/phase54_cli317_host_recheck_v1/_tools/audit_raw.py"
```

```bash
python -B "C:/Projects/AI Learning/ClaudeArchitectureResearchRuns/005/5.4/stage_A/reconciled/phase54_cli317_host_recheck_v1/_tools/validate_final.py"
```

## If interrupted

1. `state.py show` gives `next_unit`.
2. Continue at that unit; `recheck.py all` and `recheck.py a2` skip recorded cases and leave half-written folders for manual review.
3. Live sessions must stay sequential, one Claude Code child process at a time.
4. The identity gate must pass: exactly 2.1.317 with the pinned SHA-256. If it fails, stop and report BLOCKED; do not switch executable.

## Constraints carried

No change to inputs, Codex artifacts, Step 2, Step 3, kit 76, the final-acceptance folder or any candidate. The harness never approves a permission request. No package install or network operation other than the host's own API connection. No Git operation outside throw-away fixture repositories.
