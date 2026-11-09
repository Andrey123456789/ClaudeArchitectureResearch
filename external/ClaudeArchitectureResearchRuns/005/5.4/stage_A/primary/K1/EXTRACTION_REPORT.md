# Stage A primary extraction report — candidate K1

Extractor: Claude (primary). Scope: `inputs/K1/output/template/**` only; provenance documents were not treated as normative surfaces. All numbers below are computed from the ledgers in this directory.

## Source inventory

- Active template files: 87 (text: 87, binary/non-UTF-8: 0).
- Non-blank lines in text files: 5514.
- Queue batches: 13; batches checked complete: 13.
- Coverage ranges: 1818 — DUPLICATE=59, EXTRA=208, IMPLEMENTATION=191, MIXED=112, NON_NORMATIVE=771, ORACLE_LINKED=477.
- Unclassified non-blank lines: 0 (every non-blank line is in exactly one range; see validator output).

## 196-policy forward mapping

- Policies in policies.jsonl: 196 (194 inventory + 2 shared invariants).
- Status counts: MATCHED=196, PARTIAL=0, NOT_EVIDENCED=0, UNCERTAIN=0.
- Policies whose search notes carry a modality caveat, open related item or enforcement note: GOV-015, GOV-021, ARC-001, PST-008, TST-009, RUN-010, RUN-021, RUN-024, DEP-003, DEP-004, DEP-025, WF-010.

## Constraints

- Atomic constraints: 875 — ORACLE_LINKED=599, EXTRA=274, LINK_UNCERTAIN=2.
- EXTRA constraints by first-evidence area:
  - .claude/scripts/check-instructions.cjs: 16
  - .claude/skills/security-scan: 15
  - .claude/skills/ef-core: 14
  - .claude/skills/template-maintenance: 12
  - .claude/skills/httpclient-factory: 11
  - .claude/skills/modern-csharp: 11
  - .claude/skills/dotnet-testing: 10
  - .claude/skills/project-structure: 10
  - CLAUDE.md: 9
  - .claude/skills/ci-cd: 9
  - .claude/skills/docker: 9
  - .claude/skills/git-workflow: 9
  - .claude/skills/architecture-decision: 8
  - .claude/skills/http-api: 8
  - .claude/skills/logging: 8
  - .claude/skills/caching: 7
  - .claude/skills/swagger: 7
  - .claude/capabilities: 6
  - .claude/skills/add-dependency: 6
  - .claude/skills/angular: 6
  - .claude/skills/aspnet-error-handling: 6
  - .claude/skills/authentication: 6
  - .claude/skills/health-check: 6
  - .claude/skills/verify: 6
  - .editorconfig: 6
  - .claude/skills/build-fix: 5
  - .claude/skills/code-review: 5
  - .claude/skills/dependency-injection: 5
  - .claude/scripts/check-manifests.cjs: 5
  - .claude/skills/api-versioning: 4
  - .claude/skills/delivery-change: 4
  - .claude/skills/persistence-change: 4
  - .claude/MAP.md: 3
  - .claude/skills/custom-settings: 3
  - .claude/hooks/dispatch.cjs: 3
  - .claude/scripts/actual-state.cjs: 3
  - .claude/scripts/classify-command.cjs: 2
  - .claude/scripts/facets: 2
  - Directory.Build.props: 1
  - docs/architecture/decision-register.md: 1
  - .claude/rules/backend: 1
  - .claude/skills/configuration: 1
  - .claude/skills/development-workflow: 1
- Full EXTRA and LINK_UNCERTAIN list with citations: `EXTRA_CONSTRAINTS.md`.

## Orphan ledger

- ORPHAN_CANDIDATES.jsonl rows: 297 — DUPLICATE=4, EXTRA_REGISTERED=274, LINK_UNCERTAIN=2, NON_NORMATIVE=12, POLICY_LINKED=5.
- Details and every unresolved item: `ORPHAN_SWEEP_REPORT.md`.

## File types and limitations

- No binary or non-UTF-8 files; every file was decoded and line-partitioned.
- Structural validation proves accounting, not semantic exhaustiveness; an independent blind sweep is required to challenge the inventory.
- Classification of knowledge-skill imperatives as EXTRA vs non-normative technique involves judgement; each borderline call is recorded in the orphan ledger with its reason.

## Candidate-specific notes (K1)

### Instruction architecture observed
- Kind × Scope × Capability model: every artifact carries a first-line `Kind | Scope | Capability | Loading` header. `CLAUDE.md` (OP, always loaded) imports the decision register (DEC) that holds the capability selection, approved stack, conditional technologies, layout default and accepted decisions. Standards (STD) are path-scoped under `.claude/rules/<scope>/`, skills are KNW or WF (with private `references/`), `code-reviewer` is a thin agent, and `template-maintenance` is user-invoked only. `.claude/MAP.md` is the maintainers' map (not loaded).
- Capability slots (architecture frame; persistence and backend-testing required leaves; optional frontend leaf) are described by slot contracts and module manifests under `.claude/capabilities/` (not loaded). The selected implementations (clean-architecture, ef-core/sqlserver, nunit, angular) own role-named facets: framework-specific standards, knowledge skills, scaffolding references, workflows and ENF facet checks; neutral standards stay implementation-independent.
- Executable enforcement (read as code, never executed): `settings.json` registers exec-form `node dispatch.cjs <event>` hooks. PreToolUse (Bash|PowerShell, `onFailure: block`, fail-closed) uses `classify-command.cjs` to block package commands without exact versions, bulk updates, removals, peer-dependency bypass flags, deep wrapper nesting and project-reference commands not recorded as approved `From -> To` edges in the register. PostToolUse/PostToolUseFailure use `actual-state.cjs` to validate changed manifests with `check-manifests.cjs` (CPM, versions, deny/exception lists, npm categories, lockfile, facet checks), report unrecorded reference-graph changes, product-input changes and instruction-structure errors (`check-instructions.cjs`). Stop runs `check-cochange.cjs` (test reminder plus persistence facet seed/migration reminders) once per content state. No hook classifies Git commands.
- `CLAUDE.md` defines a normative vocabulary (must/must not = defect; default = deviation needs a concrete reason and must be reported; prefer/avoid = guidance; requires approval = Reserved). Modalities were assigned from that vocabulary and the clause wording.

### Classification conventions applied
- Restatements of oracle policies in standards, the register, workflows and knowledge skills are ORACLE_LINKED; new outcome-restricting imperatives, including in knowledge skills, private references, slot contracts, hook/checker/facet code and configuration assets (`.editorconfig`, `Directory.Build.props`), are EXTRA with the closest policy IDs; examples, permissive wording and investigation prompts (EXC-015 context) are NON_NORMATIVE with reasons; decision guides, inventory rows and check-by-reference lists are DUPLICATE unless an item has no owner clause (then MIXED with the item as EXTRA).
- Instruction-system and capability-system rules (Kind/Scope/Capability classification, conformance direction, one owner per rule, leak rule, facet roles, binding obligations, map/manifest maintenance, checker invariants, user-only template maintenance) are recorded as EXTRA with a repo/meta scope note.
- Hook, checker and facet behaviour that enforces an oracle policy is ORACLE_LINKED with ENFORCED/ENFORCED_ADVISORY modality; enforcement mechanisms without an oracle counterpart (fail-closed guard, removal gate, unclassifiable-command block, approval-record format for reference changes, deprecated-package list, migration-missing reminder, Stop gate) are EXTRA.

### Open items
- Two LINK_UNCERTAIN constraints: pre-mutation cache invalidation deliberately accepted by the workflow (caching) vs RUN-021; high-risk Git operations "clearly required by an approved workflow" (git-workflow) vs GOV-015. Listed in `ORPHAN_SWEEP_REPORT.md`; not resolved at Stage A.

## Check results

```text
# K1 validator results
$ py _STAGE_A_KIT/05_WORK_QUEUE_AND_PROGRESS.py check --root . --candidate K1
K1: 13/13 claimed complete batches; 87 file rows, 1818 coverage spans, 875 constraints
PASS: claimed completed batches have structural coverage (not semantic proof).
exit=0
$ py _STAGE_A_KIT/03_VALIDATE_STAGE_A.py --root . --candidate K1
{
  "candidate": "K1",
  "template_files": 87,
  "text_files": 87,
  "nonblank_lines": 5514,
  "unclassified_nonblank_lines": 0,
  "oracle_policies": 196,
  "constraints": 875,
  "extra_constraints": 274,
  "uncertain_constraints": 2,
  "coverage_segments": 1818,
  "error_count": 0
}
PASS (STRUCTURE ONLY): K1. This is not semantic completeness proof.
exit=0
$ py _STAGE_A_KIT/07_VALIDATE_ORPHANS.py --root . --candidate K1
{
  "candidate": "K1",
  "orphan_candidates": 297,
  "resolution_counts": {
    "DUPLICATE": 4,
    "EXTRA_REGISTERED": 274,
    "LINK_UNCERTAIN": 2,
    "NON_NORMATIVE": 12,
    "POLICY_LINKED": 5
  },
  "extra_constraints": 274,
  "uncertain_constraints": 2,
  "error_count": 0
}
PASS (STRUCTURE ONLY): K1. NOT a semantic exhaustion guarantee.
exit=0
```
