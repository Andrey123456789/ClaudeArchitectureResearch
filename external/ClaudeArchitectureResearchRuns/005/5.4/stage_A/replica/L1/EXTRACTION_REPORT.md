# L1 — Extraction report (Claude Run 2, blind replica)

## Scope and method

- Snapshot: `inputs/L1/output/template/` (86 files, 86 UTF-8 text, 0 binary/non-UTF-8, 4279 nonblank lines); queue `stage_A/_control/L1_WORK_QUEUE.json` (10 batches) used read-only.
- Oracle: `inputs/L1/source/inventory.json` (194) + `shared-research-invariants.json` (2) = 196 IDs.
- Every file was read in full; annotations were written per batch in `_annotations/B###.ann`, compiled by `stage_A/replica/_tools/build.py` (exact-quote verification, coverage/overlap checks, back-links) and checkpointed with `11_REPLICA_WORK_QUEUE_AND_PROGRESS.py` after each batch.
- Blindness: no file under stage_A/primary, stage_A/independent, stage_A/reconciled, work/, 5.3 or any other run was opened. CANDIDATE.md was read for provenance only.

## Counts

- Files inventoried: 86; completed batches: 10/10
- Coverage segments: 1682 — DUPLICATE 35, EXTRA 84, IMPLEMENTATION 166, MIXED 32, NON_NORMATIVE 805, ORACLE_LINKED 560
- Uncovered nonblank lines: 0 (enforced by build.py and validator 12)
- Policies: 196 — MATCHED 196, PARTIAL 0, NOT_EVIDENCED 0, UNCERTAIN 0
- Constraints: 254 — ORACLE_LINKED 217, EXTRA 35, LINK_UNCERTAIN 2
- Orphan ledger: 55 rows — DUPLICATE 2, EXTRA_REGISTERED 35, LINK_UNCERTAIN 2, NON_NORMATIVE 16

## Policy status detail

- PARTIAL: none
- NOT_EVIDENCED: none
- UNCERTAIN: none

## EXTRA constraints (summary)

- EXTRA-L1-0001 (EXTRA; closest none): Slot contract completeness: a slot implementation supplies every required facet of its slot contract with the stated form, level, loading and content (architecture: style, boundaries, layout, check; backend-testing: framework rule, commands
- EXTRA-L1-0002 (EXTRA; closest none): Leak rule: outside an implementation module (its manifest-listed facet files and module directory), instruction artifacts refer to slot concerns only by slot name, facet role (<slot>.<facet>) and the stable role vocabulary; implementation n
- EXTRA-L1-0003 (EXTRA; closest none): Content ownership in the capability model: placement belongs to the architecture frame and technique to leaf modules; implementation-independent policy (test policy, frontend structure, browser security, package-manager conventions) stays o
- EXTRA-L1-0004 (EXTRA; closest ARC-020, DEP-002, GOV-017): A capability-selection change (changing the frame, replacing a leaf implementation or provider, clearing or adding the optional frontend) requires an ADR recorded with architecture-decision in addition to Reserved approval.
- EXTRA-L1-0005 (EXTRA; closest none): Replacement and removal procedure: replacing a slot implementation replaces all of its facets together (rule facet, commands, enforcement data, knowledge content, selection row; for the frame also the CLAUDE.md style import) and keeps neutr
- EXTRA-L1-0006 (EXTRA; closest DEP-009, ARC-020, GOV-006): Persistence semantics on change: the persistence selection records declared properties (provider variant, default string-comparison/case-sensitivity semantics, migration mechanism, seeding mechanism); replacing the implementation (e.g. an O
- EXTRA-L1-0007 (EXTRA; closest PST-009, PST-010): When the schema changes, add a migration from the implementation-layer project with the entry-point project as startup project; the Stop hook reminds when domain-model or persistence-configuration files changed without a migration change an
- EXTRA-L1-0008 (EXTRA; closest WF-009): The persistence change procedure reports model changes, migration names with review notes (destructive operations called out), whether DbSeeder was updated or unaffected, and the tests added or updated.
- EXTRA-L1-0009 (EXTRA; closest DEP-004, DEP-020, DEP-010): Packages Microsoft.Extensions.Http.Polly, Polly.Extensions.Http (deprecated resilience integrations), FluentValidation.AspNetCore (deprecated automatic-validation integration) and Serilog.Sinks.Elasticsearch (deprecated sink) must not be ad
- EXTRA-L1-0010 (EXTRA; closest DEP-001, DEP-003): Dependency-removal commands (npm/pnpm uninstall, remove, rm, un, unlink; yarn remove; dotnet remove package; dotnet package remove; dotnet tool uninstall; Uninstall-Package) are treated as dependency changes: the hook denies them once and r
- EXTRA-L1-0011 (EXTRA; closest ARC-020, ARC-001, GOV-017): Changing the project reference graph is Reserved unless it implements the approved layout: every dotnet add/remove reference and dotnet reference add/remove command requires user confirmation, and removing or moving a .csproj is reported as
- EXTRA-L1-0012 (EXTRA; closest none): Level model of the instruction system: every artifact is placed by stability (0-core, 1-architecture, 2-technology, 3-project) and starts with a one-line header (Level, optional Capability/Facet, Owns, Scope, Loading); conformance dependenc
- EXTRA-L1-0013 (EXTRA; closest ARC-020, DEP-009): Static capability composition: exactly four slots (architecture required frame; persistence and backend-testing required leaves; frontend optional leaf); each required slot has exactly one selected implementation and the optional slot zero 
- EXTRA-L1-0014 (EXTRA; closest none): Hooks are registered in exec form (command node with the script path as argument data, no shell); the critical PreToolUse gate sets onFailure block so a missing script, crash, timeout or malformed input blocks the command; PostToolUse and S
- UNCERTAIN-L1-0001 (LINK_UNCERTAIN; closest GOV-015, DEP-007): Commit package.json and package-lock.json.
- EXTRA-L1-0015 (EXTRA; closest none): Instruction inventory integrity: the required workflow skills (development-workflow, project-structure, verify, code-review, build-fix, custom-settings, git-workflow, security-scan, add-dependency, architecture-decision, template-maintenanc
- EXTRA-L1-0016 (EXTRA; closest DEP-001, GOV-014): Remove dependencies that are no longer used when that is part of the current change and safe to verify; do not leave dead references.
- EXTRA-L1-0017 (EXTRA; closest WF-009): The add-dependency workflow reports package, version, license, vulnerability/deprecation result, target project and approvals obtained or still pending.
- EXTRA-L1-0018 (EXTRA; closest API-013, ARC-020): Adopting API versioning is Reserved and needs explicit approval, even when a concrete compatibility need exists.
- EXTRA-L1-0019 (EXTRA; closest GOV-017, GOV-007): Every approved Reserved decision is recorded as an ADR at docs/decisions/NNNN-<kebab-title>.md (Status Accepted with date, Approved by, Context, Decision, Consequences, Alternatives considered; docs/decisions/ created with the first ADR) an
- EXTRA-L1-0020 (EXTRA; closest WF-009): The architecture-decision workflow reports the decision, ADR path, decision files updated and follow-up work (structure, dependencies, migrations).
- EXTRA-L1-0021 (EXTRA; closest DEP-010, API-010): Register FluentValidation validators with the FluentValidation.DependencyInjectionExtensions package and follow the project's established invocation pattern instead of adding a competing mechanism.
- EXTRA-L1-0022 (EXTRA; closest WF-009): The build-fix report states the initial failure, root cause, changes made, backend build / frontend build / tests status (PASS, NOT RUN, NOT APPLICABLE) and remaining issues.
- EXTRA-L1-0023 (EXTRA; closest RUN-021, ARC-019): Do not cache tracked ORM entities across commit boundaries (named caching anti-pattern).
- EXTRA-L1-0024 (EXTRA; closest WF-011, WF-012): Code-review output gives for each finding severity, file/location, what is wrong, why it matters and the smallest reasonable fix, ordered by severity on the scale Critical (data loss, security vulnerability, reliably broken core behavior; b
- EXTRA-L1-0025 (EXTRA; closest WF-009): The custom-settings workflow reports the setting, old -> new value, every surface updated and the verify result.
- UNCERTAIN-L1-0002 (LINK_UNCERTAIN; closest GOV-015): High-risk Git operations (reset --hard, clean, push --force, push --force-with-lease, branch deletion, rebasing shared history) run only when explicitly requested or required by an approved workflow, and only after inspecting what will be l
- EXTRA-L1-0026 (EXTRA; closest WF-009): The development-workflow output summarizes what changed, Delegated decisions taken, open Decision Requests (Reserved) and the verify report.
- EXTRA-L1-0027 (EXTRA; closest GOV-015, GOV-019): Treat main, master and other protected or shared branches as non-rewritable.
- EXTRA-L1-0028 (EXTRA; closest WF-009): A pull request stays focused and its description states what changed, why, how it was verified, and compatibility or migration notes.
- EXTRA-L1-0029 (EXTRA; closest RUN-016, DEP-020): Do not wrap normal ORM operations in a generic application-level retry pipeline; use the provider's own execution strategy for transient database faults; HTTP retry policies are not database policies.
- EXTRA-L1-0030 (EXTRA; closest RUN-005): Never mutate a shared HttpClient's DefaultRequestHeaders concurrently; apply per-request values such as dynamic tokens per request or through a delegating handler.
- EXTRA-L1-0031 (EXTRA; closest DEP-008, DEP-023): global.json pins the intended SDK line: the current stable SDK of the target .NET release (no RC/preview unless explicitly requested) with a rollForward policy that allows normal patch/feature-band servicing.
- EXTRA-L1-0032 (EXTRA; closest WF-020, WF-009): Security-scan report shape: every report states the static-analysis limitation; uses the five-level severity scale Critical (sparingly) / High / Medium / Low / Info; each confirmed finding gives severity, file and location, title, evidence,
- EXTRA-L1-0033 (EXTRA; closest none): Loading and ownership placement of instruction content: always-needed planning policy goes into CLAUDE.md or an imported always rule; path-specific policy into a rule whose paths cover at least its scope; procedure obligations into the owni
- EXTRA-L1-0034 (EXTRA; closest GOV-017, GOV-005): Unclear-case test: any 'yes' makes a decision Reserved — does it add, remove or replace a dependency, framework or infrastructure capability; change a project/layer/reference boundary; establish a convention other code must follow; change o
- EXTRA-L1-0035 (EXTRA; closest RUN-009, DEP-023): Repository-wide Directory.Build.props enables nullable reference types and implicit usings for every .NET project (target framework net10.0).

## Unsupported file types

None: all template files are UTF-8 text.

## Check results

```
L1: 10/10 claimed complete batches; 86 file rows, 1682 coverage spans, 254 constraints
PASS: claimed completed batches have structural coverage (not semantic proof).
rc11=0
{
  "candidate": "L1",
  "template_files": 86,
  "text_files": 86,
  "nonblank_lines": 4279,
  "unclassified_nonblank_lines": 0,
  "oracle_policies": 196,
  "constraints": 254,
  "extra_constraints": 35,
  "uncertain_constraints": 2,
  "coverage_segments": 1682,
  "error_count": 0
}
PASS (STRUCTURE ONLY): L1. This is not semantic completeness proof.
rc12=0
{
  "candidate": "L1",
  "orphan_candidates": 55,
  "resolution_counts": {
    "DUPLICATE": 2,
    "EXTRA_REGISTERED": 35,
    "LINK_UNCERTAIN": 2,
    "NON_NORMATIVE": 16
  },
  "extra_constraints": 35,
  "uncertain_constraints": 2,
  "error_count": 0
}
PASS (STRUCTURE ONLY): L1. NOT a semantic exhaustion guarantee.
rc13=0
```

## Limitations

- Structural PASS (validators 11/12/13) is not semantic proof.
- All 196 policies are MATCHED; tightened modalities and extra gates are noted in search_notes instead of downgrading status.
- Hooks and checkers were analyzed statically, not executed.
- Two relations remain open (UNCERTAIN-L1-0001 'commit package.json and package-lock.json'; UNCERTAIN-L1-0002 'or required by an approved workflow').
- CANDIDATE.md was read as provenance only; classifications rest on the template text.
- Identifier numbers are local to this run.

