# Desktop Auto hook smoke test — K0 (Experiment 005 / Phase 5.4)

Machine-readable results: [results.json](results.json)

## Outcome

| Item | Result |
|---|---|
| Deny scenario | **NOT_VERIFIED**: the commit was blocked, but the transcript does not show the first request came from the hook and the operator could not confirm the card text |
| Allow scenario | **PASS**: hook `ask` recorded for this tool call, operator confirmed the card and a one-request Allow, exactly one commit with only the probe |
| Both interactive scenarios passed | **No**: Allow passed; Deny is not verified |
| Desktop Auto integration gap closed | **Not yet** |
| Rows that failed | None |
| Rows preventing an overall PASS | R13 for attempt 1 |

`PASS`, `FAIL` and `NOT_RUN` do not fit the Deny scenario, which ran and did not fail, so it uses `NOT_VERIFIED` from the recording sheet in `RUN_INSTRUCTIONS.md`.

**Operator follow-up.** Asked whether both cards showed K0's text, in Auto mode, with Allow for one request only, the operator replied: "First card unconfirmed". R13 for attempt 1 therefore stays `NOT_VERIFIED`. Asked next whether the second card was shown, in Auto mode, with Allow for that one request only, the operator replied: "Yes, confirmed". R1, R9 and R10 are `PASS` on that statement.

**What would close it.** The Deny path cannot be closed on this fixture, which is consumed. It needs a repeat on a fresh fixture, capturing the card text or a screenshot before choosing Deny.

## What happened

All times are local (UTC+2).

| Time | Event | Source |
|---|---|---|
| 11:26:46 | Baseline: HEAD `f4b37516`, 1 commit, only `desktop_auto_probe.txt` staged | Read-only Git |
| 11:26:51 | Attempt 1: `git commit -m "chore: add desktop auto probe"` | Transcript line 124 |
| 11:27:00 | Attempt 1 rejected, 9.7 s after the tool call | Transcript line 125 |
| 11:39:58 | Operator reports clicking DENY; Desktop showed "Stopped" | Operator, in chat |
| 11:40:31 | HEAD `f4b37516`, 1 commit, probe still staged: identical to baseline | Read-only Git |
| 11:40:56.5 | Attempt 2: same command | Transcript line 165 |
| 11:40:56.7 | K0 PreToolUse hook returned `ask` | Transcript line 166 |
| 11:41:08 | Attempt 2 succeeded, 12.4 s after the tool call: `[main d4072ec]` | Transcript line 167 |
| 11:41:40 | HEAD `d4072ec`, parent `f4b37516`, 2 commits, nothing staged | Read-only Git |

## Hook decisions versus ordinary Auto-mode permissions

| | Attempt 1 (Deny) | Attempt 2 (Allow) |
|---|---|---|
| Hook record bound to this tool use | **None in the transcript** | **Present**: `hook_success`, `PreToolUse:PowerShell`, exit 0, 160 ms |
| Hook decision | Not recorded | `ask` |
| K0 text tied to this command | Absent | Present |
| Ordinary Auto-mode permission reason recorded | None | None |
| Result seen by the agent | Generic rejection, no reason given | Command output |

Recorded hook reason for attempt 2:

> Repository-changing Git command (commit): git commit -m chore: add desktop auto probe
> Run it only when the user explicitly requested it or pre-approved this operation and scope (CLAUDE.md § Git); procedure: `git-workflow`.

**Why attempt 1 is not credited to the hook.** The same command, tool and hook produced `ask` 14 minutes later, so a hook origin is likely. But `RUN_INSTRUCTIONS.md` requires judging the two requests separately and says a request appearing is not enough. The only rejection text the agent received is generic: "The user doesn't want to proceed with this tool use." The absence of a recorded ordinary Auto-mode reason does not prove the hook asked either.

**Finding for the experiment.** The denied attempt left no hook record in the transcript, while the allowed attempt did. The cause is unknown. Here the transcript could not establish hook origin for the denied request, which leaves the card text or a screenshot as the only source.

## Recording sheet

| # | Check | Status | Basis |
|---|---|---|---|
| R1 | Desktop Auto mode | PASS | Transcript `permissionMode` is `auto`; operator confirmed Auto mode |
| R2 | Version 2.1.317 | PASS | Transcript |
| R3 | Project hooks active | PASS | `.claude/.hook-state` present; hook record at line 166 |
| R4 | Trust or hooks prompt at start | NOT_VERIFIED | Operator-only, not reported (not in overall criteria) |
| R5 | First request shown | PASS | Operator statement; card text unknown to this session |
| R6 | Deny chosen | PASS | Operator statement |
| R7 | No new commit after Deny | PASS | In-session equivalent of `t1` |
| R8 | No retry after Deny | PASS | One tool use before the operator's continuation |
| R9 | Second request shown | PASS | Operator statement |
| R10 | Allow for one request only | PASS | Operator statement |
| R11 | One new commit, probe only | PASS | `d4072ec`, `A desktop_auto_probe.txt`, blob `53596bd8` matches staged blob |
| R12 | K0 files unchanged | PASS | `no_k0_file_changed: true` |
| R13 (attempt 1) | Request came from hook | NOT_VERIFIED | K0 text absent from transcript; operator: "First card unconfirmed" |
| R13 (attempt 2) | Request came from hook | PASS | Transcript line 166, bound by tool use id |

## Limitations

- This session cannot see the Desktop UI. Card text, buttons and clicks come only from the operator, and none are inferred here.
- `evidence/` was empty at 11:41, so there is no operator-run `t0` or `t1` record, and neither can be recreated now. R7 rests on in-session read-only commands. The `t2` criteria were evaluated with `check_state.py`'s own logic without writing to `evidence/`.
- This session read `RUN_INSTRUCTIONS.md`, `hook.cjs` and `HOOK_VERIFICATION.json`, and wrote scripts and this report, all of which contain K0's text. `check_state.py collect` will therefore list false matches in `lines_containing_k0_hook_text`. Only transcript line 166 is a hook record.
- The prompts were the operator's own, not the verbatim Prompts 0 to 2 of `RUN_INSTRUCTIONS.md`.
- The commit used the fixture's exact command, so it has no Co-Authored-By trailer.
- No hook, setting or permission rule was changed. No mode change was made by this session. This report folder is untracked and uncommitted.
