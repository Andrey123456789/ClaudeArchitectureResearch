# Decision implementation matrix

Built before the first edit. Authority: `_STAGE_A_KIT/61_...TASK_EN.md` (contract) and `_STAGE_A_KIT/62_...RU.md` (the user's approved decisions). Evidence paths are relative to `inputs/<C>/output/template/`; they were read on 2026-11-03 from the frozen inputs. Status is kept in `STATUS.json`, `GATE_LOG.jsonl` and `CHECKPOINTS/`, not here.

Modification types: `TEMPLATE_RULE`, `ENFORCEMENT`, `CLASSIFICATION_ONLY`, `PROTOCOL`, `NO_CHANGE_VERIFIED`, `DEFERRED`.

## Order and why it differs from the raw queue

The contract order is kept. Three written refinements:

1. `9.1 protected branches` is the register's approved variation of `HQ-01`, so it is one logical rule with `R02`, not a separate gate.
2. The 103 corrections run after all template rules, because a template edit can move, reword or remove the quoted claim (contract §3.5, §4). PI-012-dependent corrections are adjudicated against the addendum from `R01`.
3. `R06` (peer bypass) runs after `R04` (floating exception) because both touch the same command classifiers in M1 and K1. The exception record must never read as a route around the peer rule. That interaction is a named regression in both suites.

## Rules

| Rule | Item | Target behavior | Evidence (original) | Candidates | Type | Depends on | Tests | Expected gate |
|---|---|---|---|---|---|---|---|---|
| R01 | HQ-06 PI-012 | Separate semantics and condition, source authority, and modality. Equivalent `only when` / `do not unless` under equal authority and scope get the same modality. Bare negation is not automatically a prohibition. Technique does not become policy without owner evidence | `METHODOLOGY_NOTE.md`, `PI012_NEGATIVE_MODALITY_REVIEW.jsonl`, `A13_RESIDUAL_LEADS.jsonl` | all (data) | PROTOCOL, CLASSIFICATION_ONLY | none | all 79 + 230 read one by one; blind pass then compare; equivalence pairs; dedup by key; sensitivity | PASS when every case has a disposition, quotes verify, frozen protocol hash unchanged |
| R02 | HQ-01 / GOV-015 and 9.1 | Git changes need a specific request or a clearly bounded pre-approved operation or scope. Generic approved workflow is no authority. Pre-existing uncommitted changes at task start: two options only (commit identified changes with authorized scope, or suspend for manual cleanup); headless without an adequate standing choice pauses. Changes made during the task are not that condition. Re-check authority and foreign changes before dangerous actions. Explicit request to rewrite `main` is valid unless another policy forbids it | `CLAUDE.md` § Git (M:145, M1:109, L0:69, L1:52, K0:53, K1:57); `git-workflow` destructive and push sections; K0 `hook.cjs` Git ask; K0 `git-workflow:13` | all six | TEMPLATE_RULE; ENFORCEMENT only where a Git hook already exists (K0) | R01 for record modality | staged, unstaged, untracked, foreign, clean tree in disposable Git repos; headless; reset and force-push; explicit and vague main authorization; K0 hook executed; mutations | PASS |
| R03 | HQ-02 / RUN-021 | Invalidation is coherent with the successful mutation. Strategy accounts for isolation level, concurrent read and refill, commit and rollback order, crash between commit and invalidate, retries, documented staleness. Pre-mutation invalidation allowed when correctness is shown. `commit -> evict` is not claimed atomic | `rules/performance.md` M:57, M1:72; `0-core/runtime-principles.md` L0:22; `0-core/backend-code.md` L1:36; `backend/caching.md` K0:16; `backend/runtime.md` K1:39; `caching` skills M:92, M1:86, L0:43/51, L1:49, K0:66, K1:56 | all six | TEMPLATE_RULE | none | semantic timelines: commit, rollback, crash window, concurrent refill, isolation comparison, staleness; no Redis needed | PASS |
| R04 | HQ-03 / DEP-003 | Floating and prerelease forbidden by default. An explicit bounded user request authorizes the named package and range. Checkers honor the same exception without a global switch | `add-dependency` (M:45, M1:47, L0:22, L1:26, K0:30, K1:32); checkers M `check-manifests.mjs:232,339`; M1 `check-manifests.js:127,151`; L0 `manifest-checks.mjs:272,329`; L1 `post-change-checks.mjs:74,87`; K0 `check-dependencies.cjs:177,196`; K1 `check-manifests.cjs:112,141`, `classify-command.cjs` | all six | TEMPLATE_RULE, ENFORCEMENT | none | default rejected, authorized accepted, wrong package, wrong range, wrong manifest, wildcard record, malformed record, no global disable; network registry NOT_RUN | PASS |
| R05 | HQ-04 / GOV-017 | Headless may implement a specific, previously explicitly approved Reserved change. It may not make a new Reserved decision. Vague authorization is insufficient. Record approval evidence and scope, emit a decision log, stop on an unexpected Reserved choice | `CLAUDE.md` M:138-141, M1:101-105, L0:16/55, L1:38, K0:48-49, K1:45-46; `architecture-decision` skills | all six | TEMPLATE_RULE | R02 (headless wording stays compatible) | scenario matrix; text postconditions; mutations | PASS |
| R06 | HQ-05 / DEP-025 | `ask`, shell markers and comments cannot override. `--force` and `--legacy-peer-deps` used to evade an unresolved peer conflict are denied. Legitimate installs keep working | M1 `dependency-commands.js:16,392`, `add-dependency:101-108`; L1 `pre-shell-command.mjs:169`; K0 `hook.cjs:290-295` (marker skips the force denial); L0 `add-dependency:55`; M, K1 hooks | all six | ENFORCEMENT, TEMPLATE_RULE | R04 | hooks executed: direct, marker, nested shell, chained, env and config forms, safe installs; mutations | PASS |
| R07 | 8.1 Swagger UI | Applicable Development API behavior change: open Development Swagger UI and confirm it loads. Equal obligation and condition, native routing kept. Not applicable without a UI or a runnable app; that verification is reported NOT RUN | `swagger` M:137, M1:119, L0:90, L1:64, K0:86, K1:70; `verify` smoke lines M:75, M1:56, L0:38, L1:33, K0:46, K1:39 | all six | TEMPLATE_RULE | R02 no; none | text postconditions; WF-005, WF-006, API-016, TST-010 entailment; live UI NOT_RUN | PASS_WITH_NOT_RUN |
| R08 | 8.2 K0 CPM | Checker honors the effective `ManagePackageVersionsCentrally`, including inherited setting, rejects disabled or overridden values, keeps central version enforcement | K0 `scripts/check-dependencies.cjs:167-169`; DEP-006 | K0 | ENFORCEMENT | none | property in each permitted place, disabled, conflicting, project-level override; MSBuild evaluation attempted only as a labeled extra | PASS, with effective-state limit documented |
| R09 | 8.3 K1 compiled queries | Align with RUN-008: measured or clearly demonstrated need, no speculative use | K1 `ef-core:128,241`; `backend/runtime.md:13` | K1 | TEMPLATE_RULE | none | text postconditions, counterexample | PASS |
| R10 | 8.4 L0 production migrations | Align with WF-019: no automatic Production migration at normal startup by default; separately approved controlled deployment-time steps stay possible; credential and no-seeding guarantees kept | L0 `project-structure:70`; `delivery-pipeline:33-35` | L0 | TEMPLATE_RULE | none | text postconditions, SEC-001 and seeding retained | PASS |
| R11 | 8.7 CUSTOM_SETTINGS | L0, K0, K1 read `CUSTOM_SETTINGS.md` when planning a new application or substantial feature, as M, M1, L1 do. Absent or empty file stays legitimate. No second normative owner | `development-workflow` M:19, M1:15, L1:12, L0:17, K0:14, K1:18 | L0, K0, K1 | TEMPLATE_RULE | none | text postconditions; absence and empty behavior; budget unchanged | PASS |
| R12 | 8.7 K1 local migrations | Remove only the standalone duty to mutate a local database in every scenario. Keep migration generation and review, schema before seed, validation | K1 `persistence-change:45`; PST-005, 006, 009, 010 | K1 | TEMPLATE_RULE | none | negative test: retained duties must stay | PASS |
| R13 | 8.7 test priority | Compare all six. Fix classification first. Change text only for a demonstrated difference | `dotnet-testing`, `code-review` in six | all (data) | CLASSIFICATION_ONLY unless a difference is proven | none | six-way source comparison | PASS |
| R14 | 8.7 C# language version | Same method for language-version checks | `modern-csharp`, `code-review` in six | all (data) | CLASSIFICATION_ONLY unless a difference is proven | none | six-way source comparison | PASS |
| R15 | 8.5 HTTP timeout | No Markdown change. All six separate client cancel, local timeout, upstream timeout. Label fixes only | `http-api` M:207-213, M1:206-212, L0:52, L1:42, K0:82, K1:50 | all (data) | NO_CHANGE_VERIFIED | none | six-way source check, modality check | PASS |
| R16 | 8.6 L1 liveness | Do not weaken the principle. Grade the skill example under PI-012 | L1 `rules/0-core/http-api.md`; `health-check:22-25` | L1 (data) | NO_CHANGE_VERIFIED | R01 | source check, API-019 | PASS |
| R17 | 8.7 security scan minimality | No change, principle in all six | `security-scan` M:218+, M1:201+, L0:114, L1:107, K0:136, K1:134 | all (data) | NO_CHANGE_VERIFIED | none | source check | PASS |
| R18 | 8.7 fast and slow external tests | No change, present in all six | `dotnet-testing` in six | all (data) | NO_CHANGE_VERIFIED | none | source check | PASS |
| R19 | 8.7 CI dependency auto-updates | Keep in L0, L1, K0, K1. Label as outside practical evaluation. No CI trial | L0 `delivery-pipeline:25`, L1 `ci-cd:77`, K0 `ci-cd:97`, K1 `delivery-change:25` | L0, L1, K0, K1 (data) | NO_CHANGE_VERIFIED | none | source check, retained in all four | PASS |
| R20 | 9.2 K0 deserialization | Read as a security-audit criterion. No HARD product prohibition without an owner. Keep the risk register | K0 `security-scan/references/scan-layers.md:77` | K0 (data) | CLASSIFICATION_ONLY | R01 | source check, SEC-003 not extended | PASS |
| R21 | 10 four clauses | Source-verify; add as separate candidate-specific proposals; no promotion and no replication | `NEW_CLAUSE_PROPOSALS.jsonl` | M, M1, L0 (data) | CLASSIFICATION_ONLY | none | quote verification | PASS |
| R22 | 11.1 trigger and delivery | Derive `applicability_trigger` and `delivery_context` with explicit unknowns. Keep the original field. No claim of 4,617 verified | `DRIFT_DIAGNOSTIC.md`; all records | all (data) | CLASSIFICATION_ONLY | R01 | counts, provenance, sampled reading stated as a sample | PASS |
| R23 | 11.2 cross-method adjudication | MIXED, partial witnesses, 5 strength cells, 3 qualified overrides and source-policy conflicts: semantic entailment, falsifying counterexample, executable test where applicable. Keep disagreements | `COVERAGE_OVERRIDE_REVIEW.jsonl`, `UNRESOLVED_QUEUE.jsonl` | all (data) | CLASSIFICATION_ONLY | R02-R12 | per-cell review | PASS |
| R24 | 11.3 limits | State same-family reviewer bias, targeted sampling, NOT_RUN and no unbiased error rate | `SEMANTIC_AUDIT_REPORT.md` | report | PROTOCOL (documentation) | none | presence check | PASS |
| R25 | 103 corrections | Each one accepted, rejected or unresolved against original and current sources. 43 / 51 / 9 groups verified, not assumed | `CORRECTION_PROPOSALS.jsonl` | all (data) | CLASSIFICATION_ONLY | R01-R24 | per-record gate with whole-dataset invariants | PASS |
| R26 | Repaired view | `FROZEN_BASELINE_REFERENCE` untouched; `REPAIRED_CANDIDATE_DERIVED_VIEW` with crosswalk, recomputed coverage, deterministic replay | §4 | all (data) | CLASSIFICATION_ONLY | R25 | replay, identities, quote resolution, 196 x 6 | PASS |
| R27 | Final audit | Cold re-read from final bytes, falsification attempts, all fixtures | §6 | all | none | all | §6 list | PASS_WITH_DOCUMENTED_NOT_RUN or BLOCKED |

## Known cross-queue interactions (impact graph seeds)

- Git authority (R02) and headless Reserved approval (R05) both speak about what a headless run may do. Neither may read as authority for the other.
- Floating exception (R04) and peer bypass (R06) share command classifiers. An exception record never authorizes a force flag.
- Peer denial (R06) and K0's dependency marker: the marker keeps its routing role but never suppresses the force denial.
- Cache semantics (R03) and transactions, Unit of Work and logging rules: no change to commit-boundary ownership.
- L0 migration wording (R10) and seeding and credential rules, plus the same scaffolding line in M, M1, L1, K1 (a parity lead, see below).
- Swagger UI (R07) and noninteractive verification: unavailable runtime is reported NOT RUN, never PASS.
- PI-012 modality (R01) and every record edited later: modality of a reworded claim is read under the addendum.

## Parity leads recorded for the user, not edited here

- The line "Production migration automation" in a scaffolding step also exists in M, M1, L1 and K1. The register approves the change for L0 only (`8.4`). See `UNRESOLVED_DECISIONS.jsonl` once written.
- L1 `development-workflow:42` says "Never apply" with no "by default". Not in the approved queue. Recorded as a parity lead.

## Final status

Added after the gates. The matrix above is unchanged from before the first edit.

| Rule | Decision | Gate |
|---|---|---|
| R01 | HQ-06 PI-012 reading | PASS |
| R02 | HQ-01, 9.1 Git authority, dirty tree, protected branches | PASS_WITH_NOT_RUN |
| R03 | HQ-02 cache invalidation | PASS_WITH_NOT_RUN |
| R04 | HQ-03 floating versions | PASS_WITH_NOT_RUN |
| R05 | HQ-04 headless Reserved work | PASS_WITH_NOT_RUN |
| R06 | HQ-05 peer bypass | PASS_WITH_NOT_RUN |
| R07 | 8.1 Swagger UI | PASS_WITH_NOT_RUN |
| R08 | 8.2 K0 effective CPM | PASS_WITH_NOT_RUN |
| R09 | 8.3 K1 compiled queries | PASS_WITH_NOT_RUN |
| R10 | 8.4 L0 Production migrations | PASS_WITH_NOT_RUN |
| R11 | 8.7 CUSTOM_SETTINGS | PASS_WITH_NOT_RUN |
| R12 | 8.7 K1 local migrations | PASS_WITH_NOT_RUN |
| R13 | 8.7 test priorities | PASS_WITH_NOT_RUN |
| R14 | 8.7 C# language version | PASS_WITH_NOT_RUN |
| R15 | 8.5 HTTP timeout | PASS_WITH_NOT_RUN |
| R16 | 8.6 L1 liveness | PASS_WITH_NOT_RUN |
| R17 | 8.7 security scan minimality | PASS_WITH_NOT_RUN |
| R18 | 8.7 fast and slow tests | PASS_WITH_NOT_RUN |
| R19 | 8.7 CI dependency updates | PASS_WITH_NOT_RUN |
| R20 | 9.2 K0 deserialization | PASS_WITH_NOT_RUN |
| R21 | 10 four new clauses | PASS_WITH_NOT_RUN |
| R22 | 11.1 applicability and delivery | PASS_WITH_NOT_RUN |
| R23 | 11.2 cross-method adjudication | PASS_WITH_NOT_RUN |
| R24 | 11.3 evidence limits | PASS_WITH_NOT_RUN |
| R25 | 103 corrections | PASS_WITH_NOT_RUN |
| R26 | Repaired view | PASS_WITH_NOT_RUN |
| R27 | Final audit | PASS_WITH_NOT_RUN |
