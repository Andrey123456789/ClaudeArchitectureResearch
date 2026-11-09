# Final benchmark-readiness decisions — FAIR-01, FAIR-02, CP-01 (kit 76)

**Scope verdict:** the three kit-76 units are complete. **Benchmark readiness as a whole is NOT complete**: no runner exists, the live-host pilot is NOT_RUN, and Step 4 was not started. Passing FAIR-02's synthetic checks and reproducing CP-01 does not make the candidates benchmark-ready on its own.

Output folder: `stage_A/reconciled/benchmark_readiness_fair02_cp01_v1/`. No candidate template, Step 2 v3, Step 3, original input, Codex pass or kit file changed (`PROTECTED_INPUTS_VERIFICATION.json`).

## 1. Decisions and their state

| ID | Item | State | Action taken here | User decision still needed? |
|---|---|---|---|---|
| FAIR-01 | Enforcement asymmetries between M, M1, L0, L1, K0, K1 | **APPROVED by the user: preserve** | Recorded with what benchmarks must measure (`FAIR01_APPROVED_DISPOSITION.md`) | No |
| FAIR-02 | Shared prompted reporting contract + secondary score | **IMPLEMENTED, integration PREPARED** | Instruction, assembly tool, evidence schema, rubric, scorer, synthetic validation, protocol addendum (`FAIR02_IMPLEMENTATION_REPORT.md`) | No new decision. Adopt `fair02/BENCHMARK_PROTOCOL_ADDENDUM_FAIR02.md` when the benchmark protocol and runner are written. |
| CP-01 | M's IDE0005 build configuration | **EXPERIMENT DONE; no functional defect** | Reproduced on SDK 10.0.403 (`CP01_IDE0005_REPRODUCTION_REPORT.md`); correction proposal written, not applied (`CP01_CORRECTION_PROPOSAL.md`) | **Optional.** Default with no decision: option 0, leave M unchanged (consistent with FAIR-01). Decide only if you want option 1 (comment-only clarification of two M lines) in a separately versioned repair. Option 2 (add `GenerateDocumentationFile` to M) is not recommended: it would harmonize an enforcement difference FAIR-01 preserves. |
| CP-01 → Step 3 | RUN-010 D2 refinements | Recorded here only | Step 3 files unchanged; refinements in CP-01 report section 6 | No. Cite this folder in any independent review of Step 3. |

## 2. Evidence classes

**Completed implementation (this task):** FAIR-01 disposition; FAIR-02 instruction (verbatim, hash-pinned), `assemble_prompt.py`, `score_report.py`, rubric, evidence schema, protocol addendum, integration contract; CP-01 wrapper, replica harness, cross-check parser; manifest, provenance, protected-input verification.

**Experiment-confirmed behavior (this host, .NET SDK 10.0.403, minimal fixture, two identical replicates):**
- M as is: `dotnet build` emits **no** IDE0005; it emits the SDK hint `EnableGenerateDocumentationFile`.
- M + `GenerateDocumentationFile=true` (with or without `NoWarn=CS1591`): IDE0005 emitted at build.
- L0 as is: IDE0005 emitted at build.
- M: `dotnet format style --diagnostics IDE0005 --verify-no-changes` and M's verify command `dotnet format --verify-no-changes` both detect IDE0005 (exit 2) without `GenerateDocumentationFile`.
- The supplied `Test-IDE0005.ps1` cannot complete under Windows PowerShell 5.1 (stderr → `NativeCommandError`) and its IDE0005 detector gives false positives (folder name, hint text).
- FAIR-02 synthetic checks: 103/103 on attempt 3. Accurate reports 90–100 (an accurate report of a failed run scores 100); vague or failure-omitting reports 61.6–70.4; reports with false success claims 14.0–77.0 (S8 14.0, S4 17.0, R3 74.4, R4 77.0), with Verification at 0–7 of 30 in every one of them.

**Unverified (no claim made):**
- Live Claude Code host behavior of hooks, asks, denials and Stop (Step 3 Q-08) — NOT_RUN.
- Whether agents actually run `dotnet build` / `dotnet format`, read their output, or remove unused usings (agent compliance).
- IDE0005 build behavior of M1, L1, K0, K1 (source-read in Step 3 only); other warning-severity style rules in M's build.
- Scorer accuracy on real agent reports; inter-assessor agreement; real token costs (`NOT_AVAILABLE`).

**Limited-scope readiness (ready now):** the reporting instruction can be appended byte-identically to any shared task prompt; the evidence format and scorer can score archived runs; CP-01's harness can re-test any configuration change; FAIR-01 measures are defined.

## 3. Preconditions still open before measured C# benchmark runs

1. A benchmark runner and protocol: dependencies R1–R9 in `fair02/INTEGRATION_CONTRACT.md` (task prompt, launcher, provisioning, archival, harness re-execution with one shared oracle checker, report extraction, blind annotation, separate scoring, host pilot).
2. Step 3 condition 1: the minimal host pilot (`step3_six_way_strictness_v1/HOOK_AND_CHECKER_EFFECTIVE_BEHAVIOR.md` section 6) to replace NOT_RUN for ask/deny/exit 2/`onFailure`/Stop and headless `ask`.
3. Step 3 open user items Q-01, Q-02, Q-03, Q-12 (Step 3 recommended "leave"); optional data repair RD-01/RD-02; optional independent review of Step 3's challenge log.
4. Benchmark design notes from this task: log edits to `Directory.Build.props` / `.editorconfig` per candidate (M's per-build hint warning may tempt an agent to change build configuration); capture stdout and stderr separately (`dotnet format` reports on stderr).

## 4. Not done, by design

No candidate patched; no full C# benchmark or application generation; no new normative audit; no harmonization; Stage A Step 4 not started.
