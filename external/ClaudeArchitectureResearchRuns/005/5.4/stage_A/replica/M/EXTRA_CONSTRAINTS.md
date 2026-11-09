# M — EXTRA and LINK_UNCERTAIN constraints (Claude Run 2, blind replica)

Every constraint below is an effective candidate behavior judged not entailed by the 196 oracle policies (EXTRA) or whose relation could not be decided (LINK_UNCERTAIN). Citations are template-relative paths under `inputs/M/output/template/` with exact source quotes (newlines shown as ⏎).

## EXTRA (26)

### EXTRA-M-0001
- Closest oracle policies: ARC-020, ARC-001, GOV-017
- Modality: REQUIRES_APPROVAL (Reserved; PostToolUse routing)
- Normative action: A changed production project reference graph, including a removed project file, is a Reserved decision that goes through Decision Control.
- Trigger/scope: .NET project references and project files
- Exceptions: Already required by the specification or established project structure.
- Why EXTRA: ARC-020 requires approval for new layers/projects and ARC-001 constrains direction; no oracle policy makes individual reference edges or project removal Reserved.
- Evidence:
  - `.claude/hooks/dependency-guard.mjs:130-133` (MIXED, M-S000023): "changed production reference graph went through CLAUDE.md § Decision Control"
  - `.claude/hooks/dependency-guard.mjs:169-170` (EXTRA, M-S000027): "which goes through CLAUDE.md § Decision Control"
  - `.claude/MAP.md:113-113` (DUPLICATE, M-S000095): "| `.claude/hooks/dependency-guard.mjs` | Blocks npm force/legacy-peer-deps installs (also behind npm global options); after dependency or `dotnet` project-reference commands, runs manifest checks and routes to `add-dependency` or `architecture.md` § Project References; after any other shell command, and after a failed one, checks the manifests whose content changed since the last check (one initia"
  - `CLAUDE.md:118-119` (MIXED, M-S001817): "3. a new production project, layer, or assembly, a changed project reference"

### EXTRA-M-0002
- Closest oracle policies: GOV-017, ARC-020
- Modality: REQUIRES_APPROVAL
- Normative action: For an unclear decision, any 'yes' to five questions makes it Reserved: does it add, remove or replace a dependency, framework or infrastructure capability; change a project, layer or reference boundary; establish a convention other code is expected to follow; change observable behavior or a public contract; or would it be expensive to reverse once other code depends on it.
- Trigger/scope: decision classification
- Exceptions: none stated
- Why EXTRA: GOV-017 defines Decided/Delegated/Reserved classes; the oracle does not provide a test that turns any of these properties into a Reserved decision.
- Evidence:
  - `.claude/hooks/dependency-guard.mjs:169-170` (EXTRA, M-S000027): "which goes through CLAUDE.md § Decision Control"
  - `CLAUDE.md:130-134` (EXTRA, M-S001821): "Unclear case — any"

### EXTRA-M-0003
- Closest oracle policies: DEP-001
- Modality: MUST
- Normative action: Dependency removals follow the add-dependency workflow like additions and updates.
- Trigger/scope: NuGet and npm dependency removals
- Exceptions: none stated
- Why EXTRA: DEP-001..DEP-005 govern additions and updates; no oracle policy routes removals through the dependency workflow.
- Evidence:
  - `.claude/hooks/file-change.mjs:65-68` (MIXED, M-S000043): "dependency additions, updates, and removals follow the add-dependency workflow."
  - `.claude/rules/dependencies.md:13-16` (MIXED, M-S000217): "Adding, updating, or removing a dependency follows `add-dependency` (version"
  - `CLAUDE.md:155-166` (MIXED, M-S001829): "| Adding, updating, or removing a NuGet/npm dependency | `add-dependency` |"

### EXTRA-M-0004
- Closest oracle policies: none
- Modality: MUST
- Normative action: Ownership of instruction content: rules and CLAUDE.md hold normative policy; workflow skills hold procedures, stop conditions and output shape; knowledge skills hold technique and examples only and own no policy; hooks, scripts and configuration enforce what is mechanically checkable; a pointer or check-by-reference is never a second owner.
- Trigger/scope: instruction-system maintenance
- Exceptions: none stated
- Why EXTRA: Instruction-system ownership rule; the oracle does not regulate where instruction content lives.
- Evidence:
  - `.claude/MAP.md:22-26` (EXTRA, M-S000078): "is never a second owner."
  - `.claude/MAP.md:74-77` (EXTRA, M-S000087): "owns no policy, and has no mechanical enforcement;"
  - `.claude/skills/architecture-decision/SKILL.md:56-57` (EXTRA, M-S000526): "owning `.claude/rules/` file in place — one owner, no copies elsewhere."
  - `.claude/skills/security-scan/SKILL.md:151-154` (EXTRA, M-S001666): "`httpclient-factory`, `ef-core`, and `angular` skills. Do not duplicate their"
  - `.claude/skills/template-maintenance/SKILL.md:19-22` (EXTRA, M-S001718): "One authoritative owner per policy."
  - `.claude/skills/template-maintenance/SKILL.md:28-29` (EXTRA, M-S001720): "Knowledge skills and private references hold technique only; they never own a"
  - `CLAUDE.md:152-153` (EXTRA, M-S001828): "Workflow skills own procedures, stop conditions, and output shape."

### EXTRA-M-0005
- Closest oracle policies: none
- Modality: MUST
- Normative action: New instruction content is placed by kind (planning-time governance and decisions in the compact CLAUDE.md or technology-stack; area constraints in a flat path rule whose paths cover the needed scope; procedures, stop conditions and output formats in workflow skills; technique in knowledge skills or their references; mechanical checks in scripts or hooks plus a concise rule), after which MAP.md is updated and check-instructions is run.
- Trigger/scope: instruction-system maintenance
- Exceptions: none stated
- Why EXTRA: Instruction-system maintenance procedure; no oracle policy governs instruction placement.
- Evidence:
  - `.claude/MAP.md:198-212` (EXTRA, M-S000104): "Needed while planning, before any file is opened (governance, approval"
  - `.claude/skills/template-maintenance/SKILL.md:23-27` (EXTRA, M-S001719): "Keep each policy at its trigger:"
  - `.claude/skills/template-maintenance/SKILL.md:34-35` (EXTRA, M-S001722): "Keep CLAUDE.md, `docs/technology-stack.md`, and skill descriptions compact;"
  - `.claude/skills/template-maintenance/SKILL.md:52-55` (EXTRA, M-S001726): "3. Update `.claude/MAP.md` (file table and topic index)."
  - `.claude/skills/template-maintenance/SKILL.md:56-61` (EXTRA, M-S001727): "structure checker and fix every failure:"

### EXTRA-M-0006
- Closest oracle policies: none
- Modality: MUST (checker-enforced)
- Normative action: Hooks are registered in exec form (node plus the script path anchored at ${CLAUDE_PROJECT_DIR}, no shell), including the dependency guard for PostToolUseFailure; the PreToolUse guard fails closed (onFailure block) while advisory hooks fail open.
- Trigger/scope: hook configuration
- Exceptions: none stated
- Why EXTRA: Hook wiring is template infrastructure; no oracle policy addresses hook registration or failure modes.
- Evidence:
  - `.claude/MAP.md:111-111` (EXTRA, M-S000093): "the PreToolUse guard fails closed"
  - `.claude/scripts/check-instructions.mjs:11-21` (EXTRA, M-S000351): "header on every instruction"
  - `.claude/scripts/check-instructions.mjs:44-53` (EXTRA, M-S000356): "const REQUIRED_HOOKS = ["
  - `.claude/scripts/check-instructions.mjs:263-328` (EXTRA, M-S000366): "so a failing or timed-out guard blocks the tool call"
  - `.claude/settings.json:3-39` (EXTRA, M-S000401): ""onFailure": "block""
  - `.claude/skills/template-maintenance/SKILL.md:36-46` (EXTRA, M-S001723): "command string. The placeholder only locates the script; hooks derive the"

### EXTRA-M-0007
- Closest oracle policies: API-013, ARC-020
- Modality: REQUIRES_APPROVAL (Reserved)
- Normative action: Adopting API versioning is a Reserved decision even when a concrete compatibility need exists.
- Trigger/scope: HTTP API versioning
- Exceptions: none stated
- Why EXTRA: API-013 allows introducing versioning for a concrete compatibility need without requiring approval; ARC-020's consequential-change list does not name versioning adoption.
- Evidence:
  - `.claude/rules/api.md:33-35` (MIXED, M-S000138): "Adopting versioning is a Reserved decision."
  - `CLAUDE.md:127-127` (MIXED, M-S001819): "9. a breaking public API change or adopting API versioning;"

### EXTRA-M-0008
- Closest oracle policies: none
- Modality: MUST (checker-enforced)
- Normative action: Instruction-system structure: required files exist; CLAUDE.md imports only docs/technology-stack.md and no other instruction file imports; every instruction file starts with a one-line '> Owns: ...
- Trigger/scope: Scope: ...
- Exceptions: Loads: ...' header whose Loads value matches its kind; no Level:/Kind: classification lines; .claude/rules stays flat with non-empty paths; skill folders hold SKILL.md plus optional Markdown references; the required workflow and knowledge skills exist with name equal to the folder, a description of at most 1024 characters, knowledge descriptions starting with 'Use when'; no competing serilog/resilience skills; template-maintenance is user-only; the code-reviewer stays a thin wrapper; private references are used only by their owning skill; file, section and skill references resolve; MAP.md lists every instruction, hook and script file and is never imported; an always-loaded estimate above about 6000 tokens is warned.
- Why EXTRA: instruction-system files
- Evidence:
  - `.claude/scripts/check-instructions.mjs:11-21` (EXTRA, M-S000351): "header on every instruction"
  - `.claude/scripts/check-instructions.mjs:27-30` (EXTRA, M-S000353): "const REQUIRED_FILES = ["
  - `.claude/scripts/check-instructions.mjs:31-39` (EXTRA, M-S000354): "const WORKFLOW_SKILLS = ["
  - `.claude/scripts/check-instructions.mjs:40-43` (EXTRA, M-S000355): "const FORBIDDEN_SKILLS = ['serilog', 'resilience'];"
  - `.claude/scripts/check-instructions.mjs:65-102` (EXTRA, M-S000358): "fail(`missing required file ${file}`)"
  - `.claude/scripts/check-instructions.mjs:104-114` (EXTRA, M-S000359): "only CLAUDE.md imports"
  - `.claude/scripts/check-instructions.mjs:116-136` (EXTRA, M-S000360): "first line after frontmatter must be"
  - `.claude/scripts/check-instructions.mjs:138-154` (EXTRA, M-S000361): ".claude/rules/ must stay flat (no subdirectories)"
  - `.claude/scripts/check-instructions.mjs:156-178` (EXTRA, M-S000362): "must set disable-model-invocation: true (user-only workflow)"
  - `.claude/scripts/check-instructions.mjs:180-189` (MIXED, M-S000363): "must disallow Write and Edit (read-only reviewer)"
  - `.claude/scripts/check-instructions.mjs:191-249` (EXTRA, M-S000364): "references private reference"
  - `.claude/scripts/check-instructions.mjs:251-261` (EXTRA, M-S000365): "MAP.md must not be imported (it is human-facing only)"
  - `.claude/scripts/check-instructions.mjs:330-335` (EXTRA, M-S000367): "check for content that belongs in a rule, workflow, or skill"
  - `.claude/skills/template-maintenance/SKILL.md:7-7` (EXTRA, M-S001712): "disable-model-invocation: true"
  - `.claude/skills/template-maintenance/SKILL.md:14-15` (EXTRA, M-S001716): "This workflow runs only when the user invokes it."
  - `.claude/skills/template-maintenance/SKILL.md:30-33` (EXTRA, M-S001721): "`.claude/rules/` stays flat. CLAUDE.md imports only"
  - `.claude/skills/template-maintenance/SKILL.md:34-35` (EXTRA, M-S001722): "Keep CLAUDE.md, `docs/technology-stack.md`, and skill descriptions compact;"
  - `.claude/skills/template-maintenance/SKILL.md:56-61` (EXTRA, M-S001727): "structure checker and fix every failure:"

### EXTRA-M-0009
- Closest oracle policies: DEP-004, DEP-020
- Modality: MUST NOT (manifest check violation; no approval path)
- Normative action: Microsoft.Extensions.Http.Polly and Polly.Extensions.Http (deprecated resilience integration packages) must not be added; their presence is reported as a violation with blocking hook feedback.
- Trigger/scope: NuGet manifests
- Exceptions: none stated
- Why EXTRA: DEP-004 requires deprecation checks and DEP-020 prefers the Microsoft resilience packages; no oracle policy forbids specific packages outright regardless of approval.
- Evidence:
  - `.claude/scripts/check-manifests.mjs:29-33` (EXTRA, M-S000374): "// Packages that must not be added."
  - `.claude/scripts/check-manifests.mjs:219-223` (MIXED, M-S000384): "if (DENIED_NUGET.has(lower))"
  - `.claude/skills/add-dependency/SKILL.md:25-31` (MIXED, M-S000411): "Do not add the deprecated `Microsoft.Extensions.Http.Polly` or"

### EXTRA-M-0010
- Closest oracle policies: DEP-001, GOV-014
- Modality: MUST
- Normative action: Remove dependencies that are no longer used when doing so is part of the current change and safe to verify; do not leave dead package references behind.
- Trigger/scope: dependency changes
- Exceptions: Unrelated cleanup in a narrowly scoped task.
- Why EXTRA: DEP-001 governs adding dependencies and GOV-014 limits scope; no oracle policy requires removing unused dependencies.
- Evidence:
  - `.claude/skills/add-dependency/SKILL.md:141-143` (MIXED, M-S000435): "do not leave dead package references behind."

### EXTRA-M-0011
- Closest oracle policies: DEP-004, DEP-005, WF-009
- Modality: MUST
- Normative action: The add-dependency report states the package, selected version, license, checks performed and approval status (approved / awaiting approval / not needed).
- Trigger/scope: dependency changes
- Exceptions: none stated
- Why EXTRA: DEP-004/DEP-005 require the checks and approval gate and WF-009 truthful verification reporting; no oracle policy prescribes the dependency report contents.
- Evidence:
  - `.claude/skills/add-dependency/SKILL.md:147-148` (EXTRA, M-S000437): "Report the package, selected version, license, checks performed, and approval"

### EXTRA-M-0012
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST
- Normative action: An approved Reserved decision (including an explicit instruction in the original request) is recorded before its Reserved part is implemented: a record docs/decisions/NNNN-short-title.md with Status, Date, Context, Decision, Alternatives considered and Consequences, plus an update of the planning-time owner (CLAUDE.md Architecture Defaults or docs/technology-stack.md); new path-rule constraints are edited into the owning rule; rejected or deferred decisions worth keeping are recorded with that status.
- Trigger/scope: approved decisions
- Exceptions: Product behavior and tunable values go to SPECIFICATION.md / CUSTOM_SETTINGS.md.
- Why EXTRA: GOV-017 requires approval for Reserved decisions but no recording artifact; no oracle policy requires decision records or planning-owner updates.
- Evidence:
  - `.claude/skills/architecture-decision/SKILL.md:43-48` (EXTRA, M-S000524): "is recorded before the Reserved part is implemented:"
  - `.claude/skills/architecture-decision/SKILL.md:49-55` (MIXED, M-S000525): "product behavior or tunable values → `SPECIFICATION.md`, or"
  - `.claude/skills/architecture-decision/SKILL.md:56-57` (EXTRA, M-S000526): "owning `.claude/rules/` file in place — one owner, no copies elsewhere."
  - `.claude/skills/architecture-decision/SKILL.md:62-63` (EXTRA, M-S000529): "When the discussion is worth keeping, record it with Status Rejected or"
  - `.claude/skills/architecture-decision/SKILL.md:67-68` (MIXED, M-S000531): "The Decision Request (or the recorded decision and the files updated), and the"
  - `CLAUDE.md:138-141` (MIXED, M-S001823): "An explicit user instruction counts as approval and is recorded through the same"

### EXTRA-M-0013
- Closest oracle policies: DEP-010, API-010
- Modality: MUST
- Normative action: Register FluentValidation validators with FluentValidation.DependencyInjectionExtensions (AddValidatorsFromAssemblyContaining) and follow the project's established validation invocation pattern rather than a second competing mechanism.
- Trigger/scope: backend validation setup
- Exceptions: none stated
- Why EXTRA: DEP-010 fixes FluentValidation as the library and API-010 the validation boundaries; no oracle policy prescribes the registration package or method.
- Evidence:
  - `.claude/skills/aspnet-error-handling/SKILL.md:152-156` (MIXED, M-S000556): "Register validators with `FluentValidation.DependencyInjectionExtensions`"
  - `docs/technology-stack.md:18-22` (MIXED, M-S001849): "`FluentValidation.DependencyInjectionExtensions`) is the standard library for"

### EXTRA-M-0014
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: The build-fix report states the initial failure, root cause, changes made, backend build / frontend build / tests status (PASS, NOT RUN, NOT APPLICABLE) and remaining issues.
- Trigger/scope: build and test repair
- Exceptions: none stated
- Why EXTRA: WF-009 requires reporting actual verification states only; the failure, root-cause, changes and remaining-issues sections are additional reporting duties.
- Evidence:
  - `.claude/skills/build-fix/SKILL.md:243-251` (MIXED, M-S000671): "Backend build: PASS / NOT RUN / NOT APPLICABLE"

### EXTRA-M-0016
- Closest oracle policies: WF-011, WF-012
- Modality: MUST
- Normative action: Code-review findings are reported ordered by severity, each with severity, file/location, what is wrong, why it matters and the smallest reasonable fix, using the fixed severity scale Critical / High / Medium / Low with defined meanings.
- Trigger/scope: code review output
- Exceptions: none stated
- Why EXTRA: WF-011/WF-012 govern priorities and honesty of findings; the oracle does not prescribe a findings format or severity scale.
- Evidence:
  - `.claude/skills/code-review/SKILL.md:175-184` (EXTRA, M-S000787): "For each finding provide: severity,"

### EXTRA-M-0017
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: The development-workflow output reports what changed, Delegated choices worth noting, unresolved Decision Requests, the verify report and every change-specific obligation that was not applicable with the reason.
- Trigger/scope: implementation reports
- Exceptions: none stated
- Why EXTRA: WF-009 requires truthful verification reporting and GOV-017 reporting of unresolved Decision Requests; no oracle policy requires reporting delegated choices or non-applicable obligations.
- Evidence:
  - `.claude/skills/development-workflow/SKILL.md:119-121` (MIXED, M-S000906): "Report what changed, Delegated choices worth noting, unresolved Decision"

### EXTRA-M-0018
- Closest oracle policies: GOV-015, GOV-020
- Modality: MUST NOT
- Normative action: main, master and other protected or shared branches are treated as non-rewritable; a shared branch is never force-pushed unless the user explicitly requests history rewriting and the consequences are understood.
- Trigger/scope: push and history rewriting
- Exceptions: Explicit user request for history rewriting of a shared branch.
- Why EXTRA: GOV-015 requires an explicit request for force-push; the oracle does not declare named branches categorically non-rewritable.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:77-79` (MIXED, M-S001092): "rewriting and the consequences are understood. Treat `main`, `master`, and"

### EXTRA-M-0019
- Closest oracle policies: WF-009, WF-022
- Modality: MUST
- Normative action: Run verify before preparing a pull request; the PR has a focused purpose and its description explains what changed, why, how it was verified and important compatibility or migration notes.
- Trigger/scope: pull requests
- Exceptions: none stated
- Why EXTRA: WF-009 covers truthful verification reporting and WF-022 focused commits; the oracle does not prescribe PR preparation or description contents.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:91-94` (MIXED, M-S001096): "claim checks were run if they were not."

### EXTRA-M-0020
- Closest oracle policies: RUN-016
- Modality: DEFAULT
- Normative action: Do not wrap normal EF Core operations in a generic application-level retry pipeline by default; prefer the provider's EF Core execution strategy for transient faults and handle transaction/retry interaction per the provider's guidance.
- Trigger/scope: persistence resilience
- Exceptions: Reported deviation with a concrete reason.
- Why EXTRA: RUN-016 limits retries to safe repeats; no oracle policy forbids application-level retry of persistence operations or prescribes the EF Core execution strategy.
- Evidence:
  - `.claude/skills/httpclient-factory/references/resilience.md:99-104` (EXTRA, M-S001240): "Do not wrap normal EF Core operations in a generic application-level retry"
  - `.claude/skills/httpclient-factory/references/resilience.md:133-136` (DUPLICATE, M-S001250): "Avoid retrying every exception or HTTP status, circuit breakers without a failure ⏎ scenario, hedging writes, generic resilience wrappers around EF Core without ⏎ understanding provider behavior, stacked handlers with overlapping strategies, ⏎ and unbounded retry/timeout combinations."
  - `.claude/skills/httpclient-factory/references/resilience.md:140-150` (DUPLICATE, M-S001252): "| Scenario | Default consideration | ⏎ |---|---| ⏎ | External I/O | Bound execution time | ⏎ | Safe transient HTTP failure | Consider retry | ⏎ | Unsafe write | No retry unless duplicate-safe | ⏎ | `429` from dependency | Respect `Retry-After` where appropriate | ⏎ | Repeated dependency outage | Consider circuit breaker | ⏎ | Optional data unavailable | Consider explicit fallback | ⏎ | Latency-sensitive idempoten"

### EXTRA-M-0021
- Closest oracle policies: RUN-005
- Modality: MUST NOT
- Normative action: Per-request values such as dynamic access tokens are applied to the specific request or through a handler; shared DefaultRequestHeaders are not mutated concurrently for request-specific values.
- Trigger/scope: outbound HTTP
- Exceptions: none stated
- Why EXTRA: RUN-005 governs client lifetime; no oracle policy addresses mutation of shared default headers.
- Evidence:
  - `.claude/skills/httpclient-factory/SKILL.md:166-169` (EXTRA, M-S001292): "through a handler; do not mutate shared `DefaultRequestHeaders` concurrently for"
  - `.claude/skills/httpclient-factory/SKILL.md:195-197` (DUPLICATE, M-S001300): "Avoid making typed, keyed, or named clients mandatory universally, ignoring ⏎ cancellation, putting dynamic auth tokens in shared `DefaultRequestHeaders`, and ⏎ adding resilience pipelines without understanding their behavior."

### EXTRA-M-0022
- Closest oracle policies: DEP-008, DEP-003
- Modality: MUST
- Normative action: global.json pins the repository to the intended supported .NET SDK line; when scaffolding select the current stable SDK for the target .NET release (no RC/preview unless explicitly requested) and allow servicing through the chosen rollForward policy.
- Trigger/scope: repository SDK configuration
- Exceptions: Preview SDK explicitly requested.
- Why EXTRA: DEP-008 fixes the .NET platform and DEP-003 package versions; no oracle policy requires an SDK pin file.
- Evidence:
  - `.claude/skills/project-structure/references/solution-layout.md:94-97` (EXTRA, M-S001481): "pin the repository to the intended supported .NET SDK line."

### EXTRA-M-0023
- Closest oracle policies: WF-020
- Modality: MUST
- Normative action: Security findings are reported in a fixed shape: severity tag, file:line location and title, OWASP category when applicable, Evidence, Impact (why it is a risk) and Remediation; uncertain findings use the NEEDS VERIFICATION form stating what effective behavior depends on.
- Trigger/scope: security review output
- Exceptions: none stated
- Why EXTRA: WF-020 requires evidence and contextual severity; the oracle does not prescribe a security finding format.
- Evidence:
  - `.claude/skills/security-scan/references/scan-layers.md:339-354` (EXTRA, M-S001628): "### [HIGH] src/.../File.cs:42 — Resource authorization missing"
  - `.claude/skills/security-scan/references/scan-layers.md:356-362` (EXTRA, M-S001629): "### [NEEDS VERIFICATION] ..."
  - `.claude/skills/security-scan/SKILL.md:158-161` (MIXED, M-S001668): "remediation, and the OWASP category when applicable. Label uncertain findings"
  - `.claude/skills/security-scan/SKILL.md:165-211` (EXTRA, M-S001670): "# Security Scan Report"

### EXTRA-M-0024
- Closest oracle policies: WF-020, WF-009
- Modality: MUST
- Normative action: The security scan report contains Scope, a Limitations statement (static analysis only), a severity Summary table, Findings and Layer Results for the seven layers using PASS / FINDINGS / NOT APPLICABLE / NOT CHECKED, with the fixed severity scale Critical / High / Medium / Low / Info and defined meanings.
- Trigger/scope: security scan output
- Exceptions: none stated
- Why EXTRA: WF-020/WF-009 require contextual severity and truthful status reporting; the oracle does not prescribe report sections, layer tables or a severity scale.
- Evidence:
  - `.claude/skills/security-scan/SKILL.md:15-20` (MIXED, M-S001635): "exploitation. State that limitation in the report."
  - `.claude/skills/security-scan/SKILL.md:119-129` (EXTRA, M-S001660): "use sparingly for immediately exploitable, high-impact"
  - `.claude/skills/security-scan/SKILL.md:165-211` (EXTRA, M-S001670): "# Security Scan Report"
  - `.claude/skills/security-scan/SKILL.md:213-214` (MIXED, M-S001671): "Use `PASS`, `FINDINGS`, `NOT APPLICABLE`, or `NOT CHECKED`; never mark an"
  - `.claude/skills/security-scan/SKILL.md:227-229` (DUPLICATE, M-S001675): "A security scan is complete when all applicable layers were inspected, findings ⏎ have evidence, uncertain findings are labeled, severity reflects actual risk, ⏎ limitations are stated, and no layer is marked PASS without being checked."

### EXTRA-M-0025
- Closest oracle policies: none
- Modality: MUST
- Normative action: After hook or script changes run the changed script with sample input and confirm both the pass and the failure paths; the maintenance report lists the files changed, owners added or moved and the checker result.
- Trigger/scope: instruction-system maintenance
- Exceptions: none stated
- Why EXTRA: Instruction-system maintenance procedure; no oracle policy governs testing or reporting of instruction-system changes.
- Evidence:
  - `.claude/skills/template-maintenance/SKILL.md:63-65` (EXTRA, M-S001728): "For hook or script changes, run the changed script with sample input (usage"
  - `.claude/skills/template-maintenance/SKILL.md:66-66` (EXTRA, M-S001729): "6. Report the files changed, owners added or moved, and the checker result."

### EXTRA-M-0026
- Closest oracle policies: none
- Modality: MUST
- Normative action: Normative vocabulary: a 'default' may be deviated from only with a concrete reason, and every such deviation must be reported.
- Trigger/scope: all instruction defaults
- Exceptions: none stated
- Why EXTRA: The oracle defines DEFAULT-strength policies but does not attach a duty to report deviations.
- Evidence:
  - `CLAUDE.md:14-14` (EXTRA, M-S001789): "- **default** — deviation needs a concrete reason and must be reported."

### EXTRA-M-0027
- Closest oracle policies: DEP-023, RUN-009
- Modality: MUST
- Normative action: Nullable reference types, implicit usings and the latest analysis level are enabled repository-wide through Directory.Build.props.
- Trigger/scope: backend build configuration
- Exceptions: none stated
- Why EXTRA: DEP-023 places shared settings in Directory.Build.props but no oracle policy requires nullable reference types, implicit usings or a particular analysis level.
- Evidence:
  - `Directory.Build.props:9-11` (EXTRA, M-S001837): "<Nullable>enable</Nullable>"

## LINK_UNCERTAIN (2)

### UNCERTAIN-M-0001
- Closest oracle policies: GOV-015, DEP-007
- Modality: MUST
- Normative action: Maintain and commit package.json and package-lock.json.
- Trigger/scope: npm manifests
- Exceptions: none stated
- Open question: DEP-007 requires a consistent lockfile, while GOV-015 forbids commits without an explicit request; whether 'commit' is a commit instruction or only means 'keep under version control' cannot be decided from the text.
- Evidence:
  - `.claude/rules/dependencies.md:34-37` (MIXED, M-S000223): "package manager. Maintain and commit `package.json` and `package-lock.json` and"
  - `.claude/scripts/check-manifests.mjs:351-353` (MIXED, M-S000395): "commit the lockfile"
  - `.claude/skills/add-dependency/SKILL.md:117-117` (LINK_UNCERTAIN, M-S000428): "Commit `package.json` and `package-lock.json` together."

### UNCERTAIN-M-0002
- Closest oracle policies: GOV-015, GOV-020
- Modality: MUST NOT (high-risk)
- Normative action: High-risk Git operations (reset --hard, clean, push --force, push --force-with-lease, branch deletion, rebase of shared history) are performed only when explicitly requested or clearly required by an approved workflow, after inspecting what will be lost or rewritten.
- Trigger/scope: Git operations
- Exceptions: Clearly required by an approved workflow.
- Open question: GOV-015 requires an explicit request for repository-changing operations; whether 'clearly required by an approved workflow' is an admissible substitute for that request cannot be decided from the oracle text.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:98-102` (LINK_UNCERTAIN, M-S001098): "high-risk. Perform them only when explicitly requested or clearly required by an"

