# EXTRA and LINK_UNCERTAIN constraints — candidate M

Generated deterministically from the annotation ledger. Each entry cites the exact
source evidence (path, line range, verbatim quote). `policy_ids` on an EXTRA entry
name the closest oracle policy only; origin stays EXTRA.

## EXTRA constraints (221)

### EXTRA-M-0033
- Closest oracle policies: DEP-025
- Modality: ENFORCED
- Normative action: The npm bypass block applies unconditionally (no exception path), including setting the npm config key without any install.
- Trigger/scope: executable hook on Bash/PowerShell tool calls (registered in settings.json)
- Exceptions: none
- Why EXTRA: DEP-025 forbids using the flags 'merely to bypass incompatible peer dependencies'; the hook blocks every such use regardless of purpose and also blocks the config change itself.
- Evidence M-S000398: `output/template/.claude/hooks/dependency-guard.mjs:80-82` — "const BYPASS_FLAG = /^(--force|-f|--legacy-peer-deps)(=(.*))?$/i; ⏎ const BYPASS_CONFIG_KEY = /legacy-peer-deps|^force(=|$)/i; ⏎ const BYPASS_ENV = /\bnpm_config_(force|legacy_peer_deps)\s*=/i;"
- Evidence M-S000402: `output/template/.claude/hooks/dependency-guard.mjs:99-105` — "if (BYPASS_ENV.test(command) && npmSegments.some((segment) => NPM_INSTALL_LIKE.has(segment.npm.sub))) { ⏎     blockTool( ⏎       'Blocked: the command sets npm_config_force or npm_config_legacy_peer_deps for an npm install, which ' + ⏎       'bypasses npm peer-dependency resolution. Resolve the actual compatibility problem instead; see ' + ⏎       '.claude/skills/add-dependency/SKILL.md (Apply, np …"
- Evidence M-S000403: `output/template/.claude/hooks/dependency-guard.mjs:106-116` — "for (const { npm, text } of npmSegments) { ⏎     const bypassFlag = npm.options.some(isBypassFlag); ⏎     const bypassConfig = NPM_CONFIG.includes(npm.sub) && ⏎       (npm.positionals.some((arg) => BYPASS_CONFIG_KEY.test(arg)) || npm.options.some((arg) => /legacy-peer-deps/i.test(arg))); ⏎     if ((NPM_INSTALL_LIKE.has(npm.sub) && bypassFlag) || bypassConfig) { ⏎       blockTool( ⏎         `Blocke …"

### EXTRA-M-0034
- Closest oracle policies: ARC-020, ARC-001
- Modality: ENFORCED_ADVISORY
- Normative action: When a project or package-version manifest is removed, Claude is told the change goes through CLAUDE.md Decision Control.
- Trigger/scope: executable hook on Bash/PowerShell tool calls (registered in settings.json)
- Exceptions: none
- Why EXTRA: Treats removal of a project/manifest file as a Reserved-decision matter; the oracle gates new projects and architecture changes but not removal of manifests per se.
- Evidence M-S000412: `output/template/.claude/hooks/dependency-guard.mjs:169-170` — "(removed.length > 0 ? '; a removed project or package-version file changes the project graph or dependency set, ' + ⏎         'which goes through CLAUDE.md § Decision Control' : '');"

### EXTRA-M-0035
- Closest oracle policies: TST-009, TST-010
- Modality: ENFORCED_ADVISORY
- Normative action: At Stop, if frontend production .ts files changed without any .spec.ts/e2e change, the same test-coverage reminder is raised.
- Trigger/scope: executable Stop hook (end of each Claude turn) in a Git working tree
- Exceptions: none
- Why EXTRA: Oracle TST-009/TST-010 are scoped to backend tests; extending the test-change reminder to frontend production code is additional.
- Evidence M-S000462: `output/template/.claude/hooks/stop-co-change.mjs:74-74` — "const frontendGap = changed.some(isFrontendProduction) && !changed.some(isFrontendTest);"
- Evidence M-S000463: `output/template/.claude/hooks/stop-co-change.mjs:75-78` — "if (backendGap || frontendGap) { ⏎   reminders.push('Production code changed without test changes: confirm regression coverage for bug fixes and that ' + ⏎     'behavioral probes are preserved as maintained tests (development-workflow, Bug fixes; verify, step 4).'); ⏎ }"

### EXTRA-M-0036
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: The Stop hook returns decision:block once per change-set state; Claude must address each reminder or briefly state why it does not apply before finishing.
- Trigger/scope: executable Stop hook (end of each Claude turn) in a Git working tree
- Exceptions: Shown once per distinct state; suppressed while stop_hook_active.
- Why EXTRA: Imposes a turn-completion gate (address-or-justify each co-change reminder) that the oracle does not require; the oracle policies only require the underlying co-changes/reviews.
- Evidence M-S000466: `output/template/.claude/hooks/stop-co-change.mjs:103-107` — "respond({ ⏎   decision: 'block', ⏎   reason: 'Co-change check (shown once for this set of changes):\n- ' + reminders.join('\n- ') + ⏎     '\nAddress each item or state briefly why it does not apply, then finish.', ⏎ });"

### EXTRA-M-0001
- Closest oracle policies: none
- Modality: MUST
- Normative action: Keep normative policy in rules and CLAUDE.md, procedures/stop conditions/output shape in workflow skills, technique/examples only in knowledge skills, mechanical checks in hooks/scripts/config; a pointer or check-by-reference is never a second owner.
- Trigger/scope: instruction-system maintenance (MAP.md read by maintainers / user-invoked template-maintenance skill; never loaded into Claude context)
- Exceptions: none
- Why EXTRA: Instruction-system ownership discipline (repo/meta); the oracle's 196 policies govern engineering behaviour, not where instruction content may be placed.
- Evidence M-S000006: `output/template/.claude/MAP.md:22-26` — "Responsibility split: rules and `CLAUDE.md` hold normative policy (must / must ⏎ not / default / requires approval); workflow skills hold procedures, stop ⏎ conditions, and output shape; knowledge skills hold technique and examples only; ⏎ hooks, scripts, and configuration enforce what is mechanically checkable. A ⏎ pointer ("run X", "see Y") or a yes/no check-by-reference is never a second owner."
- Evidence M-S001923: `output/template/.claude/skills/template-maintenance/SKILL.md:28-29` — "- Knowledge skills and private references hold technique only; they never own a ⏎   must/must-not policy. A private reference is read only by its owning skill."

### EXTRA-M-0002
- Closest oracle policies: none
- Modality: MUST
- Normative action: Place new instruction content by kind: planning-time governance/decisions in CLAUDE.md or docs/technology-stack.md (kept compact); area constraints in the matching flat rule (new rule only when no topic/paths fit, paths covering at least the needed scope); procedures in workflow skills; technique in knowledge skills/references; mechanically checkable items in scripts/hooks plus a concise naming rule.
- Trigger/scope: instruction-system maintenance (MAP.md read by maintainers / user-invoked template-maintenance skill; never loaded into Claude context)
- Exceptions: New flat rule allowed when no existing rule fits.
- Why EXTRA: Repo/meta placement rule for instruction maintenance; not entailed by any oracle policy.
- Evidence M-S000009: `output/template/.claude/MAP.md:32-35` — "| File | Owns | Scope | Enforcement | Extend here when… | ⏎ | --- | --- | --- | --- | --- | ⏎ | `CLAUDE.md` | Product-source governance, custom-settings governance, core defaults, challenge obligation, architecture defaults (decision summary, layout, patterns not adopted), decision control, Git boundaries, workflow routing | common | `check-instructions.mjs` (imports, header) | A rule must be know …"
- Evidence M-S000011: `output/template/.claude/MAP.md:39-51` — "| File | Owns | Scope | `paths` | Enforcement | Extend here when… | ⏎ | --- | --- | --- | --- | --- | --- | ⏎ | `.claude/rules/architecture.md` | Dependency direction, project and test references, Domain/Application/API responsibilities, repositories, Unit of Work, EF Core boundary, composition and DI, typed options, Serilog registration, boundary contracts | backend, backend-tests | `backend/**/* …"
- Evidence M-S000013: `output/template/.claude/MAP.md:55-70` — "| File | Owns | Scope | Loads | Enforcement | Extend here when… | ⏎ | --- | --- | --- | --- | --- | --- | ⏎ | `.claude/skills/development-workflow/SKILL.md` | Implementation step order, specification read, behavior-source sync, persistence co-change and migration review, regression tests, performance-change procedure, generated output, API deprecation, CI/CD and production migrations, review and v …"
- Evidence M-S000016: `output/template/.claude/MAP.md:79-99` — "| File | Technique for | Scope | Extend here when… | ⏎ | --- | --- | --- | --- | ⏎ | `.claude/skills/ef-core/SKILL.md` | DbContext, repositories/UoW implementation, queries, migrations commands, seeder implementation | backend | EF Core how-to or example | ⏎ | `.claude/skills/http-api/SKILL.md` | Status-code reference, idempotency, ETags, headers | backend | HTTP example or less-common status deta …"
- Evidence M-S000026: `output/template/.claude/MAP.md:198-209` — "1. Needed while planning, before any file is opened (governance, approval ⏎    boundary, architecture or technology decision) → `CLAUDE.md` or ⏎    `docs/technology-stack.md`. Keep these compact. ⏎ 2. A constraint on files of an area → the matching rule in `.claude/rules/`; add ⏎    a new flat rule only when no existing rule's topic and `paths` fit, and ⏎    declare `paths` covering at least the s …"
- Evidence M-S001929: `output/template/.claude/skills/template-maintenance/SKILL.md:52-53` — "Find the current owner and the right location with `.claude/MAP.md`"

### EXTRA-M-0003
- Closest oracle policies: none
- Modality: MUST
- Normative action: After placing new instruction content, update MAP.md and run node .claude/scripts/check-instructions.mjs from the repository root.
- Trigger/scope: instruction-system maintenance (MAP.md read by maintainers / user-invoked template-maintenance skill; never loaded into Claude context)
- Exceptions: none
- Why EXTRA: Repo/meta maintenance obligation not in the oracle.
- Evidence M-S000027: `output/template/.claude/MAP.md:210-212` — "6. Then update this map and, from the repository root ⏎    (`git rev-parse --show-toplevel`), run ⏎    `node .claude/scripts/check-instructions.mjs` (`/template-maintenance`)."
- Evidence M-S001931: `output/template/.claude/skills/template-maintenance/SKILL.md:55-55` — "3. Update `.claude/MAP.md` (file table and topic index)."
- Evidence M-S001932: `output/template/.claude/skills/template-maintenance/SKILL.md:56-61` — "run the"

### EXTRA-M-0004
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: Keep status-code behaviour consistent across similar endpoints.
- Trigger/scope: path-scoped: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Cross-endpoint consistency obligation; oracle API policies define per-outcome semantics and stable error contracts but not consistency across similar endpoints.
- Evidence M-S000059: `output/template/.claude/rules/api.md:29-29` — "- Keep status-code behavior consistent across similar endpoints."
- Evidence M-S001354: `output/template/.claude/skills/http-api/SKILL.md:78-81` — "Choose consistently whether a repeated `DELETE` of an already absent resource ⏎ returns `204` (the desired final state holds) or `404` (the addressed resource ⏎ does not exist); either can be valid, but do not mix them between equivalent ⏎ resources."

### EXTRA-M-0005
- Closest oracle policies: ARC-028, DEP-013
- Modality: DEFAULT
- Normative action: Backend test projects follow the canonical set <Name>.Domain.Tests (optional), <Name>.Application.Tests, <Name>.IntegrationTests, <Name>.Infrastructure.Tests (optional).
- Trigger/scope: path-scoped: backend/**/*.cs, backend/**/*.csproj
- Exceptions: Domain.Tests and Infrastructure.Tests optional.
- Why EXTRA: Oracle constrains test references and location but not test-project naming/roles; this fixes a naming convention (also relied on by check-manifests).
- Evidence M-S000082: `output/template/.claude/rules/architecture.md:40-44` — "- `<Name>.Domain.Tests` (optional) → `Domain`; ⏎ - `<Name>.Application.Tests` → `Application`, and `Domain` as needed; ⏎ - `<Name>.IntegrationTests` → `Api` (for `WebApplicationFactory<Program>`); ⏎ - `<Name>.Infrastructure.Tests` (optional) → `Infrastructure`, narrower ⏎   references as required."
- Evidence M-S000503: `output/template/.claude/scripts/check-manifests.mjs:297-300` — "if (!source.layer) { ⏎       result.notes.push({ file: rel, message: `reference to ${targetName} not checked: tested layer of "${projectName}" is unknown (use <Name>.<Layer>.Tests or <Name>.IntegrationTests)` }); ⏎       continue; ⏎     }"
- Evidence M-S001674: `output/template/.claude/skills/project-structure/references/solution-layout.md:66-75` — "```text ⏎ ProjectName.Domain.Tests        optional; non-trivial behavior that genuinely ⏎                                 belongs to Domain ⏎ ProjectName.Application.Tests   application-service and use-case behavior ⏎ ProjectName.IntegrationTests    API + Application + Infrastructure integration ⏎                                 (references the Api project for ⏎                                 Web …"
- Evidence M-S001713: `output/template/.claude/skills/project-structure/SKILL.md:88-94` — "Create only useful test projects, placed as CLAUDE.md § Architecture Defaults ⏎ describes — typically `<Name>.Application.Tests` and `<Name>.IntegrationTests`. Create `<Name>.Domain.Tests` only when Domain contains ⏎ non-trivial behavior worth testing independently — a Domain made mainly of ⏎ entities and enums does not need one — and `<Name>.Infrastructure.Tests` only ⏎ for a concrete testing nee …"

### EXTRA-M-0006
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Primary constructors fit DI or simple clear initialization; use a regular constructor when validation/initialization is non-trivial, explicit fields improve readability, the codebase uses that style, or parameter capture hurts understanding.
- Trigger/scope: path-scoped: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Constructor-style selection criteria; oracle (RUN-009, EXC-002/EXC-003) leaves constructor preferences outside the policy set.
- Evidence M-S000129: `output/template/.claude/rules/coding-style.md:32-36` — "- Primary constructors fit dependency injection or simple initialization that ⏎   stays clear. Use a regular constructor when validation or initialization is ⏎   non-trivial, explicit fields improve readability, the codebase consistently ⏎   uses that style, or parameter capture would make the class harder to ⏎   understand. Do not convert constructors mechanically."

### EXTRA-M-0007
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Use records when value semantics/immutability are desirable (many DTOs, genuine Value Objects) and classes when identity, mutable lifecycle, inheritance or framework behaviour fit; do not turn every DTO or Domain type into a record.
- Trigger/scope: path-scoped: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Record/class selection style rule not in the oracle (EXC-003 lists record preferences as outside it).
- Evidence M-S000130: `output/template/.claude/rules/coding-style.md:37-40` — "- Use records when value semantics and immutability are desirable (many DTOs, ⏎   genuine Value Objects); use classes when identity, mutable lifecycle, ⏎   inheritance, or framework behavior makes class semantics clearer. Do not turn ⏎   every DTO or Domain type into a record."

### EXTRA-M-0008
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Keep implementation details non-public unless part of the public API; use sealed to communicate deliberate non-inheritance, not as speculative JIT optimization.
- Trigger/scope: path-scoped: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Visibility/sealed conventions are not in the oracle.
- Evidence M-S000131: `output/template/.claude/rules/coding-style.md:41-44` — "- Keep implementation details non-public when they are not part of the ⏎   project's public API. Use `sealed` when the type is deliberately not meant for ⏎   inheritance and the modifier communicates that intent, not as a speculative ⏎   JIT optimization."

### EXTRA-M-0009
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Use var when the type is obvious or unimportant; explicit type when it improves clarity.
- Trigger/scope: path-scoped: backend/**/*.cs
- Exceptions: none
- Why EXTRA: Type-inference style convention outside the oracle.
- Evidence M-S000133: `output/template/.claude/rules/coding-style.md:48-49` — "- Use `var` when the type is obvious from the right-hand side or unimportant to ⏎   understanding the code; use an explicit type when it improves clarity."
- Evidence M-S002002: `output/template/.editorconfig:40-42` — "csharp_style_var_when_type_is_apparent = true:suggestion ⏎ csharp_style_var_for_built_in_types = false:silent ⏎ csharp_style_var_elsewhere = false:silent"

### EXTRA-M-0010
- Closest oracle policies: RUN-009
- Modality: MUST
- Normative action: Use standard .NET naming (PascalCase types/methods/properties/public members, camelCase parameters/locals, meaningful names); private-field naming follows the repository convention.
- Trigger/scope: path-scoped: backend/**/*.cs
- Exceptions: Private-field naming follows established repository convention.
- Why EXTRA: Concrete naming convention not stated in any oracle policy (RUN-009 only defers to existing conventions).
- Evidence M-S000134: `output/template/.claude/rules/coding-style.md:50-53` — "- Use standard .NET naming: PascalCase for types, methods, properties, and public ⏎   members; camelCase for parameters and locals; meaningful names over ⏎   abbreviations. Private-field naming follows the repository's established ⏎   convention."
- Evidence M-S002006: `output/template/.editorconfig:51-56` — "dotnet_naming_rule.interfaces_begin_with_i.symbols = interfaces ⏎ dotnet_naming_rule.interfaces_begin_with_i.style = begin_with_i ⏎ dotnet_naming_rule.interfaces_begin_with_i.severity = warning ⏎ dotnet_naming_symbols.interfaces.applicable_kinds = interface ⏎ dotnet_naming_style.begin_with_i.required_prefix = I ⏎ dotnet_naming_style.begin_with_i.capitalization = pascal_case"
- Evidence M-S002010: `output/template/.editorconfig:68-72` — "dotnet_naming_rule.types_and_members_pascal.symbols = types_and_members ⏎ dotnet_naming_rule.types_and_members_pascal.style = pascal_case_style ⏎ dotnet_naming_rule.types_and_members_pascal.severity = suggestion ⏎ dotnet_naming_symbols.types_and_members.applicable_kinds = class, struct, interface, enum, delegate, method, property, event ⏎ dotnet_naming_style.pascal_case_style.capitalization = pasc …"
- Evidence M-S002012: `output/template/.editorconfig:76-80` — "dotnet_naming_rule.parameters_and_locals_camel.symbols = parameters_and_locals ⏎ dotnet_naming_rule.parameters_and_locals_camel.style = camel_case_style ⏎ dotnet_naming_rule.parameters_and_locals_camel.severity = suggestion ⏎ dotnet_naming_symbols.parameters_and_locals.applicable_kinds = parameter, local ⏎ dotnet_naming_style.camel_case_style.capitalization = camel_case"

### EXTRA-M-0011
- Closest oracle policies: RUN-011
- Modality: AVOID
- Normative action: Avoid mixing large formatting or modernization changes with functional work.
- Trigger/scope: path-scoped: backend/**/*.cs
- Exceptions: none
- Why EXTRA: RUN-011 limits style rewrites outside the requested change; avoiding large formatting/modernization changes mixed into functional work within the change is additional.
- Evidence M-S000138: `output/template/.claude/rules/coding-style.md:62-64` — "Do not perform style-only rewrites outside the requested change unless ⏎ explicitly asked, and avoid mixing large formatting or modernization changes ⏎ with functional work. Removing unused `using` directives from changed files is a"

### EXTRA-M-0012
- Closest oracle policies: API-007, API-011
- Modality: MUST
- Normative action: Catch an exception only when the current layer can recover, translate it into its own abstraction-level outcome, perform a defined fallback, add context while preserving the original exception, or perform required cleanup.
- Trigger/scope: path-scoped: backend/**/*.cs
- Exceptions: The five enumerated purposes.
- Why EXTRA: API-007 discourages repetitive catch/log/rethrow; a closed whitelist of acceptable catch purposes forbids any other catch (stricter than the oracle).
- Evidence M-S000158: `output/template/.claude/rules/error-handling.md:22-27` — "- Unexpected failures propagate to centralized `IExceptionHandler` handling by ⏎   default. Avoid broad `try/catch` blocks in Controllers, Application Services, ⏎   or repositories that only log and rethrow. Catch an exception only when the ⏎   current layer can recover, translate it into its own abstraction-level ⏎   outcome, perform a defined fallback, add useful context while preserving the ⏎   …"
- Evidence M-S000750: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:170-174` — "Catch an external-service exception locally only when the layer can do something ⏎ meaningful — translate it into an Application outcome, add useful context, ⏎ perform a defined fallback, or apply an appropriate retry policy at the ⏎ infrastructure boundary. Otherwise let it propagate to centralized handling; do ⏎ not swallow it."

### EXTRA-M-0013
- Closest oracle policies: TST-005
- Modality: PREFER
- Normative action: Prefer one observable scenario per test; a multi-step test only when the sequence itself is the behaviour.
- Trigger/scope: path-scoped: backend/**/*Tests/**/*.cs, backend/**/*Tests/*.csproj
- Exceptions: Multi-step test when the sequence is the behaviour.
- Why EXTRA: Test-shape preference not entailed by TST-005 (which concerns explicit cases vs computed case machinery).
- Evidence M-S000269: `output/template/.claude/rules/testing.md:45-48` — "For small finite input or state spaces, prefer explicit declarative cases (for ⏎ example `[TestCase]`) over loops, branches, LINQ, generated case machinery, or ⏎ code that computes the expected result. Prefer one observable scenario per test; ⏎ a multi-step test fits when the sequence itself is the behavior."

### EXTRA-M-0014
- Closest oracle policies: TST-012
- Modality: DEFAULT
- Normative action: Default test-name pattern MethodOrScenario_Condition_ExpectedBehavior.
- Trigger/scope: path-scoped: backend/**/*Tests/**/*.cs, backend/**/*Tests/*.csproj
- Exceptions: Unless the project already has an established convention.
- Why EXTRA: TST-012 requires descriptive names but no specific pattern; the pattern is an added default.
- Evidence M-S000278: `output/template/.claude/rules/testing.md:72-75` — "Use descriptive test names that communicate the scenario or condition and the ⏎ expected behavior. The default pattern is ⏎ `MethodOrScenario_Condition_ExpectedBehavior` unless the project already has an ⏎ established convention."

### EXTRA-M-0042
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: CLAUDE.md, docs/technology-stack.md, .claude/MAP.md, .claude/settings.json, .claude/agents/code-reviewer.md, SPECIFICATION.md and CUSTOM_SETTINGS.md must exist (failure otherwise).
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: none
- Why EXTRA: Instruction-system structural invariant (repo/meta), not an oracle engineering policy.
- Evidence M-S000537: `output/template/.claude/scripts/check-instructions.mjs:27-30` — "const REQUIRED_FILES = [ ⏎   'CLAUDE.md', 'docs/technology-stack.md', '.claude/MAP.md', '.claude/settings.json', ⏎   '.claude/agents/code-reviewer.md', 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md', ⏎ ];"
- Evidence M-S000547: `output/template/.claude/scripts/check-instructions.mjs:66-66` — "missing required file"

### EXTRA-M-0043
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: The workflow skills (development-workflow, project-structure, verify, code-review, build-fix, custom-settings, git-workflow, security-scan, add-dependency, architecture-decision, template-maintenance) and knowledge skills (ef-core, http-api, aspnet-error-handling, dotnet-testing, logging, httpclient-factory, configuration, dependency-injection, caching, swagger, api-versioning, health-check, docker, ci-cd, angular, modern-csharp, authentication) must exist; skills named serilog or resilience are forbidden.
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: none
- Why EXTRA: Repo/meta skill-inventory invariant not present in the oracle.
- Evidence M-S000538: `output/template/.claude/scripts/check-instructions.mjs:31-39` — "const WORKFLOW_SKILLS = [ ⏎   'development-workflow', 'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings', ⏎   'git-workflow', 'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance', ⏎ ]; ⏎ const KNOWLEDGE_SKILLS = [ ⏎   'ef-core', 'http-api', 'aspnet-error-handling', 'dotnet-testing', 'logging', 'httpclient-factory', ⏎   'configuration', 'depen …"
- Evidence M-S000539: `output/template/.claude/scripts/check-instructions.mjs:40-40` — "const FORBIDDEN_SKILLS = ['serilog', 'resilience'];"
- Evidence M-S000560: `output/template/.claude/scripts/check-instructions.mjs:157-162` — "for (const required of [...WORKFLOW_SKILLS, ...KNOWLEDGE_SKILLS]) { ⏎   if (!skillNames.includes(required)) fail(`missing required skill .claude/skills/${required}`); ⏎ } ⏎ for (const forbidden of FORBIDDEN_SKILLS) { ⏎   if (skillNames.includes(forbidden)) fail(`.claude/skills/${forbidden} competes with an existing knowledge skill; keep that depth as a private reference`); ⏎ }"

### EXTRA-M-0044
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: CLAUDE.md must import docs/technology-stack.md and only that file; imports must resolve; no other instruction file may contain an @ import.
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: none
- Why EXTRA: Repo/meta loading invariant.
- Evidence M-S000540: `output/template/.claude/scripts/check-instructions.mjs:41-41` — "const ALLOWED_IMPORTS = ['docs/technology-stack.md'];"
- Evidence M-S000553: `output/template/.claude/scripts/check-instructions.mjs:105-114` — "const claude = existsSync(abs('CLAUDE.md')) ? read('CLAUDE.md') : ''; ⏎ const imports = importsOf(claude); ⏎ for (const imp of imports) { ⏎   if (!ALLOWED_IMPORTS.includes(imp)) fail(`CLAUDE.md imports ${imp}; only ${ALLOWED_IMPORTS.join(', ')} may be imported`); ⏎   if (!existsSync(abs(imp))) fail(`CLAUDE.md import does not resolve: ${imp}`); ⏎ } ⏎ for (const required of ALLOWED_IMPORTS) if (!imp …"
- Evidence M-S001924: `output/template/.claude/skills/template-maintenance/SKILL.md:30-33` — "- Every instruction file starts with the one-line ⏎   `> Owns: ... | Scope: ... | Loads: ...` header; every rule declares `paths`; ⏎   `.claude/rules/` stays flat. CLAUDE.md imports only ⏎   `docs/technology-stack.md`."

### EXTRA-M-0045
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Every instruction file's first non-frontmatter line must be '> Owns: … | Scope: … | Loads: …' with Loads 'path-scoped' for rules, 'private reference' for references, 'on demand' for knowledge skills, 'workflow' or 'user-invoked' for workflow skills.
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: none
- Why EXTRA: Repo/meta header convention.
- Evidence M-S000541: `output/template/.claude/scripts/check-instructions.mjs:42-42` — "const HEADER = /^> Owns: .+ \| Scope: .+ \| Loads: .+$/;"
- Evidence M-S000555: `output/template/.claude/scripts/check-instructions.mjs:117-132` — "for (const file of existingInstructionFiles) { ⏎   const { body } = splitFrontmatter(read(file)); ⏎   const firstLine = body.split(/\r?\n/).find((line) => line.trim() !== '') ?? ''; ⏎   if (!HEADER.test(firstLine.trim())) { ⏎     fail(`${file}: first line after frontmatter must be "> Owns: ... | Scope: ... | Loads: ..."`); ⏎   } else { ⏎     const loads = firstLine.split('| Loads:')[1].toLowerCase …"
- Evidence M-S001924: `output/template/.claude/skills/template-maintenance/SKILL.md:30-33` — "- Every instruction file starts with the one-line ⏎   `> Owns: ... | Scope: ... | Loads: ...` header; every rule declares `paths`; ⏎   `.claude/rules/` stays flat. CLAUDE.md imports only ⏎   `docs/technology-stack.md`."

### EXTRA-M-0046
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: No instruction file may contain Level: or Kind: classification lines.
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: none
- Why EXTRA: Repo/meta architecture-identity invariant (anti-leakage), not an oracle policy.
- Evidence M-S000556: `output/template/.claude/scripts/check-instructions.mjs:133-136` — "for (const line of read(file).split(/\r?\n/)) { ⏎     if (/^\s*(\*\*)?(Level|Kind)(\*\*)?\s*:/.test(line)) fail(`${file}: classification line "${line.trim()}" is not part of this instruction system`); ⏎   } ⏎ }"

### EXTRA-M-0047
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: .claude/rules/ must be flat, contain only Markdown, and each rule must declare a non-empty paths list.
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: none
- Why EXTRA: Repo/meta rule-layout invariant.
- Evidence M-S000558: `output/template/.claude/scripts/check-instructions.mjs:139-154` — "for (const entry of ruleFiles) { ⏎   const path = `.claude/rules/${entry}`; ⏎   if (statSync(abs(path)).isDirectory()) { ⏎     fail(`${path}: .claude/rules/ must stay flat (no subdirectories)`); ⏎     continue; ⏎   } ⏎   if (!entry.endsWith('.md')) { ⏎     fail(`${path}: rule files must be Markdown`); ⏎     continue; ⏎   } ⏎   const { data } = splitFrontmatter(read(path)); ⏎   const paths = data.p …"
- Evidence M-S001924: `output/template/.claude/skills/template-maintenance/SKILL.md:30-33` — "- Every instruction file starts with the one-line ⏎   `> Owns: ... | Scope: ... | Loads: ...` header; every rule declares `paths`; ⏎   `.claude/rules/` stays flat. CLAUDE.md imports only ⏎   `docs/technology-stack.md`."

### EXTRA-M-0048
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Agents are single Markdown files; a skill folder holds only SKILL.md and an optional references/ directory containing only Markdown; SKILL.md is mandatory.
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: none
- Why EXTRA: Repo/meta skill-shape invariant.
- Evidence M-S000549: `output/template/.claude/scripts/check-instructions.mjs:77-80` — "agents are single Markdown files"
- Evidence M-S000550: `output/template/.claude/scripts/check-instructions.mjs:81-101` — "a skill folder holds SKILL.md and optional references/"

### EXTRA-M-0049
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Skill frontmatter name equals the folder name; description present and ≤1024 characters; knowledge-skill descriptions start with 'Use when'; template-maintenance sets disable-model-invocation: true.
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: none
- Why EXTRA: Repo/meta skill-metadata invariant.
- Evidence M-S000561: `output/template/.claude/scripts/check-instructions.mjs:163-178` — "const descriptions = []; ⏎ for (const skill of skillNames) { ⏎   const path = `.claude/skills/${skill}/SKILL.md`; ⏎   if (!existsSync(abs(path))) continue; ⏎   const { data } = splitFrontmatter(read(path)); ⏎   if (data.name !== skill) fail(`${path}: frontmatter name "${data.name}" must equal the folder name`); ⏎   const description = typeof data.description === 'string' ? data.description.trim()  …"

### EXTRA-M-0050
- Closest oracle policies: WF-010
- Modality: ENFORCED
- Normative action: The code-reviewer agent body must stay ≤1500 characters (thin wrapper).
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: none
- Why EXTRA: Size limit on the agent file is a repo/meta invariant beyond WF-010.
- Evidence M-S000565: `output/template/.claude/scripts/check-instructions.mjs:187-187` — "if (body.length > 1500) fail(`${agentPath}: agent body should stay a thin wrapper (<= 1500 characters)`);"

### EXTRA-M-0051
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: A skill's references/*.md may be referenced only by its owning skill (MAP.md exempt) and must exist.
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: MAP.md exempt.
- Why EXTRA: Repo/meta privacy invariant for references.
- Evidence M-S000569: `output/template/.claude/scripts/check-instructions.mjs:197-208` — "// private references ⏎   for (const m of text.matchAll(/skills\/([a-z0-9-]+)\/references\/([A-Za-z0-9_.-]+\.md)/g)) { ⏎     if (file !== '.claude/MAP.md' && m[1] !== ownerSkill) fail(`${file}: references private reference ${m[0]} owned by ${m[1]}`); ⏎   } ⏎   for (const m of text.matchAll(/(?<![\w/])references\/([A-Za-z0-9_.-]+\.md)/g)) { ⏎     if (file === '.claude/MAP.md') continue; ⏎     if (! …"

### EXTRA-M-0052
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Backticked repo/doc paths, '§ Heading' section references and skill/agent routing targets in instruction files must resolve (docs/decisions and README.md exempt).
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: docs/decisions paths and README.md are exempt.
- Why EXTRA: Repo/meta reference-integrity invariant.
- Evidence M-S000570: `output/template/.claude/scripts/check-instructions.mjs:210-219` — "does not resolve"
- Evidence M-S000571: `output/template/.claude/scripts/check-instructions.mjs:221-235` — "section reference"
- Evidence M-S000572: `output/template/.claude/scripts/check-instructions.mjs:237-249` — "routes to unknown skill or agent"

### EXTRA-M-0053
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: MAP.md must list every instruction file, settings.json, every hook and every script.
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: none
- Why EXTRA: Repo/meta map-completeness invariant.
- Evidence M-S000574: `output/template/.claude/scripts/check-instructions.mjs:252-259` — "if (existsSync(abs('.claude/MAP.md'))) { ⏎   const map = read('.claude/MAP.md'); ⏎   const listed = [...existingInstructionFiles, '.claude/settings.json', ...listDir('.claude/hooks').map((f) => `.claude/hooks/${f}`), ⏎     ...listDir('.claude/scripts').map((f) => `.claude/scripts/${f}`)]; ⏎   for (const file of listed) { ⏎     if (file === '.claude/MAP.md') continue; ⏎     if (!map.includes(file)) …"

### EXTRA-M-0054
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: MAP.md must not be imported by CLAUDE.md.
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: none
- Why EXTRA: Repo/meta loading invariant (keeps MAP.md out of context).
- Evidence M-S000575: `output/template/.claude/scripts/check-instructions.mjs:260-261` — "if (importsOf(claude).some((imp) => imp.endsWith('MAP.md'))) fail('MAP.md must not be imported (it is human-facing only)'); ⏎ }"

### EXTRA-M-0055
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: Every settings.json hook must be a command hook in exec form ('node' plus exactly one argument '${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs'), the script must exist, and a script dispatching on hook_event_name must handle each registered event.
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: none
- Why EXTRA: Repo/meta hook-registration invariant.
- Evidence M-S000579: `output/template/.claude/scripts/check-instructions.mjs:276-305` — "const hookArg = /^\$\{CLAUDE_PROJECT_DIR\}\/\.claude\/hooks\/([A-Za-z0-9_.-]+\.mjs)$/; ⏎   const execForm = '"command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs"]'; ⏎   for (const [event, groups] of Object.entries(settings?.hooks ?? {})) { ⏎     for (const group of Array.isArray(groups) ? groups : []) { ⏎       for (const hook of group.hooks ?? []) { ⏎         const where …"
- Evidence M-S001926: `output/template/.claude/skills/template-maintenance/SKILL.md:36-46` — "- Hooks are registered in exec form — `"command": "node"` with ⏎   `"args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs"]`, never a shell ⏎   command string. The placeholder only locates the script; hooks derive the ⏎   repository root they inspect from the hook input (`cwd`, or the edited file's ⏎   location) and checkers from the current directory ⏎   (`.claude/scripts/repo-root.mjs`). Ho …"

### EXTRA-M-0056
- Closest oracle policies: DEP-025
- Modality: ENFORCED
- Normative action: PreToolUse hooks must set onFailure: block; non-PreToolUse (advisory) hooks must not.
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: none
- Why EXTRA: Enforces the fail-closed guard / fail-open advisory split as an instruction-system invariant (not an oracle policy).
- Evidence M-S000581: `output/template/.claude/scripts/check-instructions.mjs:310-314` — "if (event === 'PreToolUse' && hook.onFailure !== 'block') { ⏎           fail(`${where}: the policy guard must set "onFailure": "block" so a failing or timed-out guard blocks the tool call`); ⏎         } else if (event !== 'PreToolUse' && hook.onFailure === 'block') { ⏎           fail(`${where}: advisory hook must not set "onFailure": "block" (the event already happened; a failing Stop hook could l …"
- Evidence M-S001926: `output/template/.claude/skills/template-maintenance/SKILL.md:36-46` — "- Hooks are registered in exec form — `"command": "node"` with ⏎   `"args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs"]`, never a shell ⏎   command string. The placeholder only locates the script; hooks derive the ⏎   repository root they inspect from the hook input (`cwd`, or the edited file's ⏎   location) and checkers from the current directory ⏎   (`.claude/scripts/repo-root.mjs`). Ho …"

### EXTRA-M-0057
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: settings.json must register dependency-guard for PreToolUse, PostToolUse and PostToolUseFailure on Bash|PowerShell, file-change for PostToolUse on Edit|Write|MultiEdit, and stop-co-change for Stop.
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: none
- Why EXTRA: Repo/meta enforcement-wiring invariant.
- Evidence M-S000544: `output/template/.claude/scripts/check-instructions.mjs:47-53` — "const REQUIRED_HOOKS = [ ⏎   ['PreToolUse', ['Bash', 'PowerShell'], 'dependency-guard.mjs'], ⏎   ['PostToolUse', ['Bash', 'PowerShell'], 'dependency-guard.mjs'], ⏎   ['PostToolUseFailure', ['Bash', 'PowerShell'], 'dependency-guard.mjs'], ⏎   ['PostToolUse', ['Edit', 'Write', 'MultiEdit'], 'file-change.mjs'], ⏎   ['Stop', [], 'stop-co-change.mjs'], ⏎ ];"
- Evidence M-S000583: `output/template/.claude/scripts/check-instructions.mjs:318-327` — "required hook"
- Evidence M-S001926: `output/template/.claude/skills/template-maintenance/SKILL.md:36-46` — "- Hooks are registered in exec form — `"command": "node"` with ⏎   `"args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs"]`, never a shell ⏎   command string. The placeholder only locates the script; hooks derive the ⏎   repository root they inspect from the hook input (`cwd`, or the edited file's ⏎   location) and checkers from the current directory ⏎   (`.claude/scripts/repo-root.mjs`). Ho …"

### EXTRA-M-0058
- Closest oracle policies: none
- Modality: ENFORCED_WARNING
- Normative action: Warn when the always-loaded estimate (CLAUDE.md + imports + skill/agent descriptions) exceeds ~6000 tokens.
- Trigger/scope: executable: check-instructions.mjs run during template maintenance / CI over the instruction system (CLAUDE.md, docs/technology-stack.md, .claude/**)
- Exceptions: Warning only (does not fail).
- Why EXTRA: Context-budget threshold not in the oracle.
- Evidence M-S000542: `output/template/.claude/scripts/check-instructions.mjs:43-43` — "const BUDGET_WARN_TOKENS = 6000;"
- Evidence M-S000586: `output/template/.claude/scripts/check-instructions.mjs:331-335` — "exceeds"

### EXTRA-M-0037
- Closest oracle policies: DEP-020, DEP-004
- Modality: MUST_NOT
- Normative action: Microsoft.Extensions.Http.Polly and Polly.Extensions.Http are reported as violations (deprecated integration packages; must not be added).
- Trigger/scope: executable: check-manifests.mjs over **/*.csproj, Directory.Packages.props, package.json (excluding .claude, node_modules, bin, obj, dist, etc.); run by hooks after manifest edits/shell commands and by workflows/CI
- Exceptions: none
- Why EXTRA: DEP-020 makes Microsoft resilience the default and direct Polly an explicit exception; a hard executable ban on these two packages (violation, no exception path) is stricter than the oracle.
- Evidence M-S000474: `output/template/.claude/scripts/check-manifests.mjs:30-33` — "const DENIED_NUGET = new Map([ ⏎   ['microsoft.extensions.http.polly', 'deprecated integration package - see add-dependency (package choices)'], ⏎   ['polly.extensions.http', 'deprecated integration package - see add-dependency (package choices)'], ⏎ ]);"
- Evidence M-S000492: `output/template/.claude/scripts/check-manifests.mjs:219-223` — "function checkNuGetId(id, rel, result) { ⏎   const lower = id.toLowerCase(); ⏎   if (DENIED_NUGET.has(lower)) result.violations.push({ file: rel, message: `${id}: ${DENIED_NUGET.get(lower)}` }); ⏎   if (REVIEW_NUGET.has(lower)) result.notes.push({ file: rel, message: `${id}: ${REVIEW_NUGET.get(lower)}` }); ⏎ }"
- Evidence M-S000598: `output/template/.claude/skills/add-dependency/SKILL.md:25-31` — "- Resilience: when resilience is required, prefer ⏎     `Microsoft.Extensions.Http.Resilience` for `HttpClient` and ⏎     `Microsoft.Extensions.Resilience` for general resilience pipelines. Direct ⏎     Polly usage is an explicit exception rather than the default — use it only ⏎     when a concrete requirement cannot be expressed through those packages, and ⏎     document why. Do not add the depre …"

### EXTRA-M-0038
- Closest oracle policies: DEP-004, DEP-021
- Modality: ENFORCED_ADVISORY
- Normative action: Serilog.Sinks.Elasticsearch is flagged (note) as a deprecated sink package.
- Trigger/scope: executable: check-manifests.mjs over **/*.csproj, Directory.Packages.props, package.json (excluding .claude, node_modules, bin, obj, dist, etc.); run by hooks after manifest edits/shell commands and by workflows/CI
- Exceptions: none
- Why EXTRA: Package-specific advisory not entailed by the oracle (DEP-004 requires checking deprecation, but naming this sink as deprecated is candidate knowledge).
- Evidence M-S000480: `output/template/.claude/scripts/check-manifests.mjs:41-41` — "['serilog.sinks.elasticsearch', 'deprecated sink package - see the logging skill'],"
- Evidence M-S000492: `output/template/.claude/scripts/check-manifests.mjs:219-223` — "function checkNuGetId(id, rel, result) { ⏎   const lower = id.toLowerCase(); ⏎   if (DENIED_NUGET.has(lower)) result.violations.push({ file: rel, message: `${id}: ${DENIED_NUGET.get(lower)}` }); ⏎   if (REVIEW_NUGET.has(lower)) result.notes.push({ file: rel, message: `${id}: ${REVIEW_NUGET.get(lower)}` }); ⏎ }"
- Evidence M-S001545: `output/template/.claude/skills/logging/references/serilog.md:275-277` — "The `Serilog.Sinks.Elasticsearch` package is deprecated. Use the official ⏎ `Elastic.Serilog.Sinks` package, which writes ECS-formatted documents to data ⏎ streams:"

### EXTRA-M-0039
- Closest oracle policies: DEP-006
- Modality: ENFORCED_ADVISORY
- Normative action: A PackageReference VersionOverride is flagged as needing a concrete, documented reason.
- Trigger/scope: executable: check-manifests.mjs over **/*.csproj, Directory.Packages.props, package.json (excluding .claude, node_modules, bin, obj, dist, etc.); run by hooks after manifest edits/shell commands and by workflows/CI
- Exceptions: none
- Why EXTRA: DEP-006 says references are normally versionless; requiring a documented reason for VersionOverride adds a documentation obligation.
- Evidence M-S000499: `output/template/.claude/scripts/check-manifests.mjs:279-281` — "if (attrs.versionoverride !== undefined) { ⏎       result.notes.push({ file: rel, message: `${id}: VersionOverride "${attrs.versionoverride}" needs a concrete, documented reason` }); ⏎     }"

### EXTRA-M-0040
- Closest oracle policies: DEP-003
- Modality: ENFORCED
- Normative action: Floating or range versions (NuGet *, bracket/comma ranges; npm empty, *, x, latest, next, x-suffix, >=) are always violations with no explicit-request exception.
- Trigger/scope: executable: check-manifests.mjs over **/*.csproj, Directory.Packages.props, package.json (excluding .claude, node_modules, bin, obj, dist, etc.); run by hooks after manifest edits/shell commands and by workflows/CI
- Exceptions: none (npm ^/~ ranges are not flagged)
- Why EXTRA: DEP-003 permits floating versions when explicitly requested; the checker reports them as violations unconditionally.
- Evidence M-S000494: `output/template/.claude/scripts/check-manifests.mjs:230-236` — "const v = version.trim(); ⏎   if (v.includes('*') || /^[[(]/.test(v) || v.includes(',')) { ⏎     result.violations.push({ file: rel, message: `${id}: floating or range version "${v}" - pin the latest stable compatible version (add-dependency)` }); ⏎   } else if (/^\d+(\.\d+)*-/.test(v)) { ⏎     result.notes.push({ file: rel, message: `${id}: prerelease version "${v}" - allowed only when explicitly …"
- Evidence M-S000509: `output/template/.claude/scripts/check-manifests.mjs:338-342` — "if (['', '*', 'x', 'X', 'latest', 'next'].includes(spec) || /(^|\.)[xX*]$/.test(spec) || /^>=?[^<]*$/.test(spec)) { ⏎         result.violations.push({ file: rel, message: `${section}.${name}: floating version "${spec}" - pin the latest stable compatible version (add-dependency)` }); ⏎       } else if (/\d+\.\d+\.\d+-/.test(spec)) { ⏎         result.notes.push({ file: rel, message: `${section}.${na …"

### EXTRA-M-0041
- Closest oracle policies: DEP-025
- Modality: ENFORCED
- Normative action: The PreToolUse guard fails closed (onFailure: block): if the guard cannot run (e.g. Node.js unavailable, invalid hook input, crash or timeout) the Bash/PowerShell tool call is blocked.
- Trigger/scope: Claude Code hook registration (all sessions in this project)
- Exceptions: Other hooks fail open.
- Why EXTRA: Not entailed by any oracle policy: it makes Node.js availability a precondition for every shell command in a session, an executable restriction beyond blocking npm bypass flags.
- Evidence M-S000523: `output/template/.claude/settings.json:7-7` — "{ "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dependency-guard.mjs"], "timeout": 30, "onFailure": "block" }"

### EXTRA-M-0059
- Closest oracle policies: DEP-020
- Modality: MUST
- Normative action: When direct Polly is used, document why.
- Trigger/scope: workflow add-dependency (adding/updating/removing NuGet or npm packages)
- Exceptions: none
- Why EXTRA: DEP-020 makes Polly an explicit exception but does not require documenting the reason.
- Evidence M-S000598: `output/template/.claude/skills/add-dependency/SKILL.md:25-31` — "- Resilience: when resilience is required, prefer ⏎     `Microsoft.Extensions.Http.Resilience` for `HttpClient` and ⏎     `Microsoft.Extensions.Resilience` for general resilience pipelines. Direct ⏎     Polly usage is an explicit exception rather than the default — use it only ⏎     when a concrete requirement cannot be expressed through those packages, and ⏎     document why. Do not add the depre …"

### EXTRA-M-0060
- Closest oracle policies: DEP-005
- Modality: MUST_NOT
- Normative action: Do not draw legal conclusions beyond what the published license information supports.
- Trigger/scope: workflow add-dependency (adding/updating/removing NuGet or npm packages)
- Exceptions: none
- Why EXTRA: Additional restraint on license analysis not stated in DEP-004/DEP-005.
- Evidence M-S000607: `output/template/.claude/skills/add-dependency/SKILL.md:76-78` — "Never silently replace the requested package with an alternative. If no ⏎ reasonable free alternative exists, say so explicitly. Do not draw legal ⏎ conclusions beyond what the published license information supports."

### EXTRA-M-0061
- Closest oracle policies: DEP-001, GOV-014
- Modality: MUST
- Normative action: Remove dependencies no longer used when that is part of the current change and safe to verify; do not leave dead package references behind.
- Trigger/scope: workflow add-dependency (adding/updating/removing NuGet or npm packages)
- Exceptions: Only within the current change.
- Why EXTRA: Oracle has no obligation to remove dead dependency references.
- Evidence M-S000622: `output/template/.claude/skills/add-dependency/SKILL.md:141-143` — "Remove dependencies that are no longer used when doing so is part of the current ⏎ change and safe to verify; do not leave dead package references behind. Do not ⏎ perform unrelated dependency cleanup during a narrowly scoped task."

### EXTRA-M-0062
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Report package, selected version, license, checks performed and approval status (approved / awaiting approval / not needed).
- Trigger/scope: workflow add-dependency (adding/updating/removing NuGet or npm packages)
- Exceptions: none
- Why EXTRA: Workflow output-shape obligation not in the oracle.
- Evidence M-S000624: `output/template/.claude/skills/add-dependency/SKILL.md:147-148` — "Report the package, selected version, license, checks performed, and approval ⏎ status (approved / awaiting approval / not needed)."

### EXTRA-M-0063
- Closest oracle policies: FE-004
- Modality: PREFER
- Normative action: Use computed for derived state and avoid unnecessary effect() when computed, template binding or explicit event handling is clearer.
- Trigger/scope: on-demand knowledge skill angular (Angular code)
- Exceptions: none
- Why EXTRA: Signal-API technique preference (computed vs effect) not entailed by FE-004.
- Evidence M-S000638: `output/template/.claude/skills/angular/SKILL.md:81-83` — "Use `computed` for derived state, and avoid unnecessary `effect()` when ⏎ `computed`, template binding, or explicit event handling expresses the ⏎ dependency more clearly."

### EXTRA-M-0064
- Closest oracle policies: FE-010, FE-003
- Modality: MUST_NOT
- Normative action: Do not duplicate complex Domain rules in TypeScript unless the UI genuinely needs an equivalent user-facing rule.
- Trigger/scope: on-demand knowledge skill angular (Angular code)
- Exceptions: UI genuinely needs an equivalent user-facing rule.
- Why EXTRA: FE-010 says frontend validation is UX; a prohibition on duplicating complex Domain rules in TypeScript is additional.
- Evidence M-S000653: `output/template/.claude/skills/angular/SKILL.md:136-137` — "Keep transport/request mapping explicit. Do not duplicate complex Domain rules ⏎ in TypeScript unless the UI genuinely needs an equivalent user-facing rule."

### EXTRA-M-0065
- Closest oracle policies: DEP-014, DEP-002
- Modality: DEFAULT
- Normative action: When the project uses Angular Material use its components consistently for common primitives; do not add Material automatically to an existing project that has not chosen it; do not wrap every Material component in a custom abstraction without a concrete reason.
- Trigger/scope: on-demand knowledge skill angular (Angular code)
- Exceptions: Concrete reason for wrappers.
- Why EXTRA: DEP-014 lists Material in the baseline stack; consistency, not retrofitting existing projects and no gratuitous wrappers are additional usage rules.
- Evidence M-S000662: `output/template/.claude/skills/angular/SKILL.md:169-172` — "When the project uses Angular Material, use its components consistently for ⏎ common UI primitives where they satisfy the requirement. Do not add Angular ⏎ Material automatically to an existing project that has not chosen it, and do not ⏎ wrap every Material component in a custom abstraction without a concrete reason."

### EXTRA-M-0066
- Closest oracle policies: TST-002, TST-003, TST-011
- Modality: DEFAULT
- Normative action: Test frontend behaviour at the appropriate level (component behaviour, validation, data-access mapping, route/auth behaviour, complex state); do not test Angular internals; E2E covers a small number of important workflows unless broader coverage is required; do not duplicate the same behaviour at every level; use the test runner configured in package.json.
- Trigger/scope: on-demand knowledge skill angular (Angular code)
- Exceptions: Broader E2E when the project requires it.
- Why EXTRA: Oracle testing policies are scoped to backend tests; this frontend testing guidance is additional.
- Evidence M-S000666: `output/template/.claude/skills/angular/SKILL.md:182-187` — "Test frontend behavior at the appropriate level: meaningful component behavior, ⏎ validation, data-access request mapping, important route/auth behavior, complex ⏎ reactive state. Do not test Angular framework internals. E2E tests focus on a ⏎ small number of important user workflows unless the project requires broader ⏎ E2E coverage, and the same behavior is not duplicated at every test level. Us …"

### EXTRA-M-0067
- Closest oracle policies: RUN-001, FE-005
- Modality: DEFAULT
- Normative action: Do not prematurely optimize Angular code; use lazy loading and sensible rendering/data access first; add memoization, virtual scrolling or custom change detection only after identifying a real need.
- Trigger/scope: on-demand knowledge skill angular (Angular code)
- Exceptions: none
- Why EXTRA: RUN-001/RUN-008 are backend-scoped; this frontend optimization discipline is additional.
- Evidence M-S000668: `output/template/.claude/skills/angular/SKILL.md:191-194` — "Do not prematurely optimize normal Angular code. Use route lazy loading and ⏎ sensible rendering and data access first; introduce memoization, virtual ⏎ scrolling, custom change-detection work, or other optimizations after ⏎ identifying a real need."

### EXTRA-M-0068
- Closest oracle policies: TST-002, TST-011, API-022
- Modality: DEFAULT
- Normative action: When versions coexist test version routing, version-specific shapes, deprecated versions still operational in their support period, unsupported-version behaviour and shared behaviour consistency; do not duplicate identical tests for versions sharing Application behaviour.
- Trigger/scope: on-demand knowledge skill api-versioning
- Exceptions: Only when versions coexist.
- Why EXTRA: Version-specific test obligations are not entailed by the oracle's testing or API policies.
- Evidence M-S000696: `output/template/.claude/skills/api-versioning/SKILL.md:135-139` — "When versions coexist, test meaningful differences: version routing, ⏎ version-specific response shape, a deprecated version still operational during ⏎ its support period, unsupported-version behavior, and shared Application ⏎ behavior staying consistent where intended. Do not duplicate identical tests ⏎ because two versions share Application behavior."

### EXTRA-M-0069
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: A Decision Request presents: title, Context, Options (incl. staying within current decisions, trade-offs, reversal cost), Recommendation, Blocked work and Proceeding-with work.
- Trigger/scope: workflow architecture-decision (Reserved decisions)
- Exceptions: none
- Why EXTRA: GOV-017 requires approval for Reserved changes; the mandatory request structure is a candidate-specific output format.
- Evidence M-S000706: `output/template/.claude/skills/architecture-decision/SKILL.md:23-23` — "Stop the Reserved part of the work and present:"
- Evidence M-S000707: `output/template/.claude/skills/architecture-decision/SKILL.md:25-35` — "```text ⏎ Decision Request: <short title> ⏎  ⏎ Context: <what requires the decision; which accepted decision, rule, or ⏎          product source it touches> ⏎ Options: <realistic alternatives, including staying within current decisions, ⏎          with trade-offs and reversal cost> ⏎ Recommendation: <preferred option and why> ⏎ Blocked: <work that cannot continue until this is decided> ⏎ Proceedin …"

### EXTRA-M-0070
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: An explicit approval (including an explicit instruction in the original request) is recorded before the Reserved part is implemented.
- Trigger/scope: workflow architecture-decision (Reserved decisions)
- Exceptions: none
- Why EXTRA: Sequencing/recording obligation beyond GOV-017's approval requirement.
- Evidence M-S000710: `output/template/.claude/skills/architecture-decision/SKILL.md:43-44` — "An explicit approval — including an explicit instruction in the original request ⏎ — is recorded before the Reserved part is implemented:"

### EXTRA-M-0071
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST
- Normative action: Record an accepted decision as docs/decisions/<NNNN>-<short-title>.md (create directory with first record) with Status, Date, Context, Decision, Alternatives considered, Consequences.
- Trigger/scope: workflow architecture-decision (Reserved decisions)
- Exceptions: none
- Why EXTRA: ADR file convention not entailed by the oracle.
- Evidence M-S000711: `output/template/.claude/skills/architecture-decision/SKILL.md:46-48` — "1. Add a record `docs/decisions/<NNNN>-<short-title>.md` (create the directory ⏎    with the first record) containing: Status (Accepted), Date, Context, ⏎    Decision, Alternatives considered, Consequences."

### EXTRA-M-0072
- Closest oracle policies: GOV-007
- Modality: MUST
- Normative action: After an approved architecture/pattern/layer/approval-boundary decision update CLAUDE.md Architecture Defaults; after technology adoption/replacement/conditional activation update docs/technology-stack.md.
- Trigger/scope: workflow architecture-decision (Reserved decisions)
- Exceptions: none
- Why EXTRA: GOV-007 covers approved behavioural rules; updating instruction files for architecture/technology decisions is additional.
- Evidence M-S000712: `output/template/.claude/skills/architecture-decision/SKILL.md:49-49` — "2. Update the planning-time owner so the decision is visible when planning:"
- Evidence M-S000713: `output/template/.claude/skills/architecture-decision/SKILL.md:50-53` — "- architecture style, pattern, layer, or approval-boundary decisions → ⏎      CLAUDE.md § Architecture Defaults; ⏎    - technology adoption, replacement, or activation of a conditional ⏎      technology → `docs/technology-stack.md`;"

### EXTRA-M-0073
- Closest oracle policies: none
- Modality: MUST
- Normative action: When a decision needs new path-scoped constraints edit the owning .claude/rules/ file in place (one owner, no copies elsewhere).
- Trigger/scope: workflow architecture-decision (Reserved decisions)
- Exceptions: none
- Why EXTRA: Instruction-ownership obligation (repo/meta) not in the oracle.
- Evidence M-S000715: `output/template/.claude/skills/architecture-decision/SKILL.md:56-57` — "3. When the decision needs new constraints in a path-scoped rule, edit the ⏎    owning `.claude/rules/` file in place — one owner, no copies elsewhere."

### EXTRA-M-0074
- Closest oracle policies: GOV-017
- Modality: ALLOWED
- Normative action: When worth keeping, record a rejected or deferred decision with Status Rejected/Deferred, then continue with the compliant alternative.
- Trigger/scope: workflow architecture-decision (Reserved decisions)
- Exceptions: Discretionary ('when the discussion is worth keeping').
- Why EXTRA: Optional recording practice beyond the oracle.
- Evidence M-S000718: `output/template/.claude/skills/architecture-decision/SKILL.md:62-63` — "When the discussion is worth keeping, record it with Status Rejected or ⏎ Deferred, then continue with the compliant alternative."

### EXTRA-M-0075
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: Output the Decision Request (or the recorded decision and files updated) and the work that proceeded meanwhile.
- Trigger/scope: workflow architecture-decision (Reserved decisions)
- Exceptions: none
- Why EXTRA: Workflow output-shape obligation.
- Evidence M-S000720: `output/template/.claude/skills/architecture-decision/SKILL.md:67-68` — "The Decision Request (or the recorded decision and the files updated), and the ⏎ work that proceeded meanwhile."

### EXTRA-M-0076
- Closest oracle policies: API-009
- Modality: PREFER
- Normative action: If a Result pattern is adopted, use typed errors rather than arbitrary strings passed through every layer.
- Trigger/scope: on-demand knowledge skill aspnet-error-handling (backend)
- Exceptions: Only when a Result pattern is adopted.
- Why EXTRA: Oracle leaves the Result shape open; typed errors is an added design preference.
- Evidence M-S000737: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:92-95` — "For a command with several meaningful outcomes, an explicit typed outcome may be ⏎ clearer. If the project deliberately adopts a Result pattern (a project-wide ⏎ convention — Reserved), use it consistently with typed errors rather than ⏎ arbitrary strings passed through every layer."
- Evidence M-S000758: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:208-208` — "If introduced, prefer typed errors"

### EXTRA-M-0077
- Closest oracle policies: API-010, DEP-010
- Modality: MUST
- Normative action: Register validators via AddValidatorsFromAssemblyContaining and follow the project's established validation invocation pattern rather than adding a second competing mechanism.
- Trigger/scope: on-demand knowledge skill aspnet-error-handling (backend)
- Exceptions: none
- Why EXTRA: Single-invocation-mechanism rule not entailed by API-010/DEP-010.
- Evidence M-S000745: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:152-156` — "Register validators with `FluentValidation.DependencyInjectionExtensions` ⏎ (`services.AddValidatorsFromAssemblyContaining<...>()`), and follow the ⏎ project's established validation invocation pattern rather than adding a second ⏎ competing mechanism. Do not add a deprecated automatic-validation integration ⏎ package to connect FluentValidation to the pipeline."

### EXTRA-M-0078
- Closest oracle policies: SEC-005
- Modality: PREFER
- Normative action: Prefer policy-based authorization when logic is more than a trivial role check.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: none
- Why EXTRA: Authorization-mechanism preference not in the oracle.
- Evidence M-S000769: `output/template/.claude/skills/authentication/SKILL.md:19-21` — "Prefer policies when authorization logic is more"

### EXTRA-M-0079
- Closest oracle policies: SEC-016, ARC-020
- Modality: DEFAULT
- Normative action: Choose the authentication scheme from the actual application: Bearer/OIDC for SPA→API, cookies for server-rendered apps, ASP.NET Core Identity when owning local users/passwords, external OIDC/OAuth when identity is delegated.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: none
- Why EXTRA: Scheme-selection mapping is candidate guidance; the oracle only requires platform mechanisms and approval for auth architecture.
- Evidence M-S000771: `output/template/.claude/skills/authentication/SKILL.md:25-30` — "Choose the scheme from the actual application: ⏎  ⏎ - Bearer/OIDC for an SPA calling an API; ⏎ - cookies for server-rendered interactive web applications; ⏎ - ASP.NET Core Identity when the application owns local users and passwords; ⏎ - an external OpenID Connect/OAuth provider when identity is delegated."

### EXTRA-M-0080
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Use stable constants for repeated policy names; avoid role/permission magic strings scattered through the codebase.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: none
- Why EXTRA: Code-hygiene convention not in the oracle.
- Evidence M-S000784: `output/template/.claude/skills/authentication/SKILL.md:93-93` — "Use stable constants for policy names repeated across the application."
- Evidence M-S000804: `output/template/.claude/skills/authentication/SKILL.md:168-170` — "Avoid hardcoded signing keys, role/permission magic strings scattered through the ⏎ codebase, and adding Identity, JWT issuance, or OIDC infrastructure without an ⏎ actual need."

### EXTRA-M-0081
- Closest oracle policies: SEC-005
- Modality: PREFER
- Normative action: Use roles only for genuinely role-oriented models; avoid scattered compound role strings; prefer a policy when several roles/claims represent one capability.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: none
- Why EXTRA: Authorization-modelling preference not in the oracle.
- Evidence M-S000786: `output/template/.claude/skills/authentication/SKILL.md:97-99` — "Roles fit a genuinely role-oriented business authorization model. Avoid ⏎ scattering compound role strings; prefer a policy when several roles or claims ⏎ represent one business capability."

### EXTRA-M-0082
- Closest oracle policies: TST-003, SEC-005
- Modality: DEFAULT
- Normative action: Test authorization behaviour of important protected operations: unauthenticated→401, unauthorized→403, permitted success, ownership rules, intended anonymous access.
- Trigger/scope: on-demand knowledge skill authentication (backend, frontend)
- Exceptions: none
- Why EXTRA: Specific security test obligations not entailed by the oracle testing policies.
- Evidence M-S000801: `output/template/.claude/skills/authentication/SKILL.md:156-162` — "Test authorization behavior for important protected operations: ⏎  ⏎ - unauthenticated request → `401`; ⏎ - authenticated caller without permission → `403`; ⏎ - permitted caller → expected success; ⏎ - resource-specific ownership rules; ⏎ - anonymous endpoint remains accessible when intended."

### EXTRA-M-0083
- Closest oracle policies: WF-013
- Modality: MUST_NOT
- Normative action: Do not fabricate replacement APIs from memory when they can be verified.
- Trigger/scope: workflow build-fix (failing .NET/Angular build or tests)
- Exceptions: When verification is impossible.
- Why EXTRA: Verification-of-API-knowledge obligation not stated in the oracle.
- Evidence M-S000847: `output/template/.claude/skills/build-fix/SKILL.md:174-180` — "When failures follow a .NET, Angular, TypeScript, EF Core, or other framework ⏎ upgrade: inspect the actual installed version, distinguish compilation errors ⏎ from changed runtime behavior, check official migration documentation when ⏎ needed, update obsolete API usage deliberately, and preserve architecture and ⏎ behavior where the upgrade does not require change. Do not fabricate ⏎ replacement  …"

### EXTRA-M-0084
- Closest oracle policies: DEP-008, WF-009
- Modality: MUST_NOT
- Normative action: Do not change the repository's declared SDK, Node, framework or language version because the local machine differs; if the toolchain is unavailable and cannot be resolved safely, report the limitation instead of editing source to compensate.
- Trigger/scope: workflow build-fix (failing .NET/Angular build or tests)
- Exceptions: none
- Why EXTRA: Toolchain-pinning and report-instead-of-compensate rule beyond the oracle.
- Evidence M-S000849: `output/template/.claude/skills/build-fix/SKILL.md:184-191` — "Determine whether the failure comes from source code or the local toolchain ⏎ (`dotnet --info`, `dotnet --version`, `node --version`, `npm --version`; ⏎ `global.json`, target framework, Angular package versions, ⏎ `package-lock.json`, CI/runtime version configuration). Do not change the ⏎ repository's declared SDK, Node, framework, or language version because the ⏎ local machine has a different ve …"

### EXTRA-M-0085
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Build-fix report includes Initial failure, Root cause, Changes made and Remaining issues fields.
- Trigger/scope: workflow build-fix (failing .NET/Angular build or tests)
- Exceptions: none
- Why EXTRA: Report field structure beyond WF-009's status vocabulary.
- Evidence M-S000862: `output/template/.claude/skills/build-fix/SKILL.md:243-251` — "```text ⏎ Initial failure: <failure> ⏎ Root cause: <cause> ⏎ Changes made: <changes> ⏎ Backend build: PASS / NOT RUN / NOT APPLICABLE ⏎ Frontend build: PASS / NOT RUN / NOT APPLICABLE ⏎ Tests: PASS / NOT RUN / NOT APPLICABLE ⏎ Remaining issues: None / <details> ⏎ ```"

### EXTRA-M-0086
- Closest oracle policies: RUN-020
- Modality: DEFAULT
- Normative action: Centralize cache-key construction when duplicated key formats become hard to maintain.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: Conditional on duplication becoming hard to maintain.
- Why EXTRA: Key-construction organisation is not in the oracle.
- Evidence M-S000882: `output/template/.claude/skills/caching/SKILL.md:79-81` — "Dimensions that commonly affect the result: entity identifier, tenant, user when ⏎ genuinely user-specific, locale, relevant query/filter parameters. Centralize key ⏎ construction when duplicated key formats become hard to maintain."

### EXTRA-M-0087
- Closest oracle policies: RUN-023, RUN-007
- Modality: MUST
- Normative action: Choose cache expiration from data semantics (change rate, regeneration cost, staleness, memory, source-unavailable behaviour) rather than a universal default.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: RUN-023 requires a lifetime/invalidation strategy; forbidding a universal default TTL in favour of per-data semantics is additional.
- Evidence M-S000884: `output/template/.claude/skills/caching/SKILL.md:85-87` — "Choose expiration from data semantics rather than a universal default: how often ⏎ the data changes, regeneration cost, acceptable staleness, memory footprint, and ⏎ failure behavior when the source is unavailable."

### EXTRA-M-0088
- Closest oracle policies: RUN-018
- Modality: MUST
- Normative action: Decide explicitly whether a cache failure falls back to the source, fails the request or returns stale data.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: Explicit cache-failure policy decision is not required by the oracle.
- Evidence M-S000894: `output/template/.claude/skills/caching/SKILL.md:124-125` — "Decide whether a cache failure falls back to the source, fails the request, or ⏎ returns stale data."

### EXTRA-M-0089
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Test cache behaviour when it affects correctness (invalidation after mutation, tenant/user isolation, miss fallback, outage policy); do not unit-test framework cache internals.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: Only when caching affects observable correctness.
- Why EXTRA: Cache-specific test obligations beyond the oracle.
- Evidence M-S000896: `output/template/.claude/skills/caching/SKILL.md:129-132` — "Test cache behavior when it affects observable correctness: stale entries are ⏎ invalidated after a successful mutation; tenant/user keys are isolated; a miss ⏎ falls back correctly; an outage follows the intended failure policy. Do not ⏎ unit-test framework cache internals."

### EXTRA-M-0090
- Closest oracle policies: RUN-021, ARC-016
- Modality: AVOID
- Normative action: Avoid caching EF tracked entities across Unit of Work boundaries.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: none
- Why EXTRA: EF-tracking-specific caching restriction not in the oracle.
- Evidence M-S000898: `output/template/.claude/skills/caching/SKILL.md:136-138` — "Avoid caching EF tracked entities across Unit of Work boundaries, using a cache ⏎ as authoritative persistence, and adding Redis merely because the application ⏎ has caching."

### EXTRA-M-0091
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: Build deployable artifacts reproducibly and keep deployment/environment configuration outside compiled artifacts where practical.
- Trigger/scope: on-demand knowledge skill ci-cd (pipelines)
- Exceptions: Where practical.
- Why EXTRA: Artifact reproducibility/config separation is conditional delivery technique outside the oracle (EXC-014).
- Evidence M-S000905: `output/template/.claude/skills/ci-cd/SKILL.md:18-20` — "Build deployable artifacts reproducibly, keep deployment and environment ⏎ configuration outside compiled artifacts where practical, and add pipeline ⏎ stages for the actual project rather than generic boilerplate."

### EXTRA-M-0092
- Closest oracle policies: WF-017, GOV-003
- Modality: MUST_NOT
- Normative action: Do not turn an optional local formatter into a mandatory CI gate unless the project adopts that policy.
- Trigger/scope: on-demand knowledge skill ci-cd (pipelines)
- Exceptions: Project adopts the policy.
- Why EXTRA: Restriction on CI gate design not stated in the oracle.
- Evidence M-S000912: `output/template/.claude/skills/ci-cd/SKILL.md:44-45` — "Do not turn an optional local formatter into a mandatory CI gate unless the ⏎ project adopts that policy."

### EXTRA-M-0093
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: Store or publish only the artifacts later stages need.
- Trigger/scope: on-demand knowledge skill ci-cd (pipelines)
- Exceptions: none
- Why EXTRA: Artifact-retention rule outside the oracle.
- Evidence M-S000926: `output/template/.claude/skills/ci-cd/SKILL.md:137-138` — "Store or publish only the artifacts later stages"

### EXTRA-M-0094
- Closest oracle policies: WF-017
- Modality: PREFER
- Normative action: When artifact promotion is supported prefer promoting the same tested artifact/image through environments instead of recompiling; environment behaviour from runtime configuration; avoid rebuilding different source per environment without reason.
- Trigger/scope: on-demand knowledge skill ci-cd (pipelines)
- Exceptions: Deployment model supports promotion.
- Why EXTRA: Build-once/promote preference is explicitly outside the oracle (EXC-014).
- Evidence M-S000930: `output/template/.claude/skills/ci-cd/SKILL.md:148-150` — "When the deployment model supports artifact promotion, prefer promoting the same ⏎ tested artifact or image through environments instead of recompiling for each ⏎ environment; environment-specific behavior comes from runtime configuration."
- Evidence M-S000940: `output/template/.claude/skills/ci-cd/SKILL.md:180-182` — "Avoid project-specific database infrastructure in a generic pipeline, ⏎ rebuilding different source for every environment without a reason, and assuming ⏎ Docker deployment."

### EXTRA-M-0095
- Closest oracle policies: SEC-002
- Modality: PREFER
- Normative action: Prefer workload/federated identity over long-lived deployment credentials when the platform supports it.
- Trigger/scope: on-demand knowledge skill ci-cd (pipelines)
- Exceptions: Platform support.
- Why EXTRA: Credential-type preference not in the oracle.
- Evidence M-S000932: `output/template/.claude/skills/ci-cd/SKILL.md:154-156` — "Use the CI platform's secret/identity mechanism instead of values in pipeline ⏎ YAML, and prefer workload/federated identity over long-lived deployment ⏎ credentials when the platform supports it."

### EXTRA-M-0096
- Closest oracle policies: WF-017
- Modality: DEFAULT
- Normative action: Separate CI and CD as appropriate (green CI does not imply deployment) and use environment protection or approval appropriate to the hosting platform.
- Trigger/scope: on-demand knowledge skill ci-cd (pipelines)
- Exceptions: none
- Why EXTRA: Deployment-gating practice outside the oracle.
- Evidence M-S000936: `output/template/.claude/skills/ci-cd/SKILL.md:167-169` — "CI and CD may be separate workflows; a green CI build does not mean every branch ⏎ deploys. Use environment protection or approval appropriate to the hosting ⏎ platform."

### EXTRA-M-0097
- Closest oracle policies: WF-017, SEC-001
- Modality: MUST
- Normative action: Before considering a pipeline complete verify clean-environment restore, backend build, frontend build when present, configured tests, no developer-machine dependence, no secret exposure and expected artifacts.
- Trigger/scope: on-demand knowledge skill ci-cd (pipelines)
- Exceptions: none
- Why EXTRA: Pipeline-completion checklist beyond WF-017.
- Evidence M-S000938: `output/template/.claude/skills/ci-cd/SKILL.md:173-176` — "Before considering a pipeline complete, verify that it restores from a clean ⏎ environment, builds the backend, builds the frontend when present, runs the ⏎ configured tests, does not depend on developer-machine state, does not expose ⏎ secrets, and produces the expected artifacts."

### EXTRA-M-0098
- Closest oracle policies: WF-011
- Modality: MUST
- Normative action: Report findings ordered by severity with severity, file/location, what is wrong, why it matters and smallest fix, using the Critical/High/Medium/Low scale as defined.
- Trigger/scope: workflow code-review (reviews and the review gate)
- Exceptions: none
- Why EXTRA: The findings format and four-level severity scale are candidate output-shape rules not in the oracle.
- Evidence M-S000979: `output/template/.claude/skills/code-review/SKILL.md:175-184` — "Report findings ordered by severity. For each finding provide: severity, ⏎ file/location, what is wrong, why it matters, and the smallest reasonable fix. ⏎  ⏎ - **Critical** — data loss, a security vulnerability, reliably broken core ⏎   behavior, or another issue that should block use or merge immediately. ⏎ - **High** — a likely defect or architectural/data-integrity issue that should ⏎   be fix …"

### EXTRA-M-0099
- Closest oracle policies: WF-012
- Modality: MUST_NOT
- Normative action: Do not add filler praise to balance criticism.
- Trigger/scope: workflow code-review (reviews and the review gate)
- Exceptions: none
- Why EXTRA: Output-tone restriction not stated in WF-012.
- Evidence M-S000980: `output/template/.claude/skills/code-review/SKILL.md:186-188` — "Do not invent findings to populate categories. When there are no meaningful ⏎ findings, say so and state any important areas that could not be verified. Do ⏎ not add filler praise to balance criticism."

### EXTRA-M-0100
- Closest oracle policies: GOV-021, GOV-012
- Modality: PREFER
- Normative action: Prefer one normal source in code or configuration over duplicating a setting's literal across layers.
- Trigger/scope: workflow custom-settings (CUSTOM_SETTINGS.md value added/changed/removed/applied/reviewed)
- Exceptions: none
- Why EXTRA: Single-source design preference not stated in GOV-021.
- Evidence M-S001016: `output/template/.claude/skills/custom-settings/SKILL.md:25-26` — "2. Update the owning code, validation, and configuration. Prefer one normal ⏎    source in code or configuration over duplicating the literal across layers."

### EXTRA-M-0101
- Closest oracle policies: RUN-015, GOV-010
- Modality: MUST
- Normative action: Example numeric values are not approved defaults; choose retry counts, timeouts, limits and similar operational values from actual integration and deployment requirements.
- Trigger/scope: on-demand knowledge skill configuration (backend)
- Exceptions: none
- Why EXTRA: Prohibits adopting example operational values; the oracle governs tunable product values (GOV-010) and bounded timeouts (RUN-015) but not this.
- Evidence M-S000994: `output/template/.claude/skills/configuration/SKILL.md:67-69` — "Numeric values in examples are illustrative, not approved defaults. Choose retry ⏎ counts, timeouts, limits, and similar operational values from the actual ⏎ integration and deployment requirements."
- Evidence M-S001424: `output/template/.claude/skills/httpclient-factory/references/resilience.md:41-43` — "Distinguish the attempt timeout from the total operation timeout, especially ⏎ when retries are enabled. Choose values from actual latency requirements rather ⏎ than copying numbers from an example."
- Evidence M-S001485: `output/template/.claude/skills/httpclient-factory/SKILL.md:123-125` — "Choose timeouts from the remote operation and the application's latency budget. ⏎ With resilience pipelines, understand the difference between a per-attempt ⏎ timeout and a total-operation timeout (`references/resilience.md`)."
- Evidence M-S001515: `output/template/.claude/skills/logging/references/serilog.md:76-81` — "The configuration below deliberately demonstrates several optional sinks and ⏎ enrichers in one example. File, Seq, OpenTelemetry, Elasticsearch, and other ⏎ sinks or enrichers shown here are not baseline dependencies: configure only what ⏎ the project needs — a Console sink is enough for a simple local Development ⏎ baseline. Numeric limits and retention values in examples are illustrative, not ⏎ …"

### EXTRA-M-0102
- Closest oracle policies: ARC-021, ARC-007
- Modality: DEFAULT
- Normative action: Register Application services, repositories and external adapters at architectural boundaries interface-to-implementation; concrete registration only for implementation-only helpers without a separate contract.
- Trigger/scope: on-demand knowledge skill dependency-injection (backend)
- Exceptions: Implementation-only helpers.
- Why EXTRA: Registration-shape rule not entailed by ARC-021..ARC-023.
- Evidence M-S001035: `output/template/.claude/skills/dependency-injection/SKILL.md:19-22` — "- Use interface-to-implementation registration for Application services, ⏎   repositories, and external adapters at architectural boundaries; concrete ⏎   registration is fine for implementation-only helpers that need no separate ⏎   contract."

### EXTRA-M-0103
- Closest oracle policies: GOV-012
- Modality: DEFAULT
- Normative action: Use keyed services only when implementations are selected by a known key; decorators when the same cross-cutting behaviour wraps an abstraction; assembly scanning only for genuinely repetitive registration and over the assembly that owns the services.
- Trigger/scope: on-demand knowledge skill dependency-injection (backend)
- Exceptions: none
- Why EXTRA: Conditional DI technique selection (EXC-005 classifies decorators/scanning as optional technique).
- Evidence M-S001045: `output/template/.claude/skills/dependency-injection/SKILL.md:76-78` — "Use keyed services when multiple implementations of the same abstraction are ⏎ selected by a known key, not when a normal single registration or a simple ⏎ explicit factory is clearer."
- Evidence M-S001048: `output/template/.claude/skills/dependency-injection/SKILL.md:98-99` — "Use a decorator when the same cross-cutting behavior should wrap an abstraction ⏎ without changing its implementation."
- Evidence M-S001054: `output/template/.claude/skills/dependency-injection/SKILL.md:167-169` — "Use assembly scanning when registration volume creates genuinely repetitive ⏎ boilerplate, and scan the assembly that actually owns the services — not only the ⏎ API assembly by accident."

### EXTRA-M-0104
- Closest oracle policies: WF-009, GOV-017
- Modality: MUST
- Normative action: Report what changed, notable Delegated choices, unresolved Decision Requests, the verify report, and any change-specific obligation that was not applicable and why.
- Trigger/scope: workflow development-workflow (any implementation change)
- Exceptions: none
- Why EXTRA: Workflow output-shape obligation (incl. reporting Delegated choices and non-applicable obligations) beyond the oracle.
- Evidence M-S001102: `output/template/.claude/skills/development-workflow/SKILL.md:119-121` — "Report what changed, Delegated choices worth noting, unresolved Decision ⏎ Requests, the `verify` report, and any change-specific obligation that was not ⏎ applicable and why."

### EXTRA-M-0105
- Closest oracle policies: DEP-019, ARC-002
- Modality: DEFAULT
- Normative action: Keep images reproducible and configuration external, keep Docker concerns separate from application architecture (no Docker-specific changes in Domain/Application), and use the platform's health-probe capabilities when practical.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: When practical.
- Why EXTRA: Container practices outside the oracle (EXC-006).
- Evidence M-S001107: `output/template/.claude/skills/docker/SKILL.md:19-22` — "Keep build tooling out of production runtime images, keep images reproducible ⏎ and configuration external, keep Docker concerns separate from application ⏎ architecture, and use the deployment platform's health-probe capabilities when ⏎ practical."
- Evidence M-S001139: `output/template/.claude/skills/docker/SKILL.md:170-172` — "Avoid arbitrary infrastructure services in Compose, assuming curl/wget in ⏎ runtime images, specialized image variants without compatibility verification, ⏎ and Docker-specific changes leaking into Domain or Application code."

### EXTRA-M-0106
- Closest oracle policies: DEP-019
- Modality: DEFAULT
- Normative action: Use a multi-stage build for ASP.NET Core Dockerfiles.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Dockerfile shape is conditional technique outside the oracle (EXC-006).
- Evidence M-S001109: `output/template/.claude/skills/docker/SKILL.md:26-26` — "Use a multi-stage build:"

### EXTRA-M-0107
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Copy only repository-level build files that exist and are needed for restore; copy project files explicitly; avoid wildcard tricks that flatten multi-project structure.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Dockerfile copy technique not in the oracle.
- Evidence M-S001111: `output/template/.claude/skills/docker/SKILL.md:61-63` — "Copy only repository-level build files that exist and are required by restore. ⏎ Copy project files required for restore explicitly; avoid fragile wildcard ⏎ tricks that flatten or rearrange a multi-project structure."

### EXTRA-M-0108
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Copy project/build dependency files before the full source for restore caching; update the copy section when structure changes; never trade correctness of the restored project graph for caching.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Restore-layer caching technique not in the oracle.
- Evidence M-S001113: `output/template/.claude/skills/docker/SKILL.md:67-70` — "Copy project and build dependency files before the full source tree so source ⏎ changes do not invalidate NuGet restore layers. Update the project-copy section ⏎ when the solution structure changes; do not optimize caching at the cost of a ⏎ Dockerfile that no longer restores the actual project graph."

### EXTRA-M-0109
- Closest oracle policies: DEP-019
- Modality: DEFAULT
- Normative action: Use the built-in non-root user of modern .NET images when it fits.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: When it fits.
- Why EXTRA: DEP-019 forbids switching to root to bypass problems; actively running as the built-in non-root user is additional.
- Evidence M-S001117: `output/template/.claude/skills/docker/SKILL.md:79-79` — "Use the built-in non-root user of modern .NET images when it fits:"

### EXTRA-M-0110
- Closest oracle policies: SEC-002
- Modality: DEFAULT
- Normative action: Pass environment-specific configuration at runtime (e.g. ASPNETCORE_ENVIRONMENT, ConnectionStrings__Default).
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Runtime-configuration practice for containers beyond the oracle.
- Evidence M-S001121: `output/template/.claude/skills/docker/SKILL.md:90-95` — "Pass environment-specific configuration at runtime, for example ⏎ `ASPNETCORE_ENVIRONMENT`, `ConnectionStrings__Default`, ⏎ `Authentication__Authority`. Places where real credentials must never go: the ⏎ Dockerfile, committed Compose files, build arguments that remain visible in ⏎ image metadata, and copied appsettings files containing production secrets. Use ⏎ platform/container secret mechanisms …"

### EXTRA-M-0111
- Closest oracle policies: API-019
- Modality: DEFAULT
- Normative action: Expose liveness/readiness via ASP.NET Core health checks and prefer orchestrator HTTP probes; do not assume curl/wget/shell in runtime images; verify or add a probe mechanism weighing the cost of debug packages.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Probe mechanics are container technique outside the oracle (EXC-006).
- Evidence M-S001127: `output/template/.claude/skills/docker/SKILL.md:121-126` — "Expose liveness/readiness endpoints through ASP.NET Core health checks ⏎ (`health-check` skill) and prefer native HTTP probes supplied by the ⏎ orchestrator. Do not assume the runtime image contains `curl`, `wget`, or shell ⏎ utilities; if Compose must run an in-container health command, verify the ⏎ executable exists or add an appropriate probe mechanism, weighing the cost of ⏎ installing debuggi …"
- Evidence M-S001139: `output/template/.claude/skills/docker/SKILL.md:170-172` — "Avoid arbitrary infrastructure services in Compose, assuming curl/wget in ⏎ runtime images, specialized image variants without compatibility verification, ⏎ and Docker-specific changes leaking into Domain or Application code."

### EXTRA-M-0112
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: For static Angular deployment build in a Node stage and serve assets with the selected hosting strategy (Nginx not mandatory); keep API base URLs/environment config compatible with the deployment.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Frontend container technique outside the oracle.
- Evidence M-S001129: `output/template/.claude/skills/docker/SKILL.md:130-134` — "When the Angular frontend is deployed as a static application, build it in a Node ⏎ build stage and serve the generated assets with the selected hosting strategy. ⏎ Nginx is not mandatory; the platform may provide static hosting directly. Keep ⏎ API base URLs and environment configuration compatible with the deployment ⏎ strategy."

### EXTRA-M-0113
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Exclude non-build files from the Docker context (.git, bin, obj, node_modules, etc.); do not exclude tests the image build runs; never exclude files required by restore/build.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: none
- Why EXTRA: Build-context hygiene not in the oracle.
- Evidence M-S001131: `output/template/.claude/skills/docker/SKILL.md:138-138` — "Exclude files that do not belong in the build context:"
- Evidence M-S001133: `output/template/.claude/skills/docker/SKILL.md:150-151` — "Do not exclude tests when the image build intentionally runs them, and never ⏎ exclude files required by restore/build."

### EXTRA-M-0114
- Closest oracle policies: DEP-019
- Modality: DEFAULT
- Normative action: Start with standard supported .NET runtime images; use Alpine/chiseled/trimming/Native AOT only when justified and verify globalization, native dependencies, reflection and diagnostics.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: Compatibility and deployment requirements justify.
- Why EXTRA: Image-size optimization discipline is outside the oracle (EXC-006).
- Evidence M-S001135: `output/template/.claude/skills/docker/SKILL.md:155-159` — "Start with standard supported .NET runtime images. Consider Alpine, chiseled ⏎ images, trimming, Native AOT, or other size optimizations only when ⏎ compatibility and deployment requirements justify them, and verify ⏎ globalization, native dependencies, reflection, diagnostics, and other runtime ⏎ behavior when using specialized images."
- Evidence M-S001139: `output/template/.claude/skills/docker/SKILL.md:170-172` — "Avoid arbitrary infrastructure services in Compose, assuming curl/wget in ⏎ runtime images, specialized image variants without compatibility verification, ⏎ and Docker-specific changes leaking into Domain or Application code."

### EXTRA-M-0115
- Closest oracle policies: WF-006
- Modality: MUST
- Normative action: For Docker changes build the image, verify startup, ports/configuration, non-root behaviour, health-probe integration, review for accidental secrets/files, and run meaningful tests in or outside the pipeline.
- Trigger/scope: on-demand knowledge skill docker (containers)
- Exceptions: As relevant.
- Why EXTRA: Docker-specific verification checklist beyond WF-006.
- Evidence M-S001137: `output/template/.claude/skills/docker/SKILL.md:163-166` — "For Docker changes: build the image; verify application startup, required ports ⏎ and configuration, non-root behavior when relevant, and health-probe ⏎ integration; review the image for accidental secrets or files. Run meaningful ⏎ application tests outside or as part of the selected build pipeline."

### EXTRA-M-0116
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Use fakes/stubs/mocks when they make an isolated test clearer; do not mock every collaborator mechanically; do not forbid mocking project-owned abstractions when isolation helps; mock/fake architectural boundaries when that clarifies behaviour.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Mock/fake choice is test technique outside the oracle (EXC-012).
- Evidence M-S001155: `output/template/.claude/skills/dotnet-testing/SKILL.md:83-86` — "Use fakes, stubs, or mocks when they make an isolated test clearer; do not mock ⏎ every collaborator mechanically, and do not forbid mocking project-owned ⏎ abstractions when isolation is useful. Mock or fake architectural boundaries ⏎ when that clarifies the behavior under test."

### EXTRA-M-0117
- Closest oracle policies: TST-004
- Modality: DEFAULT
- Normative action: Keep slow or unreliable external-system tests separate from ordinary fast runs.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Test-suite partitioning not required by the oracle.
- Evidence M-S001172: `output/template/.claude/skills/dotnet-testing/SKILL.md:194-198` — "At the relevant boundary use a fake or mock abstraction for unit tests, a stub ⏎ `HttpMessageHandler`, WireMock or another local fake server for HTTP ⏎ integration, or a dedicated sandbox only when the test explicitly targets that ⏎ integration. Keep slow or unreliable external-system tests separate from ⏎ ordinary fast runs."

### EXTRA-M-0118
- Closest oracle policies: TST-008, GOV-012
- Modality: DEFAULT
- Normative action: Keep test data explicit and minimal; introduce builders/fixtures/factories only when repeated setup becomes hard to read, not a generic test-data framework for a few objects.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Builder/fixture technique outside the oracle (EXC-012).
- Evidence M-S001174: `output/template/.claude/skills/dotnet-testing/SKILL.md:202-204` — "Keep test data explicit and minimal. Introduce builders, fixtures, or factories ⏎ when repeated setup becomes hard to read — not a generic test-data framework for ⏎ a few simple objects."

### EXTRA-M-0119
- Closest oracle policies: TST-010
- Modality: MUST
- Normative action: Review a temporary probe before keeping it as a permanent test rather than committing it as-is.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: none
- Why EXTRA: Additional review step on probe conversion.
- Evidence M-S001180: `output/template/.claude/skills/dotnet-testing/SKILL.md:222-227` — "When a probe must become maintained coverage (`verify` step 4): replay an ad-hoc ⏎ HTTP request as a `WebApplicationFactory` test that sends the same request and ⏎ asserts the observed response; replace a manual database check with an ⏎ integration test that asserts the persisted state; turn a temporary regression ⏎ probe into a focused regression test. Review a temporary probe before keeping ⏎ it …"

### EXTRA-M-0120
- Closest oracle policies: TST-003
- Modality: AVOID
- Normative action: Avoid assertion-free tests unless the behaviour is explicitly 'does not throw'.
- Trigger/scope: on-demand knowledge skill dotnet-testing (backend tests)
- Exceptions: Explicit 'does not throw' behaviour.
- Why EXTRA: Test-hygiene rule not in the oracle.
- Evidence M-S001188: `output/template/.claude/skills/dotnet-testing/SKILL.md:248-251` — "Avoid assertions that merely repeat the implementation, assertion-free tests ⏎ (unless the behavior is explicitly "does not throw"), arbitrary delays such as ⏎ `Task.Delay` to make timing-sensitive tests pass, and Testcontainers when no ⏎ provider fidelity is required."

### EXTRA-M-0121
- Closest oracle policies: ARC-019
- Modality: DEFAULT
- Normative action: Keep entity configuration separate with IEntityTypeConfiguration<T>.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Configuration-organisation technique not in the oracle.
- Evidence M-S001198: `output/template/.claude/skills/ef-core/SKILL.md:32-32` — "Keep entity configuration separate with `IEntityTypeConfiguration<T>`."

### EXTRA-M-0122
- Closest oracle policies: RUN-006
- Modality: DEFAULT
- Normative action: Use tracking intentionally: tracking queries for entities modified in the current UoW; AsNoTracking for read-only entity queries; not mechanically on DTO projections.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Tracking technique outside the oracle (EXC-011).
- Evidence M-S001220: `output/template/.claude/skills/ef-core/SKILL.md:178-182` — "Use tracking intentionally: normal tracking queries when loaded entities will be ⏎ modified and committed through the current Unit of Work; `AsNoTracking()` for ⏎ read-only entity queries where change tracking provides no value. Do not add ⏎ `AsNoTracking()` mechanically to projections that already produce non-entity ⏎ DTOs."

### EXTRA-M-0123
- Closest oracle policies: RUN-006
- Modality: PREFER
- Normative action: Prefer explicit query shape (projection for selected data, Include/ThenInclude when the graph is needed); for large collection includes consider split queries and verify generated SQL/performance.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Query-shaping technique outside the oracle (EXC-011).
- Evidence M-S001226: `output/template/.claude/skills/ef-core/SKILL.md:200-204` — "Prefer an explicit query shape: projection when only selected related data is ⏎ needed; `Include`/`ThenInclude` when the entity graph itself is required. Avoid ⏎ lazy loading by default because it hides database access and causes N+1 ⏎ queries. For large collection includes, consider split queries and verify the ⏎ generated SQL and performance."

### EXTRA-M-0124
- Closest oracle policies: RUN-006
- Modality: MUST
- Normative action: Always use deterministic ordering for paged queries.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Deterministic paging order is a concrete correctness rule not stated in RUN-006.
- Evidence M-S001228: `output/template/.claude/skills/ef-core/SKILL.md:208-209` — "Apply filtering, ordering, and pagination in the database, and always use ⏎ deterministic ordering for paged queries:"

### EXTRA-M-0125
- Closest oracle policies: RUN-021, ARC-016
- Modality: MUST_NOT
- Normative action: Do not casually mix ExecuteUpdateAsync/ExecuteDeleteAsync with tracked entities for the same rows; understand their transaction and consistency implications.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Bulk-operation consistency caution not in the oracle.
- Evidence M-S001234: `output/template/.claude/skills/ef-core/SKILL.md:242-244` — "They execute directly against the database and bypass change tracking. Do not ⏎ mix them casually with tracked entities representing the same rows, and ⏎ understand their transaction and consistency implications."

### EXTRA-M-0126
- Closest oracle policies: ARC-018, ARC-020
- Modality: MUST_NOT
- Normative action: Do not attempt distributed transactions with EF transaction APIs.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Prohibition not stated in the oracle.
- Evidence M-S001236: `output/template/.claude/skills/ef-core/SKILL.md:248-251` — "A single `SaveChangesAsync` is normally the transaction boundary for one ⏎ application operation. Use an explicit transaction when a concrete use case ⏎ needs several database operations or several `SaveChangesAsync` calls to succeed ⏎ atomically. Do not attempt distributed transactions with EF transaction APIs."

### EXTRA-M-0127
- Closest oracle policies: API-011, ARC-019
- Modality: MUST_NOT
- Normative action: Use EF Core interceptors for infrastructure-level cross-cutting behaviour (e.g. auditing) and never hide business behaviour in persistence interceptors.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Interceptor placement/prohibition is EF technique outside the oracle (EXC-011).
- Evidence M-S001240: `output/template/.claude/skills/ef-core/SKILL.md:262-263` — "Use EF Core interceptors for infrastructure-level cross-cutting behavior such as"
- Evidence M-S001242: `output/template/.claude/skills/ef-core/SKILL.md:295-295` — "Do not hide business behavior in persistence interceptors."

### EXTRA-M-0128
- Closest oracle policies: ARC-019
- Modality: DEFAULT
- Normative action: Create migrations from the Infrastructure project, using the API project as startup project when required.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Migration-command technique not in the oracle.
- Evidence M-S001255: `output/template/.claude/skills/ef-core/SKILL.md:380-381` — "Create migrations from the Infrastructure project, using the API project as the ⏎ startup project when required:"

### EXTRA-M-0129
- Closest oracle policies: WF-019
- Modality: PREFER
- Normative action: For controlled production deployment generated (idempotent) migration scripts are often preferable.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Deployment-artifact preference beyond WF-019.
- Evidence M-S001257: `output/template/.claude/skills/ef-core/SKILL.md:387-389` — "After a model change, recreating an empty Development database must produce ⏎ seed data that is valid for the migrated schema. For controlled production ⏎ deployment, generated migration scripts are often preferable:"

### EXTRA-M-0130
- Closest oracle policies: RUN-002
- Modality: AVOID
- Normative action: Avoid fire-and-forget EF asynchronous operations.
- Trigger/scope: on-demand knowledge skill ef-core (backend persistence)
- Exceptions: none
- Why EXTRA: Not stated in RUN-002 (which targets sync-over-async).
- Evidence M-S001264: `output/template/.claude/skills/ef-core/SKILL.md:410-412` — "Avoid loading all rows and filtering in memory when the database can filter, ⏎ lazy loading by default, fire-and-forget EF asynchronous operations, and raw SQL ⏎ introduced merely to appear more performant."

### EXTRA-M-0131
- Closest oracle policies: GOV-016
- Modality: DEFAULT
- Normative action: Follow the repository's branch-naming convention; otherwise use prefixes like feature/, fix/, refactor/, test/, docs/, chore/ with meaningful names; do not rename existing user branches to satisfy the convention.
- Trigger/scope: workflow git-workflow (Git operations requested by the user)
- Exceptions: Existing repository convention.
- Why EXTRA: Branch-naming convention not in the oracle.
- Evidence M-S001277: `output/template/.claude/skills/git-workflow/SKILL.md:33-36` — "Follow the repository's branch-naming convention when one exists. Otherwise, ⏎ clear prefixes such as `feature/`, `fix/`, `refactor/`, `test/`, `docs/`, and ⏎ `chore/` are reasonable defaults. Use meaningful names that describe the work, ⏎ and do not rename an existing user branch merely to satisfy this convention."

### EXTRA-M-0132
- Closest oracle policies: GOV-016
- Modality: MUST_NOT
- Normative action: One branch must not be checked out simultaneously in multiple normal worktrees.
- Trigger/scope: workflow git-workflow (Git operations requested by the user)
- Exceptions: none
- Why EXTRA: Worktree constraint not stated in GOV-016.
- Evidence M-S001279: `output/template/.claude/skills/git-workflow/SKILL.md:40-41` — "- One branch must not be checked out simultaneously in multiple normal ⏎   worktrees."

### EXTRA-M-0133
- Closest oracle policies: WF-022
- Modality: PREFER
- Normative action: Prefer one logical change per commit with implementation and its protecting tests together; no artificial tiny commits.
- Trigger/scope: workflow git-workflow (Git operations requested by the user)
- Exceptions: none
- Why EXTRA: Commit granularity preferences beyond WF-022.
- Evidence M-S001283: `output/template/.claude/skills/git-workflow/SKILL.md:49-52` — "- Prefer one logical change per commit; implementation and the tests that ⏎   protect it belong in the same logical commit. ⏎ - Do not create artificial tiny commits, and do not combine unrelated fixes or ⏎   refactors into one commit."

### EXTRA-M-0134
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Follow the repository commit-message convention, else Conventional Commits; use the body for important motivation/constraints/migration info and do not narrate obvious diff details.
- Trigger/scope: workflow git-workflow (Git operations requested by the user)
- Exceptions: Existing repository convention.
- Why EXTRA: Commit-message convention not in the oracle.
- Evidence M-S001284: `output/template/.claude/skills/git-workflow/SKILL.md:53-54` — "- Follow the repository's commit-message convention. Without one, ⏎   Conventional Commits are a useful default:"
- Evidence M-S001286: `output/template/.claude/skills/git-workflow/SKILL.md:65-66` — "Use the body when important motivation, constraints, or migration information ⏎   would otherwise be lost; do not narrate obvious diff details."

### EXTRA-M-0135
- Closest oracle policies: WF-003
- Modality: MUST
- Normative action: Ensure relevant verification has completed before pushing.
- Trigger/scope: workflow git-workflow (Git operations requested by the user)
- Exceptions: none
- Why EXTRA: Pre-push verification gate not in the oracle (WF-003 gates completion claims, not pushes).
- Evidence M-S001288: `output/template/.claude/skills/git-workflow/SKILL.md:70-75` — "Before pushing: ⏎  ⏎ 1. confirm the intended branch; ⏎ 2. confirm the working and staged state is understood; ⏎ 3. ensure relevant verification has completed; ⏎ 4. avoid pushing unrelated local commits accidentally."

### EXTRA-M-0136
- Closest oracle policies: GOV-015
- Modality: MUST_NOT
- Normative action: Treat main, master and other protected or shared branches as non-rewritable.
- Trigger/scope: workflow git-workflow (Git operations requested by the user)
- Exceptions: none
- Why EXTRA: Absolute protection of main/master/shared branches exceeds GOV-015 (which allows rewriting on explicit request).
- Evidence M-S001289: `output/template/.claude/skills/git-workflow/SKILL.md:77-79` — "Never force-push a shared branch unless the user explicitly requests history ⏎ rewriting and the consequences are understood. Treat `main`, `master`, and ⏎ other protected or shared branches as non-rewritable."

### EXTRA-M-0137
- Closest oracle policies: GOV-015
- Modality: MUST
- Normative action: Follow repository/team convention or explicit request for merge vs rebase; resolve conflicts from the intended combined behaviour (not mechanical ours/theirs) and run relevant verification afterwards.
- Trigger/scope: workflow git-workflow (Git operations requested by the user)
- Exceptions: none
- Why EXTRA: Merge/rebase practice beyond the oracle.
- Evidence M-S001291: `output/template/.claude/skills/git-workflow/SKILL.md:83-87` — "Follow repository/team convention or the user's explicit request rather than ⏎ personal preference. Before either operation, inspect local uncommitted work, ⏎ and do not automatically stash, reset, or discard work to make it proceed. ⏎ Resolve conflicts from the intended combined behavior, not by mechanically ⏎ choosing "ours" or "theirs", then run relevant verification."

### EXTRA-M-0138
- Closest oracle policies: WF-003, WF-022
- Modality: MUST
- Normative action: Run verify before preparing a PR; a PR has a focused purpose and a description explaining what changed, why, how verified and compatibility/migration notes.
- Trigger/scope: workflow git-workflow (Git operations requested by the user)
- Exceptions: none
- Why EXTRA: PR preparation rules not in the oracle.
- Evidence M-S001293: `output/template/.claude/skills/git-workflow/SKILL.md:91-94` — "Run `verify` before preparing a PR. A PR has a focused purpose without ⏎ accidental unrelated changes, and its description explains what changed, why, ⏎ how it was verified, and important compatibility or migration notes. Do not ⏎ claim checks were run if they were not."

### EXTRA-M-0139
- Closest oracle policies: WF-009
- Modality: ALLOWED
- Normative action: After Git operations report resulting state when useful (branch, commit, push target, PR status, remaining uncommitted changes).
- Trigger/scope: workflow git-workflow (Git operations requested by the user)
- Exceptions: Discretionary ('when useful').
- Why EXTRA: Reporting practice beyond the oracle.
- Evidence M-S001297: `output/template/.claude/skills/git-workflow/SKILL.md:106-108` — "After Git operations, report the resulting state when useful: branch, commit ⏎ created, push target, PR preparation status, and uncommitted changes that ⏎ remain."

### EXTRA-M-0140
- Closest oracle policies: API-019
- Modality: DEFAULT
- Normative action: Register readiness checks with tags (and map readiness endpoints by tag).
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Tagging/endpoint technique outside the oracle (EXC-010).
- Evidence M-S001311: `output/template/.claude/skills/health-check/SKILL.md:50-51` — "Readiness asks: can this instance currently serve the traffic it is responsible ⏎ for? Register readiness checks with tags:"

### EXTRA-M-0141
- Closest oracle policies: API-018
- Modality: DEFAULT
- Normative action: Use provider/framework health-check integration where suitable.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: Where suitable.
- Why EXTRA: Implementation preference not in the oracle.
- Evidence M-S001316: `output/template/.claude/skills/health-check/SKILL.md:75-77` — "A lightweight connectivity/availability check — no expensive business queries, ⏎ large scans, or data modification. Use provider/framework health-check ⏎ integration where suitable."

### EXTRA-M-0142
- Closest oracle policies: API-019
- Modality: MUST_NOT
- Normative action: Health endpoints return success when healthy and non-success when unhealthy per the probe policy; do not reuse business API status semantics mechanically for orchestrator probes.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Probe status-mapping rule outside the oracle (EXC-010).
- Evidence M-S001320: `output/template/.claude/skills/health-check/SKILL.md:88-91` — "Health endpoints return success when healthy and a non-success status when ⏎ unhealthy according to the configured probe policy; `HealthCheckOptions` allows ⏎ status-code mapping. Do not reuse business API status semantics mechanically for ⏎ orchestrator probes."

### EXTRA-M-0143
- Closest oracle policies: API-020, SEC-006
- Modality: DEFAULT
- Normative action: Choose health endpoint exposure from the deployment topology (internal network, management port, host restrictions, or authorization where probes support it).
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Exposure-mechanics guidance outside the oracle (EXC-010).
- Evidence M-S001324: `output/template/.claude/skills/health-check/SKILL.md:101-104` — "Health endpoints often must be reachable by infrastructure without ordinary user ⏎ authentication. Choose exposure from the deployment topology: private/internal ⏎ network access, a dedicated management port, host restrictions, or authorization ⏎ where the probe infrastructure supports it."

### EXTRA-M-0144
- Closest oracle policies: RUN-013, API-018
- Modality: AVOID
- Normative action: Avoid Error-level logs for every normal failed probe.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Logging-level rule for probes not in the oracle.
- Evidence M-S001328: `output/template/.claude/skills/health-check/SKILL.md:113-115` — "Health checks may run frequently. Avoid expensive queries, long external ⏎ timeouts, large allocations, full business workflows, and Error-level logs for ⏎ every normal failed probe."

### EXTRA-M-0145
- Closest oracle policies: TST-003
- Modality: DEFAULT
- Normative action: Test meaningful health configuration when deployment relies on it (live endpoint, readiness vs required dependency, no sensitive leakage, optional-dependency semantics); no elaborate tests of uncustomized framework behaviour.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: When deployment relies on it.
- Why EXTRA: Health-check test obligations beyond the oracle.
- Evidence M-S001330: `output/template/.claude/skills/health-check/SKILL.md:119-123` — "Test meaningful health configuration when deployment relies on it: the live ⏎ endpoint responds when the process is healthy; readiness changes with a required ⏎ dependency; the response leaks no sensitive details; optional-dependency ⏎ behavior matches the intended readiness semantics. Do not build elaborate tests ⏎ for framework behavior the application does not customize."

### EXTRA-M-0146
- Closest oracle policies: API-018
- Modality: AVOID
- Normative action: Avoid using health checks as a code-quality grading system.
- Trigger/scope: on-demand knowledge skill health-check (backend)
- Exceptions: none
- Why EXTRA: Anti-pattern not stated in API-018..API-020.
- Evidence M-S001332: `output/template/.claude/skills/health-check/SKILL.md:127-128` — "Avoid using health checks as a code-quality grading system and remote dependency ⏎ chains without operational justification."

### EXTRA-M-0147
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Observe retries, timeouts and circuit behaviour when they materially affect operations; give important production circuit breakers operational visibility.
- Trigger/scope: private reference of on-demand knowledge skill httpclient-factory (outbound resilience)
- Exceptions: When material.
- Why EXTRA: Observability obligation for resilience not in the oracle.
- Evidence M-S001417: `output/template/.claude/skills/httpclient-factory/references/resilience.md:16-17` — "4. Observe retries, timeouts, and circuit behavior when they materially affect ⏎    operations."

### EXTRA-M-0148
- Closest oracle policies: RUN-016
- Modality: MUST_NOT
- Normative action: Do not retry validation errors, authentication/authorization failures, permanent 404 outcomes or deterministic business rejections.
- Trigger/scope: private reference of on-demand knowledge skill httpclient-factory (outbound resilience)
- Exceptions: none
- Why EXTRA: Explicit non-retryable categories beyond RUN-016's safety criterion.
- Evidence M-S001427: `output/template/.claude/skills/httpclient-factory/references/resilience.md:51-53` — "Not retried: validation errors, authentication/authorization failures, permanent ⏎ `404` outcomes, deterministic business rejections, and non-idempotent operations ⏎ without a duplicate-prevention strategy."

### EXTRA-M-0149
- Closest oracle policies: RUN-016
- Modality: MUST_NOT
- Normative action: Do not invent a client-side Idempotency-Key unless the remote service supports that contract.
- Trigger/scope: private reference of on-demand knowledge skill httpclient-factory (outbound resilience)
- Exceptions: none
- Why EXTRA: Specific prohibition not stated in RUN-016.
- Evidence M-S001432: `output/template/.claude/skills/httpclient-factory/references/resilience.md:67-70` — "If the answer is "duplicate side effect", automatic retry is unsafe. Use an ⏎ API-supported idempotency mechanism when appropriate, and do not invent a ⏎ client-side `Idempotency-Key` unless the remote service actually supports that ⏎ contract."

### EXTRA-M-0150
- Closest oracle policies: RUN-015
- Modality: DEFAULT
- Normative action: Use a circuit breaker only when repeated calls to a failing dependency would add load/latency (not without a repeated-failure pattern).
- Trigger/scope: private reference of on-demand knowledge skill httpclient-factory (outbound resilience)
- Exceptions: none
- Why EXTRA: Circuit-breaker technique is outside the oracle (EXC-007).
- Evidence M-S001434: `output/template/.claude/skills/httpclient-factory/references/resilience.md:74-76` — "Use one when repeated calls to a failing dependency would create additional load ⏎ or latency, not for a dependency without a meaningful repeated-failure pattern. ⏎ Give an important production circuit breaker operational visibility."
- Evidence M-S001452: `output/template/.claude/skills/httpclient-factory/references/resilience.md:133-136` — "Avoid retrying every exception or HTTP status, circuit breakers without a failure ⏎ scenario, hedging writes, generic resilience wrappers around EF Core without ⏎ understanding provider behavior, stacked handlers with overlapping strategies, ⏎ and unbounded retry/timeout combinations."

### EXTRA-M-0151
- Closest oracle policies: RUN-016
- Modality: MUST_NOT
- Normative action: Do not wrap normal EF Core operations in a generic application-level retry pipeline by default; prefer EF Core execution strategies/provider configuration and follow provider transaction/retry guidance; HTTP retry policies are not automatically appropriate for databases.
- Trigger/scope: private reference of on-demand knowledge skill httpclient-factory (outbound resilience)
- Exceptions: none
- Why EXTRA: Database-retry technique outside the oracle (EXC-007).
- Evidence M-S001442: `output/template/.claude/skills/httpclient-factory/references/resilience.md:99-104` — "Do not wrap normal EF Core operations in a generic application-level retry ⏎ pipeline by default. When the provider supports transient retry through EF Core ⏎ execution strategies or provider configuration, prefer that mechanism, and ⏎ handle transaction/retry interaction according to the provider's EF Core ⏎ guidance. An HTTP retry policy is not automatically appropriate for database ⏎ operations …"
- Evidence M-S001452: `output/template/.claude/skills/httpclient-factory/references/resilience.md:133-136` — "Avoid retrying every exception or HTTP status, circuit breakers without a failure ⏎ scenario, hedging writes, generic resilience wrappers around EF Core without ⏎ understanding provider behavior, stacked handlers with overlapping strategies, ⏎ and unbounded retry/timeout combinations."

### EXTRA-M-0152
- Closest oracle policies: RUN-016
- Modality: DEFAULT
- Normative action: Retrying publication can duplicate delivery; use idempotent consumers, broker deduplication or outbox when required; retry does not give exactly-once delivery.
- Trigger/scope: private reference of on-demand knowledge skill httpclient-factory (outbound resilience)
- Exceptions: When the business requirement needs it.
- Why EXTRA: Message-delivery technique outside the oracle (EXC-007).
- Evidence M-S001444: `output/template/.claude/skills/httpclient-factory/references/resilience.md:108-111` — "Retrying publication can produce duplicate delivery. Use idempotent consumers, ⏎ broker-supported deduplication, outbox patterns, or other mechanisms when the ⏎ business requirement needs them; a retry policy does not provide exactly-once ⏎ delivery."

### EXTRA-M-0153
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: Inbound ASP.NET Core rate limiting is distinct from outbound resilience; rejected requests normally return 429 with Retry-After when a useful delay is known.
- Trigger/scope: private reference of on-demand knowledge skill httpclient-factory (outbound resilience)
- Exceptions: none
- Why EXTRA: HTTP rate-limiting semantics not in the oracle.
- Evidence M-S001386: `output/template/.claude/skills/http-api/SKILL.md:182-184` — "Rate limiting rejected the request. Include `Retry-After` when the server knows ⏎ when another attempt is appropriate. Do not represent validation failure as rate ⏎ limiting."
- Evidence M-S001446: `output/template/.claude/skills/httpclient-factory/references/resilience.md:115-118` — "ASP.NET Core rate limiting protects this API from excessive incoming traffic and ⏎ is conceptually different from outbound resilience. A rejected request normally ⏎ returns `429 Too Many Requests`, with `Retry-After` when a useful delay is known ⏎ (`http-api` skill)."

### EXTRA-M-0154
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: Include a Location header identifying a created resource when a stable resource URI exists.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: Stable resource URI exists.
- Why EXTRA: Location-header obligation not in the oracle.
- Evidence M-S001345: `output/template/.claude/skills/http-api/SKILL.md:42-43` — "Include a `Location` header identifying the created resource when a stable ⏎ resource URI exists:"
- Evidence M-S001896: `output/template/.claude/skills/swagger/SKILL.md:83-84` — "Document `201 Created` when that is the runtime contract, and prefer ⏎ `CreatedAtAction`/`CreatedAtRoute` when a canonical resource URL exists."

### EXTRA-M-0155
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: When practical return an operation identifier or Location to observe progress for 202 responses.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: When practical.
- Why EXTRA: Operation-tracking response shape not in the oracle.
- Evidence M-S001349: `output/template/.claude/skills/http-api/SKILL.md:58-60` — "For accepted but incomplete processing — long-running operations, background ⏎ jobs, asynchronous imports, queued processing. When practical, return an ⏎ operation identifier or a `Location` where the client can observe progress:"

### EXTRA-M-0156
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: Use 304 only for conditional requests whose cached representation is still valid; never as a generic 'nothing changed' business response.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Less-common status semantics outside the oracle (EXC-009).
- Evidence M-S001357: `output/template/.claude/skills/http-api/SKILL.md:87-89` — "Only for a conditional request (`If-None-Match`/ETag, `If-Modified-Since`) ⏎ when the client's cached representation is still valid. It carries no normal ⏎ representation and is not a generic "nothing changed" business response."

### EXTRA-M-0157
- Closest oracle policies: API-003
- Modality: MUST
- Normative action: 406 when no acceptable response representation can be produced; 415 when the request body media type is unsupported; do not confuse them.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Content-negotiation status semantics outside the oracle (EXC-009).
- Evidence M-S001368: `output/template/.claude/skills/http-api/SKILL.md:121-123` — "The server cannot produce a representation acceptable under the client's ⏎ content negotiation. This concerns the response representation — do not confuse ⏎ it with `415`."
- Evidence M-S001376: `output/template/.claude/skills/http-api/SKILL.md:148-150` — "The server does not support the request representation, for example ⏎ `Content-Type: application/xml` on a JSON-only endpoint. `415` concerns the ⏎ request body format; `406` concerns acceptable response formats."

### EXTRA-M-0158
- Closest oracle policies: API-003, API-002
- Modality: DEFAULT
- Normative action: Use 422 for structurally valid requests with invalid semantics/business content; follow an established project convention when 400 is used for both; new APIs that distinguish use 400 for contract errors and 422 for semantic errors.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: Established project convention of 400 for both.
- Why EXTRA: 400/422 distinction is not in the oracle.
- Evidence M-S001378: `output/template/.claude/skills/http-api/SKILL.md:154-157` — "The request is syntactically and structurally valid, but its semantic or ⏎ business content cannot be processed — impossible business values, a business ⏎ rule rejection that is not a state conflict, a semantically invalid combination ⏎ of valid fields (for example `startDate > endDate`)."
- Evidence M-S001379: `output/template/.claude/skills/http-api/SKILL.md:159-160` — "Some APIs deliberately use `400` for both transport and semantic validation; ⏎ follow an established project convention. For new APIs that distinguish them:"

### EXTRA-M-0159
- Closest oracle policies: API-006
- Modality: MUST
- Normative action: Use 428 when a contract-required precondition (e.g. If-Match) is absent; for other mandatory preconditions only when the contract explicitly defines them.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: 428 semantics outside the oracle (API-006 covers 409/412 only).
- Evidence M-S001382: `output/template/.claude/skills/http-api/SKILL.md:169-170` — "The API contract requires a precondition the client did not provide, for example ⏎ a `PUT /api/orders/123` that requires `If-Match`:"
- Evidence M-S001384: `output/template/.claude/skills/http-api/SKILL.md:177-178` — "Use `428` for other mandatory preconditions only when the contract explicitly ⏎ defines them."

### EXTRA-M-0160
- Closest oracle policies: API-003
- Modality: MUST_NOT
- Normative action: 502/504 only when this API acts as an intermediary receiving an invalid upstream response or upstream timeout; do not map every dependency failure to 502 or every TaskCanceledException to 504; distinguish own timeouts from upstream timeouts.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: Gateway status semantics outside the oracle (EXC-009).
- Evidence M-S001391: `output/template/.claude/skills/http-api/SKILL.md:196-198` — "This API acts as an intermediary and received an invalid or unusable response ⏎ from an upstream service. Do not convert every dependency failure into `502` ⏎ mechanically."
- Evidence M-S001395: `output/template/.claude/skills/http-api/SKILL.md:209-213` — "This API acts as an intermediary and an upstream service did not respond in ⏎ time. Do not return `504` for every internal `TaskCanceledException`; ⏎ distinguish a client-cancelled request, our own operation timing out, and an ⏎ upstream dependency timing out — the correct response depends on which occurred ⏎ and on the role this API plays."

### EXTRA-M-0161
- Closest oracle policies: API-003
- Modality: DEFAULT
- Normative action: 503 for temporary inability (maintenance, critical dependency unavailable, chosen overload semantics) with Retry-After when a meaningful time is known.
- Trigger/scope: on-demand knowledge skill http-api (backend Controllers)
- Exceptions: none
- Why EXTRA: 503 semantics outside the oracle.
- Evidence M-S001393: `output/template/.claude/skills/http-api/SKILL.md:202-205` — "The service is temporarily unable to handle the request: intentional ⏎ maintenance, a critical dependency unavailable for this operation, or temporary ⏎ overload when the service chooses `503` semantics. Include `Retry-After` when a ⏎ meaningful retry time is known."

### EXTRA-M-0162
- Closest oracle policies: ARC-025, API-011
- Modality: MUST_NOT
- Normative action: Use DelegatingHandler only for genuine HTTP pipeline concerns (auth header acquisition, correlation propagation, request signing), never for business decisions.
- Trigger/scope: on-demand knowledge skill httpclient-factory (outbound HTTP)
- Exceptions: none
- Why EXTRA: Handler-responsibility rule not in the oracle.
- Evidence M-S001478: `output/template/.claude/skills/httpclient-factory/SKILL.md:85-87` — "Use a `DelegatingHandler` for genuine HTTP pipeline concerns — authorization ⏎ header acquisition, correlation/context propagation, specialized request ⏎ signing — never for business decisions."

### EXTRA-M-0163
- Closest oracle policies: ARC-025, API-003
- Modality: MUST_NOT
- Normative action: Do not blindly call EnsureSuccessStatusCode when remote statuses carry contract meaning; do not expose every upstream status through your API or map every upstream failure mechanically to one status.
- Trigger/scope: on-demand knowledge skill httpclient-factory (outbound HTTP)
- Exceptions: none
- Why EXTRA: Response-mapping rules beyond ARC-025.
- Evidence M-S001487: `output/template/.claude/skills/httpclient-factory/SKILL.md:129-131` — "Infrastructure translates remote responses into the abstraction consumed by ⏎ Application. Do not blindly call `EnsureSuccessStatusCode()` when specific ⏎ remote statuses carry contract meaning:"
- Evidence M-S001489: `output/template/.claude/skills/httpclient-factory/SKILL.md:142-145` — "For richer failure semantics, translate responses into explicit Infrastructure ⏎ or Application outcomes. Do not simply expose every upstream status code through ⏎ your own API, and do not map every upstream failure mechanically to the same ⏎ status."

### EXTRA-M-0164
- Closest oracle policies: none
- Modality: MUST_NOT
- Normative action: Apply per-request values (dynamic tokens) to the request or via a handler; do not mutate shared DefaultRequestHeaders concurrently for request-specific values.
- Trigger/scope: on-demand knowledge skill httpclient-factory (outbound HTTP)
- Exceptions: none
- Why EXTRA: HttpClient header-safety rule not in the oracle.
- Evidence M-S001495: `output/template/.claude/skills/httpclient-factory/SKILL.md:166-169` — "Stable headers such as media types may be configured on the client. Apply ⏎ per-request values such as dynamic access tokens to the specific request or ⏎ through a handler; do not mutate shared `DefaultRequestHeaders` concurrently for ⏎ request-specific values."
- Evidence M-S001503: `output/template/.claude/skills/httpclient-factory/SKILL.md:195-197` — "Avoid making typed, keyed, or named clients mandatory universally, ignoring ⏎ cancellation, putting dynamic auth tokens in shared `DefaultRequestHeaders`, and ⏎ adding resilience pipelines without understanding their behavior."

### EXTRA-M-0165
- Closest oracle policies: none
- Modality: PREFER
- Normative action: Prefer System.Net.Http.Json/System.Text.Json where sufficient; use explicit serialization options when the external contract differs from application defaults.
- Trigger/scope: on-demand knowledge skill httpclient-factory (outbound HTTP)
- Exceptions: none
- Why EXTRA: Serializer choice preference not in the oracle.
- Evidence M-S001497: `output/template/.claude/skills/httpclient-factory/SKILL.md:173-176` — "Prefer `System.Net.Http.Json` / `System.Text.Json` where sufficient. Use ⏎ explicit serialization options when the external contract differs from the ⏎ application's defaults, and do not reuse internal Domain entities as remote API ⏎ contracts merely to avoid mapping."

### EXTRA-M-0166
- Closest oracle policies: RUN-013
- Modality: DEFAULT
- Normative action: Log information that helps diagnose/operate and choose levels by operational meaning: Trace/Debug troubleshooting detail; Information normal meaningful events (not every method call); Warning recovered degraded conditions; Error failed operations needing attention; Critical subsystem cannot continue safely.
- Trigger/scope: on-demand knowledge skill logging (backend)
- Exceptions: none
- Why EXTRA: Log-level taxonomy not in the oracle.
- Evidence M-S001553: `output/template/.claude/skills/logging/SKILL.md:19-20` — "choose levels by"
- Evidence M-S001560: `output/template/.claude/skills/logging/SKILL.md:42-51` — "- **Trace / Debug** — detailed diagnostics mainly useful while troubleshooting. ⏎   Debug or Trace does not make sensitive data safe. ⏎ - **Information** — normal meaningful events: a background job completed, an ⏎   important business operation completed, a runtime lifecycle event. Avoid ⏎   logging every internal method call. ⏎ - **Warning** — an unexpected or degraded condition the application  …"

### EXTRA-M-0167
- Closest oracle policies: RUN-013
- Modality: DEFAULT
- Normative action: Use ILogger.BeginScope when several entries need shared context.
- Trigger/scope: on-demand knowledge skill logging (backend)
- Exceptions: none
- Why EXTRA: Scope technique outside the oracle (EXC-013).
- Evidence M-S001564: `output/template/.claude/skills/logging/SKILL.md:60-60` — "Use `ILogger.BeginScope` when several entries need shared context:"

### EXTRA-M-0168
- Closest oracle policies: RUN-013
- Modality: DEFAULT
- Normative action: Prefer platform/runtime trace identifiers for correlation; add an explicit correlation id only when an integration/operational requirement needs it; propagate tracing context across outbound calls with the chosen infrastructure.
- Trigger/scope: on-demand knowledge skill logging (backend)
- Exceptions: none
- Why EXTRA: Correlation implementation is technique outside the oracle (EXC-013).
- Evidence M-S001568: `output/template/.claude/skills/logging/SKILL.md:78-83` — "Prefer platform/runtime trace identifiers when they already provide adequate ⏎ request correlation. Add an explicit correlation identifier only when an ⏎ integration or operational requirement needs one; validate or normalize an ⏎ identifier accepted from an external client before propagating it. Propagate ⏎ correlation/tracing context across outbound calls with the project's chosen ⏎ tracing or H …"

### EXTRA-M-0169
- Closest oracle policies: none
- Modality: AVOID
- Normative action: Avoid using logs as an audit database unless a dedicated audit design has been adopted.
- Trigger/scope: on-demand knowledge skill logging (backend)
- Exceptions: Adopted audit design.
- Why EXTRA: Anti-pattern not in the oracle.
- Evidence M-S001574: `output/template/.claude/skills/logging/SKILL.md:101-103` — "Avoid putting provider-specific APIs throughout Application code, dumping full ⏎ objects without review, and using logs as an audit database unless a dedicated ⏎ audit design has been adopted."

### EXTRA-M-0170
- Closest oracle policies: DEP-021
- Modality: DEFAULT
- Normative action: Use two-stage (bootstrap logger) Serilog initialization when startup logging matters; simpler apps may use host-managed setup.
- Trigger/scope: private reference of on-demand knowledge skill logging (Serilog)
- Exceptions: Simpler applications without startup-logging needs.
- Why EXTRA: Bootstrap technique not in the oracle.
- Evidence M-S001508: `output/template/.claude/skills/logging/references/serilog.md:11-14` — "1. Use two-stage initialization when startup logging matters: a bootstrap ⏎    logger captures failures before the full DI/configuration pipeline exists. ⏎    Simpler applications may use normal host-managed Serilog setup without ⏎    bootstrap logging."

### EXTRA-M-0171
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: When using Serilog's static/bootstrap Log.Logger flush it on shutdown; for purely host-managed logging follow the provider lifetime instead of static lifecycle code.
- Trigger/scope: private reference of on-demand knowledge skill logging (Serilog)
- Exceptions: none
- Why EXTRA: Serilog lifecycle technique not in the oracle.
- Evidence M-S001539: `output/template/.claude/skills/logging/references/serilog.md:249-250` — "When the application uses Serilog's static/bootstrap `Log.Logger`, flush it on ⏎ shutdown so buffered events (Seq, OTLP, Elasticsearch sinks) are written:"
- Evidence M-S001541: `output/template/.claude/skills/logging/references/serilog.md:258-259` — "For purely host-managed logging, follow the configured provider's lifetime ⏎ behavior instead of adding static Serilog lifecycle code."

### EXTRA-M-0172
- Closest oracle policies: DEP-004
- Modality: DEFAULT
- Normative action: Use the official Elastic.Serilog.Sinks package instead of the deprecated Serilog.Sinks.Elasticsearch when writing to Elasticsearch.
- Trigger/scope: private reference of on-demand knowledge skill logging (Serilog)
- Exceptions: Only when Elasticsearch is used.
- Why EXTRA: Package-specific replacement guidance not in the oracle.
- Evidence M-S001545: `output/template/.claude/skills/logging/references/serilog.md:275-277` — "The `Serilog.Sinks.Elasticsearch` package is deprecated. Use the official ⏎ `Elastic.Serilog.Sinks` package, which writes ECS-formatted documents to data ⏎ streams:"

### EXTRA-M-0173
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Use collection expressions when the target type is clear; use required when initialization is part of the valid construction contract (not a substitute for constructor/domain validation); avoid deeply nested patterns; use field to remove trivial backing fields.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Context-sensitive language-feature technique, explicitly outside the oracle (EXC-002).
- Evidence M-S001584: `output/template/.claude/skills/modern-csharp/SKILL.md:30-30` — "Use them when the target type is clear:"
- Evidence M-S001589: `output/template/.claude/skills/modern-csharp/SKILL.md:46-47` — "Use `required` when initializing a property is part of the type's valid ⏎ construction contract:"
- Evidence M-S001591: `output/template/.claude/skills/modern-csharp/SKILL.md:53-54` — "`required` is not a substitute for constructor or domain validation where ⏎ invariants must be protected."
- Evidence M-S001594: `output/template/.claude/skills/modern-csharp/SKILL.md:67-68` — "Avoid deeply nested patterns that are harder to understand than straightforward ⏎ conditions."
- Evidence M-S001598: `output/template/.claude/skills/modern-csharp/SKILL.md:85-86` — "Use it to remove an otherwise trivial backing field; do not rewrite manual ⏎ backing fields that already contain clear or substantial logic."

### EXTRA-M-0174
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Records suit immutable DTOs, genuine Value Objects and messages; identity/lifecycle entities normally stay classes; prefer immutability when natural but do not force it where controlled mutation is clearer.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Record/immutability guidance outside the oracle (EXC-002).
- Evidence M-S001587: `output/template/.claude/skills/modern-csharp/SKILL.md:40-42` — "Good record candidates include immutable transport DTOs, genuine Value Objects, ⏎ and immutable messages. Entities with identity and lifecycle normally remain ⏎ classes unless the model genuinely benefits from record semantics."
- Evidence M-S001608: `output/template/.claude/skills/modern-csharp/SKILL.md:124-126` — "Prefer immutability when it represents the model naturally; do not force ⏎ immutable representations onto framework models or workflows where controlled ⏎ mutation is simpler and clearer."

### EXTRA-M-0175
- Closest oracle policies: DEP-008
- Modality: MUST_NOT
- Normative action: Before using a language feature confirm the configured language version supports it; do not change LangVersion or the target framework to use newer syntax.
- Trigger/scope: on-demand knowledge skill modern-csharp (backend C#)
- Exceptions: none
- Why EXTRA: Prohibition on version changes for syntax is broader than DEP-008's preview/RC approval gate.
- Evidence M-S001612: `output/template/.claude/skills/modern-csharp/SKILL.md:135-137` — "Before using a language feature, confirm that the project's configured language ⏎ version supports it; do not change `LangVersion` or the target framework to use ⏎ newer syntax."

### EXTRA-M-0176
- Closest oracle policies: DEP-022
- Modality: DEFAULT
- Normative action: Repository-wide scaffold files are <Name>.slnx, global.json, .gitignore and README.md (following solution-layout.md).
- Trigger/scope: workflow project-structure (new solution/project or repository-structure change)
- Exceptions: none
- Why EXTRA: global.json/README.md/.gitignore as standard scaffold set is not in the oracle (DEP-022 covers only .slnx).
- Evidence M-S001705: `output/template/.claude/skills/project-structure/SKILL.md:60-64` — "Following `references/solution-layout.md`, create only the required top-level ⏎ directories and repository-wide files (`<Name>.slnx`, `global.json`, ⏎ `.gitignore`, `README.md`). This template already provides `.editorconfig`, ⏎ `Directory.Build.props`, and `Directory.Packages.props`; keep them at the ⏎ repository root."

### EXTRA-M-0177
- Closest oracle policies: DEP-024
- Modality: DEFAULT
- Normative action: Angular unit/component tests are colocated with the code they test; E2E tests, when used, live under the workspace (e.g. frontend/<Name>.Web/e2e/).
- Trigger/scope: workflow project-structure (new solution/project or repository-structure change)
- Exceptions: none
- Why EXTRA: Frontend test placement convention not in the oracle.
- Evidence M-S001713: `output/template/.claude/skills/project-structure/SKILL.md:88-94` — "Create only useful test projects, placed as CLAUDE.md § Architecture Defaults ⏎ describes — typically `<Name>.Application.Tests` and `<Name>.IntegrationTests`. Create `<Name>.Domain.Tests` only when Domain contains ⏎ non-trivial behavior worth testing independently — a Domain made mainly of ⏎ entities and enums does not need one — and `<Name>.Infrastructure.Tests` only ⏎ for a concrete testing nee …"

### EXTRA-M-0178
- Closest oracle policies: ARC-027, DEP-024
- Modality: DEFAULT
- Normative action: Scaffold backend folders by role: Application Abstractions/Persistence, Abstractions/ExternalServices, Services, DTOs, Validation, DependencyInjection.cs; Infrastructure Persistence/{Configurations,Repositories,Migrations,Seeding}, Services, DependencyInjection.cs.
- Trigger/scope: private reference of workflow project-structure (backend scaffolding)
- Exceptions: Folders only when needed.
- Why EXTRA: Directory naming/layout is scaffolding technique outside the oracle (EXC-004).
- Evidence M-S001625: `output/template/.claude/skills/project-structure/references/backend-layout.md:35-36` — "- `Abstractions/Persistence` — inward-facing persistence contracts such as ⏎   `ITaskRepository.cs`, `IOrderRepository.cs`, `IUnitOfWork.cs`."
- Evidence M-S001626: `output/template/.claude/skills/project-structure/references/backend-layout.md:37-40` — "- `Abstractions/ExternalServices` — Application-owned abstractions implemented ⏎   by outer layers when needed (`IEmailSender.cs`, `ICurrentUser.cs`, ⏎   `IFileStorage.cs`, `IPaymentGateway.cs`); create it only when such ⏎   dependencies exist."
- Evidence M-S001627: `output/template/.claude/skills/project-structure/references/backend-layout.md:41-42` — "- `Services` — Application Services and useful public service contracts ⏎   (`ITaskService.cs`, `TaskService.cs`). No handler/CQRS/MediatR structures."
- Evidence M-S001628: `output/template/.claude/skills/project-structure/references/backend-layout.md:43-44` — "- `DTOs` — Application-level operation/data models when useful; not a generic ⏎   dumping ground."
- Evidence M-S001629: `output/template/.claude/skills/project-structure/references/backend-layout.md:45-46` — "- `Validation` — FluentValidation validators for Application-level input and ⏎   use-case validation when required."
- Evidence M-S001630: `output/template/.claude/skills/project-structure/references/backend-layout.md:47-48` — "- `DependencyInjection.cs` — registers Application-owned services and ⏎   Application-level validation; never concrete Infrastructure implementations."
- Evidence M-S001636: `output/template/.claude/skills/project-structure/references/backend-layout.md:92-92` — "- `Configurations` — EF Core entity mappings."
- Evidence M-S001637: `output/template/.claude/skills/project-structure/references/backend-layout.md:93-94` — "- `Repositories` — concrete repository implementations (an Infrastructure-only ⏎   generic base is allowed when it removes real duplication)."
- Evidence M-S001638: `output/template/.claude/skills/project-structure/references/backend-layout.md:95-99` — "- `Migrations` — EF Core migrations. ⏎ - `Seeding` — Development database initialization (`ef-core` skill). ⏎ - `Services` — technical/external implementations of Application abstractions ⏎   (`EmailSender.cs`, `FileStorage.cs`, `PaymentGateway.cs`); add ⏎   capability-specific subdirectories when they improve cohesion."
- Evidence M-S001639: `output/template/.claude/skills/project-structure/references/backend-layout.md:100-102` — "- `DependencyInjection.cs` — registers `AppDbContext`, repository ⏎   implementations, `IUnitOfWork`, external adapters, the SQL Server provider, ⏎   `HttpClient` integrations, and resilience handlers when used."

### EXTRA-M-0179
- Closest oracle policies: RUN-009
- Modality: DEFAULT
- Normative action: Make supporting-type roles clear by name/directory using suffixes (Service, Dto, Request/Response, Result/Outcome, Validator, Rules/Policy, Factory, Mapper, Adapter); avoid ambiguous names; add responsibility subdirectories only when a flat directory becomes hard to navigate.
- Trigger/scope: private reference of workflow project-structure (backend scaffolding)
- Exceptions: none
- Why EXTRA: Type-role naming heuristics explicitly outside the oracle (EXC-004).
- Evidence M-S001632: `output/template/.claude/skills/project-structure/references/backend-layout.md:52-64` — "Within a feature or service area, make each supporting type's responsibility ⏎ clear from its name, its immediate directory, or both. Useful suffixes: ⏎  ⏎ - `Service` — use-case orchestration; ⏎ - `Dto` — data-transfer models; ⏎ - `Request` / `Response` — Application operation contracts (transport-specific ⏎   HTTP contracts belong to the Api project); ⏎ - `Result` / `Outcome` — operation results …"
- Evidence M-S001633: `output/template/.claude/skills/project-structure/references/backend-layout.md:66-72` — "Avoid ambiguous names such as `TaskWorkflow` when the role cannot be inferred ⏎ without opening the file; prefer `TaskWorkflowRules`, `TaskWorkflowPolicy`, or ⏎ `TaskWorkflowService` according to the actual responsibility. Add ⏎ responsibility-specific subdirectories when a feature accumulates enough ⏎ heterogeneous supporting types that a flat directory is hard to navigate, not to ⏎ classify one  …"

### EXTRA-M-0180
- Closest oracle policies: ARC-012
- Modality: MUST_NOT
- Normative action: Keep Api Extensions cohesive; do not move arbitrary code out of Program.cs solely to make it shorter.
- Trigger/scope: private reference of workflow project-structure (backend scaffolding)
- Exceptions: none
- Why EXTRA: Program.cs organisation rule not in the oracle.
- Evidence M-S001645: `output/template/.claude/skills/project-structure/references/backend-layout.md:124-125` — "- `Extensions` — cohesive API/composition extension methods; do not move ⏎   arbitrary code out of `Program.cs` solely to make it shorter."

### EXTRA-M-0181
- Closest oracle policies: none
- Modality: DEFAULT
- Normative action: Add project references with the dotnet CLI (dotnet add ... reference ...).
- Trigger/scope: private reference of workflow project-structure (backend scaffolding)
- Exceptions: none
- Why EXTRA: Tooling technique not in the oracle.
- Evidence M-S001657: `output/template/.claude/skills/project-structure/references/backend-layout.md:171-174` — "The production and test reference graph is owned by ⏎ `.claude/rules/architecture.md` § Project References. Add references with the ⏎ CLI and check the result, running both commands from the repository root ⏎ (`git rev-parse --show-toplevel`):"

### EXTRA-M-0182
- Closest oracle policies: DEP-008, DEP-003
- Modality: DEFAULT
- Normative action: Pin the repository to the intended .NET SDK line with global.json: select the current stable SDK for the target release (no RC/preview unless requested) and allow patch/feature-band servicing via rollForward.
- Trigger/scope: private reference of workflow project-structure (repository scaffolding)
- Exceptions: RC/preview when explicitly requested.
- Why EXTRA: SDK pinning via global.json is not in the oracle.
- Evidence M-S001682: `output/template/.claude/skills/project-structure/references/solution-layout.md:94-97` — "- `global.json` — pin the repository to the intended supported .NET SDK line. ⏎   When scaffolding, select the current stable SDK for the target .NET release ⏎   (no RC/preview unless explicitly requested) and allow normal patch or ⏎   feature-band servicing through the chosen `rollForward` policy."

### EXTRA-M-0183
- Closest oracle policies: RUN-009
- Modality: PREFER
- Normative action: Keep deterministic formatting/code-style configuration in .editorconfig and prefer enforceable tooling configuration over restating mechanical formatting rules in instructions.
- Trigger/scope: private reference of workflow project-structure (repository scaffolding)
- Exceptions: none
- Why EXTRA: Instruction-design preference (repo/meta) not in the oracle.
- Evidence M-S001684: `output/template/.claude/skills/project-structure/references/solution-layout.md:101-103` — "Deterministic repository-wide formatting and code-style configuration lives ⏎ here. Prefer enforceable tooling configuration over restating mechanical ⏎ formatting rules in instructions."

### EXTRA-M-0184
- Closest oracle policies: SEC-001
- Modality: DEFAULT
- Normative action: Ignore generated and local artifacts (bin, obj, .vs, node_modules, dist, .angular, TestResults, coverage, local secret/config overrides).
- Trigger/scope: private reference of workflow project-structure (repository scaffolding)
- Exceptions: Where applicable.
- Why EXTRA: Ignore-file conventions are not in the oracle (secrets aspect partially relates to SEC-001).
- Evidence M-S001686: `output/template/.claude/skills/project-structure/references/solution-layout.md:107-107` — "Ignore generated and local artifacts where applicable:"

### EXTRA-M-0185
- Closest oracle policies: WF-009, WF-020
- Modality: MUST
- Normative action: State in the scan report that static review cannot prove security and may miss runtime, infrastructure, business-logic, authorization-bypass, deployment and dynamic-exploitation issues.
- Trigger/scope: workflow security-scan (security audit or scan)
- Exceptions: none
- Why EXTRA: Limitation-disclosure obligation not stated in the oracle.
- Evidence M-S001837: `output/template/.claude/skills/security-scan/SKILL.md:15-20` — "Perform an evidence-based static security review of the repository. This is ⏎ not a penetration test: static review cannot prove the application is secure and ⏎ may miss runtime-only vulnerabilities, infrastructure configuration outside the ⏎ repository, complex business-logic abuse, sophisticated authorization bypasses, ⏎ deployment-specific weaknesses, and vulnerabilities that need dynamic ⏎ exp …"
- Evidence M-S001877: `output/template/.claude/skills/security-scan/SKILL.md:227-229` — "A security scan is complete when all applicable layers were inspected, findings ⏎ have evidence, uncertain findings are labeled, severity reflects actual risk, ⏎ limitations are stated, and no layer is marked PASS without being checked."

### EXTRA-M-0186
- Closest oracle policies: WF-020
- Modality: DEFAULT
- Normative action: Use OWASP Top 10:2025 as an awareness taxonomy when it genuinely fits; do not force inaccurate category mappings.
- Trigger/scope: workflow security-scan (security audit or scan)
- Exceptions: none
- Why EXTRA: Taxonomy choice not in the oracle.
- Evidence M-S001847: `output/template/.claude/skills/security-scan/SKILL.md:46-46` — "Use OWASP Top 10:2025 as an awareness taxonomy when it genuinely fits:"
- Evidence M-S001849: `output/template/.claude/skills/security-scan/SKILL.md:61-61` — "Not every issue needs a category; do not force an inaccurate mapping."

### EXTRA-M-0187
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: Use the five-level scan severity scale (Critical sparingly for immediately exploitable high impact, High, Medium, Low, Info) as defined.
- Trigger/scope: workflow security-scan (security audit or scan)
- Exceptions: none
- Why EXTRA: Concrete severity scale and definitions are a candidate reporting convention.
- Evidence M-S001862: `output/template/.claude/skills/security-scan/SKILL.md:119-129` — "- **Critical** — use sparingly for immediately exploitable, high-impact ⏎   conditions: exposed real production credentials, reachable authentication ⏎   bypass, straightforward remote code execution, exploitable injection with ⏎   major data/system impact. ⏎ - **High** — a serious vulnerability that is realistically exploitable or can ⏎   substantially compromise data, authorization, or system be …"

### EXTRA-M-0188
- Closest oracle policies: WF-020, WF-009
- Modality: MUST
- Normative action: Security findings include severity, file/location, title, evidence, risk, impact, smallest remediation and OWASP category when applicable; the report follows the prescribed Security Scan Report shape; do not duplicate other skills' implementation guidance in the scan.
- Trigger/scope: workflow security-scan (security audit or scan)
- Exceptions: none
- Why EXTRA: Report structure is a candidate output-shape rule.
- Evidence M-S001868: `output/template/.claude/skills/security-scan/SKILL.md:151-154` — "Do not duplicate their"
- Evidence M-S001870: `output/template/.claude/skills/security-scan/SKILL.md:158-161` — "Every confirmed finding includes: severity, file and location, title, ⏎ evidence, why it is a security risk, likely impact, the smallest reasonable ⏎ remediation, and the OWASP category when applicable. Label uncertain findings ⏎ `NEEDS VERIFICATION` instead of presenting them as confirmed."
- Evidence M-S001872: `output/template/.claude/skills/security-scan/SKILL.md:165-211` — "```markdown ⏎ # Security Scan Report ⏎  ⏎ Scope: ⏎ - ... ⏎  ⏎ Limitations: ⏎ Static analysis only. This does not replace penetration testing, ⏎ dynamic testing, threat modeling, or infrastructure review. ⏎  ⏎ ## Summary ⏎  ⏎ | Severity | Count | ⏎ |---|---:| ⏎ | Critical | 0 | ⏎ | High | 0 | ⏎ | Medium | 0 | ⏎ | Low | 0 | ⏎ | Info | 0 | ⏎  ⏎ ## Findings ⏎  ⏎ ### [HIGH] File:Line — Finding title ⏎  …"

### EXTRA-M-0189
- Closest oracle policies: WF-020, DEP-004
- Modality: MUST
- Normative action: Supply-chain layer: review vulnerable direct/transitive dependencies, advisories, actual usage, patched compatible versions, untrusted NuGet sources; inspect npm audit distinguishing production vs dev and direct vs transitive; review lockfiles when integrity matters.
- Trigger/scope: private reference of workflow security-scan (security scans)
- Exceptions: When the layer applies.
- Why EXTRA: Per-layer scan coverage is investigation procedure beyond WF-020 (EXC-015).
- Evidence M-S001739: `output/template/.claude/skills/security-scan/references/scan-layers.md:21-24` — "Review vulnerable direct and transitive dependencies, severity/advisory ⏎ information, whether the vulnerable component is actually used in the affected ⏎ application, whether a patched compatible version exists, and unexpected or ⏎ untrusted NuGet sources."
- Evidence M-S001742: `output/template/.claude/skills/security-scan/references/scan-layers.md:31-35` — "When an npm frontend exists, inspect `npm audit` and distinguish production ⏎ from development/build dependencies and direct from transitive packages. A ⏎ development-only vulnerability can still matter to the supply chain, but its ⏎ runtime impact differs from a browser-shipped dependency. Review lockfiles when ⏎ package integrity or unexpected dependency changes are relevant."

### EXTRA-M-0190
- Closest oracle policies: WF-020, SEC-001
- Modality: MUST
- Normative action: Secrets/config layer: search .cs/.ts/.json/.yml/.yaml/.xml/.config/.env*/Dockerfiles/Compose/CI/scripts for real credentials; review production debug flags, certificate-validation bypass, credential-bearing URLs, verbose production errors and committed .env files.
- Trigger/scope: private reference of workflow security-scan (security scans)
- Exceptions: none
- Why EXTRA: Investigation coverage beyond the oracle (EXC-015).
- Evidence M-S001745: `output/template/.claude/skills/security-scan/references/scan-layers.md:41-43` — "Search source-controlled files for real credentials and secret material: ⏎ `.cs`, `.ts`, `.json`, `.yml`, `.yaml`, `.xml`, `.config`, `.env*`, Dockerfiles, ⏎ Compose files, CI workflow files, scripts."
- Evidence M-S001752: `output/template/.claude/skills/security-scan/references/scan-layers.md:69-71` — "Also review production debug/development flags, certificate-validation bypass, ⏎ insecure URLs carrying credentials, overly verbose production error ⏎ configuration, and accidentally committed `.env` files."

### EXTRA-M-0191
- Closest oracle policies: WF-020, SEC-003, SEC-004
- Modality: MUST
- Normative action: Injection layer: look for SQL built from untrusted input, command execution with user input, path traversal, SSRF via user-controlled host/URL, Angular sanitizer bypasses/direct DOM with untrusted content, unsafe polymorphic deserialization.
- Trigger/scope: private reference of workflow security-scan (security scans)
- Exceptions: none
- Why EXTRA: Investigation coverage beyond the oracle (EXC-015).
- Evidence M-S001756: `output/template/.claude/skills/security-scan/references/scan-layers.md:80-80` — "Look for SQL constructed from untrusted input:"
- Evidence M-S001758: `output/template/.claude/skills/security-scan/references/scan-layers.md:87-90` — "or interpolated/concatenated data passed to APIs that do not parameterize it. ⏎ Safe alternatives: EF Core LINQ, parameterized SQL, `FromSqlInterpolated` where ⏎ appropriate, ADO.NET/Dapper parameters. Do not report normal EF Core LINQ as SQL ⏎ injection merely because user input participates in a predicate."
- Evidence M-S001760: `output/template/.claude/skills/security-scan/references/scan-layers.md:94-97` — "Inspect `Process.Start`, shell execution, PowerShell/bash invocation, and ⏎ command arguments built from user input. Prefer APIs that separate executable ⏎ and arguments; validate or constrain external input when command execution is ⏎ genuinely needed."
- Evidence M-S001762: `output/template/.claude/skills/security-scan/references/scan-layers.md:101-104` — "Review user-controlled file names, paths, archive extraction, download paths, ⏎ and upload destinations for `../`, absolute-path injection, escaping the ⏎ intended root, and unsafe archive extraction. Normalize and verify that paths ⏎ remain within the intended storage boundary."
- Evidence M-S001764: `output/template/.claude/skills/security-scan/references/scan-layers.md:108-112` — "Inspect outbound requests where users can influence the scheme, host, port, ⏎ full URL, or redirect destination — especially when the server can reach ⏎ internal networks, metadata endpoints, or privileged services. Do not report ⏎ every user-supplied query parameter in an outbound request as SSRF; ⏎ host/control-plane influence matters."
- Evidence M-S001766: `output/template/.claude/skills/security-scan/references/scan-layers.md:116-121` — "For Angular, investigate deliberate sanitizer bypasses ⏎ (`bypassSecurityTrustHtml`, `bypassSecurityTrustScript`, ⏎ `bypassSecurityTrustResourceUrl`) and direct DOM manipulation with untrusted ⏎ content. Ordinary Angular binding benefits from framework escaping and ⏎ sanitization and is not automatically XSS. Review deliberate raw HTML handling in ⏎ any server-rendered UI as well."
- Evidence M-S001768: `output/template/.claude/skills/security-scan/references/scan-layers.md:125-127` — "Investigate dangerous polymorphic or type-driven deserialization, such as ⏎ `BinaryFormatter` or unsafe Newtonsoft `TypeNameHandling` configurations. Do not ⏎ deserialize untrusted payloads into arbitrary runtime types."

### EXTRA-M-0192
- Closest oracle policies: SEC-003
- Modality: PREFER
- Normative action: When command execution is genuinely needed prefer APIs separating executable and arguments and validate/constrain external input.
- Trigger/scope: private reference of workflow security-scan (security scans)
- Exceptions: none
- Why EXTRA: Command-injection engineering guidance not in the oracle.
- Evidence M-S001760: `output/template/.claude/skills/security-scan/references/scan-layers.md:94-97` — "Inspect `Process.Start`, shell execution, PowerShell/bash invocation, and ⏎ command arguments built from user input. Prefer APIs that separate executable ⏎ and arguments; validate or constrain external input when command execution is ⏎ genuinely needed."

### EXTRA-M-0193
- Closest oracle policies: SEC-003
- Modality: MUST
- Normative action: Normalize user-influenced paths and verify they remain within the intended storage boundary (incl. archive extraction).
- Trigger/scope: private reference of workflow security-scan (security scans)
- Exceptions: none
- Why EXTRA: Path-safety rule not in the oracle.
- Evidence M-S001762: `output/template/.claude/skills/security-scan/references/scan-layers.md:101-104` — "Review user-controlled file names, paths, archive extraction, download paths, ⏎ and upload destinations for `../`, absolute-path injection, escaping the ⏎ intended root, and unsafe archive extraction. Normalize and verify that paths ⏎ remain within the intended storage boundary."

### EXTRA-M-0194
- Closest oracle policies: SEC-003
- Modality: MUST_NOT
- Normative action: Do not deserialize untrusted payloads into arbitrary runtime types (e.g. BinaryFormatter, unsafe TypeNameHandling).
- Trigger/scope: private reference of workflow security-scan (security scans)
- Exceptions: none
- Why EXTRA: Deserialization prohibition not in the oracle.
- Evidence M-S001768: `output/template/.claude/skills/security-scan/references/scan-layers.md:125-127` — "Investigate dangerous polymorphic or type-driven deserialization, such as ⏎ `BinaryFormatter` or unsafe Newtonsoft `TypeNameHandling` configurations. Do not ⏎ deserialize untrusted payloads into arbitrary runtime types."

### EXTRA-M-0195
- Closest oracle policies: WF-020, SEC-005
- Modality: MUST
- Normative action: Access-control layer: look for identifier-only access to other users'/tenants' data (IDOR) and review password hashing, reset, lockout, enumeration and credential storage for local accounts.
- Trigger/scope: private reference of workflow security-scan (security scans)
- Exceptions: none
- Why EXTRA: Investigation coverage beyond the oracle (EXC-015).
- Evidence M-S001778: `output/template/.claude/skills/security-scan/references/scan-layers.md:157-160` — "Look for operations such as `GET /orders/{id}`, `PUT /users/{id}`, or ⏎ `DELETE /documents/{id}` where possessing an identifier could be enough to ⏎ access another user's or tenant's data. Verify ownership, tenant, permission, or ⏎ resource policy where required. Client-side filtering is not authorization."
- Evidence M-S001782: `output/template/.claude/skills/security-scan/references/scan-layers.md:174-176` — "When the application owns local accounts, review password hashing, password ⏎ reset behavior, lockout/brute-force controls where appropriate, ⏎ account-enumeration behavior, and credential storage."

### EXTRA-M-0196
- Closest oracle policies: WF-020, SEC-015
- Modality: MUST
- Normative action: Upload layer: inspect size limits, storage path safety, file-name handling, content/type assumptions, execution/public-serving risks and authorization.
- Trigger/scope: private reference of workflow security-scan (security scans)
- Exceptions: When uploads exist.
- Why EXTRA: Investigation coverage beyond the oracle.
- Evidence M-S001794: `output/template/.claude/skills/security-scan/references/scan-layers.md:214-216` — "When uploads exist, inspect size limits, storage path safety, file-name ⏎ handling, content/type assumptions, execution/public-serving risks, and ⏎ authorization. Client-provided MIME types are not authoritative."

### EXTRA-M-0197
- Closest oracle policies: WF-020
- Modality: DEFAULT
- Normative action: Consider rate limiting where abuse realistically matters (login, password reset, expensive anonymous/resource-intensive endpoints); do not require it on every endpoint.
- Trigger/scope: private reference of workflow security-scan (security scans)
- Exceptions: none
- Why EXTRA: Rate-limiting guidance not in the oracle.
- Evidence M-S001796: `output/template/.claude/skills/security-scan/references/scan-layers.md:220-222` — "Consider rate limiting where abuse could realistically matter — login and ⏎ password reset, expensive anonymous endpoints, resource-intensive operations. ⏎ Do not require rate limiting on every endpoint. `429` semantics: `http-api`."

### EXTRA-M-0198
- Closest oracle policies: WF-020, ARC-029
- Modality: MUST
- Normative action: Sensitive-data layer: review duplicate/missing security-relevant logging (without demanding logs for every request) and response data (entities returned directly, password hashes, security fields, unnecessary PII); explicit response contracts preferable where needed.
- Trigger/scope: private reference of workflow security-scan (security scans)
- Exceptions: none
- Why EXTRA: Investigation coverage beyond the oracle.
- Evidence M-S001800: `output/template/.claude/skills/security-scan/references/scan-layers.md:230-234` — "Look for logged passwords, access/refresh tokens, private keys, authentication ⏎ secrets, and full payment credentials; review PII against project requirements. ⏎ Debug/Trace level is not a security boundary. Review duplicate or missing ⏎ security-relevant logging in context; do not demand logs for every successful ⏎ request."
- Evidence M-S001804: `output/template/.claude/skills/security-scan/references/scan-layers.md:243-246` — "Look for database/domain entities returned directly, password hashes, internal ⏎ security fields, unnecessary personal information, and secret metadata. ⏎ Returning a Domain entity is not automatically vulnerable — inspect the actual ⏎ serialized fields — but explicit response contracts are preferable where needed."

### EXTRA-M-0199
- Closest oracle policies: WF-020, RUN-015
- Modality: MUST
- Normative action: Exceptional-conditions layer: review operations/inputs that can consume unbounded time, memory, rows, file/body size, retries or parallel work.
- Trigger/scope: private reference of workflow security-scan (security scans)
- Exceptions: none
- Why EXTRA: Investigation coverage beyond the oracle.
- Evidence M-S001817: `output/template/.claude/skills/security-scan/references/scan-layers.md:289-292` — "Review external operations or public inputs that can consume unbounded time, ⏎ memory, database rows, file size, request body, retry attempts, or parallel ⏎ work. A theoretical lack of a limit is not automatically High severity; evaluate ⏎ whether an attacker can actually exploit it."

### EXTRA-M-0200
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: Identify meaningful security-sensitive workflows (insecure design, tenant isolation, workflow abuse, privilege escalation, idempotency abuse, multi-step authorization) as candidates for threat modeling/manual review instead of claiming the static scan proves them secure.
- Trigger/scope: private reference of workflow security-scan (security scans)
- Exceptions: When such workflows exist.
- Why EXTRA: Design-review escalation obligation not in the oracle.
- Evidence M-S001824: `output/template/.claude/skills/security-scan/references/scan-layers.md:311-316` — "Static pattern checks do not fully cover A06 Insecure Design, tenant isolation, ⏎ business workflow abuse, privilege escalation through legitimate operations, ⏎ financial/idempotency abuse, or multi-step authorization problems. When the ⏎ application has meaningful security-sensitive workflows, identify them as ⏎ candidates for threat modeling or dedicated manual review instead of claiming ⏎ the s …"

### EXTRA-M-0201
- Closest oracle policies: API-017
- Modality: DEFAULT
- Normative action: For a new local Development API configure the launch profile to open Swagger when helpful; application HTTP/HTTPS URLs must agree with the launch profile (no HTTPS launch URL on an HTTP-only port).
- Trigger/scope: on-demand knowledge skill swagger (backend API documentation)
- Exceptions: When that helps.
- Why EXTRA: Launch-profile technique outside the oracle (EXC-008).
- Evidence M-S001889: `output/template/.claude/skills/swagger/SKILL.md:47-48` — "For a new local Development API, configure the launch profile so the browser ⏎ opens Swagger directly when that helps:"
- Evidence M-S001891: `output/template/.claude/skills/swagger/SKILL.md:57-58` — "The application's HTTP/HTTPS URLs must agree with the launch profile; do not ⏎ point the launch URL at HTTPS on an HTTP-only port."

### EXTRA-M-0202
- Closest oracle policies: API-016, DEP-012
- Modality: DEFAULT
- Normative action: For Bearer authentication expose a Bearer scheme so authenticated endpoints can be exercised from Swagger UI.
- Trigger/scope: on-demand knowledge skill swagger (backend API documentation)
- Exceptions: When the API uses Bearer auth.
- Why EXTRA: Usability configuration beyond API-016's accuracy requirement.
- Evidence M-S001900: `output/template/.claude/skills/swagger/SKILL.md:95-99` — "When the API actually uses authentication, configure the matching security ⏎ definition and requirements; for Bearer authentication expose a Bearer scheme so ⏎ authenticated endpoints can be exercised from Swagger UI. Do not add a scheme ⏎ merely because an authentication package is installed, and do not apply ⏎ authentication requirements globally to anonymous endpoints."

### EXTRA-M-0203
- Closest oracle policies: API-016
- Modality: DEFAULT
- Normative action: Document consumer-relevant contract information (preconditions, idempotency, pagination/filtering, outcomes); avoid descriptions that repeat action/property names.
- Trigger/scope: on-demand knowledge skill swagger (backend API documentation)
- Exceptions: none
- Why EXTRA: Documentation-content guidance not in the oracle.
- Evidence M-S001902: `output/template/.claude/skills/swagger/SKILL.md:103-105` — "Document what helps a consumer understand the contract — important ⏎ preconditions, idempotency semantics, pagination/filtering behavior, meaningful ⏎ outcomes. Avoid descriptions that repeat action or property names."

### EXTRA-M-0204
- Closest oracle policies: GOV-012
- Modality: MUST_NOT
- Normative action: XML comments only when the project chooses them for public contracts; do not add them to every internal type solely for Swagger.
- Trigger/scope: on-demand knowledge skill swagger (backend API documentation)
- Exceptions: Project chooses XML docs.
- Why EXTRA: Documentation practice outside the oracle.
- Evidence M-S001904: `output/template/.claude/skills/swagger/SKILL.md:109-110` — "XML comments may help public API contracts when the project chooses them; do not ⏎ add them to every internal type solely for Swagger."

### EXTRA-M-0205
- Closest oracle policies: API-016
- Modality: MUST_NOT
- Normative action: Use multiple Swagger documents only for a real contract separation (API versions, public/internal surfaces).
- Trigger/scope: on-demand knowledge skill swagger (backend API documentation)
- Exceptions: none
- Why EXTRA: Document-partitioning technique outside the oracle (EXC-008).
- Evidence M-S001906: `output/template/.claude/skills/swagger/SKILL.md:114-115` — "Use multiple Swagger documents only for a real contract separation, such as API ⏎ versions or distinct public/internal surfaces (`api-versioning` skill)."

### EXTRA-M-0206
- Closest oracle policies: ARC-029, API-016
- Modality: AVOID
- Normative action: Avoid unstable anonymous response shapes and anonymous objects as long-lived contracts; use explicit request/response contracts.
- Trigger/scope: on-demand knowledge skill swagger (backend API documentation)
- Exceptions: none
- Why EXTRA: Explicit-contract requirement for generated clients is not stated in the oracle (ARC-029 only discourages gratuitous DTO duplication).
- Evidence M-S001908: `output/template/.claude/skills/swagger/SKILL.md:119-122` — "When the contract feeds Angular or other client generation: treat breaking ⏎ schema changes seriously, keep response metadata accurate, avoid unstable ⏎ anonymous response shapes, use explicit request/response contracts, and review ⏎ generated-client changes when the contract changes."
- Evidence M-S001910: `output/template/.claude/skills/swagger/SKILL.md:126-128` — "Avoid treating Swagger as a substitute for integration tests, using anonymous ⏎ objects as important long-lived contracts, and adding a second competing ⏎ API-documentation stack without a concrete need."

### EXTRA-M-0207
- Closest oracle policies: TST-006
- Modality: AVOID
- Normative action: Avoid treating Swagger as a substitute for integration tests.
- Trigger/scope: on-demand knowledge skill swagger (backend API documentation)
- Exceptions: none
- Why EXTRA: Anti-pattern not in the oracle.
- Evidence M-S001910: `output/template/.claude/skills/swagger/SKILL.md:126-128` — "Avoid treating Swagger as a substitute for integration tests, using anonymous ⏎ objects as important long-lived contracts, and adding a second competing ⏎ API-documentation stack without a concrete need."

### EXTRA-M-0208
- Closest oracle policies: WF-006, DEP-012
- Modality: MUST
- Normative action: Open the Development Swagger UI to confirm it loads and exercise representative endpoints through it when meaningful.
- Trigger/scope: on-demand knowledge skill swagger (backend API documentation)
- Exceptions: When a meaningful behavioural check.
- Why EXTRA: Swagger-UI-specific verification step beyond the oracle.
- Evidence M-S001912: `output/template/.claude/skills/swagger/SKILL.md:132-139` — "When API behavior changes: ⏎  ⏎ 1. verify Controller behavior and relevant integration tests; ⏎ 2. verify response metadata; ⏎ 3. start the API when the change affects startup/composition; ⏎ 4. open the Development Swagger UI and confirm it loads; ⏎ 5. exercise representative endpoints through Swagger when that is a meaningful ⏎    behavioral check;"

### EXTRA-M-0209
- Closest oracle policies: none
- Modality: ENFORCED
- Normative action: template-maintenance runs only when the user invokes it; Claude must not start it automatically (disable-model-invocation: true).
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance; never automatic)
- Exceptions: none
- Why EXTRA: Invocation restriction on a repo/meta workflow; not an oracle policy.
- Evidence M-S001915: `output/template/.claude/skills/template-maintenance/SKILL.md:7-7` — "disable-model-invocation: true"
- Evidence M-S001919: `output/template/.claude/skills/template-maintenance/SKILL.md:14-15` — "This workflow runs only when the user invokes it. Claude must not start it ⏎ automatically."

### EXTRA-M-0210
- Closest oracle policies: none
- Modality: MUST
- Normative action: One authoritative owner per policy; elsewhere only routing pointers or yes/no check-by-reference, never reworded copies; decision summaries only in CLAUDE.md Architecture Defaults and docs/technology-stack.md; edit the owner in place and replace other copies with pointers.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance; never automatic)
- Exceptions: none
- Why EXTRA: Instruction-ownership invariant (repo/meta) not in the oracle.
- Evidence M-S001921: `output/template/.claude/skills/template-maintenance/SKILL.md:19-22` — "- One authoritative owner per policy. Elsewhere use a routing pointer ("run ⏎   workflow X", "see file Y") or a yes/no check-by-reference — never a reworded ⏎   copy. Decision summaries appear only in CLAUDE.md § Architecture Defaults and ⏎   `docs/technology-stack.md`."
- Evidence M-S001930: `output/template/.claude/skills/template-maintenance/SKILL.md:54-54` — "2. Edit the owner in place; replace any other copy with a pointer."

### EXTRA-M-0211
- Closest oracle policies: none
- Modality: MUST
- Normative action: Keep each policy at its trigger (planning-time policy in CLAUDE.md/technology-stack, area constraints in flat path-scoped rules, procedures in workflow skills); do not promote content into CLAUDE.md for easier loading nor demote planning-time policy to save tokens.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance; never automatic)
- Exceptions: none
- Why EXTRA: Instruction-placement invariant (repo/meta).
- Evidence M-S001922: `output/template/.claude/skills/template-maintenance/SKILL.md:23-27` — "- Keep each policy at its trigger: CLAUDE.md and `docs/technology-stack.md` only ⏎   for planning-time policy; a flat path-scoped rule for constraints on files of ⏎   an area; a workflow skill for procedure steps, stop conditions, and output ⏎   shape. Do not promote content into CLAUDE.md to make loading easier, and do not ⏎   demote planning-time policy to save tokens."

### EXTRA-M-0212
- Closest oracle policies: none
- Modality: MUST
- Normative action: Keep CLAUDE.md, docs/technology-stack.md and skill descriptions compact; descriptions start with concrete triggers.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance; never automatic)
- Exceptions: none
- Why EXTRA: Context-size and description-style invariant (repo/meta).
- Evidence M-S001925: `output/template/.claude/skills/template-maintenance/SKILL.md:34-35` — "- Keep CLAUDE.md, `docs/technology-stack.md`, and skill descriptions compact; ⏎   descriptions start with concrete triggers."

### EXTRA-M-0213
- Closest oracle policies: none
- Modality: MUST
- Normative action: Hooks fail visibly and point messages at the owning file instead of restating policy.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance; never automatic)
- Exceptions: none
- Why EXTRA: Hook-design invariant (repo/meta).
- Evidence M-S001926: `output/template/.claude/skills/template-maintenance/SKILL.md:36-46` — "- Hooks are registered in exec form — `"command": "node"` with ⏎   `"args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs"]`, never a shell ⏎   command string. The placeholder only locates the script; hooks derive the ⏎   repository root they inspect from the hook input (`cwd`, or the edited file's ⏎   location) and checkers from the current directory ⏎   (`.claude/scripts/repo-root.mjs`). Ho …"

### EXTRA-M-0214
- Closest oracle policies: WF-005
- Modality: MUST
- Normative action: For hook or script changes run the changed script with sample input and confirm both pass and failure paths.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance; never automatic)
- Exceptions: none
- Why EXTRA: Verification obligation for instruction-system scripts beyond the oracle.
- Evidence M-S001933: `output/template/.claude/skills/template-maintenance/SKILL.md:63-65` — "5. For hook or script changes, run the changed script with sample input (usage ⏎    is documented in each script's header) and confirm both the pass and the ⏎    failure paths."

### EXTRA-M-0215
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: Report files changed, owners added or moved, and the checker result after template maintenance.
- Trigger/scope: user-invoked workflow template-maintenance (instruction-system maintenance; never automatic)
- Exceptions: none
- Why EXTRA: Output-shape obligation of the maintenance workflow.
- Evidence M-S001934: `output/template/.claude/skills/template-maintenance/SKILL.md:66-66` — "6. Report the files changed, owners added or moved, and the checker result."

### EXTRA-M-0216
- Closest oracle policies: WF-005
- Modality: MUST_NOT
- Normative action: Do not use --no-restore unless restore is known to be complete.
- Trigger/scope: workflow verify (before declaring a change complete or preparing a PR)
- Exceptions: Restore known complete.
- Why EXTRA: Build-flag caution not in the oracle.
- Evidence M-S001947: `output/template/.claude/skills/verify/SKILL.md:47-50` — "For Angular changes, run the frontend's configured build command, typically ⏎ `npm run build`. Use a more targeted project or solution command when ⏎ appropriate, and do not use `--no-restore` unless restore is known to be ⏎ complete. A build failure means the implementation is not complete."

### EXTRA-M-0217
- Closest oracle policies: WF-005, WF-007
- Modality: DEFAULT
- Normative action: For small solutions run the complete test suite; for large solutions run affected projects first, then broader suites as risk requires.
- Trigger/scope: workflow verify (before declaring a change complete or preparing a PR)
- Exceptions: none
- Why EXTRA: Test-breadth policy not stated in WF-005.
- Evidence M-S001951: `output/template/.claude/skills/verify/SKILL.md:60-63` — "For Angular changes, run the test command configured in `package.json` — ⏎ inspect it rather than assuming a runner. For small solutions run the complete ⏎ suite; for large solutions run affected test projects first, then any broader ⏎ suite the repository or change risk requires."

### EXTRA-M-0218
- Closest oracle policies: RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: All files use UTF-8, space indentation, a final newline and trimmed trailing whitespace (Markdown keeps trailing whitespace).
- Trigger/scope: repository files (EditorConfig: IDE, dotnet format, build diagnostics)
- Exceptions: Markdown exempt from trailing-whitespace trimming.
- Why EXTRA: RUN-009 requires following .editorconfig but does not fix its content; these concrete formatting settings are candidate-specific.
- Evidence M-S001984: `output/template/.editorconfig:7-10` — "charset = utf-8 ⏎ indent_style = space ⏎ insert_final_newline = true ⏎ trim_trailing_whitespace = true"
- Evidence M-S001986: `output/template/.editorconfig:13-13` — "trim_trailing_whitespace = false"

### EXTRA-M-0219
- Closest oracle policies: RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: Indent 2 spaces for JSON/YAML, project/XML files and TS/JS/HTML/SCSS/CSS (TS/JS single quotes); 4 spaces for C#.
- Trigger/scope: repository files (EditorConfig: IDE, dotnet format, build diagnostics)
- Exceptions: none
- Why EXTRA: Concrete indentation/quote settings are candidate-specific (RUN-009 only defers to .editorconfig).
- Evidence M-S001988: `output/template/.editorconfig:16-16` — "indent_size = 2"
- Evidence M-S001990: `output/template/.editorconfig:19-19` — "indent_size = 2"
- Evidence M-S001992: `output/template/.editorconfig:22-23` — "indent_size = 2 ⏎ quote_type = single"
- Evidence M-S001994: `output/template/.editorconfig:26-26` — "indent_size = 4"

### EXTRA-M-0220
- Closest oracle policies: RUN-010
- Modality: ENFORCED_DEFAULT
- Normative action: System usings sorted first; using directives placed outside the namespace (suggestion).
- Trigger/scope: repository files (EditorConfig: IDE, dotnet format, build diagnostics)
- Exceptions: none
- Why EXTRA: Using-ordering/placement conventions not in the oracle.
- Evidence M-S001996: `output/template/.editorconfig:29-30` — "dotnet_sort_system_directives_first = true ⏎ csharp_using_directive_placement = outside_namespace:suggestion"

### EXTRA-M-0221
- Closest oracle policies: RUN-009
- Modality: ENFORCED_ADVISORY
- Normative action: Do not qualify fields, properties, methods or events with this. (suggestion).
- Trigger/scope: repository files (EditorConfig: IDE, dotnet format, build diagnostics)
- Exceptions: none
- Why EXTRA: Qualification style not in the oracle.
- Evidence M-S002004: `output/template/.editorconfig:45-48` — "dotnet_style_qualification_for_field = false:suggestion ⏎ dotnet_style_qualification_for_property = false:suggestion ⏎ dotnet_style_qualification_for_method = false:suggestion ⏎ dotnet_style_qualification_for_event = false:suggestion"

### EXTRA-M-0015
- Closest oracle policies: none
- Modality: DEFINITION
- Normative action: Interpret 'must / must not' so that any violation is a defect.
- Trigger/scope: always (CLAUDE.md is always loaded)
- Exceptions: none
- Why EXTRA: Interpretive meta-rule; the oracle defines no modal vocabulary. It fixes the binding force of every candidate 'must' (no 'must' is softened to guidance).
- Evidence M-S000283: `output/template/CLAUDE.md:13-13` — "- **must / must not** — a violation is a defect."

### EXTRA-M-0016
- Closest oracle policies: none
- Modality: MUST
- Normative action: Any deviation from a rule marked 'default' needs a concrete reason and must be reported.
- Trigger/scope: always (CLAUDE.md is always loaded)
- Exceptions: none
- Why EXTRA: The oracle's DEFAULT policies allow deviation with justification but do not require deviations to be reported; this adds a reporting obligation to all candidate defaults.
- Evidence M-S000284: `output/template/CLAUDE.md:14-14` — "- **default** — deviation needs a concrete reason and must be reported."

### EXTRA-M-0017
- Closest oracle policies: none
- Modality: DEFINITION
- Normative action: Treat 'prefer / avoid' wording as guidance (non-binding).
- Trigger/scope: always (CLAUDE.md is always loaded)
- Exceptions: none
- Why EXTRA: Relaxing meta-rule: several oracle DEFAULT/MUST policies are worded with prefer/avoid in the candidate; this vocabulary downgrades them to guidance, which the oracle does not entail.
- Evidence M-S000285: `output/template/CLAUDE.md:15-15` — "- **prefer / avoid** — guidance."

### EXTRA-M-0018
- Closest oracle policies: GOV-001, GOV-017
- Modality: MUST_NOT
- Normative action: Product inputs (SPECIFICATION.md, CUSTOM_SETTINGS.md, feature specs, task prompts) are not instruction layers and never silently override CLAUDE.md, docs/technology-stack.md or .claude/rules/; a product request for an engineering decision goes through Decision Control.
- Trigger/scope: always (CLAUDE.md is always loaded)
- Exceptions: none
- Why EXTRA: Establishes a precedence of engineering instruction layers over product inputs (including task prompts); GOV-001 makes the spec authoritative for product behaviour but says nothing about product inputs being unable to override engineering instructions.
- Evidence M-S000288: `output/template/CLAUDE.md:20-24` — "`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specifications, and task ⏎ prompts are product inputs, not instruction layers. They may request an ⏎ engineering decision, but they never silently override this file, ⏎ `docs/technology-stack.md`, or `.claude/rules/`; such a request goes through ⏎ Decision Control."
- Evidence M-S001927: `output/template/.claude/skills/template-maintenance/SKILL.md:47-48` — "- Product inputs (`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`) stay inputs; they do ⏎   not carry instructions."

### EXTRA-M-0019
- Closest oracle policies: ARC-020, ARC-001
- Modality: REQUIRES_APPROVAL
- Normative action: Any changed project reference graph is Reserved (requires approval).
- Trigger/scope: always (CLAUDE.md is always loaded)
- Exceptions: Unless already required by spec/established structure.
- Why EXTRA: ARC-020 gates new layers/projects; the oracle does not require approval for changing references between existing projects (ARC-001 only constrains direction).
- Evidence M-S000316: `output/template/CLAUDE.md:118-119` — "3. a new production project, layer, or assembly, a changed project reference ⏎      graph, or an additional `DbContext`/persistence boundary;"
- Evidence M-S000407: `output/template/.claude/hooks/dependency-guard.mjs:130-133` — "if (referenceChanges.length > 0) { ⏎     commandOwners.push('confirm the project references follow .claude/rules/architecture.md (Project References) and that a ' + ⏎       'changed production reference graph went through CLAUDE.md § Decision Control'); ⏎   }"

### EXTRA-M-0020
- Closest oracle policies: ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Introducing search, external storage or external identity infrastructure is Reserved.
- Trigger/scope: always (CLAUDE.md is always loaded)
- Exceptions: Unless already required.
- Why EXTRA: ARC-020's enumerated categories are messaging/background/distributed caching/auth architecture; search and external storage (and identity as an infrastructure category) are additional approval gates.
- Evidence M-S000318: `output/template/CLAUDE.md:121-122` — "5. a new infrastructure category (messaging, background processing, ⏎      distributed caching, search, external storage, external identity);"

### EXTRA-M-0021
- Closest oracle policies: DEP-001, GOV-013
- Modality: REQUIRES_APPROVAL
- Normative action: Adding any major library or framework is Reserved (requires approval).
- Trigger/scope: always (CLAUDE.md is always loaded)
- Exceptions: Unless already required.
- Why EXTRA: Oracle requires a concrete need (DEP-001/GOV-013) and approval only for replacement or risky licenses; approval for every major library addition is an added gate.
- Evidence M-S000319: `output/template/CLAUDE.md:123-123` — "6. a major library or framework, or replacing an approved baseline technology;"
- Evidence M-S000596: `output/template/.claude/skills/add-dependency/SKILL.md:21-23` — "- A major library or framework, a new infrastructure capability, or the ⏎   replacement of an approved technology is Reserved (CLAUDE.md § Decision ⏎   Control): stop and run `architecture-decision`."

### EXTRA-M-0022
- Closest oracle policies: ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: Any project-wide convention or abstraction other code must follow is Reserved.
- Trigger/scope: always (CLAUDE.md is always loaded)
- Exceptions: Unless already required.
- Why EXTRA: Generalises ARC-020's 'project-wide Result' example to every project-wide convention/abstraction.
- Evidence M-S000320: `output/template/CLAUDE.md:124-125` — "7. a project-wide convention or abstraction other code must follow (for ⏎      example a project-wide Result model);"

### EXTRA-M-0023
- Closest oracle policies: API-013, DEP-017
- Modality: REQUIRES_APPROVAL
- Normative action: Adopting API versioning is Reserved (requires explicit approval).
- Trigger/scope: always (CLAUDE.md is always loaded)
- Exceptions: Unless already required.
- Why EXTRA: API-013 permits versioning when a concrete compatibility need exists without an approval gate; the candidate adds explicit approval for adoption.
- Evidence M-S000061: `output/template/.claude/rules/api.md:33-35` — "- Do not introduce API versioning merely because an API exists; add it when ⏎   published compatibility or coexistence of client generations creates a ⏎   concrete need. Adopting versioning is a Reserved decision."
- Evidence M-S000322: `output/template/CLAUDE.md:127-127` — "9. a breaking public API change or adopting API versioning;"

### EXTRA-M-0024
- Closest oracle policies: GOV-017
- Modality: MUST
- Normative action: In an unclear case classify as Reserved if any answer is yes: adds/removes/replaces a dependency, framework or infrastructure capability; changes a project/layer/reference boundary; establishes a convention other code follows; changes observable behaviour or a public contract; would be expensive to reverse.
- Trigger/scope: always (CLAUDE.md is always loaded)
- Exceptions: Only for cases not otherwise clear.
- Why EXTRA: GOV-017 names the classes but no classification test; this heuristic widens Reserved (e.g. adding or removing any dependency, any expensive-to-reverse choice) beyond the oracle's approval gates.
- Evidence M-S000324: `output/template/CLAUDE.md:130-134` — "Unclear case — any "yes" makes it Reserved: (1) Does it add, remove, or replace ⏎ a dependency, framework, or infrastructure capability? (2) Does it change a ⏎ project/layer/reference boundary? (3) Does it establish a convention other code ⏎ is expected to follow? (4) Does it change observable behavior or a public ⏎ contract? (5) Would it be expensive to reverse once other code depends on it?"

### EXTRA-M-0025
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST
- Normative action: An explicit user instruction counts as approval and must be recorded through the architecture-decision workflow.
- Trigger/scope: always (CLAUDE.md is always loaded)
- Exceptions: none
- Why EXTRA: Defines what constitutes approval and adds a recording obligation for every approved Reserved decision; not entailed by GOV-017 (GOV-007 only covers approved behavioural rules).
- Evidence M-S000326: `output/template/CLAUDE.md:138-138` — "An explicit user instruction counts as approval and is recorded through the same"
- Evidence M-S000327: `output/template/CLAUDE.md:139-139` — "workflow. In an autonomous or headless run, never make a Reserved decision:"
- Evidence M-S000710: `output/template/.claude/skills/architecture-decision/SKILL.md:43-44` — "An explicit approval — including an explicit instruction in the original request ⏎ — is recorded before the Reserved part is implemented:"

### EXTRA-M-0026
- Closest oracle policies: DEP-008
- Modality: MUST
- Normative action: Use .NET 10 on its latest stable servicing release.
- Trigger/scope: always (imported by CLAUDE.md)
- Exceptions: none
- Why EXTRA: DEP-008 fixes the major platform (.NET 10 LTS) only; requiring the latest stable servicing (patch) release is an additional version constraint.
- Evidence M-S000362: `output/template/docs/technology-stack.md:12-14` — "- Platform: .NET 10 LTS on its latest stable servicing release, C# 14, ⏎   ASP.NET Core, ASP.NET Core Controllers. Moving to a preview/RC .NET or C# ⏎   release requires approval."

### EXTRA-M-0027
- Closest oracle policies: DEP-010
- Modality: MUST_NOT
- Normative action: Do not use a deprecated or legacy ASP.NET automatic-validation integration package.
- Trigger/scope: always (imported by CLAUDE.md)
- Exceptions: Concrete requirement.
- Why EXTRA: Oracle names FluentValidation as standard but does not prohibit its automatic ASP.NET validation integration packages.
- Evidence M-S000364: `output/template/docs/technology-stack.md:18-22` — "- Validation: FluentValidation (`FluentValidation`, ⏎   `FluentValidation.DependencyInjectionExtensions`) is the standard library for ⏎   explicit request and use-case validation; do not use a deprecated or legacy ⏎   ASP.NET automatic-validation integration package without a concrete ⏎   requirement."
- Evidence M-S000479: `output/template/.claude/scripts/check-manifests.mjs:40-40` — "['fluentvalidation.aspnetcore', 'legacy automatic-validation integration - needs a concrete reason (docs/technology-stack.md)'],"
- Evidence M-S000492: `output/template/.claude/scripts/check-manifests.mjs:219-223` — "function checkNuGetId(id, rel, result) { ⏎   const lower = id.toLowerCase(); ⏎   if (DENIED_NUGET.has(lower)) result.violations.push({ file: rel, message: `${id}: ${DENIED_NUGET.get(lower)}` }); ⏎   if (REVIEW_NUGET.has(lower)) result.notes.push({ file: rel, message: `${id}: ${REVIEW_NUGET.get(lower)}` }); ⏎ }"
- Evidence M-S000745: `output/template/.claude/skills/aspnet-error-handling/SKILL.md:152-156` — "Register validators with `FluentValidation.DependencyInjectionExtensions` ⏎ (`services.AddValidatorsFromAssemblyContaining<...>()`), and follow the ⏎ project's established validation invocation pattern rather than adding a second ⏎ competing mechanism. Do not add a deprecated automatic-validation integration ⏎ package to connect FluentValidation to the pipeline."

### EXTRA-M-0028
- Closest oracle policies: DEP-011, DEP-002, ARC-002
- Modality: MUST_NOT
- Normative action: No other mapping framework without approval; mapping-library concerns stay out of Domain.
- Trigger/scope: always (imported by CLAUDE.md)
- Exceptions: Approval.
- Why EXTRA: DEP-011 approves Mapster conditionally but does not forbid other mappers or exclude mapping-library concerns from Domain (ARC-002 lists EF/ASP.NET/HTTP/persistence/external-service concerns only).
- Evidence M-S000375: `output/template/docs/technology-stack.md:56-59` — "- Mapping: manual mapping is fine for simple cases; Mapster (`Mapster`, ⏎   `Mapster.DependencyInjection`) is approved when mapping volume warrants it. ⏎   No other mapping framework without approval; mapping-library concerns stay ⏎   out of Domain."

### EXTRA-M-0029
- Closest oracle policies: RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: Nullable reference types are enabled for every project.
- Trigger/scope: all .NET projects in the repository (MSBuild auto-import)
- Exceptions: Project-level override possible.
- Why EXTRA: The oracle does not mandate nullable reference types; this executable build default changes compiler diagnostics for all code.
- Evidence M-S000344: `output/template/Directory.Build.props:9-9` — "<Nullable>enable</Nullable>"

### EXTRA-M-0030
- Closest oracle policies: RUN-010
- Modality: ENFORCED_DEFAULT
- Normative action: Implicit global usings are enabled for every project.
- Trigger/scope: all .NET projects in the repository (MSBuild auto-import)
- Exceptions: Project-level override possible.
- Why EXTRA: Not in the oracle; affects which usings are redundant (RUN-010) and the compile surface.
- Evidence M-S000345: `output/template/Directory.Build.props:10-10` — "<ImplicitUsings>enable</ImplicitUsings>"

### EXTRA-M-0031
- Closest oracle policies: WF-007
- Modality: ENFORCED_DEFAULT
- Normative action: .NET analyzers run at AnalysisLevel=latest for every project.
- Trigger/scope: all .NET projects in the repository (MSBuild auto-import)
- Exceptions: Project-level override possible.
- Why EXTRA: The oracle has no analyzer-level requirement; enables newest analyzer rule set repo-wide.
- Evidence M-S000346: `output/template/Directory.Build.props:11-11` — "<AnalysisLevel>latest</AnalysisLevel>"

### EXTRA-M-0032
- Closest oracle policies: RUN-009
- Modality: ENFORCED_DEFAULT
- Normative action: .editorconfig code-style diagnostics are enforced during build (EnforceCodeStyleInBuild=true).
- Trigger/scope: all .NET projects in the repository (MSBuild auto-import)
- Exceptions: Project-level override possible.
- Why EXTRA: RUN-009 says follow .editorconfig; making IDE code-style rules build diagnostics is an additional executable enforcement.
- Evidence M-S000348: `output/template/Directory.Build.props:13-13` — "<EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>"

## LINK_UNCERTAIN constraints (2)

### UNCERTAIN-M-0001
- Closest oracle policies: RUN-021
- Modality: ALLOWED
- Normative action: Invalidating a cache entry before the underlying mutation is known to have succeeded is acceptable only when the workflow deliberately accepts that behaviour.
- Trigger/scope: on-demand knowledge skill caching (backend)
- Exceptions: Deliberate workflow acceptance.
- Open question: Open question: is pre-success invalidation (which never makes the cache a second source of truth) still 'consistent with successful underlying mutations' under RUN-021, or does this clause relax RUN-021 with an exception?
- Evidence M-S000887: `output/template/.claude/skills/caching/SKILL.md:92-94` — "Invalidating before the"

### UNCERTAIN-M-0002
- Closest oracle policies: GOV-015
- Modality: ALLOWED
- Normative action: Destructive Git operations may be performed when explicitly requested or clearly required by an approved workflow.
- Trigger/scope: workflow git-workflow (Git operations requested by the user)
- Exceptions: Approved workflow requirement.
- Open question: Open question: does 'clearly required by an approved workflow' relax GOV-015 (which permits repository-changing Git operations only when explicitly requested), or is an approved workflow itself an explicit request?
- Evidence M-S001295: `output/template/.claude/skills/git-workflow/SKILL.md:98-102` — "Treat `git reset --hard`, `git clean`, `git push --force`, ⏎ `git push --force-with-lease`, branch deletion, and rebase of shared history as ⏎ high-risk. Perform them only when explicitly requested or clearly required by an ⏎ approved workflow, and inspect what will be lost or rewritten before executing ⏎ them."

