# EXTRA and LINK_UNCERTAIN constraints — candidate K1

Generated deterministically from the annotation ledger. Each entry cites the exact
source evidence (path, line range, verbatim quote). `policy_ids` on an EXTRA entry
name the closest oracle policy only; origin stays EXTRA.

## EXTRA constraints (274)

### EXTRA-K1-0001
- Closest oracle policies: none
- Modality: MUST
- Normative action: Vocabulary: a must/must-not violation is a defect; a deviation from a 'default' needs a concrete reason and must be reported; prefer/avoid are guidance; 'requires approval' marks a Reserved decision.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Reporting obligation for default deviations is not in the oracle.
- Evidence K1-S000575: `output/template/CLAUDE.md:11-11` — "**must / must not** — a violation is a defect. **Default** — deviation needs a concrete reason and must be reported. **Prefer / avoid** — guidance. **Requires approval** — a Reserved decision (see Decision control)."
- Evidence K1-S001754: `output/template/.claude/skills/template-maintenance/SKILL.md:36-36` — "must / must not"

### EXTRA-K1-0002
- Closest oracle policies: GOV-001, GOV-008
- Modality: MUST_NOT
- Normative action: Product, feature and task inputs may request a decision change but must not silently override engineering policy or recorded decisions.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Product-input vs engineering-policy precedence not stated in the oracle.
- Evidence K1-S000586: `output/template/CLAUDE.md:24-24` — "- Product, feature, and task inputs may request a decision change; they must not silently override engineering policy or recorded decisions."

### EXTRA-K1-0003
- Closest oracle policies: ARC-020, ARC-001
- Modality: REQUIRES_APPROVAL
- Normative action: Changing the project reference graph is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Not gated by ARC-020.
- Evidence K1-S000594: `output/template/CLAUDE.md:35-35` — "3. adding a production project, layer, or assembly, or changing the project reference graph;"

### EXTRA-K1-0004
- Closest oracle policies: ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Adding search, external storage or external identity infrastructure is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Beyond ARC-020's list.
- Evidence K1-S000596: `output/template/CLAUDE.md:37-37` — "5. adding an infrastructure category: messaging, background processing, distributed cache, search, external storage, external identity;"

### EXTRA-K1-0005
- Closest oracle policies: DEP-001, GOV-013
- Modality: REQUIRES_APPROVAL
- Normative action: Adding a major library or framework is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: The oracle requires a concrete need, not approval.
- Evidence K1-S000597: `output/template/CLAUDE.md:38-38` — "6. adding a major library or framework, or replacing approved baseline technology;"

### EXTRA-K1-0006
- Closest oracle policies: ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Introducing a project-wide convention or abstraction that other code is expected to follow is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Generalizes ARC-020's project-wide Result example.
- Evidence K1-S000598: `output/template/CLAUDE.md:39-39` — "7. introducing a project-wide convention or abstraction that other code is expected to follow;"

### EXTRA-K1-0007
- Closest oracle policies: API-013, DEP-017
- Modality: REQUIRES_APPROVAL
- Normative action: Adopting API versioning is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: API-013 requires a concrete need, not approval.
- Evidence K1-S000600: `output/template/CLAUDE.md:41-41` — "9. a breaking public API change or adopting API versioning;"
- Evidence K1-S000756: `output/template/.claude/skills/api-versioning/SKILL.md:13-13` — "Policy: `.claude/rules/backend/api-contracts.md`. Adopting versioning is Reserved (`architecture-decision`); its package is added through `add-dependency`; deprecation steps: `development-workflow`. Versioning belongs to the API contract, not to Domain or Application."
- Evidence K1-S001113: `output/template/.claude/skills/development-workflow/SKILL.md:44-44` — "- **Deprecating an externally consumed API version:** mark the deprecation in versioning metadata, document the replacement version, communicate a realistic migration period and removal timeline, and keep the old version working for the promised support period; never remove it without considering its published support contract. Breaking changes and adopting versioning are Reserved (`architecture-d …"

### EXTRA-K1-0008
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST
- Normative action: An explicit user instruction counts as approval; the accepted decision must still be recorded through architecture-decision.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Recording obligation added to GOV-017.
- Evidence K1-S000604: `output/template/CLAUDE.md:45-45` — "- For a Reserved choice, raise a Decision Request through `architecture-decision` and do not implement it before approval. An explicit user instruction counts as approval; the accepted decision must still be recorded through `architecture-decision`."

### EXTRA-K1-0009
- Closest oracle policies: none
- Modality: MUST
- Normative action: Changes to this instruction system are governed by template-maintenance, which is user-invoked only.
- Trigger/scope: repo/meta (instruction-system change)
- Exceptions: none
- Why EXTRA: Instruction-system maintenance gate not in the oracle.
- Evidence K1-S000620: `output/template/CLAUDE.md:79-79` — "Path-scoped standards in `.claude/rules/<scope>/` load when matching files are read; knowledge skills load on demand. `template-maintenance` (user-invoked only) governs changes to this instruction system."
- Evidence K1-S000790: `output/template/.claude/skills/architecture-decision/SKILL.md:42-42` — "3. When the decision changes instruction content (standards, knowledge, workflows), ask the user to run the user-invoked `template-maintenance` workflow; afterwards run `node "<root>/.claude/scripts/check-instructions.cjs"` (`<root>`: the active repository root; command form in `verify`, Risk-scoped checks)."
- Evidence K1-S001741: `output/template/.claude/skills/template-maintenance/SKILL.md:7-7` — "disable-model-invocation: true"
- Evidence K1-S001745: `output/template/.claude/skills/template-maintenance/SKILL.md:14-14` — "Use only when the user explicitly asks to change the instruction system. Maintainer overview: `.claude/MAP.md`."

### EXTRA-K1-0010
- Closest oracle policies: DEP-023, RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: Shared build settings Nullable enable and ImplicitUsings enable.
- Trigger/scope: all .NET projects (MSBuild import)
- Exceptions: none
- Why EXTRA: Concrete compiler settings not in the oracle.
- Evidence K1-S000630: `output/template/Directory.Build.props:7-8` — "<Nullable>enable</Nullable> ⏎     <ImplicitUsings>enable</ImplicitUsings>"

### EXTRA-K1-0011
- Closest oracle policies: ARC-020
- Modality: MUST
- Normative action: Static composition: exactly one implementation per required capability slot and zero or one for the optional slot; unselected implementations are not part of the runtime; each module manifest lists its facets.
- Trigger/scope: repo/meta (capability selection)
- Exceptions: none
- Why EXTRA: Capability-slot composition rule not in the oracle.
- Evidence K1-S000134: `output/template/.claude/MAP.md:141-141` — "one implementation per required slot"
- Evidence K1-S000643: `output/template/docs/architecture/decision-register.md:10-10` — "Static composition: exactly one implementation per required slot and zero or one for the optional slot; unselected implementations are not part of the runtime. Each manifest lists its facets: `.claude/capabilities/<slot>/<implementation>/MODULE.md`."
- Evidence K1-S000793: `output/template/.claude/skills/architecture-decision/SKILL.md:47-47` — "Capability slots (architecture, persistence, backend-testing, frontend) compose statically; a selection change is Reserved."

### EXTRA-K1-0012
- Closest oracle policies: GOV-007, GOV-017
- Modality: MUST
- Normative action: Accepted decisions are recorded in the register by architecture-decision, with optional detailed records in docs/decisions/.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Decision-recording mechanism not in the oracle.
- Evidence K1-S000667: `output/template/docs/architecture/decision-register.md:46-46` — "Recorded by `architecture-decision`; optional detailed records live in `docs/decisions/`."

### EXTRA-K1-0013
- Closest oracle policies: ARC-001, ARC-020
- Modality: MUST
- Normative action: The architecture slot is a required frame with exactly one implementation that binds no slot and defines the stable role vocabulary; placement belongs to the frame and technique to the leaves; an implementation must provide role map, dependency direction, domain modeling, use-case orchestration, commit-boundary placement, composition root, transport contracts, test-project placement, not-adopted styles, scaffold layout and a deterministic reference check.
- Trigger/scope: repo/meta (capability slots)
- Exceptions: none
- Why EXTRA: Capability contract not in the oracle.
- Evidence K1-S000009: `output/template/.claude/capabilities/architecture/clean-architecture/MODULE.md:5-9` — "Slot: architecture"
- Evidence K1-S000015: `output/template/.claude/capabilities/architecture/clean-architecture/MODULE.md:25-35` — "`reference-check`"
- Evidence K1-S000018: `output/template/.claude/capabilities/architecture/CONTRACT.md:5-8` — "- Slot type: required frame ⏎ - Cardinality: exactly one implementation ⏎ - Binds: — (the frame binds no slot; leaves bind to it) ⏎ - Stable role vocabulary usable by non-slot artifacts: Domain, Application, Infrastructure, Api (host and composition root), Application Service, repository contract, Unit of Work (`IUnitOfWork`, commit boundary), test projects."
- Evidence K1-S000019: `output/template/.claude/capabilities/architecture/CONTRACT.md:10-10` — "Placement belongs to the frame; technique belongs to the leaves (persistence, backend-testing), which declare their frame bindings with `Binds:`."
- Evidence K1-S000022: `output/template/.claude/capabilities/architecture/CONTRACT.md:16-26` — "| `role-map` | The concrete projects for each backend role under `backend/<Name>.<Layer>/` | ⏎ | `dependency-direction` | Allowed and forbidden references between roles | ⏎ | `domain-modeling` | The default domain modeling style and when richer modeling needs approval | ⏎ | `use-case-orchestration` | The default orchestration mechanism for use cases | ⏎ | `commit-boundary-placement` | Where the co …"
- Evidence K1-S000189: `output/template/.claude/rules/backend/architecture-style.md:10-10` — "Placement belongs to this frame"

### EXTRA-K1-0014
- Closest oracle policies: none
- Modality: MUST
- Normative action: Every implementation provides exactly the slot contract's role-named facet locations (DEC selection row, STD, KNW named in the register, WF, ENF); file names never change with the implementation; module manifests list their facets and contract coverage.
- Trigger/scope: repo/meta (capability slots)
- Exceptions: none
- Why EXTRA: Facet-role convention not in the oracle.
- Evidence K1-S000012: `output/template/.claude/capabilities/architecture/clean-architecture/MODULE.md:15-19` — "role map, dependency direction"
- Evidence K1-S000024: `output/template/.claude/capabilities/architecture/CONTRACT.md:30-30` — "Role-named facet locations; every implementation provides exactly these (file names never change with the implementation)."
- Evidence K1-S000026: `output/template/.claude/capabilities/architecture/CONTRACT.md:34-38` — "| DEC | common | `docs/architecture/decision-register.md` (capability-selection row) | ⏎ | STD | backend | `.claude/rules/backend/architecture-style.md` | ⏎ | STD | backend-tests | `.claude/rules/backend-tests/test-projects.md` | ⏎ | WF | backend | `.claude/skills/project-structure/references/backend-layout.md` | ⏎ | ENF | backend | `.claude/scripts/facets/architecture-style.cjs` |"
- Evidence K1-S000035: `output/template/.claude/capabilities/backend-testing/CONTRACT.md:23-23` — "Role-named facet locations; every implementation provides exactly these (file names never change with the implementation)."
- Evidence K1-S000037: `output/template/.claude/capabilities/backend-testing/CONTRACT.md:27-31` — "| DEC | common | `docs/architecture/decision-register.md` (capability-selection row) | ⏎ | STD | backend-tests | `.claude/rules/backend-tests/test-framework.md` | ⏎ | KNW | backend-tests | knowledge facet named in the decision register | ⏎ | WF | backend-tests | `.claude/skills/project-structure/references/test-setup.md` | ⏎ | ENF | backend-tests | `.claude/scripts/facets/test-framework.cjs` |"
- Evidence K1-S000043: `output/template/.claude/capabilities/backend-testing/nunit/MODULE.md:15-19` — "default framework standard"
- Evidence K1-S000052: `output/template/.claude/capabilities/frontend/angular/MODULE.md:15-19` — "workspace scaffolding"
- Evidence K1-S000064: `output/template/.claude/capabilities/frontend/CONTRACT.md:24-24` — "Role-named facet locations; every implementation provides exactly these (file names never change with the implementation)."
- Evidence K1-S000066: `output/template/.claude/capabilities/frontend/CONTRACT.md:28-32` — "| DEC | common | `docs/architecture/decision-register.md` (capability-selection row) | ⏎ | STD | frontend | `.claude/rules/frontend/frontend-framework.md` | ⏎ | KNW | frontend | knowledge facet named in the decision register | ⏎ | WF | frontend | `.claude/skills/project-structure/references/frontend-setup.md` | ⏎ | ENF | frontend | `.claude/scripts/facets/frontend-framework.cjs` |"
- Evidence K1-S000076: `output/template/.claude/capabilities/persistence/CONTRACT.md:28-28` — "Role-named facet locations; every implementation provides exactly these (file names never change with the implementation)."
- Evidence K1-S000078: `output/template/.claude/capabilities/persistence/CONTRACT.md:32-36` — "| DEC | common | `docs/architecture/decision-register.md` (capability-selection row) | ⏎ | STD | backend | `.claude/rules/backend/persistence-technology.md` | ⏎ | KNW | backend | knowledge facet named in the decision register | ⏎ | WF | backend | `.claude/skills/persistence-change/SKILL.md` | ⏎ | ENF | backend | `.claude/scripts/facets/persistence-technology.cjs` |"
- Evidence K1-S000085: `output/template/.claude/capabilities/persistence/ef-core/MODULE.md:15-19` — "inner-layer package leak check"

### EXTRA-K1-0015
- Closest oracle policies: TST-001, DEP-013
- Modality: MUST
- Normative action: The backend-testing slot is a required leaf with exactly one implementation bound to the architecture frame; the framework-neutral testing standard stays unchanged on replacement and the knowledge facet keeps the name dotnet-testing; an implementation must provide a framework standard, integration-host binding, knowledge, test scaffold and a check flagging additional test frameworks.
- Trigger/scope: repo/meta (capability slots)
- Exceptions: none
- Why EXTRA: Capability contract not in the oracle.
- Evidence K1-S000029: `output/template/.claude/capabilities/backend-testing/CONTRACT.md:5-7` — "- Slot type: required leaf ⏎ - Cardinality: exactly one implementation ⏎ - Binds: architecture (test-project placement and references belong to the frame)"
- Evidence K1-S000030: `output/template/.claude/capabilities/backend-testing/CONTRACT.md:9-9` — "The framework-neutral testing standard (`.claude/rules/backend-tests/testing.md`) stays unchanged when the implementation is replaced. The knowledge facet keeps the shared skill name `dotnet-testing`."
- Evidence K1-S000033: `output/template/.claude/capabilities/backend-testing/CONTRACT.md:15-19` — "| `framework-standard` | The default-framework standard for backend tests | ⏎ | `integration-host-binding` | How integration tests host the API (declared property) | ⏎ | `knowledge` | The `dotnet-testing` knowledge facet | ⏎ | `test-scaffold` | A scaffolding facet for creating test projects | ⏎ | `framework-consistency-check` | A deterministic check that flags additional test frameworks |"
- Evidence K1-S000040: `output/template/.claude/capabilities/backend-testing/nunit/MODULE.md:5-9` — "Slot: backend-testing"
- Evidence K1-S000046: `output/template/.claude/capabilities/backend-testing/nunit/MODULE.md:25-29` — "`framework-consistency-check`"

### EXTRA-K1-0016
- Closest oracle policies: DEP-014, DEP-024
- Modality: MUST
- Normative action: The frontend slot is an optional leaf with zero or one implementation ('none' means no workspace, no facets and a register row recording none) in frontend/<Name>.Web/; neutral frontend standards stay unchanged on replacement; an implementation must provide stack properties, framework standard, knowledge, workspace scaffold and a package.json library check; with 'none' the facet locations are absent and pointers to them stay dormant.
- Trigger/scope: repo/meta (capability slots)
- Exceptions: none
- Why EXTRA: Capability contract not in the oracle.
- Evidence K1-S000049: `output/template/.claude/capabilities/frontend/angular/MODULE.md:5-9` — "Slot: frontend"
- Evidence K1-S000055: `output/template/.claude/capabilities/frontend/angular/MODULE.md:25-29` — "`library-check`"
- Evidence K1-S000058: `output/template/.claude/capabilities/frontend/CONTRACT.md:5-8` — "- Slot type: optional leaf ⏎ - Cardinality: zero or one implementation; "none" means no frontend workspace, no facets, and the register row records `none` ⏎ - Workspace location: `frontend/<Name>.Web/` (shared layout convention) ⏎ - Binds: — (independent leaf)"
- Evidence K1-S000059: `output/template/.claude/capabilities/frontend/CONTRACT.md:10-10` — "The framework-neutral frontend standards (`.claude/rules/frontend/frontend.md`, `.claude/rules/frontend/security.md`, `.claude/rules/frontend/dependencies.md`) stay unchanged when the implementation is replaced."
- Evidence K1-S000062: `output/template/.claude/capabilities/frontend/CONTRACT.md:16-20` — "| `stack-properties` | Declared stack and libraries not added by default (decision register) | ⏎ | `framework-standard` | Framework-specific frontend standards | ⏎ | `knowledge` | The framework knowledge facet | ⏎ | `workspace-scaffold` | A scaffolding facet for creating the workspace | ⏎ | `library-check` | A deterministic `package.json` check for non-default libraries and misplaced tooling |"
- Evidence K1-S000067: `output/template/.claude/capabilities/frontend/CONTRACT.md:34-34` — "With the selection `none`, these locations are absent; pointers to them from neutral artifacts stay valid and dormant."

### EXTRA-K1-0017
- Closest oracle policies: DEP-009, ARC-019
- Modality: MUST
- Normative action: The persistence slot is a required leaf with exactly one implementation and one provider variant, bound to the architecture frame; an implementation must provide technology boundary, commit-boundary binding, migration mechanism, seeding mechanism, provider variant, declared properties (e.g. string comparison), testing implications, change workflow, knowledge and enforcement.
- Trigger/scope: repo/meta (capability slots)
- Exceptions: none
- Why EXTRA: Capability contract not in the oracle.
- Evidence K1-S000070: `output/template/.claude/capabilities/persistence/CONTRACT.md:5-7` — "- Slot type: required leaf ⏎ - Cardinality: exactly one implementation, with one provider variant ⏎ - Binds: architecture (Infrastructure role implements the Application persistence and commit-boundary contracts)"
- Evidence K1-S000074: `output/template/.claude/capabilities/persistence/CONTRACT.md:15-24` — "| `technology-boundary` | Which technology types exist only in Infrastructure and how they stay out of Application | ⏎ | `commit-boundary-binding` | How the Application commit-boundary contract is implemented | ⏎ | `migration-mechanism` | How schema changes are created, reviewed, and applied | ⏎ | `seeding-mechanism` | How Development seed data is constructed and invoked | ⏎ | `provider-variant` | …"
- Evidence K1-S000081: `output/template/.claude/capabilities/persistence/ef-core/MODULE.md:5-8` — "Slot: persistence"
- Evidence K1-S000088: `output/template/.claude/capabilities/persistence/ef-core/MODULE.md:25-34` — "`change-workflow`"

### EXTRA-K1-0018
- Closest oracle policies: ARC-020, GOV-017
- Modality: MUST
- Normative action: A provider change is a variant change inside the persistence slot; replacing the implementation requires every contract item, and an item the proposal cannot provide (e.g. a migration mechanism) is surfaced as Blocked in the Decision Request instead of being dropped.
- Trigger/scope: repo/meta (capability slots)
- Exceptions: Persistence implementation or provider changes.
- Why EXTRA: Replacement procedure not in the oracle.
- Evidence K1-S000071: `output/template/.claude/capabilities/persistence/CONTRACT.md:9-9` — "A provider change (for example to another relational database) is a variant change inside this slot, not a new slot. Replacing the implementation (for example with a micro-ORM) requires every item below; an item the proposed implementation cannot provide — such as a migration mechanism — is surfaced as *Blocked* in the Decision Request instead of being dropped."

### EXTRA-K1-0019
- Closest oracle policies: DEP-006
- Modality: MUST
- Normative action: A VersionOverride needs a recorded reason.
- Trigger/scope: path-scoped: backend/**/*, Directory.Packages.props, Directory.Build.props
- Exceptions: none
- Why EXTRA: VersionOverride condition not in the oracle.
- Evidence K1-S000237: `output/template/.claude/rules/backend/dependencies.md:12-12` — "- NuGet Central Package Management is mandatory: package versions live in `Directory.Packages.props`; project `PackageReference` entries carry no version (central versions are never duplicated in project files; a `VersionOverride` needs a recorded reason) and live in the narrowest project that actually requires the package."

### EXTRA-K1-0053
- Closest oracle policies: DEP-020
- Modality: MUST
- Normative action: Direct Polly usage is an explicit exception that must be documented.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Documentation obligation not in the oracle.
- Evidence K1-S000679: `output/template/.claude/skills/add-dependency/SKILL.md:23-23` — "- Default: when resilience is required, `Microsoft.Extensions.Http.Resilience` for `HttpClient` and `Microsoft.Extensions.Resilience` for general pipelines. Direct Polly usage is an explicit, documented exception; never add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`."

### EXTRA-K1-0054
- Closest oracle policies: DEP-020, DEP-004
- Modality: MUST_NOT
- Normative action: Never add the deprecated Microsoft.Extensions.Http.Polly or Polly.Extensions.Http packages.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Concrete package ban not in the oracle.
- Evidence K1-S000679: `output/template/.claude/skills/add-dependency/SKILL.md:23-23` — "- Default: when resilience is required, `Microsoft.Extensions.Http.Resilience` for `HttpClient` and `Microsoft.Extensions.Resilience` for general pipelines. Direct Polly usage is an explicit, documented exception; never add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`."

### EXTRA-K1-0055
- Closest oracle policies: ARC-002
- Modality: MUST_NOT
- Normative action: Mapster is never referenced from Domain.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Mapping-library placement not in the oracle.
- Evidence K1-S000680: `output/template/.claude/skills/add-dependency/SKILL.md:24-24` — "- Mapping: `Mapster` with `Mapster.DependencyInjection` once mapping volume warrants it (never referenced from Domain); Testcontainers, Playwright, and similar conditional packages: per the decision register."

### EXTRA-K1-0056
- Closest oracle policies: DEP-001, GOV-014
- Modality: MUST
- Normative action: Remove dependencies that are no longer used when that is part of the current change and safe to verify; do not leave dead package references behind.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: Within the current change and safely verifiable.
- Why EXTRA: Dead-reference removal not in the oracle.
- Evidence K1-S000701: `output/template/.claude/skills/add-dependency/SKILL.md:76-76` — "Remove dependencies that are no longer used when doing so is part of the current change and safe to verify; do not leave dead package references behind, and do not perform unrelated dependency cleanup during a narrowly scoped task."

### EXTRA-K1-0057
- Closest oracle policies: DEP-006, DEP-007
- Modality: MUST
- Normative action: Because removal commands are blocked, remove the manifest entries (PackageReference, the central PackageVersion when unused, the package.json entry) and then restore (dotnet restore, npm install) so the lockfile stays consistent.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Removal procedure not in the oracle.
- Evidence K1-S000702: `output/template/.claude/skills/add-dependency/SKILL.md:78-78` — "The dependency-command hook blocks removal commands (`npm uninstall`, `dotnet remove … package`, and equivalents) so that removals pass this checklist: remove the entry from the manifest (the project `PackageReference`, plus the central `PackageVersion` when no project uses it any more; the `package.json` entry), then restore (`dotnet restore`, `npm install`) so the lockfile stays consistent."

### EXTRA-K1-0058
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Report package, version, license, due-diligence results and any approval obtained or pending.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Workflow output contract not in the oracle.
- Evidence K1-S000704: `output/template/.claude/skills/add-dependency/SKILL.md:82-82` — "Build and run the affected tests (`verify`). Report: package, version, license, due-diligence results, and any approval obtained or pending."

### EXTRA-K1-0059
- Closest oracle policies: FE-002
- Modality: DEFAULT
- Normative action: Route-level page components coordinate UI behaviour; reusable presentation components receive data through explicit inputs and emit meaningful events.
- Trigger/scope: on-demand knowledge angular (frontend)
- Exceptions: none
- Why EXTRA: Component-role split not in the oracle.
- Evidence K1-S000715: `output/template/.claude/skills/angular/SKILL.md:41-41` — "Introduce NgModules only when an integration or legacy dependency genuinely requires them. Route-level page components coordinate UI behavior; reusable presentation components receive data through explicit inputs and emit meaningful events."

### EXTRA-K1-0060
- Closest oracle policies: FE-004
- Modality: PREFER
- Normative action: Use computed for derived state and avoid effect() when computed, template binding or explicit event handling expresses the dependency more clearly.
- Trigger/scope: on-demand knowledge angular (frontend)
- Exceptions: none
- Why EXTRA: effect() guidance not in the oracle.
- Evidence K1-S000718: `output/template/.claude/skills/angular/SKILL.md:51-51` — "Use `computed` for derived state. Avoid `effect()` when `computed`, template binding, or explicit event handling expresses the dependency more clearly. Do not convert every Observable into a Signal, and do not pick Signals or RxJS merely because one is newer."

### EXTRA-K1-0061
- Closest oracle policies: FE-012
- Modality: PREFER
- Normative action: Prefer the async pipe or toSignal when they remove a manual subscription entirely.
- Trigger/scope: on-demand knowledge angular (frontend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000722: `output/template/.claude/skills/angular/SKILL.md:67-67` — "Prefer the `async` pipe or `toSignal` when they remove the manual subscription entirely."

### EXTRA-K1-0062
- Closest oracle policies: FE-010
- Modality: DEFAULT
- Normative action: Map form values to request models explicitly; duplicate complex Domain rules in TypeScript only when the UI genuinely needs an equivalent user-facing rule.
- Trigger/scope: on-demand knowledge angular (frontend)
- Exceptions: Genuine user-facing need.
- Why EXTRA: Form-mapping guidance not in the oracle.
- Evidence K1-S000733: `output/template/.claude/skills/angular/SKILL.md:100-100` — "Reactive forms (rule: `frontend-framework.md`): `FormBuilder` with typed `FormGroup`/`FormControl`, built-in and custom validators, and explicit mapping from form value to request model. Do not duplicate complex Domain rules in TypeScript unless the UI genuinely needs an equivalent user-facing rule."

### EXTRA-K1-0063
- Closest oracle policies: DEP-014, DEP-001
- Modality: DEFAULT
- Normative action: When the project has chosen Angular Material use it consistently for common UI primitives; do not add it to projects that have not chosen it, and do not wrap every Material component in a custom abstraction without a concrete reason.
- Trigger/scope: on-demand knowledge angular (frontend)
- Exceptions: none
- Why EXTRA: Material usage guidance not in the oracle.
- Evidence K1-S000740: `output/template/.claude/skills/angular/SKILL.md:121-121` — "When the project has chosen Angular Material, use its components consistently for common UI primitives where they satisfy the requirement; do not add it to projects that have not chosen it, and do not wrap every Material component in a custom abstraction without a concrete reason."

### EXTRA-K1-0064
- Closest oracle policies: TST-002, DEP-016
- Modality: DEFAULT
- Normative action: Do not duplicate the same behaviour at every level; E2E tests (Playwright, when adopted) cover a small number of important workflows unless broader coverage is required.
- Trigger/scope: on-demand knowledge angular (frontend)
- Exceptions: none
- Why EXTRA: E2E scope guidance not in the oracle.
- Evidence K1-S000746: `output/template/.claude/skills/angular/SKILL.md:133-133` — "Use the workspace's configured runner (Vitest for new projects). Test meaningful component behavior, validation, data-access request mapping (`provideHttpClientTesting`, `HttpTestingController`), important route/auth behavior, and complex reactive state; do not test framework internals or duplicate the same behavior at every level. E2E tests (Playwright, when adopted) cover a small number of impor …"

### EXTRA-K1-0065
- Closest oracle policies: API-014
- Modality: DEFINITION
- Normative action: Commonly breaking: removing a used field, changing meaning/type or required input, incompatible semantics, removing an endpoint, incompatible documented HTTP behaviour (compilation does not decide); often compatible: optional response fields, new endpoints, backward-compatible optional parameters, contract-preserving internal changes; consider client generation.
- Trigger/scope: on-demand knowledge api-versioning (backend)
- Exceptions: none
- Why EXTRA: Compatibility classification not in the oracle.
- Evidence K1-S000767: `output/template/.claude/skills/api-versioning/SKILL.md:68-68` — "Commonly breaking: removing a field clients may depend on, changing a field's meaning or type, changing required input, incompatible resource or workflow semantics, removing an endpoint, incompatible changes to documented HTTP behavior. Compilation success does not decide compatibility. Often compatible: an optional response field, a new endpoint, an optional backward-compatible query parameter, i …"

### EXTRA-K1-0066
- Closest oracle policies: API-016
- Modality: DEFAULT
- Normative action: Generate separate or clearly grouped OpenAPI documents per supported version when clients need them.
- Trigger/scope: on-demand knowledge api-versioning (backend)
- Exceptions: Clients need them.
- Why EXTRA: Not in the oracle.
- Evidence K1-S000771: `output/template/.claude/skills/api-versioning/SKILL.md:76-76` — "Generate separate or clearly grouped documents per supported version when clients need them (`swagger`); the documented version must match runtime routing and controller metadata. Version changes never override normal HTTP semantics (`http-api`)."

### EXTRA-K1-0067
- Closest oracle policies: TST-011, API-022
- Modality: DEFAULT
- Normative action: When versions coexist test meaningful differences (routing, version-specific shapes, deprecated versions operating during support, unsupported versions, consistent shared behaviour); do not duplicate identical tests per version.
- Trigger/scope: on-demand knowledge api-versioning (backend)
- Exceptions: none
- Why EXTRA: Version-testing guidance not in the oracle.
- Evidence K1-S000773: `output/template/.claude/skills/api-versioning/SKILL.md:80-80` — "When versions coexist, test meaningful differences: version routing, version-specific response shapes, deprecated versions still operational during the support period, unsupported-version behavior, shared Application behavior consistent where intended. Do not duplicate identical tests per version."

### EXTRA-K1-0068
- Closest oracle policies: API-014, ARC-010
- Modality: AVOID
- Normative action: Avoid Minimal API version-group examples in a Controller project and a new version for every implementation change.
- Trigger/scope: on-demand knowledge api-versioning (backend)
- Exceptions: none
- Why EXTRA: No owner clause for these items.
- Evidence K1-S000775: `output/template/.claude/skills/api-versioning/SKILL.md:84-84` — "Minimal API version-group examples in a Controller-based project, a new version for every implementation change, silently removing deprecated versions."

### EXTRA-K1-0069
- Closest oracle policies: GOV-007, ARC-020
- Modality: MUST
- Normative action: After approval add an Accepted-decisions row (date, decision, scope, record link) and update the affected register section; for project or reference changes name every added/removed project and list every affected reference as 'From -> To' (the reference hook accepts exactly these recorded changes).
- Trigger/scope: workflow architecture-decision (Reserved decisions, recording, capability selection changes)
- Exceptions: none
- Why EXTRA: Decision-recording format not in the oracle.
- Evidence K1-S000788: `output/template/.claude/skills/architecture-decision/SKILL.md:40-40` — "1. Add a row to the decision register's *Accepted decisions* table (date, decision, scope, record link); update the affected register section (stack, conditional technology, project default, or capability selection). For a project or project-reference change, name every added or removed project and list every affected reference as `From -> To` (project names, e.g. `Shop.Api -> Shop.Infrastructure` …"

### EXTRA-K1-0070
- Closest oracle policies: GOV-007
- Modality: DEFAULT
- Normative action: For a consequential or non-obvious decision add docs/decisions/NNNN-short-title.md (context, decision, alternatives, consequences, date, approver).
- Trigger/scope: workflow architecture-decision (Reserved decisions, recording, capability selection changes)
- Exceptions: none
- Why EXTRA: Decision-record mechanism not in the oracle.
- Evidence K1-S000789: `output/template/.claude/skills/architecture-decision/SKILL.md:41-41` — "2. For a consequential or non-obvious decision, add `docs/decisions/NNNN-short-title.md` (context, decision, alternatives considered, consequences, date, approver)."

### EXTRA-K1-0071
- Closest oracle policies: none
- Modality: MUST
- Normative action: After instruction-content changes (via the user-invoked template-maintenance) run check-instructions with the active repository root.
- Trigger/scope: repo/meta
- Exceptions: none
- Why EXTRA: Instruction-system checker obligation.
- Evidence K1-S000790: `output/template/.claude/skills/architecture-decision/SKILL.md:42-42` — "3. When the decision changes instruction content (standards, knowledge, workflows), ask the user to run the user-invoked `template-maintenance` workflow; afterwards run `node "<root>/.claude/scripts/check-instructions.cjs"` (`<root>`: the active repository root; command form in `verify`, Risk-scoped checks)."

### EXTRA-K1-0072
- Closest oracle policies: ARC-020
- Modality: MUST
- Normative action: For a capability selection change read the slot CONTRACT.md and the current module manifest.
- Trigger/scope: repo/meta (capability slots)
- Exceptions: none
- Why EXTRA: Capability procedure not in the oracle.
- Evidence K1-S000794: `output/template/.claude/skills/architecture-decision/SKILL.md:49-49` — "1. Read `.claude/capabilities/<slot>/CONTRACT.md` and the current module manifest (`.claude/capabilities/<slot>/<implementation>/MODULE.md`)."

### EXTRA-K1-0073
- Closest oracle policies: ARC-020, GOV-017
- Modality: MUST
- Normative action: Map every contract item to a concrete mechanism of the proposed implementation; an item without a mechanism is named under Blocked in the Decision Request, never silently dropped.
- Trigger/scope: workflow architecture-decision (Reserved decisions, recording, capability selection changes)
- Exceptions: none
- Why EXTRA: Capability procedure not in the oracle.
- Evidence K1-S000795: `output/template/.claude/skills/architecture-decision/SKILL.md:50-50` — "2. For the proposed implementation, map every contract item to a concrete mechanism. An item without a mechanism (for example a persistence implementation without a migration mechanism) must be named in the Decision Request under *Blocked* — never silently dropped."

### EXTRA-K1-0074
- Closest oracle policies: none
- Modality: MUST
- Normative action: After approval, in a user-invoked template-maintenance session, replace the module directory and facets (role-based file names unchanged), update the register selection row, remove every old facet and run check-instructions until no leak, manifest, binding, facet-role or contract errors remain; clearing the optional frontend removes module, facets and MAP rows and sets the row to none.
- Trigger/scope: repo/meta (capability slots)
- Exceptions: none
- Why EXTRA: Capability replacement procedure not in the oracle.
- Evidence K1-S000796: `output/template/.claude/skills/architecture-decision/SKILL.md:51-51` — "3. After approval, in a user-invoked `template-maintenance` session: replace the module directory and its facets (role-based facet file names stay the same), update the register's capability selection row, remove every facet of the old implementation, and run `node "<root>/.claude/scripts/check-instructions.cjs"` until it reports no leak, manifest, binding, facet-role, or contract errors. Facet fi …"

### EXTRA-K1-0075
- Closest oracle policies: ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: A provider variant change inside a slot is a Reserved persistence-technology change but not a new slot: update the module Variant line, variant-specific facet sections, the register row and provider-dependent tests.
- Trigger/scope: workflow architecture-decision (Reserved decisions, recording, capability selection changes)
- Exceptions: none
- Why EXTRA: Variant-change procedure not in the oracle.
- Evidence K1-S000798: `output/template/.claude/skills/architecture-decision/SKILL.md:54-54` — "A provider variant change inside a slot (for example a different database provider for the same persistence technology) is a Reserved persistence-technology change but not a new slot: update the module's `Variant:` line, its variant-specific facet sections, the register row, and the affected provider-dependent tests."

### EXTRA-K1-0076
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: Report the decision, its class, approval source, register/record updates and any unresolved request.
- Trigger/scope: workflow architecture-decision (Reserved decisions, recording, capability selection changes)
- Exceptions: none
- Why EXTRA: Workflow output contract not in the oracle.
- Evidence K1-S000800: `output/template/.claude/skills/architecture-decision/SKILL.md:58-58` — "List the decision, its class, approval source, register/record updates, and any request still unresolved."

### EXTRA-K1-0077
- Closest oracle policies: DEP-010, DEP-004
- Modality: MUST_NOT
- Normative action: Do not add deprecated/legacy ASP.NET automatic-validation integration packages.
- Trigger/scope: on-demand knowledge aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: Package-class ban not in the oracle.
- Evidence K1-S000820: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:102-102` — "Do not move Domain invariants into FluentValidation merely because the library is available, and do not duplicate one rule in several layers unless each has a distinct reason. Register validators with `FluentValidation.DependencyInjectionExtensions`; do not add deprecated/legacy ASP.NET automatic-validation integration packages, and follow the project's established invocation pattern instead of ad …"

### EXTRA-K1-0078
- Closest oracle policies: API-010
- Modality: MUST
- Normative action: Follow the project's established validator invocation pattern instead of adding a competing one.
- Trigger/scope: on-demand knowledge aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000820: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:102-102` — "Do not move Domain invariants into FluentValidation merely because the library is available, and do not duplicate one rule in several layers unless each has a distinct reason. Register validators with `FluentValidation.DependencyInjectionExtensions`; do not add deprecated/legacy ASP.NET automatic-validation integration packages, and follow the project's established invocation pattern instead of ad …"

### EXTRA-K1-0079
- Closest oracle policies: API-011, ARC-020
- Modality: DEFAULT
- Normative action: Typed exceptions for selected cases only as a deliberate, consistent project-level decision.
- Trigger/scope: on-demand knowledge aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000822: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:106-106` — "A project may deliberately use typed exceptions for selected cases, but only as a consistent project-level decision."

### EXTRA-K1-0080
- Closest oracle policies: API-012, RUN-013
- Modality: DEFAULT
- Normative action: Expected outcomes (not found, validation failures, rejected operations) are normally not logged as application errors.
- Trigger/scope: on-demand knowledge aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: Log-level rule for expected outcomes not in the oracle.
- Evidence K1-S000828: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:127-127` — "Expected outcomes (not found, validation failures, rejected business operations) are normally not logged as application errors. Logging technique: `logging`."
- Evidence K1-S001433: `output/template/.claude/skills/logging/SKILL.md:26-30` — "- **Trace/Debug** — detailed troubleshooting diagnostics; never assume sensitive data is safe at these levels. ⏎ - **Information** — meaningful application events (a background job completed, an important business operation completed, a lifecycle event); not every internal method call. ⏎ - **Warning** — an unexpected or degraded condition the application recovered from (fallback used, retries exha …"
- Evidence K1-S001447: `output/template/.claude/skills/logging/SKILL.md:69-69` — "String interpolation in log templates, duplicate exception logging, expected business outcomes logged as errors, dumping full objects without review, provider-specific APIs throughout Application code, and using logs as an audit database unless a dedicated audit design was adopted."
- Evidence K1-S001450: `output/template/.claude/skills/logging/SKILL.md:75-80` — ""

### EXTRA-K1-0081
- Closest oracle policies: API-009
- Modality: MUST
- Normative action: If a Result pattern is adopted use typed errors rather than string arrays.
- Trigger/scope: on-demand knowledge aspnet-error-handling (backend)
- Exceptions: Result pattern adopted.
- Why EXTRA: Not in the oracle.
- Evidence K1-S000830: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:131-131` — "Consider `Result<T>` when an operation has several expected failure modes, callers benefit from typed outcomes, exception-based control flow would otherwise be common, and the project will use it consistently. Avoid it when `null`, `bool`, or a simple typed response suffices, when it wraps straightforward CRUD in noise, or when it would spread to every method without need (project-wide adoption: ` …"

### EXTRA-K1-0082
- Closest oracle policies: API-010, ARC-010
- Modality: AVOID
- Normative action: Avoid coupling validation to Minimal API endpoint filters when Controllers are the HTTP model.
- Trigger/scope: on-demand knowledge aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: No owner clause for this item.
- Evidence K1-S000833: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:139-139` — "Returning raw exception messages, inconsistent anonymous error objects, putting business rules only in request validators, and coupling validation to Minimal API endpoint filters when Controllers are the HTTP model."

### EXTRA-K1-0083
- Closest oracle policies: SEC-016, GOV-013
- Modality: DEFAULT
- Normative action: Choose the scheme by the application: Bearer/OIDC for an SPA calling an API, cookies for server-rendered apps, Identity when the app owns local users and needs account management, external OIDC/OAuth when identity is delegated; a User entity does not justify Identity; no custom JWT issuance when an identity provider owns token issuance.
- Trigger/scope: on-demand knowledge authentication (backend)
- Exceptions: none
- Why EXTRA: Scheme-selection guidance not in the oracle.
- Evidence K1-S000842: `output/template/.claude/skills/authentication/SKILL.md:17-17` — "Choose the scheme by the actual application: Bearer/OIDC for a SPA calling an API; cookies for server-rendered interactive web applications; ASP.NET Core Identity when the application owns local users, credentials, and needs account management; an external OpenID Connect/OAuth provider when identity is delegated. A business entity named `User` or profile management does not justify Identity, and d …"
- Evidence K1-S000869: `output/template/.claude/skills/authentication/SKILL.md:101-101` — "Hardcoded signing keys, authorization only in the frontend, Application depending on `HttpContext`, 401 for authenticated-but-forbidden or 403 for missing authentication, role/permission magic strings throughout the codebase, adding Identity, JWT issuance, or OIDC infrastructure without an actual need."

### EXTRA-K1-0084
- Closest oracle policies: SEC-006
- Modality: PREFER
- Normative action: Prefer policies for meaningful capabilities with stable constants; roles only for a genuinely role-oriented model; avoid scattered compound role strings and magic strings.
- Trigger/scope: on-demand knowledge authentication (backend)
- Exceptions: none
- Why EXTRA: Policy-vs-role guidance not in the oracle.
- Evidence K1-S000851: `output/template/.claude/skills/authentication/SKILL.md:42-42` — "Prefer policies for meaningful capabilities, with stable constants for repeated policy names:"
- Evidence K1-S000853: `output/template/.claude/skills/authentication/SKILL.md:55-55` — "Roles fit a genuinely role-oriented model; prefer a policy when several roles or claims represent one capability, and avoid scattered compound role strings."
- Evidence K1-S000869: `output/template/.claude/skills/authentication/SKILL.md:101-101` — "Hardcoded signing keys, authorization only in the frontend, Application depending on `HttpContext`, 401 for authenticated-but-forbidden or 403 for missing authentication, role/permission magic strings throughout the codebase, adding Identity, JWT issuance, or OIDC infrastructure without an actual need."

### EXTRA-K1-0085
- Closest oracle policies: SEC-005
- Modality: MUST
- Normative action: Resource-dependent permissions use ASP.NET Core resource authorization or explicit Application authorization logic.
- Trigger/scope: on-demand knowledge authentication (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000855: `output/template/.claude/skills/authentication/SKILL.md:59-59` — "Some permissions depend on the resource (users edit only their own records, members update only their projects, administrators access everything). Use ASP.NET Core resource authorization or explicit Application authorization logic; client-side checks are UX."
- Evidence K1-S001635: `output/template/.claude/skills/security-scan/references/scan-layers.md:89-89` — "Look for operations such as `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` where possessing an identifier could expose another user's or tenant's data; verify ownership, tenant, permission, or resource policy where required. Client-side filtering is not authorization."

### EXTRA-K1-0086
- Closest oracle policies: API-005, ARC-011
- Modality: DEFAULT
- Normative action: Authentication/authorization middleware normally produces 401/403 rather than controllers manufacturing them.
- Trigger/scope: on-demand knowledge authentication (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000858: `output/template/.claude/skills/authentication/SKILL.md:68-68` — "Authentication/authorization middleware normally produces these responses rather than controllers manufacturing them."

### EXTRA-K1-0087
- Closest oracle policies: SEC-011
- Modality: DEFAULT
- Normative action: For cookie authentication use ASP.NET Core antiforgery (AddAntiforgery, token validation on state-changing endpoints) paired with the SPA's matching XSRF header handling.
- Trigger/scope: on-demand knowledge authentication (backend)
- Exceptions: none
- Why EXTRA: Antiforgery technique not in the oracle.
- Evidence K1-S000865: `output/template/.claude/skills/authentication/SKILL.md:93-93` — "CSRF and token-storage rules: `.claude/rules/frontend/security.md`. Technique for cookie authentication: ASP.NET Core antiforgery (`AddAntiforgery`, token validation on state-changing endpoints) paired with the SPA's matching XSRF header handling. Signing secrets follow the configuration and secret rules."

### EXTRA-K1-0088
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Test authorization behaviour of important protected operations (401, 403, success, ownership, intended anonymous access), not merely the presence of [Authorize].
- Trigger/scope: on-demand knowledge authentication (backend)
- Exceptions: none
- Why EXTRA: Authorization-test guidance not in the oracle.
- Evidence K1-S000867: `output/template/.claude/skills/authentication/SKILL.md:97-97` — "Test authorization behavior of important protected operations: unauthenticated → 401; authenticated without permission → 403; permitted → expected success; resource ownership rules; intended anonymous endpoints remain accessible. Verify observable behavior, not merely the presence of `[Authorize]`."

### EXTRA-K1-0089
- Closest oracle policies: WF-014, WF-008
- Modality: MUST
- Normative action: Stop when progress has clearly stalled instead of making speculative edits.
- Trigger/scope: workflow build-fix (failing build or tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000881: `output/template/.claude/skills/build-fix/SKILL.md:25-25` — "- Stop when progress has clearly stalled instead of making speculative edits."

### EXTRA-K1-0090
- Closest oracle policies: GOV-014, FE-009
- Modality: MUST_NOT
- Normative action: Determine which contract is authoritative; never patch both sides independently into inconsistent shapes merely to compile.
- Trigger/scope: workflow build-fix (failing build or tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000892: `output/template/.claude/skills/build-fix/SKILL.md:52-52` — "Determine which contract is authoritative (response shape, generated client vs. OpenAPI, enum/value semantics, endpoint path or method, nullability, authentication contract). Never patch both sides independently into inconsistent shapes merely to compile. With OpenAPI client generation: verify the backend contract, regenerate the client through the project's normal workflow, review the generated c …"

### EXTRA-K1-0091
- Closest oracle policies: WF-013
- Modality: MUST_NOT
- Normative action: Update APIs from verified documentation; never fabricate replacement APIs from memory.
- Trigger/scope: workflow build-fix (failing build or tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000898: `output/template/.claude/skills/build-fix/SKILL.md:64-64` — "For upgrade fallout, inspect the installed version, separate compile errors from changed runtime behavior, update obsolete APIs deliberately from verified documentation (never fabricate replacement APIs from memory), and do not perform an additional unrelated upgrade. For toolchain problems check `dotnet --info`, `dotnet --version`, `node --version`, `npm --version`, `global.json`, target framewor …"

### EXTRA-K1-0092
- Closest oracle policies: DEP-008, GOV-014
- Modality: MUST_NOT
- Normative action: Never change the declared SDK, Node, framework or language version because the local machine differs; report an unavailable toolchain instead of editing source to compensate.
- Trigger/scope: workflow build-fix (failing build or tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000898: `output/template/.claude/skills/build-fix/SKILL.md:64-64` — "For upgrade fallout, inspect the installed version, separate compile errors from changed runtime behavior, update obsolete APIs deliberately from verified documentation (never fabricate replacement APIs from memory), and do not perform an additional unrelated upgrade. For toolchain problems check `dotnet --info`, `dotnet --version`, `node --version`, `npm --version`, `global.json`, target framewor …"

### EXTRA-K1-0093
- Closest oracle policies: WF-008, GOV-014
- Modality: MUST
- Normative action: If a fix introduces new failures that are not a legitimate dependency of the change, revert or correct it; never leave the repository knowingly worse than at the start.
- Trigger/scope: workflow build-fix (failing build or tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000902: `output/template/.claude/skills/build-fix/SKILL.md:72-72` — "Use bounded iteration — several focused attempts, not an unlimited edit/build loop. Stop and reassess when the same root failure survives materially different fixes, fixes create increasing unrelated failures, the toolchain is incompatible, required external infrastructure is unavailable, package compatibility cannot be resolved safely, or correct behavior cannot be determined. Never repeat varian …"

### EXTRA-K1-0094
- Closest oracle policies: RUN-007, RUN-021
- Modality: MUST
- Normative action: Define consistency semantics (acceptable staleness, invalidation) before writing cache code.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000912: `output/template/.claude/skills/caching/SKILL.md:13-13` — "Policy: `.claude/rules/backend/runtime.md` (need, keys, lifetimes, invalidation), `.claude/rules/backend/architecture.md` (cache technology boundaries). Adding a distributed cache is a Reserved infrastructure decision (`CLAUDE.md`). Clear reasons to cache: measured expensive repeated work, high read volume, expensive remote calls — with acceptable staleness semantics; a value being read frequently …"

### EXTRA-K1-0095
- Closest oracle policies: ARC-024
- Modality: DEFAULT
- Normative action: HTTP response caching uses ASP.NET Core output caching when the entire response can safely be reused, in the Api layer.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000914: `output/template/.claude/skills/caching/SKILL.md:17-17` — "- **HTTP response caching** — ASP.NET Core output caching when the entire response can safely be reused; lives in the Api layer."

### EXTRA-K1-0096
- Closest oracle policies: RUN-020
- Modality: DEFAULT
- Normative action: Centralize key construction once duplicated key formats become hard to maintain.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000924: `output/template/.claude/skills/caching/SKILL.md:48-48` — "Include every dimension that affects the result: entity identifier, tenant, user when genuinely user-specific, locale, relevant query/filter parameters. Centralize key construction once duplicated key formats become hard to maintain."

### EXTRA-K1-0097
- Closest oracle policies: ARC-010
- Modality: DEFAULT
- Normative action: Apply output-cache policies through controller/action metadata.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000931: `output/template/.claude/skills/caching/SKILL.md:69-69` — "Apply the policy through controller/action metadata. Never cache authenticated or user-specific responses unless the key and policy isolate users and authorization context."

### EXTRA-K1-0098
- Closest oracle policies: RUN-018
- Modality: MUST
- Normative action: Decide whether a cache failure falls back to the source, fails the request or returns stale data.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000933: `output/template/.claude/skills/caching/SKILL.md:73-73` — "Application Services keep their normal repository/Unit of Work workflow; coordinate required invalidation through an abstraction instead of bypassing repositories or `IUnitOfWork`. Decide whether a cache failure falls back to the source, fails the request, or returns stale data. Never cache tracked persistence entities across Unit of Work boundaries."

### EXTRA-K1-0099
- Closest oracle policies: ARC-019, RUN-021
- Modality: MUST_NOT
- Normative action: Never cache tracked persistence entities across Unit of Work boundaries.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000933: `output/template/.claude/skills/caching/SKILL.md:73-73` — "Application Services keep their normal repository/Unit of Work workflow; coordinate required invalidation through an abstraction instead of bypassing repositories or `IUnitOfWork`. Decide whether a cache failure falls back to the source, fails the request, or returns stale data. Never cache tracked persistence entities across Unit of Work boundaries."

### EXTRA-K1-0100
- Closest oracle policies: TST-003, TST-011
- Modality: DEFAULT
- Normative action: Test caching when it affects observable correctness (invalidation after mutation, key isolation, miss fallback, outage policy); do not unit-test framework cache internals.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000935: `output/template/.claude/skills/caching/SKILL.md:77-77` — "Test caching when it affects observable correctness: stale entries invalidated after successful mutation, tenant/user key isolation, cache-miss fallback, outage behavior per the intended failure policy. Do not unit-test framework cache internals."

### EXTRA-K1-0101
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: Build deployable artifacts reproducibly and keep deployment/environment configuration outside compiled artifacts where practical.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000942: `output/template/.claude/skills/ci-cd/SKILL.md:13-13` — "Procedure and obligations: `delivery-change`. Build deployable artifacts reproducibly and keep deployment/environment configuration outside compiled artifacts where practical."

### EXTRA-K1-0102
- Closest oracle policies: WF-017, DEP-008
- Modality: MUST
- Normative action: Adapt CI action and runtime versions to the repository's supported versions.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000950: `output/template/.claude/skills/ci-cd/SKILL.md:72-72` — "Adapt action and runtime versions to the repository's supported versions."

### EXTRA-K1-0103
- Closest oracle policies: TST-004, GOV-013
- Modality: MUST
- Normative action: Provide CI services (database, cache, broker) only when tests require them, as service containers or Testcontainers; do not hardcode a database provider into a generic pipeline.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000952: `output/template/.claude/skills/ci-cd/SKILL.md:76-76` — "Provide services (the selected database server, cache, broker) only when tests require them, as CI service containers or Testcontainers, isolated from Development and Production data; do not hardcode a database provider into a generic pipeline. Testing technique: the backend-testing knowledge facet named in the decision register."
- Evidence K1-S000967: `output/template/.claude/skills/ci-cd/SKILL.md:109-109` — "Project-specific database infrastructure in a generic pipeline, rebuilding different source per environment, assuming container deployment. Pipeline obligations (visible failures, declared scripts, lockfile installs, deliberate production migrations): `delivery-change`."

### EXTRA-K1-0104
- Closest oracle policies: DEP-004
- Modality: MUST
- Normative action: Run dependency audits (dotnet package list --vulnerable, restore auditing, npm audit) and treat findings per the project's security policy.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000954: `output/template/.claude/skills/ci-cd/SKILL.md:80-80` — "`dotnet package list --vulnerable --include-transitive`; NuGet auditing also runs during restore on modern SDKs; `npm audit` for the frontend. Treat findings per the project's security policy."
- Evidence K1-S001057: `output/template/.claude/skills/delivery-change/SKILL.md:25-25` — "- Enforced formatting/analyzer gates only when the project has adopted them; dependency vulnerability inspection per the project's security policy; no automatic package upgrades unless the project adopted automated updates."

### EXTRA-K1-0105
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: Store or publish only artifacts later stages need.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000957: `output/template/.claude/skills/ci-cd/SKILL.md:89-89` — "Store or publish only artifacts later stages need. Build and publish container images only when container deployment is part of the project (`docker`)."
- Evidence K1-S001060: `output/template/.claude/skills/delivery-change/SKILL.md:30-30` — "Build images and deployable artifacts only when the project deploys them; publish only artifacts later stages need, reproducibly. Runtime images: `.claude/rules/backend/operations.md`. Images, build arguments, and committed Compose files are source-controlled surfaces for `.claude/rules/common/security.md` (Secrets)."

### EXTRA-K1-0106
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: Where supported promote the same tested artifact/image through environments instead of recompiling; environment behaviour comes from runtime configuration.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: Deployment model does not support promotion.
- Why EXTRA: Not in the oracle.
- Evidence K1-S000959: `output/template/.claude/skills/ci-cd/SKILL.md:93-93` — "Where the deployment model supports promotion, promote the same tested artifact/image through environments instead of recompiling per environment; environment-specific behavior comes from runtime configuration."
- Evidence K1-S000967: `output/template/.claude/skills/ci-cd/SKILL.md:109-109` — "Project-specific database infrastructure in a generic pipeline, rebuilding different source per environment, assuming container deployment. Pipeline obligations (visible failures, declared scripts, lockfile installs, deliberate production migrations): `delivery-change`."

### EXTRA-K1-0107
- Closest oracle policies: SEC-002
- Modality: PREFER
- Normative action: Prefer workload or federated identity over long-lived deployment credentials.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000961: `output/template/.claude/skills/ci-cd/SKILL.md:97-97` — "Use the CI platform's secret/identity mechanism; prefer workload or federated identity over long-lived deployment credentials."
- Evidence K1-S001065: `output/template/.claude/skills/delivery-change/SKILL.md:39-39` — "Pipeline secrets come from the CI platform's secret/identity mechanism (prefer workload or federated identity over long-lived credentials), per `.claude/rules/common/security.md`. A green CI build does not imply every branch deploys; use environment protection or approval where the hosting platform supports it."

### EXTRA-K1-0108
- Closest oracle policies: WF-019
- Modality: MUST
- Normative action: The deployment migration step fails visibly on error.
- Trigger/scope: on-demand knowledge ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000963: `output/template/.claude/skills/ci-cd/SKILL.md:101-101` — "Generate migration scripts/artifacts in CI and execute them at a controlled deployment step with approved credentials, failing visibly on error. Migration technique: the persistence knowledge facet named in the decision register."
- Evidence K1-S001062: `output/template/.claude/skills/delivery-change/SKILL.md:34-34` — "- Production database migrations must not run automatically from normal application startup by default. A production migration is an explicit deployment operation: make the step explicit, use the project's approved credentials, run it at a controlled point, and fail visibly on error."

### EXTRA-K1-0109
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: CI and CD may be separate workflows; use environment protection/approval appropriate to the hosting platform.
- Trigger/scope: delivery
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000965: `output/template/.claude/skills/ci-cd/SKILL.md:105-105` — "CI and CD may be separate workflows; use environment protection/approval appropriate to the hosting platform."

### EXTRA-K1-0110
- Closest oracle policies: WF-011
- Modality: MUST_NOT
- Normative action: Do not report formatting already owned by tooling.
- Trigger/scope: workflow code-review (reviews of completed changes)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000974: `output/template/.claude/skills/code-review/SKILL.md:20-20` — "Prioritize findings in this order: correctness; security and authorization; data integrity and persistence; architectural boundary violations; concurrency and integration behavior; missing meaningful tests; maintainability; credible performance problems. Never elevate style preferences above behavioral defects, and do not report formatting already owned by tooling."

### EXTRA-K1-0111
- Closest oracle policies: FE-007
- Modality: MUST_NOT
- Normative action: Do not apply backend project-boundary rules mechanically to frontend code.
- Trigger/scope: workflow code-review (reviews of completed changes)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000991: `output/template/.claude/skills/code-review/SKILL.md:62-62` — "When frontend code is in scope, check against `.claude/rules/frontend/` (feature boundaries, data-access boundary, subscription lifetime, error contract, route guards not treated as server authorization, no unnecessary global state, meaningful tests). Do not apply backend project-boundary rules mechanically to frontend code."

### EXTRA-K1-0112
- Closest oracle policies: WF-020
- Modality: MUST_NOT
- Normative action: Run the full security-scan only for a requested audit, a materially security-sensitive change or a finding justifying it, not for every ordinary review.
- Trigger/scope: workflow code-review (reviews of completed changes)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000993: `output/template/.claude/skills/code-review/SKILL.md:66-66` — "Review transaction/commit behavior, destructive data changes, raw SQL parameterization, authorization, input trust boundaries, secrets, sensitive logging, concurrency, migrations, and cache consistency. Run the full `security-scan` procedure only when a security audit was requested, the change is materially security-sensitive, or a concrete finding justifies broader investigation — not for every o …"
- Evidence K1-S001789: `output/template/.claude/skills/verify/SKILL.md:55-55` — "- **Dependencies and security:** for dependency changes or security-sensitive work, inspect vulnerabilities (`dotnet package list --vulnerable --include-transitive`, `npm audit`) and changed secrets, authorization, raw SQL, CORS/TLS, sensitive logging, and certificate validation. A full `security-scan` is not required for every small change."

### EXTRA-K1-0113
- Closest oracle policies: WF-011
- Modality: MUST
- Normative action: Report findings ordered by severity, each with severity, location, what is wrong, why it matters and the smallest fix, using the Critical/High/Medium/Low definitions.
- Trigger/scope: workflow code-review (reviews of completed changes)
- Exceptions: none
- Why EXTRA: Finding format not in the oracle.
- Evidence K1-S001003: `output/template/.claude/skills/code-review/SKILL.md:86-86` — "Report findings ordered by severity. Each finding: severity, file/location, what is wrong, why it matters, smallest reasonable fix."
- Evidence K1-S001004: `output/template/.claude/skills/code-review/SKILL.md:88-91` — "- **Critical** — data loss, security vulnerability, reliably broken core behavior; blocks use/merge. ⏎ - **High** — likely defect or architectural/data-integrity issue to fix before merge. ⏎ - **Medium** — real maintainability, robustness, or test gap; not a likely immediate failure. ⏎ - **Low** — non-blocking improvement."

### EXTRA-K1-0114
- Closest oracle policies: WF-012
- Modality: MUST_NOT
- Normative action: No filler praise.
- Trigger/scope: workflow code-review (reviews of completed changes)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001005: `output/template/.claude/skills/code-review/SKILL.md:93-93` — "Never invent findings to populate a category. When there are no meaningful findings, say so and name important areas that could not be verified. No filler praise."

### EXTRA-K1-0115
- Closest oracle policies: GOV-010, RUN-015
- Modality: MUST
- Normative action: Numeric example values are illustrative, not approved defaults; choose retry counts, timeouts and limits from actual integration and deployment requirements; complex rules use a validation delegate.
- Trigger/scope: on-demand knowledge configuration (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001016: `output/template/.claude/skills/configuration/SKILL.md:43-43` — "Numeric values in examples are illustrative, not approved defaults; choose retry counts, timeouts, and limits from the actual integration and deployment requirements. Complex rules use a validation delegate:"
- Evidence K1-S001337: `output/template/.claude/skills/httpclient-factory/references/resilience.md:18-18` — "Distinguish attempt timeout from total operation timeout, especially with retries enabled, and choose values from actual latency requirements rather than copying example numbers."

### EXTRA-K1-0116
- Closest oracle policies: GOV-011, GOV-008
- Modality: MUST_NOT
- Normative action: Do not record a framework default the project has not intentionally overridden.
- Trigger/scope: workflow custom-settings (CUSTOM_SETTINGS.md value added, changed, removed, reviewed or applied)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001035: `output/template/.claude/skills/custom-settings/SKILL.md:20-20` — "- [ ] The value belongs in the file per `CLAUDE.md` (Product sources) and is not merely a framework default the project has not intentionally overridden."

### EXTRA-K1-0117
- Closest oracle policies: GOV-021
- Modality: PREFER
- Normative action: Avoid duplicating the same literal across layers when a single source in code or configuration is appropriate.
- Trigger/scope: workflow custom-settings (CUSTOM_SETTINGS.md value added, changed, removed, reviewed or applied)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001037: `output/template/.claude/skills/custom-settings/SKILL.md:24-24` — "Record it in `CUSTOM_SETTINGS.md` with a stable descriptive name, its value, and its purpose. Avoid duplicating the same literal across many layers when a single source in code or configuration is appropriate."

### EXTRA-K1-0118
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Report the setting, old → new value, every updated surface, migration created and the verify result.
- Trigger/scope: workflow custom-settings (CUSTOM_SETTINGS.md value added, changed, removed, reviewed or applied)
- Exceptions: none
- Why EXTRA: Workflow output contract not in the oracle.
- Evidence K1-S001047: `output/template/.claude/skills/custom-settings/SKILL.md:44-44` — "List the setting, old → new value, every updated surface, migration created (if any), and the `verify` result."

### EXTRA-K1-0119
- Closest oracle policies: GOV-013, WF-001
- Modality: MUST
- Normative action: Inspect the repository before writing a pipeline or container file; do not assume a database provider, cache, container or frontend tooling; add stages for the actual project, not generic boilerplate.
- Trigger/scope: workflow delivery-change (CI/CD, containers, deployment)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001053: `output/template/.claude/skills/delivery-change/SKILL.md:19-19` — "Inspect the repository before writing a pipeline or container file: .NET backend, frontend workspace, test projects, Dockerfiles, provider-specific integration tests, generated clients, deployment artifacts. Do not assume a database provider, cache, container tooling, or frontend tooling exists, and add stages for the actual project, not generic boilerplate."

### EXTRA-K1-0120
- Closest oracle policies: DEP-003
- Modality: MUST_NOT
- Normative action: No automatic package upgrades unless the project adopted automated updates.
- Trigger/scope: workflow delivery-change (CI/CD, containers, deployment)
- Exceptions: Adopted automation.
- Why EXTRA: Not in the oracle.
- Evidence K1-S001057: `output/template/.claude/skills/delivery-change/SKILL.md:25-25` — "- Enforced formatting/analyzer gates only when the project has adopted them; dependency vulnerability inspection per the project's security policy; no automatic package upgrades unless the project adopted automated updates."

### EXTRA-K1-0121
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: A green CI build does not imply every branch deploys; use environment protection or approval where the platform supports it.
- Trigger/scope: delivery
- Exceptions: Platform support.
- Why EXTRA: Not in the oracle.
- Evidence K1-S001065: `output/template/.claude/skills/delivery-change/SKILL.md:39-39` — "Pipeline secrets come from the CI platform's secret/identity mechanism (prefer workload or federated identity over long-lived credentials), per `.claude/rules/common/security.md`. A green CI build does not imply every branch deploys; use environment protection or approval where the hosting platform supports it."

### EXTRA-K1-0122
- Closest oracle policies: WF-003, WF-006
- Modality: MUST
- Normative action: Before completion verify the pipeline restores from a clean environment, builds backend and frontend, runs configured tests, does not depend on developer-machine state, exposes no secrets and produces expected artifacts.
- Trigger/scope: workflow delivery-change (CI/CD, containers, deployment)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001067: `output/template/.claude/skills/delivery-change/SKILL.md:43-43` — "Before considering the pipeline complete, verify that it restores from a clean environment, builds the backend, builds the frontend when present, runs the configured tests, does not depend on developer-machine state, does not expose secrets, and produces the expected artifacts. Report each item as PASS / NOT RUN / NOT APPLICABLE."

### EXTRA-K1-0123
- Closest oracle policies: ARC-021, ARC-023
- Modality: DEFAULT
- Normative action: Use abstractions at architectural boundaries (Application services, repositories, external adapters); concrete registration is fine for implementation-only helpers.
- Trigger/scope: on-demand knowledge dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001073: `output/template/.claude/skills/dependency-injection/SKILL.md:18-18` — "Use abstractions at architectural boundaries (Application services, repositories, external adapters); concrete registration is fine for implementation-only helpers without a separate contract."

### EXTRA-K1-0124
- Closest oracle policies: GOV-012
- Modality: PREFER
- Normative action: Prefer explicit registration in small and medium applications; scanning, keyed services, factories or decorators only for actual composition problems.
- Trigger/scope: on-demand knowledge dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001075: `output/template/.claude/skills/dependency-injection/SKILL.md:49-49` — "Prefer explicit registration in small and medium applications; add scanning, keyed services, factories, or decorators when they solve an actual composition problem."

### EXTRA-K1-0125
- Closest oracle policies: GOV-012
- Modality: DEFAULT
- Normative action: Keyed services for several implementations selected by a known key, not when a single registration or simple factory is clearer.
- Trigger/scope: on-demand knowledge dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001082: `output/template/.claude/skills/dependency-injection/SKILL.md:76-76` — "For several implementations of one abstraction selected by a known key; not when a single registration or a simple explicit factory is clearer."
- Evidence K1-S001371: `output/template/.claude/skills/httpclient-factory/SKILL.md:42-42` — ""

### EXTRA-K1-0126
- Closest oracle policies: DEP-001, GOV-013
- Modality: MUST_NOT
- Normative action: Do not add Scrutor for a single decoration when normal composition is simpler.
- Trigger/scope: on-demand knowledge dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001087: `output/template/.claude/skills/dependency-injection/SKILL.md:106-106` — "If Scrutor is already used: `services.AddScoped<IOrderService, OrderService>(); services.Decorate<IOrderService, LoggingOrderService>();`. Do not add Scrutor for a single decoration when normal composition is simpler."

### EXTRA-K1-0127
- Closest oracle policies: GOV-012, ARC-023
- Modality: DEFAULT
- Normative action: Use assembly scanning only when registration volume creates genuine boilerplate, scanning the assembly that owns the services.
- Trigger/scope: on-demand knowledge dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001089: `output/template/.claude/skills/dependency-injection/SKILL.md:110-110` — "Use assembly scanning only when registration volume creates genuine boilerplate, and scan the assembly that owns the services (not accidentally only the Api assembly):"

### EXTRA-K1-0128
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Summarize what changed and why, the verify report and approvals obtained.
- Trigger/scope: workflow development-workflow (feature, fix, refactor, performance, API change, new application)
- Exceptions: none
- Why EXTRA: Workflow output contract not in the oracle.
- Evidence K1-S001121: `output/template/.claude/skills/development-workflow/SKILL.md:60-60` — "Summarize what changed and why, the `verify` report, approvals obtained, and every unresolved Decision Request."

### EXTRA-K1-0129
- Closest oracle policies: DEP-018, ARC-002
- Modality: DEFAULT
- Normative action: Keep configuration external, images reproducible and Docker concerns out of Domain/Application code.
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001125: `output/template/.claude/skills/docker/SKILL.md:13-13` — "Containers are optional infrastructure (decision register). Policy: `.claude/rules/backend/operations.md` (runtime image, non-root), `.claude/rules/common/security.md` (secrets). Procedure: `delivery-change`. Keep build tooling out of production images, configuration external, images reproducible, and Docker concerns out of Domain/Application code."

### EXTRA-K1-0130
- Closest oracle policies: DEP-023
- Modality: MUST
- Normative action: Copy only repository-level build files that exist and restore needs; copy project files explicitly (no flattening wildcards) and update the section when the solution changes; never trade a correct restore graph for layer caching.
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001128: `output/template/.claude/skills/docker/SKILL.md:46-46` — "Copy only repository-level build files that exist and are needed for restore; never add them just to satisfy the example. Copy project files explicitly — no wildcard tricks that flatten or rearrange the multi-project structure — and update this section when the solution structure changes. Never optimize layer caching at the cost of restoring the wrong project graph."

### EXTRA-K1-0131
- Closest oracle policies: SEC-002
- Modality: DEFAULT
- Normative action: Pass environment-specific configuration at runtime (ASPNETCORE_ENVIRONMENT, ConnectionStrings__Default, Authentication__Authority).
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001132: `output/template/.claude/skills/docker/SKILL.md:54-54` — "Pass environment-specific configuration at runtime (`ASPNETCORE_ENVIRONMENT`, `ConnectionStrings__Default`, `Authentication__Authority`) and supply secrets through platform/container secret mechanisms. Surfaces to check for credentials: the Dockerfile, committed Compose files, build arguments (visible in image metadata), and copied appsettings files."

### EXTRA-K1-0132
- Closest oracle policies: GOV-013, DEP-018
- Modality: MUST
- Normative action: Use Compose for local infrastructure only when beneficial and add only services the project uses.
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001134: `output/template/.claude/skills/docker/SKILL.md:58-58` — "Useful for local infrastructure such as a database or cache when the project benefits from it; add only services the project uses, and keep local passwords in an ignored `.env` or similar mechanism."

### EXTRA-K1-0133
- Closest oracle policies: API-019
- Modality: DEFAULT
- Normative action: Expose liveness/readiness through ASP.NET Core health checks and prefer orchestrator-native HTTP probes; for in-container health commands verify the executable exists or add an explicit probe, weighing extra packages in production images.
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001137: `output/template/.claude/skills/docker/SKILL.md:75-75` — "Expose liveness/readiness through ASP.NET Core health checks (`health-check`) and prefer orchestrator-native HTTP probes. Runtime images may lack `curl`, `wget`, or a shell; if Compose must run an in-container health command, verify the executable exists or add an explicit probe mechanism, weighing the cost of extra packages in production images."

### EXTRA-K1-0134
- Closest oracle policies: DEP-018
- Modality: DEFAULT
- Normative action: Build static frontend assets in a Node stage and serve them with the selected hosting strategy (a web server image is not mandatory); keep API base URLs and environment configuration compatible.
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001139: `output/template/.claude/skills/docker/SKILL.md:79-79` — "When the frontend is deployed as static assets, build it in a Node stage and serve the output with the selected hosting strategy (a web server image is not mandatory when the platform hosts static files). Keep API base URLs and environment configuration compatible with that strategy."

### EXTRA-K1-0135
- Closest oracle policies: none
- Modality: MUST
- Normative action: Exclude .git, .vs, bin, obj, node_modules, TestResults and coverage, but not tests the image build runs or files restore/build needs.
- Trigger/scope: delivery
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001141: `output/template/.claude/skills/docker/SKILL.md:83-83` — "Exclude `.git`, `.vs`, `**/bin`, `**/obj`, `**/node_modules`, `TestResults`, `coverage`; do not exclude tests the image build intentionally runs or files restore/build needs."

### EXTRA-K1-0136
- Closest oracle policies: RUN-008, GOV-013
- Modality: DEFAULT
- Normative action: Start with standard images; Alpine, chiseled, trimming or Native AOT only when compatibility and deployment requirements justify them, verifying globalization, native dependencies, reflection and diagnostics.
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001143: `output/template/.claude/skills/docker/SKILL.md:87-87` — "Start with standard supported images. Consider Alpine, chiseled images, trimming, or Native AOT only when compatibility and deployment requirements justify them, and verify globalization, native dependencies, reflection, and diagnostics when you do."

### EXTRA-K1-0137
- Closest oracle policies: WF-006, SEC-001
- Modality: MUST
- Normative action: Build the image and verify startup, port/configuration, non-root behaviour, health-probe integration and absence of accidental secrets/files; run meaningful tests outside or in the pipeline.
- Trigger/scope: on-demand knowledge docker (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001147: `output/template/.claude/skills/docker/SKILL.md:95-95` — "Build the image, verify application startup, required port/configuration, non-root behavior when relevant, health-probe integration, and the absence of accidental secrets/files; run meaningful tests outside or as part of the pipeline."

### EXTRA-K1-0138
- Closest oracle policies: GOV-012, TST-011
- Modality: DEFAULT
- Normative action: Do not build test infrastructure without a concrete testing need; a small project does not need an enterprise harness.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001152: `output/template/.claude/skills/dotnet-testing/SKILL.md:15-15` — "Do not build test infrastructure without a concrete testing need; a small project does not need an enterprise-sized harness."

### EXTRA-K1-0139
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Arrange/Act/Assert is a useful default (comments optional when obvious); use the NUnit constraint model (Assert.That).
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001155: `output/template/.claude/skills/dotnet-testing/SKILL.md:39-39` — "Arrange/Act/Assert is a useful default; comments are optional when the phases are obvious. Use the constraint model (`Assert.That(actual, Is...)`)."

### EXTRA-K1-0140
- Closest oracle policies: TST-003
- Modality: PREFER
- Normative action: Prefer one observable scenario per test; multi-step tests when the sequence itself is the scenario.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001159: `output/template/.claude/skills/dotnet-testing/SKILL.md:57-57` — "Prefer one observable scenario per test; multi-step tests fit when the sequence itself is the scenario (an entire workflow or a replace-set lifecycle)."

### EXTRA-K1-0141
- Closest oracle policies: TST-002, TST-003
- Modality: DEFAULT
- Normative action: Unit-test candidates: domain behaviour owned by Domain, calculations, state transitions, validation, Application orchestration with simple fakes; do not mock every collaborator mechanically nor forbid mocking project-owned abstractions.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001161: `output/template/.claude/skills/dotnet-testing/SKILL.md:61-61` — "Good unit-test candidates: non-trivial domain behavior that genuinely belongs to Domain, calculations, workflow/state transitions at the owning layer, validation logic, and Application orchestration with simple fakes or mocks when isolation gives useful feedback. Do not mock every collaborator mechanically, and do not forbid mocking project-owned abstractions when isolation helps."

### EXTRA-K1-0142
- Closest oracle policies: TST-007
- Modality: MUST
- Normative action: Choose the test-database strategy by what the test must prove (provider fidelity vs application/API integration) and be explicit about the trade-off.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001168: `output/template/.claude/skills/dotnet-testing/SKILL.md:105-105` — "Choose the database strategy by what the test must prove (provider fidelity vs. application/API integration) and be explicit about the trade-off. Start from a known state with a simple strategy: recreate or reset the isolated database, use transactions when their semantics fit, seed only the data the test needs, use unique identifiers to avoid collisions. Never modify production data."

### EXTRA-K1-0143
- Closest oracle policies: TST-004
- Modality: DEFAULT
- Normative action: Keep slow or unreliable external-system tests out of ordinary fast runs.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001173: `output/template/.claude/skills/dotnet-testing/SKILL.md:118-118` — "Never call uncontrolled external services from normal test runs. At the boundary use a fake or mock abstraction (unit tests), a stub `HttpMessageHandler`, WireMock or another local fake server (HTTP integration), or a dedicated sandbox only when the test explicitly targets that integration. Keep slow or unreliable external-system tests out of ordinary fast runs."

### EXTRA-K1-0144
- Closest oracle policies: TST-008, GOV-012
- Modality: DEFAULT
- Normative action: Keep test data explicit and minimal; builders/fixtures only when repeated setup becomes hard to read; no generic test-data framework for a few objects.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001175: `output/template/.claude/skills/dotnet-testing/SKILL.md:122-122` — "Keep test data explicit and minimal. Introduce builders, fixtures, or factories when repeated setup becomes hard to read; do not add a generic test-data framework for a few simple objects."

### EXTRA-K1-0145
- Closest oracle policies: WF-006
- Modality: DEFINITION
- Normative action: A smoke test is a small set of fast checks that a built or deployed application is basically operational, not every integration test.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001181: `output/template/.claude/skills/dotnet-testing/SKILL.md:134-134` — ""Smoke test" means a small set of fast checks that a built or deployed application is basically operational — not a synonym for every integration test. Coverage is diagnostic, not a target; prioritize meaningful behavior, edge cases, and risky integrations. Snapshot testing can help for large stable outputs, but do not add a snapshot library by default; explicit assertions are clearer for small or …"
- Evidence K1-S001186: `output/template/.claude/skills/dotnet-testing/SKILL.md:144-152` — ""

### EXTRA-K1-0146
- Closest oracle policies: TST-003, DEP-001
- Modality: DEFAULT
- Normative action: Snapshot testing for large stable outputs only; no snapshot library by default; explicit assertions for small or important contracts.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001181: `output/template/.claude/skills/dotnet-testing/SKILL.md:134-134` — ""Smoke test" means a small set of fast checks that a built or deployed application is basically operational — not a synonym for every integration test. Coverage is diagnostic, not a target; prioritize meaningful behavior, edge cases, and risky integrations. Snapshot testing can help for large stable outputs, but do not add a snapshot library by default; explicit assertions are clearer for small or …"

### EXTRA-K1-0147
- Closest oracle policies: TST-003
- Modality: AVOID
- Normative action: Avoid assertion-free tests unless the behaviour is 'does not throw'.
- Trigger/scope: on-demand knowledge dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: No owner clause for this item.
- Evidence K1-S001183: `output/template/.claude/skills/dotnet-testing/SKILL.md:138-138` — "Avoid assertions that merely repeat the implementation, assertion-free tests (unless the behavior is "does not throw"), arbitrary delays such as `Task.Delay` to make timing-sensitive tests pass, and Testcontainers when no provider fidelity is required."

### EXTRA-K1-0148
- Closest oracle policies: ARC-019
- Modality: DEFAULT
- Normative action: Keep entity configuration in separate IEntityTypeConfiguration<T> classes.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001194: `output/template/.claude/skills/ef-core/SKILL.md:21-21` — "Keep entity configuration in separate `IEntityTypeConfiguration<T>` classes and keep persistence-specific configuration out of Domain entities where practical."

### EXTRA-K1-0149
- Closest oracle policies: RUN-006
- Modality: DEFAULT
- Normative action: Tracking queries when entities will be modified and committed through the Unit of Work; AsNoTracking() for read-only entity queries; no mechanical AsNoTracking() on DTO projections.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001206: `output/template/.claude/skills/ef-core/SKILL.md:106-106` — "- **Tracking:** use tracking queries when loaded entities will be modified and committed through the current Unit of Work; `AsNoTracking()` for read-only entity queries where tracking adds nothing. Do not add `AsNoTracking()` mechanically to projections that already produce non-entity DTOs."
- Evidence K1-S001240: `output/template/.claude/skills/ef-core/SKILL.md:234-244` — ""

### EXTRA-K1-0150
- Closest oracle policies: RUN-006
- Modality: DEFAULT
- Normative action: Prefer an explicit query shape (projection or Include/ThenInclude); for large collection includes consider split queries and verify the generated SQL.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001208: `output/template/.claude/skills/ef-core/SKILL.md:108-108` — "- **Related data:** prefer an explicit query shape — projection for selected related data, `Include`/`ThenInclude` when the entity graph itself is needed. Avoid lazy loading by default (it hides database access and causes N+1 queries). For large collection includes consider split queries and verify the generated SQL."

### EXTRA-K1-0151
- Closest oracle policies: RUN-006
- Modality: MUST
- Normative action: Pagination always uses deterministic ordering.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001209: `output/template/.claude/skills/ef-core/SKILL.md:109-109` — "- **Pagination:** filter, order, and page in the database, always with deterministic ordering; consider keyset pagination for very large or frequently traversed datasets."

### EXTRA-K1-0152
- Closest oracle policies: ARC-016, ARC-019
- Modality: MUST_NOT
- Normative action: ExecuteUpdateAsync/ExecuteDeleteAsync bypass change tracking: do not mix them casually with tracked entities for the same rows; understand transaction and consistency implications.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001211: `output/template/.claude/skills/ef-core/SKILL.md:119-119` — "- **Bulk update/delete:** `ExecuteUpdateAsync`/`ExecuteDeleteAsync` run directly against the database and bypass change tracking; do not mix them casually with tracked entities for the same rows, and understand their transaction and consistency implications."
- Evidence K1-S001240: `output/template/.claude/skills/ef-core/SKILL.md:234-244` — ""

### EXTRA-K1-0153
- Closest oracle policies: RUN-002
- Modality: MUST_NOT
- Normative action: Never fire-and-forget EF Core asynchronous operations; a DbContext is not thread-safe.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001212: `output/template/.claude/skills/ef-core/SKILL.md:120-120` — "- **Never fire-and-forget** EF Core asynchronous operations; a `DbContext` is not thread-safe."

### EXTRA-K1-0154
- Closest oracle policies: ARC-019
- Modality: MUST_NOT
- Normative action: EF Core interceptors only for infrastructure-level cross-cutting behaviour with a clear benefit (e.g. auditing); never hide business behaviour in them.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001218: `output/template/.claude/skills/ef-core/SKILL.md:132-132` — "Use interceptors for infrastructure-level cross-cutting behavior with a clear benefit, such as auditing; never hide business behavior in them."

### EXTRA-K1-0155
- Closest oracle policies: GOV-003, PST-001
- Modality: MUST
- Normative action: When the required graph is complex the task should describe the dataset explicitly instead of inventing a large generic graph.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001223: `output/template/.claude/skills/ef-core/SKILL.md:201-201` — "Representative states to consider: newly created, active/in progress, completed, inactive/archived, with and without optional values and relationships, representative status values, meaningful boundary states. When the required graph is complex, the task should describe the dataset explicitly instead of inventing a large generic graph."

### EXTRA-K1-0156
- Closest oracle policies: ARC-019
- Modality: DEFAULT
- Normative action: Create migrations from the Infrastructure project with the Api project as startup project.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001225: `output/template/.claude/skills/ef-core/SKILL.md:205-205` — "Create migrations from the Infrastructure project with the Api project as startup project:"

### EXTRA-K1-0157
- Closest oracle policies: GOV-006
- Modality: MUST
- Normative action: Make an approved collation choice explicit with UseCollation(...) or a column-level collation.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: Approved choice.
- Why EXTRA: Not in the oracle.
- Evidence K1-S001231: `output/template/.claude/skills/ef-core/SKILL.md:220-220` — "- String comparison in queries follows the column/database collation; SQL Server's default collations are case-insensitive. Choosing case sensitivity or a collation is a product decision when observable — make an approved choice explicit with `UseCollation(...)` or a column-level collation in configuration."

### EXTRA-K1-0158
- Closest oracle policies: RUN-016
- Modality: PREFER
- Normative action: Prefer provider execution strategies (EnableRetryOnFailure) over generic application retry pipelines, wrap explicit transactions in the execution strategy, and never apply HTTP retry policies to database operations.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001232: `output/template/.claude/skills/ef-core/SKILL.md:221-221` — "- Transient faults: prefer provider execution strategies (`options.UseSqlServer(cs, sql => sql.EnableRetryOnFailure())`) over generic application-level retry pipelines; with an execution strategy, wrap explicit transactions in `db.Database.CreateExecutionStrategy().ExecuteAsync(...)`. Do not apply HTTP retry policies to database operations."

### EXTRA-K1-0159
- Closest oracle policies: TST-007
- Modality: MUST
- Normative action: A lighter isolated relational database may suffice when provider specifics are irrelevant; state the trade-off.
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001235: `output/template/.claude/skills/ef-core/SKILL.md:226-226` — "- Provider fidelity: run provider-sensitive tests against SQL Server (for example a Testcontainers `MsSql` container or an isolated LocalDB/SQL Server database); a lighter isolated relational database may suffice when provider specifics are irrelevant — state the trade-off."

### EXTRA-K1-0160
- Closest oracle policies: TST-004, TST-006
- Modality: DEFAULT
- Normative action: Integration tests replace the registered DbContextOptions in WebApplicationFactory with an isolated test database and create the schema from migrations (EnsureCreated only for disposable test databases).
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001236: `output/template/.claude/skills/ef-core/SKILL.md:227-227` — "- Integration tests replace the registered `DbContextOptions<AppDbContext>` in `WebApplicationFactory` with an isolated test database and create the schema from migrations (or `EnsureCreated` for disposable test databases only)."

### EXTRA-K1-0161
- Closest oracle policies: TST-002
- Modality: DEFAULT
- Normative action: Test repository implementations and mappings when there is meaningful persistence behaviour (custom mappings, filters, projections, non-trivial queries, relationships, concurrency, provider behaviour).
- Trigger/scope: on-demand knowledge ef-core (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001237: `output/template/.claude/skills/ef-core/SKILL.md:228-228` — "- Test repository implementations and mappings when there is meaningful persistence behavior: custom mappings, query filters, projections, non-trivial queries, relationships, concurrency, provider-specific behavior — not every trivial `Add`/`Get`."

### EXTRA-K1-0162
- Closest oracle policies: WF-022
- Modality: PREFER
- Normative action: Prefer one logical change per commit with its tests; no artificial tiny commits or combined unrelated fixes and refactors.
- Trigger/scope: workflow git-workflow (requested Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001250: `output/template/.claude/skills/git-workflow/SKILL.md:23-23` — "Before committing, inspect the staged diff: it must contain only the intended logical change. Never stage or clean unrelated files merely because they are modified. Prefer one logical change per commit, with implementation and the tests that protect it together; do not create artificial tiny commits or combine unrelated fixes and refactors."

### EXTRA-K1-0163
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Follow the branch-naming convention (feature/, fix/, refactor/, test/, docs/, chore/ as defaults); meaningful names; do not rename an existing user branch.
- Trigger/scope: workflow git-workflow (requested Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001252: `output/template/.claude/skills/git-workflow/SKILL.md:27-27` — "Follow the repository's branch-naming convention; without one, prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, `chore/` are reasonable defaults. Use meaningful names and do not rename an existing user branch to satisfy a convention. One branch must not be checked out in multiple normal worktrees; keep each worktree focused on its branch's concern; before removing a worktree, ve …"

### EXTRA-K1-0164
- Closest oracle policies: GOV-016
- Modality: MUST
- Normative action: One branch is not checked out in multiple normal worktrees; each worktree stays focused on its branch's concern.
- Trigger/scope: workflow git-workflow (requested Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001252: `output/template/.claude/skills/git-workflow/SKILL.md:27-27` — "Follow the repository's branch-naming convention; without one, prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, `chore/` are reasonable defaults. Use meaningful names and do not rename an existing user branch to satisfy a convention. One branch must not be checked out in multiple normal worktrees; keep each worktree focused on its branch's concern; before removing a worktree, ve …"

### EXTRA-K1-0165
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Follow the commit-message convention (Conventional Commits as default); use the body for motivation, constraints or migration notes; do not narrate obvious diff details.
- Trigger/scope: workflow git-workflow (requested Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001254: `output/template/.claude/skills/git-workflow/SKILL.md:31-31` — "Follow the repository's convention; without one, Conventional Commits are a useful default (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`). Use the body for motivation, constraints, or migration notes that would otherwise be lost; do not narrate obvious diff details."

### EXTRA-K1-0166
- Closest oracle policies: GOV-020, WF-003
- Modality: MUST
- Normative action: Before pushing confirm the branch and understood state, ensure verification completed and avoid pushing unrelated local commits.
- Trigger/scope: workflow git-workflow (requested Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001256: `output/template/.claude/skills/git-workflow/SKILL.md:35-35` — "Before pushing: confirm the intended branch, confirm the working/staged state is understood, ensure relevant verification has completed, and avoid pushing unrelated local commits. Never force-push a shared branch unless the user explicitly requests history rewriting and understands the consequences; treat `main`, `master`, and other protected/shared branches as non-rewritable."

### EXTRA-K1-0167
- Closest oracle policies: GOV-015
- Modality: MUST_NOT
- Normative action: Treat main, master and other protected/shared branches as non-rewritable.
- Trigger/scope: workflow git-workflow (requested Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001256: `output/template/.claude/skills/git-workflow/SKILL.md:35-35` — "Before pushing: confirm the intended branch, confirm the working/staged state is understood, ensure relevant verification has completed, and avoid pushing unrelated local commits. Never force-push a shared branch unless the user explicitly requests history rewriting and understands the consequences; treat `main`, `master`, and other protected/shared branches as non-rewritable."

### EXTRA-K1-0168
- Closest oracle policies: none
- Modality: MUST
- Normative action: Follow the repository/team convention or the user's explicit request for merge vs rebase; resolve conflicts from the intended combined behaviour, not mechanically; run relevant verification afterwards.
- Trigger/scope: workflow git-workflow (requested Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001258: `output/template/.claude/skills/git-workflow/SKILL.md:39-39` — "Follow the repository/team convention or the user's explicit request rather than personal preference. Inspect local uncommitted work first, and never automatically stash, reset, or discard it to let an operation proceed. Resolve conflicts from the intended combined behavior, not by mechanically choosing "ours" or "theirs", and run relevant verification afterwards."

### EXTRA-K1-0169
- Closest oracle policies: WF-003, GOV-014
- Modality: MUST
- Normative action: Run verify before preparing a PR; a PR has a focused purpose and describes what changed, why, how it was verified and compatibility/migration notes.
- Trigger/scope: workflow git-workflow (requested Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001260: `output/template/.claude/skills/git-workflow/SKILL.md:43-43` — "Run `verify` before preparing a PR. A PR has a focused purpose without accidental unrelated changes; its description explains what changed, why, how it was verified, and compatibility/migration notes. Never claim checks that were not run."

### EXTRA-K1-0170
- Closest oracle policies: WF-009
- Modality: DEFAULT
- Normative action: Report the resulting Git state when useful (branch, commit, push target, PR status, remaining uncommitted changes).
- Trigger/scope: workflow git-workflow (requested Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001262: `output/template/.claude/skills/git-workflow/SKILL.md:47-47` — "Report the resulting state when useful: branch, commit created, push target, PR preparation status, and uncommitted changes that remain."

### EXTRA-K1-0171
- Closest oracle policies: API-019
- Modality: AVOID
- Normative action: Avoid readiness cascades (A → B → C) without understanding their operational consequences.
- Trigger/scope: on-demand knowledge health-check (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001278: `output/template/.claude/skills/health-check/SKILL.md:50-50` — "A database check performs a lightweight connectivity/availability check (provider or framework health-check integration where suitable) — no business queries, large scans, or data modification. Check an external dependency only when its availability matters to readiness, and avoid readiness cascades (A → B readiness → C readiness ...) without understanding the operational consequences; prefer a li …"
- Evidence K1-S001288: `output/template/.claude/skills/health-check/SKILL.md:70-70` — "Health checks as a code-quality grading system, database writes or business transactions from probes, every dependency on liveness, remote dependency chains without operational justification, stack traces from health endpoints."

### EXTRA-K1-0172
- Closest oracle policies: API-019, API-003
- Modality: MUST
- Normative action: Healthy → success, unhealthy → non-success per the configured probe policy (ResultStatusCodes); do not reuse business API status semantics mechanically.
- Trigger/scope: on-demand knowledge health-check (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001280: `output/template/.claude/skills/health-check/SKILL.md:54-54` — "Healthy → success, unhealthy → non-success per the configured probe policy (`HealthCheckOptions.ResultStatusCodes` maps statuses); do not reuse business API status semantics mechanically for probes. Keep probe responses small; protect operator-facing detailed diagnostics with network or authorization controls instead of exposing connection strings, credentials, raw exceptions, or infrastructure to …"

### EXTRA-K1-0173
- Closest oracle policies: SEC-006
- Modality: DEFAULT
- Normative action: Choose probe exposure by topology (private network, management port, host restrictions, supported authorization); probes often need unauthenticated infrastructure access.
- Trigger/scope: on-demand knowledge health-check (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001282: `output/template/.claude/skills/health-check/SKILL.md:58-58` — "Probes often must be reachable by infrastructure without user authentication. Choose exposure by topology: private network access, a dedicated management port, host restrictions, or authorization the probe infrastructure supports."

### EXTRA-K1-0174
- Closest oracle policies: RUN-013
- Modality: AVOID
- Normative action: Avoid Error-level logs for every normal failed probe.
- Trigger/scope: on-demand knowledge health-check (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001284: `output/template/.claude/skills/health-check/SKILL.md:62-62` — "Probes run frequently: avoid expensive queries, long external timeouts, large allocations, full workflows, and Error-level logs for every normal failed probe."

### EXTRA-K1-0175
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Test health configuration the deployment relies on (liveness responds, readiness follows required dependencies, no sensitive leaks, optional dependencies as intended); do not test uncustomized framework behaviour.
- Trigger/scope: on-demand knowledge health-check (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001286: `output/template/.claude/skills/health-check/SKILL.md:66-66` — "Test health configuration the deployment relies on: live endpoint responds when healthy, readiness follows a required dependency, responses do not leak sensitive details, optional-dependency behavior matches the intended semantics. Do not test framework behavior the application does not customize."

### EXTRA-K1-0176
- Closest oracle policies: API-018
- Modality: MUST_NOT
- Normative action: Health checks are not a code-quality grading system.
- Trigger/scope: on-demand knowledge health-check (backend)
- Exceptions: none
- Why EXTRA: No owner clause for this item.
- Evidence K1-S001288: `output/template/.claude/skills/health-check/SKILL.md:70-70` — "Health checks as a code-quality grading system, database writes or business transactions from probes, every dependency on liveness, remote dependency chains without operational justification, stack traces from health endpoints."

### EXTRA-K1-0177
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: Keep status-code behaviour consistent across similar endpoints.
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001292: `output/template/.claude/skills/http-api/SKILL.md:13-13` — "Policy: `.claude/rules/backend/api.md`. Exception/failure handling: `aspnet-error-handling`. Keep status-code behavior consistent across similar endpoints."

### EXTRA-K1-0178
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: A 202 returns an operation identifier or a progress Location when practical.
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001297: `output/template/.claude/skills/http-api/SKILL.md:24-24` — "- **202 Accepted** — processing accepted but not complete (long-running operation, background job, asynchronous import, queued processing); return an operation identifier or a `Location` for progress when practical (`AcceptedAtAction(...)`)."

### EXTRA-K1-0179
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: Choose consistently whether repeated DELETE of an absent resource returns 204 or 404; do not mix conventions between equivalent resources.
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001298: `output/template/.claude/skills/http-api/SKILL.md:25-25` — "- **204 No Content** — completed with no body needed (successful `DELETE`, an update where returning the representation adds nothing). A `204` response must not contain a body. Choose consistently whether repeated `DELETE` of an absent resource returns `204` (desired state holds) or `404` (resource absent); do not mix conventions between equivalent resources."

### EXTRA-K1-0180
- Closest oracle policies: API-003
- Modality: DEFINITION
- Normative action: 304 only for a conditional request whose cached representation is still valid; not a generic 'nothing changed' business response.
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001300: `output/template/.claude/skills/http-api/SKILL.md:29-29` — "**304 Not Modified** only for a conditional request (`If-None-Match`/ETag, `If-Modified-Since`) whose cached representation is still valid; it carries no representation and is not a generic "nothing changed" business response."
- Evidence K1-S001329: `output/template/.claude/skills/http-api/SKILL.md:82-102` — ""

### EXTRA-K1-0181
- Closest oracle policies: API-003, API-002
- Modality: DEFINITION
- Normative action: Status semantics beyond the oracle: 400 for invalid HTTP requests (never authentication failures); 406/415 for content negotiation and unsupported media types; 429 for rate limiting with Retry-After when known (never validation); 502/503/504 for intermediary, unavailability and upstream-timeout cases (not every dependency failure; 503 with Retry-After when meaningful).
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001302: `output/template/.claude/skills/http-api/SKILL.md:33-33` — "- **400 Bad Request** — the HTTP request itself is invalid: malformed JSON, invalid shape, model-binding failure, invalid formatting, missing transport-level input. `[ApiController]` handles many of these automatically. Never use `400` for authentication failure."
- Evidence K1-S001306: `output/template/.claude/skills/http-api/SKILL.md:37-37` — "- **406 Not Acceptable** — no representation acceptable to the client's content negotiation (response format); not `415`."
- Evidence K1-S001309: `output/template/.claude/skills/http-api/SKILL.md:40-40` — "- **415 Unsupported Media Type** — the request body format is unsupported (e.g. `Content-Type: application/xml` on a JSON-only endpoint)."
- Evidence K1-S001312: `output/template/.claude/skills/http-api/SKILL.md:43-43` — "- **429 Too Many Requests** — rate limiting rejected the request; include `Retry-After` when known. Never represent validation failure as rate limiting."
- Evidence K1-S001315: `output/template/.claude/skills/http-api/SKILL.md:48-48` — "- **502 Bad Gateway** — acting as an intermediary and receiving an invalid or unusable upstream response; do not map every dependency failure to `502`."
- Evidence K1-S001316: `output/template/.claude/skills/http-api/SKILL.md:49-49` — "- **503 Service Unavailable** — temporarily unable to handle the request (maintenance, a critical dependency the operation needs is down, chosen overload semantics); include `Retry-After` when meaningful."
- Evidence K1-S001317: `output/template/.claude/skills/http-api/SKILL.md:50-50` — "- **504 Gateway Timeout** — acting as an intermediary and an upstream did not respond in time. Distinguish client cancellation of the incoming request, our own operation timing out, and an upstream timeout; not every `TaskCanceledException` is a `504`."
- Evidence K1-S001329: `output/template/.claude/skills/http-api/SKILL.md:82-102` — ""

### EXTRA-K1-0182
- Closest oracle policies: API-003, API-010
- Modality: DEFAULT
- Normative action: 422 for structurally valid requests with invalid semantics; follow an established 400-for-both convention, otherwise new APIs use 400 for invalid contracts and 422 for invalid semantics.
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: Established convention.
- Why EXTRA: Not in the oracle.
- Evidence K1-S001310: `output/template/.claude/skills/http-api/SKILL.md:41-41` — "- **422 Unprocessable Content** — structurally valid request with invalid semantics or business input (e.g. `startDate > endDate`, a business rule rejection that is not a state conflict). Some APIs deliberately use `400` for both; follow an established convention. New APIs that distinguish them: `400` = invalid HTTP/request contract, `422` = valid structure, invalid semantics."
- Evidence K1-S001329: `output/template/.claude/skills/http-api/SKILL.md:82-102` — ""

### EXTRA-K1-0183
- Closest oracle policies: API-006
- Modality: DEFINITION
- Normative action: 428 when a contract-required precondition is omitted (missing If-Match → 428, stale → 412); other preconditions only when the contract makes them mandatory.
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001311: `output/template/.claude/skills/http-api/SKILL.md:42-42` — "- **428 Precondition Required** — the contract requires a precondition the client omitted (missing required `If-Match` → `428`; stale `If-Match` → `412`). Use it for other preconditions only when the contract defines them as mandatory."
- Evidence K1-S001329: `output/template/.claude/skills/http-api/SKILL.md:82-102` — ""

### EXTRA-K1-0184
- Closest oracle policies: RUN-016, API-006
- Modality: DEFAULT
- Normative action: GET safe/idempotent, PUT idempotent, DELETE idempotent in intended state, POST generally not; consider an Idempotency-Key for non-duplicating POSTs (different payload → 409); do not claim idempotency because duplicates are unlikely.
- Trigger/scope: on-demand knowledge http-api (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001319: `output/template/.claude/skills/http-api/SKILL.md:54-54` — "`GET` is safe and idempotent, `PUT` idempotent, `DELETE` idempotent in intended state, `POST` generally not. For a `POST` that must not duplicate effects, consider an `Idempotency-Key` header associated with the request/result per the API contract; reuse with a materially different payload → `409`. Do not claim idempotency because duplicates are merely unlikely."

### EXTRA-K1-0185
- Closest oracle policies: DEP-020, GOV-013
- Modality: MUST
- Normative action: Resilience mechanisms are added only when failure and operation semantics justify them, and their behaviour is observed when it matters operationally.
- Trigger/scope: private reference resilience (read by httpclient-factory)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001332: `output/template/.claude/skills/httpclient-factory/references/resilience.md:5-5` — "Policy: `.claude/rules/backend/runtime.md`. Package defaults (Microsoft resilience integration, direct Polly only as a documented exception): `add-dependency`. Resilience mechanisms are added only when failure and operation semantics justify them, and their behavior is observed when it matters operationally."
- Evidence K1-S001390: `output/template/.claude/skills/httpclient-factory/SKILL.md:99-99` — "Making typed/keyed/named clients mandatory universally, infinite or poorly bounded retries, ignoring cancellation, dynamic auth tokens in shared `DefaultRequestHeaders`, mapping every upstream failure to the same status, and adding resilience pipelines without understanding their behavior."

### EXTRA-K1-0186
- Closest oracle policies: DEP-020, RUN-016
- Modality: DEFAULT
- Normative action: The standard resilience handler fits when its behaviour matches the remote API, is not mandatory, and its retry behaviour is reviewed carefully for state-changing requests.
- Trigger/scope: private reference resilience (read by httpclient-factory)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001335: `output/template/.claude/skills/httpclient-factory/references/resilience.md:14-14` — "The standard handler fits when its behavior matches the remote API; it is not mandatory for every client. Review its retry behavior carefully for state-changing requests, and do not stack resilience handlers with overlapping strategies. The modern Microsoft packages are built on Polly v8, but application code configures them through the Microsoft.Extensions resilience APIs."

### EXTRA-K1-0187
- Closest oracle policies: RUN-015
- Modality: DEFAULT
- Normative action: Use a circuit breaker when repeated calls to a failing dependency would add load or latency, not without a meaningful repeated-failure pattern; give it operational visibility when it matters.
- Trigger/scope: private reference resilience (read by httpclient-factory)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001343: `output/template/.claude/skills/httpclient-factory/references/resilience.md:30-30` — "Use one when repeated calls to a failing dependency would add load or latency; not for a dependency without a meaningful repeated failure pattern. Give it operational visibility when it matters in production."
- Evidence K1-S001358: `output/template/.claude/skills/httpclient-factory/references/resilience.md:60-68` — ""

### EXTRA-K1-0188
- Closest oracle policies: RUN-016, ARC-019
- Modality: MUST_NOT
- Normative action: Do not wrap normal database operations in a generic application retry pipeline or apply HTTP retry policies to them; use provider-level transient-fault handling.
- Trigger/scope: private reference resilience (read by httpclient-factory)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001349: `output/template/.claude/skills/httpclient-factory/references/resilience.md:42-42` — "Do not wrap normal database operations in a generic application-level retry pipeline or apply an HTTP retry policy to them; use the persistence technology's provider-level transient-fault handling (persistence knowledge facet named in the decision register)."
- Evidence K1-S001358: `output/template/.claude/skills/httpclient-factory/references/resilience.md:60-68` — ""

### EXTRA-K1-0189
- Closest oracle policies: RUN-016
- Modality: MUST
- Normative action: Retrying publication may duplicate delivery: use idempotent consumers, broker deduplication or an outbox when the business requires it; never claim exactly-once because a retry policy exists.
- Trigger/scope: private reference resilience (read by httpclient-factory)
- Exceptions: Business requirement.
- Why EXTRA: Not in the oracle.
- Evidence K1-S001351: `output/template/.claude/skills/httpclient-factory/references/resilience.md:46-46` — "Retrying publication may produce duplicate delivery; use idempotent consumers, broker deduplication, an outbox, or similar mechanisms when the business requires them, and never claim exactly-once delivery merely because a retry policy exists."

### EXTRA-K1-0190
- Closest oracle policies: RUN-017
- Modality: DEFINITION
- Normative action: ASP.NET Core inbound rate limiting is separate from outbound resilience; rejected requests return 429 with Retry-After when a useful delay is known.
- Trigger/scope: private reference resilience (read by httpclient-factory)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001353: `output/template/.claude/skills/httpclient-factory/references/resilience.md:50-50` — "ASP.NET Core rate limiting protects this API from excessive incoming traffic and is conceptually separate from outbound resilience; a rejected request returns `429` with `Retry-After` when a useful delay is known (`http-api`)."
- Evidence K1-S001358: `output/template/.claude/skills/httpclient-factory/references/resilience.md:60-68` — ""

### EXTRA-K1-0191
- Closest oracle policies: GOV-013
- Modality: MUST_NOT
- Normative action: Observe retries, timeouts, circuit state, rate-limit rejections and latency with the adopted telemetry stack when they matter; OpenTelemetry is not required merely because pipelines exist.
- Trigger/scope: private reference resilience (read by httpclient-factory)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001355: `output/template/.claude/skills/httpclient-factory/references/resilience.md:54-54` — "Propagate caller cancellation through pipelines. Observe retry counts, timeout frequency, circuit state, rate-limit rejections, and dependency latency when they matter, using the telemetry stack the project adopted; OpenTelemetry is not required merely because pipelines exist."

### EXTRA-K1-0192
- Closest oracle policies: GOV-012
- Modality: DEFAULT
- Normative action: Named, typed and keyed clients are all valid; choose the model that makes ownership and lifetime easiest to understand; do not make one model mandatory universally.
- Trigger/scope: on-demand knowledge httpclient-factory (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001367: `output/template/.claude/skills/httpclient-factory/SKILL.md:33-33` — "Named, typed, and keyed clients are all valid; choose the model that makes ownership and lifetime easiest to understand."
- Evidence K1-S001390: `output/template/.claude/skills/httpclient-factory/SKILL.md:99-99` — "Making typed/keyed/named clients mandatory universally, infinite or poorly bounded retries, ignoring cancellation, dynamic auth tokens in shared `DefaultRequestHeaders`, mapping every upstream failure to the same status, and adding resilience pipelines without understanding their behavior."

### EXTRA-K1-0193
- Closest oracle policies: ARC-025
- Modality: MUST_NOT
- Normative action: Use DelegatingHandlers only for genuine HTTP pipeline concerns (authorization headers, correlation, signing), never for business decisions.
- Trigger/scope: on-demand knowledge httpclient-factory (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001373: `output/template/.claude/skills/httpclient-factory/SKILL.md:46-46` — "Use a `DelegatingHandler` for genuine HTTP pipeline concerns — authorization header acquisition, correlation/context propagation, request signing — never for business decisions."

### EXTRA-K1-0194
- Closest oracle policies: ARC-025
- Modality: DEFAULT
- Normative action: Do not blindly call EnsureSuccessStatusCode() when specific statuses carry contract meaning; map them explicitly.
- Trigger/scope: on-demand knowledge httpclient-factory (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001378: `output/template/.claude/skills/httpclient-factory/SKILL.md:66-66` — "Translate remote responses into the abstraction Application consumes. Do not blindly call `EnsureSuccessStatusCode()` when specific statuses carry contract meaning:"
- Evidence K1-S001390: `output/template/.claude/skills/httpclient-factory/SKILL.md:99-99` — "Making typed/keyed/named clients mandatory universally, infinite or poorly bounded retries, ignoring cancellation, dynamic auth tokens in shared `DefaultRequestHeaders`, mapping every upstream failure to the same status, and adding resilience pipelines without understanding their behavior."

### EXTRA-K1-0195
- Closest oracle policies: none
- Modality: MUST
- Normative action: Stable headers on the client; per-request values (dynamic tokens) on the request or via a handler, never by mutating shared DefaultRequestHeaders concurrently; prefer System.Net.Http.Json/System.Text.Json with explicit options when the external contract differs.
- Trigger/scope: on-demand knowledge httpclient-factory (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001384: `output/template/.claude/skills/httpclient-factory/SKILL.md:85-85` — "Configure stable headers (media types) on the client; apply per-request values such as dynamic access tokens to the specific request or through a handler, never by mutating shared `DefaultRequestHeaders` concurrently. Prefer `System.Net.Http.Json`/`System.Text.Json`, with explicit serializer options when the external contract differs from application defaults; never reuse Domain entities as remote …"
- Evidence K1-S001390: `output/template/.claude/skills/httpclient-factory/SKILL.md:99-99` — "Making typed/keyed/named clients mandatory universally, infinite or poorly bounded retries, ignoring cancellation, dynamic auth tokens in shared `DefaultRequestHeaders`, mapping every upstream failure to the same status, and adding resilience pipelines without understanding their behavior."

### EXTRA-K1-0196
- Closest oracle policies: DEP-021
- Modality: DEFAULT
- Normative action: Use two-stage initialization (bootstrap logger) when startup logging before DI/configuration matters; simpler applications may use host-managed setup.
- Trigger/scope: private reference serilog (read by logging)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001395: `output/template/.claude/skills/logging/references/serilog.md:9-9` — "1. **Two-stage initialization when startup logging matters** — a bootstrap logger captures failures before DI/configuration is available; simpler applications may use host-managed setup without bootstrap logging."

### EXTRA-K1-0197
- Closest oracle policies: DEP-021
- Modality: DEFAULT
- Normative action: Serilog.AspNetCore is the baseline integration package; a Console sink suffices for a simple Development baseline; File, Seq, OpenTelemetry, Elasticsearch and enrichers are optional; example limits and retention values are illustrative.
- Trigger/scope: private reference serilog (read by logging)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001402: `output/template/.claude/skills/logging/references/serilog.md:51-51` — "Baseline integration package: `Serilog.AspNetCore`. A Console sink suffices for a simple local Development baseline; File, Seq, OpenTelemetry, Elasticsearch, and enrichers such as `WithMachineName`/`WithEnvironmentName` are optional — add sinks and enrichers only when the project requires them (`add-dependency`). Numeric limits and retention values in examples are illustrative, not approved defaul …"

### EXTRA-K1-0198
- Closest oracle policies: RUN-014
- Modality: MUST_NOT
- Normative action: Never destructure large graphs such as HttpRequest without limits; configure depth/string/collection limits or transform to specific properties.
- Trigger/scope: private reference serilog (read by logging)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001412: `output/template/.claude/skills/logging/references/serilog.md:109-109` — "Never destructure large graphs such as `HttpRequest` without limits; configure `Destructure.ToMaximumDepth/StringLength/CollectionCount` or transform to specific properties (`Destructure.ByTransforming<HttpRequest>(r => new { r.Method, r.Path })`)."

### EXTRA-K1-0199
- Closest oracle policies: DEP-004
- Modality: MUST_NOT
- Normative action: Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks.
- Trigger/scope: private reference serilog (read by logging)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001418: `output/template/.claude/skills/logging/references/serilog.md:127-127` — "- Elasticsearch: the `Serilog.Sinks.Elasticsearch` package is deprecated; use `Elastic.Serilog.Sinks` (`.WriteTo.Elasticsearch([new Uri("https://elastic.example.com:9200")], opts => opts.DataStream = new DataStreamName("logs", "myapp"))`)."

### EXTRA-K1-0200
- Closest oracle policies: DEP-021
- Modality: MUST
- Normative action: When the static/bootstrap Log.Logger is used flush it on shutdown (CloseAndFlushAsync) so asynchronous sinks keep buffered events.
- Trigger/scope: private reference serilog (read by logging)
- Exceptions: Purely host-managed logging follows the provider lifetime.
- Why EXTRA: Not in the oracle.
- Evidence K1-S001421: `output/template/.claude/skills/logging/references/serilog.md:132-132` — "When the static/bootstrap `Log.Logger` is used, flush it on shutdown (`try { app.Run(); } ... finally { await Log.CloseAndFlushAsync(); }`) so asynchronous sinks do not lose buffered events. Purely host-managed logging follows the provider's lifetime instead."

### EXTRA-K1-0201
- Closest oracle policies: RUN-013
- Modality: DEFINITION
- Normative action: Choose levels by operational meaning: Trace/Debug diagnostics (never assume sensitive data is safe there), Information meaningful events, Warning recovered/degraded conditions, Error failed operations needing investigation, Critical when the application or a subsystem cannot continue.
- Trigger/scope: on-demand knowledge logging (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001433: `output/template/.claude/skills/logging/SKILL.md:26-30` — "- **Trace/Debug** — detailed troubleshooting diagnostics; never assume sensitive data is safe at these levels. ⏎ - **Information** — meaningful application events (a background job completed, an important business operation completed, a lifecycle event); not every internal method call. ⏎ - **Warning** — an unexpected or degraded condition the application recovered from (fallback used, retries exha …"
- Evidence K1-S001434: `output/template/.claude/skills/logging/SKILL.md:32-32` — "Choose levels by operational meaning, not by how unusual an event feels."

### EXTRA-K1-0202
- Closest oracle policies: RUN-013
- Modality: PREFER
- Normative action: Prefer platform trace identifiers; add an explicit correlation identifier only for an integration or operational requirement; propagate tracing context across outbound calls.
- Trigger/scope: on-demand knowledge logging (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001439: `output/template/.claude/skills/logging/SKILL.md:47-47` — "Providers enrich scopes differently; provider-specific mechanisms such as Serilog `LogContext` are in the reference. Prefer platform trace identifiers when they already correlate requests; add an explicit correlation identifier only for an integration or operational requirement, validate or normalize one accepted from an external client, and propagate tracing context across outbound calls with the …"

### EXTRA-K1-0203
- Closest oracle policies: RUN-014
- Modality: AVOID
- Normative action: Do not use logs as an audit database (or AuditTo) unless a dedicated audit design was adopted.
- Trigger/scope: on-demand knowledge logging (backend)
- Exceptions: Adopted audit design.
- Why EXTRA: No owner clause for this item.
- Evidence K1-S001419: `output/template/.claude/skills/logging/references/serilog.md:128-128` — "- Audit trails: `AuditTo` (synchronous; exceptions propagate) — only with an adopted audit design."
- Evidence K1-S001447: `output/template/.claude/skills/logging/SKILL.md:69-69` — "String interpolation in log templates, duplicate exception logging, expected business outcomes logged as errors, dumping full objects without review, provider-specific APIs throughout Application code, and using logs as an audit database unless a dedicated audit design was adopted."

### EXTRA-K1-0204
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: Prefer a regular constructor when validation/initialization is non-trivial, explicit fields read better, the codebase uses that style or parameter capture would obscure the class.
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001458: `output/template/.claude/skills/modern-csharp/SKILL.md:25-25` — "Prefer a regular constructor when validation or initialization is non-trivial, explicit fields improve readability, the codebase consistently uses that style, or parameter capture would obscure the class. Never convert constructors mechanically."

### EXTRA-K1-0205
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Use collection expressions when the target type is clear.
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001461: `output/template/.claude/skills/modern-csharp/SKILL.md:34-34` — "Use them when the target type is clear; do not replace existing initializers solely to modernize."

### EXTRA-K1-0206
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Records for intentional value semantics (immutable DTOs, genuine Value Objects, immutable messages); classes for identity, mutable lifecycle, inheritance or framework behaviour; do not turn every DTO or Domain type into a record.
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001463: `output/template/.claude/skills/modern-csharp/SKILL.md:38-38` — "Records fit intentional value semantics: immutable transport DTOs, genuine Value Objects, immutable messages. Classes fit identity, mutable lifecycle, inheritance, or framework behavior; entities with identity normally stay classes. Do not turn every DTO or Domain type into a record."
- Evidence K1-S001492: `output/template/.claude/skills/modern-csharp/SKILL.md:123-123` — "Newest syntax for its own sake, every class as a record, `record struct` merely to avoid allocations, `Span<T>` without a performance reason, mass constructor conversion."

### EXTRA-K1-0207
- Closest oracle policies: ARC-004, API-010
- Modality: DEFINITION
- Normative action: Use required when initialization is part of the valid construction contract, not as a substitute for constructor/domain validation protecting invariants.
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001466: `output/template/.claude/skills/modern-csharp/SKILL.md:46-46` — "Use `required` when initialization is part of the type's valid construction contract — not as a substitute for constructor/domain validation that protects invariants."

### EXTRA-K1-0208
- Closest oracle policies: RUN-009
- Modality: AVOID
- Normative action: Avoid deeply nested patterns that are harder to read than plain conditions.
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001469: `output/template/.claude/skills/modern-csharp/SKILL.md:59-59` — "Avoid deeply nested patterns that are harder to read than plain conditions."

### EXTRA-K1-0209
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: var when the type is obvious or unimportant; an explicit type when it improves clarity; follow the project convention.
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001480: `output/template/.claude/skills/modern-csharp/SKILL.md:103-103` — "- `var` when the type is obvious or unimportant; an explicit type when it improves clarity; follow the project's convention."

### EXTRA-K1-0210
- Closest oracle policies: RUN-009, RUN-024
- Modality: MUST
- Normative action: Standard .NET naming (PascalCase types/members, camelCase parameters/locals, meaningful names; private fields per repository convention).
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001481: `output/template/.claude/skills/modern-csharp/SKILL.md:104-104` — "- Standard .NET naming: PascalCase for types, methods, properties, and public members; camelCase for parameters and locals; meaningful names over abbreviations; private-field naming per the repository's convention."

### EXTRA-K1-0211
- Closest oracle policies: RUN-009
- Modality: MUST
- Normative action: Keep implementation details non-public unless part of the public API; sealed communicates deliberate design, not a speculative JIT optimization.
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001482: `output/template/.claude/skills/modern-csharp/SKILL.md:105-105` — "- Keep implementation details non-public when they are not part of the project's public API; use `sealed` to communicate a deliberate "not for inheritance" design, not as a speculative JIT optimization."

### EXTRA-K1-0212
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Immutability where it represents the model naturally; controlled mutation where framework models or workflows are simpler with it.
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001484: `output/template/.claude/skills/modern-csharp/SKILL.md:107-107` — "- Immutability where it represents the model naturally; controlled mutation where framework models or workflows are simpler with it."

### EXTRA-K1-0213
- Closest oracle policies: DEP-008, ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Confirm the configured language version supports a feature; never silently change LangVersion or the target framework (a platform change is Reserved).
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: LangVersion/TFM gate beyond DEP-008's preview/RC rule.
- Evidence K1-S001488: `output/template/.claude/skills/modern-csharp/SKILL.md:115-115` — "Confirm the configured language version supports a feature before using it; never silently change `LangVersion` or the target framework to use newer syntax (a platform change is Reserved)."

### EXTRA-K1-0214
- Closest oracle policies: RUN-008
- Modality: AVOID
- Normative action: Avoid record struct merely to avoid allocations.
- Trigger/scope: on-demand knowledge modern-csharp (backend)
- Exceptions: none
- Why EXTRA: No owner clause for this item.
- Evidence K1-S001492: `output/template/.claude/skills/modern-csharp/SKILL.md:123-123` — "Newest syntax for its own sake, every class as a record, `record struct` merely to avoid allocations, `Span<T>` without a performance reason, mass constructor conversion."

### EXTRA-K1-0215
- Closest oracle policies: DEP-009, DEP-006
- Modality: DEFAULT
- Normative action: Microsoft.EntityFrameworkCore.SqlServer in Infrastructure, Microsoft.EntityFrameworkCore.Design where design-time tooling needs it (startup project), dotnet-ef as a local tool when the CLI is used.
- Trigger/scope: new solutions
- Exceptions: none
- Why EXTRA: Concrete package set not in the oracle.
- Evidence K1-S001498: `output/template/.claude/skills/persistence-change/SKILL.md:19-19` — "1. Packages through `add-dependency`: `Microsoft.EntityFrameworkCore.SqlServer` in Infrastructure; `Microsoft.EntityFrameworkCore.Design` where design-time tooling needs it (startup project); the `dotnet-ef` tool as a local tool when the project uses the CLI."

### EXTRA-K1-0216
- Closest oracle policies: TST-007, TST-002
- Modality: DEFAULT
- Normative action: Add or update persistence/integration tests when provider behaviour, mappings, constraints or non-trivial queries changed.
- Trigger/scope: workflow persistence-change (persistence model, migrations, seed data)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001512: `output/template/.claude/skills/persistence-change/SKILL.md:46-46` — "6. Add or update persistence/integration tests when provider behavior, mappings, constraints, or non-trivial queries changed (provider fidelity: `ef-core`, Testing)."

### EXTRA-K1-0217
- Closest oracle policies: WF-006, WF-005
- Modality: MUST
- Normative action: Build, run affected tests, start the API against a freshly recreated Development database when seeding or schema changed, run check-cochange, then verify.
- Trigger/scope: workflow persistence-change (persistence model, migrations, seed data)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001514: `output/template/.claude/skills/persistence-change/SKILL.md:50-50` — "Build, run the affected tests, start the API against a freshly recreated Development database when seeding or the schema changed, and run `node "<root>/.claude/scripts/check-cochange.cjs"` (`<root>`: the active repository root; command form in `verify`, Risk-scoped checks). Continue with `verify`."

### EXTRA-K1-0218
- Closest oracle policies: WF-009, PST-010
- Modality: MUST
- Normative action: Report model changes, migration name and review notes (destructive operations called out), seeder updates and verification results.
- Trigger/scope: workflow persistence-change (persistence model, migrations, seed data)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001516: `output/template/.claude/skills/persistence-change/SKILL.md:54-54` — "Model changes, migration name and review notes (destructive operations called out), seeder updates, and verification results."

### EXTRA-K1-0219
- Closest oracle policies: RUN-024
- Modality: MUST
- Normative action: Supporting type roles are clear from name and/or directory (established suffixes; e.g. TaskWorkflowRules over ambiguous TaskWorkflow); responsibility subdirectories only when a flat feature directory becomes hard to navigate.
- Trigger/scope: private reference backend-layout (read by project-structure)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001525: `output/template/.claude/skills/project-structure/references/backend-layout.md:30-30` — "Supporting type roles should be clear from the type name, its directory, or both. Prefer established suffixes: `Service` (use-case orchestration), `Dto`, `Request`/`Response` (Application operation contracts; HTTP contracts belong to Api), `Result`/`Outcome`, `Validator`, `Rules`/`Policy` (decision or workflow rules), `Factory`, `Mapper`, `Adapter`. Avoid ambiguous names such as `TaskWorkflow` whe …"

### EXTRA-K1-0220
- Closest oracle policies: ARC-012, GOV-012
- Modality: MUST_NOT
- Normative action: Extensions hold cohesive composition extensions; do not move code just to shorten Program.cs.
- Trigger/scope: private reference backend-layout (read by project-structure)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001530: `output/template/.claude/skills/project-structure/references/backend-layout.md:45-56` — "```text ⏎ backend/ProjectName.Api/ ⏎ ├── Controllers/ ⏎ ├── Contracts/ ⏎ │   ├── Requests/ ⏎ │   └── Responses/ ⏎ ├── Middleware/               # only when custom middleware exists ⏎ ├── Extensions/               # cohesive composition extensions; do not move code just to shorten Program.cs ⏎ ├── Program.cs                # composition root: AddApplication(); AddInfrastructure(builder.Configuratio …"

### EXTRA-K1-0221
- Closest oracle policies: SEC-009
- Modality: MUST
- Normative action: Configure the API base URL for the Development backend compatible with the backend's CORS configuration.
- Trigger/scope: private reference frontend-setup (read by project-structure)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001547: `output/template/.claude/skills/project-structure/references/frontend-setup.md:16-16` — "4. Configure the API base URL for the Development backend and keep it compatible with the backend's CORS configuration."

### EXTRA-K1-0222
- Closest oracle policies: DEP-014
- Modality: MUST_NOT
- Normative action: Do not impose an obsolete directory structure when the current framework CLI generates a different supported one.
- Trigger/scope: private reference solution-layout (read by project-structure)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001558: `output/template/.claude/skills/project-structure/references/solution-layout.md:38-38` — "The frontend workspace lives outside the .NET tree in `frontend/ProjectName.Web/` and owns its `package.json`, `package-lock.json`, framework configuration, `tsconfig` files, `src/`, and `public/`. Do not impose an obsolete directory structure when the current framework CLI generates a different supported one. Frontend unit/component tests stay inside the workspace (normally colocated with the cod …"

### EXTRA-K1-0223
- Closest oracle policies: DEP-008
- Modality: MUST
- Normative action: global.json pins the intended supported SDK line (current stable SDK of the target release) with servicing per the chosen rollForward policy.
- Trigger/scope: private reference solution-layout (read by project-structure)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001564: `output/template/.claude/skills/project-structure/references/solution-layout.md:48-48` — "- `global.json` — pin the intended supported SDK line: select the current stable SDK for the target .NET release (no RC/preview unless explicitly requested) and allow servicing according to the chosen `rollForward` policy."

### EXTRA-K1-0224
- Closest oracle policies: none
- Modality: PREFER
- Normative action: .editorconfig holds deterministic repository-wide formatting/style; prefer enforceable tooling configuration over restating mechanical formatting rules in instructions.
- Trigger/scope: private reference solution-layout (read by project-structure)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001565: `output/template/.claude/skills/project-structure/references/solution-layout.md:49-49` — "- `.editorconfig` — deterministic repository-wide formatting and code-style configuration; prefer enforceable tooling configuration over restating mechanical formatting rules in instructions."

### EXTRA-K1-0225
- Closest oracle policies: SEC-001
- Modality: MUST
- Normative action: Ignore generated/local artifacts (bin, obj, .vs, node_modules, dist, TestResults, coverage, local secret/config overrides, .claude/settings.local.json); do not ignore files intentionally part of the Development configuration contract.
- Trigger/scope: private reference solution-layout (read by project-structure)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001567: `output/template/.claude/skills/project-structure/references/solution-layout.md:53-53` — "Ignore normal generated/local artifacts where applicable: `bin/`, `obj/`, `.vs/`, `node_modules/`, `dist/`, `TestResults/`, `coverage/`, local secret/config overrides, and the Claude Code local settings file (`settings.local.json` in `.claude/`). Do not ignore files that are intentionally part of the Development configuration contract."

### EXTRA-K1-0226
- Closest oracle policies: DEP-013
- Modality: DEFAULT
- Normative action: Test packages: NUnit, NUnit3TestAdapter, Microsoft.NET.Test.Sdk and, for integration tests, Microsoft.AspNetCore.Mvc.Testing; remove unused template packages.
- Trigger/scope: private reference test-setup (read by project-structure)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001575: `output/template/.claude/skills/project-structure/references/test-setup.md:15-15` — "2. Under Central Package Management, move the template's package versions into `Directory.Packages.props` and keep the project references versionless (`add-dependency` resolves current stable versions): `NUnit`, `NUnit3TestAdapter`, `Microsoft.NET.Test.Sdk`, and for integration tests `Microsoft.AspNetCore.Mvc.Testing`. Remove template packages the project does not use."

### EXTRA-K1-0227
- Closest oracle policies: ARC-001, ARC-020
- Modality: MUST
- Normative action: Project and reference creation changes the reference graph (Reserved): record the requested scaffold or reference first through architecture-decision, listing each reference as 'From -> To', because the hook blocks unrecorded reference commands and reports unrecorded changes.
- Trigger/scope: workflow project-structure (scaffolding, adding/removing projects, restructuring)
- Exceptions: none
- Why EXTRA: Recording-before-command procedure not in the oracle.
- Evidence K1-S001576: `output/template/.claude/skills/project-structure/references/test-setup.md:16-16` — "3. Add only the production project references the test scope requires (`dotnet add <test project> reference <production project>`), recorded first as `From -> To` through `architecture-decision` (`project-structure`, step 4)."
- Evidence K1-S001595: `output/template/.claude/skills/project-structure/SKILL.md:36-36` — "4. **Backend projects and references** — read `references/backend-layout.md`; create the four backend projects and only the references it lists. Never add an outward reference to make compilation easier. Projects and project references change the project reference graph (Reserved): first record the requested scaffold through `architecture-decision` — its accepted decision lists each project refere …"
- Evidence K1-S001604: `output/template/.claude/skills/project-structure/SKILL.md:47-47` — "3. Add only the minimum required references, preserving dependency direction; each new reference is recorded first (`architecture-decision`)."

### EXTRA-K1-0228
- Closest oracle policies: GOV-014, GOV-012
- Modality: MUST_NOT
- Normative action: Do not force an established project to match this template when doing so provides no concrete value.
- Trigger/scope: workflow project-structure (scaffolding, adding/removing projects, restructuring)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001610: `output/template/.claude/skills/project-structure/SKILL.md:61-61` — "Do not force an established project to match this template when doing so provides no concrete value."

### EXTRA-K1-0229
- Closest oracle policies: SEC-003
- Modality: PREFER
- Normative action: Prefer APIs that separate executable and arguments; validate or constrain input when command execution is genuinely needed.
- Trigger/scope: private reference scan-layers (read by security-scan)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001623: `output/template/.claude/skills/security-scan/references/scan-layers.md:55-55` — "Inspect `Process.Start`, shell execution, PowerShell/bash invocation, and command arguments built from user input. Prefer APIs that separate executable and arguments; validate or constrain input when command execution is genuinely needed."

### EXTRA-K1-0230
- Closest oracle policies: SEC-003
- Modality: MUST
- Normative action: Normalize and verify that user-influenced paths remain within the intended storage boundary.
- Trigger/scope: private reference scan-layers (read by security-scan)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001625: `output/template/.claude/skills/security-scan/references/scan-layers.md:59-59` — "Review user-controlled file names, paths, archive extraction, download paths, and upload destinations for `../`, absolute-path injection, escapes from the intended root, and unsafe archive extraction. Normalize and verify that paths remain within the intended storage boundary."

### EXTRA-K1-0231
- Closest oracle policies: SEC-003
- Modality: MUST_NOT
- Normative action: Untrusted payloads must not deserialize into arbitrary runtime types (e.g. BinaryFormatter, unsafe TypeNameHandling).
- Trigger/scope: private reference scan-layers (read by security-scan)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001627: `output/template/.claude/skills/security-scan/references/scan-layers.md:71-71` — "Investigate polymorphic/type-driven deserialization (legacy examples: `BinaryFormatter`, unsafe Newtonsoft `TypeNameHandling`). Untrusted payloads must not deserialize into arbitrary runtime types."

### EXTRA-K1-0232
- Closest oracle policies: SEC-017
- Modality: MUST_NOT
- Normative action: Do not require manually setting every TokenValidationParameters property when authority/metadata configuration establishes secure validation, and do not impose an arbitrary universal ClockSkew.
- Trigger/scope: private reference scan-layers (read by security-scan)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001637: `output/template/.claude/skills/security-scan/references/scan-layers.md:93-93` — "For Bearer/OIDC, inspect whether issuer, audience where applicable, signature/signing authority, and lifetime are validated. Do not require manually setting every `TokenValidationParameters` property when the provider's authority/metadata configuration already establishes secure validation, and do not impose an arbitrary universal `ClockSkew` value. Flag intentionally disabled validation that weak …"

### EXTRA-K1-0233
- Closest oracle policies: SEC-013, RUN-017
- Modality: DEFAULT
- Normative action: Consider rate limiting where abuse realistically matters (login/password reset, expensive anonymous endpoints, resource-intensive operations); do not require it on every endpoint.
- Trigger/scope: private reference scan-layers (read by security-scan)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001651: `output/template/.claude/skills/security-scan/references/scan-layers.md:123-123` — "Consider rate limiting where abuse realistically matters (login/password reset, expensive anonymous endpoints, resource-intensive operations); do not require it on every endpoint. `http-api` covers 429 semantics."

### EXTRA-K1-0234
- Closest oracle policies: ARC-029, SEC-010
- Modality: PREFER
- Normative action: Prefer explicit response contracts where needed, but inspect the serialized fields before calling a returned entity a vulnerability.
- Trigger/scope: private reference scan-layers (read by security-scan)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001656: `output/template/.claude/skills/security-scan/references/scan-layers.md:137-137` — "Look for database/domain entities returned directly, password hashes, internal security fields, unnecessary personal information, and secret metadata. Prefer explicit response contracts where needed, but inspect the actual serialized fields before calling a returned entity a vulnerability."

### EXTRA-K1-0235
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: When meaningful security-sensitive workflows exist, flag them for threat modeling or manual review instead of claiming the scan proves them secure.
- Trigger/scope: private reference scan-layers (read by security-scan)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001671: `output/template/.claude/skills/security-scan/references/scan-layers.md:171-171` — "Static pattern checks do not cover insecure design, tenant isolation, business workflow abuse, privilege escalation through legitimate operations, financial/idempotency abuse, or multi-step authorization problems. When meaningful security-sensitive workflows exist, flag them for threat modeling or dedicated manual review instead of claiming the scan proves them secure."

### EXTRA-K1-0236
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: The scan is an evidence-based static review, not a penetration test, and cannot prove the application secure; state that limitation in the report.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001680: `output/template/.claude/skills/security-scan/SKILL.md:17-17` — "Perform an evidence-based static security review. This is not a penetration test: static review cannot prove the application secure and may miss runtime-only vulnerabilities, infrastructure outside the repository, complex business-logic abuse, sophisticated authorization bypasses, deployment-specific weaknesses, and vulnerabilities that need dynamic exploitation. State that limitation in the repor …"
- Evidence K1-S001715: `output/template/.claude/skills/security-scan/SKILL.md:138-138` — "The scan is complete when all applicable layers were inspected, findings have evidence, uncertain findings are labeled, severity reflects actual risk, limitations are stated, and no layer is marked PASS without being checked."

### EXTRA-K1-0237
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: Inspect which surfaces exist and skip irrelevant checks instead of reporting them as failures.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001691: `output/template/.claude/skills/security-scan/SKILL.md:32-32` — "Inspect which surfaces exist — .NET backend, frontend, authentication/authorization, database access, external HTTP integrations, file upload/download, container configuration, CI/CD, production configuration, logging, caching, background processing — and skip irrelevant checks instead of reporting them as failures. A full pre-release or explicitly requested audit reviews all applicable layers; a  …"

### EXTRA-K1-0238
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: A full pre-release or requested audit reviews all applicable layers; a targeted change focuses on affected layers and expands when it crosses security boundaries.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001691: `output/template/.claude/skills/security-scan/SKILL.md:32-32` — "Inspect which surfaces exist — .NET backend, frontend, authentication/authorization, database access, external HTTP integrations, file upload/download, container configuration, CI/CD, production configuration, logging, caching, background processing — and skip irrelevant checks instead of reporting them as failures. A full pre-release or explicitly requested audit reviews all applicable layers; a  …"
- Evidence K1-S001693: `output/template/.claude/skills/security-scan/SKILL.md:36-44` — ""

### EXTRA-K1-0239
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: Map OWASP Top 10:2025 categories only when they genuinely fit.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001698: `output/template/.claude/skills/security-scan/SKILL.md:60-60` — "OWASP categories: A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging & Alerting Failures, A10 Mishandling of Exceptional Conditions. Map only when a category genuinely fits."

### EXTRA-K1-0240
- Closest oracle policies: WF-020
- Modality: DEFINITION
- Normative action: Severity scale: Critical (sparingly), High, Medium, Low, Info.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001704: `output/template/.claude/skills/security-scan/SKILL.md:72-76` — "- **Critical** — sparingly: exposed real production credentials, reachable authentication bypass, straightforward remote code execution, exploitable injection with major impact. ⏎ - **High** — realistically exploitable or substantially compromises data, authorization, or system behavior. ⏎ - **Medium** — meaningful weakness needing realistic conditions, limited access, or extra steps. ⏎ - **Low**  …"

### EXTRA-K1-0241
- Closest oracle policies: SEC-006, SEC-009, SEC-008
- Modality: DEFINITION
- Normative action: Not automatically vulnerabilities: endpoints without [Authorize] under a secure fallback, bare [Authorize] when authentication alone is intended, AllowAnyOrigin for a public non-credentialed API, MD5/SHA1 checksums, no app-level encryption when platform encryption suffices, obvious fake credentials, secure framework defaults.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001706: `output/template/.claude/skills/security-scan/SKILL.md:80-80` — "Not automatically vulnerabilities: an endpoint without `[Authorize]` under a secure fallback policy; bare `[Authorize]` when authentication alone is intended; `AllowAnyOrigin()` for a genuinely public non-credentialed API; MD5/SHA1 as a non-security checksum; no application-level encryption when platform/storage encryption satisfies the requirement; obviously fake test credentials; framework defau …"

### EXTRA-K1-0242
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: Every confirmed finding includes severity, location, title, evidence, why it is a risk, likely impact, smallest remediation and OWASP category when applicable.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001709: `output/template/.claude/skills/security-scan/SKILL.md:86-86` — "Every confirmed finding includes: severity, file and location, title, evidence, why it is a risk, likely impact, smallest reasonable remediation, and an OWASP category when applicable. Label uncertain items `NEEDS VERIFICATION` instead of presenting them as confirmed."

### EXTRA-K1-0243
- Closest oracle policies: SEC-008, GOV-013
- Modality: MUST_NOT
- Normative action: Prefer the smallest secure change; do not recommend blanket encryption of all fields, security libraries merely to satisfy the scan, or disabling functionality a static scanner cannot understand.
- Trigger/scope: workflow security-scan (security audit or materially security-sensitive change)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001713: `output/template/.claude/skills/security-scan/SKILL.md:134-134` — "Prefer the smallest secure change consistent with the architecture. Do not recommend a new authentication system unnecessarily, custom cryptography, blanket encryption of all database fields, `[Authorize]` on every action when a global policy already protects it, security libraries merely to satisfy the scan, or disabling functionality because a static scanner cannot understand it."

### EXTRA-K1-0244
- Closest oracle policies: ARC-012
- Modality: MUST
- Normative action: Keep Swagger configuration in the Api/composition layer.
- Trigger/scope: on-demand knowledge swagger (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001722: `output/template/.claude/skills/swagger/SKILL.md:32-32` — "Keep Swagger configuration in the Api/composition layer. Package: `Swashbuckle.AspNetCore` (`add-dependency`)."

### EXTRA-K1-0245
- Closest oracle policies: WF-006
- Modality: MUST
- Normative action: Application HTTP/HTTPS URLs must agree with the launch profile; never point a browser launch URL to HTTPS on an HTTP-only port.
- Trigger/scope: on-demand knowledge swagger (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001724: `output/template/.claude/skills/swagger/SKILL.md:36-36` — "A launch profile can open Swagger directly (`"launchBrowser": true, "launchUrl": "swagger"`). The actual HTTP/HTTPS application URLs must agree with the profile; never point a browser launch URL to HTTPS on an HTTP-only port."

### EXTRA-K1-0246
- Closest oracle policies: API-002, API-016
- Modality: DEFAULT
- Normative action: Describe ProblemDetails/ValidationProblemDetails where useful.
- Trigger/scope: on-demand knowledge swagger (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001727: `output/template/.claude/skills/swagger/SKILL.md:50-50` — "Document only statuses in the endpoint's real runtime contract: never `201` when the endpoint returns `200`, never `204` when it returns a body, no speculative entries because a status is theoretically possible. Consider the complete pipeline — model binding, validation, authentication/authorization, rate limiting, centralized exception handling, other middleware — not only explicit controller bra …"

### EXTRA-K1-0247
- Closest oracle policies: API-016
- Modality: DEFAULT
- Normative action: Document what helps consumers (preconditions, idempotency, pagination/filtering, outcomes), not name repetitions; XML comments only when the project chooses them, not on every internal type.
- Trigger/scope: on-demand knowledge swagger (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001731: `output/template/.claude/skills/swagger/SKILL.md:58-58` — "Document what helps a consumer: important preconditions, idempotency semantics, pagination/filtering behavior, meaningful outcomes; avoid descriptions that repeat action or property names. XML comments may document public contracts when the project chooses them; do not add them to every internal type for Swagger."

### EXTRA-K1-0248
- Closest oracle policies: API-016
- Modality: MUST_NOT
- Normative action: Use several documents only for a real contract separation (API versions, public/internal surfaces).
- Trigger/scope: on-demand knowledge swagger (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001733: `output/template/.claude/skills/swagger/SKILL.md:62-62` — "Use several documents only for a real contract separation (API versions, distinct public/internal surfaces); versioning strategy: `api-versioning`."

### EXTRA-K1-0249
- Closest oracle policies: API-016, ARC-029
- Modality: MUST
- Normative action: Avoid unstable anonymous response shapes, use explicit request/response contracts and review generated-client changes when the contract changes.
- Trigger/scope: on-demand knowledge swagger (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001735: `output/template/.claude/skills/swagger/SKILL.md:66-66` — "When the contract feeds frontend or other client generation: treat breaking schema changes seriously, keep metadata accurate, avoid unstable anonymous response shapes, use explicit request/response contracts, and review generated-client changes when the contract changes."
- Evidence K1-S001739: `output/template/.claude/skills/swagger/SKILL.md:74-74` — "Metadata that disagrees with runtime responses, Swagger UI exposed publicly without a reason, Swagger as a substitute for integration tests, anonymous objects as long-lived contracts, and a second competing documentation stack without a concrete need."

### EXTRA-K1-0250
- Closest oracle policies: TST-006
- Modality: MUST_NOT
- Normative action: Swagger is not a substitute for integration tests.
- Trigger/scope: on-demand knowledge swagger (backend)
- Exceptions: none
- Why EXTRA: No owner clause for this item.
- Evidence K1-S001739: `output/template/.claude/skills/swagger/SKILL.md:74-74` — "Metadata that disagrees with runtime responses, Swagger UI exposed publicly without a reason, Swagger as a substitute for integration tests, anonymous objects as long-lived contracts, and a second competing documentation stack without a concrete need."

### EXTRA-K1-0251
- Closest oracle policies: none
- Modality: MUST
- Normative action: Implementation-specific content of a slot becomes a facet listed in the module manifest with 'Capability: <slot>/<implementation>'; implementation-independent slot policy stays in the neutral standard; placement belongs to the architecture frame, technique to leaves declaring frame bindings in Binds:.
- Trigger/scope: repo/meta (instruction-system change)
- Exceptions: none
- Why EXTRA: Instruction-system placement rule.
- Evidence K1-S001747: `output/template/.claude/skills/template-maintenance/SKILL.md:18-18` — "1. **Capability** — is it specific to the selected implementation of a slot (architecture, persistence, backend-testing, frontend)? Yes → the module owns it: it becomes a facet listed in that module's manifest (`.claude/capabilities/<slot>/<implementation>/MODULE.md`), and its header declares `Capability: <slot>/<implementation>`. No → non-slot content with `Capability: —`. Implementation-independ …"

### EXTRA-K1-0252
- Closest oracle policies: none
- Modality: MUST
- Normative action: A rule's paths include its scope's canonical glob (**/*, backend/**/*, backend/**/*Tests/**/*, frontend/**/*); no other directory hierarchy under .claude/rules/.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Instruction-system rule.
- Evidence K1-S001751: `output/template/.claude/skills/template-maintenance/SKILL.md:31-31` — "3. **Scope** — `common`, `backend`, `backend-tests`, `frontend`, `delivery`, `repo/meta`. A rule's `paths:` must include its scope's canonical glob (`**/*`, `backend/**/*`, `backend/**/*Tests/**/*`, `frontend/**/*`); no other directory hierarchy under `.claude/rules/`."

### EXTRA-K1-0253
- Closest oracle policies: none
- Modality: MUST
- Normative action: Every normative statement has exactly one owner; elsewhere only a routing pointer, a check-by-reference item or a register decision summary.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Instruction-system rule.
- Evidence K1-S001753: `output/template/.claude/skills/template-maintenance/SKILL.md:35-35` — "- Every normative statement has exactly one owner. Elsewhere use only a routing pointer ("run `x`"), a check-by-reference item pointing at the owner, or a decision summary in the decision register."

### EXTRA-K1-0254
- Closest oracle policies: none
- Modality: MUST
- Normative action: Keep the trigger role: always-loaded policy in OP/DEC, path policy in STD, procedure obligations in WF; do not move content between roles to save tokens; never place critical must-policy only in a skill.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Instruction-system rule.
- Evidence K1-S001755: `output/template/.claude/skills/template-maintenance/SKILL.md:37-37` — "- Trigger role is part of the content: always-loaded policy stays in OP/DEC, path policy in STD, procedure obligations in WF. Do not move content between roles to save tokens or to make loading easier; never place critical must-policy only in a skill."

### EXTRA-K1-0255
- Closest oracle policies: none
- Modality: MUST_NOT
- Normative action: Outside a module's facets, manifest, the register's selection block and the map, never name the selected implementation; facet file names are role-based.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Instruction-system rule.
- Evidence K1-S001757: `output/template/.claude/skills/template-maintenance/SKILL.md:39-39` — "- Leak rule: outside a module's facets, its manifest, the decision register's capability-selection block, and the maintainer map, never name the selected implementation; refer to slot and facet roles instead. Facet file names are role-based (`test-framework.md`, not the implementation's name)."

### EXTRA-K1-0256
- Closest oracle policies: none
- Modality: MUST
- Normative action: Start each artifact with the header 'Kind | Scope | Capability | Loading' (after required frontmatter).
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Instruction-system rule.
- Evidence K1-S001759: `output/template/.claude/skills/template-maintenance/SKILL.md:43-43` — "1. Start each artifact with the one-line header `Kind | Scope | Capability | Loading` (after frontmatter where frontmatter is required)."

### EXTRA-K1-0257
- Closest oracle policies: none
- Modality: MUST
- Normative action: Skill frontmatter name equals the directory and the description is concise and trigger-first; WF bodies own procedure and output; KNW bodies own technique and point to standards for policy.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Instruction-system rule.
- Evidence K1-S001760: `output/template/.claude/skills/template-maintenance/SKILL.md:44-44` — "2. Skills: frontmatter `name` equal to the directory, a concise trigger-first `description` with concrete cues; WF bodies own procedure and output shape; KNW bodies own technique and point to standards for policy."

### EXTRA-K1-0258
- Closest oracle policies: ARC-020
- Modality: MUST
- Normative action: Capability changes follow architecture-decision (contract coverage, single implementation per slot, no unselected implementations at runtime).
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Instruction-system rule.
- Evidence K1-S001761: `output/template/.claude/skills/template-maintenance/SKILL.md:45-45` — "3. Capability changes: follow `architecture-decision` (contract coverage, single implementation per slot, no unselected implementations at runtime)."

### EXTRA-K1-0259
- Closest oracle policies: none
- Modality: MUST
- Normative action: Update the module manifest's facet table and both MAP views for every added, moved or removed artifact.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Instruction-system rule.
- Evidence K1-S001762: `output/template/.claude/skills/template-maintenance/SKILL.md:46-46` — "4. Update the module manifest's facet table and `.claude/MAP.md` (both views) for every added, moved, or removed artifact."

### EXTRA-K1-0260
- Closest oracle policies: none
- Modality: MUST
- Normative action: Hooks use exec form (node + [dispatch.cjs launcher, event]); the launcher only locates code while checks use the active root from the hook input cwd; the PreToolUse guard keeps onFailure block; post and Stop hooks stay advisory; hook messages point to owners.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Instruction-system rule.
- Evidence K1-S001763: `output/template/.claude/skills/template-maintenance/SKILL.md:47-47` — "5. Hooks: exec form only (`"command": "node"`, `"args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dispatch.cjs", "<event>"]`); `${CLAUDE_PROJECT_DIR}` only locates the hook code, while every check uses the active repository or worktree derived from the hook input `cwd`. The dependency and reference guard (PreToolUse) keeps `"onFailure": "block"`; post-tool and Stop hooks stay advisory. Hook messages p …"

### EXTRA-K1-0261
- Closest oracle policies: none
- Modality: MUST
- Normative action: ENF artifacts declare their policy owners on the line after the header ('Conforms: …' or '—') and every cited owner path is declared; slot bindings and facet roles are fixed; contract and manifest Binds agree.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Instruction-system rule.
- Evidence K1-S001764: `output/template/.claude/skills/template-maintenance/SKILL.md:48-48` — "6. Enforcement artifacts (ENF) declare their policy owners on the line after the header: `Conforms: <STD or DEC owner>, …` or `Conforms: —`; every standard or register path an ENF artifact cites must be declared. Slot binding obligations (persistence and backend-testing bind architecture) and the contract's facet roles are fixed; keep `Binds:` in the contract and the manifest in agreement."

### EXTRA-K1-0262
- Closest oracle policies: none
- Modality: MUST
- Normative action: Run check-instructions with the active root and fix every error; review the always-loaded size and keep it compact without moving required planning-time policy out.
- Trigger/scope: repo/meta: template-maintenance (instruction-system changes; user-invoked only)
- Exceptions: none
- Why EXTRA: Instruction-system rule.
- Evidence K1-S001766: `output/template/.claude/skills/template-maintenance/SKILL.md:52-52` — "Run `node "<root>/.claude/scripts/check-instructions.cjs"` (`<root>`: the active repository root; command form in `verify`, Risk-scoped checks) and fix every error. Review the reported always-loaded size; keep it compact without moving required planning-time policy out of the always-loaded surface."

### EXTRA-K1-0263
- Closest oracle policies: WF-005
- Modality: MUST_NOT
- Normative action: Do not use --no-restore unless restore is known to be complete.
- Trigger/scope: workflow verify (before declaring work finished)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001776: `output/template/.claude/skills/verify/SKILL.md:31-31` — "Build the affected solution or projects (`dotnet build`, or a targeted project/solution path). For frontend changes, inspect `package.json` and run the workspace's declared build script (typically `npm run build`). Do not use `--no-restore` unless restore is known to be complete. A build failure means the implementation is not complete."

### EXTRA-K1-0264
- Closest oracle policies: WF-005
- Modality: DEFAULT
- Normative action: Small solutions run the full suite; large solutions run affected test projects first, then the broader suite required.
- Trigger/scope: workflow verify (before declaring work finished)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001778: `output/template/.claude/skills/verify/SKILL.md:35-35` — "Run tests covering the changed area (`dotnet test`, targeted where useful; the frontend's declared test script when one exists — inspect `package.json` rather than assuming a runner). Small solutions: run the full suite. Large solutions: affected test projects first, then the broader suite required by the repository or the change risk. Investigate every newly failing relevant test; never dismiss a …"

### EXTRA-K1-0265
- Closest oracle policies: none
- Modality: MUST
- Normative action: Run checker commands by absolute path (node "<root>/.claude/scripts/<checker>.cjs", root from git rev-parse --show-toplevel or the directory holding CLAUDE.md and .claude/).
- Trigger/scope: repo/meta
- Exceptions: none
- Why EXTRA: Command-form rule not in the oracle.
- Evidence K1-S001785: `output/template/.claude/skills/verify/SKILL.md:49-49` — "Checker commands work from any directory of the active repository or worktree: run them by absolute path, `node "<root>/.claude/scripts/<checker>.cjs"`, where `<root>` is the output of `git rev-parse --show-toplevel` (outside Git: the directory that holds `CLAUDE.md` and `.claude/`). Each checker inspects the repository or worktree that contains the current directory and prints the root it checked …"

### EXTRA-K1-0266
- Closest oracle policies: PST-008, TST-009
- Modality: DEFAULT
- Normative action: Run check-cochange for seed, migration and test reminders of the working tree.
- Trigger/scope: workflow verify (before declaring work finished)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001787: `output/template/.claude/skills/verify/SKILL.md:53-53` — "- **Co-change reminders:** `node "<root>/.claude/scripts/check-cochange.cjs"` (seed, migration, and test reminders for the working tree)."

### EXTRA-K1-0267
- Closest oracle policies: none
- Modality: MUST
- Normative action: When .claude/, CLAUDE.md or the register changed run check-instructions.
- Trigger/scope: repo/meta
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001790: `output/template/.claude/skills/verify/SKILL.md:56-56` — "- **Instruction system:** when `.claude/`, `CLAUDE.md`, or the decision register changed, run `node "<root>/.claude/scripts/check-instructions.cjs"`."

### EXTRA-K1-0268
- Closest oracle policies: WF-004
- Modality: MUST
- Normative action: Final diff review also checks commented-out code, temporary logging, unintended TODO/FIXME markers and stale temporary tests or scripts.
- Trigger/scope: workflow verify (before declaring work finished)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001792: `output/template/.claude/skills/verify/SKILL.md:60-60` — "Review the final diff after all fixes. Check for accidental unrelated edits, commented-out code, temporary logging, unintended TODO/FIXME markers, stale temporary tests or scripts, architecture drift, unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`, stale code/tests/docs/config after a settings change, and behavior verified manually but never preserved as a test."

### EXTRA-K1-0269
- Closest oracle policies: RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: UTF-8, space indentation of 4 (2 for JSON/YAML/project/XML and TS/JS/HTML/SCSS/CSS), final newline, trimmed trailing whitespace (not in Markdown).
- Trigger/scope: all files (.editorconfig; C# rules for *.cs)
- Exceptions: none
- Why EXTRA: Concrete formatting settings not in the oracle.
- Evidence K1-S001804: `output/template/.editorconfig:8-21` — "charset = utf-8 ⏎ indent_style = space ⏎ indent_size = 4 ⏎ insert_final_newline = true ⏎ trim_trailing_whitespace = true ⏎  ⏎ [*.{json,yml,yaml,props,targets,csproj,slnx,xml}] ⏎ indent_size = 2 ⏎  ⏎ [*.{ts,js,cjs,mjs,html,scss,css}] ⏎ indent_size = 2 ⏎  ⏎ [*.md] ⏎ trim_trailing_whitespace = false"

### EXTRA-K1-0270
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: System directives sorted first; import groups not separated.
- Trigger/scope: all files (.editorconfig; C# rules for *.cs)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001808: `output/template/.editorconfig:26-27` — "dotnet_sort_system_directives_first = true ⏎ dotnet_separate_import_directive_groups = false"

### EXTRA-K1-0271
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: var suggested when the type is apparent; explicit types suggested for built-in types; silent elsewhere.
- Trigger/scope: all files (.editorconfig; C# rules for *.cs)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001811: `output/template/.editorconfig:31-33` — "csharp_style_var_for_built_in_types = false:suggestion ⏎ csharp_style_var_when_type_is_apparent = true:suggestion ⏎ csharp_style_var_elsewhere = false:silent"

### EXTRA-K1-0272
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: Primary constructors (silent), collection expressions and switch expressions (suggestion), pattern matching (silent).
- Trigger/scope: all files (.editorconfig; C# rules for *.cs)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001813: `output/template/.editorconfig:36-39` — "csharp_style_prefer_primary_constructors = true:silent ⏎ dotnet_style_prefer_collection_expression = when_types_loosely_match:suggestion ⏎ csharp_style_prefer_switch_expression = true:suggestion ⏎ csharp_style_prefer_pattern_matching = true:silent"

### EXTRA-K1-0273
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: Braces suggested when multiline; expression-bodied methods on single lines and properties (silent).
- Trigger/scope: all files (.editorconfig; C# rules for *.cs)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001815: `output/template/.editorconfig:42-44` — "csharp_prefer_braces = when_multiline:suggestion ⏎ csharp_style_expression_bodied_methods = when_on_single_line:silent ⏎ csharp_style_expression_bodied_properties = true:silent"

### EXTRA-K1-0274
- Closest oracle policies: RUN-009, RUN-024
- Modality: ENFORCED_ADVISORY
- Normative action: I-prefix for interfaces and PascalCase for types and members (suggestion).
- Trigger/scope: all files (.editorconfig; C# rules for *.cs)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S001817: `output/template/.editorconfig:47-58` — "dotnet_naming_rule.interfaces_should_begin_with_i.symbols = interface_symbols ⏎ dotnet_naming_rule.interfaces_should_begin_with_i.style = prefix_i_style ⏎ dotnet_naming_rule.interfaces_should_begin_with_i.severity = suggestion ⏎ dotnet_naming_symbols.interface_symbols.applicable_kinds = interface ⏎ dotnet_naming_style.prefix_i_style.required_prefix = I ⏎ dotnet_naming_style.prefix_i_style.capitali …"

### EXTRA-K1-0020
- Closest oracle policies: DEP-003, DEP-025, ARC-001
- Modality: ENFORCED
- Normative action: The PreToolUse guard fails closed: internal errors, empty/malformed/mismatched hook input and host-level failures (onFailure block) block the command; Post and Stop failures are advisory (exit 1).
- Trigger/scope: PreToolUse Bash/PowerShell
- Exceptions: none
- Why EXTRA: Fail-closed enforcement policy not in the oracle.
- Evidence K1-S000091: `output/template/.claude/hooks/dispatch.cjs:5-12` — "PreToolUse guards policy-critical commands and fails closed"
- Evidence K1-S000103: `output/template/.claude/hooks/dispatch.cjs:143-153` — "function main(event) { ⏎   run(event).then( ⏎     code => { ⏎       process.exitCode = code; ⏎     }, ⏎     err => { ⏎       const critical = CRITICAL.has(event); ⏎       process.stderr.write(`[hook ${event}] ${critical ? 'blocked (fail closed)' : 'failed'}: ${err && err.message ? err.message : err}\n`); ⏎       process.exitCode = critical ? 2 : 1; ⏎     }); ⏎ }"
- Evidence K1-S000125: `output/template/.claude/MAP.md:100-114` — "fails closed"
- Evidence K1-S000568: `output/template/.claude/settings.json:12-12` — ""onFailure": "block""

### EXTRA-K1-0021
- Closest oracle policies: ARC-001, ARC-020
- Modality: ENFORCED
- Normative action: dotnet project-reference add/remove commands are blocked before execution unless every named edge is recorded as an approved 'From -> To' in the decision register's Accepted decisions.
- Trigger/scope: PreToolUse Bash/PowerShell
- Exceptions: Recorded approval for every edge.
- Why EXTRA: Reference-graph approval gate not in the oracle.
- Evidence K1-S000096: `output/template/.claude/hooks/dispatch.cjs:71-75` — "if (findings.some(f => f.kind === 'reference-change')) { ⏎     const manifests = require('../scripts/check-manifests.cjs'); ⏎     const approvals = manifests.acceptedDecisionText(lib.activeRoot(cwd)); ⏎     findings = findings.filter(f => f.kind !== 'reference-change' || !f.edges.length || f.edges.some(e => !manifests.isApprovedEdge(approvals, e.from, e.to))); ⏎   }"
- Evidence K1-S000521: `output/template/.claude/scripts/classify-command.cjs:301-306` — "if (kind === 'reference') { ⏎     if (action === 'update') return []; ⏎     const from = projectName(project, cwd); ⏎     const edges = positional.map(ref => ({ from, to: projectName(ref, cwd) })); ⏎     return [{ kind: 'reference-change', segment, action, edges }]; ⏎   }"

### EXTRA-K1-0022
- Closest oracle policies: PST-008, PST-010, TST-009
- Modality: ENFORCED_ADVISORY
- Normative action: At Stop, co-change reminders block finishing once per content state: address each item or state why it does not apply; the hook never re-blocks its own continuation and is inactive (system message) outside a Git work tree.
- Trigger/scope: Stop (dispatch.cjs + check-cochange.cjs)
- Exceptions: none
- Why EXTRA: Stop-gate mechanism not in the oracle.
- Evidence K1-S000101: `output/template/.claude/hooks/dispatch.cjs:115-128` — "function stop(input) { ⏎   if (input.stop_hook_active) return 0; // never re-block a continuation triggered by this hook ⏎   const cochange = require('../scripts/check-cochange.cjs'); ⏎   const result = cochange.run(lib.activeRoot(workingDirectory(input)), 'hook'); ⏎   if (!result.applicable) { ⏎     process.stdout.write(`${JSON.stringify({ systemMessage: 'Co-change reminders inactive: the project …"
- Evidence K1-S000125: `output/template/.claude/MAP.md:100-114` — "fails closed"

### EXTRA-K1-0023
- Closest oracle policies: DEP-001, DEP-006
- Modality: ENFORCED
- Normative action: Package removal commands (npm/pnpm/yarn remove variants, dotnet remove … package, dotnet package remove) are blocked before execution and routed to add-dependency (removal).
- Trigger/scope: PreToolUse Bash/PowerShell (classify-command.cjs via dispatch.cjs)
- Exceptions: none
- Why EXTRA: Removal gate not in the oracle.
- Evidence K1-S000516: `output/template/.claude/scripts/classify-command.cjs:244-244` — "if (category === 'remove') findings.push({ kind: 'dependency-removal', segment, specs });"
- Evidence K1-S000522: `output/template/.claude/scripts/classify-command.cjs:307-307` — "if (action === 'remove') return [{ kind: 'dependency-removal', segment, specs: positional }];"
- Evidence K1-S000702: `output/template/.claude/skills/add-dependency/SKILL.md:78-78` — "The dependency-command hook blocks removal commands (`npm uninstall`, `dotnet remove … package`, and equivalents) so that removals pass this checklist: remove the entry from the manifest (the project `PackageReference`, plus the central `PackageVersion` when no project uses it any more; the `package.json` entry), then restore (`dotnet restore`, `npm install`) so the lockfile stays consistent."
- Evidence K1-S000705: `output/template/.claude/skills/add-dependency/SKILL.md:84-84` — "routes additions and updates without an exact version"

### EXTRA-K1-0024
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Commands nested in more than three shell wrappers are blocked as unclassifiable; the command must be run directly.
- Trigger/scope: PreToolUse Bash/PowerShell (classify-command.cjs via dispatch.cjs)
- Exceptions: none
- Why EXTRA: Classifier-depth rule not in the oracle.
- Evidence K1-S000526: `output/template/.claude/scripts/classify-command.cjs:334-334` — "else findings.push({ kind: 'unclassifiable', segment });"

### EXTRA-K1-0025
- Closest oracle policies: ARC-001, ARC-020
- Modality: ENFORCED_ADVISORY
- Normative action: Project-reference edges added or removed relative to the previous observation and HEAD, and non-test projects added or removed, are errors unless an accepted decision records the edge ('From -> To') or names the project.
- Trigger/scope: PostToolUse / PostToolUseFailure (actual-state.cjs via dispatch.cjs)
- Exceptions: Recorded approval; committed history and reverted edits are not pending changes.
- Why EXTRA: Reference-graph approval check not in the oracle.
- Evidence K1-S000418: `output/template/.claude/scripts/actual-state.cjs:5-9` — "Reference-graph changes count only while they differ from HEAD"
- Evidence K1-S000420: `output/template/.claude/scripts/actual-state.cjs:107-129` — "/** Reference-graph findings for one project file: (current Δ base) ∩ (current Δ HEAD), minus recorded approvals. */ ⏎ function graphFindings(rel, current, base, head, hasHead, approvals, roleOf) { ⏎   const name = path.posix.basename(rel).replace(/\.csproj$/i, ''); ⏎   const key = s => s.toLowerCase(); ⏎   const cur = new Map((current || []).map(e => [key(e), e])); ⏎   const bas = new Map((base | …"

### EXTRA-K1-0026
- Closest oracle policies: DEP-007, DEP-001
- Modality: ENFORCED_ADVISORY
- Normative action: Deleting a package.json produces a warning that dependency removals go through add-dependency.
- Trigger/scope: PostToolUse / PostToolUseFailure (actual-state.cjs via dispatch.cjs)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000426: `output/template/.claude/scripts/actual-state.cjs:189-189` — "else if (path.posix.basename(rel) === 'package.json') findings.push(lib.finding('warn', rel, 'dependency manifest was deleted; dependency removals go through the add-dependency workflow', '.claude/rules/frontend/dependencies.md'));"

### EXTRA-K1-0027
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: A change to CLAUDE.md, the register or .claude/ instruction files runs check-instructions and returns its errors (template-maintenance).
- Trigger/scope: repo/meta (instruction-system change)
- Exceptions: none
- Why EXTRA: Instruction-system checker invariants.
- Evidence K1-S000428: `output/template/.claude/scripts/actual-state.cjs:205-208` — "let instructionErrors = []; ⏎   if (instructionChanged) { ⏎     instructionErrors = require('./check-instructions.cjs').check(root).filter(f => f.severity === 'error'); ⏎   }"

### EXTRA-K1-0028
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: One role-named facet check per capability slot is composed statically; a missing required facet check (architecture, persistence, backend-testing) is an error; the optional frontend facet may be absent when its selection is none.
- Trigger/scope: repo/meta (capability enforcement)
- Exceptions: none
- Why EXTRA: Capability-facet composition not in the oracle.
- Evidence K1-S000478: `output/template/.claude/scripts/check-manifests.cjs:9-16` — "// Static composition: one role-named facet check per capability slot (no discovery). ⏎ // "required" facets must exist; the optional frontend slot may be absent when its selection is "none". ⏎ const FACETS = [ ⏎   { slot: 'architecture', file: 'facets/architecture-style.cjs', required: true }, ⏎   { slot: 'persistence', file: 'facets/persistence-technology.cjs', required: true }, ⏎   { slot: 'bac …"
- Evidence K1-S000483: `output/template/.claude/scripts/check-manifests.cjs:35-48` — "function loadFacets() { ⏎   const facets = {}; ⏎   for (const facet of FACETS) { ⏎     const abs = path.join(__dirname, facet.file); ⏎     if (!fs.existsSync(abs)) { ⏎       if (facet.required) { ⏎         throw new Error(`Required capability facet check missing for slot "${facet.slot}": ${lib.toPosix(path.relative(path.join(__dirname, '..', '..'), abs))}`); ⏎       } ⏎       continue; ⏎     } ⏎   …"

### EXTRA-K1-0029
- Closest oracle policies: DEP-004, DEP-020
- Modality: ENFORCED_ADVISORY
- Normative action: Microsoft.Extensions.Http.Polly and Polly.Extensions.Http in project or central package references are errors (deprecated resilience integration packages).
- Trigger/scope: check-manifests.cjs (manifest hooks, verify)
- Exceptions: none
- Why EXTRA: Concrete deny list not in the oracle.
- Evidence K1-S000480: `output/template/.claude/scripts/check-manifests.cjs:24-28` — "// Approved-stack exceptions owned by the add-dependency workflow. ⏎ const NUGET_DENY = new Map([ ⏎   ['microsoft.extensions.http.polly', 'deprecated resilience integration package'], ⏎   ['polly.extensions.http', 'deprecated resilience integration package'], ⏎ ]);"
- Evidence K1-S000487: `output/template/.claude/scripts/check-manifests.cjs:90-91` — "const denied = NUGET_DENY.get(pkg.id.toLowerCase()); ⏎     if (denied) findings.push(lib.finding('error', rel, `"${pkg.id}": ${denied}`, OWNER_WORKFLOW));"
- Evidence K1-S000493: `output/template/.claude/scripts/check-manifests.cjs:116-116` — "if (NUGET_DENY.has(id)) findings.push(lib.finding('error', rel, `"${pkg.id}": ${NUGET_DENY.get(id)}`, OWNER_WORKFLOW));"

### EXTRA-K1-0030
- Closest oracle policies: DEP-020
- Modality: ENFORCED_ADVISORY
- Normative action: Central versions for Polly or Polly.Core produce a warning that direct Polly usage is a documented exception.
- Trigger/scope: check-manifests.cjs (manifest hooks, verify)
- Exceptions: none
- Why EXTRA: Documentation requirement not in the oracle.
- Evidence K1-S000481: `output/template/.claude/scripts/check-manifests.cjs:29-32` — "const NUGET_EXCEPTION = new Map([ ⏎   ['polly', 'direct Polly usage is a documented exception'], ⏎   ['polly.core', 'direct Polly usage is a documented exception'], ⏎ ]);"
- Evidence K1-S000494: `output/template/.claude/scripts/check-manifests.cjs:117-117` — "if (NUGET_EXCEPTION.has(id)) findings.push(lib.finding('warn', rel, `"${pkg.id}": ${NUGET_EXCEPTION.get(id)}`, OWNER_WORKFLOW));"

### EXTRA-K1-0031
- Closest oracle policies: DEP-006
- Modality: ENFORCED_ADVISORY
- Normative action: A PackageReference using VersionOverride produces a warning to record the reason.
- Trigger/scope: check-manifests.cjs (manifest hooks, verify)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000486: `output/template/.claude/scripts/check-manifests.cjs:87-89` — "if (pkg.versionOverride) { ⏎       findings.push(lib.finding('warn', rel, `PackageReference "${pkg.id}" uses VersionOverride; record the reason`, OWNER_NUGET)); ⏎     }"

### EXTRA-K1-0032
- Closest oracle policies: ARC-020, GOV-017
- Modality: ENFORCED
- Normative action: Approvals for Reserved reference-graph or project changes count only when recorded in a register Accepted-decisions row with a valid ISO date (placeholders do not count), or in a docs/decisions record it links, listing the edge as 'From -> To' or naming the project.
- Trigger/scope: check-manifests.cjs (manifest hooks, verify)
- Exceptions: none
- Why EXTRA: Approval-record format not in the oracle.
- Evidence K1-S000504: `output/template/.claude/scripts/check-manifests.cjs:192-233` — "/** A real calendar date in the register's ISO form YYYY-MM-DD; placeholders such as TBD or pending are not dates. */ ⏎ function isIsoDate(value) { ⏎   const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value); ⏎   if (!m) return false; ⏎   const [year, month, day] = m.slice(1).map(Number); ⏎   const leap = (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0; ⏎   const days = [31, leap ? 29 : 28, 31, …"

### EXTRA-K1-0033
- Closest oracle policies: ARC-028
- Modality: ENFORCED_ADVISORY
- Normative action: A test project referencing another test project produces a warning.
- Trigger/scope: architecture-style facet (check-manifests: manifest hooks, verify)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000534: `output/template/.claude/scripts/facets/architecture-style.cjs:57-61` — "} else if (role.kind === 'test') { ⏎       if (target.kind === 'test') { ⏎         findings.push(lib.finding('warn', project.rel, `test project references another test project "${ref.name}"`, OWNER_TESTS)); ⏎         continue; ⏎       }"

### EXTRA-K1-0034
- Closest oracle policies: PST-009, PST-010
- Modality: ENFORCED_ADVISORY
- Normative action: Persistence model changes without a migration produce a reminder to confirm whether the schema changed.
- Trigger/scope: Stop hook / verify (check-cochange)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000554: `output/template/.claude/scripts/facets/persistence-technology.cjs:40-47` — "if (model.length && !migrations.length) { ⏎     reminders.push({ ⏎       id: 'persistence-migration', ⏎       message: 'persistence model changed without a migration; confirm whether the schema changed', ⏎       owner: OWNER_WF, ⏎       paths: model, ⏎     }); ⏎   }"

### EXTRA-K1-0035
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: Every instruction artifact carries the first-line header 'Kind | Scope | Capability | Loading' with a known Kind allowed at its location, a known Scope and a well-formed Capability; Level headers are not used; project-owned files only warn.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: SPECIFICATION.md is exempt.
- Why EXTRA: Instruction-system structure invariant.
- Evidence K1-S000442: `output/template/.claude/scripts/check-instructions.cjs:151-165` — "function checkHeaders(artifacts, out) { ⏎   for (const a of artifacts.values()) { ⏎     if (a.rel === 'SPECIFICATION.md') continue; // product input; intentionally empty in the template ⏎     if (!validHeader(a)) { ⏎       out.push(lib.finding(PROJECT_OWNED.includes(a.rel) ? WARN : ERR, a.rel, 'missing or malformed header "Kind | Scope | Capability | Loading" on the first content line')); ⏎        …"

### EXTRA-K1-0036
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: Rules live only in .claude/rules/<scope>/<topic>.md with the header Scope equal to the directory and non-empty paths frontmatter including the scope's canonical glob.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: Delivery rules declare their own globs.
- Why EXTRA: Standard-placement invariant.
- Evidence K1-S000443: `output/template/.claude/scripts/check-instructions.cjs:167-189` — "function checkRules(root, artifacts, out) { ⏎   for (const dir of lib.walk(root, '.claude/rules').map(r => r.split('/')[2]).filter(Boolean)) { ⏎     if (!RULE_SCOPE_DIRS.includes(dir)) out.push(lib.finding(ERR, `.claude/rules/${dir}`, 'rules are organized only by scope directory')); ⏎   } ⏎   for (const a of artifacts.values()) { ⏎     if (!a.rel.startsWith('.claude/rules/')) continue; ⏎     const …"

### EXTRA-K1-0037
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: CLAUDE.md imports the decision register; imports must resolve and only OP/DEC artifacts may be imported; only CLAUDE.md contains @ imports.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: none
- Why EXTRA: Always-loaded surface invariant.
- Evidence K1-S000444: `output/template/.claude/scripts/check-instructions.cjs:191-209` — "function checkImports(root, artifacts, out) { ⏎   const claude = artifacts.get('CLAUDE.md'); ⏎   if (!claude) { ⏎     out.push(lib.finding(ERR, 'CLAUDE.md', 'missing')); ⏎     return []; ⏎   } ⏎   const imports = claude.body.split(/\r?\n/).map(l => /^@(\S+)\s*$/.exec(l.trim())).filter(Boolean).map(m => lib.toPosix(path.posix.normalize(m[1]))); ⏎   if (!imports.includes(REGISTER)) out.push(lib.find …"

### EXTRA-K1-0038
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: Every skill directory has a SKILL.md whose frontmatter name equals the directory and which has a description (warning above 450 characters); no standalone serilog/resilience skills; template-maintenance is user-only; required workflows (WF) and knowledge skills (KNW) exist with the right Kind.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: none
- Why EXTRA: Skill-structure invariants.
- Evidence K1-S000446: `output/template/.claude/scripts/check-instructions.cjs:220-243` — "function checkSkills(root, artifacts, skills, out) { ⏎   for (const dir of new Set(lib.walk(root, '.claude/skills').map(r => r.split('/')[2]))) { ⏎     if (!skills.has(dir)) out.push(lib.finding(ERR, `.claude/skills/${dir}`, 'skill directory without SKILL.md')); ⏎   } ⏎   for (const [name, a] of skills) { ⏎     if (frontmatterValue(a.frontmatter, 'name') !== name) out.push(lib.finding(ERR, a.rel,  …"

### EXTRA-K1-0039
- Closest oracle policies: WF-010
- Modality: ENFORCED_ADVISORY
- Normative action: The agent body above 15 non-blank lines produces a warning: keep it a thin delegate.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence K1-S000448: `output/template/.claude/scripts/check-instructions.cjs:255-256` — "const lines = a.body.split(/\r?\n/).filter(l => l.trim()).length; ⏎   if (lines > 15) out.push(lib.finding(WARN, rel, `agent body has ${lines} lines; keep it a thin delegate`));"

### EXTRA-K1-0040
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: Backtick references must resolve (unknown skills, unresolved or ambiguous references are errors); skill-private references are used only within their skill; non-routing references follow WF → KNW → STD → DEC → OP; a standard depends on another standard only when that scope loads reliably; the conformance graph is acyclic; pointers to dormant facet roles are allowed.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: Routing pointers (skills, agents, SKILL.md files) and enforcement pointers are not dependencies.
- Why EXTRA: Conformance-direction invariant.
- Evidence K1-S000452: `output/template/.claude/scripts/check-instructions.cjs:281-285` — "must follow"
- Evidence K1-S000453: `output/template/.claude/scripts/check-instructions.cjs:286-348` — "function checkReferences(root, artifacts, skills, dormant, graph, out) { ⏎   const basenameIndex = new Map(); ⏎   for (const rel of artifacts.keys()) { ⏎     const base = path.posix.basename(rel); ⏎     basenameIndex.set(base, [...(basenameIndex.get(base) || []), rel]); ⏎   } ⏎   const agents = new Set([...artifacts.keys()].filter(r => r.startsWith('.claude/agents/')).map(r => path.posix.basename( …"
- Evidence K1-S000472: `output/template/.claude/scripts/check-instructions.cjs:787-788` — "const cycle = findCycle(graph.conformance); ⏎   if (cycle) out.push(lib.finding(ERR, cycle[0], `conformance dependency cycle: ${cycle.join(' -> ')}`));"

### EXTRA-K1-0041
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: Every ENF artifact declares 'Conforms:' (owners or —) on the line after its header; targets exist, have valid headers and are STD/DEC; capability facets conform only to neutral owners, their own module or the bound frame; every policy owner cited in the file must be declared.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: Project-owned files only warn.
- Why EXTRA: ENF-conformance invariant.
- Evidence K1-S000457: `output/template/.claude/scripts/check-instructions.cjs:398-433` — "function checkEnforcement(root, artifacts, graph, out) { ⏎   for (const a of artifacts.values()) { ⏎     if (!validHeader(a) || a.header.kind !== 'ENF') continue; ⏎     const severity = PROJECT_OWNED.includes(a.rel) ? WARN : ERR; ⏎     const declared = parseConforms(a.body); ⏎     if (declared === null) { ⏎       out.push(lib.finding(severity, a.rel, 'ENF artifact lacks its conformance declaration …"

### EXTRA-K1-0042
- Closest oracle policies: ARC-020
- Modality: ENFORCED_ADVISORY
- Normative action: The decision register carries slot-selection block markers with exactly one selection row per slot.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: none
- Why EXTRA: Capability-selection format invariant.
- Evidence K1-S000460: `output/template/.claude/scripts/check-instructions.cjs:465-488` — "function registerSelection(artifacts, out) { ⏎   const reg = artifacts.get(REGISTER); ⏎   if (!reg) { ⏎     out.push(lib.finding(ERR, REGISTER, 'decision register is missing')); ⏎     return { selection: {}, knowledge: {}, block: '' }; ⏎   } ⏎   const m = /<!-- slot-selection:begin -->([\s\S]*?)<!-- slot-selection:end -->/.exec(reg.body); ⏎   if (!m) { ⏎     out.push(lib.finding(ERR, REGISTER, 'ca …"

### EXTRA-K1-0043
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: Slot contracts and module manifests declare '- Binds:'; only leaves bind and only to the architecture frame; required leaf → frame bindings must be present with a stated role or reason; a slot cannot bind itself.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: none
- Why EXTRA: Capability-binding invariant.
- Evidence K1-S000462: `output/template/.claude/scripts/check-instructions.cjs:503-520` — "/** Binding obligations: the slot identity (SLOTS) first, then contract and manifest agreement. */ ⏎ function checkBinds(slot, file, binds, out) { ⏎   const model = SLOTS[slot]; ⏎   if (binds === null) { ⏎     out.push(lib.finding(ERR, file, `binding: "- Binds:" is missing (${model.binds.length ? `${slot} must bind ${model.binds.join(', ')}` : 'declare "—" when independent'})`)); ⏎     return; ⏎   …"

### EXTRA-K1-0044
- Closest oracle policies: ARC-020
- Modality: ENFORCED_ADVISORY
- Normative action: Only the agreed slots exist; each has a contract with the right slot type and facet roles; a selection is recorded per slot; required slots cannot be none; at most one implementation is present and it must be the selected one with a module directory; a none selection has no implementation, knowledge facet or facet-role files; module binds match the contract; artifacts declaring a capability are listed facets of a selected module.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: none
- Why EXTRA: Capability-composition invariant.
- Evidence K1-S000463: `output/template/.claude/scripts/check-instructions.cjs:522-569` — "function checkCapabilities(root, artifacts, sel, out) { ⏎   const { selection, knowledge, block } = sel; ⏎   const slotDirs = new Set(lib.walk(root, '.claude/capabilities').map(r => r.split('/')[2])); ⏎   const modules = []; ⏎   for (const dir of slotDirs) if (!(dir in SLOTS)) out.push(lib.finding(ERR, `.claude/capabilities/${dir}`, 'only the agreed capability slots may exist')); ⏎   for (const [s …"

### EXTRA-K1-0045
- Closest oracle policies: ARC-020
- Modality: ENFORCED_ADVISORY
- Normative action: Module manifests exist with matching Capability, Slot, Implementation and Names; facet files exist with headers matching the manifest; the DEC facet is the register; non-knowledge facet file names are role-based; the module provides exactly the contract's facet roles (KNW = the register's knowledge facet); every contract item has a provider, and a 'missing' item requires a Decision Request before selection.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: none
- Why EXTRA: Module-conformance invariant.
- Evidence K1-S000464: `output/template/.claude/scripts/check-instructions.cjs:571-643` — "function checkModule(root, artifacts, slot, impl, contract, knowledgeFacet, out) { ⏎   const id = `${slot}/${impl}`; ⏎   const manifest = `.claude/capabilities/${id}/MODULE.md`; ⏎   const m = artifacts.get(manifest); ⏎   if (!m) { ⏎     out.push(lib.finding(ERR, manifest, 'module manifest is missing')); ⏎     return null; ⏎   } ⏎   if (m.header && m.header.capability !== id) out.push(lib.finding(E …"

### EXTRA-K1-0046
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: No artifact outside the module's facets and manifest, the map, the register's selection block and decision log and project-owned files names the selected implementation (its Names tokens); refer to the slot or facet role instead.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: none
- Why EXTRA: Implementation-neutrality invariant.
- Evidence K1-S000466: `output/template/.claude/scripts/check-instructions.cjs:649-663` — "function checkLeaks(artifacts, modules, registerBlock, out) { ⏎   // Allowed: module facets and manifest, the maintainer map, the register's selection block and its accepted-decision log, ⏎   // and project-owned product/build files (product inputs and package manifests legitimately name technologies). ⏎   const reg = artifacts.get(REGISTER); ⏎   const decisionLog = reg ? reg.text.slice(Math.max(0 …"

### EXTRA-K1-0047
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: .claude/MAP.md exists, lists every artifact, lists no missing artifact and has a capability view per slot.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: none
- Why EXTRA: Map-maintenance invariant.
- Evidence K1-S000468: `output/template/.claude/scripts/check-instructions.cjs:667-681` — "function checkMap(root, files, out) { ⏎   if (!lib.exists(root, MAP)) { ⏎     out.push(lib.finding(ERR, MAP, 'maintainer map is missing')); ⏎     return; ⏎   } ⏎   const map = lib.readText(root, MAP); ⏎   for (const rel of files) { ⏎     if (rel === MAP) continue; ⏎     if (!map.includes(`\`${rel}\``)) out.push(lib.finding(ERR, MAP, `artifact not listed: ${rel}`)); ⏎   } ⏎   for (const m of map.ma …"

### EXTRA-K1-0048
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: settings.json registers only PreToolUse, PostToolUse, PostToolUseFailure and Stop, each with matchers covering the required tools and exec-form command hooks (node + [${CLAUDE_PROJECT_DIR}/.claude/hooks/dispatch.cjs, event]) handled by the dispatcher, no variable expansion, a 1-600 s timeout; the PreToolUse policy hook fails closed and advisory hooks must not block on failure.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: none
- Why EXTRA: Hook-configuration invariant.
- Evidence K1-S000469: `output/template/.claude/scripts/check-instructions.cjs:683-740` — "function checkSettings(root, out) { ⏎   const rel = '.claude/settings.json'; ⏎   if (!lib.exists(root, rel)) { ⏎     out.push(lib.finding(ERR, rel, 'missing')); ⏎     return; ⏎   } ⏎   let settings; ⏎   try { ⏎     settings = JSON.parse(lib.readText(root, rel)); ⏎   } catch (err) { ⏎     out.push(lib.finding(ERR, rel, `invalid JSON (${err.message})`)); ⏎     return; ⏎   } ⏎   const hooks = setting …"

### EXTRA-K1-0049
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: 'normally' in OP/DEC/STD normative text produces a warning; use must/default/prefer.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: none
- Why EXTRA: Vocabulary invariant.
- Evidence K1-S000470: `output/template/.claude/scripts/check-instructions.cjs:742-747` — "function checkVocabulary(artifacts, out) { ⏎   for (const a of artifacts.values()) { ⏎     if (!a.header || !['OP', 'DEC', 'STD'].includes(a.header.kind)) continue; ⏎     if (/\bnormally\b/i.test(a.body)) out.push(lib.finding(WARN, a.rel, 'ambiguous "normally" in normative text; use must/default/prefer')); ⏎   } ⏎ }"

### EXTRA-K1-0050
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: An always-loaded surface above about 6000 tokens (CLAUDE.md, imports, model-invocable skill and agent descriptions) produces a warning; target about 5k.
- Trigger/scope: repo/meta: check-instructions.cjs (instruction-change hooks, verify, template-maintenance)
- Exceptions: none
- Why EXTRA: Context-budget invariant.
- Evidence K1-S000474: `output/template/.claude/scripts/check-instructions.cjs:794-794` — "if (tokens > BUDGET_WARN_TOKENS) out.push(lib.finding(WARN, 'CLAUDE.md', `always-loaded surface is about ${tokens} tokens (target about 5k)`));"

### EXTRA-K1-0051
- Closest oracle policies: none
- Modality: MUST
- Normative action: Classify every instruction artifact by Capability (owned by the selected module of a replaceable slot, header 'Capability: <slot>/<implementation>', otherwise —), then Kind (OP, DEC, STD, KNW, WF, ENF, IN; decides mechanism and location), then Scope (decides rule directory and paths).
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Instruction-system classification rule.
- Evidence K1-S000108: `output/template/.claude/MAP.md:7-9` — "1. **Capability** — does it belong to a replaceable capability slot (architecture, persistence, backend-testing, frontend)? Then the selected module owns it and its header says `Capability: <slot>/<implementation>`; otherwise `Capability: —`. ⏎ 2. **Kind** — OP operating policy · DEC decisions · STD path-scoped standards · KNW knowledge · WF procedures · ENF enforcement · IN product inputs. Kind d …"
- Evidence K1-S001748: `output/template/.claude/skills/template-maintenance/SKILL.md:19-19` — "2. **Kind** — determines mechanism and location:"
- Evidence K1-S001750: `output/template/.claude/skills/template-maintenance/SKILL.md:23-29` — "| OP | Operating policy, approval and stop boundaries | `CLAUDE.md` (always loaded) | ⏎    | DEC | Project decisions, stack, defaults, capability selection | `docs/architecture/decision-register.md` (imported) | ⏎    | STD | Path-scoped normative standards | `.claude/rules/<scope>/<topic>.md` with `paths:` | ⏎    | KNW | Technique, examples, depth | `.claude/skills/<name>/SKILL.md` (+ private `ref …"

### EXTRA-K1-0052
- Closest oracle policies: none
- Modality: MUST
- Normative action: Dependencies point WF → KNW → STD → DEC → OP and ENF → STD/DEC, declared on each ENF artifact's Conforms line; product inputs never override policy; skill and agent references are routing pointers; changes to the system go through template-maintenance (user-invoked) and capability-selection changes through architecture-decision.
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Instruction-system conformance rule.
- Evidence K1-S000109: `output/template/.claude/MAP.md:11-11` — "Dependency direction: WF → KNW → STD → DEC → OP; ENF → STD/DEC, declared on each ENF artifact's `Conforms:` line (the line after its header); product inputs never override policy. Skill and agent references are routing pointers. Changing this system: `template-maintenance` (user-invoked); capability selection changes: `architecture-decision`."
- Evidence K1-S001756: `output/template/.claude/skills/template-maintenance/SKILL.md:38-38` — "- Dependency direction: WF → KNW → STD → DEC → OP, and ENF → STD/DEC. References to invocable skills are routing pointers and may point anywhere; references to non-invocable files are conformance dependencies, must follow this direction, and a skill-private reference is used only by its owning skill. Product inputs never override policy."

## LINK_UNCERTAIN constraints (2)

### UNCERTAIN-K1-0001
- Closest oracle policies: RUN-021
- Modality: ALLOWED
- Normative action: Invalidate before the mutation succeeds only when the workflow deliberately accepts that behaviour.
- Trigger/scope: on-demand knowledge caching (backend)
- Exceptions: Deliberate acceptance by the workflow.
- Open question: Open question: RUN-021 requires invalidation only consistent with successful underlying mutations; whether a deliberately accepted pre-mutation invalidation is a permitted exception or a relaxation that contradicts RUN-021 cannot be decided from the text.
- Evidence K1-S000928: `output/template/.claude/skills/caching/SKILL.md:56-56` — "Remove the affected key after a successful mutation; short TTL with tolerated staleness; tag/group invalidation; versioned keys. Invalidate before the mutation succeeds only when the workflow deliberately accepts that behavior."

### UNCERTAIN-K1-0002
- Closest oracle policies: GOV-015
- Modality: ALLOWED
- Normative action: reset --hard, clean, push --force, push --force-with-lease, branch deletion and rebasing shared history are performed only when explicitly requested or clearly required by an approved workflow.
- Trigger/scope: workflow git-workflow (requested Git operations)
- Exceptions: Explicit request or approved workflow.
- Open question: Open question: GOV-015 permits repository-changing Git operations only when explicitly requested; whether 'clearly required by an approved workflow' widens that condition or only describes an explicitly requested workflow cannot be decided from the text.
- Evidence K1-S001248: `output/template/.claude/skills/git-workflow/SKILL.md:19-19` — "- Treat `git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion, and rebasing shared history as high-risk: perform them only when explicitly requested or clearly required by an approved workflow, after inspecting what will be lost or rewritten."

