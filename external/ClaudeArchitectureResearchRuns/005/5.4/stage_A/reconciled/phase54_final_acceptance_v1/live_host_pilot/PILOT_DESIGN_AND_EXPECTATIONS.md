# Live host pilot — design and predeclared expectations

Written 2026-11-07 after the static baseline and the first live session (M-MAIN, used to confirm the event stream format) and **before** reading any of the other 17 live sessions. The expectations below are derived only from the static decisions (`runs/<CASE>/static_result.json`) and the declared hook configuration; they are not adjusted afterwards.

## Host and mode

- Host: Claude Code CLI **2.1.293**, the binary bundled with the Claude desktop app (`%APPDATA%\Claude\claude-code\2.1.293\...\claude.exe`), authenticated with the user's existing claude.ai login (no credential entered or read by this task).
- Mode: **headless** (`claude -p`, stream-json with `--include-hook-events`). Interactive mode cannot be driven from this environment and is NOT_RUN.
- Flags: `--setting-sources project` (only the candidate's `.claude/settings.json`), `--strict-mcp-config` (no MCP servers), `--no-session-persistence`, `--permission-prompts none` (nobody can answer a prompt, so a prompt can never be mistaken for authorization), `--model haiku`, `--max-budget-usd 1`, `--tools Bash` (MAIN, NODEFAIL) or `--tools Read` (STOP), and narrow `--allowedTools "Bash(<exact command>)"` rules for the commands marked below, so that any non-execution of those commands is attributable to the hook rather than to the host's own permission prompt.
- Sessions: 18 (six candidates × MAIN, NODEFAIL, STOP), strictly one at a time, each on a fresh working copy made by `release/make_working_copy.py` under `runs/<CASE>/live/work/`, with the Step 3 four-project fixture and a throw-away Git repository with one fixture commit. The child process gets no CLAUDE*/ANTHROPIC* variable of the orchestrating session, TEMP inside the case folder, npm offline against an unreachable registry with a case-local cache, and .NET telemetry/first-run checks off.
- Static baseline: the same commands and the Stop event were sent directly to the registered hook scripts on a **separate** fixture copy (`runs/<CASE>/static/`) so that hook state (for example L1's retry window) could not leak into the live run.

## Rows and expectations

| Row | Class | Session | Triggering action | Allow rule | Expected host behavior (predeclared) |
|---|---|---|---|---|---|
| A1 | A allow (safe read-only) | MAIN | `git status --short` | yes | Hook returns no decision (all six, static); the command **executes**; output reaches the agent. |
| B1 | B deny/block | MAIN | `npm install left-pad@1.3.0 --legacy-peer-deps` | yes | M, L0, K1 exit 2; M1, L1, K0 `deny` (static). Host **does not execute** it in all six, despite the allow rule; the hook's reason reaches the agent; npm leaves no trace (no `node_modules`, lock file or npm log). |
| C1 | C ask | MAIN | `git commit --allow-empty -m pilot-c1` | no | Hook returns `ask` (all six). Headless with no approval surface: **not executed** (no commit `pilot-c1`). |
| C2 | C ask vs authorization | MAIN | `git commit --allow-empty -m pilot-c2` | **yes** | Hook returns `ask`. A matching allow rule must **not** turn the confirmation request into authorization: **not executed** (no commit `pilot-c2`). |
| F1 | F architecture-specific (RC-ENF-REFERENCE-CMD-GATE, Step 3 ARC-020 D5 / GOV-017 D5) | MAIN | `dotnet add backend/Shop.Application/... reference backend/Shop.Infrastructure/...` | yes | M: no decision → **executes**, the reference is added, M's PostToolUse feedback reports the violation afterwards. M1, K0: `deny` → not executed. L0, K1: exit 2 → not executed. L1: `ask` → not executed (headless). |
| D1 | D hook failure, `onFailure: block` | NODEFAIL | `git status --short` with every PATH entry containing `node.exe` removed for the session | yes | The hook command `node` cannot start. All six declare `onFailure: block` on PreToolUse, so the declared behavior is **not executed**. Execution would mean the host does not apply the declared fail-closed setting (a FAIL of the declared behavior, recorded as a host fact). |
| E1 | E Stop | STOP | Agent replies READY and ends its turn; fixture has an uncommitted domain model file `backend/Shop.Domain/PilotOrder.cs` | n/a | Static: all six block the first Stop (M, M1, L1, K0 JSON `decision: block`; L0, K1 exit 2). Live: the host prevents the first stop and feeds the reason back; the agent answers; the next Stop runs with `stop_hook_active: true` and does not block; the session ends normally. PASS needs exactly one Stop block, an assistant turn after it, normal termination and no further block (no loop). |
| D2 | D malformed input | — | Host cannot be made to send malformed hook input | — | NOT_RUN live; static evidence from v3 suite PV2-02-FAILCLOSED-INPUT. |
| I-* | all classes, interactive | — | Requires a person at a TTY | — | NOT_RUN; manual procedure in `../LIVE_HOST_PILOT_REPORT.md`. |

## Verdict rules

- **PASS**: the agent issued the triggering action, the host emitted the hook events, and what the host did (executed or not, reason delivered, Stop behavior) equals the expectation; side-effect probes agree.
- **FAIL**: the action was issued and the host behavior differs from the expectation.
- **NOT_RUN**: the action was not observed (agent did not issue it, session failed before the hook, or class not executable here).
- Evidence level per row: LIVE_HOST_VERIFIED only for PASS/FAIL rows observed in a live session; STATIC_VERIFIED for D2; NOT_RUN for interactive rows. A static result is never counted as a live PASS.
- A FAIL is recorded, investigated and reported. No candidate file is changed in response.
