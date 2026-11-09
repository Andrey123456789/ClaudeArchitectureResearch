# Stage A primary extraction report — candidate K0

Extractor: Claude (primary). Scope: `inputs/K0/output/template/**` only; provenance documents were not treated as normative surfaces. All numbers below are computed from the ledgers in this directory.

## Source inventory

- Active template files: 63 (text: 63, binary/non-UTF-8: 0).
- Non-blank lines in text files: 5183.
- Queue batches: 13; batches checked complete: 13.
- Coverage ranges: 1710 — DUPLICATE=46, EXTRA=172, IMPLEMENTATION=157, MIXED=104, NON_NORMATIVE=764, ORACLE_LINKED=467.
- Unclassified non-blank lines: 0 (every non-blank line is in exactly one range; see validator output).

## 196-policy forward mapping

- Policies in policies.jsonl: 196 (194 inventory + 2 shared invariants).
- Status counts: MATCHED=196, PARTIAL=0, NOT_EVIDENCED=0, UNCERTAIN=0.
- Policies whose search notes carry a modality caveat, open related item or enforcement note: GOV-015, GOV-021, ARC-001, PST-008, RUN-010, DEP-003, DEP-004, DEP-025, WF-010.

## Constraints

- Atomic constraints: 810 — ORACLE_LINKED=566, EXTRA=243, LINK_UNCERTAIN=1.
- EXTRA constraints by first-evidence area:
  - .claude/skills/security-scan: 15
  - .claude/skills/httpclient-factory: 11
  - .claude/skills/project-structure: 11
  - CLAUDE.md: 10
  - .claude/skills/dotnet-testing: 10
  - .claude/skills/template-maintenance: 10
  - .claude/scripts/check-instructions.cjs: 10
  - .claude/skills/docker: 9
  - .claude/skills/ef-core: 9
  - .claude/skills/git-workflow: 9
  - .claude/skills/logging: 8
  - .claude/hooks/hook.cjs: 8
  - .claude/skills/architecture-decision: 7
  - .claude/skills/caching: 7
  - .claude/skills/ci-cd: 7
  - .claude/skills/http-api: 7
  - .claude/skills/swagger: 7
  - .claude/MAP.md: 6
  - .claude/rules/backend: 6
  - .claude/skills/add-dependency: 6
  - .claude/skills/delivery-pipeline: 6
  - .claude/skills/health-check: 6
  - .editorconfig: 6
  - .claude/skills/angular: 5
  - .claude/skills/aspnet-error-handling: 5
  - .claude/skills/authentication: 5
  - .claude/skills/build-fix: 5
  - .claude/skills/code-review: 5
  - .claude/skills/modern-csharp: 5
  - .claude/skills/api-versioning: 4
  - .claude/skills/dependency-injection: 4
  - .claude/scripts/check-dependencies.cjs: 4
  - .claude/skills/verify: 3
  - .claude/skills/custom-settings: 2
  - .claude/skills/development-workflow: 2
  - Directory.Build.props: 1
  - .claude/rules/common: 1
  - .claude/skills/configuration: 1
- Full EXTRA and LINK_UNCERTAIN list with citations: `EXTRA_CONSTRAINTS.md`.

## Orphan ledger

- ORPHAN_CANDIDATES.jsonl rows: 270 — DUPLICATE=5, EXTRA_REGISTERED=243, LINK_UNCERTAIN=1, NON_NORMATIVE=16, POLICY_LINKED=5.
- Details and every unresolved item: `ORPHAN_SWEEP_REPORT.md`.

## File types and limitations

- No binary or non-UTF-8 files; every file was decoded and line-partitioned.
- Structural validation proves accounting, not semantic exhaustiveness; an independent blind sweep is required to challenge the inventory.
- Classification of knowledge-skill imperatives as EXTRA vs non-normative technique involves judgement; each borderline call is recorded in the orphan ledger with its reason.

## Candidate-specific notes (K0)

### Instruction architecture observed
- Kind/Scope model: every artifact carries a first-line `Kind | Scope | Owner | Loading` header. Kinds: OP (`CLAUDE.md`, always loaded), DEC (`docs/architecture/decision-register.md`, the single register with D-01…D-18, imported by `CLAUDE.md`), STD (path-scoped standards under `.claude/rules/<scope>/<topic>.md` for common, backend, backend-tests, frontend), KNW (on-demand knowledge skills, some with private `references/`), WF (workflow skills and the `code-reviewer` agent; `template-maintenance` is user-invoked only), ENF (`settings.json`, `hooks/hook.cjs`, `scripts/*.cjs`, `.editorconfig`, `Directory.*.props`) and IN (`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`). `.claude/MAP.md` is the maintainers' map (not loaded).
- Executable enforcement (read as code, never executed): `settings.json` registers exec-form `node hook.cjs <event>` hooks for PreToolUse (Bash|PowerShell, `onFailure: block`, fail-closed), PostToolUse (edit tools and shell), PostToolUseFailure (shell) and Stop. The pre-command gate denies package-changing commands without the self-declared `# add-dependency: reviewed` marker and project-reference commands without `# project-references: approved`, and returns 'ask' for repository-changing Git commands. Post-change handling observes the actual worktree state (per-worktree snapshots in `.claude/.hook-state/`), validates manifests with `check-dependencies.cjs`, reports reference-graph changes, removed/moved manifests and product-input changes, and runs `check-instructions.cjs` after instruction edits. Stop blocks once per material state with seeder, migration-review, test and custom-settings reminders.
- `CLAUDE.md` defines a normative vocabulary (must/must not = defect; default = deviation needs a concrete reason and must be reported; prefer/avoid = guidance; requires approval = Reserved). Modalities were assigned from that vocabulary and the clause wording.

### Classification conventions applied
- Restatements of oracle policies in standards, the decision register, workflows and knowledge skills are ORACLE_LINKED; new outcome-restricting imperatives, including in knowledge skills, private references, hook/checker code and configuration assets (`.editorconfig`, `Directory.Build.props`), are EXTRA with the closest policy IDs; examples, permissive wording and investigation prompts (EXC-015 context) are NON_NORMATIVE with reasons; decision guides and check-by-reference lists are DUPLICATE unless an item has no owner clause (then MIXED with the item as EXTRA).
- Instruction-system rules (Kind/Scope placement, conformance direction, one owner per rule, map maintenance, checker invariants, user-only template maintenance) are recorded as EXTRA with a repo/meta scope note; they constrain maintenance of the instruction system rather than product code.
- Hook and checker behaviour that enforces an oracle policy is ORACLE_LINKED with ENFORCED/ENFORCED_ADVISORY modality; enforcement mechanisms without an oracle counterpart (fail-closed gate, self-declared approval markers, reference-graph gate, deprecated-package list, removal/move feedback, Stop gate) are EXTRA.

### Open items
- One LINK_UNCERTAIN constraint: destructive Git operations "required by an approved workflow" (git-workflow) vs GOV-015. Listed in `ORPHAN_SWEEP_REPORT.md`; not resolved at Stage A.

## Check results

```text
# K0 validator results
$ py _STAGE_A_KIT/05_WORK_QUEUE_AND_PROGRESS.py check --root . --candidate K0
K0: 13/13 claimed complete batches; 63 file rows, 1710 coverage spans, 810 constraints
PASS: claimed completed batches have structural coverage (not semantic proof).
exit=0
$ py _STAGE_A_KIT/03_VALIDATE_STAGE_A.py --root . --candidate K0
{
  "candidate": "K0",
  "template_files": 63,
  "text_files": 63,
  "nonblank_lines": 5183,
  "unclassified_nonblank_lines": 0,
  "oracle_policies": 196,
  "constraints": 810,
  "extra_constraints": 243,
  "uncertain_constraints": 1,
  "coverage_segments": 1710,
  "error_count": 0
}
PASS (STRUCTURE ONLY): K0. This is not semantic completeness proof.
exit=0
$ py _STAGE_A_KIT/07_VALIDATE_ORPHANS.py --root . --candidate K0
{
  "candidate": "K0",
  "orphan_candidates": 270,
  "resolution_counts": {
    "DUPLICATE": 5,
    "EXTRA_REGISTERED": 243,
    "LINK_UNCERTAIN": 1,
    "NON_NORMATIVE": 16,
    "POLICY_LINKED": 5
  },
  "extra_constraints": 243,
  "uncertain_constraints": 1,
  "error_count": 0
}
PASS (STRUCTURE ONLY): K0. NOT a semantic exhaustion guarantee.
exit=0
```
