# Open decisions and sensitivity — Stage A Step 3 (six-way comparison, v1)

Scope: the v3 queue `UNRESOLVED_AND_USER_DECISION_QUEUE.jsonl` (Q-01 to Q-13), the decisions Step 3 itself had to make when reading, and how each alternative reading would change the Step 3 results. **Step 3 decides nothing for the user.** Every USER_DECISION item stays OPEN. No candidate file was edited.

Baseline Step 3 result (196 policies): **FULL_SEMANTIC_PARITY 165 · PARTIAL_PARITY_WITH_DELTA 16 · MEANINGFUL_DIVERGENCE 15 · CONTEXT_DEPENDENT 0 · UNVERIFIED 0.** All 15 material differences are on the enforcement axis. The normative axis has 7 recorded differences, none material.

## 1. Q-01 to Q-13

| ID | v3 kind | Step 3 disposition | Narrow fact | Effect on study tasks | Effect on Step 3 results |
|---|---|---|---|---|---|
| Q-01 | USER_DECISION | **OPEN** | L0 lacks the security-scan prompt "review deliberate raw HTML in any server-rendered UI"; M, M1, L1, K0, K1 carry it (v3 CL15). Extras cluster X0400. | Only a security scan of an app with a server-rendered UI that emits raw HTML. All candidates target an Angular SPA, so none in the planned study. | None on policy labels (not a canonical policy). One extras cluster stays UNRESOLVED_OR_DECISION_DEPENDENT. |
| Q-02 | USER_DECISION | **OPEN** | A blank PreToolUse command (valid JSON, empty string) is allowed by L0, K0, K1 and blocked by M, M1 (PV2-02 scope) and L1. Malformed or unreadable input is blocked by all six (v3 SAME_TASK_MATRIX_V3 `bad_input`). | None: a blank command runs nothing. | None. Recorded in extras X0225. |
| Q-03 | USER_DECISION | **OPEN** | Event/tool mismatch handling differs: K1 alone blocks a mismatched event; L0 and L1 block a non-shell tool; M1 blocks a non-PreToolUse event. | None while the host sends consistent payloads (host behavior NOT_RUN). | None. |
| Q-04 | OBSERVATION | OBSERVATION (kept) | K0 asks for `git` after an unrecognized leading word (`echo git commit -m x`); the other five allow it. | One extra prompt in K0 for an unusual command shape. In a headless run an `ask` may stall (Q-08). | GOV-015 is PARTIAL (D3, root RC-ENF-GIT-Q04, non-material). |
| Q-05 | OBSERVATION | OBSERVATION (kept) | M1 check-instructions accepts a section reference whose leading words match a heading (CL21). | None: instruction-maintenance checker only. | None. |
| Q-06 | OPEN_CLASS | NOT USED for any conclusion; universe recorded | "do not" bans stored at a soft modality were not reviewed as a class. Current count of active v3 records whose quote or claim contains "do not"/"don't": 1,485; of these 492 are stored at a soft modality (DEFAULT 460, SHOULD_NOT 29, MAY 2, SHOULD 1). | None directly. | None: Step 3 read deontic force from source for all 1,176 cells and used no stored-modality counts (example: FE-001, where M/M1 store MUST_NOT and L1 DEFAULT for the same NgModule ban, was judged the same default). The 492 records remain unreviewed as a class; any future metric built on stored modality would inherit that gap. |
| Q-07 | OPEN_HYPOTHESIS_RESIDUE | Limitation (kept) | Codex ran three of six strategy families; Pass 0004+ was paused. | Unknown. | The extras inventory covers the recorded universe (1,777 active records). Clauses no pass recorded are not covered. Step 3 surfaced 10 genuine extra-norm roots, all from recorded clauses; no saturation is claimed. |
| Q-08 | NOT_RUN | NOT_RUN (kept) | Live Claude Code host behavior: how `ask`, `deny`, exit 2 and `onFailure` are shown and applied, and what a headless run does on `ask`. | Medium for later experiments: Git commands meet `ask` in all six; L1 answers project-reference commands with `ask`. | All 11 material enforcement roots are mediated by hooks or checkers. Their script outputs are verified statically (v3 suites, PROBE-HOOK-01/02/03); their effect on a live agent is NOT_RUN. See section 3 (S-HOST) and `HOOK_AND_CHECKER_EFFECTIVE_BEHAVIOR.md` section 6 for a manual reproduction procedure. |
| Q-09 | QUALIFIED | No action | L1's 304 catalogue line is stored DEFAULT although it says "never". | None. | None (extras X0001: same 304 rule in all six). |
| Q-10 | RESOLVED | Not reopened | PackageVersion without Version: resolved in v3 (V3-Q10-PACKAGEVERSION-VERSION). | None. | None. |
| Q-11 | OBSERVATION | OBSERVATION (kept) | Without the .NET SDK, K0 and M keep a static CPM error where M1, L0, L1, K1 report NOT_RUN (exit 3). With the SDK all six agree. | None on hosts with the SDK; both outcomes are non-pass. | DEP-006 is PARTIAL (D2, root RC-ENF-CPM-NO-SDK, decision link Q-11, non-material). |
| Q-12 | USER_DECISION | **OPEN** | No candidate checks the name of a central package file MSBuild imports through DirectoryPackagesPropsPath; all six accept `config/Packages.props`. | None in the planned layout. | None: identical in all six, so no comparison changes. |
| Q-13 | ENVIRONMENT | ENVIRONMENT (kept) | The v2 convenience archive was removed outside the session; v3 zip and an interim review were added (EXTERNAL_EVENTS ENV-01..03). | None. | None: Step 3 verified the v3 tree file by file (preflight P04/P17); the v2 tree itself is unchanged. |

### Options and recommendations for the open USER_DECISION items

Recommendations are given only to help the user decide; none is applied.

| ID | Option A | Option B | Changes a Step 3 conclusion? | Changes later benchmark comparability? | Step 3 recommendation |
|---|---|---|---|---|---|
| Q-01 | Leave as written (L0 without the prompt). | Approve the same sentence in L0's scan-layers reference (homogenizes a five-candidate extra). | No (A or B). B turns X0400 into SAME_NORM_DIFFERENT_PACKAGING. | No for SPA tasks; only for a scan of a server-rendered UI. | **A** for the freeze; revisit only if a benchmark task adds a server-rendered UI and a security scan. |
| Q-02 | Leave. | Approve blocking a blank command in L0, K0, K1. | No. | No (nothing executes either way). | **A**. |
| Q-03 | Leave. | Approve one mismatch rule for all six. | No. | No while payloads are consistent; observe in the host pilot (Q-08). | **A**, with a host-pilot check. |
| Q-12 | Leave. | Require the name Directory.Packages.props in all six. | No. | No (uniform). | **A**. |

## 2. Readings Step 3 had to choose (and the alternative)

| ID | Where | Primary reading (used) | Alternative reading | Label effect of the alternative |
|---|---|---|---|---|
| S-VOCAB | RC-TXT-FORCE-VOCABULARY (extras X0259/X0554/X0556) | M, L0, K0, K1 define "default — deviation needs a concrete reason and must be reported" in the root file; M1 and L1 define no force vocabulary. Scored once as a cross-cutting genuine extra norm. | Treat the vocabulary as part of the force of every canonical DEFAULT policy. | 51 FULL policies with canonical DEFAULT strength become PARTIAL (a non-material NORMATIVE delta, M1 and L1 lacking the reporting duty): **FULL 114 · PARTIAL 67 · MEANINGFUL 15**. Still no material normative difference. |
| S-EVASION | DEP-025 D2 (RC-ENF-NPMRC-BYPASS) | A persistent bypass written into `.npmrc` after a refused flag is flagged only by L0; scored material. | Exclude evasion routes from materiality. | DEP-025 → FULL: **166 · 16 · 14**. |
| S-WF006 | WF-006 | The unlabeled imperative (M, M1, L0) and the "Default:" label (L1, K0, K1) state the same trigger and qualifier: no force difference. | Score the label as a force difference. | WF-006 → PARTIAL: **164 · 17 · 15**. |
| S-GOV017 | GOV-017 D4/D5 | The shared research invariant carries the same enforcement roots as ARC-020 (counted once in the root summary). | Score GOV-017 on text only. | GOV-017 → FULL: **166 · 16 · 14**. |
| S-MULTIEDIT | WF-010 D2 | M, L0, K1 omit MultiEdit from the reviewer's disallowedTools; non-material because no candidate disallows the shell. | The host has no separate MultiEdit tool (UNVERIFIED). | WF-010 → FULL: **166 · 15 · 15**. |
| S-Q04 | GOV-015 D3 | K0's extra Git prompt is non-material. | Treat a stalled headless `ask` as a different outcome. | GOV-015 → MEANINGFUL: **165 · 15 · 16**. |
| S-API019 | API-019 D1 | L1's indicative "Liveness avoids" read as binding (stricter tier). | Read it as a default. | L1 moves to the lower tier; label unchanged (PARTIAL). |
| S-REPORT | RC-TXT-REPORT-* extras (7 items) | Report and review-output content, not engineering outcome. | A benchmark that grades the agent's final report. | No policy label changes; the seven extras become scoring-relevant (see `EXTRA_GENUINE_ROOTS.json`). |

**Range over all alternatives** (WF-006 is one of the 51 DEFAULT policies, so S-WF006 is contained in S-VOCAB): FULL 114–168, PARTIAL 14–67, MEANINGFUL 13–16. In **no** reading does a material normative difference appear, so the predeclared ranking rule (PROTOCOL section 10) yields no global ranking under any option.

## 3. Host-dependent sensitivity (S-HOST, Q-08)

| Host behavior (NOT_RUN) | Consequence for Step 3 |
|---|---|
| Host applies PreToolUse `deny`/exit 2 as documented (refuses the command, shows the reason). | Static results stand: RC-ENF-REFERENCE-CMD-GATE, RC-ENF-DEP-INSTALL-GATE and the extras-level RC-ENF-DEP-REMOVAL-GATE separate the candidates as recorded. |
| Headless run turns `ask` into a refusal. | L1's project-reference `ask` behaves like a block; L1 stays in the gated tier. Git `ask` rows are identical in all six (v3 SAME_TASK_MATRIX_V3), so no new difference. |
| Headless run stalls on `ask`. | Git operations stall alike in all six; L1 also stalls on reference commands. A harness concern for later experiments, not a strictness difference. |
| PostToolUse/Stop feedback (exit 2 or `decision: block`) does not reach the agent. | The post-change roots (INNER-LAYER, TEST-REFS, TOP-LEVEL-TESTS, PKG-LISTS, COMPETING-TEST-FW, MIGRATION-REMINDER, NPMRC-BYPASS, IDE0005-BUILD only through build output) lose their in-session effect; the checkers still run when the agent invokes them. |
| A hook exceeds its budget (M1 sets none; L1 15 s/30 s; others 30 s/60 s). | PreToolUse is fail-closed (`onFailure: block`) in all six; post and Stop hooks are advisory. Budgets are recorded, not measured. |

## 4. Step 3 findings that may need a user decision before freeze

None blocks the Step 3 comparison. They are listed because they bear on the fairness of later practical experiments.

1. **Enforcement asymmetries (11 material roots).** M1, L1 and K1 carry more mechanical checks through their capability modules; M and L0 rely more on reminders. These are architecture-specific by design, not defects. Whether to keep them as part of the compared architectures or to harmonize them is a Step 4 or design question, not a Step 3 decision.
2. **Force vocabulary (RC-TXT-FORCE-VOCABULARY).** M1 and L1 do not say that departing from a default must be justified and reported. If a later benchmark scores deviation reporting, this matters.
3. **Dependency removal gate (RC-ENF-DEP-REMOVAL-GATE).** K1 blocks removal and bare-update commands with no command route; M and L0 allow them. A cleanup task takes a different path in each.
4. **Report-content differences (RC-TXT-REPORT-*).** Seven items; relevant only if final reports are graded.
5. **L1 lacks the "no fire-and-forget EF Core" technique (RC-TXT-L1-EF-FIRE-AND-FORGET).** Low likelihood, technique level.
6. **v3 record-text discrepancies (data only).** FG-L1-5a6df8a726's stored claim says peer-bypass commands "run only after the user confirms" (extras X0286), and FG-M1-159a4ef4c3's says the flags are denied "unless the marker is present" (X0791). PROBE-HOOK-02 (Q1–Q10) shows both scripts refuse the bypass with or without markers, as the current lines state. Proposal: correct the two claim texts in a future data repair; no template change.

Change proposals for items 2–5, if the user wants them, belong to a separately approved repair task with the one-rule-at-a-time regression procedure. Step 3 applies none.
