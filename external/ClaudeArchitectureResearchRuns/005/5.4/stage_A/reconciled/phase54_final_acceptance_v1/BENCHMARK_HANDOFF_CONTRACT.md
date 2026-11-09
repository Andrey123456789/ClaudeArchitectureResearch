# Benchmark handoff contract — practical C# benchmarks on the six normalized Phase 5.4 candidates

This contract states what the next phase receives and what it must do to measure the six candidates fairly. It does not implement a runner. Every item marked **GATE** must be satisfied (or explicitly waived by the user) before the first measured run.

## 1. What is handed over

| Item | Location | Status |
|---|---|---|
| Six frozen candidates | `release/candidates/{M,M1,L0,L1,K0,K1}/template/` | 448 files, byte-identical to Step 2 v3, read-only, `release/verify_release.py` PASS |
| Release manifest and provenance | `release/CANDIDATE_FREEZE_MANIFEST.json` (+ `.sha256`), `release/RELEASE_PROVENANCE.md` | source version, policy-data version, decisions, runtime dependencies |
| Working-copy tool | `release/make_working_copy.py` | verified copy per run, provenance outside the copy |
| Reporting contract (FAIR-02) | `../benchmark_readiness_fair02_cp01_v1/fair02/` (`RUN_REPORT_INSTRUCTION.txt`, `BENCHMARK_PROTOCOL_ADDENDUM_FAIR02.md`, `INTEGRATION_CONTRACT.md`, `REPORT_COMPLETENESS_RUBRIC.md`, `RUN_EVIDENCE_SCHEMA.md`, `assemble_prompt.py`, `score_report.py`) | adopted; prompt assembly byte-identical for six (`closure_review/fair02_assembly_check/`) |
| Live host facts | `LIVE_HOST_PILOT_REPORT.md`, `LIVE_HOST_PILOT_MATRIX.jsonl` | headless, CLI 2.1.293 |
| Differences to measure | `ARCHITECTURE_DIFFERENCES_AND_LIMITS.md` §5 | preserved per FAIR-01 |

## 2. Required common tasks

1. One or more **identical** benchmark engineering task prompts (C# / .NET 10 application work within the common engineering contract), the same text for all six candidates. No candidate-specific hints.
2. Each task prompt is completed by `assemble_prompt.py` (FAIR-02 instruction appended as the final block); the assembled prompts must be byte-identical across candidates.
3. Tasks must be realistic for the shared contract (Angular SPA frontend, ASP.NET Core backend, EF Core, NUnit, CPM). CI/CD is **outside** the practical benchmark scope (decision register 8.7); tasks must not require pipeline work.
4. Tasks should be chosen so that the enforcement differences can show (dependency additions, project references, persistence/migration changes, test changes), without being designed to trigger one candidate's gate only.
5. If a task requires Git commits, the approval policy in §5 applies (approved user-authorization requirement for Git operations is preserved).

## 3. Independent execution copies

- One fresh working copy per run: `python -B release/make_working_copy.py <C> <run>/work` — never run inside `release/`.
- Record the copy's tree hash (in `<run>/work.provenance.json`) and initialize the run's own Git repository with one baseline commit, so the diff is measurable.
- Same starting fixture (if any) added identically for all six, recorded with hashes.
- Verify `release/verify_release.py` PASS before a batch and after the last run.

## 4. Shared verification oracles

- One harness-side oracle for all six, run after each session on the final workspace: `dotnet build`, `dotnet test`, `dotnet format --verify-no-changes`, frontend build/tests if in scope, plus a shared rule checker for the canonical policies under test (independent of any candidate's own checkers).
- The oracle defines primary correctness; a candidate's own hook or checker output is evidence of enforcement behavior, never of correctness.
- Capture stdout and stderr separately (`dotnet format` reports on stderr; CP-01).
- Log edits to `Directory.Build.props` and `.editorconfig` per run (M's per-build `EnableGenerateDocumentationFile` hint may tempt an agent to change build configuration; CP-01).

## 5. Session isolation and host configuration

- **GATE G2 — run mode.** Decide headless or interactive before the first run and use it for all six.
  - Headless (verified): every `ask` is denied immediately and the session continues; an allow rule does not override `ask`. A task step that needs `ask` approval (all six: Git commits; L1: project-reference commands) cannot complete. This is part of the enforcement variable and must be reported, not worked around.
  - Interactive (not verified): needs a predeclared approval policy (who answers, which answers, blind to candidate where possible) and the manual pilot in `LIVE_HOST_PILOT_REPORT.md` §7 first.
- **GATE G1 — hook health (HOST-01).** On CLI 2.1.293 a PreToolUse hook that cannot start, exits with a code other than 2, or times out lets the command run (`onFailure: block` is ignored). Required: `node` on PATH in every run environment; a per-batch preflight that runs a known-blocked command (for example B1 of the pilot) in each candidate and confirms it is refused; capture hook events (`--include-hook-events` with stream-json, or equivalent) and flag any run with a PreToolUse `outcome` of `error` or `cancelled` as **hook-degraded** (report separately; do not silently pool).
- **GATE G3 — host pin.** One Claude Code version for all runs, recorded per run; re-run the pilot (`_tools/live_pilot.py` on a scratch copy) if the version changes.
- One fresh session per run; no session resume; no shared memory between runs (`--no-session-persistence` or a fresh config directory); same model, effort and permission mode for all six; no MCP servers unless identical for all six.
- Load only project settings (`--setting-sources project` or an equivalent clean user configuration), so user-level hooks or permissions cannot leak into a candidate.
- Sequential or fully isolated parallel runs; never two sessions on one workspace.
- The agent must not see research or evaluation material (5.2 rule): no Stage A files, rubric, scorer or this contract in the workspace.
- No network beyond what the task explicitly needs; if package restore is needed, the same feed configuration for all six.

## 6. Evidence capture (per run, per `RUN_EVIDENCE_SCHEMA.md`)

Full event stream/transcript; hook events (event, decision, exit code, outcome, reason, duration); permission denials; terminal output; final workspace diff against the baseline commit; oracle results (`harness_checks.json`); the final assistant message verbatim as `report.md`; `run_metadata.json` (candidate, release id, tree hash, host version, model, effort, mode, start/end, tokens or `NOT_AVAILABLE`, cost).

## 7. Metrics

| Kind | Metric | Notes |
|---|---|---|
| **Primary** | Task correctness and C# application quality from the shared oracle (build, tests, format, rule checks, functional acceptance) | Independent of candidate hooks and reports |
| Primary | Enforcement effects (FAIR-01): interventions, blocks, asks and their resolution, retries, false positives, missed violations | Per candidate and per root; never merged into one strictness number |
| Primary | Cost and overhead: wall time, turns, tokens, hook time | |
| **Secondary** | Report Completeness Score (FAIR-02) | Shown per dimension and per candidate; never combined with primary metrics |

Scorer limits to keep in view (do not redesign in this phase): invented file paths cost little (fixture S9 with two fabricated paths still scores 96.0; −2 per unknown path, max −6); paraphrased outcome statements lose status credit (R2: 90.0, `OUTCOME_STATUS_MISSING`) and an earlier version misread a mixed count line as PASS (fixed in attempt 3; real reports may expose similar cases); keyword matching cannot judge whether an issue is described correctly; same-author validation. A blinded second assessor reviews flags before small score differences are interpreted.

No ranking may be produced from Stage A results; rankings, if any, come only from these benchmark metrics with their uncertainty.

## 8. Readiness gate summary

| Gate | Item | State now |
|---|---|---|
| G1 | Hook-health precondition and degraded-run detection (HOST-01) | **OPEN** — defined here, not implemented |
| G2 | Run mode decided; approval policy if interactive | **OPEN** (user decision) |
| G3 | Host version pinned and pilot re-run on change | Pilot done for 2.1.293 |
| G4 | Runner dependencies R1–R8 (task prompts, launcher, provisioning, archival, oracle, report extraction, blind annotation, separate scoring) | **OPEN** — no runner exists |
| G5 | R9 host pilot | **DONE for headless** (this task); interactive NOT_RUN |
| G6 | FAIR-02 protocol addendum adopted into the benchmark protocol | ready to adopt |
| G7 | Open user items Q-01, Q-02, Q-03, Q-12 (recommended: leave), optional RD-01/RD-02 data repair, optional independent review | open, non-blocking |
| G8 | Candidate timeouts (M1 none, L1 15 s) observed in real runs via hook-event durations | to be logged |

Not in scope of this contract: implementing the runner, choosing the tasks, or changing any candidate.
