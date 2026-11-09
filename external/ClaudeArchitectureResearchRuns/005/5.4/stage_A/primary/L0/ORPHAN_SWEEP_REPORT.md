# Orphan sweep report — candidate L0

Every EXTRA and LINK_UNCERTAIN constraint has at least one orphan row; additional rows record clauses that were examined as possible extras and resolved as oracle-linked, duplicate or non-normative. Disproven hypotheses are kept, not deleted.

## Counts

- Orphan candidates identified: 235
- EXTRA registered (EXTRA_REGISTERED): 208 (EXTRA constraints: 208)
- Mapped to oracle (POLICY_LINKED): 11
- Non-normative / discarded (NON_NORMATIVE): 10
- Duplicates (DUPLICATE): 5
- Unresolved (LINK_UNCERTAIN): 1

## Unresolved items

### ORPHAN-L0-0113
- Constraint(s): UNCERTAIN-L0-0001; closest policies: GOV-015
- Evidence: `output/template/.claude/skills/git-workflow/SKILL.md:45-45` — "`git reset --hard`, `git clean`, `git push --force`, `git push --force-with-lease`, branch deletion, and rebasing shared history are high-risk: perform them only when explicitly requested or clearly required by an approved workflow, and inspect what will be lost or rewritten first."
- Open question: GOV-015 permits repository-changing Git operations only when explicitly requested; whether 'clearly required by an approved workflow' widens that condition (a relaxation) or merely describes an explicitly requested workflow cannot be decided from the text.

## Rejected false leads and oracle-linked resolutions

- ORPHAN-L0-0210 [DUPLICATE] `.claude/hooks/claude-hook.mjs:9-13` — Header comment states exit-code semantics and the fail-closed pre-bash policy implemented at 46-61 and in settings.json.
- ORPHAN-L0-0211 [POLICY_LINKED] `.claude/INSTRUCTION_MAP.md:22-22` — Map loading description repeats that workflows read the rules they depend on because path rules may not have fired.
- ORPHAN-L0-0212 [DUPLICATE] `.claude/INSTRUCTION_MAP.md:96-100` — Enforcement-asset rows describe the hook/checker behaviour; each behaviour is captured from settings.json, claude-hook.mjs, manifest-checks.mjs and check-instructions.mjs.
- ORPHAN-L0-0213 [DUPLICATE] `.claude/INSTRUCTION_MAP.md:102-102` — Hook runtime paragraph (visible failure, fail-closed PreToolUse guard, foreign repositories not checked) is captured from claude-hook.mjs and settings.json.
- ORPHAN-L0-0214 [DUPLICATE] `.claude/rules/1-architecture/overview.md:36-41` — Decision-summary list of not-adopted-by-default patterns; each item is owned and captured at its owner rule (backend-layers, outcomes, persistence-boundary, CLAUDE.md Reserved list).
- ORPHAN-L0-0215 [POLICY_LINKED] `.claude/rules/3-project/decisions.md:30-30` — Heading 'approved, not installed by default' restates that approved/conditional technologies are not installed by default (DEP-001).
- ORPHAN-L0-0216 [NON_NORMATIVE] `.claude/skills/aspnet-error-handling/SKILL.md:17-50` — Example handler returns status 499 and skips error logging for client-aborted requests; the 499 code is example technique, not stated as a rule; the operative rule (client cancellation is not a server failure) is API-021 in runtime-principles.md.
- ORPHAN-L0-0217 [NON_NORMATIVE] `.claude/skills/aspnet-error-handling/SKILL.md:93-93` — Permissive list of what a ProblemDetails contract 'may contain'; no obligation.
- ORPHAN-L0-0218 [POLICY_LINKED] `.claude/skills/configuration/SKILL.md:107-116` — Anti-example comments ('stringly typed, scattered configuration access', 'misconfiguration discovered only at runtime') restate RUN-022.
- ORPHAN-L0-0219 [POLICY_LINKED] `.claude/skills/dependency-injection/SKILL.md:67-83` — Code comment 'Only if Scrutor is already used by the project' conditions the example on an existing dependency; captured by the no-Scrutor-for-one-decoration rule.
- ORPHAN-L0-0220 [NON_NORMATIVE] `.claude/skills/dotnet-testing/SKILL.md:34-34` — Arrange/Act/Assert described as a useful structure with optional comments; permissive.
- ORPHAN-L0-0221 [POLICY_LINKED] `.claude/skills/ef-core/SKILL.md:66-87` — Code comment 'stages only; no SaveChanges here' illustrates the Unit of Work commit boundary (ARC-016).
- ORPHAN-L0-0222 [NON_NORMATIVE] `.claude/skills/ef-core/SKILL.md:128-128` — Keyset pagination is advisory ('consider'); no obligation.
- ORPHAN-L0-0223 [NON_NORMATIVE] `.claude/skills/ef-core/SKILL.md:225-225` — Idempotent scripts/bundles described as 'often preferable'; hedged advisory; the binding production-migration rule (WF-019) is captured from delivery-pipeline.
- ORPHAN-L0-0224 [POLICY_LINKED] `.claude/skills/http-api/SKILL.md:17-27` — Code comment '204 — never with a body' restates API-003 (captured at line 31).
- ORPHAN-L0-0225 [DUPLICATE] `.claude/skills/http-api/SKILL.md:64-70` — Flow text 'If-Match required but absent → 428' duplicates the 428 extra captured from the status table.
- ORPHAN-L0-0226 [NON_NORMATIVE] `.claude/skills/logging/references/serilog.md:149-149` — Permissive note that audit trails 'can use' AuditTo; no obligation.
- ORPHAN-L0-0227 [POLICY_LINKED] `.claude/skills/logging/SKILL.md:16-24` — Anti-example comment ('interpolation turns structured values into opaque text') restates RUN-013 from logging.md.
- ORPHAN-L0-0228 [POLICY_LINKED] `.claude/skills/project-structure/references/backend-layout.md:46-59` — Tree comment '(+ optional Infrastructure-only base)' restates that a generic base may exist only in Infrastructure (ARC-015).
- ORPHAN-L0-0229 [POLICY_LINKED] `.claude/skills/security-scan/references/scan-layers.md:5-5` — 'Investigation prompts, not automatic vulnerability declarations' is the WF-020 contextual-severity principle captured at lines 61/71.
- ORPHAN-L0-0230 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:20-20` — Investigation prompts (EXC-015 context) without an added requirement beyond SEC-007/API-008/SEC-001 owners.
- ORPHAN-L0-0231 [NON_NORMATIVE] `.claude/skills/security-scan/references/scan-layers.md:52-52` — Investigation prompt for public error contents; the owning invariant API-008 is captured from security-principles.md.
- ORPHAN-L0-0232 [POLICY_LINKED] `.claude/skills/security-scan/references/scan-layers.md:73-76` — Severity examples illustrate WF-020.
- ORPHAN-L0-0233 [NON_NORMATIVE] `.claude/skills/security-scan/SKILL.md:28-38` — Change-to-priority-layer table is advisory investigation guidance (EXC-015 context); the binding scope rule is line 26.
- ORPHAN-L0-0234 [NON_NORMATIVE] `.editorconfig:71-71` — Comment states private-field naming is not enforced and follows the repository convention; no added rule.
- ORPHAN-L0-0235 [POLICY_LINKED] `CLAUDE.md:90-90` — Loading description 'Workflows explicitly read the rule files they depend on' restates the owner-reading obligation captured from development-workflow and the other workflows.

## Reverse checks conducted

- Full reverse annotation: every non-blank line of all 71 active files (12 queue batches) was assigned to exactly one coverage range; normative ranges cite their constraints and every NON_NORMATIVE / IMPLEMENTATION / DUPLICATE range carries a specific reason. Hook and checker scripts were reviewed branch by branch (pre-bash block paths, fail-closed `unavailable()` path, post-bash/post-edit reporting paths, Stop reminder conditions and de-duplication, checker error vs warning branches).
- Keyword sweep: `stagea.py sweep` listed 160 normative-keyword hits inside 115 NON_NORMATIVE / IMPLEMENTATION / DUPLICATE ranges. Each hit was reviewed; most are code tokens (`throw`, `catch`, `required`, `default`, `stop`), banners with ownership metadata, headings or pointers.
- Borderline hits and examined hypotheses were recorded as explicit orphan rows (Z_SWEEP): code comments carrying rules (UoW staging, 204 without body, Scrutor condition, logging/configuration anti-examples), map/summary rows (DUPLICATE to the enforcing constraint), hedged or permissive skill wording (keyset pagination, idempotent scripts, AAA, AuditTo, ProblemDetails contents), the 499 status in an error-handling example, investigation prompts and severity examples in the security-scan reference.
- Check-by-reference lists and decision tables were verified item by item against owner clauses while annotating; lists containing items without an owner clause were annotated MIXED with the item registered as EXTRA (aspnet-error-handling endpoint-filter rule, swagger anti-patterns, caching/health-check/http-client/dotnet-testing anti-patterns).
- Forward check: each of the 196 policies was searched across all 71 files and cross-checked against the constraint ledger; all 196 have at least one oracle-linked constraint. Modality differences, enforcement notes and the open related item are recorded in `policies.jsonl` search notes.

## Limitation

A complete line disposition plus this sweep is not proof of semantic exhaustiveness.
