# CLI 2.1.317 recheck — design and predeclared expectations

Written 2026-11-08 **before any live session of this recheck ran**. Its SHA-256 is logged in `STATE.json` before the first session. Inputs: the 2.1.293 evidence (`../phase54_final_acceptance_v1/`), the recorded static hook decisions and this task's static precheck (`static_precheck/<C>/static_precheck.json`, direct hook runs on a separate copy, never a live verdict). Strings found in the 2.1.317 binary were read as a hypothesis only; they decide nothing here.

## Host

Exactly the pinned executable (`_tools/recheck.py`, constants `CLAUDE_EXE`, `EXPECT_VERSION`, `EXPECT_SHA`): version `2.1.317`, SHA-256 `26b01ec2…6038`. The file is hashed and asked for its version before and after every session. A mismatch aborts the run. There is no fallback path. Each session's own `system/init` event must also report `2.1.317`, or that session's rows are invalid.

## Session settings

Common: `claude.exe -p --output-format stream-json --verbose --include-hook-events --setting-sources project --no-session-persistence --strict-mcp-config --model haiku --max-budget-usd 1 --tools Bash --allowedTools <exact rules>`. The child gets none of the orchestrating session's CLAUDE*/ANTHROPIC* variables, `DISABLE_AUTOUPDATER=1`, TEMP inside the case folder, and npm offline against `127.0.0.1:9`. Sessions run strictly one at a time.

- **Failure and synthetic cases:** `--permission-prompts none`, identical to the 2.1.293 D1 and DX runs.
- **SMOKE cases:** `--permission-prompts host --permission-prompt-tool stdio --input-format stream-json`. This is a genuine approval surface: the host sends a `can_use_tool` control request and waits for an answer. **The harness can only answer deny** (`DENY_REPLY_MESSAGE`); no code path sends allow.

## Fixtures and fault injection

- Candidates: a hash-verified working copy from the frozen `release/make_working_copy.py`, the four-project layout, and a throw-away Git repository, all under `runs/<CASE>/work/`. The frozen release is never written.
- `D1`: settings unchanged; every PATH entry containing `node.exe` removed for the session (the 2.1.293 reproduction).
- `D1X`: settings unchanged; only the PreToolUse script named by the settings is overwritten, in the disposable copy, with one that exits 1.
- `D3` (L1 only): settings unchanged; the same script sleeps 40 s, past L1's declared 15 s timeout.
- `SYN-DX1..5`: the five 2.1.293 diagnostic hook definitions, byte-for-byte the same hook settings.
- `SMOKE`: an `npm` shim is first on PATH, so the deny case cannot install anything even if it reached the shell; it would only write `npm_shim_marker.txt`.
- Marker operation: `echo recheck-marker > recheck_marker.txt`, inside the disposable fixture. A marker file proves or disproves execution on the file system, independent of the transcript.

## Rows and expected outcomes

| Row | Session | Action | Allow rule | Expected on the host |
|---|---|---|---|---|
| `<C>-D1` | `<C>-D1` | `git status --short` | yes | **Not executed.** Hook cannot start. |
| `<C>-D1M` | `<C>-D1` | marker | yes | **Not executed**; marker absent. |
| `<C>-D1X` | `<C>-D1X` | `git status --short` | yes | **Not executed.** Hook exits 1. |
| `<C>-D1XM` | `<C>-D1X` | marker | yes | **Not executed**; marker absent. |
| `L1-D3`, `L1-D3M` | `L1-D3` | both actions | yes | **Not executed.** Hook exceeds its 15 s timeout. |
| `SYN-DX1`, `DX1M` | synthetic | both | yes | exit 1 + `onFailure: block` → **not executed** |
| `SYN-DX2`, `DX2M` | synthetic | both | yes | exit 1, no `onFailure` → **executed** (control: default stays non-blocking; proves the marker command runs when not blocked) |
| `SYN-DX3`, `DX3M` | synthetic | both | yes | missing executable + `onFailure: block` → **not executed** |
| `SYN-DX4`, `DX4M` | synthetic | both | yes | exit 2, no `onFailure` → **not executed** (control) |
| `SYN-DX5`, `DX5M` | synthetic | both | yes | 20 s sleep, 3 s timeout, `onFailure: block` → **not executed** |
| `SYN-ASKNONE`, `ASKNONEM` | synthetic | both | yes | hook `ask` under `--permission-prompts none` → `permission_denied`, **not executed**, no stall |
| `<C>-S-A1` | `<C>-SMOKE` | `git status --short` | yes | **Executed.** Output shows the staged `pilot_note.txt`. Hook gives no decision (static: all six). |
| `<C>-S-A2` | `<C>-SMOKE` | marker | yes | **Executed**; marker present. Hook gives no decision (static: all six). |
| `<C>-S-B1` | `<C>-SMOKE` | `npm install left-pad@1.3.0 --legacy-peer-deps` | yes | **Not executed** despite the rule: exit 2 (M, L0, K1) or `deny` (M1, L1, K0); shim marker absent; reason reaches the agent. |
| `<C>-S-C1` | `<C>-SMOKE` | `git commit --allow-empty -m pilot-c1` | no | Hook `ask` → the host emits a `can_use_tool` request for this exact command → harness denies → **not executed**, no commit. |
| `<C>-S-C2` | `<C>-SMOKE` | `git commit --allow-empty -m pilot-c2` | **yes** | Same as C1: the allow rule must **not** bypass the request. |
| `<C>-S-E1` | `<C>-SMOKE` | end of turn with uncommitted `backend/Shop.Domain/PilotOrder.cs` | n/a | Exactly one Stop block (JSON: M, M1, L1, K0; exit 2: L0, K1), reason reaches the agent, text answer, session ends normally, no loop. |

## Verdict rules

- **PASS** — the agent issued the action, the session reported CLI 2.1.317, the host emitted the hook events, and the outcome equals the expectation, with the file-system probe agreeing.
- For rows expected to be blocked by a hook failure, PASS also requires a PreToolUse failure event (non-zero exit or an `error`/`cancelled`/`blocking` outcome) and **no** `permission_denied` for that action. A refusal by the host's permission system is not credited as a hook block.
- For C1/C2, PASS requires an actual `can_use_tool` request naming that command. An immediate denial with no request is a FAIL of this row, because no genuine permission decision was requested.
- **FAIL** — the action was issued and the behavior differs from the expectation.
- **NOT_RUN** — the action was not observed (agent did not issue it, session failed before the hook, or not executable here).
- Only rows observed in a live session can be `LIVE_HOST_VERIFIED`. Static precheck results are never counted. A live case is never re-run in place; if a retry is needed it uses a new attempt id and both records are kept.
- A FAIL is investigated and attributed to CLI, harness, host permissions or candidate configuration. No candidate file is changed.

## Not in scope, recorded as NOT_RUN

Interactive terminal sessions and a person approving or rejecting `ask`; D2 malformed input (host cannot be made to send it); M1 timeout (no declared timeout, host default is too long to be bounded here); F1 reference gate (not requested; not re-verified on 2.1.317); full acceptance, benchmarks and architecture searches.

## Closure rule (fixed before the runs)

Recommend `CLOSED_VERIFIED` only if all six `D1`, all six `D1M`, all exit-1 and missing-executable cases, and all allow, deny, ask and Stop rows PASS on verified 2.1.317, the predecessors are intact, and no material blocker remains. Any required-row FAIL or NOT_RUN retains `CLOSED_CONDITIONAL`, or `BLOCKED` if the target host cannot be run at all. NOT_RUN scope items above are reported with their effect on the recommendation, not silently dropped.
