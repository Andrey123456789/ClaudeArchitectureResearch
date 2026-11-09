# Experiment 005 / Stage A / Step 2 — Pass 2+3 Integration (v3)

Experiment 005 / Phase 5.4 / Stage A / Step 2 — Codex Pass 2+3 Integration and Approved Post-v2 Parity Closure

WORKING DIRECTORY
C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4

THIS IS A NEW CONTROLLED FOLLOW-UP TASK, NOT A RESTART OF STAGE A.

OBJECTIVE
Starting from the verified step2_controlled_repair_v2 checkpoint, independently adjudicate the completed Codex macro-passes 0002 and 0003, reconcile their genuinely new source-grounded normative evidence with the existing Pass-1-augmented union, apply four explicitly user-approved parity corrections, make only other changes that follow unambiguously from already approved common policy, and perform full sequential and final regression/consistency verification. Preserve all original research inputs and architectural identities. Do not start Step 3 or practical benchmark runs.

MANDATORY PREFLIGHT — DO NOT ASSUME A PASS IS COMPLETE
1. Read the pertinent Stage A/Step 2 specification, the v2 FINAL_PARITY_AND_CONSISTENCY_REPORT.md, RESUME.md, EVIDENCE_LIMITS.md, change/checkpoint logs and v1/v2 test contracts; inspect the actual current files, not remembered summaries.
2. Inspect:
   - stage_A/codex_iterative_search/STATE.json and RESUME.md (context only; DO NOT resume or edit the Codex task);
   - stage_A/codex_iterative_search/PASSES/pass_0002/PASS_VALIDATION.json and PASS_REPORT.md;
   - stage_A/codex_iterative_search/PASSES/pass_0003/PASS_VALIDATION.json and PASS_REPORT.md;
   - their claims, comparison/evidence files, candidate checkpoints, hashes and coverage receipts;
   - stage_A/reconciled/step1_union_augmented_pass1/REVIEW_REPORT.md and AUGMENTED_UNION_VIEW.jsonl;
   - stage_A/reconciled/step2_controlled_repair_v2/ and its verified final candidate trees and classifications.
3. Require PASS_VALIDATION.status == COMPLETE for BOTH passes 0002 and 0003; require all six candidates and 448 active source files accounted for; validate reported source/baseline fingerprints, completed-unit receipts and applicable structural validation. Pass 0003 may have completed even if Codex's global STATE.json subsequently points to pass 0004: use the specific completed-pass evidence, not the global pointer. Do not read pass 0004+ evidence even if it exists.
4. If pass 0003 is not fully validated or required predecessor artifacts are absent/altered, STOP WITHOUT MODIFYING CANDIDATE OR CLASSIFICATION DATA. Write a concise English preflight-blocker report in the new v3 output directory. Do not improvise missing evidence or treat 448 file receipts alone as full semantic completion.
5. Verify predecessor integrity; take a manifest of all protected sources and v2 artifacts before work. All outputs from this task go ONLY under stage_A/reconciled/step2_controlled_repair_v3/. Never modify inputs/, original candidate trees, stage_A/primary/, replica/, independent/, step1_union/, step1_union_augmented_pass1/, step2_controlled_repair_v1/, step2_controlled_repair_v2/, or anything under stage_A/codex_iterative_search/. No mutating Git operations on the research repository. Keep all generated .md reports in English.

HISTORICAL FACTS TO VERIFY, NOT REDO
Codex Pass 0001 was independently adjudicated by Claude on 2026-11-02 in stage_A/reconciled/step1_union_augmented_pass1/. It classified 152 Pass-1 records as 26 distinct-unrepresented proposals, 29 existing-group facets, 71 non-independent details, 25 already covered, and 1 unresolved. v1 and v2 already build on this augmented union. DO NOT re-review Pass 1 as if new. Use the original three extraction runs, the Pass-1 augmented union and the final v2 classifications as baselines for *semantic* novelty comparisons, not just IDs, lexical matches, or line overlap. Do not misrepresent the 26 proposals as already approved universal policies.

PART A — INDEPENDENT ADJUDICATION OF PASSES 0002 AND 0003
1. Inventory every effective finding and unresolved hypothesis in BOTH completed passes, including revisions/supersessions. Preserve IDs, candidate, exact source path/quote/location, claimed actor/action/trigger/scope/modality/exception/lifecycle, relation to existing policy and evidence status. Build a comprehensive source-grounded crosswalk.
2. Deduplicate across Pass 2, Pass 3, Pass 1's augmented union, the three raw extraction runs, and v2. Perform *semantic* comparisons, distinguishing repeated records per candidate from distinct logical rules. Count at least: (a) original finding records; (b) unique semantic issue clusters; (c) truly new independent normative obligations; (d) new facets or corrections to existing obligations; (e) already covered; (f) non-normative examples/implementation facts; (g) unverified hypotheses and cases needing user approval. Never count multiple rephrasings as separate discoveries.
3. Inspect the actual immutable sources and effective instruction-loading/enforcement paths for each plausible new rule. Distinguish a binding obligation from advice, illustrative technique, static configuration, implementation detail, checker bug and delivery-specific behavior. Do not infer a universally shared policy merely because one candidate has additional technique guidance. Do not silently weaken valid candidate-specific rules solely for aesthetic parity.
4. For each proposed change, establish whether the issue (i) existed in frozen inputs, (ii) was absent or mislabeled in all three original extractions, (iii) was already handled by Pass 1, and (iv) still exists in v2. Provide exact evidence and reproducible counter-scenarios where possible.
5. Keep uncertain findings OPEN with explicit reason and risk. Do not upgrade a Codex hypothesis to a proven EXTRA or a proven cross-candidate difference without independent evidence. Do not invent authority to create new shared normative requirements. Where a genuine new policy choice is not already approved by the user, retain a clearly specified decision item and proceed with uncontroversial approved work; do not make that choice implicitly.
6. Reconcile the relevant claim, classification, modality, coverage, and strength records in a non-destructive overlay with stable provenance and original identity. Update shared-policy mappings only when justified. Do not rely on raw MUST_NOT counts as strictness evidence, especially with the previously flagged 86 softer-modality negative claims. Individually source-review those 86 flagged records (unless a prior independently verified disposition already exists), correct proved modality errors with per-rule gates, and retain unresolved ones with explicit evidence. Report effects on all 196 policies x 6 candidates (1,176 cells), including any non-equivalence.

PART B — FOUR EXPLICITLY APPROVED CORRECTIONS (NO FURTHER USER APPROVAL REQUIRED)
Implement as four separate logical rule changes, in a dependency-aware order. This text is the full authorization; do not require an additional handoff file.

PV2-01 — Git PreToolUse permission parity.
K0 has a hook that asks for approval for repository-mutating Git commands; M, M1, L0, L1 and K1 require equivalent effective gating within their OWN existing hook architectures. Allow ordinary read-only git status/diff/log without Git-specific permission prompts. Correctly distinguish mutations from read-only operations, including global options, command wrappers and multi-command lines; do not make a generic substring heuristic the only enforcement. For mutating commands return the host-compatible `ask` decision, unless an existing more restrictive non-Git guard must `deny`. An `ask` response is not user authorization: preserve HQ-01/GOV-015 (explicitly requested or specifically preapproved operation and scope), dirty-tree behavior, headless standing decision, scoped commits, and explicitly authorized main rewrites where not otherwise prohibited. Do not introduce unconditional commits or weaken unrelated dependency guards. Verify equivalent script-level PreToolUse decisions for six candidates with common positive, negative, combined-command and malformed fixtures, and separately distinguish untested live-host behavior.

PV2-02 — Fail-closed malformed shell PreToolUse input for M and M1.
Explicitly block malformed/empty/non-object JSON, missing, blank or non-string tool_input.command on shell-command PreToolUse events, and genuinely inconsistent event/tool payloads when applicable. Existing M hook exits 1 for certain malformed input and relies on host onFailure: block; ensure explicit script-level blocking with valid host-compatible behavior, without falsely treating untested host behavior as verified. Preserve allowed valid read-only commands and do not require tool_input.command on unrelated event types. Verify with an adversarial fixture matrix against direct execution, exit codes and decision payloads.

PV2-03 — Remove K0-only repository-root requirement for Directory.Packages.props.
Remove the universal D-17/check-dependencies.cjs mandate that Directory.Packages.props physically reside at repository root. Allow valid nested/otherwise legitimately effective central package configurations, validated using per-project effective MSBuild properties, matching the agreed CPM semantics of all six candidates. Do not relax effective CPM enforcement, valid dependency versions, floating-version approval exceptions, or unrelated guards. Test nested positive fixtures, inherited/overridden/disabled properties, multiple projects and malformed/invalid package metadata. A root-level props file may remain a non-binding typical layout example.

PV2-04 — Frontend-test placement parity for M.
Add to M's appropriate normative owner the explicit ban on placing frontend tests under backend/, equivalent in scope, authority and modality to the other five candidates. Update relevant claims/witnesses/strength records and test both acceptable and forbidden layouts, without adding extraneous layout mandates.

PART C — CONTROLLED CHANGE AND VERIFICATION PROTOCOL
- Start with an immutable snapshot/copy of v2 into v3. Maintain precise manifests and source-to-final crosswalks; keep v2 unchanged.
- First finish the Pass 2+3 independent evidence adjudication and construct a queue of proposed fixes. The four PV2 corrections are pre-approved. Other clear defects can be corrected only to implement previously approved policy semantics; record any genuinely new policy decisions for the user rather than silently choosing. Integrate source-grounded classification improvements without automatically changing candidate template text.
- For EACH individual logical rule correction: (1) declare exact files/claims/policies affected and expected behavior; (2) checkpoint; (3) make the single change; (4) test its positive, negative, boundary and interaction cases; (5) verify whole affected candidate architecture and all linked policies, and six-candidate parity for the specific agreed obligation; (6) run the FULL cumulative regression suites from v1, v2 and all earlier v3 corrections on the actual latest v3 trees; (7) commit a *data checkpoint*, not a Git commit, ONLY on a fully passing gate. A failed gate must be fixed or the current change rolled back before advancing. Keep evidence of every failed attempt and repair.
- Reuse/extend reliable existing harnesses rather than replacing them with weaker presence/regex checks. Prevent unintended field loss in classification overlays and test replay reproducibility.
- Perform a separate adversarial cold audit on FINAL six trees and FINAL overlays, including cross-rule contradictions, same-task behavioral matrices, authorization vs ask/deny differences, side-effect interactions, all 1,176 policy coverage cells and modality/strength changes. Distinguish mechanical-witness checks from manual semantic reads and from live-host/real-application checks. Never convert NOT_RUN into PASS. Do not claim full semantic equivalence merely from a clean mechanical audit.
- Do not alter candidate architecture identities, create a universal new architecture, perform full practical benchmarks, or run Stage A Step 3 in this task. Preserve original research study isolation.

CHECKPOINTS AND OUTPUTS
- Write ONLY in stage_A/reconciled/step2_controlled_repair_v3/; create RESUME.md and a machine-readable STATE/checkpoint record immediately after passing preflight. Checkpoint after every evidence-adjudication batch and every correction gate. A new session must be able to resume without repeating completed work.
- Produce English-language artifacts at minimum:
  * FINAL_PASS2_PASS3_INTEGRATION_AND_PARITY_REPORT.md — executive findings, counts, policy decisions, files and claims changed, residual risk, Step 3 recommendation;
  * PASS2_PASS3_ADJUDICATION.jsonl — one entry per effective Pass-2/Pass-3 finding with source evidence, reasoned verdict, v2 relation and provenance;
  * UNIQUE_ISSUE_CLUSTERS.jsonl — one row per semantic cluster, cross-pass duplicates and significance;
  * APPROVED_DECISION_IMPLEMENTATION_MATRIX.md — PV2-01..04 with exact checks and outcomes;
  * CHANGE_LOG.jsonl, GATE_LOG.jsonl, REGRESSION_MATRIX.md, FINAL_AUDIT_RESULTS.jsonl;
  * final candidate manifest with SHA-256, v2-to-v3 file/claim crosswalks, final classifications/overlays, and an explicit unresolved/user-decision queue;
  * EVIDENCE_LIMITS.md and RESUME.md.
- Clearly distinguish counts of Codex records, distinct logical requirements, genuinely new normative requirements, already covered items, hypothesis-only items, applied fixes and candidate files changed. Report anything left outside scope.
- Make status `GO` only if it is demonstrably justified by the evidence; otherwise `CONDITIONAL_GO` or `BLOCKED` with precise blockers. Self-audit is not independent validation by a separate model family; say so.

EXECUTION
Start now. Do not ask me to reapprove the four PV2 decisions or to supply Pass 1 again. Do not stop merely to ask whether Pass 2/3 should be processed; this instruction authorizes their evidence review. Only seek a new policy decision if it is genuinely necessary to choose between non-equivalent normative requirements. Do the work in this turn/session until completion or an actual quota interruption, saving durable checkpoints throughout. At completion report the precise output folder, the unique new issue counts versus Pass 1 and prior audits, changes actually implemented, full test outcomes and remaining NOT_RUN/unresolved evidence. Do not promise asynchronous work.
