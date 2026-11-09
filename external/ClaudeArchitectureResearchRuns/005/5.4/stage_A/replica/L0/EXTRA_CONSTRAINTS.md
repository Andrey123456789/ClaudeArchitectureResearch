# L0 — EXTRA and LINK_UNCERTAIN constraints (Claude Run 2, blind replica)

Every constraint below is an effective candidate behavior judged not entailed by the 196 oracle policies (EXTRA) or whose relation could not be decided (LINK_UNCERTAIN). Citations are template-relative paths under `inputs/L0/output/template/` with exact source quotes (newlines shown as ⏎).

## EXTRA (30)

### EXTRA-L0-0001
- Closest oracle policies: ARC-020, ARC-001, GOV-017
- Modality: REQUIRES_APPROVAL (Reserved; PreToolUse blocks every reference command; post-bash and post-edit report every reference change)
- Normative action: Project-reference graph changes: every 'dotnet add/remove ... reference' and 'dotnet reference add/remove' command is blocked before it runs; references mapped by layout.md follow project-structure, any other reference-graph change needs a Decision Request (architecture-decision) and an approved change is applied in the project file; every added or removed ProjectReference and every added, moved or removed project file is reported for confirmation against the layout or an approved decision and must be reported.
- Trigger/scope: .NET project references and project files in the active worktree
- Exceptions: Layout-mapped references are not Reserved but must be written into the project file because the CLI path is always blocked.
- Why EXTRA: ARC-020 requires approval for new layers/projects and ARC-001 fixes direction; no oracle policy makes individual reference edges between existing projects Reserved or forbids the CLI route for approved or layout references.
- Evidence:
  - `.claude/hooks/claude-hook.mjs:366-369` (EXTRA, L0-S000019): "changes the project reference graph, which requires approval"
  - `.claude/hooks/claude-hook.mjs:422-424` (EXTRA, L0-S000022): "confirm it is the layout mapped by"
  - `.claude/hooks/claude-hook.mjs:426-430` (MIXED, L0-S000023): "a production project or reference-graph change outside the layout mapped by"
  - `.claude/INSTRUCTION_MAP.md:97-97` (DUPLICATE, L0-S000106): "| `.claude/hooks/claude-hook.mjs` | `pre-bash` (fails closed): blocks npm/pnpm/yarn force/legacy-peer flags and `dotnet add/remove … reference` / `dotnet reference add/remove` before they run, also behind global options such as `--prefix`, `--dir`, `--cwd` · `post-bash`, after successful and failed shell calls: compares the active worktree's manifests (tracked and untracked, not ignored) with a pe"
  - `.claude/skills/project-structure/SKILL.md:50-50` (MIXED, L0-S001279): "include those reports in the scaffolding report"
  - `CLAUDE.md:42-42` (MIXED, L0-S001558): "changing the project reference graph"

### EXTRA-L0-0002
- Closest oracle policies: WF-009, DEP-004
- Modality: MUST
- Normative action: Every dependency change reports the results of its version, deprecation, vulnerability and license checks (hook feedback: 'report them'; add-dependency report).
- Trigger/scope: dependency changes
- Exceptions: none stated
- Why EXTRA: DEP-003/DEP-004 require the checks; WF-009 covers verification reporting only; no oracle policy requires reporting dependency due-diligence results.
- Evidence:
  - `.claude/hooks/claude-hook.mjs:457-459` (MIXED, L0-S000025): "confirm its version, deprecation, vulnerability, and license steps were completed and report them"
  - `.claude/hooks/claude-hook.mjs:488-491` (MIXED, L0-S000027): "confirm its version, deprecation, vulnerability, and license steps were completed and report them"
  - `.claude/hooks/claude-hook.mjs:579-581` (MIXED, L0-S000032): "follow ${ADD_DEPENDENCY} and report its checks"
  - `.claude/INSTRUCTION_MAP.md:97-97` (DUPLICATE, L0-S000106): "| `.claude/hooks/claude-hook.mjs` | `pre-bash` (fails closed): blocks npm/pnpm/yarn force/legacy-peer flags and `dotnet add/remove … reference` / `dotnet reference add/remove` before they run, also behind global options such as `--prefix`, `--dir`, `--cwd` · `post-bash`, after successful and failed shell calls: compares the active worktree's manifests (tracked and untracked, not ignored) with a pe"
  - `.claude/skills/add-dependency/SKILL.md:59-59` (MIXED, L0-S000483): "Report: package · version · license · reason · checks performed."

### EXTRA-L0-0003
- Closest oracle policies: none
- Modality: MUST (checker-enforced; PostToolUse feedback after instruction edits)
- Normative action: Level model of the instruction system: every instruction artifact carries a header (Level, Owns, Scope, Loads, Depends on); rules live in level directories with paths front matter; conformance dependencies ('Depends on') point only to the same or a more stable level without cycles; Levels 0 and 1 name no concrete technology beyond .NET, C#, TypeScript (Git for repository safety); every artifact is listed in the instruction map; after editing CLAUDE.md or .claude/**/*.md|json|mjs the structure checker runs and every reported error must be fixed.
- Trigger/scope: authoring or changing instruction artifacts
- Exceptions: Routing pointers ('run verify', 'see layout.md') are not conformance dependencies.
- Why EXTRA: Instruction-system organization rule of the L0 template; the oracle defines no level hierarchy, header format or technology-neutrality requirement for instruction files.
- Evidence:
  - `.claude/hooks/claude-hook.mjs:594-606` (EXTRA, L0-S000034): "Instruction-structure check failed after editing"
  - `.claude/INSTRUCTION_MAP.md:17-17` (EXTRA, L0-S000087): "may point only to the same or a more stable level"
  - `.claude/INSTRUCTION_MAP.md:18-18` (EXTRA, L0-S000088): "is not a conformance dependency and may point in any direction"
  - `.claude/INSTRUCTION_MAP.md:19-19` (EXTRA, L0-S000089): "Levels 0 and 1 name no concrete technology beyond the fixed platform"
  - `.claude/INSTRUCTION_MAP.md:97-97` (DUPLICATE, L0-S000106): "| `.claude/hooks/claude-hook.mjs` | `pre-bash` (fails closed): blocks npm/pnpm/yarn force/legacy-peer flags and `dotnet add/remove … reference` / `dotnet reference add/remove` before they run, also behind global options such as `--prefix`, `--dir`, `--cwd` · `post-bash`, after successful and failed shell calls: compares the active worktree's manifests (tracked and untracked, not ignored) with a pe"
  - `.claude/INSTRUCTION_MAP.md:99-99` (DUPLICATE, L0-S000108): "| `.claude/tools/check-instructions.mjs` | structure checker: `node "$(git rev-parse --show-toplevel)/.claude/tools/check-instructions.mjs"` (Bash or PowerShell, from any directory of the repository or worktree) — level-first layout, headers, `paths`, Level 0/1 neutrality, dependency direction and cycles, imports, references, private references, hook registrations (exec form, launcher placeholder,"
  - `.claude/INSTRUCTION_MAP.md:124-124` (EXTRA, L0-S000114): "Levels 0 and 1 stay unchanged."
  - `.claude/INSTRUCTION_MAP.md:128-131` (EXTRA, L0-S000116): "Names a technology beyond the fixed platform → Level 2."
  - `.claude/skills/template-maintenance/SKILL.md:19-22` (EXTRA, L0-S001408): "Names a technology other than the fixed platform"
  - `.claude/skills/template-maintenance/SKILL.md:24-24` (EXTRA, L0-S001409): "A statement's level is set by the most volatile thing it depends on."
  - `.claude/skills/template-maintenance/SKILL.md:40-43` (EXTRA, L0-S001415): "Update `.claude/INSTRUCTION_MAP.md` for every added, moved, or removed artifact."
  - `.claude/skills/template-maintenance/SKILL.md:47-47` (EXTRA, L0-S001417): "fix every reported error"
  - `.claude/tools/check-instructions.mjs:150-153` (EXTRA, L0-S001459): "first line must be the classification header"
  - `.claude/tools/check-instructions.mjs:154-154` (EXTRA, L0-S001460): "must be named"
  - `.claude/tools/check-instructions.mjs:163-163` (EXTRA, L0-S001463): "rules must live in .claude/rules/"
  - `.claude/tools/check-instructions.mjs:168-168` (EXTRA, L0-S001465): "does not match directory"
  - `.claude/tools/check-instructions.mjs:169-170` (EXTRA, L0-S001466): "every rule file must declare a non-empty 'paths' list"
  - `.claude/tools/check-instructions.mjs:234-234` (EXTRA, L0-S001484): "must not name the concrete technology"
  - `.claude/tools/check-instructions.mjs:253-253` (EXTRA, L0-S001488): "is not an instruction artifact"
  - `.claude/tools/check-instructions.mjs:261-261` (EXTRA, L0-S001490): "must not depend on more volatile Level"
  - `.claude/tools/check-instructions.mjs:270-270` (EXTRA, L0-S001492): "dependency cycle"
  - `.claude/tools/check-instructions.mjs:401-401` (EXTRA, L0-S001514): "does not list"

### EXTRA-L0-0004
- Closest oracle policies: DEP-004, DEP-020, DEP-010
- Modality: MUST NOT (manifest check finding; no approval path)
- Normative action: Packages Microsoft.Extensions.Http.Polly and Polly.Extensions.Http (deprecated resilience integrations) and Serilog.Sinks.Elasticsearch (deprecated sink) must not be added; they are reported on every manifest validation.
- Trigger/scope: NuGet manifests
- Exceptions: none stated (accepted decisions do not exempt deny-listed packages)
- Why EXTRA: DEP-004 requires checking deprecation and DEP-020 treats direct Polly integration as an explicit exception; no oracle policy forbids specific packages outright regardless of approval.
- Evidence:
  - `.claude/hooks/manifest-checks.mjs:18-23` (EXTRA, L0-S000045): "deprecated resilience integration"
  - `.claude/hooks/manifest-checks.mjs:264-264` (EXTRA, L0-S000060): "if (DENY_NUGET.has(key))"
  - `.claude/INSTRUCTION_MAP.md:98-98` (DUPLICATE, L0-S000107): "| `.claude/hooks/manifest-checks.mjs` | central versions, `VersionOverride`, floating/prerelease versions, deny/review package lists (approved exceptions are read from the "Accepted" sections of the decision summaries), npm tooling category, `.npmrc` bypass, outward project references; reads UTF-8, UTF-8 with BOM, and BOM-tagged UTF-16 files and reports undecodable ones |"
  - `.claude/skills/add-dependency/SKILL.md:49-49` (MIXED, L0-S000477): "Do not add the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`."
  - `.claude/skills/logging/references/serilog.md:141-141` (EXTRA, L0-S001139): "the `Serilog.Sinks.Elasticsearch` package is deprecated"

### EXTRA-L0-0005
- Closest oracle policies: DEP-010, DEP-004
- Modality: DEFAULT (manifest check: flagged unless an accepted decision names it)
- Normative action: Do not adopt a deprecated or legacy ASP.NET automatic-validation integration package (FluentValidation.AspNetCore) unless a concrete project requirement justifies it; deviation needs a recorded decision or reported reason.
- Trigger/scope: backend validation packages
- Exceptions: Concrete project requirement recorded as an accepted decision.
- Why EXTRA: DEP-010 fixes FluentValidation as the library and DEP-004 requires deprecation checks; no oracle policy restricts its ASP.NET integration package.
- Evidence:
  - `.claude/hooks/manifest-checks.mjs:31-31` (EXTRA, L0-S000050): "legacy automatic-validation integration"
  - `.claude/hooks/manifest-checks.mjs:265-267` (MIXED, L0-S000061): "needs a recorded decision or reported reason"
  - `.claude/INSTRUCTION_MAP.md:98-98` (DUPLICATE, L0-S000107): "| `.claude/hooks/manifest-checks.mjs` | central versions, `VersionOverride`, floating/prerelease versions, deny/review package lists (approved exceptions are read from the "Accepted" sections of the decision summaries), npm tooling category, `.npmrc` bypass, outward project references; reads UTF-8, UTF-8 with BOM, and BOM-tagged UTF-16 files and reports undecodable ones |"
  - `.claude/rules/2-technology/fluentvalidation.md:12-12` (MIXED, L0-S000384): "do not adopt a deprecated or legacy ASP.NET automatic-validation integration package"

### EXTRA-L0-0006
- Closest oracle policies: none
- Modality: MUST
- Normative action: Placement and ownership of instruction content: rule = normative constraint, workflow skill = procedure, knowledge skill = technique (never the sole owner of a rule), product files = inputs, hooks/scripts/config = deterministic enforcement; each rule has exactly one owner and other files point to it; planning-time rules go to CLAUDE.md or a decision summary, file-scoped rules to a path rule covering at least their scope; maintenance runs template-maintenance.
- Trigger/scope: template maintenance
- Exceptions: none stated
- Why EXTRA: Instruction-system placement and ownership rules; the oracle does not regulate where instruction content lives or how it is owned.
- Evidence:
  - `.claude/INSTRUCTION_MAP.md:24-24` (EXTRA, L0-S000092): "Each rule has exactly one owner; other files point to it."
  - `.claude/INSTRUCTION_MAP.md:133-133` (EXTRA, L0-S000117): "Then pick the artifact by responsibility and trigger"
  - `.claude/skills/template-maintenance/SKILL.md:28-32` (EXTRA, L0-S001411): "never the sole owner of a must-rule"
  - `.claude/skills/template-maintenance/SKILL.md:36-36` (EXTRA, L0-S001413): "State each rule once, in its owner."

### EXTRA-L0-0007
- Closest oracle policies: none
- Modality: MUST (checker-enforced)
- Normative action: Hook registration form: hooks are registered in exec form (command node, args with the ${CLAUDE_PROJECT_DIR} placeholder, no shell); PreToolUse Bash|PowerShell runs pre-bash with onFailure block; PostToolUse and PostToolUseFailure Bash|PowerShell run post-bash; PostToolUse Edit|MultiEdit|Write runs post-edit; Stop runs stop; only the PreToolUse hook fails closed.
- Trigger/scope: .claude/settings.json (template maintenance)
- Exceptions: none stated
- Why EXTRA: Hook-configuration design of the template; no oracle policy regulates hook registration or failure semantics.
- Evidence:
  - `.claude/INSTRUCTION_MAP.md:96-96` (EXTRA, L0-S000105): "`"onFailure": "block"`"
  - `.claude/INSTRUCTION_MAP.md:99-99` (DUPLICATE, L0-S000108): "| `.claude/tools/check-instructions.mjs` | structure checker: `node "$(git rev-parse --show-toplevel)/.claude/tools/check-instructions.mjs"` (Bash or PowerShell, from any directory of the repository or worktree) — level-first layout, headers, `paths`, Level 0/1 neutrality, dependency direction and cycles, imports, references, private references, hook registrations (exec form, launcher placeholder,"
  - `.claude/settings.json:7-7` (EXTRA, L0-S000460): ""onFailure": "block""
  - `.claude/tools/check-instructions.mjs:360-360` (EXTRA, L0-S001506): "hook type must be 'command'"
  - `.claude/tools/check-instructions.mjs:361-363` (EXTRA, L0-S001507): "hook must use exec form"
  - `.claude/tools/check-instructions.mjs:364-366` (EXTRA, L0-S001508): "so the hook starts from any working directory"
  - `.claude/tools/check-instructions.mjs:367-370` (EXTRA, L0-S001509): "a positive timeout is required"
  - `.claude/tools/check-instructions.mjs:371-375` (EXTRA, L0-S001510): "the critical guard must fail closed"
  - `.claude/tools/check-instructions.mjs:380-386` (EXTRA, L0-S001512): "registration${scope} running"

### EXTRA-L0-0008
- Closest oracle policies: GOV-017, GOV-007
- Modality: MUST
- Normative action: Accepted decisions are recorded in the decision summary of their level (architecture decisions in overview.md, project/stack decisions in decisions.md) with date, decision, scope, consequences and the owning rule updated; approved exceptions for review-listed packages take effect only through these 'Accepted' sections.
- Trigger/scope: approved Reserved decisions
- Exceptions: none stated
- Why EXTRA: GOV-017 requires approval for Reserved decisions but no recording format; GOV-007 covers product behavior sources. No oracle policy requires level-stratified decision summaries or makes package exceptions depend on them.
- Evidence:
  - `.claude/rules/1-architecture/overview.md:47-47` (EXTRA, L0-S000298): "Approved architecture changes are recorded here by `architecture-decision`"
  - `.claude/rules/3-project/decisions.md:53-53` (EXTRA, L0-S000434): "Approved stack or default changes are recorded here by `architecture-decision`"
  - `.claude/skills/architecture-decision/SKILL.md:35-36` (EXTRA, L0-S000558): "Add an entry to the matching decision summary"
  - `CLAUDE.md:16-16` (MIXED, L0-S001541): "record the accepted decision with `architecture-decision`"

### EXTRA-L0-0009
- Closest oracle policies: DEP-010, API-010
- Modality: MUST
- Normative action: Application-level validators live in Application and are registered with FluentValidation.DependencyInjectionExtensions from Application's own registration.
- Trigger/scope: backend validation setup
- Exceptions: none stated
- Why EXTRA: DEP-010 fixes FluentValidation and API-010 the validation boundaries; no oracle policy prescribes the registration package.
- Evidence:
  - `.claude/rules/2-technology/fluentvalidation.md:11-11` (MIXED, L0-S000383): "registered with `FluentValidation.DependencyInjectionExtensions` from Application's own registration"
  - `.claude/rules/3-project/decisions.md:24-24` (MIXED, L0-S000415): "`FluentValidation.DependencyInjectionExtensions`"
  - `.claude/skills/aspnet-error-handling/SKILL.md:105-105` (MIXED, L0-S000583): "(FluentValidation.DependencyInjectionExtensions)"

### EXTRA-L0-0010
- Closest oracle policies: DEP-001, DEP-006
- Modality: MUST
- Normative action: Removing a dependency removes the project reference and, when no project uses it any more, its central version in Directory.Packages.props, then rebuilds and runs the affected tests.
- Trigger/scope: dependency removal
- Exceptions: none stated
- Why EXTRA: DEP-001..DEP-006 govern additions and central version placement; no oracle policy prescribes a removal procedure or the cleanup of unused central versions.
- Evidence:
  - `.claude/skills/add-dependency/SKILL.md:63-63` (EXTRA, L0-S000485): "and its central version when no project uses it any more"

### EXTRA-L0-0011
- Closest oracle policies: API-013, ARC-020
- Modality: REQUIRES_APPROVAL (Reserved)
- Normative action: Adopting API versioning is Reserved and needs explicit approval, even when a concrete compatibility need exists.
- Trigger/scope: HTTP API versioning
- Exceptions: none stated
- Why EXTRA: API-013 allows introducing versioning when a real compatibility need exists and does not require approval; the oracle's consequential-change list does not name versioning adoption.
- Evidence:
  - `.claude/skills/api-versioning/SKILL.md:13-13` (MIXED, L0-S000525): "adopting versioning is Reserved"
  - `CLAUDE.md:48-48` (MIXED, L0-S001560): "adopting API versioning"

### EXTRA-L0-0012
- Closest oracle policies: WF-009, GOV-017
- Modality: MUST
- Normative action: Decision reporting: Delegated decisions taken are mentioned in the report, and a rejected Decision Request is not recorded as a decision but mentioned in the report.
- Trigger/scope: decision handling
- Exceptions: none stated
- Why EXTRA: GOV-017 requires classification and reporting of unresolved Decision Requests in headless runs; no oracle policy requires reporting Delegated decisions or rejected requests.
- Evidence:
  - `.claude/skills/architecture-decision/SKILL.md:19-19` (MIXED, L0-S000552): "Delegated → proceed and mention it in the report."
  - `.claude/skills/architecture-decision/SKILL.md:39-39` (EXTRA, L0-S000560): "A rejected request is not recorded as a decision; mention it in the report."

### EXTRA-L0-0013
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: The build-fix report states the initial failure, root cause, changes made, backend build / frontend build / tests status (PASS, NOT RUN, NOT APPLICABLE) and remaining issues.
- Trigger/scope: build and test repair
- Exceptions: none stated
- Why EXTRA: WF-009 requires reporting actual verification states only; no oracle policy prescribes failure/root-cause/changes sections.
- Evidence:
  - `.claude/skills/build-fix/SKILL.md:74-82` (MIXED, L0-S000663): "Backend build: PASS / NOT RUN / NOT APPLICABLE"

### EXTRA-L0-0014
- Closest oracle policies: WF-011, WF-012
- Modality: MUST
- Normative action: Code-review findings are reported ordered by severity with severity, file/location, problem, why it matters and smallest reasonable fix, on the scale Critical (data loss, security vulnerability, reliably broken core behavior; blocks merge), High, Medium, Low.
- Trigger/scope: code review output
- Exceptions: none stated
- Why EXTRA: WF-011/WF-012 set priorities and forbid manufactured findings; the oracle prescribes no output format or severity scale.
- Evidence:
  - `.claude/skills/code-review/SKILL.md:65-70` (EXTRA, L0-S000749): "severity · file/location · problem · why it matters · smallest reasonable fix"

### EXTRA-L0-0015
- Closest oracle policies: RUN-021, ARC-019
- Modality: MUST NOT
- Normative action: Do not cache EF tracked entities across Unit of Work boundaries (named caching anti-pattern).
- Trigger/scope: caching with EF Core
- Exceptions: none stated
- Why EXTRA: RUN-021 governs invalidation consistency and ARC-019 confines EF Core to Infrastructure; caching tracked entities is an EF technique pitfall (EXC-011 class) that the template turns into a named prohibition.
- Evidence:
  - `.claude/skills/caching/SKILL.md:78-78` (MIXED, L0-S000691): "Caching EF tracked entities across Unit of Work boundaries"

### EXTRA-L0-0016
- Closest oracle policies: PST-009, PST-010
- Modality: MUST
- Normative action: Schema changes are created as new EF Core migrations from the Infrastructure project with the Api project as startup project.
- Trigger/scope: schema changes
- Exceptions: none stated
- Why EXTRA: The oracle requires a migration only for schema-affecting CUSTOM_SETTINGS changes (PST-009) and review of generated migrations (PST-010); it has no general rule that every schema change is made through a new migration with fixed projects.
- Evidence:
  - `.claude/skills/development-workflow/SKILL.md:49-49` (MIXED, L0-S000860): "Treat migrations as source code: review each generated migration before committing it"

### EXTRA-L0-0017
- Closest oracle policies: WF-009, GOV-017
- Modality: MUST
- Normative action: The development-workflow report summarizes what changed, the verify result block, unresolved Decision Requests and remaining known issues.
- Trigger/scope: implementation work
- Exceptions: none stated
- Why EXTRA: WF-009 covers the verification state and GOV-017 the listing of unresolved Decision Requests in headless runs; a fixed summary of changes and remaining known issues for every implementation is an additional reporting duty.
- Evidence:
  - `.claude/skills/development-workflow/SKILL.md:59-59` (MIXED, L0-S000866): "Summarize what changed, the `verify` result block, unresolved Decision Requests, and remaining known issues."

### EXTRA-L0-0018
- Closest oracle policies: GOV-015, GOV-019
- Modality: MUST NOT
- Normative action: Treat main, master and other protected/shared branches as non-rewritable.
- Trigger/scope: Git history rewriting
- Exceptions: none stated
- Why EXTRA: GOV-015 allows repository-changing operations, including history rewriting, on explicit request; this rule forbids rewriting these branches without an approval path.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:33-33` (MIXED, L0-S000990): "treat `main`, `master`, and other protected/shared branches as non-rewritable"

### EXTRA-L0-0019
- Closest oracle policies: WF-009
- Modality: MUST
- Normative action: A pull request has a focused purpose and its description explains what changed, why, how it was verified, and compatibility/migration notes.
- Trigger/scope: pull request preparation
- Exceptions: none stated
- Why EXTRA: No oracle policy prescribes PR description contents; WF-009 only requires truthful verification reporting.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:41-41` (MIXED, L0-S000994): "Never claim checks that were not run."

### EXTRA-L0-0020
- Closest oracle policies: RUN-002, ARC-017
- Modality: MUST NOT
- Normative action: Do not make fire-and-forget EF Core async calls (named anti-pattern).
- Trigger/scope: EF Core usage
- Exceptions: none stated
- Why EXTRA: RUN-002 concerns blocking on async I/O and ARC-017 the shared scoped context; no oracle policy names unawaited (fire-and-forget) EF calls, which is EF technique turned into a prohibition.
- Evidence:
  - `.claude/skills/ef-core/SKILL.md:237-237` (MIXED, L0-S000973): "fire-and-forget EF async calls"

### EXTRA-L0-0021
- Closest oracle policies: RUN-016, DEP-020
- Modality: MUST NOT
- Normative action: Do not wrap normal EF Core operations in a generic application-level retry pipeline; prefer the provider's EF Core execution strategy (e.g. EnableRetryOnFailure for SQL Server) and follow provider guidance for transaction/retry interaction.
- Trigger/scope: database access resilience
- Exceptions: none stated
- Why EXTRA: RUN-016 governs when retries are safe and the oracle treats database-retry examples as conditional technique (EXC-007); no oracle policy forbids an application-level retry pipeline around EF Core operations.
- Evidence:
  - `.claude/skills/httpclient-factory/references/resilience.md:42-42` (EXTRA, L0-S001074): "Do not wrap normal EF Core operations in a generic application-level retry pipeline."
  - `.claude/skills/httpclient-factory/references/resilience.md:69-69` (DUPLICATE, L0-S001085): "| EF transient faults | provider/EF execution strategy |"

### EXTRA-L0-0022
- Closest oracle policies: RUN-005
- Modality: MUST NOT
- Normative action: Never mutate a shared HttpClient's DefaultRequestHeaders concurrently; apply per-request values such as dynamic tokens per request or through a handler.
- Trigger/scope: outbound HTTP clients
- Exceptions: none stated
- Why EXTRA: RUN-005 governs client lifetime only; thread-safe header handling is client technique not stated by any oracle policy.
- Evidence:
  - `.claude/skills/httpclient-factory/SKILL.md:88-88` (MIXED, L0-S001110): "never mutate shared `DefaultRequestHeaders` concurrently"
  - `.claude/skills/httpclient-factory/SKILL.md:102-102` (DUPLICATE, L0-S001116): "Making one client style mandatory everywhere; dynamic tokens in shared default headers; mapping every upstream failure to the same status; resilience pipelines added without understanding their behavior."

### EXTRA-L0-0023
- Closest oracle policies: DEP-008, DEP-023
- Modality: MUST
- Normative action: Scaffolding creates global.json pinning the intended SDK line: the current stable SDK of the target release (no preview/RC line unless approved) with a rollForward policy that allows normal patch/feature-band servicing.
- Trigger/scope: repository scaffolding
- Exceptions: Preview/RC with approval.
- Why EXTRA: DEP-008 fixes the platform and DEP-023 repository-level build configuration; no oracle policy requires a global.json SDK pin or a particular roll-forward policy.
- Evidence:
  - `.claude/skills/project-structure/references/solution-layout.md:54-54` (EXTRA, L0-S001255): "`global.json` — pins the intended SDK line"
  - `.claude/skills/project-structure/references/solution-layout.md:65-65` (MIXED, L0-S001257): "choose a `rollForward` policy that allows normal patch/feature-band servicing"
  - `.claude/skills/project-structure/SKILL.md:34-34` (MIXED, L0-S001274): "Create only the required top-level directories and repository files"

### EXTRA-L0-0024
- Closest oracle policies: WF-020, WF-009
- Modality: MUST
- Normative action: Security-scan report shape: every report states the static-analysis limitation; severity uses the five levels Critical (sparingly) / High / Medium / Low / Info; each confirmed finding gives severity, file and location, title, evidence, why it is a risk, likely impact, smallest remediation and OWASP category when applicable; the report contains scope, limitations, a severity summary, findings and per-layer results.
- Trigger/scope: security reviews
- Exceptions: none stated
- Why EXTRA: WF-020 requires evidence-based contextual severity and WF-009 truthful status reporting; the oracle prescribes no report structure, severity scale or mandatory limitation statement.
- Evidence:
  - `.claude/skills/security-scan/SKILL.md:12-12` (MIXED, L0-S001343): "State that limitation in every report."
  - `.claude/skills/security-scan/SKILL.md:64-68` (MIXED, L0-S001361): "**Critical** (sparingly)"
  - `.claude/skills/security-scan/SKILL.md:78-78` (MIXED, L0-S001366): "Label uncertain items `NEEDS VERIFICATION`."
  - `.claude/skills/security-scan/SKILL.md:80-108` (EXTRA, L0-S001367): "Limitations: Static analysis only."

### EXTRA-L0-0025
- Closest oracle policies: none
- Modality: MUST
- Normative action: template-maintenance runs only when the user invokes it (disable-model-invocation; never started automatically), and maintenance keeps the always-loaded surface compact (CLAUDE.md plus the two imported decision summaries; the checker prints its estimate).
- Trigger/scope: instruction-system maintenance
- Exceptions: none stated
- Why EXTRA: Invocation and loading-surface rules of the template; no oracle policy regulates how the instruction system is maintained.
- Evidence:
  - `.claude/skills/template-maintenance/SKILL.md:6-6` (EXTRA, L0-S001401): "disable-model-invocation: true"
  - `.claude/skills/template-maintenance/SKILL.md:13-13` (EXTRA, L0-S001405): "Run only when the user invokes it. Never start it automatically."
  - `.claude/skills/template-maintenance/SKILL.md:47-47` (EXTRA, L0-S001417): "fix every reported error"
  - `.claude/tools/check-instructions.mjs:184-186` (EXTRA, L0-S001471): "enlarges the always-loaded surface"
  - `.claude/tools/check-instructions.mjs:210-213` (EXTRA, L0-S001477): "must set disable-model-invocation: true (user-only)"
  - `.claude/tools/check-instructions.mjs:414-414` (EXTRA, L0-S001516): "exceeds the"

### EXTRA-L0-0026
- Closest oracle policies: none
- Modality: MUST (checker-enforced)
- Normative action: Instruction inventory and model integrity: the required workflow skills (project-structure, verify, code-review, build-fix, custom-settings, git-workflow, security-scan, add-dependency, architecture-decision, template-maintenance) and knowledge skills (ef-core, http-api, aspnet-error-handling, dotnet-testing, logging, httpclient-factory, configuration, dependency-injection, caching, swagger, api-versioning, health-check, docker, ci-cd, angular, modern-csharp, authentication) exist with frontmatter name equal to the directory and a description; no standalone serilog or resilience skill; agents declare name and description; CLAUDE.md is Level 0 and imports the two stratified decision summaries (1-architecture/overview.md, 3-project/decisions.md) with resolving imports; no 'Kind:' classification and no manifests, capability contracts or slots under .claude; file, skill, agent and routed-workflow references resolve; skill-private references are used only by their owning skill.
- Trigger/scope: template maintenance
- Exceptions: The instruction map may list private references.
- Why EXTRA: Inventory and model invariants of the L0 template; no oracle policy requires particular instruction artifacts, imports or forbids other instruction models' constructs.
- Evidence:
  - `.claude/tools/check-instructions.mjs:155-155` (EXTRA, L0-S001461): "'Kind:' classification is not part of this instruction model"
  - `.claude/tools/check-instructions.mjs:176-176` (EXTRA, L0-S001468): "CLAUDE.md: must be Level 0 Core"
  - `.claude/tools/check-instructions.mjs:177-179` (EXTRA, L0-S001469): "does not resolve"
  - `.claude/tools/check-instructions.mjs:180-183` (EXTRA, L0-S001470): "must import the stratified decision summary"
  - `.claude/tools/check-instructions.mjs:200-201` (EXTRA, L0-S001473): "frontmatter name must be"
  - `.claude/tools/check-instructions.mjs:204-206` (EXTRA, L0-S001475): "is missing"
  - `.claude/tools/check-instructions.mjs:207-209` (EXTRA, L0-S001476): "duplicates a private reference of the knowledge surface"
  - `.claude/tools/check-instructions.mjs:218-218` (EXTRA, L0-S001479): "agent frontmatter needs name and description"
  - `.claude/tools/check-instructions.mjs:309-309` (EXTRA, L0-S001494): "does not resolve"
  - `.claude/tools/check-instructions.mjs:312-312` (EXTRA, L0-S001496): "may be used only by skill"
  - `.claude/tools/check-instructions.mjs:317-317` (EXTRA, L0-S001498): "does not exist"
  - `.claude/tools/check-instructions.mjs:320-320` (EXTRA, L0-S001500): "routed workflow"
  - `.claude/tools/check-instructions.mjs:324-324` (EXTRA, L0-S001502): "routing target"
  - `.claude/tools/check-instructions.mjs:330-330` (EXTRA, L0-S001504): "manifests, capability contracts, and slots are not part of this instruction model"

### EXTRA-L0-0027
- Closest oracle policies: none
- Modality: MUST
- Normative action: Normative vocabulary: 'must / must not' violations are defects; a 'default' may be deviated from only with a concrete reason and the deviation must be reported; 'prefer / avoid' are guidance; 'requires approval' marks a Reserved decision.
- Trigger/scope: interpretation of all instruction text
- Exceptions: none stated
- Why EXTRA: The oracle's DEFAULT strength allows deviation for a concrete reason but requires no report of each deviation; the reporting duty and the vocabulary itself are template constructs.
- Evidence:
  - `CLAUDE.md:20-20` (EXTRA, L0-S001543): "**default** — deviation needs a concrete reason and must be reported"

### EXTRA-L0-0028
- Closest oracle policies: GOV-017, GOV-005
- Modality: MUST
- Normative action: Unclear-case test: any 'yes' makes a choice Reserved — does it add, remove or replace a dependency, framework or infrastructure capability; change a project/layer/reference boundary; establish a convention other code is expected to follow; change observable behavior or a public contract; become expensive to reverse once other code depends on it?
- Trigger/scope: choices whose classification is unclear
- Exceptions: none stated
- Why EXTRA: GOV-017 requires classification but not this test; under it any unclear dependency addition or removal becomes Reserved, whereas the oracle allows dependencies with a concrete need (DEP-001) and delegates routine internal choices (GOV-005).
- Evidence:
  - `CLAUDE.md:51-51` (EXTRA, L0-S001562): "Unclear case — any **yes** makes it Reserved"

### EXTRA-L0-0029
- Closest oracle policies: GOV-018
- Modality: MUST
- Normative action: Instruction precedence: engineering policy lives in the instruction system; a more volatile level may refine a more stable level but must not contradict it; when a contradiction is found it is reported instead of choosing a side.
- Trigger/scope: conflicts between instruction levels
- Exceptions: none stated
- Why EXTRA: GOV-018 asks to raise concerns about questionable requests, including conflicts; no oracle policy defines precedence between instruction levels or requires reporting internal instruction contradictions instead of resolving them.
- Evidence:
  - `CLAUDE.md:14-14` (EXTRA, L0-S001539): "report a contradiction instead of choosing a side"

### EXTRA-L0-0030
- Closest oracle policies: RUN-009, DEP-023
- Modality: MUST (repository build configuration)
- Normative action: Repository-wide Directory.Build.props enables nullable reference types, implicit usings and the latest analysis level for every .NET project.
- Trigger/scope: all .NET projects
- Exceptions: Project-specific overrides.
- Why EXTRA: DEP-023 places shared settings in Directory.Build.props and DEP-008 fixes the platform; no oracle policy requires nullable reference types, implicit usings or the latest analyzer level.
- Evidence:
  - `Directory.Build.props:5-7` (EXTRA, L0-S001594): "<Nullable>enable</Nullable>"

## LINK_UNCERTAIN (2)

### UNCERTAIN-L0-0001
- Closest oracle policies: GOV-015, DEP-007
- Modality: MUST
- Normative action: Commit package.json and package-lock.json and keep the lockfile consistent with every change.
- Trigger/scope: frontend workspace manifests
- Exceptions: none stated
- Open question: Read as a version-control content convention the clause is entailed by DEP-007; read as an instruction to perform commits it conflicts with GOV-015 (commits only on explicit request). The text does not settle the reading.
- Evidence:
  - `.claude/rules/3-project/package-management.md:23-23` (MIXED, L0-S000457): "commit `package.json` and `package-lock.json` and keep the lockfile consistent with every change"

### UNCERTAIN-L0-0002
- Closest oracle policies: GOV-015
- Modality: MUST NOT (conditional)
- Normative action: git reset --hard, git clean, git push --force / --force-with-lease, branch deletion and rebasing shared history are performed only when explicitly requested or clearly required by an approved workflow, after inspecting what will be lost or rewritten.
- Trigger/scope: high-risk Git operations
- Exceptions: 'clearly required by an approved workflow'
- Open question: GOV-015 permits repository-changing Git operations only on explicit request; 'clearly required by an approved workflow' names no workflow and may authorize high-risk operations without an explicit request, or may only refer to an explicitly approved procedure.
- Evidence:
  - `.claude/skills/git-workflow/SKILL.md:45-45` (MIXED, L0-S000996): "clearly required by an approved workflow"

