# EXTRA and LINK_UNCERTAIN constraints — candidate L1

Generated deterministically from the annotation ledger. Each entry cites the exact
source evidence (path, line range, verbatim quote). `policy_ids` on an EXTRA entry
name the closest oracle policy only; origin stays EXTRA.

## EXTRA constraints (233)

### EXTRA-L1-0001
- Closest oracle policies: GOV-001, GOV-008
- Modality: MUST_NOT
- Normative action: SPECIFICATION.md, CUSTOM_SETTINGS.md, feature specifications and task prompts are inputs, not instruction layers; they may request a decision change but never silently override engineering policy.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Product-input vs engineering-policy precedence not stated in the oracle.
- Evidence L1-S000423: `output/template/CLAUDE.md:15-15` — "`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specifications, and task prompts are inputs, not instruction layers. They may request a decision change; they never silently override engineering policy."

### EXTRA-L1-0002
- Closest oracle policies: ARC-020, ARC-001
- Modality: REQUIRES_APPROVAL
- Normative action: Changing the project reference graph is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Not gated by ARC-020.
- Evidence L1-S000438: `output/template/CLAUDE.md:35-35` — "- **Reserved** — requires approval: changing an accepted project/architecture decision; adopting a new architectural style or pattern (Rich Domain Model or DDD tactical patterns, CQRS, mediator-based organization, Vertical Slice Architecture, event sourcing, a project-wide Result model, microservices); adding a production project/layer or changing the project reference graph; changing persistence  …"

### EXTRA-L1-0003
- Closest oracle policies: ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Adding search, external storage or external identity infrastructure is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Beyond ARC-020's list.
- Evidence L1-S000438: `output/template/CLAUDE.md:35-35` — "- **Reserved** — requires approval: changing an accepted project/architecture decision; adopting a new architectural style or pattern (Rich Domain Model or DDD tactical patterns, CQRS, mediator-based organization, Vertical Slice Architecture, event sourcing, a project-wide Result model, microservices); adding a production project/layer or changing the project reference graph; changing persistence  …"

### EXTRA-L1-0004
- Closest oracle policies: DEP-001, GOV-013
- Modality: REQUIRES_APPROVAL
- Normative action: Adding a major library/framework is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: The oracle requires current need, not approval.
- Evidence L1-S000438: `output/template/CLAUDE.md:35-35` — "- **Reserved** — requires approval: changing an accepted project/architecture decision; adopting a new architectural style or pattern (Rich Domain Model or DDD tactical patterns, CQRS, mediator-based organization, Vertical Slice Architecture, event sourcing, a project-wide Result model, microservices); adding a production project/layer or changing the project reference graph; changing persistence  …"
- Evidence L1-S000663: `output/template/.claude/skills/add-dependency/SKILL.md:14-14` — "State the concrete current requirement. Use the approved technology when one exists; replacing an approved technology or adding a major library is Reserved. Conditional technologies (decisions file) are added only when their capability is needed; package choices:"

### EXTRA-L1-0005
- Closest oracle policies: ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Introducing any project-wide convention or abstraction is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Generalizes ARC-020's Result example.
- Evidence L1-S000438: `output/template/CLAUDE.md:35-35` — "- **Reserved** — requires approval: changing an accepted project/architecture decision; adopting a new architectural style or pattern (Rich Domain Model or DDD tactical patterns, CQRS, mediator-based organization, Vertical Slice Architecture, event sourcing, a project-wide Result model, microservices); adding a production project/layer or changing the project reference graph; changing persistence  …"

### EXTRA-L1-0006
- Closest oracle policies: API-013, DEP-017
- Modality: REQUIRES_APPROVAL
- Normative action: Adopting API versioning is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: API-013 requires a concrete need, not approval.
- Evidence L1-S000438: `output/template/CLAUDE.md:35-35` — "- **Reserved** — requires approval: changing an accepted project/architecture decision; adopting a new architectural style or pattern (Rich Domain Model or DDD tactical patterns, CQRS, mediator-based organization, Vertical Slice Architecture, event sourcing, a project-wide Result model, microservices); adding a production project/layer or changing the project reference graph; changing persistence  …"

### EXTRA-L1-0007
- Closest oracle policies: ARC-020, DEP-002
- Modality: REQUIRES_APPROVAL
- Normative action: Changing a capability selection is Reserved and also requires an ADR (recorded with architecture-decision).
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Capability-selection gate and ADR obligation not in the oracle.
- Evidence L1-S000104: `output/template/.claude/INSTRUCTION_MAP.md:127-127` — "Selection record: `.claude/rules/3-project/decisions.md` § Capability selection (the only place outside modules that names implementations, besides this map). Changing a selection is Reserved and needs an ADR (`architecture-decision`)."
- Evidence L1-S000351: `output/template/.claude/rules/3-project/decisions.md:10-10` — "When an approved technology exists here, use it rather than silently selecting an alternative; replacing it, or changing a capability selection, is Reserved (CLAUDE.md decision control; record with `architecture-decision`)."
- Evidence L1-S000438: `output/template/CLAUDE.md:35-35` — "- **Reserved** — requires approval: changing an accepted project/architecture decision; adopting a new architectural style or pattern (Rich Domain Model or DDD tactical patterns, CQRS, mediator-based organization, Vertical Slice Architecture, event sourcing, a project-wide Result model, microservices); adding a production project/layer or changing the project reference graph; changing persistence  …"
- Evidence L1-S000517: `output/template/.claude/capabilities/architecture/CONTRACT.md:24-24` — "Changing the frame is Reserved and requires an ADR (`architecture-decision`). A replacement module supplies every facet above, updates the selection record and the `CLAUDE.md` import of its style facet, and passes `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"`."
- Evidence L1-S000525: `output/template/.claude/capabilities/backend-testing/CONTRACT.md:18-18` — "Replacing the framework (for example with another .NET test framework) replaces this module: new rule facet, commands, enforcement data, knowledge content, and the selection-record row. Workflows refer only to `backend-testing.*` facets and need no edits. Changing the selection is Reserved and requires an ADR."
- Evidence L1-S000572: `output/template/.claude/capabilities/frontend/CONTRACT.md:19-19` — "Clearing the optional selection removes the frontend without hunting: set the selection row to `none`, delete the files listed in the module manifest, remove the `frontend-stack.md` import line from `CLAUDE.md`, remove the module's rows from `.claude/INSTRUCTION_MAP.md`, then run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"`. Neutral rules stay; they only load fo …"
- Evidence L1-S000757: `output/template/.claude/skills/architecture-decision/SKILL.md:47-47` — "Changing a slot implementation (or clearing the optional frontend) always needs an ADR. Then: replace or remove the module per its slot contract and manifest (`.claude/capabilities/<slot>/`), update the selection row and declared properties, update the `CLAUDE.md` import if an always-loaded facet changed, and run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"`. A c …"

### EXTRA-L1-0008
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST
- Normative action: An explicit user instruction counts as approval; the accepted decision must be recorded with architecture-decision.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Recording obligation added to GOV-017.
- Evidence L1-S000441: `output/template/CLAUDE.md:38-38` — "- An explicit user instruction counts as approval; record the accepted decision with `architecture-decision`. In autonomous/headless runs, take only a policy-compliant non-Reserved path and report unresolved Decision Requests explicitly."

### EXTRA-L1-0009
- Closest oracle policies: DEP-023, RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: Shared build settings Nullable enable and ImplicitUsings enable.
- Trigger/scope: all .NET projects (MSBuild import)
- Exceptions: none
- Why EXTRA: Concrete compiler settings not in the oracle.
- Evidence L1-S000459: `output/template/Directory.Build.props:5-6` — "<Nullable>enable</Nullable> ⏎     <ImplicitUsings>enable</ImplicitUsings>"

### EXTRA-L1-0010
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Conformance dependencies point only to the same or a more stable level (0-core → 1-architecture → 2-technology → 3-project).
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Instruction-architecture invariant (repo/meta), checked by check-instructions.mjs.
- Evidence L1-S000084: `output/template/.claude/INSTRUCTION_MAP.md:7-7` — "1. **Where does it belong by stability?** → Level: `0-core` (operating policy, technology-neutral principles) → `1-architecture` (role vocabulary, boundaries) → `2-technology` (concrete technique and bindings) → `3-project` (selection, defaults, layout). Conformance dependencies point only to the same or a more stable level; Core and Architecture name no concrete implementation technology in any f …"
- Evidence L1-S000646: `output/template/.claude/scripts/check-instructions.mjs:378-395` — "// Conformance direction: a rule may depend only on rules/facets of the same or a more stable level. ⏎   // The only exempt reverse form is a binding pointer ("Framework binding: `<slot>.<facet>` ..."). ⏎   const facetLevel = new Map(modules.flatMap((m) => m.facets.map((f) => [f.facet, LEVELS.indexOf(f.level)]))); ⏎   for (const [p, d] of docs) { ⏎     if (!p.startsWith('.claude/rules/') || !d.hea …"

### EXTRA-L1-0011
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Core and Architecture name no concrete implementation technology in any form, pure pointers included; fixed vocabulary is .NET, C#, TypeScript, Git and HTTP; Level 2 is referenced only by role, capability, facet or technology-neutral skill name.
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta invariant, checked by check-instructions.mjs.
- Evidence L1-S000084: `output/template/.claude/INSTRUCTION_MAP.md:7-7` — "1. **Where does it belong by stability?** → Level: `0-core` (operating policy, technology-neutral principles) → `1-architecture` (role vocabulary, boundaries) → `2-technology` (concrete technique and bindings) → `3-project` (selection, defaults, layout). Conformance dependencies point only to the same or a more stable level; Core and Architecture name no concrete implementation technology in any f …"
- Evidence L1-S000632: `output/template/.claude/scripts/check-instructions.mjs:21-40` — "// Core/Architecture neutrality: Levels 0/1 name no concrete implementation technology in any form, from prose to ⏎ // a pure pointer (heading, list, table row, code span or fence, link, frontmatter, or wrapper such as ⏎ // `Technique: <skill>`, `See <skill>`, `area → <skill>`). There is no pointer or context exemption. Fixed platform ⏎ // (allowed): .NET, C#, TypeScript, Git, and HTTP as protocol …"
- Evidence L1-S000637: `output/template/.claude/scripts/check-instructions.mjs:187-216` — "function neutralityCheck(p, d, ctx) { ⏎   const blocks = parseBlocks(d.body); ⏎   const description = (d.fm.match(/^description:\s*(.+)$/m) || [])[1]; ⏎   if (description) blocks.push({ type: 'para', text: description, headings: [], ancestors: [] }); ⏎   const reported = new Set(); ⏎   const report = (token, why) => { ⏎     const key = token.toLowerCase(); ⏎     if (reported.has(key)) return; ⏎    …"
- Evidence L1-S000649: `output/template/.claude/scripts/check-instructions.mjs:420-456` — "// Core and Architecture neutrality (no pointer exemption; fixed platform only). ⏎   const skillsDir = path.join(claude, 'skills'); ⏎   const skills = existsSync(skillsDir) ? readdirSync(skillsDir).filter((e) => existsSync(path.join(skillsDir, e, 'SKILL.md'))) : []; ⏎   const techSkills = new Set(skills.filter((s) => { const d = docs.get(`.claude/skills/${s}/SKILL.md`); return d && d.header && d.h …"
- Evidence L1-S001502: `output/template/.claude/skills/template-maintenance/SKILL.md:16-16` — "2. **Level** (first match wins): project-specific selection, layout, or default → `3-project`; concrete non-platform technology → `2-technology`; adopted architecture, role, or boundary → `1-architecture`; otherwise → `0-core`. Core and Architecture name no concrete technology — not even in a pointer to a Level-2 skill — beyond the fixed platform vocabulary (.NET, C#, TypeScript, Git; HTTP as prot …"

### EXTRA-L1-0012
- Closest oracle policies: none
- Modality: MUST
- Normative action: Place content by stability: operating policy/neutral principles in 0-core, role vocabulary/boundaries in 1-architecture, concrete technique/bindings in 2-technology, selection/defaults/layout in 3-project.
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta placement rule.
- Evidence L1-S000084: `output/template/.claude/INSTRUCTION_MAP.md:7-7` — "1. **Where does it belong by stability?** → Level: `0-core` (operating policy, technology-neutral principles) → `1-architecture` (role vocabulary, boundaries) → `2-technology` (concrete technique and bindings) → `3-project` (selection, defaults, layout). Conformance dependencies point only to the same or a more stable level; Core and Architecture name no concrete implementation technology in any f …"
- Evidence L1-S001502: `output/template/.claude/skills/template-maintenance/SKILL.md:16-16` — "2. **Level** (first match wins): project-specific selection, layout, or default → `3-project`; concrete non-platform technology → `2-technology`; adopted architecture, role, or boundary → `1-architecture`; otherwise → `0-core`. Core and Architecture name no concrete technology — not even in a pointer to a Level-2 skill — beyond the fixed platform vocabulary (.NET, C#, TypeScript, Git; HTTP as prot …"

### EXTRA-L1-0013
- Closest oracle policies: none
- Modality: MUST
- Normative action: Only four replaceable capability slots exist (architecture frame, persistence, backend-testing, optional frontend); module-owned artifacts declare Capability and appear in their MODULE.md.
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Capability-system rule (repo/meta).
- Evidence L1-S000085: `output/template/.claude/INSTRUCTION_MAP.md:8-8` — "2. **Can it be replaced as one module?** → Capability: only the four slots `architecture` (frame), `persistence`, `backend-testing`, `frontend` (optional). Module-owned artifacts declare `Capability:` and appear in their `MODULE.md`."
- Evidence L1-S000629: `output/template/.claude/scripts/check-instructions.mjs:13-14` — "const LEVELS = ['0-core', '1-architecture', '2-technology', '3-project']; ⏎ const SLOTS = { architecture: 'required frame', persistence: 'required leaf', 'backend-testing': 'required leaf', frontend: 'optional leaf' };"
- Evidence L1-S000640: `output/template/.claude/scripts/check-instructions.mjs:246-276` — "// Selection record, slot directories, slot contracts. ⏎   const selection = parseSelection(root); ⏎   const selected = {}; ⏎   const capDir = path.join(claude, 'capabilities'); ⏎   const slotDirs = existsSync(capDir) ? readdirSync(capDir).filter((e) => statSync(path.join(capDir, e)).isDirectory()) : []; ⏎   for (const dir of slotDirs) if (!(dir in SLOTS)) fail(`.claude/capabilities/${dir}`, `unkn …"

### EXTRA-L1-0014
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Each artifact starts with a one-line header (Level, optional Capability/Facet, Owns, Scope, Loading).
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta invariant.
- Evidence L1-S000086: `output/template/.claude/INSTRUCTION_MAP.md:10-10` — "Product inputs (`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specs, task prompts) sit outside the hierarchy. Each artifact starts with a one-line header (`Level`, optional `Capability`/`Facet`, `Owns`, `Scope`, `Loading`). Run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"` after any change (works from nested directories and linked worktrees)."
- Evidence L1-S000639: `output/template/.claude/scripts/check-instructions.mjs:237-244` — "// Headers. ⏎   for (const [p, d] of docs) { ⏎     if (!d.header) { fail(p, 'missing one-line header starting with "> Level: "'); continue; } ⏎     if (!LEVELS.includes(d.header.Level)) fail(p, `unknown Level '${d.header.Level}'`); ⏎     if (!d.header.Owns) fail(p, 'header lacks "Owns:"'); ⏎     if (!d.header.Loading) fail(p, 'header lacks "Loading:"'); ⏎     if ('Kind' in d.header) fail(p, 'heade …"
- Evidence L1-S001507: `output/template/.claude/skills/template-maintenance/SKILL.md:23-23` — "1. Draft the change and place it with the decision list above; keep the header line (`Level`, `Capability` when module-owned, `Owns`, `Scope`, `Loading`)."

### EXTRA-L1-0015
- Closest oracle policies: none
- Modality: MUST
- Normative action: Run check-instructions.mjs after any instruction-system change.
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta rule.
- Evidence L1-S000086: `output/template/.claude/INSTRUCTION_MAP.md:10-10` — "Product inputs (`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specs, task prompts) sit outside the hierarchy. Each artifact starts with a one-line header (`Level`, optional `Capability`/`Facet`, `Owns`, `Scope`, `Loading`). Run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"` after any change (works from nested directories and linked worktrees)."
- Evidence L1-S001510: `output/template/.claude/skills/template-maintenance/SKILL.md:26-26` — "4. Run the checker and fix every reported item:"

### EXTRA-L1-0016
- Closest oracle policies: none
- Modality: MUST_NOT
- Normative action: Outside modules, implementations are named only in the capability selection record of decisions.md (and the map).
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Capability-system rule (repo/meta).
- Evidence L1-S000104: `output/template/.claude/INSTRUCTION_MAP.md:127-127` — "Selection record: `.claude/rules/3-project/decisions.md` § Capability selection (the only place outside modules that names implementations, besides this map). Changing a selection is Reserved and needs an ADR (`architecture-decision`)."
- Evidence L1-S000648: `output/template/.claude/scripts/check-instructions.mjs:408-418` — "// Implementation-name leakage (case-insensitive). ⏎   for (const [p, d] of docs) { ⏎     if (LEAK_ALLOWED.has(p)) continue; ⏎     const owner = ownerOf(p); ⏎     for (const m of modules) { ⏎       if (owner === m) continue; ⏎       for (const token of m.tokens) { ⏎         if (wordRe(token).test(d.body)) fail(p, `names '${token}' from module ${m.capability}; use slot/facet/role vocabulary or move …"

### EXTRA-L1-0017
- Closest oracle policies: none
- Modality: MUST
- Normative action: Static composition: each required slot has exactly one selected implementation, the optional slot zero or one; only selected modules ship.
- Trigger/scope: always (imported); paths **/*
- Exceptions: none
- Why EXTRA: Capability-system rule (repo/meta).
- Evidence L1-S000363: `output/template/.claude/rules/3-project/decisions.md:28-28` — "Static composition: each required slot has exactly one selected implementation, the optional slot zero or one; only selected modules ship."
- Evidence L1-S000640: `output/template/.claude/scripts/check-instructions.mjs:246-276` — "// Selection record, slot directories, slot contracts. ⏎   const selection = parseSelection(root); ⏎   const selected = {}; ⏎   const capDir = path.join(claude, 'capabilities'); ⏎   const slotDirs = existsSync(capDir) ? readdirSync(capDir).filter((e) => statSync(path.join(capDir, e)).isDirectory()) : []; ⏎   for (const dir of slotDirs) if (!(dir in SLOTS)) fail(`.claude/capabilities/${dir}`, `unkn …"

### EXTRA-L1-0034
- Closest oracle policies: none
- Modality: MUST
- Normative action: The frame maps the role vocabulary to projects and owns placement; leaf slots depend on roles, not frame terms; placement belongs to the frame, technique to the leaf.
- Trigger/scope: repo/meta (capability maintenance)
- Exceptions: none
- Why EXTRA: Capability-system rule (repo/meta).
- Evidence L1-S000510: `output/template/.claude/capabilities/architecture/CONTRACT.md:5-5` — "The architecture slot is a **frame**: it maps the stable role vocabulary (`.claude/rules/1-architecture/roles.md`, outside every module) to concrete projects and owns placement. Leaf slots depend on roles, not on frame terms. Placement belongs to the frame; technique belongs to the leaf."
- Evidence L1-S000575: `output/template/.claude/capabilities/persistence/CONTRACT.md:5-5` — "Covers more than the ORM name: access and commit-boundary binding, migrations, seeding, provider variant, observable string-comparison defaults, relational testing expectations, and implementation-specific workflow and enforcement. Placement comes from the architecture frame; this slot supplies technique."

### EXTRA-L1-0035
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Each slot contract lists required facets (form, level, loading, content) that the selected module must provide; checked by check-instructions.mjs.
- Trigger/scope: repo/meta (capability maintenance)
- Exceptions: none
- Why EXTRA: Capability-system invariant (repo/meta).
- Evidence L1-S000513: `output/template/.claude/capabilities/architecture/CONTRACT.md:11-14` — "| `architecture.style` | rule | 1 | always (imported by `CLAUDE.md`) | adopted style, role → project mapping, patterns not adopted | ⏎ | `architecture.boundaries` | rule | 1 | path: backend | dependency direction, layer responsibilities, placement of persistence-access contracts and commit boundary, composition root, test-project references | ⏎ | `architecture.layout` | workflow-read reference | 1 …"
- Evidence L1-S000523: `output/template/.claude/capabilities/backend-testing/CONTRACT.md:11-14` — "| `backend-testing.framework` | rule | 2 | path: backend-tests | framework selection rule and bindings of neutral rules to framework constructs | ⏎ | `backend-testing.commands` | workflow-read reference | 2 | read by workflows | test-project scaffold packages and commands, test run/filter commands | ⏎ | `backend-testing.enforcement` | enforcement data (JSON) | 2 | scripts | adapter for neutral arc …"
- Evidence L1-S000570: `output/template/.claude/capabilities/frontend/CONTRACT.md:11-15` — "| `frontend.framework` | rule | 2 | path: frontend | framework-specific rules | ⏎ | `frontend.stack` | rule | 3 | always (imported by `CLAUDE.md`) | selected frontend technology decisions and approved optional libraries | ⏎ | `frontend.commands` | workflow-read reference | 2 | read by workflows | scaffold, clean install, build, test, lint, audit commands, build-fix notes | ⏎ | `frontend.enforcemen …"
- Evidence L1-S000578: `output/template/.claude/capabilities/persistence/CONTRACT.md:11-17` — "| `persistence.access` | rule | 2 | path: backend | confinement of the implementation, repository-contract leak rule, bindings for persistence context, commit boundary, relational fidelity | ⏎ | `persistence.seeding` | rule | 2 | path: backend | Development seeding mechanism and constraints | ⏎ | `persistence.dev-config` | rule | 3 | path: backend | local Development connection default | ⏎ | `pers …"
- Evidence L1-S000640: `output/template/.claude/scripts/check-instructions.mjs:246-276` — "// Selection record, slot directories, slot contracts. ⏎   const selection = parseSelection(root); ⏎   const selected = {}; ⏎   const capDir = path.join(claude, 'capabilities'); ⏎   const slotDirs = existsSync(capDir) ? readdirSync(capDir).filter((e) => statSync(path.join(capDir, e)).isDirectory()) : []; ⏎   for (const dir of slotDirs) if (!(dir in SLOTS)) fail(`.claude/capabilities/${dir}`, `unkn …"
- Evidence L1-S000641: `output/template/.claude/scripts/check-instructions.mjs:278-316` — "// Module manifests. ⏎   const modules = []; ⏎   for (const [slot, impl] of Object.entries(selected)) { ⏎     if (!impl) continue; ⏎     const manifestPath = `.claude/capabilities/${slot}/${impl}/MODULE.md`; ⏎     const doc = docs.get(manifestPath); ⏎     if (!doc) { fail(manifestPath, 'missing module manifest'); continue; } ⏎     const capability = `${slot}/${impl}`; ⏎     const line = (key) => ( …"

### EXTRA-L1-0036
- Closest oracle policies: none
- Modality: MUST
- Normative action: The frame expresses every role in roles.md without contradicting role-level rules, keeps leaf technology out of frame facets, and leaf bindings not expressible through roles are declared as binds in the leaf manifest.
- Trigger/scope: repo/meta (capability maintenance)
- Exceptions: none
- Why EXTRA: Capability-system rule (repo/meta).
- Evidence L1-S000515: `output/template/.claude/capabilities/architecture/CONTRACT.md:18-20` — "- Express every role in `roles.md`; never contradict a role-level rule. ⏎ - Keep leaf technology out of frame facets (refer to persistence-implementation types generically; the persistence module binds them). ⏎ - Leaf bindings that cannot be expressed through roles must be declared by the leaf as `binds:` in its manifest."

### EXTRA-L1-0037
- Closest oracle policies: ARC-020
- Modality: MUST
- Normative action: A replacement module supplies every required facet, updates the selection record (and the CLAUDE.md import of a style/stack facet) and passes check-instructions.mjs; workflows refer only to slot facets.
- Trigger/scope: repo/meta (capability maintenance)
- Exceptions: Module replacement.
- Why EXTRA: Capability replacement procedure (repo/meta).
- Evidence L1-S000507: `output/template/.claude/capabilities/architecture/clean-architecture/MODULE.md:23-23` — "Replace all four facets together, keep `.claude/rules/1-architecture/roles.md` unchanged unless the role vocabulary itself changes (Reserved), and update the selection record row."
- Evidence L1-S000517: `output/template/.claude/capabilities/architecture/CONTRACT.md:24-24` — "Changing the frame is Reserved and requires an ADR (`architecture-decision`). A replacement module supplies every facet above, updates the selection record and the `CLAUDE.md` import of its style facet, and passes `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"`."
- Evidence L1-S000525: `output/template/.claude/capabilities/backend-testing/CONTRACT.md:18-18` — "Replacing the framework (for example with another .NET test framework) replaces this module: new rule facet, commands, enforcement data, knowledge content, and the selection-record row. Workflows refer only to `backend-testing.*` facets and need no edits. Changing the selection is Reserved and requires an ADR."
- Evidence L1-S000757: `output/template/.claude/skills/architecture-decision/SKILL.md:47-47` — "Changing a slot implementation (or clearing the optional frontend) always needs an ADR. Then: replace or remove the module per its slot contract and manifest (`.claude/capabilities/<slot>/`), update the selection row and declared properties, update the `CLAUDE.md` import if an always-loaded facet changed, and run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"`. A c …"

### EXTRA-L1-0038
- Closest oracle policies: ARC-027, DEP-024
- Modality: DEFAULT
- Normative action: Folder roles: Application Abstractions/Persistence (no persistence-implementation types), Abstractions/ExternalServices (only once dependencies exist), Services, DTOs (not a dumping ground), Validation; Infrastructure Persistence/{Configurations,Repositories,Migrations,Seeding}, Services; Api entry-point folder, Contracts/Requests|Responses, Middleware, Extensions.
- Trigger/scope: workflow-read facet architecture.layout (scaffolding and placement)
- Exceptions: Only when needed.
- Why EXTRA: Layout convention not in the oracle.
- Evidence L1-S000483: `output/template/.claude/capabilities/architecture/clean-architecture/layout.md:31-40` — "```text ⏎ <Name>.Application/ ⏎ ├── Abstractions/ ⏎ │   ├── Persistence/        # repository interfaces, IUnitOfWork — no persistence-implementation types ⏎ │   └── ExternalServices/   # IEmailSender, ICurrentUser, IFileStorage ... only once such dependencies exist ⏎ ├── Services/               # Application Services (ITaskService, TaskService) ⏎ ├── DTOs/                   # operation/data models …"
- Evidence L1-S000486: `output/template/.claude/capabilities/architecture/clean-architecture/layout.md:46-56` — "```text ⏎ <Name>.Infrastructure/ ⏎ ├── Persistence/ ⏎ │   ├── <persistence context and commit-boundary implementation> ⏎ │   ├── Configurations/     # entity mappings ⏎ │   ├── Repositories/       # concrete repositories (optional internal generic base) ⏎ │   ├── Migrations/ ⏎ │   └── Seeding/            # Development seeding (persistence.seeding) ⏎ ├── Services/               # implementations of …"
- Evidence L1-S000489: `output/template/.claude/capabilities/architecture/clean-architecture/layout.md:62-73` — "```text ⏎ <Name>.Api/ ⏎ ├── <entry-point adapters>/   # folder named by the entry-point mechanism (backend platform binding) ⏎ ├── Contracts/ ⏎ │   ├── Requests/ ⏎ │   └── Responses/ ⏎ ├── Middleware/             # only when custom middleware exists ⏎ ├── Extensions/             # cohesive composition extensions; not merely to shorten Program.cs ⏎ ├── Program.cs ⏎ ├── appsettings.json ⏎ └── appset …"

### EXTRA-L1-0039
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Supporting-type roles clear from name/directory using suffixes (Service, Dto, Request/Response — HTTP contracts in Api, Result/Outcome, Validator, Rules/Policy, Factory, Mapper, Adapter); prefer unambiguous names; responsibility subdirectories only for many heterogeneous types.
- Trigger/scope: workflow-read facet architecture.layout (scaffolding and placement)
- Exceptions: none
- Why EXTRA: Naming heuristics not in the oracle.
- Evidence L1-S000484: `output/template/.claude/capabilities/architecture/clean-architecture/layout.md:42-42` — "Supporting type roles should be clear from the type name, its directory, or both. Useful suffixes: `Service` (use-case orchestration), `Dto`, `Request`/`Response` (Application operation contracts; HTTP contracts belong to Api), `Result`/`Outcome`, `Validator`, `Rules`/`Policy` (decision or workflow rules), `Factory`, `Mapper`, `Adapter`. Prefer `TaskWorkflowRules` or `TaskWorkflowService` over an  …"

### EXTRA-L1-0040
- Closest oracle policies: ARC-027
- Modality: DEFAULT
- Normative action: Create capability-specific subdirectories under Infrastructure Services/ when they improve cohesion.
- Trigger/scope: workflow-read facet architecture.layout (scaffolding and placement)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000487: `output/template/.claude/capabilities/architecture/clean-architecture/layout.md:58-58` — "Create capability-specific subdirectories under `Services/` when they improve cohesion."

### EXTRA-L1-0041
- Closest oracle policies: ARC-012
- Modality: MUST_NOT
- Normative action: Extensions/ holds cohesive composition extensions, not code moved merely to shorten Program.cs.
- Trigger/scope: workflow-read facet architecture.layout (scaffolding and placement)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000489: `output/template/.claude/capabilities/architecture/clean-architecture/layout.md:62-73` — "```text ⏎ <Name>.Api/ ⏎ ├── <entry-point adapters>/   # folder named by the entry-point mechanism (backend platform binding) ⏎ ├── Contracts/ ⏎ │   ├── Requests/ ⏎ │   └── Responses/ ⏎ ├── Middleware/             # only when custom middleware exists ⏎ ├── Extensions/             # cohesive composition extensions; not merely to shorten Program.cs ⏎ ├── Program.cs ⏎ ├── appsettings.json ⏎ └── appset …"

### EXTRA-L1-0042
- Closest oracle policies: GOV-006, PST-010
- Modality: MUST
- Normative action: The selection record declares provider variant, default string-comparison/case-sensitivity semantics, migration mechanism and seeding mechanism for the persistence slot.
- Trigger/scope: repo/meta (capability maintenance)
- Exceptions: none
- Why EXTRA: Capability-system rule (repo/meta).
- Evidence L1-S000580: `output/template/.claude/capabilities/persistence/CONTRACT.md:21-21` — "Provider variant, default string-comparison/case-sensitivity semantics, migration mechanism, seeding mechanism."

### EXTRA-L1-0043
- Closest oracle policies: none
- Modality: MUST
- Normative action: The selected persistence module declares binds to the selected frame because its commands name frame projects.
- Trigger/scope: repo/meta (capability maintenance)
- Exceptions: none
- Why EXTRA: Capability-system rule (repo/meta).
- Evidence L1-S000582: `output/template/.claude/capabilities/persistence/CONTRACT.md:25-25` — "- requires-binds: architecture — migration and startup commands need the frame's implementation-layer and entry-point projects, so the selected module declares `binds:` to the selected frame."
- Evidence L1-S000643: `output/template/.claude/scripts/check-instructions.mjs:321-356` — "// Binds: the frame binds nothing; a leaf binds only the selected frame, with a reason; required when the ⏎   // contract says so or when the module's content uses frame-specific vocabulary. ⏎   // Project-name segments come from the frame's own check specification (role project patterns). ⏎   const frameSegments = []; ⏎   const frameCheck = frame && frame.facets.find((f) => f.facet === 'architect …"

### EXTRA-L1-0044
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: A missing required facet is a conformance failure: raise a Decision Request instead of shipping the module.
- Trigger/scope: repo/meta (capability maintenance)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000583: `output/template/.claude/capabilities/persistence/CONTRACT.md:26-26` — "- A missing required facet is a conformance failure: raise a Decision Request instead of shipping the module."

### EXTRA-L1-0045
- Closest oracle policies: PST-005, PST-006, PST-010
- Modality: MUST_NOT
- Normative action: Replacing the persistence implementation must not silently lose migration or seeding semantics; the new module states its mechanisms explicitly.
- Trigger/scope: repo/meta (capability maintenance)
- Exceptions: Implementation replacement.
- Why EXTRA: Not in the oracle.
- Evidence L1-S000584: `output/template/.claude/capabilities/persistence/CONTRACT.md:27-27` — "- Replacing the implementation (for example an ORM with a micro-ORM) must not silently lose migration or seeding semantics; the new module states its migration and seeding mechanisms explicitly."

### EXTRA-L1-0046
- Closest oracle policies: DEP-009, ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: A database-provider change is a Reserved variation inside the persistence slot requiring updates to declared properties, dev-config, relational-fidelity binding and commands.
- Trigger/scope: repo/meta (capability maintenance)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000585: `output/template/.claude/capabilities/persistence/CONTRACT.md:28-28` — "- A database-provider change (one relational provider for another) is a variation inside this slot, not a new slot: update the declared properties, `persistence.dev-config`, the relational-fidelity binding, and commands. It is Reserved and observable string-comparison changes need approval."

### EXTRA-L1-0047
- Closest oracle policies: DEP-009, DEP-006
- Modality: DEFAULT
- Normative action: Scaffold package placement: Microsoft.EntityFrameworkCore.SqlServer in Infrastructure, Microsoft.EntityFrameworkCore.Design in the Api startup project, dotnet-ef via a tool manifest.
- Trigger/scope: workflow-read facet persistence.commands (scaffolding, migrations, verification)
- Exceptions: none
- Why EXTRA: Package placement not in the oracle.
- Evidence L1-S000591: `output/template/.claude/capabilities/persistence/ef-core/commands.md:11-13` — "| `Microsoft.EntityFrameworkCore.SqlServer` | `<Name>.Infrastructure` | baseline persistence | ⏎ | `Microsoft.EntityFrameworkCore.Design` | `<Name>.Api` (startup project) | design-time services for migrations | ⏎ | `dotnet-ef` (local or global .NET tool) | repository tool manifest | migration commands |"

### EXTRA-L1-0048
- Closest oracle policies: ARC-023
- Modality: DEFAULT
- Normative action: Register the context in AddInfrastructure with UseSqlServer(GetConnectionString("DefaultConnection")); the Development string follows persistence.dev-config.
- Trigger/scope: workflow-read facet persistence.commands (scaffolding, migrations, verification)
- Exceptions: none
- Why EXTRA: Registration technique not in the oracle.
- Evidence L1-S000593: `output/template/.claude/capabilities/persistence/ef-core/commands.md:16-16` — "Register the context in `AddInfrastructure` with `options.UseSqlServer(configuration.GetConnectionString("DefaultConnection"))`; the Development connection string follows `persistence.dev-config`."

### EXTRA-L1-0049
- Closest oracle policies: ARC-019
- Modality: MUST
- Normative action: Update affected entity configurations (IEntityTypeConfiguration<T>) and repository implementations for a model change.
- Trigger/scope: workflow-read facet persistence.workflow (model/persistence changes, schema-affecting settings)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000614: `output/template/.claude/capabilities/persistence/ef-core/workflow.md:9-9` — "1. Update the entity configurations (`IEntityTypeConfiguration<T>`) and the repository implementations affected by the change."

### EXTRA-L1-0050
- Closest oracle policies: ARC-019
- Modality: DEFAULT
- Normative action: When the schema changes add a migration from the implementation-layer project with the entry-point project as startup project.
- Trigger/scope: workflow-read facet persistence.workflow (model/persistence changes, schema-affecting settings)
- Exceptions: Schema changes.
- Why EXTRA: Migration command technique not in the oracle.
- Evidence L1-S000616: `output/template/.claude/capabilities/persistence/ef-core/workflow.md:11-11` — "3. When the schema changes, add a migration from the implementation-layer project with the entry-point project as startup project."

### EXTRA-L1-0051
- Closest oracle policies: WF-005
- Modality: MUST
- Normative action: Build the affected projects and list or script pending migrations to confirm the expected schema change.
- Trigger/scope: workflow-read facet persistence.workflow (model/persistence changes, schema-affecting settings)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000622: `output/template/.claude/capabilities/persistence/ef-core/workflow.md:26-26` — "- Build the affected projects and list or script the pending migrations to confirm the expected schema change."

### EXTRA-L1-0052
- Closest oracle policies: PST-005, WF-006
- Modality: MUST
- Normative action: Apply migrations to a local Development database explicitly, start the API in Development and confirm the seeder populates an empty database or leaves an existing one unchanged.
- Trigger/scope: workflow-read facet persistence.workflow (model/persistence changes, schema-affecting settings)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000623: `output/template/.claude/capabilities/persistence/ef-core/workflow.md:27-27` — "- Apply migrations to a local Development database explicitly, then start the API in Development and confirm the seeder populates an empty database (or leaves an existing one unchanged)."

### EXTRA-L1-0053
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Report model changes, migration names with review notes (destructive operations called out), whether DbSeeder was updated, and tests added/updated.
- Trigger/scope: workflow-read facet persistence.workflow (model/persistence changes, schema-affecting settings)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000626: `output/template/.claude/capabilities/persistence/ef-core/workflow.md:32-32` — "Report model changes, migration names with review notes (destructive operations called out), whether `DbSeeder` was updated or unaffected, and the tests added or updated."

### EXTRA-L1-0054
- Closest oracle policies: none
- Modality: MUST
- Normative action: Implementation-independent policy stays in neutral rule files outside leaf modules; placement and references belong to the frame.
- Trigger/scope: repo/meta (capability maintenance)
- Exceptions: none
- Why EXTRA: Capability-system rule (repo/meta).
- Evidence L1-S000520: `output/template/.claude/capabilities/backend-testing/CONTRACT.md:5-5` — "Implementation-independent test policy stays outside the module in `.claude/rules/0-core/testing.md`: test levels, behavior focus, determinism, isolation, relational fidelity, probe-to-test preservation (owned by `verify`), and framework-neutral naming. Test-project placement and references belong to the architecture frame."
- Evidence L1-S000567: `output/template/.claude/capabilities/frontend/CONTRACT.md:5-5` — "Framework-neutral frontend structural policy stays outside the module in `.claude/rules/0-core/frontend.md`; browser security stays in `.claude/rules/0-core/security.md`; package-manager conventions stay in `.claude/rules/3-project/package-management.md`."

### EXTRA-L1-0055
- Closest oracle policies: DEP-013
- Modality: DEFAULT
- Normative action: NUnit.Analyzers (template default) and Microsoft.Extensions.TimeProvider.Testing when time control is useful.
- Trigger/scope: workflow-read facet backend-testing.commands
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000533: `output/template/.claude/capabilities/backend-testing/nunit/commands.md:19-22` — "| `NUnit`, `NUnit3TestAdapter`, `Microsoft.NET.Test.Sdk` | framework, runner adapter, test host | ⏎ | `NUnit.Analyzers` | analyzer for NUnit usage (template default) | ⏎ | `Microsoft.AspNetCore.Mvc.Testing` | `WebApplicationFactory<Program>` integration tests | ⏎ | `Microsoft.Extensions.TimeProvider.Testing` | `FakeTimeProvider` when time control is useful |"

### EXTRA-L1-0056
- Closest oracle policies: none
- Modality: MUST
- Normative action: Clearing the optional frontend slot: set the selection to none, delete the manifest-listed files, remove the frontend-stack import and map rows, run the checker; neutral rules stay and load only for frontend paths.
- Trigger/scope: repo/meta (capability maintenance)
- Exceptions: Frontend removal.
- Why EXTRA: Capability-system procedure (repo/meta).
- Evidence L1-S000564: `output/template/.claude/capabilities/frontend/angular/MODULE.md:22-22` — "Delete every file in the table plus this directory, remove the `@.claude/rules/3-project/frontend-stack.md` line from `CLAUDE.md`, set the frontend selection row to `none`, remove the module's rows from `.claude/INSTRUCTION_MAP.md`, and run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"`."
- Evidence L1-S000572: `output/template/.claude/capabilities/frontend/CONTRACT.md:19-19` — "Clearing the optional selection removes the frontend without hunting: set the selection row to `none`, delete the files listed in the module manifest, remove the `frontend-stack.md` import line from `CLAUDE.md`, remove the module's rows from `.claude/INSTRUCTION_MAP.md`, then run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"`. Neutral rules stay; they only load fo …"

### EXTRA-L1-0057
- Closest oracle policies: DEP-014
- Modality: MUST
- Normative action: Confirm the exact flags of the installed CLI with ng new --help rather than from memory.
- Trigger/scope: workflow-read facet frontend.commands
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000547: `output/template/.claude/capabilities/frontend/angular/commands.md:9-9` — "Create the workspace with the current Angular CLI using the baseline from the frontend stack rule: standalone APIs, routing, SCSS, strict mode, zoneless mode when supported. Confirm the exact flags of the installed CLI with `ng new --help` rather than from memory."

### EXTRA-L1-0018
- Closest oracle policies: none
- Modality: MUST
- Normative action: The selected frame maps each role to a project; instructions outside the frame use role names instead of frame-specific layer names.
- Trigger/scope: path rule: backend/**/*
- Exceptions: none
- Why EXTRA: Instruction-system rule (repo/meta), checked by check-instructions.mjs (frame terms).
- Evidence L1-S000266: `output/template/.claude/rules/1-architecture/roles.md:12-12` — "The selected architecture frame maps each role to a concrete project (imported adopted-architecture rule). Instructions outside the frame use these roles instead of frame-specific layer names."

### EXTRA-L1-0019
- Closest oracle policies: ARC-010
- Modality: DEFAULT
- Normative action: Controller classes live in a Controllers/ folder of the entry-point project.
- Trigger/scope: path rule: backend/**/*
- Exceptions: none
- Why EXTRA: Placement convention not in the oracle.
- Evidence L1-S000289: `output/template/.claude/rules/2-technology/backend-platform.md:14-14` — "- Entry-point mechanism: ASP.NET Core Controllers (decided stack), as controller classes in a `Controllers/` folder of the entry-point project; do not create Minimal API endpoint groups unless explicitly requested."

### EXTRA-L1-0020
- Closest oracle policies: TST-004
- Modality: DEFAULT
- Normative action: Create WebApplicationFactory in [OneTimeSetUp] and dispose it in [OneTimeTearDown].
- Trigger/scope: path rule: backend/**/*Tests/**/*
- Exceptions: none
- Why EXTRA: Lifecycle technique not in the oracle.
- Evidence L1-S000315: `output/template/.claude/rules/2-technology/backend-testing/test-framework.md:17-17` — "- In-process host for integration tests: `WebApplicationFactory<Program>`, created in `[OneTimeSetUp]` and disposed in `[OneTimeTearDown]`."

### EXTRA-L1-0021
- Closest oracle policies: DEP-006
- Modality: MUST
- Normative action: Use a VersionOverride only for a concrete, reported reason.
- Trigger/scope: path rule: backend/**, frontend/**, *.csproj, Directory.*.props, package.json, package-lock.json
- Exceptions: Concrete reported reason.
- Why EXTRA: Not in DEP-006.
- Evidence L1-S000034: `output/template/.claude/hooks/post-change-checks.mjs:59-66` — "function checkCsproj(rel, text, rules, findings) { ⏎   const info = parseCsproj(text); ⏎   for (const pkg of info.packages) { ⏎     if (pkg.version) findings.push(`${rel}: PackageReference '${pkg.id}' declares a version; versions belong only in Directory.Packages.props (owner: ${PCM}).`); ⏎     else if (pkg.versionOverride) findings.push(`${rel}: PackageReference '${pkg.id}' uses VersionOverride;  …"
- Evidence L1-S000383: `output/template/.claude/rules/3-project/package-management.md:16-16` — "- Use NuGet Central Package Management: package versions live only in `Directory.Packages.props`; project `PackageReference` entries are versionless — never duplicate a centrally managed version in a project file, and use a `VersionOverride` only for a concrete, reported reason — and sit in the narrowest project that actually needs the package."

### EXTRA-L1-0058
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Required workflow skills (development-workflow, project-structure, verify, code-review, build-fix, custom-settings, git-workflow, security-scan, add-dependency, architecture-decision, template-maintenance), shared knowledge skills and selected module knowledge skills must exist with matching names and descriptions; template-maintenance must be user-only and all others model-invocable; long descriptions warn.
- Trigger/scope: instruction-system files when the checker is run (after instruction changes)
- Exceptions: Checker run.
- Why EXTRA: Repo/meta invariant.
- Evidence L1-S000630: `output/template/.claude/scripts/check-instructions.mjs:15-18` — "const REQUIRED_WORKFLOWS = ['development-workflow', 'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings', ⏎   'git-workflow', 'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance']; ⏎ const REQUIRED_SHARED_KNOWLEDGE = ['http-api', 'aspnet-error-handling', 'logging', 'httpclient-factory', 'configuration', ⏎   'dependency-injection', 'caching', 's …"
- Evidence L1-S000651: `output/template/.claude/scripts/check-instructions.mjs:468-485` — "// Skills and agents. ⏎   const agents = listFiles(path.join(claude, 'agents'), (f) => f.endsWith('.md')).map((f) => path.basename(f, '.md')); ⏎   const moduleKnowledge = modules.flatMap((m) => m.facets.filter((f) => f.facet.endsWith('.knowledge')).map((f) => f.file.split('/')[2])); ⏎   for (const name of [...REQUIRED_WORKFLOWS, ...REQUIRED_SHARED_KNOWLEDGE, ...moduleKnowledge]) { ⏎     if (!skill …"

### EXTRA-L1-0059
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Module manifests must have leak-tokens and binds lines, a facet table belonging to the slot, matching Capability headers, existing facet files with matching Capability/Facet/Level headers, valid JSON facets and every contract-required facet.
- Trigger/scope: instruction-system files when the checker is run (after instruction changes)
- Exceptions: Checker run.
- Why EXTRA: Repo/meta invariant.
- Evidence L1-S000641: `output/template/.claude/scripts/check-instructions.mjs:278-316` — "// Module manifests. ⏎   const modules = []; ⏎   for (const [slot, impl] of Object.entries(selected)) { ⏎     if (!impl) continue; ⏎     const manifestPath = `.claude/capabilities/${slot}/${impl}/MODULE.md`; ⏎     const doc = docs.get(manifestPath); ⏎     if (!doc) { fail(manifestPath, 'missing module manifest'); continue; } ⏎     const capability = `${slot}/${impl}`; ⏎     const line = (key) => ( …"

### EXTRA-L1-0060
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: A file declaring Capability must belong to a selected module and be listed in its manifest.
- Trigger/scope: instruction-system files when the checker is run (after instruction changes)
- Exceptions: Checker run.
- Why EXTRA: Repo/meta invariant.
- Evidence L1-S000644: `output/template/.claude/scripts/check-instructions.mjs:358-364` — "// Capability declarations must match manifests. ⏎   for (const [p, d] of docs) { ⏎     if (!d.header || !d.header.Capability) continue; ⏎     const m = modules.find((x) => x.capability === d.header.Capability); ⏎     if (!m) { fail(p, `declares Capability '${d.header.Capability}', which is not a selected module`); continue; } ⏎     if (!(p.startsWith(m.dir) || m.facets.some((f) => f.file === p))) …"

### EXTRA-L1-0061
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Rules live in a level directory matching their header Level, declare non-empty paths frontmatter, and rules in capability subdirectories declare Capability.
- Trigger/scope: instruction-system files when the checker is run (after instruction changes)
- Exceptions: Checker run.
- Why EXTRA: Repo/meta invariant.
- Evidence L1-S000645: `output/template/.claude/scripts/check-instructions.mjs:366-376` — "// Rules: level directory, paths, capability subdirectories. ⏎   for (const [p, d] of docs) { ⏎     if (!p.startsWith('.claude/rules/')) continue; ⏎     const parts = p.split('/'); ⏎     const levelDir = parts[2]; ⏎     if (!LEVELS.includes(levelDir)) fail(p, `rule outside a level directory (${LEVELS.join(', ')})`); ⏎     if (d.header && d.header.Level !== levelDir) fail(p, `header Level '${d.head …"

### EXTRA-L1-0062
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: CLAUDE.md imports must resolve and be 'Loading: always'; every 'Loading: always' artifact must be imported by CLAUDE.md.
- Trigger/scope: instruction-system files when the checker is run (after instruction changes)
- Exceptions: Checker run.
- Why EXTRA: Repo/meta invariant.
- Evidence L1-S000647: `output/template/.claude/scripts/check-instructions.mjs:397-406` — "// Always-loaded surface: CLAUDE.md imports. ⏎   const imports = [...docs.get('CLAUDE.md').body.matchAll(/^@(\S+)\s*$/gm)].map((m) => m[1]); ⏎   for (const imp of imports) { ⏎     if (!exists(imp)) { fail('CLAUDE.md', `import does not resolve: @${imp}`); continue; } ⏎     const d = docs.get(imp); ⏎     if (d && d.header && !/^always/.test(d.header.Loading)) fail(imp, 'imported by CLAUDE.md but hea …"

### EXTRA-L1-0063
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Facet references (<slot>.<facet>) must resolve to facets declared by the selected module; references to an unselected required slot fail.
- Trigger/scope: instruction-system files when the checker is run (after instruction changes)
- Exceptions: Checker run.
- Why EXTRA: Repo/meta invariant.
- Evidence L1-S000650: `output/template/.claude/scripts/check-instructions.mjs:458-466` — "// Facet references. ⏎   for (const [p, d] of docs) { ⏎     for (const m of d.body.matchAll(/(?<![\w./-])(architecture|persistence|backend-testing|frontend)\.([a-z][a-z-]*)(?![\w-])/g)) { ⏎       const [ref, slot] = [m[0], m[1]]; ⏎       const mod = modules.find((x) => x.slot === slot); ⏎       if (!mod) { if (SLOTS[slot].startsWith('required')) fail(p, `facet reference '${ref}' but slot '${slot}' …"

### EXTRA-L1-0064
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Named skill/agent references and backticked .claude/ path references must resolve.
- Trigger/scope: instruction-system files when the checker is run (after instruction changes)
- Exceptions: Checker run.
- Why EXTRA: Repo/meta invariant.
- Evidence L1-S000653: `output/template/.claude/scripts/check-instructions.mjs:494-512` — "// Named skill/agent references. ⏎   const known = new Set([...skills, ...agents]); ⏎   for (const [p, d] of docs) { ⏎     const re = /`([a-z][a-z0-9-]*)`(?=\s+(?:skill|workflow|agent)\b)|(?:\brun|→|->|[Tt]echniques?:|Procedures?:)\s+`([a-z][a-z0-9-]*)`/g; ⏎     for (const m of d.body.matchAll(re)) { ⏎       const name = m[1] || m[2]; ⏎       if (!known.has(name)) fail(p, `references unknown skill …"

### EXTRA-L1-0065
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Skill-private references may be used only by their owning skill (or listed in the map).
- Trigger/scope: instruction-system files when the checker is run (after instruction changes)
- Exceptions: Checker run.
- Why EXTRA: Repo/meta invariant.
- Evidence L1-S000654: `output/template/.claude/scripts/check-instructions.mjs:514-523` — "// Skill-private references are used only by their owning skill (the map may list them). ⏎   for (const p of docs.keys()) { ⏎     const m = p.match(/^\.claude\/skills\/([^/]+)\/references\/(.+)$/); ⏎     if (!m) continue; ⏎     for (const [other, d] of docs) { ⏎       if (other === p || other === '.claude/INSTRUCTION_MAP.md' || other.startsWith(`.claude/skills/${m[1]}/`)) continue; ⏎       const o …"

### EXTRA-L1-0066
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: The instruction map must list every artifact and must not be imported by CLAUDE.md.
- Trigger/scope: instruction-system files when the checker is run (after instruction changes)
- Exceptions: Checker run.
- Why EXTRA: Repo/meta invariant.
- Evidence L1-S000655: `output/template/.claude/scripts/check-instructions.mjs:525-531` — "// Human map coverage. ⏎   const map = docs.get('.claude/INSTRUCTION_MAP.md'); ⏎   if (!map) fail('.claude/INSTRUCTION_MAP.md', 'missing instruction map'); ⏎   else { ⏎     for (const p of docs.keys()) if (p !== '.claude/INSTRUCTION_MAP.md' && !map.body.includes(p)) fail('.claude/INSTRUCTION_MAP.md', `does not list ${p}`); ⏎     if (imports.includes('.claude/INSTRUCTION_MAP.md')) fail('CLAUDE.md', …"

### EXTRA-L1-0067
- Closest oracle policies: DEP-025
- Modality: ENFORCED
- Normative action: Hooks must be exec form (bare command, args with the ${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs launcher, no expansion), have numeric timeouts; only PreToolUse sets onFailure block; PreToolUse/PostToolUse/PostToolUseFailure must cover Bash/PowerShell (and edit tools for PostToolUse) and a Stop hook must exist.
- Trigger/scope: instruction-system files when the checker is run (after instruction changes)
- Exceptions: Checker run.
- Why EXTRA: Enforcement-configuration invariant (repo/meta).
- Evidence L1-S000656: `output/template/.claude/scripts/check-instructions.mjs:533-562` — "// Hooks: exec form (command + args, placeholder only as argument data), required registrations, failure semantics. ⏎   const settingsPath = path.join(claude, 'settings.json'); ⏎   if (!existsSync(settingsPath)) fail('.claude/settings.json', 'missing'); ⏎   else { ⏎     const S = '.claude/settings.json'; ⏎     const settings = JSON.parse(readText(settingsPath, S)); ⏎     const hooks = settings.hoo …"

### EXTRA-L1-0068
- Closest oracle policies: DEP-020, DEP-004
- Modality: MUST_NOT
- Normative action: The deprecated Microsoft.Extensions.Http.Polly / Polly.Extensions.Http integrations are never added.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Concrete deny rule not in the oracle.
- Evidence L1-S000665: `output/template/.claude/skills/add-dependency/SKILL.md:17-17` — "- `Microsoft.Extensions.Http.Resilience` (outbound `HttpClient`) or `Microsoft.Extensions.Resilience` (other pipelines) — Default: these are the resilience packages when resilience is required; direct Polly usage is an explicit, documented exception, and the deprecated `Microsoft.Extensions.Http.Polly` / `Polly.Extensions.Http` integrations are never added;"
- Evidence L1-S001340: `output/template/.claude/skills/project-structure/references/baseline-packages.md:18-18` — "Do not use deprecated or legacy ASP.NET automatic-validation integration packages, `Microsoft.Extensions.Http.Polly`, or `Polly.Extensions.Http`. Do not make the built-in `AddOpenApi()`/`MapOpenApi()` endpoint the template default when the requirement is interactive Swagger UI testing."

### EXTRA-L1-0069
- Closest oracle policies: DEP-005
- Modality: MUST_NOT
- Normative action: Make no legal conclusions beyond the published license information.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Not in DEP-005.
- Evidence L1-S000677: `output/template/.claude/skills/add-dependency/SKILL.md:36-36` — "Do not install automatically when the package requires payment or a commercial license, or when its license has material obligations or cannot be confidently classified (strong copyleft, dual licensing that may require a commercial license, source-available/custom terms, unclear or missing license). Present the concern and reasonable alternatives, never substitute silently, and make no legal concl …"

### EXTRA-L1-0070
- Closest oracle policies: DEP-001
- Modality: MUST
- Normative action: Remove dependencies no longer used when part of the current change and safe to verify; leave no dead references.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: Safe to verify.
- Why EXTRA: Not in the oracle.
- Evidence L1-S000686: `output/template/.claude/skills/add-dependency/SKILL.md:69-69` — "Remove dependencies that are no longer used when that is part of the current change and safe to verify; do not leave dead references, and do not perform unrelated dependency cleanup during a narrow task."

### EXTRA-L1-0071
- Closest oracle policies: DEP-004
- Modality: MUST
- Normative action: Report package, version, license, vulnerability/deprecation result, target project and approvals obtained or pending.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Report fields not in the oracle.
- Evidence L1-S000688: `output/template/.claude/skills/add-dependency/SKILL.md:73-73` — "Package, version, license, vulnerability/deprecation result, target project, and approvals obtained or still pending. Then continue the calling workflow (`verify` covers the build)."

### EXTRA-L1-0072
- Closest oracle policies: GOV-017, ARC-020
- Modality: MUST
- Normative action: Record an approved decision as an ADR at docs/decisions/NNNN-<kebab-title>.md (Status/Approved by, Context, Decision, Consequences, Alternatives considered), creating docs/decisions/ with the first ADR.
- Trigger/scope: workflow architecture-decision (Reserved decisions)
- Exceptions: Approved decision.
- Why EXTRA: ADR obligation not in the oracle.
- Evidence L1-S000753: `output/template/.claude/skills/architecture-decision/SKILL.md:27-36` — "1. Write an ADR at `docs/decisions/NNNN-<kebab-title>.md` (create `docs/decisions/` with the first ADR): ⏎  ⏎    ```markdown ⏎    # NNNN. <Title> ⏎    Status: Accepted (<date>) · Approved by: <user or reference> ⏎    ## Context ⏎    ## Decision ⏎    ## Consequences ⏎    ## Alternatives considered ⏎    ```"

### EXTRA-L1-0073
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: Update the decision file at the level the decision belongs to (frame style rule, decisions.md, frontend stack rule), never a single cross-level register.
- Trigger/scope: workflow architecture-decision (Reserved decisions)
- Exceptions: none
- Why EXTRA: Repo/meta recording rule.
- Evidence L1-S000754: `output/template/.claude/skills/architecture-decision/SKILL.md:38-42` — "2. Update the decision file at the level the decision belongs to — never a single cross-level register: ⏎    - adopted style, role mapping, or patterns not adopted → the frame's style rule (`.claude/rules/1-architecture/frame/`); ⏎    - stack, conditional technology, layout default → `.claude/rules/3-project/decisions.md`; ⏎    - frontend stack → the frontend stack rule; ⏎    - product behavior or …"

### EXTRA-L1-0074
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: Record the change as a decision summary line pointing to the ADR; do not restate rules that live elsewhere.
- Trigger/scope: workflow architecture-decision (Reserved decisions)
- Exceptions: none
- Why EXTRA: Repo/meta rule.
- Evidence L1-S000755: `output/template/.claude/skills/architecture-decision/SKILL.md:43-43` — "3. Record the change as a decision summary line pointing to the ADR; do not restate rules that live elsewhere."

### EXTRA-L1-0075
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Report the decision, ADR path, updated decision files and follow-up work.
- Trigger/scope: workflow architecture-decision (Reserved decisions)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000759: `output/template/.claude/skills/architecture-decision/SKILL.md:51-51` — "Decision, ADR path, decision files updated, follow-up work (structure, dependencies, migrations)."

### EXTRA-L1-0076
- Closest oracle policies: FE-002
- Modality: DEFAULT
- Normative action: Route-level page components coordinate UI behaviour; reusable presentation components take explicit inputs and emit meaningful events.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000698: `output/template/.claude/skills/angular/SKILL.md:38-38` — "Do not introduce NgModules for ordinary feature work unless an integration or legacy dependency requires them. Route-level page components coordinate UI behavior; reusable presentation components take explicit inputs and emit meaningful events."

### EXTRA-L1-0077
- Closest oracle policies: FE-004
- Modality: AVOID
- Normative action: Use computed for derived state; avoid effect() when computed, template binding or explicit event handling is clearer.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000701: `output/template/.claude/skills/angular/SKILL.md:48-48` — "Use `computed` for derived state and avoid `effect()` when `computed`, template binding, or explicit event handling expresses the dependency more clearly. RxJS fits `HttpClient`, debounced search, cancellation/switching (`switchMap`), combining async sources, and event streams. For manual subscriptions in components or services, `takeUntilDestroyed()` (or the `DestroyRef` it uses) ties lifetime to …"

### EXTRA-L1-0078
- Closest oracle policies: FE-010, API-010
- Modality: MUST_NOT
- Normative action: Keep request mapping explicit; do not duplicate complex domain rules in TypeScript unless the UI needs an equivalent user-facing rule.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: UI needs it.
- Why EXTRA: Not in the oracle.
- Evidence L1-S000710: `output/template/.claude/skills/angular/SKILL.md:77-77` — "Reactive forms suit non-trivial forms needing explicit state, validation, and testability. Keep transport/request mapping explicit. Do not duplicate complex domain rules in TypeScript unless the UI genuinely needs an equivalent user-facing rule."

### EXTRA-L1-0079
- Closest oracle policies: DEP-014
- Modality: DEFAULT
- Normative action: Use Material components consistently for common primitives when they satisfy the requirement; do not wrap every component without a reason.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000715: `output/template/.claude/skills/angular/SKILL.md:94-94` — "Use Material components consistently for common primitives when they satisfy the requirement; do not wrap every Material component in a custom abstraction without a reason."

### EXTRA-L1-0080
- Closest oracle policies: TST-002
- Modality: DEFAULT
- Normative action: Frontend test targets: meaningful component behaviour, validation, request mapping, important route/auth behaviour, complex reactive state with the configured runner; E2E covers a few important workflows.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000719: `output/template/.claude/skills/angular/SKILL.md:102-102` — "Test meaningful component behavior, validation, data-access request mapping, important route/auth behavior, and complex reactive state with the configured runner; do not test framework internals. E2E covers a few important user workflows unless broader coverage is required; avoid duplicating the same behavior at every level."

### EXTRA-L1-0081
- Closest oracle policies: API-016
- Modality: DEFAULT
- Normative action: Generate separate or clearly grouped Swagger documents per supported version.
- Trigger/scope: on-demand knowledge skill api-versioning (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000742: `output/template/.claude/skills/api-versioning/SKILL.md:62-62` — "Generate separate or clearly grouped Swagger documents per supported version (`swagger`), matching runtime routing and metadata. Version changes never override normal HTTP semantics (`http-api`). Test meaningful differences: version routing, version-specific shapes, deprecated versions still operating during support, unsupported-version behavior, shared behavior consistent where intended — without …"

### EXTRA-L1-0082
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Test meaningful version differences (routing, shapes, deprecated versions still working, unsupported-version behaviour, intended shared behaviour) without duplicating identical tests per version.
- Trigger/scope: on-demand knowledge skill api-versioning (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000742: `output/template/.claude/skills/api-versioning/SKILL.md:62-62` — "Generate separate or clearly grouped Swagger documents per supported version (`swagger`), matching runtime routing and metadata. Version changes never override normal HTTP semantics (`http-api`). Test meaningful differences: version routing, version-specific shapes, deprecated versions still operating during support, unsupported-version behavior, shared behavior consistent where intended — without …"

### EXTRA-L1-0083
- Closest oracle policies: API-010, DEP-002
- Modality: MUST_NOT
- Normative action: Follow the project's established validation invocation pattern instead of adding a competing mechanism; do not add deprecated automatic-validation integration packages.
- Trigger/scope: on-demand knowledge skill aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000775: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:69-69` — "- FluentValidation fits required application input, string/collection constraints, ranges, cross-property and conditional rules. Register validators with `FluentValidation.DependencyInjectionExtensions`; follow the project's established invocation pattern instead of adding a competing mechanism, and do not add deprecated automatic-validation integration packages."
- Evidence L1-S001340: `output/template/.claude/skills/project-structure/references/baseline-packages.md:18-18` — "Do not use deprecated or legacy ASP.NET automatic-validation integration packages, `Microsoft.Extensions.Http.Polly`, or `Polly.Extensions.Http`. Do not make the built-in `AddOpenApi()`/`MapOpenApi()` endpoint the template default when the requirement is interactive Swagger UI testing."

### EXTRA-L1-0084
- Closest oracle policies: API-009
- Modality: MUST
- Normative action: If Result is adopted use typed errors (e.g. AppError(Code, Message)), never arbitrary string arrays.
- Trigger/scope: on-demand knowledge skill aspnet-error-handling (backend)
- Exceptions: Result adopted.
- Why EXTRA: Not in the oracle.
- Evidence L1-S000783: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:93-93` — "Consider `Result<T>` when an operation has several expected failure modes, callers benefit from typed outcomes, exception-based flow would otherwise be common, and the project will use it consistently (adopting it project-wide is Reserved). Avoid it when `null`, `bool`, or a simple typed response is clear or it only wraps straightforward CRUD. If adopted, use typed errors: `public sealed record Ap …"

### EXTRA-L1-0085
- Closest oracle policies: API-010, ARC-010
- Modality: AVOID
- Normative action: Avoid Minimal API endpoint filters for validation in a Controller project.
- Trigger/scope: on-demand knowledge skill aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000785: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:97-97` — "Raw exception messages to clients; inconsistent anonymous error objects; use-case code depending on HTTP status codes; `Result<T>` everywhere; exceptions for every negative branch; swallowed exceptions; catch/log/rethrow at every layer; duplicate logging; sensitive data in `ProblemDetails`; business rules only in request validators; Minimal API endpoint filters for validation in a Controller proje …"

### EXTRA-L1-0086
- Closest oracle policies: SEC-016, ARC-020
- Modality: DEFAULT
- Normative action: Bearer/OIDC for SPA→API, cookies for server-rendered apps, Identity for owned local accounts (not merely because an entity is called User), external OIDC/OAuth when identity is delegated.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000793: `output/template/.claude/skills/authentication/SKILL.md:14-17` — "- Bearer/OIDC for a browser SPA calling an API; ⏎ - cookies for server-rendered interactive applications; ⏎ - ASP.NET Core Identity when the application owns local accounts and passwords and needs Identity's account management — not merely because a business entity is named `User`; ⏎ - an external OpenID Connect/OAuth provider when identity is delegated; do not issue custom JWTs when an existing p …"

### EXTRA-L1-0087
- Closest oracle policies: SEC-005
- Modality: PREFER
- Normative action: Prefer policies for meaningful capabilities; keep repeated policy names in constants; roles only for role-oriented models; a policy when several roles/claims form one capability; avoid scattered compound role/permission strings.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000800: `output/template/.claude/skills/authentication/SKILL.md:36-36` — "A secure global/fallback policy can make repeated `[Authorize]` unnecessary; mark deliberate public endpoints `[AllowAnonymous]`. Prefer policies for meaningful capabilities:"
- Evidence L1-S000802: `output/template/.claude/skills/authentication/SKILL.md:49-49` — "Keep policy names in constants when repeated. Use roles when the business model is genuinely role-oriented; prefer a policy when several roles or claims form one capability; avoid scattered compound role strings."
- Evidence L1-S000817: `output/template/.claude/skills/authentication/SKILL.md:90-90` — "Custom password hashing; disabled token validation; hardcoded signing keys; authorization only in the frontend; use-case code depending on `HttpContext`; `401` for forbidden or `403` for unauthenticated; logged tokens; scattered permission strings; Identity, JWT issuance, or OIDC infrastructure without an actual need."

### EXTRA-L1-0088
- Closest oracle policies: API-005
- Modality: DEFAULT
- Normative action: Authentication/authorization middleware normally produces 401/403 rather than controllers manufacturing them.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: none
- Why EXTRA: Not in API-005.
- Evidence L1-S000806: `output/template/.claude/skills/authentication/SKILL.md:57-57` — "Authentication/authorization middleware normally produces `401` (not authenticated or authentication failed) and `403` (authenticated, not permitted) rather than controllers manufacturing them. A deliberate `404` for some forbidden lookups must be a consistent policy (`http-api`)."
- Evidence L1-S001190: `output/template/.claude/skills/http-api/SKILL.md:28-28` — "- **401 / 403** — authentication missing or failed vs. authenticated but not permitted (missing permission, insufficient role, policy prohibits the operation); the client cannot fix `403` by resending the same credentials. Authentication/authorization middleware normally produces these."

### EXTRA-L1-0089
- Closest oracle policies: ARC-007
- Modality: DEFAULT
- Normative action: When use cases repeatedly need caller identity define a small use-case abstraction implemented at an outer boundary; passing an explicit user id is fine when simpler.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: Repeated need.
- Why EXTRA: Not in the oracle.
- Evidence L1-S000810: `output/template/.claude/skills/authentication/SKILL.md:70-70` — "When use cases repeatedly need caller identity, define a small use-case-layer abstraction and implement the HTTP adapter at an outer boundary; use-case code never depends on `HttpContext`, `ClaimsPrincipal`, or `IHttpContextAccessor`. Passing an explicit user id is fine when simpler."

### EXTRA-L1-0090
- Closest oracle policies: TST-003, SEC-005
- Modality: DEFAULT
- Normative action: Integration-test protected operations: unauthenticated→401, unauthorized→403, permitted success, ownership rules, intentionally anonymous endpoints reachable.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000815: `output/template/.claude/skills/authentication/SKILL.md:86-86` — "Integration-test important protected operations: unauthenticated → `401`; authenticated without permission → `403`; permitted → success; ownership rules; intentionally anonymous endpoints stay reachable. Verify behavior, not just attribute presence."

### EXTRA-L1-0091
- Closest oracle policies: ARC-024, RUN-007
- Modality: DEFAULT
- Normative action: Output caching lives at the entry point when the whole response is reusable; implementation-layer adapters may cache expensive calls when their exposed contract stays intact.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000862: `output/template/.claude/skills/caching/SKILL.md:14-14` — "- **HTTP response caching** — ASP.NET Core output caching when the whole response is safely reusable; lives at the entry point."
- Evidence L1-S000864: `output/template/.claude/skills/caching/SKILL.md:16-16` — "- **Adapter caching** — an implementation-layer adapter may cache expensive remote or persistence calls when the contract it exposes stays intact."

### EXTRA-L1-0092
- Closest oracle policies: RUN-020
- Modality: PREFER
- Normative action: Centralize key construction once formats repeat.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000873: `output/template/.claude/skills/caching/SKILL.md:47-47` — "- Key dimensions: entity id, tenant, user (when genuinely user-specific), locale, relevant query/filter parameters. Centralize key construction once formats repeat."

### EXTRA-L1-0093
- Closest oracle policies: RUN-007
- Modality: DEFAULT
- Normative action: Apply output-cache policies through controller/action metadata.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000878: `output/template/.claude/skills/caching/SKILL.md:60-60` — "Apply the policy through controller/action metadata. Cache authenticated or user-specific responses only when the key and policy isolate users and authorization context."

### EXTRA-L1-0094
- Closest oracle policies: RUN-018
- Modality: MUST
- Normative action: Decide whether a cache failure falls back to the source, fails the request or serves stale data.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000880: `output/template/.claude/skills/caching/SKILL.md:64-64` — "Use cases keep their normal repository/commit-boundary flow; coordinate invalidation through an abstraction when it is part of the use-case semantics instead of bypassing repositories. Decide whether a cache failure falls back to the source, fails the request, or serves stale data."

### EXTRA-L1-0095
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Test caching where it affects observable correctness (invalidation, key isolation, miss fallback, outage behaviour).
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000882: `output/template/.claude/skills/caching/SKILL.md:68-68` — "Test caching where it affects observable correctness: invalidation after successful mutation, tenant/user key isolation, correct miss fallback, intended outage behavior. Do not unit-test framework cache internals."

### EXTRA-L1-0096
- Closest oracle policies: ARC-016, RUN-021
- Modality: MUST_NOT
- Normative action: Do not cache tracked ORM entities across commit boundaries.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000884: `output/template/.claude/skills/caching/SKILL.md:72-72` — "Caching by default; global keys for tenant/user data; mutable data cached indefinitely; cache technology in the domain model; use-case code depending on `HybridCache` without a deliberate decision; caching tracked ORM entities across commit boundaries; cache as authoritative persistence; Redis merely because caching exists."

### EXTRA-L1-0097
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: Publish only artifacts later stages need; where possible build once and promote the same tested artifact/image with runtime configuration.
- Trigger/scope: on-demand knowledge skill ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000907: `output/template/.claude/skills/ci-cd/SKILL.md:85-85` — "Publish only artifacts later stages need. Where the deployment model allows, build once and promote the same tested artifact or image, with environment behavior from runtime configuration. Build and publish container images only when container deployment is part of the project (`docker`)."

### EXTRA-L1-0098
- Closest oracle policies: SEC-002, WF-017
- Modality: PREFER
- Normative action: Prefer workload/federated identity over long-lived credentials; CI and CD may be separate; use environment protection and approvals.
- Trigger/scope: on-demand knowledge skill ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000909: `output/template/.claude/skills/ci-cd/SKILL.md:89-89` — "Use the CI platform's secret or identity mechanism, preferring workload/federated identity over long-lived deployment credentials. CI and CD may be separate workflows; a green CI build does not mean every branch deploys — use environment protection and approvals suited to the platform."

### EXTRA-L1-0099
- Closest oracle policies: WF-019
- Modality: MUST
- Normative action: The migration step fails visibly.
- Trigger/scope: on-demand knowledge skill ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Not in WF-019.
- Evidence L1-S000911: `output/template/.claude/skills/ci-cd/SKILL.md:93-93` — "When deployment migrates the database: an explicit step at a controlled point, approved credentials, visible failure; migration scripts may be generated in CI and executed during deployment (`persistence.commands`)."

### EXTRA-L1-0100
- Closest oracle policies: WF-017, SEC-001
- Modality: MUST
- Normative action: Pipeline verification: clean restore, backend/frontend builds, configured tests, no developer-machine dependency, no exposed secrets, expected artifacts.
- Trigger/scope: on-demand knowledge skill ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000913: `output/template/.claude/skills/ci-cd/SKILL.md:97-97` — "Restores from a clean environment, builds backend and frontend (when present), runs configured tests, does not depend on developer-machine state, exposes no secrets, produces the expected artifacts."

### EXTRA-L1-0101
- Closest oracle policies: WF-017
- Modality: AVOID
- Normative action: Avoid rebuilding different source per environment without reason.
- Trigger/scope: on-demand knowledge skill ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000915: `output/template/.claude/skills/ci-cd/SKILL.md:101-101` — "Project-specific database infrastructure in a generic pipeline; deployment secrets in YAML; rebuilding different source per environment without reason; suppressed failing tests; automatic production seeding or startup migrations; assuming Docker; assuming frontend scripts the repository does not define."

### EXTRA-L1-0102
- Closest oracle policies: WF-012
- Modality: MUST_NOT
- Normative action: Do not apply backend project-boundary rules mechanically to frontend code.
- Trigger/scope: workflow code-review (reviews of completed changes)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000934: `output/template/.claude/skills/code-review/SKILL.md:40-40` — "Apply the frontend rules and the frontend knowledge skill: feature boundaries and component responsibility, HTTP calls behind a data-access boundary, subscription and reactive-state lifetime, frontend error handling, route guards not treated as authorization, unnecessary global/shared state, meaningful frontend tests. Do not apply backend project-boundary rules mechanically to frontend code."

### EXTRA-L1-0103
- Closest oracle policies: WF-011
- Modality: MUST
- Normative action: For each finding give severity, file/location, what is wrong, why it matters and the smallest reasonable fix, ordered by severity.
- Trigger/scope: workflow code-review (reviews of completed changes)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000946: `output/template/.claude/skills/code-review/SKILL.md:64-64` — "For each finding: severity, file/location, what is wrong, why it matters, smallest reasonable fix — ordered by severity:"

### EXTRA-L1-0104
- Closest oracle policies: WF-011
- Modality: DEFINITION
- Normative action: Severity scale: Critical (blocks use/merge), High (fix before merge), Medium, Low.
- Trigger/scope: workflow code-review (reviews of completed changes)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000947: `output/template/.claude/skills/code-review/SKILL.md:66-69` — "- **Critical** — data loss, security vulnerability, reliably broken core behavior; blocks use or merge. ⏎ - **High** — likely defect or architecture/data-integrity issue; fix before merge. ⏎ - **Medium** — real maintainability, robustness, or test gap; not a likely immediate failure. ⏎ - **Low** — non-blocking improvement."

### EXTRA-L1-0105
- Closest oracle policies: GOV-010, RUN-015
- Modality: MUST
- Normative action: Example numbers are illustrative, not approved defaults; derive retry counts, timeouts and limits from the real integration and deployment.
- Trigger/scope: on-demand knowledge skill configuration (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000959: `output/template/.claude/skills/configuration/SKILL.md:36-36` — "Numbers in examples are illustrative, not approved defaults — derive retry counts, timeouts, and limits from the real integration and deployment."
- Evidence L1-S000969: `output/template/.claude/skills/configuration/SKILL.md:76-76` — "Services reading string keys from `IConfiguration`; secrets in committed settings files; `Configure<T>(section)` without validation for settings the app cannot run without; copying example numbers into production configuration."
- Evidence L1-S001218: `output/template/.claude/skills/httpclient-factory/references/resilience.md:18-18` — "- **Timeouts** — set attempt and total-operation timeouts from real latency requirements, not example numbers."
- Evidence L1-S001269: `output/template/.claude/skills/logging/references/serilog.md:45-45` — "Configure only the sinks and enrichers the project needs; a Console sink is enough for a simple local Development baseline. File, Seq, OpenTelemetry, or Elasticsearch sinks are options, not baseline dependencies, and numeric limits below are illustrative."

### EXTRA-L1-0106
- Closest oracle policies: GOV-008
- Modality: MUST
- Normative action: Record an approved setting under a stable descriptive name with value and purpose.
- Trigger/scope: workflow custom-settings (CUSTOM_SETTINGS.md changes)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000975: `output/template/.claude/skills/custom-settings/SKILL.md:14-14` — "1. Record it in `CUSTOM_SETTINGS.md` under a stable descriptive name with its value and purpose."

### EXTRA-L1-0107
- Closest oracle policies: GOV-021, RUN-009
- Modality: AVOID
- Normative action: Avoid copying the same literal across many layers when one source in code or configuration is appropriate.
- Trigger/scope: workflow custom-settings (CUSTOM_SETTINGS.md changes)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000977: `output/template/.claude/skills/custom-settings/SKILL.md:19-19` — "Avoid copying the same literal across many layers when one source in code or configuration is appropriate. Framework defaults the project has not intentionally overridden do not belong in the file."

### EXTRA-L1-0108
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Report the setting, old → new value, every surface updated and the verify result.
- Trigger/scope: workflow custom-settings (CUSTOM_SETTINGS.md changes)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000985: `output/template/.claude/skills/custom-settings/SKILL.md:49-49` — "Report the setting, old → new value, every surface updated, and the `verify` result."

### EXTRA-L1-0109
- Closest oracle policies: ARC-021, ARC-007
- Modality: DEFAULT
- Normative action: Interface-to-implementation registration suits use-case units, repositories and adapters; concrete registration is fine for implementation-only helpers.
- Trigger/scope: on-demand knowledge skill dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000989: `output/template/.claude/skills/dependency-injection/SKILL.md:10-10` — "Rules: constructor injection and lifetime rules (`.claude/rules/0-core/backend-code.md`); where registration lives (frame boundaries). Interface-to-implementation registration suits use-case units, repositories, and adapters; concrete registration is fine for implementation-only helpers. Prefer explicit registration in small and medium projects; add scanning, keyed services, factories, or decorato …"

### EXTRA-L1-0110
- Closest oracle policies: ARC-022, ARC-006
- Modality: MUST
- Normative action: Within that scope resolve a scoped orchestration service, not implementation internals.
- Trigger/scope: on-demand knowledge skill dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000995: `output/template/.claude/skills/dependency-injection/SKILL.md:48-48` — "A singleton or hosted service that needs scoped work creates a scope per operation and resolves a scoped orchestration service, not implementation internals:"

### EXTRA-L1-0111
- Closest oracle policies: ARC-021
- Modality: DEFAULT
- Normative action: Keyed services for several implementations selected by a known key; prefer a single registration or simple factory when clearer.
- Trigger/scope: on-demand knowledge skill dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000999: `output/template/.claude/skills/dependency-injection/SKILL.md:66-66` — "- **Keyed services** — several implementations selected by a known key: `AddKeyedScoped<INotificationService, EmailNotificationService>("email")` and `[FromKeyedServices("email")] INotificationService notifier`. Prefer a single registration or simple factory when clearer."

### EXTRA-L1-0112
- Closest oracle policies: ARC-023
- Modality: MUST
- Normative action: Scan the assembly that owns the services, not just the entry-point assembly.
- Trigger/scope: on-demand knowledge skill dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001001: `output/template/.claude/skills/dependency-injection/SKILL.md:68-68` — "- **Convention scanning** — only when registration volume creates real boilerplate; scan the assembly that owns the services (`scan.FromAssemblyOf<IOrderService>()`), not just the entry-point assembly."

### EXTRA-L1-0113
- Closest oracle policies: RUN-022, SEC-014
- Modality: DEFAULT
- Normative action: Factory delegates for runtime selection throw for unknown configuration values.
- Trigger/scope: on-demand knowledge skill dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001002: `output/template/.claude/skills/dependency-injection/SKILL.md:69-69` — "- **Factory delegate** — runtime selection: `services.AddScoped<IPaymentProcessor>(sp => ... ActivatorUtilities.CreateInstance<StripeProcessor>(sp) ...)`, throwing for unknown configuration values."

### EXTRA-L1-0114
- Closest oracle policies: TST-009
- Modality: MUST
- Normative action: A regression test fails before the fix and passes after it.
- Trigger/scope: workflow development-workflow (feature, bug fix, refactor, performance, persistence, CI/CD or deployment change)
- Exceptions: none
- Why EXTRA: Not in TST-009.
- Evidence L1-S001017: `output/template/.claude/skills/development-workflow/SKILL.md:28-28` — "**Bug fix** — Default: for a meaningful bug with plausible recurrence, add a regression test that fails before the fix and passes after it, unless equivalent coverage already exists."
- Evidence L1-S001086: `output/template/.claude/skills/dotnet-testing/SKILL.md:120-120` — "A regression test reproduces the failure before the fix and passes after it. Converting a temporary probe: a curl, PowerShell, or REST check becomes a host integration test; a manual database check becomes a persistence test; reuse existing coverage when it already exercises the behavior, after confirming it really does."

### EXTRA-L1-0115
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Summarize what changed, Delegated decisions taken and the verify report.
- Trigger/scope: workflow development-workflow (feature, bug fix, refactor, performance, persistence, CI/CD or deployment change)
- Exceptions: none
- Why EXTRA: Report fields not in the oracle.
- Evidence L1-S001029: `output/template/.claude/skills/development-workflow/SKILL.md:54-54` — "Summarize what changed, Delegated decisions taken, open Decision Requests (Reserved), and the `verify` report."

### EXTRA-L1-0116
- Closest oracle policies: DEP-023
- Modality: MUST_NOT
- Normative action: Copy only repository build files that exist and restore needs; do not add them just for the Dockerfile.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001036: `output/template/.claude/skills/docker/SKILL.md:35-35` — "- Copy only repository build files that exist and restore needs; do not add them just for the Dockerfile."

### EXTRA-L1-0117
- Closest oracle policies: DEP-019
- Modality: DEFAULT
- Normative action: Copy project files explicitly before the source tree, update when the structure changes, avoid flattening wildcard tricks.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001037: `output/template/.claude/skills/docker/SKILL.md:36-36` — "- Copy project files explicitly before the source tree so source edits do not invalidate the restore layer; update this section when the solution structure changes; avoid wildcard tricks that flatten the directory structure."

### EXTRA-L1-0118
- Closest oracle policies: DEP-019, SEC-007
- Modality: DEFAULT
- Normative action: Use the built-in non-root user (USER app) of current .NET images.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Not in DEP-019.
- Evidence L1-S001039: `output/template/.claude/skills/docker/SKILL.md:38-38` — "- `USER app` is the built-in non-root user of current .NET images; give writable directories correct ownership."

### EXTRA-L1-0119
- Closest oracle policies: SEC-002
- Modality: MUST
- Normative action: Pass environment-specific configuration at runtime.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001041: `output/template/.claude/skills/docker/SKILL.md:42-42` — "Pass environment-specific configuration at runtime (`ASPNETCORE_ENVIRONMENT`, `ConnectionStrings__Default`, `Authentication__Authority`). Never put real credentials in the Dockerfile, committed Compose files, build arguments (visible in image metadata), or copied settings files; use platform/container secret mechanisms."

### EXTRA-L1-0120
- Closest oracle policies: API-019
- Modality: PREFER
- Normative action: Expose liveness/readiness through health checks, prefer orchestrator HTTP probes, verify in-container probe commands exist or add an explicit probe mechanism weighing image size.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001046: `output/template/.claude/skills/docker/SKILL.md:63-63` — "Expose liveness/readiness through ASP.NET Core health checks (`health-check`) and prefer the orchestrator's native HTTP probes. Runtime images may lack `curl`, `wget`, or a shell — verify any in-container probe command exists or add an explicit probe mechanism, weighing image size."
- Evidence L1-S001057: `output/template/.claude/skills/docker/SKILL.md:93-93` — "SDK image at runtime; root execution without reason; baked-in secrets; arbitrary Compose services; assuming `curl`/`wget`; automatic production migrations; unverified specialized images; Docker concerns leaking into use-case or domain code."

### EXTRA-L1-0121
- Closest oracle policies: DEP-018
- Modality: DEFAULT
- Normative action: Build static frontend assets in a Node stage and serve them with the selected hosting strategy (no mandatory web server); keep API base URLs compatible.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001048: `output/template/.claude/skills/docker/SKILL.md:67-67` — "Build static frontend assets in a Node build stage and serve them with the selected hosting strategy (a dedicated web server is not mandatory). Keep API base URLs compatible with the deployment."

### EXTRA-L1-0122
- Closest oracle policies: DEP-019
- Modality: MUST_NOT
- Normative action: Do not exclude files restore/build needs or tests the image build intentionally runs.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001051: `output/template/.claude/skills/docker/SKILL.md:81-81` — "Do not exclude files restore/build needs, or tests when the image build intentionally runs them."

### EXTRA-L1-0123
- Closest oracle policies: RUN-008, DEP-019
- Modality: DEFAULT
- Normative action: Start with standard images; Alpine/chiseled/trimming/Native AOT only when justified and verified (globalization, native dependencies, reflection, diagnostics).
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001053: `output/template/.claude/skills/docker/SKILL.md:85-85` — "Start with standard supported images. Alpine, chiseled images, trimming, or Native AOT only when compatibility and deployment justify them — verify globalization, native dependencies, reflection, and diagnostics."
- Evidence L1-S001057: `output/template/.claude/skills/docker/SKILL.md:93-93` — "SDK image at runtime; root execution without reason; baked-in secrets; arbitrary Compose services; assuming `curl`/`wget`; automatic production migrations; unverified specialized images; Docker concerns leaking into use-case or domain code."

### EXTRA-L1-0124
- Closest oracle policies: SEC-001, WF-006
- Modality: MUST
- Normative action: Verify container changes: build the image, startup, port, configuration, non-root behaviour, health-probe integration, no secrets or stray files in the image.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001055: `output/template/.claude/skills/docker/SKILL.md:89-89` — "Build the image, verify startup, port, and configuration, non-root behavior when relevant, health-probe integration, and that no secrets or stray files landed in the image; run tests outside or inside the pipeline as chosen."

### EXTRA-L1-0125
- Closest oracle policies: TST-003
- Modality: PREFER
- Normative action: Prefer one observable scenario per test; multi-step tests only when the sequence is the scenario.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001071: `output/template/.claude/skills/dotnet-testing/SKILL.md:62-62` — "Prefer one observable scenario per test; a multi-step test fits when the sequence is the scenario (a whole workflow or replace-set lifecycle)."

### EXTRA-L1-0126
- Closest oracle policies: TST-003
- Modality: ALLOWED
- Normative action: Do not forbid mocking project-owned abstractions when isolation helps.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Explicit permission not in the oracle.
- Evidence L1-S001073: `output/template/.claude/skills/dotnet-testing/SKILL.md:66-66` — "Good unit candidates: non-trivial domain behavior that genuinely belongs to the domain model, calculations, workflow/state transitions at their owning layer, validation logic, orchestration with simple fakes. Replace persistence-access contracts and external abstractions with controlled doubles; assert the use-case result and meaningful side effects. "Method X was called once" is useful only when  …"

### EXTRA-L1-0127
- Closest oracle policies: TST-011, TST-003
- Modality: DEFAULT
- Normative action: Persistence tests target meaningful behaviour (custom mappings, filters, projections, non-trivial queries, relationships, concurrency, provider behaviour), not trivial Add/Get.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001080: `output/template/.claude/skills/dotnet-testing/SKILL.md:110-110` — "- Persistence tests target meaningful behavior — custom mappings, query filters, projections, non-trivial queries, relationships, concurrency, provider behavior — not every trivial `Add`/`Get`."

### EXTRA-L1-0128
- Closest oracle policies: TST-005
- Modality: DEFAULT
- Normative action: Keep test data explicit and minimal; builders/fixtures only when repeated setup hurts readability, no generic data framework for a few objects.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001084: `output/template/.claude/skills/dotnet-testing/SKILL.md:116-116` — "- Keep test data explicit and minimal; add builders/fixtures when repeated setup hurts readability, not a generic data framework for a few objects."

### EXTRA-L1-0129
- Closest oracle policies: TST-005
- Modality: DEFINITION
- Normative action: 'Smoke test' means a small set of fast basic-operation checks, not every integration test; explicit assertions suit small or important contracts.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001090: `output/template/.claude/skills/dotnet-testing/SKILL.md:128-128` — ""Smoke test" means a small set of fast checks that a built or deployed application is basically operational — not every integration test. Coverage percentage is diagnostic only. Snapshot testing can help for large stable outputs but is not added by default; explicit assertions suit small or important contracts."

### EXTRA-L1-0130
- Closest oracle policies: TST-003, TST-010
- Modality: AVOID
- Normative action: Avoid assertion-free tests (unless 'does not throw') and keeping temporary probes as permanent tests without review.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001092: `output/template/.claude/skills/dotnet-testing/SKILL.md:132-132` — "Testing private details; mocking every class; hitting production resources; shared mutable state; assertions that repeat the implementation; assertion-free tests (unless the behavior is "does not throw"); `Task.Delay` to make timing pass; real-provider containers when fidelity is irrelevant; in-memory providers claimed as relational coverage; keeping temporary probes as permanent tests without rev …"

### EXTRA-L1-0131
- Closest oracle policies: ARC-019
- Modality: PREFER
- Normative action: Keep entity configuration in IEntityTypeConfiguration<T> classes.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Mapping technique not in the oracle.
- Evidence L1-S001098: `output/template/.claude/skills/ef-core/SKILL.md:14-14` — "Keep entity configuration in `IEntityTypeConfiguration<T>` classes and persistence-specific configuration out of domain-model entities where practical."

### EXTRA-L1-0132
- Closest oracle policies: RUN-006
- Modality: DEFAULT
- Normative action: Tracking queries for entities to be modified and committed; AsNoTracking() for read-only entity queries; not needed on projections.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Tracking technique (EXC-011 context) phrased as a directive.
- Evidence L1-S001109: `output/template/.claude/skills/ef-core/SKILL.md:78-78` — "- **Tracking** — tracking queries for entities that will be modified and committed; `AsNoTracking()` for read-only entity queries; not needed on projections to non-entity DTOs."

### EXTRA-L1-0133
- Closest oracle policies: RUN-006
- Modality: PREFER
- Normative action: Explicit query shape (projection or Include/ThenInclude for needed graphs); consider split queries for large collection includes and verify the SQL.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Query-shape technique (EXC-011 context).
- Evidence L1-S001111: `output/template/.claude/skills/ef-core/SKILL.md:80-80` — "- **Related data** — explicit query shape: projection for selected related data, `Include`/`ThenInclude` when the graph itself is needed; avoid lazy loading by default (hidden queries, N+1); consider split queries for large collection includes and verify the SQL."

### EXTRA-L1-0134
- Closest oracle policies: RUN-006
- Modality: MUST
- Normative action: Paged queries are ordered deterministically.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001112: `output/template/.claude/skills/ef-core/SKILL.md:81-81` — "- **Pagination** — filter, order deterministically, and page in the database; consider keyset pagination for very large or frequently traversed sets."

### EXTRA-L1-0135
- Closest oracle policies: RUN-021, ARC-016
- Modality: MUST_NOT
- Normative action: ExecuteUpdateAsync/ExecuteDeleteAsync bypass change tracking: do not mix them casually with tracked entities for the same rows; understand their transaction semantics.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001114: `output/template/.claude/skills/ef-core/SKILL.md:90-90` — "- **Bulk operations** — `ExecuteUpdateAsync`/`ExecuteDeleteAsync` run directly against the database and bypass change tracking; do not mix them casually with tracked entities for the same rows; understand their transaction semantics."

### EXTRA-L1-0136
- Closest oracle policies: ARC-019
- Modality: MUST_NOT
- Normative action: Use interceptors for infrastructure cross-cutting behaviour such as auditing; never hide business behaviour in them.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Interceptor technique (EXC-011 context) phrased as a restriction.
- Evidence L1-S001120: `output/template/.claude/skills/ef-core/SKILL.md:98-98` — "Use interceptors for infrastructure cross-cutting behavior such as auditing; never hide business behavior in them."

### EXTRA-L1-0137
- Closest oracle policies: PST-003
- Modality: DEFAULT
- Normative action: Place the Development seeder under Persistence/Seeding/ in the implementation project.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Placement convention not in the oracle.
- Evidence L1-S001123: `output/template/.claude/skills/ef-core/SKILL.md:120-120` — "Placement: `Persistence/Seeding/` in the implementation project. The concrete entities and states must match the current model; when the required graph is complex, ask for the desired dataset instead of inventing a large generic one."

### EXTRA-L1-0138
- Closest oracle policies: GOV-004, PST-001
- Modality: MUST
- Normative action: When the required seed graph is complex ask for the desired dataset instead of inventing a large generic one.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: Complex graph.
- Why EXTRA: Not in the oracle.
- Evidence L1-S001123: `output/template/.claude/skills/ef-core/SKILL.md:120-120` — "Placement: `Persistence/Seeding/` in the implementation project. The concrete entities and states must match the current model; when the required graph is complex, ask for the desired dataset instead of inventing a large generic one."

### EXTRA-L1-0139
- Closest oracle policies: GOV-015
- Modality: MUST_NOT
- Normative action: Treat main, master and other protected or shared branches as non-rewritable.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001134: `output/template/.claude/skills/git-workflow/SKILL.md:16-16` — "- High-risk operations — `git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion, rebasing shared history — run only when explicitly requested or required by an approved workflow, and only after inspecting what will be lost or rewritten. Treat `main`, `master`, and other protected or shared branches as non-rewritable."

### EXTRA-L1-0140
- Closest oracle policies: WF-022
- Modality: PREFER
- Normative action: One logical change per commit with its protecting tests; no artificial micro-commits or bundled unrelated fixes.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001137: `output/template/.claude/skills/git-workflow/SKILL.md:21-21` — "- Prefer one logical change per commit; implementation and the tests protecting it normally belong together. No artificial micro-commits, no unrelated fixes bundled together."

### EXTRA-L1-0141
- Closest oracle policies: WF-022
- Modality: DEFAULT
- Normative action: Follow the repository commit-message convention, otherwise Conventional Commits; use the body for motivation/constraints/migration notes.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001138: `output/template/.claude/skills/git-workflow/SKILL.md:22-22` — "- Follow the repository's commit-message convention; otherwise Conventional Commits are a useful default (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`). Use the body for motivation, constraints, or migration notes; do not narrate the obvious diff."

### EXTRA-L1-0142
- Closest oracle policies: GOV-016
- Modality: DEFAULT
- Normative action: Follow an existing branch-naming convention, otherwise conventional prefixes; do not rename an existing user branch to fit.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001140: `output/template/.claude/skills/git-workflow/SKILL.md:26-26` — "- Follow an existing branch-naming convention; otherwise prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, `chore/` are reasonable. Do not rename an existing user branch to fit."

### EXTRA-L1-0143
- Closest oracle policies: GOV-020
- Modality: MUST
- Normative action: Before pushing confirm the branch, understand working/staged state, ensure verification completed, avoid pushing unrelated commits.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001144: `output/template/.claude/skills/git-workflow/SKILL.md:32-32` — "- Before pushing: confirm the intended branch, understand the working/staged state, ensure relevant verification completed, and avoid pushing unrelated local commits."

### EXTRA-L1-0144
- Closest oracle policies: GOV-020
- Modality: MUST
- Normative action: Choose merge or rebase by convention or request; resolve conflicts by intended combined behaviour, not ours/theirs; run verification afterwards.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001145: `output/template/.claude/skills/git-workflow/SKILL.md:33-33` — "- Choose merge or rebase by repository convention or the user's request, not preference. Inspect uncommitted work first; never stash, reset, or discard automatically to let the operation proceed."
- Evidence L1-S001146: `output/template/.claude/skills/git-workflow/SKILL.md:34-34` — "- Resolve conflicts by the intended combined behavior, not by mechanically taking "ours" or "theirs"; run relevant verification afterwards."

### EXTRA-L1-0145
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Keep the PR focused; describe what changed, why, how it was verified and compatibility/migration notes.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001148: `output/template/.claude/skills/git-workflow/SKILL.md:38-38` — "Run `verify` before preparing a PR. Keep the PR focused; describe what changed, why, how it was verified, and compatibility or migration notes. Never claim checks that were not run."

### EXTRA-L1-0146
- Closest oracle policies: WF-009
- Modality: DEFAULT
- Normative action: When useful report the resulting state (branch, commit, push target, PR status, remaining uncommitted changes).
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: When useful.
- Why EXTRA: Not in the oracle.
- Evidence L1-S001150: `output/template/.claude/skills/git-workflow/SKILL.md:42-42` — "When useful, report the resulting state: branch, commit created, push target, PR status, and uncommitted changes that remain."

### EXTRA-L1-0147
- Closest oracle policies: API-019
- Modality: DEFAULT
- Normative action: Tag the checks that matter for readiness and map the readiness endpoint by tag.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001161: `output/template/.claude/skills/health-check/SKILL.md:30-30` — ""Can this instance serve the traffic it is responsible for?" — tag the checks that matter:"

### EXTRA-L1-0148
- Closest oracle policies: API-018
- Modality: PREFER
- Normative action: Use provider/framework health-check integrations where suitable.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: Where suitable.
- Why EXTRA: Not in the oracle.
- Evidence L1-S001165: `output/template/.claude/skills/health-check/SKILL.md:45-45` — "- Database: a lightweight connectivity check; use provider/framework integrations where suitable."

### EXTRA-L1-0149
- Closest oracle policies: API-019
- Modality: MUST_NOT
- Normative action: Health endpoints return success/non-success per probe policy (ResultStatusCodes); do not reuse business API status semantics mechanically.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001168: `output/template/.claude/skills/health-check/SKILL.md:50-50` — "Health endpoints return success when healthy and non-success when unhealthy per the probe policy (`HealthCheckOptions.ResultStatusCodes`); do not reuse business API status semantics mechanically. Keep probe responses small; put detailed diagnostics behind network or authorization controls for operators."

### EXTRA-L1-0150
- Closest oracle policies: API-020
- Modality: DEFAULT
- Normative action: Choose probe exposure by deployment topology (private network, management port, host restrictions, supported authorization); prefer orchestrator HTTP probes.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001170: `output/template/.claude/skills/health-check/SKILL.md:54-54` — "Probes often need access without user authentication: use private networks, a management port, host restrictions, or authorization the probe infrastructure supports, chosen by deployment topology. Prefer the orchestrator's native HTTP probes."

### EXTRA-L1-0151
- Closest oracle policies: RUN-013
- Modality: AVOID
- Normative action: Avoid Error-level logs for every normal failed probe.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001172: `output/template/.claude/skills/health-check/SKILL.md:58-58` — "Probes run frequently: avoid long external timeouts, large allocations, and Error-level logs for every normal failed probe."

### EXTRA-L1-0152
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: When deployment relies on health configuration test liveness, readiness against required dependencies, no sensitive leaks and optional dependency behaviour; skip tests of uncustomized framework behaviour.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: Deployment relies on it.
- Why EXTRA: Not in the oracle.
- Evidence L1-S001174: `output/template/.claude/skills/health-check/SKILL.md:62-62` — "When deployment relies on health configuration, test that live responds while healthy, readiness follows required dependencies, responses leak nothing sensitive, and optional dependencies behave as intended. Skip elaborate tests for uncustomized framework behavior."

### EXTRA-L1-0153
- Closest oracle policies: API-018
- Modality: AVOID
- Normative action: Do not use health checks as a quality grading system.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001176: `output/template/.claude/skills/health-check/SKILL.md:66-66` — "Health checks as a quality grading system; writes or business transactions in probes; every dependency on liveness; expensive queries; secrets or stack traces in payloads; remote dependency chains without operational justification."

### EXTRA-L1-0154
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: Keep status behaviour consistent across similar endpoints (e.g. one convention for repeated DELETE of an absent resource: 204 or 404).
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001180: `output/template/.claude/skills/http-api/SKILL.md:10-10` — "Rules: `.claude/rules/0-core/http-api.md` (response, failure, versioning rules) and the role rule that HTTP semantics belong to the entry point. Keep status behavior consistent across similar endpoints."
- Evidence L1-S001186: `output/template/.claude/skills/http-api/SKILL.md:22-22` — "- **204 No Content** — success with no body (`DELETE`, updates where returning the representation adds nothing); a `204` never carries a body. Choose one convention for repeated `DELETE` of an absent resource — `204` (final state holds) or `404` (resource absent) — and apply it consistently across equivalent resources."

### EXTRA-L1-0155
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: Include Location (CreatedAtAction) when a stable URI exists.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: Stable URI exists.
- Why EXTRA: Not in the oracle.
- Evidence L1-S001183: `output/template/.claude/skills/http-api/SKILL.md:15-15` — "- **201 Created** — the HTTP operation created a new API resource; include `Location` when a stable URI exists. `PUT` may return `201` when it creates the target resource."
- Evidence L1-S001485: `output/template/.claude/skills/swagger/SKILL.md:48-48` — "Consider the whole pipeline when listing responses — model binding, validation, authentication/authorization, rate limiting, centralized exception handling, other middleware — not only explicit action branches. Document `201` with `CreatedAtAction`/`CreatedAtRoute` when a canonical URL exists; never `201` for an endpoint returning `200` or `204` for one returning a body. Describe `ProblemDetails`/ …"

### EXTRA-L1-0156
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: Return an operation id or Location where 202 progress is observable.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001185: `output/template/.claude/skills/http-api/SKILL.md:21-21` — "- **202 Accepted** — processing accepted but incomplete (long-running operation, background job, async import, queued work); return an operation id or a `Location` where progress is observable: `AcceptedAtAction(nameof(GetOperation), new { id = operationId }, response)`."

### EXTRA-L1-0157
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: 304 only for conditional requests with a still-valid cached representation; never a generic 'nothing changed' business response.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: EXC-009 context.
- Evidence L1-S001187: `output/template/.claude/skills/http-api/SKILL.md:23-23` — "- **304 Not Modified** — only for conditional requests (`If-None-Match`/ETag, `If-Modified-Since`) when the cached representation is still valid; never a generic "nothing changed" business response."

### EXTRA-L1-0158
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: 406 when no acceptable representation can be produced; 415 for unsupported request body formats.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: EXC-009 context.
- Evidence L1-S001192: `output/template/.claude/skills/http-api/SKILL.md:30-30` — "- **406 Not Acceptable** — the server cannot produce a representation the client accepts (response negotiation). **415 Unsupported Media Type** — the server does not support the request body format (`Content-Type: application/xml` on a JSON-only endpoint)."

### EXTRA-L1-0159
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: 422 for structurally valid but semantically invalid requests; follow an established 400-for-both convention; new distinguishing APIs use 400 for contract errors and 422 for semantics.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: Established convention.
- Why EXTRA: Not in the oracle.
- Evidence L1-S001195: `output/template/.claude/skills/http-api/SKILL.md:33-33` — "- **422 Unprocessable Content** — structurally valid request with invalid semantics or business input (`startDate > endDate`, business rejection that is not a state conflict). Some APIs use `400` for both; follow an established convention. New APIs that distinguish them: `400` = invalid HTTP/request contract, `422` = valid structure, invalid semantics."

### EXTRA-L1-0160
- Closest oracle policies: API-006
- Modality: MUST
- Normative action: 428 when the contract requires a precondition the client omitted (missing If-Match → 428; stale → 412).
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Not in API-006.
- Evidence L1-S001196: `output/template/.claude/skills/http-api/SKILL.md:34-34` — "- **428 Precondition Required** — the contract requires a precondition the client omitted (missing required `If-Match` → `428`; stale `If-Match` → `412`)."
- Evidence L1-S001205: `output/template/.claude/skills/http-api/SKILL.md:48-48` — "For HTTP-level optimistic concurrency prefer standard conditional requests: `GET` → `ETag: "v7"`; `PUT`/`PATCH` with `If-Match: "v7"`; unchanged → success; changed → `412`; required but absent → `428`. Do not replace these with custom status codes."

### EXTRA-L1-0161
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: 429 for rate-limited requests with Retry-After when known; never for validation failures.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001197: `output/template/.claude/skills/http-api/SKILL.md:35-35` — "- **429 Too Many Requests** — rate limiting rejected the request; include `Retry-After` when known. Never use it for validation failures."

### EXTRA-L1-0162
- Closest oracle policies: API-003
- Modality: MUST_NOT
- Normative action: 502/504 only when acting as an intermediary (invalid upstream response / upstream timeout); do not map every dependency failure to 502.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: EXC-009 context.
- Evidence L1-S001200: `output/template/.claude/skills/http-api/SKILL.md:40-40` — "- **502 Bad Gateway** — this API acts as an intermediary and received an invalid or unusable upstream response; do not map every dependency failure to `502`."
- Evidence L1-S001202: `output/template/.claude/skills/http-api/SKILL.md:42-42` — "- **504 Gateway Timeout** — as an intermediary, the upstream did not answer in time. Distinguish client cancellation, our own timeout, and upstream timeout; not every `TaskCanceledException` is a `504`."

### EXTRA-L1-0163
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: 503 for temporary inability (maintenance, critical dependency unavailable, overload) with Retry-After when meaningful.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001201: `output/template/.claude/skills/http-api/SKILL.md:41-41` — "- **503 Service Unavailable** — temporarily unable to serve (maintenance, a critical dependency unavailable for this operation, overload); include `Retry-After` when meaningful."

### EXTRA-L1-0164
- Closest oracle policies: RUN-016
- Modality: DEFAULT
- Normative action: For a POST that must not duplicate effects consider an Idempotency-Key stored with request/result per the contract.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001204: `output/template/.claude/skills/http-api/SKILL.md:46-46` — "`GET` is safe and idempotent; `PUT` is idempotent; `DELETE` is idempotent in intended final state; `POST` generally is not. For a `POST` that must not create duplicate effects, consider an `Idempotency-Key` stored with the request/result per the contract; claim idempotency only when it is implemented."

### EXTRA-L1-0165
- Closest oracle policies: RUN-005
- Modality: DEFAULT
- Normative action: Named, typed and keyed clients are all valid; choose the simplest for consumer and lifetime; keyed only when keyed DI is clearer; no single mandatory model.
- Trigger/scope: on-demand knowledge skill httpclient-factory (backend outbound HTTP)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001241: `output/template/.claude/skills/httpclient-factory/SKILL.md:30-30` — "Named, typed, and keyed clients are all valid; choose the simplest one for the consumer and lifetime."
- Evidence L1-S001243: `output/template/.claude/skills/httpclient-factory/SKILL.md:37-37` — "Keyed clients fit when keyed DI makes consumption clearer — not automatically. Do not capture a transient typed client inside a singleton without understanding the lifetime consequences."
- Evidence L1-S001260: `output/template/.claude/skills/httpclient-factory/SKILL.md:88-88` — "Per-request `HttpClient`; mandating one client model everywhere; retries on unsafe operations without idempotency analysis; unbounded retries; leaking `HttpResponseMessage`; ignored cancellation; dynamic tokens in shared default headers; mapping every upstream failure to one status; resilience pipelines added without understanding their behavior."

### EXTRA-L1-0166
- Closest oracle policies: ARC-025
- Modality: MUST_NOT
- Normative action: DelegatingHandler only for genuine pipeline concerns (tokens, correlation, signing), never business decisions.
- Trigger/scope: on-demand knowledge skill httpclient-factory (backend outbound HTTP)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001245: `output/template/.claude/skills/httpclient-factory/SKILL.md:41-41` — "Use a `DelegatingHandler` for genuine pipeline concerns — token acquisition, correlation propagation, request signing — never for business decisions:"

### EXTRA-L1-0167
- Closest oracle policies: ARC-025
- Modality: MUST_NOT
- Normative action: Do not call EnsureSuccessStatusCode() blindly when specific statuses carry meaning.
- Trigger/scope: on-demand knowledge skill httpclient-factory (backend outbound HTTP)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001250: `output/template/.claude/skills/httpclient-factory/SKILL.md:61-61` — "Translate remote responses into the abstraction's outcomes; do not call `EnsureSuccessStatusCode()` blindly when specific statuses carry meaning:"

### EXTRA-L1-0168
- Closest oracle policies: API-003, ARC-025
- Modality: MUST_NOT
- Normative action: Do not forward every upstream status to the own API or map every upstream failure to one status; outbound retry and inbound response are separate decisions.
- Trigger/scope: on-demand knowledge skill httpclient-factory (backend outbound HTTP)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001252: `output/template/.claude/skills/httpclient-factory/SKILL.md:72-72` — "Do not forward every upstream status code to your own API; outbound retry behavior and the inbound response your API returns are separate decisions."
- Evidence L1-S001260: `output/template/.claude/skills/httpclient-factory/SKILL.md:88-88` — "Per-request `HttpClient`; mandating one client model everywhere; retries on unsafe operations without idempotency analysis; unbounded retries; leaking `HttpResponseMessage`; ignored cancellation; dynamic tokens in shared default headers; mapping every upstream failure to one status; resilience pipelines added without understanding their behavior."

### EXTRA-L1-0169
- Closest oracle policies: RUN-005
- Modality: MUST_NOT
- Normative action: Stable headers on the client, per-request values per request or via a handler; never mutate shared DefaultRequestHeaders concurrently.
- Trigger/scope: on-demand knowledge skill httpclient-factory (backend outbound HTTP)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001256: `output/template/.claude/skills/httpclient-factory/SKILL.md:80-80` — "Configure stable headers (media types) on the client; apply per-request values such as dynamic tokens per request or through a handler — never mutate shared `DefaultRequestHeaders` concurrently. Prefer `System.Net.Http.Json` / `System.Text.Json`, with explicit options when the remote contract differs; do not reuse domain entities as remote contracts."
- Evidence L1-S001260: `output/template/.claude/skills/httpclient-factory/SKILL.md:88-88` — "Per-request `HttpClient`; mandating one client model everywhere; retries on unsafe operations without idempotency analysis; unbounded retries; leaking `HttpResponseMessage`; ignored cancellation; dynamic tokens in shared default headers; mapping every upstream failure to one status; resilience pipelines added without understanding their behavior."

### EXTRA-L1-0170
- Closest oracle policies: ARC-025, ARC-002
- Modality: MUST_NOT
- Normative action: Prefer System.Net.Http.Json/System.Text.Json with explicit options when contracts differ; do not reuse domain entities as remote contracts.
- Trigger/scope: on-demand knowledge skill httpclient-factory (backend outbound HTTP)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001256: `output/template/.claude/skills/httpclient-factory/SKILL.md:80-80` — "Configure stable headers (media types) on the client; apply per-request values such as dynamic tokens per request or through a handler — never mutate shared `DefaultRequestHeaders` concurrently. Prefer `System.Net.Http.Json` / `System.Text.Json`, with explicit options when the remote contract differs; do not reuse domain entities as remote contracts."

### EXTRA-L1-0171
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Test adapters with a controlled HttpMessageHandler (method/path, headers, payload, mapping, cancellation/failure).
- Trigger/scope: on-demand knowledge skill httpclient-factory (backend outbound HTTP)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001258: `output/template/.claude/skills/httpclient-factory/SKILL.md:84-84` — "A controlled `HttpMessageHandler` verifies method/path, headers, payload, response mapping, and cancellation/failure behavior. `new HttpClient(testHandler) { BaseAddress = new Uri("https://example.test/") }` is fine in a focused test — the lifetime rule concerns production code."

### EXTRA-L1-0172
- Closest oracle policies: RUN-016
- Modality: MUST_NOT
- Normative action: Transient: selected network failures, temporary unavailability, rate limiting when allowed, transient provider database failures; never validation, auth failures, permanent 404 or deterministic business rejection.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: Explicit categories beyond RUN-016.
- Evidence L1-S001219: `output/template/.claude/skills/httpclient-factory/references/resilience.md:19-19` — "- **Retry** — plausibly transient failures only: selected network failures, temporary unavailability, rate limiting when retry is allowed, transient provider-specific database failures. Never validation errors, authentication/authorization failures, permanent `404`, deterministic business rejection, or non-idempotent operations without duplicate prevention. Ask: if the first attempt succeeded remo …"

### EXTRA-L1-0173
- Closest oracle policies: RUN-016
- Modality: MUST_NOT
- Normative action: Do not invent a client-side Idempotency-Key unless the remote service supports it.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: Not in RUN-016.
- Evidence L1-S001219: `output/template/.claude/skills/httpclient-factory/references/resilience.md:19-19` — "- **Retry** — plausibly transient failures only: selected network failures, temporary unavailability, rate limiting when retry is allowed, transient provider-specific database failures. Never validation errors, authentication/authorization failures, permanent `404`, deterministic business rejection, or non-idempotent operations without duplicate prevention. Ask: if the first attempt succeeded remo …"

### EXTRA-L1-0174
- Closest oracle policies: RUN-015
- Modality: DEFAULT
- Normative action: Circuit breakers when repeated calls to a failing dependency add load/latency, with production visibility; skip without a repeated-failure scenario.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: EXC-007 context.
- Evidence L1-S001221: `output/template/.claude/skills/httpclient-factory/references/resilience.md:21-21` — "- **Circuit breaker** — when repeated calls to a failing dependency add load or latency; give it operational visibility in production; skip it without a repeated-failure scenario."

### EXTRA-L1-0175
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: Inbound rate limiting is separate from outbound resilience; rejected requests get 429 with Retry-After when useful.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001224: `output/template/.claude/skills/httpclient-factory/references/resilience.md:24-24` — "- **Inbound rate limiting** — ASP.NET Core rate limiting protects this API and is separate from outbound resilience; rejected requests get `429` with `Retry-After` when useful (`http-api`)."

### EXTRA-L1-0176
- Closest oracle policies: RUN-016
- Modality: MUST_NOT
- Normative action: Do not wrap normal ORM operations in a generic application retry pipeline; prefer the provider execution strategy; HTTP retry policies are not database policies.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: EXC-007 context.
- Evidence L1-S001226: `output/template/.claude/skills/httpclient-factory/references/resilience.md:28-28` — "Do not wrap normal ORM operations in a generic application-level retry pipeline; prefer the provider's own execution strategy and handle transaction/retry interaction per the persistence knowledge skill. HTTP retry policies are not database policies."

### EXTRA-L1-0177
- Closest oracle policies: RUN-016
- Modality: DEFAULT
- Normative action: Publication retries can duplicate delivery; use idempotent consumers, deduplication or an outbox when needed; never claim exactly-once because a retry exists.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: When needed.
- Why EXTRA: Not in the oracle.
- Evidence L1-S001228: `output/template/.claude/skills/httpclient-factory/references/resilience.md:32-32` — "Retrying publication can duplicate delivery; use idempotent consumers, broker deduplication, or an outbox when the business needs it, and never claim exactly-once delivery because a retry exists."

### EXTRA-L1-0178
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Observe retry counts, timeouts, circuit state, rate-limit rejections and dependency latency where operationally important, with the adopted telemetry stack.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: Where operationally important.
- Why EXTRA: Not in the oracle.
- Evidence L1-S001230: `output/template/.claude/skills/httpclient-factory/references/resilience.md:36-36` — "Observe retry counts, timeout frequency, circuit state, rate-limit rejections, and dependency latency where operationally important, using the telemetry stack the project adopted; resilience alone does not require OpenTelemetry."

### EXTRA-L1-0179
- Closest oracle policies: RUN-013
- Modality: DEFAULT
- Normative action: Levels by operational meaning: Trace/Debug diagnostics, Information for meaningful events (not every call), Warning for recovered/degraded states, Error for failures needing attention, Critical when the application cannot continue.
- Trigger/scope: on-demand knowledge skill logging (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001289: `output/template/.claude/skills/logging/SKILL.md:21-25` — "- **Trace/Debug** — detailed troubleshooting diagnostics (still never a safe place for sensitive data). ⏎ - **Information** — meaningful application events: a background job completed, an important business operation finished, lifecycle events. Not every method call. ⏎ - **Warning** — unexpected or degraded but recovered: fallback used, optional dependency unavailable, unusual handled state. ⏎ - * …"

### EXTRA-L1-0180
- Closest oracle policies: RUN-013
- Modality: PREFER
- Normative action: Prefer platform trace identifiers; explicit correlation ids only for a concrete need; propagate tracing context across outbound calls.
- Trigger/scope: on-demand knowledge skill logging (backend)
- Exceptions: none
- Why EXTRA: EXC-013 context.
- Evidence L1-S001294: `output/template/.claude/skills/logging/SKILL.md:40-40` — "Prefer platform trace identifiers when they already correlate requests; add an explicit correlation id only for a concrete integration or operational need, validate or normalize ids accepted from clients, and propagate tracing context across outbound calls with the chosen tracing/HTTP infrastructure."

### EXTRA-L1-0181
- Closest oracle policies: RUN-013
- Modality: AVOID
- Normative action: Do not use logs as an audit database without an adopted audit design.
- Trigger/scope: on-demand knowledge skill logging (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001301: `output/template/.claude/skills/logging/SKILL.md:60-60` — "Interpolated log messages; duplicate exception logging; expected outcomes logged as errors; credentials or secrets in logs; dumping whole objects without review; provider-specific APIs throughout use-case code; logs used as an audit database without an adopted audit design."

### EXTRA-L1-0182
- Closest oracle policies: DEP-021
- Modality: DEFAULT
- Normative action: Two-stage bootstrap when startup failures must be logged before DI/configuration exist; host-managed setup otherwise.
- Trigger/scope: private reference of on-demand skill logging (Serilog)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001265: `output/template/.claude/skills/logging/references/serilog.md:9-9` — "Two-stage bootstrap is worthwhile when startup failures must be logged before DI and configuration exist; simpler applications can use host-managed setup only."

### EXTRA-L1-0183
- Closest oracle policies: DEP-021
- Modality: MUST
- Normative action: Flush the static/bootstrap logger on shutdown when used; host-managed logging follows the provider lifetime.
- Trigger/scope: private reference of on-demand skill logging (Serilog)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001267: `output/template/.claude/skills/logging/references/serilog.md:41-41` — "Flush the static/bootstrap logger on shutdown when it is used (async sinks lose buffered events otherwise); purely host-managed logging follows the provider's lifetime instead."

### EXTRA-L1-0184
- Closest oracle policies: DEP-004
- Modality: MUST_NOT
- Normative action: Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- Trigger/scope: private reference of on-demand skill logging (Serilog)
- Exceptions: Elasticsearch chosen.
- Why EXTRA: Not in the oracle.
- Evidence L1-S001279: `output/template/.claude/skills/logging/references/serilog.md:95-95` — "The `Serilog.Sinks.Elasticsearch` package is deprecated; use `Elastic.Serilog.Sinks` when Elasticsearch is the chosen log store. OTLP export is available through `Serilog.Sinks.OpenTelemetry` without the OpenTelemetry SDK."

### EXTRA-L1-0185
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: Use a regular constructor when validation/initialization is non-trivial, explicit fields read better, the codebase uses that style or capture would obscure the class.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001311: `output/template/.claude/skills/modern-csharp/SKILL.md:22-22` — "Use a regular constructor when validation or initialization is non-trivial, explicit fields read better, the codebase consistently uses that style, or parameter capture would obscure the class. Never convert constructors mechanically."

### EXTRA-L1-0186
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Records for intentional value semantics (immutable DTOs, value objects, messages); identity/lifecycle entities stay classes unless record semantics genuinely help.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001313: `output/template/.claude/skills/modern-csharp/SKILL.md:26-26` — "Records fit intentional value semantics: immutable transport DTOs, genuine value objects, immutable messages. Entities with identity and lifecycle stay classes unless record semantics genuinely help; inheritance or framework behavior may also favor classes. Avoid `record struct` merely to dodge allocations."

### EXTRA-L1-0187
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: required for valid-construction contracts (not invariant validation); collection expressions when the target type is clear; patterns/switch when they clarify, no deep nesting; field keyword to remove trivial backing fields.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001315: `output/template/.claude/skills/modern-csharp/SKILL.md:30-30` — "- `required` when initialization is part of the valid-construction contract (`public required string Name { get; init; }`) — not a substitute for invariant validation."
- Evidence L1-S001316: `output/template/.claude/skills/modern-csharp/SKILL.md:31-31` — "- Collection expressions when the target type is clear (`string[] names = ["Alice", "Bob"];`); do not rewrite existing initializers just to modernize."
- Evidence L1-S001317: `output/template/.claude/skills/modern-csharp/SKILL.md:32-32` — "- Pattern matching and switch expressions when they clarify branching; avoid deeply nested patterns."
- Evidence L1-S001318: `output/template/.claude/skills/modern-csharp/SKILL.md:33-33` — "- `field` keyword (C# 14) to remove a trivial backing field:"

### EXTRA-L1-0188
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: var when the type is obvious or unimportant; explicit types when they aid understanding; follow the project convention.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001323: `output/template/.claude/skills/modern-csharp/SKILL.md:56-56` — "- `var` when the type is obvious or unimportant; explicit types when they aid understanding; follow the project's convention."

### EXTRA-L1-0189
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Keep implementation details non-public; sealed to communicate non-inheritance, not as a speculative JIT optimization.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001325: `output/template/.claude/skills/modern-csharp/SKILL.md:60-60` — "- Keep implementation details non-public when they are not part of the project's public API; use `sealed` when it communicates that a type is not designed for inheritance, not as a speculative JIT optimization."

### EXTRA-L1-0190
- Closest oracle policies: RUN-024
- Modality: DEFAULT
- Normative action: PascalCase types/methods/properties/public members, camelCase parameters/locals, meaningful names, private-field naming per convention.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Beyond RUN-024.
- Evidence L1-S001326: `output/template/.claude/skills/modern-csharp/SKILL.md:61-61` — "- Standard .NET naming: PascalCase for types, methods, properties, and public members; camelCase for parameters and locals; meaningful names over abbreviations; private-field naming per repository convention."

### EXTRA-L1-0191
- Closest oracle policies: RUN-024
- Modality: ALLOWED
- Normative action: Small private or nested supporting types may stay with their owner for locality.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001327: `output/template/.claude/skills/modern-csharp/SKILL.md:62-62` — "- Small private or nested supporting types may stay with their owning type when that improves locality; do not reorganize a file only to satisfy a preferred member order."

### EXTRA-L1-0192
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: Prefer immutability when it models the domain naturally, not where controlled mutation is simpler.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001328: `output/template/.claude/skills/modern-csharp/SKILL.md:63-63` — "- Prefer immutability when it models the domain naturally, not where controlled mutation is simpler."

### EXTRA-L1-0193
- Closest oracle policies: RUN-009
- Modality: MUST
- Normative action: Confirm the configured language version supports a feature.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001332: `output/template/.claude/skills/modern-csharp/SKILL.md:71-71` — "Confirm the configured language version supports a feature; changing `LangVersion` or the target framework requires approval."

### EXTRA-L1-0194
- Closest oracle policies: DEP-008, ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Changing LangVersion or the target framework requires approval.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: DEP-008 gates only preview/RC moves.
- Evidence L1-S001332: `output/template/.claude/skills/modern-csharp/SKILL.md:71-71` — "Confirm the configured language version supports a feature; changing `LangVersion` or the target framework requires approval."

### EXTRA-L1-0195
- Closest oracle policies: DEP-024
- Modality: DEFAULT
- Normative action: Frontend unit/component tests stay inside the frontend workspace (colocated); E2E, when used, under frontend/<Name>.Web/e2e/.
- Trigger/scope: workflow project-structure (solution creation, projects, references, repository layout)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001348: `output/template/.claude/skills/project-structure/references/solution-layout.md:29-29` — "The frontend workspace owns its manifest, lockfile, framework configuration, and sources. Do not impose an obsolete directory structure when the current CLI generates a different supported one. Frontend tests stay inside the workspace (colocated unit/component tests; E2E under `e2e/` when used) — never under `backend/`."
- Evidence L1-S001370: `output/template/.claude/skills/project-structure/SKILL.md:26-26` — "7. **Test projects** — only useful ones, placed and referenced per `architecture.layout`, scaffolded with `backend-testing.commands`. Frontend unit/component tests stay inside the frontend workspace; E2E (when used) under `frontend/<Name>.Web/e2e/`."

### EXTRA-L1-0196
- Closest oracle policies: DEP-006
- Modality: DEFAULT
- Normative action: Package placement: validation in the use-case project; logging provider, Swashbuckle and Asp.Versioning in the entry-point project; resilience in the implementation project; Mvc.Testing in the integration-test project.
- Trigger/scope: private reference of workflow project-structure (baseline packages, Development configuration)
- Exceptions: none
- Why EXTRA: Placement convention not in the oracle.
- Evidence L1-S001339: `output/template/.claude/skills/project-structure/references/baseline-packages.md:9-16` — "| Validation | `FluentValidation`, `FluentValidation.DependencyInjectionExtensions` | use-case project | baseline when validation is needed | ⏎ | Logging provider | `Serilog.AspNetCore` (+ sinks only when required; Console is enough locally) | entry-point project | baseline | ⏎ | Interactive API docs | `Swashbuckle.AspNetCore` | entry-point project | baseline | ⏎ | Host integration tests | `Micros …"

### EXTRA-L1-0197
- Closest oracle policies: WF-006
- Modality: DEFAULT
- Normative action: Configure the launch profile so a Development run can open /swagger when helpful, with HTTP/HTTPS URLs consistent with the profile.
- Trigger/scope: private reference of workflow project-structure (baseline packages, Development configuration)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001342: `output/template/.claude/skills/project-structure/references/baseline-packages.md:22-22` — "The entry-point project carries `appsettings.json` and `appsettings.Development.json`. The local database connection default follows the persistence dev-config rule; real usernames, passwords, tokens, production hosts, and production connection strings are never committed. Configure the launch profile so a Development run can open `/swagger` directly when that helps, keeping HTTP/HTTPS URLs consis …"

### EXTRA-L1-0198
- Closest oracle policies: DEP-008, DEP-023
- Modality: DEFAULT
- Normative action: Pin the intended SDK line in global.json with a rollForward policy allowing normal patch/feature-band servicing.
- Trigger/scope: private reference of workflow project-structure (repository layout)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001352: `output/template/.claude/skills/project-structure/references/solution-layout.md:35-35` — "- `global.json` — pin the intended SDK line: the current stable SDK of the target .NET release (no RC/preview unless explicitly requested), with a `rollForward` policy that allows normal patch/feature-band servicing."

### EXTRA-L1-0199
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: Keep deterministic formatting/code style in .editorconfig; prefer enforceable tooling over restating mechanical formatting in instructions.
- Trigger/scope: private reference of workflow project-structure (repository layout)
- Exceptions: none
- Why EXTRA: Repo/meta preference.
- Evidence L1-S001353: `output/template/.claude/skills/project-structure/references/solution-layout.md:36-36` — "- `.editorconfig` — deterministic formatting and code-style configuration; prefer enforceable tooling configuration over restating mechanical formatting rules in instructions."

### EXTRA-L1-0200
- Closest oracle policies: SEC-001
- Modality: DEFAULT
- Normative action: Ignore generated and local artifacts (bin, obj, .vs, node_modules, dist, TestResults, coverage, local secret/config overrides).
- Trigger/scope: private reference of workflow project-structure (repository layout)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001355: `output/template/.claude/skills/project-structure/references/solution-layout.md:40-40` — "Ignore generated and local artifacts: `bin/`, `obj/`, `.vs/`, `node_modules/`, `dist/`, `TestResults/`, `coverage/`, local secret/config overrides. Do not ignore files that are intentionally part of the Development configuration contract."
- Evidence L1-S001556: `output/template/.gitignore:2-12` — "bin/ ⏎ obj/ ⏎ .vs/ ⏎ TestResults/ ⏎ coverage/ ⏎ *.user ⏎  ⏎ # Frontend ⏎ node_modules/ ⏎ dist/ ⏎ .angular/"
- Evidence L1-S001558: `output/template/.gitignore:20-21` — "# Claude Code hook state ⏎ .claude/.hook-state/"

### EXTRA-L1-0201
- Closest oracle policies: WF-020, WF-009
- Modality: MUST
- Normative action: State in every report that static review is not a penetration test and may miss runtime, infrastructure, business-logic, authorization-bypass, deployment and dynamic-exploitation issues.
- Trigger/scope: workflow security-scan (security scan, audit, targeted security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001443: `output/template/.claude/skills/security-scan/SKILL.md:10-10` — "Evidence-based static review of the repository. It is not a penetration test and cannot prove the application secure: it may miss runtime-only vulnerabilities, infrastructure outside the repository, complex business-logic abuse, sophisticated authorization bypasses, deployment-specific weaknesses, and anything requiring dynamic exploitation. State that limitation in every report. Security invarian …"
- Evidence L1-S001472: `output/template/.claude/skills/security-scan/SKILL.md:111-111` — "All applicable layers inspected, findings carry evidence, uncertain items are labeled, severity reflects actual risk, limitations are stated, and no layer is marked `PASS` without being checked."

### EXTRA-L1-0202
- Closest oracle policies: WF-020
- Modality: DEFAULT
- Normative action: OWASP categories are an awareness taxonomy: map only when it genuinely fits.
- Trigger/scope: workflow security-scan (security scan, audit, targeted security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001459: `output/template/.claude/skills/security-scan/SKILL.md:54-54` — "OWASP categories (A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging & Alerting Failures, A10 Mishandling of Exceptional Conditions) are an awareness taxonomy: map only when it genuinely fits."

### EXTRA-L1-0203
- Closest oracle policies: WF-020
- Modality: DEFINITION
- Normative action: Severity scale Critical (sparingly), High, Medium, Low, Info (hardening observation).
- Trigger/scope: workflow security-scan (security scan, audit, targeted security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001463: `output/template/.claude/skills/security-scan/SKILL.md:62-66` — "- **Critical** — use sparingly: exposed real production credentials, reachable authentication bypass, straightforward remote code execution, exploitable injection with major impact. ⏎ - **High** — realistically exploitable or substantially compromises data, authorization, or system behavior. ⏎ - **Medium** — meaningful weakness needing realistic conditions, limited access, or extra steps. ⏎ - **Lo …"

### EXTRA-L1-0204
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: Name technique skills instead of copying guidance into the report; each confirmed finding states severity, location, title, evidence, why it is a risk, impact, smallest remediation and OWASP category when applicable.
- Trigger/scope: workflow security-scan (security scan, audit, targeted security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001466: `output/template/.claude/skills/security-scan/SKILL.md:72-72` — "Name technique skills instead of copying their guidance into the report. Each confirmed finding: severity, file and location, title, evidence, why it is a risk, likely impact, smallest reasonable remediation, OWASP category when applicable. Label uncertain items `NEEDS VERIFICATION`."

### EXTRA-L1-0205
- Closest oracle policies: WF-020, WF-009
- Modality: DEFAULT
- Normative action: Report shape: Scope, Limitations, severity Summary, Findings, Layer Results.
- Trigger/scope: workflow security-scan (security scan, audit, targeted security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001467: `output/template/.claude/skills/security-scan/SKILL.md:74-101` — "```markdown ⏎ # Security Scan Report ⏎  ⏎ Scope: ... ⏎ Limitations: Static analysis only. This does not replace penetration testing, dynamic testing, threat modeling, or infrastructure review. ⏎  ⏎ ## Summary ⏎ | Severity | Count | ⏎ |---|---:| ⏎ | Critical | 0 | ⏎ | High | 0 | ⏎ | Medium | 0 | ⏎ | Low | 0 | ⏎ | Info | 0 | ⏎  ⏎ ## Findings ⏎ ### [HIGH] File:Line — Finding title ⏎ OWASP: A01:2025 B …"

### EXTRA-L1-0206
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED.
- Trigger/scope: workflow security-scan (security scan, audit, targeted security review)
- Exceptions: none
- Why EXTRA: Vocabulary differs from WF-009.
- Evidence L1-S001468: `output/template/.claude/skills/security-scan/SKILL.md:103-103` — "Layer status is `PASS`, `FINDINGS`, `NOT APPLICABLE`, or `NOT CHECKED` — never `PASS` for an uninspected layer."

### EXTRA-L1-0207
- Closest oracle policies: SEC-003
- Modality: PREFER
- Normative action: Prefer APIs separating executable and arguments and constrain input for command execution.
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001401: `output/template/.claude/skills/security-scan/references/scan-layers.md:24-24` — "- **Command injection** — `Process.Start`, shell/PowerShell invocation, arguments built from user input; prefer APIs separating executable and arguments; constrain input."

### EXTRA-L1-0208
- Closest oracle policies: SEC-003, SEC-015
- Modality: MUST
- Normative action: Normalize and verify user-controlled paths stay inside the intended root.
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001402: `output/template/.claude/skills/security-scan/references/scan-layers.md:25-25` — "- **Path traversal** — user-controlled file names, paths, archive extraction, download/upload destinations; look for `../`, absolute-path injection, unsafe extraction; normalize and verify paths stay inside the intended root."

### EXTRA-L1-0209
- Closest oracle policies: WF-020
- Modality: DEFAULT
- Normative action: Consider rate limiting where abuse realistically matters (login, password reset, expensive anonymous or resource-intensive endpoints); not required everywhere.
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001419: `output/template/.claude/skills/security-scan/references/scan-layers.md:46-46` — "- **Rate limiting** — consider it where abuse realistically matters (login, password reset, expensive anonymous or resource-intensive endpoints); not required everywhere. 429 semantics: `http-api`."

### EXTRA-L1-0210
- Closest oracle policies: WF-020, WF-012
- Modality: MUST
- Normative action: Name security-sensitive workflows (tenant isolation, workflow abuse, privilege escalation, idempotency abuse, multi-step authorization) as threat-modeling/manual-review candidates instead of claiming the scan proves them secure.
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001433: `output/template/.claude/skills/security-scan/references/scan-layers.md:66-66` — "Static checks do not cover insecure design, tenant isolation, business workflow abuse, privilege escalation through legitimate operations, financial/idempotency abuse, or multi-step authorization problems. Name meaningful security-sensitive workflows as candidates for threat modeling or dedicated manual review instead of claiming the scan proves them secure."

### EXTRA-L1-0211
- Closest oracle policies: WF-020
- Modality: DEFAULT
- Normative action: Finding format: [SEVERITY] path:line — title, OWASP, Evidence, Impact, Remediation.
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001437: `output/template/.claude/skills/security-scan/references/scan-layers.md:77-83` — "```markdown ⏎ ### [HIGH] src/.../File.cs:42 — Resource authorization missing ⏎ OWASP: A01:2025 Broken Access Control ⏎ Evidence: The endpoint loads an order solely by route ID and does not constrain it to the authenticated customer. ⏎ Impact: An authenticated user who learns another order ID may access that customer's order. ⏎ Remediation: Apply resource/ownership authorization before returning th …"

### EXTRA-L1-0212
- Closest oracle policies: ARC-012
- Modality: DEFAULT
- Normative action: Keep Swagger configuration in the entry-point/composition code.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001479: `output/template/.claude/skills/swagger/SKILL.md:29-29` — "Keep Swagger configuration in the entry-point/composition code. Do not make `AddOpenApi()`/`MapOpenApi()` the default when the requirement is Swagger UI testing."

### EXTRA-L1-0213
- Closest oracle policies: WF-006
- Modality: MUST_NOT
- Normative action: Keep application URLs consistent with the launch profile; never a launch URL pointing to HTTPS on an HTTP-only port.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001482: `output/template/.claude/skills/swagger/SKILL.md:37-37` — "Keep application URLs consistent with the profile — never a launch URL pointing to HTTPS on an HTTP-only port."

### EXTRA-L1-0214
- Closest oracle policies: DEP-012
- Modality: DEFAULT
- Normative action: Add a Bearer scheme so authenticated endpoints can be exercised from Swagger UI.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: Bearer used.
- Why EXTRA: Not in the oracle.
- Evidence L1-S001487: `output/template/.claude/skills/swagger/SKILL.md:52-52` — "When the API really uses authentication, add the matching security definition and requirements (a Bearer scheme so authenticated endpoints can be exercised from the UI). Do not add a scheme merely because a package is installed, and do not apply requirements globally to anonymous endpoints."

### EXTRA-L1-0215
- Closest oracle policies: API-016
- Modality: DEFAULT
- Normative action: Describe consumer-relevant preconditions, idempotency, pagination/filtering and outcomes, not restated names; XML comments optional for public contracts.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001489: `output/template/.claude/skills/swagger/SKILL.md:56-56` — "Describe what helps consumers: preconditions, idempotency, pagination/filtering, meaningful outcomes — not restated names. XML comments are optional for public contracts. Use multiple documents only for a real contract separation (API versions — see `api-versioning` — or public vs internal surfaces)."

### EXTRA-L1-0216
- Closest oracle policies: API-016, API-015
- Modality: MUST_NOT
- Normative action: Use multiple Swagger documents only for a real contract separation (versions, public vs internal).
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001489: `output/template/.claude/skills/swagger/SKILL.md:56-56` — "Describe what helps consumers: preconditions, idempotency, pagination/filtering, meaningful outcomes — not restated names. XML comments are optional for public contracts. Use multiple documents only for a real contract separation (API versions — see `api-versioning` — or public vs internal surfaces)."

### EXTRA-L1-0217
- Closest oracle policies: API-016, API-014
- Modality: AVOID
- Normative action: Avoid anonymous response shapes / anonymous objects as long-lived contracts; use explicit request/response contracts.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001491: `output/template/.claude/skills/swagger/SKILL.md:60-60` — "When the contract feeds client generation: treat breaking schema changes seriously, keep metadata accurate, avoid anonymous response shapes, use explicit request/response contracts, review generated-client diffs."
- Evidence L1-S001495: `output/template/.claude/skills/swagger/SKILL.md:68-68` — "Metadata disagreeing with runtime; public Swagger UI without a reason; Swagger as a substitute for integration tests; global auth requirements on anonymous endpoints; anonymous objects as long-lived contracts; a second competing documentation stack without need."

### EXTRA-L1-0218
- Closest oracle policies: TST-002
- Modality: MUST_NOT
- Normative action: Swagger is not a substitute for integration tests.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001495: `output/template/.claude/skills/swagger/SKILL.md:68-68` — "Metadata disagreeing with runtime; public Swagger UI without a reason; Swagger as a substitute for integration tests; global auth requirements on anonymous endpoints; anonymous objects as long-lived contracts; a second competing documentation stack without need."

### EXTRA-L1-0219
- Closest oracle policies: none
- Modality: MUST
- Normative action: Place content by kind: normative constraint → rule; procedure → workflow skill; technique → knowledge skill/private reference; product facts → product inputs; mechanical check → hook, script or configuration.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta placement rule.
- Evidence L1-S001501: `output/template/.claude/skills/template-maintenance/SKILL.md:15-15` — "1. **Kind of content** — normative constraint → rule; multi-step procedure → workflow skill; technique/examples → knowledge skill or private reference; product facts → `SPECIFICATION.md` / `CUSTOM_SETTINGS.md`; mechanical check → hook, script, or configuration."

### EXTRA-L1-0220
- Closest oracle policies: none
- Modality: MUST
- Normative action: Content specific to a selected slot implementation goes into that module's facets with a Capability header; everything else uses roles and <slot>.<facet> references, never implementation names.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Capability-system rule (repo/meta).
- Evidence L1-S001503: `output/template/.claude/skills/template-maintenance/SKILL.md:17-17` — "3. **Capability** — content specific to a selected slot implementation goes into that module's facets (`.claude/capabilities/<slot>/<implementation>/MODULE.md` lists them) and declares `Capability:`; everything else uses roles and `<slot>.<facet>` references, never implementation names."

### EXTRA-L1-0221
- Closest oracle policies: none
- Modality: MUST
- Normative action: Always-needed planning policy in CLAUDE.md or an imported always rule; path-specific policy in a rule whose paths cover its scope; procedure obligations in the owning workflow.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta placement rule.
- Evidence L1-S001504: `output/template/.claude/skills/template-maintenance/SKILL.md:18-18` — "4. **Trigger** — always-needed planning policy goes into `CLAUDE.md` or an imported always rule; path-specific policy into a rule whose `paths` cover at least its scope; procedure obligations into the owning workflow."

### EXTRA-L1-0222
- Closest oracle policies: none
- Modality: MUST
- Normative action: Add each rule once; elsewhere use a pointer or a yes/no check naming the owner.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta ownership rule.
- Evidence L1-S001505: `output/template/.claude/skills/template-maintenance/SKILL.md:19-19` — "5. **One owner** — add the rule once; elsewhere use a pointer or a yes/no check that names the owner."

### EXTRA-L1-0223
- Closest oracle policies: none
- Modality: MUST
- Normative action: Update INSTRUCTION_MAP.md (level tables, capability view, policy locator) for instruction changes.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta rule.
- Evidence L1-S001508: `output/template/.claude/skills/template-maintenance/SKILL.md:24-24` — "2. Update `.claude/INSTRUCTION_MAP.md` (level tables, capability view, policy locator)."

### EXTRA-L1-0224
- Closest oracle policies: ARC-020, GOV-017
- Modality: MUST
- Normative action: Capability replacement or removal follows the slot CONTRACT.md and module MODULE.md and records an ADR with architecture-decision.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance)
- Exceptions: Capability replacement/removal.
- Why EXTRA: Repo/meta procedure.
- Evidence L1-S001509: `output/template/.claude/skills/template-maintenance/SKILL.md:25-25` — "3. For a capability replacement or removal, follow the slot `CONTRACT.md` and module `MODULE.md`; record the ADR with `architecture-decision`."

### EXTRA-L1-0225
- Closest oracle policies: none
- Modality: MUST_NOT
- Normative action: Keep the always-loaded surface compact; do not move path/workflow policy into it to simplify loading nor always-needed policy out of it to save tokens.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta rule.
- Evidence L1-S001513: `output/template/.claude/skills/template-maintenance/SKILL.md:34-34` — "5. Keep the always-loaded surface compact (`CLAUDE.md` plus its imports and skill descriptions); do not move path or workflow policy into it to simplify loading, and do not move always-needed policy out of it to save tokens."

### EXTRA-L1-0226
- Closest oracle policies: WF-005
- Modality: MUST_NOT
- Normative action: Do not use --no-restore unless restore is known to be complete.
- Trigger/scope: workflow verify (before declaring a change finished or preparing a PR)
- Exceptions: Restore known complete.
- Why EXTRA: Not in the oracle.
- Evidence L1-S001524: `output/template/.claude/skills/verify/SKILL.md:25-25` — "Build the affected solution or projects (`dotnet build`, or a targeted project/solution path); for frontend changes use the build command from `frontend.commands`. Do not use `--no-restore` unless restore is known to be complete. A build failure means the implementation is not complete."

### EXTRA-L1-0227
- Closest oracle policies: WF-005, TST-002
- Modality: DEFAULT
- Normative action: Small solutions run the full suite; large ones run affected projects first, then the broader suite the risk requires.
- Trigger/scope: workflow verify (before declaring a change finished or preparing a PR)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001526: `output/template/.claude/skills/verify/SKILL.md:29-29` — "Run tests covering the changed area (`backend-testing.commands`; frontend: the configured test script per `frontend.commands`). For small solutions run the full suite; for large ones run affected test projects first, then any broader suite the change risk requires. Investigate every newly failing relevant test — do not dismiss a failure as unrelated without checking it."

### EXTRA-L1-0228
- Closest oracle policies: WF-004
- Modality: MUST
- Normative action: Final diff has no commented-out code, temporary logging, unintended TODO/FIXME markers or stale temporary tests/scripts.
- Trigger/scope: workflow verify (before declaring a change finished or preparing a PR)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001538: `output/template/.claude/skills/verify/SKILL.md:53-53` — "After all fixes, review the final diff for accidental unrelated edits, commented-out code, temporary logging, unintended TODO/FIXME markers, stale temporary tests or scripts, architecture drift, unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`, stale code/tests/docs/config after a settings change, and behavior verified manually but never preserved as a test."

### EXTRA-L1-0229
- Closest oracle policies: RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: UTF-8, final newline, trimmed trailing whitespace (not Markdown), space indentation 4 by default and 2 for JSON/YAML/TS/HTML/CSS/Markdown and MSBuild/XML files.
- Trigger/scope: all repository files (editor/analyzer configuration)
- Exceptions: none
- Why EXTRA: Concrete formatting settings beyond RUN-009.
- Evidence L1-S001545: `output/template/.editorconfig:4-18` — "[*] ⏎ charset = utf-8 ⏎ insert_final_newline = true ⏎ trim_trailing_whitespace = true ⏎ indent_style = space ⏎ indent_size = 4 ⏎  ⏎ [*.{json,yml,yaml,ts,html,scss,css,md}] ⏎ indent_size = 2 ⏎  ⏎ [*.{csproj,props,targets,slnx,xml,config}] ⏎ indent_size = 2 ⏎  ⏎ [*.md] ⏎ trim_trailing_whitespace = false"

### EXTRA-L1-0230
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: System directives first, no separated import groups, usings outside the namespace (suggestion).
- Trigger/scope: all repository files (editor/analyzer configuration)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001548: `output/template/.editorconfig:23-25` — "dotnet_sort_system_directives_first = true ⏎ dotnet_separate_import_directive_groups = false ⏎ csharp_using_directive_placement = outside_namespace:suggestion"

### EXTRA-L1-0231
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: var when the type is apparent; explicit types for built-ins (suggestions).
- Trigger/scope: all repository files (editor/analyzer configuration)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001550: `output/template/.editorconfig:29-32` — "# var: when the type is apparent; explicit type when it aids clarity ⏎ csharp_style_var_for_built_in_types = false:suggestion ⏎ csharp_style_var_when_type_is_apparent = true:suggestion ⏎ csharp_style_var_elsewhere = false:silent"

### EXTRA-L1-0232
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: Braces always (suggestion); new line before open brace for all constructs.
- Trigger/scope: all repository files (editor/analyzer configuration)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S001552: `output/template/.editorconfig:40-42` — "# Braces and layout ⏎ csharp_prefer_braces = true:suggestion ⏎ csharp_new_line_before_open_brace = all"

### EXTRA-L1-0233
- Closest oracle policies: RUN-024
- Modality: ENFORCED_ADVISORY
- Normative action: PascalCase types and members, I-prefixed interfaces, camelCase parameters and locals (suggestions).
- Trigger/scope: all repository files (editor/analyzer configuration)
- Exceptions: none
- Why EXTRA: Beyond RUN-024.
- Evidence L1-S001553: `output/template/.editorconfig:44-62` — "# Naming: PascalCase types and members, camelCase parameters and locals, I-prefixed interfaces ⏎ dotnet_naming_symbols.types_and_members.applicable_kinds = class, struct, interface, enum, delegate, method, property, event ⏎ dotnet_naming_style.pascal_case.capitalization = pascal_case ⏎ dotnet_naming_rule.types_and_members_pascal.symbols = types_and_members ⏎ dotnet_naming_rule.types_and_members_pa …"

### EXTRA-L1-0022
- Closest oracle policies: DEP-025, ARC-001
- Modality: ENFORCED
- Normative action: The PreToolUse gate fails closed: empty, malformed or incomplete input and any internal failure block the command (exit 2); settings.json sets onFailure block for launch failures, crashes and timeouts.
- Trigger/scope: every Bash/PowerShell tool call (PreToolUse), governed active root
- Exceptions: none
- Why EXTRA: Fail-closed enforcement policy not in the oracle.
- Evidence L1-S000057: `output/template/.claude/hooks/pre-shell-command.mjs:156-165` — "async function main() { ⏎   let input; ⏎   try { ⏎     input = await readStdinJson(); ⏎   } catch (error) { ⏎     block(error.message); ⏎   } ⏎   const command = input.tool_input && input.tool_input.command; ⏎   if (typeof command !== 'string' || !command.trim()) block('Hook input has no tool_input.command.');"
- Evidence L1-S000065: `output/template/.claude/hooks/pre-shell-command.mjs:197-197` — "main().catch((error) => block(`internal failure: ${error.message}`));"
- Evidence L1-S000407: `output/template/.claude/settings.json:7-7` — "{ "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-shell-command.mjs"], "timeout": 15, "onFailure": "block" }"

### EXTRA-L1-0023
- Closest oracle policies: DEP-025
- Modality: ENFORCED
- Normative action: Peer-bypass commands receive an 'ask' permission decision: they run if the user explicitly confirms.
- Trigger/scope: every Bash/PowerShell tool call (PreToolUse), governed active root
- Exceptions: Explicit user confirmation.
- Why EXTRA: User-confirmed override path not stated in DEP-025.
- Evidence L1-S000059: `output/template/.claude/hooks/pre-shell-command.mjs:168-170` — "if (verdict.force) { ⏎     decide('ask', 'Peer-dependency bypass flag (--force / -f / --legacy-peer-deps) detected. The add-dependency workflow requires resolving the actual compatibility problem; confirm only if the user explicitly wants this.'); ⏎   }"

### EXTRA-L1-0024
- Closest oracle policies: ARC-001, ARC-020
- Modality: ENFORCED
- Normative action: dotnet add/remove … reference and dotnet reference add/remove commands receive an 'ask' decision: Reserved unless they implement the approved layout; confirm only with that approval.
- Trigger/scope: every Bash/PowerShell tool call (PreToolUse), governed active root
- Exceptions: Implements the approved layout.
- Why EXTRA: Reference-graph gate beyond the oracle.
- Evidence L1-S000052: `output/template/.claude/hooks/pre-shell-command.mjs:78-88` — "function dotnetVerdict(args, out) { ⏎   const { positionals } = splitArgs('dotnet', args); ⏎   const [sub, a1, a2] = positionals.map((p) => p.toLowerCase()); ⏎   if (sub === 'add' || sub === 'remove') { ⏎     const noun = a1 === 'package' || a1 === 'reference' ? a1 : a2; ⏎     if (noun === 'package') out.dependency = true; ⏎     if (noun === 'reference') out.reference = true; ⏎   } else if (sub == …"
- Evidence L1-S000060: `output/template/.claude/hooks/pre-shell-command.mjs:171-173` — "if (verdict.reference) { ⏎     decide('ask', 'Project-reference graph change detected. Changing the project reference graph is Reserved (CLAUDE.md § Decision control) unless it implements the approved layout (architecture.layout via project-structure); confirm only with that approval. The architecture check validates the resulting graph.'); ⏎   }"
- Evidence L1-S001368: `output/template/.claude/skills/project-structure/SKILL.md:24-24` — "5. **Project references** — add only the references `architecture.layout` shows; never an outward reference to make compilation easier. The project-graph hook asks for confirmation of every reference command; confirm only references the approved layout shows."

### EXTRA-L1-0025
- Closest oracle policies: DEP-004
- Modality: ENFORCED
- Normative action: A dependency command is denied the first time and allowed when the identical command is retried within 30 minutes; deny-once state lives in the active worktree.
- Trigger/scope: every Bash/PowerShell tool call (PreToolUse), governed active root
- Exceptions: Identical retry within the grace window.
- Why EXTRA: Deny-once mechanism not in the oracle.
- Evidence L1-S000046: `output/template/.claude/hooks/pre-shell-command.mjs:14-14` — "const GRACE_MS = 30 * 60 * 1000;"
- Evidence L1-S000062: `output/template/.claude/hooks/pre-shell-command.mjs:176-193` — "const stateDir = hookStateDir(active); ⏎   const stateFile = path.join(stateDir, 'dependency-commands.json'); ⏎   const now = Date.now(); ⏎   let state = {}; ⏎   if (existsSync(stateFile)) { ⏎     try { state = JSON.parse(readFileSync(stateFile, 'utf8')); } catch { state = {}; } ⏎   } ⏎   for (const [key, ts] of Object.entries(state)) if (now - ts > GRACE_MS) delete state[key]; ⏎  ⏎   const key =  …"

### EXTRA-L1-0026
- Closest oracle policies: DEP-004
- Modality: ENFORCED_ADVISORY
- Normative action: Package ids or versions using MSBuild properties are flagged because the hook does not evaluate MSBuild; confirm the resolved package/version is allowed and pinned.
- Trigger/scope: edits (Edit/Write/MultiEdit/NotebookEdit) and Bash/PowerShell calls (success and failure) in the governed active root
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000033: `output/template/.claude/hooks/post-change-checks.mjs:51-57` — "function checkNugetIds(ids, rules, rel, findings) { ⏎   for (const id of ids) { ⏎     if (/\$\(/.test(id || '')) { findings.push(`${rel}: package id '${id}' uses an MSBuild property; the hook does not evaluate MSBuild, so confirm the resolved package is allowed (owner: add-dependency).`); continue; } ⏎     for (const r of packageMatches(id, rules.nugetDenied)) findings.push(`${rel}: '${id}' must n …"
- Evidence L1-S000035: `output/template/.claude/hooks/post-change-checks.mjs:68-78` — "function checkPackagesProps(rel, text, rules, findings) { ⏎   const props = parsePackagesProps(text); ⏎   if (!props.central) findings.push(`${rel}: ManagePackageVersionsCentrally must stay true (owner: ${PCM}).`); ⏎   for (const { id, version } of props.versions) { ⏎     if (!id) continue; ⏎     if (/\$\(/.test(version)) findings.push(`${rel}: '${id}' version '${version}' uses an MSBuild property …"

### EXTRA-L1-0027
- Closest oracle policies: DEP-020, DEP-004, API-010
- Modality: ENFORCED_ADVISORY
- Normative action: Microsoft.Extensions.Http.Polly, Polly.Extensions.Http, FluentValidation.AspNetCore and Serilog.Sinks.Elasticsearch are flagged as packages that must not be added.
- Trigger/scope: edits (Edit/Write/MultiEdit/NotebookEdit) and Bash/PowerShell calls (success and failure) in the governed active root
- Exceptions: none
- Why EXTRA: Concrete deny list not in the oracle.
- Evidence L1-S000022: `output/template/.claude/hooks/manifest-policy.json:4-9` — ""denied": [ ⏎       { "id": "Microsoft.Extensions.Http.Polly", "reason": "deprecated integration; use Microsoft.Extensions.Http.Resilience", "owner": "add-dependency" }, ⏎       { "id": "Polly.Extensions.Http", "reason": "deprecated integration; use Microsoft.Extensions.Http.Resilience", "owner": "add-dependency" }, ⏎       { "id": "FluentValidation.AspNetCore", "reason": "deprecated automatic-val …"
- Evidence L1-S000033: `output/template/.claude/hooks/post-change-checks.mjs:51-57` — "function checkNugetIds(ids, rules, rel, findings) { ⏎   for (const id of ids) { ⏎     if (/\$\(/.test(id || '')) { findings.push(`${rel}: package id '${id}' uses an MSBuild property; the hook does not evaluate MSBuild, so confirm the resolved package is allowed (owner: add-dependency).`); continue; } ⏎     for (const r of packageMatches(id, rules.nugetDenied)) findings.push(`${rel}: '${id}' must n …"

### EXTRA-L1-0028
- Closest oracle policies: ARC-020, DEP-006
- Modality: ENFORCED_ADVISORY
- Normative action: Removed or moved manifests are reported: a removed/moved .csproj changes the project set/reference graph (Reserved unless the approved layout); a removed package file removes configuration the package-management rule relies on.
- Trigger/scope: edits (Edit/Write/MultiEdit/NotebookEdit) and Bash/PowerShell calls (success and failure) in the governed active root
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000041: `output/template/.claude/hooks/post-change-checks.mjs:193-222` — "function shellFlow(input) { ⏎   const { active, config } = resolveRoots(input.cwd); ⏎   const current = snapshot(active); ⏎   const previous = loadState(active); ⏎   const before = previous && previous.mode === current.mode ? previous.files : null; ⏎   const changed = []; ⏎   const removed = []; ⏎   for (const [rel, id] of Object.entries(current.files)) if (!before || before[rel] !== id) changed.p …"

### EXTRA-L1-0029
- Closest oracle policies: PST-010, PST-009
- Modality: ENFORCED_ADVISORY
- Normative action: At Stop, model changes without a migration prompt confirming no schema change is needed.
- Trigger/scope: Stop event in the governed active root
- Exceptions: none
- Why EXTRA: Model→migration co-change reminder not in the oracle.
- Evidence L1-S000019: `output/template/.claude/capabilities/persistence/ef-core/enforcement.json:6-12` — ""cochange": { ⏎     "modelRoles": ["domain-model"], ⏎     "modelPathGlobs": ["backend/*.Infrastructure/Persistence/Configurations/**"], ⏎     "seederPathGlobs": ["backend/*.Infrastructure/Persistence/Seeding/**"], ⏎     "migrationPathGlobs": ["backend/*.Infrastructure/Persistence/Migrations/**"], ⏎     "owner": "persistence.workflow (.claude/capabilities/persistence/ef-core/workflow.md)" ⏎   }"
- Evidence L1-S000074: `output/template/.claude/hooks/stop-cochange.mjs:55-62` — "if (persistence && persistence.cochange) { ⏎       const c = persistence.cochange; ⏎       const model = touched([...(c.modelRoles || []).flatMap((r) => roleGlobs[r] || []), ...(c.modelPathGlobs || [])]).filter((f) => !/\.csproj$/i.test(f)); ⏎       if (model.length > 0) { ⏎         if (touched(c.seederPathGlobs).length === 0) reminders.push({ id: 'seed', text: `Domain/persistence model files chan …"

### EXTRA-L1-0030
- Closest oracle policies: TST-009, TST-010
- Modality: ENFORCED_ADVISORY
- Normative action: At Stop, backend production code changes without test changes prompt confirming coverage, regression tests and probe preservation.
- Trigger/scope: Stop event in the governed active root
- Exceptions: none
- Why EXTRA: General test co-change reminder not in the oracle.
- Evidence L1-S000075: `output/template/.claude/hooks/stop-cochange.mjs:63-67` — "const productionGlobs = Object.entries(roleGlobs).filter(([role]) => role !== 'tests').flatMap(([, globs]) => globs); ⏎     const production = files.filter((f) => f.endsWith('.cs') && matchesAny(f, productionGlobs)); ⏎     if (production.length > 0 && touched(roleGlobs.tests || []).length === 0) { ⏎       reminders.push({ id: 'tests', text: 'Backend production code changed without test changes: co …"
- Evidence L1-S000415: `output/template/.claude/settings.json:36-36` — "{ "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/stop-cochange.mjs"], "timeout": 15 }"

### EXTRA-L1-0031
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: The Stop hook blocks once per change state; Claude must handle each item or state briefly that it is handled/not applicable, then finish; never loops.
- Trigger/scope: Stop event in the governed active root
- Exceptions: none
- Why EXTRA: Hook procedure (repo/meta).
- Evidence L1-S000079: `output/template/.claude/hooks/stop-cochange.mjs:84-87` — "output({ ⏎     decision: 'block', ⏎     reason: `Co-change check (shown once per change state):\n- ${reminders.map((r) => r.text).join('\n- ')}\nIf an item is already handled or not applicable, say so briefly and finish.`, ⏎   });"

### EXTRA-L1-0032
- Closest oracle policies: DEP-011, DEP-002
- Modality: ENFORCED_ADVISORY
- Normative action: Packages prefixed AutoMapper are flagged as a Reserved library addition (Mapster is the approved option).
- Trigger/scope: manifest checks
- Exceptions: User approved.
- Why EXTRA: Not in the oracle.
- Evidence L1-S000023: `output/template/.claude/hooks/manifest-policy.json:10-13` — ""approvalRequired": [ ⏎       { "id": "Polly", "reason": "direct Polly usage is a documented exception to the Microsoft resilience packages", "owner": "add-dependency" }, ⏎       { "prefix": "AutoMapper", "reason": "another mapping framework is a Reserved library addition (Mapster is the approved option)", "owner": "CLAUDE.md § Decision control" } ⏎     ]"

### EXTRA-L1-0033
- Closest oracle policies: ARC-027, ARC-020
- Modality: ENFORCED_ADVISORY
- Normative action: Backend projects whose names match no frame role, production projects referencing test packages and references that do not resolve to mapped projects raise warnings.
- Trigger/scope: backend project files of the active root
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L1-S000010: `output/template/.claude/capabilities/backend-testing/nunit/enforcement.json:3-3` — ""testProjectMarkerPackages": ["NUnit", "NUnit3TestAdapter", "Microsoft.NET.Test.Sdk"],"
- Evidence L1-S000392: `output/template/.claude/scripts/check-architecture.mjs:65-73` — "for (const p of projects) { ⏎     const isMarkedTest = p.info.packages.some((pkg) => markers.includes((pkg.id || '').toLowerCase())); ⏎     if (!p.role) { ⏎       warnings.push(`${p.rel}: project name matches no role of the selected frame${isMarkedTest ? ' (references test packages)' : ''}; review placement (architecture.layout)`); ⏎       continue; ⏎     } ⏎     if (isMarkedTest && !p.role.test)  …"
- Evidence L1-S000393: `output/template/.claude/scripts/check-architecture.mjs:74-88` — "for (const ref of p.info.projects) { ⏎       const target = byPath.get(path.resolve(path.dirname(p.file), ref.replace(/\\/g, '/')).toLowerCase()); ⏎       if (!target || !target.role) { ⏎         warnings.push(`${p.rel}: reference '${ref}' does not resolve to a mapped backend project`); ⏎         continue; ⏎       } ⏎       if (!p.role.test && target.role.test) { ⏎         violations.push(`${p.rel …"

## LINK_UNCERTAIN constraints (2)

### UNCERTAIN-L1-0001
- Closest oracle policies: RUN-021
- Modality: ALLOWED
- Normative action: Invalidating before the mutation is known to succeed is permitted when it is a deliberate choice.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: Deliberate choice.
- Open question: Open question: RUN-021 requires invalidation only consistent with successful underlying mutations; whether a deliberate pre-mutation invalidation is a permitted exception or a relaxation that contradicts RUN-021 cannot be decided from the text.
- Evidence L1-S000875: `output/template/.claude/skills/caching/SKILL.md:49-49` — "- Invalidation strategies: remove affected keys after a successful mutation, short TTL with tolerated staleness, tag/group invalidation, versioned keys. Invalidating before the mutation is known to succeed must be a deliberate choice."

### UNCERTAIN-L1-0002
- Closest oracle policies: GOV-015
- Modality: ALLOWED
- Normative action: High-risk operations (reset --hard, clean, force push, force-with-lease, branch deletion, rebasing shared history) run only when explicitly requested or required by an approved workflow.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: Explicit request or approved workflow.
- Open question: Open question: GOV-015 permits repository-changing Git operations only when explicitly requested; whether 'required by an approved workflow' widens that condition or only describes an explicitly requested workflow cannot be decided from the text.
- Evidence L1-S001134: `output/template/.claude/skills/git-workflow/SKILL.md:16-16` — "- High-risk operations — `git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion, rebasing shared history — run only when explicitly requested or required by an approved workflow, and only after inspecting what will be lost or rewritten. Treat `main`, `master`, and other protected or shared branches as non-rewritable."

