# EXTRA and LINK_UNCERTAIN constraints — candidate M1

Generated deterministically from the annotation ledger. Each entry cites the exact
source evidence (path, line range, verbatim quote). `policy_ids` on an EXTRA entry
name the closest oracle policy only; origin stays EXTRA.

## EXTRA constraints (248)

### EXTRA-M1-0025
- Closest oracle policies: none
- Modality: MUST
- Normative action: Placement belongs to the architecture frame; technique belongs to leaf capabilities.
- Trigger/scope: capability maintenance (contract read during capability maintenance; JSON enforced by check-instructions.js)
- Exceptions: none
- Why EXTRA: Capability-system ownership rule (repo/meta), not an oracle policy.
- Evidence M1-S000174: `output/template/.claude/capabilities/architecture/CONTRACT.md:10-11` — "Binding rule: placement belongs to the frame; technique belongs"
- Evidence M1-S000242: `output/template/.claude/capabilities/persistence/CONTRACT.md:7-9` — "It binds to frame roles; it"

### EXTRA-M1-0026
- Closest oracle policies: none
- Modality: MUST
- Normative action: A leaf that must name a frame-specific project or directory declares a binds entry in its manifest (enforced by check-instructions.js).
- Trigger/scope: capability maintenance (contract read during capability maintenance; JSON enforced by check-instructions.js)
- Exceptions: none
- Why EXTRA: Capability-system rule (repo/meta).
- Evidence M1-S000178: `output/template/.claude/capabilities/architecture/CONTRACT.md:27-28` — "Leaf capabilities bind to these roles. A leaf that must name a frame-specific ⏎ project or directory declares a `binds` entry in its manifest."
- Evidence M1-S000435: `output/template/.claude/scripts/check-instructions.js:383-390` — "for (const m of modules) { ⏎     for (const b of m.manifest.binds || []) { ⏎       const [slot, impl] = String(b.target).split('/'); ⏎       if (!modules.some((x) => x.slot === slot && x.implementation === impl)) add('ERROR', m.file, `binds target is not selected: ${b.target}`); ⏎       if (!b.reason) add('ERROR', m.file, `binds entry needs a reason: ${b.target}`); ⏎       if (slot === 'architectu …"

### EXTRA-M1-0027
- Closest oracle policies: ARC-020
- Modality: MUST
- Normative action: A replacement frame must supply every role mapping and facet; a frame replacement reviews embedded rules that use layer names.
- Trigger/scope: capability maintenance (contract read during capability maintenance; JSON enforced by check-instructions.js)
- Exceptions: Only on frame replacement.
- Why EXTRA: Capability replacement procedure not in the oracle.
- Evidence M1-S000183: `output/template/.claude/capabilities/architecture/CONTRACT.md:41-44` — "A replacement frame must supply every role mapping and facet above. Embedded ⏎ rules (error handling, API, performance, security) use the frame's layer names ⏎ as project vocabulary, so a frame replacement reviews them as part of the ⏎ change."

### EXTRA-M1-0028
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Selected modules must provide every contract-required facet at the role-named location, every required property and every required enforcement data entry (check-instructions.js errors otherwise).
- Trigger/scope: capability maintenance (contract read during capability maintenance; JSON enforced by check-instructions.js)
- Exceptions: none
- Why EXTRA: Capability conformance invariant (repo/meta).
- Evidence M1-S000185: `output/template/.claude/capabilities/architecture/CONTRACT.md:48-58` — ""slot": "architecture", ⏎   "slotType": "frame", ⏎   "required": true, ⏎   "requiredFacets": { ⏎     "planning": "docs/capabilities/architecture.md", ⏎     "rules": ".claude/rules/architecture.md", ⏎     "placement": ".claude/skills/project-structure/references/backend-layout.md" ⏎   }, ⏎   "requiredProperties": ["adoptedStyle", "roleMap", "patternsNotAdopted", "repositoryLayout"], ⏎   "requiredEn …"
- Evidence M1-S000200: `output/template/.claude/capabilities/backend-testing/CONTRACT.md:38-48` — ""slot": "backend-testing", ⏎   "slotType": "leaf", ⏎   "required": true, ⏎   "requiredFacets": { ⏎     "planning": "docs/capabilities/backend-testing.md", ⏎     "rules": ".claude/rules/test-framework.md", ⏎     "knowledge": null ⏎   }, ⏎   "requiredProperties": ["framework", "packages", "caseMechanism", "fixtureLifecycle", "filterCommand"], ⏎   "requiredEnforcement": ["testFrameworkPackages", "com …"
- Evidence M1-S000237: `output/template/.claude/capabilities/frontend/CONTRACT.md:41-51` — ""slot": "frontend", ⏎   "slotType": "leaf", ⏎   "required": false, ⏎   "requiredFacets": { ⏎     "planning": "docs/capabilities/frontend.md", ⏎     "rules": ".claude/rules/frontend-framework.md", ⏎     "knowledge": null ⏎   }, ⏎   "requiredProperties": ["testRunner", "e2eTool", "scaffoldCommand", "bindings"], ⏎   "requiredEnforcement": ["notByDefaultPackages", "devOnlyPackages"], ⏎   "roles": ["fe …"
- Evidence M1-S000256: `output/template/.claude/capabilities/persistence/CONTRACT.md:44-55` — ""slot": "persistence", ⏎   "slotType": "leaf", ⏎   "required": true, ⏎   "requiredFacets": { ⏎     "planning": "docs/capabilities/persistence.md", ⏎     "rules": ".claude/rules/persistence-technology.md", ⏎     "workflow": ".claude/skills/persistence-change/SKILL.md", ⏎     "knowledge": null ⏎   }, ⏎   "requiredProperties": ["commitBinding", "migrationMechanism", "seedingMechanism", "providerVaria …"
- Evidence M1-S000419: `output/template/.claude/scripts/check-instructions.js:105-109` — "for (const m of modules) { ⏎     for (const facet of [...(m.manifest.facets.knowledge || []), ...(m.manifest.facets.workflow || [])]) { ⏎       if (!common.exists(facet)) add('ERROR', m.file, `facet skill missing: ${facet}`); ⏎     } ⏎   }"
- Evidence M1-S000431: `output/template/.claude/scripts/check-instructions.js:284-326` — "const contractFile = `.claude/capabilities/${slot}/CONTRACT.md`; ⏎     const moduleFile = `.claude/capabilities/${slot}/${impl}/MODULE.md`; ⏎     if (!common.exists(moduleFile)) { ⏎       add('ERROR', moduleFile, 'manifest of the selected implementation is missing.'); ⏎       continue; ⏎     } ⏎     let contract; ⏎     let manifest; ⏎     try { ⏎       contract = common.extractJsonBlock(common.rea …"

### EXTRA-M1-0029
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Instruction and enforcement files outside a capability's own facets must not name a selected implementation's leak tokens (e.g. Clean Architecture, NUnit, Angular, EF Core) unless a binds entry declares it; check-instructions.js reports errors.
- Trigger/scope: executable data of the selected architecture module (consumed by hooks/checkers)
- Exceptions: Owning facets, MAP.md and capability-selection.md exempt; binds entries.
- Why EXTRA: Implementation-name isolation is a capability-system invariant (repo/meta), not an oracle policy.
- Evidence M1-S000162: `output/template/.claude/capabilities/architecture/clean-architecture/MODULE.md:31-31` — ""leakTokens": ["Clean Architecture", "clean-architecture"],"
- Evidence M1-S000208: `output/template/.claude/capabilities/backend-testing/nunit/MODULE.md:32-32` — ""leakTokens": ["NUnit", "nunit", "[TestCase", "[TestFixture", "TestCaseSource", "OneTimeSetUp", "Assert.That"],"
- Evidence M1-S000218: `output/template/.claude/capabilities/frontend/angular/MODULE.md:29-29` — ""leakTokens": ["Angular", "angular", "RxJS", "NgRx", "NgModule", "Vitest", "@angular", "ng add", "ng new", "provideHttpClient"],"
- Evidence M1-S000265: `output/template/.claude/capabilities/persistence/ef-core/MODULE.md:51-51` — ""leakTokens": ["EF Core", "Entity Framework""
- Evidence M1-S000434: `output/template/.claude/scripts/check-instructions.js:353-382` — "// Implementation-name leaks, workflow facet roles, and binds. ⏎   const frame = modules.find((m) => m.slot === 'architecture'); ⏎   const detailTokens = (frame && frame.manifest.enforcement && frame.manifest.enforcement.detailTokens) || []; ⏎   const scanned = [...files, ...enforcementFiles()].filter((f) => !ALLOW_ALL_TOKENS.includes(f) && !f.startsWith('.claude/capabilities/')); ⏎   const usedBi …"
- Evidence M1-S000479: `output/template/.claude/MAP.md:139-144` — "Composition is static: one implementation per required slot, zero or one for ⏎ the optional frontend slot (`docs/capability-selection.md`). Contracts and ⏎ manifests are maintainer metadata. Outside a module's own facets, instructions ⏎ refer to slots and facet roles, never to the selected implementation's name; ⏎ the instruction checker enforces this with each manifest's leak tokens. Add ⏎ implem …"

### EXTRA-M1-0030
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Non-frame capability facets must not use frame-specific names (Infrastructure, .Domain, .Application, .Api) without a binds entry to the frame.
- Trigger/scope: executable data of the selected architecture module (consumed by hooks/checkers)
- Exceptions: binds to the frame.
- Why EXTRA: Capability-system invariant (repo/meta).
- Evidence M1-S000163: `output/template/.claude/capabilities/architecture/clean-architecture/MODULE.md:32-33` — ""detailTokens": ["Infrastructure", ".Domain", ".Application", ".Api"],"
- Evidence M1-S000434: `output/template/.claude/scripts/check-instructions.js:353-382` — "// Implementation-name leaks, workflow facet roles, and binds. ⏎   const frame = modules.find((m) => m.slot === 'architecture'); ⏎   const detailTokens = (frame && frame.manifest.enforcement && frame.manifest.enforcement.detailTokens) || []; ⏎   const scanned = [...files, ...enforcementFiles()].filter((f) => !ALLOW_ALL_TOKENS.includes(f) && !f.startsWith('.claude/capabilities/')); ⏎   const usedBi …"

### EXTRA-M1-0031
- Closest oracle policies: none
- Modality: MUST
- Normative action: Leaf modules hold only implementation-specific facets; framework-independent policy stays in the neutral rule files outside the module, and placement belongs to the frame.
- Trigger/scope: capability maintenance (backend-testing slot)
- Exceptions: none
- Why EXTRA: Capability-system ownership rule (repo/meta).
- Evidence M1-S000190: `output/template/.claude/capabilities/backend-testing/CONTRACT.md:7-13` — "Framework-independent test policy (levels, behavior focus, determinism,"
- Evidence M1-S000226: `output/template/.claude/capabilities/frontend/CONTRACT.md:7-12` — "The optional frontend leaf supplies the web frontend framework: ⏎ framework-specific rules and role bindings, knowledge, scaffold and build/test ⏎ command notes, and selected-technology decisions. Framework-independent frontend ⏎ policy (feature structure, presentation focus, HTTP boundary, API errors, state, ⏎ routing, validation authority) stays in `.claude/rules/frontend.md` outside the ⏎ modul …"

### EXTRA-M1-0032
- Closest oracle policies: none
- Modality: MUST
- Normative action: Clearing the optional frontend selection removes the module's facets and its planning import; nothing outside the listed facets may need to change (check-instructions.js errors on imported/present planning facets of unselected slots).
- Trigger/scope: capability maintenance (frontend slot)
- Exceptions: none
- Why EXTRA: Capability-system invariant (repo/meta).
- Evidence M1-S000227: `output/template/.claude/capabilities/frontend/CONTRACT.md:14-15` — "Clearing the selection removes the module's facets and its planning import; ⏎ nothing outside the facets listed in the manifest needs to change."
- Evidence M1-S002083: `output/template/.claude/skills/template-maintenance/SKILL.md:77-84` — "Set the frontend row to status `disabled` with implementation `—`; delete the ⏎ facet files listed in the frontend `MODULE.md` manifest and its module ⏎ directory; remove the `@docs/capabilities/frontend.md` import from ⏎ `CLAUDE.md`; update the frontend entry in the map's capability view; run the ⏎ checker. Other instructions need no edits: their references to the slot's ⏎ role-named facets apply …"

### EXTRA-M1-0033
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: A missing required facet or property is a conformance failure whose resolution requires a Decision Request.
- Trigger/scope: capability maintenance (persistence slot)
- Exceptions: none
- Why EXTRA: Capability-system rule tied to Decision Control; not an oracle policy.
- Evidence M1-S000243: `output/template/.claude/capabilities/persistence/CONTRACT.md:11-11` — "A missing required facet or property is a conformance failure; resolving it"
- Evidence M1-S000244: `output/template/.claude/capabilities/persistence/CONTRACT.md:12-12` — "requires a Decision Request. Replacing the technology (for example with a"

### EXTRA-M1-0034
- Closest oracle policies: PST-005, PST-006, PST-010
- Modality: MUST_NOT
- Normative action: Replacing the persistence technology must not silently lose migration or seeding semantics.
- Trigger/scope: capability maintenance (persistence slot)
- Exceptions: Only on technology replacement.
- Why EXTRA: Replacement-continuity obligation not in the oracle.
- Evidence M1-S000244: `output/template/.claude/capabilities/persistence/CONTRACT.md:12-12` — "requires a Decision Request. Replacing the technology (for example with a"
- Evidence M1-S000245: `output/template/.claude/capabilities/persistence/CONTRACT.md:13-13` — "micro-ORM) must not silently lose the migration or seeding semantics. A"

### EXTRA-M1-0035
- Closest oracle policies: DEP-009
- Modality: DEFINITION
- Normative action: A provider change (e.g. SQL Server to PostgreSQL) is a provider-variant change inside the persistence slot, not a new slot.
- Trigger/scope: capability maintenance (persistence slot)
- Exceptions: none
- Why EXTRA: Capability-taxonomy rule (repo/meta).
- Evidence M1-S000245: `output/template/.claude/capabilities/persistence/CONTRACT.md:13-13` — "micro-ORM) must not silently lose the migration or seeding semantics. A"
- Evidence M1-S000246: `output/template/.claude/capabilities/persistence/CONTRACT.md:14-15` — "provider change (for example SQL Server to PostgreSQL) is a provider-variant ⏎ change inside this slot, not a new slot."

### EXTRA-M1-0036
- Closest oracle policies: DEP-009
- Modality: MUST
- Normative action: Provider-variant content is confined to the listed sections; a provider change edits only those sections, the provider property and the declared string-comparison property.
- Trigger/scope: executable data of the selected persistence module
- Exceptions: none
- Why EXTRA: Capability maintenance rule (repo/meta).
- Evidence M1-S000261: `output/template/.claude/capabilities/persistence/ef-core/MODULE.md:11-14` — "Provider-variant content (SQL Server) is confined to the sections listed in ⏎ `providerVariantSections`; a provider change edits only those sections, the ⏎ provider property in `docs/capability-selection.md`, and the declared ⏎ string-comparison property."
- Evidence M1-S002081: `output/template/.claude/skills/template-maintenance/SKILL.md:71-73` — "Edit the provider-variant sections listed in the persistence `MODULE.md` ⏎ manifest, the provider property in `docs/capability-selection.md`, and the ⏎ declared string-comparison property; record the ADR."

### EXTRA-M1-0037
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Post-change checks return WARN-level findings (e.g. VersionOverride, competing test framework, not-by-default packages) as well as ERRORs in a decision:block that Claude must address.
- Trigger/scope: executable hook after file edits and shell commands (registered in settings.json)
- Exceptions: After failed shell commands findings are added as context instead.
- Why EXTRA: Escalating advisory findings to a blocking reason is an enforcement-strength choice not in the oracle.
- Evidence M1-S000274: `output/template/.claude/hooks/post-tool-use.js:53-57` — "function report(findings, title) { ⏎   const relevant = findings.filter((f) => f.level === 'ERROR' || f.level === 'WARN'); ⏎   if (!relevant.length) return []; ⏎   return [`${title}:`, ...limit(common.formatFindings(relevant).split('\n'))]; ⏎ }"
- Evidence M1-S000286: `output/template/.claude/hooks/post-tool-use.js:221-222` — "if (messages.length && event === 'PostToolUseFailure') out.addContext(event, messages.join('\n')); ⏎   if (messages.length) out.block(messages.join('\n'));"

### EXTRA-M1-0038
- Closest oracle policies: GOV-007
- Modality: ENFORCED_ADVISORY
- Normative action: After editing SPECIFICATION.md Claude is told to record approved behaviour through the architecture-decision workflow.
- Trigger/scope: executable hook after file edits and shell commands (registered in settings.json)
- Exceptions: none
- Why EXTRA: Routing of approved behaviour changes through architecture-decision is not entailed by GOV-007.
- Evidence M1-S000277: `output/template/.claude/hooks/post-tool-use.js:72-74` — "if (rel === 'SPECIFICATION.md') { ⏎     msgs.push('SPECIFICATION.md changed: keep it consistent with CUSTOM_SETTINGS.md (CLAUDE.md, Product Sources); record approved behavior through the architecture-decision workflow.'); ⏎   }"

### EXTRA-M1-0039
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: After editing CLAUDE.md, an imported file or anything under .claude/, check-instructions.js runs and its ERROR findings are returned as a blocking reason.
- Trigger/scope: executable hook after file edits and shell commands (registered in settings.json)
- Exceptions: none
- Why EXTRA: Automatic enforcement of instruction-system invariants on every instruction edit (repo/meta).
- Evidence M1-S000279: `output/template/.claude/hooks/post-tool-use.js:78-81` — "if (instructions.isInstructionPath(rel)) { ⏎     const { findings } = instructions.run(); ⏎     msgs.push(...report(findings.filter((f) => f.level === 'ERROR'), 'Instruction-structure check (template-maintenance workflow)')); ⏎   }"

### EXTRA-M1-0040
- Closest oracle policies: DEP-025, DEP-003
- Modality: ENFORCED
- Normative action: The PreToolUse guard fails closed: an internal error, malformed hook input, helper load failure, crash or timeout blocks the shell command (and the user is told the instruction system needs repair via template-maintenance).
- Trigger/scope: executable PreToolUse hook on Bash/PowerShell
- Exceptions: none
- Why EXTRA: Makes a working hook a precondition for every Bash/PowerShell call; not an oracle policy.
- Evidence M1-S000290: `output/template/.claude/hooks/pre-tool-use.js:27-31` — "} catch (e) { ⏎   if (out) out.denyOnFailure('pre-tool-use', e, 'dependency and project-reference routing could not be applied'); ⏎   process.stderr.write(`pre-tool-use hook failed (${e && e.message ? e.message : e}); the command was blocked.\n`); ⏎   process.exit(2); ⏎ }"
- Evidence M1-S000394: `output/template/.claude/scripts/lib/hook-output.js:27-33` — "// PreToolUse: an internal failure denies the tool call instead of silently allowing it. ⏎ function denyOnFailure(hookName, error, consequence) { ⏎   denyToolUse( ⏎     `${hookName} hook failed (${errorText(error)}); ${consequence}, so the command was blocked.\n` + ⏎       'Report the hook failure to the user; the instruction system is repaired through the template-maintenance workflow.\n' ⏎   );  …"
- Evidence M1-S000398: `output/template/.claude/settings.json:7-12` — "{ ⏎             "type": "command", ⏎             "command": "node", ⏎             "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-tool-use.js"], ⏎             "onFailure": "block" ⏎           }"
- Evidence M1-S000475: `output/template/.claude/MAP.md:113-119` — ""

### EXTRA-M1-0041
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: The Stop hook blocks once per change state; Claude must address each reminder or state why it does not apply before finishing.
- Trigger/scope: executable Stop hook (end of turn) over the uncommitted change set
- Exceptions: Not re-blocked while stop_hook_active or for an unchanged state.
- Why EXTRA: Turn-completion gate not required by the oracle.
- Evidence M1-S000301: `output/template/.claude/hooks/stop.js:107-107` — "hook.block(`Co-change check:\n- ${messages.join('\n- ')}\nAddress these or state why they do not apply, then finish.`);"

### EXTRA-M1-0069
- Closest oracle policies: none
- Modality: MUST
- Normative action: Every rule has exactly one owner and other files point to it; related new content goes where the 'Add here' column says.
- Trigger/scope: instruction-system maintenance (MAP.md, not auto-loaded)
- Exceptions: none
- Why EXTRA: Instruction-ownership rule (repo/meta).
- Evidence M1-S000449: `output/template/.claude/MAP.md:5-8` — "Every table lists, per artifact: **File**, **Owner** (the policy or procedure ⏎ it is authoritative for; every rule has exactly one owner and other files point ⏎ to it), **Scope**, **Loading**, **Enforcement**, and **Add here** (where related ⏎ new content belongs)."
- Evidence M1-S002070: `output/template/.claude/skills/template-maintenance/SKILL.md:32-33` — "1. Find the current authoritative owner in the map; change the rule there and ⏎    use pointers elsewhere — never restate a rule in a second place."

### EXTRA-M1-0070
- Closest oracle policies: none
- Modality: MUST
- Normative action: Place new instruction content in the artifact whose 'Add here' column covers it (governance only in CLAUDE.md, selection changes only via ADR, rules by topic, procedures in workflows, technique in knowledge skills, mechanisms in hooks/scripts, implementation-specific content only in module facets).
- Trigger/scope: instruction-system maintenance (MAP.md, not auto-loaded)
- Exceptions: none
- Why EXTRA: Repo/meta placement guidance.
- Evidence M1-S000454: `output/template/.claude/MAP.md:27-29` — "| `CLAUDE.md` | product-source authority, custom-settings boundary, core defaults, challenge duty, decision control, Git boundary, workflow routing | common, repo/meta | always | instruction checker | only governance that must be known while planning | ⏎ | `docs/technology-stack.md` | approved stack and conditional technologies outside the slots | common | always (import) | manifest check (deny-li …"
- Evidence M1-S000458: `output/template/.claude/MAP.md:38-47` — "| `rules/frontend.md` | framework-independent frontend structure, HTTP boundary, errors, state, routing, validation authority | frontend (`frontend/**/*`) | path | — | framework-independent frontend rules | ⏎ | `rules/testing.md` | framework-independent test policy | backend-tests (`backend/**/*Tests/**`) | path | stop hook (test co-change) | framework-independent test rules | ⏎ | `rules/coding-st …"
- Evidence M1-S000462: `output/template/.claude/MAP.md:56-68` — "| `skills/development-workflow/SKILL.md` | implementation procedure: product sources, inspection and owner reads, bug-fix regression, performance changes, review before verify | common | workflow | — | implementation steps | ⏎ | `skills/verify/SKILL.md` | completion gates, probe preservation, using cleanup, delivery-pipeline checks, reporting | common | workflow | runs the checkers | verification  …"
- Evidence M1-S000466: `output/template/.claude/MAP.md:78-93` — "| `skills/http-api/SKILL.md` | status-code reference (policy: `rules/api.md`) | backend | on demand | — | HTTP response technique | ⏎ | `skills/aspnet-error-handling/SKILL.md` | exception handler, ProblemDetails, validation technique (policy: `rules/error-handling.md`) | backend | on demand | — | error-handling examples | ⏎ | `skills/logging/SKILL.md` | ILogger technique (policy: `rules/compositio …"
- Evidence M1-S000470: `output/template/.claude/MAP.md:102-102` — "| `agents/code-reviewer.md` | independent read-only review; preloads `code-review` | common | delegated by `code-review` or the user | `disallowedTools` (read-only) | nothing: review criteria belong in `code-review` |"
- Evidence M1-S000473: `output/template/.claude/MAP.md:108-109` — "| `SPECIFICATION.md` | product behavior input; empty in the template by design | product | read by workflows | post-edit and stop reminders | approved product behavior | ⏎ | `CUSTOM_SETTINGS.md` | approved tunable values input | product | read by workflows | post-edit and stop reminders | approved tunable values |"
- Evidence M1-S000477: `output/template/.claude/MAP.md:123-135` — "| `settings.json` | wires the hooks in exec form (`node` + script path through `${CLAUDE_PROJECT_DIR}`, no shell); the critical pre-tool hook fails closed (`onFailure: "block"`); failed shell commands are post-checked too (`PostToolUseFailure`) | repo/meta | hook | new hook wiring | ⏎ | `hooks/pre-tool-use.js` | denies dependency commands until `add-dependency` was applied and project-reference co …"
- Evidence M1-S000479: `output/template/.claude/MAP.md:139-144` — "Composition is static: one implementation per required slot, zero or one for ⏎ the optional frontend slot (`docs/capability-selection.md`). Contracts and ⏎ manifests are maintainer metadata. Outside a module's own facets, instructions ⏎ refer to slots and facet roles, never to the selected implementation's name; ⏎ the instruction checker enforces this with each manifest's leak tokens. Add ⏎ implem …"
- Evidence M1-S002068: `output/template/.claude/skills/template-maintenance/SKILL.md:19-28` — "| Content | Location | ⏎ |---|---| ⏎ | governance needed at planning time | `CLAUDE.md` (keep it compact) | ⏎ | approved stack or conditional technology outside the slots | `docs/technology-stack.md` | ⏎ | planning-time decision of a selected capability implementation | `docs/capabilities/<slot>.md` | ⏎ | path-scoped normative rule | `.claude/rules/<topic>.md` — flat, `paths:` required; implementa …"

### EXTRA-M1-0071
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: A 201 response includes Location when a stable resource URI exists.
- Trigger/scope: path rule: backend/**/*.cs, backend/**/launchSettings.json
- Exceptions: Stable resource URI exists.
- Why EXTRA: Location header requirement not in the oracle.
- Evidence M1-S000500: `output/template/.claude/rules/api.md:19-22` — "- Choose `200`, `201`, `202`, or `204` according to the actual HTTP semantics of ⏎   the outcome. Do not return `200` for every outcome, `201` merely because a row ⏎   was inserted internally (`201` means a new API resource, with `Location` when ⏎   a stable resource URI exists), or `202` for work that already completed."
- Evidence M1-S001497: `output/template/.claude/skills/http-api/SKILL.md:41-42` — "The request created a new API resource. Include a `Location` header when a ⏎ stable resource URI exists:"
- Evidence M1-S002046: `output/template/.claude/skills/swagger/SKILL.md:75-76` — "Document `201 Created` when that is the runtime contract, and prefer ⏎ `CreatedAtAction` / `CreatedAtRoute` when a canonical resource URL exists."

### EXTRA-M1-0072
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Primary constructors when DI/simple initialization stays clear; regular constructors when validation/initialization is non-trivial, explicit fields help, the codebase uses that style, or capture hurts understanding.
- Trigger/scope: path rule: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Constructor style criteria outside the oracle (EXC-002/EXC-003).
- Evidence M1-S000573: `output/template/.claude/rules/coding-style.md:38-39` — "Primary constructors are appropriate when dependency injection or simple"
- Evidence M1-S000575: `output/template/.claude/rules/coding-style.md:49-52` — "Use a regular constructor when validation or initialization is non-trivial, ⏎ explicit fields improve readability, the existing codebase consistently uses ⏎ that style, or parameter capture would make the class harder to understand. Do ⏎ not convert constructors mechanically."

### EXTRA-M1-0073
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Records when value semantics/immutability are desirable (many DTOs, genuine Value Objects); classes for identity/mutable lifecycle/inheritance/framework behaviour; not every DTO/Domain type becomes a record.
- Trigger/scope: path rule: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Record/class style rule outside the oracle.
- Evidence M1-S000577: `output/template/.claude/rules/coding-style.md:56-59` — "Use records when value semantics and immutability are desirable, for example ⏎ many DTOs and genuine Value Objects. Use classes when identity, mutable ⏎ lifecycle, inheritance, or framework behavior makes class semantics clearer. Do ⏎ not turn every DTO or Domain type into a record automatically."

### EXTRA-M1-0074
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Keep implementation details non-public unless public API; use sealed for deliberate non-inheritance intent, not speculative JIT optimization.
- Trigger/scope: path rule: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Visibility/sealed conventions outside the oracle.
- Evidence M1-S000579: `output/template/.claude/rules/coding-style.md:63-66` — "Keep implementation details non-public when they are not part of the project's ⏎ public API. Use `sealed` when a type is deliberately not intended for ⏎ inheritance and the modifier communicates useful design intent; do not add ⏎ `sealed` merely as a speculative JIT optimization."

### EXTRA-M1-0075
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Use var when the type is obvious or unimportant; explicit type when clearer.
- Trigger/scope: path rule: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Type-inference convention outside the oracle.
- Evidence M1-S000582: `output/template/.claude/rules/coding-style.md:73-74` — "`var` when the type is obvious from the right-hand side or not important to ⏎ understanding the code; use an explicit type when it improves clarity."

### EXTRA-M1-0076
- Closest oracle policies: RUN-009
- Modality: MUST
- Normative action: Standard .NET naming: PascalCase types/methods/properties/public members, camelCase parameters/locals, meaningful names; private fields per repository convention.
- Trigger/scope: path rule: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Naming convention not in the oracle.
- Evidence M1-S000584: `output/template/.claude/rules/coding-style.md:78-81` — "Use standard .NET naming: PascalCase for types, methods, properties, and public ⏎ members; camelCase for parameters and local variables; meaningful names over ⏎ abbreviations. Private-field naming follows the repository's established ⏎ convention."

### EXTRA-M1-0077
- Closest oracle policies: RUN-011
- Modality: AVOID
- Normative action: Avoid mixing large formatting or modernization changes with functional work.
- Trigger/scope: path rule: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Goes beyond RUN-011's outside-scope prohibition.
- Evidence M1-S000586: `output/template/.claude/rules/coding-style.md:85-87` — "Do not perform style-only rewrites outside the requested change unless ⏎ explicitly asked. Avoid mixing large formatting or modernization changes with ⏎ functional work. Using-directive cleanup of changed files is a `verify` step."

### EXTRA-M1-0078
- Closest oracle policies: API-007, API-011
- Modality: MUST
- Normative action: Catch an exception only to recover, translate into the layer's own outcome, perform a defined fallback, add context preserving the original, or perform required cleanup.
- Trigger/scope: path rule: backend/**/*.cs
- Exceptions: The listed purposes.
- Why EXTRA: Closed whitelist of catch purposes is stricter than API-007.
- Evidence M1-S000624: `output/template/.claude/rules/error-handling.md:38-41` — "Catch an exception only when the current layer can meaningfully recover, ⏎ translate it into its own abstraction-level outcome, perform a defined fallback, ⏎ add useful context while preserving the original exception, or perform required ⏎ cleanup. Never swallow exceptions to continue execution."
- Evidence M1-S000947: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:152-156` — "Catch an external-service exception locally only when the layer can translate ⏎ it into an Application-level outcome, add useful context, perform a defined ⏎ fallback, or apply an appropriate retry policy at the infrastructure boundary; ⏎ otherwise let it propagate to centralized handling. Do not swallow ⏎ external-service failures."

### EXTRA-M1-0079
- Closest oracle policies: TST-001
- Modality: DEFAULT
- Normative action: Use normal NUnit conventions: [TestFixture] classes, [Test] for single scenarios, [SetUp]/[OneTimeSetUp] with matching teardown, Assert.That constraint assertions.
- Trigger/scope: path rule: backend/**/*Tests/**/*.cs, backend/**/*Tests/*.csproj
- Exceptions: none
- Why EXTRA: Framework-convention rules not in the oracle.
- Evidence M1-S000762: `output/template/.claude/rules/test-framework.md:16-20` — "- Use normal NUnit conventions: `[TestFixture]` classes, `[Test]` for single ⏎   scenarios, `[SetUp]`/`[OneTimeSetUp]` with matching teardown for fixture ⏎   lifetime, and `Assert.That` constraint assertions. The explicit case tables ⏎   required by `testing.md` § Test Readability are written as `[TestCase]` rows ⏎   rather than `TestCaseSource` generators."

### EXTRA-M1-0080
- Closest oracle policies: TST-005
- Modality: PREFER
- Normative action: Prefer one observable scenario per test; multi-step tests only when the sequence is the behaviour.
- Trigger/scope: path rule: backend/**/*Tests/**/*.cs, backend/**/*Tests/*.csproj
- Exceptions: Sequence is the behaviour.
- Why EXTRA: Test-shape preference not in TST-005.
- Evidence M1-S000773: `output/template/.claude/rules/testing.md:38-41` — "For small finite input or state spaces, prefer explicit declarative test cases ⏎ over loops, branches, LINQ, or generated case machinery inside tests; state ⏎ expected results rather than computing them. Prefer one observable scenario per ⏎ test; a multi-step test is appropriate when the sequence itself is the behavior."

### EXTRA-M1-0081
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Use fakes/stubs/mocks when they make an isolated test clearer; do not mock everything mechanically; do not forbid mocking project-owned abstractions.
- Trigger/scope: path rule: backend/**/*Tests/**/*.cs, backend/**/*Tests/*.csproj
- Exceptions: none
- Why EXTRA: Mock/fake choice is technique outside the oracle (EXC-012).
- Evidence M1-S000775: `output/template/.claude/rules/testing.md:45-49` — "Use fakes, stubs, or mocks when they make an isolated test clearer; do not mock ⏎ every dependency mechanically, and do not forbid mocking project-owned ⏎ abstractions. When important behavior depends on real persistence, provider, or ⏎ HTTP semantics, prefer an integration test over reproducing that behavior with ⏎ mocks."

### EXTRA-M1-0082
- Closest oracle policies: TST-012
- Modality: DEFAULT
- Normative action: Example default pattern MethodOrScenario_Condition_ExpectedBehavior.
- Trigger/scope: path rule: backend/**/*Tests/**/*.cs, backend/**/*Tests/*.csproj
- Exceptions: Established project convention.
- Why EXTRA: Concrete naming pattern not in the oracle.
- Evidence M1-S000784: `output/template/.claude/rules/testing.md:76-79` — "By default use descriptive test names that communicate the scenario or ⏎ condition and the expected behavior, for example ⏎ `MethodOrScenario_Condition_ExpectedBehavior`; follow an established project ⏎ convention when one exists."

### EXTRA-M1-0042
- Closest oracle policies: DEP-024, ARC-001
- Modality: ENFORCED_ADVISORY
- Normative action: Backend projects are expected to end with the frame suffixes (.Domain, .Application, .Infrastructure, .Api, .Domain.Tests, .Application.Tests, .Infrastructure.Tests, .IntegrationTests); others are flagged.
- Trigger/scope: executable: check-architecture.js (hooks after edits/commands; manual/verify runs)
- Exceptions: none
- Why EXTRA: Project naming convention not in the oracle.
- Evidence M1-S000309: `output/template/.claude/scripts/check-architecture.js:75-79` — "for (const [name, p] of info) { ⏎     const { names: refs, unreadable } = projectReferences(p.xml); ⏎     if (p.cls.kind === 'unknown') { ⏎       findings.push(finding('WARN', p.file, `project ${name} does not match a frame layer or test-project role; adding a project or layer is Reserved (${ctx.owner}).`)); ⏎       continue;"

### EXTRA-M1-0043
- Closest oracle policies: DEP-020, DEP-004
- Modality: ENFORCED
- Normative action: Microsoft.Extensions.Http.Polly and Polly.Extensions.Http are errors (deprecated resilience integrations).
- Trigger/scope: executable: check-manifests.js (hooks after edits/commands, Stop, manual)
- Exceptions: none
- Why EXTRA: Hard executable ban stricter than DEP-020's default/exception wording.
- Evidence M1-S000324: `output/template/.claude/scripts/check-manifests.js:20-21` — "['Microsoft.Extensions.Http.Polly', 'deprecated resilience integration; use the approved Microsoft.Extensions resilience packages'], ⏎   ['Polly.Extensions.Http', 'deprecated resilience integration; use the approved Microsoft.Extensions resilience packages'],"
- Evidence M1-S000333: `output/template/.claude/scripts/check-manifests.js:75-85` — "function checkPackageId(file, id, data, findings) { ⏎   if (DEPRECATED_PACKAGES.has(id)) { ⏎     findings.push(finding('ERROR', file, `${id}: ${DEPRECATED_PACKAGES.get(id)} (${OWNER_WORKFLOW}).`)); ⏎   } ⏎   if (EXCEPTION_PACKAGES.has(id)) { ⏎     findings.push(finding('WARN', file, `${id}: ${EXCEPTION_PACKAGES.get(id)}.`)); ⏎   } ⏎   if (data.reservedPackages.includes(id)) { ⏎     findings.push(f …"

### EXTRA-M1-0044
- Closest oracle policies: DEP-004, DEP-021
- Modality: ENFORCED
- Normative action: Serilog.Sinks.Elasticsearch is an error (deprecated sink; use Elastic.Serilog.Sinks).
- Trigger/scope: executable: check-manifests.js (hooks after edits/commands, Stop, manual)
- Exceptions: none
- Why EXTRA: Package-specific ban not in the oracle.
- Evidence M1-S000325: `output/template/.claude/scripts/check-manifests.js:22-22` — "['Serilog.Sinks.Elasticsearch', 'deprecated sink package; use Elastic.Serilog.Sinks'],"
- Evidence M1-S000333: `output/template/.claude/scripts/check-manifests.js:75-85` — "function checkPackageId(file, id, data, findings) { ⏎   if (DEPRECATED_PACKAGES.has(id)) { ⏎     findings.push(finding('ERROR', file, `${id}: ${DEPRECATED_PACKAGES.get(id)} (${OWNER_WORKFLOW}).`)); ⏎   } ⏎   if (EXCEPTION_PACKAGES.has(id)) { ⏎     findings.push(finding('WARN', file, `${id}: ${EXCEPTION_PACKAGES.get(id)}.`)); ⏎   } ⏎   if (data.reservedPackages.includes(id)) { ⏎     findings.push(f …"

### EXTRA-M1-0045
- Closest oracle policies: DEP-010
- Modality: ENFORCED
- Normative action: FluentValidation.AspNetCore is an error (legacy automatic-validation integration).
- Trigger/scope: executable: check-manifests.js (hooks after edits/commands, Stop, manual)
- Exceptions: none
- Why EXTRA: The oracle names FluentValidation as standard but does not ban this integration package.
- Evidence M1-S000326: `output/template/.claude/scripts/check-manifests.js:23-23` — "['FluentValidation.AspNetCore', 'legacy automatic-validation integration; do not add it merely to connect validation to the pipeline'],"
- Evidence M1-S000333: `output/template/.claude/scripts/check-manifests.js:75-85` — "function checkPackageId(file, id, data, findings) { ⏎   if (DEPRECATED_PACKAGES.has(id)) { ⏎     findings.push(finding('ERROR', file, `${id}: ${DEPRECATED_PACKAGES.get(id)} (${OWNER_WORKFLOW}).`)); ⏎   } ⏎   if (EXCEPTION_PACKAGES.has(id)) { ⏎     findings.push(finding('WARN', file, `${id}: ${EXCEPTION_PACKAGES.get(id)}.`)); ⏎   } ⏎   if (data.reservedPackages.includes(id)) { ⏎     findings.push(f …"

### EXTRA-M1-0046
- Closest oracle policies: DEP-006
- Modality: ENFORCED_ADVISORY
- Normative action: VersionOverride is flagged as needing a concrete, documented reason.
- Trigger/scope: executable: check-manifests.js (hooks after edits/commands, Stop, manual)
- Exceptions: none
- Why EXTRA: Documentation obligation beyond DEP-006.
- Evidence M1-S000336: `output/template/.claude/scripts/check-manifests.js:97-99` — "if (ref.override !== null) { ⏎       findings.push(finding('WARN', file, `PackageReference ${ref.id} uses VersionOverride; this needs a concrete, documented reason (${OWNER_RULE}).`)); ⏎     }"
- Evidence M1-S000607: `output/template/.claude/rules/dependencies.md:26-29` — "Use NuGet Central Package Management. Package versions belong in ⏎ `Directory.Packages.props`; project `PackageReference` entries are versionless ⏎ by default, and a `VersionOverride` needs a concrete, documented reason. Do not ⏎ duplicate centrally managed versions in individual `.csproj` files."

### EXTRA-M1-0047
- Closest oracle policies: DEP-003
- Modality: ENFORCED
- Normative action: Floating or empty versions ('*', empty; npm '', '*', 'latest', x) are errors with no explicit-request exception (range specifiers such as ^/~/[..] are not flagged).
- Trigger/scope: executable: check-manifests.js (hooks after edits/commands, Stop, manual)
- Exceptions: none
- Why EXTRA: DEP-003 allows floating versions when explicitly requested.
- Evidence M1-S000342: `output/template/.claude/scripts/check-manifests.js:124-131` — "const version = versionOf(item); ⏎     if (version !== null) { ⏎       if (version.includes('*') || version.trim() === '') { ⏎         findings.push(finding('ERROR', file, `${id}: floating or empty version "${version}"; select the latest stable compatible version (${OWNER_WORKFLOW}).`)); ⏎       } else if (PRERELEASE.test(version)) { ⏎         findings.push(finding('WARN', file, `${id}: prerelease …"
- Evidence M1-S000346: `output/template/.claude/scripts/check-manifests.js:150-154` — "if (s === '' || s === '*' || s === 'latest' || /^x(\.x)*$/i.test(s)) { ⏎         findings.push(finding('ERROR', file, `${section}.${id}: floating version "${s}"; pin the latest stable compatible version (${OWNER_WORKFLOW}).`)); ⏎       } else if (PRERELEASE.test(s)) { ⏎         findings.push(finding('WARN', file, `${section}.${id}: prerelease version "${s}" is allowed only when explicitly requeste …"
- Evidence M1-S000797: `output/template/.claude/skills/add-dependency/SKILL.md:41-49` — "For every NuGet or npm addition or update: ⏎  ⏎ 1. determine the latest stable version compatible with the project's target ⏎    framework/runtime and peer dependencies; ⏎ 2. verify the current version from the package registry rather than relying on ⏎    a remembered version; ⏎ 3. do not select preview, alpha, beta, RC, dev, nightly, or other prerelease ⏎    versions unless explicitly requested;  …"

### EXTRA-M1-0052
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Exactly the four capability slots (architecture, persistence, backend-testing required; frontend optional) may exist, each with a contract; the selection record must be readable and list no unknown slot.
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Capability-system invariant (repo/meta).
- Evidence M1-S000406: `output/template/.claude/scripts/check-instructions.js:15-16` — "const SLOTS = ['architecture', 'persistence', 'backend-testing', 'frontend']; ⏎ const REQUIRED_SLOTS = ['architecture', 'persistence', 'backend-testing'];"
- Evidence M1-S000429: `output/template/.claude/scripts/check-instructions.js:258-269` — "function checkCapabilities(files) { ⏎   let rows; ⏎   try { ⏎     rows = common.readSelection(); ⏎   } catch (e) { ⏎     add('ERROR', common.SELECTION_FILE, `cannot read the capability selection record: ${e.message}`); ⏎     return []; ⏎   } ⏎   const contractDirs = common.walk('.claude/capabilities').filter((f) => /\/CONTRACT\.md$/.test(f)).map((f) => f.split('/')[2]); ⏎   for (const slot of cont …"

### EXTRA-M1-0053
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Required workflow skills (project-structure, verify, code-review, build-fix, custom-settings, git-workflow, security-scan, add-dependency, architecture-decision, template-maintenance, development-workflow) and embedded knowledge skills (http-api, aspnet-error-handling, logging, httpclient-factory, configuration, dependency-injection, caching, swagger, api-versioning, health-check, docker, ci-cd, modern-csharp, authentication) must exist.
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Skill-inventory invariant (repo/meta).
- Evidence M1-S000407: `output/template/.claude/scripts/check-instructions.js:17-24` — "const REQUIRED_WORKFLOWS = [ ⏎   'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings', 'git-workflow', ⏎   'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance', 'development-workflow', ⏎ ]; ⏎ const REQUIRED_EMBEDDED_KNOWLEDGE = [ ⏎   'http-api', 'aspnet-error-handling', 'logging', 'httpclient-factory', 'configuration', 'dependency-injection', ⏎ …"
- Evidence M1-S000418: `output/template/.claude/scripts/check-instructions.js:103-104` — "for (const w of REQUIRED_WORKFLOWS) if (!names.includes(w)) add('ERROR', '.claude/skills', `required workflow skill missing: ${w}`); ⏎   for (const k of REQUIRED_EMBEDDED_KNOWLEDGE) if (!names.includes(k)) add('ERROR', '.claude/skills', `required knowledge skill missing: ${k}`);"

### EXTRA-M1-0054
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: template-maintenance must set disable-model-invocation: true.
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta invocation invariant.
- Evidence M1-S000408: `output/template/.claude/scripts/check-instructions.js:25-25` — "const USER_ONLY_SKILLS = ['template-maintenance'];"
- Evidence M1-S000416: `output/template/.claude/scripts/check-instructions.js:88-98` — "function checkSkills(modules) { ⏎   const names = skillNames(); ⏎   for (const name of names) { ⏎     const file = `.claude/skills/${name}/SKILL.md`; ⏎     const fm = common.parseFrontMatter(common.readText(file)); ⏎     if (fm.data.name !== name) add('ERROR', file, `front-matter name "${fm.data.name || ''}" must equal the directory name "${name}".`); ⏎     if (!fm.data.description || String(fm.da …"

### EXTRA-M1-0055
- Closest oracle policies: none
- Modality: ENFORCED_WARNING
- Normative action: Warn when the always-loaded surface exceeds about 6500 tokens.
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: Warning only.
- Why EXTRA: Context budget threshold not in the oracle.
- Evidence M1-S000409: `output/template/.claude/scripts/check-instructions.js:26-26` — "const BUDGET_TOKENS = 6500;"
- Evidence M1-S000444: `output/template/.claude/scripts/check-instructions.js:511-512` — "always-loaded surface is about"

### EXTRA-M1-0056
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Every instruction file's first content line must be a '> ' classification/ownership header.
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta header convention.
- Evidence M1-S000413: `output/template/.claude/scripts/check-instructions.js:60-70` — "// ---------- headers and classification ---------- ⏎ function checkHeaders(files) { ⏎   for (const f of files) { ⏎     const text = common.readText(f); ⏎     const header = common.firstContentLine(text); ⏎     if (!header.startsWith('> ')) add('ERROR', f, 'missing one-line classification/ownership header (first content line must start with "> ").'); ⏎     if (/(^|\n)\s*>?\s*(Level|Kind):/.test(te …"

### EXTRA-M1-0057
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: No Level:/Kind: classification may appear in instruction files.
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Architecture-identity invariant (repo/meta).
- Evidence M1-S000413: `output/template/.claude/scripts/check-instructions.js:60-70` — "// ---------- headers and classification ---------- ⏎ function checkHeaders(files) { ⏎   for (const f of files) { ⏎     const text = common.readText(f); ⏎     const header = common.firstContentLine(text); ⏎     if (!header.startsWith('> ')) add('ERROR', f, 'missing one-line classification/ownership header (first content line must start with "> ").'); ⏎     if (/(^|\n)\s*>?\s*(Level|Kind):/.test(te …"

### EXTRA-M1-0058
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: .claude/rules/ stays flat and every rule declares a non-empty paths list.
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Rule-layout invariant (repo/meta).
- Evidence M1-S000414: `output/template/.claude/scripts/check-instructions.js:72-81` — "// ---------- rules ---------- ⏎ function checkRules() { ⏎   for (const f of common.walk('.claude/rules')) { ⏎     if (f.split('/').length > 3) add('ERROR', f, 'rules must stay flat in .claude/rules/ (no level- or scope-first subdirectories).'); ⏎     if (!f.endsWith('.md')) continue; ⏎     const fm = common.parseFrontMatter(common.readText(f)); ⏎     const paths = fm.data.paths; ⏎     if (!fm.has …"

### EXTRA-M1-0059
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Skill front-matter name equals its directory and has a concrete description (≥20 characters).
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Skill metadata invariant (repo/meta).
- Evidence M1-S000416: `output/template/.claude/scripts/check-instructions.js:88-98` — "function checkSkills(modules) { ⏎   const names = skillNames(); ⏎   for (const name of names) { ⏎     const file = `.claude/skills/${name}/SKILL.md`; ⏎     const fm = common.parseFrontMatter(common.readText(file)); ⏎     if (fm.data.name !== name) add('ERROR', file, `front-matter name "${fm.data.name || ''}" must equal the directory name "${name}".`); ⏎     if (!fm.data.description || String(fm.da …"

### EXTRA-M1-0060
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Skill-private files live only in the skill's references/ directory.
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Skill-shape invariant (repo/meta).
- Evidence M1-S000417: `output/template/.claude/scripts/check-instructions.js:99-102` — "for (const f of common.walk('.claude/skills')) { ⏎     const parts = f.split('/'); ⏎     if (parts.length > 4 && parts[3] !== 'references') add('ERROR', f, 'skill-private files belong in the skill\'s references/ directory.'); ⏎   }"

### EXTRA-M1-0061
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: CLAUDE.md imports must resolve and no other instruction file may contain an @-import (always-loaded files are imported directly from CLAUDE.md).
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Loading invariant (repo/meta).
- Evidence M1-S000423: `output/template/.claude/scripts/check-instructions.js:127-138` — "function checkImports(files) { ⏎   for (const imp of claudeImports()) { ⏎     if (!common.exists(imp)) add('ERROR', 'CLAUDE.md', `import does not resolve: @${imp}`); ⏎   } ⏎   for (const f of files) { ⏎     if (f === 'CLAUDE.md') continue; ⏎     const body = stripCode(common.readText(f)); ⏎     for (const line of body.split(/\r?\n/)) { ⏎       if (/^@[\w./-]+\.md\s*$/.test(line.trim())) add('ERROR …"

### EXTRA-M1-0062
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Backticked instruction references, workflow/skill/agent references, § section references, routing targets and manifest anchors must resolve (inactive facets of disabled slots exempt).
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Reference-integrity invariant (repo/meta).
- Evidence M1-S000426: `output/template/.claude/scripts/check-instructions.js:195-229` — "function checkReferences(files) { ⏎   const names = skillNames(); ⏎   const inactive = inactiveFacetLocations(); ⏎   const isInactive = (t) => inactive.has(t.replace(/#.*$/, '')); ⏎   for (const f of files) { ⏎     const raw = common.readText(f); ⏎     const flat = flatten(raw); ⏎     const tokens = [...flat.matchAll(/`([^`\n]+)`/g)].map((m) => m[1]); ⏎     for (const t of tokens) { ⏎       if (lo …"
- Evidence M1-S000427: `output/template/.claude/scripts/check-instructions.js:231-240` — "function checkAnchor(ref, fromFile) { ⏎   const [file, anchor] = ref.split('#'); ⏎   if (!common.exists(file)) { ⏎     add('ERROR', fromFile, `manifest path does not resolve: ${file}`); ⏎     return; ⏎   } ⏎   if (anchor && !common.headings(common.readText(file)).some((h) => common.slugify(h) === anchor)) { ⏎     add('ERROR', fromFile, `manifest anchor does not resolve: ${ref}`); ⏎   } ⏎ }"

### EXTRA-M1-0063
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Every facet file of a selected module must declare 'Capability: <slot>/<implementation>' in its header.
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Capability-system invariant (repo/meta).
- Evidence M1-S000431: `output/template/.claude/scripts/check-instructions.js:284-326` — "const contractFile = `.claude/capabilities/${slot}/CONTRACT.md`; ⏎     const moduleFile = `.claude/capabilities/${slot}/${impl}/MODULE.md`; ⏎     if (!common.exists(moduleFile)) { ⏎       add('ERROR', moduleFile, 'manifest of the selected implementation is missing.'); ⏎       continue; ⏎     } ⏎     let contract; ⏎     let manifest; ⏎     try { ⏎       contract = common.extractJsonBlock(common.rea …"

### EXTRA-M1-0064
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: A file declaring a Capability header must belong to a selected module and be listed in its manifest; unselected implementations must not enter runtime.
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Capability-system invariant (repo/meta).
- Evidence M1-S000432: `output/template/.claude/scripts/check-instructions.js:328-341` — "// Facet ownership: every Capability header belongs to a selected module and is listed in its manifest. ⏎   for (const f of files) { ⏎     const cap = common.capabilityOf(common.readText(f)); ⏎     if (!cap) continue; ⏎     const m = modules.find((x) => x.slot === cap.slot && x.implementation === cap.implementation); ⏎     if (!m) { ⏎       add('ERROR', f, `declares Capability: ${cap.slot}/${cap.i …"

### EXTRA-M1-0065
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Planning facets are imported from CLAUDE.md exactly for selected slots; an unselected slot's planning facet must not be imported or present.
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Capability-system invariant (repo/meta).
- Evidence M1-S000433: `output/template/.claude/scripts/check-instructions.js:343-351` — "// Planning facets are imported from CLAUDE.md exactly for the selected slots. ⏎   const imports = claudeImports(); ⏎   for (const slot of SLOTS) { ⏎     const planning = `docs/capabilities/${slot}.md`; ⏎     const m = modules.find((x) => x.slot === slot); ⏎     if (m && !imports.includes(planning)) add('ERROR', 'CLAUDE.md', `planning facet of selected slot ${slot} is not imported: @${planning}`); …"

### EXTRA-M1-0066
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: settings.json must register pre-tool-use.js (PreToolUse: Bash, PowerShell), post-tool-use.js (PostToolUse: Write, Edit, MultiEdit, Bash, PowerShell; PostToolUseFailure: Bash, PowerShell) and stop.js (Stop), in exec form with only expected events.
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Hook-wiring invariant (repo/meta).
- Evidence M1-S000437: `output/template/.claude/scripts/check-instructions.js:394-405` — "// ---------- hooks, map, budget ---------- ⏎ // Expected wiring: each event runs its script for the listed tools. Hooks use exec form ⏎ // (command "node", the script path as the only argument, located through the ⏎ // ${CLAUDE_PROJECT_DIR} placeholder that Claude Code substitutes without a shell). ⏎ // Only PreToolUse enforcement is critical and fails closed (onFailure "block"). ⏎ // PostToolUse …"
- Evidence M1-S000439: `output/template/.claude/scripts/check-instructions.js:422-438` — "function checkHookHandler(file, event, spec, hook) { ⏎   const where = `${event} hook`; ⏎   if (hook.type !== 'command') add('ERROR', file, `${where}: type must be "command".`); ⏎   if (hook.command !== 'node') add('ERROR', file, `${where}: use exec form — command "node" with the script in args (found command ${JSON.stringify(hook.command)}).`); ⏎   const script = hookScript(hook); ⏎   if (!script …"
- Evidence M1-S000440: `output/template/.claude/scripts/check-instructions.js:440-468` — "function checkSettings() { ⏎   const file = '.claude/settings.json'; ⏎   if (!common.exists(file)) { ⏎     add('ERROR', file, 'settings file missing.'); ⏎     return; ⏎   } ⏎   let settings; ⏎   try { ⏎     settings = JSON.parse(common.readText(file)); ⏎   } catch (e) { ⏎     add('ERROR', file, `invalid JSON: ${e.message}`); ⏎     return; ⏎   } ⏎   const hooks = settings.hooks || {}; ⏎   for (cons …"

### EXTRA-M1-0067
- Closest oracle policies: DEP-025
- Modality: ENFORCED
- Normative action: The PreToolUse handler must set onFailure block; no other hook may set onFailure.
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Fail-closed policy as an instruction-system invariant.
- Evidence M1-S000439: `output/template/.claude/scripts/check-instructions.js:422-438` — "function checkHookHandler(file, event, spec, hook) { ⏎   const where = `${event} hook`; ⏎   if (hook.type !== 'command') add('ERROR', file, `${where}: type must be "command".`); ⏎   if (hook.command !== 'node') add('ERROR', file, `${where}: use exec form — command "node" with the script in args (found command ${JSON.stringify(hook.command)}).`); ⏎   const script = hookScript(hook); ⏎   if (!script …"

### EXTRA-M1-0068
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: MAP.md must list every instruction file, enforcement script/JSON, root config file, SPECIFICATION.md and CUSTOM_SETTINGS.md.
- Trigger/scope: executable: check-instructions.js (post-tool-use after edits of CLAUDE.md/imports/.claude/**; template maintenance)
- Exceptions: none
- Why EXTRA: Map completeness invariant (repo/meta).
- Evidence M1-S000441: `output/template/.claude/scripts/check-instructions.js:470-483` — "function checkMap(files) { ⏎   const mapFile = '.claude/MAP.md'; ⏎   if (!common.exists(mapFile)) { ⏎     add('ERROR', mapFile, 'human map missing.'); ⏎     return; ⏎   } ⏎   const map = common.readText(mapFile); ⏎   const listed = [...files, ...enforcementFiles(), ...ROOT_CONFIG.filter((f) => common.exists(f)), 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md']; ⏎   for (const f of listed) { ⏎     if (f = …"

### EXTRA-M1-0048
- Closest oracle policies: DEP-003, DEP-004
- Modality: ENFORCED
- Normative action: Every NuGet/npm package addition, update or removal command (dotnet add/remove package, npm/pnpm/yarn install <pkg>/remove/update, audit fix, ng add/update, nuget, Install-Package) is denied unless its line carries the trailing comment '# add-dependency: checked' after the add-dependency workflow.
- Trigger/scope: executable PreToolUse gate on Bash/PowerShell command text
- Exceptions: Restore commands (npm ci, install without packages) are not gated.
- Why EXTRA: Executable pre-approval protocol for dependency commands; the oracle requires due diligence but no command gate or marker.
- Evidence M1-S000371: `output/template/.claude/scripts/lib/dependency-commands.js:15-15` — "const CHECKED = /#\s*add-dependency:\s*checked\b/i;"
- Evidence M1-S000388: `output/template/.claude/scripts/lib/dependency-commands.js:407-418` — "const changes = ops.filter((op) => op.type === 'package' && op.mode === 'change' && !CHECKED.test(op.comment)); ⏎   if (!changes.length) return { block: false }; ⏎   const op = changes[0]; ⏎   const notes = versionNotes(op); ⏎   return { ⏎     block: true, ⏎     message: ⏎       `Dependency change detected (${describe(op)}) in: ${op.text}\n` + ⏎       `Run the add-dependency workflow first (${DEPE …"
- Evidence M1-S000809: `output/template/.claude/skills/add-dependency/SKILL.md:104-108` — "The pre-tool hook stops package commands until this workflow has been applied. ⏎ After completing steps 1–5, re-run the same command with the trailing comment ⏎ `# add-dependency: checked`. A peer-dependency override additionally needs the ⏎ user's explicit approval and the trailing comment ⏎ `# peer-override: approved-by-user`."

### EXTRA-M1-0049
- Closest oracle policies: DEP-025
- Modality: ENFORCED
- Normative action: npm/pnpm/yarn force or legacy-peer-deps flags are allowed when the line carries '# peer-override: approved-by-user' after explicit user approval.
- Trigger/scope: executable PreToolUse gate on Bash/PowerShell command text
- Exceptions: User approval marker.
- Why EXTRA: Adds a user-approval exception to DEP-025, which forbids the flags merely to bypass peer conflicts without an approval path.
- Evidence M1-S000372: `output/template/.claude/scripts/lib/dependency-commands.js:16-16` — "const PEER_OVERRIDE = /#\s*peer-override:\s*approved-by-user\b/i;"
- Evidence M1-S000386: `output/template/.claude/scripts/lib/dependency-commands.js:381-395` — "// Returns { block: boolean, message?: string }. ⏎ function analyzeCommand(command, shell) { ⏎   const ops = classifyCommand(command, shell); ⏎   for (const op of ops) { ⏎     const flag = forceFlag(op); ⏎     if (flag && !PEER_OVERRIDE.test(op.comment)) { ⏎       return { ⏎         block: true, ⏎         message: ⏎           `Peer-dependency override flag detected (${flag}) in: ${op.text}\n` + ⏎  …"
- Evidence M1-S000809: `output/template/.claude/skills/add-dependency/SKILL.md:104-108` — "The pre-tool hook stops package commands until this workflow has been applied. ⏎ After completing steps 1–5, re-run the same command with the trailing comment ⏎ `# add-dependency: checked`. A peer-dependency override additionally needs the ⏎ user's explicit approval and the trailing comment ⏎ `# peer-override: approved-by-user`."

### EXTRA-M1-0050
- Closest oracle policies: ARC-001, ARC-028
- Modality: ENFORCED
- Normative action: dotnet add/remove reference (and reference add/remove) commands are denied unless the line carries '# project-reference: checked' after the project-structure workflow.
- Trigger/scope: executable PreToolUse gate on Bash/PowerShell command text
- Exceptions: none
- Why EXTRA: Executable gate for project-reference changes not in the oracle.
- Evidence M1-S000373: `output/template/.claude/scripts/lib/dependency-commands.js:17-17` — "const REFERENCE_CHECKED = /#\s*project-reference:\s*checked\b/i;"
- Evidence M1-S000387: `output/template/.claude/scripts/lib/dependency-commands.js:396-406` — "const references = ops.filter((op) => op.type === 'reference' && !REFERENCE_CHECKED.test(op.comment)); ⏎   if (references.length) { ⏎     return { ⏎       block: true, ⏎       message: ⏎         `Project-reference change detected (${describe(references[0])}) in: ${references[0].text}\n` + ⏎         `Apply the project-structure workflow first (${REFERENCE_WORKFLOW}, Changing Project References): it …"
- Evidence M1-S001879: `output/template/.claude/skills/project-structure/SKILL.md:118-119` — "The pre-tool hook stops `dotnet add/remove ... reference` and ⏎ `dotnet reference add/remove` commands until this procedure has been applied."
- Evidence M1-S001882: `output/template/.claude/skills/project-structure/SKILL.md:128-129` — "3. Re-run the same command with the trailing comment ⏎    `# project-reference: checked`."

### EXTRA-M1-0051
- Closest oracle policies: ARC-020
- Modality: ENFORCED_ADVISORY
- Normative action: Reference-graph changes that are Reserved are routed to architecture-decision.
- Trigger/scope: executable PreToolUse gate on Bash/PowerShell command text
- Exceptions: none
- Why EXTRA: Reference-graph changes as Reserved decisions are an added gate.
- Evidence M1-S000387: `output/template/.claude/scripts/lib/dependency-commands.js:396-406` — "const references = ops.filter((op) => op.type === 'reference' && !REFERENCE_CHECKED.test(op.comment)); ⏎   if (references.length) { ⏎     return { ⏎       block: true, ⏎       message: ⏎         `Project-reference change detected (${describe(references[0])}) in: ${references[0].text}\n` + ⏎         `Apply the project-structure workflow first (${REFERENCE_WORKFLOW}, Changing Project References): it …"
- Evidence M1-S001881: `output/template/.claude/skills/project-structure/SKILL.md:124-127` — "2. Classify the change with `CLAUDE.md` § Decision Control. Adding a reference ⏎    that the layout prescribes for projects of the approved structure follows ⏎    the Decided layout (Scaffolding Procedure, step 6); any other change to the ⏎    reference graph is Reserved: raise it through `architecture-decision` first."

### EXTRA-M1-0083
- Closest oracle policies: DEP-020, DEP-004
- Modality: MUST_NOT
- Normative action: Never add the deprecated Microsoft.Extensions.Http.Polly or Polly.Extensions.Http integrations.
- Trigger/scope: workflow add-dependency (NuGet/npm add/update/remove)
- Exceptions: none
- Why EXTRA: Package-specific prohibition beyond DEP-020.
- Evidence M1-S000794: `output/template/.claude/skills/add-dependency/SKILL.md:29-35` — "- **Resilience** — when resilience is required, prefer ⏎   `Microsoft.Extensions.Http.Resilience` for `HttpClient` and ⏎   `Microsoft.Extensions.Resilience` for general pipelines. Never add the ⏎   deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http` ⏎   integrations. Direct Polly usage is an explicit exception: use it only when a ⏎   concrete requirement cannot be expressed thr …"

### EXTRA-M1-0084
- Closest oracle policies: DEP-020
- Modality: MUST
- Normative action: Document why direct Polly is used.
- Trigger/scope: workflow add-dependency (NuGet/npm add/update/remove)
- Exceptions: none
- Why EXTRA: Documentation obligation not in DEP-020.
- Evidence M1-S000794: `output/template/.claude/skills/add-dependency/SKILL.md:29-35` — "- **Resilience** — when resilience is required, prefer ⏎   `Microsoft.Extensions.Http.Resilience` for `HttpClient` and ⏎   `Microsoft.Extensions.Resilience` for general pipelines. Never add the ⏎   deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http` ⏎   integrations. Direct Polly usage is an explicit exception: use it only when a ⏎   concrete requirement cannot be expressed thr …"

### EXTRA-M1-0085
- Closest oracle policies: DEP-010
- Modality: MUST_NOT
- Normative action: Do not add deprecated or legacy ASP.NET automatic-validation integration packages merely to connect FluentValidation to the pipeline.
- Trigger/scope: workflow add-dependency (NuGet/npm add/update/remove)
- Exceptions: none
- Why EXTRA: Not stated in DEP-010.
- Evidence M1-S000795: `output/template/.claude/skills/add-dependency/SKILL.md:36-37` — "- **Validation** — do not add deprecated or legacy ASP.NET automatic-validation ⏎   integration packages merely to connect FluentValidation to the pipeline."

### EXTRA-M1-0086
- Closest oracle policies: DEP-005
- Modality: MUST_NOT
- Normative action: Do not make legal conclusions beyond what published license information supports.
- Trigger/scope: workflow add-dependency (NuGet/npm add/update/remove)
- Exceptions: none
- Why EXTRA: Restraint not stated in DEP-005.
- Evidence M1-S000805: `output/template/.claude/skills/add-dependency/SKILL.md:91-92` — "Do not make legal conclusions beyond what the published license information ⏎ supports."

### EXTRA-M1-0087
- Closest oracle policies: DEP-001
- Modality: MUST
- Normative action: Remove no-longer-used dependencies when part of the current change and safe to verify; leave no dead package references.
- Trigger/scope: workflow add-dependency (NuGet/npm add/update/remove)
- Exceptions: Within the current change.
- Why EXTRA: Dead-reference removal obligation not in the oracle.
- Evidence M1-S000815: `output/template/.claude/skills/add-dependency/SKILL.md:127-129` — "Remove dependencies that are no longer used when doing so is part of the ⏎ current change and safe to verify; do not leave dead package references, and ⏎ do not perform unrelated dependency cleanup during a narrowly scoped task."

### EXTRA-M1-0088
- Closest oracle policies: GOV-007
- Modality: MUST
- Normative action: Record an accepted decision in the same change that implements it.
- Trigger/scope: workflow architecture-decision
- Exceptions: none
- Why EXTRA: Sequencing obligation not in the oracle.
- Evidence M1-S000909: `output/template/.claude/skills/architecture-decision/SKILL.md:50-50` — "Record the outcome in the same change that implements it:"

### EXTRA-M1-0089
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST
- Normative action: Architecture, stack, convention or public-contract decisions are recorded as docs/decisions/NNNN-short-title.md (Status, Context, Decision, Consequences) and the affected decision record is updated.
- Trigger/scope: workflow architecture-decision
- Exceptions: none
- Why EXTRA: ADR convention not in the oracle.
- Evidence M1-S000910: `output/template/.claude/skills/architecture-decision/SKILL.md:52-55` — "- architecture, stack, convention, or public-contract decisions → an ADR in ⏎   `docs/decisions/NNNN-short-title.md` (Status, Context, Decision, ⏎   Consequences), and update the affected decision record ⏎   (`docs/technology-stack.md` or `docs/capabilities/<slot>.md`);"

### EXTRA-M1-0090
- Closest oracle policies: GOV-017
- Modality: ALLOWED
- Normative action: Record a rejected request only when the rejection is itself a durable decision (e.g. a pattern ruled out).
- Trigger/scope: workflow architecture-decision
- Exceptions: none
- Why EXTRA: Recording practice beyond the oracle.
- Evidence M1-S000913: `output/template/.claude/skills/architecture-decision/SKILL.md:60-61` — "A rejected request is recorded only when the rejection itself is a durable ⏎ decision, for example a pattern explicitly ruled out."

### EXTRA-M1-0091
- Closest oracle policies: FE-004
- Modality: PREFER
- Normative action: Use computed for derived state; avoid unnecessary effect() when computed, template binding or event handling is clearer.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: none
- Why EXTRA: Signal API technique not entailed by FE-004.
- Evidence M1-S000828: `output/template/.claude/skills/angular/SKILL.md:73-75` — "Use `computed` for derived state. Avoid unnecessary `effect()` when `computed`, ⏎ template binding, or explicit event handling expresses the dependency more ⏎ clearly."

### EXTRA-M1-0092
- Closest oracle policies: FE-010
- Modality: MUST_NOT
- Normative action: Do not duplicate complex Domain rules in TypeScript unless the UI genuinely needs an equivalent user-facing rule.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: UI needs an equivalent rule.
- Why EXTRA: Not stated in FE-010/FE-003.
- Evidence M1-S000843: `output/template/.claude/skills/angular/SKILL.md:131-134` — "Reactive Forms give explicit state, validation, and testability for ⏎ non-trivial forms. Keep transport/request mapping explicit, and do not ⏎ duplicate complex Domain rules in TypeScript unless the UI genuinely needs an ⏎ equivalent user-facing rule."

### EXTRA-M1-0093
- Closest oracle policies: DEP-014
- Modality: DEFAULT
- Normative action: When Angular Material is chosen use it consistently for common primitives; do not add it automatically to projects that have not chosen it; do not wrap every Material component without a concrete reason.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: none
- Why EXTRA: Material usage conventions beyond DEP-014.
- Evidence M1-S000852: `output/template/.claude/skills/angular/SKILL.md:166-169` — "When the project has chosen Angular Material, use its components consistently ⏎ for common UI primitives where they satisfy the requirement. Do not add it ⏎ automatically to a project that has not chosen it, and do not wrap every ⏎ Material component in a custom abstraction without a concrete reason."

### EXTRA-M1-0094
- Closest oracle policies: TST-003, TST-011
- Modality: DEFAULT
- Normative action: Frontend tests target meaningful component behaviour, validation, data-access mapping, route/auth behaviour and complex state; not framework internals; E2E for a few important workflows unless broader coverage is required; no duplication across levels.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: Broader E2E when required.
- Why EXTRA: Oracle testing policies are backend-scoped.
- Evidence M1-S000856: `output/template/.claude/skills/angular/SKILL.md:180-184` — "Useful frontend test targets: meaningful component behavior, validation, ⏎ data-access request mapping, important route/auth behavior, and complex ⏎ reactive state. Do not test Angular framework internals. End-to-end tests focus ⏎ on a small number of important user workflows unless the project requires ⏎ broader E2E coverage; do not duplicate the same behavior at every test level."

### EXTRA-M1-0095
- Closest oracle policies: RUN-001, FE-005
- Modality: DEFAULT
- Normative action: Do not prematurely optimize Angular code; lazy loading and sensible rendering/data access first; memoization/virtual scrolling/custom change detection after a real need.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: none
- Why EXTRA: Frontend optimization discipline beyond backend-scoped RUN policies.
- Evidence M1-S000858: `output/template/.claude/skills/angular/SKILL.md:188-191` — "Do not prematurely optimize normal Angular code. Use route lazy loading and ⏎ sensible rendering and data access first; introduce memoization, virtual ⏎ scrolling, custom change-detection work, or other optimizations after ⏎ identifying a real need."

### EXTRA-M1-0096
- Closest oracle policies: WF-020, SEC-003
- Modality: DEFAULT
- Normative action: In security review investigate deliberate sanitizer bypasses (bypassSecurityTrustHtml/Script/ResourceUrl) and direct DOM manipulation with untrusted content; ordinary Angular binding is sanitized.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: none
- Why EXTRA: Framework-specific review guidance not in the oracle.
- Evidence M1-S000860: `output/template/.claude/skills/angular/SKILL.md:195-198` — "Deliberate sanitizer bypasses deserve investigation during security review: ⏎ `bypassSecurityTrustHtml`, `bypassSecurityTrustScript`, ⏎ `bypassSecurityTrustResourceUrl`, and direct DOM manipulation with untrusted ⏎ content. Ordinary Angular binding is escaped/sanitized by the framework."

### EXTRA-M1-0097
- Closest oracle policies: DEP-024
- Modality: DEFAULT
- Normative action: Unit/component tests are colocated in the workspace; Playwright E2E tests, when required, live under frontend/<Name>.Web/e2e/.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: none
- Why EXTRA: Frontend test placement convention not in the oracle.
- Evidence M1-S000866: `output/template/.claude/skills/angular/SKILL.md:221-222` — "- Unit and component tests stay colocated in the workspace; Playwright E2E ⏎   tests, when required, live under `frontend/<Name>.Web/e2e/`."

### EXTRA-M1-0098
- Closest oracle policies: TST-002, API-022
- Modality: DEFAULT
- Normative action: When versions coexist test routing, version-specific shapes, deprecated versions operational during support, unsupported-version behaviour and shared behaviour consistency; no duplicated identical tests.
- Trigger/scope: on-demand knowledge skill api-versioning
- Exceptions: Coexisting versions.
- Why EXTRA: Version-specific test obligations not in the oracle.
- Evidence M1-S000895: `output/template/.claude/skills/api-versioning/SKILL.md:126-130` — "When versions coexist, test meaningful differences: version routing, ⏎ version-specific response shape, a deprecated version still operational during ⏎ its support period, unsupported-version behavior, and shared Application ⏎ behavior staying consistent where intended. Do not duplicate identical tests ⏎ merely because two versions share Application behavior."

### EXTRA-M1-0099
- Closest oracle policies: API-010
- Modality: MUST
- Normative action: Follow the project's established validation invocation pattern rather than adding a second competing mechanism.
- Trigger/scope: on-demand knowledge skill aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: Single-mechanism rule not in the oracle.
- Evidence M1-S000943: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:139-141` — "Register validators with `FluentValidation.DependencyInjectionExtensions` and ⏎ follow the project's established validation invocation pattern rather than ⏎ adding a second competing mechanism."

### EXTRA-M1-0100
- Closest oracle policies: API-009
- Modality: PREFER
- Normative action: If a Result pattern is adopted prefer typed errors over string arrays.
- Trigger/scope: on-demand knowledge skill aspnet-error-handling (backend)
- Exceptions: Adopted Result pattern.
- Why EXTRA: Shape preference not in the oracle.
- Evidence M1-S000955: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:189-190` — "would make every method return `Result<T>` without need. If adopted ⏎ (project-wide adoption is Reserved), prefer typed errors over string arrays:"

### EXTRA-M1-0248
- Closest oracle policies: API-010, ARC-010
- Modality: MUST_NOT
- Normative action: In a Controller-based project do not use Minimal API endpoint filters for validation.
- Trigger/scope: on-demand knowledge skill aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: Not stated in error-handling.md or the oracle.
- Evidence M1-S000958: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:200-206` — "Check-by-reference against `error-handling.md`: raw exception messages returned ⏎ to clients; inconsistent anonymous error objects; Application depending on HTTP ⏎ status codes; every method forced to return `Result<T>`; exceptions for every ⏎ negative branch; swallowed exceptions; catch/log/rethrow at every layer; ⏎ repeated logging; sensitive details in `ProblemDetails`; business rules only in ⏎ …"

### EXTRA-M1-0101
- Closest oracle policies: SEC-005
- Modality: PREFER
- Normative action: Prefer policies when authorization logic is more than a trivial role check.
- Trigger/scope: on-demand knowledge skill authentication
- Exceptions: none
- Why EXTRA: Mechanism preference not in the oracle.
- Evidence M1-S000964: `output/template/.claude/skills/authentication/SKILL.md:13-16` — "Authentication determines who the caller is; authorization determines what an ⏎ authenticated caller may do. Prefer policies when authorization logic is more ⏎ than a trivial role check, and keep ASP.NET Core transport/authentication types ⏎ out of Domain."

### EXTRA-M1-0102
- Closest oracle policies: SEC-016, ARC-020
- Modality: DEFAULT
- Normative action: Choose the scheme by application type: Bearer/OIDC for SPA→API, cookies for server-rendered apps, Identity for owned local accounts, external OIDC/OAuth for delegated identity.
- Trigger/scope: on-demand knowledge skill authentication
- Exceptions: none
- Why EXTRA: Scheme-selection mapping not in the oracle.
- Evidence M1-S000966: `output/template/.claude/skills/authentication/SKILL.md:20-23` — "Choose the scheme according to the actual application: Bearer/OIDC for an SPA ⏎ calling an API, cookies for server-rendered interactive web applications, ⏎ ASP.NET Core Identity when the application owns local users and passwords, an ⏎ external OpenID Connect/OAuth provider when identity is delegated."

### EXTRA-M1-0103
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Use stable constants for repeated policy names.
- Trigger/scope: on-demand knowledge skill authentication
- Exceptions: none
- Why EXTRA: Code-hygiene convention not in the oracle.
- Evidence M1-S000978: `output/template/.claude/skills/authentication/SKILL.md:82-82` — "Use stable constants for policy names repeated across the application."
- Evidence M1-S000997: `output/template/.claude/skills/authentication/SKILL.md:159-164` — "Check-by-reference against `security.md` § Authentication and Authorization: ⏎ custom password hashing; disabled token validation; hardcoded signing keys; ⏎ authorization only in the frontend; Application depending on `HttpContext`; ⏎ `401` for an authenticated-but-forbidden user or `403` for missing ⏎ authentication; logged tokens; scattered role/permission magic strings; ⏎ Identity, JWT issuance …"

### EXTRA-M1-0104
- Closest oracle policies: SEC-005
- Modality: PREFER
- Normative action: Roles only for genuinely role-oriented models; avoid scattered compound role strings; prefer policies for capabilities spanning roles/claims.
- Trigger/scope: on-demand knowledge skill authentication
- Exceptions: none
- Why EXTRA: Modelling preference not in the oracle.
- Evidence M1-S000980: `output/template/.claude/skills/authentication/SKILL.md:86-88` — "Roles fit when the business authorization model is genuinely role-oriented. ⏎ Avoid scattering compound role strings; prefer a policy when several roles or ⏎ claims represent one capability."
- Evidence M1-S000997: `output/template/.claude/skills/authentication/SKILL.md:159-164` — "Check-by-reference against `security.md` § Authentication and Authorization: ⏎ custom password hashing; disabled token validation; hardcoded signing keys; ⏎ authorization only in the frontend; Application depending on `HttpContext`; ⏎ `401` for an authenticated-but-forbidden user or `403` for missing ⏎ authentication; logged tokens; scattered role/permission magic strings; ⏎ Identity, JWT issuance …"

### EXTRA-M1-0105
- Closest oracle policies: TST-003, SEC-005
- Modality: DEFAULT
- Normative action: Test authorization for important protected operations: unauthenticated→401, unauthorized→403, permitted success, ownership rules, intended anonymous access.
- Trigger/scope: on-demand knowledge skill authentication
- Exceptions: none
- Why EXTRA: Security test obligations not in the oracle.
- Evidence M1-S000995: `output/template/.claude/skills/authentication/SKILL.md:151-155` — "Test authorization behavior for important protected operations: an ⏎ unauthenticated request → `401`; an authenticated caller without permission → ⏎ `403`; a permitted caller → expected success; resource-specific ownership rules; ⏎ anonymous endpoints remain accessible when intended. Verify observable behavior ⏎ rather than the mere presence of `[Authorize]`."

### EXTRA-M1-0106
- Closest oracle policies: WF-013
- Modality: MUST_NOT
- Normative action: Do not fabricate replacement APIs from memory when they can be verified.
- Trigger/scope: workflow build-fix (failing build or tests)
- Exceptions: none
- Why EXTRA: Verification obligation not in the oracle.
- Evidence M1-S001039: `output/template/.claude/skills/build-fix/SKILL.md:166-172` — "After a .NET, frontend framework, TypeScript, persistence-library, or other ⏎ framework upgrade: inspect the actual installed version, distinguish ⏎ compilation errors from changed runtime behavior, check official migration ⏎ documentation, update obsolete API usage deliberately, and preserve ⏎ architecture and behavior where the upgrade does not require change. Do not ⏎ fabricate replacement APIs …"

### EXTRA-M1-0107
- Closest oracle policies: DEP-008, WF-009
- Modality: MUST_NOT
- Normative action: Do not change declared SDK/Node/framework/language versions because the local machine differs; report an unresolvable toolchain limitation instead of editing source.
- Trigger/scope: workflow build-fix (failing build or tests)
- Exceptions: none
- Why EXTRA: Toolchain rule beyond the oracle.
- Evidence M1-S001041: `output/template/.claude/skills/build-fix/SKILL.md:176-183` — "Determine whether the failure comes from source code or from the local ⏎ toolchain (`dotnet --info`, `dotnet --version`, `node --version`, ⏎ `npm --version`; `global.json`, target framework, framework package versions, ⏎ `package-lock.json`, CI/runtime version configuration). Do not change the ⏎ repository's declared SDK, Node, framework, or language version merely because ⏎ the local machine has  …"

### EXTRA-M1-0108
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Build-fix report includes Initial failure, Root cause, Changes made and Remaining issues.
- Trigger/scope: workflow build-fix (failing build or tests)
- Exceptions: none
- Why EXTRA: Report field structure beyond WF-009.
- Evidence M1-S001055: `output/template/.claude/skills/build-fix/SKILL.md:238-246` — "```text ⏎ Initial failure: <failure> ⏎ Root cause: <cause> ⏎ Changes made: <changes> ⏎ Backend build: PASS / NOT RUN / NOT APPLICABLE ⏎ Frontend build: PASS / NOT RUN / NOT APPLICABLE ⏎ Tests: PASS / NOT RUN / NOT APPLICABLE ⏎ Remaining issues: None / <details> ⏎ ```"

### EXTRA-M1-0109
- Closest oracle policies: RUN-020
- Modality: DEFAULT
- Normative action: Centralize key construction when duplicated key formats become hard to maintain.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Key-construction organisation not in the oracle.
- Evidence M1-S001074: `output/template/.claude/skills/caching/SKILL.md:74-75` — "Centralize key construction when duplicated key formats become hard to ⏎ maintain."

### EXTRA-M1-0110
- Closest oracle policies: RUN-023
- Modality: MUST
- Normative action: Choose expiration from data semantics (change frequency, regeneration cost, staleness, memory, source-failure behaviour) rather than arbitrary universal defaults.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Forbids universal default TTLs; RUN-023 only requires some lifetime/invalidation.
- Evidence M1-S001076: `output/template/.claude/skills/caching/SKILL.md:79-81` — "Choose expiration from data semantics rather than arbitrary universal defaults: ⏎ change frequency, regeneration cost, acceptable staleness, memory footprint, ⏎ and failure behavior when the source is unavailable. Avoid unbounded entries."

### EXTRA-M1-0111
- Closest oracle policies: RUN-018
- Modality: MUST
- Normative action: Decide whether a cache failure falls back to the source, fails the request or returns stale data.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Explicit failure-policy decision not in the oracle.
- Evidence M1-S001086: `output/template/.claude/skills/caching/SKILL.md:118-119` — "Decide whether a cache failure falls back to the source, fails the request, or ⏎ returns stale data."

### EXTRA-M1-0112
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Test cache behaviour affecting correctness (invalidation after mutation, key isolation, miss fallback, outage policy); not framework internals.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Cache test obligations not in the oracle.
- Evidence M1-S001088: `output/template/.claude/skills/caching/SKILL.md:123-126` — "Test cache behavior when it affects observable correctness: stale entries are ⏎ invalidated after a successful mutation, tenant/user keys are isolated, a miss ⏎ falls back correctly, an outage follows the intended failure policy. Do not ⏎ unit-test framework cache internals."

### EXTRA-M1-0113
- Closest oracle policies: RUN-021, ARC-016
- Modality: MUST_NOT
- Normative action: Do not cache tracked persistence entities across Unit of Work boundaries.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Not stated in the oracle or in the cited owner rules.
- Evidence M1-S001090: `output/template/.claude/skills/caching/SKILL.md:130-136` — "Check-by-reference against `performance.md` § Caching and `architecture.md` ⏎ § Layer Placement: caching by default without a reason; global keys for ⏎ tenant/user data; mutable data cached indefinitely without invalidation; cache ⏎ technology in Domain; Application depending directly on `HybridCache` without a ⏎ deliberate decision; tracked persistence entities cached across Unit of Work ⏎ bounda …"

### EXTRA-M1-0114
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: Build deployable artifacts reproducibly and keep deployment/environment configuration outside compiled artifacts where practical.
- Trigger/scope: on-demand knowledge skill ci-cd (pipelines)
- Exceptions: Where practical.
- Why EXTRA: Delivery technique outside the oracle (EXC-014).
- Evidence M1-S001096: `output/template/.claude/skills/ci-cd/SKILL.md:13-15` — "Build deployable artifacts reproducibly, keep deployment/environment ⏎ configuration outside compiled artifacts where practical, and add pipeline ⏎ stages according to the actual project rather than generic boilerplate."

### EXTRA-M1-0115
- Closest oracle policies: WF-017
- Modality: MUST_NOT
- Normative action: Do not turn an optional local formatter into a mandatory CI gate without the project adopting that policy.
- Trigger/scope: on-demand knowledge skill ci-cd (pipelines)
- Exceptions: Project adoption.
- Why EXTRA: CI-gate restriction not in the oracle.
- Evidence M1-S001101: `output/template/.claude/skills/ci-cd/SKILL.md:32-35` — "Run formatting or analyzers when the repository has adopted them as enforced ⏎ checks, for example `dotnet format --verify-no-changes --no-restore`; do not ⏎ turn an optional local formatter into a mandatory CI gate without the project ⏎ adopting that policy."

### EXTRA-M1-0116
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: Store or publish only artifacts required by later stages.
- Trigger/scope: on-demand knowledge skill ci-cd (pipelines)
- Exceptions: none
- Why EXTRA: Artifact retention rule outside the oracle.
- Evidence M1-S001114: `output/template/.claude/skills/ci-cd/SKILL.md:120-121` — "Store or"

### EXTRA-M1-0117
- Closest oracle policies: WF-017
- Modality: PREFER
- Normative action: Prefer promoting the same tested artifact/image through environments over recompiling different production code per environment; environment behaviour from runtime configuration.
- Trigger/scope: on-demand knowledge skill ci-cd (pipelines)
- Exceptions: Promotion-capable deployment.
- Why EXTRA: Build-once/promote preference is outside the oracle (EXC-014).
- Evidence M1-S001118: `output/template/.claude/skills/ci-cd/SKILL.md:131-134` — "For a deployment model that supports artifact promotion, prefer promoting the ⏎ same tested artifact or image through environments over recompiling different ⏎ production code per environment; environment-specific behavior comes from ⏎ runtime configuration."

### EXTRA-M1-0118
- Closest oracle policies: SEC-002
- Modality: PREFER
- Normative action: Prefer workload/federated identity over long-lived deployment credentials when supported.
- Trigger/scope: on-demand knowledge skill ci-cd (pipelines)
- Exceptions: Platform support.
- Why EXTRA: Credential-type preference not in the oracle.
- Evidence M1-S001120: `output/template/.claude/skills/ci-cd/SKILL.md:138-140` — "Use the CI platform's secret/identity mechanism, never real secrets in pipeline ⏎ YAML, and prefer workload/federated identity over long-lived deployment ⏎ credentials when the platform supports it."

### EXTRA-M1-0119
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: CI and CD may be separate; a green CI does not imply deployment; use environment protection/approval appropriate to the platform.
- Trigger/scope: on-demand knowledge skill ci-cd (pipelines)
- Exceptions: none
- Why EXTRA: Deployment gating practice outside the oracle.
- Evidence M1-S001124: `output/template/.claude/skills/ci-cd/SKILL.md:152-154` — "CI and CD may be separate workflows. A successful CI build does not imply that ⏎ every branch deploys; use environment protection/approval where appropriate to ⏎ the hosting platform."

### EXTRA-M1-0120
- Closest oracle policies: WF-017, SEC-001
- Modality: MUST
- Normative action: Before a pipeline is complete confirm clean restore, backend build, frontend build when present, configured tests, no developer-machine dependence, no secret exposure and expected artifacts.
- Trigger/scope: on-demand knowledge skill ci-cd (pipelines)
- Exceptions: none
- Why EXTRA: Pipeline completion checklist beyond WF-017.
- Evidence M1-S001126: `output/template/.claude/skills/ci-cd/SKILL.md:158-161` — "Before considering a pipeline complete, confirm that it restores from a clean ⏎ environment, builds the backend, builds the frontend when present, runs ⏎ configured tests, does not depend on developer-machine state, does not expose ⏎ secrets, and produces the expected artifacts."

### EXTRA-M1-0121
- Closest oracle policies: WF-011
- Modality: MUST
- Normative action: Report findings by severity with severity, location, problem, impact and smallest fix, using the Critical/High/Medium/Low definitions.
- Trigger/scope: workflow code-review
- Exceptions: none
- Why EXTRA: Output format and severity scale not in the oracle.
- Evidence M1-S001163: `output/template/.claude/skills/code-review/SKILL.md:148-157` — "Report findings ordered by severity. For each finding give severity, ⏎ file/location, what is wrong, why it matters, and the smallest reasonable fix. ⏎  ⏎ - **Critical** — data loss, security vulnerability, reliably broken core ⏎   behavior, or another issue that should block use or merge immediately. ⏎ - **High** — likely defect or architectural/data-integrity issue that should be ⏎   fixed befor …"

### EXTRA-M1-0122
- Closest oracle policies: WF-012
- Modality: MUST_NOT
- Normative action: Do not add filler praise to balance criticism.
- Trigger/scope: workflow code-review
- Exceptions: none
- Why EXTRA: Output-tone rule not in WF-012.
- Evidence M1-S001164: `output/template/.claude/skills/code-review/SKILL.md:159-161` — "Do not manufacture findings to populate categories. When there are no ⏎ meaningful findings, say so and name important areas that could not be ⏎ verified. Do not add filler praise to balance criticism."

### EXTRA-M1-0123
- Closest oracle policies: RUN-015, GOV-010
- Modality: MUST
- Normative action: Example numeric values are not approved defaults; choose retry counts, timeouts, limits and similar operational values from actual integration/deployment requirements.
- Trigger/scope: on-demand knowledge skill configuration (backend)
- Exceptions: none
- Why EXTRA: Not entailed by the oracle.
- Evidence M1-S001175: `output/template/.claude/skills/configuration/SKILL.md:56-58` — "Numeric values in examples are illustrative, not approved defaults. Choose ⏎ retry counts, timeouts, limits, and similar operational values from the actual ⏎ integration and deployment requirements."
- Evidence M1-S001567: `output/template/.claude/skills/httpclient-factory/references/resilience.md:31-33` — "Distinguish the attempt timeout from the total operation timeout, especially ⏎ when retries are enabled, and choose values from actual latency requirements ⏎ rather than copying numbers from an example."
- Evidence M1-S001624: `output/template/.claude/skills/httpclient-factory/SKILL.md:111-113` — "Choose timeouts from the remote operation and the application's latency ⏎ budget. With resilience pipelines, distinguish the per-attempt timeout from the ⏎ total-operation timeout."
- Evidence M1-S001653: `output/template/.claude/skills/logging/references/serilog.md:72-76` — "The configuration below deliberately shows several optional sinks and ⏎ enrichers together. File, Seq, OpenTelemetry, Elasticsearch, and other sinks ⏎ are not baseline dependencies: configure only what the project needs — a ⏎ Console sink is enough for a simple local baseline. Numeric limits and retention ⏎ values are illustrative, not approved defaults."

### EXTRA-M1-0124
- Closest oracle policies: GOV-021, GOV-012
- Modality: AVOID
- Normative action: Avoid duplicating the same literal across layers when a single source in code or configuration is appropriate.
- Trigger/scope: workflow custom-settings
- Exceptions: none
- Why EXTRA: Single-source preference not in GOV-021.
- Evidence M1-S001197: `output/template/.claude/skills/custom-settings/SKILL.md:28-29` — "Avoid duplicating the same literal across many layers when a normal single ⏎ source in code or configuration is appropriate."

### EXTRA-M1-0125
- Closest oracle policies: ARC-021, ARC-007
- Modality: DEFAULT
- Normative action: Application services, repositories and external adapters use interface-to-implementation registration at boundaries; concrete registration for implementation-only helpers.
- Trigger/scope: on-demand knowledge skill dependency-injection (backend)
- Exceptions: Implementation-only helpers.
- Why EXTRA: Registration-shape rule not in the oracle.
- Evidence M1-S001212: `output/template/.claude/skills/dependency-injection/SKILL.md:16-18` — "contract. Prefer explicit registration in small applications, and add ⏎ convention scanning, keyed services, factories, or decorators only when they ⏎ solve an actual composition problem."
- Evidence M1-S001265: `output/template/.claude/skills/dependency-injection/SKILL.md:13-15` — "Application services, repositories, and external adapters use ⏎ interface-to-implementation registration at architectural boundaries; concrete ⏎ registration is fine for implementation-only helpers without a separate"

### EXTRA-M1-0126
- Closest oracle policies: GOV-012
- Modality: DEFAULT
- Normative action: Keyed services only for key-selected implementations; decorators for cross-cutting wrapping; assembly scanning only for genuinely repetitive registration and over the owning assembly.
- Trigger/scope: on-demand knowledge skill dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Optional DI technique (EXC-005).
- Evidence M1-S001221: `output/template/.claude/skills/dependency-injection/SKILL.md:67-69` — "Use keyed services when multiple implementations of one abstraction are ⏎ selected by a known key, not when a single registration or a simple explicit ⏎ factory is clearer."
- Evidence M1-S001224: `output/template/.claude/skills/dependency-injection/SKILL.md:89-90` — "Use a decorator when the same cross-cutting behavior should wrap an abstraction ⏎ without changing its implementation."
- Evidence M1-S001230: `output/template/.claude/skills/dependency-injection/SKILL.md:158-161` — "Prefer explicit registrations in small and medium projects because they are ⏎ easy to discover and debug. Use assembly scanning when registration volume ⏎ creates genuine repetitive boilerplate, and scan the assembly that actually ⏎ owns the services — not accidentally only the API assembly."

### EXTRA-M1-0127
- Closest oracle policies: DEP-019, ARC-002
- Modality: DEFAULT
- Normative action: Keep images reproducible and configuration external, keep Docker concerns out of application architecture (Domain/Application), use platform health probes when practical.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: When practical.
- Why EXTRA: Container practices outside the oracle (EXC-006).
- Evidence M1-S001269: `output/template/.claude/skills/docker/SKILL.md:13-16` — "Keep build tooling out of production runtime images, keep images reproducible ⏎ and configuration external, keep Docker concerns separate from application ⏎ architecture, and use the deployment platform's health-probe capabilities when ⏎ practical."
- Evidence M1-S001299: `output/template/.claude/skills/docker/SKILL.md:158-163` — "Check-by-reference against `security.md` § Containers and `verify` § Delivery ⏎ Changes: SDK image as production runtime; root execution without a concrete ⏎ reason; secrets baked into images; arbitrary infrastructure in Compose; assumed ⏎ `curl`/`wget`; automatic production database migration; specialized image ⏎ variants without compatibility verification; Docker-specific changes leaking ⏎ into  …"

### EXTRA-M1-0128
- Closest oracle policies: DEP-019
- Modality: DEFAULT
- Normative action: Use a multi-stage build for ASP.NET Core Dockerfiles.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Dockerfile shape is technique outside the oracle.
- Evidence M1-S001271: `output/template/.claude/skills/docker/SKILL.md:20-20` — "Use a multi-stage build:"

### EXTRA-M1-0129
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Copy only present build files needed by restore (do not add them to satisfy the Dockerfile); copy project files explicitly without flattening wildcards.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Dockerfile technique.
- Evidence M1-S001273: `output/template/.claude/skills/docker/SKILL.md:55-58` — "The example assumes the repository-level build files exist; copy only build ⏎ files that are present and required by restore, and do not add them merely to ⏎ satisfy the Dockerfile. Copy project files required for restore explicitly; do ⏎ not use wildcard tricks that flatten or rearrange the multi-project structure."

### EXTRA-M1-0130
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Copy project/build-dependency files before full source; update the copy section with structure changes; never sacrifice restoring the real project graph for caching.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Restore caching technique.
- Evidence M1-S001275: `output/template/.claude/skills/docker/SKILL.md:62-65` — "Copy project and build-dependency files before the full source tree so source ⏎ changes do not invalidate NuGet restore layers. Update the project-copy section ⏎ when the solution structure changes; never optimize layer caching at the cost of ⏎ a Dockerfile that no longer restores the real project graph."

### EXTRA-M1-0131
- Closest oracle policies: DEP-019
- Modality: DEFAULT
- Normative action: Use the built-in non-root user (USER app) when it fits the image and deployment.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: When it fits.
- Why EXTRA: Beyond DEP-019's 'do not switch to root to bypass problems'.
- Evidence M1-S001279: `output/template/.claude/skills/docker/SKILL.md:74-76` — "Use the built-in non-root user of modern .NET images when it fits the image and ⏎ deployment environment (`USER app`), and give directories the application ⏎ writes to appropriate ownership and permissions."

### EXTRA-M1-0132
- Closest oracle policies: SEC-002
- Modality: DEFAULT
- Normative action: Pass environment-specific configuration at runtime (ASPNETCORE_ENVIRONMENT, ConnectionStrings__Default, Authentication__Authority).
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Container configuration practice not in the oracle.
- Evidence M1-S001281: `output/template/.claude/skills/docker/SKILL.md:80-84` — "Pass environment-specific configuration at runtime, for example ⏎ `ASPNETCORE_ENVIRONMENT`, `ConnectionStrings__Default`, ⏎ `Authentication__Authority`. Real credentials never go into a Dockerfile, ⏎ committed Compose files, build arguments visible in image metadata, or copied ⏎ appsettings files; use platform or container secret mechanisms."

### EXTRA-M1-0133
- Closest oracle policies: API-019
- Modality: DEFAULT
- Normative action: Expose liveness/readiness via ASP.NET Core health checks, prefer orchestrator HTTP probes, do not assume curl/wget/shell in runtime images; verify or add a probe mechanism weighing debug-package cost.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Probe mechanics outside the oracle (EXC-006).
- Evidence M1-S001287: `output/template/.claude/skills/docker/SKILL.md:110-115` — "Expose liveness/readiness endpoints through ASP.NET Core health checks ⏎ (`health-check` skill) and prefer the orchestrator's native HTTP probes. Do not ⏎ assume the runtime image contains `curl`, `wget`, or shell utilities; when ⏎ Compose must run an in-container health command, verify the executable exists or ⏎ add an appropriate probe mechanism, weighing the cost of installing debugging ⏎ packa …"
- Evidence M1-S001299: `output/template/.claude/skills/docker/SKILL.md:158-163` — "Check-by-reference against `security.md` § Containers and `verify` § Delivery ⏎ Changes: SDK image as production runtime; root execution without a concrete ⏎ reason; secrets baked into images; arbitrary infrastructure in Compose; assumed ⏎ `curl`/`wget`; automatic production database migration; specialized image ⏎ variants without compatibility verification; Docker-specific changes leaking ⏎ into  …"

### EXTRA-M1-0134
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: For static frontend deployment build in a Node stage and serve assets with the selected hosting strategy (Nginx not mandatory); keep API base URLs/config compatible.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Frontend container technique.
- Evidence M1-S001289: `output/template/.claude/skills/docker/SKILL.md:119-122` — "When the frontend is deployed as a static application, build it in a Node build ⏎ stage and serve the generated assets with the selected hosting strategy; Nginx ⏎ is not mandatory, since the platform may provide static hosting. Keep API base ⏎ URLs and environment configuration compatible with that strategy."

### EXTRA-M1-0135
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Exclude non-build content from the build context; do not exclude tests the image build runs or files required by restore/build.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Build-context hygiene.
- Evidence M1-S001291: `output/template/.claude/skills/docker/SKILL.md:126-126` — "Exclude what does not belong in the build context:"
- Evidence M1-S001293: `output/template/.claude/skills/docker/SKILL.md:138-139` — "Do not exclude tests when the image build intentionally runs them, and never ⏎ exclude files required by restore or build."

### EXTRA-M1-0136
- Closest oracle policies: DEP-019
- Modality: DEFAULT
- Normative action: Start with standard runtime images; Alpine/chiseled/trimming/Native AOT only when justified, verifying globalization, native dependencies, reflection and diagnostics.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: Justified by compatibility/deployment needs.
- Why EXTRA: Image optimization discipline (EXC-006).
- Evidence M1-S001295: `output/template/.claude/skills/docker/SKILL.md:143-147` — "Start with standard supported .NET runtime images. Consider Alpine, chiseled ⏎ images, trimming, Native AOT, or other size optimizations only when ⏎ compatibility and deployment requirements justify them, and verify ⏎ globalization, native dependencies, reflection, and diagnostics when using ⏎ specialized images."
- Evidence M1-S001299: `output/template/.claude/skills/docker/SKILL.md:158-163` — "Check-by-reference against `security.md` § Containers and `verify` § Delivery ⏎ Changes: SDK image as production runtime; root execution without a concrete ⏎ reason; secrets baked into images; arbitrary infrastructure in Compose; assumed ⏎ `curl`/`wget`; automatic production database migration; specialized image ⏎ variants without compatibility verification; Docker-specific changes leaking ⏎ into  …"

### EXTRA-M1-0137
- Closest oracle policies: WF-006
- Modality: MUST
- Normative action: For Docker changes build the image, verify startup, ports/configuration, non-root behaviour, health probes, review for accidental secrets/files, and run meaningful tests.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: As relevant.
- Why EXTRA: Docker verification checklist beyond the oracle.
- Evidence M1-S001297: `output/template/.claude/skills/docker/SKILL.md:151-154` — "For Docker changes: build the image, verify application startup, required ⏎ port/configuration, non-root behavior when relevant, and health-probe ⏎ integration, and review the image for accidental secrets or files. Run ⏎ meaningful application tests outside or as part of the build pipeline."

### EXTRA-M1-0138
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Mock or fake architectural boundaries when that makes the behaviour under test clearer.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Mocking technique outside the oracle (EXC-012).
- Evidence M1-S001312: `output/template/.claude/skills/dotnet-testing/SKILL.md:70-74` — "Mock or fake architectural boundaries when that makes the"

### EXTRA-M1-0139
- Closest oracle policies: TST-004
- Modality: DEFAULT
- Normative action: Keep slow or unreliable external-system tests separate from ordinary fast runs.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Test-suite partitioning not in the oracle.
- Evidence M1-S001329: `output/template/.claude/skills/dotnet-testing/SKILL.md:181-185` — "At the relevant boundary use a fake or mock abstraction for unit tests, a stub ⏎ `HttpMessageHandler`, WireMock or another local fake server for HTTP ⏎ integration, or a dedicated sandbox only when the test explicitly targets that ⏎ integration. Keep slow or unreliable external-system tests separate from ⏎ ordinary fast runs."

### EXTRA-M1-0140
- Closest oracle policies: TST-008, GOV-012
- Modality: DEFAULT
- Normative action: Keep test data explicit and minimal; builders/fixtures only when repeated setup gets hard to read; no generic test-data framework for a few objects.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Builder technique (EXC-012).
- Evidence M1-S001331: `output/template/.claude/skills/dotnet-testing/SKILL.md:189-191` — "Keep test data explicit and minimal. Introduce builders, fixtures, or factories ⏎ when repeated setup becomes hard to read; do not introduce a generic test-data ⏎ framework for a few simple objects."

### EXTRA-M1-0141
- Closest oracle policies: TST-010
- Modality: MUST
- Normative action: Review a temporary probe before keeping it as a permanent test.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Added review step.
- Evidence M1-S001335: `output/template/.claude/skills/dotnet-testing/SKILL.md:203-208` — "Typical temporary probes to convert (`verify` § Preserve Behavioral ⏎ Verification): HTTP requests used to check an endpoint, PowerShell or shell ⏎ scripts that exercise behavior, ad-hoc test methods, manual database checks, ⏎ temporary regression probes. For example, replace an ad-hoc `curl` or REST ⏎ request with an NUnit integration test using `WebApplicationFactory`. Review a ⏎ temporary probe …"

### EXTRA-M1-0142
- Closest oracle policies: TST-003
- Modality: AVOID
- Normative action: Avoid assertion-free tests unless the behaviour is 'does not throw'.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: 'Does not throw' behaviour.
- Why EXTRA: Not stated in testing.md or the oracle.
- Evidence M1-S001341: `output/template/.claude/skills/dotnet-testing/SKILL.md:223-228` — "Check-by-reference against `.claude/rules/testing.md`: private implementation ⏎ details tested; every class mocked; production resources reached; shared ⏎ mutable state between tests; assertions that repeat the implementation; ⏎ assertion-free tests (unless the behavior is "does not throw"); arbitrary delays ⏎ such as `Task.Delay`; Testcontainers without a provider-fidelity need; an ⏎ in-memory pr …"

### EXTRA-M1-0143
- Closest oracle policies: DEP-013
- Modality: DEFAULT
- Normative action: Create test projects with the NUnit template (dotnet new nunit).
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Tooling technique not in the oracle.
- Evidence M1-S001343: `output/template/.claude/skills/dotnet-testing/SKILL.md:232-235` — "- Create test projects with the NUnit template (`dotnet new nunit`) at the ⏎   locations and with the references the `project-structure` workflow defines, ⏎   then remove properties duplicated by `Directory.Build.props` and package ⏎   versions duplicated by Central Package Management."

### EXTRA-M1-0144
- Closest oracle policies: ARC-019
- Modality: DEFAULT
- Normative action: Keep entity configuration separate with IEntityTypeConfiguration<T>.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: EF technique not in the oracle.
- Evidence M1-S001354: `output/template/.claude/skills/ef-core/SKILL.md:25-25` — "Keep entity configuration separate with `IEntityTypeConfiguration<T>`:"

### EXTRA-M1-0145
- Closest oracle policies: ARC-027, PST-003
- Modality: DEFAULT
- Normative action: Adapter-layer persistence layout: Persistence/{AppDbContext.cs, UnitOfWork.cs, Configurations/, Repositories/, Migrations/, Seeding/{DbSeeder.cs, DatabaseInitializationExtensions.cs}}.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Folder convention outside the oracle (co-change detection assumes it).
- Evidence M1-S001367: `output/template/.claude/skills/ef-core/SKILL.md:132-143` — "```text ⏎ <adapter-layer project>/ ⏎   Persistence/ ⏎     AppDbContext.cs ⏎     UnitOfWork.cs ⏎     Configurations/ ⏎     Repositories/ ⏎     Migrations/ ⏎     Seeding/ ⏎       DbSeeder.cs ⏎       DatabaseInitializationExtensions.cs ⏎ ```"

### EXTRA-M1-0146
- Closest oracle policies: RUN-006
- Modality: DEFAULT
- Normative action: Tracking queries for entities modified in the current UoW; AsNoTracking for read-only entity queries; not mechanically on DTO projections.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Tracking technique (EXC-011).
- Evidence M1-S001376: `output/template/.claude/skills/ef-core/SKILL.md:183-186` — "Use tracking queries when loaded entities will be modified and committed ⏎ through the current Unit of Work. Use `AsNoTracking()` for read-only entity ⏎ queries where change tracking provides no value; do not add it mechanically to ⏎ projections that already produce non-entity DTOs."

### EXTRA-M1-0147
- Closest oracle policies: RUN-006
- Modality: PREFER
- Normative action: Prefer explicit query shape (projection or Include/ThenInclude); consider split queries for large collection includes and verify generated SQL/performance.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Query technique (EXC-011).
- Evidence M1-S001382: `output/template/.claude/skills/ef-core/SKILL.md:204-208` — "Prefer an explicit query shape: projection when only selected related data is ⏎ needed, `Include`/`ThenInclude` when the entity graph itself is required. Avoid ⏎ lazy loading by default because it hides database access and causes N+1 ⏎ queries. For large collection includes, consider split queries and verify the ⏎ generated SQL and performance."

### EXTRA-M1-0148
- Closest oracle policies: RUN-006
- Modality: MUST
- Normative action: Paged queries always use a deterministic order.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Not stated in RUN-006.
- Evidence M1-S001384: `output/template/.claude/skills/ef-core/SKILL.md:212-213` — "Apply filtering, ordering, and pagination in the database, always with a ⏎ deterministic order:"

### EXTRA-M1-0149
- Closest oracle policies: RUN-021, ARC-016
- Modality: MUST_NOT
- Normative action: Do not casually mix ExecuteUpdateAsync/ExecuteDeleteAsync with tracked entities for the same rows; understand transaction/consistency implications.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Bulk-operation caution not in the oracle.
- Evidence M1-S001390: `output/template/.claude/skills/ef-core/SKILL.md:245-247` — "They execute directly against the database and bypass change tracking; do not ⏎ mix them casually with tracked entities representing the same rows, and ⏎ understand their transaction and consistency implications."

### EXTRA-M1-0150
- Closest oracle policies: ARC-018
- Modality: MUST_NOT
- Normative action: Do not attempt to solve distributed transactions with EF Core transaction APIs.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Not stated in the oracle.
- Evidence M1-S001392: `output/template/.claude/skills/ef-core/SKILL.md:251-254` — "An explicit transaction fits when a concrete use case needs multiple database ⏎ operations or multiple `SaveChangesAsync` calls to succeed atomically ⏎ (`persistence-technology.md` § Transactions). Do not attempt to solve ⏎ distributed transactions with EF Core transaction APIs."

### EXTRA-M1-0151
- Closest oracle policies: API-011, ARC-019
- Modality: MUST_NOT
- Normative action: Do not hide business behaviour in persistence interceptors.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Interceptor restriction not in the oracle (EXC-011).
- Evidence M1-S001398: `output/template/.claude/skills/ef-core/SKILL.md:297-297` — "Do not hide business behavior in persistence interceptors."

### EXTRA-M1-0152
- Closest oracle policies: WF-019
- Modality: PREFER
- Normative action: For controlled production deployment generated idempotent migration scripts are often preferable.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Deployment-artifact preference beyond WF-019.
- Evidence M1-S001407: `output/template/.claude/skills/ef-core/SKILL.md:372-375` — "Commands and the review checklist: `persistence-change` § Migrations; seed ⏎ co-change: `persistence-change` § Seed Data. For controlled production deployment, generated migration scripts ⏎ (`dotnet ef migrations script --idempotent`) are often preferable; production ⏎ migration runs as an explicit deployment step."

### EXTRA-M1-0153
- Closest oracle policies: DEP-006
- Modality: DEFAULT
- Normative action: Add Microsoft.EntityFrameworkCore.Design to the startup project when migrations are created from the CLI, and use the dotnet-ef tool.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: When migrations come from the CLI.
- Why EXTRA: Tooling technique not in the oracle.
- Evidence M1-S001413: `output/template/.claude/skills/ef-core/SKILL.md:393-396` — "- Packages (through `add-dependency`): `Microsoft.EntityFrameworkCore.SqlServer` ⏎   in the adapter-layer project; `Microsoft.EntityFrameworkCore.Design` in the ⏎   startup project when migrations are created from the CLI; the `dotnet-ef` ⏎   tool."

### EXTRA-M1-0154
- Closest oracle policies: RUN-002
- Modality: MUST_NOT
- Normative action: Do not use fire-and-forget EF asynchronous operations.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Not stated in the oracle or the cited owner rules.
- Evidence M1-S001418: `output/template/.claude/skills/ef-core/SKILL.md:413-420` — "Check-by-reference against `persistence-technology.md` and `architecture.md`: ⏎ `DbContext`, `DbSet<T>`, or EF-backed `IQueryable<T>` exposed outside the ⏎ adapter layer; the use-case layer depending on EF Core; a generic CRUD contract ⏎ exposed to the use-case layer; `SaveChangesAsync` called from every repository ⏎ operation; all rows loaded and filtered in memory; lazy loading by default; ⏎ fir …"

### EXTRA-M1-0155
- Closest oracle policies: GOV-016
- Modality: DEFAULT
- Normative action: Follow an existing branch-naming convention, otherwise prefixes like feature/, fix/, refactor/, test/, docs/, chore/; meaningful names; do not rename existing user branches for it.
- Trigger/scope: workflow git-workflow
- Exceptions: Existing convention.
- Why EXTRA: Branch naming not in the oracle.
- Evidence M1-S001432: `output/template/.claude/skills/git-workflow/SKILL.md:38-41` — "Follow an existing branch-naming convention when one exists. Otherwise clear ⏎ prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, and ⏎ `chore/` are reasonable defaults. Use meaningful names, and do not rename an ⏎ existing user branch merely to satisfy this convention."

### EXTRA-M1-0156
- Closest oracle policies: GOV-016
- Modality: MUST_NOT
- Normative action: One branch must not be checked out simultaneously in multiple normal worktrees.
- Trigger/scope: workflow git-workflow
- Exceptions: none
- Why EXTRA: Not stated in GOV-016.
- Evidence M1-S001434: `output/template/.claude/skills/git-workflow/SKILL.md:45-47` — "Parallel implementation streams use separate branches or worktrees ⏎ (`CLAUDE.md` § Git). One branch must not be checked out simultaneously in ⏎ multiple normal worktrees. Keep each worktree focused on its branch's concern."

### EXTRA-M1-0157
- Closest oracle policies: WF-022
- Modality: PREFER
- Normative action: Prefer one logical change per commit with implementation and protecting tests together by default; no artificial tiny commits.
- Trigger/scope: workflow git-workflow
- Exceptions: none
- Why EXTRA: Commit granularity beyond WF-022.
- Evidence M1-S001437: `output/template/.claude/skills/git-workflow/SKILL.md:54-56` — "Prefer one logical change per commit; implementation and the tests that protect ⏎ it belong to the same commit by default. Do not create artificial tiny commits or ⏎ combine unrelated fixes or refactors."

### EXTRA-M1-0158
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Follow the repository commit convention or Conventional Commits; use the body for important motivation/constraints/migration notes; do not narrate obvious diffs.
- Trigger/scope: workflow git-workflow
- Exceptions: Existing convention.
- Why EXTRA: Commit-message convention not in the oracle.
- Evidence M1-S001438: `output/template/.claude/skills/git-workflow/SKILL.md:58-59` — "Follow the repository's commit-message convention. When none exists, ⏎ Conventional Commits are a useful default:"
- Evidence M1-S001440: `output/template/.claude/skills/git-workflow/SKILL.md:70-71` — "Use the body when important motivation, constraints, or migration information ⏎ would otherwise be lost; do not narrate obvious diff details."

### EXTRA-M1-0159
- Closest oracle policies: WF-003
- Modality: MUST
- Normative action: Ensure relevant verification has completed before pushing.
- Trigger/scope: workflow git-workflow
- Exceptions: none
- Why EXTRA: Pre-push verification gate not in the oracle.
- Evidence M1-S001442: `output/template/.claude/skills/git-workflow/SKILL.md:75-80` — "Before pushing: confirm the intended branch, confirm the working and staged ⏎ state is understood, ensure relevant verification has completed, and avoid ⏎ pushing unrelated local commits. Never force-push a shared branch unless the ⏎ user explicitly requests history rewriting and the consequences are understood; ⏎ treat `main`, `master`, and other protected or shared branches as ⏎ non-rewritable."

### EXTRA-M1-0160
- Closest oracle policies: GOV-015
- Modality: MUST_NOT
- Normative action: Treat main, master and other protected/shared branches as non-rewritable.
- Trigger/scope: workflow git-workflow
- Exceptions: none
- Why EXTRA: Stricter than GOV-015.
- Evidence M1-S001442: `output/template/.claude/skills/git-workflow/SKILL.md:75-80` — "Before pushing: confirm the intended branch, confirm the working and staged ⏎ state is understood, ensure relevant verification has completed, and avoid ⏎ pushing unrelated local commits. Never force-push a shared branch unless the ⏎ user explicitly requests history rewriting and the consequences are understood; ⏎ treat `main`, `master`, and other protected or shared branches as ⏎ non-rewritable."

### EXTRA-M1-0161
- Closest oracle policies: GOV-015
- Modality: MUST
- Normative action: Follow team convention or explicit request for merge vs rebase; resolve conflicts from intended combined behaviour (not mechanical ours/theirs); run relevant verification afterwards.
- Trigger/scope: workflow git-workflow
- Exceptions: none
- Why EXTRA: Merge practice beyond the oracle.
- Evidence M1-S001444: `output/template/.claude/skills/git-workflow/SKILL.md:84-89` — "Follow the repository/team convention or the user's explicit request rather ⏎ than personal preference. Before either operation, inspect local uncommitted ⏎ work; do not automatically stash, reset, or discard work to make the operation ⏎ proceed. Resolve conflicts from the intended combined behavior, not by ⏎ mechanically choosing "ours" or "theirs", and run relevant verification after ⏎ resolutio …"

### EXTRA-M1-0162
- Closest oracle policies: WF-003, WF-022
- Modality: MUST
- Normative action: Run verify before preparing a PR; PRs have a focused purpose; descriptions explain what/why/how verified and compatibility/migration notes.
- Trigger/scope: workflow git-workflow
- Exceptions: none
- Why EXTRA: PR rules not in the oracle.
- Evidence M1-S001446: `output/template/.claude/skills/git-workflow/SKILL.md:93-96` — "Before preparing a PR, run `verify`. A PR has a focused purpose without ⏎ accidental unrelated changes. A useful description explains what changed, why, ⏎ how it was verified, and important compatibility or migration notes. Do not ⏎ claim checks were run if they were not."

### EXTRA-M1-0163
- Closest oracle policies: WF-009
- Modality: ALLOWED
- Normative action: Report the actual resulting state after Git operations when useful.
- Trigger/scope: workflow git-workflow
- Exceptions: When useful.
- Why EXTRA: Reporting practice beyond the oracle.
- Evidence M1-S001450: `output/template/.claude/skills/git-workflow/SKILL.md:107-109` — "After Git operations, report the actual resulting state when useful: branch, ⏎ commit created, push target, PR preparation status, and uncommitted changes ⏎ that remain."

### EXTRA-M1-0164
- Closest oracle policies: API-019
- Modality: DEFAULT
- Normative action: Register readiness checks with tags (and map readiness endpoints by tag).
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Tagging technique (EXC-010).
- Evidence M1-S001463: `output/template/.claude/skills/health-check/SKILL.md:47-48` — "Register readiness checks with tags:"

### EXTRA-M1-0165
- Closest oracle policies: API-018
- Modality: DEFAULT
- Normative action: Use provider/framework health-check integration where suitable.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: Where suitable.
- Why EXTRA: Implementation preference not in the oracle.
- Evidence M1-S001470: `output/template/.claude/skills/health-check/SKILL.md:78-80` — "A database check performs a lightweight connectivity/availability check — ⏎ no expensive business queries, large scans, or writes. Use provider/framework ⏎ health-check integration where suitable."

### EXTRA-M1-0166
- Closest oracle policies: API-019
- Modality: MUST_NOT
- Normative action: Health endpoints return success when healthy and non-success when unhealthy per probe policy; do not reuse business API status semantics mechanically for probes.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Probe status semantics outside the oracle.
- Evidence M1-S001474: `output/template/.claude/skills/health-check/SKILL.md:91-94` — "Health endpoints return success when healthy and a non-success status when ⏎ unhealthy according to the configured probe policy; `HealthCheckOptions` allows ⏎ status-code mapping. Do not reuse business API status-code semantics ⏎ mechanically for orchestrator probes."

### EXTRA-M1-0167
- Closest oracle policies: API-020
- Modality: DEFAULT
- Normative action: Choose health endpoint exposure by deployment topology (internal network, management port, host restrictions, authorization where supported).
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Exposure mechanics (EXC-010).
- Evidence M1-S001478: `output/template/.claude/skills/health-check/SKILL.md:103-106` — "Health endpoints often need to be reachable by infrastructure without user ⏎ authentication. Choose exposure by deployment topology: private/internal ⏎ network access, a dedicated management port, host restrictions, or ⏎ authorization where the probe infrastructure supports it."

### EXTRA-M1-0168
- Closest oracle policies: RUN-013
- Modality: AVOID
- Normative action: Avoid Error-level logs for every normal failed probe.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence M1-S001480: `output/template/.claude/skills/health-check/SKILL.md:110-112` — "Health checks may be called frequently: avoid expensive queries, long external ⏎ timeouts, large allocations, full business workflows, and Error-level logs for ⏎ every normal failed probe."

### EXTRA-M1-0169
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Test meaningful health configuration when deployment relies on it; no elaborate tests of uncustomized framework behaviour.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: When deployment relies on it.
- Why EXTRA: Health test obligations not in the oracle.
- Evidence M1-S001482: `output/template/.claude/skills/health-check/SKILL.md:116-120` — "Test meaningful health configuration when deployment relies on it: the live ⏎ endpoint responds when healthy, readiness changes with a required dependency, ⏎ responses do not leak sensitive details, optional-dependency behavior matches ⏎ the intended semantics. Do not build elaborate tests for framework behavior the ⏎ application does not customize."

### EXTRA-M1-0170
- Closest oracle policies: API-018
- Modality: AVOID
- Normative action: Do not use health checks as a code-quality grading system.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Not stated in api.md or the oracle.
- Evidence M1-S001484: `output/template/.claude/skills/health-check/SKILL.md:124-127` — "Check-by-reference against `api.md` § Health Checks: health checks used as a ⏎ code-quality grading system; database writes or business transactions from ⏎ probes; every dependency on liveness; expensive queries; secrets or stack traces ⏎ in responses; remote dependency chains without operational justification."

### EXTRA-M1-0171
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Observe retries, timeouts and circuit behaviour when material; give important production circuit breakers operational visibility.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: When material.
- Why EXTRA: Observability obligation not in the oracle.
- Evidence M1-S001561: `output/template/.claude/skills/httpclient-factory/references/resilience.md:5-9` — "Resilience policies match failure and operation semantics. Circuit breakers ⏎ help when repeated dependency failures would otherwise consume resources or ⏎ amplify an outage. Do not add resilience mechanisms merely because they are ⏎ available, and observe retries, timeouts, and circuit behavior when they ⏎ materially affect operations."

### EXTRA-M1-0172
- Closest oracle policies: RUN-016
- Modality: MUST_NOT
- Normative action: Do not retry validation errors, auth failures, permanent 404s or deterministic business rejections.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: Explicit categories beyond RUN-016.
- Evidence M1-S001569: `output/template/.claude/skills/httpclient-factory/references/resilience.md:37-41` — "Plausibly transient failures: selected network failures, temporary service ⏎ unavailability, rate limiting when retry is allowed, transient provider-specific ⏎ database failures. Not retried: validation errors, authentication/authorization ⏎ failures, permanent `404` outcomes, deterministic business rejection, and ⏎ non-idempotent operations without a duplicate-prevention strategy."

### EXTRA-M1-0173
- Closest oracle policies: RUN-016
- Modality: MUST_NOT
- Normative action: Do not invent a client-side Idempotency-Key unless the remote service supports it.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: Not in RUN-016.
- Evidence M1-S001575: `output/template/.claude/skills/httpclient-factory/references/resilience.md:57-59` — "If the answer is "duplicate side effect", automatic retry is unsafe. Use an ⏎ API-supported idempotency mechanism when appropriate; do not invent a ⏎ client-side `Idempotency-Key` unless the remote service supports that contract."

### EXTRA-M1-0174
- Closest oracle policies: RUN-015
- Modality: DEFAULT
- Normative action: Use a circuit breaker only for meaningful repeated-failure patterns that would add load/latency.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: Circuit breaker technique (EXC-007).
- Evidence M1-S001577: `output/template/.claude/skills/httpclient-factory/references/resilience.md:63-65` — "Use one when repeated calls to a failing dependency create additional load or ⏎ latency; not for a dependency without a meaningful repeated-failure pattern. ⏎ Give an important production circuit breaker operational visibility."
- Evidence M1-S001594: `output/template/.claude/skills/httpclient-factory/references/resilience.md:121-127` — "Check-by-reference against `performance.md` § Outbound Calls: retrying every ⏎ exception or HTTP status; retrying unsafe writes without idempotency analysis; ⏎ retrying client cancellation; circuit breakers without a failure scenario; ⏎ fallback values that conceal incorrect business results; hedged writes; generic ⏎ retry wrappers around persistence without understanding provider behavior; ⏎ stac …"

### EXTRA-M1-0175
- Closest oracle policies: RUN-016
- Modality: MUST_NOT
- Normative action: Do not wrap persistence in a generic application retry pipeline; prefer the provider's execution strategy and its transaction/retry guidance; HTTP retry policies are not automatically appropriate for databases.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: Database retry technique (EXC-007).
- Evidence M1-S001584: `output/template/.claude/skills/httpclient-factory/references/resilience.md:86-91` — "Do not wrap normal persistence operations in a generic application-level retry ⏎ pipeline. When the persistence provider supports transient retry through its ⏎ execution strategy or provider configuration, prefer that mechanism, and handle ⏎ transaction/retry interaction according to the provider's guidance (persistence ⏎ knowledge skill). An HTTP retry policy is not automatically appropriate for  …"
- Evidence M1-S001594: `output/template/.claude/skills/httpclient-factory/references/resilience.md:121-127` — "Check-by-reference against `performance.md` § Outbound Calls: retrying every ⏎ exception or HTTP status; retrying unsafe writes without idempotency analysis; ⏎ retrying client cancellation; circuit breakers without a failure scenario; ⏎ fallback values that conceal incorrect business results; hedged writes; generic ⏎ retry wrappers around persistence without understanding provider behavior; ⏎ stac …"

### EXTRA-M1-0176
- Closest oracle policies: RUN-016
- Modality: DEFAULT
- Normative action: Publication retries can duplicate delivery; use idempotent consumers/deduplication/outbox when required and never claim exactly-once because of retries.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: When required.
- Why EXTRA: Message delivery technique (EXC-007).
- Evidence M1-S001586: `output/template/.claude/skills/httpclient-factory/references/resilience.md:95-99` — "Retrying message publication requires understanding the broker and delivery ⏎ semantics; a retry may produce duplicate delivery. Use idempotent consumers, ⏎ broker-supported deduplication, outbox patterns, or similar mechanisms when the ⏎ business requirement needs them, and do not claim exactly-once delivery because ⏎ a retry policy exists."

### EXTRA-M1-0177
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: Inbound rate limiting is distinct from outbound resilience; rejected requests receive 429 with Retry-After when known.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: Rate-limiting semantics not in the oracle.
- Evidence M1-S001588: `output/template/.claude/skills/httpclient-factory/references/resilience.md:103-106` — "ASP.NET Core rate limiting protects this API from excessive incoming traffic ⏎ and is different from outbound resilience. A rejected request receives ⏎ `429 Too Many Requests`, with `Retry-After` when a useful delay is known ⏎ (`http-api` skill)."

### EXTRA-M1-0178
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: Keep status-code behaviour consistent across similar endpoints (e.g. one convention for repeated DELETE of an absent resource: 204 or 404, not mixed).
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Consistency obligation not in the oracle.
- Evidence M1-S001488: `output/template/.claude/skills/http-api/SKILL.md:13-14` — "Keep status-code behavior consistent across similar endpoints."
- Evidence M1-S001506: `output/template/.claude/skills/http-api/SKILL.md:79-81` — "Choose consistently whether a repeated `DELETE` of an absent resource returns ⏎ `204` (the desired final state holds) or `404` (the addressed resource does not ⏎ exist); do not mix conventions between equivalent resources."

### EXTRA-M1-0179
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: When practical return an operation identifier or Location to observe 202 progress.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: When practical.
- Why EXTRA: Not in the oracle.
- Evidence M1-S001501: `output/template/.claude/skills/http-api/SKILL.md:57-60` — "Processing was accepted but is not complete when the response is sent — a ⏎ long-running operation, background job, asynchronous import, or queued ⏎ processing. When practical, return an operation identifier or a `Location` ⏎ where the client can observe progress:"

### EXTRA-M1-0180
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: 304 only for conditional requests with a still-valid cached representation; never a generic business response.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Less-common status semantics (EXC-009).
- Evidence M1-S001509: `output/template/.claude/skills/http-api/SKILL.md:87-89` — "Only for a conditional request (`If-None-Match`/ETag, `If-Modified-Since`) ⏎ when the client's cached representation is still valid. It carries no normal ⏎ representation and is not a generic "nothing changed" business response."

### EXTRA-M1-0181
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: 406 when no acceptable response representation can be produced; 415 for unsupported request media type; do not confuse them.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Content-negotiation semantics (EXC-009).
- Evidence M1-S001520: `output/template/.claude/skills/http-api/SKILL.md:122-124` — "The server cannot produce a representation acceptable under the client's ⏎ content negotiation. It concerns the response representation; do not confuse ⏎ it with `415`."
- Evidence M1-S001528: `output/template/.claude/skills/http-api/SKILL.md:149-151` — "The server does not support the request representation, for example ⏎ `Content-Type: application/xml` on a JSON-only endpoint. `415` concerns the ⏎ request body format; `406` concerns acceptable response formats."

### EXTRA-M1-0182
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: 422 for structurally valid but semantically invalid requests; follow an established 400-for-both convention; new APIs distinguishing them use 400 for contract errors and 422 for semantics.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: Established convention.
- Why EXTRA: 400/422 distinction not in the oracle.
- Evidence M1-S001530: `output/template/.claude/skills/http-api/SKILL.md:155-160` — "The request is syntactically and structurally valid but its semantic or ⏎ business content is invalid — impossible business values, a business-rule ⏎ rejection that is not a state conflict, or a semantically invalid combination ⏎ such as `startDate > endDate`. Some APIs deliberately use `400` for both ⏎ transport and semantic validation; follow an established project convention. ⏎ For new APIs tha …"

### EXTRA-M1-0183
- Closest oracle policies: API-006
- Modality: MUST
- Normative action: 428 when a contract-required precondition is absent; for other preconditions only when the contract defines them.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Not in API-006.
- Evidence M1-S001533: `output/template/.claude/skills/http-api/SKILL.md:169-170` — "The API contract requires a precondition the client did not provide, for ⏎ example a `PUT /api/orders/123` that requires `If-Match`:"
- Evidence M1-S001535: `output/template/.claude/skills/http-api/SKILL.md:177-178` — "Use `428` for other mandatory preconditions only when the contract explicitly ⏎ defines them."

### EXTRA-M1-0184
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: 429 for rate-limited requests with Retry-After when known; never represent validation failures as rate limiting.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Rate-limiting semantics not in the oracle.
- Evidence M1-S001537: `output/template/.claude/skills/http-api/SKILL.md:182-184` — "Rate limiting rejected the request. Include `Retry-After` when the server knows ⏎ when another attempt is appropriate. Do not represent validation failure as ⏎ rate limiting."

### EXTRA-M1-0185
- Closest oracle policies: API-003
- Modality: MUST_NOT
- Normative action: 502/504 only when acting as an intermediary (invalid upstream response / upstream timeout); not for every dependency failure or TaskCanceledException; distinguish own timeouts from upstream ones.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Gateway status semantics (EXC-009).
- Evidence M1-S001542: `output/template/.claude/skills/http-api/SKILL.md:196-197` — "This API acts as an intermediary and receives an invalid or unusable upstream ⏎ response. Do not convert every dependency failure into `502`."
- Evidence M1-S001546: `output/template/.claude/skills/http-api/SKILL.md:208-212` — "This API acts as an intermediary and an upstream service did not respond in ⏎ time. Not for every internal `TaskCanceledException`: distinguish a client that ⏎ cancelled the incoming request, an operation of our own that timed out, and an ⏎ upstream timeout; the external response depends on which occurred and the role ⏎ this API plays."

### EXTRA-M1-0186
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: 503 for temporary inability (maintenance, critical dependency unavailable, chosen overload semantics) with Retry-After when meaningful.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence M1-S001544: `output/template/.claude/skills/http-api/SKILL.md:201-204` — "The service is temporarily unable to handle the request — maintenance, a ⏎ critical dependency unavailable for this operation, or overload when the service ⏎ chooses `503` semantics. Include `Retry-After` when a meaningful retry time is ⏎ known."

### EXTRA-M1-0187
- Closest oracle policies: ARC-025, API-011
- Modality: MUST_NOT
- Normative action: Use DelegatingHandler only for genuine HTTP pipeline concerns, never for business decisions.
- Trigger/scope: on-demand knowledge skill httpclient-factory (outbound HTTP)
- Exceptions: none
- Why EXTRA: Handler responsibility rule not in the oracle.
- Evidence M1-S001618: `output/template/.claude/skills/httpclient-factory/SKILL.md:75-77` — "Use a `DelegatingHandler` for genuine HTTP pipeline concerns — authorization ⏎ header acquisition, correlation/context propagation, specialized request ⏎ signing — and never for business decisions."

### EXTRA-M1-0188
- Closest oracle policies: ARC-025, API-003
- Modality: MUST_NOT
- Normative action: Do not blindly call EnsureSuccessStatusCode when remote statuses carry meaning; do not expose every upstream status through your API or map every upstream failure to the same status.
- Trigger/scope: on-demand knowledge skill httpclient-factory (outbound HTTP)
- Exceptions: none
- Why EXTRA: Response-mapping rules beyond ARC-025.
- Evidence M1-S001626: `output/template/.claude/skills/httpclient-factory/SKILL.md:117-119` — "Translate remote responses into the abstraction Application consumes. Do not ⏎ blindly call `EnsureSuccessStatusCode()` when specific remote statuses carry ⏎ contract meaning:"
- Evidence M1-S001628: `output/template/.claude/skills/httpclient-factory/SKILL.md:130-132` — "For richer failure semantics, translate responses into explicit Infrastructure ⏎ or Application outcomes, and do not expose every upstream status code through ⏎ your own API."
- Evidence M1-S001642: `output/template/.claude/skills/httpclient-factory/SKILL.md:181-187` — "Check-by-reference against `performance.md` § Outbound Calls and ⏎ `architecture.md` § Layer Placement: a new `HttpClient` per request; typed, ⏎ keyed, or named clients made mandatory universally; retries on unsafe ⏎ operations without idempotency analysis; infinite or poorly bounded retries; ⏎ `HttpResponseMessage` leaking across boundaries; ignored cancellation; dynamic ⏎ tokens in shared `Defau …"

### EXTRA-M1-0189
- Closest oracle policies: none
- Modality: MUST_NOT
- Normative action: Apply per-request values (dynamic tokens) to the request or via a handler; do not mutate shared default headers concurrently.
- Trigger/scope: on-demand knowledge skill httpclient-factory (outbound HTTP)
- Exceptions: none
- Why EXTRA: Header-safety rule not in the oracle.
- Evidence M1-S001634: `output/template/.claude/skills/httpclient-factory/SKILL.md:153-155` — "Stable headers such as media types may be configured on the client. Apply ⏎ per-request values such as dynamic access tokens to the specific request or ⏎ through a handler; do not mutate shared default headers concurrently."
- Evidence M1-S001642: `output/template/.claude/skills/httpclient-factory/SKILL.md:181-187` — "Check-by-reference against `performance.md` § Outbound Calls and ⏎ `architecture.md` § Layer Placement: a new `HttpClient` per request; typed, ⏎ keyed, or named clients made mandatory universally; retries on unsafe ⏎ operations without idempotency analysis; infinite or poorly bounded retries; ⏎ `HttpResponseMessage` leaking across boundaries; ignored cancellation; dynamic ⏎ tokens in shared `Defau …"

### EXTRA-M1-0190
- Closest oracle policies: none
- Modality: PREFER
- Normative action: Prefer System.Net.Http.Json/System.Text.Json with explicit options when external contracts differ.
- Trigger/scope: on-demand knowledge skill httpclient-factory (outbound HTTP)
- Exceptions: none
- Why EXTRA: Serializer preference not in the oracle.
- Evidence M1-S001636: `output/template/.claude/skills/httpclient-factory/SKILL.md:159-162` — "Prefer `System.Net.Http.Json` / `System.Text.Json` where sufficient, with ⏎ explicit serialization options when the external contract differs from the ⏎ application's defaults. Do not reuse internal Domain entities as remote API ⏎ contracts to avoid mapping."

### EXTRA-M1-0191
- Closest oracle policies: RUN-013
- Modality: DEFAULT
- Normative action: Log what helps diagnose/operate; choose levels by operational meaning (Trace/Debug troubleshooting; Information meaningful events, not every method call; Warning recovered degraded conditions; Error failed operations needing investigation; Critical subsystem cannot continue).
- Trigger/scope: on-demand knowledge skill logging (backend)
- Exceptions: none
- Why EXTRA: Log-level taxonomy not in the oracle.
- Evidence M1-S001687: `output/template/.claude/skills/logging/SKILL.md:13-14` — "choose log"
- Evidence M1-S001693: `output/template/.claude/skills/logging/SKILL.md:34-44` — "- **Trace / Debug** — detailed diagnostics for troubleshooting (sensitive-data ⏎   rules apply at every level: `security.md`). ⏎ - **Information** — normal meaningful events: a background job completed, an ⏎   important business operation completed, a runtime lifecycle event. Avoid ⏎   logging every internal method call. ⏎ - **Warning** — an unexpected or degraded condition the application recover …"

### EXTRA-M1-0192
- Closest oracle policies: RUN-013
- Modality: DEFAULT
- Normative action: Use ILogger.BeginScope when several entries share contextual data.
- Trigger/scope: on-demand knowledge skill logging (backend)
- Exceptions: none
- Why EXTRA: Scope technique (EXC-013).
- Evidence M1-S001697: `output/template/.claude/skills/logging/SKILL.md:54-54` — "Use `ILogger.BeginScope` when several entries share contextual data:"

### EXTRA-M1-0193
- Closest oracle policies: RUN-013
- Modality: DEFAULT
- Normative action: Prefer platform trace identifiers; explicit correlation id only when required; propagate tracing context via the chosen infrastructure.
- Trigger/scope: on-demand knowledge skill logging (backend)
- Exceptions: none
- Why EXTRA: Correlation technique (EXC-013).
- Evidence M1-S001701: `output/template/.claude/skills/logging/SKILL.md:72-77` — "Prefer platform/runtime trace identifiers when they already provide adequate ⏎ request correlation. Add an explicit correlation identifier only when an ⏎ integration or operational requirement needs one; validate or normalize an ⏎ identifier accepted from an external client before propagating it. Propagate ⏎ correlation/tracing context across outbound calls with the project's chosen ⏎ tracing or H …"

### EXTRA-M1-0194
- Closest oracle policies: none
- Modality: AVOID
- Normative action: Do not use logs as an audit database without a dedicated audit design.
- Trigger/scope: on-demand knowledge skill logging (backend)
- Exceptions: Adopted audit design.
- Why EXTRA: Not in the oracle.
- Evidence M1-S001707: `output/template/.claude/skills/logging/SKILL.md:95-99` — "Check-by-reference against the policy owners above: string interpolation in ⏎ structured logs; duplicate exception logging; expected business outcomes logged ⏎ as errors; credentials or secrets logged; full objects dumped without review; ⏎ provider-specific APIs spread through Application code; logs used as an audit ⏎ database without a dedicated audit design."

### EXTRA-M1-0195
- Closest oracle policies: DEP-021
- Modality: DEFAULT
- Normative action: Use two-stage bootstrap initialization when startup logging matters; simpler apps may use host-managed setup.
- Trigger/scope: private reference of on-demand skill logging (Serilog)
- Exceptions: Simpler applications.
- Why EXTRA: Bootstrap technique not in the oracle.
- Evidence M1-S001646: `output/template/.claude/skills/logging/references/serilog.md:7-10` — "- Use two-stage initialization when startup logging matters: a bootstrap logger ⏎   captures failures before the full DI/configuration pipeline exists. Simpler ⏎   applications may use normal host-managed Serilog setup without bootstrap ⏎   logging."

### EXTRA-M1-0196
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Flush the static/bootstrap Log.Logger on shutdown; for host-managed logging follow the provider lifetime instead.
- Trigger/scope: private reference of on-demand skill logging (Serilog)
- Exceptions: none
- Why EXTRA: Serilog lifecycle technique.
- Evidence M1-S001674: `output/template/.claude/skills/logging/references/serilog.md:229-231` — "When the application uses the static/bootstrap `Log.Logger`, flush it on ⏎ shutdown so buffered events from asynchronous sinks (Seq, OTLP, Elasticsearch) ⏎ are written:"
- Evidence M1-S001676: `output/template/.claude/skills/logging/references/serilog.md:239-240` — "For purely host-managed logging, follow the configured provider's lifetime ⏎ behavior instead of adding static lifecycle code."

### EXTRA-M1-0197
- Closest oracle policies: DEP-004
- Modality: DEFAULT
- Normative action: Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks for Elasticsearch.
- Trigger/scope: private reference of on-demand skill logging (Serilog)
- Exceptions: Only when Elasticsearch is used.
- Why EXTRA: Package guidance not in the oracle.
- Evidence M1-S001680: `output/template/.claude/skills/logging/references/serilog.md:256-258` — "The `Serilog.Sinks.Elasticsearch` package is deprecated; use the official ⏎ `Elastic.Serilog.Sinks` package, which writes ECS-formatted documents to data ⏎ streams:"

### EXTRA-M1-0198
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: Prefer a normal constructor when initialization, validation, field naming or debugging is clearer that way.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Constructor technique (EXC-002).
- Evidence M1-S001717: `output/template/.claude/skills/modern-csharp/SKILL.md:28-29` — "Prefer a normal constructor when initialization, validation, field naming, or ⏎ debugging is clearer that way."

### EXTRA-M1-0199
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Collection expressions when the target type is clear; required when initialization is part of the construction contract (not a substitute for validation); avoid deeply nested patterns; field keyword for trivial backing fields.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Language-feature technique (EXC-002).
- Evidence M1-S001719: `output/template/.claude/skills/modern-csharp/SKILL.md:33-33` — "Use them when the target type is clear:"
- Evidence M1-S001725: `output/template/.claude/skills/modern-csharp/SKILL.md:51-52` — "Use `required` when initializing a property is part of the type's valid ⏎ construction contract:"
- Evidence M1-S001727: `output/template/.claude/skills/modern-csharp/SKILL.md:58-59` — "Do not use `required` as a substitute for constructor or domain validation where ⏎ invariants must be protected."
- Evidence M1-S001731: `output/template/.claude/skills/modern-csharp/SKILL.md:74-75` — "Avoid deeply nested patterns that are harder to read than straightforward ⏎ conditions."
- Evidence M1-S001735: `output/template/.claude/skills/modern-csharp/SKILL.md:92-93` — "Use it to remove an otherwise trivial backing field; do not rewrite manual ⏎ backing fields with clear or substantial logic solely to use it."

### EXTRA-M1-0200
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Records for immutable DTOs, Value Objects and messages; identity/lifecycle entities remain classes; do not convert every class to a record.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Record guidance (EXC-002).
- Evidence M1-S001723: `output/template/.claude/skills/modern-csharp/SKILL.md:45-47` — "Good candidates: immutable transport DTOs, genuine Value Objects, immutable ⏎ messages. Entities with identity and lifecycle remain classes unless the model ⏎ genuinely benefits from record semantics."
- Evidence M1-S001753: `output/template/.claude/skills/modern-csharp/SKILL.md:155-157` — "Newest syntax for its own sake; converting every class to a record; ⏎ `record struct` merely to avoid allocations; `Span<T>` without a performance ⏎ reason; deeply nested patterns; mass constructor conversion."

### EXTRA-M1-0201
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: Prefer immutability when natural; do not force it where controlled mutation is simpler.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Immutability guidance (EXC-002).
- Evidence M1-S001745: `output/template/.claude/skills/modern-csharp/SKILL.md:131-132` — "Prefer immutability when it represents the model naturally; do not force it onto ⏎ framework models or workflows where controlled mutation is simpler."

### EXTRA-M1-0202
- Closest oracle policies: RUN-009
- Modality: MUST
- Normative action: Confirm the configured language version supports a feature before using it.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence M1-S001749: `output/template/.claude/skills/modern-csharp/SKILL.md:143-145` — "Confirm that the project's configured language version supports a feature ⏎ before using it. Changing `LangVersion` or the target framework is a stack ⏎ decision, not a modernization step."

### EXTRA-M1-0203
- Closest oracle policies: ARC-019
- Modality: DEFAULT
- Normative action: Change IEntityTypeConfiguration<T> mappings in the adapter layer.
- Trigger/scope: workflow persistence-change (persistence model, mapping, migration, seed-data, schema-affecting settings)
- Exceptions: none
- Why EXTRA: EF mapping technique not in the oracle.
- Evidence M1-S001761: `output/template/.claude/skills/persistence-change/SKILL.md:25-26` — "Change the `IEntityTypeConfiguration<T>` mappings in the adapter layer; keep ⏎ persistence-specific configuration out of the core model where practical."

### EXTRA-M1-0204
- Closest oracle policies: ARC-019
- Modality: DEFAULT
- Normative action: Create migrations from the adapter-layer project with the composition-root project as startup project.
- Trigger/scope: workflow persistence-change (persistence model, mapping, migration, seed-data, schema-affecting settings)
- Exceptions: none
- Why EXTRA: Migration command technique.
- Evidence M1-S001763: `output/template/.claude/skills/persistence-change/SKILL.md:30-31` — "Create migrations from the adapter-layer project with the composition-root ⏎ project as startup project:"

### EXTRA-M1-0205
- Closest oracle policies: PST-005, WF-006
- Modality: MUST
- Normative action: Confirm the migration applies to a freshly created Development database before seeding.
- Trigger/scope: workflow persistence-change (persistence model, mapping, migration, seed-data, schema-affecting settings)
- Exceptions: none
- Why EXTRA: Specific verification step not in the oracle.
- Evidence M1-S001772: `output/template/.claude/skills/persistence-change/SKILL.md:72-75` — "Build the affected projects, run the persistence and integration tests, and ⏎ confirm the migration applies to a freshly created Development database before ⏎ seeding. Production migration remains explicit deployment work (`verify` ⏎ § Delivery Changes)."

### EXTRA-M1-0206
- Closest oracle policies: ARC-027, DEP-024
- Modality: DEFAULT
- Normative action: Scaffold backend folders by role: Application Abstractions/Persistence, Abstractions/ExternalServices, Services, DTOs, Validation, DependencyInjection.cs; Infrastructure Persistence/{Configurations,Repositories,Migrations,Seeding}, Services, DependencyInjection.cs.
- Trigger/scope: private reference of workflow project-structure (backend placement)
- Exceptions: Only when needed.
- Why EXTRA: Directory layout convention (EXC-004).
- Evidence M1-S001781: `output/template/.claude/skills/project-structure/references/backend-layout.md:36-38` — "- `Abstractions/Persistence` — inward-facing persistence contracts such as ⏎   `ITaskRepository.cs`, `IOrderRepository.cs`, `IUnitOfWork.cs`; no ⏎   persistence-technology types."
- Evidence M1-S001782: `output/template/.claude/skills/project-structure/references/backend-layout.md:39-42` — "- `Abstractions/ExternalServices` — Application-owned abstractions implemented ⏎   by outer layers when needed, such as `IEmailSender.cs`, `ICurrentUser.cs`, ⏎   `IFileStorage.cs`, `IPaymentGateway.cs`; do not create it before such ⏎   dependencies exist."
- Evidence M1-S001783: `output/template/.claude/skills/project-structure/references/backend-layout.md:43-44` — "- `Services` — Application Services and useful public service contracts ⏎   (`ITaskService.cs`, `TaskService.cs`); no handler/CQRS/mediator structures."
- Evidence M1-S001784: `output/template/.claude/skills/project-structure/references/backend-layout.md:45-46` — "- `DTOs` — Application-level operation and data models when useful; not a ⏎   dumping ground."
- Evidence M1-S001785: `output/template/.claude/skills/project-structure/references/backend-layout.md:47-48` — "- `Validation` — FluentValidation validators for Application-level input and ⏎   use-case validation when required."
- Evidence M1-S001786: `output/template/.claude/skills/project-structure/references/backend-layout.md:49-51` — "- `DependencyInjection.cs` — registers Application-owned services and ⏎   Application-level validation infrastructure; never concrete Infrastructure ⏎   implementations."
- Evidence M1-S001792: `output/template/.claude/skills/project-structure/references/backend-layout.md:83-87` — "- `Persistence/` — the persistence implementation: session, Unit of Work, ⏎   entity configurations, concrete repositories (an Infrastructure-only generic ⏎   base is allowed when it removes real duplication), migrations, and ⏎   Development seeding. Technology-specific contents: the persistence knowledge ⏎   skill."
- Evidence M1-S001793: `output/template/.claude/skills/project-structure/references/backend-layout.md:88-90` — "- `Services/` — technical and external implementations of Application ⏎   abstractions (`EmailSender.cs`, `FileStorage.cs`, `PaymentGateway.cs`); add ⏎   capability-specific subdirectories when they improve cohesion."
- Evidence M1-S001794: `output/template/.claude/skills/project-structure/references/backend-layout.md:91-94` — "- `DependencyInjection.cs` — registers Infrastructure-owned implementations and ⏎   technical dependencies: the persistence session and provider, repository ⏎   implementations, `IUnitOfWork`, external adapters, `HttpClient` ⏎   integrations, resilience handlers when used."

### EXTRA-M1-0207
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Make supporting-type roles clear via established suffixes (Service, Dto, Request/Response, Result/Outcome, Validator, Rules/Policy, Factory, Mapper, Adapter); avoid ambiguous names; subdirectories only when a flat directory gets hard to navigate.
- Trigger/scope: private reference of workflow project-structure (backend placement)
- Exceptions: none
- Why EXTRA: Naming heuristics (EXC-004).
- Evidence M1-S001788: `output/template/.claude/skills/project-structure/references/backend-layout.md:55-60` — "Within a feature or service area, make each supporting type's responsibility ⏎ clear from its name, its immediate directory, or both. Prefer established ⏎ suffixes: `Service` (use-case orchestration), `Dto` (data transfer), ⏎ `Request`/`Response` (Application operation contracts; HTTP transport contracts ⏎ belong to Api), `Result`/`Outcome` (operation results), `Validator`, ⏎ `Rules`/`Policy` (dec …"
- Evidence M1-S001789: `output/template/.claude/skills/project-structure/references/backend-layout.md:62-67` — "Avoid ambiguous names such as `TaskWorkflow` when the role cannot be inferred ⏎ without opening the file; prefer `TaskWorkflowRules`, `TaskWorkflowPolicy`, or ⏎ `TaskWorkflowService` according to the actual responsibility. Add ⏎ responsibility-specific subdirectories only when a flat directory becomes hard ⏎ to navigate, and avoid generic `Models`, `Helpers`, `Common`, or `Utils` ⏎ buckets when a  …"

### EXTRA-M1-0208
- Closest oracle policies: ARC-012
- Modality: MUST_NOT
- Normative action: Extensions hold cohesive API/composition methods; do not move arbitrary code out of Program.cs solely to shorten it.
- Trigger/scope: private reference of workflow project-structure (backend placement)
- Exceptions: none
- Why EXTRA: Program.cs organisation rule not in the oracle.
- Evidence M1-S001801: `output/template/.claude/skills/project-structure/references/backend-layout.md:119-120` — "- `Extensions` — cohesive API/composition extension methods; do not move ⏎   arbitrary code out of `Program.cs` solely to shorten it."

### EXTRA-M1-0209
- Closest oracle policies: DEP-024
- Modality: DEFAULT
- Normative action: Frontend unit/component tests inside the workspace, typically colocated; E2E tests, when introduced, e.g. under frontend/ProjectName.Web/e2e/.
- Trigger/scope: private reference of workflow project-structure (repository layout)
- Exceptions: none
- Why EXTRA: Frontend test placement convention not in the oracle.
- Evidence M1-S001825: `output/template/.claude/skills/project-structure/references/solution-layout.md:48-51` — "- Frontend unit and component tests: inside the frontend workspace, typically ⏎   colocated with the code they test according to current framework conventions. ⏎ - Frontend E2E tests, when introduced: inside the frontend workspace, for ⏎   example `frontend/ProjectName.Web/e2e/`."
- Evidence M1-S001862: `output/template/.claude/skills/project-structure/SKILL.md:73-76` — "Create only useful backend test projects, at the locations and with the ⏎ references given in `references/backend-layout.md`, using the backend-testing ⏎ skill § Test Project Setup. Frontend unit/component tests and E2E tests stay ⏎ inside the frontend workspace."

### EXTRA-M1-0210
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: Keep deterministic formatting/code-style in .editorconfig; prefer enforceable tooling over restating mechanical formatting rules in instructions.
- Trigger/scope: private reference of workflow project-structure (repository layout)
- Exceptions: none
- Why EXTRA: Instruction-design preference (repo/meta).
- Evidence M1-S001834: `output/template/.claude/skills/project-structure/references/solution-layout.md:76-78` — "Keep deterministic repository-wide formatting and code-style configuration in ⏎ `.editorconfig`; prefer enforceable tooling configuration over restating ⏎ mechanical formatting rules in instructions."

### EXTRA-M1-0211
- Closest oracle policies: SEC-001
- Modality: DEFAULT
- Normative action: Ignore generated/local artifacts (bin, obj, .vs, node_modules, dist, TestResults, coverage, local secret/config overrides).
- Trigger/scope: private reference of workflow project-structure (repository layout)
- Exceptions: Where applicable.
- Why EXTRA: Ignore-file convention not in the oracle.
- Evidence M1-S001836: `output/template/.claude/skills/project-structure/references/solution-layout.md:82-85` — "Ignore generated and local artifacts where applicable: `bin/`, `obj/`, `.vs/`, ⏎ `node_modules/`, `dist/`, `TestResults/`, `coverage/`, and local secret or ⏎ config overrides. Do not ignore files that are intentionally part of the ⏎ Development configuration contract."

### EXTRA-M1-0212
- Closest oracle policies: SEC-003
- Modality: PREFER
- Normative action: Prefer APIs that separate executable and arguments; validate or constrain external input when command execution is genuinely needed.
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: Command execution genuinely needed.
- Why EXTRA: Command-injection prevention is not stated in the oracle.
- Evidence M1-S001917: `output/template/.claude/skills/security-scan/references/scan-layers.md:86-89` — "Inspect `Process.Start`, shell execution, PowerShell/bash invocation, and ⏎ command arguments built from user input. Prefer APIs that separate executable ⏎ and arguments; validate or constrain external input when command execution is ⏎ genuinely needed."

### EXTRA-M1-0213
- Closest oracle policies: SEC-003, SEC-015
- Modality: MUST
- Normative action: Normalize user-controlled paths and verify they remain within the intended storage boundary (traversal, absolute-path injection, unsafe archive extraction).
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Path-traversal invariant not in the oracle.
- Evidence M1-S001919: `output/template/.claude/skills/security-scan/references/scan-layers.md:93-96` — "Review user-controlled file names, paths, archive extraction, download paths, ⏎ and upload destinations for `../`, absolute-path injection, escape from the ⏎ intended root, and unsafe archive extraction. Normalize and verify that paths ⏎ remain within the intended storage boundary."

### EXTRA-M1-0214
- Closest oracle policies: SEC-003
- Modality: MUST_NOT
- Normative action: Do not deserialize untrusted payloads into arbitrary runtime types (BinaryFormatter, unsafe TypeNameHandling).
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Deserialization invariant not in the oracle.
- Evidence M1-S001925: `output/template/.claude/skills/security-scan/references/scan-layers.md:116-118` — "Investigate dangerous polymorphic or type-driven deserialization, such as ⏎ `BinaryFormatter` or unsafe Newtonsoft `TypeNameHandling` configurations. Do ⏎ not deserialize untrusted payloads into arbitrary runtime types."

### EXTRA-M1-0215
- Closest oracle policies: WF-020
- Modality: DEFAULT
- Normative action: Consider rate limiting where abuse could realistically matter (login, password reset, expensive anonymous or resource-intensive operations); do not require it on every endpoint.
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Rate-limiting security expectation not in the oracle.
- Evidence M1-S001953: `output/template/.claude/skills/security-scan/references/scan-layers.md:211-214` — "Consider rate limiting where abuse could realistically matter — login and ⏎ password reset, expensive anonymous endpoints, resource-intensive operations. ⏎ Do not require it on every endpoint; `429` semantics are in the `http-api` ⏎ skill."

### EXTRA-M1-0216
- Closest oracle policies: API-008
- Modality: PREFER
- Normative action: Prefer explicit response contracts where needed instead of returning entities with hashes, internal security fields, unnecessary personal data or secret metadata.
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: Where needed.
- Why EXTRA: Response-data minimization is not stated in the oracle.
- Evidence M1-S001961: `output/template/.claude/skills/security-scan/references/scan-layers.md:235-238` — "Look for database/domain entities returned directly, password hashes, internal ⏎ security fields, unnecessary personal information, and secret metadata. Prefer ⏎ explicit response contracts where needed; inspect the actual serialized fields ⏎ rather than assuming a returned entity is vulnerable."

### EXTRA-M1-0217
- Closest oracle policies: WF-020, WF-012
- Modality: MUST
- Normative action: Identify security-sensitive workflows (tenant isolation, workflow abuse, privilege escalation, idempotency abuse, multi-step authorization) as threat-modeling/manual-review candidates rather than claiming a static scan proves them secure.
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Design-review output obligation not in the oracle.
- Evidence M1-S001979: `output/template/.claude/skills/security-scan/references/scan-layers.md:292-296` — "Static checks do not fully cover insecure design, tenant isolation, business ⏎ workflow abuse, privilege escalation through legitimate operations, ⏎ financial/idempotency abuse, or multi-step authorization problems. Identify ⏎ meaningful security-sensitive workflows as candidates for threat modeling or ⏎ dedicated manual review rather than claiming the static scan proves them secure."

### EXTRA-M1-0218
- Closest oracle policies: WF-020
- Modality: DEFAULT
- Normative action: Report each finding as [SEVERITY] path:line — title with OWASP category, Evidence, Impact and Remediation.
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Report template not in the oracle.
- Evidence M1-S001984: `output/template/.claude/skills/security-scan/references/scan-layers.md:312-327` — "```markdown ⏎ ### [HIGH] src/.../File.cs:42 — Resource authorization missing ⏎  ⏎ OWASP: A01:2025 Broken Access Control ⏎  ⏎ Evidence: ⏎ The endpoint loads an order solely by route ID and does not constrain it to the ⏎ authenticated customer. ⏎  ⏎ Impact: ⏎ An authenticated user who learns another order ID may access that customer's ⏎ order. ⏎  ⏎ Remediation: ⏎ Apply resource/ownership authorizati …"

### EXTRA-M1-0219
- Closest oracle policies: WF-020, WF-009
- Modality: MUST
- Normative action: State in the report that a static review cannot prove the application secure and may miss runtime, infrastructure, business-logic and dynamic-exploitation issues.
- Trigger/scope: workflow security-scan (security scan, audit or targeted security review)
- Exceptions: none
- Why EXTRA: Limitation statement not in the oracle.
- Evidence M1-S001991: `output/template/.claude/skills/security-scan/SKILL.md:15-20` — "Perform an evidence-based static security review of the repository. This is ⏎ not a penetration test: static review cannot prove the application is secure ⏎ and may miss runtime-only vulnerabilities, infrastructure outside the ⏎ repository, complex business-logic abuse, sophisticated authorization bypasses, ⏎ deployment-specific weaknesses, and vulnerabilities that require dynamic ⏎ exploitation.  …"
- Evidence M1-S002030: `output/template/.claude/skills/security-scan/SKILL.md:209-211` — "A security scan is complete when all applicable layers were inspected, findings ⏎ have evidence, uncertain findings are labeled, severity reflects actual risk, ⏎ limitations are stated, and no layer is marked PASS without being checked."

### EXTRA-M1-0220
- Closest oracle policies: WF-020
- Modality: DEFAULT
- Normative action: Use OWASP Top 10:2025 as an awareness taxonomy when it genuinely fits; not every issue needs a category; do not force an inaccurate mapping.
- Trigger/scope: workflow security-scan (security scan, audit or targeted security review)
- Exceptions: none
- Why EXTRA: Taxonomy usage rule not in the oracle.
- Evidence M1-S002003: `output/template/.claude/skills/security-scan/SKILL.md:42-42` — "Use OWASP Top 10:2025 as an awareness taxonomy when it genuinely fits:"
- Evidence M1-S002005: `output/template/.claude/skills/security-scan/SKILL.md:57-57` — "Not every issue needs a category; do not force an inaccurate mapping."

### EXTRA-M1-0221
- Closest oracle policies: WF-020
- Modality: DEFINITION
- Normative action: Severity scale: Critical (sparingly, immediately exploitable high impact), High, Medium, Low, Info (hardening observation, not a demonstrated vulnerability).
- Trigger/scope: workflow security-scan (security scan, audit or targeted security review)
- Exceptions: none
- Why EXTRA: Five-level scale definition not in the oracle.
- Evidence M1-S002018: `output/template/.claude/skills/security-scan/SKILL.md:112-122` — "- **Critical** — use sparingly for immediately exploitable, high-impact ⏎   conditions: exposed real production credentials, reachable authentication ⏎   bypass, straightforward remote code execution, exploitable injection with ⏎   major impact. ⏎ - **High** — a serious vulnerability that is realistically exploitable or can ⏎   substantially compromise data, authorization, or system behavior. ⏎ -  …"

### EXTRA-M1-0222
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: Every confirmed finding includes severity, file/location, title, evidence, why it is a risk, likely impact, smallest reasonable remediation and the OWASP category when applicable.
- Trigger/scope: workflow security-scan (security scan, audit or targeted security review)
- Exceptions: none
- Why EXTRA: Mandatory finding fields not in the oracle.
- Evidence M1-S002024: `output/template/.claude/skills/security-scan/SKILL.md:143-146` — "Every confirmed finding includes severity, file and location, title, evidence, ⏎ why it is a security risk, likely impact, the smallest reasonable remediation, ⏎ and the OWASP category when applicable. Label uncertain findings ⏎ `NEEDS VERIFICATION` rather than presenting them as confirmed."

### EXTRA-M1-0223
- Closest oracle policies: WF-020, WF-009
- Modality: DEFAULT
- Normative action: Security report shape: Scope, Limitations, severity Summary counts, Findings, Layer Results table.
- Trigger/scope: workflow security-scan (security scan, audit or targeted security review)
- Exceptions: none
- Why EXTRA: Report template not in the oracle.
- Evidence M1-S002025: `output/template/.claude/skills/security-scan/SKILL.md:148-194` — "```markdown ⏎ # Security Scan Report ⏎  ⏎ Scope: ⏎ - ... ⏎  ⏎ Limitations: ⏎ Static analysis only. This does not replace penetration testing, ⏎ dynamic testing, threat modeling, or infrastructure review. ⏎  ⏎ ## Summary ⏎  ⏎ | Severity | Count | ⏎ |---|---:| ⏎ | Critical | 0 | ⏎ | High | 0 | ⏎ | Medium | 0 | ⏎ | Low | 0 | ⏎ | Info | 0 | ⏎  ⏎ ## Findings ⏎  ⏎ ### [HIGH] File:Line — Finding title ⏎  …"

### EXTRA-M1-0224
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Layer results use PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED.
- Trigger/scope: workflow security-scan (security scan, audit or targeted security review)
- Exceptions: none
- Why EXTRA: Status vocabulary differs from WF-009's PASS/NOT RUN/NOT APPLICABLE.
- Evidence M1-S002026: `output/template/.claude/skills/security-scan/SKILL.md:196-197` — "Use `PASS`, `FINDINGS`, `NOT APPLICABLE`, or `NOT CHECKED`; never mark an ⏎ uninspected layer as passed."

### EXTRA-M1-0225
- Closest oracle policies: ARC-012
- Modality: DEFAULT
- Normative action: Keep Swagger configuration in the API/composition layer.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Placement rule not in the oracle.
- Evidence M1-S002037: `output/template/.claude/skills/swagger/SKILL.md:35-36` — "Keep Swagger configuration in the API/composition layer. Select the package ⏎ version through `add-dependency`."

### EXTRA-M1-0226
- Closest oracle policies: DEP-012
- Modality: DEFAULT
- Normative action: For a new local Development API configure the launch profile to open Swagger directly when that helps.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: When that helps.
- Why EXTRA: Launch configuration not in the oracle.
- Evidence M1-S002039: `output/template/.claude/skills/swagger/SKILL.md:40-41` — "For a new local Development API, configure the launch profile so the browser ⏎ opens Swagger directly when that helps:"

### EXTRA-M1-0227
- Closest oracle policies: WF-006
- Modality: MUST
- Normative action: Application URLs agree with the launch profile; do not point a browser launch URL at HTTPS on an HTTP-only port.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Launch consistency rule not in the oracle.
- Evidence M1-S002041: `output/template/.claude/skills/swagger/SKILL.md:50-51` — "The application URLs must agree with the launch profile; do not point a ⏎ browser launch URL at HTTPS on an HTTP-only port."

### EXTRA-M1-0228
- Closest oracle policies: DEP-012
- Modality: DEFAULT
- Normative action: For Bearer authentication expose a Bearer scheme so authenticated endpoints can be exercised through Swagger UI.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: Bearer authentication used.
- Why EXTRA: Not in the oracle.
- Evidence M1-S002050: `output/template/.claude/skills/swagger/SKILL.md:86-90` — "When the API actually uses authentication, configure the matching security ⏎ definition and requirements; for Bearer authentication expose a Bearer scheme so ⏎ authenticated endpoints can be exercised through Swagger UI. Do not add a scheme ⏎ merely because an authentication package is installed, and do not apply ⏎ authentication requirements globally to anonymous endpoints."

### EXTRA-M1-0229
- Closest oracle policies: API-016
- Modality: DEFAULT
- Normative action: Document consumer-relevant preconditions, idempotency, pagination/filtering and outcomes rather than repeating action/property names.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Documentation-content guidance not in the oracle.
- Evidence M1-S002052: `output/template/.claude/skills/swagger/SKILL.md:94-96` — "Document what helps a consumer understand the contract — important ⏎ preconditions, idempotency semantics, pagination/filtering behavior, meaningful ⏎ outcomes — rather than repeating action or property names."

### EXTRA-M1-0230
- Closest oracle policies: API-016
- Modality: MUST_NOT
- Normative action: Do not add XML comments to every internal type solely for Swagger generation.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence M1-S002054: `output/template/.claude/skills/swagger/SKILL.md:100-101` — "XML comments may help public API contracts when the project chooses them; do ⏎ not add them to every internal type solely for Swagger generation."

### EXTRA-M1-0231
- Closest oracle policies: API-016, API-015
- Modality: MUST_NOT
- Normative action: Use multiple Swagger documents only for a real contract separation (versions, public/internal surfaces).
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence M1-S002056: `output/template/.claude/skills/swagger/SKILL.md:105-106` — "Use multiple Swagger documents only for a real contract separation, such as API ⏎ versions or distinct public/internal surfaces (`api-versioning` skill)."

### EXTRA-M1-0232
- Closest oracle policies: API-016, API-014
- Modality: AVOID
- Normative action: Avoid unstable anonymous response shapes / anonymous objects as long-lived API contracts; use explicit request/response contracts.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Explicit-contract rule not in the oracle.
- Evidence M1-S002058: `output/template/.claude/skills/swagger/SKILL.md:110-113` — "If the contract feeds frontend or other client generation: treat breaking ⏎ schema changes seriously, keep response metadata accurate, avoid unstable ⏎ anonymous response shapes, use explicit request/response contracts, and review ⏎ generated-client changes when the contract changes."
- Evidence M1-S002062: `output/template/.claude/skills/swagger/SKILL.md:126-129` — "Check-by-reference against `api.md` § Swagger: metadata that disagrees with ⏎ runtime responses; Swagger UI exposed publicly without a reason; Swagger used as ⏎ a substitute for integration tests; anonymous objects as long-lived API ⏎ contracts; a second competing documentation stack without a concrete need."

### EXTRA-M1-0233
- Closest oracle policies: TST-002
- Modality: MUST_NOT
- Normative action: Swagger must not be used as a substitute for integration tests.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in api.md or the oracle.
- Evidence M1-S002062: `output/template/.claude/skills/swagger/SKILL.md:126-129` — "Check-by-reference against `api.md` § Swagger: metadata that disagrees with ⏎ runtime responses; Swagger UI exposed publicly without a reason; Swagger used as ⏎ a substitute for integration tests; anonymous objects as long-lived API ⏎ contracts; a second competing documentation stack without a concrete need."

### EXTRA-M1-0234
- Closest oracle policies: none
- Modality: MUST
- Normative action: Read .claude/MAP.md first when maintaining the instruction system.
- Trigger/scope: user-invoked workflow template-maintenance (changes to the instruction system, capability modules, MAP)
- Exceptions: none
- Why EXTRA: Repo/meta procedure.
- Evidence M1-S002066: `output/template/.claude/skills/template-maintenance/SKILL.md:14-15` — "Read `.claude/MAP.md` first; it lists every instruction artifact, its owner, ⏎ scope, loading, and enforcement."

### EXTRA-M1-0235
- Closest oracle policies: none
- Modality: MUST
- Normative action: Keep each policy's trigger role: planning-time policy on the always-loaded surface, path policy in a path rule covering its full scope, procedural obligations in their workflow.
- Trigger/scope: user-invoked workflow template-maintenance (changes to the instruction system, capability modules, MAP)
- Exceptions: none
- Why EXTRA: Instruction-placement invariant (repo/meta).
- Evidence M1-S002071: `output/template/.claude/skills/template-maintenance/SKILL.md:34-36` — "2. Keep each policy's trigger role: planning-time policy stays on the ⏎    always-loaded surface, path policy stays in a path rule covering its full ⏎    scope, and procedural obligations stay in their workflow."

### EXTRA-M1-0236
- Closest oracle policies: none
- Modality: MUST_NOT
- Normative action: Do not hide a must/must-not rule only inside a knowledge skill or a private reference.
- Trigger/scope: user-invoked workflow template-maintenance (changes to the instruction system, capability modules, MAP)
- Exceptions: none
- Why EXTRA: Instruction-placement invariant (repo/meta).
- Evidence M1-S002072: `output/template/.claude/skills/template-maintenance/SKILL.md:37-38` — "3. Do not hide a must/must-not rule only inside a knowledge skill or a private ⏎    reference."

### EXTRA-M1-0237
- Closest oracle policies: none
- Modality: MUST
- Normative action: Outside a capability implementation refer to slot names and facet roles, not the selected implementation's name.
- Trigger/scope: user-invoked workflow template-maintenance (changes to the instruction system, capability modules, MAP)
- Exceptions: none
- Why EXTRA: Capability-system rule (repo/meta).
- Evidence M1-S002073: `output/template/.claude/skills/template-maintenance/SKILL.md:39-40` — "4. Outside a capability implementation, refer to slot names and facet roles, ⏎    not to the selected implementation's name."

### EXTRA-M1-0238
- Closest oracle policies: none
- Modality: MUST_NOT
- Normative action: Keep the always-loaded surface (CLAUDE.md, imports, skill descriptions) compact; do not load the whole corpus to solve reliability.
- Trigger/scope: user-invoked workflow template-maintenance (changes to the instruction system, capability modules, MAP)
- Exceptions: none
- Why EXTRA: Repo/meta rule.
- Evidence M1-S002074: `output/template/.claude/skills/template-maintenance/SKILL.md:41-42` — "5. Keep the always-loaded surface (`CLAUDE.md`, its imports, skill ⏎    descriptions) compact; do not load the whole corpus to solve reliability."

### EXTRA-M1-0239
- Closest oracle policies: none
- Modality: MUST
- Normative action: Update .claude/MAP.md after changing instruction artifacts.
- Trigger/scope: user-invoked workflow template-maintenance (changes to the instruction system, capability modules, MAP)
- Exceptions: none
- Why EXTRA: Repo/meta rule.
- Evidence M1-S002075: `output/template/.claude/skills/template-maintenance/SKILL.md:43-43` — "6. Update `.claude/MAP.md`."

### EXTRA-M1-0240
- Closest oracle policies: none
- Modality: MUST
- Normative action: Run check-instructions.js after instruction-system changes and fix every error.
- Trigger/scope: user-invoked workflow template-maintenance (changes to the instruction system, capability modules, MAP)
- Exceptions: none
- Why EXTRA: Repo/meta rule.
- Evidence M1-S002076: `output/template/.claude/skills/template-maintenance/SKILL.md:44-46` — "7. Run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.js"` ⏎    (from any directory of the repository or worktree being changed) and fix ⏎    every error."

### EXTRA-M1-0241
- Closest oracle policies: ARC-020, DEP-002
- Modality: MUST
- Normative action: Capability replacement procedure: read CONTRACT.md and current MODULE.md, create a complete new manifest, rewrite every facet at its role-named location with updated Capability headers, update the selection row and remove the old directory, review binds and frame layer names, run the checker and update the map.
- Trigger/scope: user-invoked workflow template-maintenance (changes to the instruction system, capability modules, MAP)
- Exceptions: After an approved ADR.
- Why EXTRA: Repo/meta procedure.
- Evidence M1-S002079: `output/template/.claude/skills/template-maintenance/SKILL.md:53-67` — "1. Read `.claude/capabilities/<slot>/CONTRACT.md` for the required facets, ⏎    properties, and role vocabulary. ⏎ 2. Read the current `<implementation>/MODULE.md`; its manifest lists every ⏎    runtime facet and its physical location. ⏎ 3. Create `.claude/capabilities/<slot>/<new-implementation>/MODULE.md` with a ⏎    complete manifest (facets, properties, binds, leak tokens, enforcement ⏎    dat …"

### EXTRA-M1-0242
- Closest oracle policies: DEP-009, GOV-017
- Modality: MUST
- Normative action: Record an ADR for a persistence provider-variant change.
- Trigger/scope: user-invoked workflow template-maintenance (changes to the instruction system, capability modules, MAP)
- Exceptions: none
- Why EXTRA: Recording obligation not in the oracle.
- Evidence M1-S002081: `output/template/.claude/skills/template-maintenance/SKILL.md:71-73` — "Edit the provider-variant sections listed in the persistence `MODULE.md` ⏎ manifest, the provider property in `docs/capability-selection.md`, and the ⏎ declared string-comparison property; record the ADR."

### EXTRA-M1-0243
- Closest oracle policies: none
- Modality: MUST
- Normative action: Removing the optional frontend slot: set the row to disabled with implementation '—', delete listed facet files and the module directory, remove the frontend planning import, update the map, run the checker; other instructions need no edits.
- Trigger/scope: user-invoked workflow template-maintenance (changes to the instruction system, capability modules, MAP)
- Exceptions: Frontend slot removal.
- Why EXTRA: Repo/meta procedure.
- Evidence M1-S002083: `output/template/.claude/skills/template-maintenance/SKILL.md:77-84` — "Set the frontend row to status `disabled` with implementation `—`; delete the ⏎ facet files listed in the frontend `MODULE.md` manifest and its module ⏎ directory; remove the `@docs/capabilities/frontend.md` import from ⏎ `CLAUDE.md`; update the frontend entry in the map's capability view; run the ⏎ checker. Other instructions need no edits: their references to the slot's ⏎ role-named facets apply …"

### EXTRA-M1-0244
- Closest oracle policies: WF-005
- Modality: MUST_NOT
- Normative action: Do not use --no-restore unless restore is known to be complete.
- Trigger/scope: workflow verify (before declaring implementation complete or preparing a PR)
- Exceptions: Restore known complete.
- Why EXTRA: Build-command restriction not in the oracle.
- Evidence M1-S002092: `output/template/.claude/skills/verify/SKILL.md:37-40` — "Build the affected solution or projects (for example `dotnet build`, or the ⏎ frontend's configured build script such as `npm run build`). Do not use ⏎ `--no-restore` unless restore is known to be complete. A build failure means ⏎ the implementation is not complete."

### EXTRA-M1-0245
- Closest oracle policies: WF-005, TST-002
- Modality: DEFAULT
- Normative action: Small solutions run the complete suite; large ones run affected test projects first then any broader suite the risk requires; inspect package.json rather than assuming a frontend test runner.
- Trigger/scope: workflow verify (before declaring implementation complete or preparing a PR)
- Exceptions: none
- Why EXTRA: Test-run scope rule not in the oracle.
- Evidence M1-S002094: `output/template/.claude/skills/verify/SKILL.md:44-49` — "Run the tests covering the changed area (for example `dotnet test --no-build`, ⏎ and the frontend test script when `package.json` defines one — inspect ⏎ `package.json` rather than assuming a runner). For small solutions run the ⏎ complete suite; for large ones run affected test projects first, then any ⏎ broader suite the change risk requires. Investigate every newly failing ⏎ relevant test; do n …"

### EXTRA-M1-0246
- Closest oracle policies: WF-004
- Modality: MUST
- Normative action: Final diff contains no commented-out code, temporary logging, unintended TODO/FIXME markers or stale temporary tests/scripts.
- Trigger/scope: workflow verify (before declaring implementation complete or preparing a PR)
- Exceptions: none
- Why EXTRA: Diff-hygiene items not in the oracle.
- Evidence M1-S002111: `output/template/.claude/skills/verify/SKILL.md:127-132` — "Review the final diff after all fixes for: accidental unrelated edits; ⏎ commented-out code; temporary logging; unintended TODO/FIXME markers; stale ⏎ temporary tests or scripts; architecture drift; unapproved drift from ⏎ `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`; stale code, tests, docs, or ⏎ configuration after a `CUSTOM_SETTINGS.md` change; behavior verified manually ⏎ but never preserved as  …"

### EXTRA-M1-0247
- Closest oracle policies: none
- Modality: MUST
- Normative action: When instruction files changed run check-instructions.js during verification.
- Trigger/scope: workflow verify (before declaring implementation complete or preparing a PR)
- Exceptions: Instruction files changed.
- Why EXTRA: Repo/meta check.
- Evidence M1-S002113: `output/template/.claude/skills/verify/SKILL.md:140-141` — "When instruction files changed, run ⏎ `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.js"`."

### EXTRA-M1-0001
- Closest oracle policies: GOV-001, GOV-017
- Modality: MUST_NOT
- Normative action: Product and task inputs are not instruction layers: they may request an engineering decision change but never silently override engineering policy; a conflicting request becomes a Decision Request.
- Trigger/scope: always (CLAUDE.md)
- Exceptions: none
- Why EXTRA: Precedence of engineering policy over product/task inputs is not entailed by GOV-001 (which concerns product behaviour authority).
- Evidence M1-S000039: `output/template/CLAUDE.md:45-47` — "Product and task inputs are inputs, not instruction layers: they may request an ⏎ engineering decision change but never silently override engineering policy; a ⏎ conflicting request becomes a Decision Request."

### EXTRA-M1-0002
- Closest oracle policies: ARC-020, ARC-001
- Modality: REQUIRES_APPROVAL
- Normative action: Changing the project reference graph is Reserved.
- Trigger/scope: always (CLAUDE.md)
- Exceptions: none
- Why EXTRA: ARC-020 gates new projects/layers; changes to references between existing projects need no approval in the oracle.
- Evidence M1-S000051: `output/template/CLAUDE.md:78-79` — "3. adding a production project, layer, or assembly, or changing the project ⏎      reference graph;"
- Evidence M1-S001872: `output/template/.claude/skills/project-structure/SKILL.md:106-107` — "1. Determine whether a new assembly is justified — a new production project or ⏎    a changed reference graph is Reserved (`CLAUDE.md` § Decision Control)."
- Evidence M1-S001881: `output/template/.claude/skills/project-structure/SKILL.md:124-127` — "2. Classify the change with `CLAUDE.md` § Decision Control. Adding a reference ⏎    that the layout prescribes for projects of the approved structure follows ⏎    the Decided layout (Scaffolding Procedure, step 6); any other change to the ⏎    reference graph is Reserved: raise it through `architecture-decision` first."

### EXTRA-M1-0003
- Closest oracle policies: ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Adding search, external storage or external identity infrastructure is Reserved.
- Trigger/scope: always (CLAUDE.md)
- Exceptions: none
- Why EXTRA: Categories beyond ARC-020's enumeration.
- Evidence M1-S000053: `output/template/CLAUDE.md:82-83` — "5. adding an infrastructure category: messaging, background processing, ⏎      distributed caching, search, external storage, external identity;"

### EXTRA-M1-0004
- Closest oracle policies: DEP-001, GOV-013
- Modality: REQUIRES_APPROVAL
- Normative action: Adding a major library or framework is Reserved.
- Trigger/scope: always (CLAUDE.md)
- Exceptions: none
- Why EXTRA: Oracle requires concrete need for libraries but approval only for replacement/risky licences.
- Evidence M1-S000054: `output/template/CLAUDE.md:84-85` — "6. adding a major library or framework, or replacing an approved baseline ⏎      technology;"
- Evidence M1-S000790: `output/template/.claude/skills/add-dependency/SKILL.md:17-19` — "- Use the approved technology when one exists (`docs/technology-stack.md`, ⏎   `docs/capabilities/`). A major library or framework, or a replacement for an ⏎   approved technology, is Reserved (`CLAUDE.md` § Decision Control)."

### EXTRA-M1-0005
- Closest oracle policies: ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Introducing any project-wide convention or abstraction other code must follow is Reserved.
- Trigger/scope: always (CLAUDE.md)
- Exceptions: none
- Why EXTRA: Generalises ARC-020's project-wide Result example.
- Evidence M1-S000055: `output/template/CLAUDE.md:86-87` — "7. introducing a project-wide convention or abstraction other code must ⏎      follow;"

### EXTRA-M1-0006
- Closest oracle policies: API-013, DEP-017
- Modality: REQUIRES_APPROVAL
- Normative action: Adopting API versioning is Reserved.
- Trigger/scope: always (CLAUDE.md)
- Exceptions: none
- Why EXTRA: API-013 allows versioning for a concrete need without approval.
- Evidence M1-S000057: `output/template/CLAUDE.md:89-89` — "9. making a breaking public API change or adopting API versioning;"
- Evidence M1-S000505: `output/template/.claude/rules/api.md:33-35` — "- Do not introduce API versioning merely because an API exists; add it when ⏎   published compatibility or coexisting client generations create a concrete ⏎   need. Adopting versioning is Reserved."

### EXTRA-M1-0007
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: In an unclear case any yes makes it Reserved: adds/removes/replaces a dependency, framework or infrastructure capability; changes a project/layer/reference boundary; establishes a convention; changes observable behaviour or a public contract; expensive to reverse.
- Trigger/scope: always (CLAUDE.md)
- Exceptions: Unclear cases only.
- Why EXTRA: Classification heuristic widening Reserved beyond the oracle's gates.
- Evidence M1-S000059: `output/template/CLAUDE.md:93-98` — "For an unclear case, any "yes" makes it Reserved: (1) does it add, remove, or ⏎ replace a dependency, framework, or infrastructure capability? (2) does it ⏎ change a project, layer, or reference boundary? (3) does it establish a ⏎ convention other code is expected to follow? (4) does it change observable ⏎ behavior or a public contract? (5) would it be expensive to reverse once other ⏎ code depend …"

### EXTRA-M1-0008
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: A Decision Request contains Context, Options, Recommendation, Blocked and Proceeding with.
- Trigger/scope: always (CLAUDE.md)
- Exceptions: none
- Why EXTRA: Fixed request format not in the oracle.
- Evidence M1-S000060: `output/template/CLAUDE.md:100-101` — "Raise a Reserved decision as a Decision Request (Context, Options, ⏎ Recommendation, Blocked, Proceeding with) through `architecture-decision`. An"
- Evidence M1-S000904: `output/template/.claude/skills/architecture-decision/SKILL.md:20-38` — "```text ⏎ Decision Request: <short title> ⏎  ⏎ Context: ⏎ <what triggered the decision; the relevant facts, constraints, and owners> ⏎  ⏎ Options: ⏎ 1. <option> — <consequences, cost to reverse> ⏎ 2. <option> — <consequences, cost to reverse> ⏎  ⏎ Recommendation: ⏎ <preferred option and why> ⏎  ⏎ Blocked: ⏎ <work that cannot proceed until the decision is made> ⏎  ⏎ Proceeding with: ⏎ <policy-compl …"

### EXTRA-M1-0009
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST
- Normative action: An explicit user instruction may count as approval but must be recorded through architecture-decision.
- Trigger/scope: always (CLAUDE.md)
- Exceptions: none
- Why EXTRA: Defines approval and adds a recording obligation.
- Evidence M1-S000061: `output/template/CLAUDE.md:102-102` — "explicit user instruction may count as approval but must be recorded there. In"
- Evidence M1-S000906: `output/template/.claude/skills/architecture-decision/SKILL.md:42-43` — "- Interactive session: wait for an explicit answer before implementing the ⏎   Reserved part; an explicit user instruction counts as approval."

### EXTRA-M1-0010
- Closest oracle policies: none
- Modality: MUST
- Normative action: For changes to the instruction system itself ask the user to run /template-maintenance (do not perform it automatically).
- Trigger/scope: always (CLAUDE.md)
- Exceptions: none
- Why EXTRA: Repo/meta restriction on instruction-system changes; not an oracle policy.
- Evidence M1-S000069: `output/template/CLAUDE.md:129-129` — "| changing the instruction system itself | ask the user to run `/template-maintenance` |"
- Evidence M1-S000917: `output/template/.claude/skills/architecture-decision/SKILL.md:71-73` — "After approval, record the ADR and the new selection intent. Applying the ⏎ replacement changes the instruction system, so ask the user to run ⏎ `/template-maintenance` (§ Capability Replacement)."

### EXTRA-M1-0011
- Closest oracle policies: DEP-008
- Modality: MUST
- Normative action: Use the latest stable servicing release of the .NET 10 line.
- Trigger/scope: always (imported by CLAUDE.md)
- Exceptions: none
- Why EXTRA: Patch-level requirement beyond DEP-008.
- Evidence M1-S000131: `output/template/docs/technology-stack.md:16-18` — "- .NET 10 LTS (latest stable servicing release of the line), C# 14, ASP.NET ⏎   Core, and ASP.NET Core Controllers. Do not move to a preview/RC .NET or C# ⏎   release without approval."

### EXTRA-M1-0012
- Closest oracle policies: DEP-008, DEP-022
- Modality: DEFAULT
- Normative action: global.json pins the stable SDK line.
- Trigger/scope: always (imported by CLAUDE.md)
- Exceptions: none
- Why EXTRA: SDK pinning via global.json is not in the oracle.
- Evidence M1-S000133: `output/template/docs/technology-stack.md:21-25` — "- Shared build configuration: repository-level `Directory.Build.props` for ⏎   genuinely shared .NET settings (target framework, nullable, implicit usings, ⏎   analysis/compiler settings) and `Directory.Packages.props` for NuGet Central ⏎   Package Management; project-specific settings stay in their owning projects. ⏎   `global.json` pins the stable SDK line."
- Evidence M1-S001832: `output/template/.claude/skills/project-structure/references/solution-layout.md:69-72` — "- `global.json` — pin the intended stable SDK line; when scaffolding, select the ⏎   current stable SDK for the target .NET release (no RC/preview SDK unless ⏎   explicitly requested) and allow normal servicing through the chosen ⏎   `rollForward` policy."

### EXTRA-M1-0013
- Closest oracle policies: DEP-011, ARC-002
- Modality: MUST_NOT
- Normative action: Keep mapping-library concerns out of Domain; no other mapping framework without approval.
- Trigger/scope: always (imported by CLAUDE.md)
- Exceptions: Approval.
- Why EXTRA: Not stated in DEP-011/ARC-002.
- Evidence M1-S000142: `output/template/docs/technology-stack.md:48-48` — "| Mapster, Mapster.DependencyInjection | mapping volume becomes repetitive or non-trivial; manual mapping is fine for simple cases; keep mapping-library concerns out of Domain; no other mapping framework without approval |"

### EXTRA-M1-0014
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST
- Normative action: Changing a capability selection requires an ADR via architecture-decision.
- Trigger/scope: always (imported by CLAUDE.md)
- Exceptions: none
- Why EXTRA: ADR obligation not entailed by the oracle.
- Evidence M1-S000117: `output/template/docs/capability-selection.md:1-1` — "> Capability selection record · Always loaded (imported by `CLAUDE.md`) · Changing a selection is Reserved and requires an ADR (`architecture-decision` workflow)"
- Evidence M1-S000915: `output/template/.claude/skills/architecture-decision/SKILL.md:65-67` — "Changing a slot selection, enabling or disabling the optional frontend slot, or ⏎ changing a declared property such as the persistence provider variant is ⏎ Reserved and requires an ADR. An observable declared-property change (for"

### EXTRA-M1-0015
- Closest oracle policies: none
- Modality: MUST
- Normative action: Static composition: each required slot has exactly one selected implementation, the optional slot zero or one; only selected implementations have runtime facets.
- Trigger/scope: always (imported by CLAUDE.md)
- Exceptions: none
- Why EXTRA: Capability-system invariant (repo/meta), not an oracle policy.
- Evidence M1-S000119: `output/template/docs/capability-selection.md:5-7` — "Static composition: each required slot has exactly one selected implementation; ⏎ the optional slot has zero or one. Only selected implementations have runtime ⏎ facets."
- Evidence M1-S000430: `output/template/.claude/scripts/check-instructions.js:271-283` — "const modules = []; ⏎   for (const slot of SLOTS) { ⏎     const slotRows = rows.filter((r) => r.slot === slot); ⏎     if (slotRows.length !== 1) { ⏎       add('ERROR', common.SELECTION_FILE, `slot ${slot} must appear exactly once (found ${slotRows.length}).`); ⏎       continue; ⏎     } ⏎     const row = slotRows[0]; ⏎     const impl = common.selectedImplementation(row); ⏎     if (/[,;]|\band\b|\// …"

### EXTRA-M1-0016
- Closest oracle policies: DEP-013, ARC-028
- Modality: DEFAULT
- Normative action: Test projects are <Name>.Application.Tests and <Name>.IntegrationTests (Domain.Tests/Infrastructure.Tests only when justified).
- Trigger/scope: always (imported by CLAUDE.md)
- Exceptions: Optional projects when justified.
- Why EXTRA: Test-project naming/set convention not in the oracle.
- Evidence M1-S000095: `output/template/docs/capabilities/architecture.md:23-23` — "| test projects | `<Name>.Application.Tests` and `<Name>.IntegrationTests`; `<Name>.Domain.Tests` or `<Name>.Infrastructure.Tests` only when justified |"
- Evidence M1-S001807: `output/template/.claude/skills/project-structure/references/backend-layout.md:146-148` — "Typical intent: `Application.Tests` covers application-service and use-case ⏎ behavior; `IntegrationTests` covers Api + Application + Infrastructure through ⏎ the real host (`WebApplicationFactory<Program>`)."

### EXTRA-M1-0017
- Closest oracle policies: RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: Nullable reference types enabled repository-wide.
- Trigger/scope: all .NET projects (MSBuild)
- Exceptions: Project override possible.
- Why EXTRA: Not mandated by the oracle.
- Evidence M1-S000080: `output/template/Directory.Build.props:8-8` — "<Nullable>enable</Nullable>"

### EXTRA-M1-0018
- Closest oracle policies: RUN-010
- Modality: ENFORCED_DEFAULT
- Normative action: Implicit usings enabled repository-wide.
- Trigger/scope: all .NET projects (MSBuild)
- Exceptions: Project override possible.
- Why EXTRA: Not mandated by the oracle.
- Evidence M1-S000081: `output/template/Directory.Build.props:9-9` — "<ImplicitUsings>enable</ImplicitUsings>"

### EXTRA-M1-0019
- Closest oracle policies: RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: UTF-8, final newline, trimmed trailing whitespace, space indentation of 4 by default.
- Trigger/scope: repository files (EditorConfig)
- Exceptions: none
- Why EXTRA: Concrete formatting settings beyond RUN-009's 'follow .editorconfig'.
- Evidence M1-S000004: `output/template/.editorconfig:8-12` — "charset = utf-8 ⏎ insert_final_newline = true ⏎ trim_trailing_whitespace = true ⏎ indent_style = space ⏎ indent_size = 4"

### EXTRA-M1-0020
- Closest oracle policies: RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: 2-space indentation for JSON/YAML/Markdown, TS/HTML/SCSS/CSS and project/XML files.
- Trigger/scope: repository files (EditorConfig)
- Exceptions: none
- Why EXTRA: Concrete formatting settings.
- Evidence M1-S000006: `output/template/.editorconfig:15-15` — "indent_size = 2"
- Evidence M1-S000008: `output/template/.editorconfig:18-18` — "indent_size = 2"
- Evidence M1-S000010: `output/template/.editorconfig:21-21` — "indent_size = 2"

### EXTRA-M1-0021
- Closest oracle policies: RUN-010
- Modality: ENFORCED_DEFAULT
- Normative action: System usings sorted first; no blank-line separation of import groups.
- Trigger/scope: repository files (EditorConfig)
- Exceptions: none
- Why EXTRA: Using-ordering conventions not in the oracle.
- Evidence M1-S000014: `output/template/.editorconfig:26-27` — "dotnet_sort_system_directives_first = true ⏎ dotnet_separate_import_directive_groups = false"

### EXTRA-M1-0022
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: var when the type is apparent; explicit types for built-in types and elsewhere (suggestion).
- Trigger/scope: repository files (EditorConfig)
- Exceptions: none
- Why EXTRA: Type-inference style not in the oracle.
- Evidence M1-S000017: `output/template/.editorconfig:31-33` — "csharp_style_var_for_built_in_types = false:suggestion ⏎ csharp_style_var_when_type_is_apparent = true:suggestion ⏎ csharp_style_var_elsewhere = false:suggestion"

### EXTRA-M1-0023
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: Braces preferred for control blocks (suggestion).
- Trigger/scope: repository files (EditorConfig)
- Exceptions: none
- Why EXTRA: Brace style not in the oracle.
- Evidence M1-S000020: `output/template/.editorconfig:42-42` — "csharp_prefer_braces = true:suggestion"

### EXTRA-M1-0024
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: PascalCase types/members, I-prefixed PascalCase interfaces, camelCase parameters/locals (suggestion).
- Trigger/scope: repository files (EditorConfig)
- Exceptions: none
- Why EXTRA: Naming conventions not in the oracle.
- Evidence M1-S000023: `output/template/.editorconfig:47-51` — "dotnet_naming_symbols.types_and_members.applicable_kinds = class, struct, interface, enum, method, property, event, delegate ⏎ dotnet_naming_style.pascal_case.capitalization = pascal_case ⏎ dotnet_naming_rule.types_and_members_pascal.symbols = types_and_members ⏎ dotnet_naming_rule.types_and_members_pascal.style = pascal_case ⏎ dotnet_naming_rule.types_and_members_pascal.severity = suggestion"
- Evidence M1-S000024: `output/template/.editorconfig:53-58` — "dotnet_naming_symbols.interfaces.applicable_kinds = interface ⏎ dotnet_naming_style.i_prefix.required_prefix = I ⏎ dotnet_naming_style.i_prefix.capitalization = pascal_case ⏎ dotnet_naming_rule.interfaces_i_prefix.symbols = interfaces ⏎ dotnet_naming_rule.interfaces_i_prefix.style = i_prefix ⏎ dotnet_naming_rule.interfaces_i_prefix.severity = suggestion"
- Evidence M1-S000025: `output/template/.editorconfig:60-64` — "dotnet_naming_symbols.parameters_and_locals.applicable_kinds = parameter, local ⏎ dotnet_naming_style.camel_case.capitalization = camel_case ⏎ dotnet_naming_rule.parameters_and_locals_camel.symbols = parameters_and_locals ⏎ dotnet_naming_rule.parameters_and_locals_camel.style = camel_case ⏎ dotnet_naming_rule.parameters_and_locals_camel.severity = suggestion"

## LINK_UNCERTAIN constraints (3)

### UNCERTAIN-M1-0002
- Closest oracle policies: RUN-021
- Modality: ALLOWED
- Normative action: Invalidate before the mutation is known to have succeeded only when the workflow deliberately accepts that behaviour.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: Deliberate acceptance.
- Open question: Open question: is pre-success invalidation an exception relaxing RUN-021 ('only consistently with successful mutations') or consistent with it because it never makes the cache a source of truth?
- Evidence M1-S001079: `output/template/.claude/skills/caching/SKILL.md:86-88` — "TTL with tolerated staleness, tag/group invalidation, versioned keys. Invalidate ⏎ before the mutation is known to have succeeded only when the workflow ⏎ deliberately accepts that behavior."

### UNCERTAIN-M1-0003
- Closest oracle policies: GOV-015
- Modality: ALLOWED
- Normative action: Perform destructive Git operations only when explicitly requested or clearly required by an approved workflow.
- Trigger/scope: workflow git-workflow
- Exceptions: Approved workflow.
- Open question: Open question: does 'clearly required by an approved workflow' relax GOV-015's explicit-request condition, or is an approved workflow equivalent to an explicit request?
- Evidence M1-S001448: `output/template/.claude/skills/git-workflow/SKILL.md:100-103` — "Treat these as high-risk: `git reset --hard`, `git clean`, `git push --force`, ⏎ `git push --force-with-lease`, branch deletion, and rebasing shared history. ⏎ Perform them only when explicitly requested or clearly required by an approved ⏎ workflow, after inspecting what will be lost or rewritten."

### UNCERTAIN-M1-0001
- Closest oracle policies: GOV-006
- Modality: DEFAULT
- Normative action: SQL Server default collation compares case-insensitively and accent-sensitively; it is declared a technology default, not an approved product semantic.
- Trigger/scope: always (imported by CLAUDE.md)
- Exceptions: none
- Open question: Open question: does declaring the SQL Server collation default (CI/AS) as the persistence default (referenced from CLAUDE.md line 27-28) let implementations rely on it without approval, relaxing GOV-006, or is it documentation only with any material choice still requiring approval?
- Evidence M1-S000123: `output/template/docs/capability-selection.md:18-22` — "- persistence / string comparison: equality, uniqueness, ordering, and lookup ⏎   in database queries follow the database and column collation. SQL Server ⏎   default collations compare case-insensitively and accent-sensitively. This is ⏎   a technology default, not an approved product semantic; changing the ⏎   effective collation is a product decision (`CLAUDE.md` § Product Sources)."

