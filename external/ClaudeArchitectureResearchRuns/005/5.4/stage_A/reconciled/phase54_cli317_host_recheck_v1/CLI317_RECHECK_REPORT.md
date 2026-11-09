# Claude Code 2.1.317 live hook compatibility recheck — report

**Result.** On genuine Claude Code 2.1.317 host sessions, a failing PreToolUse hook declared with `onFailure: "block"` now blocks the operation, in all six frozen architectures. The six cases that failed under 2.1.293 all pass, and the file-system probe confirms the operations did not run. Allow, deny, ask and Stop show no regression. **Effective rows: 78 PASS, 0 FAIL, 19 NOT_RUN**, the 19 being items outside this recheck's live plan (section 7).

**Recommendation: upgrade to CLOSED_VERIFIED, bound to CLI 2.1.317.** The reasoning and the one judgment call are in `PHASE54_CLOSURE_ADDENDUM.md`.

Two things went wrong during the work and are recorded below: seven attempt-1 rows failed because of my marker command (section 5), and I briefly created empty folders inside the frozen release (section 6).

## 1. Host and method

| Item | Value |
|---|---|
| Host | Claude Code CLI **2.1.317**, SHA-256 `26b01ec2…6038` (`CLI_VERSION_AND_HASH.md`), Windows 11 Pro 10.0.26200 |
| Mode | headless `claude -p`, `--output-format stream-json --verbose --include-hook-events` |
| Model | `--model haiku`, resolved to `claude-haiku-5-5`. The model only decides to issue a command; applying hooks is host behavior. |
| Settings | `--setting-sources project`, `--strict-mcp-config`, `--no-session-persistence`, `--max-budget-usd 1`, `--tools Bash`, exact `--allowedTools` rules |
| Environment | none of the orchestrating session's CLAUDE*/ANTHROPIC* variables; `DISABLE_AUTOUPDATER=1`; TEMP inside the case folder; npm offline against `127.0.0.1:9` |
| Sessions | 51, strictly one at a time: 26 in attempt 1, 25 in attempt 2. All exited 0 with no timeout. Reported cost USD 0.12. |
| Fixtures | `runs/<CASE>/work/`: hash-verified working copies from the frozen `release/make_working_copy.py`, or synthetic one-hook projects, each with a throw-away Git repository |

Expectations were written before the first live session (`DESIGN_AND_EXPECTATIONS.md`, SHA-256 `ed1e0e9c…ed19`, logged in `STATE.json`). Two append-only amendments, each written before the cases it adds, are in `DESIGN_AMENDMENTS.md`.

## 2. Results (effective rows)

| Row | What happened in the test | M | M1 | L0 | L1 | K0 | K1 |
|---|---|---|---|---|---|---|---|
| D1 | `node` removed from PATH, frozen settings, `git status --short` | PASS | PASS | PASS | PASS | PASS | PASS |
| D1M | same session, marker command; marker absent | PASS | PASS | PASS | PASS | PASS | PASS |
| D1X | hook script exits 1, `git status --short` | PASS | PASS | PASS | PASS | PASS | PASS |
| D1XM | same session, marker command; marker absent | PASS | PASS | PASS | PASS | PASS | PASS |
| D3 / D3M | hook exceeds the declared 15 s timeout | n/a | NOT_RUN | n/a | PASS / PASS | n/a | n/a |
| S-A1 | allow: `git status --short` ran | PASS | PASS | PASS | PASS | PASS | PASS |
| S-A2 | allow: marker command ran; marker present | PASS | PASS | PASS | PASS | PASS | PASS |
| S-B1 | deny despite allow rule; npm shim never ran | PASS exit 2 | PASS deny | PASS exit 2 | PASS deny | PASS deny | PASS exit 2 |
| S-C1 | ask: permission requested, harness denied, no commit | PASS | PASS | PASS | PASS | PASS | PASS |
| S-C2 | ask with matching allow rule: still requested, denied, no commit | PASS | PASS | PASS | PASS | PASS | PASS |
| S-E1 | Stop: one block, text answer, clean end, no loop | PASS JSON | PASS JSON | PASS exit 2 | PASS JSON | PASS JSON | PASS exit 2 |

In every D1, D1X and D3 row the host's tool result reads, for example:

> `PreToolUse:Bash hook error: [node ${CLAUDE_PROJECT_DIR}/.claude/hooks/dependency-guard.mjs]: failed; blocking because onFailure is "block"`

D3 reads `timed out; blocking because onFailure is "block"`. L1's hook was cancelled after 15.29 s and 15.33 s, matching its declared budget.

**Synthetic controls (16 rows, all PASS).** These use the same five hook definitions as the 2.1.293 diagnostic, plus three more sessions:

| Case | Hook | `onFailure` | Ran? |
|---|---|---|---|
| SYN-DX1 | exit 1 | block | no |
| SYN-DX2 | exit 1 | none | **yes, marker present** |
| SYN-DX3 | executable not on PATH | block | no |
| SYN-DX4 | exit 2 | none | no |
| SYN-DX5 | 20 s sleep, 3 s timeout (cancelled at 3.31 s and 3.29 s) | block | no |
| SYN-SHIM | exit 0, no decision | none | **yes, marker and npm shim marker present** |
| SYN-ASKNONE | `ask`, `--permission-prompts none` | none | no, `permission_denied`, no stall |
| SYN-ASKHOST | `ask`, approval surface | none | no, requested and denied |

SYN-DX2 and SYN-SHIM show the marker does appear when nothing blocks it, which is what makes "marker absent" meaningful in the D rows.

## 3. Comparison with 2.1.293

| Scenario | 2.1.293 | 2.1.317 |
|---|---|---|
| Six candidates, `node` missing | **ran** (6 FAIL) | **blocked** (6 PASS) |
| exit 1 + `onFailure: block` | ran | **blocked** |
| Missing executable + `onFailure: block` | ran | **blocked** |
| Timeout + `onFailure: block` | ran | **blocked** |
| exit 1, no `onFailure` | ran | ran (unchanged) |
| exit 2 | blocked | blocked (unchanged) |

The hook events themselves did not change: the PreToolUse response is still `exit 1, outcome error`, or `cancelled` on timeout. The difference is what the host does next. Anything monitoring hook health should read the tool result, because `outcome` alone does not say whether the operation was blocked.

The change applies only where `onFailure: "block"` is declared. SYN-DX2 shows the default is still non-blocking. In the six candidates only PreToolUse declares it, so when `node` was missing the Stop hook failed (`exit 1, outcome error`) and the session ended normally.

## 4. Ask: a genuine permission decision

The SMOKE sessions used the host's real approval surface (`--permission-prompts host --permission-prompt-tool stdio`). The host stops, emits a `can_use_tool` control request and waits. Each candidate produced exactly two requests, one per `git commit`, carrying `decision_reason_type: hook`, `decision_reason_hook_event: PreToolUse` and the hook's own reason (`runs/<C>-SMOKE__a2/permission_requests.jsonl`).

**No approval was granted or simulated.** The harness can only answer deny. All 32 permission requests across both attempts were denied (`RAW_EVIDENCE_AUDIT.json`, R5), and no commit was created. A matching allow rule (S-C2) did not bypass the request.

This is the host's SDK permission surface. It is not a terminal prompt shown to a person, which remains NOT_RUN.

## 5. Failures and investigation

**Attempt 1 had 7 FAIL rows:** `SYN-DX2M` and `<C>-S-A2` for all six candidates. All expected the marker command to run, and it did not.

- **Cause.** The marker command was `echo recheck-marker > recheck_marker.txt`. The host's own permission system refused it after the hook had passed it: `Output redirection to '…recheck_marker.txt' needs approval … Claude Code asks before a shell command creates, changes or removes files there`. An exact allow rule does not cover output redirection. In SMOKE this appeared as a `can_use_tool` request with no hook reason, which the harness denied.
- **Attribution: test harness** (my choice of marker command), acting through a host permission rule. Not the CLI's hook handling and not candidate configuration.
- **Why it mattered beyond those rows.** Under those flags the marker could never have been created, so "marker absent" in the attempt-1 D rows proved nothing. The host's refusal text was valid, but I did not count those rows as file-system proof.
- **Fix.** Attempt 2 (Amendment A2) used `touch recheck_marker.txt`, added the SYN-SHIM positive control, and re-ran every affected session. Candidate files were not changed. Attempt-1 folders are preserved and stay in the matrix as superseded records (`effective: false`), with these 7 FAILs and their attribution.

A parser correction is also recorded in A2: hook events are now attributed by their `hook_started` position. The attempt-1 window also caught the previous command's response when the agent issued both commands in one turn.

## 6. Incident INC-01: empty folders created inside the frozen release

At 19:47:58 on 2026-11-08, a `cd` in my shell left the working directory inside `phase54_final_acceptance_v1/release/`, and a relative `mkdir` then created `release/stage_A/reconciled/phase54_cli317_host_recheck_v1/{_tools,_baseline,cli_identity,runs,static_precheck}`: 7 empty directories, 0 files.

I found it within a minute, confirmed there were no files inside, and removed exactly those directories with non-recursive deletes.

- **Lasting trace:** the `release/` directory's last-write time is now 2026-11-08 19:48:43, previously 2026-11-07 14:48:49. I did not reset it.
- **File contents are unaffected:** `release/verify_release.py` PASS, 448 of 448 files; `FILE_MANIFEST.json` 632 of 632 hashed entries match; no unknown entries remain in `release/`.

This was a breach of the immutability instruction, though brief and at the directory level only. My own baseline was taken after the incident, so it cannot vouch for the moment before it; the two checks above and section 8 use records made on 2026-11-07.

## 7. Not verified

| Item | Rows | Status | Effect |
|---|---|---|---|
| Interactive terminal sessions; a person approving or rejecting `ask` | 6 | NOT_RUN | Matters only if an interactive benchmark mode is chosen |
| D2 malformed hook input | 6 | NOT_RUN live | Host cannot be made to send it; static evidence only (v3 PV2-02) |
| F1 reference-command gate on 2.1.317 | 6 | NOT_RUN | Not requested. It uses the same exit 2, deny and ask mechanisms verified here, but the gate itself was not re-run |
| M1 timeout | 1 | NOT_RUN | M1 declares no timeout, and the host default is too long to bound here. Timeout handling is shown by L1-D3 and SYN-DX5 |

Further limits: one OS and one model; each effective row comes from one session; minimal fixtures. Headless modes only. The `D1X` and `D3` faults were injected into disposable copies; `D1` used unmodified frozen settings and scripts.

## 8. Preservation of predecessors and candidates

| Check | Result | Evidence |
|---|---|---|
| Frozen release | PASS, 448 files | `release/verify_release.py` |
| Final-acceptance folder vs its own manifest | 632 of 632 hashed entries match | `_baseline/PREDECESSOR_MANIFEST_CHECK.json` |
| Rest of the project vs the 2026-11-07 baseline | 14,617 of 14,617 files identical | `_baseline/COMPARE_WITH_PRIOR_KIT_BASELINE.json` |
| Whole 5.4 tree during this task | no file or directory added, removed or changed since this task's baseline (23,968 files) | `_baseline/PROTECTED_VERIFY_FINAL.json` |
| Candidate configuration | `settings.json` byte-identical to frozen in every candidate fixture; only the declared injected script differs in D1X and D3 | `RAW_EVIDENCE_AUDIT.json`, R6 |

`.claude/settings.local.json` at the project root is the only file not in the 2026-11-07 baseline. It is Claude Code's local settings file rather than research data, it was last written at 19:43:05 before this task created anything, and none of this task's tools touched it.

## 9. Side effects outside the output folder

- 51 **empty** folders under `%USERPROFILE%\.claude\projects\`, one per child session (59 to 110 folders; 0 files inside). They can be removed by the user; this task did not delete them.
- About USD 0.12 of the user's plan usage.
- No package was installed. No registry or remote repository was contacted by a test. No Git command ran outside the throw-away fixture repositories. The Claude host's own API connection is the only network use.

## 10. Files

`CLI317_RECHECK_MATRIX.jsonl` (169 rows: 97 effective, 72 superseded) · `RECHECK_TOTALS.json` · `RAW_EVIDENCE_AUDIT.json` (8 of 8) · `CLI_VERSION_AND_HASH.md` · `PHASE54_CLOSURE_ADDENDUM.md` · `DESIGN_AND_EXPECTATIONS.md`, `DESIGN_AMENDMENTS.md` · `SEQUENTIAL_RUN_LOG.txt`, `SEQUENTIAL_RUN_LOG_ATTEMPT2.txt` · `runs/<CASE>[__a2]/{stdout.jsonl, events_timestamped.jsonl, stderr.txt, permission_requests.jsonl, result.json, parsed_session.json, work/}` · `static_precheck/` (never counted as live) · `cli_identity/` · `_baseline/` · `_tools/` · `STATE.json`, `RESUME.md`, `VALIDATION_REPORT.json`, `FILE_MANIFEST.json`.
