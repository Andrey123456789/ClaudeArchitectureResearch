# Architecture differences and limits — the six normalized Phase 5.4 candidates

Scope: the six **normalized** candidates in `release/` (byte-identical to Step 2 v3). The original Phase 5.3 candidates differ from these in 104 of 448 files through 21 researcher change rules (`PHASE54_METRIC_LINEAGE.md` §2). Nothing below says which original architecture was intrinsically better, and nothing below is a ranking. The axes are kept apart and never combined.

## 1. Canonical policy coverage

All six cover the same 196 canonical policies; all 1,176 cells were source-compared (owner text per atomic dimension). Canonical compliance: 1,156 equivalent, 20 stricter than canonical, 0 weaker.

## 2. Normative semantic parity

165 policies FULL parity, 16 PARTIAL with a non-material delta, 15 MEANINGFUL — and all 15 meaningful differences are on the enforcement axis. **No identical realistic study task gets a different required or forbidden outcome from the six texts.** The seven non-material normative deltas: GOV-006 materiality threshold for asking (M, M1, L0), GOV-007 "in the same change" (L0, L1, K1), GOV-009 L0 conflict wording, GOV-011 L0 lacks the framework-default exclusion, ARC-020 D1 capability selection (M1, L1, K1 — architecture-specific), API-019 liveness force, SEC-014 "must not fall back" (K0, K1).

## 3. Candidate-specific extra obligations (separate universe, not in canonical counts)

19 genuine extra-norm clusters (10 roots + the open Q-01):

| Root | Present | Absent |
|---|---|---|
| RC-ENF-DEP-REMOVAL-GATE | M1, K0 (marker), L1 (once), K1 (block) | M, L0 |
| RC-TXT-FORCE-VOCABULARY (deviation from a default must be reported) | M, L0, K0, K1 | M1, L1 |
| RC-TXT-L1-EF-FIRE-AND-FORGET | M, M1, L0, K0, K1 | L1 |
| RC-TXT-REPORT-DEPENDENCY | M, L0, L1, K0, K1 | M1 |
| RC-TXT-REPORT-DELEGATED | M, L0, L1, K0 | M1, K1 |
| RC-TXT-REPORT-DECISION | M, L1, K0, K1 | M1, L0 |
| RC-TXT-REPORT-SETTINGS | L1, K1 | M, M1, L0, K0 |
| RC-TXT-REPORT-PERSISTENCE | L1, K1 | M, M1, L0, K0 |
| RC-TXT-REPORT-DELIVERY | K0 | the other five |
| RC-TXT-REVIEW-PRAISE | M, M1, L0, K0, K1 | L1 |
| Q-01 raw-HTML scan prompt (open) | M, M1, L1, K0, K1 | L0 |

Seven roots concern only report or review content. Under FAIR-02 they stay; report-completeness results must be shown per dimension and per candidate with this caveat (especially decisions/deviations).

## 4. Delivery and instruction reachability

Parity at materiality. Two non-material delivery deltas: GOV-007 reaches M1 and K0 only through the architecture-decision skill; only L0 and L1 ship a `.gitignore` (SEC-001). Loading and routing mechanisms (root `CLAUDE.md`, maps, rules, skills, capability modules in M1/L1/K1) differ by design and are preserved (FAIR-01).

## 5. Enforcement behavior — the experimental independent variable (FAIR-01: preserved)

Tier per root (1 = strongest tier / number of tiers; equal tiers may be incomparable):

| Root | Policies | M | M1 | L0 | L1 | K0 | K1 | Evidence |
|---|---|---|---|---|---|---|---|---|
| RC-ENF-INNER-LAYER | ARC-002/008/019 | 2/2 | 1/2 | 2/2 | 1/2 | 2/2 | 1/2 | source-read |
| RC-ENF-MEDIATOR-PKG | ARC-009 | 2/3 | 1/3 | 1/3 | 1/3 | 2/3 | 3/3 | source-read |
| RC-ENF-REFERENCE-CMD-GATE | ARC-020 D5, GOV-017 D5 | 2/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | static + **live (F1)** |
| RC-ENF-TEST-REFS | ARC-028 | 1/3 | 1/3 | 3/3 | 1/3 | 2/3 | 1/3 | source-read |
| RC-ENF-MIGRATION-REMINDER | PST-009 | 2/2 | 1/2 | 2/2 | 1/2 | 2/2 | 1/2 | source-read |
| RC-ENF-MIGRATION-REMINDER | PST-010 | 1/2 | 2/2 | 1/2 | 2/2 | 1/2 | 1/2 | source-read |
| RC-ENF-COMPETING-TEST-FW | TST-001 | 2/2 | 1/2 | 2/2 | 1/2 | 2/2 | 1/2 | source-read |
| RC-ENF-IDE0005-BUILD | RUN-010 | 2/3 | 3/3 | 1/3 | 2/3 | 2/3 | 3/3 | CP-01 build (M, L0); others source-read |
| RC-ENF-PKG-LISTS | DEP-002 | 2/2 | 2/2 | 1/2 | 1/2 | 1/2 | 2/2 | source-read |
| RC-ENF-DEP-INSTALL-GATE | DEP-004 | 4/4 | 1/4 | 4/4 | 2/4 | 1/4 | 3/4 | static |
| RC-ENF-TOP-LEVEL-TESTS | DEP-024 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 2/3 | source-read |
| RC-ENF-NPMRC-BYPASS | DEP-025 | 2/2 | 2/2 | 1/2 | 2/2 | 2/2 | 2/2 | source-read; shell variants static + **live (B1)** |

Every candidate pair has roots in both directions: no candidate dominates another. Pattern: M1, L1, K1 add capability-module checks; M and L0 rely more on reminders; M1 and K0 gate commands with self-written markers; K1 ties reference commands to recorded decisions; L1 uses `ask` and a one-time refusal window. CP-01: M finds IDE0005 through `dotnet format`, L0 also at build (M unchanged by decision).

What benchmarks must measure about these differences (FAIR-01): hook interventions per run (by event, decision and reason), blocks, confirmation requests and how they were resolved, retries after a refusal, false positives (refusals of legitimate steps), missed violations (found by the shared oracle but not by the candidate), and execution overhead (hook time, extra turns, tokens).

## 6. Runtime-verified versus static-only

| Behavior | Level |
|---|---|
| Allow of safe commands; exit 2 and JSON deny blocking with the reason delivered; `ask` never treated as authorization (headless denial, also against a matching allow rule); Stop block once without a loop; reference-command gate per candidate | **LIVE_HOST_VERIFIED** (headless, CLI 2.1.293, all six) |
| PreToolUse `onFailure: block` | **LIVE_HOST_VERIFIED not applied** — fail-open when the hook cannot start, exits ≠ 2 or times out (all six; synthetic DX1–DX5 confirm the key has no effect) |
| Malformed input refusal; Git classification table; dependency/removal gates other than B1/F1; manifest and CPM checks | STATIC_VERIFIED (v3 suites, Step 3 probes) |
| Inner-layer, mediator, test-reference, competing-framework, package-list, top-level-test, migration-reminder, `.npmrc` checks | source-read (not executed) |
| Interactive prompts and human answers; candidate timeouts (M1 none, L1 15 s) | NOT_RUN |

## 7. Remaining uncertainties

1. **HOST-01** fail-open PreToolUse on hook failure (symmetric; needs a harness guard — see `BENCHMARK_HANDOFF_CONTRACT.md` G1).
2. Interactive behavior and the human approval policy for `ask` (all six ask for Git commits; L1 also for reference commands).
3. Headless runs deny every `ask`: a task that needs a commit or (in L1) a reference command cannot complete it headless. This is part of the enforcement variable but makes the run mode a primary design decision.
4. Most material enforcement roots are source-read only; their live effect on a full task is unknown until benchmarks run.
5. Same-family self-review throughout Stage A; no independent second-model or human review of the Step 3 challenge log.
6. Open user items Q-01, Q-02, Q-03, Q-12 (recommended: leave); data errors RD-01/RD-02 (claim texts only); Q-06 and Q-07 remain limitations.
7. Host-version dependence: every live fact is for CLI 2.1.293.

## 8. Not concluded

No architecture ranking, no quality or productivity claim, no claim about the original Phase 5.3 architectures, and no use of raw record or `MUST_NOT` counts as strictness.
