# Audit B — Phase 5.4 requirement parity backlog

## Comparison contract and decision separation

The normalized local inventory and two invariants control the common contract, not the strictest candidate or a self-reported PASS. Actual counts are 194 distinct inventory IDs in 10 groups plus GOV-017/GOV-018 (MUST), totaling 196 unique IDs. All six 43-file source trees are byte-identical. Every current CANDIDATE.md equals baseline/CANDIDATE.md, and all baseline TASK.md copies agree. Essential local inputs exist. The unavailable historical research citation does not remove the locally embedded invariant authority.

The CSV is a static clause-level evidence map, not 196/196 executed passes. SAME means the cited current owner expresses an equivalent obligation under the recorded trigger/scope and chosen stack; it does not certify live delivery or generated behavior. DIFFERENT identifies an extra exception/constraint relative to the normalized rule. UNVERIFIED preserves unresolved force/exception wording. Conditional policies remain represented when dormant in an empty template. Comparison assumes identical specification, repository, .NET/C#/SQL Server/NUnit/Angular selection, acceptance tests and model. An optional frontend slot never licenses ignoring an explicit Angular product requirement.

Semantic obligations and delivery are separate axes. Counts: 2 confirmed significant parity-only gaps; 1 shared-contract violation cross-referenced to Audit A; 3 uncertain observations; 2 delivery risks. No generated-code quality difference was measured. Stronger conditions are reported when they narrow identical benchmark choices; the candidate concepts reviewed do not explicitly require the added Polly eligibility test or one host lifetime.

## PAR-001 — Remote HTTP abstraction boundary

SHARED_CONTRACT_VIOLATION; severity HIGH; confidence HIGH; cross-reference A-001, counted once.

**Canonical:** M/source/inventory.json#policygroups[id=architecture].policies[id=ARC-025] (byte-identical in all six candidates) — MUST; Infrastructure translates remote HTTP responses into Application-facing abstractions; do not leak HttpResponseMessage or remote transport concerns into Application.

| Candidate | Status versus canonical | Current evidence |
|---|---|---|
| M | SAME | M/output/template/.claude/rules/architecture.md:158 — - Infrastructure translates remote HTTP responses into Application-facing   abstractions; do not leak `HttpResponseMessage` or remote transport concerns   into Application. |
| M1 | DIFFERENT | M1/output/template/.claude/rules/architecture.md:135 — - Infrastructure translates remote HTTP responses into Application-facing   abstractions; do not leak `HttpResponseMessage` or remote transport concerns   into Application contracts unless the Application explicitly models HTTP. |
| L0 | SAME | L0/output/template/.claude/rules/1-architecture/backend-layers.md:40 — - Infrastructure translates remote HTTP responses into the Application-facing abstraction; do not leak `HttpResponseMessage` or other remote-transport concerns into Application. |
| L1-Restart | SAME | L1-Restart/output/template/.claude/rules/1-architecture/roles.md:29 — - Default: represent common expected outcomes explicitly when useful (`null`, `bool`, a typed outcome), but do not force a generic result-wrapper pattern and do not name use-case outcome categories after HTTP statuses (bad request, unauthorized, forbidden); the entry point maps outcomes such as validation failure, not found, or conflict to HTTP. - Keep cache technology out of the domain model, and do not leak infrastructure cache APIs into the use-case layer without a deliberate boundary abstraction. - The implementation layer translates remote HTTP responses into use-case-layer abstractions; remote transport response objects and other remote transport concerns must not leak into the use-case layer.  /  L1-Restart/output/template/.claude/rules/2-technology/backend-platform.md:14 — - Entry-point mechanism: ASP.NET Core Controllers (decided stack), as controller classes in a `Controllers/` folder of the entry-point project; do not create Minimal API endpoint groups unless explicitly requested. - Transport result types that stay at the entry point: `IActionResult`, `ActionResult<T>`, `IResult`, and status-code constants. - Remote transport responses that the implementation layer translates: `HttpResponseMessage` and its headers and status. |
| K0 | SAME | K0/output/template/.claude/rules/backend/integrations.md:13 — - Infrastructure translates remote HTTP responses into Application-facing abstractions; `HttpResponseMessage` and other remote transport concerns must not leak into Application. |
| K1 | SAME | K1/output/template/.claude/rules/backend/architecture.md:25 — - Infrastructure translates remote HTTP responses into Application-facing abstractions; `HttpResponseMessage` and other remote transport concerns must not leak into Application. |

**Identical task:** implement a supplier HTTP adapter exposing response metadata to a use case. M1's exception could permit HttpResponseMessage at the Application boundary; the other five require translation. A neutral metadata model remains available to all. Contrary generic abstraction language and the M1 technique warning are retained in A-001. **Canonical resolution already exists:** restore the unconditional boundary in separately authorized correction while preserving M1's capability architecture. This is necessary for 5.3, not solely a future backlog item. No generation result was observed.

## PAR-002 — Eligibility for direct Polly exception

PARITY_GAP; MEDIUM severity; HIGH textual confidence. M/M1/K0 add a threshold relative to the common floor. No independent 5.3 MUST violation is established.

**Canonical:** M/source/inventory.json#policygroups[id=dependencies-stack].policies[id=DEP-020] (byte-identical in all six candidates) — DEFAULT; When resilience is required, prefer Microsoft.Extensions.Http.Resilience for HttpClient and Microsoft.Extensions.Resilience for general pipelines; direct Polly integration is an explicit exception rather than the default.

| Candidate | Status versus canonical | Current evidence |
|---|---|---|
| M | DIFFERENT | M/output/template/.claude/skills/add-dependency/SKILL.md:24 — - Package choices: - Resilience: when resilience is required, prefer `Microsoft.Extensions.Http.Resilience` for `HttpClient` and `Microsoft.Extensions.Resilience` for general resilience pipelines. Direct Polly usage is an explicit exception rather than the default — use it only when a concrete requirement cannot be expressed through those packages, and document why. Do not add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`. |
| M1 | DIFFERENT | M1/output/template/.claude/skills/add-dependency/SKILL.md:29 — - **Resilience** — when resilience is required, prefer `Microsoft.Extensions.Http.Resilience` for `HttpClient` and `Microsoft.Extensions.Resilience` for general pipelines. Never add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http` integrations. Direct Polly usage is an explicit exception: use it only when a concrete requirement cannot be expressed through the Microsoft resilience APIs, and document why. |
| L0 | SAME | L0/output/template/.claude/skills/add-dependency/SKILL.md:49 — - **Resilience:** when resilience is required, prefer `Microsoft.Extensions.Http.Resilience` for `HttpClient` and `Microsoft.Extensions.Resilience` for general pipelines; a direct Polly reference or Polly API configuration is an explicit, documented exception rather than the default (default). Do not add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`. |
| L1-Restart | SAME | L1-Restart/output/template/.claude/skills/add-dependency/SKILL.md:17 — - `Microsoft.Extensions.Http.Resilience` (outbound `HttpClient`) or `Microsoft.Extensions.Resilience` (other pipelines) — Default: these are the resilience packages when resilience is required; direct Polly usage is an explicit, documented exception, and the deprecated `Microsoft.Extensions.Http.Polly` / `Polly.Extensions.Http` integrations are never added; |
| K0 | DIFFERENT | K0/output/template/.claude/skills/add-dependency/SKILL.md:20 — - **Resilience** — when resilience is required, prefer `Microsoft.Extensions.Http.Resilience` for HttpClient and `Microsoft.Extensions.Resilience` for general pipelines (D-12). Do not add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`; a direct Polly reference or Polly API configuration is an explicit exception that needs a documented reason why the Microsoft.Extensions APIs cannot express the requirement. |
| K1 | SAME | K1/output/template/.claude/skills/add-dependency/SKILL.md:23 — - Default: when resilience is required, `Microsoft.Extensions.Http.Resilience` for `HttpClient` and `Microsoft.Extensions.Resilience` for general pipelines. Direct Polly usage is an explicit, documented exception; never add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`. |

M/M1/K0 require that Microsoft resilience APIs cannot express the requirement. L0/L1-Restart/K1 require an explicit documented exception without that impossibility test. All six prefer the same modern packages, require concrete need and due diligence, and prohibit deprecated integrations. The linked httpclient-factory/references/resilience.md material was checked across six candidates: it reinforces defaults and references the add-dependency owner without supplying a uniform impossibility threshold. This does not mean any candidate permits arbitrary undocumented Polly usage.

**Identical task:** add resilience to an existing adapter while retaining an approved reusable direct-Polly pipeline. Microsoft wrappers could express the same behavior; the proposed exception is interoperability with the existing pipeline. M/M1/K0's technical-inexpressibility condition can require a different implementation or decision; the other three can assess the stated reason without that proof. Dependencies, integration effort and validation scope could differ. No output difference was generated.

**REQUIRES_RESEARCH_DECISION:** decide whether a concrete documented justification is enough or technical inexpressibility is required. Phase 5.4 should align exception eligibility in existing owners/references, preserving hooks, governance and architecture. Do not adopt the strictest version by default.

## PAR-003 — Integration-test host lifetime

PARITY_GAP; MEDIUM severity; MEDIUM confidence in engineering effect. L1-Restart adds a prescription; no violation of mandatory isolation is proved.

**Canonical:** M/source/inventory.json#policygroups[id=testing-quality].policies[id=TST-006] (byte-identical in all six candidates) — DEFAULT; Use WebApplicationFactory-based integration testing when routing, binding, middleware, auth, DI, repositories, EF Core or database persistence is what the test must prove.

| Candidate | Status versus canonical | Current evidence |
|---|---|---|
| M | SAME | M/output/template/.claude/rules/testing.md:30 — - Use `WebApplicationFactory<Program>`-based integration tests when routing,   model binding, middleware, authentication/authorization, dependency   injection, repositories, EF Core, or database persistence is what the test   must prove. |
| M1 | SAME | M1/output/template/.claude/rules/testing.md:23 — Use `WebApplicationFactory<Program>`-based integration tests when routing, binding, middleware, authentication/authorization, dependency injection, repositories, or database persistence is what the test must prove. |
| L0 | SAME | L0/output/template/.claude/rules/2-technology/dotnet-testing.md:14 — - Use `WebApplicationFactory<Program>`-based integration tests when routing, binding, middleware, authentication/authorization, dependency injection, repositories, EF Core, or database persistence is what the test must prove (default). The `Testing` environment uses isolated test resources. |
| L1-Restart | DIFFERENT | L1-Restart/output/template/.claude/rules/2-technology/backend-testing/test-framework.md:10 — - Default: NUnit is the .NET automated test framework. In an established project that deliberately uses another framework, follow that convention; do not introduce a second test framework without a concrete reason. ## Bindings These bind the framework-neutral test rules to NUnit; they add no separate policy. - Explicit case = an NUnit `[TestCase]` row; `TestCaseSource` counts as generated case machinery. - In-process host for integration tests: `WebApplicationFactory<Program>`, created in `[OneTimeSetUp]` and disposed in `[OneTimeTearDown]`. Technique: `dotnet-testing`. Commands: `backend-testing.commands`. |
| K0 | SAME | K0/output/template/.claude/rules/backend-tests/testing.md:17 — - Default: use `WebApplicationFactory`-based integration tests when routing, binding, middleware, authentication, DI, repositories, EF Core or database persistence is what the test must prove. |
| K1 | SAME | K1/output/template/.claude/rules/backend-tests/testing.md:16 — - Default: `WebApplicationFactory`-based integration tests when routing, model binding, middleware, authentication/authorization, dependency injection, repositories, the persistence technology, or database persistence is what the test must prove. |

Related canonical rules: TST-001 default NUnit, TST-002 appropriate test level, TST-004/TST-008 isolation and owned known setup. L1-Restart test-framework.md:14 says bindings add no separate policy, but :17 fixes creation in OneTimeSetUp and disposal in OneTimeTearDown. Other normative owners require appropriate host tests without that single lifetime. M1 test-framework.md:16–18 accommodates SetUp/OneTimeSetUp. Technique examples were not counted as mandatory lifetime constraints.

**Identical task:** isolated authentication integration tests with per-test service overrides and mutable state, on the same NUnit/WebApplicationFactory stack. Per-test hosts and fixture hosts with explicit reset can both satisfy common isolation. L1's binding narrows setup choice and can require different reset/rebuild arrangements, affecting reliability or complexity. Shared hosts are not inherently invalid; no quality advantage is claimed.

**REQUIRES_RESEARCH_DECISION:** permit equivalent safe per-test/per-fixture lifetimes, or deliberately control one lifetime across benchmarks and document the additional obligation. Align only semantics if approved; retain L1 levels/capabilities. Actual generated setup and runtime remain NOT_RUN.

## PAR-004 — Diagnostic profiles; weaker obligations not established

UNCERTAIN; MEDIUM severity; HIGH confidence in configuration difference, LOW in changed accepted code. Canonical RUN-009, RUN-010, DEP-023 and WF-007 do not prescribe one analyzer profile. All six are SAME for common convention/cleanup obligations.

| Candidate | Exact current configuration evidence | Status for normalized obligation |
|---|---|---|
| M | Directory.Build.props:11–13: latest analysis, build code style; .editorconfig:34 IDE0005 warning, :53 interface warning. No GenerateDocumentationFile setting. | SAME |
| M1 | Directory.Build.props:7–9: target/nullable/implicit only; .editorconfig:28 IDE0005 suggestion. | SAME |
| L0 | Directory.Build.props:7–12: latest analysis, build code style, documentation generation and CS1591 suppression; .editorconfig:27 IDE0005 warning. | SAME |
| L1-Restart | Directory.Build.props:4–6: target/nullable/implicit only; .editorconfig:27 IDE0005 warning. | SAME |
| K0 | Directory.Build.props:8: latest analysis; .editorconfig:23 IDE0005 warning; no build code-style setting. | SAME |
| K1 | Directory.Build.props:6–8: target/nullable/implicit only; .editorconfig:28 IDE0005 suggestion, :62 async naming silent. | SAME |

Paths above are relative to each candidate/output/template. All six verify workflows explicitly require removing unused usings and inspecting changed files. Different IDE0005 configuration does not prove permission to retain them. No TreatWarningsAsErrors setting is present in these assets. M's .editorconfig:32 itself notes a documentation-generation condition for command-line reporting; severity alone is not observed output.

**Identical task:** the same service edit containing a redundant using and an interface naming deviation, followed by configured checks. Feedback could differ, but common explicit cleanup still applies. No application build ran; exact diagnostics and final code are UNVERIFIED. **REQUIRES_RESEARCH_DECISION:** decide whether analyzer configuration is a controlled input or a delivery variable, then verify with a paired offline fixture. No confirmed semantic gap or freeze blocker.

## PAR-005 — Explicit-case default versus required wording

UNCERTAIN; LOW severity; MEDIUM confidence. Canonical TST-005 is DEFAULT, not a blanket prohibition on case sources.

| Candidate | Status versus canonical | Current evidence |
|---|---|---|
| M | SAME | M/output/template/.claude/rules/testing.md:44 — For small finite input or state spaces, prefer explicit declarative cases (for example `[TestCase]`) over loops, branches, LINQ, generated case machinery, or code that computes the expected result. Prefer one observable scenario per test; a multi-step test fits when the sequence itself is the behavior. |
| M1 | UNVERIFIED | M1/output/template/.claude/rules/test-framework.md:16 — - Use normal NUnit conventions: `[TestFixture]` classes, `[Test]` for single scenarios, `[SetUp]`/`[OneTimeSetUp]` with matching teardown for fixture lifetime, and `Assert.That` constraint assertions. The explicit case tables required by `testing.md` § Test Readability are written as `[TestCase]` rows rather than `TestCaseSource` generators.  /  M1/output/template/.claude/rules/testing.md:36 — ## Test Readability For small finite input or state spaces, prefer explicit declarative test cases over loops, branches, LINQ, or generated case machinery inside tests; state expected results rather than computing them. Prefer one observable scenario per test; a multi-step test is appropriate when the sequence itself is the behavior. |
| L0 | SAME | L0/output/template/.claude/rules/0-core/testing-principles.md:31 — - For small finite input/state spaces, prefer explicit declarative cases over loops, branching, LINQ, or generated case machinery inside tests; state expected results instead of computing them (default). |
| L1-Restart | SAME | L1-Restart/output/template/.claude/rules/0-core/testing.md:13 — - Default: for small finite input/state spaces, list explicit declarative cases instead of loops, branching, LINQ, or generated case machinery inside tests, and state expected results instead of computing them. |
| K0 | SAME | K0/output/template/.claude/rules/backend-tests/testing.md:22 — - Default: for small finite input or state spaces, explicit declarative cases (for example `[TestCase]` rows) instead of loops, branching, LINQ or generated case machinery inside tests. |
| K1 | SAME | K1/output/template/.claude/rules/backend-tests/testing.md:26 — - Default: for small finite input/state spaces, explicit declarative cases instead of loops, branches, LINQ, or generated case machinery inside tests; expected results are stated by the test, not computed. |

M1 testing.md:38 says prefer; test-framework.md:18–20 calls case tables required. L1 classifies TestCaseSource as generated machinery while its neutral policy remains Default; that alone does not remove justified deviations. Contrary evidence prevents a confirmed blanket mandatory-case finding.

**Identical task:** add a finite-state test following an existing readable TestCaseSource convention with a concrete reason to retain it. M1's treatment as a justified default deviation or forbidden binding choice is UNVERIFIED. **Proposed 5.4 action:** clarify intended default force through bindings; a mandatory syntax rule requires a research decision. No measured effect or 5.3 blocker.

## PAR-006 — Production-startup migration exception wording

UNCERTAIN; MEDIUM severity; MEDIUM confidence. WF-019 prohibits startup migrations by default, requires deliberate deployment operations/approved credentials, and forbids Development seeding in Production.

| Candidate | Status versus canonical | Current evidence |
|---|---|---|
| M | SAME | M/output/template/.claude/skills/development-workflow/SKILL.md:101 — - Do not apply production database migrations automatically from normal   application startup by default: production migration is an explicit   deployment operation at a controlled point, using approved credentials and   failing visibly, and deployment never runs Development seeding in Production.   Technique: `ci-cd`, `docker`. |
| M1 | SAME | M1/output/template/.claude/skills/verify/SKILL.md:120 — - production database migrations are not applied automatically from normal   application startup by default; production migration is an explicit   deployment operation that uses approved credentials, and Development seeding   never runs in Production. |
| L0 | SAME | L0/output/template/.claude/skills/delivery-pipeline/SKILL.md:33 — - Do not apply production database migrations automatically from normal application startup by default — in containers or anywhere else. |
| L1-Restart | UNVERIFIED | L1-Restart/output/template/.claude/skills/development-workflow/SKILL.md:42 — - Never apply production database migrations automatically from normal application startup: production migration is an explicit deployment operation using approved credentials, and Development seeding never runs in Production. |
| K0 | SAME | K0/output/template/.claude/skills/delivery-pipeline/SKILL.md:26 — - Do not apply production database migrations automatically from normal application startup by default. A production migration is an explicit deployment operation: a dedicated step at a controlled point of the deployment, using the project's approved credentials, failing visibly. Migration scripts or bundles may be generated earlier in CI and executed during deployment. |
| K1 | SAME | K1/output/template/.claude/skills/delivery-change/SKILL.md:34 — - Production database migrations must not run automatically from normal application startup by default. A production migration is an explicit deployment operation: make the step explicit, use the project's approved credentials, run it at a controlled point, and fail visibly on error. |

L1-Restart/output/template/.claude/skills/development-workflow/SKILL.md:42 says Never without default; its ci-cd technique also warns against startup migrations. Other five retain by default in the owner or surrounding procedure. All six reserve material architecture/deployment changes for approval. Whether that governance preserves the same exceptional path in L1 is unresolved; neither a new absolute prohibition nor automatic exception is assumed.

**Identical task:** assess an explicitly requested single-instance deployment with approved production-startup migration. The uncertainty is approval overriding a default versus conflicting with an unconditional rule. Routine unapproved startup migrations are prohibited by all six. **REQUIRES_RESEARCH_DECISION:** define exception authority consistently while retaining credential, visible-failure and seed restrictions. No deployment/generation attempted.

## Intentional architecture differences — preserve

M is flat topical delivery; M1 adds four static slots. L0 uses stability levels; L1 combines levels/capabilities and bindings. K0 uses Kind -> Scope with one register; K1 adds Capability -> Kind -> Scope. File/module counts, token estimates, filenames, lazy loading, routers, binds and replaceability are experimental variables, not code-quality advantages. No homogenization is proposed.

All six preserve specification authority and challenge/Reserved-decision governance. Optional frontend cardinality in M1/L1/K1 does not override an explicit Angular requirement (GOV-001/GOV-003). Testcontainers optionality is not absence of a real-provider obligation when relational fidelity matters. Versions were not judged obsolete through network research.

## Separate delivery axis

**RCH-001 — Split owner/facet and path delivery.** REACHABILITY_RISK; MEDIUM severity/confidence. Evidence: each CLAUDE.md, transitive imports in report 04, .claude/MAP.md and CSV owner paths. M/M1 use flat path rules/workflows; L0 splits neutral architecture from technology; L1 adds facet resolution; K0/K1 route through Kind/Scope/register, with K1 capability facets. L1 ARC-025 combines roles.md and backend-platform.md; M expresses both in architecture.md. L1 PST-008 resides in the selected persistence workflow facet, others in direct workflows/skills. Import targets exist and representative static globs cover code/tests/manifests, but actual host retention and symbolic-route use are untested. Measure whether equivalent edits load all owners; do not flatten modules or broaden all globs for symmetry. No specific broken route proved.

**RCH-002 — Pre-routing versus post-state enforcement.** REACHABILITY_RISK; MEDIUM severity; HIGH routing confidence, MEDIUM impact confidence. Evidence: six settings.json files and exact pre/post records. M's pinned package/reference probes are quiet pre-execution with later state checking. M1/K0 deny and request workflow markers. L1 denies/retries package commands and asks for force/reference approval. L0/K1 permit pinned-package probes but block tested force/reference commands. All six still require due diligence, and after-failure probes detect active XML violations. Equivalent edits may meet the owner at different times. Quiet pre-output does not prove absence of policy; markers/retry do not prove due diligence occurred. Measure invocation/approval and post-failure repair later, preserving design.

## Domain review coverage

| Domain | Result |
|---|---|
| Architecture, repositories, UoW, external HTTP | Shared inward boundary and commit model represented; PAR-001 exception. |
| Platform/frontend, controllers versus Minimal API | Common defaults and approval controls; optional slot does not change explicit task scope. |
| Diagnostics, CPM, pinning, dependencies | Common controls mapped; finite XML evidence; PAR-002/PAR-004. |
| Persistence, transactions, migrations, seeds | Common rules and seed co-change routes; PAR-006 uncertainty; no database run. |
| HTTP status/body/Location/ProblemDetails/versioning/auth | Owner evidence supports normalized rules; no other confirmed material gap. |
| Tests, isolation, provider fidelity, regression and CI | Common floors; PAR-003/PAR-005; no execution benchmark. |
| Workflow triggers and verification | Textual obligations mapped; live delivery separately uncertain. |
| Security, secrets, performance, maintainability | Shared owners mapped; no assertion of vulnerability absence or measured performance. |

Only approved semantic alignment belongs in 5.4. No changes implemented and no 5.4 folder created.
