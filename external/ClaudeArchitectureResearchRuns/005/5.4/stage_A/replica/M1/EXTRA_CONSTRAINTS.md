# M1 — EXTRA and LINK_UNCERTAIN constraints (Claude Run 2, blind replica)

Every constraint below is an effective candidate behavior judged not entailed by the 196 oracle policies (EXTRA) or whose relation could not be decided (LINK_UNCERTAIN). Citations are template-relative paths under `inputs/M1/output/template/` with exact source quotes (newlines shown as ⏎).

## EXTRA (34)

### EXTRA-M1-0001
- Closest oracle policies: ARC-020, DEP-009
- Modality: MUST
- Normative action: Static capability composition: exactly the four slots architecture (required frame), persistence and backend-testing (required leaves) and frontend (optional leaf); each required slot has exactly one selected implementation and the optional slot zero or one; only selected implementations have runtime facets; contracts and manifests are maintainer metadata, not auto-loaded.
- Trigger/scope: template capability structure and selection record
- Exceptions: none stated
- Why EXTRA: No oracle policy defines capability slots, their cardinality or a selection record; ARC-020/DEP-009 only fix the approved stack and require approval to change it.
- Evidence:
  - `.claude/capabilities/architecture/CONTRACT.md:46-60` (EXTRA, M1-S000034): ""requiredProperties": ["adoptedStyle", "roleMap", "patternsNotAdopted", "repositoryLayout"],"
  - `.claude/capabilities/backend-testing/CONTRACT.md:36-50` (EXTRA, M1-S000045): ""requiredEnforcement": ["testFrameworkPackages", "competingFrameworkPackages"],"
  - `.claude/capabilities/frontend/CONTRACT.md:39-53` (EXTRA, M1-S000073): ""requiredEnforcement": ["notByDefaultPackages", "devOnlyPackages"],"
  - `.claude/capabilities/persistence/CONTRACT.md:42-57` (EXTRA, M1-S000085): ""requiredEnforcement": ["technologyNamespaces", "coChange"],"
  - `.claude/MAP.md:139-144` (EXTRA, M1-S000154): "never to the selected implementation's name"
  - `.claude/scripts/check-architecture.js:22-22` (EXTRA, M1-S000455): "no architecture frame is selected"
  - `.claude/scripts/check-instructions.js:263-263` (EXTRA, M1-S000508): "cannot read the capability selection record"
  - `.claude/scripts/check-instructions.js:267-269` (EXTRA, M1-S000510): "only the four agreed capability slots are allowed."
  - `.claude/scripts/check-instructions.js:275-275` (EXTRA, M1-S000512): "must appear exactly once"
  - `.claude/scripts/check-instructions.js:280-282` (EXTRA, M1-S000514): "lists more than one implementation."
  - `.claude/scripts/check-instructions.js:334-334` (EXTRA, M1-S000526): "unselected implementations must not enter runtime"
  - `.claude/scripts/check-instructions.js:348-350` (EXTRA, M1-S000530): "planning facet of unselected slot"
  - `docs/capability-selection.md:5-7` (EXTRA, M1-S002015): "Static composition: each required slot has exactly one selected implementation;"
  - `docs/capability-selection.md:9-14` (EXTRA, M1-S002016): "| persistence | leaf, required | selected | ef-core | provider: sqlserver |"

### EXTRA-M1-0002
- Closest oracle policies: none
- Modality: MUST (checker-enforced)
- Normative action: Slot contract completeness: a slot implementation supplies every required facet (planning, rules, workflow/placement, knowledge), required property, required enforcement data and role mapping listed in its slot contract; a missing required facet or property is a conformance failure that requires a Decision Request.
- Trigger/scope: creating or replacing a slot implementation
- Exceptions: none stated
- Why EXTRA: Template capability-contract structure; no oracle policy requires implementations to ship particular facets, properties or enforcement data.
- Evidence:
  - `.claude/capabilities/architecture/CONTRACT.md:32-37` (EXTRA, M1-S000031): "layer and boundary rules"
  - `.claude/capabilities/architecture/CONTRACT.md:41-44` (EXTRA, M1-S000033): "A replacement frame must supply every role mapping and facet above."
  - `.claude/capabilities/architecture/CONTRACT.md:46-60` (EXTRA, M1-S000034): ""requiredProperties": ["adoptedStyle", "roleMap", "patternsNotAdopted", "repositoryLayout"],"
  - `.claude/capabilities/backend-testing/CONTRACT.md:25-29` (EXTRA, M1-S000042): "a knowledge skill of the implementation, including § Test Project Setup"
  - `.claude/capabilities/backend-testing/CONTRACT.md:33-34` (EXTRA, M1-S000044): "Framework name, framework/adapter packages"
  - `.claude/capabilities/backend-testing/CONTRACT.md:36-50` (EXTRA, M1-S000045): ""requiredEnforcement": ["testFrameworkPackages", "competingFrameworkPackages"],"
  - `.claude/capabilities/frontend/CONTRACT.md:28-32` (EXTRA, M1-S000070): "including the bindings table"
  - `.claude/capabilities/frontend/CONTRACT.md:36-37` (EXTRA, M1-S000072): "Test runner, E2E tool, scaffold command"
  - `.claude/capabilities/frontend/CONTRACT.md:39-53` (EXTRA, M1-S000073): ""requiredEnforcement": ["notByDefaultPackages", "devOnlyPackages"],"
  - `.claude/capabilities/persistence/CONTRACT.md:11-15` (EXTRA, M1-S000078): "must not silently lose the migration or seeding semantics"
  - `.claude/capabilities/persistence/CONTRACT.md:28-33` (EXTRA, M1-S000082): "workflow (routed from `CLAUDE.md`)"
  - `.claude/capabilities/persistence/CONTRACT.md:42-57` (EXTRA, M1-S000085): ""requiredEnforcement": ["technologyNamespaces", "coChange"],"
  - `.claude/scripts/check-instructions.js:107-107` (EXTRA, M1-S000486): "facet skill missing"
  - `.claude/scripts/check-instructions.js:287-287` (EXTRA, M1-S000516): "manifest of the selected implementation is missing."
  - `.claude/scripts/check-instructions.js:303-303` (EXTRA, M1-S000518): "manifest slot/implementation does not match its location."
  - `.claude/scripts/check-instructions.js:309-310` (EXTRA, M1-S000520): "required facet missing"
  - `.claude/scripts/check-instructions.js:319-319` (EXTRA, M1-S000522): "facet header must declare Capability"
  - `.claude/scripts/check-instructions.js:322-323` (EXTRA, M1-S000524): "required property missing"
  - `.claude/scripts/check-instructions.js:339-339` (EXTRA, M1-S000528): "capability-owned file is not listed in"
  - `.claude/skills/template-maintenance/SKILL.md:53-67` (EXTRA, M1-S001884): "Create `.claude/capabilities/<slot>/<new-implementation>/MODULE.md` with a"

### EXTRA-M1-0003
- Closest oracle policies: none
- Modality: MUST (checker-enforced)
- Normative action: Role vocabulary and leak rule: other instructions use the slot contracts' stable role vocabulary (core model, use-case layer, use-case unit, persistence-access contract, commit boundary, adapter layer, entry point, composition root, test projects, persistence session, test framework, feature data-access service, ...) instead of implementation names; implementation leak tokens appear only in the module's facets, manifest and the selection metadata; a leaf that must name frame-specific projects or directories declares a binds entry.
- Trigger/scope: authoring or changing instruction artifacts
- Exceptions: Module-owned facets, manifests, the selection record and declared properties.
- Why EXTRA: Instruction-authoring vocabulary rule of the M1 capability design; no oracle policy restricts which technology names may appear in which instruction files.
- Evidence:
  - `.claude/capabilities/architecture/CONTRACT.md:7-11` (EXTRA, M1-S000026): "placement belongs to the frame; technique belongs"
  - `.claude/capabilities/architecture/CONTRACT.md:27-28` (EXTRA, M1-S000029): "declares a `binds` entry in its manifest"
  - `.claude/capabilities/backend-testing/CONTRACT.md:17-21` (EXTRA, M1-S000040): "the selected framework and its conventions"
  - `.claude/capabilities/backend-testing/nunit/MODULE.md:10-11` (EXTRA, M1-S000049): "test-project placement is taken from the frame's placement"
  - `.claude/capabilities/frontend/CONTRACT.md:19-24` (EXTRA, M1-S000068): "the framework's explicit HTTP boundary for a feature"
  - `.claude/capabilities/persistence/CONTRACT.md:19-24` (EXTRA, M1-S000080): "the scoped unit shared by the repositories and the commit boundary of one use case"
  - `.claude/capabilities/persistence/ef-core/MODULE.md:16-19` (EXTRA, M1-S000090): "only executable guidance names"
  - `.claude/MAP.md:139-144` (EXTRA, M1-S000154): "never to the selected implementation's name"
  - `.claude/scripts/check-instructions.js:319-319` (EXTRA, M1-S000522): "facet header must declare Capability"
  - `.claude/scripts/check-instructions.js:368-368` (EXTRA, M1-S000532): "without a declared binds entry."
  - `.claude/scripts/check-instructions.js:371-371` (EXTRA, M1-S000534): "refer to the slot or facet role instead."
  - `.claude/scripts/check-instructions.js:380-380` (EXTRA, M1-S000536): "without declaring binds to the architecture frame."
  - `.claude/scripts/check-instructions.js:386-388` (EXTRA, M1-S000538): "binds entry needs a reason"
  - `.claude/skills/template-maintenance/SKILL.md:39-40` (EXTRA, M1-S001879): "not to the selected implementation's name."
  - `docs/capabilities/architecture.md:11-11` (EXTRA, M1-S001989): "Other instructions use these stable roles; this frame maps them to layers."
  - `docs/capabilities/architecture.md:13-23` (MIXED, M1-S001990): "| use-case unit | Application Service |"

### EXTRA-M1-0004
- Closest oracle policies: none
- Modality: MUST
- Normative action: Content ownership in the capability model: placement belongs to the architecture frame and technique to the leaf; implementation-independent policy (framework-independent testing rules, framework-independent frontend rules) stays outside the modules; test-project placement and the frontend workspace location belong to the frame; the persistence leaf binds to frame roles and does not decide placement.
- Trigger/scope: template content placement
- Exceptions: none stated
- Why EXTRA: Template-structure ownership rule; the oracle prescribes no ownership location for instruction content.
- Evidence:
  - `.claude/capabilities/architecture/CONTRACT.md:7-11` (EXTRA, M1-S000026): "placement belongs to the frame; technique belongs"
  - `.claude/capabilities/backend-testing/CONTRACT.md:7-13` (EXTRA, M1-S000038): "Framework-independent test policy"
  - `.claude/capabilities/frontend/CONTRACT.md:7-12` (EXTRA, M1-S000065): "Framework-independent frontend"
  - `.claude/capabilities/persistence/CONTRACT.md:7-9` (EXTRA, M1-S000077): "does not decide placement"
  - `docs/capabilities/backend-testing.md:9-10` (EXTRA, M1-S002000): "Backend test projects are placed by the architecture frame"
  - `docs/capability-selection.md:26-30` (EXTRA, M1-S002020): "Slot contracts and implementation manifests (maintainer metadata, read only"

### EXTRA-M1-0005
- Closest oracle policies: none
- Modality: MUST
- Normative action: Replacement and removal procedure: replacing a leaf replaces its facets (planning, rule facet, knowledge content, adapter data) without touching the framework-independent rules; clearing the optional frontend removes its facets and planning import with nothing else to change; a persistence provider change edits only the declared provider-variant sections, the provider property and the declared string-comparison property; a frame replacement supplies every role mapping and facet and reviews embedded rules that use the frame's layer names.
- Trigger/scope: capability replacement and removal
- Exceptions: none stated
- Why EXTRA: Template maintenance procedure; no oracle policy governs how instruction files change when a technology is replaced.
- Evidence:
  - `.claude/capabilities/architecture/CONTRACT.md:41-44` (EXTRA, M1-S000033): "A replacement frame must supply every role mapping and facet above."
  - `.claude/capabilities/backend-testing/nunit/MODULE.md:5-8` (EXTRA, M1-S000048): "without touching the framework-independent testing rule"
  - `.claude/capabilities/frontend/CONTRACT.md:14-15` (EXTRA, M1-S000066): "Clearing the selection removes the module's facets and its planning import"
  - `.claude/capabilities/persistence/ef-core/MODULE.md:11-14` (EXTRA, M1-S000089): "a provider change edits only those sections"
  - `.claude/scripts/check-instructions.js:348-350` (EXTRA, M1-S000530): "planning facet of unselected slot"
  - `.claude/skills/architecture-decision/SKILL.md:71-73` (EXTRA, M1-S000736): "ask the user to run"
  - `.claude/skills/template-maintenance/SKILL.md:53-67` (EXTRA, M1-S001884): "Create `.claude/capabilities/<slot>/<new-implementation>/MODULE.md` with a"
  - `.claude/skills/template-maintenance/SKILL.md:71-73` (EXTRA, M1-S001886): "declared string-comparison property; record the ADR."
  - `.claude/skills/template-maintenance/SKILL.md:77-84` (EXTRA, M1-S001888): "Set the frontend row to status `disabled` with implementation `—`; delete the"

### EXTRA-M1-0006
- Closest oracle policies: DEP-009, ARC-020, GOV-006
- Modality: MUST
- Normative action: Persistence semantics on change: the persistence implementation declares commit binding, migration mechanism, seeding mechanism, provider variant, observable string-comparison semantics and relational-testing expectations; replacing the technology (e.g. with a micro-ORM) must not silently lose migration or seeding semantics; a provider change is a provider-variant change inside the slot, not a new slot.
- Trigger/scope: persistence implementation or provider changes
- Exceptions: none stated
- Why EXTRA: ARC-020 requires approval for new persistence technology and GOV-006 for observable string semantics, but no oracle policy requires declared persistence properties or preservation of migration/seeding mechanisms on replacement.
- Evidence:
  - `.claude/capabilities/persistence/CONTRACT.md:11-15` (EXTRA, M1-S000078): "must not silently lose the migration or seeding semantics"
  - `.claude/capabilities/persistence/CONTRACT.md:37-40` (EXTRA, M1-S000084): "observable string-comparison semantics (also"

### EXTRA-M1-0008
- Closest oracle policies: ARC-020, ARC-001, GOV-017
- Modality: REQUIRES_APPROVAL (Reserved; PreToolUse deny until the project-reference marker; PostToolUse routing of changed project files)
- Normative action: Changing the project reference graph is Reserved; project-reference commands are denied until the project-structure workflow was applied (re-run with '# project-reference: checked'), which routes Reserved reference-graph changes to architecture-decision; project files or references changed, removed or moved without a recognized command are reported for confirmation of the owning workflow.
- Trigger/scope: .NET project references and project files
- Exceptions: The marker is self-certified; references inside the frame's layout follow project-structure without a Decision Request.
- Why EXTRA: ARC-020 requires approval for new layers/projects and ARC-001 constrains direction; no oracle policy makes individual reference edges between existing projects Reserved or gates every reference command.
- Evidence:
  - `.claude/hooks/post-tool-use.js:165-165` (MIXED, M1-S000107): "projects and project references, project-structure"
  - `.claude/MAP.md:124-124` (DUPLICATE, M1-S000149): "| `hooks/pre-tool-use.js` | denies dependency commands until `add-dependency` was applied and project-reference commands until `project-structure` was applied; stops peer-dependency override flags; fails closed | common | hook | pre-command routing |"
  - `.claude/MAP.md:125-125` (DUPLICATE, M1-S000150): "| `hooks/post-tool-use.js` | after edits and successful or failed commands: manifest and architecture checks, layer-namespace check, product-source reminders, instruction check; a shell command is judged by its effect on manifests and project files (content state per worktree in its Git directory), so unrecognized commands, branch switches, removals, and moves are checked | common | hook | post-ch"
  - `.claude/scripts/lib/dependency-commands.js:396-406` (EXTRA, M1-S000599): "routes Reserved reference-graph changes to the architecture-decision workflow"
  - `.claude/skills/development-workflow/SKILL.md:48-55` (MIXED, M1-S001072): "dependency additions, updates, or removals → `add-dependency`;"
  - `.claude/skills/project-structure/SKILL.md:106-111` (MIXED, M1-S001684): "a changed reference graph is Reserved"
  - `.claude/skills/project-structure/SKILL.md:118-119` (EXTRA, M1-S001687): "The pre-tool hook stops"
  - `.claude/skills/project-structure/SKILL.md:124-127` (MIXED, M1-S001689): "any other change to the"
  - `.claude/skills/project-structure/SKILL.md:128-129` (EXTRA, M1-S001690): "`# project-reference: checked`."
  - `CLAUDE.md:78-79` (MIXED, M1-S001958): "reference graph;"

### EXTRA-M1-0009
- Closest oracle policies: none
- Modality: MUST (PostToolUse feedback after instruction edits)
- Normative action: After an edit to an instruction file the instruction-structure check runs and its reported errors must be fixed (template-maintenance).
- Trigger/scope: edits of instruction files
- Exceptions: none stated
- Why EXTRA: Instruction-system maintenance rule; no oracle policy regulates instruction-file structure.
- Evidence:
  - `.claude/hooks/post-tool-use.js:78-81` (EXTRA, M1-S000105): "Instruction-structure check (template-maintenance workflow)"
  - `.claude/MAP.md:125-125` (DUPLICATE, M1-S000150): "| `hooks/post-tool-use.js` | after edits and successful or failed commands: manifest and architecture checks, layer-namespace check, product-source reminders, instruction check; a shell command is judged by its effect on manifests and project files (content state per worktree in its Git directory), so unrecognized commands, branch switches, removals, and moves are checked | common | hook | post-ch"
  - `.claude/skills/template-maintenance/SKILL.md:44-46` (EXTRA, M1-S001881): "(from any directory of the repository or worktree being changed) and fix"
  - `.claude/skills/verify/SKILL.md:140-141` (EXTRA, M1-S001918): "When instruction files changed, run"

### EXTRA-M1-0010
- Closest oracle policies: PST-009, PST-010
- Modality: SHOULD (Stop reminder once per change state)
- Normative action: When persistence model files change without migration changes, confirm the persistence-change workflow (schema changes paired with migrations) was applied, or state why it does not apply.
- Trigger/scope: Stop in a Git work tree
- Exceptions: Same repetition limits as RULE-M1-0015.
- Why EXTRA: The oracle requires migrations only for schema-affecting CUSTOM_SETTINGS changes (PST-009) and review of generated migrations (PST-010); it has no general duty to pair model changes with migrations or to confirm schema impact at stop time.
- Evidence:
  - `.claude/hooks/stop.js:50-51` (MIXED, M1-S000118): "confirm the persistence-change workflow was applied"
  - `.claude/MAP.md:126-126` (DUPLICATE, M1-S000151): "| `hooks/stop.js` | co-change reminders (persistence model vs. seed/migrations, code vs. tests, product sources, manifests); loop-safe; re-arms when the content of the involved files changes; state per worktree | common | hook | co-change reminders |"

### EXTRA-M1-0007
- Closest oracle policies: DEP-001, DEP-003
- Modality: MUST (PreToolUse deny until the add-dependency marker)
- Normative action: Dependency removals follow the add-dependency workflow: removal commands (npm/pnpm uninstall/remove, yarn remove, dotnet remove package, dotnet package remove, nuget delete, Uninstall-Package) are denied until re-run with '# add-dependency: checked'.
- Trigger/scope: Bash and PowerShell package-manager commands
- Exceptions: The marker is self-certified.
- Why EXTRA: DEP-001..DEP-005 govern additions and updates; no oracle policy routes removals through a workflow gate.
- Evidence:
  - `.claude/MAP.md:124-124` (DUPLICATE, M1-S000149): "| `hooks/pre-tool-use.js` | denies dependency commands until `add-dependency` was applied and project-reference commands until `project-structure` was applied; stops peer-dependency override flags; fails closed | common | hook | pre-command routing |"
  - `.claude/rules/dependencies.md:14-17` (MIXED, M1-S000273): "Adding, updating, or removing a NuGet or npm dependency follows the"
  - `.claude/scripts/lib/dependency-commands.js:407-419` (MIXED, M1-S000600): "Run the add-dependency workflow first"
  - `.claude/skills/development-workflow/SKILL.md:48-55` (MIXED, M1-S001072): "dependency additions, updates, or removals → `add-dependency`;"
  - `CLAUDE.md:116-128` (MIXED, M1-S001968): "adding, updating, or removing a NuGet or npm dependency"

### EXTRA-M1-0011
- Closest oracle policies: none
- Modality: MUST
- Normative action: Ownership of instruction content: every rule has exactly one owner and other files point to it; knowledge skills are technique only and never sole policy owners; implementation-specific content goes only into the module facets.
- Trigger/scope: template maintenance
- Exceptions: none stated
- Why EXTRA: Instruction-system ownership rule; the oracle does not regulate instruction ownership.
- Evidence:
  - `.claude/MAP.md:5-8` (EXTRA, M1-S000126): "every rule has exactly one owner and other files point"
  - `.claude/skills/template-maintenance/SKILL.md:32-33` (EXTRA, M1-S001877): "never restate a rule in a second place."

### EXTRA-M1-0012
- Closest oracle policies: none
- Modality: MUST (checker-enforced)
- Normative action: Hook registration form: hooks are wired in exec form (command node plus script path through ${CLAUDE_PROJECT_DIR}, no shell); the critical PreToolUse hook fails closed (onFailure block); failed shell commands are post-checked (PostToolUseFailure); post and Stop hooks report failures visibly without blocking.
- Trigger/scope: .claude/settings.json (template maintenance)
- Exceptions: none stated
- Why EXTRA: Hook-configuration design of the template; no oracle policy regulates hook registration.
- Evidence:
  - `.claude/MAP.md:123-123` (EXTRA, M1-S000148): "the critical pre-tool hook fails closed (`onFailure: "block"`)"
  - `.claude/scripts/check-instructions.js:424-437` (EXTRA, M1-S000540): "critical pre-tool enforcement must fail closed"
  - `.claude/scripts/check-instructions.js:454-454` (EXTRA, M1-S000542): "unexpected hook event"
  - `.claude/scripts/check-instructions.js:461-461` (EXTRA, M1-S000544): "does not run"
  - `.claude/scripts/check-instructions.js:465-465` (EXTRA, M1-S000546): "matcher does not cover the"
  - `.claude/settings.json:11-11` (EXTRA, M1-S000605): ""onFailure": "block""

### EXTRA-M1-0013
- Closest oracle policies: API-013, ARC-020
- Modality: REQUIRES_APPROVAL (Reserved)
- Normative action: Adopting API versioning is Reserved and needs explicit approval, even when a concrete compatibility need exists.
- Trigger/scope: HTTP API versioning
- Exceptions: none stated
- Why EXTRA: API-013 allows introducing versioning when a real compatibility need exists without requiring approval; the oracle's consequential-change list does not name versioning adoption.
- Evidence:
  - `.claude/rules/api.md:33-35` (MIXED, M1-S000178): "Adopting versioning is Reserved."
  - `CLAUDE.md:89-89` (MIXED, M1-S001960): "making a breaking public API change or adopting API versioning;"

### EXTRA-M1-0014
- Closest oracle policies: none
- Modality: MUST (checker-enforced)
- Normative action: Instruction-system structure: every instruction artifact starts with a one-line ownership header and uses no Level:/Kind: classification; rules stay flat in .claude/rules/ with non-empty paths; required workflow and embedded knowledge skills exist with frontmatter name equal to the directory and a concrete description, skill-private files only under references/; template-maintenance is user-only; only CLAUDE.md imports always-loaded files (no nested imports) and imports resolve; file, workflow, skill and section references resolve; CLAUDE.md keeps a Workflow Routing section whose targets exist; the map lists every instruction, enforcement and root configuration file; the always-loaded surface stays within its token target.
- Trigger/scope: template maintenance
- Exceptions: Facet locations of a disabled optional slot are treated as inactive rather than broken.
- Why EXTRA: Instruction-system organization rules of the M1 template; no oracle policy regulates instruction artifacts.
- Evidence:
  - `.claude/scripts/check-instructions.js:65-65` (EXTRA, M1-S000473): "missing one-line classification/ownership header"
  - `.claude/scripts/check-instructions.js:66-68` (EXTRA, M1-S000474): "which this instruction system does not use"
  - `.claude/scripts/check-instructions.js:75-75` (EXTRA, M1-S000476): "rules must stay flat in .claude/rules/"
  - `.claude/scripts/check-instructions.js:79-79` (EXTRA, M1-S000478): "rule file must declare a non-empty paths: list."
  - `.claude/scripts/check-instructions.js:93-97` (EXTRA, M1-S000480): "user-only workflow must set disable-model-invocation: true."
  - `.claude/scripts/check-instructions.js:101-101` (EXTRA, M1-S000482): "skill-private files belong in the skill"
  - `.claude/scripts/check-instructions.js:103-104` (EXTRA, M1-S000484): "required workflow skill missing"
  - `.claude/scripts/check-instructions.js:129-129` (EXTRA, M1-S000492): "import does not resolve"
  - `.claude/scripts/check-instructions.js:135-135` (EXTRA, M1-S000494): "nested import"
  - `.claude/scripts/check-instructions.js:204-204` (EXTRA, M1-S000496): "reference does not resolve"
  - `.claude/scripts/check-instructions.js:207-207` (EXTRA, M1-S000498): "reference does not resolve"
  - `.claude/scripts/check-instructions.js:212-212` (EXTRA, M1-S000500): "section reference target does not resolve"
  - `.claude/scripts/check-instructions.js:218-218` (EXTRA, M1-S000502): "section reference does not resolve"
  - `.claude/scripts/check-instructions.js:223-223` (EXTRA, M1-S000504): "missing the Workflow Routing section."
  - `.claude/scripts/check-instructions.js:226-226` (EXTRA, M1-S000506): "routing target does not exist"
  - `.claude/scripts/check-instructions.js:481-481` (EXTRA, M1-S000548): "map does not list"
  - `.claude/scripts/check-instructions.js:512-512` (EXTRA, M1-S000550): "always-loaded surface is about"
  - `.claude/skills/template-maintenance/SKILL.md:7-7` (EXTRA, M1-S001869): "disable-model-invocation: true"
  - `CLAUDE.md:129-129` (EXTRA, M1-S001969): "ask the user to run `/template-maintenance`"

### EXTRA-M1-0015
- Closest oracle policies: DEP-004, DEP-020, DEP-010
- Modality: MUST NOT (manifest check error; no approval path)
- Normative action: Microsoft.Extensions.Http.Polly and Polly.Extensions.Http (deprecated resilience integrations), Serilog.Sinks.Elasticsearch (deprecated sink) and FluentValidation.AspNetCore (legacy automatic-validation integration) are reported as errors whenever they appear in a manifest.
- Trigger/scope: NuGet manifests
- Exceptions: none stated
- Why EXTRA: DEP-004 requires deprecation checks and DEP-020 treats direct Polly integration as an explicit exception; no oracle policy forbids specific packages outright regardless of approval.
- Evidence:
  - `.claude/scripts/check-manifests.js:19-24` (EXTRA, M1-S000555): "deprecated resilience integration; use the approved Microsoft.Extensions resilience packages"
  - `.claude/scripts/check-manifests.js:75-78` (EXTRA, M1-S000560): "DEPRECATED_PACKAGES.has(id)"
  - `.claude/skills/add-dependency/SKILL.md:29-35` (MIXED, M1-S000616): "deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`"
  - `.claude/skills/add-dependency/SKILL.md:36-37` (EXTRA, M1-S000617): "do not add deprecated or legacy ASP.NET automatic-validation"

### EXTRA-M1-0016
- Closest oracle policies: DEP-001, GOV-014
- Modality: MUST
- Normative action: Remove dependencies that are no longer used when that is part of the current change and safe to verify; do not leave dead package references.
- Trigger/scope: dependency changes
- Exceptions: Unrelated cleanup during a narrowly scoped task is excluded.
- Why EXTRA: DEP-001 restricts additions and GOV-014 limits scope; no oracle policy requires removing dependencies made unused by a change.
- Evidence:
  - `.claude/skills/add-dependency/SKILL.md:127-129` (MIXED, M1-S000637): "do not leave dead package references"

### EXTRA-M1-0017
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST
- Normative action: Accepted architecture, stack, convention or public-contract decisions are recorded in the same change as an ADR in docs/decisions/NNNN-short-title.md (Status, Context, Decision, Consequences) and in the affected decision record (technology stack or capability planning facet); a rejected request is recorded only when the rejection itself is a durable decision.
- Trigger/scope: approved decisions
- Exceptions: Product behavior and tunable values go to SPECIFICATION.md / CUSTOM_SETTINGS.md.
- Why EXTRA: GOV-017 requires approval for Reserved decisions but no recording artifact; no oracle policy requires ADRs or decision-record updates.
- Evidence:
  - `.claude/skills/architecture-decision/SKILL.md:50-55` (EXTRA, M1-S000730): "an ADR in"
  - `.claude/skills/architecture-decision/SKILL.md:60-61` (EXTRA, M1-S000733): "A rejected request is recorded only when the rejection itself is a durable"
  - `.claude/skills/template-maintenance/SKILL.md:71-73` (EXTRA, M1-S001886): "declared string-comparison property; record the ADR."
  - `CLAUDE.md:100-105` (MIXED, M1-S001963): "explicit user instruction may count as approval but must be recorded there."

### EXTRA-M1-0018
- Closest oracle policies: ARC-020, GOV-017, DEP-002
- Modality: MUST
- Normative action: Changing a capability selection, enabling or disabling the optional frontend slot, or changing a declared property such as the persistence provider variant is Reserved and requires an ADR; after approval the replacement itself is applied by the user-run template-maintenance workflow (Capability Replacement).
- Trigger/scope: capability selection changes
- Exceptions: none stated
- Why EXTRA: ARC-020/DEP-002 require approval for replacing approved technology, but no oracle policy requires an ADR or routes the change through a user-run maintenance workflow.
- Evidence:
  - `.claude/skills/architecture-decision/SKILL.md:65-69` (MIXED, M1-S000735): "Reserved and requires an ADR."
  - `.claude/skills/architecture-decision/SKILL.md:71-73` (EXTRA, M1-S000736): "ask the user to run"
  - `.claude/skills/template-maintenance/SKILL.md:50-51` (EXTRA, M1-S001883): "Use after an ADR approved the change"
  - `CLAUDE.md:116-128` (MIXED, M1-S001968): "adding, updating, or removing a NuGet or npm dependency"
  - `docs/capability-selection.md:1-1` (EXTRA, M1-S002013): "Changing a selection is Reserved and requires an ADR"

### EXTRA-M1-0019
- Closest oracle policies: DEP-010, API-010
- Modality: MUST
- Normative action: Register FluentValidation validators with FluentValidation.DependencyInjectionExtensions and follow the project's established validation invocation pattern rather than a second competing mechanism.
- Trigger/scope: backend validation setup
- Exceptions: none stated
- Why EXTRA: DEP-010 fixes FluentValidation as the library and API-010 the validation boundaries; no oracle policy prescribes the registration package.
- Evidence:
  - `.claude/skills/aspnet-error-handling/SKILL.md:139-141` (MIXED, M1-S000762): "Register validators with `FluentValidation.DependencyInjectionExtensions` and"
  - `docs/technology-stack.md:29-31` (MIXED, M1-S002031): "`FluentValidation.DependencyInjectionExtensions`) is the standard library for"

### EXTRA-M1-0020
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: The build-fix report states the initial failure, root cause, changes made, backend build / frontend build / tests status (PASS, NOT RUN, NOT APPLICABLE) and remaining issues.
- Trigger/scope: build and test repair
- Exceptions: none stated
- Why EXTRA: WF-009 requires reporting actual verification states only; the failure/root-cause/changes sections are additional reporting duties.
- Evidence:
  - `.claude/skills/build-fix/SKILL.md:238-246` (MIXED, M1-S000874): "Backend build: PASS / NOT RUN / NOT APPLICABLE"

### EXTRA-M1-0021
- Closest oracle policies: RUN-021, ARC-016
- Modality: MUST NOT (review defect)
- Normative action: Tracked persistence entities must not be cached across Unit of Work boundaries.
- Trigger/scope: caching
- Exceptions: none stated
- Why EXTRA: RUN-021 governs invalidation consistency and ARC-016 the commit boundary; no oracle policy forbids caching tracked entities as such.
- Evidence:
  - `.claude/skills/caching/SKILL.md:130-136` (MIXED, M1-S000906): "tracked persistence entities cached across Unit of Work"

### EXTRA-M1-0022
- Closest oracle policies: WF-011, WF-012
- Modality: MUST
- Normative action: Code-review findings are reported ordered by severity, each with severity, file/location, what is wrong, why it matters and the smallest reasonable fix, using the fixed severity scale Critical / High / Medium / Low with defined meanings.
- Trigger/scope: code review output
- Exceptions: none stated
- Why EXTRA: WF-011/WF-012 govern priorities and honesty of findings; the oracle does not prescribe a findings format or severity scale.
- Evidence:
  - `.claude/skills/code-review/SKILL.md:148-157` (EXTRA, M1-S000978): "For each finding give severity,"

### EXTRA-M1-0023
- Closest oracle policies: GOV-015, GOV-020
- Modality: MUST NOT
- Normative action: main, master and other protected or shared branches are treated as non-rewritable; a shared branch is never force-pushed unless the user explicitly requests history rewriting and the consequences are understood.
- Trigger/scope: push and history rewriting
- Exceptions: Explicit user request for history rewriting of a shared branch.
- Why EXTRA: GOV-015 requires an explicit request for force-push; the oracle does not declare named branches categorically non-rewritable.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:75-80` (MIXED, M1-S001256): "treat `main`, `master`, and other protected or shared branches as"

### EXTRA-M1-0024
- Closest oracle policies: WF-009, WF-022
- Modality: MUST
- Normative action: Before preparing a pull request run verify; the PR has a focused purpose and its description explains what changed, why, how it was verified and important compatibility or migration notes.
- Trigger/scope: pull requests
- Exceptions: none stated
- Why EXTRA: WF-009 covers truthful verification reporting and WF-022 focused commits; the oracle does not prescribe PR description contents.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:93-96` (MIXED, M1-S001260): "Do not"

### EXTRA-M1-0025
- Closest oracle policies: RUN-002
- Modality: MUST NOT (review defect)
- Normative action: Fire-and-forget EF Core asynchronous operations are a defect.
- Trigger/scope: EF Core code
- Exceptions: none stated
- Why EXTRA: RUN-002 forbids blocking async I/O; the oracle does not separately forbid unawaited persistence operations.
- Evidence:
  - `.claude/skills/ef-core/SKILL.md:413-420` (MIXED, M1-S001231): "fire-and-forget EF asynchronous operations;"

### EXTRA-M1-0026
- Closest oracle policies: RUN-016
- Modality: MUST NOT
- Normative action: Do not wrap normal persistence operations in a generic application-level retry pipeline; use the persistence provider's execution strategy for transient faults and handle transaction/retry interaction per the provider's guidance.
- Trigger/scope: persistence resilience
- Exceptions: none stated
- Why EXTRA: RUN-016 limits retries to safe repeats; no oracle policy forbids application-level retry of persistence operations or prescribes the provider execution strategy.
- Evidence:
  - `.claude/skills/httpclient-factory/references/resilience.md:86-91` (EXTRA, M1-S001397): "Do not wrap normal persistence operations in a generic application-level retry"
  - `.claude/skills/httpclient-factory/references/resilience.md:121-127` (MIXED, M1-S001407): "generic"
  - `.claude/skills/httpclient-factory/references/resilience.md:131-141` (DUPLICATE, M1-S001409): "| Scenario | Default consideration | ⏎ |---|---| ⏎ | External I/O | Bound execution time | ⏎ | Safe transient HTTP failure | Consider retry | ⏎ | Unsafe write | No retry unless duplicate-safe | ⏎ | `429` from dependency | Respect `Retry-After` where appropriate | ⏎ | Repeated dependency outage | Consider circuit breaker | ⏎ | Optional data unavailable | Consider explicit fallback | ⏎ | Latency-sensitive idempoten"

### EXTRA-M1-0027
- Closest oracle policies: RUN-005
- Modality: MUST NOT
- Normative action: Per-request values such as dynamic access tokens are applied to the specific request or through a handler; shared default headers (DefaultRequestHeaders) are not mutated concurrently.
- Trigger/scope: outbound HTTP
- Exceptions: none stated
- Why EXTRA: RUN-005 governs client lifetime; no oracle policy addresses mutation of shared default headers.
- Evidence:
  - `.claude/skills/httpclient-factory/SKILL.md:153-155` (EXTRA, M1-S001446): "do not mutate shared default headers concurrently."
  - `.claude/skills/httpclient-factory/SKILL.md:181-187` (MIXED, M1-S001454): "tokens in shared `DefaultRequestHeaders`;"

### EXTRA-M1-0028
- Closest oracle policies: RUN-013, RUN-014
- Modality: MUST NOT (review defect)
- Normative action: Logs are not used as an audit database without a dedicated audit design.
- Trigger/scope: logging
- Exceptions: Dedicated audit design.
- Why EXTRA: RUN-013/RUN-014 govern structured and non-sensitive logging; no oracle policy addresses audit trails.
- Evidence:
  - `.claude/skills/logging/SKILL.md:95-99` (MIXED, M1-S001520): "logs used as an audit"

### EXTRA-M1-0029
- Closest oracle policies: DEP-008, DEP-003
- Modality: MUST
- Normative action: global.json pins the intended stable SDK line; when scaffolding select the current stable SDK for the target .NET release (no RC/preview SDK unless explicitly requested) and allow servicing through the chosen rollForward policy.
- Trigger/scope: repository SDK configuration
- Exceptions: Preview SDK explicitly requested.
- Why EXTRA: DEP-008 fixes the .NET platform and DEP-003 package versions; no oracle policy requires an SDK pin file.
- Evidence:
  - `.claude/skills/project-structure/references/solution-layout.md:69-72` (EXTRA, M1-S001644): "pin the intended stable SDK line;"
  - `docs/technology-stack.md:25-25` (EXTRA, M1-S002029): "`global.json` pins the stable SDK line."

### EXTRA-M1-0030
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: Security findings are reported in a fixed shape: severity tag, file:line location and title, OWASP category, Evidence, Impact and Remediation; findings with incomplete evidence use the NEEDS VERIFICATION form stating what effective behavior depends on.
- Trigger/scope: security review output
- Exceptions: none stated
- Why EXTRA: WF-020 requires evidence and contextual severity; the oracle does not prescribe a security report format.
- Evidence:
  - `.claude/skills/security-scan/references/scan-layers.md:312-327` (EXTRA, M1-S001792): "### [HIGH] src/.../File.cs:42 — Resource authorization missing"
  - `.claude/skills/security-scan/references/scan-layers.md:329-335` (EXTRA, M1-S001793): "### [NEEDS VERIFICATION] ..."
  - `.claude/skills/security-scan/SKILL.md:143-146` (MIXED, M1-S001829): "and the OWASP category when applicable. Label uncertain findings"
  - `.claude/skills/security-scan/SKILL.md:148-194` (EXTRA, M1-S001830): "# Security Scan Report"

### EXTRA-M1-0031
- Closest oracle policies: WF-020, WF-009
- Modality: MUST
- Normative action: The security scan report contains Scope, a Limitations statement (static analysis only), a severity Summary table, Findings and Layer Results for the seven layers with PASS / FINDINGS / NOT APPLICABLE / NOT CHECKED, using the fixed severity scale Critical / High / Medium / Low / Info with defined meanings.
- Trigger/scope: security scan output
- Exceptions: none stated
- Why EXTRA: WF-020/WF-009 require contextual severity and truthful status reporting; the oracle does not prescribe report sections, layer tables or a severity scale.
- Evidence:
  - `.claude/skills/security-scan/SKILL.md:15-20` (MIXED, M1-S001799): "State that limitation in the report."
  - `.claude/skills/security-scan/SKILL.md:112-122` (EXTRA, M1-S001823): "use sparingly for immediately exploitable, high-impact"
  - `.claude/skills/security-scan/SKILL.md:148-194` (EXTRA, M1-S001830): "# Security Scan Report"
  - `.claude/skills/security-scan/SKILL.md:196-197` (MIXED, M1-S001831): "never mark an"
  - `.claude/skills/security-scan/SKILL.md:209-211` (DUPLICATE, M1-S001835): "A security scan is complete when all applicable layers were inspected, findings ⏎ have evidence, uncertain findings are labeled, severity reflects actual risk, ⏎ limitations are stated, and no layer is marked PASS without being checked."

### EXTRA-M1-0032
- Closest oracle policies: none
- Modality: MUST
- Normative action: Template maintenance procedure: read .claude/MAP.md first; place new content by kind (planning-time governance in the compact CLAUDE.md, stack in technology-stack, capability decisions in docs/capabilities, path rules in flat .claude/rules with paths, procedures in workflow skills, technique in knowledge skills or references, mechanical checks in hooks/scripts wired in settings.json, slot metadata in CONTRACT.md/MODULE.md); keep each policy's trigger role; never hide a must/must-not rule only inside a knowledge skill or private reference; keep the always-loaded surface compact; update MAP.md.
- Trigger/scope: instruction-system maintenance
- Exceptions: none stated
- Why EXTRA: Instruction-system maintenance rule; the oracle does not regulate where instruction content lives.
- Evidence:
  - `.claude/skills/template-maintenance/SKILL.md:14-15` (EXTRA, M1-S001873): "Read `.claude/MAP.md` first;"
  - `.claude/skills/template-maintenance/SKILL.md:19-28` (EXTRA, M1-S001875): "| governance needed at planning time | `CLAUDE.md` (keep it compact) |"
  - `.claude/skills/template-maintenance/SKILL.md:34-38` (EXTRA, M1-S001878): "Do not hide a must/must-not rule only inside a knowledge skill or a private"
  - `.claude/skills/template-maintenance/SKILL.md:41-43` (EXTRA, M1-S001880): "Update `.claude/MAP.md`."

### EXTRA-M1-0033
- Closest oracle policies: GOV-017, ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: For an unclear decision, any 'yes' to five questions makes it Reserved: does it add, remove or replace a dependency, framework or infrastructure capability; change a project, layer or reference boundary; establish a convention other code must follow; change observable behavior or a public contract; or would it be expensive to reverse once other code depends on it.
- Trigger/scope: decision classification
- Exceptions: none stated
- Why EXTRA: GOV-017 defines Decided/Delegated/Reserved classes; the oracle does not provide a test that turns any of these properties into a Reserved decision.
- Evidence:
  - `CLAUDE.md:93-98` (EXTRA, M1-S001962): "makes it Reserved:"

### EXTRA-M1-0034
- Closest oracle policies: DEP-023, RUN-009
- Modality: MUST
- Normative action: Nullable reference types and implicit usings are enabled repository-wide through Directory.Build.props.
- Trigger/scope: backend build configuration
- Exceptions: none stated
- Why EXTRA: DEP-023 places shared settings in Directory.Build.props but no oracle policy requires nullable reference types or implicit usings to be enabled.
- Evidence:
  - `Directory.Build.props:8-9` (EXTRA, M1-S001979): "<Nullable>enable</Nullable>"

## LINK_UNCERTAIN (2)

### UNCERTAIN-M1-0001
- Closest oracle policies: GOV-015, DEP-007
- Modality: MUST
- Normative action: Maintain and commit package.json and package-lock.json (the manifest check also warns 'maintain and commit the lockfile' when package-lock.json is missing).
- Trigger/scope: frontend workspace manifests
- Exceptions: none stated
- Open question: Read as a version-control content convention the clause is entailed by DEP-007; read as an instruction to perform commits it conflicts with GOV-015, which allows commits only on explicit request. The text does not settle which reading is meant.
- Evidence:
  - `.claude/rules/dependencies.md:49-53` (MIXED, M1-S000281): "Maintain and commit"
  - `.claude/scripts/check-manifests.js:164-166` (MIXED, M1-S000580): "maintain and commit the lockfile"

### UNCERTAIN-M1-0002
- Closest oracle policies: GOV-015, GOV-020
- Modality: MUST NOT (high-risk)
- Normative action: High-risk Git operations (reset --hard, clean, push --force, push --force-with-lease, branch deletion, rebasing shared history) are performed only when explicitly requested or clearly required by an approved workflow, after inspecting what will be lost or rewritten.
- Trigger/scope: Git operations
- Exceptions: Clearly required by an approved workflow.
- Open question: GOV-015 requires an explicit request for repository-changing operations; whether 'clearly required by an approved workflow' is an admissible substitute for that request cannot be decided from the oracle text.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:100-103` (LINK_UNCERTAIN, M1-S001262): "clearly required by an approved"

