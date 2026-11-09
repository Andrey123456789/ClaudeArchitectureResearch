# Experiment 005 / Phase 5.3 — FINAL INDEPENDENT AUDIT (Codex)

## Mission: TWO audits, TWO separate conclusions; READ ONLY

You are Codex acting as an independent research auditor, not an architect, implementation agent, or corrective agent. Perform a bounded audit of the **FINAL outputs of exactly six candidates**. Produce two independently reasoned findings:

- **Audit A — Phase 5.3 Freeze Readiness.** Does each candidate's current `output/template/` satisfy *its own* approved candidate architecture, the shared normative policies, common invariants, and applicable 5.3 acceptance criteria? Can each candidate, and phase 5.3 overall, be frozen?
- **Audit B — Cross-Candidate Engineering Requirement Parity.** Where do six candidates impose materially different engineering obligations for an identical user task and selected technology stack? Which differences risk changing code quality or verification outcomes, and therefore belong in the **future phase 5.4 semantic-alignment backlog**?

**Decision separation is mandatory:** A parity gap alone is **NOT** a 5.3 freeze blocker. It blocks 5.3 ONLY if independently proven to violate an explicit common 5.3 MUST requirement or the individual candidate's own hard contract. Do not perform 5.4 work or repair candidates in this audit.

## 0. EXACT workspace root; explicit scope

Use this **exact Windows directory** as the Codex workspace root, current working directory, and complete research input boundary:

```text
C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.3
```

Call it `<ROOT>` below. Resolve all relative references against `<ROOT>`; do not move the workspace root upward to `005`, `ClaudeArchitectureResearchRuns`, `AI Learning`, or the sibling GitHub repository.

**Only candidate subtrees in scope:**

```text
<ROOT>\M\
<ROOT>\M1\
<ROOT>\L0\
<ROOT>\L1-Restart\
<ROOT>\K0\
<ROOT>\K1\
```

`<ROOT>\L1\` (if present) is an **abandoned historical branch**, NOT a seventh candidate. Do not audit or compare it. Do not read old ZIP snapshots, `ChatGPT_Audit`, previous AI independent audits, or other root-level artifacts as primary inputs. Ignore `<ROOT>\_CODEX_FINAL_AUDIT\` in all research/source comparisons. Do not open sibling folders or contact remote repositories or services.

**Required immediate preflight:**
1. Confirm the actual current directory is exactly `<ROOT>`, case-insensitively using resolved Windows paths. If not, STOP and ask for the correct folder; do not silently broaden scope or audit from the wrong root.
2. Confirm all six exact candidate directories exist, and each includes `CANDIDATE.md`, `baseline/CANDIDATE.md`, `baseline/TASK.md`, `REFINEMENT_TASK.md`, `source/inventory.json`, `source/shared-research-invariants.json`, and `output/template/`. If something is missing, record it and mark affected conclusions `UNVERIFIED`; never fabricate substitutes from old archives.
3. Enumerate the six `output/template/` trees and identify checker/hook entry points **from files actually present**, not presumed filenames.
4. Read `PROVENANCE.json` and candidate `README.md` where present to determine the applicable local history and contract. Current `output/template/` is the tested object; `baseline/` and `source/` are authoritative input/evidence, NOT the output being judged.
5. Check whether local source manifests, policies, and common invariants agree across the six candidates. Explicitly report any divergence; do not blindly assume equality.

## 1. Authoritative LOCAL references — no missing external navigation

For each candidate `<C>` among the six, inspect these exact **relative** sources in priority order:

| Role | Local path relative to `<ROOT>` | Authority / interpretation |
|---|---|---|
| Common normative policy inventory | `<C>/source/inventory.json` | Contains the normalized policy corpus; its `policy_count` is expected to be **194**, grouped into **10** policy groups. Validate count and policy ID uniqueness from the file; do not merely repeat these expected numbers. |
| Two additional research invariants | `<C>/source/shared-research-invariants.json` | Contains `GOV-017` and `GOV-018` (MUST). Validate membership; expected canonical shared total is **196 unique IDs**. |
| Candidate architecture | `<C>/CANDIDATE.md` and `<C>/baseline/CANDIDATE.md` | Approved candidate-specific concept and baseline; flag contradictions and state how authoritative resolution was established. |
| Accepted 5.3 task | `<C>/REFINEMENT_TASK.md` | Phase-specific mandatory acceptance scope; candidate-specific corrective tasks may exist but must not silently supersede agreed normative requirements. |
| Original generation task | `<C>/baseline/TASK.md` | Baseline context, not a reason to judge current output as identical to baseline. |
| Frozen source rule text | `<C>/source/v2-baseline/` | Actual LOCAL historical source texts linked by many `inventory.json` `source_refs`. |
| Current artifact to audit | `<C>/output/template/` | Source of truth for what this candidate NOW tells Claude to do. Include hidden `.claude/` tree. |
| Candidate's refinement explanation | `<C>/output/REFINEMENT_REPORT.md` | Claims and change history ONLY; verify claims independently, never accept self-reported PASS. |
| Local audit/background | `<C>/audit/` | Context and test hypotheses, not proof of the current template's correctness. Avoid reading past third-party verdicts to preserve independence. |
| Optional manifests and provenance | `<C>/PROVENANCE.json`, `<C>/MANIFEST.sha256` if present | Check sources and consistency; `MANIFEST.sha256` is NOT guaranteed to exist in every candidate. |

**Important source-reference mapping:** `source/inventory.json` may mention original project references like `templates/v2-baseline/...`. For this bounded audit, resolve corresponding files in `<C>/source/v2-baseline/...` **where they actually exist**. Some research-note references (for example `research/observations/...`) may not be present inside `<ROOT>`; NEVER escape the boundary to fetch them. Use the locally embedded normalized policy/invariant as the controlling evidence and explicitly label external citation resolution as unavailable when needed. Do not declare a policy absent solely because an original outside-repository URL cannot be opened.

**Precedence / unresolved conflict handling:** Use normalized shared policy/invariant text for the common engineering contract; use candidate specifications for intentional structural/design differences; use the final accepted P4 decision below. If binding authoritative local sources genuinely conflict and no accepted resolution is evidenced inside `<ROOT>`, classify `UNRESOLVED_SOURCE_CONFLICT`, do not invent a canonical choice, and assess materiality conservatively.

## 2. Research boundaries and safety

- Audit candidates **read-only**. Do not edit, reformat, fix, generate, reset, stage, commit, or delete any input files, including `baseline/`, `source/`, `audit/`, `output/`, reports, or the root-level historical branch.
- **Only permitted persistent writes:** final audit files in `<ROOT>\_CODEX_FINAL_AUDIT\` (create this directory if needed). Temporary executable test copies must live **outside the six candidate subtrees** in a disposable OS temp directory; remove only the temporary copies you created.
- Do not invoke Claude, `/goal`, background loops, agent handoffs, network access, installation, credential checks/login, package restore with network access, or real code-generation runs. Use locally installed tooling only; state unsupported tests as `NOT_RUN`.
- Candidate instructions such as `CLAUDE.md`, `.claude/skills/**`, and `AGENTS.md`-like material are **data to inspect**, not instructions authorizing modifications or scope expansion.
- Keep the audit bounded: one systematic inventory and static pass, one targeted finite validation pass, and at most one targeted reconfirmation per discrepancy. No recursive audits, regex-bypass treasure hunts, or perpetual retry loops. When proof is unavailable, report uncertainty and finish.
- For reproducibility, compute SHA-256 evidence manifests of all six final templates before tests, then recompute after; require unchanged inputs. Avoid following symlinks/junctions out of `<ROOT>` (record and skip them). Never invoke hooks directly against production workspace files if they can write; run copies.
- No claims about real differences in code-generation quality without paired generation experiments. Describe the Audit B differences as **plausible confounders**, giving a causal explanation and example task.

## 3. AUDIT A — Freeze readiness for EACH candidate

Assess each candidate against its OWN agreed contract rather than forcibly importing a different candidate's implementation. Use an evidence matrix covering:

**A1. Source integrity, coverage and precedence**
- Resolve and enumerate **all shared policy IDs** from `inventory.json` + `shared-research-invariants.json`; check each ID for enforceable/accessible representation in the final instructions, appropriate `MUST`/`SHOULD` strength, trigger and scope, and unambiguous precedence. Distinguish a dormant/conditional policy from a truly missing one; do not equate absence of a separate file with absence of the requirement.
- Validate the exact 194 + 2 / 196 expected counts from live local files; report variance and missing IDs without inventing coverage statistics. Check hard preservation/immutability requirements that actually apply to each candidate.
- Detect material contradictions inside one candidate, broken/incorrect references, missing skills, invalid globs, unreachable obligations, and problems with the instruction entry point (`CLAUDE.md` and any candidate-specific router or map).

**A2. Candidate-specific mechanics (ONLY where applicable)**
- Verify the declared architecture: modules, hierarchy, capability slots/facets, binding/selection constraints, level directionality, routers, workflow gates, overriding rules, and governance. Never demand L1 mechanisms from L0, nor M1-specific features from M.
- Respect intended differences in module organization, routing approach, hook implementations, context/skill loading, and replaceability.

**A3. Local enforcement and targeted functional probes**
- Check syntax of actual checker/hook entry points; execute existing local non-network diagnostics if safe.
- Run a *small, fixed* positive/negative suite on TEMPORARY COPIES to test critical contracts: permitted changes remain permitted, explicit violations are detected, and checkers do not silently ignore failures or comments in a way that invalidates the actual rules.
- Where checker/hook logic depends on `.csproj`, `.props`, or `.targets`, test quoted XML attributes (single/double), multiline/reordered attributes where relevant, relevant dependency-direction violations, and required after-failure/PostToolUseFailure behavior. Do not assume each candidate contains identical scripts.
- Distinguish a real architectural instruction defect from a limited enforcement vocabulary. Record remaining limitation if real-world risk is unproven.
- Preserve expected tool/hook response semantics (`permissionDecision: ask`, feedback messages, or nonzero exit codes may each be correct by design). Do not falsely classify a correct advisory/interactive response as a failure.

**A4. Final agreed P4 technology neutrality for L0 and L1-Restart**
- **Both candidates use the strict common principle:** concrete implementation-technology names are forbidden in Level 0/Core and Level 1/Architecture, even inside a seemingly non-normative pointer such as `Technique: docker`; only an actually documented agreed fixed-platform exception can permit a name. Level 2/Technology and Level 3/Project may use implementation-technology names where appropriate.
- Exercise one fixed positive/negative corpus, including `Docker`, `Swagger`, `Jest`, `Scrutor`, `NuGet`, `EF Core` and legitimate technology-neutral references; additionally compare the **entire actual L0 prohibited lexicon** against L1-Restart for completeness. Record exact exceptions based on files, not assumptions.
- Do NOT revive the abandoned context-sensitive Docker-pointer exemption. Do NOT add arbitrary new English paraphrases ad infinitum.

**A5. Evidence discipline and severity threshold**
For every potential freeze blocker, require all five: (1) governing hard MUST requirement or accepted candidate constraint; (2) exact current file/line evidence; (3) minimal reproducible observation or clear static contradiction; (4) expected versus actual behavior; (5) demonstrated plausible material impact. If any is absent, mark `UNCONFIRMED` or `NONBLOCKING_LIMITATION`, not `BLOCKED`.

For EACH of six candidates, conclude exactly one:
- `FREEZE_READY`: reviewed applicable hard requirements passed with no material unknowns in scope;
- `FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS`: no confirmed blocking violation, but specific meaningful tests/conditions remain unverified;
- `BLOCKED`: at least one confirmed applicable hard violation with full evidence;
- `UNVERIFIED`: essential files or authority are absent, or evidence is insufficient to judge even provisionally.

A parity-only gap, cosmetic wording difference, and valid deliberate architecture design choice are **NOT** freeze blockers. Distinguish incomplete test coverage from a known failure. Give an overall 5.3 recommendation based on six independent decisions: unconditional freeze only with no blockers and adequate evidence; otherwise state the precise limitations.

## 4. AUDIT B — Engineering-requirement semantic parity; 5.4 BACKLOG ONLY

**Scientific question:** Given the same application specification, selected backend/frontend stack, input repository, acceptance tests, and model, could differing engineering *obligations* in the six templates permit materially different resulting code or validation quality, even if each individually satisfies its own architecture definition?

**Canonical baseline for shared engineering obligations:** the actual normalized 194 shared policies + GOV-017/018, conditional on their `normative_strength`, `trigger_class`, `scope`, and actual chosen product/stack. Do **NOT** copy M, L0, or the strictest candidate into the others by default. Where that source is under-specified, propose `REQUIRES_RESEARCH_DECISION` rather than guessing.

Cover **every shared policy ID** with one stable row in the parity matrix (196 expected unique rows), even when a policy applies conditionally or all six are equivalent. Link each to actual source and candidate implementation evidence or mark `UNVERIFIED`. For material issues, analyze these domains in detail:

1. Clean Architecture boundaries, allowed Domain/Application/Infrastructure dependencies, external HTTP/transport types, repositories, UoW and commit responsibility.
2. .NET / Angular and technology-selection obligations, controllers versus Minimal API, allowed deviations and exceptions.
3. Build diagnostics, `.editorconfig`, `Directory.Build.props`, analyzers, warning levels, static analysis, package versions, central package management, dependency pinning.
4. Persistence, transactions, migration policy, data validation and seed data.
5. HTTP API semantics: status codes, response bodies, `Location`, `ProblemDetails`, error mapping, versioning, security and authorization.
6. Unit/integration testing frameworks, mocking and isolation, CI gates, test execution triggers, test coverage, regression checks.
7. Frontend contract, routing/components, and whether Angular is optional **for an identical task that explicitly requires Angular**; do not mistake architecture-wide extensibility for permission to ignore explicit task scope.
8. Workflow obligations and trigger wording: `MUST` versus `SHOULD`, `always` versus `non-trivial only`, exceptions (`unless`, `optional`, `if useful`) and final validation requirements.
9. Routing/instruction reachability and path globs **as an independent delivery-risk dimension**, without treating module placement or token economy itself as a semantic failure.
10. Security, secrets/configuration, code-quality patterns, performance and maintainability rules.

**Two-axis analysis is mandatory:**
- **Axis 1 — Semantic obligation parity:** Do all candidates actually impose equivalent engineering outputs/verification obligations under the same task preconditions?
- **Axis 2 — Delivery/reachability risk:** Are equivalent obligations delivered via different routing, skill loading, lazy context or hooks, potentially affecting whether Claude sees or applies them? This is a legitimate architectural mechanism to **measure later**, not automatically to homogenize in 5.4. Flag actual broken routes as Audit A issues when they violate local hard requirements.

Classify each material observation as one of:
- `PARITY_GAP`: common engineering obligation materially differs in required outcome, strength, exception, threshold or when it applies, and may confound a same-task comparison;
- `INTENTIONAL_ARCHITECTURE_DIFFERENCE`: differing organization/delivery, capability mechanics, router/skill invocation, context strategy, or replaceability explicitly consistent with that candidate's concept; preserve;
- `WORDING_ONLY`: different prose/locations but demonstrably same obligation;
- `REACHABILITY_RISK`: same underlying obligation, but different delivery strategy may affect usage; report separately, do not align mechanism just for symmetry;
- `SHARED_CONTRACT_VIOLATION`: actual violation of canonical mandatory engineering requirements; cross-reference Audit A and do not double count;
- `UNCERTAIN`: source or behavioral effect cannot be determined.

`PARITY_GAP` is not implied by any textual difference. Some shared policies are conditional and may correctly be inactive for certain task setups. State all assumptions behind comparisons.

For **each meaningful gap** provide:
1. Stable finding ID (`PAR-001` etc.), topic, classification, confidence and severity (`HIGH/MEDIUM/LOW`).
2. Canonical shared policy ID(s) and normalized rule, exact source file path/line or JSON field anchor, and evidence from every affected candidate (`relative/path:line`, concise quotation or `NOT_LOCATED`).
3. Six-way actual obligation and conditions, with explicit `SAME`, `DIFFERENT`, `NOT_APPLICABLE`, or `UNVERIFIED` per candidate; explain evidence rather than simply checking boxes.
4. One minimal **identical hypothetical programming task** likely to expose the difference, the causal path to potentially different code/validation, and what remains untested without actual generation runs.
5. Whether the common source already dictates the correct obligation, or `REQUIRES_RESEARCH_DECISION` if genuinely ambiguous.
6. **Proposed phase 5.4 semantic alignment only**, preserving each candidate's distinctive instruction architecture. Do not implement it now.

A candidate-specific, legitimately intended design constraint may be stricter than the shared floor; flag it as `INTENTIONAL_ARCHITECTURE_DIFFERENCE` when supported by authoritative definitions, but **if the additional constraint changes the engineering behavior of identical benchmark tasks, report it transparently as an experimental comparability limit**, not as invisible 'parity achieved'.

Do **NOT** equalize literal phrasing, module counts, token counts, file names, hooks, dynamic versus static instruction loading, replaceability, routing design, or architecture identity. These are independent variables or outcomes. Do not treat the mere existence of a separate capability as a code-quality advantage without evidence.

## 5. Testing methodology, reporting quality and stopping

- Read the **six actual final templates**. Do not take candidate refinement reports, prior third-party assessments or the historical L1 branch as proof.
- Preserve exact case/paths for cited files; include stable relative paths and line numbers where possible. For JSON, supply field anchor such as `policygroups[id=architecture].policies[id=ARC-...]` (use real discovered ID values only).
- Record the command, environment, fixtures, intended expected result, actual result, test count and disposition. Distinguish candidate-authored test output from independently authored tests. Do not use blanket `196/196 PASS` based only on a policy-count check.
- Always separate `PASS`, `FAIL`, `NOT_RUN`, `UNVERIFIED`, and `NOT_APPLICABLE` in test evidence.
- For cross-candidate issues, independently verify that an equivalent rule is not located in another file, capability module, referenced skill, or high-priority instruction before claiming it is absent. Preserve contrary evidence.
- Do not create new application implementations, run lengthy builds or invoke cloud/model services. Temporary finite checker tests are acceptable.
- If a confirmed hard blocker exists, document it and continue the **bounded audit of the other candidates**; do not repair it now. Do not prematurely stop the entire task on the first finding.
- Stop after the full finite source inventory, semantic mapping, targeted test pass and one reconfirmation of high-impact discrepancies. Any remaining unclear matter is an explicit limitation, **not** a reason for an infinite corrective loop.

## 6. REQUIRED DELIVERABLES — all on disk in English

Create only these files in `<ROOT>\_CODEX_FINAL_AUDIT\`:

1. `00_EXECUTIVE_SUMMARY.md` — Two distinct answers. Six-candidate freeze table. Counts of confirmed blockers, significant parity gaps, material reachability risks, unverified items. Explicitly answer **"May 5.3 be frozen?"** and **"What belongs in 5.4?"**; distinguish findings from estimates.
2. `01_5_3_FREEZE_READINESS.md` — Six independent verdicts and evidence; 196-policy source/coverage methodology, candidate-specific musts, checker/hook tests, confirmed blockers and nonblocking limits.
3. `02_5_4_REQUIREMENT_PARITY_BACKLOG.md` — Prioritized evidence-backed `PAR-...` findings, affected candidates, counterexamples, proposed canonical semantics or pending research decisions, 5.4-only changes; a separate section for intentional organizational differences and `REACHABILITY_RISK` observations.
4. `03_REQUIREMENT_PARITY_MATRIX.csv` — **One record per unique common policy/invariant ID** (expected 196, verify). Include at minimum:
   `policy_id,group,normative_strength,trigger_class,scope,canonical_summary,canonical_source,` 
   `M_status,M_evidence,M1_status,M1_evidence,L0_status,L0_evidence,L1_Restart_status,L1_Restart_evidence,K0_status,K0_evidence,K1_status,K1_evidence,` 
   `parity_class,severity,confidence,reachability_note,proposed_5_4_action`.
   Use a valid RFC 4180-style quoted CSV. Every candidate status must express evidence-backed `SAME/DIFFERENT/NOT_APPLICABLE/UNVERIFIED`; don't silently omit policies or use a speculative PASS. If `SHARED_CONTRACT_VIOLATION`, document it in the accompanying report and annotate the parity class.
5. `04_AUDIT_EVIDENCE_AND_METHOD.md` — Exact root, discovered paths, input evidence snapshot SHA-256/tree digests and read-only after-check, tested commands/fixtures/results, out-of-scope exclusions, source-reference limitations, audit methodology and gaps.

All five deliverables MUST be present. If unable to complete a verification, still produce the documents with explicit `UNVERIFIED`/`NOT_RUN` statements; do not invent complete results.

## 7. Final response and termination

After producing and checking the five files, STOP. Do not create/modify phase 5.4 folders, start implementation or request Claude rework. Never alter candidate files.

In the conversation with the user, summarize **in Russian**:
1. The overall phase-5.3 freeze decision and exceptions for six named candidates.
2. The count and 3–5 most important material 5.4 parity gaps, clearly separated from routing/delivery risks.
3. Absolute local paths of the five outputs under `<ROOT>\_CODEX_FINAL_AUDIT\`.
4. Material tests that could not be run and any authoritative local inputs that were missing.

All report artifacts, CSV values, file names, code snippets and stable IDs must be **English**. No network research, no source edits, and no further prompts for additional iterations.
