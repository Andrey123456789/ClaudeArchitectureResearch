# EXTRA and LINK_UNCERTAIN constraints — candidate K0

Generated deterministically from the annotation ledger. Each entry cites the exact
source evidence (path, line range, verbatim quote). `policy_ids` on an EXTRA entry
name the closest oracle policy only; origin stays EXTRA.

## EXTRA constraints (243)

### EXTRA-K0-0001
- Closest oracle policies: none
- Modality: MUST
- Normative action: CLAUDE.md and the decision register govern every task; path-scoped standards govern the files they cover; workflows own procedures; knowledge skills supply technique and never override a standard.
- Trigger/scope: repo/meta (instruction precedence)
- Exceptions: none
- Why EXTRA: Instruction-layer precedence is not an oracle policy.
- Evidence K0-S000422: `output/template/CLAUDE.md:11-11` — "- This file and the decision register govern every task. Standards in `.claude/rules/<scope>/` govern the files they cover. Workflows own procedures; knowledge skills supply technique and never override a standard."

### EXTRA-K0-0002
- Closest oracle policies: GOV-001, GOV-008
- Modality: MUST_NOT
- Normative action: SPECIFICATION.md, CUSTOM_SETTINGS.md, feature specifications and task prompts are product inputs: they may request a decision change but never silently override CLAUDE.md, the decision register or a standard.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Product-input vs engineering-policy precedence not stated in the oracle.
- Evidence K0-S000423: `output/template/CLAUDE.md:12-12` — "- `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specifications and task prompts are product inputs: they define product behavior and may request a decision change, but they never silently override this file, the decision register or a standard."

### EXTRA-K0-0003
- Closest oracle policies: none
- Modality: MUST
- Normative action: Vocabulary: a must/must-not violation is a defect; a deviation from a 'default' needs a concrete reason and must be reported; prefer/avoid are guidance; 'requires approval' marks a Reserved decision.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Reporting obligation for default deviations is not in the oracle.
- Evidence K0-S000424: `output/template/CLAUDE.md:13-13` — "- Vocabulary: **must / must not** — a violation is a defect; **default** — deviation needs a concrete reason and must be reported; **prefer / avoid** — guidance; **requires approval** — a Reserved decision (below)."

### EXTRA-K0-0004
- Closest oracle policies: ARC-020, ARC-001
- Modality: REQUIRES_APPROVAL
- Normative action: A change to the project reference graph is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Not gated by ARC-020.
- Evidence K0-S000444: `output/template/CLAUDE.md:39-39` — "3. a new production project, layer or assembly, or a change to the project reference graph;"
- Evidence K0-S001511: `output/template/.claude/skills/project-structure/SKILL.md:34-34` — "1. Classify the change. The layer references listed in `references/backend-layout.md` § Project references (D-01) are decided; any other added or removed reference changes the project reference graph and is Reserved (CLAUDE.md § Decisions) even when it is architecturally legal — raise a Decision Request with `architecture-decision` and wait for approval."

### EXTRA-K0-0005
- Closest oracle policies: ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: New search, external storage or external identity infrastructure is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Beyond ARC-020's list.
- Evidence K0-S000446: `output/template/CLAUDE.md:41-41` — "5. a new infrastructure category: messaging, background processing, distributed cache, search, external storage, external identity;"

### EXTRA-K0-0006
- Closest oracle policies: DEP-001, GOV-013
- Modality: REQUIRES_APPROVAL
- Normative action: A new major library or framework is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: The oracle requires a concrete need, not approval.
- Evidence K0-S000447: `output/template/CLAUDE.md:42-42` — "6. a new major library or framework;"
- Evidence K0-S000517: `output/template/.claude/skills/add-dependency/SKILL.md:15-15` — "2. Use the approved technology from the decision register; a conditional technology only when its capability is now needed. A new major library or framework, or a replacement of an approved technology, is Reserved — stop with a Decision Request (CLAUDE.md § Decisions)."

### EXTRA-K0-0007
- Closest oracle policies: ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Any project-wide convention or abstraction other code must follow is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Generalizes ARC-020's project-wide Result example.
- Evidence K0-S000448: `output/template/CLAUDE.md:43-43` — "7. a project-wide convention or abstraction other code must follow, such as a project-wide Result model;"

### EXTRA-K0-0008
- Closest oracle policies: API-013, DEP-017
- Modality: REQUIRES_APPROVAL
- Normative action: Adopting API versioning is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: API-013 requires a concrete need, not approval.
- Evidence K0-S000450: `output/template/CLAUDE.md:45-45` — "9. a breaking public API change or adopting API versioning;"
- Evidence K0-S000597: `output/template/.claude/skills/api-versioning/SKILL.md:10-10` — "adopting versioning is Reserved"

### EXTRA-K0-0009
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST
- Normative action: An explicit user instruction counts as approval; every accepted decision must be recorded (workflow architecture-decision).
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Recording obligation added to GOV-017.
- Evidence K0-S000453: `output/template/CLAUDE.md:48-48` — "- For a Reserved decision raise a **Decision Request** — Context, Options, Recommendation, Blocked, Proceeding with — and wait. An explicit user instruction counts as approval; record every accepted decision (workflow: `architecture-decision`)."
- Evidence K0-S000630: `output/template/.claude/skills/architecture-decision/SKILL.md:31-31` — "An explicit user instruction to adopt a specific option counts as approval. In an autonomous or headless run, continue only with the "Proceeding with" path and report the request as unresolved."

### EXTRA-K0-0010
- Closest oracle policies: none
- Modality: MUST
- Normative action: Changes to the instruction system go through /template-maintenance, which the user runs (never model-invoked); the model asks the user to run it.
- Trigger/scope: repo/meta (instruction-system change)
- Exceptions: none
- Why EXTRA: Instruction-system maintenance gate not in the oracle.
- Evidence K0-S000464: `output/template/CLAUDE.md:73-73` — "| Changing this instruction system | ask the user to run `/template-maintenance` (never model-invoked) |"
- Evidence K0-S000642: `output/template/.claude/skills/architecture-decision/SKILL.md:59-59` — "3. Changes to `.claude/` instruction files are instruction-system maintenance: ask the user to run `/template-maintenance` for structural changes, and run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.cjs"` after any edit."
- Evidence K0-S001650: `output/template/.claude/skills/template-maintenance/SKILL.md:4-4` — "disable-model-invocation: true"

### EXTRA-K0-0011
- Closest oracle policies: DEP-023, RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: Shared build settings Nullable enable, ImplicitUsings enable and AnalysisLevel latest.
- Trigger/scope: all .NET projects (MSBuild import)
- Exceptions: none
- Why EXTRA: Concrete compiler/analyzer settings not in the oracle.
- Evidence K0-S000474: `output/template/Directory.Build.props:6-8` — "<Nullable>enable</Nullable> ⏎     <ImplicitUsings>enable</ImplicitUsings> ⏎     <AnalysisLevel>latest</AnalysisLevel>"
- Evidence K0-S001484: `output/template/.claude/skills/project-structure/references/solution-layout.md:58-58` — "analysis and compiler settings"

### EXTRA-K0-0012
- Closest oracle policies: GOV-007
- Modality: MUST
- Normative action: architecture-decision updates the register entry and every artifact listed in Affects; policy detail stays with the 'Details in' owner.
- Trigger/scope: always (planning-time, all work)
- Exceptions: Register changes.
- Why EXTRA: Decision-propagation mechanism not in the oracle.
- Evidence K0-S000071: `output/template/.claude/MAP.md:161-178` — "D-01 (Clean Architecture) →"
- Evidence K0-S000484: `output/template/docs/architecture/decision-register.md:5-5` — "Every entry is **Decided** (CLAUDE.md § Decisions). Changing an entry is Reserved: run `architecture-decision`, which updates the entry and every artifact in **Affects**. Policy detail stays with the **Details in** owner. Paths are relative to `.claude/` unless they start with `docs/` or name a repository-root file."
- Evidence K0-S000640: `output/template/.claude/skills/architecture-decision/SKILL.md:57-57` — "1. Edit every artifact in the entry's **Affects** list so that each keeps only its own responsibility: standards cite the ID, knowledge adjusts technique, workflows adjust commands, enforcement adjusts checks (for example the deny-lists in `.claude/scripts/check-dependencies.cjs`). Example: replacing the backend test framework touches the testing standard, the testing knowledge skill, scaffolding  …"
- Evidence K0-S001668: `output/template/.claude/skills/template-maintenance/SKILL.md:44-44` — "2. Decision added or changed: follow `architecture-decision` § 3–4 (ID, Details in, Affects, propagation)."

### EXTRA-K0-0013
- Closest oracle policies: DEP-006
- Modality: MUST
- Normative action: A VersionOverride needs a concrete reason that is reported.
- Trigger/scope: path-scoped: *.csproj, Directory.*.props, package.json, package-lock.json
- Exceptions: Concrete reported reason.
- Why EXTRA: VersionOverride condition not in the oracle.
- Evidence K0-S000270: `output/template/.claude/rules/common/dependencies.md:22-22` — "- Use NuGet Central Package Management (D-17): package versions belong in `Directory.Packages.props`. Project `PackageReference` entries are versionless by default — a `VersionOverride` needs a concrete, reported reason — and must not duplicate centrally managed versions."

### EXTRA-K0-0014
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: Keep status behaviour consistent across similar endpoints.
- Trigger/scope: path-scoped: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Cross-endpoint consistency obligation not in the oracle.
- Evidence K0-S000088: `output/template/.claude/rules/backend/api.md:18-18` — "- Choose 200/201/202/204 by actual HTTP semantics: do not return 200 for every outcome, 201 merely because a row was inserted internally, or 202 for work that already completed. Keep status behavior consistent across similar endpoints."

### EXTRA-K0-0015
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: Prefer primary constructors for simple injection/initialization and regular constructors when validation is non-trivial, explicit fields read better or the codebase uses that style; no mechanical conversion.
- Trigger/scope: path-scoped: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Constructor-style guidance not in the oracle.
- Evidence K0-S000154: `output/template/.claude/rules/backend/csharp.md:19-19` — "- Prefer primary constructors for simple dependency injection or initialization, and a regular constructor when validation or initialization is non-trivial, explicit fields read better, or the codebase consistently uses that style; do not convert constructors mechanically."
- Evidence K0-S001383: `output/template/.claude/skills/modern-csharp/SKILL.md:24-24` — ""
- Evidence K0-S001414: `output/template/.claude/skills/modern-csharp/SKILL.md:127-127` — "Newest syntax for its own sake; every class turned into a record; `record struct` merely to avoid allocations; `Span<T>` without a performance reason; deeply nested patterns; mass constructor conversion; language or framework version changes without approval."

### EXTRA-K0-0016
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: Prefer records where value semantics/immutability are intended and classes where identity, lifecycle, inheritance or framework behaviour matters; do not turn every DTO or Domain type into a record.
- Trigger/scope: path-scoped: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Record/class guidance not in the oracle.
- Evidence K0-S000155: `output/template/.claude/rules/backend/csharp.md:20-20` — "- Prefer records where value semantics and immutability are intended (many DTOs, genuine Value Objects) and classes where identity, mutable lifecycle, inheritance or framework behavior matters; do not turn every DTO or Domain type into a record."
- Evidence K0-S001388: `output/template/.claude/skills/modern-csharp/SKILL.md:38-38` — ""
- Evidence K0-S001414: `output/template/.claude/skills/modern-csharp/SKILL.md:127-127` — "Newest syntax for its own sake; every class turned into a record; `record struct` merely to avoid allocations; `Span<T>` without a performance reason; deeply nested patterns; mass constructor conversion; language or framework version changes without approval."

### EXTRA-K0-0017
- Closest oracle policies: RUN-009
- Modality: MUST
- Normative action: Keep implementation details non-public unless they belong to the public API; use sealed only to communicate deliberate design intent, not as speculative optimization.
- Trigger/scope: path-scoped: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Visibility/sealed rule not in the oracle.
- Evidence K0-S000156: `output/template/.claude/rules/backend/csharp.md:21-21` — "- Keep implementation details non-public unless they belong to the project's public API; use `sealed` when it communicates deliberate design intent, not as a speculative optimization."

### EXTRA-K0-0018
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: Prefer var when the type is obvious or unimportant and an explicit type when it aids understanding.
- Trigger/scope: path-scoped: backend/**/*.cs
- Exceptions: none
- Why EXTRA: var guidance not in the oracle.
- Evidence K0-S000157: `output/template/.claude/rules/backend/csharp.md:22-22` — "- Prefer `var` when the type is obvious from the right-hand side or unimportant, and an explicit type when it aids understanding. Use standard .NET naming (PascalCase for types and members, camelCase for parameters and locals, meaningful names over abbreviations); private-field naming follows the repository's convention."

### EXTRA-K0-0019
- Closest oracle policies: RUN-009, RUN-024
- Modality: MUST
- Normative action: Standard .NET naming (PascalCase types/members, camelCase parameters/locals, meaningful names); private fields follow the repository convention.
- Trigger/scope: path-scoped: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Naming convention not in the oracle.
- Evidence K0-S000157: `output/template/.claude/rules/backend/csharp.md:22-22` — "- Prefer `var` when the type is obvious from the right-hand side or unimportant, and an explicit type when it aids understanding. Use standard .NET naming (PascalCase for types and members, camelCase for parameters and locals, meaningful names over abbreviations); private-field naming follows the repository's convention."

### EXTRA-K0-0053
- Closest oracle policies: DEP-020, DEP-004
- Modality: MUST_NOT
- Normative action: Do not add the deprecated Microsoft.Extensions.Http.Polly or Polly.Extensions.Http packages.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Concrete package ban not in the oracle.
- Evidence K0-S000520: `output/template/.claude/skills/add-dependency/SKILL.md:20-20` — "- **Resilience** — when resilience is required, prefer `Microsoft.Extensions.Http.Resilience` for HttpClient and `Microsoft.Extensions.Resilience` for general pipelines (D-12). Do not add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`; a direct Polly reference or Polly API configuration is an explicit exception that needs a documented reason why the Microsoft.Extension …"

### EXTRA-K0-0054
- Closest oracle policies: DEP-020
- Modality: MUST
- Normative action: A direct Polly reference or Polly API configuration needs a documented reason why the Microsoft.Extensions APIs cannot express the requirement.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Documentation obligation not in the oracle.
- Evidence K0-S000520: `output/template/.claude/skills/add-dependency/SKILL.md:20-20` — "- **Resilience** — when resilience is required, prefer `Microsoft.Extensions.Http.Resilience` for HttpClient and `Microsoft.Extensions.Resilience` for general pipelines (D-12). Do not add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`; a direct Polly reference or Polly API configuration is an explicit exception that needs a documented reason why the Microsoft.Extension …"

### EXTRA-K0-0055
- Closest oracle policies: DEP-010, DEP-004
- Modality: MUST_NOT
- Normative action: Do not add a deprecated or legacy ASP.NET automatic-validation integration package without a concrete requirement.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: Concrete requirement.
- Why EXTRA: Specific package-class ban not in the oracle.
- Evidence K0-S000522: `output/template/.claude/skills/add-dependency/SKILL.md:22-22` — "- **Validation** — `FluentValidation.DependencyInjectionExtensions` for registration; do not add a deprecated or legacy ASP.NET automatic-validation integration package without a concrete requirement (D-05)."
- Evidence K0-S000665: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:116-116` — "Register validators with `FluentValidation.DependencyInjectionExtensions`, follow the project's established invocation pattern instead of adding a second competing mechanism, and avoid deprecated automatic-validation integration packages. A request can be syntactically valid and still violate an Application or Domain rule; when a rule is enforced in several layers, each layer has its own reason."

### EXTRA-K0-0056
- Closest oracle policies: DEP-003, DEP-004
- Modality: MUST
- Normative action: Run the package command with the trailing '# add-dependency: reviewed' marker only after steps 1-4 (need, version, due diligence, license approval) are complete.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Self-declared marker discipline not in the oracle.
- Evidence K0-S000541: `output/template/.claude/skills/add-dependency/SKILL.md:75-75` — "- The pre-command hook stops package-changing commands — additions, updates and removals, with or without global options such as `--prefix`, and any `--force` or `--legacy-peer-deps` install — until this workflow has run. After steps 1–4, run the command with the trailing marker comment `# add-dependency: reviewed`, for example:"

### EXTRA-K0-0057
- Closest oracle policies: DEP-001, GOV-014
- Modality: MUST
- Normative action: Remove a dependency that is no longer used when that is part of the current change and safe to verify; do not leave dead references behind.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: Within the current change and safely verifiable.
- Why EXTRA: Dead-reference removal obligation not in the oracle.
- Evidence K0-S000548: `output/template/.claude/skills/add-dependency/SKILL.md:90-90` — "Remove a dependency that is no longer used when that is part of the current change and safe to verify; do not leave dead references behind, and do not perform unrelated dependency cleanup during a narrowly scoped task."

### EXTRA-K0-0058
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Report package, selected version and why, license, deprecation and vulnerability status, approval obtained, files changed and verification result.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Workflow output contract not in the oracle.
- Evidence K0-S000550: `output/template/.claude/skills/add-dependency/SKILL.md:94-94` — "Package, selected version and why, license, deprecation and vulnerability status, approval obtained (if needed), files changed, verification result."

### EXTRA-K0-0059
- Closest oracle policies: FE-002
- Modality: DEFAULT
- Normative action: Route-level/page components coordinate UI behaviour; reusable presentation components receive data through explicit inputs and emit meaningful UI events.
- Trigger/scope: on-demand knowledge angular (frontend)
- Exceptions: none
- Why EXTRA: Component-role split not in the oracle.
- Evidence K0-S000560: `output/template/.claude/skills/angular/SKILL.md:52-52` — "Route-level/page components coordinate UI behavior; reusable presentation components receive data through explicit inputs and emit meaningful UI events."

### EXTRA-K0-0060
- Closest oracle policies: FE-004
- Modality: PREFER
- Normative action: Use computed for derived state and avoid effect() when computed, template binding or explicit event handling expresses the dependency more clearly.
- Trigger/scope: on-demand knowledge angular (frontend)
- Exceptions: none
- Why EXTRA: effect() guidance not in the oracle.
- Evidence K0-S000563: `output/template/.claude/skills/angular/SKILL.md:65-65` — "Use `computed` for derived state, and avoid `effect()` when `computed`, template binding or explicit event handling expresses the dependency more clearly."

### EXTRA-K0-0061
- Closest oracle policies: FE-010
- Modality: DEFAULT
- Normative action: Keep transport/request mapping of forms explicit; duplicate a complex Domain rule in TypeScript only when the UI genuinely needs an equivalent user-facing rule.
- Trigger/scope: on-demand knowledge angular (frontend)
- Exceptions: Genuine user-facing need.
- Why EXTRA: Form-mapping and rule-duplication guidance not in the oracle.
- Evidence K0-S000576: `output/template/.claude/skills/angular/SKILL.md:107-107` — "Reactive forms give explicit state, validation and testability for non-trivial forms; keep transport/request mapping explicit. Duplicate a complex Domain rule in TypeScript only when the UI genuinely needs an equivalent user-facing rule."

### EXTRA-K0-0062
- Closest oracle policies: DEP-014
- Modality: DEFAULT
- Normative action: Use Angular Material components consistently for common UI primitives where they meet the requirement; wrap a Material component in a custom abstraction only for a concrete reason.
- Trigger/scope: on-demand knowledge angular (frontend)
- Exceptions: Concrete reason.
- Why EXTRA: Material usage/wrapping guidance not in the oracle.
- Evidence K0-S000585: `output/template/.claude/skills/angular/SKILL.md:134-134` — "Use Material components consistently for common UI primitives where they meet the requirement; wrap a Material component in a custom abstraction only for a concrete reason."

### EXTRA-K0-0063
- Closest oracle policies: TST-002, DEP-016
- Modality: DEFAULT
- Normative action: E2E tests cover a small number of important user workflows unless the project requires more, and the same behaviour is not duplicated at every level.
- Trigger/scope: on-demand knowledge angular (frontend)
- Exceptions: Project requires more.
- Why EXTRA: E2E scope guidance not in the oracle.
- Evidence K0-S000589: `output/template/.claude/skills/angular/SKILL.md:142-142` — "Useful targets: meaningful component behavior, validation, data-access request mapping, important route/auth behavior, complex reactive state — not Angular framework internals. Run the workspace's configured test runner. E2E tests cover a small number of important user workflows unless the project requires more, and the same behavior is not duplicated at every level."

### EXTRA-K0-0064
- Closest oracle policies: API-014
- Modality: DEFINITION
- Normative action: Commonly breaking: removing a used field, changing field meaning/type or required input, incompatible semantics, removing an endpoint, incompatible documented HTTP behaviour (compilation does not decide compatibility); often compatible and kept in the current version: optional response fields, new endpoints, backward-compatible optional parameters, contract-preserving internal changes; consider client generation.
- Trigger/scope: on-demand knowledge api-versioning (backend)
- Exceptions: none
- Why EXTRA: Compatibility classification not in the oracle.
- Evidence K0-S000612: `output/template/.claude/skills/api-versioning/SKILL.md:89-89` — "Commonly breaking: removing a field clients may use; changing a field's meaning or type; changing required input; incompatible resource or workflow semantics; removing an endpoint; incompatibly changing documented HTTP behavior. Whether the code compiles does not decide compatibility."
- Evidence K0-S000613: `output/template/.claude/skills/api-versioning/SKILL.md:91-91` — "Often compatible, and kept in the current version: an optional response field; a new endpoint; an optional query parameter with backward-compatible behavior; internal changes that preserve the contract. Consider client-generation behavior when OpenAPI clients are used."

### EXTRA-K0-0065
- Closest oracle policies: API-016
- Modality: DEFAULT
- Normative action: Generate separate or clearly grouped OpenAPI documents per supported version when clients need them.
- Trigger/scope: on-demand knowledge api-versioning (backend)
- Exceptions: Clients need them.
- Why EXTRA: Per-version documentation guidance not in the oracle.
- Evidence K0-S000615: `output/template/.claude/skills/api-versioning/SKILL.md:95-95` — "Generate separate or clearly grouped documents per supported version when clients need them (technique: `swagger`); the documented version matches runtime routing and Controller metadata. Versioning does not change normal HTTP semantics (`http-api`)."

### EXTRA-K0-0066
- Closest oracle policies: TST-011, API-022
- Modality: DEFAULT
- Normative action: When versions coexist test meaningful differences (version routing, version-specific shapes, deprecated version still operating, unsupported-version behaviour, consistent shared behaviour); identical behaviour needs no duplicated tests per version.
- Trigger/scope: on-demand knowledge api-versioning (backend)
- Exceptions: none
- Why EXTRA: Version-testing guidance not in the oracle.
- Evidence K0-S000617: `output/template/.claude/skills/api-versioning/SKILL.md:99-99` — "When versions coexist, test meaningful differences: version routing, version-specific response shapes, a deprecated version still operating during its support period, unsupported-version behavior, shared Application behavior staying consistent. Identical behavior needs no duplicated tests per version."

### EXTRA-K0-0067
- Closest oracle policies: API-014, ARC-010
- Modality: AVOID
- Normative action: Avoid a new API version for every implementation change and Minimal API version-group examples in a Controller project.
- Trigger/scope: on-demand knowledge api-versioning (backend)
- Exceptions: none
- Why EXTRA: No owner clause for these listed mistakes.
- Evidence K0-S000619: `output/template/.claude/skills/api-versioning/SKILL.md:103-103` — "Versioning without a compatibility requirement; Minimal API version-group examples in a Controller project; Domain models duplicated per version; an existing version changed incompatibly; a new version for every implementation change; deprecated versions removed silently; URL, header and query versioning mixed without reason."

### EXTRA-K0-0068
- Closest oracle policies: GOV-007
- Modality: MUST
- Normative action: Find what the decision touches: the register entry and its Affects list and the relevant standards, knowledge, workflows and enforcement.
- Trigger/scope: workflow architecture-decision (Reserved decisions, recording and changing accepted decisions)
- Exceptions: none
- Why EXTRA: Impact-scan step not in the oracle.
- Evidence K0-S000626: `output/template/.claude/skills/architecture-decision/SKILL.md:16-16` — "3. Find what it touches: the register entry and its **Affects** list, the relevant standards, knowledge, workflows and enforcement."

### EXTRA-K0-0069
- Closest oracle policies: GOV-007
- Modality: MUST
- Normative action: Add or update the register entry with the next free stable ID (never reusing a retired ID), a one-sentence decision, a Details-in owner and an Affects list; keep the register a summary.
- Trigger/scope: workflow architecture-decision (Reserved decisions, recording and changing accepted decisions)
- Exceptions: none
- Why EXTRA: Register-entry rules not in the oracle.
- Evidence K0-S000635: `output/template/.claude/skills/architecture-decision/SKILL.md:38-38` — "1. Add or update the register entry: next free stable ID (never reuse a retired ID), one-sentence decision, **Details in** owner, **Affects** list. Keep the register a summary, not a policy manual."

### EXTRA-K0-0070
- Closest oracle policies: GOV-007
- Modality: DEFAULT
- Normative action: When rationale, alternatives or consequences need more than the register sentence add an ADR docs/decisions/NNNN-<slug>.md and cite it in Details in.
- Trigger/scope: workflow architecture-decision (Reserved decisions, recording and changing accepted decisions)
- Exceptions: none
- Why EXTRA: ADR mechanism not in the oracle.
- Evidence K0-S000636: `output/template/.claude/skills/architecture-decision/SKILL.md:39-39` — "2. When rationale, alternatives or consequences need more than the register sentence, add an ADR `docs/decisions/NNNN-<slug>.md` (template below) and cite it in **Details in**."

### EXTRA-K0-0071
- Closest oracle policies: GOV-007
- Modality: MUST
- Normative action: Superseding: mark the old ADR 'Superseded by NNNN' and replace the register entry; never two active entries for one choice.
- Trigger/scope: workflow architecture-decision (Reserved decisions, recording and changing accepted decisions)
- Exceptions: none
- Why EXTRA: Supersession rule not in the oracle.
- Evidence K0-S000637: `output/template/.claude/skills/architecture-decision/SKILL.md:40-40` — "3. Superseding a decision: mark the old ADR `Superseded by NNNN` and replace the register entry; do not keep two active entries for one choice."

### EXTRA-K0-0072
- Closest oracle policies: GOV-007
- Modality: MUST
- Normative action: Add newly affected artifacts to Affects and remove ones that no longer depend on the decision.
- Trigger/scope: workflow architecture-decision (Reserved decisions, recording and changing accepted decisions)
- Exceptions: none
- Why EXTRA: Affects maintenance not in the oracle.
- Evidence K0-S000641: `output/template/.claude/skills/architecture-decision/SKILL.md:58-58` — "2. Add newly affected artifacts to **Affects**; remove ones that no longer depend on the decision."

### EXTRA-K0-0073
- Closest oracle policies: none
- Modality: MUST
- Normative action: Run check-instructions.cjs (root-aware) after any edit to .claude/ instruction files.
- Trigger/scope: repo/meta
- Exceptions: none
- Why EXTRA: Instruction-system checker obligation.
- Evidence K0-S000642: `output/template/.claude/skills/architecture-decision/SKILL.md:59-59` — "3. Changes to `.claude/` instruction files are instruction-system maintenance: ask the user to run `/template-maintenance` for structural changes, and run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.cjs"` after any edit."

### EXTRA-K0-0074
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: Output the pending Decision Request or the recorded outcome: register entry, ADR path, artifacts updated, checker result.
- Trigger/scope: workflow architecture-decision (Reserved decisions, recording and changing accepted decisions)
- Exceptions: none
- Why EXTRA: Workflow output contract not in the oracle.
- Evidence K0-S000644: `output/template/.claude/skills/architecture-decision/SKILL.md:63-63` — "The Decision Request (when pending) or the recorded outcome: register entry, ADR path if any, artifacts updated, checker result."

### EXTRA-K0-0075
- Closest oracle policies: API-010
- Modality: MUST
- Normative action: Follow the project's established validator invocation pattern instead of adding a second competing mechanism.
- Trigger/scope: on-demand knowledge aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: Single-invocation-mechanism rule not in the oracle.
- Evidence K0-S000665: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:116-116` — "Register validators with `FluentValidation.DependencyInjectionExtensions`, follow the project's established invocation pattern instead of adding a second competing mechanism, and avoid deprecated automatic-validation integration packages. A request can be syntactically valid and still violate an Application or Domain rule; when a rule is enforced in several layers, each layer has its own reason."

### EXTRA-K0-0076
- Closest oracle policies: API-012, RUN-013
- Modality: MUST_NOT
- Normative action: Expected outcomes such as NotFound, validation failures or rejected business operations are not logged as application errors.
- Trigger/scope: on-demand knowledge aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: Log-level rule for expected outcomes not in the oracle.
- Evidence K0-S000670: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:144-144` — "Expected outcomes such as `NotFound`, validation failures or rejected business operations are not logged as application errors. Logging technique: `logging`."
- Evidence K0-S001356: `output/template/.claude/skills/logging/SKILL.md:32-38` — "Choose levels by operational meaning: ⏎  ⏎ - **Trace/Debug** — detailed diagnostics for troubleshooting; not a safe place for sensitive data. ⏎ - **Information** — meaningful application events: a background job completed, an important business operation completed, a lifecycle event. Not every internal method call. ⏎ - **Warning** — an unexpected or degraded condition the application recovered fro …"
- Evidence K0-S001372: `output/template/.claude/skills/logging/SKILL.md:92-92` — "String interpolation in log calls; duplicate exception logging; expected outcomes logged as errors; credentials or secrets in logs; whole objects dumped without review; provider-specific APIs spread through Application code; logs used as an audit database without a dedicated audit design."
- Evidence K0-S001375: `output/template/.claude/skills/logging/SKILL.md:98-103` — ""

### EXTRA-K0-0077
- Closest oracle policies: API-009
- Modality: MUST
- Normative action: If a Result pattern is adopted use typed errors rather than string arrays.
- Trigger/scope: on-demand knowledge aspnet-error-handling (backend)
- Exceptions: Result pattern adopted.
- Why EXTRA: Typed-error requirement not in the oracle.
- Evidence K0-S000672: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:148-148` — "`Result<T>` is optional. Consider it when an operation has several expected failure modes, callers benefit from typed outcomes, exception-based control flow would otherwise be common, and the project will use it consistently. Avoid it when `null`, `bool` or a simple typed response is clear, when it wraps straightforward CRUD in noise, or when every method would return `Result<T>` without need. If  …"

### EXTRA-K0-0078
- Closest oracle policies: API-011, ARC-020
- Modality: DEFAULT
- Normative action: Using typed exceptions for selected cases must be a deliberate, consistent project-level decision.
- Trigger/scope: on-demand knowledge aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: Project-level decision requirement not in the oracle.
- Evidence K0-S000674: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:156-156` — "A project may deliberately use typed exceptions for selected cases; make that a consistent project-level decision."

### EXTRA-K0-0079
- Closest oracle policies: API-010, ARC-010
- Modality: AVOID
- Normative action: Avoid coupling validation to Minimal API endpoint filters in a Controller-based project.
- Trigger/scope: on-demand knowledge aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: No owner clause for this item.
- Evidence K0-S000676: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:160-160` — "Raw exception messages or inconsistent anonymous error objects returned to clients; Application depending on HTTP status codes; every method returning `Result<T>`; exceptions for every negative branch; swallowed exceptions; catch/log/rethrow at every layer; the same failure logged repeatedly; sensitive details in `ProblemDetails`; business rules only in request validators; validation coupled to Mi …"

### EXTRA-K0-0080
- Closest oracle policies: SEC-016, GOV-013
- Modality: DEFAULT
- Normative action: Bearer/OIDC for an SPA calling an API, cookies for server-rendered apps, Identity when the app owns local users and needs account management, external OIDC/OAuth when identity is delegated; a User entity or profile management alone does not call for Identity, and API authentication does not call for custom JWT issuance when an identity provider issues tokens.
- Trigger/scope: on-demand knowledge authentication (backend)
- Exceptions: none
- Why EXTRA: Authentication-mechanism selection guidance not in the oracle.
- Evidence K0-S000686: `output/template/.claude/skills/authentication/SKILL.md:16-21` — "- Bearer/OIDC for an SPA calling an API; ⏎ - cookies for server-rendered interactive web applications; ⏎ - ASP.NET Core Identity when the application owns local users, credentials and passwords and needs its account-management capabilities; ⏎ - an external OpenID Connect/OAuth provider when identity is delegated. ⏎  ⏎ A business entity named `User` or profile management alone does not call for Ide …"
- Evidence K0-S000713: `output/template/.claude/skills/authentication/SKILL.md:116-116` — "Custom password hashing; disabled token validation; hardcoded signing keys; authorization only in Angular; Application depending on `HttpContext`; `401` for an authenticated-but-forbidden user or `403` for missing authentication; logged tokens; scattered role/permission strings; Identity, JWT issuance or OIDC infrastructure without an actual need."

### EXTRA-K0-0081
- Closest oracle policies: SEC-006
- Modality: PREFER
- Normative action: Prefer policies for meaningful capabilities with stable constants for repeated names; roles only for a genuinely role-oriented model; a policy avoids scattered compound role strings.
- Trigger/scope: on-demand knowledge authentication (backend)
- Exceptions: none
- Why EXTRA: Policy-vs-role guidance not in the oracle.
- Evidence K0-S000695: `output/template/.claude/skills/authentication/SKILL.md:46-46` — "Prefer policies for meaningful capabilities, with stable constants for repeated policy names:"
- Evidence K0-S000697: `output/template/.claude/skills/authentication/SKILL.md:66-66` — "Roles fit a genuinely role-oriented model; when several roles or claims represent one business capability, a policy avoids scattered compound role strings."
- Evidence K0-S000713: `output/template/.claude/skills/authentication/SKILL.md:116-116` — "Custom password hashing; disabled token validation; hardcoded signing keys; authorization only in Angular; Application depending on `HttpContext`; `401` for an authenticated-but-forbidden user or `403` for missing authentication; logged tokens; scattered role/permission strings; Identity, JWT issuance or OIDC infrastructure without an actual need."

### EXTRA-K0-0082
- Closest oracle policies: SEC-005
- Modality: MUST
- Normative action: Resource-dependent permissions use ASP.NET Core resource authorization or explicit Application authorization logic.
- Trigger/scope: on-demand knowledge authentication (backend)
- Exceptions: none
- Why EXTRA: Resource-authorization technique not in the oracle.
- Evidence K0-S000699: `output/template/.claude/skills/authentication/SKILL.md:70-70` — "Some permissions depend on the resource: users editing only their own records, project members updating only their projects, administrators accessing any record. Use ASP.NET Core resource authorization or explicit Application authorization logic."
- Evidence K0-S001552: `output/template/.claude/skills/security-scan/references/scan-layers.md:99-99` — "Look for operations such as `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` where possessing an identifier could expose another user's or tenant's data. Verify ownership, tenant, permission or resource policy where required. Client-side filtering is not authorization."

### EXTRA-K0-0083
- Closest oracle policies: API-005, ARC-011
- Modality: MUST_NOT
- Normative action: Authentication/authorization middleware produces 401/403; controllers do not manufacture them.
- Trigger/scope: on-demand knowledge authentication (backend)
- Exceptions: none
- Why EXTRA: Responsibility rule not in the oracle.
- Evidence K0-S000702: `output/template/.claude/skills/authentication/SKILL.md:79-79` — "Authentication/authorization middleware produces these; controllers do not manufacture them. A deliberate `404` for some forbidden lookups hides existence when that is a consistent policy (`http-api`)."

### EXTRA-K0-0084
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Test observable authorization behaviour for important protected operations (401 unauthenticated, 403 unpermitted, success when permitted, ownership rules, intended anonymous endpoints) rather than only the presence of [Authorize].
- Trigger/scope: on-demand knowledge authentication (backend)
- Exceptions: none
- Why EXTRA: Authorization-test guidance not in the oracle.
- Evidence K0-S000711: `output/template/.claude/skills/authentication/SKILL.md:112-112` — "Test observable authorization behavior for important protected operations — unauthenticated → `401`, authenticated without permission → `403`, permitted caller → success, resource ownership rules, intended anonymous endpoints staying reachable — rather than only the presence of `[Authorize]`."

### EXTRA-K0-0085
- Closest oracle policies: WF-014, WF-008
- Modality: MUST
- Normative action: Stop when progress has clearly stalled instead of making speculative edits.
- Trigger/scope: workflow build-fix (failing build or tests)
- Exceptions: none
- Why EXTRA: Stall-stop rule not in the oracle.
- Evidence K0-S000722: `output/template/.claude/skills/build-fix/SKILL.md:17-17` — "- Preserve architecture and project conventions while fixing; stop when progress has clearly stalled instead of making speculative edits."

### EXTRA-K0-0086
- Closest oracle policies: GOV-014, FE-009
- Modality: MUST_NOT
- Normative action: For full-stack contract failures determine which contract is authoritative; do not patch both sides into inconsistent shapes merely to make both compile.
- Trigger/scope: workflow build-fix (failing build or tests)
- Exceptions: none
- Why EXTRA: Contract-authority rule not in the oracle.
- Evidence K0-S000741: `output/template/.claude/skills/build-fix/SKILL.md:85-85` — "Typical triggers: a changed response contract, endpoint path or HTTP method, nullability, enum or value semantics or authentication contract, or a generated client that no longer matches the OpenAPI document. Determine which contract is authoritative; do not patch both sides into inconsistent shapes merely to make both compile. With OpenAPI client generation: verify the backend contract, regenerat …"

### EXTRA-K0-0087
- Closest oracle policies: WF-013
- Modality: MUST_NOT
- Normative action: Do not fabricate replacement APIs from memory when they can be verified.
- Trigger/scope: workflow build-fix (failing build or tests)
- Exceptions: none
- Why EXTRA: Verification-of-APIs rule not in the oracle.
- Evidence K0-S000749: `output/template/.claude/skills/build-fix/SKILL.md:111-111` — "Inspect the installed version, distinguish compilation errors from changed runtime behavior, check official migration documentation, update obsolete API usage deliberately, and preserve architecture and behavior where the upgrade does not require change. Do not fabricate replacement APIs from memory when they can be verified, and do not perform an additional unrelated upgrade."

### EXTRA-K0-0088
- Closest oracle policies: DEP-008, GOV-014
- Modality: MUST_NOT
- Normative action: Do not change the declared SDK, Node, framework or language version because the local machine differs; report an unavailable toolchain instead of editing source to compensate.
- Trigger/scope: workflow build-fix (failing build or tests)
- Exceptions: none
- Why EXTRA: Toolchain-preservation rule not in the oracle.
- Evidence K0-S000751: `output/template/.claude/skills/build-fix/SKILL.md:115-115` — "Check whether the failure comes from source or toolchain (`dotnet --info`, `dotnet --version`, `node --version`, `npm --version`; `global.json`, target framework, Angular package versions, `package-lock.json`, CI runtime configuration). Do not change the repository's declared SDK, Node, framework or language version merely because the local machine differs; report an unavailable toolchain instead  …"

### EXTRA-K0-0089
- Closest oracle policies: WF-008, GOV-014
- Modality: MUST
- Normative action: If a fix introduces new failures that are not a legitimate dependency of the change, revert or correct it before continuing; never leave the repository knowingly worse than at the start.
- Trigger/scope: workflow build-fix (failing build or tests)
- Exceptions: none
- Why EXTRA: Regression-revert rule not in the oracle.
- Evidence K0-S000756: `output/template/.claude/skills/build-fix/SKILL.md:125-125` — "If a fix introduces new failures, decide whether they reveal a legitimate dependency of the change; otherwise revert or correct that fix before continuing. Never leave the repository knowingly worse than where the repair started. Do not clean up unrelated pre-existing failures unless they block verification of the requested repair or the user asks."

### EXTRA-K0-0090
- Closest oracle policies: RUN-007, RUN-021
- Modality: MUST
- Normative action: Define consistency semantics first (how stale data may become and how it is invalidated) before adding a cache.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: none
- Why EXTRA: Consistency-first step not in the oracle.
- Evidence K0-S000767: `output/template/.claude/skills/caching/SKILL.md:12-12` — "Define consistency semantics first — how stale data may become and how it is invalidated — and measure before adding caching purely for performance."

### EXTRA-K0-0091
- Closest oracle policies: ARC-024
- Modality: DEFAULT
- Normative action: HTTP response caching uses ASP.NET Core output caching when the whole response can safely be reused and belongs in the API layer.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: none
- Why EXTRA: Output-cache placement not in the oracle.
- Evidence K0-S000769: `output/template/.claude/skills/caching/SKILL.md:16-16` — "- **HTTP response caching** — ASP.NET Core output caching when the whole response can safely be reused; it belongs in the API layer."

### EXTRA-K0-0092
- Closest oracle policies: RUN-020
- Modality: DEFAULT
- Normative action: Centralize cache-key construction once duplicated key formats become hard to maintain.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: none
- Why EXTRA: Key-centralization guidance not in the oracle.
- Evidence K0-S000779: `output/template/.claude/skills/caching/SKILL.md:58-58` — "Infrastructure may implement it with `HybridCache`, which stays out of Application contracts (`rules/backend/caching.md`). Centralize key construction once duplicated key formats become hard to maintain."

### EXTRA-K0-0093
- Closest oracle policies: ARC-010
- Modality: DEFAULT
- Normative action: For Controllers apply the selected output-cache policy through controller/action metadata.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: none
- Why EXTRA: Controller output-cache technique not in the oracle.
- Evidence K0-S000786: `output/template/.claude/skills/caching/SKILL.md:83-83` — "For Controllers, apply the selected policy through controller/action metadata. Authenticated or user-specific responses are cached only when the key and policy isolate users and authorization context."

### EXTRA-K0-0094
- Closest oracle policies: RUN-018
- Modality: MUST
- Normative action: Decide explicitly whether a cache failure falls back to the source, fails the request or returns stale data.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: none
- Why EXTRA: Explicit cache-outage policy not in the oracle.
- Evidence K0-S000788: `output/template/.claude/skills/caching/SKILL.md:87-87` — "Application Services keep their normal repository/Unit of Work flow (`rules/backend/architecture.md` § Unit of Work) and coordinate invalidation through an abstraction when it is part of the use-case semantics. Decide explicitly whether a cache failure falls back to the source, fails the request or returns stale data."

### EXTRA-K0-0095
- Closest oracle policies: TST-003, TST-011
- Modality: DEFAULT
- Normative action: Test cache behaviour that affects observable correctness (invalidation after mutation, tenant/user key isolation, miss fallback, outage policy); framework cache internals need no tests.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: none
- Why EXTRA: Cache-test guidance not in the oracle.
- Evidence K0-S000790: `output/template/.claude/skills/caching/SKILL.md:91-91` — "Test cache behavior that affects observable correctness: stale entries invalidated after a successful mutation, tenant/user key isolation, cache-miss fallback, the intended outage policy. Framework cache internals need no tests."

### EXTRA-K0-0096
- Closest oracle policies: ARC-019, RUN-021
- Modality: AVOID
- Normative action: Avoid caching EF tracked entities across Unit of Work boundaries.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: none
- Why EXTRA: No owner clause for this item.
- Evidence K0-S000792: `output/template/.claude/skills/caching/SKILL.md:95-95` — "Caching by default without a reason; global keys for tenant/user data; indefinitely cached mutable data; cache technology in Domain; Application depending directly on `HybridCache` without a deliberate decision; caching EF tracked entities across Unit of Work boundaries; cache as authoritative persistence; Redis added merely because caching exists."
- Evidence K0-S001133: `output/template/.claude/skills/ef-core/SKILL.md:348-348` — "Loading all rows and filtering in memory; lazy loading by default; fire-and-forget EF asynchronous operations; compiled queries or raw SQL without evidence; caching tracked entities across Unit of Work boundaries."

### EXTRA-K0-0097
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: Build deployable artifacts reproducibly and keep deployment/environment configuration outside compiled artifacts where practical.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Reproducible-artifact guidance not in the oracle.
- Evidence K0-S000800: `output/template/.claude/skills/ci-cd/SKILL.md:12-12` — "Build deployable artifacts reproducibly, and keep deployment and environment configuration outside compiled artifacts where practical."

### EXTRA-K0-0098
- Closest oracle policies: WF-017, DEP-008
- Modality: MUST
- Normative action: Adapt CI action and runtime versions to the repository's supported versions.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Version-alignment rule not in the oracle.
- Evidence K0-S000811: `output/template/.claude/skills/ci-cd/SKILL.md:85-85` — "Adapt action and runtime versions to the repository's supported versions, and add frontend test/lint steps only when the project defines them."

### EXTRA-K0-0099
- Closest oracle policies: TST-004, GOV-013
- Modality: MUST
- Normative action: Provide CI services (SQL Server, PostgreSQL, Redis, brokers) only when tests require them; the generic template hardcodes no database provider.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: none
- Why EXTRA: CI-service rule not in the oracle.
- Evidence K0-S000813: `output/template/.claude/skills/ci-cd/SKILL.md:89-89` — "Provide services such as SQL Server, PostgreSQL, Redis or a message broker only when tests require them; the generic template hardcodes no database provider, and the test environment stays isolated from Development and Production data (`dotnet-testing`)."
- Evidence K0-S000827: `output/template/.claude/skills/ci-cd/SKILL.md:125-125` — "Project-specific database infrastructure in a generic pipeline; deployment secrets in YAML; different source rebuilt per environment without reason; failing tests suppressed to allow deployment; automatic production seeding or startup migrations; assumed Docker deployment; assumed frontend scripts."
- Evidence K0-S000917: `output/template/.claude/skills/delivery-pipeline/SKILL.md:21-21` — "- Provide external services (databases, caches, brokers) only when tests actually require them, isolated from Development and Production data."

### EXTRA-K0-0100
- Closest oracle policies: DEP-004, WF-007
- Modality: MUST
- Normative action: Treat dependency-audit findings according to the project's security policy; automatic dependency updates in CI need explicit adoption.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: Explicit adoption.
- Why EXTRA: Audit/auto-update policy not in the oracle.
- Evidence K0-S000816: `output/template/.claude/skills/ci-cd/SKILL.md:97-97` — "NuGet auditing also runs during restore with modern .NET SDKs. Treat findings according to the project's security policy; automatic dependency updates in CI need explicit adoption."
- Evidence K0-S000918: `output/template/.claude/skills/delivery-pipeline/SKILL.md:22-22` — "- Dependency auditing follows the project's security policy; do not enable automatic package upgrades unless the project adopted them."

### EXTRA-K0-0101
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: Store or publish only artifacts that later stages need.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Artifact-retention guidance not in the oracle.
- Evidence K0-S000819: `output/template/.claude/skills/ci-cd/SKILL.md:109-109` — "Angular artifacts come from `npm run build`. Store or publish only artifacts that later stages need. Build and publish container images from CI only when container deployment is part of the project."

### EXTRA-K0-0102
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: Where supported promote the same tested artifact or image through environments instead of recompiling per environment; environment behaviour comes from runtime configuration.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: Deployment model does not support promotion.
- Why EXTRA: Build-once-promote guidance not in the oracle.
- Evidence K0-S000821: `output/template/.claude/skills/ci-cd/SKILL.md:113-113` — "Where the deployment model supports promotion, promote the same tested artifact or image through environments instead of recompiling per environment; environment-specific behavior comes from runtime configuration."
- Evidence K0-S000827: `output/template/.claude/skills/ci-cd/SKILL.md:125-125` — "Project-specific database infrastructure in a generic pipeline; deployment secrets in YAML; different source rebuilt per environment without reason; failing tests suppressed to allow deployment; automatic production seeding or startup migrations; assumed Docker deployment; assumed frontend scripts."

### EXTRA-K0-0103
- Closest oracle policies: SEC-002
- Modality: PREFER
- Normative action: Prefer workload/federated identity over long-lived deployment credentials when the platform supports it.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Identity preference not in the oracle.
- Evidence K0-S000823: `output/template/.claude/skills/ci-cd/SKILL.md:117-117` — "Use the CI platform's secret or identity mechanism; prefer workload/federated identity over long-lived deployment credentials when the platform supports it."

### EXTRA-K0-0104
- Closest oracle policies: FE-007
- Modality: MUST_NOT
- Normative action: Do not apply backend project-boundary rules mechanically to Angular code.
- Trigger/scope: workflow code-review (reviews of completed changes)
- Exceptions: none
- Why EXTRA: Review-discipline rule not in the oracle.
- Evidence K0-S000844: `output/template/.claude/skills/code-review/SKILL.md:34-34` — "- Frontend: check against `rules/frontend/angular.md` — feature boundaries and component responsibility, HTTP behind a data-access boundary, subscription and reactive-state lifetime, frontend error handling, route guards not treated as authorization, unnecessary global state, meaningful frontend tests. Do not apply backend project-boundary rules mechanically to Angular code."

### EXTRA-K0-0105
- Closest oracle policies: WF-020
- Modality: MUST_NOT
- Normative action: Use the full security-scan only for a requested audit, a materially security-sensitive change or a finding that justifies it; do not turn every review into a full OWASP audit.
- Trigger/scope: workflow code-review (reviews of completed changes)
- Exceptions: none
- Why EXTRA: Scan-trigger limit not in the oracle.
- Evidence K0-S000847: `output/template/.claude/skills/code-review/SKILL.md:39-39` — "When relevant check commit and transaction behavior, destructive data changes, raw SQL parameterization, authorization, input trust boundaries, secrets, sensitive logging, concurrency, migrations and cache consistency against `rules/common/security.md`, `rules/backend/security.md`, `rules/backend/persistence.md` and `rules/backend/caching.md`. When a migration or model change affects seeded entiti …"
- Evidence K0-S001700: `output/template/.claude/skills/verify/SKILL.md:58-58` — "- **Dependencies and security** — for dependency changes or security-sensitive work: `dotnet package list --vulnerable --include-transitive`, `npm audit`; inspect changed code for secrets, authorization, SQL/raw query safety, CORS/TLS changes, sensitive logging and disabled certificate validation. Run the full `security-scan` only when the change warrants it."

### EXTRA-K0-0106
- Closest oracle policies: WF-011
- Modality: MUST
- Normative action: Each finding states severity, location, what is wrong, why it matters and the smallest reasonable fix; findings are ordered by severity with the Critical/High/Medium/Low definitions.
- Trigger/scope: workflow code-review (reviews of completed changes)
- Exceptions: none
- Why EXTRA: Finding format and severity scale not in the oracle.
- Evidence K0-S000857: `output/template/.claude/skills/code-review/SKILL.md:59-59` — "For each finding: severity, file/location, what is wrong, why it matters, the smallest reasonable fix. Order findings by severity:"
- Evidence K0-S000858: `output/template/.claude/skills/code-review/SKILL.md:61-64` — "- **Critical** — data loss, security vulnerability, reliably broken core behavior, or another issue that should block use or merge immediately. ⏎ - **High** — likely defect or architectural/data-integrity issue that should be fixed before merge. ⏎ - **Medium** — real maintainability, robustness or test gap worth addressing, not a likely immediate production failure. ⏎ - **Low** — non-blocking impr …"

### EXTRA-K0-0107
- Closest oracle policies: WF-012
- Modality: MUST_NOT
- Normative action: Do not add filler praise to balance criticism.
- Trigger/scope: workflow code-review (reviews of completed changes)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K0-S000859: `output/template/.claude/skills/code-review/SKILL.md:66-66` — "Do not manufacture findings to populate categories. When there are no meaningful findings, say so and name the important areas that could not be verified. Do not add filler praise to balance criticism."

### EXTRA-K0-0108
- Closest oracle policies: WF-011, WF-021
- Modality: MUST_NOT
- Normative action: Do not report formatting owned by tooling as a defect and do not assume every warning is a bug.
- Trigger/scope: workflow code-review (reviews of completed changes)
- Exceptions: none
- Why EXTRA: Tool-owned-formatting rule not in the oracle.
- Evidence K0-S000861: `output/template/.claude/skills/code-review/SKILL.md:70-70` — "Do not rewrite working code during a review unless asked; do not report formatting owned by tooling as a defect; do not demand personal style preferences; do not assume every warning is a bug; do not require patterns the project has not adopted (for example MediatR, CQRS, Vertical Slice Architecture, Minimal APIs, Rich Domain Models, Domain Events or generic repositories)."

### EXTRA-K0-0109
- Closest oracle policies: GOV-010, RUN-015
- Modality: MUST
- Normative action: Example retry counts, timeouts and limits are illustrative; choose them from the actual integration and deployment requirements.
- Trigger/scope: on-demand knowledge configuration (backend)
- Exceptions: none
- Why EXTRA: Operational-value selection rule not in the oracle.
- Evidence K0-S000871: `output/template/.claude/skills/configuration/SKILL.md:49-49` — "Numbers in examples are illustrative; choose retry counts, timeouts and limits from the actual integration and deployment requirements."
- Evidence K0-S001249: `output/template/.claude/skills/httpclient-factory/references/resilience.md:23-23` — "Distinguish attempt timeout from total operation timeout, especially with retries enabled. Choose values from actual latency requirements, not from examples."

### EXTRA-K0-0110
- Closest oracle policies: GOV-011, GOV-008
- Modality: MUST_NOT
- Normative action: Do not record framework defaults the project has not intentionally overridden.
- Trigger/scope: workflow custom-settings (CUSTOM_SETTINGS.md value added, changed, removed or applied)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K0-S000896: `output/template/.claude/skills/custom-settings/SKILL.md:16-16` — "3. Record the setting with a stable descriptive name and its purpose. Do not record framework defaults the project has not intentionally overridden."

### EXTRA-K0-0111
- Closest oracle policies: GOV-021
- Modality: PREFER
- Normative action: Prefer one normal source in code or configuration over the same literal duplicated across layers.
- Trigger/scope: workflow custom-settings (CUSTOM_SETTINGS.md value added, changed, removed or applied)
- Exceptions: none
- Why EXTRA: Single-source preference not in the oracle.
- Evidence K0-S000900: `output/template/.claude/skills/custom-settings/SKILL.md:24-24` — "Update every affected implementation, validation, configuration, test, documentation and mirrored frontend/backend surface. Prefer one normal source in code or configuration over the same literal duplicated across layers. Where frontend and backend expose the same constraint, backend validation stays authoritative and frontend validation and messages follow it for user experience (`rules/frontend/ …"

### EXTRA-K0-0112
- Closest oracle policies: GOV-013, WF-001
- Modality: MUST
- Normative action: Inspect what exists before writing a pipeline (backend, frontend, tests, Dockerfiles, provider-specific tests, generated clients, artifacts); do not assume PostgreSQL, Redis, Docker or frontend tooling; add stages for the actual project, not generic boilerplate.
- Trigger/scope: workflow delivery-pipeline (CI/CD, containers, deployment, production migrations)
- Exceptions: none
- Why EXTRA: Discovery rule not in the oracle.
- Evidence K0-S000912: `output/template/.claude/skills/delivery-pipeline/SKILL.md:14-14` — "Inspect what actually exists before writing anything: .NET backend, Angular frontend, test projects, Dockerfiles, provider-specific integration tests, generated clients, deployment artifacts. Do not assume PostgreSQL, Redis, Docker or frontend tooling exists; add stages for the actual project, not generic boilerplate. Introduce Docker or container publishing only when the project has adopted conta …"

### EXTRA-K0-0113
- Closest oracle policies: WF-019
- Modality: MUST
- Normative action: The production migration step fails visibly.
- Trigger/scope: workflow delivery-pipeline (CI/CD, containers, deployment, production migrations)
- Exceptions: none
- Why EXTRA: Visibility requirement not in the oracle.
- Evidence K0-S000920: `output/template/.claude/skills/delivery-pipeline/SKILL.md:26-26` — "- Do not apply production database migrations automatically from normal application startup by default. A production migration is an explicit deployment operation: a dedicated step at a controlled point of the deployment, using the project's approved credentials, failing visibly. Migration scripts or bundles may be generated earlier in CI and executed during deployment."

### EXTRA-K0-0114
- Closest oracle policies: WF-017
- Modality: MUST
- Normative action: Keep CI and CD separable; a green CI build does not mean every branch deploys.
- Trigger/scope: workflow delivery-pipeline (CI/CD, containers, deployment, production migrations)
- Exceptions: none
- Why EXTRA: CI/CD separation not in the oracle.
- Evidence K0-S000923: `output/template/.claude/skills/delivery-pipeline/SKILL.md:31-31` — "Keep CI and CD separable; a green CI build does not mean every branch deploys. Use the platform's secret or workload-identity mechanism — never real secrets in pipeline YAML, Dockerfiles, committed Compose files or image build arguments. Use environment protection or approvals where the hosting platform supports them."

### EXTRA-K0-0115
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Use environment protection or approvals where the hosting platform supports them.
- Trigger/scope: delivery
- Exceptions: Platform support.
- Why EXTRA: Deployment-protection guidance not in the oracle.
- Evidence K0-S000923: `output/template/.claude/skills/delivery-pipeline/SKILL.md:31-31` — "Keep CI and CD separable; a green CI build does not mean every branch deploys. Use the platform's secret or workload-identity mechanism — never real secrets in pipeline YAML, Dockerfiles, committed Compose files or image build arguments. Use environment protection or approvals where the hosting platform supports them."

### EXTRA-K0-0116
- Closest oracle policies: WF-003, WF-006
- Modality: MUST
- Normative action: Verify the pipeline restores from a clean environment, builds backend and frontend, runs configured tests, does not depend on developer-machine state, exposes no secrets and produces expected artifacts; for container changes build the image, start the app and check port/configuration, non-root execution and health-probe integration.
- Trigger/scope: workflow delivery-pipeline (CI/CD, containers, deployment, production migrations)
- Exceptions: none
- Why EXTRA: Pipeline-verification checklist not in the oracle.
- Evidence K0-S000925: `output/template/.claude/skills/delivery-pipeline/SKILL.md:35-35` — "Confirm that it restores from a clean environment, builds the backend, builds the frontend when present, runs the configured tests, does not depend on developer-machine state, does not expose secrets and produces the expected artifacts. For container changes also build the image, start the application, and check port/configuration, non-root execution and health-probe integration."

### EXTRA-K0-0117
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Report files changed, stages and their commands, what was verified and unconfirmed hosting assumptions.
- Trigger/scope: workflow delivery-pipeline (CI/CD, containers, deployment, production migrations)
- Exceptions: none
- Why EXTRA: Workflow output contract not in the oracle.
- Evidence K0-S000927: `output/template/.claude/skills/delivery-pipeline/SKILL.md:39-39` — "Files changed, stages and the commands they run, what was verified, and any assumption about the hosting platform that still needs confirmation."

### EXTRA-K0-0118
- Closest oracle policies: ARC-021, ARC-023, GOV-012
- Modality: PREFER
- Normative action: Interface-to-implementation registration at architectural boundaries, concrete registration for implementation-only helpers; prefer explicit registration in small and medium applications; keyed services, factories, decorators and scanning only for actual composition problems.
- Trigger/scope: on-demand knowledge dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Registration-shape guidance not in the oracle.
- Evidence K0-S000933: `output/template/.claude/skills/dependency-injection/SKILL.md:14-14` — "Application services, repositories and external adapters use interface-to-implementation registration at architectural boundaries; implementation-only helpers can be registered concretely. Prefer explicit registration in small and medium applications — keyed services, factories, decorators and convention scanning solve actual composition problems."

### EXTRA-K0-0119
- Closest oracle policies: GOV-012
- Modality: DEFAULT
- Normative action: Keyed services for several implementations of one abstraction selected by a known key, not when a single registration or simple factory is clearer.
- Trigger/scope: on-demand knowledge dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Keyed-service guidance not in the oracle.
- Evidence K0-S000936: `output/template/.claude/skills/dependency-injection/SKILL.md:56-56` — "For several implementations of one abstraction selected by a known key — not when a single registration or simple factory is clearer:"
- Evidence K0-S000956: `output/template/.claude/skills/dependency-injection/SKILL.md:173-181` — ""
- Evidence K0-S001288: `output/template/.claude/skills/httpclient-factory/SKILL.md:55-55` — ""

### EXTRA-K0-0120
- Closest oracle policies: DEP-001, GOV-013
- Modality: MUST_NOT
- Normative action: Scrutor is not added for a single decoration when normal composition is simpler.
- Trigger/scope: on-demand knowledge dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Concrete package guidance not in the oracle.
- Evidence K0-S000943: `output/template/.claude/skills/dependency-injection/SKILL.md:110-110` — "Scrutor is not worth adding for a single decoration when normal composition is simpler."

### EXTRA-K0-0121
- Closest oracle policies: GOV-012, ARC-023
- Modality: DEFAULT
- Normative action: Use assembly scanning only when registration volume creates genuine repetitive boilerplate, scanning the assembly that owns the services.
- Trigger/scope: on-demand knowledge dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Scanning guidance not in the oracle.
- Evidence K0-S000945: `output/template/.claude/skills/dependency-injection/SKILL.md:114-114` — "Use assembly scanning when registration volume creates genuine repetitive boilerplate, and scan the assembly that owns the services (not accidentally only the API assembly):"
- Evidence K0-S000956: `output/template/.claude/skills/dependency-injection/SKILL.md:173-181` — ""

### EXTRA-K0-0122
- Closest oracle policies: PST-008, PST-010
- Modality: MUST
- Normative action: Review the seeder together with any migration that affects seeded entities.
- Trigger/scope: workflow development-workflow (planning or implementing non-trivial changes)
- Exceptions: none
- Why EXTRA: Joint-review step not in the oracle.
- Evidence K0-S000979: `output/template/.claude/skills/development-workflow/SKILL.md:58-58` — "- Treat EF Core migrations as source code: review every generated migration before committing it, paying particular attention to destructive schema changes, unexpected column recreation, data migrations, indexes, foreign keys and delete behavior. Review the seeder together with any migration that affects seeded entities."

### EXTRA-K0-0123
- Closest oracle policies: WF-009, GOV-017
- Modality: MUST
- Normative action: Report what changed and why, Delegated decisions taken, Decision Requests raised or unresolved, and the verification report.
- Trigger/scope: workflow development-workflow (planning or implementing non-trivial changes)
- Exceptions: none
- Why EXTRA: Workflow output contract (Delegated decisions reporting) not in the oracle.
- Evidence K0-S000990: `output/template/.claude/skills/development-workflow/SKILL.md:81-81` — "- What changed and why; Delegated decisions taken; Decision Requests raised or still unresolved; the verification report (see also: `verify` § Report)."

### EXTRA-K0-0124
- Closest oracle policies: DEP-018, SEC-002
- Modality: DEFAULT
- Normative action: Keep configuration external (environment-specific values passed at runtime), images reproducible and Docker concerns out of the application architecture; prefer the deployment platform's health-probe capabilities.
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Container design principles not in the oracle.
- Evidence K0-S000995: `output/template/.claude/skills/docker/SKILL.md:12-12` — "Keep build tooling out of production runtime images, configuration external, images reproducible and Docker concerns out of the application architecture; prefer the deployment platform's health-probe capabilities."
- Evidence K0-S001005: `output/template/.claude/skills/docker/SKILL.md:63-63` — "Pass environment-specific configuration at runtime:"
- Evidence K0-S001024: `output/template/.claude/skills/docker/SKILL.md:124-124` — "SDK image as production runtime; root execution without reason; secrets baked into images; arbitrary infrastructure in Compose; assuming `curl`/`wget` exist; production migrations at application startup (see also: `delivery-pipeline` § 3); specialized image variants without compatibility checks; Docker concerns leaking into Domain/Application code."

### EXTRA-K0-0125
- Closest oracle policies: DEP-023
- Modality: MUST
- Normative action: Copy only the repository-level build files that exist and restore needs, and copy project files explicitly (no wildcard tricks that flatten the multi-project structure).
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Dockerfile copy rule not in the oracle.
- Evidence K0-S000999: `output/template/.claude/skills/docker/SKILL.md:51-51` — "Copy only the repository-level build files that exist and restore needs, and copy project files explicitly — wildcard tricks can flatten or rearrange the multi-project structure. Use the .NET runtime image (not `aspnet`) for workers that do not need ASP.NET Core."

### EXTRA-K0-0126
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Copy project and build files before the full source to keep the restore layer cached; update the project-copy section when the solution structure changes; a correct restore graph matters more than caching.
- Trigger/scope: delivery
- Exceptions: none
- Why EXTRA: Restore-layer technique not in the oracle.
- Evidence K0-S001001: `output/template/.claude/skills/docker/SKILL.md:55-55` — "Copy project and build files before the full source so source changes do not invalidate the NuGet restore layer. When the solution structure changes, update the project-copy section; a correct restore graph matters more than layer caching."

### EXTRA-K0-0127
- Closest oracle policies: GOV-013, DEP-018
- Modality: MUST
- Normative action: Add only the Compose infrastructure the project actually uses, not PostgreSQL, Redis or RabbitMQ because they appear in examples.
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Compose-scope rule not in the oracle.
- Evidence K0-S001011: `output/template/.claude/skills/docker/SKILL.md:90-90` — "Add only the infrastructure the project actually uses — not PostgreSQL, Redis or RabbitMQ because they are common in examples — and keep local passwords in an ignored `.env` or similar developer configuration."
- Evidence K0-S001024: `output/template/.claude/skills/docker/SKILL.md:124-124` — "SDK image as production runtime; root execution without reason; secrets baked into images; arbitrary infrastructure in Compose; assuming `curl`/`wget` exist; production migrations at application startup (see also: `delivery-pipeline` § 3); specialized image variants without compatibility checks; Docker concerns leaking into Domain/Application code."

### EXTRA-K0-0128
- Closest oracle policies: API-019
- Modality: DEFAULT
- Normative action: Expose liveness/readiness through ASP.NET Core health checks and prefer the orchestrator's native HTTP probes; if Compose runs an in-container health command verify the executable exists or add a deliberate probe mechanism, weighing debugging packages in production images.
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Probe technique not in the oracle.
- Evidence K0-S001013: `output/template/.claude/skills/docker/SKILL.md:94-94` — "Expose liveness/readiness through ASP.NET Core health checks (`health-check`) and prefer the orchestrator's native HTTP probes. Runtime images may lack `curl`, `wget` or a shell: if Compose itself runs an in-container health command, verify the executable exists or add a deliberate probe mechanism, weighing the cost of debugging packages in a production image."
- Evidence K0-S001024: `output/template/.claude/skills/docker/SKILL.md:124-124` — "SDK image as production runtime; root execution without reason; secrets baked into images; arbitrary infrastructure in Compose; assuming `curl`/`wget` exist; production migrations at application startup (see also: `delivery-pipeline` § 3); specialized image variants without compatibility checks; Docker concerns leaking into Domain/Application code."

### EXTRA-K0-0129
- Closest oracle policies: DEP-018
- Modality: DEFAULT
- Normative action: Build static Angular in a Node stage and serve assets with the chosen hosting strategy (Nginx not mandatory); keep API base URLs and environment configuration compatible with that strategy.
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Angular container guidance not in the oracle.
- Evidence K0-S001015: `output/template/.claude/skills/docker/SKILL.md:98-98` — "For a static Angular deployment, build in a Node stage and serve the generated assets with the chosen hosting strategy; Nginx is not mandatory when the platform hosts static files. Keep API base URLs and environment configuration compatible with that strategy."

### EXTRA-K0-0130
- Closest oracle policies: none
- Modality: MUST
- Normative action: Keep files required by restore/build in the build context, and tests when the image build intentionally runs them.
- Trigger/scope: delivery
- Exceptions: none
- Why EXTRA: .dockerignore rule not in the oracle.
- Evidence K0-S001018: `output/template/.claude/skills/docker/SKILL.md:112-112` — "Keep files required by restore/build, and keep tests when the image build intentionally runs them."

### EXTRA-K0-0131
- Closest oracle policies: RUN-008, GOV-013
- Modality: DEFAULT
- Normative action: Start from standard supported .NET images; Alpine, chiseled, trimming or Native AOT only when compatibility and deployment requirements justify them, verifying globalization, native dependencies, reflection and diagnostics.
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Image-variant guidance not in the oracle.
- Evidence K0-S001020: `output/template/.claude/skills/docker/SKILL.md:116-116` — "Start from standard supported .NET images. Alpine, chiseled images, trimming or Native AOT come in only when compatibility and deployment requirements justify them — verify globalization, native dependencies, reflection and diagnostics when using them."
- Evidence K0-S001024: `output/template/.claude/skills/docker/SKILL.md:124-124` — "SDK image as production runtime; root execution without reason; secrets baked into images; arbitrary infrastructure in Compose; assuming `curl`/`wget` exist; production migrations at application startup (see also: `delivery-pipeline` § 3); specialized image variants without compatibility checks; Docker concerns leaking into Domain/Application code."

### EXTRA-K0-0132
- Closest oracle policies: WF-006, SEC-001
- Modality: MUST
- Normative action: Build the image; verify startup, port and configuration, non-root behaviour and health-probe integration; review the image for accidental secrets or files; run meaningful tests outside the image or in the pipeline.
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Container verification checklist not in the oracle.
- Evidence K0-S001022: `output/template/.claude/skills/docker/SKILL.md:120-120` — "Build the image; verify application startup, required port and configuration, non-root behavior when relevant and health-probe integration; review the image for accidental secrets or files. Run meaningful application tests outside the image or as part of the build pipeline."

### EXTRA-K0-0133
- Closest oracle policies: GOV-012, TST-011
- Modality: DEFAULT
- Normative action: Test the risks that matter and build test infrastructure only for a concrete testing need; a small project does not need an enterprise harness.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Test-infrastructure proportionality not in the oracle.
- Evidence K0-S001029: `output/template/.claude/skills/dotnet-testing/SKILL.md:12-12` — "Test the risks that matter for the current project, and build test infrastructure only for a concrete testing need — a small project does not need an enterprise-sized harness."

### EXTRA-K0-0134
- Closest oracle policies: TST-003
- Modality: PREFER
- Normative action: Prefer one observable scenario per test; multi-step tests when the sequence itself is the scenario.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Scenario-granularity guidance not in the oracle.
- Evidence K0-S001036: `output/template/.claude/skills/dotnet-testing/SKILL.md:60-60` — "A longer explicit table beats a shorter algorithmic test when it makes the business rules visible. Prefer one observable scenario per test; multi-step tests fit when the sequence itself is the scenario (a whole workflow, a replace-set lifecycle)."

### EXTRA-K0-0135
- Closest oracle policies: TST-002, TST-003
- Modality: DEFAULT
- Normative action: Unit-test candidates: domain behaviour owned by Domain, calculations, state transitions, validation, Application orchestration with simple fakes; mock architectural boundaries when it clarifies, never every collaborator mechanically, and do not forbid mocking project-owned abstractions.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Mocking guidance not in the oracle.
- Evidence K0-S001038: `output/template/.claude/skills/dotnet-testing/SKILL.md:64-64` — "Good candidates: non-trivial domain behavior that genuinely belongs to Domain, calculations, workflow/state transitions at the owning layer, validation logic, Application orchestration with simple fakes or mocks. Mock or fake architectural boundaries when that clarifies the behavior; do not mock every collaborator mechanically, and do not forbid mocking project-owned abstractions when isolation he …"
- Evidence K0-S001068: `output/template/.claude/skills/dotnet-testing/SKILL.md:177-177` — "Testing private details; mocking every class; hitting production resources; shared mutable state; assertions that repeat the implementation; assertion-free tests (unless the behavior is "does not throw"); `Task.Delay` to make timing-sensitive tests pass; Testcontainers without a provider-fidelity need; EF InMemory while claiming relational coverage."

### EXTRA-K0-0136
- Closest oracle policies: TST-007
- Modality: MUST
- Normative action: When provider fidelity does not matter a lighter isolated relational database may be used, stating the trade-off.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Trade-off statement not in the oracle.
- Evidence K0-S001046: `output/template/.claude/skills/dotnet-testing/SKILL.md:121-121` — "Provider fidelity matters for provider-specific SQL, constraints, transactions, locking and concurrency, indexes, raw SQL, provider-specific mappings and migrations — use the actual provider; Testcontainers is a good option for an isolated real database. When provider fidelity does not matter (primarily application/API integration), a lighter isolated relational database may be acceptable — state  …"

### EXTRA-K0-0137
- Closest oracle policies: TST-002
- Modality: DEFAULT
- Normative action: Test repository implementations or EF mappings when there is meaningful persistence behaviour (custom mappings, filters, projections, non-trivial queries, relationships, concurrency, provider behaviour).
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Persistence-test targeting not in the oracle.
- Evidence K0-S001050: `output/template/.claude/skills/dotnet-testing/SKILL.md:129-129` — "Test repository implementations or EF mappings when there is meaningful persistence behavior: custom mappings, query filters, projections, non-trivial queries, relationships, concurrency, provider-specific behavior. One test per trivial `Add`/`Get` method adds coverage numbers, not value."

### EXTRA-K0-0138
- Closest oracle policies: TST-004
- Modality: DEFAULT
- Normative action: Keep slow or unreliable external-system tests separate from ordinary fast runs.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Test-separation guidance not in the oracle.
- Evidence K0-S001054: `output/template/.claude/skills/dotnet-testing/SKILL.md:145-145` — "At the relevant boundary use a fake or mock abstraction (unit tests), a stub `HttpMessageHandler`, WireMock or another local fake server (HTTP integration), or a dedicated sandbox only when the test explicitly targets that integration. Keep slow or unreliable external-system tests separate from ordinary fast runs."

### EXTRA-K0-0139
- Closest oracle policies: TST-008, GOV-012
- Modality: DEFAULT
- Normative action: Keep test data explicit and minimal; builders/fixtures only when repeated setup becomes hard to read; no generic test-data framework for a few objects.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Test-data guidance not in the oracle.
- Evidence K0-S001056: `output/template/.claude/skills/dotnet-testing/SKILL.md:149-149` — "Keep test data explicit and minimal. Introduce builders, fixtures or factories when repeated setup becomes hard to read — not a generic test-data framework for a few simple objects."

### EXTRA-K0-0140
- Closest oracle policies: WF-006
- Modality: DEFINITION
- Normative action: A smoke test is a small set of fast checks that a built or deployed application is basically operational, not every integration test.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Definition not in the oracle.
- Evidence K0-S001064: `output/template/.claude/skills/dotnet-testing/SKILL.md:169-169` — ""Smoke test" means a small set of fast checks that a built or deployed application is basically operational — not a synonym for every integration test."
- Evidence K0-S001071: `output/template/.claude/skills/dotnet-testing/SKILL.md:183-192` — ""

### EXTRA-K0-0141
- Closest oracle policies: TST-003, DEP-001
- Modality: DEFAULT
- Normative action: Snapshot testing only for large stable outputs; small or important contracts use explicit assertions; a snapshot library is not added by default.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Snapshot guidance not in the oracle.
- Evidence K0-S001066: `output/template/.claude/skills/dotnet-testing/SKILL.md:173-173` — "Coverage is diagnostic information, not a target; prioritize meaningful behavior, important edge cases and risky integrations. Snapshot testing can help for large stable outputs where explicit assertions get noisy; small or important response contracts read better with explicit assertions, and a snapshot library is not added by default."

### EXTRA-K0-0142
- Closest oracle policies: TST-003
- Modality: AVOID
- Normative action: Avoid assertion-free tests unless the behaviour is 'does not throw'.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: No owner clause for this item.
- Evidence K0-S001068: `output/template/.claude/skills/dotnet-testing/SKILL.md:177-177` — "Testing private details; mocking every class; hitting production resources; shared mutable state; assertions that repeat the implementation; assertion-free tests (unless the behavior is "does not throw"); `Task.Delay` to make timing-sensitive tests pass; Testcontainers without a provider-fidelity need; EF InMemory while claiming relational coverage."

### EXTRA-K0-0143
- Closest oracle policies: ARC-019
- Modality: DEFAULT
- Normative action: Keep entity configuration in IEntityTypeConfiguration<T> classes.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Configuration-class convention not in the oracle.
- Evidence K0-S001079: `output/template/.claude/skills/ef-core/SKILL.md:18-18` — "Keep entity configuration in `IEntityTypeConfiguration<T>` classes and persistence-specific configuration out of Domain entities where practical."

### EXTRA-K0-0144
- Closest oracle policies: RUN-006
- Modality: DEFAULT
- Normative action: Use tracking queries when loaded entities will be modified and committed through the current Unit of Work and AsNoTracking() for read-only entity queries where tracking adds nothing; projections need no AsNoTracking().
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Tracking technique not in the oracle.
- Evidence K0-S001096: `output/template/.claude/skills/ef-core/SKILL.md:163-163` — "Use tracking queries when loaded entities will be modified and committed through the current Unit of Work, and `AsNoTracking()` for read-only entity queries where tracking adds nothing. Projections to non-entity DTOs do not need `AsNoTracking()`."
- Evidence K0-S001136: `output/template/.claude/skills/ef-core/SKILL.md:354-365` — ""

### EXTRA-K0-0145
- Closest oracle policies: RUN-006
- Modality: DEFAULT
- Normative action: Make the query shape explicit (projection for selected related data, Include/ThenInclude when the graph is required); for large collection includes consider split queries and check SQL and performance.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Query-shape guidance not in the oracle.
- Evidence K0-S001100: `output/template/.claude/skills/ef-core/SKILL.md:179-179` — "Make the query shape explicit: projection for selected related data, `Include`/`ThenInclude` when the entity graph itself is required. Avoid lazy loading by default — it hides database access and invites N+1 queries. For large collection includes consider split queries and check the generated SQL and performance."

### EXTRA-K0-0146
- Closest oracle policies: RUN-006
- Modality: MUST
- Normative action: Pagination uses deterministic ordering.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Ordering requirement not in the oracle.
- Evidence K0-S001102: `output/template/.claude/skills/ef-core/SKILL.md:183-183` — "Filter, order and paginate in the database, with deterministic ordering:"

### EXTRA-K0-0147
- Closest oracle policies: ARC-016, ARC-019
- Modality: MUST_NOT
- Normative action: ExecuteUpdateAsync/ExecuteDeleteAsync bypass change tracking: do not mix them casually with tracked entities for the same rows and understand their transaction and consistency implications.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Bulk-operation rule not in the oracle.
- Evidence K0-S001107: `output/template/.claude/skills/ef-core/SKILL.md:212-212` — "`ExecuteUpdateAsync`/`ExecuteDeleteAsync` run directly against the database and bypass change tracking: do not mix them casually with tracked entities for the same rows, and understand their transaction and consistency implications."
- Evidence K0-S001136: `output/template/.claude/skills/ef-core/SKILL.md:354-365` — ""

### EXTRA-K0-0148
- Closest oracle policies: ARC-019, FE-008
- Modality: MUST_NOT
- Normative action: EF Core interceptors fit infrastructure-level cross-cutting behaviour with a clear benefit (e.g. auditing); business behaviour does not belong in them.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: EF interceptor rule not in the oracle.
- Evidence K0-S001113: `output/template/.claude/skills/ef-core/SKILL.md:224-224` — "Interceptors fit infrastructure-level cross-cutting behavior with a clear benefit, such as auditing; business behavior does not belong in them."

### EXTRA-K0-0149
- Closest oracle policies: GOV-003, PST-001
- Modality: MUST
- Normative action: When the required entity graph or scenarios are complex, ask for the desired dataset in the task requirements instead of inventing a large generic object graph.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Dataset-request rule not in the oracle.
- Evidence K0-S001123: `output/template/.claude/skills/ef-core/SKILL.md:326-326` — "Representative states to cover where applicable: newly created; active or in progress; completed; inactive or archived; with and without optional values; with and without optional relationships; representative status values; meaningful boundary states. Do not attempt every combination. When the required entity graph or scenarios are complex, ask for the desired dataset in the task requirements ins …"

### EXTRA-K0-0150
- Closest oracle policies: ARC-019
- Modality: DEFAULT
- Normative action: Create migrations from the Infrastructure project with the API project as startup project.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Migration-project convention not in the oracle.
- Evidence K0-S001125: `output/template/.claude/skills/ef-core/SKILL.md:330-330` — "Create migrations from the Infrastructure project with the API project as startup project:"

### EXTRA-K0-0151
- Closest oracle policies: RUN-002
- Modality: AVOID
- Normative action: Avoid fire-and-forget EF Core asynchronous operations.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: No owner clause for this item.
- Evidence K0-S001133: `output/template/.claude/skills/ef-core/SKILL.md:348-348` — "Loading all rows and filtering in memory; lazy loading by default; fire-and-forget EF asynchronous operations; compiled queries or raw SQL without evidence; caching tracked entities across Unit of Work boundaries."

### EXTRA-K0-0152
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Follow the repository's branch-naming convention (feature/, fix/, refactor/, test/, docs/, chore/ prefixes as defaults); do not rename an existing user branch to satisfy a convention.
- Trigger/scope: workflow git-workflow (any Git operation)
- Exceptions: none
- Why EXTRA: Branch-naming convention not in the oracle.
- Evidence K0-S001149: `output/template/.claude/skills/git-workflow/SKILL.md:31-31` — "Follow the repository's branch-naming convention. Without one, prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, `chore/` with meaningful names are reasonable defaults. Do not rename an existing user branch to satisfy a convention."

### EXTRA-K0-0153
- Closest oracle policies: GOV-016
- Modality: MUST
- Normative action: Keep each worktree focused on its branch's concern; one branch is not checked out in several normal worktrees at once.
- Trigger/scope: workflow git-workflow (any Git operation)
- Exceptions: none
- Why EXTRA: Worktree discipline not in the oracle.
- Evidence K0-S001151: `output/template/.claude/skills/git-workflow/SKILL.md:35-35` — "- Keep each worktree focused on its branch's concern; one branch is not checked out in several normal worktrees at once."

### EXTRA-K0-0154
- Closest oracle policies: WF-022
- Modality: PREFER
- Normative action: Prefer one logical change per commit with its tests; no artificial tiny commits or combined unrelated fixes and refactors.
- Trigger/scope: workflow git-workflow (any Git operation)
- Exceptions: none
- Why EXTRA: Commit-granularity guidance not in the oracle.
- Evidence K0-S001154: `output/template/.claude/skills/git-workflow/SKILL.md:40-40` — "- Prefer one logical change per commit; implementation and the tests that protect it belong together. Do not create artificial tiny commits or combine unrelated fixes and refactors."

### EXTRA-K0-0155
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Follow the repository's commit-message convention (Conventional Commits as default); use the body when motivation, constraints or migration information would otherwise be lost; do not narrate obvious diff details.
- Trigger/scope: workflow git-workflow (any Git operation)
- Exceptions: none
- Why EXTRA: Commit-message convention not in the oracle.
- Evidence K0-S001155: `output/template/.claude/skills/git-workflow/SKILL.md:41-41` — "- Follow the repository's commit-message convention. Without one, Conventional Commits are a useful default:"
- Evidence K0-S001157: `output/template/.claude/skills/git-workflow/SKILL.md:52-52` — "Use the body when important motivation, constraints or migration information would otherwise be lost; do not narrate obvious diff details."

### EXTRA-K0-0156
- Closest oracle policies: GOV-020, WF-003
- Modality: MUST
- Normative action: Before pushing confirm the intended branch and understood working/staged state, ensure relevant verification completed and avoid pushing unrelated local commits.
- Trigger/scope: workflow git-workflow (any Git operation)
- Exceptions: none
- Why EXTRA: Push checklist not in the oracle.
- Evidence K0-S001159: `output/template/.claude/skills/git-workflow/SKILL.md:56-59` — "1. Confirm the intended branch. ⏎ 2. Confirm the working and staged state is understood. ⏎ 3. Ensure relevant verification has completed. ⏎ 4. Avoid pushing unrelated local commits accidentally."

### EXTRA-K0-0157
- Closest oracle policies: GOV-015
- Modality: MUST_NOT
- Normative action: Treat main, master and other protected or shared branches as non-rewritable.
- Trigger/scope: workflow git-workflow (any Git operation)
- Exceptions: none
- Why EXTRA: Protected-branch rule not in the oracle.
- Evidence K0-S001160: `output/template/.claude/skills/git-workflow/SKILL.md:61-61` — "Never force-push a shared branch unless the user explicitly requests history rewriting and the consequences are understood; treat `main`, `master` and other protected or shared branches as non-rewritable."

### EXTRA-K0-0158
- Closest oracle policies: none
- Modality: MUST
- Normative action: Follow the repository/team convention or the user's explicit request for merge vs rebase; resolve conflicts from the intended combined behaviour (not mechanically ours/theirs) and run relevant verification afterwards.
- Trigger/scope: workflow git-workflow (any Git operation)
- Exceptions: none
- Why EXTRA: Merge practice not in the oracle.
- Evidence K0-S001162: `output/template/.claude/skills/git-workflow/SKILL.md:65-65` — "Follow the repository/team convention or the user's explicit request rather than personal preference. Inspect local uncommitted work first; do not automatically stash, reset or discard work to make the operation proceed. Resolve conflicts from the intended combined behavior, not by mechanically choosing "ours" or "theirs", and run relevant verification afterwards."

### EXTRA-K0-0159
- Closest oracle policies: WF-003, GOV-014
- Modality: MUST
- Normative action: Run verify before preparing a PR; a PR has one focused purpose without unrelated changes and describes what changed, why, how it was verified and compatibility/migration notes.
- Trigger/scope: workflow git-workflow (any Git operation)
- Exceptions: none
- Why EXTRA: PR practice not in the oracle.
- Evidence K0-S001164: `output/template/.claude/skills/git-workflow/SKILL.md:69-69` — "Run `verify` before preparing a PR. A PR has one focused purpose without accidental unrelated changes. Describe what changed, why, how it was verified and any compatibility or migration notes; never claim checks that were not run."

### EXTRA-K0-0160
- Closest oracle policies: WF-009
- Modality: DEFAULT
- Normative action: After Git operations report the resulting state when useful (branch, commit, push target, PR status, remaining uncommitted changes).
- Trigger/scope: workflow git-workflow (any Git operation)
- Exceptions: none
- Why EXTRA: Git report contract not in the oracle.
- Evidence K0-S001168: `output/template/.claude/skills/git-workflow/SKILL.md:77-77` — "After Git operations report the resulting state when useful: branch, commit created, push target, PR preparation status, uncommitted changes that remain."

### EXTRA-K0-0161
- Closest oracle policies: API-019
- Modality: AVOID
- Normative action: Avoid readiness chains (service A → B → C) without understanding their operational consequences.
- Trigger/scope: on-demand knowledge health-check (backend)
- Exceptions: none
- Why EXTRA: Readiness-chain guidance not in the oracle.
- Evidence K0-S001184: `output/template/.claude/skills/health-check/SKILL.md:60-60` — "A database check is a lightweight connectivity/availability check (`rules/backend/hosting.md` § Health checks); provider integrations help. Check an external dependency only when its availability defines readiness, prefer a lightweight check of the needed capability, and avoid readiness chains (service A → B → C) without understanding their operational consequences."
- Evidence K0-S001194: `output/template/.claude/skills/health-check/SKILL.md:80-80` — "Health checks as a code-quality grading system; database writes or business transactions from probes; every dependency on liveness; expensive queries; secrets or stack traces in payloads; remote dependency chains without operational justification."

### EXTRA-K0-0162
- Closest oracle policies: API-019, API-003
- Modality: MUST
- Normative action: Health endpoints return success when healthy and non-success when unhealthy under the probe policy (HealthCheckOptions mapping); business API status semantics do not transfer mechanically to probes.
- Trigger/scope: on-demand knowledge health-check (backend)
- Exceptions: none
- Why EXTRA: Probe status mapping not in the oracle.
- Evidence K0-S001186: `output/template/.claude/skills/health-check/SKILL.md:64-64` — "Health endpoints return success when healthy and a non-success status when unhealthy under the probe policy; `HealthCheckOptions` maps statuses. Business API status semantics do not transfer mechanically to orchestrator probes. Keep probe responses small; operator-level diagnostic detail goes behind network or authorization controls appropriate to the environment."

### EXTRA-K0-0163
- Closest oracle policies: SEC-006
- Modality: DEFAULT
- Normative action: Probes are usually reachable by infrastructure without user authentication via private networks, a management port, host restrictions or authorization when supported.
- Trigger/scope: on-demand knowledge health-check (backend)
- Exceptions: none
- Why EXTRA: Probe exposure options not in the oracle.
- Evidence K0-S001188: `output/template/.claude/skills/health-check/SKILL.md:68-68` — "Probes usually need to be reachable by infrastructure without user authentication. Options: private/internal network access, a dedicated management port, host restrictions, authorization when the probe infrastructure supports it. Detailed diagnostics are not published unauthenticated on the internet."

### EXTRA-K0-0164
- Closest oracle policies: RUN-013
- Modality: AVOID
- Normative action: Avoid Error-level logs for every normal failed probe.
- Trigger/scope: on-demand knowledge health-check (backend)
- Exceptions: none
- Why EXTRA: Probe logging guidance not in the oracle.
- Evidence K0-S001190: `output/template/.claude/skills/health-check/SKILL.md:72-72` — "Probes run frequently: avoid expensive queries, long external timeouts, large allocations, business workflows and Error-level logs for every normal failed probe."

### EXTRA-K0-0165
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: When deployment relies on health configuration test that liveness responds while healthy, readiness follows a required dependency, responses leak nothing sensitive and optional dependencies behave as intended; uncustomized framework behaviour needs no elaborate tests.
- Trigger/scope: on-demand knowledge health-check (backend)
- Exceptions: none
- Why EXTRA: Health-test guidance not in the oracle.
- Evidence K0-S001192: `output/template/.claude/skills/health-check/SKILL.md:76-76` — "When deployment relies on health configuration, test that the live endpoint responds while the process is healthy, readiness follows a required dependency, responses leak nothing sensitive, and optional dependencies behave as intended. Uncustomized framework behavior needs no elaborate tests."

### EXTRA-K0-0166
- Closest oracle policies: API-018
- Modality: MUST_NOT
- Normative action: Health checks are not a code-quality grading system.
- Trigger/scope: on-demand knowledge health-check (backend)
- Exceptions: none
- Why EXTRA: No owner clause for this item.
- Evidence K0-S001194: `output/template/.claude/skills/health-check/SKILL.md:80-80` — "Health checks as a code-quality grading system; database writes or business transactions from probes; every dependency on liveness; expensive queries; secrets or stack traces in payloads; remote dependency chains without operational justification."

### EXTRA-K0-0167
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: A 202 response returns an operation identifier or a Location where progress can be observed.
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: none
- Why EXTRA: Progress-location requirement not in the oracle.
- Evidence K0-S001205: `output/template/.claude/skills/http-api/SKILL.md:31-31` — "**202 Accepted** — accepted but not complete when the response is sent: long-running operations, background jobs, asynchronous imports, queued processing. Return an operation identifier or a `Location` where progress can be observed."

### EXTRA-K0-0168
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: Repeated DELETE of an absent resource returns 204 or 404 by one convention applied consistently across equivalent resources.
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: none
- Why EXTRA: DELETE-convention rule not in the oracle.
- Evidence K0-S001209: `output/template/.claude/skills/http-api/SKILL.md:46-46` — "Repeated `DELETE` of an absent resource may return `204` (the desired final state holds) or `404` (the addressed resource does not exist); pick one convention and apply it consistently across equivalent resources."

### EXTRA-K0-0169
- Closest oracle policies: API-003
- Modality: DEFINITION
- Normative action: 304 only answers a conditional request whose cached representation is still valid; it is not a generic 'nothing changed' business response.
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: none
- Why EXTRA: 304 semantics not in the oracle.
- Evidence K0-S001211: `output/template/.claude/skills/http-api/SKILL.md:50-50` — "**304 Not Modified** — only for a conditional request (`If-None-Match`/ETag, `If-Modified-Since`) when the client's cached representation is still valid; it carries no representation. It is not a generic "nothing changed" business response."
- Evidence K0-S001240: `output/template/.claude/skills/http-api/SKILL.md:128-148` — ""

### EXTRA-K0-0170
- Closest oracle policies: API-003, API-002
- Modality: DEFINITION
- Normative action: Status semantics beyond the oracle: 400 for invalid HTTP requests (not authentication failures); 406/415 for content negotiation and unsupported media types; 429 for rate limiting with Retry-After when known (not validation); 502/503/504 for intermediary/unavailability/upstream-timeout cases (not every dependency failure; 503 with Retry-After when meaningful).
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: none
- Why EXTRA: Status-code definitions not in the oracle.
- Evidence K0-S001213: `output/template/.claude/skills/http-api/SKILL.md:54-54` — "**400 Bad Request** — the HTTP request itself is invalid: malformed JSON, invalid shape, model-binding failure, invalid formatting, missing transport-level input. `[ApiController]` produces many of these automatically. Authentication failures are not `400`."
- Evidence K0-S001217: `output/template/.claude/skills/http-api/SKILL.md:62-62` — "**406 Not Acceptable** — the server cannot produce a representation the client accepts (response content negotiation). **415 Unsupported Media Type** — the server does not support the request body format (for example `Content-Type: application/xml` on a JSON-only endpoint)."
- Evidence K0-S001222: `output/template/.claude/skills/http-api/SKILL.md:72-72` — "**429 Too Many Requests** — rate limiting rejected the request; include `Retry-After` when the next acceptable attempt is known. Validation failures are not rate limiting."
- Evidence K0-S001225: `output/template/.claude/skills/http-api/SKILL.md:78-78` — "**502 Bad Gateway** — this API acts as an intermediary and received an invalid or unusable upstream response. Not every dependency failure is `502`."
- Evidence K0-S001226: `output/template/.claude/skills/http-api/SKILL.md:80-80` — "**503 Service Unavailable** — temporarily unable to handle the request: maintenance, a critical dependency unavailable for this operation, temporary overload. Include `Retry-After` when meaningful."
- Evidence K0-S001227: `output/template/.claude/skills/http-api/SKILL.md:82-82` — "**504 Gateway Timeout** — acting as an intermediary, an upstream service did not respond in time. Not every internal `TaskCanceledException` is `504`: distinguish a client-cancelled request, our own operation timing out, and an upstream dependency timing out — the right response depends on which occurred and the role this API plays."
- Evidence K0-S001240: `output/template/.claude/skills/http-api/SKILL.md:128-148` — ""

### EXTRA-K0-0171
- Closest oracle policies: API-003, API-010
- Modality: DEFAULT
- Normative action: 422 for structurally valid but semantically invalid content; follow an established 400-for-both convention, otherwise new APIs use 400 for invalid request contracts and 422 for invalid semantics.
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: Established convention.
- Why EXTRA: 400/422 split not in the oracle.
- Evidence K0-S001220: `output/template/.claude/skills/http-api/SKILL.md:68-68` — "**422 Unprocessable Content** — syntactically and structurally valid, but semantically or business-invalid content: impossible values, a business-rule rejection that is not a state conflict, incompatible fields such as `startDate > endDate`. Some APIs use `400` for both transport and semantic validation; follow an established convention. New APIs that distinguish them use `400` for an invalid HTTP …"
- Evidence K0-S001240: `output/template/.claude/skills/http-api/SKILL.md:128-148` — ""

### EXTRA-K0-0172
- Closest oracle policies: API-006
- Modality: DEFINITION
- Normative action: 428 when a contract-required precondition is missing (missing If-Match → 428; stale → 412); other mandatory preconditions only when the contract defines them.
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: none
- Why EXTRA: 428 semantics not in the oracle.
- Evidence K0-S001221: `output/template/.claude/skills/http-api/SKILL.md:70-70` — "**428 Precondition Required** — the contract requires a precondition the client did not send: missing required `If-Match` → `428`; provided but stale `If-Match` → `412`. Use `428` for other mandatory preconditions only when the API contract defines them."
- Evidence K0-S001232: `output/template/.claude/skills/http-api/SKILL.md:92-97` — ""
- Evidence K0-S001240: `output/template/.claude/skills/http-api/SKILL.md:128-148` — ""

### EXTRA-K0-0173
- Closest oracle policies: RUN-016, API-006
- Modality: DEFAULT
- Normative action: GET safe and idempotent, PUT idempotent, DELETE idempotent in intended state, POST generally not; consider an Idempotency-Key for POSTs that must not duplicate effects (reuse with a different payload → 409); unlikely duplicates do not make an operation idempotent.
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: none
- Why EXTRA: Idempotency guidance not in the oracle.
- Evidence K0-S001229: `output/template/.claude/skills/http-api/SKILL.md:86-86` — "`GET` is safe and idempotent; `PUT` is idempotent; `DELETE` is idempotent in intended state; `POST` generally is not. When a repeated `POST` should not create duplicate effects, consider an `Idempotency-Key` that the server associates with the request and result; reuse of a key with a materially different payload is reasonably `409`. Duplicate requests being unlikely does not make an operation ide …"

### EXTRA-K0-0174
- Closest oracle policies: GOV-012
- Modality: DEFAULT
- Normative action: Named, typed and keyed clients are all valid; choose the simplest model for the consumer and lifetime rather than mandating one model everywhere.
- Trigger/scope: on-demand knowledge httpclient-factory (backend)
- Exceptions: none
- Why EXTRA: Client-model guidance not in the oracle.
- Evidence K0-S001282: `output/template/.claude/skills/httpclient-factory/SKILL.md:33-33` — "Named, typed and keyed clients are all valid; choose the simplest model for the consumer and lifetime."
- Evidence K0-S001310: `output/template/.claude/skills/httpclient-factory/SKILL.md:132-132` — "New `HttpClient` per request; mandating one client model everywhere; retrying unsafe operations without idempotency analysis; unbounded retries; leaking `HttpResponseMessage` across boundaries; ignoring cancellation; dynamic tokens in shared default headers; mapping every upstream failure to the same status; resilience pipelines added without understanding them."

### EXTRA-K0-0175
- Closest oracle policies: ARC-025
- Modality: MUST_NOT
- Normative action: Delegating handlers serve genuine HTTP pipeline concerns (authorization headers, correlation, signing), never business decisions.
- Trigger/scope: on-demand knowledge httpclient-factory (backend)
- Exceptions: none
- Why EXTRA: Handler-scope rule not in the oracle.
- Evidence K0-S001290: `output/template/.claude/skills/httpclient-factory/SKILL.md:59-59` — "For genuine HTTP pipeline concerns — authorization header acquisition, correlation/context propagation, request signing — not business decisions:"

### EXTRA-K0-0176
- Closest oracle policies: ARC-025
- Modality: DEFAULT
- Normative action: Do not rely on EnsureSuccessStatusCode() alone when specific remote statuses carry contract meaning; map them explicitly.
- Trigger/scope: on-demand knowledge httpclient-factory (backend)
- Exceptions: none
- Why EXTRA: Status-mapping technique not in the oracle.
- Evidence K0-S001296: `output/template/.claude/skills/httpclient-factory/SKILL.md:92-92` — "Response translation boundary: `rules/backend/integrations.md`. `EnsureSuccessStatusCode()` is too blunt when specific remote statuses carry contract meaning:"
- Evidence K0-S001310: `output/template/.claude/skills/httpclient-factory/SKILL.md:132-132` — "New `HttpClient` per request; mandating one client model everywhere; retrying unsafe operations without idempotency analysis; unbounded retries; leaking `HttpResponseMessage` across boundaries; ignoring cancellation; dynamic tokens in shared default headers; mapping every upstream failure to the same status; resilience pipelines added without understanding them."

### EXTRA-K0-0177
- Closest oracle policies: none
- Modality: MUST
- Normative action: Stable headers on the client, per-request values (dynamic tokens) on the request or via a handler, never by concurrently mutating shared DefaultRequestHeaders; prefer System.Net.Http.Json/System.Text.Json with explicit options when the remote contract differs.
- Trigger/scope: on-demand knowledge httpclient-factory (backend)
- Exceptions: none
- Why EXTRA: Header/serialization technique not in the oracle.
- Evidence K0-S001304: `output/template/.claude/skills/httpclient-factory/SKILL.md:115-115` — "Stable headers (media types) can be configured on the client; per-request values such as dynamic access tokens go on the request or through a handler — mutating shared `DefaultRequestHeaders` concurrently for request-specific values is a race. Prefer `System.Net.Http.Json`/`System.Text.Json`, with explicit serializer options when the remote contract differs from the application's defaults. Interna …"
- Evidence K0-S001310: `output/template/.claude/skills/httpclient-factory/SKILL.md:132-132` — "New `HttpClient` per request; mandating one client model everywhere; retrying unsafe operations without idempotency analysis; unbounded retries; leaking `HttpResponseMessage` across boundaries; ignoring cancellation; dynamic tokens in shared default headers; mapping every upstream failure to the same status; resilience pipelines added without understanding them."

### EXTRA-K0-0178
- Closest oracle policies: DEP-020, GOV-013
- Modality: MUST
- Normative action: Resilience policies match failure and operation semantics: add a mechanism only for an identified failure scenario and observe retries, timeouts and circuit state when they matter operationally.
- Trigger/scope: private reference resilience (read by httpclient-factory)
- Exceptions: none
- Why EXTRA: Resilience-adoption rule not in the oracle.
- Evidence K0-S001244: `output/template/.claude/skills/httpclient-factory/references/resilience.md:7-7` — "Resilience policies match failure and operation semantics; add a mechanism only for an identified failure scenario, and observe retries, timeouts and circuit state when they matter operationally. The Microsoft packages are built on Polly v8, but application code uses the `Microsoft.Extensions` resilience APIs."
- Evidence K0-S001310: `output/template/.claude/skills/httpclient-factory/SKILL.md:132-132` — "New `HttpClient` per request; mandating one client model everywhere; retrying unsafe operations without idempotency analysis; unbounded retries; leaking `HttpResponseMessage` across boundaries; ignoring cancellation; dynamic tokens in shared default headers; mapping every upstream failure to the same status; resilience pipelines added without understanding them."

### EXTRA-K0-0179
- Closest oracle policies: DEP-020, RUN-016
- Modality: DEFAULT
- Normative action: The standard resilience handler is used when its behaviour fits the remote API, is not mandatory for every client, and its retry behaviour is reviewed carefully for state-changing requests.
- Trigger/scope: private reference resilience (read by httpclient-factory)
- Exceptions: none
- Why EXTRA: Standard-handler guidance not in the oracle.
- Evidence K0-S001247: `output/template/.claude/skills/httpclient-factory/references/resilience.md:19-19` — "The standard handler is useful when its behavior fits the remote API; it is not mandatory for every client. Review its retry behavior carefully for state-changing requests, and avoid stacking handlers with overlapping strategies."

### EXTRA-K0-0180
- Closest oracle policies: RUN-015
- Modality: DEFAULT
- Normative action: A circuit breaker is used only for a meaningful repeated-failure pattern where repeated calls add load or latency, with operational visibility in production when it matters.
- Trigger/scope: private reference resilience (read by httpclient-factory)
- Exceptions: none
- Why EXTRA: Circuit-breaker guidance not in the oracle.
- Evidence K0-S001256: `output/template/.claude/skills/httpclient-factory/references/resilience.md:37-37` — "Useful when repeated calls to a failing dependency would add load or latency; pointless without a meaningful repeated-failure pattern. Give it operational visibility when it matters in production."
- Evidence K0-S001273: `output/template/.claude/skills/httpclient-factory/references/resilience.md:71-79` — ""

### EXTRA-K0-0181
- Closest oracle policies: RUN-016, ARC-019
- Modality: MUST_NOT
- Normative action: Do not wrap normal EF Core operations in a generic application-level retry pipeline; prefer EF Core execution strategies/provider configuration and the provider's transaction-retry guidance; HTTP retry policies are not database policies.
- Trigger/scope: private reference resilience (read by httpclient-factory)
- Exceptions: none
- Why EXTRA: Database-resilience rule not in the oracle.
- Evidence K0-S001262: `output/template/.claude/skills/httpclient-factory/references/resilience.md:49-49` — "Do not wrap normal EF Core operations in a generic application-level retry pipeline. When the provider supports transient retry through EF Core execution strategies or provider configuration, prefer that, and handle transaction/retry interaction according to the provider's EF Core guidance. HTTP retry policies are not database policies."
- Evidence K0-S001273: `output/template/.claude/skills/httpclient-factory/references/resilience.md:71-79` — ""

### EXTRA-K0-0182
- Closest oracle policies: RUN-016
- Modality: MUST
- Normative action: Retrying message publication can duplicate delivery: use idempotent consumers, broker deduplication or outbox patterns when the business needs them; retries do not make delivery exactly-once.
- Trigger/scope: private reference resilience (read by httpclient-factory)
- Exceptions: Business requirement.
- Why EXTRA: Messaging guidance not in the oracle.
- Evidence K0-S001264: `output/template/.claude/skills/httpclient-factory/references/resilience.md:53-53` — "Retrying publication can duplicate delivery; use idempotent consumers, broker deduplication, outbox patterns or similar when the business requirement needs them. A retry policy does not make delivery exactly-once."

### EXTRA-K0-0183
- Closest oracle policies: RUN-017
- Modality: DEFINITION
- Normative action: ASP.NET Core inbound rate limiting is separate from outbound resilience; rejected requests get 429 with Retry-After when a useful delay is known.
- Trigger/scope: private reference resilience (read by httpclient-factory)
- Exceptions: none
- Why EXTRA: Inbound rate-limit guidance not in the oracle.
- Evidence K0-S001266: `output/template/.claude/skills/httpclient-factory/references/resilience.md:57-57` — "ASP.NET Core rate limiting protects this API from excessive incoming traffic and is separate from outbound resilience; rejected requests get `429` with `Retry-After` when a useful delay is known (`http-api`)."
- Evidence K0-S001273: `output/template/.claude/skills/httpclient-factory/references/resilience.md:71-79` — ""

### EXTRA-K0-0184
- Closest oracle policies: GOV-013
- Modality: MUST_NOT
- Normative action: Use the telemetry stack the project adopted; resilience handlers alone do not justify adding OpenTelemetry.
- Trigger/scope: private reference resilience (read by httpclient-factory)
- Exceptions: none
- Why EXTRA: Telemetry rule not in the oracle.
- Evidence K0-S001270: `output/template/.claude/skills/httpclient-factory/references/resilience.md:65-65` — "Useful signals: retry counts, timeout frequency, circuit state, rate-limit rejections, dependency latency. Use the telemetry stack the project adopted; resilience handlers alone do not justify adding OpenTelemetry."

### EXTRA-K0-0185
- Closest oracle policies: RUN-013
- Modality: DEFINITION
- Normative action: Choose log levels by operational meaning: Trace/Debug diagnostics (not safe for sensitive data), Information meaningful events (not every call), Warning recovered/degraded conditions, Error failed operations needing investigation, Critical when the application or a subsystem cannot continue.
- Trigger/scope: on-demand knowledge logging (backend)
- Exceptions: none
- Why EXTRA: Log-level semantics not in the oracle.
- Evidence K0-S001356: `output/template/.claude/skills/logging/SKILL.md:32-38` — "Choose levels by operational meaning: ⏎  ⏎ - **Trace/Debug** — detailed diagnostics for troubleshooting; not a safe place for sensitive data. ⏎ - **Information** — meaningful application events: a background job completed, an important business operation completed, a lifecycle event. Not every internal method call. ⏎ - **Warning** — an unexpected or degraded condition the application recovered fro …"

### EXTRA-K0-0186
- Closest oracle policies: RUN-013
- Modality: PREFER
- Normative action: Prefer platform/runtime trace identifiers; add an explicit correlation identifier only for an integration or operational requirement; propagate tracing context across outbound calls with the chosen tracing/HTTP infrastructure.
- Trigger/scope: on-demand knowledge logging (backend)
- Exceptions: none
- Why EXTRA: Correlation guidance not in the oracle.
- Evidence K0-S001363: `output/template/.claude/skills/logging/SKILL.md:61-61` — "Prefer platform/runtime trace identifiers when they already correlate requests adequately. Add an explicit correlation identifier only for an integration or operational requirement; validate or normalize an identifier accepted from an external client before propagating it, and propagate tracing context across outbound calls with the project's chosen tracing or HTTP infrastructure."

### EXTRA-K0-0187
- Closest oracle policies: RUN-014
- Modality: AVOID
- Normative action: Do not use logs as an audit database without a dedicated audit design.
- Trigger/scope: on-demand knowledge logging (backend)
- Exceptions: Dedicated audit design.
- Why EXTRA: No owner clause for this item.
- Evidence K0-S001372: `output/template/.claude/skills/logging/SKILL.md:92-92` — "String interpolation in log calls; duplicate exception logging; expected outcomes logged as errors; credentials or secrets in logs; whole objects dumped without review; provider-specific APIs spread through Application code; logs used as an audit database without a dedicated audit design."

### EXTRA-K0-0188
- Closest oracle policies: DEP-021
- Modality: DEFAULT
- Normative action: Use a two-stage bootstrap logger when startup failures before DI/configuration need to be captured; simpler applications can skip it.
- Trigger/scope: private reference serilog (read by logging)
- Exceptions: Simpler applications.
- Why EXTRA: Bootstrap-logger guidance not in the oracle.
- Evidence K0-S001318: `output/template/.claude/skills/logging/references/serilog.md:20-20` — "Use a bootstrap logger when startup failures before DI/configuration need to be captured; simpler applications can skip it."

### EXTRA-K0-0189
- Closest oracle policies: DEP-021
- Modality: MUST
- Normative action: When the static/bootstrap Log.Logger is used, flush it on shutdown (try/finally with CloseAndFlushAsync).
- Trigger/scope: private reference serilog (read by logging)
- Exceptions: Purely host-managed logging follows the provider lifetime.
- Why EXTRA: Flush requirement not in the oracle.
- Evidence K0-S001320: `output/template/.claude/skills/logging/references/serilog.md:61-61` — "When the static/bootstrap `Log.Logger` is used, flush it on shutdown (`try`/`finally` with `CloseAndFlushAsync`) so buffered events from asynchronous sinks are written; purely host-managed logging follows the provider's lifetime."

### EXTRA-K0-0190
- Closest oracle policies: DEP-001, DEP-021
- Modality: DEFAULT
- Normative action: File, Seq and other sinks are not baseline dependencies; a Console sink suffices for a simple local Development baseline; example limits and retention values are illustrative.
- Trigger/scope: private reference serilog (read by logging)
- Exceptions: none
- Why EXTRA: Sink-baseline guidance not in the oracle.
- Evidence K0-S001322: `output/template/.claude/skills/logging/references/serilog.md:65-65` — "Keep levels, sinks and overrides in configuration so they can differ per environment. The example shows several optional sinks at once — File, Seq and others are not baseline dependencies; a Console sink suffices for a simple local Development baseline, and numeric limits and retention values are illustrative."

### EXTRA-K0-0191
- Closest oracle policies: RUN-014
- Modality: DEFAULT
- Normative action: Limit destructuring of large object graphs or transform types to specific properties.
- Trigger/scope: private reference serilog (read by logging)
- Exceptions: none
- Why EXTRA: Destructuring guidance not in the oracle.
- Evidence K0-S001330: `output/template/.claude/skills/logging/references/serilog.md:151-151` — "Limit destructuring of large graphs, or transform types to specific properties:"

### EXTRA-K0-0192
- Closest oracle policies: DEP-004
- Modality: MUST_NOT
- Normative action: Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.
- Trigger/scope: private reference serilog (read by logging)
- Exceptions: none
- Why EXTRA: Concrete deprecated-package guidance not in the oracle.
- Evidence K0-S001341: `output/template/.claude/skills/logging/references/serilog.md:200-200` — "The `Serilog.Sinks.Elasticsearch` package is deprecated; use the official `Elastic.Serilog.Sinks` package (same `WriteTo.Elasticsearch` name, ECS documents to data streams):"
- Evidence K0-S001345: `output/template/.claude/skills/logging/references/serilog.md:211-219` — ""

### EXTRA-K0-0193
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Use collection expressions when the target type is clear.
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: Collection-expression guidance not in the oracle.
- Evidence K0-S001386: `output/template/.claude/skills/modern-csharp/SKILL.md:34-34` — "Use them when the target type is clear."

### EXTRA-K0-0194
- Closest oracle policies: ARC-004, API-010
- Modality: DEFINITION
- Normative action: required expresses a construction contract and does not replace constructor or domain validation where invariants need protection.
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: required-member semantics not in the oracle.
- Evidence K0-S001391: `output/template/.claude/skills/modern-csharp/SKILL.md:46-46` — "`required` expresses a construction contract; it does not replace constructor or domain validation where invariants need protection."

### EXTRA-K0-0195
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Model immutability where it is natural; framework models and controlled-mutation workflows often stay simpler mutable.
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: Immutability guidance not in the oracle.
- Evidence K0-S001405: `output/template/.claude/skills/modern-csharp/SKILL.md:105-105` — "Model immutability where it is natural; framework models and workflows with controlled mutation often stay simpler mutable."

### EXTRA-K0-0196
- Closest oracle policies: DEP-008, ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Confirm the configured language version supports a feature before using it; changing LangVersion or the target framework to use newer syntax is a decision, not a silent edit.
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: LangVersion/TFM decision gate beyond DEP-008's preview/RC rule.
- Evidence K0-S001409: `output/template/.claude/skills/modern-csharp/SKILL.md:113-113` — "Confirm the configured language version supports a feature before using it; changing `LangVersion` or the target framework to use newer syntax is a decision, not a silent edit."
- Evidence K0-S001414: `output/template/.claude/skills/modern-csharp/SKILL.md:127-127` — "Newest syntax for its own sake; every class turned into a record; `record struct` merely to avoid allocations; `Span<T>` without a performance reason; deeply nested patterns; mass constructor conversion; language or framework version changes without approval."

### EXTRA-K0-0197
- Closest oracle policies: RUN-008, RUN-009
- Modality: AVOID
- Normative action: Avoid record struct merely to avoid allocations and deeply nested patterns.
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: No owner clause for these items.
- Evidence K0-S001414: `output/template/.claude/skills/modern-csharp/SKILL.md:127-127` — "Newest syntax for its own sake; every class turned into a record; `record struct` merely to avoid allocations; `Span<T>` without a performance reason; deeply nested patterns; mass constructor conversion; language or framework version changes without approval."

### EXTRA-K0-0198
- Closest oracle policies: RUN-024
- Modality: MUST
- Normative action: Make each supporting type's responsibility clear from its name, directory or both (role suffixes; e.g. TaskWorkflowRules over TaskWorkflow); add responsibility subdirectories only when a flat feature directory becomes hard to navigate.
- Trigger/scope: private reference backend-layout (read by project-structure)
- Exceptions: none
- Why EXTRA: Type-role naming convention not in the oracle.
- Evidence K0-S001430: `output/template/.claude/skills/project-structure/references/backend-layout.md:39-39` — "Within a feature or service area, make each supporting type's responsibility clear from its name, its directory or both. Useful suffixes:"
- Evidence K0-S001432: `output/template/.claude/skills/project-structure/references/backend-layout.md:53-53` — "Prefer `TaskWorkflowRules`, `TaskWorkflowPolicy` or `TaskWorkflowService` over an ambiguous `TaskWorkflow`. Add responsibility-specific subdirectories when a flat feature directory becomes hard to navigate, not to classify one or two obvious files. Avoid generic `Models`, `Helpers`, `Common` or `Utils` buckets when a specific responsibility can be named."

### EXTRA-K0-0199
- Closest oracle policies: ARC-012, GOV-012
- Modality: MUST_NOT
- Normative action: Api Extensions hold cohesive API/composition extension methods; do not move arbitrary code out of Program.cs just to shorten it.
- Trigger/scope: private reference backend-layout (read by project-structure)
- Exceptions: none
- Why EXTRA: Program.cs extraction rule not in the oracle.
- Evidence K0-S001443: `output/template/.claude/skills/project-structure/references/backend-layout.md:94-94` — "- `Extensions` — cohesive API/composition extension methods; do not move arbitrary code out of `Program.cs` just to shorten it."

### EXTRA-K0-0200
- Closest oracle policies: DEP-013, DEP-009, DEP-010
- Modality: MUST
- Normative action: New applications install the packages each decision names plus scaffold packages: Microsoft.EntityFrameworkCore.Design where migrations are created (provider in Infrastructure, Api as startup project), a Console sink for a simple local logging baseline (Api), NUnit3TestAdapter and Microsoft.NET.Test.Sdk in test projects.
- Trigger/scope: new applications
- Exceptions: none
- Why EXTRA: Concrete scaffold package set not in the oracle.
- Evidence K0-S001456: `output/template/.claude/skills/project-structure/references/baseline-setup.md:9-9` — "Install the packages each decision names, plus the scaffold packages below, in these projects:"
- Evidence K0-S001458: `output/template/.claude/skills/project-structure/references/baseline-setup.md:13-17` — "| Persistence (D-04) | `Microsoft.EntityFrameworkCore.Design` where migrations are created | provider in Infrastructure; Api as migrations startup project | ⏎ | Validation (D-05) | — | Application | ⏎ | Logging (D-06) | Console sink for a simple local baseline | Api | ⏎ | API documentation (D-07) | — | Api | ⏎ | Tests (D-08) | `NUnit3TestAdapter`, `Microsoft.NET.Test.Sdk` | test projects |"

### EXTRA-K0-0201
- Closest oracle policies: WF-006, DEP-012
- Modality: DEFAULT
- Normative action: Set the launch profile to open Swagger (launchBrowser true, launchUrl swagger) with application URLs matching the profile.
- Trigger/scope: private reference baseline-setup (read by project-structure; new applications)
- Exceptions: none
- Why EXTRA: Launch-profile configuration not in the oracle.
- Evidence K0-S001466: `output/template/.claude/skills/project-structure/references/baseline-setup.md:39-39` — "Expose Swagger UI at `/swagger` in Development and set the launch profile to open it (`"launchBrowser": true`, `"launchUrl": "swagger"`), with application URLs that match the profile (technique: `swagger`)."

### EXTRA-K0-0202
- Closest oracle policies: DEP-024, TST-002
- Modality: DEFAULT
- Normative action: Typical test projects are Application.Tests and IntegrationTests; Domain.Tests only for non-trivial Domain behaviour; Infrastructure.Tests only for a concrete need; Angular unit/component tests stay in the workspace and adopted E2E tests under frontend/<Name>.Web/e2e/.
- Trigger/scope: workflow project-structure (solution scaffolding, project and reference changes, restructuring)
- Exceptions: none
- Why EXTRA: Concrete test-project set not in the oracle.
- Evidence K0-S001476: `output/template/.claude/skills/project-structure/references/solution-layout.md:38-42` — "non-trivial behavior that genuinely belongs to Domain"
- Evidence K0-S001480: `output/template/.claude/skills/project-structure/references/solution-layout.md:50-50` — "Angular unit and component tests stay in the workspace, usually colocated with the code they test. E2E tests, when adopted, also stay in the workspace, for example `frontend/ProjectName.Web/e2e/`. Angular tests never go under `backend/`."
- Evidence K0-S001505: `output/template/.claude/skills/project-structure/SKILL.md:26-26` — "7. **Test projects.** Create only useful test projects beside production projects under `backend/` (typically `Application.Tests` and `IntegrationTests`; `Domain.Tests` only when Domain has non-trivial behavior; `Infrastructure.Tests` only for a concrete need). Angular unit/component tests stay in the Angular workspace; E2E tests, when adopted, under `frontend/<Name>.Web/e2e/`."

### EXTRA-K0-0203
- Closest oracle policies: ARC-001, ARC-020
- Modality: MUST
- Normative action: Run an approved reference command (dotnet add/remove … reference, dotnet reference add/remove) with the trailing comment '# project-references: approved'; the hook stops reference commands without it.
- Trigger/scope: workflow project-structure (solution scaffolding, project and reference changes, restructuring)
- Exceptions: none
- Why EXTRA: Approval-marker procedure not in the oracle.
- Evidence K0-S001512: `output/template/.claude/skills/project-structure/SKILL.md:35-35` — "2. Run the reference command (`dotnet add <project> reference …`, `dotnet remove <project> reference …`, `dotnet reference add|remove …`) with the trailing comment `# project-references: approved`; the pre-command hook stops reference commands without it."

### EXTRA-K0-0204
- Closest oracle policies: GOV-014, GOV-012
- Modality: MUST_NOT
- Normative action: Do not force an established project to match this template when doing so provides no concrete value.
- Trigger/scope: workflow project-structure (solution scaffolding, project and reference changes, restructuring)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K0-S001518: `output/template/.claude/skills/project-structure/SKILL.md:56-56` — "Do not force an established project to match this template when doing so provides no concrete value."

### EXTRA-K0-0205
- Closest oracle policies: DEP-014
- Modality: MUST_NOT
- Normative action: Do not impose an obsolete Angular directory structure when the current CLI generates a different supported one.
- Trigger/scope: private reference solution-layout (read by project-structure)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K0-S001479: `output/template/.claude/skills/project-structure/references/solution-layout.md:48-48` — "The Angular workspace lives outside the .NET tree, in `frontend/ProjectName.Web/`, and owns its `package.json`, `package-lock.json`, `angular.json`, tsconfig files, `src/` and `public/`. Do not impose an obsolete Angular directory structure when the current Angular CLI generates a different supported one."

### EXTRA-K0-0206
- Closest oracle policies: DEP-008
- Modality: MUST
- Normative action: global.json pins the intended supported .NET SDK line, selecting the current stable SDK of the target release with a rollForward policy allowing patch/feature-band servicing.
- Trigger/scope: private reference solution-layout (read by project-structure)
- Exceptions: none
- Why EXTRA: SDK-pinning rule not in the oracle.
- Evidence K0-S001486: `output/template/.claude/skills/project-structure/references/solution-layout.md:60-60` — "- `global.json` — pin the intended supported .NET SDK line. When scaffolding, select the current stable SDK of the target .NET release (no RC/preview SDK unless explicitly requested) and allow patch/feature-band servicing through the chosen `rollForward` policy."

### EXTRA-K0-0207
- Closest oracle policies: none
- Modality: PREFER
- Normative action: Repository-wide formatting/code style lives in .editorconfig; prefer enforceable tooling configuration over restating mechanical formatting rules in instructions.
- Trigger/scope: private reference solution-layout (read by project-structure)
- Exceptions: none
- Why EXTRA: Instruction-placement preference not in the oracle.
- Evidence K0-S001488: `output/template/.claude/skills/project-structure/references/solution-layout.md:64-64` — "Repository-wide formatting and code-style configuration lives here; prefer enforceable tooling configuration over restating mechanical formatting rules in instructions."

### EXTRA-K0-0208
- Closest oracle policies: SEC-001
- Modality: MUST
- Normative action: Ignore generated and local artifacts (bin, obj, .vs, node_modules, dist, TestResults, coverage, local secret/config overrides, .claude/.hook-state/); do not ignore files that are part of the Development configuration contract.
- Trigger/scope: private reference solution-layout (read by project-structure)
- Exceptions: none
- Why EXTRA: Ignore-list rule not in the oracle.
- Evidence K0-S001490: `output/template/.claude/skills/project-structure/references/solution-layout.md:68-68` — "Ignore generated and local artifacts where applicable: `bin/`, `obj/`, `.vs/`, `node_modules/`, `dist/`, `TestResults/`, `coverage/`, local secret/config overrides, `.claude/.hook-state/`. Do not ignore files that are intentionally part of the Development configuration contract."

### EXTRA-K0-0209
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: The scan is an evidence-based static review, not a penetration test, and cannot prove the application secure; state that limitation in the report.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: Limitation statement not in the oracle.
- Evidence K0-S001587: `output/template/.claude/skills/security-scan/SKILL.md:16-16` — "Perform an evidence-based static review of the repository. It is not a penetration test and cannot prove the application secure; it may miss runtime-only vulnerabilities, infrastructure outside the repository, complex business-logic abuse, sophisticated authorization bypasses, deployment-specific weaknesses and issues that need dynamic exploitation. State that limitation in the report."
- Evidence K0-S001620: `output/template/.claude/skills/security-scan/SKILL.md:140-140` — "The scan is complete when every applicable layer was inspected, findings carry evidence, uncertain findings are labeled, severity reflects actual risk, limitations are stated and no layer is marked PASS without being checked."

### EXTRA-K0-0210
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: Inspect which surfaces exist (backend, frontend, auth, data access, integrations, files, containers, CI/CD, production config, logging, caching, background work) and skip irrelevant checks instead of reporting them as failures.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: Scope-determination step not in the oracle.
- Evidence K0-S001597: `output/template/.claude/skills/security-scan/SKILL.md:30-30` — "Inspect which surfaces exist — .NET backend, Angular frontend, authentication/authorization, database access, external HTTP integrations, file upload/download, Docker/container configuration, CI/CD, production configuration, logging, caching, background processing — and skip irrelevant checks instead of reporting them as failures."

### EXTRA-K0-0211
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: Scan-depth rule not in the oracle.
- Evidence K0-S001598: `output/template/.claude/skills/security-scan/SKILL.md:32-32` — "For a full pre-release or explicitly requested audit, review every applicable layer. For targeted changes, start with the affected layers and expand when the change crosses security boundaries:"
- Evidence K0-S001600: `output/template/.claude/skills/security-scan/SKILL.md:36-44` — ""

### EXTRA-K0-0212
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: OWASP Top 10:2025 is an awareness taxonomy; map a finding only when the category genuinely fits.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: OWASP-mapping rule not in the oracle.
- Evidence K0-S001605: `output/template/.claude/skills/security-scan/SKILL.md:60-60` — "OWASP Top 10:2025 is an awareness taxonomy — A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging & Alerting Failures, A10 Mishandling of Exceptional Conditions. Map a finding only when the category genui …"

### EXTRA-K0-0213
- Closest oracle policies: WF-020
- Modality: DEFINITION
- Normative action: Severity scale: Critical (sparingly; immediately exploitable high impact), High, Medium, Low, Info (hardening observation).
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: Severity scale not in the oracle.
- Evidence K0-S001609: `output/template/.claude/skills/security-scan/SKILL.md:68-72` — "- **Critical** (use sparingly) — immediately exploitable, high-impact: exposed real production credentials, reachable authentication bypass, straightforward remote code execution, exploitable injection with major impact. ⏎ - **High** — serious, realistically exploitable, or able to substantially compromise data, authorization or system behavior. ⏎ - **Medium** — meaningful weakness needing realist …"

### EXTRA-K0-0214
- Closest oracle policies: SEC-006, SEC-009, SEC-008
- Modality: DEFINITION
- Normative action: Not automatically vulnerabilities: endpoints without [Authorize] under a secure fallback, bare [Authorize] when authentication alone is intended, AllowAnyOrigin on a public non-credentialed API, MD5/SHA1 checksums, no app-level encryption when platform encryption suffices, obviously fake test credentials, framework defaults secure in the actual hosting.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: False-positive catalogue not in the oracle.
- Evidence K0-S001611: `output/template/.claude/skills/security-scan/SKILL.md:76-76` — "Not automatically vulnerabilities: an endpoint without `[Authorize]` protected by a secure fallback policy; bare `[Authorize]` when authentication alone is intended; `AllowAnyOrigin()` on a genuinely public, non-credentialed API; MD5/SHA1 as a non-security checksum; no application-level encryption when platform or storage encryption satisfies the requirement; obviously fake test credentials; frame …"

### EXTRA-K0-0215
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: Every confirmed finding includes severity, file/location, title, evidence, why it is a risk, likely impact, smallest remediation and OWASP category when applicable.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: Finding format not in the oracle.
- Evidence K0-S001614: `output/template/.claude/skills/security-scan/SKILL.md:82-82` — "Every confirmed finding includes severity, file and location, title, evidence, why it is a risk, likely impact, smallest reasonable remediation and OWASP category when applicable. Label uncertain findings `NEEDS VERIFICATION` instead of presenting them as confirmed, and never invent exploitability the code does not establish."

### EXTRA-K0-0216
- Closest oracle policies: SEC-008, GOV-013
- Modality: MUST_NOT
- Normative action: Recommend the smallest secure change consistent with the architecture; do not recommend blanket encryption of all fields, security libraries merely to satisfy the scan, or disabling functionality a static scanner cannot understand.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: Remediation discipline not in the oracle.
- Evidence K0-S001618: `output/template/.claude/skills/security-scan/SKILL.md:136-136` — "Recommend the smallest secure change consistent with the project architecture. Do not recommend a new authentication system unnecessarily, custom cryptography, blanket encryption of all database fields, `[Authorize]` on every action when a global policy already protects them, security libraries merely to satisfy the scan, or disabling functionality because a static scanner cannot understand it."

### EXTRA-K0-0217
- Closest oracle policies: SEC-003
- Modality: PREFER
- Normative action: Prefer process APIs that separate the executable from its arguments; validate or constrain external input when command execution is genuinely needed.
- Trigger/scope: private reference scan-layers (read by security-scan)
- Exceptions: none
- Why EXTRA: Command-injection guidance not in the oracle.
- Evidence K0-S001537: `output/template/.claude/skills/security-scan/references/scan-layers.md:61-61` — "Inspect `Process.Start`, shell execution, PowerShell/bash invocation and command arguments built from user input. Prefer APIs that separate the executable from its arguments; validate or constrain external input when command execution is genuinely needed."

### EXTRA-K0-0218
- Closest oracle policies: SEC-003
- Modality: MUST
- Normative action: Normalize and verify that user-influenced paths remain inside the intended storage boundary.
- Trigger/scope: private reference scan-layers (read by security-scan)
- Exceptions: none
- Why EXTRA: Path-safety rule not in the oracle.
- Evidence K0-S001539: `output/template/.claude/skills/security-scan/references/scan-layers.md:65-65` — "Review user-controlled file names, paths, archive extraction, download paths and upload destinations for `../`, absolute-path injection, escaping the intended root and unsafe archive extraction. Normalize and verify that paths remain inside the intended storage boundary."

### EXTRA-K0-0219
- Closest oracle policies: SEC-003
- Modality: MUST_NOT
- Normative action: Untrusted payloads are not deserialized into arbitrary runtime types (e.g. BinaryFormatter, unsafe TypeNameHandling).
- Trigger/scope: private reference scan-layers (read by security-scan)
- Exceptions: none
- Why EXTRA: Deserialization rule not in the oracle.
- Evidence K0-S001541: `output/template/.claude/skills/security-scan/references/scan-layers.md:77-77` — "Investigate polymorphic or type-driven deserialization such as `BinaryFormatter` or unsafe Newtonsoft `TypeNameHandling` settings. Untrusted payloads are not deserialized into arbitrary runtime types."

### EXTRA-K0-0220
- Closest oracle policies: SEC-017
- Modality: MUST_NOT
- Normative action: Do not demand manually setting every TokenValidationParameters property when authority/metadata configuration already establishes secure validation, and do not impose an arbitrary universal ClockSkew.
- Trigger/scope: private reference scan-layers (read by security-scan)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K0-S001554: `output/template/.claude/skills/security-scan/references/scan-layers.md:103-103` — "For Bearer/OIDC, check that the configured mechanism validates issuer, audience where applicable, signature/signing authority and lifetime. Do not demand manually setting every `TokenValidationParameters` property when the provider's authority/metadata configuration already establishes secure validation, and do not impose an arbitrary universal `ClockSkew`. Flag intentionally disabled validation t …"

### EXTRA-K0-0221
- Closest oracle policies: SEC-013, RUN-017
- Modality: DEFAULT
- Normative action: Consider rate limiting where abuse realistically matters (login, password reset, expensive anonymous or resource-intensive endpoints), not on every endpoint.
- Trigger/scope: private reference scan-layers (read by security-scan)
- Exceptions: none
- Why EXTRA: Rate-limiting guidance not in the oracle.
- Evidence K0-S001564: `output/template/.claude/skills/security-scan/references/scan-layers.md:133-133` — "Consider rate limiting where abuse realistically matters — login and password reset, expensive anonymous endpoints, resource-intensive operations — not on every endpoint. `429` semantics: `http-api`."

### EXTRA-K0-0222
- Closest oracle policies: ARC-029, SEC-010
- Modality: PREFER
- Normative action: Returning a Domain entity is not automatically vulnerable (inspect serialized fields), but explicit response contracts are preferable where needed.
- Trigger/scope: private reference scan-layers (read by security-scan)
- Exceptions: none
- Why EXTRA: Response-contract preference not in the oracle.
- Evidence K0-S001566: `output/template/.claude/skills/security-scan/references/scan-layers.md:147-147` — "Look for database/domain entities returned directly, password hashes, internal security fields, unnecessary personal information and secret metadata. Returning a Domain entity is not automatically vulnerable — inspect the serialized fields — but explicit response contracts are preferable where needed."

### EXTRA-K0-0223
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: When meaningful security-sensitive workflows exist, name them as candidates for threat modeling or manual review instead of claiming the static scan proves them secure.
- Trigger/scope: private reference scan-layers (read by security-scan)
- Exceptions: none
- Why EXTRA: Threat-modeling referral not in the oracle.
- Evidence K0-S001576: `output/template/.claude/skills/security-scan/references/scan-layers.md:195-195` — "Static checks do not fully cover A06 Insecure Design, tenant isolation, business-workflow abuse, privilege escalation through legitimate operations, financial/idempotency abuse or multi-step authorization problems. When meaningful security-sensitive workflows exist, name them as candidates for threat modeling or dedicated manual review rather than claiming the static scan proves them secure."

### EXTRA-K0-0224
- Closest oracle policies: ARC-012
- Modality: MUST
- Normative action: Keep Swagger configuration in the API/composition layer.
- Trigger/scope: on-demand knowledge swagger (backend)
- Exceptions: none
- Why EXTRA: Placement rule not in the oracle.
- Evidence K0-S001628: `output/template/.claude/skills/swagger/SKILL.md:31-31` — "Keep Swagger configuration in the API/composition layer. The built-in `AddOpenApi()`/`MapOpenApi()` is not a replacement when the requirement is interactive Swagger UI testing."

### EXTRA-K0-0225
- Closest oracle policies: WF-006
- Modality: MUST
- Normative action: Keep application URLs and the launch profile in agreement; a launch URL pointing to HTTPS on an HTTP-only port fails.
- Trigger/scope: on-demand knowledge swagger (backend)
- Exceptions: none
- Why EXTRA: Launch-profile consistency not in the oracle.
- Evidence K0-S001631: `output/template/.claude/skills/swagger/SKILL.md:42-42` — "Keep the application URLs and the launch profile in agreement — a browser launch URL pointing to HTTPS on an HTTP-only port fails."

### EXTRA-K0-0226
- Closest oracle policies: API-002, API-016
- Modality: DEFAULT
- Normative action: When failures use ProblemDetails/ValidationProblemDetails describe those contracts where useful.
- Trigger/scope: on-demand knowledge swagger (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K0-S001636: `output/template/.claude/skills/swagger/SKILL.md:62-62` — "When failures use `ProblemDetails`/`ValidationProblemDetails`, describe those contracts where useful. Keep internal exception types, stack traces, SQL, connection strings and filesystem paths out of Swagger examples and descriptions (`rules/backend/error-handling.md` § Unexpected failures)."

### EXTRA-K0-0227
- Closest oracle policies: API-016
- Modality: DEFAULT
- Normative action: Document what helps consumers (preconditions, idempotency, pagination/filtering, meaningful outcomes), not descriptions repeating names; XML comments only when the project chooses them.
- Trigger/scope: on-demand knowledge swagger (backend)
- Exceptions: none
- Why EXTRA: Documentation-content guidance not in the oracle.
- Evidence K0-S001640: `output/template/.claude/skills/swagger/SKILL.md:70-70` — "Document what helps consumers: important preconditions, idempotency semantics, pagination/filtering behavior, meaningful outcomes — not descriptions that repeat action or property names. XML comments can help public contracts when the project chooses them; they are not needed on every internal type."

### EXTRA-K0-0228
- Closest oracle policies: API-016
- Modality: MUST_NOT
- Normative action: Use several Swagger documents only for a real contract separation (API versions, public/internal surfaces).
- Trigger/scope: on-demand knowledge swagger (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K0-S001642: `output/template/.claude/skills/swagger/SKILL.md:74-74` — "Use several Swagger documents only for a real contract separation, such as API versions (`api-versioning`) or distinct public/internal surfaces."

### EXTRA-K0-0229
- Closest oracle policies: API-016, ARC-029
- Modality: MUST
- Normative action: Avoid unstable anonymous response shapes, use explicit request/response contracts and review generated-client changes when the contract changes.
- Trigger/scope: on-demand knowledge swagger (backend)
- Exceptions: none
- Why EXTRA: Client-contract guidance not in the oracle.
- Evidence K0-S001644: `output/template/.claude/skills/swagger/SKILL.md:78-78` — "When the contract drives Angular or other client generation: treat breaking schema changes seriously, keep response metadata accurate, avoid unstable anonymous response shapes, use explicit request/response contracts and review generated-client changes when the contract changes."
- Evidence K0-S001648: `output/template/.claude/skills/swagger/SKILL.md:91-91` — "Metadata that disagrees with runtime responses; Swagger UI exposed publicly without a reason; Swagger treated as a substitute for integration tests; global authentication requirements on anonymous endpoints; anonymous objects as long-lived contracts; a second competing documentation stack without a concrete need."

### EXTRA-K0-0230
- Closest oracle policies: TST-006
- Modality: MUST_NOT
- Normative action: Swagger is not a substitute for integration tests.
- Trigger/scope: on-demand knowledge swagger (backend)
- Exceptions: none
- Why EXTRA: No owner clause for this item.
- Evidence K0-S001648: `output/template/.claude/skills/swagger/SKILL.md:91-91` — "Metadata that disagrees with runtime responses; Swagger UI exposed publicly without a reason; Swagger treated as a substitute for integration tests; global authentication requirements on anonymous endpoints; anonymous objects as long-lived contracts; a second competing documentation stack without a concrete need."

### EXTRA-K0-0231
- Closest oracle policies: none
- Modality: MUST
- Normative action: Search for an existing owner of a rule (MAP topic index, repository search) and extend it instead of adding a second statement; other artifacts only point to the owner or check against it with a short check-by-reference item, never rewording the rule.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: One-owner rule (repo/meta).
- Evidence K0-S001661: `output/template/.claude/skills/template-maintenance/SKILL.md:32-33` — "1. Search for an existing owner of the same rule (`.claude/MAP.md` topic index, then a repository search). Extend that owner instead of adding a second statement. ⏎ 2. Other artifacts may only point to the owner (routing pointer) or check against it (a short check-by-reference item); never reword the same rule elsewhere."

### EXTRA-K0-0232
- Closest oracle policies: none
- Modality: MUST_NOT
- Normative action: A critical must/must-not rule never lives only in a knowledge skill or a skill-private reference.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Instruction-placement rule (repo/meta).
- Evidence K0-S001662: `output/template/.claude/skills/template-maintenance/SKILL.md:34-34` — "3. A critical must/must-not rule never lives only in a knowledge skill or a skill-private reference."

### EXTRA-K0-0233
- Closest oracle policies: none
- Modality: MUST
- Normative action: Keep the trigger role: always-loaded policy stays in OP/DEC, path rules stay path-scoped with at least their current scope, workflow obligations stay in workflow steps; do not move content between roles to save tokens.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Trigger-role rule (repo/meta).
- Evidence K0-S001663: `output/template/.claude/skills/template-maintenance/SKILL.md:35-35` — "4. Keep the trigger role: always-loaded policy stays in OP/DEC, path rules stay path-scoped with at least their current scope, workflow obligations stay in workflow steps. Do not move content between roles to save tokens."

### EXTRA-K0-0234
- Closest oracle policies: none
- Modality: MUST
- Normative action: Write each artifact with its one-line 'Kind | Scope | Owner | Loading' header after any frontmatter.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Header rule (repo/meta).
- Evidence K0-S001667: `output/template/.claude/skills/template-maintenance/SKILL.md:43-43` — "1. Write the artifact with its one-line header: `> Kind: … | Scope: … | Owner: … | Loading: …` (after any frontmatter)."

### EXTRA-K0-0235
- Closest oracle policies: none
- Modality: MUST
- Normative action: Knowledge skill descriptions stay concise and trigger-first ('Use when …' with concrete cues).
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Description rule (repo/meta).
- Evidence K0-S001669: `output/template/.claude/skills/template-maintenance/SKILL.md:45-45` — "3. Knowledge skill descriptions stay concise and trigger-first ("Use when …" with concrete cues)."

### EXTRA-K0-0236
- Closest oracle policies: none
- Modality: MUST
- Normative action: Update .claude/MAP.md (artifact table, Kind × Scope view, topic index, decision → Affects view) with every instruction change.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Map-maintenance rule (repo/meta).
- Evidence K0-S001670: `output/template/.claude/skills/template-maintenance/SKILL.md:46-46` — "4. Update `.claude/MAP.md`: artifact table, Kind × Scope view, topic index and decision → Affects view."

### EXTRA-K0-0237
- Closest oracle policies: none
- Modality: MUST
- Normative action: Keep the always-loaded surface (CLAUDE.md, register, skill descriptions) compact; move detail to its owner.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Context-cost rule (repo/meta).
- Evidence K0-S001671: `output/template/.claude/skills/template-maintenance/SKILL.md:47-47` — "5. Keep the always-loaded surface (CLAUDE.md, the register, skill descriptions) compact; move detail to the owner it belongs to."

### EXTRA-K0-0238
- Closest oracle policies: none
- Modality: MUST
- Normative action: Run check-instructions.cjs and fix every reported problem.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Checker obligation (repo/meta).
- Evidence K0-S001673: `output/template/.claude/skills/template-maintenance/SKILL.md:51-51` — "1. Run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.cjs"` and fix every reported problem."

### EXTRA-K0-0239
- Closest oracle policies: none
- Modality: MUST
- Normative action: When hooks or scripts changed, exercise them with a sample payload.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Hook-testing obligation (repo/meta).
- Evidence K0-S001674: `output/template/.claude/skills/template-maintenance/SKILL.md:52-52` — "2. When hooks or scripts changed, exercise them with a sample payload, for example:"

### EXTRA-K0-0240
- Closest oracle policies: none
- Modality: MUST
- Normative action: Summarize what moved, the new owners and the checker result.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Maintenance output contract (repo/meta).
- Evidence K0-S001676: `output/template/.claude/skills/template-maintenance/SKILL.md:58-58` — "3. Summarize what moved, the new owners and the checker result."

### EXTRA-K0-0241
- Closest oracle policies: WF-005
- Modality: MUST_NOT
- Normative action: Do not use --no-restore unless restore is known to be complete.
- Trigger/scope: workflow verify (before declaring implementation complete)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K0-S001687: `output/template/.claude/skills/verify/SKILL.md:32-32` — "Prefer the targeted project or `.slnx` when appropriate. Do not use `--no-restore` unless restore is known to be complete. For Angular, use the build script `package.json` actually defines."

### EXTRA-K0-0242
- Closest oracle policies: WF-005
- Modality: DEFAULT
- Normative action: Small solutions run the complete suite; large solutions run affected test projects first, then the broader suite the risk requires.
- Trigger/scope: workflow verify (before declaring implementation complete)
- Exceptions: none
- Why EXTRA: Suite-scoping guidance not in the oracle.
- Evidence K0-S001691: `output/template/.claude/skills/verify/SKILL.md:42-42` — "For Angular, inspect `package.json` and run the configured test script rather than assuming a runner. Small solutions: run the complete suite. Large solutions: affected test projects first, then the broader suite the risk requires."

### EXTRA-K0-0243
- Closest oracle policies: WF-004
- Modality: MUST
- Normative action: Final diff review also removes commented-out code, temporary logging, unintended TODO/FIXME markers and stale temporary tests or scripts.
- Trigger/scope: workflow verify (before declaring implementation complete)
- Exceptions: none
- Why EXTRA: Concrete diff-hygiene items not in the oracle.
- Evidence K0-S001703: `output/template/.claude/skills/verify/SKILL.md:63-63` — "- Also check for: accidental unrelated edits; commented-out code; temporary logging; unintended TODO/FIXME markers; stale temporary tests or scripts; architecture drift; unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md` (CLAUDE.md § Product sources); stale code, tests, docs or configuration after a `CUSTOM_SETTINGS.md` change (`custom-settings`); behavior verified manually but never …"

### EXTRA-K0-0020
- Closest oracle policies: DEP-003, ARC-001, GOV-015
- Modality: ENFORCED
- Normative action: The pre-command hook fails closed: a missing script, crash, timeout (onFailure block) or empty/invalid/unreadable hook input denies the shell command.
- Trigger/scope: PreToolUse Bash/PowerShell (hook.cjs pre-tool-use)
- Exceptions: none
- Why EXTRA: Fail-closed enforcement policy not in the oracle.
- Evidence K0-S000011: `output/template/.claude/hooks/hook.cjs:2-9` — "fail-closed: any error or unreadable input denies the command"
- Evidence K0-S000045: `output/template/.claude/hooks/hook.cjs:585-592` — "if (event === 'pre-tool-use') { ⏎     try { ⏎       preToolUse(readInput()); ⏎     } catch (error) { ⏎       preDecision('deny', [`[hook] the pre-command policy check could not run, so the command was blocked: ${error.message}`]); ⏎     } ⏎     process.exit(0); ⏎   }"
- Evidence K0-S000073: `output/template/.claude/MAP.md:182-182` — ""
- Evidence K0-S000075: `output/template/.claude/MAP.md:186-186` — ""
- Evidence K0-S000397: `output/template/.claude/settings.json:12-12` — ""onFailure": "block""

### EXTRA-K0-0021
- Closest oracle policies: ARC-001, ARC-020
- Modality: ENFORCED
- Normative action: dotnet project-reference add/remove commands (also dotnet reference add/remove and nested shell strings) are denied unless the command carries the trailing comment '# project-references: approved'; changing the reference graph is Reserved unless an accepted decision already requires it, even when the reference would be legal.
- Trigger/scope: PreToolUse Bash/PowerShell (hook.cjs pre-tool-use)
- Exceptions: Approval marker present.
- Why EXTRA: Reference-graph approval gate not in the oracle.
- Evidence K0-S000016: `output/template/.claude/hooks/hook.cjs:283-289` — "if (found.reference.length > 0 && !REFERENCE_MARKER.test(command)) { ⏎     deny.push( ⏎       `Project-reference graph change: ${found.reference.join(' | ')}`, ⏎       'Changing the project reference graph is Reserved (CLAUDE.md § Decisions) unless an accepted decision already requires the reference, even when the new reference would be legal.', ⏎       'Follow `project-structure` § Changing proje …"
- Evidence K0-S000075: `output/template/.claude/MAP.md:186-186` — ""

### EXTRA-K0-0022
- Closest oracle policies: DEP-003, DEP-004
- Modality: ENFORCED
- Normative action: After the add-dependency checks the command is re-run with the trailing comment '# add-dependency: reviewed', which lets it pass.
- Trigger/scope: PreToolUse Bash/PowerShell (hook.cjs pre-tool-use)
- Exceptions: none
- Why EXTRA: Self-declared review-marker mechanism not in the oracle.
- Evidence K0-S000017: `output/template/.claude/hooks/hook.cjs:290-294` — "if (found.dependency.length > 0 && !DEPENDENCY_MARKER.test(command)) { ⏎     deny.push( ⏎       `Dependency change detected: ${found.dependency.map((d) => d.text).join(' | ')}`, ⏎       'Run the `add-dependency` workflow first; when its checks are complete, re-run the command with the trailing comment `# add-dependency: reviewed`.', ⏎     );"
- Evidence K0-S000075: `output/template/.claude/MAP.md:186-186` — ""

### EXTRA-K0-0023
- Closest oracle policies: ARC-020, DEP-001
- Modality: ENFORCED_ADVISORY
- Normative action: A removed project or manifest returns feedback that the project graph or dependency set changed and must be confirmed as intended and approved.
- Trigger/scope: PostToolUse edits and shell commands (hook.cjs)
- Exceptions: none
- Why EXTRA: Removal-approval check not in the oracle.
- Evidence K0-S000028: `output/template/.claude/hooks/hook.cjs:464-466` — "} else if (type === 'removed') { ⏎       messages.push(`[manifest] ${rel} was removed: removing a project or manifest changes the project graph or the dependency set — confirm it was intended and approved (CLAUDE.md § Decisions; \`project-structure\`, \`add-dependency\`).`); ⏎       projectRemoved ||= rel.endsWith('.csproj');"

### EXTRA-K0-0024
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: A moved manifest (same content under a new path) returns feedback to update every reference to it.
- Trigger/scope: PostToolUse edits and shell commands (hook.cjs)
- Exceptions: none
- Why EXTRA: Move-tracking obligation not in the oracle.
- Evidence K0-S000030: `output/template/.claude/hooks/hook.cjs:468-471` — "if (type === 'moved') { ⏎         messages.push(`[manifest] ${change.from} was moved to ${rel}: update every reference to it (\`project-structure\`).`); ⏎         projectRemoved ||= rel.endsWith('.csproj'); ⏎       }"

### EXTRA-K0-0025
- Closest oracle policies: ARC-001, ARC-020
- Modality: ENFORCED_ADVISORY
- Normative action: A change to a .csproj's project references returns feedback that changing the reference graph is Reserved: confirm it was approved and recorded (architecture-decision) or revert it.
- Trigger/scope: PostToolUse edits and shell commands (hook.cjs)
- Exceptions: none
- Why EXTRA: Reference-graph approval not in the oracle.
- Evidence K0-S000032: `output/template/.claude/hooks/hook.cjs:473-477` — "const refsBefore = type === 'changed' ? change.before.refs : []; ⏎       const graphChanged = type === 'edited' ? graphHint : !sameList(refsBefore, change.after.refs); ⏎       if (rel.endsWith('.csproj') && type !== 'baseline' && graphChanged) { ⏎         messages.push(`[manifest] the project references of ${rel} changed: changing the project reference graph is Reserved (CLAUDE.md § Decisions) — c …"
- Evidence K0-S000076: `output/template/.claude/MAP.md:187-188` — ""

### EXTRA-K0-0026
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: A change to CLAUDE.md, the decision register or .claude/ instruction files runs check-instructions and returns its errors.
- Trigger/scope: repo/meta (instruction-system change)
- Exceptions: none
- Why EXTRA: Instruction-system checker invariants.
- Evidence K0-S000034: `output/template/.claude/hooks/hook.cjs:483-485` — "if (instructionsChanged && fs.existsSync(path.join(root, '.claude'))) { ⏎     for (const e of script('check-instructions.cjs').check(root).errors) messages.push(`[instructions] ${e}`); ⏎   }"
- Evidence K0-S000076: `output/template/.claude/MAP.md:187-188` — ""

### EXTRA-K0-0027
- Closest oracle policies: PST-008, PST-010, TST-009, GOV-021
- Modality: ENFORCED_ADVISORY
- Normative action: Stopping is blocked once per material state of the changed files with the co-change reminders; the same state is not reminded again and the hook never loops on its own continuation.
- Trigger/scope: Stop (hook.cjs)
- Exceptions: none
- Why EXTRA: Stop-gate mechanism not in the oracle.
- Evidence K0-S000042: `output/template/.claude/hooks/hook.cjs:573-578` — "if (reminders.length === 0) return; ⏎   const fingerprint = t.repo.hashText(reminders.map((r) => r.key).sort().join('|')); ⏎   if (readState(root, 'stop.json')?.fingerprint === fingerprint) return; // this exact state was already reminded ⏎   writeState(root, 'stop.json', { fingerprint }); ⏎   emit({ decision: 'block', reason: ['Co-change check before finishing:', ...reminders.map((r) => `- ${r.te …"
- Evidence K0-S000077: `output/template/.claude/MAP.md:189-189` — ""

### EXTRA-K0-0028
- Closest oracle policies: DEP-004, DEP-020, DEP-010
- Modality: ENFORCED_ADVISORY
- Normative action: Microsoft.Extensions.Http.Polly and Polly.Extensions.Http (use Microsoft.Extensions.Http.Resilience), Serilog.Sinks.Elasticsearch (use Elastic.Serilog.Sinks) and FluentValidation.AspNetCore (use FluentValidation.DependencyInjectionExtensions) are reported as errors.
- Trigger/scope: check-dependencies.cjs (manual run by verify/add-dependency/project-structure; post-change hook)
- Exceptions: none
- Why EXTRA: Concrete deprecated-package list not in the oracle.
- Evidence K0-S000330: `output/template/.claude/scripts/check-dependencies.cjs:17-22` — "const DEPRECATED_NUGET = { ⏎   'microsoft.extensions.http.polly': 'deprecated; use Microsoft.Extensions.Http.Resilience (D-12, add-dependency § Package-specific choices)', ⏎   'polly.extensions.http': 'deprecated; use Microsoft.Extensions.Http.Resilience (D-12, add-dependency § Package-specific choices)', ⏎   'serilog.sinks.elasticsearch': 'deprecated; use Elastic.Serilog.Sinks (logging knowledge) …"

### EXTRA-K0-0029
- Closest oracle policies: DEP-020
- Modality: ENFORCED_ADVISORY
- Normative action: A direct Polly reference produces a notice that it is an explicit exception whose reason must be documented.
- Trigger/scope: check-dependencies.cjs (manual run by verify/add-dependency/project-structure; post-change hook)
- Exceptions: Documented reason.
- Why EXTRA: Documentation obligation not in the oracle.
- Evidence K0-S000331: `output/template/.claude/scripts/check-dependencies.cjs:23-27` — "const DECISION_NUGET = { ⏎   mediatr: 'mediator-based organization is not adopted (D-02); requires an approved decision', ⏎   automapper: 'mapping framework other than the approved one (D-11); requires an approved decision', ⏎   polly: 'direct Polly is an explicit exception (add-dependency § Package-specific choices); document the reason', ⏎ };"

### EXTRA-K0-0030
- Closest oracle policies: DEP-006
- Modality: ENFORCED_ADVISORY
- Normative action: A PackageReference using VersionOverride produces a notice that it needs a concrete, reported reason.
- Trigger/scope: check-dependencies.cjs (manual run by verify/add-dependency/project-structure; post-change hook)
- Exceptions: Concrete reported reason.
- Why EXTRA: VersionOverride handling not in the oracle.
- Evidence K0-S000337: `output/template/.claude/scripts/check-dependencies.cjs:126-128` — "if (attributes.has('VersionOverride')) { ⏎       result.notices.push(`${rel}: PackageReference ${include} uses VersionOverride; it needs a concrete, reported reason (rules/common/dependencies.md § NuGet).`); ⏎     }"

### EXTRA-K0-0031
- Closest oracle policies: ARC-001
- Modality: ENFORCED_ADVISORY
- Normative action: A ProjectReference pointing to a project that does not exist is an error.
- Trigger/scope: check-dependencies.cjs (manual run by verify/add-dependency/project-structure; post-change hook)
- Exceptions: MSBuild-property paths are not checked.
- Why EXTRA: Reference-integrity check not in the oracle.
- Evidence K0-S000339: `output/template/.claude/scripts/check-dependencies.cjs:136-138` — "if (!reference.includes('$(') && !fs.existsSync(path.resolve(rootDir, path.dirname(rel), reference))) { ⏎       result.errors.push(`${rel}: ProjectReference ${reference} points to a project that does not exist (project-structure).`); ⏎     }"

### EXTRA-K0-0032
- Closest oracle policies: ARC-027
- Modality: ENFORCED_ADVISORY
- Normative action: An empty directory inside .claude/ or docs/ is an error: create directories only for real content.
- Trigger/scope: repo/meta: check-instructions.cjs (run by /template-maintenance and after instruction edits by the post-change hook)
- Exceptions: none
- Why EXTRA: Instruction-tree directory rule (repo/meta).
- Evidence K0-S000364: `output/template/.claude/scripts/check-instructions.cjs:131-131` — "if (entries.length === 0) err(relDir, 'empty directory; create directories only for real content.');"

### EXTRA-K0-0033
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: Instruction files are classified by location: no numbered/level-ordered directories, no capability contracts/manifests/slots/facets, rule files inside a scope directory, no unclassified files under .claude/ or docs/architecture/; every artifact carries the first-line 'Kind | Scope | Owner | Loading' header with known Kind/Scope, no level/capability fields, Kind matching location; OP/DEC load always; IN is read as input.
- Trigger/scope: repo/meta: check-instructions.cjs (run by /template-maintenance and after instruction edits by the post-change hook)
- Exceptions: Project-owned root build files without a header are skipped.
- Why EXTRA: Instruction-system structure invariants.
- Evidence K0-S000078: `output/template/.claude/MAP.md:190-191` — "structural predicates of this system"
- Evidence K0-S000368: `output/template/.claude/scripts/check-instructions.cjs:163-186` — "for (const rel of files) { ⏎     if (/(^|\/)\d+-[^/]*\//.test(`${rel}`) || /^\.claude\/rules\/\d/.test(rel)) err(rel, 'numbered or level-ordered directories are not used; organize by Kind and Scope.'); ⏎     if (/^\.claude\/.*(contract|manifest|slot|capabilit|facet)/i.test(rel)) err(rel, 'capability contracts, module manifests, slots or facets are not part of this system.'); ⏎     if (/^\.claude\/ …"
- Evidence K0-S000370: `output/template/.claude/scripts/check-instructions.cjs:194-209` — "for (const a of artifacts) { ⏎     if (!KINDS.includes(a.kind)) err(a.rel, `unknown Kind "${a.kind}".`); ⏎     if (!SCOPES.includes(a.scope)) err(a.rel, `unknown Scope "${a.scope}".`); ⏎     if (FORBIDDEN_FIELD.test(a.header)) err(a.rel, 'header carries a level/capability field; this system classifies by Kind and Scope only.'); ⏎     if (!a.code) { ⏎       a.prose = fences(a.body, (line, message)  …"

### EXTRA-K0-0034
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: Standards live directly in .claude/rules/<scope>/<topic>.md with matching Scope, are path-scoped with non-empty paths inside the scope territory, and contain no numbered procedures or Step/Procedure headings.
- Trigger/scope: repo/meta: check-instructions.cjs (run by /template-maintenance and after instruction edits by the post-change hook)
- Exceptions: none
- Why EXTRA: Standard-placement invariants.
- Evidence K0-S000371: `output/template/.claude/scripts/check-instructions.cjs:211-223` — "if (a.expected === 'STD') { ⏎       const dir = a.rel.split('/')[2]; ⏎       if (a.rel.split('/').length !== 4) err(a.rel, 'standards live directly in .claude/rules/<scope>/<topic>.md.'); ⏎       if (!RULE_SCOPES.includes(dir)) err(a.rel, `rules directory "${dir}" is not a scope (${RULE_SCOPES.join(', ')}).`); ⏎       if (dir !== a.scope) err(a.rel, `Scope ${a.scope} does not match its directory $ …"

### EXTRA-K0-0035
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: Skills: frontmatter name equals the directory, concrete description (20+ characters), KNW loads on demand and stays model-invocable, WF loads as a workflow, required workflows and knowledge skills exist with the right Kind, template-maintenance sets disable-model-invocation: true.
- Trigger/scope: repo/meta: check-instructions.cjs (run by /template-maintenance and after instruction edits by the post-change hook)
- Exceptions: none
- Why EXTRA: Skill-structure invariants.
- Evidence K0-S000372: `output/template/.claude/scripts/check-instructions.cjs:225-241` — "if (a.expected === 'SKILL') { ⏎       const name = a.rel.split('/')[2]; ⏎       if (a.fm.name !== name) err(a.rel, `frontmatter name "${a.fm.name}" must equal the directory name "${name}".`); ⏎       if (!a.fm.description || String(a.fm.description).length < 20) err(a.rel, 'skill needs a concrete description.'); ⏎       const userOnly = String(a.fm['disable-model-invocation']).toLowerCase() === 't …"
- Evidence K0-S000377: `output/template/.claude/scripts/check-instructions.cjs:264-265` — "for (const required of REQUIRED_WORKFLOWS) if (!exists(`.claude/skills/${required}/SKILL.md`)) err('.claude/skills', `required workflow "${required}" is missing.`); ⏎   for (const required of REQUIRED_KNOWLEDGE) if (!exists(`.claude/skills/${required}/SKILL.md`)) err('.claude/skills', `required knowledge skill "${required}" is missing.`);"

### EXTRA-K0-0036
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: A skill's references/ files share its Kind, state that only the skill reads them, and are referenced only from that skill.
- Trigger/scope: repo/meta: check-instructions.cjs (run by /template-maintenance and after instruction edits by the post-change hook)
- Exceptions: none
- Why EXTRA: Private-reference invariant.
- Evidence K0-S000373: `output/template/.claude/scripts/check-instructions.cjs:243-247` — "if (a.expected === 'REFERENCE') { ⏎       const owner = byRel.get(`.claude/skills/${a.rel.split('/')[2]}/SKILL.md`); ⏎       if (owner && owner.kind !== a.kind) err(a.rel, `private reference Kind ${a.kind} differs from its skill (${owner.kind}).`); ⏎       if (!a.loading.includes('only')) err(a.rel, 'private reference must state that only its skill reads it.'); ⏎     }"

### EXTRA-K0-0037
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: A knowledge-skill or knowledge-reference line using must/never/requires approval without an owner reference (rules/, CLAUDE.md or a D-xx ID) is an error: move the rule to its standard and point to it.
- Trigger/scope: repo/meta: check-instructions.cjs (run by /template-maintenance and after instruction edits by the post-change hook)
- Exceptions: Lines citing an owner.
- Why EXTRA: Knowledge-normativity invariant.
- Evidence K0-S000374: `output/template/.claude/scripts/check-instructions.cjs:249-255` — "if ((a.expected === 'SKILL' || a.expected === 'REFERENCE') && a.kind === 'KNW') { ⏎       a.prose.split('\n').forEach((line, i) => { ⏎         if (/\b(must|never|requires approval)\b/i.test(line) && !/(rules\/|CLAUDE\.md|D-\d\d)/.test(line)) { ⏎           err(a.rel, `line ${i + 1 + a.offset}: normative wording in knowledge without an owner reference; move the rule to its standard and point to it.` …"

### EXTRA-K0-0038
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: Exactly one Kind DEC register (docs/architecture/decision-register.md); CLAUDE.md imports exactly that register; rows are 'ID | Decision | Details in | Affects' with unique D-xx IDs and non-empty summaries; Affects targets exist, are not duplicated and are STD/KNW/WF/ENF; Details-in targets exist and are listed in Affects; the Decision cell does not depend on rules/skills/scripts.
- Trigger/scope: repo/meta: check-instructions.cjs (run by /template-maintenance and after instruction edits by the post-change hook)
- Exceptions: none
- Why EXTRA: Decision-register invariants.
- Evidence K0-S000381: `output/template/.claude/scripts/check-instructions.cjs:285-314` — "const decArtifacts = artifacts.filter((a) => a.kind === 'DEC'); ⏎   if (decArtifacts.length !== 1 || decArtifacts[0].rel !== REGISTER) err(REGISTER, `exactly one decision register (${REGISTER}) must carry Kind DEC; found ${decArtifacts.map((a) => a.rel).join(', ') || 'none'}.`); ⏎   const imports = exists('CLAUDE.md') ? [...read('CLAUDE.md').matchAll(/^@(\S+)\s*$/gm)].map((m) => m[1]) : []; ⏎   if …"

### EXTRA-K0-0039
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: An artifact citing D-xx must be listed in that decision's Affects; decision rows exist only in the register; artifacts must not restate a decision (8-word overlap) but cite its ID.
- Trigger/scope: repo/meta: check-instructions.cjs (run by /template-maintenance and after instruction edits by the post-change hook)
- Exceptions: none
- Why EXTRA: Decision-citation invariants.
- Evidence K0-S000382: `output/template/.claude/scripts/check-instructions.cjs:316-335` — "for (const a of artifacts) { ⏎     if (a.rel === REGISTER) continue; ⏎     for (const id of new Set([...a.body.matchAll(/\bD-\d\d\b/g)].map((m) => m[0]))) { ⏎       const d = decisions.get(id); ⏎       if (!d) err(a.rel, `cites unknown decision ${id}.`); ⏎       else if (!d.affects.includes(registerKey(a.rel))) err(a.rel, `cites ${id} but is not listed in its Affects (${registerKey(a.rel)}).`); ⏎  …"

### EXTRA-K0-0040
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: References must resolve (no retired or unknown skill names; section references must exist; private references stay private); non-routing references follow the conformance direction WF → KNW → STD → DEC → OP, ENF → STD/DEC, and the dependency graph is acyclic.
- Trigger/scope: repo/meta: check-instructions.cjs (run by /template-maintenance and after instruction edits by the post-change hook)
- Exceptions: Routing pointers (See also/Workflow/Technique/Procedure/Enforced by/Loading labels, invocations, routing sections, imports, register Details in/Affects cells, enforcement messages) may point anywhere.
- Why EXTRA: Conformance-direction invariant.
- Evidence K0-S000361: `output/template/.claude/scripts/check-instructions.cjs:26-29` — "Conformance direction WF → KNW → STD → DEC → OP"
- Evidence K0-S000385: `output/template/.claude/scripts/check-instructions.cjs:411-465` — "const edges = []; ⏎   for (const a of artifacts) { ⏎     const lines = a.code ? a.body.split('\n') : a.prose.split('\n'); ⏎     let routingSection = false; ⏎     lines.forEach((line, index) => { ⏎       const lineNo = index + 1 + a.offset; ⏎       if (!a.code && /^#{1,6}\s/.test(line)) routingSection = /routing/i.test(line); ⏎       const isComment = a.code && /^\s*(\/\/|#|<!--)/.test(line); ⏎     …"

### EXTRA-K0-0041
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: Manual tool invocations in instruction files and the map must not be relative to the current directory; use node "$(git rev-parse --show-toplevel)/.claude/…".
- Trigger/scope: repo/meta: check-instructions.cjs (run by /template-maintenance and after instruction edits by the post-change hook)
- Exceptions: none
- Why EXTRA: Command-form invariant.
- Evidence K0-S000386: `output/template/.claude/scripts/check-instructions.cjs:467-472` — "// Manual tool invocations must work from any directory of the repository or worktree. ⏎   for (const rel of [...artifacts.map((a) => a.rel), ...(exists(MAP) ? [MAP] : [])]) { ⏎     read(rel).split('\n').forEach((line, i) => { ⏎       if (CWD_RELATIVE_COMMAND.test(line)) err(rel, `line ${i + 1}: tool invocation is relative to the current directory; use node "$(git rev-parse --show-toplevel)/.claud …"

### EXTRA-K0-0042
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: settings.json hooks are exec-form command hooks (executable-only command, args [${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>, <event>], existing script handling the event, no variable expansion in further args, positive timeout); onFailure only as block on PreToolUse; the four required registrations exist with matchers covering their tools and the PreToolUse policy hook fails closed.
- Trigger/scope: repo/meta: check-instructions.cjs (run by /template-maintenance and after instruction edits by the post-change hook)
- Exceptions: none
- Why EXTRA: Hook-configuration invariants.
- Evidence K0-S000388: `output/template/.claude/scripts/check-instructions.cjs:478-514` — "if (!exists('.claude/settings.json')) { ⏎     err('.claude/settings.json', 'settings with hook configuration are missing.'); ⏎   } else { ⏎     let settings = null; ⏎     try { settings = JSON.parse(read('.claude/settings.json')); } catch (e) { err('.claude/settings.json', `invalid JSON: ${e.message}`); } ⏎     const registrations = []; ⏎     for (const [event, groups] of Object.entries(settings?. …"

### EXTRA-K0-0043
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: .claude/MAP.md exists, states it is not loaded, lists every artifact plus SPECIFICATION.md and settings.json, and its Decision → Affects view matches the register.
- Trigger/scope: repo/meta: check-instructions.cjs (run by /template-maintenance and after instruction edits by the post-change hook)
- Exceptions: none
- Why EXTRA: Map-maintenance invariant.
- Evidence K0-S000070: `output/template/.claude/MAP.md:159-159` — "verifies that this view matches it"
- Evidence K0-S000390: `output/template/.claude/scripts/check-instructions.cjs:520-534` — "if (!exists(MAP)) { ⏎     err(MAP, 'human-facing instruction map is missing.'); ⏎   } else { ⏎     const map = read(MAP); ⏎     if (!/^> Instruction map \|.*\| Loading: not loaded/.test(map)) err(MAP, 'map header must state that the map is not loaded.'); ⏎     for (const a of artifacts) if (!map.includes(a.rel)) err(MAP, `does not list ${a.rel}.`); ⏎     for (const extra of ['SPECIFICATION.md', '. …"

### EXTRA-K0-0044
- Closest oracle policies: RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: UTF-8 charset, final newline, trimmed trailing whitespace (not in Markdown), space indentation of 4 (2 for JSON/YAML/TS/HTML/SCSS/CSS/project/XML/config files).
- Trigger/scope: all files (.editorconfig; C# rules for *.cs)
- Exceptions: none
- Why EXTRA: Concrete formatting settings not in the oracle.
- Evidence K0-S000401: `output/template/.editorconfig:4-15` — "[*] ⏎ charset = utf-8 ⏎ insert_final_newline = true ⏎ trim_trailing_whitespace = true ⏎ indent_style = space ⏎ indent_size = 4 ⏎  ⏎ [*.{json,yml,yaml,ts,html,scss,css,csproj,props,targets,slnx,xml,config}] ⏎ indent_size = 2 ⏎  ⏎ [*.md] ⏎ trim_trailing_whitespace = false"

### EXTRA-K0-0045
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: System directives sorted first; using directives placed outside the namespace (suggestion).
- Trigger/scope: all files (.editorconfig; C# rules for *.cs)
- Exceptions: none
- Why EXTRA: Using-placement settings not in the oracle.
- Evidence K0-S000405: `output/template/.editorconfig:20-21` — "dotnet_sort_system_directives_first = true ⏎ csharp_using_directive_placement = outside_namespace:suggestion"

### EXTRA-K0-0046
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: var suggested when the type is apparent; not enforced for built-in types or elsewhere (silent).
- Trigger/scope: all files (.editorconfig; C# rules for *.cs)
- Exceptions: none
- Why EXTRA: var style settings not in the oracle.
- Evidence K0-S000409: `output/template/.editorconfig:26-28` — "csharp_style_var_when_type_is_apparent = true:suggestion ⏎ csharp_style_var_for_built_in_types = false:silent ⏎ csharp_style_var_elsewhere = false:silent"

### EXTRA-K0-0047
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: Primary constructors (silent), collection expressions, switch expressions and pattern matching are suggested.
- Trigger/scope: all files (.editorconfig; C# rules for *.cs)
- Exceptions: none
- Why EXTRA: Modern-syntax preferences not in the oracle.
- Evidence K0-S000411: `output/template/.editorconfig:31-34` — "csharp_style_prefer_primary_constructors = true:silent ⏎ dotnet_style_prefer_collection_expression = when_types_loosely_match:suggestion ⏎ csharp_style_prefer_switch_expression = true:suggestion ⏎ csharp_style_prefer_pattern_matching = true:suggestion"

### EXTRA-K0-0048
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: Open braces on new lines; braces suggested when multiline.
- Trigger/scope: all files (.editorconfig; C# rules for *.cs)
- Exceptions: none
- Why EXTRA: Brace/layout settings not in the oracle.
- Evidence K0-S000413: `output/template/.editorconfig:37-38` — "csharp_new_line_before_open_brace = all ⏎ csharp_prefer_braces = when_multiline:suggestion"

### EXTRA-K0-0049
- Closest oracle policies: RUN-009, RUN-024
- Modality: ENFORCED_ADVISORY
- Normative action: PascalCase for types and members and camelCase for parameters and locals (suggestion).
- Trigger/scope: all files (.editorconfig; C# rules for *.cs)
- Exceptions: none
- Why EXTRA: Naming rules not in the oracle.
- Evidence K0-S000415: `output/template/.editorconfig:41-51` — "dotnet_naming_symbols.types_and_members.applicable_kinds = class, struct, interface, enum, delegate, method, property, event ⏎ dotnet_naming_style.pascal_case.capitalization = pascal_case ⏎ dotnet_naming_rule.types_and_members_pascal_case.symbols = types_and_members ⏎ dotnet_naming_rule.types_and_members_pascal_case.style = pascal_case ⏎ dotnet_naming_rule.types_and_members_pascal_case.severity =  …"

### EXTRA-K0-0050
- Closest oracle policies: none
- Modality: MUST
- Normative action: Place instruction content by Kind: OP (CLAUDE.md, always; only agent-behaviour policy needed at planning time), DEC (single decision register with D-xx IDs, optional ADRs in docs/decisions/; changed via architecture-decision), STD (normative rules per scope in .claude/rules/<scope>/<topic>.md, path-scoped), KNW (technique/examples in skills, on demand), WF (procedures in skills/agents), ENF (settings, hooks, scripts, root build/format assets), IN (product inputs; product content only, never engineering policy).
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Instruction-system placement rules.
- Evidence K0-S000053: `output/template/.claude/MAP.md:14-20` — "| OP — Operating Policy | precedence, product governance, decision protocol, challenge obligation, Git safety, workflow routing | `CLAUDE.md` | always | only agent-behavior policy needed at planning time | ⏎ | DEC — Project Decisions | architecture, patterns not adopted, stack, conditional technologies, project defaults | `docs/architecture/decision-register.md` (one register, `D-xx` IDs); optiona …"
- Evidence K0-S001657: `output/template/.claude/skills/template-maintenance/SKILL.md:17-18` — "1. **What is it?** Operating policy → OP; project/architecture decision → DEC; normative rule for a scope → STD; technique or examples → KNW; multi-step procedure → WF; mechanical check or delivery asset → ENF; product requirement or tunable value → IN (product input, not an instruction). ⏎ 2. **Where does it apply?** `common`, `backend`, `backend-tests`, `frontend`, `delivery` or `repo/meta`."
- Evidence K0-S001659: `output/template/.claude/skills/template-maintenance/SKILL.md:22-28` — "| OP | `CLAUDE.md` | always | ⏎ | DEC | `docs/architecture/decision-register.md` (+ ADRs in `docs/decisions/`) | always (imported) | ⏎ | STD | `.claude/rules/<scope>/<topic>.md` with `paths:` inside the scope's territory | path-scoped | ⏎ | KNW | `.claude/skills/<name>/SKILL.md` (+ private `references/`) | on demand | ⏎ | WF | `.claude/skills/<name>/SKILL.md`, `.claude/agents/<name>.md` | workflow …"

### EXTRA-K0-0051
- Closest oracle policies: none
- Modality: MUST
- Normative action: Conformance dependencies point WF → KNW → STD → DEC → OP and ENF → STD/DEC; enforcement declares its conformance in its header and 'Conforms to:' lines; other references are routing pointers only in the listed forms; a skill's references/ files are read only by that skill; standards cite decision IDs instead of restating decisions; decision summaries exist only in the register.
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Instruction-system conformance rules.
- Evidence K0-S000054: `output/template/.claude/MAP.md:22-22` — "Conformance dependencies point WF → KNW → STD → DEC → OP, and ENF → STD/DEC; enforcement declares its conformance in its header and in `Conforms to:` comment lines. Routing pointers may point anywhere reliably invocable: references after `See also:`, `Workflow:`, `Technique:`, `Procedure:` or `Enforced by:`, workflow invocations (run, use, invoke, switch to, `→`, slash commands, agent delegation), …"
- Evidence K0-S001665: `output/template/.claude/skills/template-maintenance/SKILL.md:39-39` — "Conformance dependencies run WF → KNW → STD → DEC → OP; ENF → STD/DEC, declared in its header or a `Conforms to:` comment line. Standards cite decision IDs (`D-xx`) instead of restating decisions; decision summaries exist only in the register. Routing pointers may point anywhere reliably invocable; write them explicitly — after `See also:`, `Workflow:`, `Technique:`, `Procedure:` or `Enforced by:` …"

### EXTRA-K0-0052
- Closest oracle policies: none
- Modality: MUST
- Normative action: Standard path globs stay inside their scope territory (common any; backend backend/ and root .NET build files; backend-tests backend/ test paths; frontend frontend/; delivery Docker/Compose/CI paths); repo/meta has no standards.
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Scope-territory rule.
- Evidence K0-S000057: `output/template/.claude/MAP.md:28-33` — "| `common` | everything | any glob | ⏎ | `backend` | `backend/<Name>.<Layer>/...` and root .NET build files | `backend/`, `Directory.Build.props`, `Directory.Packages.props`, `global.json`, `*.slnx` | ⏎ | `backend-tests` | backend test projects (`backend/<Name>.<Layer>.Tests/`, `backend/<Name>.IntegrationTests/`) | `backend/` and containing `Tests` | ⏎ | `frontend` | `frontend/<Name>.Web/...` | `f …"
- Evidence K0-S001657: `output/template/.claude/skills/template-maintenance/SKILL.md:17-18` — "1. **What is it?** Operating policy → OP; project/architecture decision → DEC; normative rule for a scope → STD; technique or examples → KNW; multi-step procedure → WF; mechanical check or delivery asset → ENF; product requirement or tunable value → IN (product input, not an instruction). ⏎ 2. **Where does it apply?** `common`, `backend`, `backend-tests`, `frontend`, `delivery` or `repo/meta`."

## LINK_UNCERTAIN constraints (1)

### UNCERTAIN-K0-0001
- Closest oracle policies: GOV-015
- Modality: ALLOWED
- Normative action: High-risk operations (reset --hard, clean, push --force, push --force-with-lease, branch deletion, rebasing shared history) run only when explicitly requested or required by an approved workflow.
- Trigger/scope: workflow git-workflow (any Git operation)
- Exceptions: Explicit request or approved workflow.
- Open question: Open question: GOV-015 permits repository-changing Git operations only when explicitly requested; whether 'required by an approved workflow' widens that condition or only describes an explicitly requested workflow cannot be decided from the text.
- Evidence K0-S001166: `output/template/.claude/skills/git-workflow/SKILL.md:73-73` — "`git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion and rebasing shared history are high-risk: run them only when explicitly requested or required by an approved workflow, and inspect what will be lost or rewritten first."

