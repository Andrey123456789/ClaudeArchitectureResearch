# Experiment 005 / Phase 5.4 / Stage A / Step 3 — Six-way normative strictness comparison (final report, v1)

**Verdict: CONDITIONAL_GO** for freezing the six candidates as compared and for planning *later* practical experiments. Conditions are in section 9. Nothing in this step decided a user policy, edited a candidate, ran a benchmark, used Git, or started Step 4.

Output folder for independent review: `stage_A/reconciled/step3_six_way_strictness_v1/`.

## 1. Result in brief

- **196 policies × 6 candidates, all 1,176 cells source-compared.** Labels: **FULL_SEMANTIC_PARITY 165 · PARTIAL_PARITY_WITH_DELTA 16 · MEANINGFUL_DIVERGENCE 15 · CONTEXT_DEPENDENT 0 · UNVERIFIED 0.**
- **Normative text: parity at the materiality level.** No identical realistic study task gets a different required or forbidden outcome from the six texts. Seven normative deltas exist; none is material.
- **Enforcement: the only material differences.** All 15 MEANINGFUL policies differ in what is mechanically checked or gated (11 root causes). M1, L1 and K1 carry more mechanical checks through their capability modules; M and L0 rely more on reminders; M1 and K0 gate commands with self-written markers; K1 gates reference commands on recorded decisions. No candidate dominates another on every root.
- **Extras:** 1,777 active extra records → 797 clusters; 19 clusters (10 roots) are genuine extra norms likely to affect a comparable task, 1 is the open Q-01 decision, the rest are packaging, architecture-specific, derived or non-normative.
- **No global ranking** is defensible (predeclared rule, PROTOCOL section 10): there is no material normative difference to rank on, and the axes are not combined.
- **Live host behavior is NOT_RUN.** Every enforcement finding is static (scripts run directly or code read), not observed on a running agent.

## 2. Scope and inputs

- Input: the completed, immutable `stage_A/reconciled/step2_controlled_repair_v3/` (8,698 files). Preflight P01–P16 PASS before any result; the final manifest, all nine completed checkpoints, 448 template hashes, the 104/26 changed-file sets, the 6,498-row universe, 1,176 cells, suite tally and Q-01..Q-13 were verified (`PREFLIGHT_REPORT.md`). Every resumption re-ran P17 (inputs unchanged); gate D re-hashed the whole v3 tree at the end (no drift).
- Oracle: 194 inventory policies + GOV-017/GOV-018 (`UPSTREAM_FINGERPRINT.json`).
- Approved decisions respected: decision register 2026-11-03 (HQ-01..06, items 8.x–11.x), PV2-01..04, kit 74. Codex Pass 1–3 results used as recorded.

## 3. Method (frozen rubric: `PROTOCOL.md`, addenda AD-1..AD-8)

1. **Per policy, six cells side by side.** `_tools/dossier.py` printed the current v3 lines of every record Step 2 links to each cell; the analyst opened template files where excerpts were truncated, owners were missing (Step 2 overrides, 38 partial witnesses) or conditions could sit nearby. Judgments (`_judgments/B01..B30.py`) name atomic dimensions, the six-way label, a source-based justification for sameness, and every difference with tiers, axis, kind, materiality, evidence keys and, when material, an identical-task counterexample.
2. **Gate B per batch** (`_tools/judge.py`): schema, six-candidate coverage, label rules, every cited key resolved to current v3 lines, 15 pair labels per material dimension. 30/30 batches PASS; every attempt kept in `VALIDATION_ATTEMPTS/`.
3. **Static probes** (contract section 7): PROBE-HOOK-01 (dependency and reference commands), -02 (peer-dependency bypass, incl. marker cases), -03 (removal and bare update) ran each registered PreToolUse script on disposable copies; no Git, network, restore or host.
4. **Extras** (`_tools/extras.py`): clustering as a reading aid, an analyst decision for each of 797 clusters (455 accepted proposals, 342 decided), six-way presence by reading for genuine roots (`EXTRA_GENUINE_ROOTS.json`).
5. **Open decisions and sensitivity** (`OPEN_DECISIONS_AND_SENSITIVITY.md`), **hook/checker layers** (`HOOK_AND_CHECKER_EFFECTIVE_BEHAVIOR.md`), **assembly** (`_tools/assemble.py`), **gates C, D, E** (`_tools/gate_c.py`, `gate_d.py`, `validate.py`).

Materiality rule: a difference is material when an identical realistic study task would get a different required, forbidden or enforced outcome (a finding versus no finding counts). One source fact bearing on several policies keeps one root id.

## 4. Results

### 4.1 Policy labels

| Group (policies) | FULL | PARTIAL | MEANINGFUL |
|---|---|---|---|
| governance-product (19 GOV) | 13 | 6 | 0 |
| architecture (29 ARC) | 23 | 0 | 6 |
| persistence-data (10 PST) | 8 | 0 | 2 |
| api-errors-validation (22 API) | 21 | 1 | 0 |
| testing-quality (12 TST) | 10 | 1 | 1 |
| security (18 SEC) | 16 | 2 | 0 |
| runtime-code-performance (24 RUN) | 22 | 1 | 1 |
| dependencies-stack (26 DEP) | 18 | 4 | 4 |
| frontend (12 FE) | 12 | 0 | 0 |
| workflows-delivery (22 WF) | 21 | 1 | 0 |
| shared-research-invariants (GOV-017/018) | 1 | 0 | 1 |
| **Total (196)** | **165** | **16** | **15** |

Exact per-group counts are in `METRICS.json` (`labels_by_group`); the validator checks this table against it.

### 4.2 Cells

| Evidence level (contract 4 a–d) | Cells |
|---|---|
| (a) FULL_SOURCE_COMPARED | 1,176 |
| (b) PARTIAL_SOURCE_COMPARED | 0 |
| (c) MECHANICAL_WITNESS_ONLY | 0 |
| (d) UNVERIFIED | 0 |

What (a) means and does not mean: `METRIC_LINEAGE_AND_LIMITS.md` section 6 (owner text read for every dimension; not every line of every file; enforcement effects static only). Canonical compliance (separate axis): 1,156 EQUIVALENT, 20 STRICTER_THAN_CANONICAL, 0 WEAKER. The five v3 STRONGER_AND_WEAKER cells (API-014 K0/K1, API-019 K0/K1, GOV-007 K1) were challenged: each mixed label reflects record linkage (a stronger rule plus technique or reminder lines all six share), not a candidate-specific weakness. All 38 partial-witness cells were read and carry a note naming the lines.

### 4.3 Material differences (all on the enforcement axis)

Tier position per candidate (1 = strongest tier / number of tiers). Within a tier the candidates are equal or mutually incomparable (the five reference-command gates release on different conditions).

| Root | Policies | M | M1 | L0 | L1 | K0 | K1 | Basis |
|---|---|---|---|---|---|---|---|---|
| RC-ENF-INNER-LAYER | ARC-002, ARC-008, ARC-019 | 2/2 | 1/2 | 2/2 | 1/2 | 2/2 | 1/2 | source-read |
| RC-ENF-MEDIATOR-PKG | ARC-009 | 2/3 | 1/3 | 1/3 | 1/3 | 2/3 | 3/3 | source-read |
| RC-ENF-REFERENCE-CMD-GATE | ARC-020 D5, GOV-017 D5 | 2/2 | 1/2 | 1/2 | 1/2 | 1/2 | 1/2 | executed (PROBE-HOOK-01) |
| RC-ENF-TEST-REFS | ARC-028 | 1/3 | 1/3 | 3/3 | 1/3 | 2/3 | 1/3 | source-read |
| RC-ENF-MIGRATION-REMINDER | PST-009 | 2/2 | 1/2 | 2/2 | 1/2 | 2/2 | 1/2 | source-read |
| RC-ENF-MIGRATION-REMINDER | PST-010 | 1/2 | 2/2 | 1/2 | 2/2 | 1/2 | 1/2 | source-read |
| RC-ENF-COMPETING-TEST-FW | TST-001 | 2/2 | 1/2 | 2/2 | 1/2 | 2/2 | 1/2 | source-read |
| RC-ENF-IDE0005-BUILD | RUN-010 | 2/3 | 3/3 | 1/3 | 2/3 | 2/3 | 3/3 | source-read (no build) |
| RC-ENF-PKG-LISTS | DEP-002 | 2/2 | 2/2 | 1/2 | 1/2 | 1/2 | 2/2 | source-read |
| RC-ENF-DEP-INSTALL-GATE | DEP-004 | 4/4 | 1/4 | 4/4 | 2/4 | 1/4 | 3/4 | executed (PROBE-HOOK-01) |
| RC-ENF-TOP-LEVEL-TESTS | DEP-024 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 2/3 | source-read |
| RC-ENF-NPMRC-BYPASS | DEP-025 | 2/2 | 2/2 | 1/2 | 2/2 | 2/2 | 2/2 | source-read; shell variants executed |

Every one of these has an identical-task counterexample in `POLICY_SIX_WAY_MATRIX.jsonl` and 15 pair rows in `POLICY_PAIRWISE_DIFFERENCES.jsonl` (225 rows: 79 B_STRONGER, 51 A_STRONGER, 75 SAME, 20 INCOMPARABLE). Each was challenged in gate C (`SEMANTIC_CHALLENGE_LOG.jsonl`): 13 HOLD, 2 HOLD with a stated limit (IDE0005: build not run; NPMRC: material only under the evasion reading).

Two examples:
- *Reference command* (`dotnet add src/Shop.Application reference src/Shop.Infrastructure`): M executes it and reminds afterwards; L0 and K1 block it; M1 and K0 refuse until the agent adds a self-written marker; L1 asks the user. Editing the `.csproj` directly bypasses every pre-execution gate in all six.
- *Pinned install* (`dotnet add … package Serilog.AspNetCore --version 8.0.3` without prior checks): M1 and K0 refuse until the marker, L1 refuses once, M, L0 and K1 run it (K1 blocks only versionless installs).

### 4.4 Non-material deltas (recorded, not counted as divergence)

- **Normative (7):** GOV-006 (M, M1, L0 add a materiality threshold for asking), GOV-007 ("in the same change" in L0, L1, K1), GOV-009 (L0 conflict wording), GOV-011 (L0 lacks the framework-default exclusion), ARC-020 D1 (capability-selection item in M1, L1, K1 only — architecture-specific), API-019 (liveness force), SEC-014 (K0, K1 "must not fall back" vs "prefer").
- **Delivery (2):** GOV-007 (M1, K0 carry the rule only in architecture-decision), SEC-001 (only L0 and L1 ship a `.gitignore`).
- **Enforcement (11):** GOV-003, GOV-015 (Q-04), ARC-020 D4 / GOV-017 D4 (reserved-graph feedback), TST-009, RUN-009, DEP-003, DEP-005, DEP-006 (Q-11), DEP-007, WF-010 (reviewer MultiEdit).

### 4.5 Partial order per axis (no global ranking)

| Axis | Relation |
|---|---|
| Normative | Parity at the materiality level; no strict order. |
| Delivery / reachability | Parity at the materiality level. |
| Enforcement | Per-root tiers in 4.3. Every candidate pair has roots in both directions (`PARTIAL_ORDER_BY_AXIS.json`), so no candidate dominates another. |
| Canonical compliance | 1,156 EQUIVALENT, 20 STRICTER, 0 WEAKER cells. |

Ranking rule evaluation: condition 1 met (100% FULL cells); condition 2 not met (no material normative difference); therefore no ranking. The axes are never combined into one score, and strictness says nothing about quality or productivity.

### 4.6 Candidate-specific extras (`EXTRA_OBLIGATIONS_SIX_WAY.jsonl`)

| Class | Clusters |
|---|---|
| GENUINE_EXTRA_NORM | 19 |
| ARCHITECTURE_SPECIFIC_DIVERGENCE | 172 |
| SAME_NORM_DIFFERENT_PACKAGING | 261 |
| REDUNDANT_DERIVED_OR_NON_NORMATIVE | 344 |
| UNRESOLVED_OR_DECISION_DEPENDENT | 1 |

Genuine roots with six-way presence read from source (`EXTRA_GENUINE_ROOTS.json`):

| Root | Present | Absent | Effect |
|---|---|---|---|
| RC-ENF-DEP-REMOVAL-GATE | M1, K0 (marker), L1 (once), K1 (block) | M, L0 (allow, remind) | Engineering path of a cleanup task (PROBE-HOOK-03) |
| RC-TXT-FORCE-VOCABULARY ("default — deviation needs a concrete reason and must be reported") | M, L0, K0, K1 | M1, L1 | Deviation reporting |
| RC-TXT-L1-EF-FIRE-AND-FORGET | M, M1, L0, K0, K1 | L1 | Technique warning |
| RC-TXT-REPORT-DEPENDENCY | M, L0, L1, K0, K1 | M1 | Report content |
| RC-TXT-REPORT-DELEGATED | M, L0, L1, K0 | M1, K1 | Report content |
| RC-TXT-REPORT-DECISION | M, L1, K0, K1 | M1, L0 | Report content |
| RC-TXT-REPORT-SETTINGS | L1, K1 | M, M1, L0, K0 | Report content |
| RC-TXT-REPORT-PERSISTENCE | L1, K1 | M, M1, L0, K0 | Report content |
| RC-TXT-REPORT-DELIVERY | K0 | the other five | Report content |
| RC-TXT-REVIEW-PRAISE | M, M1, L0, K0, K1 | L1 | Review tone |
| Q-01 raw-HTML scan prompt (open) | M, M1, L1, K0, K1 | L0 | Hypothetical for an Angular SPA |

None was adopted as a common oracle policy. Most architecture-specific extras are enforcement mechanics already scored under a canonical policy and linked to its root.

### 4.7 Static vs live evidence

Static: v3 suites (3,416 PASS · 0 FAIL · 32 NOT_RUN over 44 suites) and the three Step 3 probes (24 command cases × 6 candidates × 2 runs). Git `ask`/`allow` rows are identical in all six; malformed input is refused by all six; markers never open the peer-dependency bypass in any candidate. Live host: NOT_RUN (Q-08); a manual reproduction procedure is in `HOOK_AND_CHECKER_EFFECTIVE_BEHAVIOR.md` section 6.

### 4.8 Sensitivity

Over every alternative reading (`OPEN_DECISIONS_AND_SENSITIVITY.md` section 2): FULL 114–168, PARTIAL 14–67, MEANINGFUL 13–16. The largest swing is S-VOCAB (treating the force vocabulary as part of every canonical DEFAULT policy: 51 FULL → PARTIAL, all non-material). No reading creates a material normative difference or a ranking.

## 5. Defensible comparisons

1. The six candidates state the same 196 canonical policies with the same required and forbidden outcomes for realistic study tasks.
2. They differ materially in **enforcement** on 11 roots, with no dominance relation between any two candidates.
3. M1, L1 and K1 add capability-module checks (inner layers, competing test frameworks, test references, top-level tests); M and L0 have fewer mechanical checks; L0 alone catches an `.npmrc` bypass and reports IDE0005 at build; K1 alone ties reference commands to recorded decisions and blocks removals outright.
4. Ten genuine extra-norm roots differ by candidate; seven of them concern only what the final report or review says.

## 6. Architecture-specific differences, defects and proposals

- Enforcement asymmetries, capability-selection rules (M1, L1, K1), decision-recording locations and register mechanics (K0, K1) are **architecture-specific**, not defects.
- **CP-01 (proposal, not applied):** M's `.editorconfig:32-33` says build-time IDE0005 needs `GenerateDocumentationFile`, but M's `Directory.Build.props` does not set it. Either add it (with `NoWarn CS1591`) or correct the comment. Expected impact: RUN-010 D2 would place M with L0. Needs a separately approved repair with full regression.
- **RD-01, RD-02 (data only):** two v3 claim texts (FG-L1-5a6df8a726, FG-M1-159a4ef4c3) misstate how the peer-bypass deny opens; the current lines and PROBE-HOOK-02 show no route in either. Proposal: correct the records in a future data repair.
- Step 3 corrected its own extras notes once (AD-8: PV2-02 scope); all attempts are kept.

## 7. Limitations

1. **Live host NOT_RUN** (Q-08): no claim that any hook stops, prompts or corrects a running agent.
2. **Same-family self-review:** the challenge log is a self-challenge by the same model family as the judge, not independent confirmation.
3. Checker logic outside the three probes is source-read; no build was run (IDE0005, code style).
4. Extras completeness is bounded by the recorded universe (Q-07: three of six Codex strategy families).
5. Stored modality was not used; 492 soft-stored "do not" records remain unreviewed as a class (Q-06).
6. "FULL_SOURCE_COMPARED" covers the owner text of each dimension, not every line of every file.
7. Nothing here measures quality, productivity or benchmark performance.

## 8. User decision queue

| Item | Status | Blocks | Step 3 recommendation |
|---|---|---|---|
| Q-01 raw-HTML scan prompt in L0 | OPEN | nothing in Step 3 | leave as written |
| Q-02 blank PreToolUse command | OPEN | nothing | leave |
| Q-03 event/tool mismatch | OPEN | nothing | leave; check in host pilot |
| Q-12 central-file naming | OPEN | nothing | leave |
| Enforcement asymmetries (FAIR-01) | for the user | interpretation of later experiments | keep as part of the compared architectures and log hook interventions per candidate |
| Report-content extras and force vocabulary (FAIR-02) | for the user | only if reports are graded | decide before defining report-based metrics |
| CP-01 (M IDE0005 configuration) | for the user | nothing in Step 3 | decide whether M should report IDE0005 at build |

Q-04, Q-05, Q-11 stay OBSERVATION; Q-06 OPEN_CLASS and Q-07 residue stay as limitations; Q-08 NOT_RUN; Q-09 QUALIFIED; Q-10 RESOLVED; Q-13 ENVIRONMENT.

## 9. Verdict: CONDITIONAL_GO

**GO aspects.** Normative parity at the materiality level across all 196 policies, every cell source-compared, no UNVERIFIED or CONTEXT_DEPENDENT policy, gates B (30/30), C and D passing, inputs unchanged. Nothing found requires a change before the candidates can be frozen as compared.

**Conditions before later practical experiments:**
1. Run the minimal host pilot (`HOOK_AND_CHECKER_EFFECTIVE_BEHAVIOR.md` section 6) to replace NOT_RUN for `ask`/`deny`/exit 2/`onFailure`/Stop and headless `ask`, because all material differences are hook-mediated.
2. The user takes the open decisions in section 8 (the recommended options change no Step 3 conclusion) and states whether the enforcement asymmetries and report-content extras are accepted as part of the compared architectures.
3. Optionally, an independent (different-model or fresh-session) review of `SEMANTIC_CHALLENGE_LOG.jsonl`.

**Not NO_GO,** because no finding contradicts an approved decision, no candidate is normatively weaker on a material dimension, and every open item is either decision-dependent or a verification gap with a documented procedure.

## 10. Deliverables and reproduction

| Deliverable | File |
|---|---|
| State and resume | `STATE.json`, `RESUME.md` |
| Rubric and inputs | `PROTOCOL.md`, `UPSTREAM_FINGERPRINT.json`, `UPSTREAM_V3_TREE_HASHES.json`, `PREFLIGHT_REPORT.md` |
| Six-way matrix | `POLICY_SIX_WAY_MATRIX.jsonl` (196), `POLICY_CELL_INDEX.jsonl` (1,176) |
| Pairwise | `POLICY_PAIRWISE_DIFFERENCES.jsonl` (225) |
| Extras | `EXTRA_OBLIGATIONS_SIX_WAY.jsonl` (797), `EXTRA_GENUINE_ROOTS.json` |
| Hooks and checkers | `HOOK_AND_CHECKER_EFFECTIVE_BEHAVIOR.md`, `HOOK_PROBE_RESULTS.json`, `HOOK_PROBE2_RESULTS.json`, `HOOK_PROBE3_RESULTS.json` |
| Decisions and sensitivity | `OPEN_DECISIONS_AND_SENSITIVITY.md` |
| Metrics | `METRIC_LINEAGE_AND_LIMITS.md`, `METRICS.json`, `ROOT_CAUSE_SUMMARY.json`, `PARTIAL_ORDER_BY_AXIS.json`, `V3_CHANGED_FILES_IMPACT.jsonl` |
| Challenge and validation | `SEMANTIC_CHALLENGE_LOG.jsonl`, `VALIDATION_REPORT.json`, `VALIDATION_ATTEMPTS/` |

Reproduce (read-only toward every predecessor, from the output folder): `python -B _tools/preflight.py`, `python -B _tools/judge.py status`, `python -B _tools/extras.py status`, `python -B _tools/assemble.py`, `python -B _tools/gate_c.py`, `python -B _tools/gate_d.py`, `python -B _tools/validate.py`.

**STOP.** Step 3 ends here. Step 4, template unification, application generation and any change to a predecessor tree are out of scope and were not started.
