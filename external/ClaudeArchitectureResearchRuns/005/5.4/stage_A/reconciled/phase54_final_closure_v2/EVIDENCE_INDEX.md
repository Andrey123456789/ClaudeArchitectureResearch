# Evidence index - Phase 5.4 final closure

All paths are relative to `stage_A/reconciled/` unless they begin with `~/`. Hashes are SHA-256, computed in this task.

## Primary sources

| Claim | Source | SHA-256 | How it establishes the claim |
|---|---|---|---|
| Release identity | `phase54_final_acceptance_v1/release/CANDIDATE_FREEZE_MANIFEST.json` | `4058f10d670ae1c2f2c02df5e5ab8dba06217d7e0181c02abb0c6a85a1c6537f` | Lists every released file with SHA-256 and size. Equals its sidecar (REL-01). |
| 448 files verified | `phase54_final_closure_v2/evidence/VERIFY_RELEASE_FINAL.json` | `94cae130f930a498b673bcdec2f6ee0d214eebe6f75bb7058ed17c87e826d432` | Output of the authoritative verifier in this task: PASS, 448 of 448, v3 comparison run (REL-02, REL-03). |
| FAIR-01 approved, preserve | `benchmark_readiness_fair02_cp01_v1/FAIR01_APPROVED_DISPOSITION.md` | `e46820de9b7d0120292856ea698bc1b14027ae840c6b6dde9020e778230641ff` | User decision that enforcement differences stay as in v3 (FRZ-01). |
| FAIR-02 external instruction | `benchmark_readiness_fair02_cp01_v1/fair02/RUN_REPORT_INSTRUCTION.txt` | `bb17a883e947b6d259afa683d26a5cbd23343e6a02e26bf93fd239918ffe6710` | The instruction text; hash recomputed and absent from all 448 templates (FRZ-02). |
| FAIR and CP-01 decisions | `benchmark_readiness_fair02_cp01_v1/FINAL_BENCHMARK_READINESS_DECISIONS.md` | `9cf3a4584862e2b6ad21257cfbad7c8df5c50bb29b56b56af3ea48b55ee79407` | State of FAIR-01, FAIR-02 and CP-01. |
| Step 3 six-way analysis | `step3_six_way_strictness_v1/FINAL_STAGE_A_STEP3_SIX_WAY_COMPARISON_REPORT.md` | `d116189a33a75096cd81057d7ea47d0b294080af9fd25f878d0b15298157a7ea` | COMPLETE, CONDITIONAL_GO, labels 165/16/15 (HIS-02). |
| Step 3 metrics | `step3_six_way_strictness_v1/METRICS.json` | `504cef889a67ccc4a75fdd9b79f274563afbbaf2fd9a4f4932ac11ac7c1a2655` | Machine-readable labels and counts. |
| Original closure | `phase54_final_acceptance_v1/FINAL_PHASE54_CLOSURE_REPORT.md` | `12055bbef0dafa992986daf9f3430934dd34ec9a7971414e527e093e8194f5a0` | CLOSED_CONDITIONAL on CLI 2.1.293. Preserved, not edited (HIS-03). |
| Original closure review | `phase54_final_acceptance_v1/closure_review/CLOSURE_REVIEW.json` | `16489043db5f372777eea236bb76e19148a912d3676fff449dd4fc6c5c16406b` | 11 of 11 PASS (HIS-01). |
| Original live pilot | `phase54_final_acceptance_v1/LIVE_HOST_PILOT_MATRIX.jsonl` | `36f5cbae3662eac7b0328dea91e33b4b8c8cf74303fa4a3b9606db692d11b696` | Six D1 FAIL rows on 2.1.293: the historical HOST-01 record (H-02). |
| Recheck matrix | `phase54_cli317_host_recheck_v1/CLI317_RECHECK_MATRIX.jsonl` | `491bd5115dd2fb6d8dc99d6d49ca98aadf30e41cb0e0004f1e8db660992e55f1` | 169 rows: 97 effective (78 PASS, 0 FAIL, 19 NOT_RUN), 72 superseded including 7 FAIL (CLI-02 to CLI-09). |
| Recheck report | `phase54_cli317_host_recheck_v1/CLI317_RECHECK_REPORT.md` | `cfdfc9b016a8b27e4d8f127cf4221e746d1176f743a839036bdf96938d82f118` | Method, 2.1.293 comparison, harness defect and INC-01. |
| Recheck amendments | `phase54_cli317_host_recheck_v1/DESIGN_AMENDMENTS.md` | `1d5403d368a4f5cd225e989ba105dc31680d8c5d301c385d38c305fd4956bfb6` | A1 and A2, written before the cases they add; A2 corrects the marker (CLI-09). |
| Recheck raw audit | `phase54_cli317_host_recheck_v1/RAW_EVIDENCE_AUDIT.json` | `22cb12b837ae8cc74327c883d0566ea1aeb5185be81a2f80a4316fa85c9a98ae` | 8 of 8 checks PASS from raw streams. |
| Executable identity | `phase54_cli317_host_recheck_v1/cli_identity/IDENTITY.json` | `500714e4b4110297c62dce94012e6e3872902907b9fc9501c86a23e73990acfe` | Path, size, SHA-256 and version at the first gate (CLI-01). |
| Executable probe | `phase54_cli317_host_recheck_v1/cli_identity/HOST_PROBE.txt` | `9f68830e40b8be72b2ee5189d911731be48de77b933ab2afe1632796b7f96d76` | File version, Authenticode and file id on 2026-11-08. |
| Environment at closure | `phase54_final_closure_v2/evidence/ENVIRONMENT_PROBE.txt` | `e0f1eaeb1a251ca1dd5ff7d6936722be64b5467851ce61124f47341cf3d068a7` | Desktop package, process start times and static CLI hash (ENV-01, ENV-02). |
| v1 hook record and operator lines | `phase54_final_closure_v2/evidence/v1_transcript_excerpt.jsonl` | `961d61d2ef473c627878a91009dbebe74434ce999c3ad60785b08c080666c33b` | Verbatim transcript lines 124-126, 129, 165-167, 232, 239, 285, 292 (V1-02 to V1-04). |
| v1 session's own report | `phase54_desktop_auto_smoke_v1/work/desktop_auto_smoke/results.json` | `49b7675fd265b1b153a89e8e39a20520a606341aa0caed9331e7fe77450bf0fc` | R1 to R13 as recorded by the test session, including Deny NOT_VERIFIED (NC-07). |
| v2 permission card | `phase54_desktop_auto_smoke_v2/evidence/k0_deny_permission_card.png` | `27ca23bab0026bb62eae788bcee97ef7dde1c81469edc4bda48f903a2c186e92` | Operator-supplied screenshot showing K0's text on the git commit card (V2-03). |
| Pending-card corroboration | `phase54_final_closure_v2/evidence/corroborating_pending_card_image_1_from_v1_chat.png` | `fab01f0791032ef862528a55828074ef0d19b30759b1517a1b2e043d827ea4fd` | Earlier capture of the same pending card, sent to chat at 2026-11-09T10:14:25.622Z, inside the waiting window (V2-03). |
| v2 state at closure | `phase54_final_closure_v2/evidence/v2_readonly_rerun/t1_stdout.json` | `a81cd2b8e3ba89972c044bdd6163b5d2b50feb092b4219556efe355892d0b510` | check_state.py t1 re-run in this task (V2-05 to V2-07). |
| v2 transcript summary at closure | `phase54_final_closure_v2/evidence/v2_readonly_rerun/collect_stdout.json` | `8ad802a88d8849e3b33379cb161c5c6236c3319d37f5905c101bdf76a1f85e8d` | check_state.py collect re-run in this task; no K0 text in the transcript (V2-01, V2-02). |
| v2 historical state rows | `phase54_desktop_auto_smoke_v2/evidence/state_checks.jsonl` | `10603a8a434984b660248654c73ec14b3f9266ffc4e9475713944cd1a866bed9` | t0 and three t1 rows from the run itself, not altered (V2-05, V2-07). |
| v2 static hook run | `phase54_desktop_auto_smoke_v2/setup_verification/HOOK_VERIFICATION.json` | `cc25cfcdbb44e0b98a13eab865b443bf8a9b5386582841086be83f7d16b781b2` | Shows the frozen hook generates K0's text, with the command's quotes stripped as on the card (V2-03). |
| Protected-tree verification | `phase54_final_closure_v2/_baseline/PROTECTED_VERIFY.json` | `1726e21a89e0b38df571d5f593a97f732102724e33a511c8647aa5726b18d418` | UNCHANGED across 37,617 files during this task (FRZ-03). |

## Sources outside the project tree

| Claim | Source | SHA-256 | How it establishes the claim |
|---|---|---|---|
| v1 Desktop session | `~/.claude/projects/C--Projects-AI-Learning-ClaudeArchitectureResearchRuns-005-5-4-stage-A-reconciled-phase54-desktop-auto-smoke-v1-work/41e9d77f-7c86-43f6-9462-5848bdaa0cfb.jsonl` | `49454562257a9949e84789ca88d76430254360e910803c1ad77aaea94776403e` | Entrypoint, permission mode, version, both commit attempts and the hook record. Hash taken in this task; the file is outside the protected tree. |
| v2 Desktop session | `~/.claude/projects/C--Projects-AI-Learning-ClaudeArchitectureResearchRuns-005-5-4-stage-A-reconciled-phase54-desktop-auto-smoke-v2-work/9fe6ddea-d2e5-442a-b5b3-d50708fcc695.jsonl` | `fad0f2050948dc2cbc431d0608b97fff716873ae81b7f4cfddf4352181ca5cac` | Entrypoint, permission mode, version, the single commit attempt and its rejection. Equal to both copies in v2 `evidence/` and to the copy in this package. |

## How the screenshot is tied to the tested request

File: `phase54_desktop_auto_smoke_v2/evidence/k0_deny_permission_card.png`, SHA-256 `27ca23bab0026bb62eae788bcee97ef7dde1c81469edc4bda48f903a2c186e92`, 126654 bytes, written 2026-11-09 12:37:45 local.

Visible on the card, in order: `Allow Claude to run this command?`, `Commit the already-staged probe file`, `Repository-changing Git command (commit): git commit -m chore: add desktop auto probe Run it only when the user explicitly requested it or pre-approved this operation and scope (CLAUDE.md § Git)`, the command box `git commit -m "chore: add desktop auto probe"`, and the buttons `Deny` and `Allow once`. Above the card: `Needs your input`. Bottom bar: `Auto`. Sidebar: `work · phase54_desktop_auto_smoke_v2`, session `Git status output`.

Supports criterion **V2-03** only (with `Auto` also supporting V2-01). Binding to the transcript:

- Session title in the transcript is `Git status output` (custom-title records).
- Tool description at line 78 equals the card's second line; the assistant text at line 77 and plan items at line 57 match the visible conversation.
- The folder has one session and one commit attempt, pending from 10:13:12.850Z to 10:18:08.778Z (295.9 s).
- An earlier capture of the same pending card reached the v1 chat at 10:14:25.622Z, inside that window. Its first line was scrolled out of view, so a second capture was requested; the archived file shows that first line.
- The card's text has the commit message's quotes stripped, as the frozen hook produces it (`HOOK_VERIFICATION.json`), unlike the raw command in the box.

Limits: the file was written 19 minutes after the rejection, so its write time is not its capture time. The card's unresolved state is what bounds the capture. The JSONL transcript has no K0 text for this attempt, and no such claim is made.
