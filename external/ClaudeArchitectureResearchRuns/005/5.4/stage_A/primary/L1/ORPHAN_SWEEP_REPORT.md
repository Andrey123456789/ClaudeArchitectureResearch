# Orphan sweep report — candidate L1

Every EXTRA and LINK_UNCERTAIN constraint has at least one orphan row; additional rows record clauses that were examined as possible extras and resolved as oracle-linked, duplicate or non-normative. Disproven hypotheses are kept, not deleted.

## Counts

- Orphan candidates identified: 258
- EXTRA registered (EXTRA_REGISTERED): 233 (EXTRA constraints: 233)
- Mapped to oracle (POLICY_LINKED): 8
- Non-normative / discarded (NON_NORMATIVE): 8
- Duplicates (DUPLICATE): 7
- Unresolved (LINK_UNCERTAIN): 2

## Unresolved items

### ORPHAN-L1-0093
- Constraint(s): UNCERTAIN-L1-0001; closest policies: RUN-021
- Evidence: `output/template/.claude/skills/caching/SKILL.md:49-49` — "- Invalidation strategies: remove affected keys after a successful mutation, short TTL with tolerated staleness, tag/group invalidation, versioned keys. Invalidating before the mutation is known to succeed must be a deliberate choice."
- Open question: RUN-021 requires invalidation only consistent with successful underlying mutations; whether a deliberate pre-mutation invalidation is a permitted exception or a relaxation that contradicts RUN-021 cannot be decided from the text.

### ORPHAN-L1-0140
- Constraint(s): UNCERTAIN-L1-0002; closest policies: GOV-015
- Evidence: `output/template/.claude/skills/git-workflow/SKILL.md:16-16` — "- High-risk operations — `git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion, rebasing shared history — run only when explicitly requested or required by an approved workflow, and only after inspecting what will be lost or rewritten. Treat `main`, `master`, and other protected or shared branches as non-rewritable."
- Open question: GOV-015 permits repository-changing Git operations only when explicitly requested; whether 'required by an approved workflow' widens that condition or only describes an explicitly requested workflow cannot be decided from the text.

## Rejected false leads and oracle-linked resolutions

- ORPHAN-L1-0236 [POLICY_LINKED] `.claude/capabilities/frontend/angular/commands.md:20-27` — Command table conditions ('only when configured', 'only when required') restate the existing-scripts rule and DEP-016.
- ORPHAN-L1-0237 [POLICY_LINKED] `.claude/capabilities/persistence/ef-core/commands.md:29-32` — Command comments ('Development only', 'explicit recreation for a fresh seed dataset') restate the Development-only scope captured at line 34.
- ORPHAN-L1-0238 [DUPLICATE] `.claude/capabilities/persistence/ef-core/MODULE.md:24-24` — Declared properties (incl. database default collation) restate the selection record, where relying on the collation for observable behaviour needs approval.
- ORPHAN-L1-0239 [DUPLICATE] `.claude/hooks/post-change-checks.mjs:2-12` — Header comment describing actual-state manifest validation implemented in the code segments.
- ORPHAN-L1-0240 [DUPLICATE] `.claude/hooks/pre-shell-command.mjs:2-9` — Header comment describing ask/deny-once/fail-closed behaviour implemented in the code segments.
- ORPHAN-L1-0241 [DUPLICATE] `.claude/hooks/stop-cochange.mjs:2-7` — Header comment describing the once-per-state non-looping reminder implemented in the code segments.
- ORPHAN-L1-0242 [DUPLICATE] `.claude/INSTRUCTION_MAP.md:133-140` — Enforcement-asset rows (fail-closed gate, deny-once routing, manifest/architecture/stop checks) describe behaviour captured from settings.json, the hooks and scripts.
- ORPHAN-L1-0243 [NON_NORMATIVE] `.claude/rules/1-architecture/roles.md:16-24` — Role vocabulary definitions; terminology used by other rules, no obligation of its own.
- ORPHAN-L1-0244 [DUPLICATE] `.claude/rules/3-project/decisions.md:37-37` — Facet-resolution mechanics incl. 'a cleared optional slot (none) means its facets do not apply'; the clearing procedure is captured from the frontend contract.
- ORPHAN-L1-0245 [NON_NORMATIVE] `.claude/skills/aspnet-error-handling/SKILL.md:14-38` — Example handler returns status 499 and skips error logging for aborted requests; the 499 code is example technique, the operative rule (cancellation is not a server failure) is API-021 in http-api.md.
- ORPHAN-L1-0246 [NON_NORMATIVE] `.claude/skills/aspnet-error-handling/SKILL.md:64-64` — Descriptive contents of a useful error contract; no obligation stated.
- ORPHAN-L1-0247 [POLICY_LINKED] `.claude/skills/aspnet-error-handling/SKILL.md:82-87` — Anti-example comments ('never', 'redundant when the global handler logs') restate the catch rule at line 80 (API-007/API-012).
- ORPHAN-L1-0248 [NON_NORMATIVE] `.claude/skills/caching/SKILL.md:20-20` — HybridCache described as a strong option, explicitly not mandatory.
- ORPHAN-L1-0249 [POLICY_LINKED] `.claude/skills/ci-cd/SKILL.md:18-23` — Code comment 'only if the project enforces formatting' restates the adopted-gate rule at line 25.
- ORPHAN-L1-0250 [POLICY_LINKED] `.claude/skills/configuration/SKILL.md:56-61` — Code comment contrasting typed options with parsing IConfiguration restates RUN-022.
- ORPHAN-L1-0251 [POLICY_LINKED] `.claude/skills/ef-core/SKILL.md:122-151` — Seeder example comment ('anchor entity: data exists') illustrates leaving existing data unchanged (PST-006).
- ORPHAN-L1-0252 [DUPLICATE] `.claude/skills/logging/references/serilog.md:99-108` — Decision-table row 'Audit trails (only with an adopted audit design)' restates the audit-design condition.
- ORPHAN-L1-0253 [POLICY_LINKED] `.claude/skills/project-structure/references/solution-layout.md:7-25` — Tree comments ('maintained documentation only', subdirectories 'when content exists') restate the create-only-when-needed rule.
- ORPHAN-L1-0254 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:19-19` — Investigation prompts (EXC-015 context); owning invariants SEC-001/SEC-007/API-008 are captured in the rule files.
- ORPHAN-L1-0255 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:28-28` — Unsafe-deserialization line lists patterns to investigate without an imperative; recorded as a rejected extra lead.
- ORPHAN-L1-0256 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:51-51` — Pointer-style prompt comparing public errors with http-api.md failure rules (captured there).
- ORPHAN-L1-0257 [POLICY_LINKED] `.claude/skills/security-scan/references/scan-layers.md:70-73` — Severity examples illustrate WF-020.
- ORPHAN-L1-0258 [NON_NORMATIVE] `.claude/skills/template-maintenance/SKILL.md:32-32` — Technical note on where the checker command runs; no added obligation.

## Reverse checks conducted

- Full reverse annotation: every non-blank line of all 86 active files (10 queue batches, 4279 non-blank lines) was assigned to exactly one coverage range; normative ranges cite their constraints and every NON_NORMATIVE / IMPLEMENTATION / DUPLICATE range carries a specific reason. Hook and checker scripts were reviewed branch by branch (pre-shell fail-closed input/exception paths, 'ask' and deny-once branches, post-change manifest and architecture findings, Stop reminder state de-duplication, checker error vs warning branches) and the capability `enforcement.json`/`check.json` and `manifest-policy.json` entries were read as enforcement data.
- Keyword sweep: `stagea.py sweep` listed 217 normative-keyword hits inside 131 NON_NORMATIVE / IMPLEMENTATION / DUPLICATE ranges. Each hit was reviewed; most are code tokens (`throw`, `catch`, `required`, `default`), ownership/loading banners, headings, table headers or pointers.
- Borderline hits and examined hypotheses were recorded as explicit orphan rows (Z_SWEEP): code and tree comments carrying rules (error-handling anti-example, ci-cd format gate, typed options, seeder anchor entity, solution-layout 'when content exists', EF commands 'Development only', Angular 'only when configured'), hook header comments and INSTRUCTION_MAP rows (DUPLICATE to the enforcing constraint), the decisions.md cleared-slot clause and ef-core MODULE collation property (DUPLICATE), permissive or descriptive skill wording (HybridCache 'not mandatory', error-contract contents), the 499 status in an error-handling example, investigation prompts and severity examples in the security-scan reference, role vocabulary definitions and a template-maintenance technical note.
- Check-by-reference lists and decision tables were verified item by item against owner clauses while annotating; lists containing items without an owner clause were annotated MIXED with the item registered as EXTRA.
- Forward check: each of the 196 policies was searched across all 86 files and cross-checked against the constraint ledger; all 196 have at least one oracle-linked constraint. Modality caveats, enforcement notes and the two open related items are recorded in `policies.jsonl` search notes.

## Limitation

A complete line disposition plus this sweep is not proof of semantic exhaustiveness.
