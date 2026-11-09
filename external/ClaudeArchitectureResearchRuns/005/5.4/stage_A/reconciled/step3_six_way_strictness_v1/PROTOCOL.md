# Step 3 protocol — six-way evidence-based normative strictness comparison (v1)

**Frozen on 2026-11-06, before the first policy judgment.** Any later change to this rubric must be added as a dated addendum at the end, never by editing the text above it.

Contract: `_STAGE_A_KIT/75_CLAUDE_STAGE_A_STEP3_SIX_WAY_STRICTNESS_TASK_EN.md`. Output root: `stage_A/reconciled/step3_six_way_strictness_v1/` (the only place this run writes).

## 1. Inputs (read-only)

| Input | Use |
|---|---|
| `step2_controlled_repair_v3/candidates/<C>/template/` (448 files) | **The compared objects.** Every quoted line is read from these bytes. |
| `inputs/<C>/source/inventory.json` + `shared-research-invariants.json` | The frozen 196-policy oracle (194 + GOV-017/018). |
| v3 `REPAIRED_CLASSIFICATIONS.jsonl` (6,498 rows, 3 inactive kept) | Owner records, modality, delivery context, extras. |
| v3 `REPAIRED_POLICY_COVERAGE.jsonl`, `POLICY_PARITY_MATRIX.jsonl` (1,176 rows each) | Which records Step 2 links to each cell; v3 check levels and reviews. |
| `step2_classification/per_candidate/<C>/STRENGTH_DIVERGENCES.jsonl` | Step 2 per-candidate strength divergences (flag only). |
| v3 `PARTIAL_WITNESSES_38.jsonl`, the five `STRONGER_AND_WEAKER_EVIDENCE` cells | Cells to challenge explicitly. |
| v3 `V3_FINAL_MANIFEST.json`, `V2_TO_V3_FILE_CROSSWALK.jsonl`, `V2_TO_V3_CROSSWALK.jsonl` | Changes against frozen and v2 (104 and 26 files; 6,498 claim rows). |
| v3 `PASS2_PASS3_ADJUDICATION.jsonl`, `UNIQUE_ISSUE_CLUSTERS.jsonl`; `step1_union_augmented_pass1/` | Codex provenance. **Used as recorded; not re-adjudicated.** |
| v3 `UNRESOLVED_AND_USER_DECISION_QUEUE.jsonl` | Q-01 to Q-13. |
| v3 `FINAL_SUITE_TALLY.json`, `FINAL_AUDIT_RESULTS.jsonl`, `SAME_TASK_MATRIX_V3.json`, `INTERACTION_MATRIX_V3.json`, `_investigation/` | Inherited static behavior evidence (direct script runs). Never relabelled as live-host evidence. |
| Approved decisions: decision register 2026-11-03 (HQ-01..HQ-06, items 8.x–11.x), kit 62, `Stage_A_Step2_Post_V2_Approved_Decisions_EN.md` (PV2-01..04), kit 74 | Approved readings Step 3 must respect. Step 3 makes no new policy decision. |

Hashes of all of these are in `UPSTREAM_FINGERPRINT.json`.

## 2. Universes — never mixed in one count

1. **Policies:** 196 canonical ids.
2. **Cells:** 196 × 6 = 1,176 `(candidate, policy)` cells.
3. **Atomic dimensions:** the independently testable parts of one canonical policy, written per policy by the analyst (D1, D2, …).
4. **Classification records:** 6,498 v3 rows (6,495 active). Used for owners and the extras inventory; counts of records are never a strictness measure.
5. **Extra-obligation clusters:** deduplicated across candidates (section 8).
6. **Behavior:** inherited v3 direct-script outcomes; live-host behavior is a separate, NOT_RUN layer.

## 3. Reading procedure per policy

For each policy, `_tools/dossier.py` writes a reading aid (`_dossiers/<batch>.md`) with the canonical text and, for each of the six candidates, the **current v3 source lines** of every record Step 2 links to the cell (direct, partial, stronger/weaker), deduplicated by line range, with the record's stored modality, its stored strength against canonical, its delivery class and its v2→v3 status. The analyst reads the six cells **side by side**, opens the template file around an owner when the excerpt is truncated or a condition may sit in neighbouring lines, and records a judgment in `_judgments/<batch>.py`. Stored Step 2 labels are context, never a Step 3 finding.

## 4. Cell evidence levels (contract 4 a–d)

| Level | Meaning |
|---|---|
| `FULL_SOURCE_COMPARED` | The analyst read the cell's v3 owner text for **every** atomic dimension of the policy and compared it with the other five. |
| `PARTIAL_SOURCE_COMPARED` | Owner text read for some dimensions; the rest rests on the Step 2 link and a resolving witness. The judgment names the unread dimensions. |
| `MECHANICAL_WITNESS_ONLY` | No Step 3 reading; only the mechanical check that the witness resolves at a current line. Parity is withheld. |
| `UNVERIFIED` | The owner text cannot be resolved, or the cell's outcome depends on behavior that was not run. |

Every one of the 1,176 cells receives exactly one level. Counts are reported as (a)–(d).

## 5. Comparison axes (reported separately)

1. **Normative content:** what is demanded, forbidden, preferred or permitted; deontic force (MUST, MUST_NOT, SHOULD, SHOULD_NOT, DEFAULT, MAY, REQUIRES_APPROVAL, CONDITIONAL, COMPOUND) read from source meaning; scope and applicability (platform, task type, path, phase, trigger, condition, exception, approval boundary). A file-loading trigger is **not** an applicability condition.
2. **Delivery / reachability:** how the owner reaches the agent. `_tools/reach.py` gives a mechanical class per record: `ROOT_ALWAYS`, `IMPORT_ALWAYS`, `RULE_ALWAYS`, `RULE_ANY_FILE`, `RULE_PATH`, `HOOK`, `BUILD_TOOL`, `SETTINGS`, `SKILL`, `CAPABILITY`, `SUBAGENT`, `SKILL_REF`, `CHECKER`, `HUMAN_MAP`, `OTHER`. A reach difference is recorded as **material** only when the analyst finds that, for a task inside the policy's trigger, one candidate's owner is always present while another's is present only if a skill, reference or path rule is loaded for that task, and the policy's trigger does not itself imply that loading. A knowledge skill's technique example is never promoted to an always-active policy.
3. **Enforcement:** prompt text versus mechanically executed checks (hooks, checkers, build configuration). Static behavior is the inherited v3 direct-script evidence. How the live Claude Code host applies `ask`, `deny`, exit 2 or `onFailure` is **NOT_RUN** unless Step 3 observes it.
4. **Canonical compliance** (per cell, against the oracle): `EQUIVALENT`, `STRICTER_THAN_CANONICAL`, `WEAKER_THAN_CANONICAL`, `PARTIAL`, `INCOMPARABLE`. This axis is never merged with pairwise strictness, and neither implies quality, productivity or benchmark performance.

## 6. Labels

**Atomic dimension, per candidate pair (A, B):** `SAME`, `A_STRONGER`, `B_STRONGER`, `INCOMPARABLE`, `NOT_APPLICABLE`, `UNVERIFIED`.
- A is stronger on a dimension when, for every identical task inside both scopes, A's allowed outcomes are a subset of B's and the subset is proper for at least one realistic task.
- If the allowed sets are not nested, the pair is `INCOMPARABLE`.
- If the ordering reverses between task scopes (a condition or exception in one candidate), the pair is `INCOMPARABLE` for the dimension and the policy is `CONTEXT_DEPENDENT`, with the task scopes recorded.
- If either cell is `UNVERIFIED` or `MECHANICAL_WITNESS_ONLY` for the dimension, the pair is `UNVERIFIED`. If the dimension does not exist for a candidate by design (for example an architecture without that surface), `NOT_APPLICABLE` with a reason.

**Policy, six-way:** decided in this order.
1. `UNVERIFIED` — some cell lacks a source reading of a dimension that decides the comparison.
2. `CONTEXT_DEPENDENT` — the candidate order reverses across task scopes, or depends on an open user decision or on two defensible readings (both recorded).
3. `MEANINGFUL_DIVERGENCE` — at least one material difference: an identical realistic study task would get a different required, forbidden or enforced outcome. A counterexample is mandatory.
4. `PARTIAL_PARITY_WITH_DELTA` — core requirement the same in all six; at least one recorded non-material delta (extra qualifier, example, packaging, reach that the trigger already implies, non-blocking advice) or a material delta that only an edge task would expose.
5. `FULL_SEMANTIC_PARITY` — all six cells `FULL_SOURCE_COMPARED`, every dimension the same in content, force and scope, and no material reach or enforcement difference. A concise source-based justification is mandatory; a matching label is not one.

**Variance kind** for each recorded difference: `TRUE_NORMATIVE_VARIANCE`, `DELIVERY_REACHABILITY_VARIANCE`, `ENFORCED_BEHAVIOR_VARIANCE`, `CANDIDATE_SPECIFIC_TECHNIQUE`, `HARMLESS_PARAPHRASE`, `UNCERTAINTY`. Architectural differences are not called defects unless they contradict an approved rule; a defect is reported with a proposed minimal remediation and is **not** applied.

## 7. Pairwise records

For every **material** difference, `POLICY_PAIRWISE_DIFFERENCES.jsonl` gets all 15 candidate pairs for that dimension, each with a label from section 6, the evidence keys of both sides and the counterexample, or an explicit `NOT_APPLICABLE`/`UNVERIFIED`. Non-material deltas are recorded in the policy record only. No pair is invented to fill a grid.

## 8. Extra-obligation inventory

Input: active v3 records classified `EXTRA_PRODUCT`, `EXTRA_WORKFLOW`, `CANONICAL_PLUS_DELTA` (the remainder beyond the canonical part) and `MIXED`, plus the Codex Pass 1 proposals/facets and the v3 Pass 2/3 adjudication (as recorded). `_tools/extras.py` groups records by closest canonical policy and text similarity into candidate clusters; the analyst reads every cluster, merges or splits it, and decides:
- whether it is a true obligation or an example, implementation default, technique or architecture-specific organizational description;
- presence, effective force and delivery in each of the six;
- one class: `GENUINE_EXTRA_NORM` (likely to affect a comparable task), `ARCHITECTURE_SPECIFIC_DIVERGENCE`, `SAME_NORM_DIFFERENT_PACKAGING`, `REDUNDANT_DERIVED_OR_NON_NORMATIVE`, `UNRESOLVED_OR_DECISION_DEPENDENT`.

An extra present in five candidates is **not** adopted as a common oracle policy. Q-01 (L0 raw HTML) is handled as an open decision, not by editing L0.

## 9. Open decisions and sensitivity

Each of Q-01..Q-13 is classified `RESOLVED`, `OBSERVATION`, `ENVIRONMENT`, `NOT_RUN` or `USER_DECISION`, without re-opening resolved items. For each true user decision: the narrow factual difference, its impact on study tasks, minimal options, a reasoned recommendation, and whether each option changes a Step 3 conclusion or later benchmark comparability. Nothing is decided without user authorization. For PI-012/HQ-06 and Q-06, no ranking uses raw modality counts; where a conclusion depends on two defensible readings, both are shown in a sensitivity table.

## 10. Ranking rule (predeclared)

No global ranking is reported unless **all** hold:
1. at least 95% of the 1,176 cells are `FULL_SOURCE_COMPARED`;
2. on the normative axis, for every candidate pair, the number of policies where one side is stronger on a material dimension and the other is never stronger exceeds the reverse count by more than the number of that pair's `UNVERIFIED` plus `CONTEXT_DEPENDENT` policies, and the resulting relation is acyclic;
3. the order is unchanged under every option of every open user decision in the sensitivity table.

Otherwise the report gives a **partial order per axis** and scenario-specific differences. The normative and enforcement axes are never combined into one score.

## 11. Gates

- **A Preflight:** `_tools/preflight.py` (hash and count identity with v3; frozen input untouched). Re-run read-only on every resumption.
- **B Per-batch structural:** `_tools/judge.py check <batch>` — every policy of the batch judged once; every candidate covered once per policy; every cited key exists, is linked to or readable at a resolving current v3 line; label and schema valid; tiers cover all six or declare `NOT_APPLICABLE`/`UNVERIFIED`; counters add up. Writes `CHECKPOINTS/policies/<PID>.json` and appends the cumulative tally to `CHECKPOINTS/gates/`.
- **C Semantic challenge:** every material difference and every comparison that could overturn an approved decision or benchmark fairness is challenged with both sides' evidence, exceptions and a counterexample (`SEMANTIC_CHALLENGE_LOG.jsonl`). This is a same-family self-challenge and is labelled so.
- **D Metric and provenance:** counts reconcile with v3; direct changes, indirect changes and limits stay distinct; Pass 1/2/3 provenance intact; no Codex edit re-applied.
- **E Final cold audit:** `_tools/validate.py` re-reads the final artifacts without trusting intermediate PASS labels, recomputes every count, re-hashes inputs, re-resolves every source anchor and decision cross-reference. Every attempt is kept in `VALIDATION_ATTEMPTS/`.

## 12. Checkpoints and resumption

One checkpoint per policy, per extra cluster batch and per gate, written atomically. `STATE.json` and `RESUME.md` name the next unit and the exact command. A context compaction never restarts completed batches; the rubric above is not changed silently.

## 13. Out of scope

No template or predecessor edit, no Git command, no benchmark or application generation, no unified architecture, no winner selection, no Step 4.

## Addenda (dated; the rubric above is unchanged)

- **2026-11-06 · AD-1 (reading aid).** After B01 the dossier display was compacted (direct owners shown up to four with quotes; partial owners with SAME strength listed compactly) and B03–B30 dossiers were rebuilt. B01 checkpoints keep the hash of the original B01 dossier JSON. The rubric and the judgments are unaffected.
- **2026-11-06 · AD-2 (judgment amendments).** `JUDGMENT_AMENDMENTS.jsonl`: A0 adds root tags to B02–B05 differences; A1 adds ARC-020 D5 (pre-execution reference gate) after PROBE-HOOK-01 and changes ARC-020 to MEANINGFUL_DIVERGENCE. Both batches were re-checked (gate B PASS); all attempts are kept.
- **2026-11-06 · AD-3 (static probes, contract section 7).** PROBE-HOOK-01 (dependency and reference commands), PROBE-HOOK-02 (npm peer-dependency bypass) and PROBE-HOOK-03 (removal and bare update) run each candidate's registered PreToolUse script directly on disposable copies under `_work/` (removed afterwards). No Git, network, package restore or live host. PROBE-HOOK-02 was re-run on 2026-11-06 with two added cases (Q9, Q10: bypass flags carrying markers); `HOOK_PROBE2_RESULTS.json` holds the second run, whose Q1–Q8 decisions equal the first run's printed output.
- **2026-11-06 · AD-4 (materiality of evasion routes).** A difference reached only after the agent works around a refused command (DEP-025 D2, `.npmrc`) is scored material under the section 6 rule; the alternative reading is reported as sensitivity S-EVASION.
- **2026-11-06 · AD-5 (shared roots).** One source fact bearing on several policies keeps one root id; each policy keeps its own label, and `ROOT_CAUSE_SUMMARY.json` counts the root once (ARC-002/008/019; ARC-020/GOV-017).
- **2026-11-06 · AD-6 (extras procedure detail).** `_tools/extras.py` clusters by closest policy and token Jaccard (0.42 within a policy bucket, 0.62 across buckets) and proposes a class by rule; every cluster then has an analyst decision (`A` accept / `X` decide), and every GENUINE_EXTRA_NORM needs an `X` with a task. Because one fact is often split across clusters, six-way presence for genuine extras is set by reading in `_extras/decisions/ROOTS.py` and applied at assembly (`EXTRA_GENUINE_ROOTS.json`). Report and review-output content differences are classified GENUINE but marked as non-engineering (family RC-TXT-FINAL-REPORT-CONTENT).
- **2026-11-06 · AD-7 (bookkeeping).** `_tools/state_sync.py` refreshes STATE progress from checkpoints.
- **2026-11-07 · AD-8 (corrections).** Extras notes X0225–X0229 and X0242 overstated the scope of PV2-02 (it covers M and M1; the other four fail closed by their own design) and omitted the Q-02 blank-command edge. Corrected in XC04/XC05 and re-checked; earlier attempts are kept in `VALIDATION_ATTEMPTS/`.
