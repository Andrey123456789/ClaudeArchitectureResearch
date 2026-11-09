# Phase 5.4 closure — acceptance addendum 1 (CLI 2.1.317 recheck)

**Append-only.** This addendum adds to `../phase54_final_acceptance_v1/FINAL_PHASE54_CLOSURE_REPORT.md`, dated 2026-11-07, which is not edited and stays valid as the record of what was true on CLI 2.1.293. Date of this addendum: 2026-11-08.

## Recommendation

**Upgrade CLOSED_CONDITIONAL to CLOSED_VERIFIED, bound to Claude Code CLI 2.1.317 (SHA-256 `26b01ec2…6038`), headless operation.**

## Basis

The original closure was conditional because "one critical live scenario class (D, hook failure) did not behave as declared". On 2.1.317 that class behaves as declared:

| Required check | Result | Evidence |
|---|---|---|
| Executable identified as exactly 2.1.317, with hash, no fallback | PASS, all 51 sessions | `CLI_VERSION_AND_HASH.md` |
| Six previously failing `onFailure: "block"` cases, genuine host, frozen settings | 6 of 6 PASS; were 6 FAIL on 2.1.293 | rows `<C>-D1` |
| Operation did not execute, shown on the file system | 6 of 6 marker absent, with positive controls showing the marker can appear | rows `<C>-D1M`, `SYN-DX2M`, `SYN-SHIMM` |
| Unexpected hook failure: exit 1, missing executable, timeout | all blocked: 12 candidate exit-1 rows, 2 L1 timeout rows, 6 synthetic rows | rows `D1X`, `D3`, `SYN-DX1/3/5` |
| Allow | 12 of 12 PASS | rows `S-A1`, `S-A2` |
| Deny | 6 of 6 PASS | rows `S-B1` |
| Ask, genuine permission decision requested, nothing approved | 12 of 12 PASS | rows `S-C1`, `S-C2` |
| Stop | 6 of 6 PASS | rows `S-E1` |
| Candidates unchanged | PASS | `RAW_EVIDENCE_AUDIT.json` R6, `verify_release.py` 448 of 448 |

Effective matrix: 78 PASS, 0 FAIL, 19 NOT_RUN. The 19 are listed under "Remaining" below; none was a required check of this recheck. The 7 FAIL rows from attempt 1 are retained and attributed to the test harness (report section 5).

## The one judgment call

The original closure gave a second reason for not being verified: "interactive checks are NOT_RUN". They are still NOT_RUN. No terminal prompt was shown to a person.

I do not treat this as blocking, because the original closure's own table carries those rows as a manual procedure "if interactive is chosen", and this recheck's scope, set before the runs, did not include them. The `ask` path was verified through the host's real SDK approval surface. What stays unverified is how a prompt is displayed in a terminal and what happens when a person answers it.

**If you consider interactive verification a required part of Phase 5.4 closure, keep CLOSED_CONDITIONAL.** In that case, the interactive rows are the only remaining condition, and the manual procedure in `LIVE_HOST_PILOT_REPORT.md` section 7 still applies.

## Status of carried items

| Item | Before | After |
|---|---|---|
| HOST-01 (hooks fail open) | Material, on 2.1.293 | **Resolved on 2.1.317.** Unchanged as a fact about 2.1.293 |
| G1 (hook-health benchmark gate) | Required: `node` preflight, flag degraded runs | **Reduced, not removed.** Pin 2.1.317, because older hosts fail open. Keep the `node` preflight: with `node` missing, every Bash call is now refused, so a run would be unusable rather than unguarded. To detect blocks, read the tool result, because the hook event's `outcome` is the same whether or not the host blocks |
| G2 (run mode) | User decision pending | **Still pending.** `--permission-prompts none` still denies every `ask` at once. New information only: an SDK stdio approval surface exists as a further option |
| D3 (timeouts) | NOT_RUN | L1's 15 s budget verified live. M1 has no declared timeout and remains NOT_RUN |
| Interactive rows | NOT_RUN | NOT_RUN |
| D2 malformed input | Static only | Static only |
| F1 reference gate | Verified on 2.1.293 | Not re-verified on 2.1.317 |
| Runner R1–R8, Q-items, RD-01/02, same-family review | Open | Unchanged; not in scope |

## Scope of the claim

**Holds for:** CLI 2.1.317 with the recorded hash; headless `-p` sessions; Windows 11; the six frozen candidates, unmodified; `--permission-prompts none` and the SDK stdio approval surface.

**Does not extend to:** other CLI versions; interactive terminal sessions; other operating systems.

The fail-closed property is a property of the host version. It must be re-checked whenever the host version changes.

## Procedural disclosure

During this recheck I briefly created 7 empty directories inside the frozen `release/` folder through a relative `mkdir` run from the wrong working directory. They were removed within a minute, and no file was created or changed. The `release/` directory's last-write time remains changed to 2026-11-08 19:48:43. The release verifies 448 of 448 and the predecessor manifest 632 of 632. Report section 6 has the details.

## What was not done

No candidate, template, release file or predecessor report was edited. No new architecture search, benchmark or Phase 5.5 work was started. The original closure report was not rewritten.
