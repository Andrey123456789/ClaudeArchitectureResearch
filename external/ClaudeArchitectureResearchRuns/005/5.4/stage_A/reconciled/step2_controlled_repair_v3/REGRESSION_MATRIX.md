# Regression matrix (v3)

Every gate attempt in order, from `GATE_LOG.jsonl`. A failed attempt wrote no checkpoint; the change was repaired and the whole gate re-run. NOT_RUN is never counted as PASS.

| # | Change | Gate | Pass | Fail | Not run | Failed steps / cause |
|---:|---|---|---:|---:|---:|---|
| 1 | V3-0-BASELINE-REPLAY | FAIL |  |  |  | crash: Recorded after the fact: the gate crashed in DATASET (depgraph loading C01 patches.py) before it could log. Cause: bootstrap had not copied v2 _rules/*/before/ snapshots. Fixed in bootstrap_v3.py; gate.py now logs crashes itself. |
| 2 | V3-0-BASELINE-REPLAY | FAIL | 2242 | 1 | 20 | CUMULATIVE, TOOL_INTEGRITY (R27-FINAL: [A] no file outside the run root is newer than the run start, apart fr) |
| 3 | V3-0-BASELINE-REPLAY | PASS_WITH_DOCUMENTED_NOT_RUN | 2242 |  | 20 |  |
| 4 | PV2-02-FAILCLOSED-INPUT | FAIL | 2321 | 1 | 22 | CUMULATIVE (C06-REVIEW-SETS: new claims: every v1 added claim and proposal has a row; later added c) |
| 5 | PV2-02-FAILCLOSED-INPUT | PASS_WITH_DOCUMENTED_NOT_RUN | 2323 |  | 22 |  |
| 6 | PV2-01-GIT-GATING | FAIL | 2798 | 3 | 25 | CUMULATIVE, STRUCTURE (R04-HQ03-DEP003: instruction checker passes on the dependency fixture; R04-HQ03-DEP003: instruction checker accepts a project that has a real exception record) |
| 7 | PV2-01-GIT-GATING | PASS_WITH_DOCUMENTED_NOT_RUN | 2801 |  | 25 |  |
| 8 | PV2-03-K0-CPM-ROOT | PASS_WITH_DOCUMENTED_NOT_RUN | 2886 |  | 26 |  |
| 9 | PV2-04-M-FRONTEND-TESTS | FAIL |  |  |  | crash:                                                                                   ^ SyntaxError: closing parenthesis '}' does not match opening parenthesis '('  |
| 10 | PV2-04-M-FRONTEND-TESTS | FAIL | 2933 | 1 | 28 | CUMULATIVE (C06B-R22-APPLICABILITY: every distinct parenthesis part on the current view was read in the ce) |
| 11 | PV2-04-M-FRONTEND-TESTS | PASS_WITH_DOCUMENTED_NOT_RUN | 2934 |  | 28 |  |
| 12 | V3-D01-PASS23-OVERLAY | PASS_WITH_DOCUMENTED_NOT_RUN | 3028 |  | 29 |  |
| 13 | V3-D02-MODALITY86 | FAIL | 3123 | 2 | 30 | CUMULATIVE, FENCE (R27-FINAL: [A] immutable trees unchanged (hashes rebuilt); R27-FINAL: [A] no file outside the run root is newer than the run start, apart fr) |
| 14 | V3-D02-MODALITY86 | PASS_WITH_DOCUMENTED_NOT_RUN | 3127 |  | 30 |  |
| 15 | PV2-03B-CPM-IMPORT-PROVEN | PASS_WITH_DOCUMENTED_NOT_RUN | 3256 |  | 31 |  |
| 16 | V3-Q10-PACKAGEVERSION-VERSION | PASS_WITH_DOCUMENTED_NOT_RUN | 3416 |  | 32 |  |

## Cold audit, all suites on final bytes

| Suite | Pass | Fail | Not run |
|---|---:|---:|---:|
| C01-CPM-EFFECTIVE | 619 | 0 | 1 |
| C02-RUN008-EVIDENCE | 59 | 0 | 0 |
| C03-WF019-EXCEPTION | 90 | 0 | 1 |
| C04-GIT-CONDITIONAL | 59 | 0 | 1 |
| C05-PI012-RESIDUAL | 28 | 0 | 1 |
| C06-REVIEW-SETS | 123 | 0 | 1 |
| C06B-R22-APPLICABILITY | 44 | 0 | 0 |
| C07-PARITY-CLOSE | 64 | 0 | 1 |
| PV2-01-GIT-GATING | 480 | 0 | 3 |
| PV2-02-FAILCLOSED-INPUT | 89 | 0 | 2 |
| PV2-03-K0-CPM-ROOT | 85 | 0 | 1 |
| PV2-03B-CPM-IMPORT-PROVEN | 129 | 0 | 1 |
| PV2-04-M-FRONTEND-TESTS | 46 | 0 | 2 |
| R01-HQ06-PI012 | 17 | 0 | 0 |
| R02-HQ01-GOV015 | 64 | 0 | 2 |
| R03-HQ02-RUN021 | 42 | 0 | 1 |
| R04-HQ03-DEP003 | 146 | 0 | 2 |
| R05-HQ04-GOV017 | 43 | 0 | 1 |
| R06-HQ05-DEP025 | 223 | 0 | 1 |
| R07-81-SWAGGER | 37 | 0 | 1 |
| R08-82-K0CPM | 35 | 0 | 0 |
| R09-83-K1PERF | 7 | 0 | 0 |
| R10-84-L0MIGR | 8 | 0 | 0 |
| R11-87-CUSTOMSETTINGS | 28 | 0 | 0 |
| R12-87-K1LOCALDB | 9 | 0 | 0 |
| R13-87-TESTPRIORITY | 11 | 0 | 0 |
| R14-87-LANGVERSION | 12 | 0 | 0 |
| R15-85-HTTPTIMEOUT | 13 | 0 | 0 |
| R16-86-L1LIVENESS | 4 | 0 | 0 |
| R17-87-SECSCAN | 13 | 0 | 0 |
| R18-87-FASTSLOW | 6 | 0 | 0 |
| R19-87-CIUPDATES | 7 | 0 | 1 |
| R20-92-K0DESER | 5 | 0 | 0 |
| R21-10-NEWCLAUSES | 4 | 0 | 0 |
| R22-111-TRIGGER | 12 | 0 | 0 |
| R23-112-MIXED | 6 | 0 | 0 |
| R24-113-LIMITS | 5 | 0 | 0 |
| R25-COR103 | 25 | 0 | 0 |
| R26-DATASET | 27 | 0 | 0 |
| R27-FINAL | 293 | 0 | 5 |
| V3-0-BASELINE-REPLAY | 49 | 0 | 0 |
| V3-D01-PASS23-OVERLAY | 94 | 0 | 1 |
| V3-D02-MODALITY86 | 96 | 0 | 1 |
| V3-Q10-PACKAGEVERSION-VERSION | 160 | 0 | 1 |
| **Total** | **3416** | **0** | **32** |

Notes on attempts whose cause is not a defect of the change itself:

- V3-D02 attempt 1: FENCE and R27 failed only on files changed outside this session (v2 archive removed; v3 archive and interim review added). Recorded as ENV-01 to ENV-03 in `EXTERNAL_EVENTS.json`; `fence.py` and `final_audit.py` tolerate exactly those bytes (V3_ADAPTATIONS rows, selftest negatives). The change itself was unchanged between attempts.
- PV2-04 attempt 1 crashed on a quoting error in `adaptations.py`; V3-0 attempt 1 crashed before logging (bootstrap had not copied v2 rule snapshots). Both are tooling faults, fixed and re-gated.
- Cold audit (`AUDIT_ATTEMPTS/`): attempt 1 had one FAIL, a false positive in the audit's own Codex-name scan (prose lines stating the pruning); attempt 2 was stopped after section E because the new behavioral test itself named a later pass literally; attempt 3 is final, with no FAIL.

Suites: 27 v1 rules, 9 v2 changes, and one per v3 change (V3-0-BASELINE-REPLAY, PV2-02-FAILCLOSED-INPUT, PV2-01-GIT-GATING, PV2-03-K0-CPM-ROOT, PV2-04-M-FRONTEND-TESTS, V3-D01-PASS23-OVERLAY, V3-D02-MODALITY86, PV2-03B-CPM-IMPORT-PROVEN, V3-Q10-PACKAGEVERSION-VERSION). A v1 or v2 suite changed only with a row in `_tools/adaptations.py`.
