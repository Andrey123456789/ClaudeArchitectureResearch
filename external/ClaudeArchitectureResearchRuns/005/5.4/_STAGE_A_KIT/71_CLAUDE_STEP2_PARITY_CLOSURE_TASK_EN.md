# Experiment 005 / Phase 5.4 / Stage A / Step 2
# Residual-parity closure after controlled repair v1 — execution contract

## 0. Mission and approved authority

Continue from the COMPLETED result `stage_A/reconciled/step2_controlled_repair_v1/` (27 prior rule checkpoints). This is a targeted corrective follow-up, NOT a wholesale rerun of the original 27 steps and NOT Step 3. The user has reviewed the independent analysis of v1 and explicitly APPROVED the remaining CPM change: **all six candidate checkers shall verify the actual effective `ManagePackageVersionsCentrally` semantics, rather than making K0's better implementation worse.** The remaining changes listed below are also authorized by the user's earlier decisions, as clarified in the handoff. There is no outstanding user choice to solicit before beginning.

Primary objective: eliminate residual unapproved *engineering-obligation* disparities and known classification ambiguities while preserving the six distinct instruction/delivery architectures and the entire authoritative policy contract (194 V2-derived policies + GOV-017/018 = 196 policies per candidate). Correct behavior beats literal string uniformity. If evidence proves a proposed edit unnecessary, document `NO_CHANGE_VERIFIED` with supporting sources and tests rather than modifying text.

Keep output **audit-ready and falsifiable**. A green syntactic checker alone does NOT establish semantic parity. The last v1 audit reported 1,102 passed, 0 failed, 14 NOT_RUN, 38 qualified policy witnesses, 62 `review_needed` records, and several stale claims found after green gates. These are explicit threats to address, not evidence of already proven correctness.

## 1. Authoritative inputs and immutability

Working directory: `C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4`.

Read and cross-check:

1. `stage_A/reconciled/step2_controlled_repair_v1/FINAL_CONSISTENCY_REPORT.md` sections 2, 3, 4, 5, **6, 7, 8**;
2. `.../DECISION_IMPLEMENTATION_MATRIX.md`, `STATUS.json`, `RESUME.md`, all prior `CHECKPOINTS/` and `GATE_LOG.jsonl`, `CHANGE_LOG.jsonl`, working-copy hash manifests;
3. `.../candidates/{M,M1,L0,L1,K0,K1}/template/` — **the v1 repaired candidate baseline**, NOT `inputs/<C>/output/template/`;
4. `.../REPAIRED_CLASSIFICATIONS.jsonl`, `REPAIRED_POLICY_COVERAGE.jsonl`, `ORIGINAL_TO_REPAIRED_CLAIMS.jsonl`, `REPAIRED_VIEW_MANIFEST.json`, `PROTOCOL_PI012_APPROVED_ADDENDUM.md`, `PI012_EXTENSION_REVIEW.jsonl`, `UNRESOLVED_DECISIONS.jsonl`, `CROSS_METHOD_ADJUDICATION.jsonl`, `SAME_TASK_MATRIX.json`, `POLICY_DEPENDENCY_GRAPH.json`, `EVIDENCE_LIMITS.md`;
5. `stage_A/reconciled/step2_semantic_audit_v1/` and `stage_A/reconciled/step2_classification/` for original reviewer evidence and Step 2 protocol, as needed;
6. `inputs/INPUT_MANIFEST_SHA256.csv`, relevant authoritative `inputs/*/source/inventory.json`, `inputs/*/baseline/TASK.md`, candidate definitions (to confirm architecture identities and 196 policy obligations);
7. `_STAGE_A_KIT/62_APPROVED_DECISIONS_AND_GATES_EN.md` (detailed approved decisions and per-rule verification matrix) and `_STAGE_A_KIT/72_APPROVAL_AND_HANDOFF_EN.md` (latest English handoff; its latest CPM authorization takes precedence); original `61_CLAUDE_STEP2_CONTROLLED_CORRECTIONS_TASK_EN.md` for predecessor methodology. Do not rely on earlier translations or obsolete decision files.

At startup calculate and save complete hash/path manifests for the six v1 candidate trees and all authoritative inputs. Verify v1 final state and replayability BEFORE using it as a baseline; distinguish a pre-existing v1 problem from a regression introduced by v2. Never alter any v1 file or prior audit result. **Do not read, hash, list recursively, modify, or depend on `stage_A/codex_iterative_search*` or sibling Codex artifacts** (another agent may be working). No network, external repository, installation, or temp files outside the output root. No mutating Git commands on the research repository; Git only in disposable fixture repositories created inside the v2 output root.

**New output root:** `stage_A/reconciled/step2_controlled_repair_v2/`. Preserve v1 in place. Populate v2 `candidates/<C>/template/` from the verified v1 candidate trees. Copy/derive the v1 *derived data* and source-crosswalk as needed to produce a standalone, replayable final v2 view without modifying the predecessor. Keep an explicit v1→v2 manifest; avoid unnecessary copies of raw logs and large historical artifacts if stable immutable source references plus hashes suffice. Never reference frozen-input line numbers as if they were current v2 lines.

If the root already exists and contains work, validate its checkpoint and hashes before resuming. Do not overwrite unverified or unrelated work.

## 2. Nonnegotiable one-change gate

The user requires **after EVERY single logical rule change**, not just once at the end:

A. Declare its ID, precise normative contract, affected candidates, authoritative policy IDs, likely competing/adjacent rules, owners, workflows, checkers/hooks, and expected negative cases. Record before-hashes and source anchors.

B. Add/refine executable checks and semantic falsification examples **before editing**; demonstrate that at least one relevant negative/mutation fixture detects the old defect when executable. An exception/no-change finding needs its own evidence rather than a patch.

C. Apply exactly ONE logical rule correction as an atomic change. It can span the candidate-specific Markdown and the enforcement logic that IMPLEMENT THE SAME OBLIGATION; do not bundle unrelated rules. A data-only semantic claim correction also counts as a separate atomic change with an individual gate and audit trail when it changes a substantive classification.

D. Validate the **ENTIRE affected candidate architecture(s)** against all 196 shared policies, including scope, triggers, conditional exceptions, authoritative owners, cross-references, paths, technology neutrality at L0/L1, candidate architecture identity, and absence of duplicate normative owners. Validate real behavior of any changed checker/hook; don't settle for searching an expected sentence. Recheck every related inventory policy and any identified conflicts.

E. Re-evaluate all six candidates against the common contract and same-task counterexamples for the changed topic; preserve intentional differences in delivery/routing/replaceability. A change in only one candidate may be legitimate ONLY if parity with the remaining five is demonstrable.

F. Run **ALL cumulative regression suites from the predecessor v1**, adapted carefully for new v2 paths, plus ALL previously passed v2 change suites. If the predecessor suite assumes old literal syntax, inspect why and update the test ONLY if it is legitimately too restrictive, adding a negative/mutation test proving the new intended rule. Don't weaken a test to pass a broken implementation. Recheck previously corrected logical rules A after changing subsequent B, even if tests share files. Run structural checker, Node syntax checks, source-anchor checks, classification/coverage replay, unchanged-baseline fences, and hash/path controls.

G. Record individual `PASS`, `PASS_WITH_DOCUMENTED_NOT_RUN`, `FAIL`, or `BLOCKED`, executed commands, counts, evidence and missing live tests; checkpoint ONLY after passing all applicable gates. If ANY gate fails, stop advancement, repair only that change and rerun the full gate, or roll it back; no silent bypass. No cosmetic changes after a gate without rerunning it.

H. In the event of interruption/quota reset, write precise standalone status and resume instruction. Continuing must verify hashes and retest the last checkpoint; do not rely on automatic resume or a previous chat's assertions.

Re-run all prior v2 gates on final bytes in a **separate cold adversarial audit**, not only a sum of earlier pass flags. Do independent source-to-policy entailment/counterexample analysis on any changed or previously qualified cell. Treat mechanical witnesses as *traceability*, not full semantic equivalence. If any regression appears, reopen the earliest affected rule and repeat forward checks before finalizing.

## 3. Approved targeted corrections (do them one logical rule at a time)

### C01 — CPM effective-state check: ALL SIX candidates (user explicitly approved)

The predecessor changed K0 only (`R08`), leaving M, M1, L0, L1 and K1 with literal XML tests. The user explicitly authorizes aligning **all six** to effective MSBuild state; **do not revert K0 to literal-only checks**.

For each candidate, inspect its own manifest/dependency checker and policy `DEP-006`, not just a hardcoded file name. Use the evaluated `ManagePackageVersionsCentrally` value **in the relevant MSBuild project context**; account for legitimate inherited configuration, imports, property evaluation order, explicit project-level override, conditional/per-project state and disabled/missing conditions. Define/check what CPM compliance means for the actual scoped projects: presence and evaluation of the central version configuration, package version declarations, and appropriate enforcement; merely seeing the token `true` anywhere in XML is NOT proof. Do not inadvertently accept noncompliant manifests or block compliant central declarations. Keep the engine cross-platform where the candidate's original checker was cross-platform; use a semantically sound, simple implementation and document available MSBuild prerequisites/fallbacks. Do not use a permissive fallback that returns PASS when evaluation is unavailable: emit an honest NOT_RUN or a BLOCKED decision for the required proof.

Tests must include at least: inherited `true` from a legitimate parent; false at parent/project; project override from true to false; conditionally evaluated true/false; conflicting imports/evaluation order; central declaration with a versionless PackageReference; a version incorrectly pinned in a project; missing or malformed central manifest; multiple projects that evaluate differently; and a literal appearance of `true` that is actually ineffective. Use disposable offline .NET/MSBuild fixtures to validate evaluated states where tooling exists, not just mock parsers; do NOT require an online NuGet restore to show effective-property behavior. Compare identical fixtures against all six final checkers. Keep candidate-native file/routing design.

Check closely for interactions with `DEP-003` floating-version exceptions, `DEP-006` CPM, `DEP-004` due diligence, `DEP-025` npm peer bypass and any hooks that call package/manifests checks. Do not unintentionally turn CPM effective property into a hard requirement to run `dotnet` on every unrelated file edit.

### C02 — Compiled-query optimization parity: ALL SIX

Previous `R09` aligned K1 only. Other candidates still contain technique-level 'measured hot path' lines that MAY contradict the shared `RUN-008` rule. For each candidate locate the governing rule AND relevant EF Core knowledge/ref text. Determine source authority and actual semantic effect before changing.

Common obligation: no speculative compiled queries or comparable optimization; justification must be **measured OR convincingly demonstrated by evidence**, as established by `RUN-008`. Measurement/profiling may be recommended or strongly preferred, but do not silently make it the ONLY allowable justification if the canonical rule admits other concrete evidence. Do not weaken architectural boundaries, performance scrutiny, or prohibit sensible profiling. No automatic blanket rewriting: if a 'measured hot path' line is a conditional example or an applicable stronger decision with documented authority, state this and assess parity. Where inconsistent, repair the minimal text in the native owner/knowledge role, not by creating a duplicate owner. Cross-check all six in the same hypothetical task.

### C03 — Production migration defaults and approved exceptions: ALL SIX

Previous `R10` adjusted L0 only; `R10-SCAFFOLD-WORDING` remains in M, M1, L1, K1, especially L1's unqualified `Never` and broader scaffolding prohibitions.

Preserve `WF-019`: **no automatic Production DB migrations during ordinary application startup BY DEFAULT**. Production migration is normally an explicit, controlled deployment operation with approved credentials, visible failure, and never Development seeding in Production. A precise user-approved exception, where compatible with other policies, must not be accidentally prohibited by one candidate's absolute wording. Do NOT infer that generic workflow approval automatically authorizes production startup migrations. Explicit exceptions require recorded scope. Also preserve test/dev migration and seeding rules `PST-005/006/009/010`, authorization and secrets (`SEC-*`), delivery workflows. Distinguish startup migrations from a controlled CI/CD deployment-time step; do not expand CI scope or implement CI. Fix exact contradicting lines in all relevant candidates and independently test default, exception, migration-time, seed, and no-credentials cases. Keep each architecture's own loading and owner conventions.

### C04 — Git authorization vs unconditional workflow imperatives: ALL SIX

Previous `R02` established precise Git authorizations, dirty-tree behavior and protected-branch override, but five remaining 'Commit package.json and package-lock.json' imperatives were recorded in M, M1, K0, K1. Find them on CURRENT v2 bytes, plus search all six for synonymous unconditional repository-mutating commands (not DB commits). Make imperatives conditional: e.g. 'When an authorized commit is part of this task, include package.json and package-lock.json together'; otherwise update both files coherently **without creating a Git commit**. Do not alter package-lock consistency or dependency-review obligations.

Respect the user's rules: when pre-existing uncommitted changes affect a mutating task, offer only (a) a scoped, explicitly authorized commit, or (b) suspend for manual user completion; in headless with no valid standing choice pause without mutation. Explicitly requested rewrite of `main` is permitted only if no other policy prohibits; generic 'approved workflow' is not sufficient. Do not require dirty-tree questions for strictly read-only tasks; before dangerous operations, detect third-party changes and recheck authorization. Git is an ancillary workflow for this C# instruction architecture experiment: do NOT grow a company-scale Git permissions framework. An existing K0 hook may remain different from other delivery mechanisms if the actual common obligation is the same. Test with fixtures and cross-check `GOV-015/GOV-017`, package management, headless, hook routing, and original R02-R06 regression suites.

### C05 — PI-012 remaining cases and semantic/classification risks

v1 records 79 cases (55 corrected, 22 upheld, 2 unresolved) and 230 cases (105 corrected, 123 upheld, 2 unresolved); the four unresolved *rows* concern **two unique K0 security-scan/deserialization source claims** that appear in both queues. The user already decided: treat deserialization statements in their source context as **security-audit criteria**, not automatically a new hard product prohibition without authoritative policy ownership. Resolve classifications only if original/current source context supports that interpretation; otherwise preserve `UNCERTAIN` with clear evidence and do not convert to a MUST_NOT strength fact.

v1 final report identifies **21 additional 'do not X when Y' candidates** not individually examined. Individually inspect all 21 and any deduplicated overlaps, record source quote, location, owner, applicability condition, equivalent affirmative/rephrased rule, actual modality, and keep/change decision. Distinguish descriptive text, no-obligation text ('not required'), preference, default, conditional hard constraint, and true ban. Equivalent `only when` / `do not unless` under the same normative authority and scope must not differ merely due to surface form. Apply accepted PI-012 addendum; do not silently impose alternative 'D' uniformly. Keep sensitivity analysis for materially ambiguous cases.

Any change of a classification claim is its own tracked atomic disposition and must pass classification-level integrity, source/anchor resolution, all 196 x 6 policy checks, existing corrections (especially 103 and 31 originals), and previous-fix regressions BEFORE the next substantive change. Do not mechanically close all open items merely to make counts zero. For source facts not directly accessible, document NOT_VERIFIED/UNCERTAIN accurately.

### C06 — Six reviewer readings and stale derived-data risks

Independently adjudicate the six explicit reviewer readings from v1 report §6:

1. `R02-TASK-SCOPE`: pre-existing dirty-tree check applies to mutating tasks, not read-only reviews, without hidden expansion;
2. `R02-HEADLESS-DIRTY`: approved Reserved headless action does not bypass the dirty-tree pause; Step 3 will need a clean initial tree or an explicit standing authorization;
3. `R04-RECORD-FORGERY`: an agent-writable marker is NOT strong proof of user consent; assess actual claimed assurance and avoid adding an overengineered security infrastructure. Do not pass a fake proof-of-origin test;
4. `R01-COMMON-VALUE`: unmarked `only when` in knowledge text; show both modality interpretations and their consequences; keep the chosen approved PI-012 interpretation unless source evidence contradicts it;
5. `R01-TRIGGERED-CLASS`: individually verify 21 'do not X when Y' leads as required above;
6. `R22-UNDER-EXTRACTION`: original trigger may include a parenthetical scope not extracted into derived `applicability_trigger`; inspect the extractor, fix lost applicable condition only where evidence supports it, and preserve source provenance.

Further focused data assurance: v1 contains 62 `review_needed` claims, 38 coverage cells backed by override/partial witness rather than FULL direct evidence, and 42 newly generated claims (plus four proposals). Individually inspect these bounded sets on current v2 source; separate true semantic gaps from missing evidence and classification artifacts. For each, record `CONFIRMED`, `CORRECTED`, `QUALIFIED`, `UNRESOLVED`, or `NOT_VERIFIED` and why. Do not falsely declare the remaining ~6,400 claims fully read. A targeted stratified blind reread of additional unaffected claims from all six candidates is recommended for falsification; label sample design and do not claim an unbiased global error rate unless properly randomly sampled. Avoid repeated review of the exact same sample as evidence of independence.

The `trigger` field in the v1 data was often loading context, not applicability. Preserve originals and separate `applicability_trigger` from `delivery_context` under provenance. If a derived field cannot be inferred, say unknown; don't fabricate precision.

### C07 — Close parity and data integrity, without expanding scope

Reconcile previously flagged extras (`R13-TEST-PRIORITY`, `R19-CI-RULE-SPREAD`, `R20-DESER-FORMS`) with the above fixes. Keep CI/CD OUT of practical benchmarks, retain existing general policy unless source-grounded user authorization justifies a specific change, preserve all four candidate-specific *proposals* without turning them into canonical shared policies. No unnecessary generalization of local database migration duties. No strictness totals that mix old frozen and new v2 line anchors, or treat `MIXED` and partial witnesses as full equality. Recalculate derived dataset counts rather than assuming v1 6,448 is unchanged. Reassess all prior 103 corrections and 31 initial open records only when affected by actual current text/context; still run global integrity checks on every item.

## 4. Additional assurance gates and proof requirements

For each rule and final cold audit, include:

- Policy parity matrix: **196 x 6 = 1,176** coverage cells, *current* path+line+quote witness, conditions and normative strength. Every changed/qualified/affected cell gets source-level semantic entailment and a falsifying counterexample; a mechanically resolved path is not a proof of full parity.
- Cross-architecture same-task examples, demonstrating the actual consequence of every material rule difference (or recording `NOT_TESTED`). No homogenization of M vs L vs K instruction structures or optional capability delivery.
- Executed tests of changed scripts/hooks, including negative mutation tests; replay of all previously successful rule-specific suites; all changed scripts parse with installed runtime, and changed checker behavior is confirmed in disposable fixtures.
- Full-system static checks of normative ownership, trigger/scope coverage, internal references, L0/L1 technology neutrality, and protected candidate-specific invariants.
- Interaction matrix that explicitly exercises C01 vs DEP-003 floating exception and package checker, C03 vs deployment/headless/approval and secrets, C04 vs dirty-tree and dependencies, C05 vs actual policy `strength` metrics. Re-test A after B, not only B.
- Fences: v1 and frozen original files remain unchanged (paths & hashes); Codex work not read or written; provenance and record identity deterministic replay.
- Truthful status: `PASS`, `PASS_WITH_DOCUMENTED_NOT_RUN`, `BLOCKED`; do not count live agent/headless host, real DB/cache, API+Swagger UI, registry or CI as passed unless actually executed. If runtime needed for a factual conclusion and unavailable, record its limitation, not an assurance.

An optional separate verification command should be available to re-run the completed final audit without changing candidate files. If final audit regenerates result files, disclose that fact.

## 5. Required output contract

Only under `stage_A/reconciled/step2_controlled_repair_v2/`:

- `PREDECESSOR_V1_FINGERPRINT.json` and `V2_BASELINE_MANIFEST.json`, with immutable v1 and frozen-input checks;
- `candidates/<C>/template/` (six v1-repaired baseline copies with v2 targeted changes);
- `APPROVED_SCOPE_AND_DECISIONS.md` (compact user approvals, explicit non-goals, six reviewer readings);
- `CHANGE_LOG.jsonl` (one semantic correction per atomic entry, affected candidate paths, before/after hashes, policy IDs, source evidence);
- `GATE_LOG.jsonl`, `CHECKPOINTS/`, `STATUS.json`, `RESUME.md` (per-step gate including all earlier fixes and full 196 x 6 policy checks); `REGRESSION_MATRIX.md` and `POLICY_IMPACT_GRAPH.json`;
- `_tools/` only if necessary for reproducible scripts/fixtures; keep all scratch repos and temp data under v2 root;
- `PI012_EXTRA_21_REVIEW.jsonl`, `PI012_REMAINING_ADJUDICATION.jsonl`, `REVIEW_NEEDED_62.jsonl`, `PARTIAL_WITNESSES_38.jsonl`, `NEW_CLAIMS_42_REVIEW.jsonl`, and `REVIEWER_SIX_READINGS.md` (using verified actual counts; adjust names/counts if sources differ);
- `V1_TO_V2_CROSSWALK.jsonl`, v2 repaired classifications and policy coverage, with current source anchors, `DATASET_MANIFEST.json`, explicit original-vs-derived views and deterministic replay;
- `FINAL_PARITY_AND_CONSISTENCY_REPORT.md` stating exactly which proposed edits were necessary, which were `NO_CHANGE_VERIFIED`, all policy/architecture test outcomes, remaining uncertainties, NOT_RUN evidence, and `GO`/`CONDITIONAL_GO`/`BLOCKED` recommendation for Step 3 **without starting Step 3**.

Do NOT force a particular count of atomic gates. Let actual independently justified changes set the count. Report how many files and claims changed relative to **v1** as well as relative to the original frozen `inputs/`. Never silently reset old 27 checks or pretend the first v1 27 checkpoints belong to v2. Keep both history levels traceable.

## 6. Stop rules

- If any substantive gate cannot pass, repair/rollback that change and STOP at the exact blocker. No progression on a known semantic regression.
- If source evidence conflicts with a user-approved rule, identify it precisely and preserve both rather than silently creating a new user policy. Only ask a question when implementation genuinely requires a decision not already covered by the approved register; otherwise preserve a qualified unresolved item and continue where safe.
- Do NOT edit the original inputs, v1, Step 2/audit, Codex output, or research Git. Do NOT start Step 3. Do NOT publish external/private pages.
- At completion, report evidence-backed totals, unresolved issues, independent-review limitations, and the exact folder to ZIP for external review.
