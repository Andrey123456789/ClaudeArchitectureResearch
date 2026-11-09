# L1 — EXTRA and LINK_UNCERTAIN constraints (Claude Run 2, blind replica)

Every constraint below is an effective candidate behavior judged not entailed by the 196 oracle policies (EXTRA) or whose relation could not be decided (LINK_UNCERTAIN). Citations are template-relative paths under `inputs/L1/output/template/` with exact source quotes (newlines shown as ⏎).

## EXTRA (35)

### EXTRA-L1-0001
- Closest oracle policies: none
- Modality: MUST
- Normative action: Slot contract completeness: a slot implementation supplies every required facet of its slot contract with the stated form, level, loading and content (architecture: style, boundaries, layout, check; backend-testing: framework rule, commands, enforcement adapter, knowledge skill; frontend when selected: framework, stack, commands, enforcement, knowledge; persistence: access, seeding, dev-config, workflow, commands, enforcement, knowledge) and the frame expresses every role of roles.md without contradicting a role-level rule; a missing required facet is a conformance failure raised as a Decision Request instead of shipping the module.
- Trigger/scope: creating or replacing a slot implementation (template maintenance, architecture-decision)
- Exceptions: none stated
- Why EXTRA: Template capability-contract structure; no oracle policy requires an implementation to ship enforcement data, command facets or knowledge skills, or defines conformance of instruction modules.
- Evidence:
  - `.claude/capabilities/architecture/CONTRACT.md:9-14` (EXTRA, L1-S000069): "Must provide"
  - `.claude/capabilities/architecture/CONTRACT.md:18-18` (EXTRA, L1-S000071): "Express every role in `roles.md`; never contradict a role-level rule."
  - `.claude/capabilities/backend-testing/CONTRACT.md:9-14` (EXTRA, L1-S000080): "Must provide"
  - `.claude/capabilities/frontend/CONTRACT.md:9-15` (EXTRA, L1-S000139): "Must provide"
  - `.claude/capabilities/persistence/CONTRACT.md:5-5` (EXTRA, L1-S000144): "Placement comes from the architecture frame; this slot supplies technique."
  - `.claude/capabilities/persistence/CONTRACT.md:9-17` (EXTRA, L1-S000146): "Must provide"
  - `.claude/capabilities/persistence/CONTRACT.md:26-26` (EXTRA, L1-S000151): "A missing required facet is a conformance failure"
  - `.claude/INSTRUCTION_MAP.md:138-138` (DUPLICATE, L1-S000292): "| `.claude/scripts/check-instructions.mjs` | headers and levels, rule paths, conformance direction, selection, slot contracts and manifests (required facets, `binds:`, leak tokens, frame terms), imports, leakage, Core/Architecture technology neutrality (no pointer exemption; case-, separator- and Markdown-insensitive vocabulary plus API shapes), references, required skills, exec-form hook registra"
  - `.claude/scripts/check-instructions.mjs:263-265` (EXTRA, L1-S000612): "title must declare the slot as"
  - `.claude/scripts/check-instructions.mjs:289-292` (EXTRA, L1-S000618): "missing "- leak-tokens:" line"
  - `.claude/scripts/check-instructions.mjs:299-310` (EXTRA, L1-S000622): "does not belong to slot"
  - `.claude/scripts/check-instructions.mjs:313-313` (EXTRA, L1-S000624): "missing required facet"
  - `.claude/scripts/check-instructions.mjs:362-363` (EXTRA, L1-S000633): "which is not a selected module"

### EXTRA-L1-0002
- Closest oracle policies: none
- Modality: MUST
- Normative action: Leak rule: outside an implementation module (its manifest-listed facet files and module directory), instruction artifacts refer to slot concerns only by slot name, facet role (<slot>.<facet>) and the stable role vocabulary; implementation names appear only in the selection record and the instruction map; workflows reach implementation-specific steps through facet roles and must not hardcode selected implementations; leaf slots depend on roles, not frame terms.
- Trigger/scope: authoring or changing instruction artifacts
- Exceptions: Module-owned facets; the selection record (decisions.md capability selection) and INSTRUCTION_MAP.md.
- Why EXTRA: Instruction-authoring vocabulary rule of the L1 capability design; no oracle policy restricts which technology names may appear in which instruction files.
- Evidence:
  - `.claude/capabilities/architecture/CONTRACT.md:5-5` (EXTRA, L1-S000067): "Placement belongs to the frame; technique belongs to the leaf."
  - `.claude/capabilities/backend-testing/CONTRACT.md:18-18` (MIXED, L1-S000082): "Workflows refer only to `backend-testing.*` facets and need no edits. Changing the selection is Reserved and requires an ADR."
  - `.claude/INSTRUCTION_MAP.md:127-127` (MIXED, L1-S000284): "Changing a selection is Reserved and needs an ADR"
  - `.claude/INSTRUCTION_MAP.md:138-138` (DUPLICATE, L1-S000292): "| `.claude/scripts/check-instructions.mjs` | headers and levels, rule paths, conformance direction, selection, slot contracts and manifests (required facets, `binds:`, leak tokens, frame terms), imports, leakage, Core/Architecture technology neutrality (no pointer exemption; case-, separator- and Markdown-insensitive vocabulary plus API shapes), references, required skills, exec-form hook registra"
  - `.claude/rules/1-architecture/roles.md:12-12` (EXTRA, L1-S000450): "Instructions outside the frame use these roles instead of frame-specific layer names."
  - `.claude/scripts/check-instructions.mjs:289-292` (EXTRA, L1-S000618): "missing "- leak-tokens:" line"
  - `.claude/scripts/check-instructions.mjs:297-297` (EXTRA, L1-S000620): "frame manifest lacks "- frame-terms:""
  - `.claude/scripts/check-instructions.mjs:415-415` (EXTRA, L1-S000644): "use slot/facet/role vocabulary or move the content into the module"
  - `.claude/scripts/check-instructions.mjs:463-464` (EXTRA, L1-S000650): "is not declared in"
  - `.claude/skills/template-maintenance/SKILL.md:17-17` (EXTRA, L1-S001575): "never implementation names"

### EXTRA-L1-0003
- Closest oracle policies: none
- Modality: MUST
- Normative action: Content ownership in the capability model: placement belongs to the architecture frame and technique to leaf modules; implementation-independent policy (test policy, frontend structure, browser security, package-manager conventions) stays outside modules in neutral rules; frame facets keep leaf technology out; leaf bindings that cannot be expressed through roles are declared as binds: in the leaf manifest (persistence requires a binds: declaration to the selected frame).
- Trigger/scope: template content placement during maintenance or capability replacement
- Exceptions: none stated
- Why EXTRA: Template-structure ownership rule; the oracle prescribes no ownership location for instruction content.
- Evidence:
  - `.claude/capabilities/architecture/CONTRACT.md:5-5` (EXTRA, L1-S000067): "Placement belongs to the frame; technique belongs to the leaf."
  - `.claude/capabilities/architecture/CONTRACT.md:19-19` (EXTRA, L1-S000072): "Keep leaf technology out of frame facets"
  - `.claude/capabilities/architecture/CONTRACT.md:20-20` (EXTRA, L1-S000073): "must be declared by the leaf as `binds:` in its manifest"
  - `.claude/capabilities/backend-testing/CONTRACT.md:5-5` (EXTRA, L1-S000078): "Implementation-independent test policy stays outside the module"
  - `.claude/capabilities/frontend/CONTRACT.md:5-5` (EXTRA, L1-S000137): "Framework-neutral frontend structural policy stays outside the module"
  - `.claude/capabilities/persistence/CONTRACT.md:5-5` (EXTRA, L1-S000144): "Placement comes from the architecture frame; this slot supplies technique."
  - `.claude/capabilities/persistence/CONTRACT.md:25-25` (EXTRA, L1-S000150): "requires-binds: architecture"
  - `.claude/INSTRUCTION_MAP.md:138-138` (DUPLICATE, L1-S000292): "| `.claude/scripts/check-instructions.mjs` | headers and levels, rule paths, conformance direction, selection, slot contracts and manifests (required facets, `binds:`, leak tokens, frame terms), imports, leakage, Core/Architecture technology neutrality (no pointer exemption; case-, separator- and Markdown-insensitive vocabulary plus API shapes), references, required skills, exec-form hook registra"
  - `.claude/scripts/check-instructions.mjs:289-292` (EXTRA, L1-S000618): "missing "- leak-tokens:" line"
  - `.claude/scripts/check-instructions.mjs:336-339` (EXTRA, L1-S000626): "a frame never depends on a leaf"
  - `.claude/scripts/check-instructions.mjs:342-342` (EXTRA, L1-S000628): "binds must be "none" or"
  - `.claude/scripts/check-instructions.mjs:354-355` (EXTRA, L1-S000630): "requires a binding to the"
  - `.claude/skills/template-maintenance/SKILL.md:17-17` (EXTRA, L1-S001575): "never implementation names"

### EXTRA-L1-0004
- Closest oracle policies: ARC-020, DEP-002, GOV-017
- Modality: MUST
- Normative action: A capability-selection change (changing the frame, replacing a leaf implementation or provider, clearing or adding the optional frontend) requires an ADR recorded with architecture-decision in addition to Reserved approval.
- Trigger/scope: capability selection changes
- Exceptions: none stated
- Why EXTRA: ARC-020/DEP-002/GOV-017 require explicit approval for replacing approved technology but no oracle policy requires an ADR artifact for the change.
- Evidence:
  - `.claude/capabilities/architecture/CONTRACT.md:24-24` (MIXED, L1-S000075): "Changing the frame is Reserved and requires an ADR"
  - `.claude/capabilities/backend-testing/CONTRACT.md:18-18` (MIXED, L1-S000082): "Workflows refer only to `backend-testing.*` facets and need no edits. Changing the selection is Reserved and requires an ADR."
  - `.claude/capabilities/frontend/CONTRACT.md:19-19` (MIXED, L1-S000141): "Changing the selection is Reserved and requires an ADR."
  - `.claude/INSTRUCTION_MAP.md:127-127` (MIXED, L1-S000284): "Changing a selection is Reserved and needs an ADR"
  - `.claude/skills/architecture-decision/SKILL.md:47-47` (MIXED, L1-S000789): "always needs an ADR"
  - `.claude/skills/template-maintenance/SKILL.md:25-25` (EXTRA, L1-S001579): "record the ADR with `architecture-decision`"
  - `CLAUDE.md:35-35` (MIXED, L1-S001655): "changing a capability selection (also requires an ADR)"

### EXTRA-L1-0005
- Closest oracle policies: none
- Modality: MUST
- Normative action: Replacement and removal procedure: replacing a slot implementation replaces all of its facets together (rule facet, commands, enforcement data, knowledge content, selection row; for the frame also the CLAUDE.md style import) and keeps neutral rules such as roles.md unchanged unless the role vocabulary itself changes (Reserved); workflows refer only to facets and need no edits; removing the optional frontend sets its selection row to none, deletes every manifest-listed file and the module directory, removes the frontend-stack import from CLAUDE.md and the module rows from the instruction map; every replacement or removal ends with a passing check-instructions run.
- Trigger/scope: template maintenance: capability replacement and removal
- Exceptions: none stated
- Why EXTRA: Template maintenance procedure of the capability model; no oracle policy governs how instruction files change when a technology is replaced or removed.
- Evidence:
  - `.claude/capabilities/architecture/clean-architecture/MODULE.md:23-23` (EXTRA, L1-S000064): "Replace all four facets together"
  - `.claude/capabilities/architecture/CONTRACT.md:24-24` (MIXED, L1-S000075): "Changing the frame is Reserved and requires an ADR"
  - `.claude/capabilities/backend-testing/CONTRACT.md:18-18` (MIXED, L1-S000082): "Workflows refer only to `backend-testing.*` facets and need no edits. Changing the selection is Reserved and requires an ADR."
  - `.claude/capabilities/frontend/angular/MODULE.md:22-22` (EXTRA, L1-S000134): "Delete every file in the table plus this directory"
  - `.claude/capabilities/frontend/CONTRACT.md:19-19` (MIXED, L1-S000141): "Changing the selection is Reserved and requires an ADR."
  - `.claude/skills/architecture-decision/SKILL.md:47-47` (MIXED, L1-S000789): "always needs an ADR"
  - `.claude/skills/template-maintenance/SKILL.md:25-25` (EXTRA, L1-S001579): "record the ADR with `architecture-decision`"

### EXTRA-L1-0006
- Closest oracle policies: DEP-009, ARC-020, GOV-006
- Modality: MUST
- Normative action: Persistence semantics on change: the persistence selection records declared properties (provider variant, default string-comparison/case-sensitivity semantics, migration mechanism, seeding mechanism); replacing the implementation (e.g. an ORM by a micro-ORM) must not silently lose migration or seeding semantics and the new module states its mechanisms explicitly; a database-provider change is a variation inside the persistence slot that updates the declared properties, persistence.dev-config, the relational-fidelity binding and commands.
- Trigger/scope: persistence implementation or provider changes
- Exceptions: none stated
- Why EXTRA: ARC-020 requires approval for new persistence technology and GOV-006 for observable string semantics, but no oracle policy requires preserving migration/seeding mechanisms or maintaining a declared-property record when persistence changes.
- Evidence:
  - `.claude/capabilities/persistence/CONTRACT.md:21-21` (EXTRA, L1-S000148): "Provider variant, default string-comparison/case-sensitivity semantics, migration mechanism, seeding mechanism."
  - `.claude/capabilities/persistence/CONTRACT.md:27-27` (EXTRA, L1-S000152): "must not silently lose migration or seeding semantics"
  - `.claude/capabilities/persistence/CONTRACT.md:28-28` (MIXED, L1-S000153): "It is Reserved and observable string-comparison changes need approval."
  - `.claude/rules/3-project/decisions.md:33-33` (MIXED, L1-S000549): "relying on it for observable behavior needs approval"
  - `.claude/skills/architecture-decision/SKILL.md:47-47` (MIXED, L1-S000789): "always needs an ADR"

### EXTRA-L1-0007
- Closest oracle policies: PST-009, PST-010
- Modality: MUST (workflow step) / SHOULD (Stop hook reminder, blocks stopping once per change state)
- Normative action: When the schema changes, add a migration from the implementation-layer project with the entry-point project as startup project; the Stop hook reminds when domain-model or persistence-configuration files changed without a migration change and asks to confirm that no schema change is needed.
- Trigger/scope: domain-model and persistence changes
- Exceptions: Git-only; once per material state; continuation caused by the hook is not re-blocked.
- Why EXTRA: The oracle requires a migration only for schema-affecting CUSTOM_SETTINGS changes (PST-009) and review of generated migrations (PST-010); it has no general duty to pair every schema change with a migration or to confirm schema impact at stop time.
- Evidence:
  - `.claude/capabilities/persistence/ef-core/workflow.md:11-11` (EXTRA, L1-S000190): "When the schema changes, add a migration"
  - `.claude/hooks/stop-cochange.mjs:47-47` (MIXED, L1-S000257): "Check seed, migration, and test co-changes manually"
  - `.claude/hooks/stop-cochange.mjs:60-60` (EXTRA, L1-S000260): "without a migration: confirm no schema change is needed"
  - `.claude/INSTRUCTION_MAP.md:136-136` (DUPLICATE, L1-S000290): "| `.claude/hooks/stop-cochange.mjs` | Stop reminder per material change state of the active worktree (model change without seeder/migration change, production code without test change, product-source change); unchanged state stays silent, a further change to the same file reminds again; `stop_hook_active` prevents loops | `persistence.workflow`, `verify`, `custom-settings` |"

### EXTRA-L1-0008
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: The persistence change procedure reports model changes, migration names with review notes (destructive operations called out), whether DbSeeder was updated or unaffected, and the tests added or updated.
- Trigger/scope: persistence changes
- Exceptions: none stated
- Why EXTRA: WF-009 requires reporting the actual verification state; it does not prescribe persistence-specific report contents.
- Evidence:
  - `.claude/capabilities/persistence/ef-core/workflow.md:32-32` (EXTRA, L1-S000200): "Report model changes, migration names with review notes"

### EXTRA-L1-0009
- Closest oracle policies: DEP-004, DEP-020, DEP-010
- Modality: MUST NOT (manifest hook finding after the change; no approval path)
- Normative action: Packages Microsoft.Extensions.Http.Polly, Polly.Extensions.Http (deprecated resilience integrations), FluentValidation.AspNetCore (deprecated automatic-validation integration) and Serilog.Sinks.Elasticsearch (deprecated sink) must not be added; the manifest hook reports them as 'must not be added'.
- Trigger/scope: NuGet manifests
- Exceptions: none stated
- Why EXTRA: DEP-004 requires checking deprecation and DEP-020 treats direct Polly integration as an explicit exception, but no oracle policy forbids specific packages outright regardless of approval.
- Evidence:
  - `.claude/hooks/manifest-policy.json:5-8` (EXTRA, L1-S000204): ""reason": "deprecated sink package; use Elastic.Serilog.Sinks""
  - `.claude/hooks/post-change-checks.mjs:54-54` (EXTRA, L1-S000218): "must not be added"
  - `.claude/INSTRUCTION_MAP.md:135-135` (DUPLICATE, L1-S000289): "| `.claude/hooks/post-change-checks.mjs` + `.claude/hooks/manifest-policy.json` | PostToolUse Edit/Write/MultiEdit (edited file) and Bash/PowerShell, plus PostToolUseFailure Bash/PowerShell: validates the actual manifest state of the active worktree regardless of command text (per-worktree snapshot; first observation validates all manifests, later calls only added/changed/removed/moved ones, HEAD "
  - `.claude/skills/add-dependency/SKILL.md:17-17` (MIXED, L1-S000695): "integrations are never added"
  - `.claude/skills/aspnet-error-handling/SKILL.md:69-69` (MIXED, L1-S000809): "Register validators with `FluentValidation.DependencyInjectionExtensions`"
  - `.claude/skills/httpclient-factory/references/resilience.md:5-5` (MIXED, L1-S001276): "deprecated Polly integrations never"
  - `.claude/skills/logging/references/serilog.md:95-95` (EXTRA, L1-S001345): "The `Serilog.Sinks.Elasticsearch` package is deprecated"
  - `.claude/skills/project-structure/references/baseline-packages.md:18-18` (MIXED, L1-S001417): "Do not make the built-in `AddOpenApi()`/`MapOpenApi()` endpoint the template default"

### EXTRA-L1-0010
- Closest oracle policies: DEP-001, DEP-003
- Modality: MUST (PreToolUse hook: first attempt denied)
- Normative action: Dependency-removal commands (npm/pnpm uninstall, remove, rm, un, unlink; yarn remove; dotnet remove package; dotnet package remove; dotnet tool uninstall; Uninstall-Package) are treated as dependency changes: the hook denies them once and routes them to the add-dependency workflow.
- Trigger/scope: Bash and PowerShell commands
- Exceptions: The identical command passes when retried within 30 minutes.
- Why EXTRA: DEP-001..DEP-005 govern additions and updates; no oracle policy routes dependency removals through a workflow gate.
- Evidence:
  - `.claude/hooks/pre-shell-command.mjs:194-194` (MIXED, L1-S000250): "Dependency change detected. Run the add-dependency workflow first"
  - `.claude/INSTRUCTION_MAP.md:134-134` (DUPLICATE, L1-S000288): "| `.claude/hooks/pre-shell-command.mjs` | PreToolUse Bash/PowerShell, critical, fails closed (missing script, crash, timeout, empty or malformed input block the command): dependency changes (`dotnet add/remove package`, `dotnet package add/remove/update`, `dotnet tool install`, npm/pnpm/yarn mutations incl. global options such as `--prefix`, `--workspace`, `--dir`, `--cwd`, `ng add`) → deny once, "
  - `CLAUDE.md:47-47` (MIXED, L1-S001663): "Dependency add/update/remove → `add-dependency`"

### EXTRA-L1-0011
- Closest oracle policies: ARC-020, ARC-001, GOV-017
- Modality: REQUIRES_APPROVAL (Reserved; PreToolUse hook asks on every reference command; manifest hook reports removed or moved project files)
- Normative action: Changing the project reference graph is Reserved unless it implements the approved layout: every dotnet add/remove reference and dotnet reference add/remove command requires user confirmation, and removing or moving a .csproj is reported as a Reserved change of the project set/reference graph.
- Trigger/scope: .NET project references and project files
- Exceptions: Changes implementing the approved layout (project-structure) are not Reserved, but the hook asks anyway because it cannot tell; direct .csproj edits are only checked afterwards by the architecture check.
- Why EXTRA: ARC-020 requires approval for new layers/projects and ARC-001 constrains direction; no oracle policy makes individual reference edges between existing projects (including direction-legal edges outside the documented layout) Reserved, nor requires confirmation of each reference command.
- Evidence:
  - `.claude/hooks/post-change-checks.mjs:213-213` (MIXED, L1-S000238): "a Reserved decision unless it implements the approved layout"
  - `.claude/hooks/pre-shell-command.mjs:171-173` (EXTRA, L1-S000248): "Changing the project reference graph is Reserved (CLAUDE.md § Decision control) unless it implements the approved layout"
  - `.claude/INSTRUCTION_MAP.md:134-134` (DUPLICATE, L1-S000288): "| `.claude/hooks/pre-shell-command.mjs` | PreToolUse Bash/PowerShell, critical, fails closed (missing script, crash, timeout, empty or malformed input block the command): dependency changes (`dotnet add/remove package`, `dotnet package add/remove/update`, `dotnet tool install`, npm/pnpm/yarn mutations incl. global options such as `--prefix`, `--workspace`, `--dir`, `--cwd`, `ng add`) → deny once, "
  - `.claude/INSTRUCTION_MAP.md:135-135` (DUPLICATE, L1-S000289): "| `.claude/hooks/post-change-checks.mjs` + `.claude/hooks/manifest-policy.json` | PostToolUse Edit/Write/MultiEdit (edited file) and Bash/PowerShell, plus PostToolUseFailure Bash/PowerShell: validates the actual manifest state of the active worktree regardless of command text (per-worktree snapshot; first observation validates all manifests, later calls only added/changed/removed/moved ones, HEAD "
  - `.claude/skills/project-structure/SKILL.md:24-24` (MIXED, L1-S001451): "The project-graph hook asks for confirmation of every reference command"
  - `CLAUDE.md:35-35` (MIXED, L1-S001655): "changing a capability selection (also requires an ADR)"

### EXTRA-L1-0012
- Closest oracle policies: none
- Modality: MUST (checker-enforced)
- Normative action: Level model of the instruction system: every artifact is placed by stability (0-core, 1-architecture, 2-technology, 3-project) and starts with a one-line header (Level, optional Capability/Facet, Owns, Scope, Loading); conformance dependencies point only to the same or a more stable level; Core and Architecture name no concrete implementation technology in any form, pointers included, except the fixed platform vocabulary (.NET, C#, TypeScript, Git, HTTP; ASP.NET Core and NuGet are not exempt) and refer to Level 2 only by role, capability, facet or a technology-neutral skill name; every artifact is listed in the instruction map, and check-instructions is run after any change.
- Trigger/scope: authoring or changing instruction artifacts (template maintenance)
- Exceptions: none stated
- Why EXTRA: Instruction-system organization rule of the L1 template; the oracle defines no level hierarchy, header format or technology-neutrality requirement for instruction files.
- Evidence:
  - `.claude/INSTRUCTION_MAP.md:7-7` (EXTRA, L1-S000269): "Conformance dependencies point only to the same or a more stable level; Core and Architecture name no concrete implementation technology in any form"
  - `.claude/INSTRUCTION_MAP.md:10-10` (EXTRA, L1-S000271): "Each artifact starts with a one-line header"
  - `.claude/INSTRUCTION_MAP.md:138-138` (DUPLICATE, L1-S000292): "| `.claude/scripts/check-instructions.mjs` | headers and levels, rule paths, conformance direction, selection, slot contracts and manifests (required facets, `binds:`, leak tokens, frame terms), imports, leakage, Core/Architecture technology neutrality (no pointer exemption; case-, separator- and Markdown-insensitive vocabulary plus API shapes), references, required skills, exec-form hook registra"
  - `.claude/scripts/check-instructions.mjs:196-196` (EXTRA, L1-S000603): "keep neutral policy here and move the technique to Level 2 or the owning capability facet"
  - `.claude/scripts/check-instructions.mjs:237-244` (EXTRA, L1-S000606): "missing one-line header starting with"
  - `.claude/scripts/check-instructions.mjs:297-297` (EXTRA, L1-S000620): "frame manifest lacks "- frame-terms:""
  - `.claude/scripts/check-instructions.mjs:371-375` (EXTRA, L1-S000636): "rule must declare non-empty "paths:" frontmatter"
  - `.claude/scripts/check-instructions.mjs:392-392` (EXTRA, L1-S000639): "a rule may depend only on the same or a more stable level"
  - `.claude/scripts/check-instructions.mjs:397-405` (EXTRA, L1-S000641): "imported by CLAUDE.md but header Loading is not "always""
  - `.claude/scripts/check-instructions.mjs:448-448` (EXTRA, L1-S000647): "frame vocabulary cannot legalize concrete technology at Levels 0/1"
  - `.claude/scripts/check-instructions.mjs:529-530` (EXTRA, L1-S000666): "the instruction map must not be auto-loaded"
  - `.claude/skills/template-maintenance/SKILL.md:15-15` (EXTRA, L1-S001573): "normative constraint → rule"
  - `.claude/skills/template-maintenance/SKILL.md:16-16` (EXTRA, L1-S001574): "Core and Architecture name no concrete technology"
  - `.claude/skills/template-maintenance/SKILL.md:23-24` (EXTRA, L1-S001578): "Update `.claude/INSTRUCTION_MAP.md`"
  - `.claude/skills/template-maintenance/SKILL.md:26-26` (EXTRA, L1-S001580): "Run the checker and fix every reported item:"

### EXTRA-L1-0013
- Closest oracle policies: ARC-020, DEP-009
- Modality: MUST
- Normative action: Static capability composition: exactly four slots (architecture required frame; persistence and backend-testing required leaves; frontend optional leaf); each required slot has exactly one selected implementation and the optional slot zero or one; only selected modules ship; module-owned artifacts declare Capability: and appear in their MODULE.md; a <slot>.<facet> reference resolves through the selection record and a cleared optional slot (none) means its facets do not apply.
- Trigger/scope: template capability structure and selection record
- Exceptions: none stated
- Why EXTRA: No oracle policy defines capability slots, their cardinality or a selection record; ARC-020/DEP-009 only fix the approved stack and require approval to change it.
- Evidence:
  - `.claude/INSTRUCTION_MAP.md:8-8` (EXTRA, L1-S000270): "only the four slots"
  - `.claude/INSTRUCTION_MAP.md:138-138` (DUPLICATE, L1-S000292): "| `.claude/scripts/check-instructions.mjs` | headers and levels, rule paths, conformance direction, selection, slot contracts and manifests (required facets, `binds:`, leak tokens, frame terms), imports, leakage, Core/Architecture technology neutrality (no pointer exemption; case-, separator- and Markdown-insensitive vocabulary plus API shapes), references, required skills, exec-form hook registra"
  - `.claude/rules/3-project/decisions.md:28-28` (EXTRA, L1-S000546): "Static composition: each required slot has exactly one selected implementation, the optional slot zero or one; only selected modules ship."
  - `.claude/rules/3-project/decisions.md:32-32` (EXTRA, L1-S000548): "clean-architecture"
  - `.claude/rules/3-project/decisions.md:35-35` (EXTRA, L1-S000551): "Decided stack: imported frontend stack rule."
  - `.claude/rules/3-project/decisions.md:37-37` (EXTRA, L1-S000552): "A cleared optional slot (`none`) means its facets do not apply."
  - `.claude/scripts/check-architecture.mjs:21-21` (EXTRA, L1-S000574): "the architecture slot is required"
  - `.claude/scripts/check-instructions.mjs:251-251` (EXTRA, L1-S000608): "only the four agreed slots exist"
  - `.claude/scripts/check-instructions.mjs:255-259` (EXTRA, L1-S000610): "has no selected implementation"
  - `.claude/scripts/check-instructions.mjs:271-274` (EXTRA, L1-S000614): "static composition: only selected modules ship"
  - `.claude/scripts/check-instructions.mjs:276-276` (EXTRA, L1-S000616): "(only the four agreed slots exist)"
  - `.claude/scripts/check-instructions.mjs:362-363` (EXTRA, L1-S000633): "which is not a selected module"
  - `.claude/scripts/check-instructions.mjs:463-464` (EXTRA, L1-S000650): "is not declared in"
  - `CLAUDE.md:48-48` (EXTRA, L1-S001664): "A `<slot>.<facet>` reference resolves through the capability selection in the decisions file."

### EXTRA-L1-0014
- Closest oracle policies: none
- Modality: MUST (checker-enforced)
- Normative action: Hooks are registered in exec form (command node with the script path as argument data, no shell); the critical PreToolUse gate sets onFailure block so a missing script, crash, timeout or malformed input blocks the command; PostToolUse and Stop hooks stay non-blocking.
- Trigger/scope: .claude/settings.json hook registrations (template maintenance)
- Exceptions: none stated
- Why EXTRA: Hook-configuration design of the template; no oracle policy regulates how instruction-system hooks are registered or how they fail.
- Evidence:
  - `.claude/INSTRUCTION_MAP.md:133-133` (EXTRA, L1-S000287): "the critical PreToolUse gate sets `onFailure: "block"`; post and Stop hooks stay non-blocking"
  - `.claude/INSTRUCTION_MAP.md:138-138` (DUPLICATE, L1-S000292): "| `.claude/scripts/check-instructions.mjs` | headers and levels, rule paths, conformance direction, selection, slot contracts and manifests (required facets, `binds:`, leak tokens, frame terms), imports, leakage, Core/Architecture technology neutrality (no pointer exemption; case-, separator- and Markdown-insensitive vocabulary plus API shapes), references, required skills, exec-form hook registra"
  - `.claude/scripts/check-instructions.mjs:544-553` (EXTRA, L1-S000669): "critical PreToolUse hook must set onFailure: "block""
  - `.claude/scripts/check-instructions.mjs:558-561` (EXTRA, L1-S000671): "Stop co-change hook is not registered"
  - `.claude/settings.json:7-7` (EXTRA, L1-S000684): ""onFailure": "block""

### EXTRA-L1-0015
- Closest oracle policies: none
- Modality: MUST (checker-enforced)
- Normative action: Instruction inventory integrity: the required workflow skills (development-workflow, project-structure, verify, code-review, build-fix, custom-settings, git-workflow, security-scan, add-dependency, architecture-decision, template-maintenance), the shared knowledge skills (http-api, aspnet-error-handling, logging, httpclient-factory, configuration, dependency-injection, caching, swagger, api-versioning, health-check, docker, ci-cd, modern-csharp, authentication) and each selected module's knowledge skill exist; a skill's frontmatter name equals its directory and it has a description; template-maintenance is user-only (disable-model-invocation: true) and every other skill stays model-invocable; named skill/agent references and .claude path references resolve; skill-private references are used only by their owning skill.
- Trigger/scope: template maintenance of .claude/skills, agents and references
- Exceptions: The instruction map may list private references.
- Why EXTRA: Inventory and invocation invariants of the template; no oracle policy requires particular skills to exist or fixes their invocation mode.
- Evidence:
  - `.claude/scripts/check-instructions.mjs:472-472` (EXTRA, L1-S000653): "required skill is missing"
  - `.claude/scripts/check-instructions.mjs:479-484` (EXTRA, L1-S000655): "must set disable-model-invocation: true (user-only workflow)"
  - `.claude/scripts/check-instructions.mjs:500-500` (EXTRA, L1-S000660): "references unknown skill or agent"
  - `.claude/scripts/check-instructions.mjs:510-510` (EXTRA, L1-S000662): "path reference does not resolve"
  - `.claude/scripts/check-instructions.mjs:521-521` (EXTRA, L1-S000664): "depends on private reference"
  - `.claude/skills/template-maintenance/SKILL.md:4-4` (EXTRA, L1-S001567): "disable-model-invocation: true"

### EXTRA-L1-0016
- Closest oracle policies: DEP-001, GOV-014
- Modality: MUST
- Normative action: Remove dependencies that are no longer used when that is part of the current change and safe to verify; do not leave dead references.
- Trigger/scope: dependency changes
- Exceptions: Unrelated dependency cleanup during a narrow task is excluded.
- Why EXTRA: DEP-001 restricts adding dependencies and GOV-014 limits scope; no oracle policy requires removing dependencies made unused by a change.
- Evidence:
  - `.claude/skills/add-dependency/SKILL.md:69-69` (MIXED, L1-S000712): "do not leave dead references"

### EXTRA-L1-0017
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: The add-dependency workflow reports package, version, license, vulnerability/deprecation result, target project and approvals obtained or still pending.
- Trigger/scope: dependency changes
- Exceptions: none stated
- Why EXTRA: WF-009 covers verification reporting; no oracle policy prescribes dependency-specific report contents.
- Evidence:
  - `.claude/skills/add-dependency/SKILL.md:73-73` (EXTRA, L1-S000714): "Package, version, license, vulnerability/deprecation result, target project, and approvals obtained or still pending."

### EXTRA-L1-0018
- Closest oracle policies: API-013, ARC-020
- Modality: REQUIRES_APPROVAL (Reserved)
- Normative action: Adopting API versioning is Reserved and needs explicit approval, even when a concrete compatibility need exists.
- Trigger/scope: HTTP API versioning
- Exceptions: none stated
- Why EXTRA: API-013 allows introducing versioning when a real compatibility need exists and does not require approval; the oracle's consequential-change list does not name API versioning adoption.
- Evidence:
  - `.claude/skills/api-versioning/SKILL.md:10-10` (MIXED, L1-S000759): "adopting versioning is Reserved"
  - `CLAUDE.md:35-35` (MIXED, L1-S001655): "changing a capability selection (also requires an ADR)"

### EXTRA-L1-0019
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST
- Normative action: Every approved Reserved decision is recorded as an ADR at docs/decisions/NNNN-<kebab-title>.md (Status Accepted with date, Approved by, Context, Decision, Consequences, Alternatives considered; docs/decisions/ created with the first ADR) and summarized as a decision line pointing to the ADR in the decision file of the owning level (frame style rule, decisions.md, frontend stack rule), never in a single cross-level register and without restating rules that live elsewhere.
- Trigger/scope: approved Reserved decisions
- Exceptions: Product behavior and tunable values go to SPECIFICATION.md / CUSTOM_SETTINGS.md instead.
- Why EXTRA: GOV-017 requires approval for Reserved changes but no recording artifact; GOV-007 covers product behavior sources only. No oracle policy requires ADR documents or level-stratified decision summaries.
- Evidence:
  - `.claude/skills/architecture-decision/SKILL.md:27-41` (EXTRA, L1-S000785): "Write an ADR at `docs/decisions/NNNN-<kebab-title>.md`"
  - `.claude/skills/architecture-decision/SKILL.md:43-43` (EXTRA, L1-S000787): "Record the change as a decision summary line pointing to the ADR"
  - `CLAUDE.md:38-38` (MIXED, L1-S001658): "record the accepted decision with `architecture-decision`"

### EXTRA-L1-0020
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: The architecture-decision workflow reports the decision, ADR path, decision files updated and follow-up work (structure, dependencies, migrations).
- Trigger/scope: decision recording
- Exceptions: none stated
- Why EXTRA: No oracle policy prescribes decision-recording report contents.
- Evidence:
  - `.claude/skills/architecture-decision/SKILL.md:51-51` (EXTRA, L1-S000791): "Decision, ADR path, decision files updated, follow-up work"

### EXTRA-L1-0021
- Closest oracle policies: DEP-010, API-010
- Modality: MUST
- Normative action: Register FluentValidation validators with the FluentValidation.DependencyInjectionExtensions package and follow the project's established invocation pattern instead of adding a competing mechanism.
- Trigger/scope: backend validation setup
- Exceptions: none stated
- Why EXTRA: DEP-010 fixes FluentValidation as the library and API-010 the validation boundaries; no oracle policy prescribes the registration package.
- Evidence:
  - `.claude/skills/aspnet-error-handling/SKILL.md:69-69` (MIXED, L1-S000809): "Register validators with `FluentValidation.DependencyInjectionExtensions`"
  - `.claude/skills/project-structure/references/baseline-packages.md:9-9` (MIXED, L1-S001410): "`FluentValidation.DependencyInjectionExtensions`"

### EXTRA-L1-0022
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: The build-fix report states the initial failure, root cause, changes made, backend build / frontend build / tests status (PASS, NOT RUN, NOT APPLICABLE) and remaining issues.
- Trigger/scope: build and test repair
- Exceptions: none stated
- Why EXTRA: WF-009 requires reporting actual verification states; it does not prescribe failure/root-cause/change sections.
- Evidence:
  - `.claude/skills/build-fix/SKILL.md:82-90` (MIXED, L1-S000894): "Backend build: PASS / NOT RUN / NOT APPLICABLE"

### EXTRA-L1-0023
- Closest oracle policies: RUN-021, ARC-019
- Modality: MUST NOT
- Normative action: Do not cache tracked ORM entities across commit boundaries (named caching anti-pattern).
- Trigger/scope: backend caching with the ORM
- Exceptions: none stated
- Why EXTRA: RUN-021 governs invalidation consistency and ARC-019 confines the ORM to the implementation layer; caching tracked entities is an ORM technique pitfall (EXC-011 class) that the template elevates to a named prohibition.
- Evidence:
  - `.claude/skills/caching/SKILL.md:72-72` (MIXED, L1-S000925): "caching tracked ORM entities across commit boundaries"

### EXTRA-L1-0024
- Closest oracle policies: WF-011, WF-012
- Modality: MUST
- Normative action: Code-review output gives for each finding severity, file/location, what is wrong, why it matters and the smallest reasonable fix, ordered by severity on the scale Critical (data loss, security vulnerability, reliably broken core behavior; blocks merge), High (likely defect or architecture/data-integrity issue; fix before merge), Medium (real maintainability, robustness or test gap), Low (non-blocking improvement).
- Trigger/scope: code review output
- Exceptions: none stated
- Why EXTRA: WF-011/WF-012 prescribe priorities and no manufactured findings; the oracle sets no output format or severity scale.
- Evidence:
  - `.claude/skills/code-review/SKILL.md:64-69` (EXTRA, L1-S000994): "**Critical** — data loss, security vulnerability, reliably broken core behavior"

### EXTRA-L1-0025
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: The custom-settings workflow reports the setting, old -> new value, every surface updated and the verify result.
- Trigger/scope: settings changes
- Exceptions: none stated
- Why EXTRA: No oracle policy prescribes settings-change report contents.
- Evidence:
  - `.claude/skills/custom-settings/SKILL.md:49-49` (EXTRA, L1-S001036): "Report the setting, old → new value, every surface updated, and the `verify` result."

### EXTRA-L1-0026
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: The development-workflow output summarizes what changed, Delegated decisions taken, open Decision Requests (Reserved) and the verify report.
- Trigger/scope: implementation work
- Exceptions: none stated
- Why EXTRA: WF-009 covers verification state and GOV-017 reporting of unresolved Decision Requests in headless runs; listing Delegated decisions in every implementation summary is an additional reporting duty.
- Evidence:
  - `.claude/skills/development-workflow/SKILL.md:54-54` (MIXED, L1-S001082): "Summarize what changed, Delegated decisions taken, open Decision Requests (Reserved), and the `verify` report."

### EXTRA-L1-0027
- Closest oracle policies: GOV-015, GOV-019
- Modality: MUST NOT
- Normative action: Treat main, master and other protected or shared branches as non-rewritable.
- Trigger/scope: Git history rewriting
- Exceptions: none stated
- Why EXTRA: GOV-015 permits repository-changing operations, including force-push and rebase, when explicitly requested; this rule forbids rewriting these branches without an approval path.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:16-16` (MIXED, L1-S001196): "Treat `main`, `master`, and other protected or shared branches as non-rewritable."

### EXTRA-L1-0028
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: A pull request stays focused and its description states what changed, why, how it was verified, and compatibility or migration notes.
- Trigger/scope: pull request preparation
- Exceptions: none stated
- Why EXTRA: No oracle policy prescribes PR description contents; WF-009 only requires truthful verification reporting.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:38-38` (MIXED, L1-S001210): "Never claim checks that were not run."

### EXTRA-L1-0029
- Closest oracle policies: RUN-016, DEP-020
- Modality: MUST NOT
- Normative action: Do not wrap normal ORM operations in a generic application-level retry pipeline; use the provider's own execution strategy for transient database faults; HTTP retry policies are not database policies.
- Trigger/scope: database access resilience
- Exceptions: none stated
- Why EXTRA: RUN-016 governs when retries are safe and the oracle treats database-retry examples as conditional technique (EXC-007); no oracle policy forbids an application-level retry pipeline around ORM operations.
- Evidence:
  - `.claude/skills/httpclient-factory/references/resilience.md:28-28` (EXTRA, L1-S001289): "Do not wrap normal ORM operations in a generic application-level retry pipeline"
  - `.claude/skills/httpclient-factory/references/resilience.md:49-49` (DUPLICATE, L1-S001296): "| Database transient faults | provider execution strategy |"

### EXTRA-L1-0030
- Closest oracle policies: RUN-005
- Modality: MUST NOT
- Normative action: Never mutate a shared HttpClient's DefaultRequestHeaders concurrently; apply per-request values such as dynamic tokens per request or through a delegating handler.
- Trigger/scope: outbound HTTP clients
- Exceptions: none stated
- Why EXTRA: RUN-005 governs client lifetime; thread-safe header handling is client technique that no oracle policy states.
- Evidence:
  - `.claude/skills/httpclient-factory/SKILL.md:80-80` (MIXED, L1-S001323): "never mutate shared `DefaultRequestHeaders` concurrently"
  - `.claude/skills/httpclient-factory/SKILL.md:88-88` (DUPLICATE, L1-S001327): "Per-request `HttpClient`; mandating one client model everywhere; retries on unsafe operations without idempotency analysis; unbounded retries; leaking `HttpResponseMessage`; ignored cancellation; dynamic tokens in shared default headers; mapping every upstream failure to one status; resilience pipelines added without understanding their behavior."

### EXTRA-L1-0031
- Closest oracle policies: DEP-008, DEP-023
- Modality: MUST
- Normative action: global.json pins the intended SDK line: the current stable SDK of the target .NET release (no RC/preview unless explicitly requested) with a rollForward policy that allows normal patch/feature-band servicing.
- Trigger/scope: repository scaffolding and shared .NET configuration
- Exceptions: Preview/RC when explicitly requested.
- Why EXTRA: DEP-008 fixes the platform and DEP-023 repository-level build configuration; no oracle policy requires a global.json SDK pin or a specific roll-forward policy.
- Evidence:
  - `.claude/skills/project-structure/references/solution-layout.md:35-35` (MIXED, L1-S001433): "no RC/preview unless explicitly requested"

### EXTRA-L1-0032
- Closest oracle policies: WF-020, WF-009
- Modality: MUST
- Normative action: Security-scan report shape: every report states the static-analysis limitation; uses the five-level severity scale Critical (sparingly) / High / Medium / Low / Info; each confirmed finding gives severity, file and location, title, evidence, why it is a risk, likely impact, smallest remediation and OWASP category when applicable; the report contains scope, limitations, a severity summary table, findings and per-layer results.
- Trigger/scope: security reviews
- Exceptions: none stated
- Why EXTRA: WF-020 requires evidence-based contextual severity and WF-009 truthful status reporting; the oracle prescribes no report structure, severity scale or mandatory limitation statement.
- Evidence:
  - `.claude/skills/security-scan/SKILL.md:10-10` (MIXED, L1-S001512): "State that limitation in every report."
  - `.claude/skills/security-scan/SKILL.md:62-66` (MIXED, L1-S001530): "**Critical** — use sparingly"
  - `.claude/skills/security-scan/SKILL.md:72-72` (MIXED, L1-S001533): "Label uncertain items `NEEDS VERIFICATION`."
  - `.claude/skills/security-scan/SKILL.md:74-101` (EXTRA, L1-S001534): "Limitations: Static analysis only."

### EXTRA-L1-0033
- Closest oracle policies: none
- Modality: MUST
- Normative action: Loading and ownership placement of instruction content: always-needed planning policy goes into CLAUDE.md or an imported always rule; path-specific policy into a rule whose paths cover at least its scope; procedure obligations into the owning workflow; each rule has one owner (elsewhere only a pointer or a yes/no check naming the owner); the always-loaded surface (CLAUDE.md, its imports, skill descriptions) stays compact — path or workflow policy is not moved into it and always-needed policy is not moved out of it to save tokens.
- Trigger/scope: template maintenance
- Exceptions: none stated
- Why EXTRA: Instruction-system placement rules; the oracle does not regulate where instruction content is loaded or owned.
- Evidence:
  - `.claude/skills/template-maintenance/SKILL.md:18-19` (EXTRA, L1-S001576): "add the rule once"
  - `.claude/skills/template-maintenance/SKILL.md:34-34` (EXTRA, L1-S001583): "Keep the always-loaded surface compact"

### EXTRA-L1-0034
- Closest oracle policies: GOV-017, GOV-005
- Modality: MUST
- Normative action: Unclear-case test: any 'yes' makes a decision Reserved — does it add, remove or replace a dependency, framework or infrastructure capability; change a project/layer/reference boundary; establish a convention other code must follow; change observable behavior or a public contract; become expensive to reverse once other code depends on it?
- Trigger/scope: decisions whose classification is unclear
- Exceptions: none stated
- Why EXTRA: GOV-017 requires a Decided/Delegated/Reserved classification but not this test; under it any unclear dependency addition or removal becomes Reserved, whereas the oracle allows dependencies with a concrete need (DEP-001) and delegates routine internal choices (GOV-005).
- Evidence:
  - `CLAUDE.md:36-36` (EXTRA, L1-S001656): "Unclear case: any "yes" makes it Reserved"

### EXTRA-L1-0035
- Closest oracle policies: RUN-009, DEP-023
- Modality: MUST (repository build configuration)
- Normative action: Repository-wide Directory.Build.props enables nullable reference types and implicit usings for every .NET project (target framework net10.0).
- Trigger/scope: all .NET projects
- Exceptions: Project-specific overrides in project files.
- Why EXTRA: DEP-023 places shared settings in Directory.Build.props and DEP-008 fixes the platform; no oracle policy requires nullable reference types or implicit usings.
- Evidence:
  - `Directory.Build.props:5-6` (EXTRA, L1-S001676): "<Nullable>enable</Nullable>"

## LINK_UNCERTAIN (2)

### UNCERTAIN-L1-0001
- Closest oracle policies: GOV-015, DEP-007
- Modality: MUST
- Normative action: Commit package.json and package-lock.json.
- Trigger/scope: frontend workspace manifests
- Exceptions: none stated
- Open question: Read as a version-control content convention (both files belong in the repository) the clause is entailed by DEP-007; read as an instruction to perform commits it conflicts with GOV-015, which allows commits only on explicit request. The text does not resolve which reading is meant.
- Evidence:
  - `.claude/rules/3-project/package-management.md:17-17` (MIXED, L1-S000567): "commit `package.json` and `package-lock.json`, keep the lockfile consistent"

### UNCERTAIN-L1-0002
- Closest oracle policies: GOV-015
- Modality: MUST NOT (conditional)
- Normative action: High-risk Git operations (reset --hard, clean, push --force, push --force-with-lease, branch deletion, rebasing shared history) run only when explicitly requested or required by an approved workflow, and only after inspecting what will be lost or rewritten.
- Trigger/scope: Git operations
- Exceptions: 'required by an approved workflow'
- Open question: GOV-015 allows repository-changing Git operations only on explicit request; the alternative trigger 'required by an approved workflow' names no such workflow and could authorize high-risk operations without an explicit request, or could merely refer to an explicitly approved procedure. The relation to GOV-015 cannot be settled from the text.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:16-16` (MIXED, L1-S001196): "Treat `main`, `master`, and other protected or shared branches as non-rewritable."

