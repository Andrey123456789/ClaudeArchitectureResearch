# Step 2 residual-parity closure: final report

**Recommendation for Step 3: `CONDITIONAL_GO`.** Step 3 was not started. The conditions are in section 7.

**Result:** `PASS_WITH_DOCUMENTED_NOT_RUN`. All seven approved corrections are applied, each with its own gate and checkpoint. The separate cold audit on final bytes ended with 0 failures.

This is a self-audit: one session made the changes and audited them, in the same model family that wrote the labels. Passing means the executed checks pass. It does not show how a live agent behaves, because no live agent ran. Only 96 of the 1,176 policy cells were read in v2; the rest rest on a mechanical witness (section 3).

## 1. Which proposed edits were necessary

| Item | Outcome | What happened |
|---|---|---|
| **C01** CPM effective state | **Necessary, all six** | All six checkers now ask real MSBuild for each project, in each context. 26 fixture cases ran against all six. 220 tests failed on v1 bytes first. If the SDK is missing, the result is `NOT_RUN` with exit 3, never a pass. |
| **C02** compiled queries, raw SQL | **Necessary, all six** | Compiled-query lines changed in M, M1, L0, L1, K0. K1's was already aligned. Raw SQL lines changed in all six. |
| **C03** Production migration default and exception | **Necessary, all six** | The default stays. L1's unqualified "Never" and the scaffolding lines that barred a controlled deployment step are fixed. K0 had the same scaffolding defect, though the contract did not name it. All six owners now say what an exception needs. |
| **C04** conditional Git commit steps | **Necessary, all six** | v1 listed 5 lines in four candidates. A wider sweep found 12 across all six, including checker messages. |
| **C05** PI-012 residual | **Data only** | The two K0 deserialization records close as audit criteria (4 rows). All 21 leads were read: 20 kept, 1 claim got its lost condition back, and no modality moved. |
| **C06** readings and review sets | **Data only** | See section 2. No classification or modality moved. |
| **C06B** `R22-UNDER-EXTRACTION` | **Necessary, derived field only** | Scope from the original trigger now reaches `applicability_scope_hint` on 3,117 records. No status moved. |
| **C07** extras and integrity | **Mostly `NO_CHANGE_VERIFIED`** | See the rows below. |

### `NO_CHANGE_VERIFIED`

- **`R13-TEST-PRIORITY`:** the sentence is in M, K0 and K1. `TST-011` has a direct witness in all six.
- **`R19-CI-RULE-SPREAD`:** the rule stays in all six and CI stays out of practical benchmarks. One data label was missing (section 5).
- **C02:** owner lines in all six, `code-review`, `modern-csharp`, `logging`, and the `RUN-007` caching lines.
- **C03:** `ci-cd` and `docker` lists, L1 `ef-core/commands.md`, the seeding bans, and the credential bans.
- **C04:** `git-workflow` in all six, "review migrations before committing", the secret ban, and database commit boundaries.
- **`R04-RECORD-FORGERY`:** an accepted limit. No proof-of-origin infrastructure was added, and no candidate claims such proof.
- **Unmarked `only when`:** the approved PI-012 reading stands, and option D is shown but not imposed (`PI012_SENSITIVITY_V2.md`).

The four candidate-specific proposals stay proposals, and the policy set stays at 196.

## 2. The six readings and the review sets

| Set | Result |
|---|---|
| Six reviewer readings | Adjudicated in `REVIEWER_SIX_READINGS.md`. |
| 62 `review_needed` | 34 `NOT_VERIFIED` (flag kept), 18 `CONFIRMED`, 7 `CORRECTED`, 3 `QUALIFIED`. The 34 are nearly all about how a live host applies a hook decision; the scripts themselves ran wherever they could. |
| 38 cells with no FULL direct witness | 37 `CONFIRMED`, 1 `QUALIFIED` (L0 `GOV-007`, stronger by timing). None is called full parity. |
| New claims | 70 rows: v1's 42 and 4 proposals, plus 24 added in v2. All `CONFIRMED`. Depth: one reading per rule group, plus a phrase check on each record against current bytes. |
| Blind reread | 48 records from all six: 30 agreed and 18 disagreed. Read at source, the 18 gave 15 stored labels upheld, 1 corrected, and 2 qualified. Not an error rate (`BLIND_REREAD_SUMMARY.md`). |

The 103 corrections and 31 original open records were reassessed only where v2 touched them: 6 and 2 rows (`CORRECTIONS_REASSESSED.jsonl`). All stand. Global checks ran on all of them.

## 3. Policy and architecture test results

| Check | Result |
|---|---|
| Cold final audit | 219 PASS, 0 FAIL, 23 NOT_RUN, 5 FINDING |
| All suites, cold, on final bytes | 2,184 PASS, 0 FAIL, 20 NOT_RUN (27 v1 suites and 8 v2 suites) |
| Policy cells | 1,176. Status and strength are identical to v1 in every cell, and no direct witness set changed. |
| Strength | 1,171 `EQUIVALENT_EVIDENCE_PRESENT`, 5 `STRONGER_AND_WEAKER_EVIDENCE` (K0 `API-014`, `API-019`; K1 `GOV-007`, `API-014`, `API-019`) |
| Depth of the cell checks | 66 read side by side at source in v2, 30 clause-reviewed, **1,080 mechanical witness only** |
| Fence | Inputs, Step 1, Step 2, the audit, v1 and its archive, and the kit are unchanged: 3,010 files, 0 errors. The Codex area was not read. |
| Replay | The view rebuilds from the frozen baseline to identical records. |
| Runtimes | .NET SDK 10.0.403, Node 24.21.0. MSBuild evaluation ran without restore. NuGet error codes came from offline restores of fixtures. |

"Identical in every cell" is weaker than it sounds: coverage does not read modality, so label changes cannot show up there.

### Gate history

| Change | Attempts | Failed | Result, on last attempt |
|---|---:|---:|---|
| V0 baseline replay | 2 | 1 | 1,102 pass |
| C01 | 2 | 1 | 1,721 pass |
| C02 | 1 | 0 | 1,780 pass |
| C03 | 1 | 0 | 1,870 pass |
| C04 | 1 | 0 | 1,929 pass |
| C05 | 2 | 1 | 1,957 pass |
| C06 | 1 | 0 | 2,079 pass |
| C06B | 1 | 0 | 2,123 pass |
| C07 | 1 | 0 | 2,184 pass |

The failed attempts are listed in `REGRESSION_MATRIX.md`. No failed attempt wrote a checkpoint. v1's 27 checkpoints stay in v1 and were not re-counted here; its suites replayed at every v2 gate.

## 4. Differences kept on purpose

| Topic | Difference | Reading |
|---|---|---|
| Git commands | Only K0 has a Git hook | Same obligation, different delivery |
| Hook on bad input | M exits 1 on malformed or empty input, so only the host setting `onFailure: block` can make that a block. M and M1 allow a payload with no command. The other four refuse in the script. | A real difference, reported and not changed. A live host applying it was not tested. |
| Central package file below the repo root | K0's checker errors under its decision D-17. The other five accept it. | A stricter location decision, not a different CPM obligation |
| Frontend tests under `backend/` | M has no marked ban. The other five do. | A real text difference. `DEP-024` does not require one. |
| Deserialization | Marked in M, M1, L0, K1; an audit criterion in K0; a list item in L1. All six are in a scan layer only. | Not a strictness fact. Qualified on the records. |
| New commands | L0 and L1 gained `manifest-checks.mjs` and `post-change-checks.mjs --scan`, because they had no whole-repository check | Added on existing hook scripts. No file was added. |

## 5. Defects found along the way

The regression suites, the source readings and the falsification checks caught these. All are fixed or stated.

- **A tool defect wiped stored strength readings (C05 first gate).** Any v2 update to a frozen record cleared its resolution. It affected 3 records. An R27 regression caught it; the per-claim gate had missed it. Now v2 updates keep a stored reading unless they name the code, and the per-claim gate fails on any undeclared field change. No coverage cell was affected.
- **A stored inconsistency (blind reread).** The same ban, "Never place frontend tests under `backend/`", was `MUST_NOT` in M1, L1 and K0 but `DEFAULT` in L0 and K1. Three records were corrected.
- **A wrong v1 statement.** The v1 report says the CI rule is labelled out of evaluation in all six. L0's record had no label: R19's overlay did not list it, and R25 corrected that record separately. Added.
- **My own errors, caught before they counted:**
  - The first scope filter kept delivery phrases as scope and lost real scope in mixed parentheses.
  - The first blind draw leaked the label group through its order, so it was set aside unread.
  - A staged test assumed all six hooks fail closed in the same way. They do not.
  - A same-task fixture omitted the package version, so its result looked like a difference that was not there.
- **A real interaction (C01).** A recorded `DEP-003` floating NuGet exception cannot restore without `CentralPackageFloatingVersionsEnabled`. The checker now gives a notice, and `add-dependency` names the switch.

## 6. What changed

### Against v1 and against the frozen inputs

| Candidate | Files | Changed vs v1 | Changed vs frozen |
|---|---:|---:|---:|
| M | 61 | 10 | 17 |
| M1 | 80 | 6 | 14 |
| L0 | 71 | 7 | 15 |
| L1 | 86 | 8 | 16 |
| K0 | 63 | 8 | 16 |
| K1 | 87 | 10 | 20 |
| **Total** | **448** | **49** | **98** |

No file was added or removed against either. Per-file detail: `V2_FINAL_MANIFEST.json`.

| Claims | vs v1 | vs frozen |
|---|---:|---:|
| Claim text changed | 54 | 154 |
| Classification changed | 1 | 73 |
| Modality changed | 5 | 159 |
| Records with any of these | 57 | 314 |
| Added (claims and proposals) | 24 | 70 |
| Removed (inactive, identity kept) | 0 new | 3 |

The modality changes against v1 are 2 from C01 (`SHOULD` to `MUST`, because the checker now enforces it) and 3 from C07. The classification change is `FG-L1-a9fb9c9a62`, which lost a stronger delta once its source said "by default".

The view has 6,472 rows, 6,469 of them active, recomputed rather than assumed from v1's 6,448. `V1_TO_V2_CROSSWALK.jsonl` shows 3,170 `FIELD_CHANGED`, mostly the new scope hint on 3,096 records; the claim did not change. Its 3 `CLASSIFICATION_CHANGED` rows are the C07 modality corrections.

## 7. Conditions for Step 3

1. **Start from a clean tree or an explicit standing choice.** Otherwise every headless run stops at the task-start check.
2. **Have the .NET SDK where CPM checks run.** Without it they report `NOT_RUN`, which is honest but proves nothing.
3. **Do not use raw `MUST_NOT` counts as a strictness measure.** 86 records are an open question (section 8).
4. **Keep CI/CD out of practical benchmarks.**
5. **Observe live host behavior.** How a host applies `ask`, `deny`, exit 2 and `onFailure` is untested. M's input-error path depends on it entirely.

An independent fresh-session or human review of this folder is recommended first. It is the one check this run could not give itself.

## 8. Remaining uncertainties

- **Open class of 86 records.** Their claim says "never" or "must not" at a soft modality. A word match found them and they were not read one by one; some are real marked bans, others descriptions. They stay as stored with status `NOT_VERIFIED`. If all were `MUST_NOT`, 36 would need a strength resolution (`MARKED_NEVER_SOFT_MODALITY.jsonl`, `BLIND_REREAD_SUMMARY.md`).
- **1,080 cells with a mechanical witness only.** They rest on the Step 2 classification, v1, and a witness at a current line. A witness is traceability, not parity.
- **About 6,200 of the 6,472 records were not re-read in v2.** They keep their labels.
- **Scope hints.** All 144 distinct phrases were read, but only 30 of 3,117 records. Of those, 5 were debatable: a hint can carry the delivering workflow's scope, which may be wider than the line.
- **The DEP-003 exception record is agent-writable.** A checker cannot tell who asked. The duty is in the instruction text.
- **Floating versions that come from an MSBuild property** are not detected. Candidates differ here, and it was out of C01's scope.
- **L1's `approvalRequired` key** reads as binding while the hook only reports it (`FG-L1-bd72816942`).
- **Union bound.** This work uses the Pass 1 augmented union. Codex Pass 2 was neither read nor used, so clauses outside the union are not covered.
- **`UNRESOLVED_DECISIONS.jsonl` is v1's file, unchanged.** Its 4 `OPEN` PI-012 rows are closed by `PI012_REMAINING_ADJUDICATION.jsonl`. Its 6 readings are answered in `REVIEWER_SIX_READINGS.md`, and its 6 parity leads in sections 1 and 4 here.

Full list of limits: `EVIDENCE_LIMITS.md`.

## 9. What did not run

None of these counts as passed. Each is listed in `FINAL_AUDIT_RESULTS.jsonl`.

- A live agent in any candidate, interactive or headless, including the dirty-tree stop, the conditional commit step and a Reserved headless change.
- A live host applying `ask`, `deny`, exit 2, `onFailure` or a Stop block. The hook scripts themselves were run directly.
- A real application, API or Swagger UI.
- A real database or cache, including the cache timelines and startup or deployment-time migrations.
- A package registry, including latest-version lookup and a restore that resolves a real floating package.
- CI, which is out of scope.
- A hand reading of all conditions in all 1,176 cells.
- A fresh-session or human reader of the blind sample or the PI-012 records.

## 10. How to re-check

From this folder:

```bash
PYTHONPATH=_tools python -B _tools/verify_final.py
```

Read-only, about a minute: the fence, all candidate hashes against the final manifest, and a replay of the view.

```bash
PYTHONPATH=_tools python -B _tools/final_audit_v2.py
```

The whole cold audit, about 20 minutes. It regenerates `FINAL_AUDIT_RESULTS.jsonl`, `POLICY_PARITY_MATRIX.jsonl`, `SAME_TASK_MATRIX_V2.json`, `INTERACTION_MATRIX.json`, `V2_FINAL_MANIFEST.json` and `FINAL_SUITE_TALLY.json`. It does not change candidate files. It needs Node, Git and the .NET SDK. It was run only with all three present.

Where to start reading: this report, then `REGRESSION_MATRIX.md`, `POLICY_PARITY_MATRIX.jsonl`, and `_rules/<change>/DECLARATION.md` for each change. `CHANGE_LOG.jsonl` holds every edit. `CLAIM_GATE_LOG.jsonl` holds every data disposition; C05's rows with `attempt: 2` supersede the first attempt, which stays in the log.
