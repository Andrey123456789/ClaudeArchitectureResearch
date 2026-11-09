# K0 — EXTRA and LINK_UNCERTAIN constraints (Claude Run 2, blind replica)

Every constraint below is an effective candidate behavior judged not entailed by the 196 oracle policies (EXTRA) or whose relation could not be decided (LINK_UNCERTAIN). Citations are template-relative paths under `inputs/K0/output/template/` with exact source quotes (newlines shown as ⏎).

## EXTRA (41)

### EXTRA-K0-0001
- Closest oracle policies: DEP-001, DEP-003
- Modality: MUST (PreToolUse deny; PostToolUse confirmation message on removed manifests)
- Normative action: Dependency-removal commands (npm uninstall|remove|rm|r|un|unlink, pnpm/yarn remove, dotnet remove package, dotnet package remove, Uninstall-Package) are likewise denied until the add-dependency workflow has been completed and the command carries `# add-dependency: reviewed`; a removed package manifest is reported for confirmation that the removal was intended and approved.
- Trigger/scope: Bash/PowerShell commands; package manifests
- Exceptions: Marker comment after review.
- Why EXTRA: The oracle's dependency policies (DEP-001..DEP-005) govern additions and updates; no oracle policy subjects dependency removal to a review workflow or approval confirmation.
- Evidence:
  - `.claude/hooks/hook.cjs:155-166` (MIXED, K0-S000020): "if (kind === 'change' || (kind === 'spec' && rest.length > 0)"
  - `.claude/hooks/hook.cjs:168-182` (MIXED, K0-S000021): "dotnet add/remove [<project>] package|reference"
  - `.claude/hooks/hook.cjs:238-269` (MIXED, K0-S000024): "['install-package', 'update-package', 'uninstall-package']"
  - `.claude/hooks/hook.cjs:290-296` (MIXED, K0-S000028): "Run the `add-dependency` workflow first; when its checks are complete, re-run the command with the trailing comment `# add-dependency: reviewed`."
  - `.claude/hooks/hook.cjs:464-466` (MIXED, K0-S000038): "was removed: removing a project or manifest changes the project graph or the dependency set — confirm it was intended and approved"
  - `.claude/MAP.md:182-182` (DUPLICATE, K0-S000073): "Hooks run in exec form (`node` + `args`, no shell): `${CLAUDE_PROJECT_DIR}` only locates `hook.cjs`; every check runs against the active repository or linked worktree, resolved from the hook input `cwd` (or the edited file) through Git, and keeps its state per worktree in `.claude/.hook-state/` (ignored by Git). Hook input may carry a UTF-8 byte-order mark; manifests may be UTF-8 or BOM-tagged UTF"
  - `.claude/MAP.md:184-191` (DUPLICATE, K0-S000074): "| Mechanism | Trigger | Checks | Points to | ⏎ |---|---|---|---| ⏎ | Pre-command hook (fail-closed: a missing script, crash, timeout or unreadable input blocks the command) | Bash/PowerShell command, before execution | npm/pnpm/yarn/ng/dotnet/NuGet package additions, updates and removals (global options and `--force`/`--legacy-peer-deps` included) are denied without `# add-dependency: reviewed`; `dotn"
  - `.claude/rules/common/dependencies.md:14-14` (MIXED, K0-S000259): "adding, updating or removing a package → `add-dependency`"
  - `.claude/settings.json:3-16` (MIXED, K0-S000418): ""onFailure": "block""
  - `.claude/skills/add-dependency/SKILL.md:75-75` (MIXED, K0-S000450): "run the command with the trailing marker comment `# add-dependency: reviewed`"

### EXTRA-K0-0002
- Closest oracle policies: ARC-001, ARC-020, ARC-028, GOV-017
- Modality: MUST (Reserved; PreToolUse deny; PostToolUse finding)
- Normative action: Changing the project reference graph (dotnet add|remove reference, dotnet reference add|remove, or a .csproj ProjectReference change) is Reserved unless an accepted decision already requires the reference, even when the new reference would be legal: commands are denied unless they carry `# project-references: approved` after the Decision Request; post-change findings ask to confirm the change was approved and recorded, or revert it.
- Trigger/scope: .NET project references
- Exceptions: Reference already required by an accepted decision; marker comment after approval.
- Why EXTRA: ARC-001 already permits inward references and ARC-020 gates consequential changes such as new projects/layers; no oracle policy makes every legal reference edge a Reserved decision.
- Evidence:
  - `.claude/hooks/hook.cjs:168-182` (MIXED, K0-S000021): "dotnet add/remove [<project>] package|reference"
  - `.claude/hooks/hook.cjs:238-269` (MIXED, K0-S000024): "['install-package', 'update-package', 'uninstall-package']"
  - `.claude/hooks/hook.cjs:283-289` (EXTRA, K0-S000027): "Changing the project reference graph is Reserved (CLAUDE.md § Decisions) unless an accepted decision already requires the reference, even when the new reference would be legal."
  - `.claude/hooks/hook.cjs:473-477` (EXTRA, K0-S000040): "changing the project reference graph is Reserved (CLAUDE.md § Decisions) — confirm it was approved and recorded"
  - `.claude/MAP.md:182-182` (DUPLICATE, K0-S000073): "Hooks run in exec form (`node` + `args`, no shell): `${CLAUDE_PROJECT_DIR}` only locates `hook.cjs`; every check runs against the active repository or linked worktree, resolved from the hook input `cwd` (or the edited file) through Git, and keeps its state per worktree in `.claude/.hook-state/` (ignored by Git). Hook input may carry a UTF-8 byte-order mark; manifests may be UTF-8 or BOM-tagged UTF"
  - `.claude/MAP.md:184-191` (DUPLICATE, K0-S000074): "| Mechanism | Trigger | Checks | Points to | ⏎ |---|---|---|---| ⏎ | Pre-command hook (fail-closed: a missing script, crash, timeout or unreadable input blocks the command) | Bash/PowerShell command, before execution | npm/pnpm/yarn/ng/dotnet/NuGet package additions, updates and removals (global options and `--force`/`--legacy-peer-deps` included) are denied without `# add-dependency: reviewed`; `dotn"
  - `.claude/settings.json:3-16` (MIXED, K0-S000418): ""onFailure": "block""
  - `.claude/skills/project-structure/SKILL.md:24-24` (MIXED, K0-S001384): "see § Changing project references"
  - `.claude/skills/project-structure/SKILL.md:34-34` (MIXED, K0-S001392): "any other added or removed reference changes the project reference graph and is Reserved"
  - `.claude/skills/project-structure/SKILL.md:35-35` (EXTRA, K0-S001393): "# project-references: approved"
  - `CLAUDE.md:39-39` (MIXED, K0-S001654): "or a change to the project reference graph"

### EXTRA-K0-0003
- Closest oracle policies: none
- Modality: MUST (PostToolUse feedback, decision block)
- Normative action: When instruction files change (CLAUDE.md, the decision register, .claude/** except .hook-state and settings.local.json), check-instructions runs and its errors are fed back to the agent.
- Trigger/scope: Edits/shell commands touching instruction files
- Exceptions: Only errors are fed back.
- Why EXTRA: Structural self-validation of the instruction system; not derived from any V2 policy.
- Evidence:
  - `.claude/hooks/hook.cjs:483-485` (EXTRA, K0-S000042): "if (instructionsChanged && fs.existsSync(path.join(root, '.claude'))) { ⏎     for (const e of script('check-instructions.cjs').check(root).errors) messages.push(`[instructions] ${e}`); ⏎   }"

### EXTRA-K0-0004
- Closest oracle policies: none
- Modality: MUST
- Normative action: Instruction artifacts are organized by two questions: the Kind (OP, DEC, STD, KNW, WF, ENF, IN) decides mechanism, location and loading; the Scope (common, backend, backend-tests, frontend, delivery, repo/meta) decides the directory and path globs (standard globs start in the scope's territory; repo/meta has no standards; a delivery standard is created only when a path-triggered rule is needed).
- Trigger/scope: Instruction-system authoring/maintenance
- Exceptions: none stated
- Why EXTRA: Instruction-system classification scheme of the K design; not derived from any V2 policy.
- Evidence:
  - `.claude/MAP.md:5-8` (EXTRA, K0-S000055): "the Kind decides the mechanism, location and loading"
  - `.claude/MAP.md:12-20` (EXTRA, K0-S000057): "Mechanism and location"
  - `.claude/MAP.md:26-33` (EXTRA, K0-S000060): "Standard globs start with"
  - `.claude/MAP.md:35-35` (EXTRA, K0-S000061): "Create `.claude/rules/delivery/<topic>.md` when one is."
  - `.claude/MAP.md:39-47` (DUPLICATE, K0-S000063): "| Kind | common | backend | backend-tests | frontend | delivery | repo/meta | ⏎ |---|---|---|---|---|---|---| ⏎ | OP | `CLAUDE.md` | | | | | | ⏎ | DEC | `docs/architecture/decision-register.md` | | | | | | ⏎ | STD | `rules/common/security.md`, `rules/common/dependencies.md`, `rules/common/repository-layout.md` | `rules/backend/architecture.md`, `persistence.md`, `api.md`, `error-handling.md`, `csharp.md`,"
  - `.claude/scripts/check-instructions.cjs:11-13` (EXTRA, K0-S000360): "const KINDS = ['OP', 'DEC', 'STD', 'KNW', 'WF', 'ENF', 'IN']; ⏎ const SCOPES = ['common', 'backend', 'backend-tests', 'frontend', 'delivery', 'repo/meta']; ⏎ const RULE_SCOPES = ['common', 'backend', 'backend-tests', 'frontend', 'delivery'];"
  - `.claude/skills/template-maintenance/SKILL.md:15-15` (EXTRA, K0-S001567): "Answer two questions; together they determine location, loading and owner."
  - `.claude/skills/template-maintenance/SKILL.md:17-18` (EXTRA, K0-S001568): "1. **What is it?** Operating policy → OP; project/architecture decision → DEC; normative rule for a scope → STD; technique or examples → KNW; multi-step procedure → WF; mechanical check or delivery asset → ENF; product requirement or tunable value → IN (product input, not an instruction). ⏎ 2. **Where does it apply?** `common`, `backend`, `backend-tests`, `frontend`, `delivery` or `repo/meta`."
  - `.claude/skills/template-maintenance/SKILL.md:20-28` (EXTRA, K0-S001569): "| Kind | Location | Loading | ⏎ |---|---|---| ⏎ | OP | `CLAUDE.md` | always | ⏎ | DEC | `docs/architecture/decision-register.md` (+ ADRs in `docs/decisions/`) | always (imported) | ⏎ | STD | `.claude/rules/<scope>/<topic>.md` with `paths:` inside the scope's territory | path-scoped | ⏎ | KNW | `.claude/skills/<name>/SKILL.md` (+ private `references/`) | on demand | ⏎ | WF | `.claude/skills/<name>/SKILL.md`, `.claude/agents/<name>.md` | workflow | ⏎ | ENF | `.claude/settings.json`, `.claude/hooks/`, `.claude/scripts/`, root build/format files | event/check | ⏎ | IN | `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature/task inputs | read as input |"
  - `.claude/skills/template-maintenance/SKILL.md:35-35` (EXTRA, K0-S001574): "Do not move content between roles to save tokens."

### EXTRA-K0-0005
- Closest oracle policies: none
- Modality: MUST (checked by check-instructions)
- Normative action: Conformance dependencies point WF -> KNW -> STD -> DEC -> OP and ENF -> STD/DEC (declared in the header and Conforms to: lines); routing pointers (See also/Workflow/Technique/Procedure/Enforced by, workflow invocations, CLAUDE.md routing table, register Details in/Affects) may point anywhere; every other reference is a conformance dependency checked for direction and acyclicity; skill references/ files are read only by their skill; standards cite decision IDs instead of restating decisions, and decision summaries exist only in the register.
- Trigger/scope: Instruction-system authoring/maintenance
- Exceptions: Routing pointers are exempt from the direction rule.
- Why EXTRA: Internal reference discipline of the instruction system; no oracle policy governs how instruction files reference each other or where decision summaries may appear.
- Evidence:
  - `.claude/MAP.md:22-22` (EXTRA, K0-S000058): "Conformance dependencies point WF → KNW → STD → DEC → OP, and ENF → STD/DEC; enforcement declares its conformance in its header and in `Conforms to:` comment lines. Routing pointers may point anywhere reliably invocable: references after `See also:`, `Workflow:`, `Technique:`, `Procedure:` or `Enforced by:`, workflow invocations (run, use, invoke, switch to, `→`, slash commands, agent delegation), the `CLAUDE.md` routing table, and the register's **Details in** / **Affects** cells. Every other reference is a conformance dependency, checked for direction and acyclicity by `check-instructions.cjs`; references to product inputs and enforcement files name inputs and tools, not owners. A skill's  […truncated in this report; the exact full quote is in coverage_ranges.jsonl]"
  - `.claude/scripts/check-instructions.cjs:26-38` (EXTRA, K0-S000365): "Conformance direction WF → KNW → STD → DEC → OP, and ENF → STD / DEC"
  - `.claude/scripts/check-instructions.cjs:39-45` (EXTRA, K0-S000366): "A routing pointer may point in any direction"
  - `.claude/scripts/check-instructions.cjs:411-451` (EXTRA, K0-S000398): "violates the Kind direction WF → KNW → STD → DEC → OP, ENF → STD/DEC"
  - `.claude/scripts/check-instructions.cjs:453-465` (EXTRA, K0-S000399): "conformance dependency cycle"
  - `.claude/skills/template-maintenance/SKILL.md:33-33` (EXTRA, K0-S001572): "2. Other artifacts may only point to the owner (routing pointer) or check against it (a short check-by-reference item); never reword the same rule elsewhere."
  - `.claude/skills/template-maintenance/SKILL.md:39-39` (EXTRA, K0-S001576): "Conformance dependencies run WF → KNW → STD → DEC → OP; ENF → STD/DEC, declared in its header or a `Conforms to:` comment line. Standards cite decision IDs (`D-xx`) instead of restating decisions; decision summaries exist only in the register. Routing pointers may point anywhere reliably invocable; write them explicitly — after `See also:`, `Workflow:`, `Technique:`, `Procedure:` or `Enforced by:`, or as an invocation (run, use, invoke or switch to a workflow; `→`). The checker treats every other reference as a conformance dependency; references to product inputs and enforcement files name inputs and tools, not owners. A skill's `references/` files are read only by that skill."

### EXTRA-K0-0006
- Closest oracle policies: none
- Modality: MUST
- Normative action: The maintainer map lists every artifact with its owner, loading, enforcement and 'Extend here' routing; the Decision -> Affects view is generated from the register and must match it (verified by check-instructions).
- Trigger/scope: Instruction-system maintenance
- Exceptions: none stated
- Why EXTRA: Template maintenance rule (single owner per topic, map synchronized with the register); not a V2 policy.
- Evidence:
  - `.claude/MAP.md:12-20` (EXTRA, K0-S000057): "Mechanism and location"
  - `.claude/MAP.md:53-116` (DUPLICATE, K0-S000066): "| File | Kind | Scope | Owner / responsibility | Loading | Enforcement | Extend here | ⏎ |---|---|---|---|---|---|---| ⏎ | `CLAUDE.md` | OP | common | precedence, product sources, engineering defaults, challenge, decisions, Git, routing | always | pre-command hook (Git confirmation, dependency and project-reference gates); hooks route to workflows | new agent-behavior policy | ⏎ | `docs/architecture/dec"
  - `.claude/MAP.md:120-155` (DUPLICATE, K0-S000068): "| Topic | Owner | ⏎ |---|---| ⏎ | Which source wins; vocabulary | `CLAUDE.md` § Precedence | ⏎ | Specification authority, invented behavior, ambiguity approval, string semantics, custom-settings ownership, conflicts, new tunable values, what must not go into `CUSTOM_SETTINGS.md` | `CLAUDE.md` § Product sources | ⏎ | Simplicity, speculative frameworks, scope and behavior preservation, challenge obligation "
  - `.claude/MAP.md:159-159` (EXTRA, K0-S000070): "`check-instructions.cjs` verifies that this view matches it"
  - `.claude/MAP.md:161-178` (DUPLICATE, K0-S000071): "- D-01 (Clean Architecture) → rules/backend-tests/testing.md, rules/backend/api.md, rules/backend/architecture.md, skills/build-fix, skills/code-review, skills/dependency-injection, skills/project-structure, scripts/check-dependencies.cjs ⏎ - D-02 (mediator patterns not adopted) → rules/backend/architecture.md, skills/code-review, skills/project-structure, scripts/check-dependencies.cjs ⏎ - D-03 (back"
  - `.claude/scripts/check-instructions.cjs:520-534` (EXTRA, K0-S000404): "if (!exists(MAP)) { ⏎     err(MAP, 'human-facing instruction map is missing.'); ⏎   } else { ⏎     const map = read(MAP); ⏎     if (!/^> Instruction map \|.*\| Loading: not loaded/.test(map)) err(MAP, 'map header must state that the map is not loaded.'); ⏎     for (const a of artifacts) if (!map.includes(a.rel)) err(MAP, `does not list ${a.rel}.`); ⏎     for (const extra of ['SPECIFICATION.md', '.claude/settings.json']) if (!map.includes(extra)) err(MAP, `does not list ${extra}.`); ⏎     const mapAffects = new Map(); ⏎     for (const m of map.matchAll(/^- (D-\d\d)\b[^\n]*?→\s*([^\n]+)$/gm)) mapAffects.set(m[1], m[2].split(',').map((s) => s.trim()).filter(Boolean)); ⏎     for (const [id, d] of decisions) { ⏎     […truncated in this report; the exact full quote is in coverage_ranges.jsonl]"
  - `.claude/skills/template-maintenance/SKILL.md:32-32` (EXTRA, K0-S001571): "1. Search for an existing owner of the same rule (`.claude/MAP.md` topic index, then a repository search). Extend that owner instead of adding a second statement."
  - `.claude/skills/template-maintenance/SKILL.md:33-33` (EXTRA, K0-S001572): "2. Other artifacts may only point to the owner (routing pointer) or check against it (a short check-by-reference item); never reword the same rule elsewhere."
  - `.claude/skills/template-maintenance/SKILL.md:46-46` (EXTRA, K0-S001581): "4. Update `.claude/MAP.md`: artifact table, Kind × Scope view, topic index and decision → Affects view."

### EXTRA-K0-0007
- Closest oracle policies: ARC-002, DEP-011
- Modality: MUST
- Normative action: Domain stays independent of mapping-library concerns (in addition to EF Core, ASP.NET Core, HTTP, persistence and external-service concerns).
- Trigger/scope: backend Domain
- Exceptions: none stated
- Why EXTRA: ARC-002 lists EF Core, ASP.NET Core, HTTP, persistence and external-service implementation concerns; mapping-library independence of Domain is an additional restriction (DEP-011 only governs when Mapster is approved).
- Evidence:
  - `.claude/rules/backend/architecture.md:22-22` (MIXED, K0-S000105): "including mapping-library concerns"

### EXTRA-K0-0008
- Closest oracle policies: RUN-009, RUN-024
- Modality: PREFER / imperative (path-scoped backend standard)
- Normative action: Backend C# style rules: prefer primary constructors for simple DI/initialization (regular constructors when validation is non-trivial or the codebase uses them) and records where value semantics are intended (not every DTO/Domain type); keep implementation details non-public unless part of the public API and use sealed for design intent, not as speculative optimization; prefer var when the type is obvious; use standard .NET naming (PascalCase types/members, camelCase parameters/locals, meaningful names; private fields per repository convention).
- Trigger/scope: backend/**/*.cs (rule loads for C# files)
- Exceptions: Repository conventions for private-field naming; established codebase style for constructors.
- Why EXTRA: RUN-009 delegates conventions to the repository and .editorconfig and RUN-024 covers only namespaces, one type per file and Async naming; the oracle classifies constructor/record/visibility/type-inference preferences as non-oracle style (EXC-003). The naming and var parts mirror .editorconfig (a RUN-009 convention source), but the visibility, sealed, record and primary-constructor preferences have no .editorconfig or oracle counterpart, so the loaded standard adds style constraints the 196 do not contain.
- Evidence:
  - `.claude/rules/backend/csharp.md:19-22` (MIXED, K0-S000150): "do not convert constructors mechanically"

### EXTRA-K0-0009
- Closest oracle policies: DEP-004, DEP-020, DEP-010
- Modality: MUST NOT (manifest check error)
- Normative action: The NuGet packages Microsoft.Extensions.Http.Polly, Polly.Extensions.Http, Serilog.Sinks.Elasticsearch and FluentValidation.AspNetCore are reported as errors (deprecated; use Microsoft.Extensions.Http.Resilience, Elastic.Serilog.Sinks, FluentValidation.DependencyInjectionExtensions).
- Trigger/scope: .csproj PackageReference and Directory.Packages.props PackageVersion entries
- Exceptions: none stated
- Why EXTRA: DEP-004 requires a deprecation check before installation and DEP-020/DEP-010 set defaults, but no oracle policy turns specific packages into hard errors irrespective of an explicit decision.
- Evidence:
  - `.claude/scripts/check-dependencies.cjs:17-22` (EXTRA, K0-S000326): "const DEPRECATED_NUGET = { ⏎   'microsoft.extensions.http.polly': 'deprecated; use Microsoft.Extensions.Http.Resilience (D-12, add-dependency § Package-specific choices)', ⏎   'polly.extensions.http': 'deprecated; use Microsoft.Extensions.Http.Resilience (D-12, add-dependency § Package-specific choices)', ⏎   'serilog.sinks.elasticsearch': 'deprecated; use Elastic.Serilog.Sinks (logging knowledge)', ⏎   'fluentvalidation.aspnetcore': 'deprecated automatic-validation integration; use FluentValidation.DependencyInjectionExtensions (D-05)', ⏎ };"
  - `.claude/scripts/check-dependencies.cjs:160-164` (MIXED, K0-S000342): "if (DEPRECATED_NUGET[key]) result.errors.push"
  - `.claude/skills/add-dependency/SKILL.md:20-20` (MIXED, K0-S000432): "Do not add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`"
  - `.claude/skills/add-dependency/SKILL.md:22-22` (EXTRA, K0-S000434): "- **Validation** — `FluentValidation.DependencyInjectionExtensions` for registration; do not add a deprecated or legacy ASP.NET automatic-validation integration package without a concrete requirement (D-05)."
  - `.claude/skills/logging/references/serilog.md:200-200` (MIXED, K0-S001224): "The `Serilog.Sinks.Elasticsearch` package is deprecated"

### EXTRA-K0-0010
- Closest oracle policies: none
- Modality: MUST (structure checker error)
- Normative action: Every instruction artifact carries the first-line header 'Kind
- Trigger/scope: Scope
- Exceptions: Owner
- Why EXTRA: Loading' with a known Kind and Scope; its Kind must match its location/mechanism (CLAUDE.md OP, register DEC, CUSTOM_SETTINGS IN, rules STD, agents WF, hooks/scripts/root build files ENF; skills WF or KNW); OP/DEC load always and IN is read as input; no Level/Capability/Slot/Facet/Contract/Module fields, no numbered or level-ordered directories, no capability contracts/manifests/slots/facets, no unclassified files under .claude/ or docs/architecture/.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:22-24` (EXTRA, K0-S000364): "const MD_HEADER = /^> Kind: (\S+) \| Scope: (\S+) \| Owner: (.+?) \| Loading: (.+)$/; ⏎ const CODE_HEADER = /^(?:\/\/|#|<!--)\s*Kind: (\S+) \| Scope: (\S+) \| Owner: (.+?) \| Loading: (.+?)(?:\s*-->)?$/; ⏎ const FORBIDDEN_FIELD = /(^|\|)\s*(?:>\s*)?(Level|Capability|Slot|Facet|Contract|Module)\s*:\s/;"
  - `.claude/scripts/check-instructions.cjs:150-160` (EXTRA, K0-S000376): "const locationKind = (rel) => { ⏎     if (rel === 'CLAUDE.md') return 'OP'; ⏎     if (rel === REGISTER) return 'DEC'; ⏎     if (rel === 'CUSTOM_SETTINGS.md') return 'IN'; ⏎     if (/^\.claude\/rules\/.+\.md$/.test(rel)) return 'STD'; ⏎     if (/^\.claude\/skills\/[^/]+\/SKILL\.md$/.test(rel)) return 'SKILL'; ⏎     if (/^\.claude\/skills\/[^/]+\/references\/.+\.md$/.test(rel)) return 'REFERENCE'; ⏎     if (/^\.claude\/agents\/[^/]+\.md$/.test(rel)) return 'WF'; ⏎     if (/^\.claude\/(hooks|scripts)\/[^/]+\.cjs$/.test(rel) || ['.editorconfig', 'Directory.Build.props', 'Directory.Packages.props'].includes(rel)) return 'ENF-CODE'; ⏎     return null; ⏎   };"
  - `.claude/scripts/check-instructions.cjs:163-186` (EXTRA, K0-S000378): "capability contracts, module manifests, slots or facets are not part of this system."
  - `.claude/scripts/check-instructions.cjs:194-203` (EXTRA, K0-S000380): "for (const a of artifacts) { ⏎     if (!KINDS.includes(a.kind)) err(a.rel, `unknown Kind "${a.kind}".`); ⏎     if (!SCOPES.includes(a.scope)) err(a.rel, `unknown Scope "${a.scope}".`); ⏎     if (FORBIDDEN_FIELD.test(a.header)) err(a.rel, 'header carries a level/capability field; this system classifies by Kind and Scope only.'); ⏎     if (!a.code) { ⏎       a.prose = fences(a.body, (line, message) => err(a.rel, `line ${line + a.offset}: ${message}.`)); ⏎       a.prose.split('\n').forEach((line, i) => { ⏎         if (FORBIDDEN_FIELD.test(line)) err(a.rel, `line ${i + 1 + a.offset}: "Level:"/capability fields are not used; classify by Kind and Scope.`); ⏎       }); ⏎     }"
  - `.claude/scripts/check-instructions.cjs:205-209` (EXTRA, K0-S000381): "OP/DEC must load always."
  - `.claude/skills/template-maintenance/SKILL.md:43-43` (EXTRA, K0-S001578): "1. Write the artifact with its one-line header: `> Kind: … | Scope: … | Owner: … | Loading: …` (after any frontmatter)."

### EXTRA-K0-0011
- Closest oracle policies: none
- Modality: MUST (structure checker error)
- Normative action: Standards live directly in .claude/rules/<scope>/<topic>.md for scopes common, backend, backend-tests, frontend, delivery; the header Scope equals the directory; STD loads path-scoped with non-empty paths whose globs stay inside the scope territory (backend: backend/, root .NET build files, global.json, *.slnx; backend-tests: backend/ and containing Tests; frontend: frontend/; delivery: Docker/Compose/CI paths); standards contain no numbered procedures or Step/Procedure headings (procedures belong in workflows).
- Trigger/scope: Rule files
- Exceptions: common scope accepts any glob.
- Why EXTRA: Rule-organization and loading discipline of the template; not a V2 policy.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:11-13` (EXTRA, K0-S000360): "const KINDS = ['OP', 'DEC', 'STD', 'KNW', 'WF', 'ENF', 'IN']; ⏎ const SCOPES = ['common', 'backend', 'backend-tests', 'frontend', 'delivery', 'repo/meta']; ⏎ const RULE_SCOPES = ['common', 'backend', 'backend-tests', 'frontend', 'delivery'];"
  - `.claude/scripts/check-instructions.cjs:108-117` (EXTRA, K0-S000370): "function globInScope(glob, scope) { ⏎   switch (scope) { ⏎     case 'common': return true; ⏎     case 'backend': return glob.startsWith('backend/') || ['Directory.Build.props', 'Directory.Packages.props', 'global.json', '*.slnx'].includes(glob); ⏎     case 'backend-tests': return glob.startsWith('backend/') && glob.includes('Tests'); ⏎     case 'frontend': return glob.startsWith('frontend/'); ⏎     case 'delivery': return /Dockerfile|docker|compose|\.github\/|pipeline|gitlab-ci/i.test(glob); ⏎     default: return false; ⏎   } ⏎ }"
  - `.claude/scripts/check-instructions.cjs:211-223` (EXTRA, K0-S000382): "procedures belong in a workflow, not in a standard."

### EXTRA-K0-0012
- Closest oracle policies: none
- Modality: MUST (structure checker error)
- Normative action: Skill and agent structure: skill frontmatter name equals the directory and has a concrete description (20+ characters); KNW skills load on demand and stay model-invocable; WF skills load as workflows; the required workflows (development-workflow, project-structure, verify, code-review, build-fix, custom-settings, git-workflow, security-scan, add-dependency, architecture-decision, delivery-pipeline, template-maintenance) and knowledge skills (ef-core, http-api, aspnet-error-handling, dotnet-testing, logging, httpclient-factory, configuration, dependency-injection, caching, swagger, api-versioning, health-check, docker, ci-cd, angular, modern-csharp, authentication) exist; template-maintenance is user-only (disable-model-invocation: true); private references have their skill's Kind and state that only that skill reads them; retired skill names (testing, error-handling, serilog, resilience) are not used; agents' frontmatter name equals the file name and they load as agents.
- Trigger/scope: Instruction-system skills and agents
- Exceptions: none stated
- Why EXTRA: Template inventory and packaging rules; the oracle prescribes no skill inventory or metadata.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:14-17` (EXTRA, K0-S000361): "const REQUIRED_WORKFLOWS = ['development-workflow', 'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings', 'git-workflow', 'security-scan', 'add-dependency', 'architecture-decision', 'delivery-pipeline', 'template-maintenance']; ⏎ const REQUIRED_KNOWLEDGE = ['ef-core', 'http-api', 'aspnet-error-handling', 'dotnet-testing', 'logging', 'httpclient-factory', 'configuration', 'dependency-injection', 'caching', 'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd', 'angular', 'modern-csharp', 'authentication']; ⏎ const USER_ONLY_WORKFLOWS = ['template-maintenance']; ⏎ const RETIRED_SKILL_NAMES = ['testing', 'error-handling', 'serilog', 'resilience'];"
  - `.claude/scripts/check-instructions.cjs:225-241` (EXTRA, K0-S000383): "if (a.expected === 'SKILL') { ⏎       const name = a.rel.split('/')[2]; ⏎       if (a.fm.name !== name) err(a.rel, `frontmatter name "${a.fm.name}" must equal the directory name "${name}".`); ⏎       if (!a.fm.description || String(a.fm.description).length < 20) err(a.rel, 'skill needs a concrete description.'); ⏎       const userOnly = String(a.fm['disable-model-invocation']).toLowerCase() === 'true'; ⏎       if (a.kind === 'KNW') { ⏎         if (!a.loading.includes('on demand')) err(a.rel, 'KNW must load on demand.'); ⏎         if (userOnly) err(a.rel, 'knowledge skills must stay model-invocable.'); ⏎         if (REQUIRED_WORKFLOWS.includes(name)) err(a.rel, `"${name}" is a workflow and must be Kind WF.`) […truncated in this report; the exact full quote is in coverage_ranges.jsonl]"
  - `.claude/scripts/check-instructions.cjs:243-247` (EXTRA, K0-S000384): "if (a.expected === 'REFERENCE') { ⏎       const owner = byRel.get(`.claude/skills/${a.rel.split('/')[2]}/SKILL.md`); ⏎       if (owner && owner.kind !== a.kind) err(a.rel, `private reference Kind ${a.kind} differs from its skill (${owner.kind}).`); ⏎       if (!a.loading.includes('only')) err(a.rel, 'private reference must state that only its skill reads it.'); ⏎     }"
  - `.claude/scripts/check-instructions.cjs:257-261` (EXTRA, K0-S000386): "if (a.rel.startsWith('.claude/agents/')) { ⏎       const name = path.basename(a.rel, '.md'); ⏎       if (a.fm.name !== name) err(a.rel, `frontmatter name "${a.fm.name}" must equal the file name "${name}".`); ⏎       if (!a.loading.includes('agent')) err(a.rel, 'agents load as delegated agents.'); ⏎     }"
  - `.claude/scripts/check-instructions.cjs:264-267` (MIXED, K0-S000388): "agent must delegate to the code-review workflow."
  - `.claude/skills/template-maintenance/SKILL.md:4-4` (EXTRA, K0-S001561): "disable-model-invocation: true"
  - `.claude/skills/template-maintenance/SKILL.md:45-45` (EXTRA, K0-S001580): "3. Knowledge skill descriptions stay concise and trigger-first ("Use when …" with concrete cues)."

### EXTRA-K0-0013
- Closest oracle policies: none
- Modality: MUST (structure checker error)
- Normative action: Knowledge skills and their private references must not contain normative wording (must, never, requires approval) on a line without an owner reference (rules/, CLAUDE.md or a D-xx decision ID); the rule must be moved to its standard and pointed to.
- Trigger/scope: KNW skills and references
- Exceptions: Lines citing an owner.
- Why EXTRA: Instruction-authoring rule (normative statements only in owners); no V2 policy constrains where normative wording may appear.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:249-255` (EXTRA, K0-S000385): "if ((a.expected === 'SKILL' || a.expected === 'REFERENCE') && a.kind === 'KNW') { ⏎       a.prose.split('\n').forEach((line, i) => { ⏎         if (/\b(must|never|requires approval)\b/i.test(line) && !/(rules\/|CLAUDE\.md|D-\d\d)/.test(line)) { ⏎           err(a.rel, `line ${i + 1 + a.offset}: normative wording in knowledge without an owner reference; move the rule to its standard and point to it.`); ⏎         } ⏎       }); ⏎     }"
  - `.claude/skills/template-maintenance/SKILL.md:34-34` (EXTRA, K0-S001573): "3. A critical must/must-not rule never lives only in a knowledge skill or a skill-private reference."

### EXTRA-K0-0014
- Closest oracle policies: GOV-017
- Modality: MUST (structure checker error)
- Normative action: Exactly one decision register (docs/architecture/decision-register.md) carries Kind DEC and CLAUDE.md imports exactly it; register rows are 'D-xx
- Trigger/scope: Decision
- Exceptions: Details in
- Why EXTRA: Affects' with unique IDs, a non-empty Decision that does not depend on rules/skills/scripts, existing Affects targets of Kind STD/KNW/WF/ENF and Details-in targets also listed in Affects; any artifact citing D-xx must be listed in that decision's Affects; decision entries are defined only in the register; no other artifact may restate a decision (8-word overlap) — cite the ID instead.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:285-288` (EXTRA, K0-S000390): "const decArtifacts = artifacts.filter((a) => a.kind === 'DEC'); ⏎   if (decArtifacts.length !== 1 || decArtifacts[0].rel !== REGISTER) err(REGISTER, `exactly one decision register (${REGISTER}) must carry Kind DEC; found ${decArtifacts.map((a) => a.rel).join(', ') || 'none'}.`); ⏎   const imports = exists('CLAUDE.md') ? [...read('CLAUDE.md').matchAll(/^@(\S+)\s*$/gm)].map((m) => m[1]) : []; ⏎   if (imports.length !== 1 || imports[0] !== REGISTER) err('CLAUDE.md', `must import exactly the decision register ("@${REGISTER}"); imports make content always-loaded (found: ${imports.join(', ') || 'none'}).`);"
  - `.claude/scripts/check-instructions.cjs:290-314` (EXTRA, K0-S000391): "if (exists(REGISTER)) { ⏎     for (const line of read(REGISTER).split('\n')) { ⏎       if (!/^\| D-/.test(line)) continue; ⏎       const cells = line.split('|').slice(1, -1).map((c) => c.trim()); ⏎       const [id, decision, details, affects] = cells; ⏎       if (!/^D-\d\d$/.test(id)) { err(REGISTER, `malformed decision ID "${id}".`); continue; } ⏎       if (decisions.has(id)) err(REGISTER, `duplicate decision ID ${id}.`); ⏎       if (cells.length !== 4) err(REGISTER, `${id}: rows need ID | Decision | Details in | Affects.`); ⏎       const affectsList = (affects || '').split(',').map((s) => s.trim()).filter((s) => s && s !== '—'); ⏎       const detailsList = (details || '').split(',').map((s) => s.trim().repl […truncated in this report; the exact full quote is in coverage_ranges.jsonl]"
  - `.claude/scripts/check-instructions.cjs:316-323` (EXTRA, K0-S000392): "for (const a of artifacts) { ⏎     if (a.rel === REGISTER) continue; ⏎     for (const id of new Set([...a.body.matchAll(/\bD-\d\d\b/g)].map((m) => m[0]))) { ⏎       const d = decisions.get(id); ⏎       if (!d) err(a.rel, `cites unknown decision ${id}.`); ⏎       else if (!d.affects.includes(registerKey(a.rel))) err(a.rel, `cites ${id} but is not listed in its Affects (${registerKey(a.rel)}).`); ⏎     } ⏎   }"
  - `.claude/scripts/check-instructions.cjs:324-326` (EXTRA, K0-S000393): "for (const rel of walk('')) { ⏎     if (rel !== REGISTER && /\.md$/.test(rel) && /^\| D-\d\d \|/m.test(read(rel))) err(rel, 'decision entries are defined only in the decision register.'); ⏎   }"
  - `.claude/scripts/check-instructions.cjs:327-335` (EXTRA, K0-S000394): "cite the ID instead"
  - `.claude/skills/architecture-decision/SKILL.md:38-38` (MIXED, K0-S000541): "next free stable ID (never reuse a retired ID)"
  - `docs/architecture/decision-register.md:5-5` (MIXED, K0-S001691): "Changing an entry is Reserved"

### EXTRA-K0-0015
- Closest oracle policies: none
- Modality: MUST (structure checker error)
- Normative action: References must resolve: backticked file/skill/agent references and '§ section' references must point to existing targets and headings; unknown hyphenated skill/agent names in skill contexts are errors; skill-private references are used only by their own skill.
- Trigger/scope: Instruction-system references
- Exceptions: Placeholders, commands and plain hyphenated words are skipped.
- Why EXTRA: Referential-integrity rule of the instruction system; not a V2 policy.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:392-410` (EXTRA, K0-S000397): "const SECTION_REF = /(?:`([^`]+)`|\b(CLAUDE\.md|(?:\.claude\/)?(?:rules|skills)\/[\w./-]+\.md|[a-z][a-z0-9]*(?:-[a-z0-9]+)+))\s*§\s*([^.;,)\n—'"`\\]+?)(?=\s*(?:[.;,)\n—'"`\\]|\(|$| and §| and `))/g; ⏎   const checkSections = (a, line, lineNo) => { ⏎     for (const m of line.matchAll(SECTION_REF)) { ⏎       const target = (m[1] || m[2]).replace(/\\/g, '').replace(/^\//, ''); ⏎       let rel = resolveRef(target, a.rel); ⏎       if (rel === undefined && target === 'CLAUDE.md') rel = 'CLAUDE.md'; ⏎       if (!rel) { ⏎         if (m[2] && !skillDirs.includes(target) && /-/.test(target) && !target.includes('/')) continue; // plain hyphenated words ⏎         err(a.rel, `line ${lineNo}: section reference target "${ […truncated in this report; the exact full quote is in coverage_ranges.jsonl]"
  - `.claude/scripts/check-instructions.cjs:411-451` (EXTRA, K0-S000398): "violates the Kind direction WF → KNW → STD → DEC → OP, ENF → STD/DEC"

### EXTRA-K0-0016
- Closest oracle policies: none
- Modality: MUST (structure checker error)
- Normative action: Manual tool invocations in instruction files must be root-aware: node "$(git rev-parse --show-toplevel)/.claude/..." instead of a command relative to the current directory.
- Trigger/scope: Instruction files and MAP.md
- Exceptions: none stated
- Why EXTRA: Command-portability rule of the template; not a V2 policy.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:54-55` (EXTRA, K0-S000368): "const HOOK_SCRIPT_ARG = /^\$\{CLAUDE_PROJECT_DIR\}\/\.claude\/hooks\/([^/\\]+)$/; ⏎ const CWD_RELATIVE_COMMAND = /\bnode\s+\.?\/?\.claude[\\/]/;"
  - `.claude/scripts/check-instructions.cjs:467-472` (EXTRA, K0-S000400): "// Manual tool invocations must work from any directory of the repository or worktree. ⏎   for (const rel of [...artifacts.map((a) => a.rel), ...(exists(MAP) ? [MAP] : [])]) { ⏎     read(rel).split('\n').forEach((line, i) => { ⏎       if (CWD_RELATIVE_COMMAND.test(line)) err(rel, `line ${i + 1}: tool invocation is relative to the current directory; use node "$(git rev-parse --show-toplevel)/.claude/…".`); ⏎     }); ⏎   }"

### EXTRA-K0-0017
- Closest oracle policies: none
- Modality: MUST (structure checker error)
- Normative action: Hook configuration: every hook is a command hook in exec form (executable-only command, args [${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>, <event>] with the script present and handling the event), no variable expansion in arguments, a positive timeout; PreToolUse (pre-tool-use, Bash/PowerShell), PostToolUse (post-tool-use, Edit/Write/MultiEdit/NotebookEdit/Bash/PowerShell), PostToolUseFailure (Bash/PowerShell) and Stop must be registered; only the PreToolUse policy hook may set onFailure, and it must be 'block' (fail closed).
- Trigger/scope: .claude/settings.json
- Exceptions: none stated
- Why EXTRA: Enforcement-configuration invariants of the template; no V2 policy requires hooks.
- Evidence:
  - `.claude/scripts/check-instructions.cjs:47-53` (EXTRA, K0-S000367): "// Hook registrations of the enforcement design: host event, event argument, tools the matchers must cover. ⏎ const REQUIRED_HOOKS = [ ⏎   { event: 'PreToolUse', arg: 'pre-tool-use', tools: ['Bash', 'PowerShell'], failClosed: true }, ⏎   { event: 'PostToolUse', arg: 'post-tool-use', tools: ['Edit', 'Write', 'MultiEdit', 'NotebookEdit', 'Bash', 'PowerShell'] }, ⏎   { event: 'PostToolUseFailure', arg: 'post-tool-use-failure', tools: ['Bash', 'PowerShell'] }, ⏎   { event: 'Stop', arg: 'stop', tools: [] }, ⏎ ];"
  - `.claude/scripts/check-instructions.cjs:54-55` (EXTRA, K0-S000368): "const HOOK_SCRIPT_ARG = /^\$\{CLAUDE_PROJECT_DIR\}\/\.claude\/hooks\/([^/\\]+)$/; ⏎ const CWD_RELATIVE_COMMAND = /\bnode\s+\.?\/?\.claude[\\/]/;"
  - `.claude/scripts/check-instructions.cjs:478-514` (EXTRA, K0-S000402): "if (!exists('.claude/settings.json')) { ⏎     err('.claude/settings.json', 'settings with hook configuration are missing.'); ⏎   } else { ⏎     let settings = null; ⏎     try { settings = JSON.parse(read('.claude/settings.json')); } catch (e) { err('.claude/settings.json', `invalid JSON: ${e.message}`); } ⏎     const registrations = []; ⏎     for (const [event, groups] of Object.entries(settings?.hooks || {})) { ⏎       for (const group of Array.isArray(groups) ? groups : []) { ⏎         for (const hook of group.hooks || []) { ⏎           const where = `.claude/settings.json: ${event}`; ⏎           const args = Array.isArray(hook.args) ? hook.args : null; ⏎           if (hook.type !== 'command') { errors.push(`${ […truncated in this report; the exact full quote is in coverage_ranges.jsonl]"
  - `.claude/settings.json:3-16` (MIXED, K0-S000418): ""onFailure": "block""

### EXTRA-K0-0018
- Closest oracle policies: DEP-010, DEP-004
- Modality: MUST
- Normative action: Register FluentValidation validators with FluentValidation.DependencyInjectionExtensions; do not add a deprecated or legacy ASP.NET automatic-validation integration package without a concrete requirement.
- Trigger/scope: Validation package choice
- Exceptions: concrete requirement (but FluentValidation.AspNetCore is a hard manifest error, EXTRA-K0-0009)
- Why EXTRA: DEP-010 makes FluentValidation the standard library but prescribes no registration package; no oracle policy restricts the automatic-validation integration package.
- Evidence:
  - `.claude/skills/add-dependency/SKILL.md:22-22` (EXTRA, K0-S000434): "- **Validation** — `FluentValidation.DependencyInjectionExtensions` for registration; do not add a deprecated or legacy ASP.NET automatic-validation integration package without a concrete requirement (D-05)."
  - `.claude/skills/aspnet-error-handling/SKILL.md:116-116` (MIXED, K0-S000569): "Register validators with `FluentValidation.DependencyInjectionExtensions`"
  - `docs/architecture/decision-register.md:20-20` (MIXED, K0-S001700): "`FluentValidation.DependencyInjectionExtensions`"

### EXTRA-K0-0019
- Closest oracle policies: DEP-001, GOV-014
- Modality: MUST
- Normative action: Remove a dependency that is no longer used when that is part of the current change and safe to verify; do not leave dead references behind.
- Trigger/scope: Changes that make a dependency unused
- Exceptions: Not during unrelated cleanup of a narrowly scoped task.
- Why EXTRA: No oracle policy obliges removing packages made unused by a change (RUN-010 concerns only unused usings).
- Evidence:
  - `.claude/skills/add-dependency/SKILL.md:90-90` (MIXED, K0-S000457): "Remove a dependency that is no longer used when that is part of the current change and safe to verify; do not leave dead references behind, and do not perform unrelated dependency cleanup during a narrowly scoped task."

### EXTRA-K0-0020
- Closest oracle policies: DEP-004, DEP-005, WF-009
- Modality: MUST
- Normative action: The add-dependency output reports package, selected version and why, license, deprecation and vulnerability status, approval obtained (if needed), files changed and the verification result.
- Trigger/scope: End of add-dependency
- Exceptions: none stated
- Why EXTRA: WF-009 covers verification reporting only; the per-package report content is an additional workflow duty.
- Evidence:
  - `.claude/skills/add-dependency/SKILL.md:94-94` (EXTRA, K0-S000459): "Package, selected version and why, license, deprecation and vulnerability status, approval obtained (if needed), files changed, verification result."

### EXTRA-K0-0021
- Closest oracle policies: API-013, DEP-017, ARC-020
- Modality: MUST (Reserved)
- Normative action: Adopting API versioning is Reserved (D-15).
- Trigger/scope: Introducing API versioning
- Exceptions: none stated
- Why EXTRA: API-013 forbids versioning without a concrete need and DEP-017 makes the package conditional; neither requires explicit approval once the need exists.
- Evidence:
  - `.claude/skills/api-versioning/SKILL.md:10-10` (EXTRA, K0-S000506): "adopting versioning is Reserved"
  - `CLAUDE.md:45-45` (MIXED, K0-S001660): "or adopting API versioning"

### EXTRA-K0-0022
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: Decision propagation: find everything a decision touches via its register entry and Affects list; after approval edit every artifact in Affects so each keeps only its own responsibility (standards cite the ID, knowledge adjusts technique, workflows commands, enforcement checks such as deny-lists) and keep the Affects list current.
- Trigger/scope: Approved decisions
- Exceptions: none stated
- Why EXTRA: GOV-017 requires approval of Reserved changes but no Affects-driven propagation procedure across instruction artifacts.
- Evidence:
  - `.claude/skills/architecture-decision/SKILL.md:16-16` (EXTRA, K0-S000533): "3. Find what it touches: the register entry and its **Affects** list, the relevant standards, knowledge, workflows and enforcement."
  - `.claude/skills/architecture-decision/SKILL.md:57-58` (EXTRA, K0-S000545): "1. Edit every artifact in the entry's **Affects** list so that each keeps only its own responsibility: standards cite the ID, knowledge adjusts technique, workflows adjust commands, enforcement adjusts checks (for example the deny-lists in `.claude/scripts/check-dependencies.cjs`). Example: replacing the backend test framework touches the testing standard, the testing knowledge skill, scaffolding commands and test-related checks. ⏎ 2. Add newly affected artifacts to **Affects**; remove ones that no longer depend on the decision."
  - `.claude/skills/template-maintenance/SKILL.md:44-44` (EXTRA, K0-S001579): "2. Decision added or changed: follow `architecture-decision` § 3–4 (ID, Details in, Affects, propagation)."
  - `docs/architecture/decision-register.md:5-5` (MIXED, K0-S001691): "Changing an entry is Reserved"

### EXTRA-K0-0023
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST (conditional)
- Normative action: When rationale, alternatives or consequences need more than the register sentence add an ADR docs/decisions/NNNN-<slug>.md (Status, Date, Register, Context, Decision, Alternatives considered, Consequences) cited in Details in; superseding marks the old ADR 'Superseded by NNNN' and replaces the register entry — never two active entries for one choice; register IDs are stable and never reused.
- Trigger/scope: Recording decisions
- Exceptions: none stated
- Why EXTRA: No oracle policy requires ADRs, ADR structure or superseding bookkeeping.
- Evidence:
  - `.claude/skills/architecture-decision/SKILL.md:39-40` (EXTRA, K0-S000542): "2. When rationale, alternatives or consequences need more than the register sentence, add an ADR `docs/decisions/NNNN-<slug>.md` (template below) and cite it in **Details in**. ⏎   3. Superseding a decision: mark the old ADR `Superseded by NNNN` and replace the register entry; do not keep two active entries for one choice."
  - `.claude/skills/architecture-decision/SKILL.md:42-53` (EXTRA, K0-S000543): "Status: Accepted | Superseded by NNNN"

### EXTRA-K0-0024
- Closest oracle policies: none
- Modality: MUST
- Normative action: Changes to .claude/ instruction files are instruction-system maintenance: ask the user to run /template-maintenance for structural changes and run check-instructions after any instruction edit.
- Trigger/scope: Instruction-file edits
- Exceptions: none stated
- Why EXTRA: Template-maintenance routing; no V2 policy governs instruction-file maintenance.
- Evidence:
  - `.claude/skills/architecture-decision/SKILL.md:59-59` (EXTRA, K0-S000546): "3. Changes to `.claude/` instruction files are instruction-system maintenance: ask the user to run `/template-maintenance` for structural changes, and run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.cjs"` after any edit."
  - `.claude/skills/template-maintenance/SKILL.md:4-4` (EXTRA, K0-S001561): "disable-model-invocation: true"
  - `.claude/skills/template-maintenance/SKILL.md:51-51` (EXTRA, K0-S001584): "1. Run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.cjs"` and fix every reported problem."
  - `CLAUDE.md:73-73` (EXTRA, K0-S001671): "| Changing this instruction system | ask the user to run `/template-maintenance` (never model-invoked) |"

### EXTRA-K0-0025
- Closest oracle policies: GOV-017, WF-009
- Modality: MUST
- Normative action: The architecture-decision output is the Decision Request (when pending) or the recorded outcome: register entry, ADR path if any, artifacts updated, checker result.
- Trigger/scope: End of architecture-decision
- Exceptions: none stated
- Why EXTRA: Workflow-specific report content beyond WF-009.
- Evidence:
  - `.claude/skills/architecture-decision/SKILL.md:63-63` (EXTRA, K0-S000548): "The Decision Request (when pending) or the recorded outcome: register entry, ADR path if any, artifacts updated, checker result."

### EXTRA-K0-0026
- Closest oracle policies: RUN-021, ARC-017
- Modality: AVOID (listed common mistake)
- Normative action: Caching EF tracked entities across Unit of Work boundaries is listed as a mistake to avoid.
- Trigger/scope: Caching persistence data
- Exceptions: none stated
- Why EXTRA: No oracle policy and no K0 standard forbids caching tracked entities across Unit of Work scopes; the knowledge skill adds this restriction as a named mistake.
- Evidence:
  - `.claude/skills/caching/SKILL.md:95-95` (MIXED, K0-S000697): "caching EF tracked entities across Unit of Work boundaries"
  - `.claude/skills/ef-core/SKILL.md:348-348` (MIXED, K0-S001020): "fire-and-forget EF asynchronous operations"

### EXTRA-K0-0027
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: The delivery-pipeline output lists files changed, stages and the commands they run, what was verified and any hosting-platform assumption still needing confirmation.
- Trigger/scope: End of delivery-pipeline
- Exceptions: none stated
- Why EXTRA: Workflow-specific report content beyond WF-009's verification reporting.
- Evidence:
  - `.claude/skills/delivery-pipeline/SKILL.md:39-39` (EXTRA, K0-S000826): "Files changed, stages and the commands they run, what was verified, and any assumption about the hosting platform that still needs confirmation."

### EXTRA-K0-0028
- Closest oracle policies: WF-009, GOV-017
- Modality: MUST
- Normative action: The development-workflow output states what changed and why, the Delegated decisions taken, Decision Requests raised or still unresolved, and the verification report.
- Trigger/scope: End of implementation work
- Exceptions: none stated
- Why EXTRA: WF-009 covers verification reporting; reporting every Delegated decision taken and every Decision Request is an additional duty.
- Evidence:
  - `.claude/skills/development-workflow/SKILL.md:81-81` (EXTRA, K0-S000882): "- What changed and why; Delegated decisions taken; Decision Requests raised or still unresolved; the verification report (see also: `verify` § Report)."

### EXTRA-K0-0029
- Closest oracle policies: RUN-002, ARC-022
- Modality: AVOID (listed common mistake)
- Normative action: Fire-and-forget EF Core asynchronous operations are listed as a mistake to avoid.
- Trigger/scope: EF Core data access
- Exceptions: none stated
- Why EXTRA: RUN-002 forbids blocking async I/O and ARC-022 governs lifetimes; no oracle policy (and no K0 standard) forbids un-awaited database operations.
- Evidence:
  - `.claude/skills/ef-core/SKILL.md:348-348` (MIXED, K0-S001020): "fire-and-forget EF asynchronous operations"

### EXTRA-K0-0030
- Closest oracle policies: GOV-015
- Modality: MUST NOT
- Normative action: Treat main, master and other protected or shared branches as non-rewritable.
- Trigger/scope: Git history rewriting
- Exceptions: none stated
- Why EXTRA: GOV-015 allows history-changing operations on explicit request; declaring main/master non-rewritable is a stricter, unconditional restriction.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:61-61` (MIXED, K0-S001045): "treat `main`, `master` and other protected or shared branches as non-rewritable"

### EXTRA-K0-0031
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: A PR describes what changed, why, how it was verified and any compatibility or migration notes.
- Trigger/scope: Pull requests
- Exceptions: none stated
- Why EXTRA: No oracle policy fixes PR description content.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:69-69` (MIXED, K0-S001049): "Describe what changed, why, how it was verified"

### EXTRA-K0-0032
- Closest oracle policies: RUN-016, DEP-020
- Modality: MUST NOT
- Normative action: Do not wrap normal EF Core operations in a generic application-level retry pipeline; prefer the provider's EF Core execution strategy for transient retry and handle transaction/retry interaction per provider guidance; HTTP retry policies are not database policies.
- Trigger/scope: Database operations
- Exceptions: none stated
- Why EXTRA: RUN-016 limits retries to safe operations and DEP-020 sets resilience package defaults; no oracle policy forbids application-level retry pipelines around database calls or prescribes provider execution strategies (the oracle treats database-retry examples as technique, EXC-007).
- Evidence:
  - `.claude/skills/httpclient-factory/references/resilience.md:49-49` (EXTRA, K0-S001146): "Do not wrap normal EF Core operations in a generic application-level retry pipeline. When the provider supports transient retry through EF Core execution strategies or provider configuration, prefer that, and handle transaction/retry interaction according to the provider's EF Core guidance. HTTP retry policies are not database policies."
  - `.claude/skills/httpclient-factory/references/resilience.md:69-79` (DUPLICATE, K0-S001156): "| Scenario | Consideration | ⏎ |---|---| ⏎ | External I/O | Bounded execution time | ⏎ | Safe transient HTTP failure | Consider retry | ⏎ | Unsafe write | No retry unless duplicate-safe | ⏎ | `429` from dependency | Honor `Retry-After` where appropriate | ⏎ | Repeated dependency outage | Consider circuit breaker | ⏎ | Optional data unavailable | Consider explicit fallback | ⏎ | Latency-sensitive idempotent read |"

### EXTRA-K0-0033
- Closest oracle policies: RUN-005
- Modality: MUST
- Normative action: Per-request values such as dynamic access tokens go on the request or through a handler; mutating a shared client's DefaultRequestHeaders concurrently for request-specific values is a race (stable media-type headers may be configured on the client).
- Trigger/scope: Outbound HttpClient usage
- Exceptions: stable headers
- Why EXTRA: RUN-005 governs client lifetime only; no oracle policy restricts how request-specific headers are applied.
- Evidence:
  - `.claude/skills/httpclient-factory/SKILL.md:115-115` (MIXED, K0-S001187): "mutating shared `DefaultRequestHeaders` concurrently for request-specific values is a race"
  - `.claude/skills/httpclient-factory/SKILL.md:132-132` (DUPLICATE, K0-S001193): "New `HttpClient` per request; mandating one client model everywhere; retrying unsafe operations without idempotency analysis; unbounded retries; leaking `HttpResponseMessage` across boundaries; ignoring cancellation; dynamic tokens in shared default headers; mapping every upstream failure to the same status; resilience pipelines added without understanding them."

### EXTRA-K0-0034
- Closest oracle policies: DEP-008, DEP-022, DEP-023
- Modality: MUST (scaffolding)
- Normative action: Scaffolding creates the repository-wide files global.json (pinning the intended supported .NET SDK line: current stable SDK of the target release with a chosen rollForward servicing policy), .editorconfig, .gitignore and README.md alongside the .slnx and Directory.*.props files.
- Trigger/scope: New solution scaffolding
- Exceptions: none stated
- Why EXTRA: DEP-022/DEP-023 cover the solution format and Directory.*.props; no oracle policy requires a global.json SDK pin, .editorconfig, .gitignore or README.md at scaffolding.
- Evidence:
  - `.claude/skills/project-structure/references/solution-layout.md:60-60` (MIXED, K0-S001367): "pin the intended supported .NET SDK line"
  - `.claude/skills/project-structure/SKILL.md:22-22` (MIXED, K0-S001382): "`global.json`, `.editorconfig`, `.gitignore`, `README.md`"

### EXTRA-K0-0035
- Closest oracle policies: none
- Modality: SHOULD
- Normative action: Keep the always-loaded surface (CLAUDE.md, the register, skill descriptions) compact and move detail to the owner it belongs to.
- Trigger/scope: Instruction-system maintenance
- Exceptions: none stated
- Why EXTRA: Context-budget rule of the template; no V2 policy.
- Evidence:
  - `.claude/skills/template-maintenance/SKILL.md:47-47` (EXTRA, K0-S001582): "5. Keep the always-loaded surface (CLAUDE.md, the register, skill descriptions) compact; move detail to the owner it belongs to."

### EXTRA-K0-0036
- Closest oracle policies: none
- Modality: MUST
- Normative action: When hooks or scripts change, exercise them with a sample payload (e.g. a pre-tool-use JSON for 'npm install lodash').
- Trigger/scope: Hook/script maintenance
- Exceptions: none stated
- Why EXTRA: Template-maintenance testing duty; no V2 policy concerns hook scripts.
- Evidence:
  - `.claude/skills/template-maintenance/SKILL.md:52-52` (EXTRA, K0-S001585): "2. When hooks or scripts changed, exercise them with a sample payload, for example:"

### EXTRA-K0-0037
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Template maintenance summarizes what moved, the new owners and the checker result.
- Trigger/scope: End of template-maintenance
- Exceptions: none stated
- Why EXTRA: Workflow-specific report content; not a V2 policy.
- Evidence:
  - `.claude/skills/template-maintenance/SKILL.md:58-58` (EXTRA, K0-S001587): "3. Summarize what moved, the new owners and the checker result."

### EXTRA-K0-0038
- Closest oracle policies: none
- Modality: MUST
- Normative action: Instruction precedence: CLAUDE.md and the decision register govern every task; standards govern the files they cover; workflows own procedures; knowledge skills supply technique and never override a standard.
- Trigger/scope: All tasks
- Exceptions: none stated
- Why EXTRA: Instruction-layer precedence of the template design; the oracle defines policies, not a precedence order among instruction artifacts.
- Evidence:
  - `CLAUDE.md:11-11` (EXTRA, K0-S001632): "- This file and the decision register govern every task. Standards in `.claude/rules/<scope>/` govern the files they cover. Workflows own procedures; knowledge skills supply technique and never override a standard."

### EXTRA-K0-0039
- Closest oracle policies: none
- Modality: MUST (vocabulary semantics, always loaded)
- Normative action: Vocabulary: must / must not — a violation is a defect; default — deviation needs a concrete reason and must be reported; prefer / avoid — guidance; requires approval — a Reserved decision.
- Trigger/scope: All normative text and deviations from defaults
- Exceptions: none stated
- Why EXTRA: The oracle grades policies but defines no duty to report each deviation from a default; the reporting duty changes how every default binds.
- Evidence:
  - `CLAUDE.md:13-13` (EXTRA, K0-S001634): "- Vocabulary: **must / must not** — a violation is a defect; **default** — deviation needs a concrete reason and must be reported; **prefer / avoid** — guidance; **requires approval** — a Reserved decision (below)."

### EXTRA-K0-0040
- Closest oracle policies: GOV-017, ARC-020
- Modality: MUST (classification test)
- Normative action: Unclear decisions are Reserved if any answer is yes: adds, removes or replaces a dependency, framework or infrastructure capability; changes a project, layer or reference boundary; establishes a convention other code must follow; changes observable behavior or a public contract; becomes expensive to reverse.
- Trigger/scope: Unclear decisions
- Exceptions: none stated
- Why EXTRA: GOV-017 requires classification and ARC-020 lists consequential choices, but neither contains this test; its first question makes unclear dependency additions/removals approval-gated beyond DEP-001..DEP-005.
- Evidence:
  - `CLAUDE.md:47-47` (EXTRA, K0-S001662): "- Unclear? Any "yes" makes it Reserved: Does it add, remove or replace a dependency, framework or infrastructure capability? Change a project, layer or reference boundary? Establish a convention other code must follow? Change observable behavior or a public contract? Become expensive to reverse once other code depends on it?"

### EXTRA-K0-0041
- Closest oracle policies: DEP-023, RUN-009
- Modality: DEFAULT (effective MSBuild default)
- Normative action: Shared build configuration enables Nullable reference types, ImplicitUsings and AnalysisLevel latest for every .NET project below the root.
- Trigger/scope: .NET projects
- Exceptions: Projects may override.
- Why EXTRA: DEP-023 places shared settings but no oracle policy chooses nullable reference types, implicit usings or the latest analyzer level; the template makes them effective defaults.
- Evidence:
  - `Directory.Build.props:6-8` (EXTRA, K0-S001681): "<Nullable>enable</Nullable> ⏎     <ImplicitUsings>enable</ImplicitUsings> ⏎     <AnalysisLevel>latest</AnalysisLevel>"

## LINK_UNCERTAIN (2)

### UNCERTAIN-K0-0001
- Closest oracle policies: GOV-015, DEP-007
- Modality: MUST (imperative in a standard)
- Normative action: 'Commit package.json and package-lock.json, and keep the lockfile consistent with every dependency change.'
- Trigger/scope: npm manifests (rule loads for manifests)
- Exceptions: none stated
- Open question: Open question: read literally, the standard instructs a git commit of the manifests, which GOV-015 permits only on explicit request; read as 'keep them under version control', it restates DEP-007. The imperative wording does not settle which.
- Evidence:
  - `.claude/rules/common/dependencies.md:28-28` (MIXED, K0-S000267): "Commit `package.json` and `package-lock.json`"

### UNCERTAIN-K0-0002
- Closest oracle policies: GOV-015
- Modality: MAY (exception)
- Normative action: High-risk Git operations may run when 'required by an approved workflow', not only when explicitly requested.
- Trigger/scope: Destructive Git operations
- Exceptions: none stated
- Open question: Open question: GOV-015 requires an explicit request for repository-changing Git operations; whether 'required by an approved workflow' means a workflow the user explicitly requested (entailed) or allows destructive operations without a specific request (relaxation) is not determinable from the text.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:73-73` (MIXED, K0-S001051): "or required by an approved workflow"

