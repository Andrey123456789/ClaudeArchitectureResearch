# Experiment 005 / Phase 5.4 / Stage A / Step 2 — controlled semantic and candidate corrections (v1)

## 0. Objective and authority

Perform the USER-APPROVED corrections and adjudications of the six frozen Claude Code instruction architectures **one logical rule at a time**. After **EACH** logical rule change, prove that every affected candidate still satisfies its complete common policy inventory, preserves its defining instruction-architecture invariants, and passes all previously introduced regression cases. **Never start the next rule until the current rule's gate passes.** Finally, perform a separate cumulative cross-rule/cross-candidate audit of the whole corrected system, including regression of early changes after the late ones.

This is a controlled *repair of derived candidate working copies and classification overlays*, not Step 3, not a benchmark, and not a request to redesign the candidates or invent a seventh architecture.

Execution workspace (Windows):
`C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4`

Read BEFORE changing anything:
1. `_STAGE_A_KIT/62_APPROVED_DECISIONS_AND_GATES_RU.md` — the user's approved decisions, scope and gates. If a Russian phrase is unclear, preserve the quoted decision and record the uncertainty; do not silently replace it with an invented standard.
2. `_STAGE_A_KIT/41_CLAUDE_STAGE_A_STEP2_CLASSIFICATION_TASK_EN.md` and `stage_A/reconciled/step2_classification/{CLASSIFICATION_PROTOCOL.md,PROTOCOL_ADDENDUM_A1.md,PROTOCOL_FREEZE.json,STEP2_CLASSIFICATION_REPORT.md}`.
3. `stage_A/reconciled/step2_semantic_audit_v1/{SEMANTIC_AUDIT_REPORT.md,HUMAN_DECISION_QUEUE.jsonl,METHODOLOGY_NOTE.md,FHD_REVIEW.jsonl,CORRECTION_PROPOSALS.jsonl,NEW_CLAUSE_PROPOSALS.jsonl,UNRESOLVED_QUEUE.jsonl,A13_RESIDUAL_LEADS.jsonl,PI012_NEGATIVE_MODALITY_REVIEW.jsonl,SWAGGER_UI_REVIEW.md,EFFECTIVE_VIEW_MANIFEST.json,VALIDATION_RESULT.json,UPSTREAM_MANIFEST.json}`. Read further evidence, including full source excerpts and decision ledger, on demand.
4. `inputs/<C>/{CANDIDATE.md,source/inventory.json,output/template/**}` for `C = M, M1, L0, L1, K0, K1`, and the original shared GOV-017/018 construction requirements. Establish relevant actual template paths from disk rather than assuming line numbers remain fixed.
5. `stage_A/reconciled/step2_classification/per_candidate/<C>/{CLASSIFICATIONS.jsonl,POLICY_COVERAGE.jsonl}` and its tools/validators, as needed.

**Precedence:** the user's approved decisions control the identified choices; preserve the existing 194 V2-origin canonical policies plus GOV-017 and GOV-018 in all other respects. The frozen classification protocol stays fixed except for the expressly approved PI-012 clarification, which must be separately versioned and traced. Candidate-specific architecture definitions are binding. Earlier audit findings are evidence leads, not unquestionable truths. If requirements cannot be reconciled without another *substantive* user choice, preserve the baseline, document exact evidence, and STOP at the gate for that change; do not force a convenient interpretation.

## 1. Immutable input fence and writable output

The following are **immutable** during this run:
- all `inputs/**`, including candidate templates, source inventories, and baseline trees;
- `stage_A/reconciled/step2_classification/**`;
- `stage_A/reconciled/step2_semantic_audit_v1/**`;
- other `stage_A/**` evidence, CodeX passes, all earlier Phase 5.3 work, and the research repository itself;
- `_STAGE_A_KIT/**` (task instructions may be read but not edited).

Write **only** under:
`stage_A/reconciled/step2_controlled_repair_v1/`

Create fresh working copies of `inputs/<C>/output/template/` under:
`stage_A/reconciled/step2_controlled_repair_v1/candidates/<C>/template/`
Retain each original candidate's separate structure and file identity. Copies must be derived byte-for-byte from the frozen inputs before the first patch; make original and new file fingerprints inspectable. Put all helper scripts, test fixtures, staging/rollback copies, reports and checkpoints inside this output root. Do not write temp files outside this fence. Exclude network, real production databases, destructive Git commands, mutations of neighboring worktrees and external services. No `git add`, `commit`, `reset`, `rebase`, `push` or force push on the *research* repository. Git examples/test cases must execute only in disposable isolated fixtures under the output root. The Git governance rule being repaired governs later candidate behavior; it does NOT authorize Git mutations in this research run.

If the output root already exists and has completed checkpoints, verify fingerprints and resume; never delete previous verified work. If it exists with unknown contents or different source hashes, STOP and report, instead of replacing it. Verify `UPSTREAM_MANIFEST.json`/`INPUT_MANIFEST_SHA256.csv` entries against original inputs and baseline first. Do not reuse a prior PASS under different bytes.

## 2. Non-negotiable ONE-RULE gate

A **logical rule** means one independent, user-approved semantic obligation (e.g. GOV-015's Git authority). A single logical rule may have several mutually dependent surfaces (rule text, workflow, private reference, hooks, checkers, tests and classification records). Repair these surfaces together as ONE atomic change. Do NOT combine separate logical rules in the same patch, even when they touch the same file. Record every changed file, before/after hash, canonical policy and candidate.

For EACH logical rule, execute steps **A–H in order**:

A. **Baseline and impact graph.** Write the target behavior/authority/trigger/scope/exceptions, original source quotes, affected candidates/files, related policy IDs (including transitive interactions), original enforcement paths, prior approved fixes and concrete regression risks. Explicitly differentiate required shared engineering semantics from deliberately different M/L/K/replaceable-capability mechanisms. Mark classification-only work as such.

B. **Pre-change controls.** Snapshot/hashes of affected current working-copy files; capture current all-candidate policy mappings, checker results and previous test gates. Add positive AND negative tests/semantic counterexamples BEFORE editing whenever feasible (expect the negative case to fail first). Keep tests hermetic.

C. **One atomic patch.** Change ONLY this logical rule's minimum necessary surfaces, within working copies and/or versioned derived protocol/overlay. Preserve exceptions and earlier behaviors unless the decision explicitly changes them. Do not invent a new hard product requirement, require a technology in the L0/L1 technology-neutral levels, or replace an architectural delivery mechanism merely to homogenize file layouts. If a normative requirement is mentioned in a knowledge skill, verify that its authoritative owner and effective loading path are valid.

D. **Local semantic proof.** Re-read the changed paragraphs together with adjacent context, compare against full canonical policy wording (not only titles), and show entailment or a distinguishing counterexample. Verify role/actor, timing, condition, modality, default/exception, approval authority, owner and reliable delivery. Confirm the fix actually changes the intended behavior/label without adding unrelated obligations.

E. **Complete affected-architecture consistency gate.** For EACH candidate touched by this rule, rebuild and verify the complete **194 V2 policies + GOV-017/018 = 196** mapping against its current modified template, including owner existence, direct and indirect evidence, trigger-class and scope preservation, normative single ownership, reference/import/skill/hook reachability, acyclic conformance dependencies, candidate-specific architecture constraints, and all covered mandatory subclauses. A mechanical inventory count alone is NOT semantic proof; perform source-grounded reviews of affected and transitive policies and independent cross-policy contradiction checks. Check all current rule owners and key exception paths, not only the changed file.

F. **Executable controls and regression.** Run existing available instruction checkers, schema/manifest/structural validators, relevant hook tests and new hermetic positive/negative fixtures. Add mutation tests (remove approval, invert exception, disable a hook, break an import, etc.) to prove the checker catches a regression. Where a claimed behavior requires a live app/Claude runtime/Swagger server or network unavailable in this run, label it `NOT_RUN` and keep the claim as a future experiment; NEVER mark it PASS. Exclude CI/CD deployment performance testing (out of study scope), but preserve any required existing policies.

G. **CUMULATIVE cross-rule regression.** Re-run every approved fix's regression suite and re-check its source-grounded semantic postcondition on the current working copies, **including earlier fixes in other candidate templates**. Recalculate relevant six-way equivalence/strictness cells and their provenance for the current policy. Check that the new rule did not invalidate any prior fix or permit/prohibit an unintended exception. If full automation cannot prove a policy, record an explicit source-grounded semantic check; do not substitute a green hash check.

H. **Gate and checkpoint.** Gate `PASS` only if D–G all pass and no policy or architectural invariant regresses. If any fail, repair only this rule's patch and repeat D–G, or roll it back. **Do not progress to the next rule on FAIL, UNVERIFIED critical condition, or unresolved required user choice.** Persist `CHANGE_LOG.jsonl`, `GATE_LOG.jsonl` (commands, test result, exact source hashes, changed policies, prior-fix regression status), and a restartable checkpoint. Record `NOT_RUN` without treating it as PASS; assess whether it blocks approval, depending on what is claimed. Output a clear blocker instead of making unsupported success claims.

For **classification-only record corrections**, perform equally atomic before/after with provenance, verify semantics and the **entire current derived dataset's** ID/reference/coverage invariants plus cumulative regressions after each accepted record. A faster machine-checkable whole-dataset pass is allowed; the rule-by-rule requirement is not permission to batch 103 corrections blindly. Group only inseparable facets of the *same* logical claim and document why.

## 3. Ordered repair/adjudication queue

Build `DECISION_IMPLEMENTATION_MATRIX.md` **before edits**, mapping every approved item below to input evidence, candidate(s), exact impact, modification type (`TEMPLATE_RULE`, `ENFORCEMENT`, `CLASSIFICATION_ONLY`, `PROTOCOL`, `NO_CHANGE_VERIFIED`, `DEFERRED`), dependencies, tests and expected gate. Order dependent items appropriately; any discovered interaction between two queue items must be added to the impact graph. Do not silently skip an item. This queue is authoritative together with the approved register; reorder only with written reasons.

### 3.1 PI-012 methodology — HQ-06 (FIRST)

Version an approved PI-012 clarification as a derived, explicitly labeled protocol addendum; never edit the original frozen protocol. Separate (i) semantic constraint and logical condition, (ii) normative authority/source role, and (iii) modality (`MUST_NOT`, `DEFAULT`, `SHOULD_NOT`, `NONE`, etc.). A bare negation is not necessarily a prohibition. Equivalent `only when`/`do not unless` language under equivalent authority and scope must not yield different modality merely from wording. Do not promote private skill technique to an authoritative policy without owner evidence. Run all **79** earlier flat-negative cases and **all 230** residual suspicious cases individually with actual sources, not by a bulk keyword relabel; deduplicate overlaps by original stable key. For each: text and context, canonical source, independent reading, alternative, result `UPHOLD`/`CORRECT`/`UNRESOLVED`, confidence, evidence and counterexample where it matters. Check for similar systematic untested cases and report bounds, not a fake census. Re-run cumulative data-validation gates for every approved semantic correction. Track sensitivity of strictness comparisons to unresolved decisions. Preserve indeterminate cases as such.

### 3.2 Human decisions HQ-01 through HQ-05 (separate atomic gates)

- **HQ-01 / GOV-015 / protected branches:** Git-changing operations require a specific user authorization or a clearly bounded pre-approved operation/scope; generic `approved workflow` is not blanket authority. At the start of a task, if *pre-existing* uncommitted changes are present, present only the user's two agreed options: (a) commit the identified changes with an authorized scope or (b) suspend the entire task for manual cleanup; in noninteractive/headless mode without an already adequate choice, pause safely. Do not mistake changes made by Claude during the task for this startup condition. Before dangerous Git actions, re-check authority and preservation of foreign changes. An explicit request to rewrite `main` is permitted unless another policy forbids it; do not design enterprise-style branch protection or Git administration. Test staged/unstaged/untracked/foreign changes, clean tree, unsafe reset/force push, and explicit-vs-vague main authorization. Make no actual dangerous Git changes to research inputs.
- **HQ-02 / RUN-021:** Cache invalidation/refresh must be coherent with the successful canonical data mutation. Choice of strategy depends on transaction isolation level, concurrent read/refill behavior, commit/rollback ordering, app/cache consistency guarantees, crash between commit and invalidation, retries and documented tolerated staleness. Pre-mutation invalidation is not categorically prohibited if correctness for the chosen semantics is established. Do not assert `commit -> evict` alone is fully atomic across DB and cache. Test semantic timelines/counterexamples; do not require Redis/server execution where not present.
- **HQ-03 / DEP-003:** Floating/pre-release versions are forbidden by default; an explicit, bounded user request may authorize the canonical exception. All candidate instruction texts and relevant validators/hooks must honor the same exception without disabling checks globally. Confirm package compatibility and selected exact install outcome where relevant. Test allowed approved/denied unapproved cases and scope leakage; do not claim actual network registry verification if offline.
- **HQ-04 / GOV-017:** Headless may implement a **specific, previously explicitly approved** Reserved architecture change, but cannot invent/approve a new Reserved decision. Vague authorization is insufficient. Record approval evidence, scope, output decision log and stop behavior on unexpected reserved choices. Do not add arbitrary autonomous approvals.
- **HQ-05 / DEP-025:** An ordinary `ask` confirmation or shell-comment marker (e.g. `peer-override-approved`) must not independently override peer compatibility policy or permit `npm --force` / `--legacy-peer-deps` to merely evade an unresolved incompatibility. Resolve the actual conflict. A separately explicitly changed research policy, if ever authorized, is distinct and not part of this run. Test command-string trickery, shell markers, nested calls, and hook enforcement; preserve legitimate safe installations.

For each HQ independently re-check linked `GOV`, `DEP`, `RUN`, `SEC`, `WF` policies as applicable, not only the nominal ID, and update related classification records only after the corresponding candidate change passes its gate.

### 3.3 Other approved substantive changes (one logical rule per gate)

- **8.1 Swagger UI:** For an applicable Development API behavior change, require opening Development Swagger UI and confirming it loads. Implement equivalent *obligation and condition* across all six while preserving each architecture's native workflow/skill routing. Do not force UI startup when app/runtime isn't available; such runtime verification is NOT_RUN, not PASS. Check `WF-005`, `WF-006`, `API-016`, `TST-010`, affected source claims and trigger wording.
- **8.2 K0 CPM:** Make the checker honor *effective* `ManagePackageVersionsCentrally` setting, including valid inherited MSBuild configuration, not only a literal declaration inside `Directory.Packages.props`. Retain central version-policy enforcement and avoid accepting a disabled/overridden effective value. Test property in each permitted location, disabled and conflicting values; if proving effective MSBuild evaluation requires SDK/runtime unavailable, document limitation and do not claim full effective-state proof.
- **8.3 K1 performance:** Align compiled-query optimization with `RUN-008`: justified by measurement **or** clearly demonstrated need, with no unjustified speculative optimization. Preserve associated performance policies.
- **8.4 L0 Production migrations:** Align with `WF-019`: no automatic Production migrations at normal app startup by default; separately approved controlled deployment-time migration steps remain possible. Preserve security/credential and no-Development-seeding guarantees.
- **8.7 CUSTOM_SETTINGS:** Align the obligation in L0/K0/K1 to read `CUSTOM_SETTINGS.md` when planning a new application or substantial feature, consistent with M/M1/L1, while honoring no-extra-normative-owner, legitimate absence/empty-file behavior and architecture-specific loading budgets. Check `GOV-007`, `GOV-010`, `GOV-011`, `GOV-021` and related workflow scope.
- **8.7 K1 local migrations:** Remove only a truly additional, unnecessary *mandatory local DB mutation* when it is not implied by canonical policy. Preserve schema migration generation/review, schema-before-seed and validation obligations (`PST-005/006/009/010`). If removal would lose a canonical duty, retain that duty and document why.
- **8.7 test priorities and C# language-version:** Compare actual source obligations across all six and the canonical baseline. Fix classification metadata first; modify templates only for **demonstrated** missing or stronger/weaker required obligations. Preserve intentionally different wording/placement.

### 3.4 Source-verified NO-CHANGE or classification-only resolutions

These items MUST be explicitly examined, supported by source and given a gate, even when no template edits are warranted:
- **8.5 HTTP timeout:** All six already distinguish client cancellation, local timeout and upstream timeout; do not erase L1 details. Check exact normative modality and separate genuine extras from false label drift. Keep 502/504 mapping distinctions source-grounded; classify rather than reflexively align Markdown.
- **8.6 L1 liveness:** L1 normative principle is aligned; more categorical `health-check` technique/reference should be evaluated under PI-012, not automatically rewritten. Check `API-019` and related path/skill authority.
- **8.7 security scan minimality:** The minimum-sufficient-fix / anti-overengineering principle exists in all six; correct any label drift, no blanket new policy.
- **8.7 fast/slow external tests:** Already present in all six; maintain correct classification, no L1 deletion.
- **8.7 CI dependency auto-updates:** Rule occurs in L0/L1/K0/K1; preserve and label out-of-practical-evaluation scope. No CI/CD trial or blanket deletion of existing four rules.
- **9.2 K0 unsafe deserialization:** Treat the ambiguous text as a security-audit criterion unless a distinct authoritative product prohibition is proven. Do not silently invent a `SEC-003` obligation; document any remaining uncertainty.
- **10 Four new clause proposals:** Source-verify all four `NEW_CLAUSE_PROPOSALS.jsonl` and add as separate, traceable *candidate-specific extra classification proposals* (M and M1 output-cache metadata, M1 Arrange/Act/Assert default, L0 security scan checks). Do **not** promote them automatically to the 194 shared canonical policies or distribute them across all architectures.
- **11.1 trigger/delivery:** Distinguish when a rule is *applicable* from how it is *delivered*. `trigger` contains loading context for many of 4,617 entries; create derived `applicability_trigger` and `delivery_context` where evidence supports, with explicit unknowns. Avoid silently declaring all 4,617 individually verified. Preserve original field for provenance; do not confuse workflow/scope with modality.
- **11.2 mixed evidence and cross-method adjudication:** For relevant `MIXED`, partial witnesses, five strength cells, three qualified overrides and source-policy conflicts, combine semantic entailment, a falsifying counterexample and executable behavior where applicable. Record competing interpretations rather than voting by model count. Never infer completeness from a coverage row alone.
- **11.3 evidence limits:** Document same-family-model reviewer bias, targeted sampling limitations, runtime NOT_RUN and lack of unbiased error-rate evidence.

### 3.5 Remaining audit correction proposals

Individually adjudicate **all 103 `CORRECTION_PROPOSALS.jsonl` entries** against the ORIGINAL quoted sources and the MODIFIED working copies. Do not blindly apply the old overlay: after a template is edited, the old quote/line and semantic class may no longer exist. For every proposed correction, either (a) accept it with valid current-source evidence and correct fields, (b) reject it with an explicit counterexample, or (c) keep unresolved with exact reason. Respect 43 frozen-protocol-supported, 51 PI-012-dependent and 9 partial-field groups, but verify these designations instead of assuming they remain valid. Preserve the original record key and original snapshot separately from a mapped post-edit claim; explicitly mark moved/removed/reworded source claims. Check the 31 open records and related policy choices against the user's decisions. Never silently turn an unresolved claim into a definitive strictness fact.

## 4. Dataset and provenance after template edits

**Critical:** Original Step 2 classifications are indexed to ORIGINAL frozen templates. Edits to candidate working copies invalidate exact original line anchors and can change semantic claims. Do not simply replay a 103-row overlay onto edited templates and call it an audited classification. Preserve two explicitly distinct views:

1. `FROZEN_BASELINE_REFERENCE`: original 6,402 classification identities and 1,176 policy rows, with original hashes and original source anchors untouched;
2. `REPAIRED_CANDIDATE_DERIVED_VIEW`: rechecked mapping from old original claim IDs to corrected candidate source evidence, one-to-one where justified; mark `REWORDED`, `REMOVED`, `MOVED`, `SPLIT`, or `ADDED` and issue new stable IDs for genuinely new independent claims. Report resulting counts honestly. Keep an explicit crosswalk; do not assert exact 6,402 after added/removed claims unless true and independently validated.

Preserve six-way traceability to the original 194 V2 + two shared research requirements. Every coverage cell must identify valid current working-copy witnesses with appropriate provenance; distinguish technical reachability from semantic requirement equivalence. Recompute and verify affected coverage and strictness descriptors; do not assume 1,176 rows retain the same STATUS after substantive candidate edits. Do not overwrite original classification, original Step 2 protocol or audit. Store PI-012 methodology and candidate deviations in versioned derived addenda/overlays under this run root. No Step 3 rankings, performance evaluation or implementation benchmark.

## 5. Cross-candidate parity and architecture identity invariants

For all six, retain common engineering obligation parity unless the user expressly approved a change, and preserve architecture delivery differences as experimental independent variables:
- M: flat, minimally reorganized V2-lineage rules, no Levels/Kinds/slots;
- M1: M-style organization with its specified replaceable capability boundaries;
- L0: stability-level organization, strict L0/L1 implementation-technology neutrality;
- L1: stability organization with approved replaceable capabilities and the same neutrality rule;
- K0: Kinds x Scopes, without replaceable-capability slots;
- K1: Kinds x Scopes plus approved replaceable capability boundaries.

Preserve reliable loading, owner/trigger/scope rules, designated technology decisions, approval gates, syntax, checker semantics and all unrelated original duties. Do not equalize architecture-specific file trees, force identical hooks or expand CI scope to make counts match. Do not allow improvement of one candidate to silently weaken the others or introduce extra stricter policy in only one candidate. Where requirements really differ, document a source-grounded approved exception rather than hiding it.

## 6. Final independent-style cumulative audit (MANDATORY)

**Only after all per-rule gates passed:** perform a distinct cold re-read / adversarial audit from the FINAL six working-copy trees, not a summary of accumulated PASS markers. Rebuild the impact/dependency graph and compare:

- all 196 common policies per candidate (196 x 6 = 1,176 complete policy/witness cells), including every condition, exception and normative owner;
- every post-edit policy, hook, checker, import, skill, loader, workflow and candidate-invariant;
- ALL prior rule-specific regression fixtures re-run on final bytes, including tests of rule A after rule B changed a shared file;
- all 79 PI-012 category-N cases, all 230 residual suspicious cases and unresolved cases;
- all 103 original correction proposals with source-valid post-edit resolutions;
- four new extra clauses, all qualified-coverage/strength/mixed cases and the 31 originally unresolved records;
- cross-candidate comparisons on the *same hypothetic task*, and the separation of mandatory content from loading/reachability architecture;
- original immutable input hashes, working-copy provenance and absence of writes outside allowed output root;
- accurate counts, unique identities, line/quote source resolution and overlay deterministic replay.

Explicitly attempt to falsify earlier successful gates with interactions: Git authorization vs headless approvals, floating versions vs dependency checks, peer bypass vs approval mechanism, cache semantics vs transaction and logging workflows, migration policy vs seeding/CI scope, Swagger UI vs noninteractive verification, and PI-012 modality vs classification strength. If a later edit broke an earlier rule, reopen the earliest failing rule, repair/rollback atomically, re-run its affected gate and **all** subsequent cumulative gates, then repeat the final audit. Do not report success if any earlier fix regressed.

This is a **self-audit** performed during the same run, not an independent external evaluation; state the limitation and suggest a separate fresh-session reviewer if desired. A positive result may be `PASS_WITH_DOCUMENTED_NOT_RUN`, not a falsely unconditional assurance. If a required validation can't run, report exact missing tooling or evidence and its impact.

## 7. Output contract and checkpoints

All artifacts live under `stage_A/reconciled/step2_controlled_repair_v1/`:

- `STATUS.json` (phase, rule index, source hashes, `PASS/BLOCKED/FAIL`, exact resume point) and `CHECKPOINTS/` (one machine-readable checkpoint per passed logical rule);
- `BASELINE_MANIFEST.json` and `WORKING_COPY_MANIFEST.json` (original/derived relative file hashes, candidate, origin);
- `DECISION_IMPLEMENTATION_MATRIX.md` (every user request; expected behavior, applicable source, candidates, type, priority, gate, status);
- `CHANGE_LOG.jsonl` (atomic rule ID, touched files + before/after hashes, reason, affected policies, whether candidate text or classification only);
- `GATE_LOG.jsonl` (one full gate per rule, list of 196 per-candidate policy checks, regressions of all earlier fixes, commands/results, blocked tests and retest history);
- `POLICY_DEPENDENCY_GRAPH.json` (source-proven owners/related policies/consumers), plus `POLICY_CHECKS/` and `TEST_RESULTS/`;
- `PROTOCOL_PI012_APPROVED_ADDENDUM.md`, `PI012_79_REVIEW.jsonl`, `PI012_230_REVIEW.jsonl`, `PI012_SENSITIVITY.md`;
- `CORRECTION_103_ADJUDICATION.jsonl`, `NEW_CLAUSES_4_ADJUDICATION.jsonl`, `UNRESOLVED_DECISIONS.jsonl`, `ORIGINAL_TO_REPAIRED_CLAIMS.jsonl`;
- `REPAIRED_CLASSIFICATIONS.jsonl`, `REPAIRED_POLICY_COVERAGE.jsonl`, `REPAIRED_VIEW_MANIFEST.json` (transparent counts + proper provenance; no counterfeit old IDs);
- `_tools/` for hermetic, repeatable validators and fixtures;
- `FINAL_CONSISTENCY_REPORT.md` (per-rule table, six-way outcomes, all 196-policy and previous-fix cumulative checks, truly new or remaining contradictions, actual executables run, NOT_RUN list, evidence limits, PASS/CONDITIONAL_PASS/BLOCKED and explicit Step 3 readiness recommendation).

Keep reports append-only/traceable where practical. Use atomic writes/rename and checkpoints so a quota reset or interruption cannot silently erase the last PASS. Resume only after verifying hashes and gates for saved steps. Never rely on automatic quota resume; leave a standalone resume instruction inside this output root that points to the exact next rule.

**Finish criteria:** every agreed question has a documented disposition, every actual modified logical rule has an evidence-backed PASS gate, no later change breaks earlier fixes, final 1,176 cross-candidate policy checks are accounted for, overlays are replayable, original inputs unchanged, no Step 3 run, and there is a candid final report identifying every test that was not executable. If any of these fail, finish as `BLOCKED`, not as successful.
