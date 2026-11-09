# RESUME — FAIR-02 + CP-01 (kit 76)

**Status: COMPLETE (2026-11-07). Stopped; Stage A Step 4 not started.** All units U0–U9 are DONE in `STATE.json`.

Task spec: `_STAGE_A_KIT/76_CLAUDE_FAIR02_CP01_TASK_EN.md`. Writes only inside this folder (plus Windows temp test folders listed in `FILE_MANIFEST.json`). Read-only and verified unchanged: step2_controlled_repair_v3, step3_six_way_strictness_v1, originals, Codex passes, candidate templates, kit (`PROTECTED_INPUTS_VERIFICATION.json`).

## Start here

1. `FINAL_BENCHMARK_READINESS_DECISIONS.md` — decisions, evidence classes, open preconditions.
2. `CP01_IDE0005_REPRODUCTION_REPORT.md`, `CP01_CORRECTION_PROPOSAL.md`.
3. `FAIR02_IMPLEMENTATION_REPORT.md`, then `fair02/`.
4. `FAIR01_APPROVED_DISPOSITION.md`.

## Re-validate (from this folder)

```
python -B _tools/protect_snapshot.py verify _baseline/PROTECTED_BASELINE_SHA256.json PROTECTED_INPUTS_VERIFICATION.json   (run from the 5.4 root with the folder prefix)
python -B _tools/manifest.py
python -B _tools/validate_task.py
```

`protect_snapshot.py` must be run from the 5.4 root: `python -B stage_A/reconciled/benchmark_readiness_fair02_cp01_v1/_tools/protect_snapshot.py verify stage_A/reconciled/benchmark_readiness_fair02_cp01_v1/_baseline/PROTECTED_BASELINE_SHA256.json stage_A/reconciled/benchmark_readiness_fair02_cp01_v1/PROTECTED_INPUTS_VERIFICATION.json`.

## Re-run experiments

- CP-01: `powershell -NoProfile -ExecutionPolicy Bypass -File _tools\cp01_evidence_harness.ps1 -KitDir ..\..\..\_STAGE_A_KIT\ide0005_probe_en -OutDir cp01\replica_harness_run3`, then `python -B _tools/cp01_tabulate.py` (reads run1/run2 only; extend it for run3).
- FAIR-02: from `fair02/validation`: `python -B run_synthetic_checks.py` (creates a new attempt folder; never overwrites), `python -B summarize_results.py`.

## Pitfalls met

- Bash heredocs in this environment collapsed `\\` in Python sources; write regex-heavy files with the editor tools.
- The Write tool turned Unicode escape sequences for a Cyrillic code-point range into literal characters; build such ranges with `chr()`.
- Windows PowerShell 5.1 + `$ErrorActionPreference='Stop'` + `2>&1` aborts on native stderr (`dotnet format` writes diagnostics to stderr).
- A temp folder named `IDE0005-Probe-…` makes `\bIDE0005\b` match every path line.
- PowerShell 5.1 `ConvertTo-Json` collapses one-element arrays unless wrapped with `@()`.
