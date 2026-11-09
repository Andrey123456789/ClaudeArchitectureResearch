# Orphan sweep report — candidate M

Every EXTRA and LINK_UNCERTAIN constraint has at least one orphan row; additional rows record clauses that were examined as possible extras and resolved as oracle-linked, duplicate or non-normative. Disproven hypotheses are kept, not deleted.

## Counts

- Orphan candidates identified: 283
- EXTRA registered (EXTRA_REGISTERED): 221 (EXTRA constraints: 221)
- Mapped to oracle (POLICY_LINKED): 23
- Non-normative / discarded (NON_NORMATIVE): 33
- Duplicates (DUPLICATE): 4
- Unresolved (LINK_UNCERTAIN): 2

## Unresolved items

### ORPHAN-M-0098
- Constraint(s): UNCERTAIN-M-0001; closest policies: RUN-021
- Evidence: `output/template/.claude/skills/caching/SKILL.md:92-94` — "Invalidating before the"
- Open question: is pre-success invalidation (which never makes the cache a second source of truth) still 'consistent with successful underlying mutations' under RUN-021, or does this clause relax RUN-021 with an exception?

### ORPHAN-M-0152
- Constraint(s): UNCERTAIN-M-0002; closest policies: GOV-015
- Evidence: `output/template/.claude/skills/git-workflow/SKILL.md:98-102` — "Treat `git reset --hard`, `git clean`, `git push --force`, ⏎ `git push --force-with-lease`, branch deletion, and rebase of shared history as ⏎ high-risk. Perform them only when explicitly requested or clearly required by an ⏎ approved workflow, and inspect what will be lost or rewritten before executing ⏎ them."
- Open question: does 'clearly required by an approved workflow' relax GOV-015 (which permits repository-changing Git operations only when explicitly requested), or is an approved workflow itself an explicit request?

## Rejected false leads and oracle-linked resolutions

- ORPHAN-M-0002 [NON_NORMATIVE] `.claude/MAP.md:74-77` — Considered whether 'owns no policy' downgrades all knowledge-skill imperatives to non-binding; rejected as a binding interpretation rule because MAP.md is never loaded into Claude's context, so it cannot change how skill text is applied at runtime. Knowledge-skill imperatives are classified individually.
- ORPHAN-M-0003 [DUPLICATE] `.claude/MAP.md:111-111` — 'so Node.js must be available' reads like an environment requirement; it is a description of the fail-closed PreToolUse registration in settings.json (onFailure block), captured at settings.json.
- ORPHAN-M-0004 [NON_NORMATIVE] `.claude/rules/architecture.md:96-97` — 'Aggregate Roots ... are natural repository-boundary candidates' is conditional, non-binding guidance applicable only when an approved DDD design exists; it neither requires nor forbids an outcome.
- ORPHAN-M-0005 [NON_NORMATIVE] `.claude/rules/coding-style.md:64-65` — Pointer sentence; the obligation itself (RUN-010) is owned and captured in verify, so this restatement is not an independent rule.
- ORPHAN-M-0006 [DUPLICATE] `.claude/rules/error-handling.md:56-58` — Candidate extra 'expected outcomes are not logged as application errors' checked against API-009; treated as an expression of 'expected outcomes are not system failures' rather than an independent rule.
- ORPHAN-M-0007 [NON_NORMATIVE] `CLAUDE.md:27-28` — Explanatory: states that an empty SPECIFICATION.md in the template is intentional; it imposes no engineering behaviour beyond GOV-001's 'when non-empty' precondition.
- ORPHAN-M-0039 [NON_NORMATIVE] `.claude/hooks/dependency-guard.mjs:33-34` — Documented coverage gaps (npx npm ..., PowerShell -EncodedCommand) are limitations of the guard, not rules; recorded so the bypass surface is not mistaken for permission.
- ORPHAN-M-0066 [NON_NORMATIVE] `.claude/skills/api-versioning/SKILL.md:116-117` — 'Consider client-generation behavior' is advisory deliberation with no specified outcome; rejected as an extra rule.
- ORPHAN-M-0084 [NON_NORMATIVE] `.claude/skills/authentication/SKILL.md:115-116` — Checked whether this forbids controllers from manufacturing 401/403; it is a hedged description of framework behaviour without a required outcome, so rejected as an extra rule.
- ORPHAN-M-0092 [NON_NORMATIVE] `.claude/skills/caching/SKILL.md:111-112` — 'apply the selected output-cache policy through controller or action metadata' is Controller-specific technique for applying a chosen policy; no restriction on outcomes.
- ORPHAN-M-0109 [NON_NORMATIVE] `.claude/skills/configuration/SKILL.md:209-209` — 'Validating config → ValidateDataAnnotations() + ValidateOnStart()' examined as a possible mandatory mechanism; it is a technique recommendation under RUN-022's startup-validation default, not an independent requirement.
- ORPHAN-M-0128 [NON_NORMATIVE] `.claude/skills/dotnet-testing/SKILL.md:151-152` — Exposing Program via 'public partial class Program' is a technique hint for test access, not a rule.
- ORPHAN-M-0236 [DUPLICATE] `.claude/agents/code-reviewer.md:4-6` — Agent description restates the independent read-only reviewer role (delegation trigger text); the binding rule is owned by the disallowedTools frontmatter and body captured as WF-010 constraints.
- ORPHAN-M-0237 [POLICY_LINKED] `.claude/hooks/dependency-guard.mjs:126-129` — Post-command routing to add-dependency enforces DEP-003/DEP-004/DEP-005 procedure; not an additional rule.
- ORPHAN-M-0238 [DUPLICATE] `.claude/hooks/hook-io.mjs:4-10` — Exit-code contract comment restates the fail-closed PreToolUse behaviour owned by settings.json line 7 (captured as x.settings-failclosed).
- ORPHAN-M-0239 [NON_NORMATIVE] `.claude/hooks/stop-co-change.mjs:27-28` — stop_hook_active guard prevents a Stop loop; implementation safety, no behavioural requirement on outcomes.
- ORPHAN-M-0240 [NON_NORMATIVE] `.claude/hooks/stop-co-change.mjs:30-47` — When no active root or Git is unavailable the co-change check is skipped with a non-blocking system message: an enforcement gap (PST-008/PST-010/TST-009 reminders not raised without Git), not a rule.
- ORPHAN-M-0241 [POLICY_LINKED] `.claude/hooks/stop-co-change.mjs:73-73` — The backend production-without-test reminder enforces TST-009/TST-010 as an advisory gate; only the frontend extension and the address-or-justify gate are EXTRA.
- ORPHAN-M-0242 [POLICY_LINKED] `.claude/rules/angular.md:18-20` — Not introducing NgModules for ordinary features is the complement of FE-001's standalone default, with an explicit integration/legacy exception; treated as the same policy.
- ORPHAN-M-0243 [POLICY_LINKED] `.claude/rules/api.md:21-21` — '204 has no body' is HTTP protocol semantics already entailed by API-003 ('choose statuses according to actual HTTP semantics'); no added engineering choice.
- ORPHAN-M-0244 [POLICY_LINKED] `.claude/rules/api.md:59-63` — 'Readiness stays unhealthy until required startup work completes; never use liveness for that' is the oracle's 'readiness should reflect startup/dependency availability' made explicit; not stricter in outcome.
- ORPHAN-M-0245 [POLICY_LINKED] `.claude/rules/architecture.md:89-90` — 'Controllers do not consume Infrastructure implementation types directly' follows from ARC-001 (API may reference Infrastructure only for composition) together with ARC-011.
- ORPHAN-M-0246 [POLICY_LINKED] `.claude/rules/architecture.md:109-111` — Not expanding a generic repository into an EF query replacement follows from ARC-015 (Infrastructure-only, removes real duplication) and ARC-019 (use EF normally inside Infrastructure).
- ORPHAN-M-0247 [POLICY_LINKED] `.claude/rules/architecture.md:40-44` — The per-test-project reference allow-list is an instance of ARC-028's 'no broader references than test scope requires'; only the project-name convention is recorded separately as EXTRA.
- ORPHAN-M-0248 [POLICY_LINKED] `.claude/rules/dependencies.md:35-36` — Committing package.json with package-lock.json is how DEP-007's 'keep package-lock consistent' is maintained in source control.
- ORPHAN-M-0249 [POLICY_LINKED] `.claude/rules/error-handling.md:48-49` — 'Infrastructure validates assumptions about external systems' is SEC-003 (validate untrusted data at the owning layer) within API-010's owning-boundary rule.
- ORPHAN-M-0250 [POLICY_LINKED] `.claude/rules/persistence.md:24-26` — 'Exposed through a narrow initialization extension' corresponds to the oracle's 'Infrastructure initialization surface'; the Persistence/Seeding/ path is an example.
- ORPHAN-M-0251 [POLICY_LINKED] `.claude/rules/security.md:82-84` — 'In-app HTTPS redirection is not required when that boundary already provides secure transport' is the oracle's 'respect actual hosting topology', not a separate relaxation.
- ORPHAN-M-0252 [POLICY_LINKED] `.claude/rules/testing.md:54-55` — Never connecting automated tests to Production data restates TST-004 isolation from Production data.
- ORPHAN-M-0253 [NON_NORMATIVE] `.claude/scripts/check-instructions.mjs:264-270` — An unparsable settings.json is reported as a failure because hook registrations cannot be checked; mechanical precondition.
- ORPHAN-M-0254 [NON_NORMATIVE] `.claude/scripts/check-manifests.mjs:320-328` — An unparsable package.json is reported as a violation because it cannot be checked; this is a mechanical precondition of the checker, not an engineering policy beyond the oracle.
- ORPHAN-M-0255 [NON_NORMATIVE] `.claude/scripts/check-manifests.mjs:24-27` — SKIP_DIRS (including .claude, node_modules, bin, obj) defines the scan scope of the checker; manifests under these directories are never checked. Scope limit, not a rule.
- ORPHAN-M-0256 [POLICY_LINKED] `.claude/scripts/check-manifests.mjs:52-58` — The checker permits Api→Domain, which ARC-001 does not forbid (dependencies still point inward); no relaxation of the oracle.
- ORPHAN-M-0257 [POLICY_LINKED] `.claude/scripts/check-manifests.mjs:59-65` — The checker lets IntegrationTests reference Infrastructure/Application/Domain in addition to Api (rule text lists Api); this is a looser enforcement net, not a rule permitting broader references, so ARC-028 still governs.
- ORPHAN-M-0258 [NON_NORMATIVE] `.claude/scripts/repo-root.mjs:59-63` — Throwing when no active root can be established makes callers report instead of checking the wrong tree; implementation robustness, no outcome restriction.
- ORPHAN-M-0259 [NON_NORMATIVE] `.claude/skills/angular/SKILL.md:67-68` — 'Reusable presentation components receive data through explicit inputs and emit meaningful UI events' examined as a possible mandatory component pattern; it is descriptive technique consistent with FE-002 without a required/forbidden outcome.
- ORPHAN-M-0260 [NON_NORMATIVE] `.claude/skills/angular/SKILL.md:21-48` — The 'Suggested Structure' tree (core/, shared/, features/<feature>/{pages,components,data-access,models}) was examined as a possible mandated layout; it is explicitly 'suggested' and the binding structure rule is FE-007 (angular.md).
- ORPHAN-M-0261 [NON_NORMATIVE] `.claude/skills/api-versioning/SKILL.md:102-103` — Permissive statement ('may map') with no restriction.
- ORPHAN-M-0262 [NON_NORMATIVE] `.claude/skills/aspnet-error-handling/SKILL.md:129-131` — 'A useful error contract may contain ...' is permissive (may), listing optional fields; it neither requires nor forbids a contract shape.
- ORPHAN-M-0263 [NON_NORMATIVE] `.claude/skills/authentication/SKILL.md:120-120` — Permission for Controllers to use User for purely HTTP-specific data; consistent with ARC-008 and imposes no restriction.
- ORPHAN-M-0264 [NON_NORMATIVE] `.claude/skills/build-fix/SKILL.md:67-67` — 'Use the repository's actual .slnx, project paths, and configuration' only states that the example commands are placeholders; no independent constraint.
- ORPHAN-M-0265 [POLICY_LINKED] `.claude/skills/build-fix/SKILL.md:71-75` — Using package.json scripts that exist (outside CI) is part of reproducing the actual failure (WF-013) and mirrors WF-018; not treated as a new constraint.
- ORPHAN-M-0266 [NON_NORMATIVE] `.claude/skills/caching/SKILL.md:35-37` — HybridCache is explicitly described as an option that 'is not mandatory'; no selection rule is imposed.
- ORPHAN-M-0267 [POLICY_LINKED] `.claude/skills/code-review/SKILL.md:126-127` — Not applying backend project-boundary rules mechanically to Angular follows from the backend scope of the ARC policies.
- ORPHAN-M-0268 [NON_NORMATIVE] `.claude/skills/dependency-injection/SKILL.md:255-265` — Decision-guide 'Recommendation' rows (Scoped for services using repositories/UoW, Singleton-compatible for immutable config, keyed/decorator/Scrutor/factory) examined; lifetime validity is captured as ARC-022 and the rest is optional DI technique (EXC-005).
- ORPHAN-M-0269 [POLICY_LINKED] `.claude/skills/development-workflow/SKILL.md:19-20` — Also reading CUSTOM_SETTINGS.md before planning is covered by GOV-002 together with GOV-008 (CUSTOM_SETTINGS owns approved values).
- ORPHAN-M-0270 [NON_NORMATIVE] `.claude/skills/docker/SKILL.md:99-100` — 'Compose is useful ... when the project benefits from it' is permissive; restriction to used infrastructure is captured at lines 115-117.
- ORPHAN-M-0271 [NON_NORMATIVE] `.claude/skills/dotnet-testing/SKILL.md:47-48` — Arrange/Act/Assert is described as 'a useful default structure' with optional comments; permissive technique, no mandatory outcome.
- ORPHAN-M-0272 [NON_NORMATIVE] `.claude/skills/ef-core/SKILL.md:228-229` — 'consider keyset pagination ... when justified' is advisory deliberation without a required outcome.
- ORPHAN-M-0273 [POLICY_LINKED] `.claude/skills/git-workflow/SKILL.md:14-15` — 'Completing an implementation is not a request to commit/push/merge' is GOV-015's explicit-request condition applied.
- ORPHAN-M-0274 [NON_NORMATIVE] `.claude/skills/health-check/SKILL.md:30-30` — 'Use more specific readiness/liveness endpoints when appropriate' leaves the decision open ('when appropriate'); the liveness/readiness distinction itself is captured from api.md and lines 16-18.
- ORPHAN-M-0275 [NON_NORMATIVE] `.claude/skills/http-api/SKILL.md:221-222` — 'consider an idempotency key' is advisory; the binding part (do not claim idempotency without a mechanism) is captured at lines 228-231.
- ORPHAN-M-0276 [NON_NORMATIVE] `.claude/skills/logging/references/serilog.md:287-298` — Recommendation table of optional Serilog tooling (Seq/Aspire, Elastic sink, AuditTo, Serilog.Expressions); lines 76-81 state these sinks/enrichers are not baseline dependencies, so the table imposes no adoption.
- ORPHAN-M-0277 [NON_NORMATIVE] `.claude/skills/swagger/SKILL.md:28-41` — Basic setup example enables Swagger only inside IsDevelopment(); examined as an executable rule but it is an illustrative snippet; the exposure rule is API-017 in api.md.
- ORPHAN-M-0278 [POLICY_LINKED] `.claude/skills/verify/SKILL.md:153-155` — Treating imports already provided by implicit/global usings as redundant is within RUN-010's 'unused/redundant usings'.
- ORPHAN-M-0279 [NON_NORMATIVE] `.editorconfig:31-33` — Note documents an enforcement gap: IDE0005 (unused usings) is reported in command-line builds only with GenerateDocumentationFile=true, which Directory.Build.props does not set; RUN-010 therefore relies on the verify workflow rather than build failure. Recorded as a limitation, not a rule.
- ORPHAN-M-0280 [NON_NORMATIVE] `CLAUDE.md:157-166` — Routing-table rows were examined as possible additional mandatory triggers (e.g. 'Any Git operation → git-workflow'); they are loading routes for workflows whose obligations are captured in each skill; the obligation to run the matching workflow is captured at lines 152-153 (WF-001).
- ORPHAN-M-0281 [POLICY_LINKED] `CLAUDE.md:139-141` — 'Never make a Reserved decision' in headless runs and reporting unresolved requests is entailed by GOV-017 (Reserved changes need explicit approval; headless runs must not silently alter architecture).
- ORPHAN-M-0282 [POLICY_LINKED] `CLAUDE.md:85-90` — Repository layout with tests beside production projects and no top-level tests/ directory is DEP-024/DEP-013 verbatim in substance.
- ORPHAN-M-0283 [POLICY_LINKED] `docs/technology-stack.md:24-25` — 'Add sinks only when required' is DEP-001's current-need rule applied to Serilog sink packages.

## Reverse checks conducted

- Orphan candidates were recorded during batch annotation (as each potentially normative clause was met) and in a dedicated reverse pass after all 19 batches (`_work/annot/Z_SWEEP.txt`).
- Keyword sweep: `stagea.py sweep` listed every line inside NON_NORMATIVE, IMPLEMENTATION and DUPLICATE ranges containing a normative keyword (must, never, only, should, do not, avoid, prefer, require, default, unless, except, block, deny, reject, exit(, throw, error, fail, stop, approval, allowed, instead). 222 hits were reviewed one by one; headings, ownership banners, pointers, code identifiers and example strings were confirmed non-operative, and the remaining leads were recorded as orphan rows.
- MIXED ranges (oracle + EXTRA in one physical range) were re-read so that each embedded extra clause has its own EXTRA constraint and orphan trace.
- Executable surfaces: every hook/checker branch with an exit code, `blockTool`, `postToolBlock`, `decision: block`, violation push or failure push was traced to a constraint or an IMPLEMENTATION reason; `settings.json` onFailure/timeout fields and `.editorconfig` severities were reviewed; enforcement gaps (IDE0005 not reported in CLI builds, Stop hook skipped without Git, parser gaps of the npm guard, unchecked projects with non-conforming names) were recorded as NON_NORMATIVE limitations.
- Frontmatter: `paths` globs (loading scope), skill `description` triggers, `disable-model-invocation`, agent `disallowedTools` and preloaded `skills` were reviewed as effective configuration.
- Borderline oracle-linked decisions (where a more specific clause might have been EXTRA) were recorded as POLICY_LINKED rows with the reason the oracle already entails the behaviour.

## Limitation

A complete line disposition plus this sweep is not proof of semantic exhaustiveness.
