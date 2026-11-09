# Experiment 005 / Phase 5.4 — Final closure report (addendum 2)

**Final status: CLOSED_VERIFIED, within the scope in section 2.** All 33 critical criteria are PASS, no critical blocker remains, and no effective FAIL exists on the verified host versions.

This is an append-only addendum dated 2026-11-09. It adds to, and does not replace:

- `phase54_final_acceptance_v1/FINAL_PHASE54_CLOSURE_REPORT.md` (CLOSED_CONDITIONAL, 2026-11-07)
- `phase54_cli317_host_recheck_v1/PHASE54_CLOSURE_ADDENDUM.md` (addendum 1, 2026-11-08)

Both remain valid records of what was true when they were written, and neither was edited. All paths are relative to `stage_A/reconciled/`.

## 1. Executive summary

- **The six candidates are unchanged.** M, M1, L0, L1, K0 and K1 match the frozen `phase54-final-v1` release: 448 of 448 files by SHA-256, confirmed by the authoritative verifier and by a separate per-file comparison.
- **The original hook failure no longer occurs on the current CLI.** On Claude Code 2.1.293, `onFailure: "block"` was ignored and the command ran (6 FAIL). On 2.1.317, all six candidates block, and the file system shows the operations did not run. Allow, deny, ask and Stop show no regression: 78 PASS, 0 FAIL, 19 NOT_RUN.
- **K0's hook works with a person in Claude Desktop Auto.** A person allowed one `git commit` and exactly one commit resulted (v1). On a fresh fixture, a request rejected at K0's permission card left the repository unchanged (v2). The card shows K0's own text.
- **The status has limits.** Interactive testing covered K0 only and does not prove the interactive behavior of the other five candidates. The status holds for the versions and platform in section 2.

No operator action is required for this status.

## 2. Final status and exact scope

| Area | Verified | Evidence type |
|---|---|---|
| Release | `phase54-final-v1`, six candidates, 448 files, byte-identical to Step 2 v3 | Static byte verification |
| Hook behavior, six candidates | Hook failure, allow, deny, ask (SDK approval surface answered by a harness) and Stop | Live host, headless, CLI 2.1.317 |
| Human decisions in Desktop | K0 only: one Allow (v1), one Deny (v2), for a `git commit` | Interactive, Claude Desktop 4.23118.0.0, Auto mode, CLI 2.1.317 |
| Platform | Windows 11 Pro 10.0.26200 | Environment probe |

**This status does not cover:** interactive behavior of M, M1, L0, L1 or K1; interactive terminal sessions; other CLI or Desktop versions; other operating systems; the F1 reference gate on 2.1.317; live malformed hook input; M1 timeout; or how any candidate performs on real tasks.

## 3. Original acceptance and later changes

| Date | Event | Status effect |
|---|---|---|
| 2026-11-07 | Original closure on CLI 2.1.293: release frozen, closure review 11 of 11, live pilot 36 PASS, 6 FAIL, 14 NOT_RUN | CLOSED_CONDITIONAL, for two stated reasons: hook-failure class D, and interactive NOT_RUN |
| 2026-11-08 | Recheck on CLI 2.1.317: class D passes in all six | First reason resolved; addendum 1 recommended CLOSED_VERIFIED and left interactive as a user judgment |
| 2026-11-09 | Desktop Auto v1 (K0): Allow PASS, Deny NOT_VERIFIED | Partial progress on the second reason |
| 2026-11-09 | Desktop Auto v2 (K0): Deny repeated on a fresh fixture with the card captured | Second reason addressed for K0 |
| 2026-11-09 | This reconciliation | CLOSED_VERIFIED, scoped |

## 4. Reconciliation of results

### 4.1 Original acceptance results

Retained unchanged. Closure review 11 of 11, predecessor verification 12 of 12, 448 files frozen. Live pilot on 2.1.293: A allow, B deny, C ask, E Stop and F reference gate passed; D1 failed in all six.

### 4.2 Resolved by upgrading Claude Code

HOST-01: `onFailure: "block"` was ignored on 2.1.293. Rows `M-D1`, `M1-D1`, `L0-D1`, `L1-D1`, `K0-D1` and `K1-D1` were **FAIL** on 2.1.293 and are **PASS** on 2.1.317. The synthetic rows `SYN-DX1`, `SYN-DX3` and `SYN-DX5` moved the same way. The FAIL records stay valid as facts about 2.1.293.

### 4.3 Superseded test-harness failures

Seven attempt-1 rows of the recheck failed: `SYN-DX2M` and `<C>-S-A2` for all six candidates. The test's marker command used output redirection, which the host refuses without approval even with an exact allow rule. Amendment A2 changed it to `touch`, and the affected cases were re-run in `__a2` folders. The seven FAIL rows remain in the matrix with `effective: false`.

Under that defect, "marker absent" in attempt-1 D rows proved nothing, so only attempt-2 rows are counted.

### 4.4 Genuine remaining failures

**None on the verified versions.** One behavior to keep in mind, not a failure: a hook that exits 1 without declaring `onFailure: "block"` still lets the command run (`SYN-DX2`). In the candidates only PreToolUse declares it, so a failing Stop hook ends the session normally.

### 4.5 Intentionally not run

| Item | Rows | Status | Criticality |
|---|---|---|---|
| Interactive terminal session with a person answering | 6 `IA` | NOT_RUN | Conditional on run mode; Desktop Auto is not a terminal session |
| Desktop Auto for M, M1, L0, L1, K1 | 5 candidates | NOT_RUN | Needed only if interactive mode is chosen |
| Malformed hook input, live | 6 `D2` | NOT_RUN | Host cannot be made to send it; static evidence only |
| F1 reference gate on 2.1.317 | 6 `F1` | NOT_RUN | Passed on 2.1.293; not re-verified |
| M1 timeout | 1 | NOT_RUN | M1 declares none; handling shown by L1 and synthetic cases |

None of these was converted to PASS.

### 4.6 Headless CLI versus interactive Desktop Auto

| Behavior | Headless CLI 2.1.317 | Interactive Desktop Auto |
|---|---|---|
| Candidates | All six | K0 only |
| `onFailure: "block"` | Verified | Not tested |
| Allow, deny, Stop | Verified | Not tested as separate cases |
| `ask` raised by a hook | Verified through the SDK surface | Verified: shown as a card |
| Who decided | A harness that can only deny | A person |
| Approval leading to execution | Not tested: the harness never approves | Verified once (v1) |
| Rejection leaving no commit | Verified | Verified (v1 and v2) |

The two columns are separate evidence. Neither stands in for the other.

## 5. Desktop Auto results

### 5.1 v1, Allow: PASS on the Allow path

| Requirement | Result | Evidence |
|---|---|---|
| Authentic frozen K0 hook | PASS | Transcript line 166: `hook_success`, `PreToolUse:PowerShell`, decision `ask`, K0's reason, bound to tool use `toolu_01Y71NvDWeqaJfhBB6Jfd2te`; 63 of 63 K0 files equal the frozen hashes |
| Desktop Auto on 2.1.317 | PASS | Transcript entrypoint `claude-desktop`, mode `auto`, version 2.1.317 |
| Request shown to a person | PASS, by operator statement | "Yes, confirmed", to "Was the second card shown, in Auto mode, with Allow for that one request only?" |
| Human approval of exactly one request | PASS, by operator statement | Attempt 1 rejected, attempt 2 allowed; no local rule file |
| Exactly one new commit, probe only | PASS | `d4072ec250534b8286c939ed63113e6740e9ce56`, parent `f4b37516203bc41c208ae326613b7076ab4ecc2a`, one added file, read from Git in this task |
| No frozen file changed | PASS | Re-hashed in this task |

**Retained limitation.** v1's Deny attempt stays **NOT_VERIFIED** for hook origin: the transcript holds no hook record for it, and the operator replied "First card unconfirmed". v1's `evidence/` folder is empty, its `STATE.json` was never updated, and no operator-run `t0`, `t1`, `t2` or `collect` exists. The session under test wrote the v1 report itself, in `work/desktop_auto_smoke/`. No screenshot of the Allow card exists.

### 5.2 v2, Deny: PASS

| Requirement | Result | Evidence |
|---|---|---|
| Claude Code 2.1.317, `claude-desktop`, `auto` | PASS | `collect` re-run in this task; screenshot shows `Auto` |
| Exactly one attempted `git commit` | PASS | Transcript line 78; one session for this folder |
| K0's text on the card | PASS | Screenshot, section 5.3 |
| Tool result reports user rejection | PASS | Line 80, 295.9 s after the tool call |
| Baseline HEAD `1d6630d08bdfd6d9d8c0c9daaa1c3fbb8526e194`, one commit, probe staged | PASS | `t1` re-run in this task, and three historical `t1` rows |
| No K0 file changed, no local rule file | PASS | `t1` |
| K0 project-hook state present | PASS | Absent at `t0`, present at `t1` |

### 5.3 The permission-card screenshot

- **File:** `phase54_desktop_auto_smoke_v2/evidence/k0_deny_permission_card.png`
- **SHA-256:** `27ca23bab0026bb62eae788bcee97ef7dde1c81469edc4bda48f903a2c186e92` (126,654 bytes)
- **Visible:** `Repository-changing Git command (commit)`, followed by the rest of K0's reason, on a card titled `Allow Claude to run this command?`, directly above the command box `git commit -m "chore: add desktop auto probe"`, with buttons `Deny` and `Allow once`.
- **Criterion supported:** V2-03, that K0's text is visibly associated with the tested `git commit` permission card. This is a result of visual inspection in this task.

`EVIDENCE_INDEX.md` shows how the image is tied to the transcript. **The JSONL transcript contains no K0 text for this attempt**, and this report makes no such claim.

The file was written at 12:37:45 local, 19 minutes after the rejection, so its time stamp is not its capture time. A separate earlier capture of the same waiting card reached a chat at 10:14:25.622Z, inside the waiting window. That capture is archived here as corroboration.

**What is not machine-recorded.** The v2 recording sheet is blank, so which control was pressed rests on the host's rejection record while the card was waiting. See `NC-10` in the matrix.

## 6. Why the status is CLOSED_VERIFIED

The rule: mark `CLOSED_VERIFIED` only if the required criteria are supported by genuine evidence and no critical blocker remains. Each critical row must be PASS. The result is computed by `_tools/build_package.py`, and 33 of 33 are PASS.

**The one judgment call is treating interactive tests of the other five candidates as non-critical.** The original closure carried interactive items as a manual procedure "if interactive is chosen". The v2 test instructions, written before that run, state that the v1 Allow and v2 Deny together close the Desktop Auto integration gap, and K0 was the chosen fixture. The run mode is still an undecided Iteration 006 matter.

**If you require interactive verification of all six as part of Phase 5.4, the correct status is CLOSED_CONDITIONAL**, and those five candidates are the only remaining condition.

## 7. Remaining limitations

- Each effective headless row comes from one session, on one OS and one model (Haiku 5.5), with minimal fixtures.
- Each Desktop scenario ran once. K0 only.
- The Desktop transcripts do not record a hook entry for either denied attempt; the cause is unknown.
- No process record names a test session, so which binary ran each Desktop session is shown by version and by the only 2.1.317 binary present, not at process level. See `CLI_AND_DESKTOP_ENVIRONMENT.md`.
- Trust or hooks prompts at session start were not reported.
- The v1 test session wrote its own report and read files containing K0's text, producing false matches for that text in its transcript. Only line 166 is a hook record.
- `STATE.json` in the v1 and v2 folders still reads `PREPARED_INTERACTIVE_NOT_RUN`. Both were written before the runs and were left unedited; primary records establish that the runs occurred.
- INC-01 (2026-11-08): 7 empty directories were briefly created inside `release/` and removed. No file was affected.
- The Step 3 verdict remains CONDITIONAL_GO. Its open items are unchanged, and it was not re-audited here.
- Stage A review was same-family throughout.

## 8. How this task was done

Nothing was re-run except the two permitted read-only checks. No test session, candidate, hook or setting was touched.

`check_state.py` is read-only toward `work/`, but `t1` appends to `v2/evidence/state_checks.jsonl` and `collect` adds files beside it. To leave historical evidence untouched, `_tools/run_readonly_checks.py` imported the unmodified tool and pointed its output folder at this package. `v2/evidence` was confirmed unchanged.

Protected-tree check: 37,617 files, unchanged (`_baseline/PROTECTED_VERIFY.json`).

`FRZ-03` first computed as FAIL because of a bug in this package's own builder (it compared empty lists with 0). The verifier's own verdict was UNCHANGED. The builder was corrected and rebuilt.

## 9. Package contents

`FINAL_CLOSURE_REPORT.md`, `ACCEPTANCE_MATRIX.json`, `EVIDENCE_INDEX.md`, `CLI_AND_DESKTOP_ENVIRONMENT.md`, `CANDIDATE_FREEZE_VERIFICATION.md`, `ITERATION_006_HANDOFF.md`, `FINAL_STATE.json`, `VALIDATION_REPORT.json`, `PACKAGE_MANIFEST.json`, `evidence/`, `_baseline/` and `_tools/`.

Phase 5.4 ends here. Iteration 006 was not started and needs a separate instruction.
