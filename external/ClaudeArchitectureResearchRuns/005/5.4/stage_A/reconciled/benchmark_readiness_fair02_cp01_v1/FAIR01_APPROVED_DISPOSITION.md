# FAIR-01 — Approved disposition: preserve enforcement differences

**Decision (user, recorded 2026-11-07 for kit 76):** FAIR-01 is **approved as "preserve"**. All architecture-specific hooks, checkers, delivery and loading strategies and enforcement semantics of **M, M1, L0, L1, K0 and K1** stay exactly as in `step2_controlled_repair_v3/`. They are part of the compared architectures. **Nothing is modified or harmonized**, in this task or by later benchmark preparation, unless the user decides otherwise in a separate, explicit decision.

Source of the open item: Step 3 `FINAL_STAGE_A_STEP3_SIX_WAY_COMPARISON_REPORT.md` section 8 and `OPEN_DECISIONS_AND_SENSITIVITY.md` section 4 item 1. This task changed no candidate file (verified by `PROTECTED_INPUTS_VERIFICATION.json`).

## 1. What is preserved

### 1.1 Material enforcement roots (Step 3, all on the enforcement axis)

| Root | Policies | What differs (short) | Step 3 basis |
|---|---|---|---|
| RC-ENF-INNER-LAYER | ARC-002, ARC-008, ARC-019 | M1, L1, K1 check inner-layer dependencies; M, L0, K0 do not | source-read |
| RC-ENF-MEDIATOR-PKG | ARC-009 | Three tiers of mediator-package gating | source-read |
| RC-ENF-REFERENCE-CMD-GATE | ARC-020 D5, GOV-017 D5 | M runs project-reference commands and reminds; L0, K1 block; M1, K0 require a self-written marker; L1 asks | executed (PROBE-HOOK-01) |
| RC-ENF-TEST-REFS | ARC-028 | Test-project reference checks in three tiers | source-read |
| RC-ENF-MIGRATION-REMINDER | PST-009, PST-010 | Migration reminders differ by trigger | source-read |
| RC-ENF-COMPETING-TEST-FW | TST-001 | M1, L1, K1 detect a competing test framework | source-read |
| RC-ENF-IDE0005-BUILD | RUN-010 | L0's build reports IDE0005; M's build does not (now **execution-confirmed** for M and L0 by CP-01); M's `dotnet format` route detects it | CP-01 executed (M, L0); others source-read |
| RC-ENF-PKG-LISTS | DEP-002 | Post-change package-list checks in K0, L0, L1 | source-read |
| RC-ENF-DEP-INSTALL-GATE | DEP-004 | Four tiers for pinned installs without prior checks | executed (PROBE-HOOK-01) |
| RC-ENF-TOP-LEVEL-TESTS | DEP-024 | L1, then K1, check top-level test packages | source-read |
| RC-ENF-NPMRC-BYPASS | DEP-025 | Only L0 flags a persistent `.npmrc` bypass | source-read; shell variants executed |

### 1.2 Also preserved

- Non-material enforcement deltas: RC-ENF-CODESTYLE-BUILD (RUN-009), RC-ENF-CPM-NO-SDK (DEP-006, Q-11), RC-ENF-GIT-Q04 (GOV-015, Q-04), RC-ENF-NPM-LOCKFILE (DEP-007), RC-ENF-RESERVED-GRAPH (ARC-020/GOV-017 D4), RC-ENF-REVIEWER-MULTIEDIT (WF-010), RC-ENF-TEST-CHANGE-REMINDER-SCOPE (TST-009), and the remaining items listed in Step 3 section 4.4.
- Extras-level enforcement root RC-ENF-DEP-REMOVAL-GATE (removal and bare-update commands: M1/K0 marker, L1 deny once, K1 block, M/L0 allow).
- Delivery and loading strategies (always-loaded vs path-scoped vs skill-loaded owners; capability modules in M1, L1, K1; decision registers in K0, K1), PreToolUse fail-closed behavior and hook time budgets.
- Open user items that touch enforcement remain as Step 3 left them: Q-02, Q-03 (recommended "leave"), Q-08 (live host NOT_RUN).

## 2. What later benchmarks should measure (per run, per candidate)

Because the differences are kept, benchmarks must **observe** them rather than assume them. Static hook observations (Step 2 suites, Step 3 PROBE-HOOK-01/02/03, CP-01) are **not substitutes** for real agent-host observations: they show what a script returns for a payload, not what a live Claude Code host shows, applies, or how the agent reacts.

| Measure | Definition | Minimum evidence to archive |
|---|---|---|
| Blocked operations | Tool calls refused by a hook or the host (deny, exit 2, `onFailure: block`), with the rule/hook that refused | Host event log or transcript entries with timestamps; hook stdout/stderr where available |
| Asked operations | Calls that triggered an `ask`/confirmation, how they were resolved (approved, denied, timed out, stalled headless) | Same, plus the resolution |
| Enforcement effectiveness | For each planted or naturally occurring violation (e.g. forbidden project reference, unused using, unpinned install): prevented before execution, detected after, or missed | Final repository diff and independent post-run checker results (one shared oracle checker for all six, not each candidate's own checker) |
| False positives | Blocks, asks or warnings on compliant actions (e.g. M's per-build `EnableGenerateDocumentationFile` hint, a refused but legitimate command) | Event log classified against the task's ground truth |
| Retries | Repeated attempts after a block (same or modified command; marker writing in M1/K0; L1's deny-once retry) | Ordered event log |
| Evasion or workaround | Direct file edits that bypass a command gate (e.g. editing `.csproj` instead of `dotnet add reference`), configuration edits to silence checks | Diff of build/config files; event log |
| User intervention | Number and kind of human inputs needed to continue (approvals, clarifications, unblock actions) | Harness log of injected user messages |
| Usage cost | Input/output tokens, tool calls, wall-clock time, model, effort level | Host usage export; `NOT_AVAILABLE` when the host does not expose it |

Interpretation rules:

1. Enforcement measures are **descriptive per candidate**. They are not combined with the primary code-quality outcome and do not by themselves rank architectures (Step 3 found no dominance relation on any pair).
2. A static probe result may be cited as an expectation; only a live host observation counts as an observed enforcement effect.
3. Run settings (model, effort, host version, interactive vs headless, permission mode) must be identical across candidates and recorded, because `ask` behavior depends on them (Step 3 S-HOST).

## 3. Consequence for CP-01

CP-01 confirmed that M's build does not report IDE0005 and L0's does, and that M's `dotnet format` route detects it. Under this disposition the build-time difference is an **architecture-specific enforcement difference** and is preserved; M is not changed (see `CP01_CORRECTION_PROPOSAL.md`, option 0).
