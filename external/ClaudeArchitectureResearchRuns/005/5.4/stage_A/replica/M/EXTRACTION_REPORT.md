# M — Extraction report (Claude Run 2, blind replica)

## Scope and method

- Snapshot: `inputs/M/output/template/` (61 files, 61 UTF-8 text, 0 binary/non-UTF-8, 7508 nonblank lines); queue `stage_A/_control/M_WORK_QUEUE.json` (19 batches) used read-only.
- Oracle: `inputs/M/source/inventory.json` (194) + `shared-research-invariants.json` (2) = 196 IDs.
- Every file was read in full; annotations were written per batch in `_annotations/B###.ann`, compiled by `stage_A/replica/_tools/build.py` (exact-quote verification, coverage/overlap checks, back-links) and checkpointed with `11_REPLICA_WORK_QUEUE_AND_PROGRESS.py` after each batch.
- Blindness: no file under stage_A/primary, stage_A/independent, stage_A/reconciled, work/, 5.3 or any other run was opened. CANDIDATE.md was read for provenance only.

## Counts

- Files inventoried: 61; completed batches: 19/19
- Coverage segments: 1864 — DUPLICATE 35, EXTRA 50, IMPLEMENTATION 81, LINK_UNCERTAIN 2, MIXED 25, NON_NORMATIVE 1048, ORACLE_LINKED 623
- Uncovered nonblank lines: 0 (enforced by build.py and validator 12)
- Policies: 196 — MATCHED 196, PARTIAL 0, NOT_EVIDENCED 0, UNCERTAIN 0
- Constraints: 241 — ORACLE_LINKED 213, EXTRA 26, LINK_UNCERTAIN 2
- Orphan ledger: 65 rows — DUPLICATE 1, EXTRA_REGISTERED 26, LINK_UNCERTAIN 2, NON_NORMATIVE 36

## Policy status detail

- PARTIAL: none
- NOT_EVIDENCED: none
- UNCERTAIN: none

## EXTRA constraints (summary)

- EXTRA-M-0001 (EXTRA; closest ARC-020, ARC-001, GOV-017): A changed production project reference graph, including a removed project file, is a Reserved decision that goes through Decision Control.
- EXTRA-M-0002 (EXTRA; closest GOV-017, ARC-020): For an unclear decision, any 'yes' to five questions makes it Reserved: does it add, remove or replace a dependency, framework or infrastructure capability; change a project, layer or reference boundary; establish a convention other code is
- EXTRA-M-0003 (EXTRA; closest DEP-001): Dependency removals follow the add-dependency workflow like additions and updates.
- EXTRA-M-0004 (EXTRA; closest none): Ownership of instruction content: rules and CLAUDE.md hold normative policy; workflow skills hold procedures, stop conditions and output shape; knowledge skills hold technique and examples only and own no policy; hooks, scripts and configur
- EXTRA-M-0005 (EXTRA; closest none): New instruction content is placed by kind (planning-time governance and decisions in the compact CLAUDE.md or technology-stack; area constraints in a flat path rule whose paths cover the needed scope; procedures, stop conditions and output 
- EXTRA-M-0006 (EXTRA; closest none): Hooks are registered in exec form (node plus the script path anchored at ${CLAUDE_PROJECT_DIR}, no shell), including the dependency guard for PostToolUseFailure; the PreToolUse guard fails closed (onFailure block) while advisory hooks fail 
- EXTRA-M-0007 (EXTRA; closest API-013, ARC-020): Adopting API versioning is a Reserved decision even when a concrete compatibility need exists.
- UNCERTAIN-M-0001 (LINK_UNCERTAIN; closest GOV-015, DEP-007): Maintain and commit package.json and package-lock.json.
- EXTRA-M-0008 (EXTRA; closest none): Instruction-system structure: required files exist; CLAUDE.md imports only docs/technology-stack.md and no other instruction file imports; every instruction file starts with a one-line '> Owns: ...
- EXTRA-M-0009 (EXTRA; closest DEP-004, DEP-020): Microsoft.Extensions.Http.Polly and Polly.Extensions.Http (deprecated resilience integration packages) must not be added; their presence is reported as a violation with blocking hook feedback.
- EXTRA-M-0010 (EXTRA; closest DEP-001, GOV-014): Remove dependencies that are no longer used when doing so is part of the current change and safe to verify; do not leave dead package references behind.
- EXTRA-M-0011 (EXTRA; closest DEP-004, DEP-005, WF-009): The add-dependency report states the package, selected version, license, checks performed and approval status (approved / awaiting approval / not needed).
- EXTRA-M-0012 (EXTRA; closest GOV-017, GOV-007): An approved Reserved decision (including an explicit instruction in the original request) is recorded before its Reserved part is implemented: a record docs/decisions/NNNN-short-title.md with Status, Date, Context, Decision, Alternatives co
- EXTRA-M-0013 (EXTRA; closest DEP-010, API-010): Register FluentValidation validators with FluentValidation.DependencyInjectionExtensions (AddValidatorsFromAssemblyContaining) and follow the project's established validation invocation pattern rather than a second competing mechanism.
- EXTRA-M-0014 (EXTRA; closest WF-009): The build-fix report states the initial failure, root cause, changes made, backend build / frontend build / tests status (PASS, NOT RUN, NOT APPLICABLE) and remaining issues.
- EXTRA-M-0016 (EXTRA; closest WF-011, WF-012): Code-review findings are reported ordered by severity, each with severity, file/location, what is wrong, why it matters and the smallest reasonable fix, using the fixed severity scale Critical / High / Medium / Low with defined meanings.
- EXTRA-M-0017 (EXTRA; closest WF-009): The development-workflow output reports what changed, Delegated choices worth noting, unresolved Decision Requests, the verify report and every change-specific obligation that was not applicable with the reason.
- UNCERTAIN-M-0002 (LINK_UNCERTAIN; closest GOV-015, GOV-020): High-risk Git operations (reset --hard, clean, push --force, push --force-with-lease, branch deletion, rebase of shared history) are performed only when explicitly requested or clearly required by an approved workflow, after inspecting what
- EXTRA-M-0018 (EXTRA; closest GOV-015, GOV-020): main, master and other protected or shared branches are treated as non-rewritable; a shared branch is never force-pushed unless the user explicitly requests history rewriting and the consequences are understood.
- EXTRA-M-0019 (EXTRA; closest WF-009, WF-022): Run verify before preparing a pull request; the PR has a focused purpose and its description explains what changed, why, how it was verified and important compatibility or migration notes.
- EXTRA-M-0020 (EXTRA; closest RUN-016): Do not wrap normal EF Core operations in a generic application-level retry pipeline by default; prefer the provider's EF Core execution strategy for transient faults and handle transaction/retry interaction per the provider's guidance.
- EXTRA-M-0021 (EXTRA; closest RUN-005): Per-request values such as dynamic access tokens are applied to the specific request or through a handler; shared DefaultRequestHeaders are not mutated concurrently for request-specific values.
- EXTRA-M-0022 (EXTRA; closest DEP-008, DEP-003): global.json pins the repository to the intended supported .NET SDK line; when scaffolding select the current stable SDK for the target .NET release (no RC/preview unless explicitly requested) and allow servicing through the chosen rollForwa
- EXTRA-M-0023 (EXTRA; closest WF-020): Security findings are reported in a fixed shape: severity tag, file:line location and title, OWASP category when applicable, Evidence, Impact (why it is a risk) and Remediation; uncertain findings use the NEEDS VERIFICATION form stating wha
- EXTRA-M-0024 (EXTRA; closest WF-020, WF-009): The security scan report contains Scope, a Limitations statement (static analysis only), a severity Summary table, Findings and Layer Results for the seven layers using PASS / FINDINGS / NOT APPLICABLE / NOT CHECKED, with the fixed severity
- EXTRA-M-0025 (EXTRA; closest none): After hook or script changes run the changed script with sample input and confirm both the pass and the failure paths; the maintenance report lists the files changed, owners added or moved and the checker result.
- EXTRA-M-0026 (EXTRA; closest none): Normative vocabulary: a 'default' may be deviated from only with a concrete reason, and every such deviation must be reported.
- EXTRA-M-0027 (EXTRA; closest DEP-023, RUN-009): Nullable reference types, implicit usings and the latest analysis level are enabled repository-wide through Directory.Build.props.

## Unsupported file types

None: all template files are UTF-8 text.

## Check results

```
M: 19/19 claimed complete batches; 61 file rows, 1864 coverage spans, 241 constraints
PASS: claimed completed batches have structural coverage (not semantic proof).
rc11=0
{
  "candidate": "M",
  "template_files": 61,
  "text_files": 61,
  "nonblank_lines": 7508,
  "unclassified_nonblank_lines": 0,
  "oracle_policies": 196,
  "constraints": 241,
  "extra_constraints": 26,
  "uncertain_constraints": 2,
  "coverage_segments": 1864,
  "error_count": 0
}
PASS (STRUCTURE ONLY): M. This is not semantic completeness proof.
rc12=0
{
  "candidate": "M",
  "orphan_candidates": 65,
  "resolution_counts": {
    "DUPLICATE": 1,
    "EXTRA_REGISTERED": 26,
    "LINK_UNCERTAIN": 2,
    "NON_NORMATIVE": 36
  },
  "extra_constraints": 26,
  "uncertain_constraints": 2,
  "error_count": 0
}
PASS (STRUCTURE ONLY): M. NOT a semantic exhaustion guarantee.
rc13=0
```

## Limitations

- Structural PASS (validators 11/12/13) is not semantic proof.
- All 196 policies are MATCHED; tightened modalities and extra gates are noted in search_notes instead of downgrading status.
- Hooks and checkers were analyzed statically, not executed.
- Two relations remain open (UNCERTAIN-M-0001 'maintain and commit package.json and package-lock.json'; UNCERTAIN-M-0002 'clearly required by an approved workflow').
- CANDIDATE.md was read as provenance only; classifications rest on the template text.
- Identifier numbering has gaps where constraints were merged during annotation (e.g. R151, R179, R200, R204, R209, R213); IDs are local to this run.

