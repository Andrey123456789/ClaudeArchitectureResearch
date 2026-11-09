# Orphan sweep report — candidate K0

Every EXTRA and LINK_UNCERTAIN constraint has at least one orphan row; additional rows record clauses that were examined as possible extras and resolved as oracle-linked, duplicate or non-normative. Disproven hypotheses are kept, not deleted.

## Counts

- Orphan candidates identified: 270
- EXTRA registered (EXTRA_REGISTERED): 243 (EXTRA constraints: 243)
- Mapped to oracle (POLICY_LINKED): 5
- Non-normative / discarded (NON_NORMATIVE): 16
- Duplicates (DUPLICATE): 5
- Unresolved (LINK_UNCERTAIN): 1

## Unresolved items

### ORPHAN-K0-0160
- Constraint(s): UNCERTAIN-K0-0001; closest policies: GOV-015
- Evidence: `output/template/.claude/skills/git-workflow/SKILL.md:73-73` — "`git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion and rebasing shared history are high-risk: run them only when explicitly requested or required by an approved workflow, and inspect what will be lost or rewritten first."
- Open question: GOV-015 permits repository-changing Git operations only when explicitly requested; whether 'required by an approved workflow' widens that condition or only describes an explicitly requested workflow cannot be decided from the text.

## Rejected false leads and oracle-linked resolutions

- ORPHAN-K0-0245 [DUPLICATE] `.claude/hooks/hook.cjs:2-9` — Header comment describing exec-form launch, per-worktree state, fail-closed pre-tool-use and non-critical failure exits implemented in the code segments; 'messages do not restate policy' is a maintenance note.
- ORPHAN-K0-0246 [NON_NORMATIVE] `.claude/MAP.md:193-193` — Descriptive limitation of the command classifier (indirect changes not routed; checked afterwards).
- ORPHAN-K0-0247 [DUPLICATE] `.claude/skills/angular/SKILL.md:103-103` — Pointer to the error-contract rule plus a descriptive 'common shape' (shared interceptor/utility mapping ProblemDetails); the owning rule is captured in angular.md.
- ORPHAN-K0-0248 [NON_NORMATIVE] `.claude/skills/aspnet-error-handling/SKILL.md:16-49` — Example handler returns status 499 and skips error logging for aborted requests; the 499 code is example technique, the operative rule (cancellation is not a server failure) is API-021 in error-handling.md.
- ORPHAN-K0-0249 [NON_NORMATIVE] `.claude/skills/aspnet-error-handling/SKILL.md:104-104` — Descriptive contents of a useful error contract ('may contain'); no obligation stated.
- ORPHAN-K0-0250 [NON_NORMATIVE] `.claude/skills/aspnet-error-handling/SKILL.md:108-108` — Descriptive statement of model-binding handling and of what FluentValidation expresses.
- ORPHAN-K0-0251 [POLICY_LINKED] `.claude/skills/build-fix/SKILL.md:23-28` — Scope table rows ('documentation-only failure -> no application builds without a reason') restate the affected-scope rule.
- ORPHAN-K0-0252 [NON_NORMATIVE] `.claude/skills/caching/SKILL.md:22-22` — HybridCache described as a strong option, explicitly not mandatory.
- ORPHAN-K0-0253 [DUPLICATE] `.claude/skills/custom-settings/SKILL.md:10-10` — Pointer summarizing CLAUDE.md § Product sources ('what it must not contain', conflicts, approval); the rules are captured in CLAUDE.md.
- ORPHAN-K0-0254 [NON_NORMATIVE] `.claude/skills/ef-core/SKILL.md:167-175` — FindAsync vs LINQ is a technique choice without outcome restriction.
- ORPHAN-K0-0255 [NON_NORMATIVE] `.claude/skills/ef-core/SKILL.md:202-202` — Hedged suggestion ('consider keyset pagination'); no obligation.
- ORPHAN-K0-0256 [POLICY_LINKED] `.claude/skills/ef-core/SKILL.md:271-315` — Seeder example returns when the anchor entity exists, illustrating PST-006.
- ORPHAN-K0-0257 [NON_NORMATIVE] `.claude/skills/health-check/SKILL.md:26-26` — Descriptive definition of liveness with a pointer to the owning rule.
- ORPHAN-K0-0258 [POLICY_LINKED] `.claude/skills/logging/SKILL.md:67-73` — Avoid/prefer example (credentials vs technical identifier) illustrates SEC-010.
- ORPHAN-K0-0259 [POLICY_LINKED] `.claude/skills/logging/SKILL.md:75-75` — Rationale for logging specific properties instead of whole objects restates RUN-014.
- ORPHAN-K0-0260 [DUPLICATE] `.claude/skills/modern-csharp/SKILL.md:59-59` — Hedged readability note on deeply nested patterns; the avoidance item is registered from the common-mistakes list.
- ORPHAN-K0-0261 [NON_NORMATIVE] `.claude/skills/project-structure/SKILL.md:12-16` — Loading guidance for private references ('not all of them by default'); no product or engineering obligation.
- ORPHAN-K0-0262 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:17-23` — Investigation prompts for npm audit findings (EXC-015 context).
- ORPHAN-K0-0263 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:37-44` — Preferred configuration pattern example and investigation prompts (debug flags, certificate bypass, verbose errors, committed .env); owning rules SEC-001/SEC-007/API-008 are captured in the standards.
- ORPHAN-K0-0264 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:67-75` — SSRF/XSS investigation prompts with descriptive non-findings; no rule stated.
- ORPHAN-K0-0265 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:135-145` — Logging and error-response investigation prompts; owning rules SEC-010/API-008 are captured in the standards.
- ORPHAN-K0-0266 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:157-173` — Fail-open and swallowed-exception investigation prompts; the operative statement at 175 is captured (SEC-013).
- ORPHAN-K0-0267 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:185-193` — Startup-fallback and error-exposure investigation prompts; owning rules SEC-014/API-007 are captured.
- ORPHAN-K0-0268 [DUPLICATE] `.claude/skills/security-scan/SKILL.md:84-130` — Report template including the limitation text and layer status table restates the captured reporting rules.
- ORPHAN-K0-0269 [NON_NORMATIVE] `.claude/skills/template-maintenance/SKILL.md:54-56` — Sample hook payload command for maintainers; example only (never executed during extraction).
- ORPHAN-K0-0270 [POLICY_LINKED] `CLAUDE.md:58-58` — Routing instruction 'run the matching workflow'; the operative routing rows (development-workflow, verify) are captured, the remaining rows only route to workflows that own their obligations.

## Reverse checks conducted

- Full reverse annotation: every non-blank line of all 63 active files (13 queue batches, 5183 non-blank lines) was assigned to exactly one coverage range; normative ranges cite their constraints and every NON_NORMATIVE / IMPLEMENTATION / DUPLICATE range carries a specific reason. `hook.cjs` was reviewed branch by branch (fail-closed input/exception path, command tokenizer and classifiers including nested shell launchers, marker-based deny paths, Git 'ask' path, worktree snapshot/HEAD-transition logic, product/manifest/instruction reactions, Stop reminder conditions and fingerprint de-duplication); `check-dependencies.cjs` and `check-instructions.cjs` were reviewed check by check (error vs notice branches).
- Keyword sweep: `stagea.py sweep` listed 234 normative-keyword hits inside 124 NON_NORMATIVE / IMPLEMENTATION / DUPLICATE ranges. Each hit was reviewed; most are code tokens (`throw`, `catch`, `required`, `default`, exit codes), ownership/loading banners, frontmatter descriptions, headings, table headers or pointers.
- Borderline hits and examined hypotheses were recorded as explicit orphan rows (Z_SWEEP): the CLAUDE.md routing sentence, the hook header comment, the 499 status in an error-handling example, descriptive error-contract and validation statements, scope-table rows in build-fix, the custom-settings pointer, the seeder anchor-entity example, logging avoid/prefer examples, hedged notes (HybridCache, keyset pagination, nested patterns), private-reference loading guidance, the security-scan report template, investigation prompts in the scan-layers reference, the maintainer sample hook payload and the MAP classifier limitation.
- Check-by-reference lists, decision guides and common-mistakes lists were verified item by item against owner clauses while annotating; lists containing items without an owner clause were annotated MIXED with the item registered as EXTRA.
- Forward check: each of the 196 policies was searched across all 63 files and cross-checked against the constraint ledger; all 196 have at least one oracle-linked constraint. Modality caveats, enforcement notes and the open related item are recorded in `policies.jsonl` search notes.

## Limitation

A complete line disposition plus this sweep is not proof of semantic exhaustiveness.
