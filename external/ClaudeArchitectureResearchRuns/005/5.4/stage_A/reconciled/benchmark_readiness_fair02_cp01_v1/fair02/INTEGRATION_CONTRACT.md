# FAIR-02 integration contract — shared reporting instruction

**Status: PREPARED, not yet executable.** The instruction, prompt-assembly tool, evidence schema and scorer are ready. Experiment 005 has **no benchmark-execution runner** yet, so the instruction cannot be integrated into a running harness today. Nothing in any candidate was changed.

## 1. Existing harness and protocol (inspected read-only)

| Source | What it establishes |
|---|---|
| `005/5.2/README.md` "Execution" | A fresh Claude Desktop Code session per run; identical model and effort; **"use exactly the contents of `GOAL_PROMPT.txt`"** as the prompt for every run; no candidate-specific hints; raw output preserved; "A later benchmark-execution Claude must not see research/evaluation material." |
| `005/5.2/GOAL_PROMPT.txt`, `protocol-amendments/5.2.1–5.2.3` | The single shared user-level prompt is the experiment's channel for identical instructions; amendments are recorded as separate protocol files, never by editing raw runs. |
| `005/5.1`, `5.3` (`REFINEMENT_TASK.md`), `5.4` (`SETUP_5_4.py`, `_STAGE_A_KIT`, `stage_A/`) | Template generation, refinement and Stage A analysis only. Template tasks forbid generating an application or running a benchmark. **No runner, no benchmark task prompt and no run archive format exist.** |
| v3 candidate templates | Loaded by the host as project instructions (`CLAUDE.md`, `.claude/`). Changing them changes the architecture under test; out of bounds. |

## 2. Insertion point

| Aspect | Decision |
|---|---|
| Channel | The **first user message** of every measured run (the benchmark task prompt). This is the same channel the study already uses for identical instructions (5.2 `GOAL_PROMPT.txt`). |
| Position | Appended as the **final block** of that message: `task.rstrip() + "\n\n" + RUN_REPORT_INSTRUCTION.txt`. |
| Priority and timing | User-message priority, delivered at turn 1 before any work, identical for all six candidates. |
| Text | `fair02/RUN_REPORT_INSTRUCTION.txt`, verbatim from the contract (176 words, SHA-256 `bb17a883e947b6d259afa683d26a5cbd23343e6a02e26bf93fd239918ffe6710`, provenance in `RUN_REPORT_INSTRUCTION.provenance.json`). |
| Tool | `fair02/assemble_prompt.py --task <task> --out-dir <dir>`: verifies the instruction hash, writes one prompt per candidate, and fails unless all six are byte-identical (checked on a placeholder task: `validation/prompt_assembly_check/`). |
| Goal / Stop runs | If the runner uses a Goal loop (as in 5.2), the assembled text is the Goal prompt; the report must be the final message before the run stops. |
| Headless runs | The assembled text is the prompt argument or stdin; the final assistant message is the report. Whether headless `ask` stalls before a report is written depends on the pending host pilot (Step 3 Q-08 / S-HOST). |

Rejected alternatives: editing `CLAUDE.md`, rules, skills, hooks, settings or `SPECIFICATION.md` (changes the architectures); a system-prompt append (a different priority from the study's established channel); a follow-up "write the report" message after the agent stops (timing would depend on each agent's stopping point and adds a turn). A follow-up-prompt variant is possible only as a **separate, explicitly named condition**.

## 3. Interaction with the candidates' own instructions (unchanged)

- All six `verify` skills already ask for a report of what was actually run, using PASS / NOT RUN / NOT APPLICABLE (M `verify/SKILL.md:183`, M1 `:165`, L0 `:64`, L1 `:63`, K0 `:78`, K1 `:70`). These lines fit under **Verification**. The scorer accepts `NOT RUN`, `NOT_RUN`, `NOT APPLICABLE` and `N/A`.
- The seven report-content extras (Step 3 RC-TXT-REPORT-*: dependency, delegated choices, settings, persistence, delivery, recorded decision, review praise) and the force vocabulary (RC-TXT-FORCE-VOCABULARY: M1 and L1 do not say that departing from a default must be reported) **stay**. They are architecture-specific and may make some candidates' reports richer in specific areas. Analyses must show RCS per dimension and per candidate and note this asymmetry, especially for D4 (decisions and deviations).
- If a candidate's own conventions produce a different layout, the run records it as is; non-compliance appears as section and readability flags.

## 4. What the agent must not see

Only `RUN_REPORT_INSTRUCTION.txt` enters the prompt. The contract file, rubric, scorer, evidence schema, Step 3 results and any mention of scoring stay outside the run workspace (5.2 rule: benchmark-execution Claude must not see research or evaluation material).

## 5. Pending runner dependencies

| # | Dependency | Needed for |
|---|---|---|
| R1 | Identical benchmark engineering task prompt(s) | Anything to append to |
| R2 | Run launcher: fresh session per run, identical model / effort / permission mode / host version; interactive vs headless decided | Equal priority and timing |
| R3 | Workspace provisioning: unchanged candidate template per run, starting snapshot hash | Diff and change evidence |
| R4 | Archival: transcript / event log, terminal output, diff, logs, `run_metadata.json` with token usage or `NOT_AVAILABLE` (`RUN_EVIDENCE_SCHEMA.md`) | Evidence independent of the report |
| R5 | Harness re-execution of build, tests and one shared oracle checker after each run (`harness_checks.json`) | Ground truth for D3; FAIR-01 measures |
| R6 | Verbatim report extraction (final assistant message → `report.md`) | Scoring input |
| R7 | Blind evidence annotation and run-code blinding | Unbiased `evidence.json` |
| R8 | Scoring and storage separate from primary metrics (`score_report.py`, assessor overrides) | Secondary metric |
| R9 | Minimal host pilot (Step 3 condition 1) | Knowing whether ask/deny/Stop let a headless run reach its report |

## 6. Protocol statement

See `BENCHMARK_PROTOCOL_ADDENDUM_FAIR02.md`. It must be adopted into the benchmark protocol **before** the first measured run.
