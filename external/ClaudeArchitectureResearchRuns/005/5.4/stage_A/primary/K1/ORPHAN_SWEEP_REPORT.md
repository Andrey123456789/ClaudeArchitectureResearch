# Orphan sweep report — candidate K1

Every EXTRA and LINK_UNCERTAIN constraint has at least one orphan row; additional rows record clauses that were examined as possible extras and resolved as oracle-linked, duplicate or non-normative. Disproven hypotheses are kept, not deleted.

## Counts

- Orphan candidates identified: 297
- EXTRA registered (EXTRA_REGISTERED): 274 (EXTRA constraints: 274)
- Mapped to oracle (POLICY_LINKED): 5
- Non-normative / discarded (NON_NORMATIVE): 12
- Duplicates (DUPLICATE): 4
- Unresolved (LINK_UNCERTAIN): 2

## Unresolved items

### ORPHAN-K1-0097
- Constraint(s): UNCERTAIN-K1-0001; closest policies: RUN-021
- Evidence: `output/template/.claude/skills/caching/SKILL.md:56-56` — "Remove the affected key after a successful mutation; short TTL with tolerated staleness; tag/group invalidation; versioned keys. Invalidate before the mutation succeeds only when the workflow deliberately accepts that behavior."
- Open question: RUN-021 requires invalidation only consistent with successful underlying mutations; whether a deliberately accepted pre-mutation invalidation is a permitted exception or a relaxation that contradicts RUN-021 cannot be decided from the text.

### ORPHAN-K1-0163
- Constraint(s): UNCERTAIN-K1-0002; closest policies: GOV-015
- Evidence: `output/template/.claude/skills/git-workflow/SKILL.md:19-19` — "- Treat `git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion, and rebasing shared history as high-risk: perform them only when explicitly requested or clearly required by an approved workflow, after inspecting what will be lost or rewritten."
- Open question: GOV-015 permits repository-changing Git operations only when explicitly requested; whether 'clearly required by an approved workflow' widens that condition or only describes an explicitly requested workflow cannot be decided from the text.

## Rejected false leads and oracle-linked resolutions

- ORPHAN-K1-0277 [DUPLICATE] `.claude/hooks/dispatch.cjs:5-12` — Header comment on launcher vs active root and fail-closed PreToolUse / advisory Post-Stop exit codes, implemented in the code segments.
- ORPHAN-K1-0278 [DUPLICATE] `.claude/MAP.md:141-141` — Restates the register's static-composition rule.
- ORPHAN-K1-0279 [DUPLICATE] `.claude/scripts/check-instructions.cjs:45-45` — Table comment 'the dependency/reference guard is the only fail-closed hook' restates the hook-configuration invariant checked in checkSettings.
- ORPHAN-K1-0280 [NON_NORMATIVE] `.claude/skills/angular/SKILL.md:129-129` — Security investigation prompts (sanitizer bypasses, direct DOM access) and a descriptive XSRF note; owning rules SEC-011/SEC-005 are captured in the standards.
- ORPHAN-K1-0281 [NON_NORMATIVE] `.claude/skills/aspnet-error-handling/SKILL.md:19-52` — Example handler returns status 499 and skips error logging for aborted requests; the 499 code is example technique, the operative rule (cancellation is not a server failure) is API-021 in api.md.
- ORPHAN-K1-0282 [NON_NORMATIVE] `.claude/skills/aspnet-error-handling/SKILL.md:94-94` — Descriptive statement of model-binding handling and what FluentValidation expresses.
- ORPHAN-K1-0283 [POLICY_LINKED] `.claude/skills/ci-cd/SKILL.md:17-22` — Example comment 'only when the project adopted formatting as an enforced gate' restates the adopted-gates rule owned by delivery-change.
- ORPHAN-K1-0284 [NON_NORMATIVE] `.claude/skills/configuration/SKILL.md:57-60` — Descriptive list of options interfaces and named options (technique choice).
- ORPHAN-K1-0285 [POLICY_LINKED] `.claude/skills/configuration/SKILL.md:62-74` — Avoid/prefer example contrasting string lookups with typed options restates RUN-022.
- ORPHAN-K1-0286 [NON_NORMATIVE] `.claude/skills/ef-core/SKILL.md:107-107` — FindAsync vs LINQ is a technique choice without outcome restriction.
- ORPHAN-K1-0287 [POLICY_LINKED] `.claude/skills/ef-core/SKILL.md:163-199` — Seeder example returns when the anchor entity exists (PST-006) and seeds only in Development (PST-004).
- ORPHAN-K1-0288 [NON_NORMATIVE] `.claude/skills/health-check/SKILL.md:25-25` — Descriptive definition of liveness ('usually checks no dependencies'); the operative rules are captured at lines 31/46.
- ORPHAN-K1-0289 [POLICY_LINKED] `.claude/skills/logging/SKILL.md:17-20` — Example comment 'avoid: opaque text' restates structured-template logging (RUN-013).
- ORPHAN-K1-0290 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:19-29` — npm audit and secret-indicator investigation prompts (EXC-015 context).
- ORPHAN-K1-0291 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:33-49` — Preferred configuration pattern, further investigation prompts and SQL injection anti-example; owning rules SEC-001/SEC-007/API-008/SEC-004 are captured.
- ORPHAN-K1-0292 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:61-69` — SSRF/XSS investigation prompts with descriptive non-findings; no rule stated.
- ORPHAN-K1-0293 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:131-133` — Error-response investigation prompt; API-008 is captured in api.md.
- ORPHAN-K1-0294 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:165-167` — Centralized-error investigation prompt; API-007/API-008 are captured in api.md.
- ORPHAN-K1-0295 [NON_NORMATIVE] `.claude/skills/security-scan/SKILL.md:27-27` — Instruction to apply owning standards and knowledge rather than duplicating them (routing; no product obligation).
- ORPHAN-K1-0296 [DUPLICATE] `.claude/skills/security-scan/SKILL.md:88-128` — Report template including the limitation text and layer status table restates the captured reporting rules.
- ORPHAN-K1-0297 [POLICY_LINKED] `CLAUDE.md:62-62` — Routing instruction 'run it instead of improvising'; the operative rows (development-workflow, verify) are captured; the other rows route to workflows that own their obligations.

## Reverse checks conducted

- Full reverse annotation: every non-blank line of all 87 active files (13 queue batches, 5514 non-blank lines) was assigned to exactly one coverage range; normative ranges cite their constraints and every NON_NORMATIVE / IMPLEMENTATION / DUPLICATE range carries a specific reason. `dispatch.cjs`, `classify-command.cjs`, `actual-state.cjs`, `check-cochange.cjs`, `check-manifests.cjs`, the four facet checks and `check-instructions.cjs` were reviewed branch by branch (fail-closed input/event-mismatch path, exact-version/peer-bypass/removal/reference/unclassifiable findings, approval-record matching, HEAD-relative reference-graph findings, change attribution, once-per-content-state reminders, error vs warning severities, capability/manifest/binding/leak checks).
- Keyword sweep: `stagea.py sweep` listed 246 normative-keyword hits inside 132 NON_NORMATIVE / IMPLEMENTATION / DUPLICATE ranges. Each hit was reviewed; most are code tokens (`throw`, `required`, `default`, exit codes), capability/loading banners, frontmatter descriptions, headings, table headers ('An implementation must provide', 'Default'), inventory rows or pointers.
- Borderline hits and examined hypotheses were recorded as explicit orphan rows (Z_SWEEP): the CLAUDE.md routing sentence, the dispatcher header comment, the checker's fail-closed table comment, the 499 status in an error-handling example, descriptive validation and liveness statements, the angular security prompts, code comments carrying rules (ci-cd format gate, configuration avoid/prefer, logging interpolation), the seeder anchor-entity example, the FindAsync technique note, the security-scan routing line and report template, investigation prompts in the scan-layers reference and the MAP static-composition sentence.
- Check-by-reference lists, decision guides, anti-pattern lists, MAP inventory rows and module coverage tables were verified item by item against owner clauses while annotating; lists containing items without an owner clause were annotated MIXED with the item registered as EXTRA.
- Forward check: each of the 196 policies was searched across all 87 files and cross-checked against the constraint ledger; all 196 have at least one oracle-linked constraint. Modality caveats, enforcement notes and the two open related items are recorded in `policies.jsonl` search notes.

## Limitation

A complete line disposition plus this sweep is not proof of semantic exhaustiveness.
