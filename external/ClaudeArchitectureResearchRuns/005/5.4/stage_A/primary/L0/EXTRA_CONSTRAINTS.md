# EXTRA and LINK_UNCERTAIN constraints — candidate L0

Generated deterministically from the annotation ledger. Each entry cites the exact
source evidence (path, line range, verbatim quote). `policy_ids` on an EXTRA entry
name the closest oracle policy only; origin stays EXTRA.

## EXTRA constraints (208)

### EXTRA-L0-0001
- Closest oracle policies: none
- Modality: MUST_NOT
- Normative action: Engineering policy lives in the instruction system; a more volatile level may refine but must not contradict a more stable level; report a contradiction instead of choosing a side.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Level-precedence rule of this instruction architecture (repo/meta).
- Evidence L0-S000391: `output/template/CLAUDE.md:14-14` — "- Engineering policy lives in this instruction system. A more volatile level may refine a more stable level but must not contradict it; report a contradiction instead of choosing a side."

### EXTRA-L0-0002
- Closest oracle policies: GOV-001, GOV-008
- Modality: MUST_NOT
- Normative action: SPECIFICATION.md, CUSTOM_SETTINGS.md, feature specifications and task prompts are product inputs, not instruction layers; they may request an engineering decision change but never silently override engineering policy.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Product-input vs engineering-policy precedence is not stated in the oracle.
- Evidence L0-S000392: `output/template/CLAUDE.md:15-15` — "- `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` are product inputs, as are feature specifications and task prompts. They define product behavior and approved values; they are not instruction layers. They may request an engineering decision change, but they never silently override engineering policy."
- Evidence L0-S001581: `output/template/.claude/tools/check-instructions.mjs:238-277` — "// ---- dependency direction and acyclicity ---- ⏎   const graph = new Map(); ⏎   for (const [file, entry] of meta) { ⏎     const targets = []; ⏎     for (const dep of entry.header.dependsOn) { ⏎       if (PRODUCT_INPUTS.includes(dep)) { ⏎         errors.push(`${file}: engineering policy must not depend on product input ${dep}`); ⏎         continue; ⏎       } ⏎       if (dep.endsWith('/**')) { ⏎   …"

### EXTRA-L0-0003
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST
- Normative action: An explicit user instruction may approve a Reserved decision; the accepted decision must be recorded with architecture-decision.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Recording obligation added to GOV-017.
- Evidence L0-S000393: `output/template/CLAUDE.md:16-16` — "- An explicit user instruction may approve a Reserved decision; record the accepted decision with `architecture-decision`."
- Evidence L0-S000646: `output/template/.claude/skills/architecture-decision/SKILL.md:33-33` — "An explicit user instruction counts as approval. After approval, in the same change:"

### EXTRA-L0-0004
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: Deviation from a 'default' needs a concrete reason and must be reported; violating a must/must-not is a defect; prefer/avoid are guidance; 'requires approval' marks a Reserved decision.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Vocabulary definition with a reporting obligation for default deviations (not in the oracle).
- Evidence L0-S000395: `output/template/CLAUDE.md:20-20` — "**must / must not** — violation is a defect. **default** — deviation needs a concrete reason and must be reported. **prefer / avoid** — guidance. **requires approval** — Reserved decision."

### EXTRA-L0-0005
- Closest oracle policies: ARC-020, ARC-001
- Modality: REQUIRES_APPROVAL
- Normative action: Changing the project reference graph is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: ARC-020 covers new projects/layers; reference changes between existing projects are not gated in the oracle.
- Evidence L0-S000412: `output/template/CLAUDE.md:42-42` — "3. adding a production project/layer/assembly or changing the project reference graph;"

### EXTRA-L0-0006
- Closest oracle policies: ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Adding search, external storage or external identity infrastructure is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Categories beyond ARC-020's enumeration.
- Evidence L0-S000414: `output/template/CLAUDE.md:44-44` — "5. adding an infrastructure category: messaging, background processing, distributed cache, search, external storage, external identity;"

### EXTRA-L0-0007
- Closest oracle policies: DEP-001, GOV-013
- Modality: REQUIRES_APPROVAL
- Normative action: Adding a major library or framework is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: The oracle requires current need (DEP-001), not approval, for new libraries.
- Evidence L0-S000415: `output/template/CLAUDE.md:45-45` — "6. adding a major library/framework or replacing an approved baseline technology;"

### EXTRA-L0-0008
- Closest oracle policies: ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Introducing any project-wide convention or abstraction other code is expected to follow is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: Generalizes ARC-020's project-wide Result example.
- Evidence L0-S000416: `output/template/CLAUDE.md:46-46` — "7. introducing a project-wide convention or abstraction that other code is expected to follow, for example a project-wide Result model;"

### EXTRA-L0-0009
- Closest oracle policies: API-013, DEP-017
- Modality: REQUIRES_APPROVAL
- Normative action: Adopting API versioning is Reserved.
- Trigger/scope: always (planning-time, all work)
- Exceptions: none
- Why EXTRA: API-013 requires a real compatibility need, not approval.
- Evidence L0-S000418: `output/template/CLAUDE.md:48-48` — "9. making a breaking public API change or adopting API versioning;"

### EXTRA-L0-0010
- Closest oracle policies: DEP-023, RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: Shared build settings: Nullable enable, ImplicitUsings enable, AnalysisLevel latest.
- Trigger/scope: all .NET projects (MSBuild import)
- Exceptions: none
- Why EXTRA: Concrete compiler settings not in the oracle.
- Evidence L0-S000445: `output/template/Directory.Build.props:5-7` — "<Nullable>enable</Nullable> ⏎     <ImplicitUsings>enable</ImplicitUsings> ⏎     <AnalysisLevel>latest</AnalysisLevel>"

### EXTRA-L0-0011
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: A conformance dependency may point only to the same or a more stable level; it is declared in each file's 'Depends on' header and checked mechanically.
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Instruction-architecture invariant (repo/meta).
- Evidence L0-S000007: `output/template/.claude/INSTRUCTION_MAP.md:17-17` — "- A **conformance dependency** (a rule that builds on another rule) may point only to the same or a more stable level. It is declared in each file's header (`Depends on:`) and checked mechanically."
- Evidence L0-S001519: `output/template/.claude/skills/template-maintenance/SKILL.md:41-41` — "- `Depends on` lists conformance dependencies only, and each must be the same level or more stable; routing pointers may point anywhere."
- Evidence L0-S001581: `output/template/.claude/tools/check-instructions.mjs:238-277` — "// ---- dependency direction and acyclicity ---- ⏎   const graph = new Map(); ⏎   for (const [file, entry] of meta) { ⏎     const targets = []; ⏎     for (const dep of entry.header.dependsOn) { ⏎       if (PRODUCT_INPUTS.includes(dep)) { ⏎         errors.push(`${file}: engineering policy must not depend on product input ${dep}`); ⏎         continue; ⏎       } ⏎       if (dep.endsWith('/**')) { ⏎   …"

### EXTRA-L0-0012
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Levels 0 and 1 name no concrete technology beyond the fixed platform (.NET, C#, TypeScript; Git for repository safety).
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Instruction-architecture invariant (repo/meta), checked by check-instructions.mjs.
- Evidence L0-S000009: `output/template/.claude/INSTRUCTION_MAP.md:19-19` — "- Levels 0 and 1 name no concrete technology beyond the fixed platform (.NET, C#, TypeScript; Git for repository safety). Protocols and standards (HTTP, TLS, OIDC, CSRF, SQL) are vocabulary, not technologies."
- Evidence L0-S001520: `output/template/.claude/skills/template-maintenance/SKILL.md:42-42` — "- Levels 0 and 1 must not name concrete technologies beyond the fixed platform."
- Evidence L0-S001570: `output/template/.claude/tools/check-instructions.mjs:44-53` — "// Concrete technologies that Levels 0 and 1 must not name (fixed platform: .NET, C#, TypeScript; Git). ⏎ const TECHNOLOGY_TERMS = [ ⏎   /EF Core/i, /Entity Framework/i, /\bDbContext\b/, /\bDbSet\b/, /\bNUnit\b/i, /\bxUnit\b/i, /\bMSTest\b/i, ⏎   /\bAngular\b/i, /\bRxJS\b/i, /\bSerilog\b/i, /\bFluentValidation\b/i, /ASP\.NET/i, /\bSwashbuckle\b/i, ⏎   /\bSwagger\b/i, /\bDocker\b/i, /\bKubernetes\b …"
- Evidence L0-S001580: `output/template/.claude/tools/check-instructions.mjs:229-236` — "// ---- technology neutrality of Levels 0 and 1 ---- ⏎   for (const [file, entry] of meta) { ⏎     if (entry.header.level > 1 || file === MAP) continue; ⏎     for (const term of TECHNOLOGY_TERMS) { ⏎       const hit = entry.text.match(term); ⏎       if (hit) errors.push(`${file}: Level ${entry.header.level} must not name the concrete technology '${hit[0]}'`); ⏎     } ⏎   }"

### EXTRA-L0-0013
- Closest oracle policies: none
- Modality: MUST
- Normative action: Each rule has exactly one owner; other files point to it (rule = constraint, workflow = procedure, knowledge skill = technique, hooks/scripts = enforcement).
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Instruction-ownership rule (repo/meta).
- Evidence L0-S000012: `output/template/.claude/INSTRUCTION_MAP.md:24-24` — "**Responsibilities:** rule = normative constraint · workflow skill = procedure · knowledge skill = technique · product files = inputs · hooks/scripts/config = deterministic enforcement. Each rule has exactly one owner; other files point to it."
- Evidence L0-S001516: `output/template/.claude/skills/template-maintenance/SKILL.md:36-36` — "State each rule once, in its owner. Elsewhere use only a routing pointer ("run `verify`", "see `backend-layers.md`") or a short check-by-reference item. Decision summaries appear only in `1-architecture/overview.md` and `3-project/decisions.md`."

### EXTRA-L0-0014
- Closest oracle policies: none
- Modality: MUST_NOT
- Normative action: Knowledge skills hold technique only and are never sole owners of a rule; a new rule goes to a rule file.
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Instruction-placement rule (repo/meta).
- Evidence L0-S000022: `output/template/.claude/INSTRUCTION_MAP.md:64-64` — "| Knowledge skills (technique only, never sole owners of a rule) | `.claude/skills/ef-core/SKILL.md`, `.claude/skills/http-api/SKILL.md`, `.claude/skills/aspnet-error-handling/SKILL.md`, `.claude/skills/dotnet-testing/SKILL.md`, `.claude/skills/logging/SKILL.md` (+ private `.claude/skills/logging/references/serilog.md`), `.claude/skills/httpclient-factory/SKILL.md` (+ private `.claude/skills/httpc …"
- Evidence L0-S001514: `output/template/.claude/skills/template-maintenance/SKILL.md:28-32` — "- Normative constraint → a rule module. Trigger: always-loaded only if it must be known at planning time (CLAUDE.md, or the two imported decision summaries); otherwise a path rule whose `paths` cover at least the scope where it applies. ⏎ - Multi-step procedure → a workflow skill; it explicitly reads the rule files it depends on. ⏎ - Technique, examples, depth → a knowledge skill (or its private ` …"

### EXTRA-L0-0015
- Closest oracle policies: none
- Modality: MUST
- Normative action: Mixed statements are split so each part lives at the level of what it depends on.
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Instruction-placement rule (repo/meta).
- Evidence L0-S000034: `output/template/.claude/INSTRUCTION_MAP.md:106-106` — "Mixed statements are split so each part lives at the level of what it depends on:"
- Evidence L0-S001512: `output/template/.claude/skills/template-maintenance/SKILL.md:24-24` — "A statement's level is set by the most volatile thing it depends on. Split mixed statements: the neutral rule goes to the stable level, the technology binding to Level 2, the project selection to Level 3 (see the split-statement table in `.claude/INSTRUCTION_MAP.md`)."

### EXTRA-L0-0016
- Closest oracle policies: DEP-002
- Modality: MUST
- Normative action: Replacing a technology edits its Level 2 module, the Level 3 selection and embedding workflows/assets; Levels 0 and 1 stay unchanged.
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: Technology replacement.
- Why EXTRA: Repo/meta procedure.
- Evidence L0-S000037: `output/template/.claude/INSTRUCTION_MAP.md:124-124` — "Replacing a technology (for example NUnit with xUnit) means editing its Level 2 module, the Level 3 selection, and the workflows or assets where the choice is embedded; Levels 0 and 1 stay unchanged."

### EXTRA-L0-0017
- Closest oracle policies: none
- Modality: MUST
- Normative action: Place a new rule at Level 3 if it depends on repository selection/layout/defaults/commands, Level 2 if it names a technology, Level 1 if it presupposes the architecture, else Level 0.
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta placement rule.
- Evidence L0-S000039: `output/template/.claude/INSTRUCTION_MAP.md:128-131` — "1. Depends on this repository's selection, layout, defaults, or commands → Level 3. ⏎ 2. Names a technology beyond the fixed platform → Level 2. ⏎ 3. Presupposes the architecture, a layer, role, or boundary → Level 1. ⏎ 4. Otherwise → Level 0."
- Evidence L0-S001511: `output/template/.claude/skills/template-maintenance/SKILL.md:19-22` — "1. Depends on project-specific selection, layout, defaults, or concrete commands? → **Level 3 Project** (`.claude/rules/3-project/`, project workflows). ⏎ 2. Names a technology other than the fixed platform (.NET, C#, TypeScript; Git for repository safety)? → **Level 2 Technology** (`.claude/rules/2-technology/`, knowledge skills). ⏎ 3. Presupposes the adopted architecture, a layer, role, or bound …"

### EXTRA-L0-0018
- Closest oracle policies: none
- Modality: MUST
- Normative action: Pick the artifact by responsibility and trigger (planning-time rule → CLAUDE.md or a decision summary; file-scoped → path rule covering its scope; procedure → workflow; technique → knowledge skill; mechanical check → hook/script) and run template-maintenance.
- Trigger/scope: repo/meta (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta placement rule.
- Evidence L0-S000040: `output/template/.claude/INSTRUCTION_MAP.md:133-133` — "Then pick the artifact by responsibility and trigger: planning-time rule → CLAUDE.md or a decision summary; file-scoped rule → a path rule covering at least its scope; procedure → a workflow skill; technique → a knowledge skill; mechanical check → a hook or script. Run `template-maintenance`."
- Evidence L0-S001514: `output/template/.claude/skills/template-maintenance/SKILL.md:28-32` — "- Normative constraint → a rule module. Trigger: always-loaded only if it must be known at planning time (CLAUDE.md, or the two imported decision summaries); otherwise a path rule whose `paths` cover at least the scope where it applies. ⏎ - Multi-step procedure → a workflow skill; it explicitly reads the rule files it depends on. ⏎ - Technique, examples, depth → a knowledge skill (or its private ` …"

### EXTRA-L0-0019
- Closest oracle policies: GOV-017, ARC-020
- Modality: DEFAULT
- Normative action: Approved architecture/stack changes are recorded in the decision summary by architecture-decision with date, decision, scope, consequences and updated owning rule/modules.
- Trigger/scope: always (imported); paths backend/**/*.cs, backend/**/*.csproj, frontend/**/*
- Exceptions: none
- Why EXTRA: Decision-record format not in the oracle.
- Evidence L0-S000222: `output/template/.claude/rules/1-architecture/overview.md:47-47` — "Approved architecture changes are recorded here by `architecture-decision` (date · decision · scope · consequences · owning rule updated)."
- Evidence L0-S000360: `output/template/.claude/rules/3-project/decisions.md:53-53` — "Approved stack or default changes are recorded here by `architecture-decision` (date · decision · scope · consequences · modules/workflows updated)."
- Evidence L0-S000647: `output/template/.claude/skills/architecture-decision/SKILL.md:35-35` — "1. Add an entry to the matching decision summary — architecture-level decisions (styles, patterns, layers, boundaries) in `.claude/rules/1-architecture/overview.md` → Accepted architecture decisions; stack, conditional technology, and project-default decisions in `.claude/rules/3-project/decisions.md` → Accepted project decisions. Entry: date · decision · scope · consequences · files updated."

### EXTRA-L0-0020
- Closest oracle policies: DEP-011, DEP-002
- Modality: REQUIRES_APPROVAL
- Normative action: Adding another mapping framework requires approval.
- Trigger/scope: always (imported); paths *.slnx, **/*.csproj, Directory.*.props, frontend/**/package.json
- Exceptions: none
- Why EXTRA: Approval gate not stated in DEP-011.
- Evidence L0-S000354: `output/template/.claude/rules/3-project/decisions.md:43-43` — "- Backend: mediator libraries such as MediatR or Kommand (mediator-based organization is not adopted — `1-architecture/overview.md`); another mapping framework without approval."

### EXTRA-L0-0031
- Closest oracle policies: DEP-025, ARC-001
- Modality: ENFORCED
- Normative action: pre-bash fails closed: unreadable/malformed payload, missing command, unknown event or internal error exits 2 and blocks the shell call; settings.json adds onFailure block for launch failures, crashes and timeouts; post-event and Stop failures exit 1 (visible, non-blocking).
- Trigger/scope: hook events registered in settings.json (Bash/PowerShell pre/post, Edit/MultiEdit/Write post, Stop) for the active governed repository/worktree
- Exceptions: none
- Why EXTRA: Fail-closed enforcement policy is not part of the oracle.
- Evidence L0-S000459: `output/template/.claude/hooks/claude-hook.mjs:46-61` — "const event = process.argv[2]; ⏎ const failClosed = event === 'pre-bash'; ⏎ const launcherRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..'); ⏎  ⏎ function say(lines) { ⏎   process.stderr.write(lines.map(line => `[project hook] ${line}`).join('\n') + '\n'); ⏎ } ⏎  ⏎ function unavailable(message) { ⏎   if (failClosed) { ⏎     say([`Blocked: the shell call could not be che …"
- Evidence L0-S000540: `output/template/.claude/settings.json:7-7` — "{ "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "pre-bash"], "timeout": 30, "onFailure": "block" }"

### EXTRA-L0-0032
- Closest oracle policies: DEP-025
- Modality: MUST_NOT
- Normative action: If the user explicitly decides to override a peer-dependency conflict, the user runs the command; Claude does not.
- Trigger/scope: hook events registered in settings.json (Bash/PowerShell pre/post, Edit/MultiEdit/Write post, Stop) for the active governed repository/worktree
- Exceptions: none
- Why EXTRA: DEP-025 forbids bypassing merely to pass; delegating an approved override to the user is an added restriction.
- Evidence L0-S000474: `output/template/.claude/hooks/claude-hook.mjs:362-365` — "for (const item of found.filter(entry => entry.bypass)) { ⏎     lines.push(`Blocked: '${item.text}' bypasses peer-dependency compatibility.`); ⏎     lines.push(`Resolve the conflict as ${ADD_DEPENDENCY} (Install) describes. If the user explicitly decides to override, the user runs the command.`); ⏎   }"
- Evidence L0-S000571: `output/template/.claude/skills/add-dependency/SKILL.md:55-55` — "- Never use `npm --force` or `--legacy-peer-deps` merely to bypass incompatible peer dependencies; resolve the actual compatibility problem (the project hook blocks these flags; if the user explicitly decides to override, the user runs the command)."

### EXTRA-L0-0033
- Closest oracle policies: ARC-001, ARC-020
- Modality: ENFORCED
- Normative action: pre-bash blocks every dotnet add/remove … reference and dotnet reference add/remove command (no approval marker); mapped references follow project-structure, other graph changes need a Decision Request via architecture-decision; approved changes are applied in the project file.
- Trigger/scope: hook events registered in settings.json (Bash/PowerShell pre/post, Edit/MultiEdit/Write post, Stop) for the active governed repository/worktree
- Exceptions: none
- Why EXTRA: Blocking all reference commands goes beyond ARC-001/ARC-020.
- Evidence L0-S000469: `output/template/.claude/hooks/claude-hook.mjs:276-285` — "function classifyDotnet(args) { ⏎   const [verb, second, third] = args.filter(arg => !arg.startsWith('-')).map(arg => arg.toLowerCase()); ⏎   if (verb === 'add' || verb === 'remove') { ⏎     const noun = second === 'package' || second === 'reference' ? second : third; // optional <PROJECT> argument ⏎     if (noun === 'package' || noun === 'reference') return { kind: noun, bypass: false }; ⏎   } ⏎  …"
- Evidence L0-S000475: `output/template/.claude/hooks/claude-hook.mjs:366-369` — "for (const item of found.filter(entry => entry.kind === 'reference')) { ⏎     lines.push(`Blocked: '${item.text}' changes the project reference graph, which requires approval (CLAUDE.md → Decision control).`); ⏎     lines.push(`References mapped by ${LAYOUT} follow ${PROJECT_STRUCTURE} (Project references); any other graph change needs a Decision Request through ${ARCHITECTURE_DECISION}. Apply an  …"
- Evidence L0-S001367: `output/template/.claude/skills/project-structure/SKILL.md:50-50` — "Add only the references `layout.md` maps from the Level 1 dependency direction, as `<ProjectReference>` items in the project files (for example `<ProjectReference Include="..\<Name>.Domain\<Name>.Domain.csproj" />` in `<Name>.Application.csproj`). Never add an outward reference to make compilation easier. The project hook blocks `dotnet add/remove … reference` and `dotnet reference add/remove` (re …"

### EXTRA-L0-0034
- Closest oracle policies: DEP-004, ARC-020
- Modality: ENFORCED_ADVISORY
- Normative action: post-bash reports added, removed and moved manifests (tracked and untracked, not ignored) and routes them: .csproj to project-structure (production project or reference-graph change outside the layout requires approval), others to add-dependency/package-management, with a request to report.
- Trigger/scope: hook events registered in settings.json (Bash/PowerShell pre/post, Edit/MultiEdit/Write post, Stop) for the active governed repository/worktree
- Exceptions: none
- Why EXTRA: Manifest add/remove/move routing is added enforcement.
- Evidence L0-S000480: `output/template/.claude/hooks/claude-hook.mjs:426-430` — "function ownerFor(file) { ⏎   return file.endsWith('.csproj') ⏎     ? `${PROJECT_STRUCTURE} (a production project or reference-graph change outside the layout mapped by ${LAYOUT} requires approval — CLAUDE.md → Decision control); report it` ⏎     : `${ADD_DEPENDENCY} / ${PACKAGE_MANAGEMENT}; report it`; ⏎ }"
- Evidence L0-S000481: `output/template/.claude/hooks/claude-hook.mjs:432-456` — "function compareStates(root, previous, current, fresh) { ⏎   const lines = []; ⏎   const validate = new Set(fresh ? Object.keys(current.manifests) : []); ⏎   const added = Object.keys(current.manifests).filter(file => !previous[file]); ⏎   const removed = Object.keys(previous).filter(file => !current.manifests[file]); ⏎   for (const file of removed) { ⏎     const target = added.find(candidate => c …"

### EXTRA-L0-0035
- Closest oracle policies: ARC-001, ARC-020
- Modality: ENFORCED_ADVISORY
- Normative action: Project reference graph changes in a .csproj prompt confirming the layout mapping or an approved decision, and reporting it.
- Trigger/scope: hook events registered in settings.json (Bash/PowerShell pre/post, Edit/MultiEdit/Write post, Stop) for the active governed repository/worktree
- Exceptions: none
- Why EXTRA: Reference-graph change reporting is added (tied to the Reserved reference-graph rule).
- Evidence L0-S000479: `output/template/.claude/hooks/claude-hook.mjs:422-424` — "function referenceChangeLine(file, changes) { ⏎   return `Project reference graph change in ${file}: ${changes.join(', ')} → confirm it is the layout mapped by ${LAYOUT} (${PROJECT_STRUCTURE}) or an approved decision (${ARCHITECTURE_DECISION}; CLAUDE.md → Decision control), and report it.`; ⏎ }"
- Evidence L0-S000483: `output/template/.claude/hooks/claude-hook.mjs:460-462` — "if (delta.references.length > 0) { ⏎       lines.push(referenceChangeLine(file, delta.references)); ⏎     }"
- Evidence L0-S000492: `output/template/.claude/hooks/claude-hook.mjs:565-592` — "if (isManifest(relative) && !inSkippedDir(relative)) { ⏎     const lines = checkManifestFile(root, absolute).map(problem => `  - ${problem}`); ⏎     let detection = null; ⏎     if (active.git && !relative.endsWith('.npmrc')) { ⏎       let current = { packages: new Map(), references: new Set() }; ⏎       try { ⏎         current = declaredDependencies(relative, decodeText(readFileSync(absolute))); ⏎ …"

### EXTRA-L0-0036
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: After editing CLAUDE.md or .claude/**/*.md|json|mjs (except settings.local), check-instructions runs and its errors are returned as feedback (template-maintenance); a missing checker is reported as unavailable.
- Trigger/scope: hook events registered in settings.json (Bash/PowerShell pre/post, Edit/MultiEdit/Write post, Stop) for the active governed repository/worktree
- Exceptions: none
- Why EXTRA: Instruction-system enforcement (repo/meta).
- Evidence L0-S000493: `output/template/.claude/hooks/claude-hook.mjs:594-605` — "if (relative === 'CLAUDE.md' || (relative.startsWith('.claude/') && /\.(md|json|mjs)$/.test(relative) && !relative.startsWith('.claude/settings.local'))) { ⏎     const checkerFile = [path.join(root, CHECKER), path.join(launcherRoot, CHECKER)].find(file => existsSync(file)); ⏎     if (!checkerFile) unavailable(`instruction-structure check after editing ${relative} is unavailable: ${CHECKER} is miss …"
- Evidence L0-S000544: `output/template/.claude/settings.json:21-21` — "{ "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "post-edit"], "timeout": 60 }"

### EXTRA-L0-0037
- Closest oracle policies: TST-009, TST-010
- Modality: ENFORCED_ADVISORY
- Normative action: At Stop, production backend/frontend code changes without any test change prompt confirming equivalent coverage or adding tests.
- Trigger/scope: hook events registered in settings.json (Bash/PowerShell pre/post, Edit/MultiEdit/Write post, Stop) for the active governed repository/worktree
- Exceptions: none
- Why EXTRA: General test co-change reminder not in the oracle.
- Evidence L0-S000501: `output/template/.claude/hooks/claude-hook.mjs:673-675` — "if ((productionBackend || productionFrontend) && !has(PATTERNS.backendTest) && !has(PATTERNS.frontendTest)) { ⏎     reminders.push(`Production code changed without test changes: confirm equivalent coverage exists or add tests (${DEVELOPMENT} → Implement; verify step 4).`); ⏎   }"
- Evidence L0-S000548: `output/template/.claude/settings.json:36-36` — "{ "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "stop"], "timeout": 60 }"

### EXTRA-L0-0038
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: Stop reminders must be addressed or stated as not applicable before finishing; repeated only when changed files or relevant content differ; never loops.
- Trigger/scope: hook events registered in settings.json (Bash/PowerShell pre/post, Edit/MultiEdit/Write post, Stop) for the active governed repository/worktree
- Exceptions: none
- Why EXTRA: Hook procedure (repo/meta).
- Evidence L0-S000504: `output/template/.claude/hooks/claude-hook.mjs:695-700` — "feedback([ ⏎     'Before finishing, check these co-change reminders:', ⏎     ...reminders.map(reminder => `  - ${reminder}`), ⏎     'Address each one or state why it does not apply; this reminder is repeated only when the changed files or their relevant content change.', ⏎   ]); ⏎ }"

### EXTRA-L0-0039
- Closest oracle policies: DEP-020, DEP-004
- Modality: ENFORCED_ADVISORY
- Normative action: Microsoft.Extensions.Http.Polly and Polly.Extensions.Http (deprecated resilience integration) and Serilog.Sinks.Elasticsearch (deprecated) are flagged as packages that must not be added, with no accepted-decision exception.
- Trigger/scope: manifest files checked by claude-hook.mjs (csproj, Directory.Build.props, Directory.Packages.props, package.json, .npmrc)
- Exceptions: none
- Why EXTRA: Concrete deny list not in the oracle.
- Evidence L0-S000509: `output/template/.claude/hooks/manifest-checks.mjs:18-23` — "// Packages that must not be added (deprecated or replaced by the approved integration). ⏎ const DENY_NUGET = new Map([ ⏎   ['microsoft.extensions.http.polly', `deprecated resilience integration → ${OWNER.addDependency} (Conditional package bindings)`], ⏎   ['polly.extensions.http', `deprecated resilience integration → ${OWNER.addDependency} (Conditional package bindings)`], ⏎   ['serilog.sinks.el …"
- Evidence L0-S000567: `output/template/.claude/skills/add-dependency/SKILL.md:49-49` — "- **Resilience:** when resilience is required, prefer `Microsoft.Extensions.Http.Resilience` for `HttpClient` and `Microsoft.Extensions.Resilience` for general pipelines; a direct Polly reference or Polly API configuration is an explicit, documented exception rather than the default (default). Do not add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`."

### EXTRA-L0-0040
- Closest oracle policies: DEP-011, API-010
- Modality: ENFORCED_ADVISORY
- Normative action: AutoMapper (another mapping framework) and FluentValidation.AspNetCore (legacy automatic validation) are flagged as needing a recorded decision or reported reason.
- Trigger/scope: manifest files checked by claude-hook.mjs (csproj, Directory.Build.props, Directory.Packages.props, package.json, .npmrc)
- Exceptions: Accepted decision recorded.
- Why EXTRA: Review gates beyond the oracle.
- Evidence L0-S000510: `output/template/.claude/hooks/manifest-checks.mjs:25-32` — "// Packages that need an approved decision or a reported reason before they are added. ⏎ const REVIEW_NUGET = new Map([ ⏎   ['polly', `direct Polly is an explicit exception → ${OWNER.addDependency} (Conditional package bindings)`], ⏎   ['mediatr', `mediator-based organization is not adopted (Reserved) → ${OWNER.overview}`], ⏎   ['kommand', `mediator-based organization is not adopted (Reserved) → $ …"

### EXTRA-L0-0041
- Closest oracle policies: GOV-017, ARC-020
- Modality: ENFORCED
- Normative action: Review-list exceptions are honoured only when the package name appears in an '## Accepted' section of decisions.md or overview.md; an unreadable summary keeps the package flagged.
- Trigger/scope: manifest files checked by claude-hook.mjs (csproj, Directory.Build.props, Directory.Packages.props, package.json, .npmrc)
- Exceptions: none
- Why EXTRA: Approval-recording mechanism not in the oracle.
- Evidence L0-S000517: `output/template/.claude/hooks/manifest-checks.mjs:103-119` — "function acceptedDecisionsText(root) { ⏎   // Approved exceptions are recorded in the two decision summaries (architecture-decision workflow). ⏎   let text = ''; ⏎   for (const file of [OWNER.decisions, OWNER.overview]) { ⏎     const abs = path.join(root, file); ⏎     if (!existsSync(abs)) continue; ⏎     let content; ⏎     try { ⏎       content = readText(abs); ⏎     } catch { ⏎       continue; / …"

### EXTRA-L0-0021
- Closest oracle policies: DEP-001
- Modality: PREFER
- Normative action: Remove a dependency the current change makes unused when safe to verify.
- Trigger/scope: path rule: **/*.csproj, Directory.Packages.props, package.json, package-lock.json
- Exceptions: Safe to verify.
- Why EXTRA: Removal obligation not in the oracle.
- Evidence L0-S000047: `output/template/.claude/rules/0-core/dependency-hygiene.md:17-17` — "- Remove a dependency that the current change makes unused when doing so is safe to verify; do not perform unrelated dependency cleanup during a narrowly scoped task (prefer)."

### EXTRA-L0-0022
- Closest oracle policies: RUN-009, ARC-027
- Modality: PREFER
- Normative action: Name supporting types so their architectural role is clear from the name and/or directory; split a feature into subdirectories only when a flat directory becomes hard to navigate.
- Trigger/scope: path rule: backend/**, frontend/**, docs/**, *.slnx
- Exceptions: none
- Why EXTRA: Type-role naming heuristic not in the oracle.
- Evidence L0-S000155: `output/template/.claude/rules/1-architecture/code-organization.md:16-16` — "- Name supporting types so their architectural role is clear from the type name, its immediate directory, or both (prefer). Split a feature into responsibility-specific subdirectories only when a flat directory has become hard to navigate."

### EXTRA-L0-0023
- Closest oracle policies: ARC-019
- Modality: PREFER
- Normative action: Entity mappings live in Infrastructure as IEntityTypeConfiguration<T> classes.
- Trigger/scope: path rule: backend/**/*.cs, backend/**/*.csproj
- Exceptions: none
- Why EXTRA: Mapping technique not in the oracle.
- Evidence L0-S000301: `output/template/.claude/rules/2-technology/ef-core.md:14-14` — "- Entity mappings live in Infrastructure as `IEntityTypeConfiguration<T>` classes, keeping persistence configuration out of Domain entities where practical (prefer)."

### EXTRA-L0-0024
- Closest oracle policies: API-010, DEP-002
- Modality: DEFAULT
- Normative action: Follow the established validation invocation pattern rather than adding a competing mechanism; do not adopt deprecated/legacy ASP.NET automatic-validation integration packages without a concrete requirement.
- Trigger/scope: path rule: backend/**/*.cs
- Exceptions: Concrete project requirement.
- Why EXTRA: Not in the oracle.
- Evidence L0-S000309: `output/template/.claude/rules/2-technology/fluentvalidation.md:12-12` — "- Follow the project's established validation invocation pattern rather than adding a second competing mechanism; do not adopt a deprecated or legacy ASP.NET automatic-validation integration package unless a concrete project requirement justifies it (default)."
- Evidence L0-S000673: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:105-105` — "Register validators with `services.AddValidatorsFromAssemblyContaining<CreateOrderRequestValidator>()` (FluentValidation.DependencyInjectionExtensions) and invoke them through the project's one established mechanism (for example explicitly in the Application Service, or an action filter in Api)."

### EXTRA-L0-0025
- Closest oracle policies: WF-005, DEP-014
- Modality: MUST
- Normative action: Unit/component tests run with the workspace's configured runner; inspect package.json instead of assuming a command.
- Trigger/scope: path rule: frontend/**
- Exceptions: none
- Why EXTRA: Runner-discovery obligation not in the oracle.
- Evidence L0-S000250: `output/template/.claude/rules/2-technology/angular.md:18-18` — "- Unit and component tests run with the workspace's configured runner; inspect `package.json` instead of assuming a command (the baseline runner for new workspaces is recorded in `3-project/decisions.md`)."

### EXTRA-L0-0026
- Closest oracle policies: DEP-019, SEC-007
- Modality: DEFAULT
- Normative action: Run production containers as the image's non-root user where supported.
- Trigger/scope: path rule: Dockerfile*, .dockerignore, compose*.yml, .github/workflows/**, azure-pipelines*.yml, .gitlab-ci.yml
- Exceptions: Where supported.
- Why EXTRA: Not in DEP-019.
- Evidence L0-S000270: `output/template/.claude/rules/2-technology/containers-ci.md:20-20` — "- Production containers use an appropriate runtime image (the ASP.NET runtime image for ASP.NET Core applications) rather than the SDK image solely for convenience, and run as the image's non-root user where supported; do not switch to root merely to bypass filesystem-permission problems (default)."
- Evidence L0-S000966: `output/template/.claude/skills/docker/SKILL.md:49-49` — "`USER app` uses the built-in non-root user of modern .NET images. Make directories the application writes to owned and permitted correctly instead of switching to root."

### EXTRA-L0-0027
- Closest oracle policies: SEC-002
- Modality: MUST
- Normative action: Keep environment configuration external to container images.
- Trigger/scope: path rule: Dockerfile*, .dockerignore, compose*.yml, .github/workflows/**, azure-pipelines*.yml, .gitlab-ci.yml
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000271: `output/template/.claude/rules/2-technology/containers-ci.md:21-21` — "- Keep build tooling out of production runtime images and keep environment configuration external; real secrets never go into Dockerfiles, committed Compose files, or build arguments (`0-core/security-principles.md`)."
- Evidence L0-S000968: `output/template/.claude/skills/docker/SKILL.md:53-53` — "Pass environment-specific configuration at run time (`ASPNETCORE_ENVIRONMENT`, `ConnectionStrings__Default`, `Authentication__Authority`). Where secrets must never go is owned by `containers-ci.md`; remember that build arguments stay visible in image metadata and copied appsettings files ship inside the image, so supply secrets through the platform/container secret mechanism."

### EXTRA-L0-0028
- Closest oracle policies: ARC-001
- Modality: ENFORCED
- Normative action: The project hook rejects outward references (Domain → any layer, Application → Infrastructure/Api, Infrastructure → Api).
- Trigger/scope: path rule: *.slnx, backend/**/*.csproj, frontend/*/angular.json
- Exceptions: none
- Why EXTRA: Executable enforcement (captured also from manifest-checks.mjs).
- Evidence L0-S000368: `output/template/.claude/rules/3-project/layout.md:23-23` — "`ProjectReference` entries implement the Level 1 dependency direction; the project hook rejects outward references (Domain → any layer, Application → Infrastructure/Api, Infrastructure → Api)."

### EXTRA-L0-0029
- Closest oracle policies: DEP-024
- Modality: DEFAULT
- Normative action: Unit/component tests stay inside the workspace colocated by Angular convention; E2E tests, when adopted, live in frontend/<Name>.Web/e2e/.
- Trigger/scope: path rule: *.slnx, backend/**/*.csproj, frontend/*/angular.json
- Exceptions: none
- Why EXTRA: Test placement convention not in the oracle.
- Evidence L0-S000374: `output/template/.claude/rules/3-project/layout.md:38-38` — "The Angular workspace lives at `frontend/<Name>.Web/` and owns its `package.json`, `package-lock.json`, `angular.json`, tsconfig files, `src/`, and `public/`. Unit and component tests stay inside the workspace (colocated by Angular convention); E2E tests, when adopted, live in `frontend/<Name>.Web/e2e/`. Never place frontend tests under `backend/`."

### EXTRA-L0-0030
- Closest oracle policies: DEP-006
- Modality: DEFAULT
- Normative action: A VersionOverride needs a concrete reason and must be reported.
- Trigger/scope: path rule: *.csproj, Directory.Packages.props, Directory.Build.props, package.json, package-lock.json
- Exceptions: Concrete reason.
- Why EXTRA: Not in DEP-006.
- Evidence L0-S000380: `output/template/.claude/rules/3-project/package-management.md:18-18` — "- Use NuGet Central Package Management: package versions belong in `Directory.Packages.props`, and project `PackageReference` entries are versionless and scoped as `0-core/dependency-hygiene.md` requires (default: a `VersionOverride` needs a concrete reason and must be reported)."
- Evidence L0-S000525: `output/template/.claude/hooks/manifest-checks.mjs:286-288` — "if (metadata(item, 'VersionOverride') !== undefined) { ⏎       problems.push(`${location}: PackageReference '${id}' uses VersionOverride — report the concrete reason → ${OWNER.packageManagement}`); ⏎     }"

### EXTRA-L0-0042
- Closest oracle policies: DEP-005
- Modality: MUST_NOT
- Normative action: Do not make legal conclusions beyond what the published license supports.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Not in DEP-005.
- Evidence L0-S000564: `output/template/.claude/skills/add-dependency/SKILL.md:44-44` — "If no reasonable free alternative exists, say so. Do not make legal conclusions beyond what the published license supports."

### EXTRA-L0-0043
- Closest oracle policies: DEP-004
- Modality: MUST
- Normative action: Report package, version, license, reason and checks performed.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Report fields not in the oracle.
- Evidence L0-S000573: `output/template/.claude/skills/add-dependency/SKILL.md:59-59` — "Build and test the affected scope (`verify`); for security-relevant changes run `dotnet package list --vulnerable --include-transitive` or `npm audit`. Scanner output needs context — do not replace or upgrade unrelated packages merely because a scanner reports something. Report: package · version · license · reason · checks performed."

### EXTRA-L0-0044
- Closest oracle policies: DEP-006, WF-005
- Modality: MUST
- Normative action: Removing a dependency: remove the reference and its central version when no project uses it, rebuild and run affected tests.
- Trigger/scope: workflow add-dependency (adding, updating or removing NuGet/npm packages)
- Exceptions: none
- Why EXTRA: Removal procedure not in the oracle.
- Evidence L0-S000575: `output/template/.claude/skills/add-dependency/SKILL.md:63-63` — "Remove the reference (and its central version when no project uses it any more), rebuild, and run the affected tests."

### EXTRA-L0-0045
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: Delegated choices proceed and are mentioned in the report.
- Trigger/scope: workflow architecture-decision (Reserved or unclear decisions, answered Decision Requests, API version deprecation)
- Exceptions: none
- Why EXTRA: Reporting obligation for Delegated choices not in GOV-017.
- Evidence L0-S000641: `output/template/.claude/skills/architecture-decision/SKILL.md:17-19` — "1. State the choice in one sentence. ⏎ 2. Check whether it is already Decided: the product inputs, `1-architecture/overview.md`, `3-project/decisions.md`, the governing rule files, or the established project structure. ⏎ 3. Otherwise apply the Reserved list and the five-question test. Delegated → proceed and mention it in the report. Reserved → continue."

### EXTRA-L0-0046
- Closest oracle policies: GOV-017, DEP-002
- Modality: MUST
- Normative action: In the same change update the owning rule module at the right level so no rule contradicts an accepted decision (technology replacement edits the Level 2 module, Level 3 decisions and embedding workflows/assets).
- Trigger/scope: workflow architecture-decision (Reserved or unclear decisions, answered Decision Requests, API version deprecation)
- Exceptions: none
- Why EXTRA: Instruction-update obligation (repo/meta).
- Evidence L0-S000648: `output/template/.claude/skills/architecture-decision/SKILL.md:36-36` — "2. Update the owning rule module at the right level when the decision changes a rule (for example a technology replacement edits the Level 2 module, the Level 3 decisions, and any workflow or asset where the technology is embedded), so that no rule contradicts the decision."

### EXTRA-L0-0047
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: A rejected Decision Request is not recorded as a decision but mentioned in the report.
- Trigger/scope: workflow architecture-decision (Reserved or unclear decisions, answered Decision Requests, API version deprecation)
- Exceptions: none
- Why EXTRA: Not in GOV-017.
- Evidence L0-S000650: `output/template/.claude/skills/architecture-decision/SKILL.md:39-39` — "A rejected request is not recorded as a decision; mention it in the report."

### EXTRA-L0-0048
- Closest oracle policies: FE-002
- Modality: DEFAULT
- Normative action: Route/page components coordinate UI behaviour; reusable presentation components take explicit inputs and emit meaningful events.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: none
- Why EXTRA: Component-role convention not in the oracle.
- Evidence L0-S000585: `output/template/.claude/skills/angular/SKILL.md:55-55` — "Route-level/page components coordinate UI behavior; reusable presentation components take explicit inputs and emit meaningful events."

### EXTRA-L0-0049
- Closest oracle policies: FE-004
- Modality: AVOID
- Normative action: Use computed for derived state; avoid effect() when computed, a template binding or an event handler expresses the dependency more clearly.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: none
- Why EXTRA: Signals technique rule not in the oracle.
- Evidence L0-S000588: `output/template/.claude/skills/angular/SKILL.md:65-65` — "Use `computed` for derived state; avoid `effect()` when `computed`, a template binding, or an explicit event handler expresses the dependency more clearly."

### EXTRA-L0-0050
- Closest oracle policies: FE-010, API-010
- Modality: MUST_NOT
- Normative action: Keep request mapping explicit; duplicate a complex Domain rule in TypeScript only when the UI genuinely needs an equivalent user-facing rule.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: UI genuinely needs it.
- Why EXTRA: Not in the oracle.
- Evidence L0-S000598: `output/template/.claude/skills/angular/SKILL.md:100-100` — "Reactive forms give explicit state, validation, and testability for non-trivial forms. Keep request mapping explicit. Duplicate a complex Domain rule in TypeScript only when the UI genuinely needs an equivalent user-facing rule."

### EXTRA-L0-0051
- Closest oracle policies: DEP-014
- Modality: DEFAULT
- Normative action: When Angular Material is used, use it consistently for common UI primitives; do not wrap every Material component in a custom abstraction without a concrete reason.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: Material used.
- Why EXTRA: Not in the oracle.
- Evidence L0-S000605: `output/template/.claude/skills/angular/SKILL.md:122-122` — "When the project uses Angular Material, use its components consistently for common UI primitives; do not wrap every Material component in a custom abstraction without a concrete reason."

### EXTRA-L0-0052
- Closest oracle policies: TST-002
- Modality: DEFAULT
- Normative action: Frontend test targets: meaningful component behaviour, validation, request mapping, important route/auth behaviour, complex reactive state; E2E (Playwright when adopted) focuses on a small number of important workflows unless broader coverage is required.
- Trigger/scope: on-demand knowledge skill angular (frontend)
- Exceptions: none
- Why EXTRA: Test-targeting guidance not in the oracle.
- Evidence L0-S000609: `output/template/.claude/skills/angular/SKILL.md:130-130` — "Useful targets: meaningful component behavior, validation, data-access request mapping, important route/auth behavior, complex reactive state. Do not test framework internals or duplicate the same behavior at every level. E2E tests (Playwright, when adopted) focus on a small number of important user workflows unless broader coverage is required."

### EXTRA-L0-0053
- Closest oracle policies: API-016
- Modality: DEFAULT
- Normative action: Generate separate or clearly grouped Swagger documents per supported version when clients need them.
- Trigger/scope: on-demand knowledge skill api-versioning (backend)
- Exceptions: Clients need them.
- Why EXTRA: Not in the oracle.
- Evidence L0-S000631: `output/template/.claude/skills/api-versioning/SKILL.md:87-87` — "Generate separate or clearly grouped Swagger documents per supported version when clients need them (`swagger` skill); the documented version must match routing and controller metadata. Versions never override normal HTTP semantics (`http-api` skill)."

### EXTRA-L0-0054
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Test meaningful version differences (routing, shape, deprecated version still working, unsupported version, intended shared behaviour); do not duplicate identical tests per version.
- Trigger/scope: on-demand knowledge skill api-versioning (backend)
- Exceptions: none
- Why EXTRA: Version-test guidance not in the oracle.
- Evidence L0-S000633: `output/template/.claude/skills/api-versioning/SKILL.md:91-91` — "Test meaningful differences: version routing, version-specific response shape, a deprecated version still working during its support period, unsupported-version behavior, shared behavior consistent where intended. Do not duplicate identical tests per version."

### EXTRA-L0-0055
- Closest oracle policies: API-009, ARC-020
- Modality: MUST
- Normative action: If a Result pattern is deliberately adopted, use it consistently with typed errors rather than strings.
- Trigger/scope: on-demand knowledge skill aspnet-error-handling (backend)
- Exceptions: Result adopted.
- Why EXTRA: Not in the oracle.
- Evidence L0-S000663: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:63-63` — "For a command with several meaningful outcomes, an explicit typed outcome is often clearer. If the project deliberately adopts a Result pattern, use it consistently with typed errors rather than strings:"

### EXTRA-L0-0056
- Closest oracle policies: API-010, ARC-010
- Modality: AVOID
- Normative action: Avoid validation coupled to Minimal API endpoint filters in a Controller-based project.
- Trigger/scope: on-demand knowledge skill aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000680: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:135-135` — "Avoid inconsistent anonymous error objects and validation coupled to Minimal API endpoint filters in a Controller-based project."

### EXTRA-L0-0057
- Closest oracle policies: SEC-016, ARC-020
- Modality: DEFAULT
- Normative action: Bearer/OIDC for SPA→API, cookies for server-rendered apps, Identity for owned local accounts (not merely because an entity is called User), external OIDC/OAuth provider when identity is delegated.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: none
- Why EXTRA: Scheme-selection guidance not in the oracle.
- Evidence L0-S000686: `output/template/.claude/skills/authentication/SKILL.md:16-19` — "- Bearer/OIDC for an SPA calling an API; ⏎ - cookies for server-rendered interactive applications; ⏎ - ASP.NET Core Identity when the application owns local accounts, passwords, and needs account management — not merely because a business entity is called `User`; ⏎ - an external OpenID Connect/OAuth provider when identity is delegated — do not issue custom JWTs when that provider already issues to …"

### EXTRA-L0-0058
- Closest oracle policies: SEC-005
- Modality: PREFER
- Normative action: Prefer policies over trivial role checks; keep repeated policy names in stable constants; roles only for role-oriented models; no compound role strings or role/permission magic strings scattered through the code.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: none
- Why EXTRA: Authorization-modelling conventions not in the oracle.
- Evidence L0-S000698: `output/template/.claude/skills/authentication/SKILL.md:70-70` — "Prefer policies when authorization is more than a trivial role check, and keep policy names in stable constants when they repeat. Use roles when the business model is genuinely role-oriented; prefer one policy over compound role strings scattered through the code."
- Evidence L0-S000714: `output/template/.claude/skills/authentication/SKILL.md:113-113` — "Role/permission magic strings scattered through the codebase."

### EXTRA-L0-0059
- Closest oracle policies: API-005
- Modality: DEFAULT
- Normative action: The authentication/authorization middleware produces 401/403 (challenge/forbid) instead of controllers manufacturing them.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: none
- Why EXTRA: Mechanism preference not in API-005.
- Evidence L0-S000702: `output/template/.claude/skills/authentication/SKILL.md:78-78` — "The status semantics are owned by `entry-points.md`. In practice the authentication/authorization middleware produces 401 and 403 (challenge and forbid) instead of controllers manufacturing them."
- Evidence L0-S001139: `output/template/.claude/skills/http-api/SKILL.md:50-50` — "`401` means authentication is missing, invalid, or expired; authentication middleware normally produces it. The client generally cannot fix `403` by resending the same credentials."

### EXTRA-L0-0060
- Closest oracle policies: ARC-007
- Modality: DEFAULT
- Normative action: When use cases repeatedly need caller identity define a small Application abstraction implemented at an outer boundary; skip it when passing an explicit user identifier is simpler.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: Repeated need.
- Why EXTRA: Technique not in the oracle.
- Evidence L0-S000706: `output/template/.claude/skills/authentication/SKILL.md:91-91` — "When use cases repeatedly need the caller's identity, define a small Application abstraction and implement the HTTP adapter at an outer boundary, keeping `HttpContext`, `ClaimsPrincipal`, and `IHttpContextAccessor` in Api (transport types — `aspnet-core.md`):"
- Evidence L0-S000708: `output/template/.claude/skills/authentication/SKILL.md:101-101` — "Skip the abstraction when passing an explicit user identifier is simpler."

### EXTRA-L0-0061
- Closest oracle policies: TST-003, SEC-005
- Modality: DEFAULT
- Normative action: Authorization integration cases: unauthenticated→401, unauthorized→403, permitted success, ownership rules, intended anonymous endpoints reachable.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: none
- Why EXTRA: Required test cases not in the oracle.
- Evidence L0-S000712: `output/template/.claude/skills/authentication/SKILL.md:109-109` — "Integration cases: unauthenticated → 401; authenticated without permission → 403; permitted → success; resource ownership rules; intended anonymous endpoints stay reachable. Verify observable behavior, not just the presence of `[Authorize]`."

### EXTRA-L0-0062
- Closest oracle policies: ARC-024, RUN-007
- Modality: DEFAULT
- Normative action: Output caching belongs in Api when the entire response is reusable; Infrastructure adapters may cache expensive operations when the contract to Application is preserved.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Layer placement technique not in the oracle.
- Evidence L0-S000759: `output/template/.claude/skills/caching/SKILL.md:16-16` — "- **HTTP response caching** — ASP.NET Core output caching when the entire response can safely be reused; it belongs in Api."
- Evidence L0-S000761: `output/template/.claude/skills/caching/SKILL.md:18-18` — "- **Infrastructure caching** — adapters may cache expensive remote or persistence operations when the contract to Application is preserved."

### EXTRA-L0-0063
- Closest oracle policies: RUN-020
- Modality: PREFER
- Normative action: Centralize key construction when duplicated formats become hard to maintain.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000769: `output/template/.claude/skills/caching/SKILL.md:47-47` — "Include every dimension that affects the result: entity identifier, tenant, user when genuinely user-specific, locale, relevant query/filter parameters. Centralize key construction when duplicated formats become hard to maintain."

### EXTRA-L0-0064
- Closest oracle policies: RUN-007
- Modality: DEFAULT
- Normative action: Apply output-cache policies through controller/action metadata.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Technique not in the oracle.
- Evidence L0-S000774: `output/template/.claude/skills/caching/SKILL.md:66-66` — "Apply the policy through controller/action metadata (`[OutputCache(PolicyName = "ProductById")]`). Do not cache authenticated or user-specific responses unless the key and policy isolate users and authorization context."

### EXTRA-L0-0065
- Closest oracle policies: RUN-018
- Modality: MUST
- Normative action: Decide explicitly whether a cache failure falls back to the source, fails the request or returns stale data.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Explicit cache-failure policy not in the oracle.
- Evidence L0-S000776: `output/template/.claude/skills/caching/SKILL.md:70-70` — "Decide explicitly whether a cache failure falls back to the source, fails the request, or returns stale data."

### EXTRA-L0-0066
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Test caching when it affects correctness: invalidation after mutation, tenant/user isolation, miss fallback, outage behaviour.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: Caching affects observable correctness.
- Why EXTRA: Test obligations not in the oracle.
- Evidence L0-S000778: `output/template/.claude/skills/caching/SKILL.md:74-74` — "Test caching when it affects observable correctness: stale entries invalidated after a successful mutation, tenant/user keys isolated, a miss falls back correctly, an outage follows the intended failure policy. Do not unit-test framework cache internals."

### EXTRA-L0-0067
- Closest oracle policies: ARC-016, RUN-021
- Modality: MUST_NOT
- Normative action: Do not cache EF tracked entities across Unit of Work boundaries.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000780: `output/template/.claude/skills/caching/SKILL.md:78-78` — "Caching EF tracked entities across Unit of Work boundaries; Redis added merely because the application caches."

### EXTRA-L0-0068
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: Store or publish only the artifacts later stages need.
- Trigger/scope: on-demand knowledge skill ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000796: `output/template/.claude/skills/ci-cd/SKILL.md:71-71` — "Store or publish only the artifacts later stages need; promotion and deployment steps: `delivery-pipeline`."

### EXTRA-L0-0069
- Closest oracle policies: SEC-002
- Modality: PREFER
- Normative action: Prefer workload/federated identity (e.g. OIDC to the cloud) over long-lived deployment credentials when supported.
- Trigger/scope: on-demand knowledge skill ci-cd (delivery)
- Exceptions: Supported by the platform.
- Why EXTRA: Not in the oracle.
- Evidence L0-S000800: `output/template/.claude/skills/ci-cd/SKILL.md:79-79` — "Use the CI platform's secret store; prefer workload/federated identity (for example OIDC to the cloud provider) over long-lived deployment credentials when supported."
- Evidence L0-S000891: `output/template/.claude/skills/delivery-pipeline/SKILL.md:24-24` — "- Supply credentials through the CI platform's secret/identity mechanism (secrets policy: `0-core/security-principles.md`); prefer workload/federated identity over long-lived deployment credentials where supported."

### EXTRA-L0-0070
- Closest oracle policies: WF-017
- Modality: AVOID
- Normative action: Avoid rebuilding different source per environment without a reason.
- Trigger/scope: on-demand knowledge skill ci-cd (delivery)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000805: `output/template/.claude/skills/ci-cd/SKILL.md:91-91` — "Project-specific database infrastructure in a generic pipeline; rebuilding different source per environment without a reason; assuming Docker deployment."

### EXTRA-L0-0071
- Closest oracle policies: WF-012
- Modality: MUST_NOT
- Normative action: Do not apply backend project-boundary rules mechanically to Angular code.
- Trigger/scope: workflow code-review (reviews of completed changes; also the code-reviewer agent)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000823: `output/template/.claude/skills/code-review/SKILL.md:41-41` — "When Angular code is in scope, check `1-architecture/frontend-structure.md` and `2-technology/angular.md`: feature boundaries and component responsibility, HTTP calls behind data-access boundaries, subscription and reactive-state lifetime, frontend error handling, route guards not treated as authorization, unnecessary global/shared state, meaningful frontend tests. Do not apply backend project-bou …"

### EXTRA-L0-0072
- Closest oracle policies: WF-011
- Modality: MUST
- Normative action: Report findings ordered by severity with severity, file/location, problem, why it matters and smallest reasonable fix.
- Trigger/scope: workflow code-review (reviews of completed changes; also the code-reviewer agent)
- Exceptions: none
- Why EXTRA: Findings format not in the oracle.
- Evidence L0-S000835: `output/template/.claude/skills/code-review/SKILL.md:65-65` — "Report findings ordered by severity. For each: severity · file/location · problem · why it matters · smallest reasonable fix."

### EXTRA-L0-0073
- Closest oracle policies: WF-011
- Modality: DEFINITION
- Normative action: Review severity scale: Critical (blocks use/merge), High (fix before merge), Medium, Low.
- Trigger/scope: workflow code-review (reviews of completed changes; also the code-reviewer agent)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000836: `output/template/.claude/skills/code-review/SKILL.md:67-70` — "- **Critical** — data loss, security vulnerability, reliably broken core behavior; blocks use/merge. ⏎ - **High** — likely defect or architectural/data-integrity issue that should be fixed before merge. ⏎ - **Medium** — real maintainability, robustness, or test gap, not a likely immediate production failure. ⏎ - **Low** — non-blocking improvement."

### EXTRA-L0-0074
- Closest oracle policies: GOV-010, RUN-015
- Modality: MUST
- Normative action: Numbers in examples are illustrative, not approved defaults; choose retry counts, timeouts and limits from the actual integration and deployment.
- Trigger/scope: on-demand knowledge skill configuration (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000847: `output/template/.claude/skills/configuration/SKILL.md:40-40` — "Numbers in examples are illustrative, not approved defaults; choose retry counts, timeouts, and limits from the actual integration and deployment."
- Evidence L0-S001160: `output/template/.claude/skills/httpclient-factory/references/resilience.md:18-18` — "Distinguish the **attempt timeout** from the **total operation timeout**, especially with retries. Choose values from actual latency requirements, not from examples."
- Evidence L0-S001222: `output/template/.claude/skills/logging/references/serilog.md:49-49` — "An example `appsettings*.json` section. It deliberately shows several optional sinks; File, Seq, OpenTelemetry, and Elasticsearch are not baseline dependencies, and the numbers are illustrative, not approved defaults:"

### EXTRA-L0-0075
- Closest oracle policies: GOV-008
- Modality: MUST
- Normative action: Use a stable descriptive setting name and record value and purpose in the table.
- Trigger/scope: workflow custom-settings (adding, changing, removing or applying a CUSTOM_SETTINGS.md value)
- Exceptions: none
- Why EXTRA: Naming/recording convention not in the oracle.
- Evidence L0-S000870: `output/template/.claude/skills/custom-settings/SKILL.md:17-17` — "2. Use a stable descriptive setting name and record the value and its purpose in the table."

### EXTRA-L0-0076
- Closest oracle policies: GOV-021, RUN-009
- Modality: AVOID
- Normative action: Avoid duplicating the setting literal across layers when a normal single source in code or configuration is appropriate.
- Trigger/scope: workflow custom-settings (adding, changing, removing or applying a CUSTOM_SETTINGS.md value)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000874: `output/template/.claude/skills/custom-settings/SKILL.md:25-25` — "When a value is added, changed, or removed, update every affected implementation, validation, configuration, test, documentation, and mirrored frontend/backend surface — changing one literal alone does not establish synchronization. Avoid duplicating the literal across layers when a normal single source in code or configuration is appropriate. Backend validation stays authoritative; frontend valid …"

### EXTRA-L0-0077
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: Backend CI flow: dotnet restore → dotnet build --no-restore --configuration Release → dotnet test --no-build --configuration Release.
- Trigger/scope: workflow delivery-pipeline (CI/CD, Dockerfiles, Compose, deployment, production migrations)
- Exceptions: none
- Why EXTRA: Concrete command sequence not in the oracle.
- Evidence L0-S000888: `output/template/.claude/skills/delivery-pipeline/SKILL.md:21-21` — "- Backend flow: `dotnet restore` → `dotnet build --no-restore --configuration Release` → `dotnet test --no-build --configuration Release`. Run formatting/analyzer gates only when the project has adopted them as enforced checks."

### EXTRA-L0-0078
- Closest oracle policies: DEP-019, API-019
- Modality: DEFAULT
- Normative action: Container deployments use multi-stage builds, explicit project-file copy for restore caching, runtime configuration passed at run time and health probes per the health-check skill.
- Trigger/scope: workflow delivery-pipeline (CI/CD, Dockerfiles, Compose, deployment, production migrations)
- Exceptions: Container deployment.
- Why EXTRA: Not in the oracle.
- Evidence L0-S000894: `output/template/.claude/skills/delivery-pipeline/SKILL.md:29-29` — "When the project deploys containers, follow `containers-ci.md` and the `docker` skill: multi-stage build, explicit project-file copy for restore caching, runtime configuration passed at run time, health probes per the `health-check` skill. Build and publish images from CI only when container deployment is part of the project."

### EXTRA-L0-0079
- Closest oracle policies: WF-019
- Modality: MUST
- Normative action: The migration step runs at a controlled point and fails visibly on error.
- Trigger/scope: workflow delivery-pipeline (CI/CD, Dockerfiles, Compose, deployment, production migrations)
- Exceptions: none
- Why EXTRA: Not in WF-019.
- Evidence L0-S000897: `output/template/.claude/skills/delivery-pipeline/SKILL.md:34-34` — "- Production migration is an explicit deployment operation: a deliberate step at a controlled point, using the project's approved credentials, failing visibly on error. Migration scripts or bundles may be generated earlier in CI and executed during deployment."

### EXTRA-L0-0080
- Closest oracle policies: WF-017
- Modality: PREFER
- Normative action: CI and CD may be separate; a green build does not imply every branch deploys; use environment protection/approval where supported; promote the same tested artifact/image with runtime configuration differences.
- Trigger/scope: workflow delivery-pipeline (CI/CD, Dockerfiles, Compose, deployment, production migrations)
- Exceptions: none
- Why EXTRA: Deployment practices not in the oracle.
- Evidence L0-S000900: `output/template/.claude/skills/delivery-pipeline/SKILL.md:39-39` — "CI and CD may be separate workflows; a green CI build does not imply every branch deploys. Use environment protection/approval where the hosting platform supports it. Prefer promoting the same tested artifact or image through environments, with environment differences supplied by runtime configuration (prefer)."

### EXTRA-L0-0081
- Closest oracle policies: WF-017, SEC-001
- Modality: MUST
- Normative action: Confirm the pipeline restores cleanly, builds backend/frontend, runs configured tests, does not depend on developer state, exposes no secrets and produces expected artifacts; for containers build the image and verify startup, port/configuration, non-root, health probes and no secrets/stray files.
- Trigger/scope: workflow delivery-pipeline (CI/CD, Dockerfiles, Compose, deployment, production migrations)
- Exceptions: none
- Why EXTRA: Verification checklist not in the oracle.
- Evidence L0-S000902: `output/template/.claude/skills/delivery-pipeline/SKILL.md:43-43` — "Confirm the pipeline restores from a clean environment, builds the backend, builds the frontend when present, runs the configured tests, does not depend on developer-machine state, exposes no secrets, and produces the expected artifacts. For container changes: build the image, verify startup, port/configuration, non-root behavior when relevant, health-probe integration, and that no secrets or stra …"

### EXTRA-L0-0082
- Closest oracle policies: ARC-021, ARC-007
- Modality: DEFAULT
- Normative action: Use interface-to-implementation registration at architectural boundaries (Application services, repositories, adapters); concrete registration is fine for implementation-only helpers.
- Trigger/scope: on-demand knowledge skill dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Registration convention not in the oracle.
- Evidence L0-S000907: `output/template/.claude/skills/dependency-injection/SKILL.md:14-14` — "Use interface-to-implementation registration at architectural boundaries (Application services, repositories, external adapters); concrete registration is fine for implementation-only helpers. Prefer explicit registration in small applications; add scanning, keyed services, factories, or decorators when they solve an actual composition problem."

### EXTRA-L0-0083
- Closest oracle policies: ARC-021
- Modality: DEFAULT
- Normative action: Use keyed services when several implementations of one abstraction are selected by a known key and a single registration or simple factory is not clearer.
- Trigger/scope: on-demand knowledge skill dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Technique guidance not in the oracle.
- Evidence L0-S000911: `output/template/.claude/skills/dependency-injection/SKILL.md:50-50` — "Use when several implementations of one abstraction are selected by a known key and a single registration or a simple factory is not clearer:"

### EXTRA-L0-0084
- Closest oracle policies: ARC-023
- Modality: MUST
- Normative action: Scan the assembly that owns the services, not accidentally only the Api assembly.
- Trigger/scope: on-demand knowledge skill dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000918: `output/template/.claude/skills/dependency-injection/SKILL.md:89-89` — "Prefer explicit registrations in small and medium projects; scan when registration volume creates genuine boilerplate, and scan the assembly that owns the services (not accidentally only the Api assembly):"

### EXTRA-L0-0085
- Closest oracle policies: ARC-022, ARC-006
- Modality: MUST
- Normative action: Within that scope resolve a scoped orchestration service, not Infrastructure internals.
- Trigger/scope: on-demand knowledge skill dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000923: `output/template/.claude/skills/dependency-injection/SKILL.md:116-116` — "A singleton or hosted service that needs scoped work creates a scope per operation and resolves a scoped orchestration service — not Infrastructure internals:"

### EXTRA-L0-0086
- Closest oracle policies: TST-009
- Modality: MUST
- Normative action: The regression test fails before the fix and passes after it.
- Trigger/scope: workflow development-workflow (feature, bug fix, refactor, performance change, new application)
- Exceptions: none
- Why EXTRA: Not in TST-009.
- Evidence L0-S000946: `output/template/.claude/skills/development-workflow/SKILL.md:42-42` — "- **Bug fixes:** for a meaningful bug with plausible recurrence, add a regression test that fails before the fix and passes after it, unless equivalent coverage already exists (default)."

### EXTRA-L0-0087
- Closest oracle policies: ARC-019
- Modality: DEFAULT
- Normative action: Create schema changes as new EF Core migrations from the Infrastructure project with the Api project as startup project.
- Trigger/scope: workflow development-workflow (feature, bug fix, refactor, performance change, new application)
- Exceptions: none
- Why EXTRA: Migration command technique not in the oracle.
- Evidence L0-S000951: `output/template/.claude/skills/development-workflow/SKILL.md:49-49` — "- **Migrations:** create schema changes as new EF Core migrations from the Infrastructure project with the Api project as startup project, for example `dotnet ef migrations add <Name> --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api`. Treat migrations as source code: review each generated migration before committing it, paying particular attention to destructive schema  …"

### EXTRA-L0-0088
- Closest oracle policies: TST-002, TST-009
- Modality: MUST
- Normative action: Changed behaviour gets maintained automated coverage at the right level.
- Trigger/scope: workflow development-workflow (feature, bug fix, refactor, performance change, new application)
- Exceptions: none
- Why EXTRA: General test co-change obligation not in the oracle.
- Evidence L0-S000952: `output/template/.claude/skills/development-workflow/SKILL.md:50-50` — "- **Tests:** changed behavior gets maintained automated coverage at the right level (`0-core/testing-principles.md`)."

### EXTRA-L0-0089
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Report what changed, the verify result block and remaining known issues.
- Trigger/scope: workflow development-workflow (feature, bug fix, refactor, performance change, new application)
- Exceptions: none
- Why EXTRA: Report fields not in the oracle.
- Evidence L0-S000957: `output/template/.claude/skills/development-workflow/SKILL.md:59-59` — "Summarize what changed, the `verify` result block, unresolved Decision Requests, and remaining known issues."

### EXTRA-L0-0090
- Closest oracle policies: DEP-019
- Modality: DEFAULT
- Normative action: Copy only existing needed repository build files, copy project files explicitly before the source tree for restore caching, update when structure changes, avoid flattening wildcard tricks.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Dockerfile technique not in the oracle.
- Evidence L0-S000964: `output/template/.claude/skills/docker/SKILL.md:45-45` — "Copy only the repository-level build files that exist and are needed by restore. Copy project files explicitly before the source tree so source changes do not invalidate the NuGet restore layer; update this section when the solution structure changes. Avoid wildcard tricks that flatten or rearrange a multi-project tree. Workers without ASP.NET Core use the plain .NET runtime image."

### EXTRA-L0-0091
- Closest oracle policies: API-019
- Modality: PREFER
- Normative action: Expose liveness/readiness via ASP.NET Core health checks, prefer orchestrator HTTP probes, verify curl/wget/shell availability before in-container health commands and weigh adding debugging packages to production images.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Probe mechanics not in the oracle.
- Evidence L0-S000973: `output/template/.claude/skills/docker/SKILL.md:74-74` — "Expose liveness/readiness through ASP.NET Core health checks (`health-check` skill) and prefer the orchestrator's native HTTP probes. Runtime images may not contain `curl`, `wget`, or a shell — verify before using an in-container health command, and weigh adding debugging packages to a production image."

### EXTRA-L0-0092
- Closest oracle policies: DEP-018
- Modality: DEFAULT
- Normative action: Build Angular in a Node stage and serve output with the chosen hosting strategy (Nginx not mandatory); keep API base URLs compatible with the deployment.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000975: `output/template/.claude/skills/docker/SKILL.md:78-78` — "For static deployment build in a Node stage and serve the output with the chosen hosting strategy; Nginx is not mandatory when the platform hosts static files. Keep API base URLs compatible with the deployment."

### EXTRA-L0-0093
- Closest oracle policies: DEP-019
- Modality: MUST_NOT
- Normative action: Do not exclude tests the image build runs, or files restore/build needs, in .dockerignore.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000978: `output/template/.claude/skills/docker/SKILL.md:92-92` — "Do not exclude tests if the image build intentionally runs them, or files restore/build needs."

### EXTRA-L0-0094
- Closest oracle policies: RUN-008, DEP-019
- Modality: DEFAULT
- Normative action: Start with standard supported images; Alpine/chiseled/trimming/Native AOT only when compatibility and deployment requirements justify them, then verify globalization, native dependencies, reflection and diagnostics.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S000980: `output/template/.claude/skills/docker/SKILL.md:96-96` — "Start with standard supported images. Consider Alpine, chiseled images, trimming, or Native AOT only when compatibility and deployment requirements justify them, and verify globalization, native dependencies, reflection, and diagnostics afterwards."

### EXTRA-L0-0095
- Closest oracle policies: TST-011, TST-003
- Modality: DEFAULT
- Normative action: Test repositories/mappings only for meaningful behaviour (custom mappings, filters, projections, non-trivial queries, relationships, concurrency, provider behaviour), not one test per trivial Add/Get.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001003: `output/template/.claude/skills/dotnet-testing/SKILL.md:104-104` — "Test repositories or mappings when there is meaningful behavior: custom mappings, query filters, projections, non-trivial queries, relationships, concurrency, provider-specific behavior — not one test per trivial `Add`/`Get`."

### EXTRA-L0-0096
- Closest oracle policies: TST-005
- Modality: DEFAULT
- Normative action: Keep test data explicit and minimal; introduce builders/fixtures/factories only when repeated setup becomes hard to read.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001006: `output/template/.claude/skills/dotnet-testing/SKILL.md:113-113` — "For external dependencies use a fake/mock abstraction (unit tests), a stub `HttpMessageHandler`, WireMock or another local fake server, or a dedicated sandbox only when the test explicitly targets that integration; keep slow or unreliable external tests out of the fast run. Keep test data explicit and minimal; introduce builders, fixtures, or factories only when repeated setup becomes hard to read …"

### EXTRA-L0-0097
- Closest oracle policies: TST-005
- Modality: DEFINITION
- Normative action: 'Smoke test' means a small set of fast checks that a built/deployed application is basically operational; prefer explicit assertions over snapshots for small or important contracts.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001013: `output/template/.claude/skills/dotnet-testing/SKILL.md:131-131` — ""Smoke test" means a small set of fast checks that a built or deployed application is basically operational — not a synonym for every integration test. Snapshot testing can help for large stable outputs; do not add a snapshot library by default, and prefer explicit assertions for small or important contracts."

### EXTRA-L0-0098
- Closest oracle policies: TST-003
- Modality: AVOID
- Normative action: Avoid assertion-free tests unless the behaviour is 'does not throw'.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001015: `output/template/.claude/skills/dotnet-testing/SKILL.md:135-135` — "Mocking every class; assertion-free tests (unless the behavior is "does not throw"); `Task.Delay` to make timing tests pass; Testcontainers without a fidelity need."

### EXTRA-L0-0099
- Closest oracle policies: RUN-006
- Modality: DEFAULT
- Normative action: Use tracking queries when loaded entities are modified and committed through the current Unit of Work; AsNoTracking() for read-only entity queries; projections to DTOs need no AsNoTracking().
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Tracking technique (EXC-011 context) phrased as a directive; not in the oracle.
- Evidence L0-S001035: `output/template/.claude/skills/ef-core/SKILL.md:105-105` — "- Use tracking queries when loaded entities will be modified and committed through the current Unit of Work; use `AsNoTracking()` for read-only entity queries where tracking adds nothing. Projections to non-entity DTOs do not need `AsNoTracking()`."

### EXTRA-L0-0100
- Closest oracle policies: RUN-006
- Modality: PREFER
- Normative action: Prefer an explicit query shape (projection for selected related data, Include/ThenInclude when the graph is needed); consider split queries for large collection includes and verify the generated SQL.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Query-shape technique (EXC-011 context).
- Evidence L0-S001038: `output/template/.claude/skills/ef-core/SKILL.md:110-110` — "Prefer an explicit query shape: projection for selected related data, `Include`/`ThenInclude` when the graph itself is needed. Avoid lazy loading by default — it hides database access and invites N+1 queries. For large collection includes consider split queries and verify the generated SQL."

### EXTRA-L0-0101
- Closest oracle policies: RUN-006
- Modality: MUST
- Normative action: Paged queries need a deterministic order.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Stated in a code comment; not in the oracle.
- Evidence L0-S001041: `output/template/.claude/skills/ef-core/SKILL.md:117-117` — ".OrderByDescending(x => x.CreatedAt);       // paged queries need a deterministic order"

### EXTRA-L0-0102
- Closest oracle policies: RUN-021, ARC-016
- Modality: MUST_NOT
- Normative action: ExecuteUpdateAsync/ExecuteDeleteAsync bypass change tracking: do not mix them casually with tracked entities for the same rows; understand their transaction implications.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001046: `output/template/.claude/skills/ef-core/SKILL.md:138-138` — "`ExecuteUpdateAsync`/`ExecuteDeleteAsync` run directly against the database and bypass change tracking; do not mix them casually with tracked entities for the same rows, and understand their transaction implications."

### EXTRA-L0-0103
- Closest oracle policies: ARC-019
- Modality: MUST_NOT
- Normative action: Interceptors suit infrastructure cross-cutting behaviour such as auditing, not hidden business behaviour.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Interceptor technique (EXC-011 context) phrased as a restriction.
- Evidence L0-S001051: `output/template/.claude/skills/ef-core/SKILL.md:148-148` — "Interceptors suit infrastructure cross-cutting behavior such as auditing, not hidden business behavior:"

### EXTRA-L0-0104
- Closest oracle policies: GOV-004, PST-001
- Modality: MUST
- Normative action: When the required seed graph is complex, ask the task to describe the dataset instead of inventing a large generic graph.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: Complex graph.
- Why EXTRA: Not in the oracle.
- Evidence L0-S001056: `output/template/.claude/skills/ef-core/SKILL.md:216-216` — "A representative dataset typically includes, where applicable: newly created, active/in-progress, completed, inactive/archived entities; entities with and without optional values and relationships; representative status values; meaningful boundary states. When the required graph is complex, ask the task to describe the dataset instead of inventing a large generic graph. Which model changes require …"

### EXTRA-L0-0105
- Closest oracle policies: RUN-002
- Modality: MUST_NOT
- Normative action: Do not fire-and-forget EF Core async calls.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001065: `output/template/.claude/skills/ef-core/SKILL.md:237-237` — "Lazy loading by default; fire-and-forget EF async calls."

### EXTRA-L0-0106
- Closest oracle policies: WF-022
- Modality: PREFER
- Normative action: One logical change per commit; implementation and its protecting tests together; no artificial tiny commits or combined unrelated fixes.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: none
- Why EXTRA: Commit-granularity convention not in the oracle.
- Evidence L0-S001075: `output/template/.claude/skills/git-workflow/SKILL.md:22-22` — "- Prefer one logical change per commit; implementation and the tests that protect it normally belong together. Do not create artificial tiny commits or combine unrelated fixes."

### EXTRA-L0-0107
- Closest oracle policies: WF-022
- Modality: DEFAULT
- Normative action: Follow the repository's commit-message convention; otherwise Conventional Commits; use the body for motivation, constraints or migration notes.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001076: `output/template/.claude/skills/git-workflow/SKILL.md:23-23` — "- Follow the repository's commit-message convention; without one, Conventional Commits are a useful default (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`). Use the body for motivation, constraints, or migration notes that would otherwise be lost."

### EXTRA-L0-0108
- Closest oracle policies: GOV-016
- Modality: DEFAULT
- Normative action: Follow an existing branch-naming convention, otherwise prefixes such as feature/, fix/, refactor/; do not rename an existing user branch to satisfy a convention.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001078: `output/template/.claude/skills/git-workflow/SKILL.md:27-27` — "- Follow an existing branch-naming convention; otherwise prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, `chore/` with meaningful names are reasonable defaults. Do not rename an existing user branch to satisfy a convention."

### EXTRA-L0-0109
- Closest oracle policies: GOV-020
- Modality: MUST
- Normative action: Before pushing confirm the intended branch, understand working/staged state, ensure relevant verification completed and avoid pushing unrelated local commits.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: none
- Why EXTRA: Pre-push checklist not in the oracle.
- Evidence L0-S001082: `output/template/.claude/skills/git-workflow/SKILL.md:33-33` — "Before pushing: confirm the intended branch, understand the working/staged state, ensure relevant verification completed, and avoid pushing unrelated local commits. Never force-push a shared branch unless the user explicitly requests history rewriting and understands the consequences; treat `main`, `master`, and other protected/shared branches as non-rewritable."

### EXTRA-L0-0110
- Closest oracle policies: GOV-015
- Modality: MUST_NOT
- Normative action: Treat main, master and other protected/shared branches as non-rewritable.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001082: `output/template/.claude/skills/git-workflow/SKILL.md:33-33` — "Before pushing: confirm the intended branch, understand the working/staged state, ensure relevant verification completed, and avoid pushing unrelated local commits. Never force-push a shared branch unless the user explicitly requests history rewriting and understands the consequences; treat `main`, `master`, and other protected/shared branches as non-rewritable."

### EXTRA-L0-0111
- Closest oracle policies: GOV-020
- Modality: MUST
- Normative action: Merge vs rebase follows the repository/team convention or the user's explicit request; resolve conflicts from intended combined behaviour, not mechanical ours/theirs; run relevant verification afterwards.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001084: `output/template/.claude/skills/git-workflow/SKILL.md:37-37` — "Follow the repository/team convention or the user's explicit request rather than personal preference. Inspect local uncommitted work first; do not automatically stash, reset, or discard it. Resolve conflicts from the intended combined behavior, not by mechanically choosing "ours" or "theirs", and run relevant verification afterwards."

### EXTRA-L0-0112
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: A PR has a focused purpose; its description explains what changed, why, how it was verified and compatibility/migration notes.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001086: `output/template/.claude/skills/git-workflow/SKILL.md:41-41` — "Run `verify` before preparing a PR. A PR has a focused purpose; its description explains what changed, why, how it was verified, and compatibility/migration notes. Never claim checks that were not run."

### EXTRA-L0-0113
- Closest oracle policies: WF-009
- Modality: DEFAULT
- Normative action: Report the resulting Git state when useful (branch, commit, push target, PR status, remaining uncommitted changes).
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: When useful.
- Why EXTRA: Not in the oracle.
- Evidence L0-S001090: `output/template/.claude/skills/git-workflow/SKILL.md:49-49` — "Report the resulting state when useful: branch, commit created, push target, PR status, remaining uncommitted changes."

### EXTRA-L0-0114
- Closest oracle policies: API-018
- Modality: PREFER
- Normative action: Prefer provider/framework health-check integrations where suitable (e.g. AddDbContextCheck).
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: Where suitable.
- Why EXTRA: Not in the oracle.
- Evidence L0-S001106: `output/template/.claude/skills/health-check/SKILL.md:55-55` — "A database check performs a lightweight connectivity/availability check — no business queries, large scans, or writes; prefer provider/framework health-check integrations where suitable (for EF Core: `AddDbContextCheck<AppDbContext>()`). Check an external dependency only when its availability is part of what readiness means, and avoid cascades where A's readiness calls B's readiness calls C's."

### EXTRA-L0-0115
- Closest oracle policies: API-019
- Modality: MUST
- Normative action: Healthy → success, unhealthy → non-success (configurable); probe semantics are not business API semantics.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001108: `output/template/.claude/skills/health-check/SKILL.md:59-59` — "Healthy → success status, unhealthy → non-success, configurable through `HealthCheckOptions.ResultStatusCodes`; probe semantics are not business API semantics. Keep probe responses small. If detailed diagnostics are useful to operators, put them on a protected endpoint (network or authorization controls)."

### EXTRA-L0-0116
- Closest oracle policies: API-020
- Modality: DEFAULT
- Normative action: Choose probe exposure by topology (private network, management port, RequireHost, authorization where supported); prefer orchestrator HTTP probes.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Exposure mechanics not in the oracle.
- Evidence L0-S001110: `output/template/.claude/skills/health-check/SKILL.md:63-63` — "Probes are often reached by infrastructure without user authentication. Choose exposure by topology: private/internal network, a dedicated management port, host restrictions (`RequireHost`), or authorization where the probe infrastructure supports it. Prefer the orchestrator's native HTTP probes; container images may lack `curl`/`wget` (`docker` skill)."

### EXTRA-L0-0117
- Closest oracle policies: RUN-013
- Modality: AVOID
- Normative action: Avoid Error-level logs for every normal failed probe.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001112: `output/template/.claude/skills/health-check/SKILL.md:67-67` — "Probes run frequently: avoid expensive queries, long external timeouts, large allocations, full workflows, and Error-level logs for every normal failed probe."

### EXTRA-L0-0118
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: When deployment relies on the configuration test live response, readiness reacting to required dependencies, no sensitive leaks and optional dependency behaviour; do not test uncustomized framework behaviour.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: Deployment relies on it.
- Why EXTRA: Not in the oracle.
- Evidence L0-S001114: `output/template/.claude/skills/health-check/SKILL.md:71-71` — "When deployment relies on the configuration, test that the live endpoint responds, readiness changes with a required dependency, responses leak nothing sensitive, and optional dependencies behave as intended. Do not test framework behavior the application does not customize."

### EXTRA-L0-0119
- Closest oracle policies: API-018
- Modality: AVOID
- Normative action: Do not use health checks as a code-quality grading system.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001116: `output/template/.claude/skills/health-check/SKILL.md:75-75` — "Health checks as a code-quality grading system; remote dependency chains without operational justification."

### EXTRA-L0-0120
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: Keep status-code behaviour consistent across similar endpoints (e.g. one convention for repeated DELETE of an absent resource: 204 or 404).
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Consistency obligation not in the oracle.
- Evidence L0-S001120: `output/template/.claude/skills/http-api/SKILL.md:13-13` — "Policy owners: entry-point responsibilities, success/empty-collection/401/403/409/412 semantics, versioning, documentation truth → `.claude/rules/1-architecture/entry-points.md`; ProblemDetails types and Controllers → `2-technology/aspnet-core.md`; failure exposure → `0-core/security-principles.md`. This skill adds technique and the less-common cases. Keep status-code behavior consistent across si …"
- Evidence L0-S001125: `output/template/.claude/skills/http-api/SKILL.md:31-31` — "- 204 fits a successful `DELETE` or an update whose representation adds no value. For repeated `DELETE` of an absent resource choose one convention — 204 (desired state holds) or 404 (resource absent) — and use it consistently across equivalent resources."

### EXTRA-L0-0121
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: Return an operation identifier or Location for 202 when practical.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: When practical.
- Why EXTRA: Not in the oracle.
- Evidence L0-S001124: `output/template/.claude/skills/http-api/SKILL.md:30-30` — "- 202 fits long-running operations, background jobs, asynchronous imports, queued processing; return an operation identifier or a `Location` when practical."

### EXTRA-L0-0122
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: 304 only for conditional requests with a still-valid cached representation, not a business 'nothing changed'.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Less-common status semantics (EXC-009 context).
- Evidence L0-S001129: `output/template/.claude/skills/http-api/SKILL.md:38-38` — "| Conditional request; client's cached representation still valid (`If-None-Match`/ETag, `If-Modified-Since`) | `304` (no representation; not a business "nothing changed") |"

### EXTRA-L0-0123
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: 406 when no acceptable representation can be produced; 415 for an unsupported request media type.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Content-negotiation semantics (EXC-009 context).
- Evidence L0-S001131: `output/template/.claude/skills/http-api/SKILL.md:40-41` — "| Cannot produce a representation acceptable to the client's content negotiation | `406` | ⏎ | Request body media type not supported (e.g. XML to a JSON-only endpoint) | `415` |"

### EXTRA-L0-0124
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: 422 for structurally valid but semantically invalid requests, or 400 for both when the project deliberately uses it; follow the established convention.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: Established convention.
- Why EXTRA: Not in the oracle.
- Evidence L0-S001132: `output/template/.claude/skills/http-api/SKILL.md:42-42` — "| Structurally valid request with invalid semantics (e.g. `startDate > endDate`) | `422` — or `400` when the project deliberately uses 400 for both; follow the established convention |"

### EXTRA-L0-0125
- Closest oracle policies: API-006
- Modality: MUST
- Normative action: 428 when a contract-required precondition (e.g. If-Match) is absent.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Not in API-006.
- Evidence L0-S001133: `output/template/.claude/skills/http-api/SKILL.md:43-43` — "| Contract requires a precondition (e.g. `If-Match`) but it is absent | `428` |"

### EXTRA-L0-0126
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: 429 with Retry-After when known for rate-limited requests; never for validation failures.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001134: `output/template/.claude/skills/http-api/SKILL.md:44-44` — "| Rate limiting rejected the request | `429` + `Retry-After` when known (never for validation failures) |"

### EXTRA-L0-0127
- Closest oracle policies: API-003
- Modality: MUST_NOT
- Normative action: 502/504 only when acting as an intermediary (invalid upstream response / upstream timeout); do not convert every dependency failure to 502.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Gateway semantics (EXC-009 context).
- Evidence L0-S001136: `output/template/.claude/skills/http-api/SKILL.md:46-46` — "| Acting as intermediary; upstream returned an invalid/unusable response | `502` (do not convert every dependency failure to 502) |"
- Evidence L0-S001138: `output/template/.claude/skills/http-api/SKILL.md:48-48` — "| Acting as intermediary; upstream did not respond in time | `504` |"

### EXTRA-L0-0128
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: 503 with Retry-After when meaningful for temporary inability (maintenance, required dependency down, chosen overload semantics).
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001137: `output/template/.claude/skills/http-api/SKILL.md:47-47` — "| Temporarily unable to serve (maintenance, required dependency down, chosen overload semantics) | `503` + `Retry-After` when meaningful |"

### EXTRA-L0-0129
- Closest oracle policies: RUN-016, API-006
- Modality: DEFAULT
- Normative action: When a repeated POST must not duplicate effects consider an Idempotency-Key associated with request and result; a reused key with a materially different payload returns 409.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Idempotency-key convention not in the oracle.
- Evidence L0-S001144: `output/template/.claude/skills/http-api/SKILL.md:60-60` — "`GET` is safe and idempotent; `PUT` is idempotent; `DELETE` is idempotent in intended state; `POST` generally is not. When a repeated `POST` must not duplicate effects, consider an `Idempotency-Key` that the server associates with the request and its result; a reused key with a materially different payload → `409`. Do not claim idempotency merely because duplicates are unlikely."

### EXTRA-L0-0130
- Closest oracle policies: RUN-005
- Modality: DEFAULT
- Normative action: Named, typed and keyed clients are all valid; choose the simplest for the consumer and lifetime; keyed clients only when keyed DI is clearer; no single mandatory style.
- Trigger/scope: on-demand knowledge skill httpclient-factory (backend outbound HTTP)
- Exceptions: none
- Why EXTRA: Client-style guidance not in the oracle.
- Evidence L0-S001192: `output/template/.claude/skills/httpclient-factory/SKILL.md:34-34` — "Named, typed, and keyed clients are all valid; choose the simplest for the consumer and lifetime."
- Evidence L0-S001194: `output/template/.claude/skills/httpclient-factory/SKILL.md:46-46` — "Do not capture a transient typed client inside a singleton without understanding the lifetime implications. Choose keyed clients only when keyed DI makes consumption clearer."
- Evidence L0-S001213: `output/template/.claude/skills/httpclient-factory/SKILL.md:102-102` — "Making one client style mandatory everywhere; dynamic tokens in shared default headers; mapping every upstream failure to the same status; resilience pipelines added without understanding their behavior."

### EXTRA-L0-0131
- Closest oracle policies: ARC-025
- Modality: MUST_NOT
- Normative action: Use DelegatingHandler for genuine HTTP pipeline concerns (token acquisition, correlation, signing), never for business decisions.
- Trigger/scope: on-demand knowledge skill httpclient-factory (backend outbound HTTP)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001196: `output/template/.claude/skills/httpclient-factory/SKILL.md:50-50` — "Use `DelegatingHandler` for genuine HTTP pipeline concerns — access-token acquisition, correlation propagation, request signing — never for business decisions:"

### EXTRA-L0-0132
- Closest oracle policies: ARC-025
- Modality: MUST_NOT
- Normative action: Do not call EnsureSuccessStatusCode() blindly when specific statuses carry contract meaning.
- Trigger/scope: on-demand knowledge skill httpclient-factory (backend outbound HTTP)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001201: `output/template/.claude/skills/httpclient-factory/SKILL.md:71-71` — "Translate remote responses into the abstraction Application consumes. Do not call `EnsureSuccessStatusCode()` blindly when specific statuses carry contract meaning:"

### EXTRA-L0-0133
- Closest oracle policies: API-003, ARC-025
- Modality: MUST_NOT
- Normative action: Do not pass every upstream status through to the own API or map every upstream failure to the same status; outbound retry and inbound response are separate decisions.
- Trigger/scope: on-demand knowledge skill httpclient-factory (backend outbound HTTP)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001203: `output/template/.claude/skills/httpclient-factory/SKILL.md:80-80` — "For richer failure semantics translate into explicit Infrastructure/Application outcomes; do not pass every upstream status through to your own API. The outbound retry behavior and the inbound response your API returns are separate decisions."
- Evidence L0-S001213: `output/template/.claude/skills/httpclient-factory/SKILL.md:102-102` — "Making one client style mandatory everywhere; dynamic tokens in shared default headers; mapping every upstream failure to the same status; resilience pipelines added without understanding their behavior."

### EXTRA-L0-0134
- Closest oracle policies: RUN-005
- Modality: MUST_NOT
- Normative action: Configure stable headers on the client; apply per-request values per request or via a handler; never mutate shared DefaultRequestHeaders concurrently.
- Trigger/scope: on-demand knowledge skill httpclient-factory (backend outbound HTTP)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001207: `output/template/.claude/skills/httpclient-factory/SKILL.md:88-88` — "Configure stable headers (media types) on the client; apply per-request values such as dynamic tokens per request or through a handler — never mutate shared `DefaultRequestHeaders` concurrently. Prefer `System.Net.Http.Json` / `System.Text.Json`, with explicit options when the remote contract differs; do not reuse Domain entities as remote contracts to avoid mapping."
- Evidence L0-S001213: `output/template/.claude/skills/httpclient-factory/SKILL.md:102-102` — "Making one client style mandatory everywhere; dynamic tokens in shared default headers; mapping every upstream failure to the same status; resilience pipelines added without understanding their behavior."

### EXTRA-L0-0135
- Closest oracle policies: ARC-025, ARC-002
- Modality: MUST_NOT
- Normative action: Prefer System.Net.Http.Json/System.Text.Json with explicit options when the remote contract differs; do not reuse Domain entities as remote contracts to avoid mapping.
- Trigger/scope: on-demand knowledge skill httpclient-factory (backend outbound HTTP)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001207: `output/template/.claude/skills/httpclient-factory/SKILL.md:88-88` — "Configure stable headers (media types) on the client; apply per-request values such as dynamic tokens per request or through a handler — never mutate shared `DefaultRequestHeaders` concurrently. Prefer `System.Net.Http.Json` / `System.Text.Json`, with explicit options when the remote contract differs; do not reuse Domain entities as remote contracts to avoid mapping."

### EXTRA-L0-0136
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Test adapters with a controlled HttpMessageHandler verifying method/path, headers, payload, mapping and cancellation/failure behaviour.
- Trigger/scope: on-demand knowledge skill httpclient-factory (backend outbound HTTP)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001209: `output/template/.claude/skills/httpclient-factory/SKILL.md:92-92` — "A controlled `HttpMessageHandler` verifies method/path, headers, payload, response mapping, and cancellation/failure behavior:"

### EXTRA-L0-0137
- Closest oracle policies: RUN-016
- Modality: MUST_NOT
- Normative action: Transient candidates: selected network failures, temporary unavailability, rate limiting when allowed, transient provider database failures; never retry validation errors, auth failures, permanent 404s or deterministic business rejections.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: Explicit categories beyond RUN-016.
- Evidence L0-S001162: `output/template/.claude/skills/httpclient-factory/references/resilience.md:22-22` — "Plausibly transient: selected network failures, temporary unavailability, rate limiting when retry is allowed, transient provider-specific database failures. Not retried: validation errors, authentication/authorization failures, permanent 404 outcomes, deterministic business rejections, non-idempotent operations without duplicate prevention."

### EXTRA-L0-0138
- Closest oracle policies: RUN-016
- Modality: MUST_NOT
- Normative action: Do not invent a client-side Idempotency-Key the service does not honour.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: Not in RUN-016.
- Evidence L0-S001163: `output/template/.claude/skills/httpclient-factory/references/resilience.md:24-24` — "Before retrying a write, ask: *if the first attempt succeeded remotely but the response was lost, what happens when we send it again?* If the answer is "a duplicate side effect", automatic retry is unsafe. Use an idempotency mechanism the remote API actually supports; do not invent a client-side `Idempotency-Key` the service does not honor."

### EXTRA-L0-0139
- Closest oracle policies: RUN-015
- Modality: DEFAULT
- Normative action: Use a circuit breaker only for meaningful repeated-failure patterns that add load/latency; give it operational visibility when it matters in production.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: Circuit-breaker technique (EXC-007 context).
- Evidence L0-S001166: `output/template/.claude/skills/httpclient-factory/references/resilience.md:30-30` — "Use one when repeated calls to a failing dependency would add load or latency; skip it when there is no meaningful repeated-failure pattern. Give it operational visibility when it matters in production."
- Evidence L0-S001180: `output/template/.claude/skills/httpclient-factory/references/resilience.md:58-58` — "Retrying every exception or status; circuit breakers without a failure scenario; hedged writes; stacked handlers with overlapping strategies."

### EXTRA-L0-0140
- Closest oracle policies: RUN-016
- Modality: MUST_NOT
- Normative action: Do not wrap EF Core operations in a generic application retry pipeline; prefer the provider execution strategy (EnableRetryOnFailure) and its transaction guidance; an HTTP retry policy is not a database policy.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: Database resilience technique (EXC-007 context).
- Evidence L0-S001172: `output/template/.claude/skills/httpclient-factory/references/resilience.md:42-42` — "Do not wrap normal EF Core operations in a generic application-level retry pipeline. Prefer the provider's EF Core execution strategy (for SQL Server, `options.UseSqlServer(cs, sql => sql.EnableRetryOnFailure())`) and follow the provider guidance for transaction/retry interaction. An HTTP retry policy is not a database policy."

### EXTRA-L0-0141
- Closest oracle policies: RUN-016
- Modality: DEFAULT
- Normative action: Publish retries may duplicate delivery; use idempotent consumers, broker deduplication or an outbox when the business requires it; retries do not give exactly-once delivery.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: Business requires it.
- Why EXTRA: Not in the oracle.
- Evidence L0-S001174: `output/template/.claude/skills/httpclient-factory/references/resilience.md:46-46` — "A publish retry may duplicate delivery. Use idempotent consumers, broker deduplication, an outbox, or similar mechanisms when the business requires it; a retry policy does not provide exactly-once delivery."

### EXTRA-L0-0142
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: Inbound rate limiting is separate from outbound resilience; rejected requests get 429 with Retry-After when known.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001176: `output/template/.claude/skills/httpclient-factory/references/resilience.md:50-50` — "ASP.NET Core rate limiting protects this API from excessive incoming traffic and is separate from outbound resilience; rejected requests get `429` with `Retry-After` when known (`http-api` skill)."

### EXTRA-L0-0143
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Observe retry counts, timeouts, circuit state, rate-limit rejections and dependency latency when operationally relevant, using the adopted telemetry stack.
- Trigger/scope: private reference of on-demand skill httpclient-factory (resilience)
- Exceptions: When operationally relevant.
- Why EXTRA: Not in the oracle.
- Evidence L0-S001178: `output/template/.claude/skills/httpclient-factory/references/resilience.md:54-54` — "Observe retry counts, timeout frequency, circuit state, rate-limit rejections, and dependency latency when they matter operationally, using the telemetry stack the project adopted; resilience alone does not require OpenTelemetry."

### EXTRA-L0-0144
- Closest oracle policies: RUN-013
- Modality: DEFAULT
- Normative action: Choose levels by operational meaning: Trace/Debug diagnostics, Information for meaningful events (not every method call), Warning for recovered/degraded conditions, Error for failures needing attention, Critical when the application cannot continue safely.
- Trigger/scope: on-demand knowledge skill logging (backend)
- Exceptions: none
- Why EXTRA: Level semantics not in the oracle.
- Evidence L0-S001249: `output/template/.claude/skills/logging/SKILL.md:30-36` — "Choose levels by operational meaning: ⏎  ⏎ - **Trace / Debug** — detailed troubleshooting diagnostics (not a safe place for sensitive data). ⏎ - **Information** — normal meaningful events: a background job completed, an important business operation completed, a lifecycle event. Do not log every method call. ⏎ - **Warning** — an unexpected or degraded condition the application recovered from: fallb …"

### EXTRA-L0-0145
- Closest oracle policies: RUN-013
- Modality: PREFER
- Normative action: Prefer platform/runtime trace identifiers; add explicit correlation identifiers only for an integration or operational requirement; propagate tracing context across outbound calls with the chosen infrastructure.
- Trigger/scope: on-demand knowledge skill logging (backend)
- Exceptions: none
- Why EXTRA: Correlation technique (EXC-013 context) phrased as guidance.
- Evidence L0-S001256: `output/template/.claude/skills/logging/SKILL.md:55-55` — "Prefer the platform/runtime trace identifiers when they already provide adequate request correlation. Add an explicit correlation identifier only for an integration or operational requirement; validate or normalize identifiers accepted from external clients before propagating them; propagate tracing context across outbound calls with the project's chosen tracing or HTTP infrastructure."

### EXTRA-L0-0146
- Closest oracle policies: RUN-013
- Modality: AVOID
- Normative action: Do not use logs as an audit database without an adopted audit design.
- Trigger/scope: on-demand knowledge skill logging (backend)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001264: `output/template/.claude/skills/logging/SKILL.md:79-79` — "Logging expected business outcomes as errors; logs used as an audit database without an adopted audit design."

### EXTRA-L0-0147
- Closest oracle policies: DEP-021
- Modality: DEFAULT
- Normative action: Use two-stage (bootstrap logger) initialization when startup logging matters; simpler applications may use host-managed setup.
- Trigger/scope: private reference of on-demand skill logging (Serilog)
- Exceptions: Startup logging matters.
- Why EXTRA: Not in the oracle.
- Evidence L0-S001218: `output/template/.claude/skills/logging/references/serilog.md:9-9` — "Use two-stage initialization when startup logging matters: a bootstrap logger captures failures before DI/configuration is available. Simpler applications may use host-managed setup without bootstrap logging."

### EXTRA-L0-0148
- Closest oracle policies: DEP-021
- Modality: MUST
- Normative action: When the static/bootstrap Log.Logger is used, flush it on shutdown; with purely host-managed logging follow the provider lifetime instead of static lifecycle code.
- Trigger/scope: private reference of on-demand skill logging (Serilog)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001220: `output/template/.claude/skills/logging/references/serilog.md:45-45` — "When the static/bootstrap `Log.Logger` is used, flush it on shutdown (as above) so buffered events — especially from async sinks such as Seq or OTLP — are written. With purely host-managed logging, follow the provider's lifetime instead of adding static lifecycle code."

### EXTRA-L0-0149
- Closest oracle policies: DEP-008, ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Changing LangVersion or the target framework is Reserved.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: DEP-008 requires approval only for preview/RC moves.
- Evidence L0-S001270: `output/template/.claude/skills/modern-csharp/SKILL.md:12-12` — "Policy owners: follow repository conventions and `.editorconfig`, no mechanical modernization, no style-only rewrites → `.claude/rules/2-technology/csharp.md`; changing `LangVersion` or the target framework → Reserved (CLAUDE.md); measured optimization → `0-core/runtime-principles.md`. Use a feature when it makes code clearer, safer, or simpler. This skill is technique only."

### EXTRA-L0-0150
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: Prefer a regular constructor when validation/initialization is non-trivial, explicit fields read better, the codebase uses that style or parameter capture would obscure the class.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Constructor technique not in the oracle.
- Evidence L0-S001273: `output/template/.claude/skills/modern-csharp/SKILL.md:22-22` — "Prefer a regular constructor when validation or initialization is non-trivial, explicit fields read better, the codebase uses that style consistently, or parameter capture would obscure the class."

### EXTRA-L0-0151
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Collection expressions when the target type is clear; required when initialization is part of the construction contract (not a substitute for validation); avoid deeply nested patterns; field keyword to remove trivial backing fields.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Language-feature technique not in the oracle.
- Evidence L0-S001276: `output/template/.claude/skills/modern-csharp/SKILL.md:31-31` — "Use them when the target type is clear."
- Evidence L0-S001281: `output/template/.claude/skills/modern-csharp/SKILL.md:43-43` — "Use `required` when initialization is part of the type's valid construction contract — not as a substitute for constructor or domain validation that protects invariants."
- Evidence L0-S001284: `output/template/.claude/skills/modern-csharp/SKILL.md:56-56` — "Avoid deeply nested patterns that are harder to read than plain conditions."
- Evidence L0-S001287: `output/template/.claude/skills/modern-csharp/SKILL.md:70-70` — "Use it to remove an otherwise trivial backing field; keep manual backing fields that already contain clear or substantial logic."

### EXTRA-L0-0152
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Records for intentional value semantics (immutable DTOs, Value Objects, messages); identity/lifecycle entities normally stay classes.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001278: `output/template/.claude/skills/modern-csharp/SKILL.md:35-35` — "Records fit intentional value semantics: immutable transport DTOs, genuine Value Objects, immutable messages. Entities with identity and lifecycle normally stay classes; classes also fit when inheritance or framework behavior makes class semantics clearer. Avoid `record struct` merely to avoid allocations."

### EXTRA-L0-0153
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: var when the type is obvious or unimportant; keep implementation details non-public; sealed when deliberately not designed for inheritance (not as a speculative JIT optimization); follow the private-field naming convention.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001295: `output/template/.claude/skills/modern-csharp/SKILL.md:100-100` — "Use `var` when the type is obvious from the right-hand side or unimportant; use an explicit type when it helps. Keep implementation details non-public when they are not part of the project's public API. Use `sealed` when a type is deliberately not designed for inheritance and the modifier communicates intent — not as a speculative JIT optimization. Follow the repository's established private-field …"

### EXTRA-L0-0154
- Closest oracle policies: RUN-024
- Modality: DEFAULT
- Normative action: PascalCase for types/methods/properties/public members, camelCase for parameters/locals, meaningful names; small private/nested supporting types may stay with their owner.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Naming conventions beyond RUN-024.
- Evidence L0-S001297: `output/template/.claude/skills/modern-csharp/SKILL.md:104-104` — "Standard .NET naming: PascalCase for types, methods, properties, and public members; camelCase for parameters and locals; meaningful names over abbreviations (the template's `.editorconfig` reports these as suggestions). Small private or nested supporting types may stay with their owning type when that improves locality. Do not reorganize an existing file merely to satisfy a preferred member order …"

### EXTRA-L0-0155
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: Prefer immutability when it represents the model naturally; do not force it where controlled mutation is simpler.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001299: `output/template/.claude/skills/modern-csharp/SKILL.md:108-108` — "Prefer immutability when it represents the model naturally; do not force it onto framework models or workflows where controlled mutation is simpler."

### EXTRA-L0-0156
- Closest oracle policies: RUN-009
- Modality: MUST
- Normative action: Confirm the configured language version supports a feature before using it.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001303: `output/template/.claude/skills/modern-csharp/SKILL.md:116-116` — "Confirm the configured language version supports a feature before using it."

### EXTRA-L0-0157
- Closest oracle policies: DEP-008, DEP-023
- Modality: DEFAULT
- Normative action: Scaffold a global.json pinning the intended SDK line with a rollForward policy that allows normal patch/feature-band servicing.
- Trigger/scope: workflow project-structure (solution creation, projects, references, repository layout)
- Exceptions: none
- Why EXTRA: SDK pinning file not in the oracle.
- Evidence L0-S001343: `output/template/.claude/skills/project-structure/references/solution-layout.md:54-54` — "- `global.json` — pins the intended SDK line, for example:"
- Evidence L0-S001345: `output/template/.claude/skills/project-structure/references/solution-layout.md:65-65` — "Select the current stable SDK of the target release at scaffolding time (the version above is illustrative; preview/RC lines: `.claude/rules/3-project/decisions.md`) and choose a `rollForward` policy that allows normal patch/feature-band servicing."
- Evidence L0-S001362: `output/template/.claude/skills/project-structure/SKILL.md:34-34` — "Create only the required top-level directories and repository files (`references/solution-layout.md`): the solution (`dotnet new sln -n <Name>` creates `<Name>.slnx` with the .NET 10 SDK), `global.json` (SDK selection in `references/solution-layout.md`), and the template's `Directory.Build.props`, `Directory.Packages.props`, `.editorconfig`, `.gitignore`."

### EXTRA-L0-0158
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Include the hook's reference-change and outward-reference reports in the scaffolding report.
- Trigger/scope: workflow project-structure (solution creation, projects, references, repository layout)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001367: `output/template/.claude/skills/project-structure/SKILL.md:50-50` — "Add only the references `layout.md` maps from the Level 1 dependency direction, as `<ProjectReference>` items in the project files (for example `<ProjectReference Include="..\<Name>.Domain\<Name>.Domain.csproj" />` in `<Name>.Application.csproj`). Never add an outward reference to make compilation easier. The project hook blocks `dotnet add/remove … reference` and `dotnet reference add/remove` (re …"

### EXTRA-L0-0159
- Closest oracle policies: TST-006
- Modality: DEFAULT
- Normative action: Expose Program to WebApplicationFactory<Program> (e.g. public partial class Program;) when top-level statements make it inaccessible.
- Trigger/scope: workflow project-structure (solution creation, projects, references, repository layout)
- Exceptions: none
- Why EXTRA: Technique not in the oracle.
- Evidence L0-S001371: `output/template/.claude/skills/project-structure/SKILL.md:58-58` — "Create the useful NUnit test projects from `layout.md` → Test projects (optional ones only under its conditions), for example `dotnet new nunit -n <Name>.Application.Tests -o backend/<Name>.Application.Tests`, with the narrow references listed there. Expose `Program` to `WebApplicationFactory<Program>` when top-level statements make it inaccessible (for example `public partial class Program;`)."

### EXTRA-L0-0160
- Closest oracle policies: WF-006
- Modality: MUST
- Normative action: The launch profile's URLs agree with the configured HTTP/HTTPS ports.
- Trigger/scope: workflow project-structure (solution creation, projects, references, repository layout)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001377: `output/template/.claude/skills/project-structure/SKILL.md:70-70` — "For SQL Server projects create `appsettings.json` and `appsettings.Development.json` as `data-lifecycle.md` describes, and wire Development seeding per that rule. Configure Swagger UI for Development (`aspnet-core.md`) and a launch profile whose URLs agree with the configured HTTP/HTTPS ports. Never add Production credentials or Production migration automation."

### EXTRA-L0-0161
- Closest oracle policies: ARC-027, DEP-024
- Modality: DEFAULT
- Normative action: Scaffold backend folders by role: Application Abstractions/Persistence, Abstractions/ExternalServices (only when needed), Services, DTOs (not a dumping ground), Validation, DependencyInjection.cs; Api Controllers, Contracts/Requests|Responses, Middleware, Extensions (cohesive composition only), Program.cs, appsettings.
- Trigger/scope: private reference of workflow project-structure (backend placement)
- Exceptions: Only when needed.
- Why EXTRA: Directory layout convention not in the oracle.
- Evidence L0-S001313: `output/template/.claude/skills/project-structure/references/backend-layout.md:19-28` — "```text ⏎ backend/<Name>.Application/ ⏎ ├── Abstractions/ ⏎ │   ├── Persistence/          # ITaskRepository.cs, IOrderRepository.cs, IUnitOfWork.cs ⏎ │   └── ExternalServices/     # IEmailSender.cs, ICurrentUser.cs, IFileStorage.cs — only when needed ⏎ ├── Services/                 # ITaskService.cs, TaskService.cs ⏎ ├── DTOs/                     # operation/data models when useful — not a dumping …"
- Evidence L0-S001321: `output/template/.claude/skills/project-structure/references/backend-layout.md:65-76` — "```text ⏎ backend/<Name>.Api/ ⏎ ├── Controllers/ ⏎ ├── Contracts/ ⏎ │   ├── Requests/ ⏎ │   └── Responses/ ⏎ ├── Middleware/               # only when custom middleware exists ⏎ ├── Extensions/               # cohesive composition extensions only ⏎ ├── Program.cs ⏎ ├── appsettings.json ⏎ └── appsettings.Development.json ⏎ ```"

### EXTRA-L0-0162
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Make supporting-type roles clear by name/directory using established suffixes (Service, Dto, Request/Response — HTTP contracts belong to Api, Result/Outcome, Validator, Rules/Policy, Factory/Mapper/Adapter); prefer unambiguous names; responsibility subdirectories only when a flat directory is hard to navigate.
- Trigger/scope: private reference of workflow project-structure (backend placement)
- Exceptions: none
- Why EXTRA: Naming heuristics not in the oracle.
- Evidence L0-S001315: `output/template/.claude/skills/project-structure/references/backend-layout.md:32-40` — "Make each supporting type's responsibility clear from its name, its directory, or both. Established suffixes: ⏎  ⏎ - `Service` — use-case orchestration; ⏎ - `Dto` — data-transfer model; ⏎ - `Request` / `Response` — Application operation contracts (HTTP-specific contracts belong to Api); ⏎ - `Result` / `Outcome` — operation results; ⏎ - `Validator` — validation; ⏎ - `Rules` / `Policy` — decision or …"
- Evidence L0-S001316: `output/template/.claude/skills/project-structure/references/backend-layout.md:42-42` — "Prefer `TaskWorkflowRules`, `TaskWorkflowPolicy`, or `TaskWorkflowService` over an ambiguous `TaskWorkflow`. Introduce responsibility subdirectories only when a feature accumulates enough heterogeneous types that a flat directory is hard to navigate; avoid generic `Models`, `Helpers`, `Common`, `Utils` buckets."

### EXTRA-L0-0163
- Closest oracle policies: ARC-027
- Modality: DEFAULT
- Normative action: Create capability-specific subdirectories under Infrastructure Services/ when they improve cohesion.
- Trigger/scope: private reference of workflow project-structure (backend placement)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001319: `output/template/.claude/skills/project-structure/references/backend-layout.md:61-61` — "`AddInfrastructure` registers `AppDbContext`, repository implementations, `IUnitOfWork`, external adapters, the SQL Server provider, `HttpClient` integrations, and resilience handlers when used. Create capability-specific subdirectories under `Services/` when they improve cohesion."

### EXTRA-L0-0164
- Closest oracle policies: ARC-012
- Modality: MUST_NOT
- Normative action: Do not move arbitrary code out of Program.cs only to make it shorter.
- Trigger/scope: private reference of workflow project-structure (backend placement)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001324: `output/template/.claude/skills/project-structure/references/backend-layout.md:85-85` — "Use `Contracts/` only when transport-specific contracts provide a concrete boundary benefit. Do not move arbitrary code out of `Program.cs` only to make it shorter."

### EXTRA-L0-0165
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: Keep deterministic formatting/code style in .editorconfig; prefer enforceable tooling configuration over restating mechanical formatting in instructions.
- Trigger/scope: private reference of workflow project-structure (repository layout)
- Exceptions: none
- Why EXTRA: Instruction-design preference (repo/meta).
- Evidence L0-S001347: `output/template/.claude/skills/project-structure/references/solution-layout.md:69-69` — "Deterministic repository-wide formatting and code-style configuration lives here; prefer enforceable tooling configuration over restating mechanical formatting in instructions."

### EXTRA-L0-0166
- Closest oracle policies: SEC-001
- Modality: DEFAULT
- Normative action: Ignore generated/local artifacts (bin, obj, .vs, node_modules, dist, TestResults, coverage, local secret/config overrides, .claude/settings.local.json).
- Trigger/scope: private reference of workflow project-structure (repository layout)
- Exceptions: none
- Why EXTRA: Ignore-file convention not in the oracle.
- Evidence L0-S001349: `output/template/.claude/skills/project-structure/references/solution-layout.md:73-73` — "Ignore generated/local artifacts: `bin/`, `obj/`, `.vs/`, `node_modules/`, `dist/`, `TestResults/`, `coverage/`, local secret/config overrides, `.claude/settings.local.json`. Do not ignore files that are part of the Development configuration contract (for example a non-secret `appsettings.Development.json`)."
- Evidence L0-S001602: `output/template/.gitignore:2-11` — "bin/ ⏎ obj/ ⏎ .vs/ ⏎ *.user ⏎ TestResults/ ⏎ coverage/ ⏎ node_modules/ ⏎ dist/ ⏎ .angular/ ⏎ artifacts/"
- Evidence L0-S001605: `output/template/.gitignore:20-20` — ".claude/settings.local.json"

### EXTRA-L0-0167
- Closest oracle policies: WF-020, WF-009
- Modality: MUST
- Normative action: State in every report that static review cannot prove the application secure and may miss runtime, infrastructure, business-logic, authorization-bypass, deployment and dynamic-exploitation issues.
- Trigger/scope: workflow security-scan (security scan, audit, targeted security review)
- Exceptions: none
- Why EXTRA: Limitation statement not in the oracle.
- Evidence L0-S001447: `output/template/.claude/skills/security-scan/SKILL.md:12-12` — "Perform an evidence-based static security review. This is not a penetration test: static review cannot prove the application is secure and may miss runtime-only vulnerabilities, infrastructure outside the repository, complex business-logic abuse, sophisticated authorization bypasses, deployment-specific weaknesses, and issues that need dynamic exploitation. State that limitation in every report."
- Evidence L0-S001477: `output/template/.claude/skills/security-scan/SKILL.md:118-118` — "Complete when all applicable layers were inspected, findings have evidence, uncertain findings are labeled, severity reflects actual risk, limitations are stated, and no layer is marked PASS unchecked."

### EXTRA-L0-0168
- Closest oracle policies: WF-020
- Modality: DEFAULT
- Normative action: Map findings to OWASP Top 10:2025 only when the category genuinely fits.
- Trigger/scope: workflow security-scan (security scan, audit, targeted security review)
- Exceptions: none
- Why EXTRA: Taxonomy usage rule not in the oracle.
- Evidence L0-S001461: `output/template/.claude/skills/security-scan/SKILL.md:54-54` — "OWASP Top 10:2025: A01 Broken Access Control · A02 Security Misconfiguration · A03 Software Supply Chain Failures · A04 Cryptographic Failures · A05 Injection · A06 Insecure Design · A07 Authentication Failures · A08 Software or Data Integrity Failures · A09 Security Logging & Alerting Failures · A10 Mishandling of Exceptional Conditions. Map only when the category genuinely fits."

### EXTRA-L0-0169
- Closest oracle policies: WF-020
- Modality: DEFINITION
- Normative action: Severity scale: Critical (sparingly), High, Medium, Low, Info (hardening observation, not a demonstrated vulnerability).
- Trigger/scope: workflow security-scan (security scan, audit, targeted security review)
- Exceptions: none
- Why EXTRA: Five-level scale not in the oracle.
- Evidence L0-S001466: `output/template/.claude/skills/security-scan/SKILL.md:64-68` — "- **Critical** (sparingly) — exposed real production credentials, reachable authentication bypass, straightforward remote code execution, exploitable injection with major impact. ⏎ - **High** — realistically exploitable or substantially compromises data, authorization, or system behavior. ⏎ - **Medium** — meaningful weakness needing realistic conditions, limited access, or extra steps. ⏎ - **Low** …"

### EXTRA-L0-0170
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: Each confirmed finding states severity, file/location, title, evidence, why it is a risk, likely impact, smallest remediation and OWASP category when applicable.
- Trigger/scope: workflow security-scan (security scan, audit, targeted security review)
- Exceptions: none
- Why EXTRA: Mandatory fields not in the oracle.
- Evidence L0-S001471: `output/template/.claude/skills/security-scan/SKILL.md:78-78` — "Each confirmed finding: severity · file and location · title · evidence · why it is a risk · likely impact · smallest remediation · OWASP category when applicable. Label uncertain items `NEEDS VERIFICATION`."

### EXTRA-L0-0171
- Closest oracle policies: WF-020, WF-009
- Modality: DEFAULT
- Normative action: Security report shape: Scope, Limitations, severity Summary, Findings, Layer Results.
- Trigger/scope: workflow security-scan (security scan, audit, targeted security review)
- Exceptions: none
- Why EXTRA: Report template not in the oracle.
- Evidence L0-S001472: `output/template/.claude/skills/security-scan/SKILL.md:80-108` — "```markdown ⏎ # Security Scan Report ⏎  ⏎ Scope: ... ⏎ Limitations: Static analysis only. This does not replace penetration testing, ⏎ dynamic testing, threat modeling, or infrastructure review. ⏎  ⏎ ## Summary ⏎ | Severity | Count | ⏎ |---|---:| ⏎ | Critical | 0 | ⏎ | High | 0 | ⏎ | Medium | 0 | ⏎ | Low | 0 | ⏎ | Info | 0 | ⏎  ⏎ ## Findings ⏎ ### [HIGH] File:Line — Finding title ⏎ OWASP: A01:2025 …"

### EXTRA-L0-0172
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED.
- Trigger/scope: workflow security-scan (security scan, audit, targeted security review)
- Exceptions: none
- Why EXTRA: Vocabulary differs from WF-009.
- Evidence L0-S001473: `output/template/.claude/skills/security-scan/SKILL.md:110-110` — "Layer status is `PASS`, `FINDINGS`, `NOT APPLICABLE`, or `NOT CHECKED`; never mark a layer PASS without checking it."

### EXTRA-L0-0173
- Closest oracle policies: SEC-003
- Modality: PREFER
- Normative action: Prefer APIs separating executable and arguments; constrain input when command execution is genuinely needed.
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: Command execution needed.
- Why EXTRA: Not in the oracle.
- Evidence L0-S001404: `output/template/.claude/skills/security-scan/references/scan-layers.md:25-25` — "- **Command injection:** `Process.Start`, shell/PowerShell/bash invocation, arguments built from user input. Prefer APIs that separate executable and arguments; constrain input when execution is genuinely needed."

### EXTRA-L0-0174
- Closest oracle policies: SEC-003, SEC-015
- Modality: MUST
- Normative action: Normalize user-controlled paths and verify they stay within the storage boundary (traversal, absolute-path injection, unsafe extraction).
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001405: `output/template/.claude/skills/security-scan/references/scan-layers.md:26-26` — "- **Path traversal:** user-controlled file names, paths, archive extraction, download and upload destinations; look for `../`, absolute-path injection, escaping the intended root, unsafe extraction. Normalize and verify paths stay within the storage boundary."

### EXTRA-L0-0175
- Closest oracle policies: SEC-003
- Modality: MUST_NOT
- Normative action: Never deserialize untrusted payloads into arbitrary runtime types (BinaryFormatter, unsafe TypeNameHandling).
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001408: `output/template/.claude/skills/security-scan/references/scan-layers.md:29-29` — "- **Unsafe deserialization:** polymorphic/type-driven mechanisms such as `BinaryFormatter` or unsafe Newtonsoft `TypeNameHandling`; never deserialize untrusted payloads into arbitrary runtime types."

### EXTRA-L0-0176
- Closest oracle policies: WF-020
- Modality: DEFAULT
- Normative action: Consider rate limiting where abuse realistically matters (login/reset, expensive anonymous or resource-intensive endpoints), not on every endpoint.
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001422: `output/template/.claude/skills/security-scan/references/scan-layers.md:47-47` — "- **Rate limiting:** consider it where abuse realistically matters (login/password reset, expensive anonymous endpoints, resource-intensive operations); not on every endpoint. `429` semantics: `http-api` skill."

### EXTRA-L0-0177
- Closest oracle policies: WF-020, WF-012
- Modality: MUST
- Normative action: Name insecure-design workflows (tenant isolation, workflow abuse, privilege escalation, idempotency abuse, multi-step authorization) as threat-modeling/manual-review candidates instead of claiming the scan proves them secure.
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001436: `output/template/.claude/skills/security-scan/references/scan-layers.md:67-67` — "Static checks do not cover insecure design, tenant isolation, business-workflow abuse, privilege escalation through legitimate operations, financial/idempotency abuse, or multi-step authorization. Name such workflows as candidates for threat modeling or dedicated manual review instead of claiming the scan proves them secure."

### EXTRA-L0-0178
- Closest oracle policies: WF-020
- Modality: DEFAULT
- Normative action: Finding format: [SEVERITY] path:line — title, OWASP, Evidence, Impact, Remediation.
- Trigger/scope: private reference of workflow security-scan (security review)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001441: `output/template/.claude/skills/security-scan/references/scan-layers.md:80-94` — "```markdown ⏎ ### [HIGH] src/.../File.cs:42 — Resource authorization missing ⏎  ⏎ OWASP: A01:2025 Broken Access Control ⏎  ⏎ Evidence: ⏎ The endpoint loads an order solely by route ID and does not constrain it to the ⏎ authenticated customer. ⏎  ⏎ Impact: ⏎ An authenticated user who learns another order ID may access that customer's order. ⏎  ⏎ Remediation: ⏎ Apply resource/ownership authorization …"

### EXTRA-L0-0179
- Closest oracle policies: ARC-012
- Modality: DEFAULT
- Normative action: Keep Swagger configuration in Api/composition.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001484: `output/template/.claude/skills/swagger/SKILL.md:31-31` — "Keep Swagger configuration in Api/composition. Built-in `AddOpenApi()` / `MapOpenApi()` is not the template default when the requirement is Swagger UI."

### EXTRA-L0-0180
- Closest oracle policies: WF-006
- Modality: MUST_NOT
- Normative action: The launch profile's URLs agree with the configured HTTP/HTTPS ports; never a browser launch URL pointing to HTTPS on an HTTP-only port.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001487: `output/template/.claude/skills/swagger/SKILL.md:42-42` — "The launch profile's URLs must agree with the configured HTTP/HTTPS ports — never a browser launch URL pointing to HTTPS on an HTTP-only port."

### EXTRA-L0-0181
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: Use CreatedAtAction/CreatedAtRoute (Location) when a canonical resource URL exists.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: Canonical URL exists.
- Why EXTRA: Not in the oracle.
- Evidence L0-S001490: `output/template/.claude/skills/swagger/SKILL.md:56-56` — "When determining real responses consider the whole pipeline — model binding, validation, authentication/authorization, rate limiting, centralized exception handling, other middleware — not only explicit branches in the action. Document `201 Created` (with `CreatedAtAction`/`CreatedAtRoute` when a canonical URL exists) only when that is the runtime contract; never `204` for an endpoint that returns …"

### EXTRA-L0-0182
- Closest oracle policies: DEP-012
- Modality: DEFAULT
- Normative action: Configure Bearer security requirements so authenticated endpoints can be exercised from Swagger UI.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: Bearer used.
- Why EXTRA: Not in the oracle.
- Evidence L0-S001492: `output/template/.claude/skills/swagger/SKILL.md:60-60` — "When the API actually uses Bearer authentication, add a matching security definition and requirements so authenticated endpoints can be exercised from Swagger UI:"

### EXTRA-L0-0183
- Closest oracle policies: API-016
- Modality: DEFAULT
- Normative action: Document consumer-relevant preconditions, idempotency, pagination/filtering and outcomes rather than repeating names.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001496: `output/template/.claude/skills/swagger/SKILL.md:78-78` — "Document what helps a consumer: important preconditions, idempotency semantics, pagination/filtering behavior, meaningful outcomes; avoid descriptions that repeat names. XML comments suit public API contracts when the project chooses them — not every internal type."

### EXTRA-L0-0184
- Closest oracle policies: API-016
- Modality: MUST_NOT
- Normative action: XML comments suit public API contracts when chosen, not every internal type.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001496: `output/template/.claude/skills/swagger/SKILL.md:78-78` — "Document what helps a consumer: important preconditions, idempotency semantics, pagination/filtering behavior, meaningful outcomes; avoid descriptions that repeat names. XML comments suit public API contracts when the project chooses them — not every internal type."

### EXTRA-L0-0185
- Closest oracle policies: API-016, API-015
- Modality: MUST_NOT
- Normative action: Use several Swagger documents only for a real contract separation (versions, public vs internal).
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001498: `output/template/.claude/skills/swagger/SKILL.md:82-82` — "Use several Swagger documents only for a real contract separation (API versions, public vs internal surfaces); versioning strategy belongs to the `api-versioning` skill."

### EXTRA-L0-0186
- Closest oracle policies: API-016, API-014
- Modality: AVOID
- Normative action: Avoid unstable anonymous response shapes / anonymous objects as long-lived contracts; use explicit request/response contracts.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001500: `output/template/.claude/skills/swagger/SKILL.md:86-86` — "When the contract feeds Angular or other client generation: treat breaking schema changes seriously, keep response metadata accurate, avoid unstable anonymous response shapes, use explicit request/response contracts, and review generated-client changes."
- Evidence L0-S001504: `output/template/.claude/skills/swagger/SKILL.md:94-94` — "Swagger as a substitute for integration tests; anonymous objects as long-lived contracts; a second competing documentation stack without a concrete need."

### EXTRA-L0-0187
- Closest oracle policies: TST-002
- Modality: MUST_NOT
- Normative action: Swagger is not a substitute for integration tests.
- Trigger/scope: on-demand knowledge skill swagger (API documentation)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001504: `output/template/.claude/skills/swagger/SKILL.md:94-94` — "Swagger as a substitute for integration tests; anonymous objects as long-lived contracts; a second competing documentation stack without a concrete need."

### EXTRA-L0-0188
- Closest oracle policies: none
- Modality: MUST_NOT
- Normative action: Run template-maintenance only when the user invokes it; never start it automatically.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta invocation rule.
- Evidence L0-S001508: `output/template/.claude/skills/template-maintenance/SKILL.md:13-13` — "Run only when the user invokes it. Never start it automatically."
- Evidence L0-S001577: `output/template/.claude/tools/check-instructions.mjs:210-213` — "const maintenance = meta.get('.claude/skills/template-maintenance/SKILL.md'); ⏎   if (maintenance && maintenance.data?.['disable-model-invocation'] !== 'true') { ⏎     errors.push('template-maintenance: must set disable-model-invocation: true (user-only)'); ⏎   }"

### EXTRA-L0-0189
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: Decision summaries appear only in 1-architecture/overview.md and 3-project/decisions.md; elsewhere use routing pointers or short check-by-reference items.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta rule.
- Evidence L0-S001516: `output/template/.claude/skills/template-maintenance/SKILL.md:36-36` — "State each rule once, in its owner. Elsewhere use only a routing pointer ("run `verify`", "see `backend-layers.md`") or a short check-by-reference item. Decision summaries appear only in `1-architecture/overview.md` and `3-project/decisions.md`."

### EXTRA-L0-0190
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Every artifact starts with the one-line header (Level · Owns · Scope · Loads · Depends on); every rule file declares paths.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta invariant checked by check-instructions.mjs.
- Evidence L0-S001518: `output/template/.claude/skills/template-maintenance/SKILL.md:40-40` — "- Every artifact starts with the one-line header (`Level · Owns · Scope · Loads · Depends on`); every rule file declares `paths`."
- Evidence L0-S001573: `output/template/.claude/tools/check-instructions.mjs:141-157` — "for (const file of artifacts) { ⏎     if (!existsSync(path.join(root, file))) { ⏎       errors.push(`${file}: missing`); ⏎       continue; ⏎     } ⏎     const text = read(file); ⏎     const { data, body, error } = parseFrontmatter(text); ⏎     if (error) errors.push(`${file}: ${error}`); ⏎     const header = parseHeader(body); ⏎     if (!header) { ⏎       errors.push(`${file}: first line must be t …"
- Evidence L0-S001574: `output/template/.claude/tools/check-instructions.mjs:159-171` — "// ---- rules: level-first layout and paths ---- ⏎   for (const file of ruleFiles) { ⏎     const parts = file.split('/'); ⏎     if (parts.length !== 4 || !(parts[2] in LEVEL_DIRS)) { ⏎       errors.push(`${file}: rules must live in .claude/rules/{0-core,1-architecture,2-technology,3-project}/`); ⏎       continue; ⏎     } ⏎     const entry = meta.get(file); ⏎     if (!entry) continue; ⏎     if (ent …"

### EXTRA-L0-0191
- Closest oracle policies: none
- Modality: MUST
- Normative action: Update INSTRUCTION_MAP.md for every added, moved or removed artifact.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta rule.
- Evidence L0-S001521: `output/template/.claude/skills/template-maintenance/SKILL.md:43-43` — "- Update `.claude/INSTRUCTION_MAP.md` for every added, moved, or removed artifact."
- Evidence L0-S001585: `output/template/.claude/tools/check-instructions.mjs:390-403` — "// ---- human map completeness ---- ⏎   if (existsSync(path.join(root, MAP))) { ⏎     const map = read(MAP); ⏎     const mapped = [ ⏎       ...artifacts.filter(file => file !== MAP), ⏎       ...listFiles(root, '.claude/hooks'), ⏎       ...listFiles(root, '.claude/tools'), ⏎       '.claude/settings.json', ⏎     ]; ⏎     for (const file of mapped) { ⏎       const short = file.replace(/^\.claude\/rul …"

### EXTRA-L0-0192
- Closest oracle policies: none
- Modality: MUST
- Normative action: Run check-instructions.mjs and fix every reported error; keep the always-loaded surface compact.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance)
- Exceptions: none
- Why EXTRA: Repo/meta rule.
- Evidence L0-S001523: `output/template/.claude/skills/template-maintenance/SKILL.md:47-47` — "Run the instruction-structure checker `.claude/tools/check-instructions.mjs` (command in `.claude/INSTRUCTION_MAP.md` → Enforcement) and fix every reported error. Keep the always-loaded surface compact (the checker prints its estimate)."

### EXTRA-L0-0193
- Closest oracle policies: WF-005
- Modality: MUST_NOT
- Normative action: Do not use --no-restore unless restore is known to be complete.
- Trigger/scope: workflow verify (before declaring implementation complete or preparing a PR)
- Exceptions: Restore known complete.
- Why EXTRA: Not in the oracle.
- Evidence L0-S001533: `output/template/.claude/skills/verify/SKILL.md:26-26` — "- Backend: `dotnet build` on the solution or the affected projects (do not use `--no-restore` unless restore is known to be complete)."

### EXTRA-L0-0194
- Closest oracle policies: WF-005
- Modality: MUST
- Normative action: Use the workspace's configured frontend build script, inspecting package.json first.
- Trigger/scope: workflow verify (before declaring implementation complete or preparing a PR)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001534: `output/template/.claude/skills/verify/SKILL.md:27-27` — "- Frontend: the workspace's configured build script, typically `npm run build` — inspect `package.json` first."

### EXTRA-L0-0195
- Closest oracle policies: WF-005, TST-002
- Modality: DEFAULT
- Normative action: Small solutions run the whole suite; large ones run affected projects first, then any broader suite the risk requires.
- Trigger/scope: workflow verify (before declaring implementation complete or preparing a PR)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001537: `output/template/.claude/skills/verify/SKILL.md:32-32` — "- Backend: `dotnet test` for the affected test projects; for small solutions run the whole suite, for large ones run affected projects first and then any broader suite the change risk requires."

### EXTRA-L0-0196
- Closest oracle policies: WF-004
- Modality: MUST
- Normative action: Final diff contains no commented-out code, temporary logging, unintended TODO/FIXME markers or stale temporary tests/scripts.
- Trigger/scope: workflow verify (before declaring implementation complete or preparing a PR)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001550: `output/template/.claude/skills/verify/SKILL.md:54-54` — "After all fixes, review the final diff again for: accidental unrelated edits; commented-out code; temporary logging; unintended TODO/FIXME markers; stale temporary tests or scripts; architecture drift; unapproved drift from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`; stale code, tests, docs, or configuration after a `CUSTOM_SETTINGS.md` change; behavior verified manually but never preserved as a t …"

### EXTRA-L0-0197
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: The checker requires every listed workflow skill (project-structure, verify, code-review, build-fix, custom-settings, git-workflow, security-scan, add-dependency, architecture-decision, template-maintenance) and knowledge skill to exist with matching frontmatter name and a description, and forbids standalone serilog/resilience skills.
- Trigger/scope: instruction-system files (CLAUDE.md, .claude/**) when the checker runs (post-edit hook or manual)
- Exceptions: none
- Why EXTRA: Instruction-system invariant (repo/meta).
- Evidence L0-S001568: `output/template/.claude/tools/check-instructions.mjs:18-27` — "const REQUIRED_WORKFLOWS = [ ⏎   'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings', 'git-workflow', ⏎   'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance', ⏎ ]; ⏎ const REQUIRED_KNOWLEDGE = [ ⏎   'ef-core', 'http-api', 'aspnet-error-handling', 'dotnet-testing', 'logging', 'httpclient-factory', ⏎   'configuration', 'dependency-injection', ' …"
- Evidence L0-S001576: `output/template/.claude/tools/check-instructions.mjs:188-209` — "// ---- skills and agents ---- ⏎   const skillDirs = existsSync(path.join(root, '.claude/skills')) ⏎     ? readdirSync(path.join(root, '.claude/skills')).filter(name => statSync(path.join(root, '.claude/skills', name)).isDirectory()) ⏎     : []; ⏎   const skillNames = new Set(); ⏎   for (const dir of skillDirs) { ⏎     const file = `.claude/skills/${dir}/SKILL.md`; ⏎     const entry = meta.get(fil …"

### EXTRA-L0-0198
- Closest oracle policies: DEP-025
- Modality: ENFORCED
- Normative action: Hook registrations must use exec form (command node, args [launcher placeholder, event]), a positive timeout and known handled events; PreToolUse/PostToolUse/PostToolUseFailure/Stop registrations are required; only the PreToolUse guard may (and must) set onFailure block.
- Trigger/scope: instruction-system files (CLAUDE.md, .claude/**) when the checker runs (post-edit hook or manual)
- Exceptions: none
- Why EXTRA: Enforcement-configuration invariant (repo/meta).
- Evidence L0-S001569: `output/template/.claude/tools/check-instructions.mjs:29-42` — "// Hook registrations: exec form (command "node" plus args), the launcher addressed through the host's ⏎ // project-directory placeholder, and the events the enforcement layer depends on. Only the critical ⏎ // PreToolUse guard fails closed; post-event and Stop hooks report without blocking. ⏎ const HOOK_SCRIPT = '.claude/hooks/claude-hook.mjs'; ⏎ const HOOK_LAUNCHER = `\${CLAUDE_PROJECT_DIR}/${HO …"
- Evidence L0-S001584: `output/template/.claude/tools/check-instructions.mjs:334-388` — "// ---- hooks ---- ⏎   const settingsFile = path.join(root, '.claude/settings.json'); ⏎   if (!existsSync(settingsFile)) errors.push('.claude/settings.json: missing'); ⏎   else { ⏎     let settings = null; ⏎     try { ⏎       settings = JSON.parse(read('.claude/settings.json')); ⏎     } catch (error) { ⏎       errors.push(`.claude/settings.json: invalid JSON (${error.message})`); ⏎     } ⏎     con …"

### EXTRA-L0-0199
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Rule files must live in .claude/rules/{0-core,1-architecture,2-technology,3-project}/ with a header level matching the directory.
- Trigger/scope: instruction-system files (CLAUDE.md, .claude/**) when the checker runs (post-edit hook or manual)
- Exceptions: none
- Why EXTRA: Repo/meta invariant.
- Evidence L0-S001574: `output/template/.claude/tools/check-instructions.mjs:159-171` — "// ---- rules: level-first layout and paths ---- ⏎   for (const file of ruleFiles) { ⏎     const parts = file.split('/'); ⏎     if (parts.length !== 4 || !(parts[2] in LEVEL_DIRS)) { ⏎       errors.push(`${file}: rules must live in .claude/rules/{0-core,1-architecture,2-technology,3-project}/`); ⏎       continue; ⏎     } ⏎     const entry = meta.get(file); ⏎     if (!entry) continue; ⏎     if (ent …"

### EXTRA-L0-0200
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: CLAUDE.md must be Level 0, its imports must resolve and it must import overview.md and decisions.md; additional imports raise a warning.
- Trigger/scope: instruction-system files (CLAUDE.md, .claude/**) when the checker runs (post-edit hook or manual)
- Exceptions: none
- Why EXTRA: Repo/meta invariant.
- Evidence L0-S001575: `output/template/.claude/tools/check-instructions.mjs:173-186` — "// ---- CLAUDE.md imports ---- ⏎   const claude = meta.get('CLAUDE.md'); ⏎   const imports = [...read('CLAUDE.md').matchAll(/^@(\S+)\s*$/gm)].map(m => m[1]); ⏎   if (claude && claude.header.level !== 0) errors.push('CLAUDE.md: must be Level 0 Core'); ⏎   for (const target of imports) { ⏎     if (!existsSync(path.join(root, target))) errors.push(`CLAUDE.md: import ${target} does not resolve`); ⏎    …"

### EXTRA-L0-0201
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Internal references (backticked files, .claude paths, Depends on) must resolve; skill-private references may be used only by their owning skill (or the map); named skills/agents, routed workflows and CLAUDE.md routing targets must exist.
- Trigger/scope: instruction-system files (CLAUDE.md, .claude/**) when the checker runs (post-edit hook or manual)
- Exceptions: none
- Why EXTRA: Repo/meta invariant.
- Evidence L0-S001582: `output/template/.claude/tools/check-instructions.mjs:279-325` — "// ---- internal references ---- ⏎   const ruleByBase = new Map(); ⏎   for (const file of ruleFiles) { ⏎     const base = path.posix.basename(file); ⏎     ruleByBase.set(base, ruleByBase.has(base) ? null : file); ⏎   } ⏎   const resolveReference = (from, token) => { ⏎     if (token.startsWith('.claude/') || PRODUCT_INPUTS.includes(token) || token === 'CLAUDE.md') return token; ⏎     if (/^[0-3]-[a …"

### EXTRA-L0-0202
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Files named like manifests, contracts, slots or capabilities under .claude/ are errors (not part of this instruction model).
- Trigger/scope: instruction-system files (CLAUDE.md, .claude/**) when the checker runs (post-edit hook or manual)
- Exceptions: none
- Why EXTRA: Repo/meta invariant.
- Evidence L0-S001583: `output/template/.claude/tools/check-instructions.mjs:327-332` — "// ---- forbidden constructs of other instruction models ---- ⏎   for (const file of listFiles(root, '.claude')) { ⏎     if (/(^|\/)(manifests?|contracts?|slots?|capabilit(y|ies))(\/|\.|$)/i.test(file.replace(/^\.claude\//, ''))) { ⏎       errors.push(`${file}: manifests, capability contracts, and slots are not part of this instruction model`); ⏎     } ⏎   }"

### EXTRA-L0-0203
- Closest oracle policies: none
- Modality: ENFORCED_ADVISORY
- Normative action: The always-loaded surface (CLAUDE.md, imports, model-invocable skill and agent listings) is estimated and warned above 5500 tokens.
- Trigger/scope: instruction-system files (CLAUDE.md, .claude/**) when the checker runs (post-edit hook or manual)
- Exceptions: none
- Why EXTRA: Repo/meta threshold.
- Evidence L0-S001586: `output/template/.claude/tools/check-instructions.mjs:405-414` — "// ---- always-loaded surface estimate ---- ⏎   let chars = read('CLAUDE.md').length; ⏎   for (const target of imports) if (existsSync(path.join(root, target))) chars += read(target).length; ⏎   for (const [file, entry] of meta) { ⏎     const listed = (file.endsWith('/SKILL.md') && entry.data?.['disable-model-invocation'] !== 'true') || file.startsWith('.claude/agents/'); ⏎     if (listed) chars + …"

### EXTRA-L0-0204
- Closest oracle policies: RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: UTF-8, final newline, trimmed trailing whitespace (not for Markdown), space indentation 4 by default and 2 for JSON/YAML/TS/HTML/CSS/JS and MSBuild/XML files.
- Trigger/scope: all repository files (editor/analyzer configuration)
- Exceptions: none
- Why EXTRA: Concrete formatting settings beyond RUN-009.
- Evidence L0-S001589: `output/template/.editorconfig:5-19` — "[*] ⏎ charset = utf-8 ⏎ insert_final_newline = true ⏎ trim_trailing_whitespace = true ⏎ indent_style = space ⏎ indent_size = 4 ⏎  ⏎ [*.{json,yml,yaml,ts,html,scss,css,js,mjs}] ⏎ indent_size = 2 ⏎  ⏎ [*.{csproj,props,targets,slnx,xml,config}] ⏎ indent_size = 2 ⏎  ⏎ [*.md] ⏎ trim_trailing_whitespace = false"

### EXTRA-L0-0205
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: System directives sorted first; usings outside the namespace (suggestion).
- Trigger/scope: all repository files (editor/analyzer configuration)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001592: `output/template/.editorconfig:24-25` — "dotnet_sort_system_directives_first = true ⏎ csharp_using_directive_placement = outside_namespace:suggestion"

### EXTRA-L0-0206
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: var when the type is apparent; explicit types for built-in types and elsewhere (suggestions).
- Trigger/scope: all repository files (editor/analyzer configuration)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001595: `output/template/.editorconfig:30-32` — "csharp_style_var_when_type_is_apparent = true:suggestion ⏎ csharp_style_var_for_built_in_types = false:suggestion ⏎ csharp_style_var_elsewhere = false:suggestion"

### EXTRA-L0-0207
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: Braces when multiline (suggestion); expression-bodied methods on single lines (silent).
- Trigger/scope: all repository files (editor/analyzer configuration)
- Exceptions: none
- Why EXTRA: Not in the oracle.
- Evidence L0-S001597: `output/template/.editorconfig:40-42` — "# Braces and expression bodies ⏎ csharp_prefer_braces = when_multiline:suggestion ⏎ csharp_style_expression_bodied_methods = when_on_single_line:silent"

### EXTRA-L0-0208
- Closest oracle policies: RUN-024
- Modality: ENFORCED_ADVISORY
- Normative action: PascalCase types and members, I-prefixed interfaces, camelCase parameters and locals (suggestions).
- Trigger/scope: all repository files (editor/analyzer configuration)
- Exceptions: none
- Why EXTRA: Naming rules beyond RUN-024.
- Evidence L0-S001598: `output/template/.editorconfig:44-62` — "# Naming: PascalCase types and members, camelCase parameters, Async suffix ⏎ dotnet_naming_symbols.types_and_members.applicable_kinds = class, struct, interface, enum, record, method, property, event, delegate ⏎ dotnet_naming_style.pascal_case.capitalization = pascal_case ⏎ dotnet_naming_rule.types_and_members_pascal.symbols = types_and_members ⏎ dotnet_naming_rule.types_and_members_pascal.style = …"

## LINK_UNCERTAIN constraints (1)

### UNCERTAIN-L0-0001
- Closest oracle policies: GOV-015
- Modality: ALLOWED
- Normative action: Destructive Git operations (reset --hard, clean, force push, force-with-lease, branch deletion, rebasing shared history) are performed only when explicitly requested or clearly required by an approved workflow.
- Trigger/scope: workflow git-workflow (Git operations)
- Exceptions: Explicit request or approved workflow.
- Open question: Open question: GOV-015 permits repository-changing Git operations only when explicitly requested; whether 'clearly required by an approved workflow' widens that condition (a relaxation) or merely describes an explicitly requested workflow cannot be decided from the text.
- Evidence L0-S001088: `output/template/.claude/skills/git-workflow/SKILL.md:45-45` — "`git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion, and rebasing shared history are high-risk: perform them only when explicitly requested or clearly required by an approved workflow, and inspect what will be lost or rewritten first."

