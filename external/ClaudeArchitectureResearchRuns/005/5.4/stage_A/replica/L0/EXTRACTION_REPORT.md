# L0 — Extraction report (Claude Run 2, blind replica)

## Scope and method

- Snapshot: `inputs/L0/output/template/` (71 files, 71 UTF-8 text, 0 binary/non-UTF-8, 4621 nonblank lines); queue `stage_A/_control/L0_WORK_QUEUE.json` (12 batches) used read-only.
- Oracle: `inputs/L0/source/inventory.json` (194) + `shared-research-invariants.json` (2) = 196 IDs.
- Every file was read in full; annotations were written per batch in `_annotations/B###.ann`, compiled by `stage_A/replica/_tools/build.py` (exact-quote verification, coverage/overlap checks, back-links) and checkpointed with `11_REPLICA_WORK_QUEUE_AND_PROGRESS.py` after each batch.
- Blindness: no file under stage_A/primary, stage_A/independent, stage_A/reconciled, work/, 5.3 or any other run was opened. CANDIDATE.md was read for provenance only.

## Counts

- Files inventoried: 71; completed batches: 12/12
- Coverage segments: 1602 — DUPLICATE 30, EXTRA 70, IMPLEMENTATION 87, MIXED 32, NON_NORMATIVE 854, ORACLE_LINKED 529
- Uncovered nonblank lines: 0 (enforced by build.py and validator 12)
- Policies: 196 — MATCHED 196, PARTIAL 0, NOT_EVIDENCED 0, UNCERTAIN 0
- Constraints: 248 — ORACLE_LINKED 216, EXTRA 30, LINK_UNCERTAIN 2
- Orphan ledger: 51 rows — DUPLICATE 2, EXTRA_REGISTERED 30, LINK_UNCERTAIN 2, NON_NORMATIVE 17

## Policy status detail

- PARTIAL: none
- NOT_EVIDENCED: none
- UNCERTAIN: none

## EXTRA constraints (summary)

- EXTRA-L0-0001 (EXTRA; closest ARC-020, ARC-001, GOV-017): Project-reference graph changes: every 'dotnet add/remove ... reference' and 'dotnet reference add/remove' command is blocked before it runs; references mapped by layout.md follow project-structure, any other reference-graph change needs a 
- EXTRA-L0-0002 (EXTRA; closest WF-009, DEP-004): Every dependency change reports the results of its version, deprecation, vulnerability and license checks (hook feedback: 'report them'; add-dependency report).
- EXTRA-L0-0003 (EXTRA; closest none): Level model of the instruction system: every instruction artifact carries a header (Level, Owns, Scope, Loads, Depends on); rules live in level directories with paths front matter; conformance dependencies ('Depends on') point only to the s
- EXTRA-L0-0004 (EXTRA; closest DEP-004, DEP-020, DEP-010): Packages Microsoft.Extensions.Http.Polly and Polly.Extensions.Http (deprecated resilience integrations) and Serilog.Sinks.Elasticsearch (deprecated sink) must not be added; they are reported on every manifest validation.
- EXTRA-L0-0005 (EXTRA; closest DEP-010, DEP-004): Do not adopt a deprecated or legacy ASP.NET automatic-validation integration package (FluentValidation.AspNetCore) unless a concrete project requirement justifies it; deviation needs a recorded decision or reported reason.
- EXTRA-L0-0006 (EXTRA; closest none): Placement and ownership of instruction content: rule = normative constraint, workflow skill = procedure, knowledge skill = technique (never the sole owner of a rule), product files = inputs, hooks/scripts/config = deterministic enforcement;
- EXTRA-L0-0007 (EXTRA; closest none): Hook registration form: hooks are registered in exec form (command node, args with the ${CLAUDE_PROJECT_DIR} placeholder, no shell); PreToolUse Bash|PowerShell runs pre-bash with onFailure block; PostToolUse and PostToolUseFailure Bash|Powe
- EXTRA-L0-0008 (EXTRA; closest GOV-017, GOV-007): Accepted decisions are recorded in the decision summary of their level (architecture decisions in overview.md, project/stack decisions in decisions.md) with date, decision, scope, consequences and the owning rule updated; approved exception
- EXTRA-L0-0009 (EXTRA; closest DEP-010, API-010): Application-level validators live in Application and are registered with FluentValidation.DependencyInjectionExtensions from Application's own registration.
- UNCERTAIN-L0-0001 (LINK_UNCERTAIN; closest GOV-015, DEP-007): Commit package.json and package-lock.json and keep the lockfile consistent with every change.
- EXTRA-L0-0010 (EXTRA; closest DEP-001, DEP-006): Removing a dependency removes the project reference and, when no project uses it any more, its central version in Directory.Packages.props, then rebuilds and runs the affected tests.
- EXTRA-L0-0011 (EXTRA; closest API-013, ARC-020): Adopting API versioning is Reserved and needs explicit approval, even when a concrete compatibility need exists.
- EXTRA-L0-0012 (EXTRA; closest WF-009, GOV-017): Decision reporting: Delegated decisions taken are mentioned in the report, and a rejected Decision Request is not recorded as a decision but mentioned in the report.
- EXTRA-L0-0013 (EXTRA; closest WF-009): The build-fix report states the initial failure, root cause, changes made, backend build / frontend build / tests status (PASS, NOT RUN, NOT APPLICABLE) and remaining issues.
- EXTRA-L0-0014 (EXTRA; closest WF-011, WF-012): Code-review findings are reported ordered by severity with severity, file/location, problem, why it matters and smallest reasonable fix, on the scale Critical (data loss, security vulnerability, reliably broken core behavior; blocks merge),
- EXTRA-L0-0015 (EXTRA; closest RUN-021, ARC-019): Do not cache EF tracked entities across Unit of Work boundaries (named caching anti-pattern).
- EXTRA-L0-0016 (EXTRA; closest PST-009, PST-010): Schema changes are created as new EF Core migrations from the Infrastructure project with the Api project as startup project.
- EXTRA-L0-0017 (EXTRA; closest WF-009, GOV-017): The development-workflow report summarizes what changed, the verify result block, unresolved Decision Requests and remaining known issues.
- UNCERTAIN-L0-0002 (LINK_UNCERTAIN; closest GOV-015): git reset --hard, git clean, git push --force / --force-with-lease, branch deletion and rebasing shared history are performed only when explicitly requested or clearly required by an approved workflow, after inspecting what will be lost or 
- EXTRA-L0-0018 (EXTRA; closest GOV-015, GOV-019): Treat main, master and other protected/shared branches as non-rewritable.
- EXTRA-L0-0019 (EXTRA; closest WF-009): A pull request has a focused purpose and its description explains what changed, why, how it was verified, and compatibility/migration notes.
- EXTRA-L0-0020 (EXTRA; closest RUN-002, ARC-017): Do not make fire-and-forget EF Core async calls (named anti-pattern).
- EXTRA-L0-0021 (EXTRA; closest RUN-016, DEP-020): Do not wrap normal EF Core operations in a generic application-level retry pipeline; prefer the provider's EF Core execution strategy (e.g. EnableRetryOnFailure for SQL Server) and follow provider guidance for transaction/retry interaction.
- EXTRA-L0-0022 (EXTRA; closest RUN-005): Never mutate a shared HttpClient's DefaultRequestHeaders concurrently; apply per-request values such as dynamic tokens per request or through a handler.
- EXTRA-L0-0023 (EXTRA; closest DEP-008, DEP-023): Scaffolding creates global.json pinning the intended SDK line: the current stable SDK of the target release (no preview/RC line unless approved) with a rollForward policy that allows normal patch/feature-band servicing.
- EXTRA-L0-0024 (EXTRA; closest WF-020, WF-009): Security-scan report shape: every report states the static-analysis limitation; severity uses the five levels Critical (sparingly) / High / Medium / Low / Info; each confirmed finding gives severity, file and location, title, evidence, why 
- EXTRA-L0-0025 (EXTRA; closest none): template-maintenance runs only when the user invokes it (disable-model-invocation; never started automatically), and maintenance keeps the always-loaded surface compact (CLAUDE.md plus the two imported decision summaries; the checker prints
- EXTRA-L0-0026 (EXTRA; closest none): Instruction inventory and model integrity: the required workflow skills (project-structure, verify, code-review, build-fix, custom-settings, git-workflow, security-scan, add-dependency, architecture-decision, template-maintenance) and knowl
- EXTRA-L0-0027 (EXTRA; closest none): Normative vocabulary: 'must / must not' violations are defects; a 'default' may be deviated from only with a concrete reason and the deviation must be reported; 'prefer / avoid' are guidance; 'requires approval' marks a Reserved decision.
- EXTRA-L0-0028 (EXTRA; closest GOV-017, GOV-005): Unclear-case test: any 'yes' makes a choice Reserved — does it add, remove or replace a dependency, framework or infrastructure capability; change a project/layer/reference boundary; establish a convention other code is expected to follow; 
- EXTRA-L0-0029 (EXTRA; closest GOV-018): Instruction precedence: engineering policy lives in the instruction system; a more volatile level may refine a more stable level but must not contradict it; when a contradiction is found it is reported instead of choosing a side.
- EXTRA-L0-0030 (EXTRA; closest RUN-009, DEP-023): Repository-wide Directory.Build.props enables nullable reference types, implicit usings and the latest analysis level for every .NET project.

## Unsupported file types

None: all template files are UTF-8 text.

## Check results

```
L0: 12/12 claimed complete batches; 71 file rows, 1602 coverage spans, 248 constraints
PASS: claimed completed batches have structural coverage (not semantic proof).
rc11=0
{
  "candidate": "L0",
  "template_files": 71,
  "text_files": 71,
  "nonblank_lines": 4621,
  "unclassified_nonblank_lines": 0,
  "oracle_policies": 196,
  "constraints": 248,
  "extra_constraints": 30,
  "uncertain_constraints": 2,
  "coverage_segments": 1602,
  "error_count": 0
}
PASS (STRUCTURE ONLY): L0. This is not semantic completeness proof.
rc12=0
{
  "candidate": "L0",
  "orphan_candidates": 51,
  "resolution_counts": {
    "DUPLICATE": 2,
    "EXTRA_REGISTERED": 30,
    "LINK_UNCERTAIN": 2,
    "NON_NORMATIVE": 17
  },
  "extra_constraints": 30,
  "uncertain_constraints": 2,
  "error_count": 0
}
PASS (STRUCTURE ONLY): L0. NOT a semantic exhaustion guarantee.
rc13=0
```

## Limitations

- Structural PASS (validators 11/12/13) is not semantic proof.
- All 196 policies are MATCHED; tightened modalities and extra gates are noted in search_notes instead of downgrading status.
- Hooks and checkers were analyzed statically, not executed.
- Two relations remain open (UNCERTAIN-L0-0001 'commit package.json and package-lock.json'; UNCERTAIN-L0-0002 'clearly required by an approved workflow').
- CANDIDATE.md was read as provenance only; classifications rest on the template text.
- Identifier numbering has gaps where constraints were merged during annotation; IDs are local to this run.

