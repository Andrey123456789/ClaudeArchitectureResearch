# Stage A Step 2 controlled corrections: final consistency report

**Result: `PASS_WITH_DOCUMENTED_NOT_RUN`.** Every rule gate passed, and the final audit has no failed check. Runtime behavior was not tested; the list is below.

**This is a self-audit.** The same model and session made the repairs and this audit, so it is not an independent evaluation. A fresh-session reviewer who reads the final bytes without this report is the next step if independent assurance is wanted.

**Step 3 readiness: `CONDITIONAL_GO`.** Step 3 was not started. The conditions are in section 8.

## 1. Numbers

| Item | Value |
|---|---:|
| Rules with a passing gate | 27 of 27 |
| Failed gate attempts repaired before passing | 10 |
| Files that differ from the frozen templates | 72 (M 11, M1 11, L0 12, L1 11, K0 13, K1 14) |
| Change-log rows, including rollbacks and re-applies | 325 |
| Cumulative tests on final bytes: pass | 1102 |
| Cumulative tests on final bytes: fail | 0 |
| Cumulative tests on final bytes: not run | 14 |
| Final audit rows: pass, fail, not run, finding | 293, 0, 5, 6 |
| Policy rows checked at the final gate | 1176 |
| Baseline records kept | 6,402 |
| Repaired view rows, active | 6448, 6445 |
| Crosswalk | ADDED 46, MOVED 845, REMOVED 3, REWORDED 103, REWORDED_CONTEXT 132, UNCHANGED 5319 |
| Coverage cells, moved status or strength | 1176, 0 |

The 6,448 rows are 6,402 original identities, 42 new claims and 4 proposals. 3 of the originals are inactive, because their source is gone.

## 2. Rules

| Rule | Decision | Type | Gate | Attempts |
|---|---|---|---|---:|
| R01 | HQ-06 PI-012 reading | Protocol, classification | PASS | 3 |
| R02 | HQ-01, 9.1 Git authority, dirty tree, protected branches | Template, enforcement | PASS_WITH_NOT_RUN | 2 |
| R03 | HQ-02 cache invalidation | Template | PASS_WITH_NOT_RUN | 1 |
| R04 | HQ-03 floating versions | Template, enforcement | PASS_WITH_NOT_RUN | 4 |
| R05 | HQ-04 headless Reserved work | Template | PASS_WITH_NOT_RUN | 4 |
| R06 | HQ-05 peer bypass | Template, enforcement | PASS_WITH_NOT_RUN | 1 |
| R07 | 8.1 Swagger UI | Template | PASS_WITH_NOT_RUN | 2 |
| R08 | 8.2 K0 effective CPM | Enforcement | PASS_WITH_NOT_RUN | 2 |
| R09 | 8.3 K1 compiled queries | Template | PASS_WITH_NOT_RUN | 1 |
| R10 | 8.4 L0 Production migrations | Template | PASS_WITH_NOT_RUN | 1 |
| R11 | 8.7 CUSTOM_SETTINGS | Template | PASS_WITH_NOT_RUN | 1 |
| R12 | 8.7 K1 local migrations | Template | PASS_WITH_NOT_RUN | 1 |
| R13 | 8.7 test priorities | Labels, no template edit | PASS_WITH_NOT_RUN | 1 |
| R14 | 8.7 C# language version | Labels, no template edit | PASS_WITH_NOT_RUN | 1 |
| R15 | 8.5 HTTP timeout | Labels, no template edit | PASS_WITH_NOT_RUN | 1 |
| R16 | 8.6 L1 liveness | No change verified | PASS_WITH_NOT_RUN | 1 |
| R17 | 8.7 security scan minimality | Labels, no template edit | PASS_WITH_NOT_RUN | 1 |
| R18 | 8.7 fast and slow tests | No change verified | PASS_WITH_NOT_RUN | 1 |
| R19 | 8.7 CI dependency updates | Labels, scope mark | PASS_WITH_NOT_RUN | 1 |
| R20 | 9.2 K0 deserialization | Labels, no template edit | PASS_WITH_NOT_RUN | 1 |
| R21 | 10 four new clauses | Proposals | PASS_WITH_NOT_RUN | 1 |
| R22 | 11.1 applicability and delivery | Derived fields | PASS_WITH_NOT_RUN | 1 |
| R23 | 11.2 cross-method adjudication | Adjudication | PASS_WITH_NOT_RUN | 1 |
| R24 | 11.3 evidence limits | Documentation | PASS_WITH_NOT_RUN | 1 |
| R25 | 103 corrections | Classification | PASS_WITH_NOT_RUN | 1 |
| R26 | Repaired view | Derived view | PASS_WITH_NOT_RUN | 2 |
| R27 | Final audit | Audit | PASS_WITH_NOT_RUN | 2 |

`PASS_WITH_NOT_RUN` means nothing failed, and some checks in the cumulative suite could not run here. Attempts counts every gate run, including failed runs that were repaired and re-runs after a pass.

## 3. Six-way outcome

Each cell: files edited (`e`) or records relabeled (`l`). A dash means no change there.

| Rule | M | M1 | L0 | L1 | K0 | K1 |
|---|---:|---:|---:|---:|---:|---:|
| R01 | 35l | 22l | 13l | 17l | 21l | 20l |
| R02 | 3e | 2e | 2e | 3e | 4e | 2e |
| R03 | 2e | 2e | 2e | 2e | 2e | 2e |
| R04 | 2e | 2e | 2e | 2e | 2e | 3e |
| R05 | 2e | 2e | 2e | 2e | 2e | 2e |
| R06 | 2e | 3e | 2e | 3e | 3e | 3e |
| R07 | 2e | 2e | 2e | 2e | 2e | 2e |
| R08 | — | — | — | — | 2e | — |
| R09 | — | — | — | — | — | 1e |
| R10 | — | — | 1e | — | — | — |
| R11 | — | — | 1e | — | 1e | 1e |
| R12 | — | — | — | — | — | 1e |
| R13 | — | — | — | — | — | — |
| R14 | — | — | — | — | — | — |
| R15 | — | 1l | 1l | — | 1l | 1l |
| R16 | — | — | — | — | — | — |
| R17 | 1l | — | 1l | 1l | 1l | 2l |
| R18 | — | — | — | — | — | — |
| R19 | 1l | 1l | — | 1l | 2l | 1l |
| R20 | — | — | — | — | 2l | — |
| R21 | — | — | — | — | — | — |
| R22 | — | — | — | — | — | — |
| R23 | — | — | — | — | — | — |
| R24 | — | — | — | — | — | — |
| R25 | 12l | 13l | 14l | 19l | 25l | 16l |
| R26 | 20l | 28l | 25l | 22l | 31l | 26l |
| R27 | — | — | — | — | — | — |

R13, R14, R16 and R18 show dashes because they changed no template and their label corrections are counted in the R25 row. R26 counts claims restated, removed or added.

After R02 to R07, the same obligation and condition read the same in all six, by side-by-side reading. R08 to R12 changed only the candidates the register named, and the parity leads that leaves are in section 6.

**Same hypothetical task.** `SAME_TASK_MATRIX.json` runs the same commands through each real hook and the same manifests through each real checker, and it finds each required sentence with its loading class. Force and legacy-peer forms are denied in all six on both attempts. Recorded exceptions are honored for the named package only.

Two delivery differences remain. A pinned `npm install` with no marker is denied by M1 and K0, denied once by L1, and allowed by M, L0 and K1. `git reset --hard` and `git push --force` reach a hook only in K0, as `ask`; the other five rely on the always-loaded text. The same commands on copies of the frozen templates give the same first decisions, so no rule here introduced these differences.

## 4. Cumulative checks

| Suite | Pass | Not run |
|---|---:|---:|
| R01 | 17 | 0 |
| R02 | 64 | 2 |
| R03 | 42 | 1 |
| R04 | 146 | 2 |
| R05 | 43 | 1 |
| R06 | 223 | 1 |
| R07 | 37 | 1 |
| R08 | 35 | 0 |
| R09 | 7 | 0 |
| R10 | 8 | 0 |
| R11 | 28 | 0 |
| R12 | 9 | 0 |
| R13 | 11 | 0 |
| R14 | 12 | 0 |
| R15 | 13 | 0 |
| R16 | 4 | 0 |
| R17 | 13 | 0 |
| R18 | 6 | 0 |
| R19 | 7 | 1 |
| R20 | 5 | 0 |
| R21 | 4 | 0 |
| R22 | 12 | 0 |
| R23 | 6 | 0 |
| R24 | 5 | 0 |
| R25 | 25 | 0 |
| R26 | 27 | 0 |
| R27 | 293 | 5 |

Each gate re-ran every earlier suite on current bytes, including mutation tests. A mutation test breaks a rule on a copy and confirms the test notices. All 196 policies per candidate have a row in `POLICY_CHECKS/R27-FINAL/`, joined with source reviews.

**What the 1,176 rows do and do not show.** Each cell has a live witness at a current line. That is traceability. Only the changed policies were read side by side. `DIRECT_EVIDENCE` is not parity, and 38 cells rest on a written Step 2 override or on partial witnesses, as they did in the baseline.

## 5. Data results

| Set | Outcome |
|---|---|
| PI-012, 79 cases | 55 correct, 22 upheld, 2 unresolved |
| PI-012, 230 cases | 105 correct, 123 upheld, 2 unresolved |
| 103 corrections | 79 accepted, 20 accepted with changes, 4 rejected, 0 unresolved |
| 4 new clauses | Candidate-specific proposals, not promoted, not copied |
| 31 open records | All resolved by a user decision and the matching rule, per `UNRESOLVED_DECISIONS.jsonl` |
| 5 strength cells, 3 overrides | Qualifier kept, none became a parity statement |
| 19 baseline `UNCERTAIN` records | None left; each has a rule and a current reading |
| `review_needed` flags | 62 carried from the baseline, not individually cleared |

The 4 PI-012 unresolved rows stay marked open in the view and are not strictness facts.

Applicability fields are derived, not verified: 4,621 with no condition extracted, 697 attributed, 547 written by a reviewer, 429 with the condition inside the claim text, 154 not applicable. The 30-record sample in R22 found real defects, which were fixed, and it was then read again on the same draw, so it is not an error rate.

## 6. Findings and remaining tensions

No check failed. These are real and were left as they are, because no decision covers them.

- **The Codex Pass 2 area changed near or during this run.** Files: stage_A/codex_iterative_search.zip. Folder time: 2026-11-03T19:21:58. Run start: 2026-11-03T17:48:25. Only timestamps were looked at; nothing there was read or hashed, as the contract requires. No tool of this run writes there, so something outside this run changed it. This run does not use that area.
- **Git vs headless: instruction lines that still say commit.** The Git clause names this case: such a step is not authority. 5 lines remain as written, in K0, K1, M, M1. M .claude/rules/dependencies.md:35 package manager. Maintain and commit `package.json` and `package-lock.json` and; M .claude/skills/add-dependency/SKILL.md:129 2. Commit `package.json` and `package-lock.json` together.; M1 .claude/rules/dependencies.md:50 project deliberately adopts another package manager. Maintain and commit; K0 .claude/rules/common/dependencies.md:28 - Commit `package.json` and `package-lock.json`, and keep the lockfile consisten; K1 .claude/skills/project-structure/references/frontend-setup.md:18 6. Verify with the workspace's declared scripts (`npm run build`, `npm test`) an
- **Git vs headless: a headless run with an approved Reserved change on a dirty tree.** The task-start pause comes first, so the approved change waits. The two rules do not conflict, but a harness must supply a clean tree or a standing choice.
- **Floating vs checks: a forged record.** An agent can write the record itself. The checker cannot verify who asked. Enforcement stops accidents and leaves a trail.
- **PI-012 vs strength: coverage status cannot show a modality effect.** Coverage status does not read modality, so "0 cells moved" is true by construction for modality changes. 154 records changed modality. Strength cells depend on strength_vs_canonical; the check above is the real test.
- **Cells that stand on a written Step 2 override or partial witnesses, as in the baseline.** 38 cells have no FULL direct witness in either view. Each is a qualified traceability cell, not proof of a full owner.

**Parity leads.** Each is a difference that a named rule leaves in place. The register did not authorize changing them, so they were not changed:

- `R10-SCAFFOLD-WORDING` (M, M1, L1, K1): Similar scaffold migration wording. L1 development-workflow says "Never apply" with no "by default". Register 8.4 named only L0.
- `R08-LITERAL-CPM` (M, M1, L0, L1, K1): Literal CPM checks. Register 8.2 named only K0, so an inherited setting is honored only in K0.
- `R09-MEASURED-LINES` (M, M1, L0, L1, K0): "Measured hot path" technique lines. Register 8.3 named only K1.
- `R13-TEST-PRIORITY` (M, K0, K1): The test-priority sentence appears only in these three. No obligation differs after classification.
- `R19-CI-RULE-SPREAD` (M, M1, L0, L1, K0, K1): The CI auto-update rule is in all six, not the four the task named. Preserved and labeled out of practical evaluation scope.
- `R20-DESER-FORMS` (M, M1, L0, L1, K0, K1): Deserialization forms differ: marked in M, M1, L0, K1; a scan criterion in K0; a list item in L1. All six sit in a scan layer.

**Readings that need a reviewer:**

- `R02-TASK-SCOPE`: Task-start check: "a task" is read as one that will change files or repository state. A read-only review does not trigger it. A reader could apply the check to every task. Cost: a read-only task stops on a dirty tree.
- `R02-HEADLESS-DIRTY`: A headless run on a dirty tree with no standing choice pauses and changes nothing. An experiment harness must supply a clean tree or a standing choice, or every run stops at the first step. Consequence for Step 3 runs, not a defect.
- `R04-RECORD-FORGERY`: The exception record can be written by the agent itself. A checker cannot verify who asked; `requested_by` and `request` are self-attested. Enforcement stops accidents and leaves an audit trail, not a determined agent.
- `R01-COMMON-VALUE`: The addendum reads unmarked "only when" as DEFAULT in knowledge text. Option D in PI012_SENSITIVITY.md is the alternative. MUST_NOT counts under each reading are in PI012_SENSITIVITY.md. No coverage or strength cell moves in any reading.
- `R01-TRIGGERED-CLASS`: Form "do not X when Y" stays MUST_NOT. A scan found 21 more lines of this form that were not read individually. Bound, not a census.
- `R22-UNDER-EXTRACTION`: Scope in a parenthesis of the original trigger field is not extracted. The original field keeps the text.

## 7. What ran and what did not

**Executed:** Python 3.14.0; Node v24.21.0; git version 2.56.0.windows.3; .NET SDK 10.0.403. Each candidate's own instruction, manifest, architecture and dependency checkers. Each pre-command hook with its real input format. `node --check` on all scripts. Git in disposable fixtures under `_scratch`. Real MSBuild property evaluation without restore in R08.

**Not run. None of these counts as PASS:**

| Test | Why | Impact |
|---|---|---|
| live agent stops on a dirty tree and offers exactly two options | needs a live Claude runtime; kept as a future experiment | An agent could read the rule and still not follow it. |
| host behavior of the K0 "ask" decision in a headless run | host semantics not executable here | How a headless host treats ask is unknown; the hook decision itself ran. |
| a real database and cache show these timelines | no database or cache server in this run; the simulation states the logic only | Timelines are reasoned, not observed. |
| registry lookup of the latest stable version and of the resolved install outcome | no network in this run; the duty stays in the workflow text and is not claimed as verified | Latest-stable and resolved versions are not confirmed. |
| NuGet restore with a floating version under Central Package Management | would need network and a project; MSBuild switches not exercised | Whether restore accepts a floating version under CPM is unobserved; property evaluation did run. |
| live headless run implements only the approved change and writes the decision log | needs a live Claude runtime; kept as a future experiment | The headless stop and the decision log are text, not observed. |
| host enforcement of deny and exit code 2 in a live Claude session | hook decisions were executed directly; the host loop is not available in this run | Hooks ran directly, not through the host loop. |
| a real API starts in Development and Swagger UI loads | no application or runtime exists in this research run; the obligation is text, its execution is a future experiment | The Swagger step was never carried out on an application. |
| CI trial of dependency updates | out of study scope by the register; no CI run | Out of study scope. |
| [E] Git vs headless: what an `ask` decision does in a headless host | No live host in this run. The hook decision itself was executed. | As above, host behavior of ask. |
| [E] floating vs checks: registry lookup and NuGet restore with a floating version | No network in this run. MSBuild property evaluation ran in R08; restore did not. | Latest-stable and resolved versions are not confirmed. |
| [E] cache vs transaction: timelines against a real database and cache | No server in this run. The semantic timeline tests of R03 are text and reasoning. | Timelines are reasoned, not observed. |
| [E] Swagger vs noninteractive: real API and real UI | No application runs in this run. | The Swagger step was never carried out on an application. |
| [F] all conditions and exceptions of all 1,176 cells read by hand | Not feasible in this run. Only the changed policies were read side by side (review.py). The rest got the mechanical witness checks. | Unchanged policies rest on the baseline and on mechanical witness checks. |

Full limits are in `EVIDENCE_LIMITS.md`: same-family reader, targeted sampling, no unbiased error rate, records not re-read, and the union bound. Codex Pass 2 was not read.

## 8. Step 3 conditions

`CONDITIONAL_GO` holds only if Step 3 does all of these:

1. Start each run from a clean tree or with a standing choice. Otherwise the new R02 check stops a headless run at its first step, which is by design.
2. Treat coverage as traceability. Compare strictness only from reviewed text.
3. Keep the 4 PI-012 unresolved records and the 6 readings in section 6 out of strictness counts, or report results under both readings.
4. Check the not-run list above live where a result depends on it. The Swagger, headless and dirty-tree rules have never been observed in an agent.
5. Use `REPAIRED_CANDIDATE_DERIVED_VIEW` for the repaired templates and `FROZEN_BASELINE_REFERENCE` for the originals. Never mix their line anchors.
6. Run candidates from `candidates/<C>/template/` in this folder, not from the frozen inputs. This run did not promote them anywhere.

## 9. Finish criteria

| Criterion | State | Evidence |
|---|---|---|
| Each agreed question has a disposition | Met | `DECISION_IMPLEMENTATION_MATRIX.md`, and section 2 of this report |
| Each modified rule has a passing gate | Met | `GATE_LOG.jsonl`, `CHECKPOINTS/` |
| No later change broke an earlier fix | Met | Cumulative suites on final bytes: 0 failed |
| 1,176 policy checks accounted for | Met | `POLICY_CHECKS/R27-FINAL/`, `REPAIRED_POLICY_COVERAGE.jsonl` |
| Overlays replay | Met | R26 suite and audit section F |
| Original inputs unchanged | Met | `fence.py`, audit section A |
| No Step 3 | Met | Audit section A |
| Non-executable tests named | Met | Section 7 |

## 10. Re-run

From this folder, with `PYTHONPATH=_tools`:

```bash
python -B _tools/fence.py verify
```
```bash
python -B _tools/dataset.py
```
```bash
python -B _tools/final_audit.py
```
```bash
python -B _tools/gate.py R27-FINAL --note "re-run"
```

The original templates are in `inputs/`. The repaired ones are in `candidates/<C>/template/`. Each change is in `CHANGE_LOG.jsonl` with before and after hashes.

