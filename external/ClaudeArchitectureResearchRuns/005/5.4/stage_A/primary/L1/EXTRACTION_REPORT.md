# Stage A primary extraction report — candidate L1

Extractor: Claude (primary). Scope: `inputs/L1/output/template/**` only; provenance documents were not treated as normative surfaces. All numbers below are computed from the ledgers in this directory.

## Source inventory

- Active template files: 86 (text: 86, binary/non-UTF-8: 0).
- Non-blank lines in text files: 4279.
- Queue batches: 10; batches checked complete: 10.
- Coverage ranges: 1558 — DUPLICATE=22, EXTRA=158, IMPLEMENTATION=162, MIXED=122, NON_NORMATIVE=624, ORACLE_LINKED=470.
- Unclassified non-blank lines: 0 (every non-blank line is in exactly one range; see validator output).

## 196-policy forward mapping

- Policies in policies.jsonl: 196 (194 inventory + 2 shared invariants).
- Status counts: MATCHED=196, PARTIAL=0, NOT_EVIDENCED=0, UNCERTAIN=0.
- Policies whose search notes carry a modality caveat, open related item or enforcement note: GOV-015, ARC-001, RUN-010, RUN-021, DEP-003, DEP-004, DEP-025, WF-010, WF-019.

## Constraints

- Atomic constraints: 852 — ORACLE_LINKED=617, EXTRA=233, LINK_UNCERTAIN=2.
- EXTRA constraints by first-evidence area:
  - .claude/capabilities: 26
  - .claude/skills/httpclient-factory: 14
  - .claude/skills/http-api: 11
  - .claude/skills/security-scan: 11
  - .claude/scripts/check-instructions.mjs: 10
  - .claude/skills/modern-csharp: 10
  - .claude/skills/docker: 9
  - .claude/INSTRUCTION_MAP.md: 8
  - .claude/skills/ef-core: 8
  - .claude/skills/git-workflow: 8
  - CLAUDE.md: 7
  - .claude/skills/health-check: 7
  - .claude/skills/swagger: 7
  - .claude/skills/template-maintenance: 7
  - .claude/skills/caching: 6
  - .claude/skills/dotnet-testing: 6
  - .claude/skills/logging: 6
  - .claude/skills/project-structure: 6
  - .claude/skills/angular: 5
  - .claude/skills/authentication: 5
  - .claude/skills/ci-cd: 5
  - .claude/skills/dependency-injection: 5
  - .editorconfig: 5
  - .claude/skills/add-dependency: 4
  - .claude/skills/architecture-decision: 4
  - .claude/hooks/pre-shell-command.mjs: 4
  - .claude/hooks/post-change-checks.mjs: 3
  - .claude/skills/aspnet-error-handling: 3
  - .claude/skills/code-review: 3
  - .claude/skills/custom-settings: 3
  - .claude/skills/verify: 3
  - .claude/rules/2-technology: 2
  - .claude/skills/api-versioning: 2
  - .claude/skills/development-workflow: 2
  - .claude/hooks/manifest-policy.json: 2
  - .claude/hooks/stop-cochange.mjs: 2
  - Directory.Build.props: 1
  - .claude/rules/3-project: 1
  - .claude/rules/1-architecture: 1
  - .claude/skills/configuration: 1
- Full EXTRA and LINK_UNCERTAIN list with citations: `EXTRA_CONSTRAINTS.md`.

## Orphan ledger

- ORPHAN_CANDIDATES.jsonl rows: 258 — DUPLICATE=7, EXTRA_REGISTERED=233, LINK_UNCERTAIN=2, NON_NORMATIVE=8, POLICY_LINKED=8.
- Details and every unresolved item: `ORPHAN_SWEEP_REPORT.md`.

## File types and limitations

- No binary or non-UTF-8 files; every file was decoded and line-partitioned.
- Structural validation proves accounting, not semantic exhaustiveness; an independent blind sweep is required to challenge the inventory.
- Classification of knowledge-skill imperatives as EXTRA vs non-normative technique involves judgement; each borderline call is recorded in the orphan ledger with its reason.

## Candidate-specific notes (L1)

### Instruction architecture observed
- Stability-level rules under `.claude/rules/{0-core,1-architecture,2-technology,3-project}/`, each with a one-line `Level · Owns · Scope · Loading` header and `paths` frontmatter where path-scoped. Always-loaded surface: `CLAUDE.md` plus three imports (`1-architecture/frame/adopted-style.md`, `3-project/decisions.md`, `3-project/frontend-stack.md`). `CUSTOM_SETTINGS.md` (approved tunable values) and an empty `SPECIFICATION.md` sit at the template root.
- Capability slots under `.claude/capabilities/<slot>/` (architecture, backend-testing, frontend, persistence): each slot has a `CONTRACT.md` (required facets, binds, replacement procedure) and one selected module with `MODULE.md`, command/workflow files and machine-readable `enforcement.json`/`check.json` consumed by the hooks and checkers. `3-project/decisions.md` records the selection and facet resolution.
- Workflow and knowledge skills under `.claude/skills/` (some with private `references/`); one agent (`code-reviewer`); maintainer map `.claude/INSTRUCTION_MAP.md` (not auto-loaded).
- Executable enforcement (read as code, never executed): `settings.json` registers exec-form `node` hooks — `pre-shell-command.mjs` (PreToolUse Bash|PowerShell, `onFailure: block`, fail-closed), `post-change-checks.mjs` (PostToolUse edits and shell, PostToolUseFailure shell) and `stop-cochange.mjs` (Stop). pre-shell returns 'ask' for peer-bypass flags and project-reference commands and denies dependency commands once (identical retry within 30 minutes allowed); post-change validates the actual manifest state (CPM, VersionOverride, floating/prerelease, deny/approval lists from `manifest-policy.json`, MSBuild-property versions) and runs `scripts/check-architecture.mjs` after project changes; Stop issues a once-per-state co-change reminder. `scripts/check-instructions.mjs` is a manual instruction-system checker.
- `CLAUDE.md` uses must/never/default/prefer/avoid/Reserved wording; modalities were assigned from the clause wording.

### Classification conventions applied
- Restatements of oracle policies in rules, capability files and skills are ORACLE_LINKED; new outcome-restricting imperatives, including in knowledge skills, private references, capability contracts/modules, hook/checker code and configuration assets (`.editorconfig`, `Directory.Build.props`, `Directory.Packages.props`, `.gitignore`), are EXTRA with the closest policy IDs; examples, permissive wording and investigation prompts (EXC-015 context) are NON_NORMATIVE with reasons; decision tables and check-by-reference lists are DUPLICATE unless an item has no owner clause (then MIXED with the item as EXTRA).
- Instruction-system and capability-system rules (level placement, ownership headers, map maintenance, slot/module conformance, facet resolution, checker invariants) are recorded as EXTRA with a repo/meta scope note; they constrain maintenance of the instruction system rather than product code.
- Hook and checker behaviour that enforces an oracle policy is ORACLE_LINKED with ENFORCED/ENFORCED_ADVISORY modality; enforcement mechanisms without an oracle counterpart (fail-closed gate, 'ask' decisions, deny-once routing, package deny/approval lists, Stop reminder) are EXTRA.

### Open items
- Two LINK_UNCERTAIN constraints: pre-mutation cache invalidation as a deliberate choice (caching) vs RUN-021; high-risk Git operations "required by an approved workflow" (git-workflow) vs GOV-015. Listed in `ORPHAN_SWEEP_REPORT.md`; not resolved at Stage A.

## Check results

```text
# L1 validator results
$ py _STAGE_A_KIT/05_WORK_QUEUE_AND_PROGRESS.py check --root . --candidate L1
L1: 10/10 claimed complete batches; 86 file rows, 1558 coverage spans, 852 constraints
PASS: claimed completed batches have structural coverage (not semantic proof).
exit=0
$ py _STAGE_A_KIT/03_VALIDATE_STAGE_A.py --root . --candidate L1
{
  "candidate": "L1",
  "template_files": 86,
  "text_files": 86,
  "nonblank_lines": 4279,
  "unclassified_nonblank_lines": 0,
  "oracle_policies": 196,
  "constraints": 852,
  "extra_constraints": 233,
  "uncertain_constraints": 2,
  "coverage_segments": 1558,
  "error_count": 0
}
PASS (STRUCTURE ONLY): L1. This is not semantic completeness proof.
exit=0
$ py _STAGE_A_KIT/07_VALIDATE_ORPHANS.py --root . --candidate L1
{
  "candidate": "L1",
  "orphan_candidates": 258,
  "resolution_counts": {
    "DUPLICATE": 7,
    "EXTRA_REGISTERED": 233,
    "LINK_UNCERTAIN": 2,
    "NON_NORMATIVE": 8,
    "POLICY_LINKED": 8
  },
  "extra_constraints": 233,
  "uncertain_constraints": 2,
  "error_count": 0
}
PASS (STRUCTURE ONLY): L1. NOT a semantic exhaustion guarantee.
exit=0
```
