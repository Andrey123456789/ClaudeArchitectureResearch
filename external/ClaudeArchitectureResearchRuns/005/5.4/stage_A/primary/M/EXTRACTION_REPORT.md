# Stage A primary extraction report — candidate M

Extractor: Claude (primary). Scope: `inputs/M/output/template/**` only; provenance documents were not treated as normative surfaces. All numbers below are computed from the ledgers in this directory.

## Source inventory

- Active template files: 61 (text: 61, binary/non-UTF-8: 0).
- Non-blank lines in text files: 7508.
- Queue batches: 19; batches checked complete: 19.
- Coverage ranges: 2012 — DUPLICATE=8, EXTRA=208, IMPLEMENTATION=168, LINK_UNCERTAIN=1, MIXED=110, NON_NORMATIVE=966, ORACLE_LINKED=551.
- Unclassified non-blank lines: 0 (every non-blank line is in exactly one range; see validator output).

## 196-policy forward mapping

- Policies in policies.jsonl: 196 (194 inventory + 2 shared invariants).
- Status counts: MATCHED=196, PARTIAL=0, NOT_EVIDENCED=0, UNCERTAIN=0.
- Policies whose search notes carry a modality caveat, open related item or enforcement note: GOV-012, GOV-015, ARC-013, TST-005, RUN-001, RUN-010, RUN-013, RUN-021, RUN-022, RUN-024, FE-004, FE-006, FE-008, FE-011, WF-010.

## Constraints

- Atomic constraints: 851 — ORACLE_LINKED=628, EXTRA=221, LINK_UNCERTAIN=2.
- EXTRA constraints by first-evidence area:
  - .claude/scripts/check-instructions.mjs: 17
  - .claude/skills/security-scan: 16
  - .claude/skills/docker: 11
  - .claude/skills/ef-core: 10
  - .claude/skills/httpclient-factory: 10
  - CLAUDE.md: 10
  - .claude/skills/git-workflow: 9
  - .claude/skills/http-api: 9
  - .claude/skills/project-structure: 9
  - .claude/skills/swagger: 8
  - .claude/skills/architecture-decision: 7
  - .claude/skills/ci-cd: 7
  - .claude/skills/health-check: 7
  - .claude/skills/logging: 7
  - .claude/skills/template-maintenance: 7
  - .claude/rules/coding-style.md: 6
  - .claude/skills/angular: 5
  - .claude/skills/authentication: 5
  - .claude/skills/caching: 5
  - .claude/skills/dotnet-testing: 5
  - .claude/scripts/check-manifests.mjs: 4
  - .claude/skills/add-dependency: 4
  - .editorconfig: 4
  - Directory.Build.props: 4
  - .claude/MAP.md: 3
  - .claude/skills/build-fix: 3
  - .claude/skills/modern-csharp: 3
  - docs/technology-stack.md: 3
  - .claude/hooks/dependency-guard.mjs: 2
  - .claude/hooks/stop-co-change.mjs: 2
  - .claude/rules/api.md: 2
  - .claude/rules/testing.md: 2
  - .claude/skills/aspnet-error-handling: 2
  - .claude/skills/code-review: 2
  - .claude/skills/dependency-injection: 2
  - .claude/skills/verify: 2
  - .claude/rules/architecture.md: 1
  - .claude/rules/error-handling.md: 1
  - .claude/settings.json: 1
  - .claude/skills/api-versioning: 1
  - .claude/skills/custom-settings: 1
  - .claude/skills/configuration: 1
  - .claude/skills/development-workflow: 1
- Full EXTRA and LINK_UNCERTAIN list with citations: `EXTRA_CONSTRAINTS.md`.

## Orphan ledger

- ORPHAN_CANDIDATES.jsonl rows: 283 — DUPLICATE=4, EXTRA_REGISTERED=221, LINK_UNCERTAIN=2, NON_NORMATIVE=33, POLICY_LINKED=23.
- Details and every unresolved item: `ORPHAN_SWEEP_REPORT.md`.

## File types and limitations

- No binary or non-UTF-8 files; every file was decoded and line-partitioned.
- Structural validation proves accounting, not semantic exhaustiveness; an independent blind sweep is required to challenge the inventory.
- Classification of knowledge-skill imperatives as EXTRA vs non-normative technique involves judgement; each borderline call is recorded in the orphan ledger with its reason.

## Candidate-specific observations (facts only, no cross-candidate comparison)

- Loading surfaces: always-loaded `CLAUDE.md` with an @-import of `docs/technology-stack.md`; eleven flat path-scoped rules under `.claude/rules/`; workflow skills (routed from CLAUDE.md), knowledge skills (on demand), private references read by their owning skill, one subagent, four hook scripts registered in `.claude/settings.json`, two checker scripts, `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props`. `MAP.md` is declared never loaded (maintainer map consulted by the user-invoked `template-maintenance` skill); its placement guidance was recorded as repo/meta EXTRA with that scope.
- Executable enforcement reviewed branch by branch: PreToolUse npm bypass block (fail-closed), PostToolUse/PostToolUseFailure manifest checks with block-with-feedback on violations, file-edit reminders and manifest checks, Stop-hook co-change reminders shown once per change state, manifest checker violation/note paths, instruction-structure checker failure paths, build properties and EditorConfig severities.
- `CLAUDE.md` § Normative Vocabulary defines `prefer/avoid` as guidance and requires deviations from `default` to be reported; both are recorded as EXTRA meta-rules (EXTRA-M-0016, EXTRA-M-0017) and the affected policies carry a modality caveat in their search notes.
- Knowledge skills declare themselves 'technique and examples (no policy)'. Imperative clauses inside them were nevertheless classified individually: restatements of oracle policies as ORACLE_LINKED, new outcome-restricting imperatives as EXTRA (scope: on-demand skill), permissive/descriptive text and code examples as NON_NORMATIVE with a specific reason.
- Two LINK_UNCERTAIN items remain open (see ORPHAN_SWEEP_REPORT.md).
- Snapshot verification: `py .\SETUP_5_4.py --verify` passed before extraction (484 files unchanged, all six candidates).

## Check results

```text
{
  "candidate": "M",
  "template_files": 61,
  "text_files": 61,
  "nonblank_lines": 7508,
  "unclassified_nonblank_lines": 0,
  "oracle_policies": 196,
  "constraints": 851,
  "extra_constraints": 221,
  "uncertain_constraints": 2,
  "coverage_segments": 2012,
  "error_count": 0
}
PASS (STRUCTURE ONLY): M. This is not semantic completeness proof.
{
  "candidate": "M",
  "orphan_candidates": 283,
  "resolution_counts": {
    "DUPLICATE": 4,
    "EXTRA_REGISTERED": 221,
    "LINK_UNCERTAIN": 2,
    "NON_NORMATIVE": 33,
    "POLICY_LINKED": 23
  },
  "extra_constraints": 221,
  "uncertain_constraints": 2,
  "error_count": 0
}
PASS (STRUCTURE ONLY): M. NOT a semantic exhaustion guarantee.
M: 19/19 claimed complete batches; 61 file rows, 2012 coverage spans, 851 constraints
PASS: claimed completed batches have structural coverage (not semantic proof).
```
