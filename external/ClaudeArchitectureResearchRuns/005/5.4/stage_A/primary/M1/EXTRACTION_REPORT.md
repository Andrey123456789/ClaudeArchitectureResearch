# Stage A primary extraction report — candidate M1

Extractor: Claude (primary). Scope: `inputs/M1/output/template/**` only; provenance documents were not treated as normative surfaces. All numbers below are computed from the ledgers in this directory.

## Source inventory

- Active template files: 80 (text: 80, binary/non-UTF-8: 0).
- Non-blank lines in text files: 8349.
- Queue batches: 21; batches checked complete: 21.
- Coverage ranges: 2117 — DUPLICATE=12, EXTRA=213, IMPLEMENTATION=193, LINK_UNCERTAIN=1, MIXED=127, NON_NORMATIVE=1006, ORACLE_LINKED=565.
- Unclassified non-blank lines: 0 (every non-blank line is in exactly one range; see validator output).

## 196-policy forward mapping

- Policies in policies.jsonl: 196 (194 inventory + 2 shared invariants).
- Status counts: MATCHED=196, PARTIAL=0, NOT_EVIDENCED=0, UNCERTAIN=0.
- Policies whose search notes carry a modality caveat, open related item or enforcement note: GOV-006, GOV-015, API-019, RUN-021, DEP-003, DEP-025, WF-006, WF-010.

## Constraints

- Atomic constraints: 930 — ORACLE_LINKED=679, EXTRA=248, LINK_UNCERTAIN=3.
- EXTRA constraints by first-evidence area:
  - .claude/scripts/check-instructions.js: 17
  - .claude/skills/security-scan: 13
  - .claude/capabilities: 12
  - .claude/skills/docker: 11
  - .claude/skills/ef-core: 11
  - .claude/skills/httpclient-factory: 11
  - .claude/skills/template-maintenance: 10
  - CLAUDE.md: 10
  - .claude/skills/git-workflow: 9
  - .claude/skills/http-api: 9
  - .claude/skills/swagger: 9
  - .claude/skills/angular: 7
  - .claude/skills/ci-cd: 7
  - .claude/skills/health-check: 7
  - .claude/skills/logging: 7
  - .claude/rules/coding-style.md: 6
  - .claude/skills/dotnet-testing: 6
  - .claude/skills/project-structure: 6
  - .editorconfig: 6
  - .claude/scripts/check-manifests.js: 5
  - .claude/skills/add-dependency: 5
  - .claude/skills/authentication: 5
  - .claude/skills/caching: 5
  - .claude/skills/modern-csharp: 5
  - .claude/scripts/lib: 4
  - .claude/skills/verify: 4
  - .claude/hooks/post-tool-use.js: 3
  - .claude/rules/testing.md: 3
  - .claude/skills/architecture-decision: 3
  - .claude/skills/aspnet-error-handling: 3
  - .claude/skills/build-fix: 3
  - .claude/skills/persistence-change: 3
  - docs/technology-stack.md: 3
  - .claude/MAP.md: 2
  - .claude/skills/code-review: 2
  - .claude/skills/dependency-injection: 2
  - docs/capability-selection.md: 2
  - Directory.Build.props: 2
  - .claude/hooks/pre-tool-use.js: 1
  - .claude/hooks/stop.js: 1
  - .claude/rules/api.md: 1
  - .claude/rules/error-handling.md: 1
  - .claude/rules/test-framework.md: 1
  - .claude/scripts/check-architecture.js: 1
  - .claude/skills/api-versioning: 1
  - .claude/skills/configuration: 1
  - .claude/skills/custom-settings: 1
  - docs/capabilities/architecture.md: 1
- Full EXTRA and LINK_UNCERTAIN list with citations: `EXTRA_CONSTRAINTS.md`.

## Orphan ledger

- ORPHAN_CANDIDATES.jsonl rows: 283 — DUPLICATE=8, EXTRA_REGISTERED=248, LINK_UNCERTAIN=3, NON_NORMATIVE=17, POLICY_LINKED=7.
- Details and every unresolved item: `ORPHAN_SWEEP_REPORT.md`.

## File types and limitations

- No binary or non-UTF-8 files; every file was decoded and line-partitioned.
- Structural validation proves accounting, not semantic exhaustiveness; an independent blind sweep is required to challenge the inventory.
- Classification of knowledge-skill imperatives as EXTRA vs non-normative technique involves judgement; each borderline call is recorded in the orphan ledger with its reason.

## Candidate-specific notes (M1)

### Instruction architecture observed
- Always-loaded surface: `CLAUDE.md` plus six imports (`docs/technology-stack.md`, `docs/capability-selection.md`, and the four planning facets `docs/capabilities/{architecture,persistence,backend-testing,frontend}.md`). Path rules under `.claude/rules/` are flat with `paths:` frontmatter; workflow and knowledge skills under `.claude/skills/`; one agent (`code-reviewer`).
- Capability system: `.claude/capabilities/<slot>/CONTRACT.md` and `<implementation>/MODULE.md` are maintainer metadata whose JSON blocks are consumed by `check-instructions.js`, `check-architecture.js` and `check-manifests.js`. Their tables were classified as NON_NORMATIVE (descriptive) while the enforced invariants (facet conformance, leak tokens, binds, facet headers, planning imports) were registered as EXTRA repo/meta constraints with ENFORCED modality.
- Executable enforcement: PreToolUse gate (`scripts/lib/dependency-commands.js`) denies package and project-reference commands until the trailing markers `# add-dependency: checked` / `# project-reference: checked` are present and denies npm peer-override flags unless `# peer-override: approved-by-user` is present (fails closed); PostToolUse runs manifest, architecture, synchronization and instruction checks and returns WARN and ERROR findings as a blocking reason; Stop hook issues co-change reminders. Hooks were read, never executed.

### Classification conventions applied
- M1's `CLAUDE.md` has no separate normative-vocabulary section; modality was assigned from the wording of each clause (must/never → MUST/MUST_NOT; default/by default → DEFAULT; prefer/avoid → PREFER/AVOID; Reserved → REQUIRES_APPROVAL; hook/script behaviour → ENFORCED or ENFORCED_ADVISORY).
- Restatements of oracle policies in skills/references are ORACLE_LINKED; new outcome-restricting imperatives, including in knowledge skills, private references, hook code and manifests, are EXTRA with the closest policy IDs; examples, permissive wording and investigation prompts (EXC-015 context) are NON_NORMATIVE with a reason; check-by-reference lists and decision tables are DUPLICATE unless they contain an item with no owner clause, in which case they are MIXED with the item registered as EXTRA (e.g. Minimal API endpoint filters in a Controller project; Swagger as a substitute for integration tests).
- Repository/instruction-system rules (MAP placement, one owner per rule, trigger-role preservation, checker runs, capability replacement procedures) are recorded as EXTRA with scope notes; they constrain maintenance of the instruction system rather than product code.

### Open items
- Three LINK_UNCERTAIN constraints remain (collation default vs GOV-006; pre-mutation cache invalidation vs RUN-021; destructive Git operations "clearly required by an approved workflow" vs GOV-015). They are listed in `ORPHAN_SWEEP_REPORT.md` and are not resolved at Stage A.

## Check results

```text
$ python _STAGE_A_KIT/03_VALIDATE_STAGE_A.py --candidate M1
{
  "candidate": "M1",
  "template_files": 80,
  "text_files": 80,
  "nonblank_lines": 8349,
  "unclassified_nonblank_lines": 0,
  "oracle_policies": 196,
  "constraints": 930,
  "extra_constraints": 248,
  "uncertain_constraints": 3,
  "coverage_segments": 2117,
  "error_count": 0
}
PASS (STRUCTURE ONLY): M1. This is not semantic completeness proof.

$ python _STAGE_A_KIT/07_VALIDATE_ORPHANS.py --candidate M1
{
  "candidate": "M1",
  "orphan_candidates": 283,
  "resolution_counts": {
    "DUPLICATE": 8,
    "EXTRA_REGISTERED": 248,
    "LINK_UNCERTAIN": 3,
    "NON_NORMATIVE": 17,
    "POLICY_LINKED": 7
  },
  "extra_constraints": 248,
  "uncertain_constraints": 3,
  "error_count": 0
}
PASS (STRUCTURE ONLY): M1. NOT a semantic exhaustion guarantee.

$ python _STAGE_A_KIT/05_WORK_QUEUE_AND_PROGRESS.py --candidate M1 check
M1: 21/21 claimed complete batches; 80 file rows, 2117 coverage spans, 930 constraints
PASS: claimed completed batches have structural coverage (not semantic proof).
```
