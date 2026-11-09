# Audit B — Phase 5.4 engineering-requirement parity backlog

## Comparison model and counts

Hold application specification, selected stack, input repository, acceptance tests and model constant. The initial stack includes .NET/C#, EF Core with SQL Server, NUnit and Angular when the same task calls for a frontend. An optional frontend slot does not authorize ignoring an explicit Angular requirement. No paired generation, application build or measured quality experiment was run.

Axis 1 compares engineering obligations: strength, trigger, scope and exceptions. Axis 2 compares delivery/reachability mechanisms. Placement, file counts, tokens, hook timing and capability replaceability are independent variables, not automatic semantic failures.

Priorities: one HIGH shared-contract violation (PAR-001, already A-001); one MEDIUM confirmed parity-only configuration gap (PAR-002); two MEDIUM UNCERTAIN semantic questions (PAR-003/004); three separate reachability risks. The 196-row matrix has 192 WORDING_ONLY rows, one SHARED_CONTRACT_VIOLATION, one PARITY_GAP and two UNCERTAIN rows. WORDING_ONLY describes the inspected normalized obligation, not complete architectural identity. Related policies reference the same finding rather than multiplying its count.

## PAR-001 — Remote HTTP may leak into Application in M1

**SHARED_CONTRACT_VIOLATION; HIGH severity; HIGH confidence; priority 1.** Canonical ARC-025 (MUST, path, backend): Infrastructure translates remote HTTP responses into Application-facing abstractions; no HttpResponseMessage or remote transport concerns in Application. Source: `M/source/inventory.json#policygroups[id=architecture].policies[id=ARC-025].normalized_policy`; identical in every candidate.

| Candidate | Status | Current evidence |
|---|---|---|
| M | SAME | M/output/template/.claude/rules/architecture.md:158  /  - Infrastructure translates remote HTTP responses into Application-facing abstractions; do not leak `HttpResponseMessage` or remote transport concerns into Application. |
| M1 | DIFFERENT | M1/output/template/.claude/rules/architecture.md:135  /  - Infrastructure translates remote HTTP responses into Application-facing abstractions; do not leak `HttpResponseMessage` or remote transport concerns into Application contracts unless the Application explicitly models HTTP. |
| L0 | SAME | L0/output/template/.claude/rules/1-architecture/backend-layers.md:40  /  - Infrastructure translates remote HTTP responses into the Application-facing abstraction; do not leak `HttpResponseMessage` or other remote-transport concerns into Application. |
| L1-Restart | SAME | L1-Restart/output/template/.claude/rules/1-architecture/roles.md:31  /  - The implementation layer translates remote HTTP responses into use-case-layer abstractions; remote transport response objects and other remote transport concerns must not leak into the use-case layer. |
| K0 | SAME | K0/output/template/.claude/rules/backend/integrations.md:13  /  - Infrastructure translates remote HTTP responses into Application-facing abstractions; `HttpResponseMessage` and other remote transport concerns must not leak into Application. |
| K1 | SAME | K1/output/template/.claude/rules/backend/architecture.md:25  /  - Infrastructure translates remote HTTP responses into Application-facing abstractions; `HttpResponseMessage` and other remote transport concerns must not leak into Application. |


Identical hypothetical task: add a supplier HTTP adapter to an existing Clean Architecture application, with an Application port and adapter tests. M1's exception can justify an HTTP-shaped Application contract merely by describing it as explicitly modeling HTTP. The other five require translation at the infrastructure boundary. This could change coupling, response-lifetime handling and testing seams; no generated code or comparative quality was observed.

The common source dictates the required obligation. Historical V2 technique contains the exception, but normalized priority removes authority ambiguity. M1's ASP.NET-Core-type prohibition and skill anti-pattern were checked as contrary evidence; neither reliably cancels its explicit remote-HTTP exception. See A-001 for all five blocker elements. Proposed action: remove the unsupported exception in M1's existing normative owner, preserving its flat organization and capability mechanism. This is necessary for 5.3 readiness independently of the 5.4 backlog; do not defer a hard violation by relabeling it parity-only. No change implemented.

## PAR-002 — Configured diagnostic severity and build activation differ

**PARITY_GAP; MEDIUM severity; HIGH confidence in configuration, UNVERIFIED runtime effect; priority 2.** Related normalized rules: RUN-009 (follow repository/.editorconfig defaults), RUN-010 (MUST clean changed-file unused/redundant usings), DEP-023 (shared build settings in Directory.Build.props), WF-007 (risk-scoped architecture/format/analyzer/dependency/security checks). Exact normalized text and JSON anchors are in the four corresponding matrix rows.

The source does not define an exact analyzer set, AnalysisLevel, IDE0005 severity, documentation generation switch, warning-as-error threshold, or mandatory build-versus-format diagnostic channel. Therefore **REQUIRES_RESEARCH_DECISION**; no evidence justifies copying L0 or the strictest candidate into the rest.

| Candidate | Six-way configuration status | Directory.Build.props evidence | .editorconfig evidence |
|---|---|---|---|
| M | DIFFERENT | `M/output/template/Directory.Build.props:11`: AnalysisLevel latest; `:13`: EnforceCodeStyleInBuild true; no GenerateDocumentationFile property | `M/output/template/.editorconfig:34`: IDE0005 warning; comments at 32–33 note the documentation prerequisite |
| M1 | DIFFERENT | `M1/output/template/Directory.Build.props:7`: target/nullable/implicit-usings baseline; no explicit AnalysisLevel, EnforceCodeStyleInBuild or GenerateDocumentationFile | `M1/output/template/.editorconfig:28`: IDE0005 suggestion |
| L0 | DIFFERENT | `L0/output/template/Directory.Build.props:7`: latest; `:9`: enforce; `:11`: documentation generation; `:12`: suppress CS1591 | `L0/output/template/.editorconfig:27`: IDE0005 warning |
| L1-Restart | DIFFERENT | `L1-Restart/output/template/Directory.Build.props:4`: target/nullable/implicit-usings baseline; none of the three explicit diagnostic properties above | `L1-Restart/output/template/.editorconfig:27`: IDE0005 warning |
| K0 | DIFFERENT | `K0/output/template/Directory.Build.props:8`: AnalysisLevel latest; no enforce/documentation properties | `K0/output/template/.editorconfig:23`: IDE0005 warning |
| K1 | DIFFERENT | `K1/output/template/Directory.Build.props:6`: target/nullable/implicit-usings baseline; none of the three explicit diagnostic properties above | `K1/output/template/.editorconfig:28`: IDE0005 suggestion |

DIFFERENT here means different from at least one other candidate's configured diagnostic requirements, not failure of a prescribed canonical threshold. M1 and K1 form the same observed configuration group. Matrix cells remain SAME against WF-007's shared minimum and annotate this additional gap. No explicit TreatWarningsAsErrors was found in these supplied configurations; warning does not automatically mean a failed build, and an omitted property does not mean all SDK analysis is disabled.

Identical hypothetical task: change a .NET 10 class, leaving a redundant using and a code-style/analyzer issue, then perform configured verification. Depending on SDK/project conditions and invoked tools, candidates can surface different diagnostic sets/severities and therefore different evidence before completion. The templates' settings support this plausible validation confounder; an actual build/formatter experiment is NOT_RUN. All six still instruct removal of redundant usings in changed files and risk-scoped checks, so this is not a missing-cleanup-policy finding.

Proposed 5.4 action: decide the benchmark's common diagnostic set, severity, applicable triggers and failure policy; align only those engineering thresholds in each candidate's native configuration/owner. Preserve distinct workflow/routing designs. Verify eventual effective diagnostics with the same SDK and fixture. Do not introduce a mandatory analyzer dependency merely to make files look equal.

## PAR-003 — Production-migration default qualifier

**UNCERTAIN; MEDIUM severity; MEDIUM confidence; not counted as a confirmed gap or blocker.** WF-019 (MUST_NOT, workflow) says no automatic production startup migrations **by default**, explicit deployment operation with approved credentials, and no Development seeding in Production. Source: `M/source/inventory.json#policygroups[id=workflows-delivery].policies[id=WF-019].normalized_policy`.

| Candidate | Status | Current evidence |
|---|---|---|
| M | SAME | M/output/template/.claude/skills/development-workflow/SKILL.md:101  /  - Do not apply production database migrations automatically from normal application startup by default: production migration is an explicit deployment operation at a controlled point, using approved credentials and failing visibly, and deployment never runs Development seeding in Production. Technique: `ci-cd`, `docker`. |
| M1 | SAME | M1/output/template/.claude/skills/verify/SKILL.md:120  /  - production database migrations are not applied automatically from normal application startup by default; production migration is an explicit deployment operation that uses approved credentials, and Development seeding never runs in Production. |
| L0 | SAME | L0/output/template/.claude/skills/delivery-pipeline/SKILL.md:33  /  - Do not apply production database migrations automatically from normal application startup by default — in containers or anywhere else. |
| L1-Restart | UNVERIFIED | L1-Restart/output/template/.claude/skills/development-workflow/SKILL.md:42  /  - Never apply production database migrations automatically from normal application startup: production migration is an explicit deployment operation using approved credentials, and Development seeding never runs in Production. |
| K0 | SAME | K0/output/template/.claude/skills/delivery-pipeline/SKILL.md:26  /  - Do not apply production database migrations automatically from normal application startup by default. A production migration is an explicit deployment operation: a dedicated step at a controlled point of the deployment, using the project's approved credentials, failing visibly. Migration scripts or bundles may be generated earlier in CI and executed during deployment. |
| K1 | SAME | K1/output/template/.claude/skills/delivery-change/SKILL.md:34  /  - Production database migrations must not run automatically from normal application startup by default. A production migration is an explicit deployment operation: make the step explicit, use the project's approved credentials, run it at a controlled point, and fail visibly on error. |


L1-Restart's workflow says “Never” without “by default”. The other five retain the qualifier. Contrary evidence: L1-Restart `CLAUDE.md:38` says explicit user instruction counts as approval and requires recording the accepted decision. All six require explicit production deployment control and forbid Development seeding in Production. Effective handling of an approved exception was not executed or exhaustively resolved against the hierarchy; a stronger local phrase alone is insufficient here to prove a material violation.

Identical hypothetical task: after an explicit recorded deployment decision, implement an approved one-off controlled migration arrangement that runs at startup, never seeds Production and uses approved credentials. The narrower sentence could trigger extra refusal or a different deployment shape; the approval protocol could resolve it equivalently. Neither outcome was measured. The normalized qualifier is known; no new engineering default needs invention. Proposed 5.4 action: clarify the workflow/approval relationship while retaining the normalized default and production-seeding prohibition. Until then, L1-Restart is UNVERIFIED for this exception case.

## PAR-004 — Explicit-request exception for floating versions

**UNCERTAIN; MEDIUM severity; MEDIUM confidence; not counted as a confirmed gap or blocker.** DEP-003 (MUST, workflow) requires registry-verified latest stable compatible versions and avoidance of prerelease/floating versions **unless explicitly requested**. Source: `M/source/inventory.json#policygroups[id=dependencies-stack].policies[id=DEP-003].normalized_policy`.

| Candidate | Status | Current evidence |
|---|---|---|
| M | SAME | M/output/template/.claude/skills/add-dependency/SKILL.md:41  /  1. Determine the latest stable version compatible with the project's target framework/runtime and peer dependencies. 2. Verify the current version from the package registry rather than relying on a remembered version or an example. 3. Do not select preview, alpha, beta, RC, dev, nightly, or other prerelease versions, and do not use floating versions such as `*`, unless explicitly requested. |
| M1 | UNVERIFIED | M1/output/template/.claude/skills/add-dependency/SKILL.md:43  /  1. determine the latest stable version compatible with the project's target framework/runtime and peer dependencies; 2. verify the current version from the package registry rather than relying on a remembered version; 3. do not select preview, alpha, beta, RC, dev, nightly, or other prerelease versions unless explicitly requested; 4. do not use floating versions such as `*`. |
| L0 | SAME | L0/output/template/.claude/skills/add-dependency/SKILL.md:21  /  1. Determine the latest **stable** version compatible with the target framework/runtime and peer dependencies — verify it from the package registry rather than from memory or examples. 2. Do not select preview, alpha, beta, RC, dev, nightly, or other prerelease versions, and do not use floating versions such as `*`, unless the user explicitly requests it. |
| L1-Restart | SAME | L1-Restart/output/template/.claude/skills/add-dependency/SKILL.md:25  /  1. Determine the latest **stable** version compatible with the project's target framework/runtime and peer dependencies, verified from the package registry — never from memory. 2. Do not select preview, alpha, beta, RC, dev, nightly, or other prerelease versions, and never floating versions such as `*`, unless explicitly requested. |
| K0 | SAME | K0/output/template/.claude/skills/add-dependency/SKILL.md:28  /  1. Determine the latest **stable** version compatible with the project's target framework/runtime and peer dependencies. 2. Verify the current version from the package registry instead of relying on a remembered version; do not copy versions from examples or older content. 3. Do not select preview, alpha, beta, RC, dev, nightly or other prerelease versions, or floating versions such as `*`, unless explicitly requested. |
| K1 | SAME | K1/output/template/.claude/skills/add-dependency/SKILL.md:30  /  1. Determine the latest **stable** version compatible with the project's target framework/runtime and peer dependencies. 2. Verify it from the package registry rather than from memory. 3. Never select preview, alpha, beta, RC, dev, nightly, or other prerelease versions, or floating versions such as `*`, unless the user explicitly requested them. |


M1 puts the explicit-request exception on prereleases, then separately says no floating versions at line 49. The other five attach the exception to both categories. M1's `CLAUDE.md:100` permits explicit instructions to count as approval, but effective handling of an approved floating-version exception through its full hook/checker path was not established. The unapproved floating-version rejection probes passed; they do not settle the approved case.

Identical hypothetical task: explicitly request a temporary floating package version in an approved experiment and record the exception. M1 might reject what another template permits, or its governance protocol might reconcile it. This remains a plausible difference, not a measured or confirmed one. Canonical intent is explicit; proposed 5.4 action is to clarify the exception consistently in prose and enforcement without making floating versions the default. No implementation or extra test cycle is started here.

## Intentional architecture differences to preserve

M is flat and V2-lineage constrained; M1 adds four static capability replacement boundaries. L0/L1-Restart organize by stability and enforce strict technology neutrality in Core/Architecture; only L1 adds capability selection. K0/K1 organize standards by scope with Kind-based conformance; only K1 adds the four slots. Candidate specifications establish these choices (`M/CANDIDATE.md:29`, `M1/CANDIDATE.md:51`, `L0/CANDIDATE.md:20`, `L1-Restart/CANDIDATE.md:1`, `K0/CANDIDATE.md:17`, `K1/CANDIDATE.md:67`). Class: INTENTIONAL_ARCHITECTURE_DIFFERENCE.

These choices can affect context costs and what must be read for the same task. Such comparability limits are transparent independent variables, not proof of better/worse code and not reasons to erase architecture identity. No additional candidate-specific stricter engineering outcome was established as a separate confirmed parity gap in this bounded review.

## Delivery/reachability axis — measure separately

### RCH-001 — Path rules and explicit workflow owner reads

**REACHABILITY_RISK; MEDIUM severity; MEDIUM confidence in risk, no measured failure.** Shared path/workflow obligations are distributed differently. Entry routers: `M/output/template/CLAUDE.md:157`, `M1/output/template/CLAUDE.md:118`, `L0/output/template/CLAUDE.md:78`, `L1-Restart/output/template/CLAUDE.md:46`, `K0/output/template/CLAUDE.md:62`, `K1/output/template/CLAUDE.md:66`. Development-workflow owner reads route greenfield work before matching files necessarily exist. Clean checkers report no broken references; each missing-verify negative is detected.

Same task: scaffold a backend endpoint before any backend source is open. Flat M rules, L neutral-principle plus technology layers, and K scoped standards can require different reads. The causal risk is failure to load an equivalent obligation, not absence of the obligation. Measure actual loaded owner sets and omissions later; do not homogenize paths or loading strategy.

### RCH-002 — Project-reference intervention before versus after execution

**REACHABILITY_RISK; MEDIUM severity; HIGH confidence in observed mechanism difference.** GOV-017 approval rules are SAME across six (CLAUDE anchors: M 102/112/136, M1 65/71/100, L0 37/39/55, L1-Restart 33/35/38, K0 34/36/49, K1 30/32/45). M's `.claude/hooks/dependency-guard.mjs:97` gates npm bypass flags before execution and `:130` routes project references afterward. The other five's discovered PreToolUse handlers rejected/asked for the tested reference mutation before execution. All six's post-failure checks detected the illegal Domain-to-Infrastructure fixture. Paths and raw outputs are in report 04.

Same task: attempt to add an outward project reference. M relies first on visible approval policy and then post-routing/validation; other implementations can stop/ask before the command. If an agent overlooks policy, an intermediate invalid state could exist longer in M. That is a delivery/enforcement timing hypothesis, not permission to bypass approval or an M freeze failure under its own task. Preserve mechanism; later measure compliance, intervention and recovery separately.

### RCH-003 — Selected capability facet indirection

**REACHABILITY_RISK; MEDIUM severity; MEDIUM confidence in risk.** SAME minimum obligation under the selected stack, different lookup path: M's `CLAUDE.md:9` imports technology decisions; L0 `:9–10` imports architecture/project decisions; K0 `:7` imports its register. M1 `:133–138` imports selection and capability decisions; L1-Restart `:9–11` imports frame/project/frontend decisions; K1 `:5` imports its selection-bearing register. All paths are under the named candidate's `output/template/`. Slot manifests/roles lead to selected technique/commands. Missing persistence MODULE is detected in all three capability candidates.

Same task: change a persisted entity and update provider-sensitive tests. A replacement-capability candidate has additional selected-facet reads; an embedded candidate follows direct technology rules/skills. A missed facet could omit equivalent technical guidance, but no live miss was observed. Measure facet resolution under a held-constant selection, and separately study authorized replacement. Optional Angular extensibility is not optional Angular for a task explicitly requiring it.

## Domain coverage and contrary evidence retained

| Domain | Bounded assessment |
|---|---|
| Clean Architecture, dependencies, repository/UoW/commit | ARC-001–029 mapped. No additional demonstrated material boundary difference beyond PAR-001. Frame/leaf placement preserved. |
| .NET/Angular selection, Controllers vs Minimal API | DEP and FE rows mapped. Selected technologies and approval gates retained. Backend-only configurability does not permit ignoring explicit frontend scope. |
| Diagnostics, package pinning, central management | PAR-002 and uncertain PAR-004. All six carry SDK/global.json scaffold guidance; no missing SDK-pin gap inferred solely from lack of a root global.json. |
| Persistence, transactions, seeding, migrations | PST-001–010 mapped. Provider-aware tests and synchronization steps found; PAR-003 concerns the production default qualifier only. |
| HTTP API/error/versioning/security semantics | API-001–022 and SEC-001–018 mapped. No confirmed status-code, error-body or authorization gap. Historical technique detail such as Location was not promoted to an invented mandatory policy. |
| Unit/integration frameworks, mocks, CI, coverage | TST rows mapped; NUnit selected, isolation/provider fidelity and regression preservation present. No coverage quota or identical unit/integration ratio invented. |
| Workflow strength and final verification | WF-001–022 mapped. Non-trivial-work router wording does not remove all-six final verification obligations. |
| Security, configuration, runtime/performance/style | SEC/RUN/GOV rows mapped. Defaults and conditional triggers retained; actual security/runtime outcomes NOT_RUN. |

The CSV is the full policy register. SAME is a bounded static finding, DIFFERENT identifies the confirmed ARC-025 permission change, and UNVERIFIED preserves unresolved qualifier cases. Inactive technology conditions are evaluated as conditional obligations, not blanket NOT_APPLICABLE rows. No missing policy was inferred solely from an unavailable external research citation. The audit stops with these findings and limitations.
