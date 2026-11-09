# Stage A primary extraction report — candidate L0

Extractor: Claude (primary). Scope: `inputs/L0/output/template/**` only; provenance documents were not treated as normative surfaces. All numbers below are computed from the ledgers in this directory.

## Source inventory

- Active template files: 71 (text: 71, binary/non-UTF-8: 0).
- Non-blank lines in text files: 4621.
- Queue batches: 12; batches checked complete: 12.
- Coverage ranges: 1605 — DUPLICATE=21, EXTRA=145, IMPLEMENTATION=145, MIXED=112, NON_NORMATIVE=706, ORACLE_LINKED=476.
- Unclassified non-blank lines: 0 (every non-blank line is in exactly one range; see validator output).

## 196-policy forward mapping

- Policies in policies.jsonl: 196 (194 inventory + 2 shared invariants).
- Status counts: MATCHED=196, PARTIAL=0, NOT_EVIDENCED=0, UNCERTAIN=0.
- Policies whose search notes carry a modality caveat, open related item or enforcement note: GOV-015, ARC-001, API-019, DEP-003, DEP-025, WF-006, WF-010.

## Constraints

- Atomic constraints: 813 — ORACLE_LINKED=604, EXTRA=208, LINK_UNCERTAIN=1.
- EXTRA constraints by first-evidence area:
  - .claude/skills/httpclient-factory: 14
  - .claude/skills/security-scan: 12
  - .claude/skills/http-api: 10
  - .claude/skills/project-structure: 10
  - CLAUDE.md: 9
  - .claude/skills/swagger: 9
  - .claude/INSTRUCTION_MAP.md: 8
  - .claude/hooks/claude-hook.mjs: 8
  - .claude/skills/git-workflow: 8
  - .claude/skills/modern-csharp: 8
  - .claude/skills/ef-core: 7
  - .claude/tools: 7
  - .claude/skills/caching: 6
  - .claude/skills/health-check: 6
  - .claude/rules/2-technology: 5
  - .claude/skills/angular: 5
  - .claude/skills/authentication: 5
  - .claude/skills/delivery-pipeline: 5
  - .claude/skills/docker: 5
  - .claude/skills/logging: 5
  - .claude/skills/template-maintenance: 5
  - .editorconfig: 5
  - .claude/rules/3-project: 4
  - .claude/skills/dependency-injection: 4
  - .claude/skills/development-workflow: 4
  - .claude/skills/dotnet-testing: 4
  - .claude/skills/verify: 4
  - .claude/hooks/manifest-checks.mjs: 3
  - .claude/skills/add-dependency: 3
  - .claude/skills/architecture-decision: 3
  - .claude/skills/ci-cd: 3
  - .claude/skills/code-review: 3
  - .claude/rules/1-architecture: 2
  - .claude/skills/api-versioning: 2
  - .claude/skills/aspnet-error-handling: 2
  - .claude/skills/custom-settings: 2
  - Directory.Build.props: 1
  - .claude/rules/0-core: 1
  - .claude/skills/configuration: 1
- Full EXTRA and LINK_UNCERTAIN list with citations: `EXTRA_CONSTRAINTS.md`.

## Orphan ledger

- ORPHAN_CANDIDATES.jsonl rows: 235 — DUPLICATE=5, EXTRA_REGISTERED=208, LINK_UNCERTAIN=1, NON_NORMATIVE=10, POLICY_LINKED=11.
- Details and every unresolved item: `ORPHAN_SWEEP_REPORT.md`.

## File types and limitations

- No binary or non-UTF-8 files; every file was decoded and line-partitioned.
- Structural validation proves accounting, not semantic exhaustiveness; an independent blind sweep is required to challenge the inventory.
- Classification of knowledge-skill imperatives as EXTRA vs non-normative technique involves judgement; each borderline call is recorded in the orphan ledger with its reason.

## Candidate-specific notes (L0)

### Instruction architecture observed
- Stability-level model: rules under `.claude/rules/{0-core,1-architecture,2-technology,3-project}/`, each with a one-line header (`Level · Owns · Scope · Loads · Depends on`) and `paths` frontmatter. Always-loaded surface: `CLAUDE.md` plus two imports (`1-architecture/overview.md`, `3-project/decisions.md`). Workflow and knowledge skills under `.claude/skills/`; one agent (`code-reviewer`); maintainer map `.claude/INSTRUCTION_MAP.md` (not auto-loaded).
- Executable enforcement (read as code, never executed): `.claude/hooks/claude-hook.mjs` registered in exec form for PreToolUse (pre-bash, fail-closed, onFailure block), PostToolUse/PostToolUseFailure (post-bash), PostToolUse edits (post-edit) and Stop. pre-bash blocks npm/pnpm/yarn peer-bypass flags and every `dotnet` project-reference command; post-bash/post-edit compare per-worktree manifest snapshots, route dependency and reference changes, run `manifest-checks.mjs` (central versions, VersionOverride, floating/prerelease versions, deny/review lists with 'Accepted' decision exceptions, npm tooling category, `.npmrc` bypass, outward references) and, after instruction edits, `.claude/tools/check-instructions.mjs`; Stop issues seed/migration/test/custom-settings reminders.
- `CLAUDE.md` defines a normative vocabulary (must/must not = defect; default = deviation needs a concrete reason and must be reported; prefer/avoid = guidance; requires approval = Reserved). Modalities were assigned from that vocabulary and the clause wording.

### Classification conventions applied
- Restatements of oracle policies in rules and skills are ORACLE_LINKED; new outcome-restricting imperatives, including in knowledge skills, private references, hook/checker code and configuration assets (`.editorconfig`, `Directory.Build.props`, `.gitignore`), are EXTRA with the closest policy IDs; examples, permissive wording and investigation prompts (EXC-015 context) are NON_NORMATIVE with reasons; decision tables and check-by-reference lists are DUPLICATE unless an item has no owner clause (then MIXED with the item as EXTRA).
- Instruction-system rules (level placement and neutrality, one owner per rule, split statements, map maintenance, checker invariants) are recorded as EXTRA with a repo/meta scope note; they constrain maintenance of the instruction system rather than product code.
- Hook and checker behaviour that enforces an oracle policy is ORACLE_LINKED with ENFORCED/ENFORCED_ADVISORY modality; enforcement mechanisms without an oracle counterpart (fail-closed policy, blocking all reference commands, 'Accepted' exception mechanism, deny list, checker invariants) are EXTRA.

### Open items
- One LINK_UNCERTAIN constraint: destructive Git operations "clearly required by an approved workflow" (git-workflow) vs GOV-015. Listed in `ORPHAN_SWEEP_REPORT.md`; not resolved at Stage A.

## Check results

```text
$ python _STAGE_A_KIT/03_VALIDATE_STAGE_A.py --root . --candidate L0
{
  "candidate": "L0",
  "template_files": 71,
  "text_files": 71,
  "nonblank_lines": 4621,
  "unclassified_nonblank_lines": 0,
  "oracle_policies": 196,
  "constraints": 813,
  "extra_constraints": 208,
  "uncertain_constraints": 1,
  "coverage_segments": 1605,
  "error_count": 0
}
PASS (STRUCTURE ONLY): L0. This is not semantic completeness proof.

$ python _STAGE_A_KIT/07_VALIDATE_ORPHANS.py --root . --candidate L0
{
  "candidate": "L0",
  "orphan_candidates": 235,
  "resolution_counts": {
    "DUPLICATE": 5,
    "EXTRA_REGISTERED": 208,
    "LINK_UNCERTAIN": 1,
    "NON_NORMATIVE": 10,
    "POLICY_LINKED": 11
  },
  "extra_constraints": 208,
  "uncertain_constraints": 1,
  "error_count": 0
}
PASS (STRUCTURE ONLY): L0. NOT a semantic exhaustion guarantee.

$ python _STAGE_A_KIT/05_WORK_QUEUE_AND_PROGRESS.py check --root . --candidate L0
L0: 12/12 claimed complete batches; 71 file rows, 1605 coverage spans, 813 constraints
PASS: claimed completed batches have structural coverage (not semantic proof).
```
