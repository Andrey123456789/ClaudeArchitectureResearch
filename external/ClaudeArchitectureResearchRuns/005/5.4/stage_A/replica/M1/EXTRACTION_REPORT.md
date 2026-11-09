# M1 — Extraction report (Claude Run 2, blind replica)

## Scope and method

- Snapshot: `inputs/M1/output/template/` (80 files, 80 UTF-8 text, 0 binary/non-UTF-8, 8349 nonblank lines); queue `stage_A/_control/M1_WORK_QUEUE.json` (21 batches) used read-only.
- Oracle: `inputs/M1/source/inventory.json` (194) + `shared-research-invariants.json` (2) = 196 IDs.
- Every file was read in full; annotations were written per batch in `_annotations/B###.ann`, compiled by `stage_A/replica/_tools/build.py` (exact-quote verification, coverage/overlap checks, back-links) and checkpointed with `11_REPLICA_WORK_QUEUE_AND_PROGRESS.py` after each batch.
- Blindness: no file under stage_A/primary, stage_A/independent, stage_A/reconciled, work/, 5.3 or any other run was opened. CANDIDATE.md was read for provenance only.

## Counts

- Files inventoried: 80; completed batches: 21/21
- Coverage segments: 2041 — DUPLICATE 29, EXTRA 110, IMPLEMENTATION 134, LINK_UNCERTAIN 1, MIXED 31, NON_NORMATIVE 1086, ORACLE_LINKED 650
- Uncovered nonblank lines: 0 (enforced by build.py and validator 12)
- Policies: 196 — MATCHED 196, PARTIAL 0, NOT_EVIDENCED 0, UNCERTAIN 0
- Constraints: 247 — ORACLE_LINKED 211, EXTRA 34, LINK_UNCERTAIN 2
- Orphan ledger: 69 rows — DUPLICATE 2, EXTRA_REGISTERED 34, LINK_UNCERTAIN 2, NON_NORMATIVE 31

## Policy status detail

- PARTIAL: none
- NOT_EVIDENCED: none
- UNCERTAIN: none

## EXTRA constraints (summary)

- EXTRA-M1-0001 (EXTRA; closest ARC-020, DEP-009): Static capability composition: exactly the four slots architecture (required frame), persistence and backend-testing (required leaves) and frontend (optional leaf); each required slot has exactly one selected implementation and the optional
- EXTRA-M1-0002 (EXTRA; closest none): Slot contract completeness: a slot implementation supplies every required facet (planning, rules, workflow/placement, knowledge), required property, required enforcement data and role mapping listed in its slot contract; a missing required 
- EXTRA-M1-0003 (EXTRA; closest none): Role vocabulary and leak rule: other instructions use the slot contracts' stable role vocabulary (core model, use-case layer, use-case unit, persistence-access contract, commit boundary, adapter layer, entry point, composition root, test pr
- EXTRA-M1-0004 (EXTRA; closest none): Content ownership in the capability model: placement belongs to the architecture frame and technique to the leaf; implementation-independent policy (framework-independent testing rules, framework-independent frontend rules) stays outside th
- EXTRA-M1-0005 (EXTRA; closest none): Replacement and removal procedure: replacing a leaf replaces its facets (planning, rule facet, knowledge content, adapter data) without touching the framework-independent rules; clearing the optional frontend removes its facets and planning
- EXTRA-M1-0006 (EXTRA; closest DEP-009, ARC-020, GOV-006): Persistence semantics on change: the persistence implementation declares commit binding, migration mechanism, seeding mechanism, provider variant, observable string-comparison semantics and relational-testing expectations; replacing the tec
- EXTRA-M1-0008 (EXTRA; closest ARC-020, ARC-001, GOV-017): Changing the project reference graph is Reserved; project-reference commands are denied until the project-structure workflow was applied (re-run with '# project-reference: checked'), which routes Reserved reference-graph changes to architec
- EXTRA-M1-0009 (EXTRA; closest none): After an edit to an instruction file the instruction-structure check runs and its reported errors must be fixed (template-maintenance).
- EXTRA-M1-0010 (EXTRA; closest PST-009, PST-010): When persistence model files change without migration changes, confirm the persistence-change workflow (schema changes paired with migrations) was applied, or state why it does not apply.
- UNCERTAIN-M1-0001 (LINK_UNCERTAIN; closest GOV-015, DEP-007): Maintain and commit package.json and package-lock.json (the manifest check also warns 'maintain and commit the lockfile' when package-lock.json is missing).
- EXTRA-M1-0007 (EXTRA; closest DEP-001, DEP-003): Dependency removals follow the add-dependency workflow: removal commands (npm/pnpm uninstall/remove, yarn remove, dotnet remove package, dotnet package remove, nuget delete, Uninstall-Package) are denied until re-run with '# add-dependency:
- EXTRA-M1-0011 (EXTRA; closest none): Ownership of instruction content: every rule has exactly one owner and other files point to it; knowledge skills are technique only and never sole policy owners; implementation-specific content goes only into the module facets.
- EXTRA-M1-0012 (EXTRA; closest none): Hook registration form: hooks are wired in exec form (command node plus script path through ${CLAUDE_PROJECT_DIR}, no shell); the critical PreToolUse hook fails closed (onFailure block); failed shell commands are post-checked (PostToolUseFa
- EXTRA-M1-0013 (EXTRA; closest API-013, ARC-020): Adopting API versioning is Reserved and needs explicit approval, even when a concrete compatibility need exists.
- EXTRA-M1-0014 (EXTRA; closest none): Instruction-system structure: every instruction artifact starts with a one-line ownership header and uses no Level:/Kind: classification; rules stay flat in .claude/rules/ with non-empty paths; required workflow and embedded knowledge skill
- EXTRA-M1-0015 (EXTRA; closest DEP-004, DEP-020, DEP-010): Microsoft.Extensions.Http.Polly and Polly.Extensions.Http (deprecated resilience integrations), Serilog.Sinks.Elasticsearch (deprecated sink) and FluentValidation.AspNetCore (legacy automatic-validation integration) are reported as errors w
- EXTRA-M1-0016 (EXTRA; closest DEP-001, GOV-014): Remove dependencies that are no longer used when that is part of the current change and safe to verify; do not leave dead package references.
- EXTRA-M1-0017 (EXTRA; closest GOV-017, GOV-007): Accepted architecture, stack, convention or public-contract decisions are recorded in the same change as an ADR in docs/decisions/NNNN-short-title.md (Status, Context, Decision, Consequences) and in the affected decision record (technology 
- EXTRA-M1-0018 (EXTRA; closest ARC-020, GOV-017, DEP-002): Changing a capability selection, enabling or disabling the optional frontend slot, or changing a declared property such as the persistence provider variant is Reserved and requires an ADR; after approval the replacement itself is applied by
- EXTRA-M1-0019 (EXTRA; closest DEP-010, API-010): Register FluentValidation validators with FluentValidation.DependencyInjectionExtensions and follow the project's established validation invocation pattern rather than a second competing mechanism.
- EXTRA-M1-0020 (EXTRA; closest WF-009): The build-fix report states the initial failure, root cause, changes made, backend build / frontend build / tests status (PASS, NOT RUN, NOT APPLICABLE) and remaining issues.
- EXTRA-M1-0021 (EXTRA; closest RUN-021, ARC-016): Tracked persistence entities must not be cached across Unit of Work boundaries.
- EXTRA-M1-0022 (EXTRA; closest WF-011, WF-012): Code-review findings are reported ordered by severity, each with severity, file/location, what is wrong, why it matters and the smallest reasonable fix, using the fixed severity scale Critical / High / Medium / Low with defined meanings.
- UNCERTAIN-M1-0002 (LINK_UNCERTAIN; closest GOV-015, GOV-020): High-risk Git operations (reset --hard, clean, push --force, push --force-with-lease, branch deletion, rebasing shared history) are performed only when explicitly requested or clearly required by an approved workflow, after inspecting what 
- EXTRA-M1-0023 (EXTRA; closest GOV-015, GOV-020): main, master and other protected or shared branches are treated as non-rewritable; a shared branch is never force-pushed unless the user explicitly requests history rewriting and the consequences are understood.
- EXTRA-M1-0024 (EXTRA; closest WF-009, WF-022): Before preparing a pull request run verify; the PR has a focused purpose and its description explains what changed, why, how it was verified and important compatibility or migration notes.
- EXTRA-M1-0025 (EXTRA; closest RUN-002): Fire-and-forget EF Core asynchronous operations are a defect.
- EXTRA-M1-0026 (EXTRA; closest RUN-016): Do not wrap normal persistence operations in a generic application-level retry pipeline; use the persistence provider's execution strategy for transient faults and handle transaction/retry interaction per the provider's guidance.
- EXTRA-M1-0027 (EXTRA; closest RUN-005): Per-request values such as dynamic access tokens are applied to the specific request or through a handler; shared default headers (DefaultRequestHeaders) are not mutated concurrently.
- EXTRA-M1-0028 (EXTRA; closest RUN-013, RUN-014): Logs are not used as an audit database without a dedicated audit design.
- EXTRA-M1-0029 (EXTRA; closest DEP-008, DEP-003): global.json pins the intended stable SDK line; when scaffolding select the current stable SDK for the target .NET release (no RC/preview SDK unless explicitly requested) and allow servicing through the chosen rollForward policy.
- EXTRA-M1-0030 (EXTRA; closest WF-020): Security findings are reported in a fixed shape: severity tag, file:line location and title, OWASP category, Evidence, Impact and Remediation; findings with incomplete evidence use the NEEDS VERIFICATION form stating what effective behavior
- EXTRA-M1-0031 (EXTRA; closest WF-020, WF-009): The security scan report contains Scope, a Limitations statement (static analysis only), a severity Summary table, Findings and Layer Results for the seven layers with PASS / FINDINGS / NOT APPLICABLE / NOT CHECKED, using the fixed severity
- EXTRA-M1-0032 (EXTRA; closest none): Template maintenance procedure: read .claude/MAP.md first; place new content by kind (planning-time governance in the compact CLAUDE.md, stack in technology-stack, capability decisions in docs/capabilities, path rules in flat .claude/rules 
- EXTRA-M1-0033 (EXTRA; closest GOV-017, ARC-020): For an unclear decision, any 'yes' to five questions makes it Reserved: does it add, remove or replace a dependency, framework or infrastructure capability; change a project, layer or reference boundary; establish a convention other code mu
- EXTRA-M1-0034 (EXTRA; closest DEP-023, RUN-009): Nullable reference types and implicit usings are enabled repository-wide through Directory.Build.props.

## Unsupported file types

None: all template files are UTF-8 text.

## Check results

```
M1: 21/21 claimed complete batches; 80 file rows, 2041 coverage spans, 247 constraints
PASS: claimed completed batches have structural coverage (not semantic proof).
rc11=0
{
  "candidate": "M1",
  "template_files": 80,
  "text_files": 80,
  "nonblank_lines": 8349,
  "unclassified_nonblank_lines": 0,
  "oracle_policies": 196,
  "constraints": 247,
  "extra_constraints": 34,
  "uncertain_constraints": 2,
  "coverage_segments": 2041,
  "error_count": 0
}
PASS (STRUCTURE ONLY): M1. This is not semantic completeness proof.
rc12=0
{
  "candidate": "M1",
  "orphan_candidates": 69,
  "resolution_counts": {
    "DUPLICATE": 2,
    "EXTRA_REGISTERED": 34,
    "LINK_UNCERTAIN": 2,
    "NON_NORMATIVE": 31
  },
  "extra_constraints": 34,
  "uncertain_constraints": 2,
  "error_count": 0
}
PASS (STRUCTURE ONLY): M1. NOT a semantic exhaustion guarantee.
rc13=0
```

## Limitations

- Structural PASS (validators 11/12/13) is not semantic proof.
- All 196 policies are MATCHED; tightened modalities and extra gates are noted in search_notes instead of downgrading status.
- Hooks and checkers were analyzed statically, not executed.
- Two relations remain open (UNCERTAIN-M1-0001 'maintain and commit package.json and package-lock.json'; UNCERTAIN-M1-0002 'clearly required by an approved workflow').
- CANDIDATE.md was read as provenance only; classifications rest on the template text.
- Identifier numbering has gaps where constraints were merged during annotation (R146 unused); IDs are local to this run.

