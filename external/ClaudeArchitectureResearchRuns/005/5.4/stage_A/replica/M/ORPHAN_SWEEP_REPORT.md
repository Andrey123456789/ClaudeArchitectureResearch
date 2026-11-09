# M — Orphan sweep report (Claude Run 2, blind replica)

## Counts

- Orphan candidates identified: 65
- EXTRA registered: 26 (EXTRA constraints in constraints.jsonl: 26)
- Mapped to oracle (POLICY_LINKED): 0
- Non-normative / rejected: 36
- Duplicates: 1
- Unresolved (LINK_UNCERTAIN): 2

## Unresolved items (LINK_UNCERTAIN)

- **ORPHAN-M-0008** -> UNCERTAIN-M-0001 at `.claude/rules/dependencies.md:34-37`: "package manager. Maintain and commit `package.json` and `package-lock.json` and"
  - Question: DEP-007 requires a consistent lockfile, while GOV-015 forbids commits without an explicit request; whether 'commit' is a commit instruction or only means 'keep under version control' cannot be decided from the text.
  - Ledger reason: DEP-007 requires a consistent lockfile, while GOV-015 forbids commits without an explicit request; whether 'commit' is a commit instruction or only means 'keep under version control' cannot be decided from the text.
- **ORPHAN-M-0018** -> UNCERTAIN-M-0002 at `.claude/skills/git-workflow/SKILL.md:98-102`: "high-risk. Perform them only when explicitly requested or clearly required by an"
  - Question: GOV-015 requires an explicit request for repository-changing operations; whether 'clearly required by an approved workflow' is an admissible substitute for that request cannot be decided from the oracle text.
  - Ledger reason: GOV-015 requires an explicit request for repository-changing operations; whether 'clearly required by an approved workflow' is an admissible substitute for that request cannot be decided from the oracle text.

## Reverse checks conducted

Reverse checks conducted after all 19 batches, judged from M's own text (no judgment carried over from K1, K0, L1, L0 or M1; only the classification method was reused):

1. **Keyword scan of all NON_NORMATIVE / IMPLEMENTATION / DUPLICATE spans** (`_tools/sweep.py`); every Markdown hit re-read in context. Imperative technique notes were recorded as NON_NORMATIVE orphans: coding-style.md records/visibility/modern-syntax/naming preferences (EXC-003 class), Result typed-error shape, authorization/frontend/versioning test targeting, 304/429/502/idempotency HTTP reference entries, Swagger launch profile and document partitioning, probe status mapping, Dockerfile copy/caching/context techniques, test doubles, test-data and snapshot libraries, EF Core tracking and bulk-operation caveats, message-delivery resilience, log-level definitions, required-member technique, build-once/promote preference, assembly scanning, naming heuristics, literal single-sourcing ('prefer') and conditional Git completion reporting ('when useful').
2. **CLAUDE.md vocabulary applied**: M defines 'prefer / avoid' as guidance and 'default' as deviation-with-reason-that-must-be-reported (registered as X26). Items that appear only in 'Avoid' anti-pattern lists — caching EF tracked entities, fire-and-forget EF operations, logs as an audit database — were therefore recorded as NON_NORMATIVE orphans, not EXTRA; the shared DefaultRequestHeaders rule is EXTRA (X21) because the main text states it as a binding 'do not'; the EF Core application-level retry rule is a stated default (X20).
3. **Large-span review** (NN/IM/DU spans of 15+ lines): code samples, YAML/JSON/Dockerfile examples, directory trees, MAP.md navigation tables, `.editorconfig` settings and hook registrations only.
4. **Script branch review** (static): `dependency-guard.mjs` PreToolUse blocks npm install/ci/install-test/update with --force, -f, --legacy-peer-deps, the equivalent npm config keys and npm_config_* environment settings (R4; no approval path; npx npm and PowerShell -EncodedCommand are not parsed); PostToolUse/PostToolUseFailure run the manifest check after dependency or reference commands and after any shell command that changed manifests, route to add-dependency (R5), architecture.md and Decision Control (R6, X1), and report removed manifests through Decision Control (X1, X2); there is no PreToolUse gate on package additions. `file-change.mjs` reminds about CUSTOM_SETTINGS.md/SPECIFICATION.md (R7, R8) and checks edited manifests (R5, X3). `stop-co-change.mjs` reminds about seeder co-change, migration review and missing tests once per change state (R9-R11). `check-manifests.mjs`: deny list (X9), review notes for MediatR, Polly, FluentValidation.AspNetCore, Serilog.Sinks.Elasticsearch, NgRx/Axios/Lodash/Bootstrap/Tailwind (R135-R138), CPM and versionless references (R70), floating/prerelease versions (R139), npm tooling category and lockfile (R71, U1), layer reference direction (R37, R38). `check-instructions.mjs`: predicates mapped to X6 and X8 (plus the read-only reviewer check, R1/R2).
5. **Branch findings recorded**: Stop reminders are suppressed for an unchanged state (DU orphan; exception of R9-R11); the force-flag guard has documented parsing gaps (NN orphan); the deny list has no approval path (X9).
6. **Config defaults**: settings.json (only PreToolUse fails closed; exec-form registrations X6), `.editorconfig` (IDE0005 at warning, Async suffix and file-scoped namespaces at suggestion), Directory.Build.props (net10.0 R214; Nullable, ImplicitUsings and AnalysisLevel latest registered as X27; EnforceCodeStyleInBuild implements RUN-010), Directory.Packages.props (CPM on, empty), solution-layout (global.json SDK pin X22).
7. **Mixed clauses** split into oracle and extra parts (CLAUDE.md Reserved items 3 and 9, approval-and-recording line, workflow routing; dependency rule and file-change hook removal routing; git-workflow push and pull-request paragraphs; build-fix, development-workflow and security-scan reports; FluentValidation registration package).
8. **Notable M-specific structure**: the instruction-system ownership, placement, header/paths and hook-registration rules are template-structure extras (X4, X5, X6, X8, X25); CLAUDE.md adds the unclear-case test that makes any 'yes' Reserved (X2) and the duty to report every deviation from a default (X26).

Classification rule (same method as for K1, K0, L1, L0 and M1): EXTRA when binding (must/never/do not/only, a named anti-pattern prohibition, or hook/checker-enforced), outcome-changing and not entailed by a stack-neutral reading of an oracle policy; technique classes excluded by the oracle (EXC-002..EXC-018) stay NON_NORMATIVE; workflow report-content mandates beyond WF-009 are EXTRA; statements the template itself marks as 'prefer/avoid' guidance are not registered as EXTRA.

## Full orphan ledger

| ID | Resolution | Location | Constraints | Closest policies | Reason |
|---|---|---|---|---|---|
| ORPHAN-M-0001 | EXTRA_REGISTERED | `.claude/hooks/dependency-guard.mjs:130-133` | EXTRA-M-0001 | ARC-020, ARC-001, GOV-017 | ARC-020 requires approval for new layers/projects and ARC-001 constrains direction; no oracle policy makes individual reference edges or project removal Reserved. |
| ORPHAN-M-0002 | EXTRA_REGISTERED | `.claude/hooks/dependency-guard.mjs:169-170` | EXTRA-M-0002 | GOV-017, ARC-020 | GOV-017 defines Decided/Delegated/Reserved classes; the oracle does not provide a test that turns any of these properties into a Reserved decision. |
| ORPHAN-M-0003 | EXTRA_REGISTERED | `.claude/hooks/file-change.mjs:65-68` | EXTRA-M-0003 | DEP-001 | DEP-001..DEP-005 govern additions and updates; no oracle policy routes removals through the dependency workflow. |
| ORPHAN-M-0004 | EXTRA_REGISTERED | `.claude/MAP.md:22-26` | EXTRA-M-0004 | — | Instruction-system ownership rule; the oracle does not regulate where instruction content lives. |
| ORPHAN-M-0005 | EXTRA_REGISTERED | `.claude/MAP.md:198-212` | EXTRA-M-0005 | — | Instruction-system maintenance procedure; no oracle policy governs instruction placement. |
| ORPHAN-M-0006 | EXTRA_REGISTERED | `.claude/MAP.md:111-111` | EXTRA-M-0006 | — | Hook wiring is template infrastructure; no oracle policy addresses hook registration or failure modes. |
| ORPHAN-M-0007 | EXTRA_REGISTERED | `.claude/rules/api.md:33-35` | EXTRA-M-0007 | API-013, ARC-020 | API-013 allows introducing versioning for a concrete compatibility need without requiring approval; ARC-020's consequential-change list does not name versioning adoption. |
| ORPHAN-M-0008 | LINK_UNCERTAIN | `.claude/rules/dependencies.md:34-37` | UNCERTAIN-M-0001 | GOV-015, DEP-007 | DEP-007 requires a consistent lockfile, while GOV-015 forbids commits without an explicit request; whether 'commit' is a commit instruction or only means 'keep under version control' cannot be decided from the text. |
| ORPHAN-M-0009 | EXTRA_REGISTERED | `.claude/scripts/check-instructions.mjs:11-21` | EXTRA-M-0008 | — | instruction-system files |
| ORPHAN-M-0010 | EXTRA_REGISTERED | `.claude/scripts/check-manifests.mjs:29-33` | EXTRA-M-0009 | DEP-004, DEP-020 | DEP-004 requires deprecation checks and DEP-020 prefers the Microsoft resilience packages; no oracle policy forbids specific packages outright regardless of approval. |
| ORPHAN-M-0011 | EXTRA_REGISTERED | `.claude/skills/add-dependency/SKILL.md:141-143` | EXTRA-M-0010 | DEP-001, GOV-014 | DEP-001 governs adding dependencies and GOV-014 limits scope; no oracle policy requires removing unused dependencies. |
| ORPHAN-M-0012 | EXTRA_REGISTERED | `.claude/skills/add-dependency/SKILL.md:147-148` | EXTRA-M-0011 | DEP-004, DEP-005, WF-009 | DEP-004/DEP-005 require the checks and approval gate and WF-009 truthful verification reporting; no oracle policy prescribes the dependency report contents. |
| ORPHAN-M-0013 | EXTRA_REGISTERED | `.claude/skills/architecture-decision/SKILL.md:43-48` | EXTRA-M-0012 | GOV-017, GOV-007 | GOV-017 requires approval for Reserved decisions but no recording artifact; no oracle policy requires decision records or planning-owner updates. |
| ORPHAN-M-0014 | EXTRA_REGISTERED | `.claude/skills/aspnet-error-handling/SKILL.md:152-156` | EXTRA-M-0013 | DEP-010, API-010 | DEP-010 fixes FluentValidation as the library and API-010 the validation boundaries; no oracle policy prescribes the registration package or method. |
| ORPHAN-M-0015 | EXTRA_REGISTERED | `.claude/skills/build-fix/SKILL.md:243-251` | EXTRA-M-0014 | WF-009 | WF-009 requires reporting actual verification states only; the failure, root-cause, changes and remaining-issues sections are additional reporting duties. |
| ORPHAN-M-0016 | EXTRA_REGISTERED | `.claude/skills/code-review/SKILL.md:175-184` | EXTRA-M-0016 | WF-011, WF-012 | WF-011/WF-012 govern priorities and honesty of findings; the oracle does not prescribe a findings format or severity scale. |
| ORPHAN-M-0017 | EXTRA_REGISTERED | `.claude/skills/development-workflow/SKILL.md:119-121` | EXTRA-M-0017 | WF-009 | WF-009 requires truthful verification reporting and GOV-017 reporting of unresolved Decision Requests; no oracle policy requires reporting delegated choices or non-applicable obligations. |
| ORPHAN-M-0018 | LINK_UNCERTAIN | `.claude/skills/git-workflow/SKILL.md:98-102` | UNCERTAIN-M-0002 | GOV-015, GOV-020 | GOV-015 requires an explicit request for repository-changing operations; whether 'clearly required by an approved workflow' is an admissible substitute for that request cannot be decided from the oracle text. |
| ORPHAN-M-0019 | EXTRA_REGISTERED | `.claude/skills/git-workflow/SKILL.md:77-79` | EXTRA-M-0018 | GOV-015, GOV-020 | GOV-015 requires an explicit request for force-push; the oracle does not declare named branches categorically non-rewritable. |
| ORPHAN-M-0020 | EXTRA_REGISTERED | `.claude/skills/git-workflow/SKILL.md:91-94` | EXTRA-M-0019 | WF-009, WF-022 | WF-009 covers truthful verification reporting and WF-022 focused commits; the oracle does not prescribe PR preparation or description contents. |
| ORPHAN-M-0021 | EXTRA_REGISTERED | `.claude/skills/httpclient-factory/references/resilience.md:99-104` | EXTRA-M-0020 | RUN-016 | RUN-016 limits retries to safe repeats; no oracle policy forbids application-level retry of persistence operations or prescribes the EF Core execution strategy. |
| ORPHAN-M-0022 | EXTRA_REGISTERED | `.claude/skills/httpclient-factory/SKILL.md:166-169` | EXTRA-M-0021 | RUN-005 | RUN-005 governs client lifetime; no oracle policy addresses mutation of shared default headers. |
| ORPHAN-M-0023 | EXTRA_REGISTERED | `.claude/skills/project-structure/references/solution-layout.md:94-97` | EXTRA-M-0022 | DEP-008, DEP-003 | DEP-008 fixes the .NET platform and DEP-003 package versions; no oracle policy requires an SDK pin file. |
| ORPHAN-M-0024 | EXTRA_REGISTERED | `.claude/skills/security-scan/references/scan-layers.md:339-354` | EXTRA-M-0023 | WF-020 | WF-020 requires evidence and contextual severity; the oracle does not prescribe a security finding format. |
| ORPHAN-M-0025 | EXTRA_REGISTERED | `.claude/skills/security-scan/SKILL.md:15-20` | EXTRA-M-0024 | WF-020, WF-009 | WF-020/WF-009 require contextual severity and truthful status reporting; the oracle does not prescribe report sections, layer tables or a severity scale. |
| ORPHAN-M-0026 | EXTRA_REGISTERED | `.claude/skills/template-maintenance/SKILL.md:63-65` | EXTRA-M-0025 | — | Instruction-system maintenance procedure; no oracle policy governs testing or reporting of instruction-system changes. |
| ORPHAN-M-0027 | EXTRA_REGISTERED | `CLAUDE.md:14-14` | EXTRA-M-0026 | — | The oracle defines DEFAULT-strength policies but does not attach a duty to report deviations. |
| ORPHAN-M-0028 | EXTRA_REGISTERED | `Directory.Build.props:9-11` | EXTRA-M-0027 | DEP-023, RUN-009 | DEP-023 places shared settings in Directory.Build.props but no oracle policy requires nullable reference types, implicit usings or a particular analysis level. |
| ORPHAN-M-0029 | NON_NORMATIVE | `.claude/rules/coding-style.md:37-40` | — | RUN-009, RUN-011 | Records-vs-classes preference (EXC-003 class); the anti-mechanical-conversion clause is aligned with RUN-011 and not registered separately. |
| ORPHAN-M-0030 | NON_NORMATIVE | `.claude/rules/coding-style.md:41-44` | — | RUN-009 | Visibility and sealed-modifier preference (EXC-003 class); low-level style guidance. |
| ORPHAN-M-0031 | NON_NORMATIVE | `.claude/rules/coding-style.md:45-47` | — | RUN-009 | Modern-syntax preference (EXC-003 class); readability judgment left to the agent. |
| ORPHAN-M-0032 | NON_NORMATIVE | `.claude/rules/coding-style.md:50-53` | — | RUN-009, RUN-024 | Standard .NET naming (EXC-003 class); private-field naming defers to repository conventions (RUN-009). |
| ORPHAN-M-0033 | NON_NORMATIVE | `.claude/skills/aspnet-error-handling/SKILL.md:92-95` | — | API-009, ARC-020 | Shape guidance for an optional Result pattern whose project-wide adoption is Reserved (RULE-M-0142); technique of an approval-gated pattern. |
| ORPHAN-M-0034 | NON_NORMATIVE | `.claude/skills/authentication/SKILL.md:156-164` | — | TST-003, SEC-005 | Authorization test targeting (EXC-012 class); consistent with behavior-focused testing (RULE-M-0128). |
| ORPHAN-M-0035 | NON_NORMATIVE | `.claude/skills/http-api/SKILL.md:87-89` | — | API-003 | 304 reference entry (EXC-009); standard conditional-request semantics. |
| ORPHAN-M-0036 | NON_NORMATIVE | `.claude/skills/http-api/SKILL.md:182-184` | — | API-003 | 429 reference entry (EXC-009). |
| ORPHAN-M-0037 | NON_NORMATIVE | `.claude/skills/http-api/SKILL.md:196-198` | — | API-003 | 502 reference entry (EXC-009). |
| ORPHAN-M-0038 | NON_NORMATIVE | `.claude/skills/http-api/SKILL.md:228-231` | — | API-003, RUN-016 | Idempotency-key reference (EXC-009); truthfulness of a contract claim, not a separate obligation. |
| ORPHAN-M-0039 | NON_NORMATIVE | `.claude/skills/swagger/SKILL.md:57-58` | — | API-016 | Launch-profile technique (EXC-008). |
| ORPHAN-M-0040 | NON_NORMATIVE | `.claude/skills/swagger/SKILL.md:114-115` | — | API-016 | Document partitioning (EXC-008). |
| ORPHAN-M-0041 | NON_NORMATIVE | `.claude/skills/health-check/SKILL.md:88-91` | — | API-018, API-019 | Probe status mapping (EXC-010). |
| ORPHAN-M-0042 | NON_NORMATIVE | `.claude/skills/docker/SKILL.md:61-63` | — | DEP-018, DEP-019 | Dockerfile shape (EXC-006). |
| ORPHAN-M-0043 | NON_NORMATIVE | `.claude/skills/docker/SKILL.md:67-70` | — | DEP-019 | Restore-layer caching technique (EXC-006). |
| ORPHAN-M-0044 | NON_NORMATIVE | `.claude/skills/docker/SKILL.md:150-151` | — | DEP-019 | Build-context exclusion technique (EXC-006). |
| ORPHAN-M-0045 | NON_NORMATIVE | `.claude/skills/dotnet-testing/SKILL.md:83-86` | — | TST-003 | Mock/fake choice (EXC-012). |
| ORPHAN-M-0046 | NON_NORMATIVE | `.claude/skills/dotnet-testing/SKILL.md:202-204` | — | GOV-013, TST-008 | Builders/fixtures technique (EXC-012). |
| ORPHAN-M-0047 | NON_NORMATIVE | `.claude/skills/dotnet-testing/SKILL.md:242-244` | — | GOV-013 | Snapshot-testing technique (EXC-012). |
| ORPHAN-M-0048 | NON_NORMATIVE | `.claude/skills/angular/SKILL.md:182-187` | — | TST-003, TST-011 | Frontend test targeting (EXC-018). |
| ORPHAN-M-0049 | NON_NORMATIVE | `.claude/skills/api-versioning/SKILL.md:135-139` | — | TST-003, API-022 | Versioning test targeting (EXC-012 class). |
| ORPHAN-M-0050 | NON_NORMATIVE | `.claude/skills/ef-core/SKILL.md:178-182` | — | RUN-006 | Tracking technique (EXC-011). |
| ORPHAN-M-0051 | NON_NORMATIVE | `.claude/skills/ef-core/SKILL.md:242-244` | — | RUN-006, ARC-016 | Consistency caveat of an optional bulk-operation technique (EXC-011); 'casually' leaves the outcome to judgment. |
| ORPHAN-M-0052 | NON_NORMATIVE | `.claude/skills/ef-core/SKILL.md:410-412` | — | RUN-002 | Listed under Anti-Patterns with 'Avoid', which CLAUDE.md's normative vocabulary defines as guidance; therefore not registered as EXTRA. |
| ORPHAN-M-0053 | NON_NORMATIVE | `.claude/skills/caching/SKILL.md:136-138` | — | RUN-021, ARC-016 | 'Avoid' guidance in CLAUDE.md's vocabulary; the tracked-entity item is not registered as EXTRA; the other items restate RULE-M-0093 and RULE-M-0149. |
| ORPHAN-M-0054 | NON_NORMATIVE | `.claude/skills/logging/SKILL.md:101-103` | — | RUN-013, RUN-014 | 'Avoid' guidance in CLAUDE.md's vocabulary; the audit-database item is not registered as EXTRA. |
| ORPHAN-M-0055 | NON_NORMATIVE | `.claude/skills/logging/SKILL.md:44-51` | — | API-012, API-009 | Log-level definitions are operational technique; which outcomes are not errors is owned by error-handling.md (RULE-M-0078). |
| ORPHAN-M-0056 | NON_NORMATIVE | `.claude/skills/httpclient-factory/references/resilience.md:108-111` | — | RUN-016 | Message-delivery technique (EXC-007). |
| ORPHAN-M-0057 | NON_NORMATIVE | `.claude/skills/modern-csharp/SKILL.md:53-54` | — | ARC-003, ARC-004 | Required-member technique (EXC-002). |
| ORPHAN-M-0058 | NON_NORMATIVE | `.claude/skills/ci-cd/SKILL.md:148-150` | — | WF-017 | Build-once/promote preference (EXC-014). |
| ORPHAN-M-0059 | NON_NORMATIVE | `.claude/skills/dependency-injection/SKILL.md:167-169` | — | ARC-021, ARC-023 | Assembly-scanning technique (EXC-005). |
| ORPHAN-M-0060 | NON_NORMATIVE | `.claude/skills/project-structure/references/backend-layout.md:66-72` | — | ARC-027 | Naming and bucket heuristics (EXC-004); 'avoid'/'prefer' guidance. |
| ORPHAN-M-0061 | NON_NORMATIVE | `.claude/skills/custom-settings/SKILL.md:23-29` | — | GOV-021 | 'Prefer' guidance on single sourcing of a setting literal; not an outcome-changing obligation. |
| ORPHAN-M-0062 | NON_NORMATIVE | `.claude/skills/git-workflow/SKILL.md:106-108` | — | WF-009 | Conditional ('when useful') completion reporting; not registered as a report-content EXTRA. |
| ORPHAN-M-0063 | DUPLICATE | `.claude/hooks/stop-co-change.mjs:6-9` | RULE-M-0009, RULE-M-0010, RULE-M-0011 | — | Executable default of the Stop hook: seed, migration-review and test reminders are repeated only for a changed state and never while stop_hook_active is set; recorded in the exceptions of R9-R11. |
| ORPHAN-M-0064 | NON_NORMATIVE | `.claude/hooks/dependency-guard.mjs:25-34` | — | DEP-025 | Enforcement limitation of the PreToolUse force-flag guard (RULE-M-0004): commands routed through npx npm or an encoded PowerShell command are not parsed. Not an additional rule. |
| ORPHAN-M-0065 | NON_NORMATIVE | `.claude/hooks/hook-io.mjs:4-9` | — | — | Hook failure policy (PreToolUse fails closed, other hooks fail visibly); describes enforcement behavior, not an additional rule for agent output. |

A completed line disposition plus this sweep is not proof of semantic exhaustiveness.
