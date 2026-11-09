# Experiment 005 / Phase 5.4 — FAIR-02 reporting contract and CP-01 IDE0005 reproduction

## Status and authority

This task implements the user's post-Step-3 decisions. Read the completed Stage A Step 3 final report, evidence limitations and open-decision register first. Read `Benchmark_Run_Report_Contract_EN.md` and `ide0005_probe_en/README_EN.md` in full.

Run from `C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4`.

The completed `stage_A/reconciled/step2_controlled_repair_v3/` and `stage_A/reconciled/step3_six_way_strictness_v1/`, frozen originals, Codex Passes 0001–0003, all candidate templates, policy matrices and Git state are **read-only**. Never edit those inputs for this task. Write exclusively inside `stage_A/reconciled/benchmark_readiness_fair02_cp01_v1/`, except the Windows temporary test-directory created by the supplied probe. Keep all Markdown and research artifacts in English.

Do not start Stage A Step 4, a full application-generation benchmark, a new normative audit, or mass architectural alignment. No `/goal` is required.

## FAIR-01 — approved: preserve enforcement differences

The user explicitly accepted FAIR-01: retain all architecture-specific hooks, checkers, delivery/loading strategies and enforcement semantics of M, M1, L0, L1, K0 and K1. **Do not modify or harmonize them.** Record this approved disposition in `FAIR01_APPROVED_DISPOSITION.md`, together with what later benchmarks should measure: blocked/asked operations, enforcement effectiveness, false positives, retries, user intervention and usage costs. Static hook observations are not substitutes for real agent-host observations.

## FAIR-02 — implement a shared reporting contract

The user wants useful, complete final reports across many C# generation runs without excessive token cost. Implement the exact shared reporting instruction from `Benchmark_Run_Report_Contract_EN.md` as a **single external user-level benchmark instruction** identical for all six candidates. Do not change their own instructions.

1. Inspect the existing study harness/protocol without mutating it and identify the correct insertion point at equal instruction priority and timing across candidates. Preserve identical substantive engineering tasks.
2. Produce a ready-to-use reporting-instruction text file and a clear integration contract (including whether integration is already possible or merely prepared for a runner not yet implemented). Do not invent a new full benchmark runner or a large framework.
3. Final report headings: Outcome, Changes, Verification, Decisions and deviations, Risks and follow-ups. Prefer 250–500 words, but never hide important failures, missing checks or open work to meet a target.
4. Require verifiable paths and actual commands/results where available, accurate PASS/FAIL/NOT_RUN distinctions and no fabricated successes. Save terminal output, test logs, run metadata and changes independently; self-reported success is not evidence of execution.
5. Implement a separate 0–100 Report Completeness Score using the six-dimension rubric in the contract. Validate scores against archived execution evidence. `N/A` requires justification; reward accuracy rather than length.
6. Keep report quality secondary and distinct from primary code-quality metrics; record report words and approximate output-token cost where accessible, explicitly `NOT_AVAILABLE` otherwise.
7. Build lightweight synthetic checks for genuinely completed, partially completed, failed, and misleading reports. Test that fabricated PASS claims are penalized; store the evidence cases and actual check outcomes.
8. State in the protocol that this condition measures compliance with an identical **prompted** report request, not spontaneous/unprompted reporting quality. Do not silently change the baseline experimental design or previous Step 3 findings.

Outputs: `FAIR02_IMPLEMENTATION_REPORT.md`, reusable contract text, scoring rubric, minimal validation scripts/fixtures/results, and an integration note with pending runner dependencies.

## CP-01 — controlled IDE0005 experiment

Question: M and L0 configure IDE0005 as warning and `EnforceCodeStyleInBuild=true`, but M lacks `GenerateDocumentationFile=true` and L0 enables it. Distinguish build-time enforcement from `dotnet format` enforcement and actual agent compliance. Do not edit candidate templates based merely on static settings.

The kit embeds final Step 2 v3 files under `ide0005_probe_en/configs/{M,L0}`. Before the test, compare all four supplied file hashes with the authoritative v3 candidate files. The supplied `ide0005_probe_en/CONFIG_PROVENANCE_SHA256.json` records expected bytes; if a mismatch exists, STOP and investigate rather than silently swap sources.

Run the provided `ide0005_probe_en/Test-IDE0005.ps1` in an isolated Windows temporary directory, but first review the script for safety and environment assumptions. It creates minimal C# projects with identical `Source.cs` (an unused `using`) and `Probe.csproj`; it is not a benchmark execution. Confirm an **active** .NET 10 SDK (`dotnet --version`, not merely `--list-sdks`) and avoid installing packages, changing machine configuration or contacting remote package feeds. If .NET 10 is unavailable, report `NOT_RUN` with evidence; do not substitute a different SDK.

Required cases:
- **A:** M as is, `dotnet restore` + `dotnet build`.
- **B:** M as is except command-line `GenerateDocumentationFile=true` positive control (and `NoWarn=CS1591` where needed).
- **C:** L0 as is, same source and project.
- **Additional:** M `dotnet format style --verify-no-changes --diagnostics IDE0005` route.

For each case record actual SDK version, effective `EnforceCodeStyleInBuild` and `GenerateDocumentationFile` properties (query MSBuild if possible), commands, exit codes, diagnostics, relevant file hashes and unmodified original configurations, and full output logs. Never treat a warning as confirmed if it was not emitted. If expected behavior fails, investigate fixture setup, toolchain behavior and conditional properties before drawing conclusions. Distinguish a genuine bug in M's claim about build-time reporting from valid alternative enforcement in M's workflow.

**Do not edit M, L0, any other candidate, the existing Step 3 results, or research rules automatically.** For a confirmed M defect, document the smallest proposed fix and its possible side-effects and test plan for user authorization. No user choice is needed for a read-only isolated experiment.

Outputs: `CP01_IDE0005_REPRODUCTION_REPORT.md`, complete reproducible logs and factual observed-versus-expected table, plus a separate potential correction proposal only if justified.

## Execution checkpoints, validation, and handoff

Create `STATE.json` and `RESUME.md` in the dedicated output directory immediately. Checkpoint each unit and resume without repeating validated work. Keep all artifacts, reports and source code written for this task in English.

Complete only the scope above and produce:

- `FAIR01_APPROVED_DISPOSITION.md`
- `FAIR02_IMPLEMENTATION_REPORT.md`
- FAIR-02 reusable instruction, score rubric and actual synthetic test evidence
- `CP01_IDE0005_REPRODUCTION_REPORT.md`
- CP-01 build and `dotnet format` logs, or explicit NOT_RUN explanation
- `FINAL_BENCHMARK_READINESS_DECISIONS.md`
- `STATE.json`, `RESUME.md`, and a file manifest/provenance record

In the final response distinguish completed implementation, experiment-confirmed behavior, unverified claims, limited-scope readiness, and any user decision that is genuinely needed. Do not claim Step 4 or benchmark readiness is fully completed solely because FAIR-02/CP-01 passed. STOP.
