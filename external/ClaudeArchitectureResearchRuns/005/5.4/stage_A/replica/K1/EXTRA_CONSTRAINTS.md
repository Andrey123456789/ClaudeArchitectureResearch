# K1 — EXTRA and LINK_UNCERTAIN constraints (Claude Run 2, blind replica)

Every constraint below is an effective candidate behavior judged not entailed by the 196 oracle policies (EXTRA) or whose relation could not be decided (LINK_UNCERTAIN). Citations are template-relative paths under `inputs/K1/output/template/` with exact source quotes (newlines shown as ⏎).

## EXTRA (45)

### EXTRA-K1-0001
- Closest oracle policies: ARC-020, DEP-009
- Modality: MUST
- Normative action: Static capability composition: each required slot (architecture frame, persistence leaf, backend-testing leaf) has exactly one implementation (persistence with exactly one provider variant); the optional frontend slot has zero or one; selection none means no frontend workspace, no facets and a register row recording none (pointers to absent facet locations stay valid and dormant); unselected implementations are not part of the runtime.
- Trigger/scope: Template capability structure: .claude/capabilities, decision-register selection, template maintenance and capability replacement
- Exceptions: none stated
- Why EXTRA: No oracle policy defines the template's own capability-slot composition or cardinality; this constrains how the instruction system may be structured and changed (repo/meta), beyond ARC-020/DEP-009 which only require approval for new persistence or replacing approved technology.
- Evidence:
  - `.claude/capabilities/architecture/CONTRACT.md:5-6` (EXTRA, K1-S000016): "Cardinality: exactly one implementation"
  - `.claude/capabilities/backend-testing/CONTRACT.md:5-6` (EXTRA, K1-S000024): "Cardinality: exactly one implementation"
  - `.claude/capabilities/frontend/CONTRACT.md:5-6` (EXTRA, K1-S000041): "- Slot type: optional leaf ⏎ - Cardinality: zero or one implementation; "none" means no frontend workspace, no facets, and the register row records `none`"
  - `.claude/capabilities/frontend/CONTRACT.md:34-34` (EXTRA, K1-S000047): "With the selection `none`, these locations are absent; pointers to them from neutral artifacts stay valid and dormant."
  - `.claude/capabilities/persistence/CONTRACT.md:5-6` (EXTRA, K1-S000050): "Cardinality: exactly one implementation, with one provider variant"
  - `.claude/MAP.md:139-189` (DUPLICATE, K1-S000093): "## View 2 — Capabilities ⏎  ⏎ Static composition: one implementation per required slot, zero or one for the optional slot; the selection lives in the decision register. ⏎  ⏎ ### architecture ⏎  ⏎ - Selected: clean-architecture (required frame). Binds: —. Declared: roles Domain, Application, Infrastructure, Api; not-adopted mediator-based styles. ⏎  ⏎ | Kind | Facet | Scope | Loading | ⏎ |---|---|---|---| ⏎ | DEC | `d"
  - `.claude/scripts/check-instructions.cjs:24-31` (EXTRA, K1-S000377): "The required leaf -> frame bindings are fixed here"
  - `.claude/scripts/check-instructions.cjs:465-488` (EXTRA, K1-S000404): "static composition allows one"
  - `.claude/scripts/check-instructions.cjs:522-569` (EXTRA, K1-S000407): "unselected implementation must not be part of the runtime"
  - `.claude/scripts/check-instructions.cjs:762-771` (EXTRA, K1-S000415): "pointers to them from neutral artifacts are dormant, not broken"
  - `.claude/scripts/check-manifests.cjs:9-16` (EXTRA, K1-S000425): "one role-named facet check per capability slot (no discovery)"
  - `.claude/scripts/check-manifests.cjs:35-48` (EXTRA, K1-S000430): "Required capability facet check missing for slot"
  - `.claude/skills/architecture-decision/SKILL.md:47-47` (MIXED, K1-S000646): "a selection change is Reserved"
  - `.claude/skills/architecture-decision/SKILL.md:51-51` (EXTRA, K1-S000649): "role-based facet file names stay the same"
  - `.claude/skills/template-maintenance/SKILL.md:45-45` (EXTRA, K1-S001597): "3. Capability changes: follow `architecture-decision` (contract coverage, single implementation per slot, no unselected implementations at runtime)."
  - `docs/architecture/decision-register.md:10-10` (EXTRA, K1-S001706): "Static composition: exactly one implementation per required slot and zero or one for the optional slot; unselected implementations are not part of the runtime. Each manifest lists its facets: `.claude/capabilities/<slot>/<implementation>/MODULE.md`."
  - `docs/architecture/decision-register.md:14-14` (MIXED, K1-S001708): "introducing any of them requires explicit approval"
  - `docs/architecture/decision-register.md:15-15` (MIXED, K1-S001709): "Default persistence: EF Core with Microsoft SQL Server"
  - `docs/architecture/decision-register.md:16-16` (MIXED, K1-S001710): "`WebApplicationFactory<Program>` is the ASP.NET Core integration-test baseline"
  - `docs/architecture/decision-register.md:17-17` (MIXED, K1-S001711): "Not added by default: NgRx, Axios, Lodash, Bootstrap, Tailwind"

### EXTRA-K1-0002
- Closest oracle policies: none
- Modality: MUST
- Normative action: A slot implementation must provide every required item listed in its slot CONTRACT.md (architecture: role-map, dependency-direction, domain-modeling, use-case-orchestration, commit-boundary-placement, composition-root, transport-contracts, test-project-placement, not-adopted-styles, scaffold-layout, reference-check; backend-testing: framework-standard, integration-host-binding, knowledge, test-scaffold, framework-consistency-check; frontend: stack-properties, framework-standard, knowledge, workspace-scaffold, library-check; persistence: technology-boundary, commit-boundary-binding, migration-mechanism, seeding-mechanism, provider-variant, declared-properties, testing-implications, change-workflow, knowledge, enforcement).
- Trigger/scope: Creating or replacing a slot implementation (template maintenance, architecture-decision)
- Exceptions: none stated
- Why EXTRA: Template capability contracts are research/template structure, not V2 policy; they require e.g. deterministic reference checks, library checks and framework-consistency checks as part of any implementation, which no oracle policy demands.
- Evidence:
  - `.claude/capabilities/architecture/CONTRACT.md:12-26` (EXTRA, K1-S000020): "An implementation must provide"
  - `.claude/capabilities/backend-testing/CONTRACT.md:11-19` (EXTRA, K1-S000027): "An implementation must provide"
  - `.claude/capabilities/frontend/CONTRACT.md:12-20` (EXTRA, K1-S000045): "An implementation must provide"
  - `.claude/capabilities/persistence/CONTRACT.md:11-24` (EXTRA, K1-S000053): "An implementation must provide"
  - `.claude/scripts/check-instructions.cjs:571-643` (EXTRA, K1-S000408): "raise a Decision Request before selecting this implementation"
  - `.claude/skills/architecture-decision/SKILL.md:49-49` (EXTRA, K1-S000647): "1. Read `.claude/capabilities/<slot>/CONTRACT.md` and the current module manifest (`.claude/capabilities/<slot>/<implementation>/MODULE.md`)."
  - `.claude/skills/template-maintenance/SKILL.md:45-45` (EXTRA, K1-S001597): "3. Capability changes: follow `architecture-decision` (contract coverage, single implementation per slot, no unselected implementations at runtime)."

### EXTRA-K1-0003
- Closest oracle policies: none
- Modality: MUST
- Normative action: Non-slot artifacts refer to slot concerns through each slot's stable role vocabulary (architecture: Domain, Application, Infrastructure, Api, Application Service, repository contract, Unit of Work/IUnitOfWork, test projects) rather than through the selected implementation's names (leak rule).
- Trigger/scope: Authoring or changing instruction-system artifacts outside capability modules
- Exceptions: Per the leak checker: facet files listed in the module manifest, the module directory, .claude/MAP.md, project-owned files (SPECIFICATION.md, CUSTOM_SETTINGS.md, .editorconfig, Directory.Build.props, Directory.Packages.props), and the register's capability-selection block and Accepted decisions log may name the implementation.
- Why EXTRA: Instruction-authoring vocabulary rule of the K1 capability design; no oracle policy restricts which technology names may appear in which instruction files.
- Evidence:
  - `.claude/capabilities/architecture/CONTRACT.md:8-8` (EXTRA, K1-S000018): "Stable role vocabulary usable by non-slot artifacts"
  - `.claude/scripts/check-instructions.cjs:40-41` (EXTRA, K1-S000382): "header problems are warnings and the leak rule does not apply"
  - `.claude/scripts/check-instructions.cjs:649-663` (EXTRA, K1-S000410): "outside its module; refer to the slot/facet role"
  - `.claude/skills/template-maintenance/SKILL.md:39-39` (EXTRA, K1-S001593): "- Leak rule: outside a module's facets, its manifest, the decision register's capability-selection block, and the maintainer map, never name the selected implementation; refer to slot and facet roles instead. Facet file names are role-based (`test-framework.md`, not the implementation's name)."

### EXTRA-K1-0004
- Closest oracle policies: none
- Modality: MUST
- Normative action: Frame/leaf ownership: placement (project roles, commit-boundary placement, composition, test-project placement and references) belongs to the architecture frame; technique belongs to the leaf slots (persistence, backend-testing), which declare their frame bindings with Binds:.
- Trigger/scope: Template content ownership during template maintenance or capability replacement
- Exceptions: The frame binds no slot.
- Why EXTRA: Template-structure ownership rule from the K1 capability model; the oracle prescribes no ownership location for instruction content (inventory grouping explicitly must not determine candidate structure).
- Evidence:
  - `.claude/capabilities/architecture/CONTRACT.md:7-7` (EXTRA, K1-S000017): "the frame binds no slot; leaves bind to it"
  - `.claude/capabilities/architecture/CONTRACT.md:10-10` (EXTRA, K1-S000019): "Placement belongs to the frame; technique belongs to the leaves (persistence, backend-testing), which declare their frame bindings with `Binds:`."
  - `.claude/capabilities/backend-testing/CONTRACT.md:7-7` (EXTRA, K1-S000025): "- Binds: architecture (test-project placement and references belong to the frame)"
  - `.claude/capabilities/persistence/CONTRACT.md:7-7` (EXTRA, K1-S000051): "- Binds: architecture (Infrastructure role implements the Application persistence and commit-boundary contracts)"
  - `.claude/rules/backend/architecture-style.md:10-10` (EXTRA, K1-S000128): "Placement belongs to this frame; technique belongs to the leaf capabilities that bind to it."
  - `.claude/rules/backend/persistence-technology.md:10-10` (MIXED, K1-S000194): "Binds to the architecture frame: EF Core lives in the Infrastructure role and implements the Application persistence and commit-boundary contracts."
  - `.claude/scripts/check-instructions.cjs:24-31` (EXTRA, K1-S000377): "The required leaf -> frame bindings are fixed here"
  - `.claude/scripts/check-instructions.cjs:383-433` (EXTRA, K1-S000402): "ENF artifact lacks its conformance declaration"
  - `.claude/scripts/check-instructions.cjs:503-520` (EXTRA, K1-S000406): "only leaves bind, and only to the ${FRAME} frame"
  - `.claude/scripts/check-instructions.cjs:522-569` (EXTRA, K1-S000407): "unselected implementation must not be part of the runtime"
  - `.claude/skills/template-maintenance/SKILL.md:18-18` (EXTRA, K1-S001585): "1. **Capability** — is it specific to the selected implementation of a slot (architecture, persistence, backend-testing, frontend)? Yes → the module owns it: it becomes a facet listed in that module's manifest (`.claude/capabilities/<slot>/<implementation>/MODULE.md`), and its header declares `Capability: <slot>/<implementation>`. No → non-slot content with `Capability: —`. Implementation-independent policy for a slot concern stays in the neutral standard; only implementation-specific rules go to the facet. Placement belongs to the architecture frame; technique belongs to leaves, which declare unavoidable frame bindings in `Binds:`."
  - `.claude/skills/template-maintenance/SKILL.md:48-48` (EXTRA, K1-S001600): "6. Enforcement artifacts (ENF) declare their policy owners on the line after the header: `Conforms: <STD or DEC owner>, …` or `Conforms: —`; every standard or register path an ENF artifact cites must be declared. Slot binding obligations (persistence and backend-testing bind architecture) and the contract's facet roles are fixed; keep `Binds:` in the contract and the manifest in agreement."

### EXTRA-K1-0005
- Closest oracle policies: none
- Modality: MUST
- Normative action: Facet locations are role-named and fixed: every implementation of a slot provides exactly the slot's listed facet locations (DEC row in the decision register, STD rule file, KNW facet, WF reference/skill, ENF facet script), file names never change with the implementation, and the backend-testing knowledge facet keeps the shared skill name dotnet-testing.
- Trigger/scope: Template maintenance and capability replacement
- Exceptions: With frontend selection none the frontend facet locations are absent.
- Why EXTRA: File-naming/location rule of the template's capability design, not derived from V2 policy.
- Evidence:
  - `.claude/capabilities/architecture/CONTRACT.md:28-38` (EXTRA, K1-S000021): "Role-named facet locations; every implementation provides exactly these (file names never change with the implementation)."
  - `.claude/capabilities/backend-testing/CONTRACT.md:9-9` (EXTRA, K1-S000026): "The framework-neutral testing standard (`.claude/rules/backend-tests/testing.md`) stays unchanged when the implementation is replaced. The knowledge facet keeps the shared skill name `dotnet-testing`."
  - `.claude/capabilities/backend-testing/CONTRACT.md:21-31` (EXTRA, K1-S000028): "Role-named facet locations; every implementation provides exactly these (file names never change with the implementation)."
  - `.claude/capabilities/frontend/CONTRACT.md:22-32` (EXTRA, K1-S000046): "Role-named facet locations; every implementation provides exactly these (file names never change with the implementation)."
  - `.claude/capabilities/persistence/CONTRACT.md:26-36` (EXTRA, K1-S000054): "Role-named facet locations; every implementation provides exactly these (file names never change with the implementation)."
  - `.claude/MAP.md:139-189` (DUPLICATE, K1-S000093): "## View 2 — Capabilities ⏎  ⏎ Static composition: one implementation per required slot, zero or one for the optional slot; the selection lives in the decision register. ⏎  ⏎ ### architecture ⏎  ⏎ - Selected: clean-architecture (required frame). Binds: —. Declared: roles Domain, Application, Infrastructure, Api; not-adopted mediator-based styles. ⏎  ⏎ | Kind | Facet | Scope | Loading | ⏎ |---|---|---|---| ⏎ | DEC | `d"
  - `.claude/scripts/check-instructions.cjs:522-569` (EXTRA, K1-S000407): "unselected implementation must not be part of the runtime"
  - `.claude/scripts/check-instructions.cjs:571-643` (EXTRA, K1-S000408): "raise a Decision Request before selecting this implementation"
  - `.claude/scripts/check-manifests.cjs:9-16` (EXTRA, K1-S000425): "one role-named facet check per capability slot (no discovery)"
  - `.claude/skills/architecture-decision/SKILL.md:51-51` (EXTRA, K1-S000649): "role-based facet file names stay the same"
  - `.claude/skills/template-maintenance/SKILL.md:18-18` (EXTRA, K1-S001585): "1. **Capability** — is it specific to the selected implementation of a slot (architecture, persistence, backend-testing, frontend)? Yes → the module owns it: it becomes a facet listed in that module's manifest (`.claude/capabilities/<slot>/<implementation>/MODULE.md`), and its header declares `Capability: <slot>/<implementation>`. No → non-slot content with `Capability: —`. Implementation-independent policy for a slot concern stays in the neutral standard; only implementation-specific rules go to the facet. Placement belongs to the architecture frame; technique belongs to leaves, which declare unavoidable frame bindings in `Binds:`."
  - `.claude/skills/template-maintenance/SKILL.md:39-39` (EXTRA, K1-S001593): "- Leak rule: outside a module's facets, its manifest, the decision register's capability-selection block, and the maintainer map, never name the selected implementation; refer to slot and facet roles instead. Facet file names are role-based (`test-framework.md`, not the implementation's name)."
  - `.claude/skills/template-maintenance/SKILL.md:46-46` (EXTRA, K1-S001598): "4. Update the module manifest's facet table and `.claude/MAP.md` (both views) for every added, moved, or removed artifact."
  - `docs/architecture/decision-register.md:10-10` (EXTRA, K1-S001706): "Static composition: exactly one implementation per required slot and zero or one for the optional slot; unselected implementations are not part of the runtime. Each manifest lists its facets: `.claude/capabilities/<slot>/<implementation>/MODULE.md`."

### EXTRA-K1-0006
- Closest oracle policies: none
- Modality: MUST
- Normative action: Framework-neutral standards (rules/backend-tests/testing.md; rules/frontend/frontend.md, rules/frontend/security.md, rules/frontend/dependencies.md) stay unchanged when a slot implementation is replaced.
- Trigger/scope: Capability replacement (backend-testing, frontend)
- Exceptions: none stated
- Why EXTRA: Change-procedure rule for the template's capability model; the oracle does not regulate how instruction files change when a technology is replaced.
- Evidence:
  - `.claude/capabilities/backend-testing/CONTRACT.md:9-9` (EXTRA, K1-S000026): "The framework-neutral testing standard (`.claude/rules/backend-tests/testing.md`) stays unchanged when the implementation is replaced. The knowledge facet keeps the shared skill name `dotnet-testing`."
  - `.claude/capabilities/frontend/CONTRACT.md:10-10` (EXTRA, K1-S000044): "The framework-neutral frontend standards (`.claude/rules/frontend/frontend.md`, `.claude/rules/frontend/security.md`, `.claude/rules/frontend/dependencies.md`) stay unchanged when the implementation is replaced."
  - `.claude/skills/template-maintenance/SKILL.md:18-18` (EXTRA, K1-S001585): "1. **Capability** — is it specific to the selected implementation of a slot (architecture, persistence, backend-testing, frontend)? Yes → the module owns it: it becomes a facet listed in that module's manifest (`.claude/capabilities/<slot>/<implementation>/MODULE.md`), and its header declares `Capability: <slot>/<implementation>`. No → non-slot content with `Capability: —`. Implementation-independent policy for a slot concern stays in the neutral standard; only implementation-specific rules go to the facet. Placement belongs to the architecture frame; technique belongs to leaves, which declare unavoidable frame bindings in `Binds:`."

### EXTRA-K1-0007
- Closest oracle policies: ARC-020, DEP-002, GOV-017
- Modality: MUST
- Normative action: A persistence provider change is a variant change inside the persistence slot, not a new slot; replacing the persistence implementation requires every contract item, and an item the proposed implementation cannot provide (e.g. a migration mechanism) is surfaced as Blocked in the Decision Request instead of being dropped.
- Trigger/scope: Proposals to change the persistence provider or implementation (architecture-decision)
- Exceptions: none stated
- Why EXTRA: DEP-002/ARC-020 require approval for replacing approved technology, but no oracle policy requires a contract-item completeness assessment or a Blocked marking inside the Decision Request.
- Evidence:
  - `.claude/capabilities/persistence/CONTRACT.md:9-9` (EXTRA, K1-S000052): "A provider change (for example to another relational database) is a variant change inside this slot, not a new slot. Replacing the implementation (for example with a micro-ORM) requires every item below; an item the proposed implementation cannot provide — such as a migration mechanism — is surfaced as *Blocked* in the Decision Request instead of being dropped."
  - `.claude/scripts/check-instructions.cjs:571-643` (EXTRA, K1-S000408): "raise a Decision Request before selecting this implementation"
  - `.claude/skills/architecture-decision/SKILL.md:50-50` (EXTRA, K1-S000648): "2. For the proposed implementation, map every contract item to a concrete mechanism. An item without a mechanism (for example a persistence implementation without a migration mechanism) must be named in the Decision Request under *Blocked* — never silently dropped."
  - `.claude/skills/architecture-decision/SKILL.md:54-54` (MIXED, K1-S000651): "is a Reserved persistence-technology change but not a new slot"

### EXTRA-K1-0008
- Closest oracle policies: DEP-001, DEP-003
- Modality: MUST (PreToolUse hook: blocks before execution, exit 2; PostToolUse warning on deleted package.json)
- Normative action: Dependency-removal commands (npm/pnpm uninstall|remove|rm|r|un|unlink, yarn remove, dotnet remove package, dotnet package remove) are blocked before execution and routed to the add-dependency workflow (removal); deleting a frontend package.json is reported as a warning that dependency removals go through add-dependency.
- Trigger/scope: Bash and PowerShell commands; frontend manifests
- Exceptions: none in the hook
- Why EXTRA: No oracle policy governs dependency removal (DEP-001..DEP-005 cover additions and updates); the hook makes every removal command fail via the shell regardless of approval.
- Evidence:
  - `.claude/hooks/dispatch.cjs:54-55` (EXTRA, K1-S000070): "-> add-dependency workflow (removal)"
  - `.claude/hooks/dispatch.cjs:65-79` (MIXED, K1-S000074): "Blocked before execution (dependency and project-reference guard)"
  - `.claude/rules/common/dependencies.md:12-12` (MIXED, K1-S000287): "every NuGet or npm addition, update, or removal runs `add-dependency`"
  - `.claude/scripts/actual-state.cjs:189-189` (EXTRA, K1-S000357): "dependency removals go through the add-dependency workflow"
  - `.claude/scripts/classify-command.cjs:242-251` (MIXED, K1-S000467): "findings.push({ kind: 'dependency-removal', segment, specs })"
  - `.claude/scripts/classify-command.cjs:307-307` (EXTRA, K1-S000472): "if (action === 'remove') return [{ kind: 'dependency-removal', segment, specs: positional }];"
  - `.claude/settings.json:3-16` (MIXED, K1-S000525): ""onFailure": "block""
  - `.claude/skills/add-dependency/SKILL.md:78-78` (EXTRA, K1-S000557): "The dependency-command hook blocks removal commands (`npm uninstall`, `dotnet remove … package`, and equivalents) so that removals pass this checklist: remove the entry from the manifest (the project `PackageReference`, plus the central `PackageVersion` when no project uses it any more; the `package.json` entry), then restore (`dotnet restore`, `npm install`) so the lockfile stays consistent."
  - `.claude/skills/add-dependency/SKILL.md:84-84` (DUPLICATE, K1-S000560): "Enforcement: before execution, the dependency-command hook routes additions and updates without an exact version, bulk updates, removals, and `--force`/`--legacy-peer-deps` here (updates re-run the install command with the exact selected version); after edits and shell commands, the manifest hook runs `.claude/scripts/check-manifests.cjs` on the files that actually changed."

### EXTRA-K1-0009
- Closest oracle policies: ARC-001, ARC-020, ARC-028, GOV-017
- Modality: MUST (Reserved; PreToolUse block for dotnet reference commands; PostToolUse error finding for .csproj edits)
- Normative action: Every .NET project-reference change (dotnet add|remove reference, dotnet reference add|remove, or a .csproj ProjectReference edit) is a Reserved decision: it is blocked or flagged as an error unless each edge appears as `From -> To` in a dated (YYYY-MM-DD) row of the decision register's Accepted decisions or a docs/decisions record linked from such a row.
- Trigger/scope: .NET project references in the active repository or worktree
- Exceptions: dotnet reference update is not classified; edges already in HEAD and reverted edits are not flagged; the Accepted decisions table ships empty.
- Why EXTRA: ARC-001 already permits inward references (Api -> Application, Infrastructure -> Application) and ARC-020 requires approval for consequential changes such as new layers/projects; no oracle policy requires a recorded, dated approval for each individual reference edge, including standard inward or narrow test references.
- Evidence:
  - `.claude/hooks/dispatch.cjs:58-59` (EXTRA, K1-S000072): "changes the project reference graph (${f.edges.map(e => `${e.from} -> ${e.to}`).join(', ') || 'unnamed project'}), a Reserved decision without a recorded approval"
  - `.claude/hooks/dispatch.cjs:65-79` (MIXED, K1-S000074): "Blocked before execution (dependency and project-reference guard)"
  - `.claude/scripts/actual-state.cjs:121-126` (EXTRA, K1-S000350): "for (const [k, to] of cur) { ⏎     if (!bas.has(k) && (!hasHead || !hd.has(k)) && !manifests.isApprovedEdge(approvals, name, to)) changes.push(`${name} -> ${to} added`); ⏎   } ⏎   for (const [k, to] of bas) { ⏎     if (!cur.has(k) && (!hasHead || hd.has(k)) && !manifests.isApprovedEdge(approvals, name, to)) changes.push(`${name} -> ${to} removed`); ⏎   }"
  - `.claude/scripts/actual-state.cjs:127-129` (MIXED, K1-S000351): "project reference graph changed without a recorded approval (Reserved)"
  - `.claude/scripts/check-manifests.cjs:190-201` (EXTRA, K1-S000451): "placeholders such as TBD or pending are not dates"
  - `.claude/scripts/check-manifests.cjs:202-221` (MIXED, K1-S000452): "register rows with a valid Date"
  - `.claude/scripts/check-manifests.cjs:223-228` (EXTRA, K1-S000453): "An edge is approved when an accepted decision lists it as `From -> To`."
  - `.claude/scripts/classify-command.cjs:301-306` (EXTRA, K1-S000471): "return [{ kind: 'reference-change', segment, action, edges }];"
  - `.claude/settings.json:3-16` (MIXED, K1-S000525): ""onFailure": "block""
  - `.claude/skills/architecture-decision/SKILL.md:40-40` (MIXED, K1-S000641): "list every affected reference as `From -> To`"
  - `.claude/skills/project-structure/references/test-setup.md:16-16` (MIXED, K1-S001401): "recorded first as `From -> To` through `architecture-decision`"
  - `.claude/skills/project-structure/SKILL.md:36-36` (MIXED, K1-S001418): "first record the requested scaffold through `architecture-decision`"
  - `.claude/skills/project-structure/SKILL.md:47-47` (MIXED, K1-S001426): "each new reference is recorded first"
  - `CLAUDE.md:35-35` (MIXED, K1-S001663): "or changing the project reference graph"

### EXTRA-K1-0010
- Closest oracle policies: PST-009, PST-010
- Modality: MUST (workflow rule) / SHOULD (Stop hook reminder, blocks stopping once per content state)
- Normative action: If the schema changes, a new migration is created (persistence-change); when persistence model files (Domain .cs, Infrastructure/Persistence/Configurations/*.cs, Infrastructure/Persistence/*DbContext.cs) change without any migration change, the agent is reminded at Stop to confirm whether the schema changed (a schema change is expected to come with a migration) and must address the reminder or state why it does not apply.
- Trigger/scope: Stop event in a Git work tree
- Exceptions: Git-only; once per content state.
- Why EXTRA: The oracle requires a migration only for schema-affecting CUSTOM_SETTINGS changes (PST-009) and review of generated migrations (PST-010); it contains no general duty that every model change be checked for schema impact and paired with a migration, nor a stop-time confirmation.
- Evidence:
  - `.claude/hooks/dispatch.cjs:124-128` (MIXED, K1-S000077): "Address each item or state why it does not apply, then finish."
  - `.claude/scripts/facets/persistence-technology.cjs:40-47` (EXTRA, K1-S000502): "persistence model changed without a migration; confirm whether the schema changed"
  - `.claude/settings.json:43-54` (MIXED, K1-S000528): ""Stop""
  - `.claude/skills/persistence-change/SKILL.md:36-36` (EXTRA, K1-S001331): "If the schema changes, create a **new** migration:"
  - `.claude/skills/verify/SKILL.md:53-53` (MIXED, K1-S001622): "Co-change reminders:"

### EXTRA-K1-0012
- Closest oracle policies: none
- Modality: MUST
- Normative action: Every instruction artifact is classified in the order Capability -> Kind -> Scope: capability-owned artifacts declare Capability: <slot>/<implementation> (others Capability: —); Kind (OP, DEC, STD, KNW, WF, ENF, IN) decides mechanism and location; Scope (common, backend, backend-tests, frontend, delivery, repo/meta) decides the rule directory and paths:.
- Trigger/scope: Authoring or changing instruction-system artifacts
- Exceptions: none stated
- Why EXTRA: Instruction-system classification scheme of the K1 design; no oracle policy dictates how instruction artifacts are classified, headed or located.
- Evidence:
  - `.claude/MAP.md:5-9` (EXTRA, K1-S000081): "Three coordinates classify every artifact, asked in this order:"
  - `.claude/scripts/check-instructions.cjs:10-11` (EXTRA, K1-S000374): "const KINDS = ['OP', 'DEC', 'STD', 'KNW', 'WF', 'ENF', 'IN', '—']; ⏎ const SCOPES = ['common', 'backend', 'backend-tests', 'frontend', 'delivery', 'repo/meta'];"
  - `.claude/scripts/check-instructions.cjs:40-41` (EXTRA, K1-S000382): "header problems are warnings and the leak rule does not apply"
  - `.claude/scripts/check-instructions.cjs:97-98` (EXTRA, K1-S000388): "const HEADER_RE = /^(?:>|\/\/|#|<!--)\s*Kind:\s*(\S+)(?:\s*\([^)]*\))?\s*\|\s*Scope:\s*([\w/-]+)\s*\|\s*Capability:\s*([^|]+?)\s*\|\s*Loading:\s*(.+?)\s*(?:-->)?\s*$/; ⏎ const CONFORMS_RE = /^(?:\/\/|#|<!--)\s*Conforms:\s*(.*?)\s*(?:-->)?\s*$/;"
  - `.claude/scripts/check-instructions.cjs:122-132` (EXTRA, K1-S000390): "function expectedKind(rel) { ⏎   if (rel === 'CLAUDE.md') return ['OP']; ⏎   if (rel === REGISTER) return ['DEC']; ⏎   if (rel === 'CUSTOM_SETTINGS.md' || rel === 'SPECIFICATION.md') return ['IN']; ⏎   if (rel === MAP || /^\.claude\/capabilities\/.+\/(CONTRACT|MODULE)\.md$/.test(rel)) return ['—']; ⏎   if (/^\.claude\/rules\//.test(rel)) return ['STD']; ⏎   if (/^\.claude\/skills\//.test(rel)) return ['KNW', 'WF']; ⏎   if (/^\.claude\/agents\//.test(rel)) return ['WF']; ⏎   if (/^\.claude\/(hooks|scripts)\//.test(rel) || ['.editorconfig', 'Directory.Build.props', 'Directory.Packages.props'].includes(rel)) return ['ENF']; ⏎   return null; ⏎ }"
  - `.claude/scripts/check-instructions.cjs:149-165` (EXTRA, K1-S000392): "Level headers are not part of this instruction system"
  - `.claude/skills/template-maintenance/SKILL.md:18-18` (EXTRA, K1-S001585): "1. **Capability** — is it specific to the selected implementation of a slot (architecture, persistence, backend-testing, frontend)? Yes → the module owns it: it becomes a facet listed in that module's manifest (`.claude/capabilities/<slot>/<implementation>/MODULE.md`), and its header declares `Capability: <slot>/<implementation>`. No → non-slot content with `Capability: —`. Implementation-independent policy for a slot concern stays in the neutral standard; only implementation-specific rules go to the facet. Placement belongs to the architecture frame; technique belongs to leaves, which declare unavoidable frame bindings in `Binds:`."
  - `.claude/skills/template-maintenance/SKILL.md:19-29` (EXTRA, K1-S001586): "2. **Kind** — determines mechanism and location: ⏎  ⏎    | Kind | Content | Location / mechanism | ⏎    |---|---|---| ⏎    | OP | Operating policy, approval and stop boundaries | `CLAUDE.md` (always loaded) | ⏎    | DEC | Project decisions, stack, defaults, capability selection | `docs/architecture/decision-register.md` (imported) | ⏎    | STD | Path-scoped normative standards | `.claude/rules/<scope>/<topic>.md` with `paths:` | ⏎    | KNW | Technique, examples, depth | `.claude/skills/<name>/SKILL.md` (+ private `references/`) | ⏎    | WF | Multi-step procedures, stop conditions, report shape | `.claude/skills/<name>/SKILL.md`, `.claude/agents/` | ⏎    | ENF | Deterministic enforcement/delivery | `.claude/ho […truncated in this report; the exact full quote is in coverage_ranges.jsonl]"
  - `.claude/skills/template-maintenance/SKILL.md:37-37` (EXTRA, K1-S001591): "never place critical must-policy only in a skill"
  - `.claude/skills/template-maintenance/SKILL.md:43-43` (EXTRA, K1-S001595): "1. Start each artifact with the one-line header `Kind | Scope | Capability | Loading` (after frontmatter where frontmatter is required)."
  - `.claude/skills/template-maintenance/SKILL.md:44-44` (EXTRA, K1-S001596): "2. Skills: frontmatter `name` equal to the directory, a concise trigger-first `description` with concrete cues; WF bodies own procedure and output shape; KNW bodies own technique and point to standards for policy."

### EXTRA-K1-0013
- Closest oracle policies: none
- Modality: MUST
- Normative action: Instruction dependency direction is WF -> KNW -> STD -> DEC -> OP and ENF -> STD/DEC; each ENF artifact declares what it conforms to on a Conforms: line directly after its header.
- Trigger/scope: Instruction-system artifacts
- Exceptions: Skill and agent references are routing pointers, not dependencies.
- Why EXTRA: Internal dependency discipline of the instruction system, not derived from any V2 policy.
- Evidence:
  - `.claude/MAP.md:11-11` (MIXED, K1-S000082): "Dependency direction: WF → KNW → STD → DEC → OP; ENF → STD/DEC, declared on each ENF artifact's `Conforms:` line (the line after its header); product inputs never override policy. Skill and agent references are routing pointers. Changing this system: `template-maintenance` (user-invoked); capability selection changes: `architecture-decision`."
  - `.claude/scripts/check-instructions.cjs:20-23` (EXTRA, K1-S000376): "const SCOPE_PARENT = { 'backend-tests': 'backend', backend: 'common', frontend: 'common', delivery: 'common', 'repo/meta': 'common', common: null }; ⏎ const RANK = { OP: 0, DEC: 1, STD: 2, KNW: 3, WF: 4 }; ⏎ // ENF conformance targets (ENF -> STD / DEC); ENF is not part of the Markdown rank chain. ⏎ const ENF_TARGET_KINDS = ['STD', 'DEC'];"
  - `.claude/scripts/check-instructions.cjs:97-98` (EXTRA, K1-S000388): "const HEADER_RE = /^(?:>|\/\/|#|<!--)\s*Kind:\s*(\S+)(?:\s*\([^)]*\))?\s*\|\s*Scope:\s*([\w/-]+)\s*\|\s*Capability:\s*([^|]+?)\s*\|\s*Loading:\s*(.+?)\s*(?:-->)?\s*$/; ⏎ const CONFORMS_RE = /^(?:\/\/|#|<!--)\s*Conforms:\s*(.*?)\s*(?:-->)?\s*$/;"
  - `.claude/scripts/check-instructions.cjs:281-348` (EXTRA, K1-S000399): "references to other non-invocable files are conformance dependencies and must follow"
  - `.claude/scripts/check-instructions.cjs:383-433` (EXTRA, K1-S000402): "ENF artifact lacks its conformance declaration"
  - `.claude/skills/template-maintenance/SKILL.md:38-38` (MIXED, K1-S001592): "Product inputs never override policy."
  - `.claude/skills/template-maintenance/SKILL.md:48-48` (EXTRA, K1-S001600): "6. Enforcement artifacts (ENF) declare their policy owners on the line after the header: `Conforms: <STD or DEC owner>, …` or `Conforms: —`; every standard or register path an ENF artifact cites must be declared. Slot binding obligations (persistence and backend-testing bind architecture) and the contract's facet roles are fixed; keep `Binds:` in the contract and the manifest in agreement."

### EXTRA-K1-0014
- Closest oracle policies: none
- Modality: MUST
- Normative action: Single owner per topic: each rule/topic lives in the artifact recorded as its owner in the map (Owns / Extend here when / Where does a topic live), new content is added at its owner, and the map is updated whenever an artifact is added, moved, or removed.
- Trigger/scope: Instruction-system maintenance
- Exceptions: none stated
- Why EXTRA: Research construction principle (one normative owner) realised as an instruction-maintenance rule; not one of the 196 V2 policies.
- Evidence:
  - `.claude/MAP.md:13-20` (DUPLICATE, K1-S000083): "## View 1 — Kind × Scope ⏎  ⏎ ### OP and DEC (always loaded) ⏎  ⏎ | File | Owns | Scope | Capability | Loading | Enforcement | Extend here when | ⏎ |---|---|---|---|---|---|---| ⏎ | `CLAUDE.md` | Product-source authority and approvals, string semantics, custom-settings boundaries, decision control (Decided/Delegated/Reserved, Reserved list, five-question test, headless behavior), simplicity and scope defaults"
  - `.claude/MAP.md:22-46` (DUPLICATE, K1-S000084): "### STD (path-scoped standards) ⏎  ⏎ | File | Owns | Scope | Capability | Loading | Enforcement | Extend here when | ⏎ |---|---|---|---|---|---|---| ⏎ | `.claude/rules/common/security.md` | Secrets, untrusted input, server-side authorization, TLS and certificate validation, sensitive and payload logging, fail-safe checks, visible security-configuration failure | common | — | `**/*` | — | a security rule a"
  - `.claude/MAP.md:48-70` (DUPLICATE, K1-S000085): "### WF (procedures) ⏎  ⏎ | File | Owns | Scope | Capability | Loading | Enforcement | Extend here when | ⏎ |---|---|---|---|---|---|---| ⏎ | `.claude/skills/development-workflow/SKILL.md` | Implementation sequence: read specification, inspect code, plan, regression tests, performance changes, API deprecation, durable-source sync, review, verify, report | common | — | on-demand workflow | — | an implementa"
  - `.claude/MAP.md:72-94` (DUPLICATE, K1-S000086): "### KNW (technique, on demand) ⏎  ⏎ | File | Owns | Scope | Capability | Loading | Enforcement | Extend here when | ⏎ |---|---|---|---|---|---|---| ⏎ | `.claude/skills/ef-core/SKILL.md` | EF Core technique, seeding code, migrations commands, raw SQL, SQL Server provider, EF Core testing | backend | persistence/ef-core | on-demand | via standards and checks of its slot facet | EF Core technique or examples"
  - `.claude/MAP.md:96-114` (DUPLICATE, K1-S000087): "### ENF (deterministic enforcement and delivery) ⏎  ⏎ | File | Owns | Scope | Capability | Loading | Enforcement | Extend here when | ⏎ |---|---|---|---|---|---|---| ⏎ | `.claude/settings.json` | Hook registration in exec form (`node`, launcher `${CLAUDE_PROJECT_DIR}/.claude/hooks/dispatch.cjs`, event): dependency/reference guard (PreToolUse, fails closed), actual-state checks after edits and shell comman"
  - `.claude/MAP.md:116-121` (DUPLICATE, K1-S000088): "### IN (product inputs, not instruction layers) ⏎  ⏎ | File | Owns | Scope | Capability | Loading | Enforcement | Extend here when | ⏎ |---|---|---|---|---|---|---| ⏎ | `SPECIFICATION.md` | Project-specific functional requirements and observable behavior (empty in the template) | common | — | read by workflows | edit hook: synchronization reminder | product behavior is approved | ⏎ | `CUSTOM_SETTINGS.md` | "
  - `.claude/MAP.md:123-126` (DUPLICATE, K1-S000089): "### Maintenance metadata (not loaded) ⏎  ⏎ | File | Owns | Scope | Capability | Loading | Enforcement | Extend here when | ⏎ |---|---|---|---|---|---|---|"
  - `.claude/MAP.md:127-127` (EXTRA, K1-S000090): "any artifact is added, moved, or removed"
  - `.claude/MAP.md:128-135` (EXTRA, K1-S000091): "the slot contract changes (rare; Reserved)"
  - `.claude/MAP.md:191-212` (DUPLICATE, K1-S000094): "## Where does a topic live? ⏎  ⏎ | Topic | Owner | ⏎ |---|---| ⏎ | Product authority, approvals, string semantics, tunable values | `CLAUDE.md` | ⏎ | Reserved decisions, Decision Requests | `CLAUDE.md` (policy), `.claude/skills/architecture-decision/SKILL.md` (procedure) | ⏎ | Selected technologies and defaults | `docs/architecture/decision-register.md` | ⏎ | Layer rules and dependency direction | `.claude/rule"
  - `.claude/scripts/check-instructions.cjs:665-681` (EXTRA, K1-S000411): "artifact not listed: ${rel}"
  - `.claude/skills/template-maintenance/SKILL.md:35-35` (EXTRA, K1-S001589): "- Every normative statement has exactly one owner. Elsewhere use only a routing pointer ("run `x`"), a check-by-reference item pointing at the owner, or a decision summary in the decision register."
  - `.claude/skills/template-maintenance/SKILL.md:46-46` (EXTRA, K1-S001598): "4. Update the module manifest's facet table and `.claude/MAP.md` (both views) for every added, moved, or removed artifact."

### EXTRA-K1-0015
- Closest oracle policies: GOV-017
- Modality: MUST (Reserved for contracts)
- Normative action: Changes to the instruction system go through the user-invoked template-maintenance workflow, and changing a slot contract is a Reserved decision (rare).
- Trigger/scope: Instruction-system and capability-contract changes
- Exceptions: none stated
- Why EXTRA: GOV-017 makes Reserved changes approval-gated but does not make the template's own slot contracts Reserved or route instruction changes through a user-invoked maintenance workflow.
- Evidence:
  - `.claude/MAP.md:11-11` (MIXED, K1-S000082): "Dependency direction: WF → KNW → STD → DEC → OP; ENF → STD/DEC, declared on each ENF artifact's `Conforms:` line (the line after its header); product inputs never override policy. Skill and agent references are routing pointers. Changing this system: `template-maintenance` (user-invoked); capability selection changes: `architecture-decision`."
  - `.claude/MAP.md:128-135` (EXTRA, K1-S000091): "the slot contract changes (rare; Reserved)"
  - `.claude/scripts/check-instructions.cjs:220-243` (EXTRA, K1-S000396): "template-maintenance must set disable-model-invocation: true"
  - `.claude/skills/architecture-decision/SKILL.md:42-42` (EXTRA, K1-S000643): "ask the user to run the user-invoked `template-maintenance` workflow"
  - `.claude/skills/architecture-decision/SKILL.md:51-51` (EXTRA, K1-S000649): "role-based facet file names stay the same"
  - `.claude/skills/template-maintenance/SKILL.md:7-7` (EXTRA, K1-S001579): "disable-model-invocation: true"
  - `.claude/skills/template-maintenance/SKILL.md:14-14` (EXTRA, K1-S001583): "Use only when the user explicitly asks to change the instruction system."
  - `CLAUDE.md:79-79` (EXTRA, K1-S001685): "`template-maintenance` (user-invoked only) governs changes to this instruction system"

### EXTRA-K1-0017
- Closest oracle policies: API-013, DEP-017, ARC-020
- Modality: MUST (Reserved)
- Normative action: Adopting API versioning is a Reserved decision (explicit approval required, per CLAUDE.md).
- Trigger/scope: Introducing API versioning in the backend
- Exceptions: none stated
- Why EXTRA: API-013 only forbids versioning without a concrete need and DEP-017 makes the package conditional; neither requires explicit approval to adopt versioning once a concrete need exists, and ARC-020's approval list does not include API versioning.
- Evidence:
  - `.claude/rules/backend/api-contracts.md:12-12` (MIXED, K1-S000098): "- Must not introduce API versioning merely because an API exists; add it only when published compatibility or coexistence of client generations creates a concrete need (adopting versioning: Reserved, `CLAUDE.md`)."
  - `.claude/skills/api-versioning/SKILL.md:13-13` (MIXED, K1-S000611): "Adopting versioning is Reserved (`architecture-decision`)"
  - `.claude/skills/development-workflow/SKILL.md:44-44` (MIXED, K1-S000951): "Breaking changes and adopting versioning are Reserved"
  - `CLAUDE.md:41-41` (MIXED, K1-S001669): "or adopting API versioning"

### EXTRA-K1-0016
- Closest oracle policies: PST-003, ARC-019
- Modality: MUST (placement convention; enforcement reminders key on these paths)
- Normative action: EF Core persistence code is organised under backend/<Name>.Infrastructure/Persistence/: the DbSeeder in Persistence/Seeding/, migrations in Persistence/Migrations/, entity configurations in Persistence/Configurations/ and the DbContext file there.
- Trigger/scope: backend persistence layout
- Exceptions: none stated
- Why EXTRA: PST-003 requires a dedicated internal seeder surface and ARC-019 keeps EF Core in Infrastructure, but no oracle policy fixes folder paths; the candidate binds concrete folders and its Stop-hook reminders only recognise these paths.
- Evidence:
  - `.claude/rules/backend/persistence-technology.md:21-21` (MIXED, K1-S000201): "- Substantial seed construction lives in a dedicated internal `DbSeeder` (`Persistence/Seeding/` in Infrastructure), exposed through a narrow Infrastructure initialization extension — never in `Program.cs`, `AppDbContext` configuration, entity configurations, or migrations."
  - `.claude/scripts/facets/persistence-technology.cjs:19-24` (EXTRA, K1-S000500): "Infrastructure\/Persistence\/Seeding"
  - `.claude/skills/persistence-change/SKILL.md:20-20` (EXTRA, K1-S001324): "2. In Infrastructure `Persistence/`: `AppDbContext` (configurations applied from the assembly), entity configurations in `Configurations/`, repositories in `Repositories/`, `UnitOfWork` implementing the Application `IUnitOfWork`, and `Seeding/DbSeeder.cs` plus the initialization extension."

### EXTRA-K1-0011
- Closest oracle policies: none
- Modality: MUST (PostToolUse feedback, exit 2)
- Normative action: When instruction files change (CLAUDE.md, docs/architecture/decision-register.md, .claude/** except settings.local.json), the instruction-structure checker runs and its errors are fed back to the agent for correction through the template-maintenance workflow.
- Trigger/scope: Edit/Write/MultiEdit or shell commands touching instruction files
- Exceptions: Warnings are not fed back; only checker errors.
- Why EXTRA: Structural self-validation of the instruction system; no oracle policy constrains instruction-file structure.
- Evidence:
  - `.claude/scripts/actual-state.cjs:205-208` (EXTRA, K1-S000359): "let instructionErrors = []; ⏎   if (instructionChanged) { ⏎     instructionErrors = require('./check-instructions.cjs').check(root).filter(f => f.severity === 'error'); ⏎   }"
  - `.claude/skills/template-maintenance/SKILL.md:52-52` (EXTRA, K1-S001602): "Run `node "<root>/.claude/scripts/check-instructions.cjs"` (`<root>`: the active repository root; command form in `verify`, Risk-scoped checks) and fix every error. Review the reported always-loaded size; keep it compact without moving required planning-time policy out of the always-loaded surface."
  - `.claude/skills/verify/SKILL.md:56-56` (EXTRA, K1-S001624): "- **Instruction system:** when `.claude/`, `CLAUDE.md`, or the decision register changed, run `node "<root>/.claude/scripts/check-instructions.cjs"`."

### EXTRA-K1-0018
- Closest oracle policies: none
- Modality: MUST (structure checker error)
- Normative action: Path-scoped standards live directly in .claude/rules/<scope>/ using only the scope directories common, backend, backend-tests, frontend, delivery (no deeper hierarchy); the header Scope equals the directory; every rule declares frontmatter paths: that include its scope's canonical glob (common **/*, backend backend/**/*, backend-tests backend/**/*Tests/**/*, frontend frontend/**/*).
- Trigger/scope: Adding or changing rule files
- Exceptions: Delivery rules declare their own CI/container globs (no canonical glob).
- Why EXTRA: Loading/organization rule of the K1 instruction system; no V2 policy regulates rule-file layout or globs.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:12-19` (EXTRA, K1-S000375): "const RULE_SCOPE_DIRS = ['common', 'backend', 'backend-tests', 'frontend', 'delivery']; ⏎ const CANONICAL_GLOBS = { ⏎   common: '**/*', ⏎   backend: 'backend/**/*', ⏎   'backend-tests': 'backend/**/*Tests/**/*', ⏎   frontend: 'frontend/**/*', ⏎   delivery: null, // delivery rules declare their own CI/container globs ⏎ };"
  - `.claude/scripts/check-instructions.cjs:167-189` (EXTRA, K1-S000393): "function checkRules(root, artifacts, out) { ⏎   for (const dir of lib.walk(root, '.claude/rules').map(r => r.split('/')[2]).filter(Boolean)) { ⏎     if (!RULE_SCOPE_DIRS.includes(dir)) out.push(lib.finding(ERR, `.claude/rules/${dir}`, 'rules are organized only by scope directory')); ⏎   } ⏎   for (const a of artifacts.values()) { ⏎     if (!a.rel.startsWith('.claude/rules/')) continue; ⏎     const parts = a.rel.split('/'); ⏎     if (parts.length !== 4) { ⏎       out.push(lib.finding(ERR, a.rel, 'rule files live directly in .claude/rules/<scope>/ (no deeper hierarchy)')); ⏎       continue; ⏎     } ⏎     const scope = parts[2]; ⏎     if (validHeader(a) && a.header.scope !== scope) out.push(lib.finding(ERR, a.rel, `he […truncated in this report; the exact full quote is in coverage_ranges.jsonl]"
  - `.claude/skills/template-maintenance/SKILL.md:31-31` (EXTRA, K1-S001587): "3. **Scope** — `common`, `backend`, `backend-tests`, `frontend`, `delivery`, `repo/meta`. A rule's `paths:` must include its scope's canonical glob (`**/*`, `backend/**/*`, `backend/**/*Tests/**/*`, `frontend/**/*`); no other directory hierarchy under `.claude/rules/`."

### EXTRA-K1-0019
- Closest oracle policies: none
- Modality: MUST (structure checker error)
- Normative action: CLAUDE.md must @-import the decision register; only OP/DEC artifacts may be @-imported into the always-loaded surface, every import must resolve, and no Markdown file other than CLAUDE.md may contain @ imports.
- Trigger/scope: Instruction-system structure
- Exceptions: none stated
- Why EXTRA: Always-loaded-surface composition rule of the template; not a V2 policy.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:191-209` (EXTRA, K1-S000394): "function checkImports(root, artifacts, out) { ⏎   const claude = artifacts.get('CLAUDE.md'); ⏎   if (!claude) { ⏎     out.push(lib.finding(ERR, 'CLAUDE.md', 'missing')); ⏎     return []; ⏎   } ⏎   const imports = claude.body.split(/\r?\n/).map(l => /^@(\S+)\s*$/.exec(l.trim())).filter(Boolean).map(m => lib.toPosix(path.posix.normalize(m[1]))); ⏎   if (!imports.includes(REGISTER)) out.push(lib.finding(ERR, 'CLAUDE.md', `must import the decision register (@${REGISTER})`)); ⏎   for (const imp of imports) { ⏎     const target = artifacts.get(imp); ⏎     if (!lib.exists(root, imp)) out.push(lib.finding(ERR, 'CLAUDE.md', `import does not resolve: @${imp}`)); ⏎     else if (!validHeader(target) || !['OP', 'DEC'].include […truncated in this report; the exact full quote is in coverage_ranges.jsonl]"

### EXTRA-K1-0020
- Closest oracle policies: none
- Modality: MUST (structure checker error; description length warning)
- Normative action: Skill inventory and structure: every skill directory has a SKILL.md whose frontmatter name equals the directory name and which has a description (warning above 450 characters: keep concise and trigger-first); required workflows (project-structure, verify, code-review, build-fix, custom-settings, git-workflow, security-scan, add-dependency, architecture-decision, template-maintenance) exist as Kind WF; required knowledge skills (http-api, aspnet-error-handling, logging, httpclient-factory, configuration, dependency-injection, caching, swagger, api-versioning, health-check, docker, ci-cd, modern-csharp, authentication) exist as Kind KNW; standalone serilog or resilience skills are forbidden (use a private reference of the owning knowledge skill).
- Trigger/scope: Instruction-system maintenance
- Exceptions: none stated
- Why EXTRA: Template inventory constraint; the oracle prescribes no skill inventory, naming or packaging.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:32-33` (EXTRA, K1-S000378): "const REQUIRED_WORKFLOWS = ['project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings', 'git-workflow', ⏎   'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance'];"
  - `.claude/scripts/check-instructions.cjs:34-36` (EXTRA, K1-S000379): "// Non-slot knowledge skills; slot knowledge facets are required through their contracts and manifests. ⏎ const REQUIRED_KNOWLEDGE = ['http-api', 'aspnet-error-handling', 'logging', 'httpclient-factory', 'configuration', ⏎   'dependency-injection', 'caching', 'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd', 'modern-csharp', 'authentication'];"
  - `.claude/scripts/check-instructions.cjs:37-37` (EXTRA, K1-S000380): "const FORBIDDEN_SKILLS = ['serilog', 'resilience'];"
  - `.claude/scripts/check-instructions.cjs:220-243` (EXTRA, K1-S000396): "template-maintenance must set disable-model-invocation: true"
  - `.claude/skills/template-maintenance/SKILL.md:44-44` (EXTRA, K1-S001596): "2. Skills: frontmatter `name` equal to the directory, a concise trigger-first `description` with concrete cues; WF bodies own procedure and output shape; KNW bodies own technique and point to standards for policy."

### EXTRA-K1-0021
- Closest oracle policies: none
- Modality: MUST (structure checker error)
- Normative action: Instruction references must resolve: no references to unknown skills, no unresolved or ambiguous file references; skill-private references/ files are used only by their owning skill; conformance dependencies must not form cycles.
- Trigger/scope: Instruction-system maintenance
- Exceptions: References to absent facet roles of a slot selected none are dormant, not errors.
- Why EXTRA: Referential-integrity rule of the instruction system; not a V2 policy.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:281-348` (EXTRA, K1-S000399): "references to other non-invocable files are conformance dependencies and must follow"
  - `.claude/scripts/check-instructions.cjs:787-788` (EXTRA, K1-S000417): "conformance dependency cycle"
  - `.claude/skills/template-maintenance/SKILL.md:38-38` (MIXED, K1-S001592): "Product inputs never override policy."

### EXTRA-K1-0022
- Closest oracle policies: none
- Modality: MUST (structure checker error)
- Normative action: Hook configuration: settings.json registers only and all of PreToolUse, PostToolUse, PostToolUseFailure and Stop; each hook uses exec form (command node with args [${CLAUDE_PROJECT_DIR}/.claude/hooks/dispatch.cjs, <event>]) without shell-variable expansion in command, a timeout of 1-600 seconds, and matchers covering Bash|PowerShell (PreToolUse, PostToolUseFailure) and Edit|Write|MultiEdit|Bash|PowerShell (PostToolUse); only the PreToolUse dependency/reference guard fails closed (onFailure block) and advisory hooks must not block on failure; the dispatcher must have a handler for each event.
- Trigger/scope: .claude/settings.json maintenance
- Exceptions: none stated
- Why EXTRA: Enforcement-configuration invariants of the template; no oracle policy requires hooks or their configuration.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:45-51` (EXTRA, K1-S000384): "// Required hook coverage: event -> matcher tools; the dependency/reference guard is the only fail-closed hook. ⏎ const REQUIRED_HOOKS = { ⏎   PreToolUse: { tools: ['Bash', 'PowerShell'], critical: true }, ⏎   PostToolUse: { tools: ['Edit', 'Write', 'MultiEdit', 'Bash', 'PowerShell'] }, ⏎   PostToolUseFailure: { tools: ['Bash', 'PowerShell'] }, ⏎   Stop: { tools: null }, ⏎ };"
  - `.claude/scripts/check-instructions.cjs:683-740` (EXTRA, K1-S000412): "policy-critical hook must fail closed ("onFailure": "block")"
  - `.claude/settings.json:3-16` (MIXED, K1-S000525): ""onFailure": "block""
  - `.claude/skills/template-maintenance/SKILL.md:47-47` (EXTRA, K1-S001599): "5. Hooks: exec form only (`"command": "node"`, `"args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dispatch.cjs", "<event>"]`); `${CLAUDE_PROJECT_DIR}` only locates the hook code, while every check uses the active repository or worktree derived from the hook input `cwd`. The dependency and reference guard (PreToolUse) keeps `"onFailure": "block"`; post-tool and Stop hooks stay advisory. Hook messages point to the owner instead of restating it."

### EXTRA-K1-0023
- Closest oracle policies: none
- Modality: SHOULD (structure checker warning)
- Normative action: Normative text in OP, DEC and STD artifacts avoids the ambiguous word 'normally' and uses must/default/prefer vocabulary instead.
- Trigger/scope: Authoring always-loaded and path-scoped normative text
- Exceptions: Warning only; not applied to KNW/WF artifacts.
- Why EXTRA: Authoring-vocabulary rule of the template; the oracle itself uses 'normally' in several policies and imposes no vocabulary rule.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:742-747` (EXTRA, K1-S000413): "function checkVocabulary(artifacts, out) { ⏎   for (const a of artifacts.values()) { ⏎     if (!a.header || !['OP', 'DEC', 'STD'].includes(a.header.kind)) continue; ⏎     if (/\bnormally\b/i.test(a.body)) out.push(lib.finding(WARN, a.rel, 'ambiguous "normally" in normative text; use must/default/prefer')); ⏎   } ⏎ }"

### EXTRA-K1-0024
- Closest oracle policies: none
- Modality: SHOULD (structure checker warning)
- Normative action: The always-loaded surface (CLAUDE.md, its imports, names/descriptions of model-invocable skills and agent descriptions) stays near a 5k-token target; above about 6000 estimated tokens a warning is raised.
- Trigger/scope: Instruction-system maintenance
- Exceptions: Warning only; skills with disable-model-invocation are not counted.
- Why EXTRA: Context-budget rule of the template design; not a V2 policy.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:52-52` (EXTRA, K1-S000385): "const BUDGET_WARN_TOKENS = 6000;"
  - `.claude/scripts/check-instructions.cjs:749-760` (EXTRA, K1-S000414): "function alwaysLoadedTokens(artifacts, skills, imports) { ⏎   let chars = 0; ⏎   for (const rel of ['CLAUDE.md', ...imports]) if (artifacts.get(rel)) chars += artifacts.get(rel).text.length; ⏎   for (const [name, a] of skills) { ⏎     if (frontmatterValue(a.frontmatter, 'disable-model-invocation') === 'true') continue; ⏎     chars += name.length + (frontmatterValue(a.frontmatter, 'description') || '').length + 4; ⏎   } ⏎   for (const a of artifacts.values()) { ⏎     if (a.rel.startsWith('.claude/agents/')) chars += (frontmatterValue(a.frontmatter, 'description') || '').length; ⏎   } ⏎   return Math.round(chars / 4); ⏎ }"
  - `.claude/scripts/check-instructions.cjs:793-794` (EXTRA, K1-S000419): "always-loaded surface is about ${tokens} tokens (target about 5k)"
  - `.claude/skills/template-maintenance/SKILL.md:52-52` (EXTRA, K1-S001602): "Run `node "<root>/.claude/scripts/check-instructions.cjs"` (`<root>`: the active repository root; command form in `verify`, Risk-scoped checks) and fix every error. Review the reported always-loaded size; keep it compact without moving required planning-time policy out of the always-loaded surface."

### EXTRA-K1-0025
- Closest oracle policies: DEP-020, DEP-004
- Modality: MUST NOT (manifest check error)
- Normative action: The NuGet packages Microsoft.Extensions.Http.Polly and Polly.Extensions.Http are denied as deprecated resilience integration packages (error in project files and in Directory.Packages.props).
- Trigger/scope: NuGet manifests (.csproj, Directory.Packages.props)
- Exceptions: none stated
- Why EXTRA: DEP-020 treats direct Polly integration as an explicit exception rather than a prohibition, and DEP-004 requires checking deprecation before installation but sets no fixed deny list; the candidate makes these two packages hard errors regardless of any explicit decision.
- Evidence:
  - `.claude/scripts/check-manifests.cjs:24-28` (EXTRA, K1-S000427): "deprecated resilience integration package"
  - `.claude/scripts/check-manifests.cjs:90-92` (EXTRA, K1-S000434): "const denied = NUGET_DENY.get(pkg.id.toLowerCase()); ⏎     if (denied) findings.push(lib.finding('error', rel, `"${pkg.id}": ${denied}`, OWNER_WORKFLOW)); ⏎   }"
  - `.claude/scripts/check-manifests.cjs:116-116` (EXTRA, K1-S000438): "if (NUGET_DENY.has(id)) findings.push(lib.finding('error', rel, `"${pkg.id}": ${NUGET_DENY.get(id)}`, OWNER_WORKFLOW));"
  - `.claude/skills/add-dependency/SKILL.md:23-23` (MIXED, K1-S000539): "never add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`"

### EXTRA-K1-0026
- Closest oracle policies: DEP-011, ARC-002
- Modality: MUST NOT
- Normative action: Mapster (with Mapster.DependencyInjection) is never referenced from Domain.
- Trigger/scope: Adding/using the mapping library
- Exceptions: none stated
- Why EXTRA: DEP-011 approves Mapster when mapping volume warrants it and ARC-002 keeps Domain free of EF Core, ASP.NET Core, HTTP, persistence and external-service concerns; no oracle policy forbids a mapping library in Domain.
- Evidence:
  - `.claude/skills/add-dependency/SKILL.md:24-24` (MIXED, K1-S000540): "never referenced from Domain"

### EXTRA-K1-0027
- Closest oracle policies: DEP-001, GOV-014
- Modality: MUST
- Normative action: Remove dependencies that are no longer used when doing so is part of the current change and safe to verify; do not leave dead package references behind.
- Trigger/scope: Changes that make a dependency unused
- Exceptions: Not during unrelated cleanup of a narrowly scoped task.
- Why EXTRA: No oracle policy requires removing packages made unused by a change (RUN-010 covers only unused usings in changed C# files); the candidate adds a cleanup obligation.
- Evidence:
  - `.claude/skills/add-dependency/SKILL.md:76-76` (MIXED, K1-S000556): "Remove dependencies that are no longer used when doing so is part of the current change and safe to verify; do not leave dead package references behind, and do not perform unrelated dependency cleanup during a narrowly scoped task."

### EXTRA-K1-0028
- Closest oracle policies: DEP-004, DEP-005, WF-009
- Modality: MUST
- Normative action: After a dependency change, build and run affected tests (verify) and report the package, version, license, due-diligence results and any approval obtained or pending.
- Trigger/scope: Completion of add/update/remove dependency work
- Exceptions: none stated
- Why EXTRA: WF-009 requires reporting what verification actually ran; no oracle policy requires reporting package, version, license and due-diligence outcomes for each dependency change.
- Evidence:
  - `.claude/skills/add-dependency/SKILL.md:82-82` (MIXED, K1-S000559): "Build and run the affected tests (`verify`). Report: package, version, license, due-diligence results, and any approval obtained or pending."

### EXTRA-K1-0032
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST (conditional)
- Normative action: For a consequential or non-obvious accepted decision, add a docs/decisions/NNNN-short-title.md record (context, decision, alternatives considered, consequences, date, approver).
- Trigger/scope: Consequential or non-obvious approved decisions
- Exceptions: none stated
- Why EXTRA: GOV-017 requires approval of Reserved changes and GOV-007 synchronization of approved product rules, but no oracle policy requires a separate architecture decision record with fixed content.
- Evidence:
  - `.claude/skills/architecture-decision/SKILL.md:41-41` (EXTRA, K1-S000642): "2. For a consequential or non-obvious decision, add `docs/decisions/NNNN-short-title.md` (context, decision, alternatives considered, consequences, date, approver)."

### EXTRA-K1-0033
- Closest oracle policies: GOV-017, WF-009
- Modality: MUST
- Normative action: The architecture-decision workflow reports the decision, its class, the approval source, register/record updates and any request still unresolved.
- Trigger/scope: End of an architecture-decision run
- Exceptions: none stated
- Why EXTRA: Reporting duty specific to the decision workflow; WF-009 covers verification reporting only.
- Evidence:
  - `.claude/skills/architecture-decision/SKILL.md:58-58` (EXTRA, K1-S000653): "List the decision, its class, approval source, register/record updates, and any request still unresolved."

### EXTRA-K1-0034
- Closest oracle policies: DEP-010, DEP-004, API-010
- Modality: MUST
- Normative action: Register FluentValidation validators with FluentValidation.DependencyInjectionExtensions and do not add deprecated/legacy ASP.NET automatic-validation integration packages.
- Trigger/scope: Backend validation setup
- Exceptions: Follow the project's established invocation pattern instead of adding a competing one.
- Why EXTRA: DEP-010 makes FluentValidation the standard library but prescribes no registration package; no oracle policy forbids the ASP.NET automatic-validation integration packages outright (DEP-004 only requires a deprecation check).
- Evidence:
  - `.claude/skills/aspnet-error-handling/SKILL.md:102-102` (MIXED, K1-S000673): "do not add deprecated/legacy ASP.NET automatic-validation integration packages"

### EXTRA-K1-0035
- Closest oracle policies: RUN-021, ARC-017
- Modality: MUST NOT
- Normative action: Never cache tracked persistence entities across Unit of Work boundaries.
- Trigger/scope: Caching of persistence data
- Exceptions: none stated
- Why EXTRA: RUN-021 governs invalidation consistency and ARC-017 the shared scoped context, but no oracle policy forbids caching tracked entities across Unit of Work scopes.
- Evidence:
  - `.claude/skills/caching/SKILL.md:73-73` (MIXED, K1-S000782): "Never cache tracked persistence entities across Unit of Work boundaries."

### EXTRA-K1-0036
- Closest oracle policies: GOV-021, WF-009
- Modality: MUST
- Normative action: The custom-settings report lists the setting, old -> new value, every updated surface, any migration created and the verify result.
- Trigger/scope: End of a custom-settings run
- Exceptions: none stated
- Why EXTRA: Reporting duty specific to the workflow; WF-009 requires reporting verification state only, not a per-setting surface inventory.
- Evidence:
  - `.claude/skills/custom-settings/SKILL.md:44-44` (EXTRA, K1-S000888): "List the setting, old → new value, every updated surface, migration created (if any), and the `verify` result."

### EXTRA-K1-0037
- Closest oracle policies: WF-009, GOV-017
- Modality: MUST
- Normative action: The development-workflow final report summarizes what changed and why, the verify report, approvals obtained and every unresolved Decision Request.
- Trigger/scope: End of implementation work
- Exceptions: none stated
- Why EXTRA: WF-009 requires reporting actual verification state; the duty to report the change rationale, approvals and every unresolved Decision Request is an additional reporting obligation.
- Evidence:
  - `.claude/skills/development-workflow/SKILL.md:60-60` (EXTRA, K1-S000959): "Summarize what changed and why, the `verify` report, approvals obtained, and every unresolved Decision Request."

### EXTRA-K1-0038
- Closest oracle policies: RUN-002, ARC-022
- Modality: MUST NOT
- Normative action: Never fire-and-forget EF Core asynchronous operations; a DbContext is not thread-safe.
- Trigger/scope: EF Core data access
- Exceptions: none stated
- Why EXTRA: RUN-002 forbids blocking async I/O and ARC-022 governs DI lifetimes; no oracle policy forbids un-awaited (fire-and-forget) database operations or concurrent DbContext use.
- Evidence:
  - `.claude/skills/ef-core/SKILL.md:120-120` (EXTRA, K1-S001049): "- **Never fire-and-forget** EF Core asynchronous operations; a `DbContext` is not thread-safe."

### EXTRA-K1-0039
- Closest oracle policies: RUN-016, DEP-020
- Modality: MUST NOT
- Normative action: Do not wrap normal database operations in a generic application-level retry pipeline or apply an HTTP retry policy to them; database transient faults use the persistence provider's execution strategy (EnableRetryOnFailure), with explicit transactions wrapped in the execution strategy.
- Trigger/scope: Database operations
- Exceptions: none stated
- Why EXTRA: RUN-016 limits retries to safe operations and DEP-020 sets the default resilience packages, but no oracle policy prescribes provider-level execution strategies or forbids application-level retry pipelines for database calls (the oracle treats database-retry examples as technique, EXC-007).
- Evidence:
  - `.claude/skills/ef-core/SKILL.md:221-221` (EXTRA, K1-S001069): "- Transient faults: prefer provider execution strategies (`options.UseSqlServer(cs, sql => sql.EnableRetryOnFailure())`) over generic application-level retry pipelines; with an execution strategy, wrap explicit transactions in `db.Database.CreateExecutionStrategy().ExecuteAsync(...)`. Do not apply HTTP retry policies to database operations."
  - `.claude/skills/httpclient-factory/references/resilience.md:42-42` (EXTRA, K1-S001179): "Do not wrap normal database operations in a generic application-level retry pipeline or apply an HTTP retry policy to them; use the persistence technology's provider-level transient-fault handling (persistence knowledge facet named in the decision register)."
  - `.claude/skills/httpclient-factory/references/resilience.md:58-68` (DUPLICATE, K1-S001187): "| Scenario | Default consideration | ⏎ |---|---| ⏎ | External I/O | Bound execution time | ⏎ | Safe transient HTTP failure | Consider retry | ⏎ | Unsafe write | No retry unless duplicate-safe | ⏎ | `429` from dependency | Respect `Retry-After` where appropriate | ⏎ | Repeated dependency outage | Consider circuit breaker | ⏎ | Optional data unavailable | Consider explicit fallback | ⏎ | Latency-sensitive idempoten"

### EXTRA-K1-0040
- Closest oracle policies: GOV-015
- Modality: MUST NOT
- Normative action: Treat main, master and other protected/shared branches as non-rewritable.
- Trigger/scope: Git history rewriting
- Exceptions: none stated
- Why EXTRA: GOV-015 allows force-push and other history-changing operations when explicitly requested; declaring main/master non-rewritable is stricter (read literally, even an explicit request does not unlock rewriting them).
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:35-35` (MIXED, K1-S001092): "treat `main`, `master`, and other protected/shared branches as non-rewritable"

### EXTRA-K1-0041
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: A pull request description explains what changed, why, how it was verified and compatibility/migration notes.
- Trigger/scope: Pull requests
- Exceptions: none stated
- Why EXTRA: WF-009 covers truthful verification reporting; no oracle policy fixes PR description content.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:43-43` (MIXED, K1-S001096): "its description explains what changed, why, how it was verified"

### EXTRA-K1-0042
- Closest oracle policies: RUN-005
- Modality: MUST NOT
- Normative action: Apply per-request values such as dynamic access tokens to the specific request or through a handler; never mutate a shared HttpClient's DefaultRequestHeaders concurrently.
- Trigger/scope: Outbound HttpClient usage
- Exceptions: Stable headers (media types) may be configured on the client.
- Why EXTRA: RUN-005 governs HttpClient lifetime only; no oracle policy forbids mutating shared default headers.
- Evidence:
  - `.claude/skills/httpclient-factory/SKILL.md:85-85` (MIXED, K1-S001212): "never by mutating shared `DefaultRequestHeaders` concurrently"
  - `.claude/skills/httpclient-factory/SKILL.md:99-99` (DUPLICATE, K1-S001217): "Making typed/keyed/named clients mandatory universally, infinite or poorly bounded retries, ignoring cancellation, dynamic auth tokens in shared `DefaultRequestHeaders`, mapping every upstream failure to the same status, and adding resilience pipelines without understanding their behavior."

### EXTRA-K1-0044
- Closest oracle policies: TST-007, PST-009
- Modality: MUST
- Normative action: Add or update persistence/integration tests when provider behavior, mappings, constraints or non-trivial queries changed.
- Trigger/scope: Persistence model or mapping changes
- Exceptions: none stated
- Why EXTRA: PST-009 requires updating provider-sensitive tests only for schema-affecting CUSTOM_SETTINGS changes and TST-007 governs provider fidelity, not when tests must be added; no oracle policy obliges new or updated tests for every mapping/constraint/query change.
- Evidence:
  - `.claude/skills/persistence-change/SKILL.md:46-46` (EXTRA, K1-S001337): "6. Add or update persistence/integration tests when provider behavior, mappings, constraints, or non-trivial queries changed (provider fidelity: `ef-core`, Testing)."

### EXTRA-K1-0045
- Closest oracle policies: PST-010, WF-009
- Modality: MUST
- Normative action: The persistence-change report lists model changes, migration name and review notes (destructive operations called out), seeder updates and verification results.
- Trigger/scope: End of a persistence change
- Exceptions: none stated
- Why EXTRA: WF-009 requires truthful verification reporting; reporting migration review notes and seeder updates is an extra workflow report duty.
- Evidence:
  - `.claude/skills/persistence-change/SKILL.md:54-54` (EXTRA, K1-S001341): "Model changes, migration name and review notes (destructive operations called out), seeder updates, and verification results."

### EXTRA-K1-0046
- Closest oracle policies: DEP-008
- Modality: MUST
- Normative action: The repository includes a global.json pinning the intended supported SDK line: the current stable SDK for the target .NET release (no RC/preview unless explicitly requested), with servicing allowed by the chosen rollForward policy.
- Trigger/scope: Repository scaffolding
- Exceptions: RC/preview SDK when explicitly requested.
- Why EXTRA: DEP-008 fixes the platform (.NET 10 LTS, no preview without approval) but no oracle policy requires an SDK-pinning global.json file.
- Evidence:
  - `.claude/skills/project-structure/references/solution-layout.md:48-48` (MIXED, K1-S001389): "pin the intended supported SDK line"

### EXTRA-K1-0047
- Closest oracle policies: none
- Modality: MUST (vocabulary semantics, always loaded)
- Normative action: Normative vocabulary: must / must not — a violation is a defect; Default — deviation needs a concrete reason and must be reported; Prefer / avoid — guidance; Requires approval — a Reserved decision.
- Trigger/scope: All normative text and all deviations from Default rules
- Exceptions: none stated
- Why EXTRA: The oracle grades policies (MUST, DEFAULT, REQUIRES_APPROVAL) but defines no duty to report every deviation from a Default; the reporting duty and the 'defect' classification change how all Default rules bind.
- Evidence:
  - `.claude/skills/template-maintenance/SKILL.md:36-36` (EXTRA, K1-S001590): "- Vocabulary: must / must not, Default, prefer / avoid, requires approval (`CLAUDE.md`)."
  - `CLAUDE.md:11-11` (EXTRA, K1-S001646): "**must / must not** — a violation is a defect. **Default** — deviation needs a concrete reason and must be reported. **Prefer / avoid** — guidance. **Requires approval** — a Reserved decision (see Decision control)."

### EXTRA-K1-0048
- Closest oracle policies: GOV-017, ARC-020
- Modality: MUST (classification test)
- Normative action: Unclear decisions are Reserved if any answer is yes: (1) adds, removes or replaces a dependency, framework or infrastructure capability; (2) changes a project/layer/reference boundary; (3) establishes a convention other code is expected to follow; (4) changes observable behavior or a public contract; (5) would be expensive to reverse after other code depends on it.
- Trigger/scope: Unclear decision cases
- Exceptions: Routine local decisions already constrained by the specification, register, existing code or standards are not escalated.
- Why EXTRA: GOV-017 requires a Decided/Delegated/Reserved classification and ARC-020 lists consequential choices, but neither defines this five-question test; question 1 alone makes any dependency addition/removal or replacement in an unclear case approval-gated, which DEP-001..DEP-005 do not.
- Evidence:
  - `CLAUDE.md:43-43` (EXTRA, K1-S001671): "- Unclear case — any "yes" makes it Reserved: (1) Does it add, remove, or replace a dependency, framework, or infrastructure capability? (2) Does it change a project/layer/reference boundary? (3) Does it establish a convention other code is expected to follow? (4) Does it change observable behavior or a public contract? (5) Would it be expensive to reverse after other code depends on it?"

### EXTRA-K1-0049
- Closest oracle policies: DEP-023, RUN-009
- Modality: DEFAULT (effective MSBuild default)
- Normative action: Shared build configuration enables Nullable reference types and ImplicitUsings for every .NET project below the repository root.
- Trigger/scope: .NET projects
- Exceptions: Projects may override in their own files.
- Why EXTRA: DEP-023 says where shared settings live but no oracle policy chooses nullable reference types or implicit usings; the template makes both effective defaults for all projects.
- Evidence:
  - `Directory.Build.props:7-8` (EXTRA, K1-S001694): "<Nullable>enable</Nullable> ⏎     <ImplicitUsings>enable</ImplicitUsings>"

## LINK_UNCERTAIN (3)

### UNCERTAIN-K1-0002
- Closest oracle policies: DEP-002, DEP-001, ARC-020
- Modality: MUST (workflow checklist)
- Normative action: Before adding a dependency, the choice must match the decision register's approved stack; anything else goes through architecture-decision first.
- Trigger/scope: Every NuGet/npm addition via add-dependency
- Exceptions: none stated
- Open question: Open question: if 'anything else' covers any package not named in the register (e.g. a small utility library for a concern with no approved technology), the clause makes every non-stack dependency a Reserved decision, which is stricter than DEP-001/DEP-002 (need-based additions are allowed; only silent replacement of an approved technology needs approval). If it only means alternatives to an approved technology, it restates DEP-002. The text does not settle which reading applies.
- Evidence:
  - `.claude/skills/add-dependency/SKILL.md:20-20` (MIXED, K1-S000536): "anything else goes through `architecture-decision` first"

### UNCERTAIN-K1-0003
- Closest oracle policies: GOV-015
- Modality: MAY (exception)
- Normative action: High-risk Git operations may be performed when 'clearly required by an approved workflow', not only when explicitly requested.
- Trigger/scope: High-risk Git operations
- Exceptions: none stated
- Open question: Open question: GOV-015 permits repository-changing Git operations only when explicitly requested; whether 'clearly required by an approved workflow' merely refers to a workflow the user explicitly requested (entailed) or lets a workflow trigger destructive operations without a specific request (a relaxation) is not determinable from the text.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:19-19` (MIXED, K1-S001084): "or clearly required by an approved workflow"

### UNCERTAIN-K1-0004
- Closest oracle policies: GOV-015, DEP-007
- Modality: MUST (scaffolding step)
- Normative action: Frontend scaffolding ends with 'Verify with the workspace's declared scripts ... and commit package-lock.json'.
- Trigger/scope: Frontend workspace creation
- Exceptions: none stated
- Open question: Open question: if 'commit package-lock.json' instructs the agent to run git commit during scaffolding, it conflicts with GOV-015 (repository-changing Git operations only on explicit request); if it only means the lockfile must be tracked in version control (as in rules/frontend/dependencies.md), it restates DEP-007. The imperative step wording does not settle which.
- Evidence:
  - `.claude/skills/project-structure/references/frontend-setup.md:18-18` (MIXED, K1-S001374): "commit `package-lock.json`"

