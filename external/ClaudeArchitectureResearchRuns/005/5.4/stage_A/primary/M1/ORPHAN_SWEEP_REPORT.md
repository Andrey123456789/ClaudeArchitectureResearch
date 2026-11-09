# Orphan sweep report — candidate M1

Every EXTRA and LINK_UNCERTAIN constraint has at least one orphan row; additional rows record clauses that were examined as possible extras and resolved as oracle-linked, duplicate or non-normative. Disproven hypotheses are kept, not deleted.

## Counts

- Orphan candidates identified: 283
- EXTRA registered (EXTRA_REGISTERED): 248 (EXTRA constraints: 248)
- Mapped to oracle (POLICY_LINKED): 7
- Non-normative / discarded (NON_NORMATIVE): 17
- Duplicates (DUPLICATE): 8
- Unresolved (LINK_UNCERTAIN): 3

## Unresolved items

### ORPHAN-M1-0017
- Constraint(s): UNCERTAIN-M1-0001; closest policies: GOV-006
- Evidence: `output/template/docs/capability-selection.md:18-22` — "- persistence / string comparison: equality, uniqueness, ordering, and lookup ⏎   in database queries follow the database and column collation. SQL Server ⏎   default collations compare case-insensitively and accent-sensitively. This is ⏎   a technology default, not an approved product semantic; changing the ⏎   effective collation is a product decision (`CLAUDE.md` § Product Sources)."
- Open question: does declaring the SQL Server collation default (CI/AS) as the persistence default (referenced from CLAUDE.md line 27-28) let implementations rely on it without approval, relaxing GOV-006, or is it documentation only with any material choice still requiring approval?

### ORPHAN-M1-0117
- Constraint(s): UNCERTAIN-M1-0002; closest policies: RUN-021
- Evidence: `output/template/.claude/skills/caching/SKILL.md:86-88` — "TTL with tolerated staleness, tag/group invalidation, versioned keys. Invalidate ⏎ before the mutation is known to have succeeded only when the workflow ⏎ deliberately accepts that behavior."
- Open question: is pre-success invalidation an exception relaxing RUN-021 ('only consistently with successful mutations') or consistent with it because it never makes the cache a source of truth?

### ORPHAN-M1-0172
- Constraint(s): UNCERTAIN-M1-0003; closest policies: GOV-015
- Evidence: `output/template/.claude/skills/git-workflow/SKILL.md:100-103` — "Treat these as high-risk: `git reset --hard`, `git clean`, `git push --force`, ⏎ `git push --force-with-lease`, branch deletion, and rebasing shared history. ⏎ Perform them only when explicitly requested or clearly required by an approved ⏎ workflow, after inspecting what will be lost or rewritten."
- Open question: does 'clearly required by an approved workflow' relax GOV-015's explicit-request condition, or is an approved workflow equivalent to an explicit request?

## Rejected false leads and oracle-linked resolutions

- ORPHAN-M1-0001 [NON_NORMATIVE] `CLAUDE.md:12-13` — '(an empty file in the reusable template is intentional)' only explains the template state; no engineering obligation.
- ORPHAN-M1-0071 [NON_NORMATIVE] `.claude/rules/architecture.md:80-81` — 'When an explicitly approved DDD design contains Aggregate Roots, they are natural repository-boundary candidates' is conditional non-binding guidance.
- ORPHAN-M1-0086 [NON_NORMATIVE] `.claude/skills/api-versioning/SKILL.md:111-112` — 'Consider client-generation behavior' is advisory with no required outcome.
- ORPHAN-M1-0103 [NON_NORMATIVE] `.claude/skills/authentication/SKILL.md:108-109` — 'Middleware generates these responses by default rather than controllers manufacturing them' describes framework default behaviour; no required outcome.
- ORPHAN-M1-0114 [NON_NORMATIVE] `.claude/skills/caching/SKILL.md:105-106` — Applying the output-cache policy via controller/action metadata is Controller technique, no outcome restriction.
- ORPHAN-M1-0130 [NON_NORMATIVE] `.claude/skills/configuration/SKILL.md:196-196` — 'ValidateDataAnnotations() + ValidateOnStart()' examined as a mandated mechanism; it is a recommendation under RUN-022's startup validation default.
- ORPHAN-M1-0135 [NON_NORMATIVE] `.claude/skills/dotnet-testing/SKILL.md:137-139` — Exposing Program via 'public partial class Program' is a technique hint.
- ORPHAN-M1-0174 [NON_NORMATIVE] `.claude/skills/http-api/SKILL.md:217-220` — 'consider an Idempotency-Key header' and its 409 reuse convention are advisory technique without a required outcome.
- ORPHAN-M1-0198 [NON_NORMATIVE] `.claude/skills/logging/references/serilog.md:278-278` — 'Audit trails → AuditTo' is a tooling recommendation, not an adoption requirement.
- ORPHAN-M1-0260 [POLICY_LINKED] `.claude/agents/code-reviewer.md:12-12` — Banner restates that the agent is a thin read-only wrapper and that code-review owns the criteria; captured as WF-010 constraints from the agent body.
- ORPHAN-M1-0261 [DUPLICATE] `.claude/capabilities/architecture/CONTRACT.md:34-37` — Required-facet table is maintainer metadata; the operative obligation (selected modules provide every contract-required facet) is captured from the contract JSON and check-instructions.js.
- ORPHAN-M1-0262 [DUPLICATE] `.claude/capabilities/backend-testing/CONTRACT.md:27-29` — Required-facet table (maintainer metadata); operative conformance obligation captured from the contract JSON and check-instructions.js.
- ORPHAN-M1-0263 [POLICY_LINKED] `.claude/capabilities/frontend/angular/MODULE.md:24-24` — Manifest property 'Playwright, only when E2E coverage is required' is data consumed by checks; the conditional E2E tool policy is captured from the frontend planning facet.
- ORPHAN-M1-0264 [DUPLICATE] `.claude/capabilities/frontend/CONTRACT.md:30-32` — Required-facet table (maintainer metadata); operative conformance obligation captured from the contract JSON and check-instructions.js.
- ORPHAN-M1-0265 [POLICY_LINKED] `.claude/capabilities/persistence/CONTRACT.md:21-24` — Role vocabulary defines persistence-technology types as types that must not leak into the core model or use-case layer and the development seeder as a Development-only empty-database initializer; the rules themselves are captured from architecture/persistence rule files.
- ORPHAN-M1-0266 [DUPLICATE] `.claude/capabilities/persistence/CONTRACT.md:30-33` — Required-facet table (maintainer metadata); operative conformance obligation captured from the contract JSON and check-instructions.js.
- ORPHAN-M1-0267 [POLICY_LINKED] `.claude/capabilities/persistence/ef-core/MODULE.md:36-36` — Manifest seedingMechanism value (internal DbSeeder, Development-only, empty-database-only, no schema creation) is data; the seeding rules are captured from persistence-technology.md.
- ORPHAN-M1-0268 [POLICY_LINKED] `.claude/capabilities/persistence/ef-core/MODULE.md:38-38` — Manifest stringComparison value declares the collation property; the string-semantics policy is captured from capability-selection.md (with its LINK_UNCERTAIN collation-default item).
- ORPHAN-M1-0269 [DUPLICATE] `.claude/hooks/post-tool-use.js:10-16` — Header comment describing effect-based manifest re-validation and routing of unexplained changes; the executable behaviour is captured from the post-tool-use code segments.
- ORPHAN-M1-0270 [DUPLICATE] `.claude/MAP.md:74-74` — Heading asserts knowledge skills are technique only and never sole policy owners; the same placement invariant is captured as an extra from template-maintenance.
- ORPHAN-M1-0271 [DUPLICATE] `.claude/scripts/lib/dependency-commands.js:9-10` — Trailing-comment approval-marker rule is captured with the marker-gate extra.
- ORPHAN-M1-0272 [DUPLICATE] `.claude/scripts/lib/hook-output.js:5-7` — Failure-policy comment: PreToolUse fail-closed behaviour is captured from settings/pre-tool-use; visible non-blocking Post/Stop failure reporting is implementation behaviour.
- ORPHAN-M1-0273 [NON_NORMATIVE] `.claude/skills/api-versioning/SKILL.md:101-103` — Hedged list of changes that commonly justify a new version; it informs API-014 (captured elsewhere) without adding an obligation.
- ORPHAN-M1-0274 [POLICY_LINKED] `.claude/skills/build-fix/SKILL.md:41-46` — Illustrative scope table; 'no application builds without a reason' restates the preceding prohibition on unrelated build systems (WF-007).
- ORPHAN-M1-0275 [NON_NORMATIVE] `.claude/skills/caching/SKILL.md:30-32` — HybridCache is presented as an option and explicitly 'Not mandatory'; no obligation.
- ORPHAN-M1-0276 [NON_NORMATIVE] `.claude/skills/dotnet-testing/SKILL.md:42-43` — Arrange/Act/Assert described as a useful default with optional comments; permissive.
- ORPHAN-M1-0277 [NON_NORMATIVE] `.claude/skills/ef-core/SKILL.md:190-191` — Permissive description of when FindAsync fits; no restriction.
- ORPHAN-M1-0278 [NON_NORMATIVE] `.claude/skills/ef-core/SKILL.md:232-233` — Keyset pagination is advisory ('when justified'); no obligation beyond RUN-performance policies captured elsewhere.
- ORPHAN-M1-0279 [NON_NORMATIVE] `.claude/skills/project-structure/SKILL.md:15-15` — Context-loading guidance for the skill's own references; affects what Claude reads, not product outcomes.
- ORPHAN-M1-0280 [POLICY_LINKED] `.claude/skills/security-scan/references/scan-layers.md:303-308` — Severity examples illustrate the contextual-severity rule (WF-020).
- ORPHAN-M1-0281 [NON_NORMATIVE] `.claude/skills/security-scan/SKILL.md:87-97` — Change-to-priority-area table is advisory investigation guidance (EXC-015 context); the binding scope rule is lines 83-85.
- ORPHAN-M1-0282 [NON_NORMATIVE] `docs/capability-selection.md:26-30` — Loading information (contracts and manifests are maintainer metadata read only during maintenance); no product obligation.

## Reverse checks conducted

- Full reverse annotation: every non-blank line of all 80 active files was assigned to exactly one coverage range during batch annotation (21 queue batches); each normative range cites its constraints and each non-normative/implementation/duplicate range carries a reason.
- Keyword sweep: `stagea.py sweep` listed 275 normative-keyword hits (must, never, do not, only, default, required, avoid, prefer, should, error, …) inside 173 NON_NORMATIVE / IMPLEMENTATION / DUPLICATE ranges. Each hit was reviewed. Most are code tokens in examples or scripts (`throw`, `required`, `default:`, `process.exit`, `require(...)`), headings, banners carrying ownership metadata, or pointers.
- Borderline hits were recorded as explicit orphan rows (Z_SWEEP): capability-contract facet tables and manifest property values (DUPLICATE/POLICY_LINKED to the enforced or rule-owned constraint), MAP headings, permissive skill wording (HybridCache 'Not mandatory', FindAsync, keyset pagination, AAA), loading guidance, illustrative scope tables, severity examples, hook/script header comments.
- Check-by-reference lists and decision tables were re-verified item by item against owner clauses. Two lists contained items without an owner clause and were reclassified from DUPLICATE to MIXED with new EXTRA constraints: `aspnet-error-handling` (Minimal API endpoint filters for validation in a Controller-based project) and `authentication` (scattered role/permission strings traced to the skill's own policy-constant/role extras). The Swagger review list was annotated as MIXED from the start for the same reason.
- Forward check: each of the 196 policies was searched across all 80 files and cross-checked against the constraint ledger; all 196 have at least one oracle-linked constraint. Modality differences, enforcement notes and open related items are recorded in `policies.jsonl` search notes.
- Executable sources (hooks, scripts, settings.json, manifests JSON) were read as code; enforced behaviour (gates, markers, fail-closed policy, blocking findings, deny lists, floating-version errors) was registered as constraints; argument parsing and helper code are IMPLEMENTATION.

## Limitation

A complete line disposition plus this sweep is not proof of semantic exhaustiveness.
