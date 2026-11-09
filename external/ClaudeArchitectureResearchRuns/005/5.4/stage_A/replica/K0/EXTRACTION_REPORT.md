# K0 — Extraction report (Claude Run 2, blind replica)

## Scope and method

- Snapshot: `inputs/K0/output/template/` (63 files, 63 UTF-8 text, 0 binary/non-UTF-8, 5183 nonblank lines); queue `stage_A/_control/K0_WORK_QUEUE.json` (13 batches) used read-only.
- Oracle: `inputs/K0/source/inventory.json` (194) + `shared-research-invariants.json` (2) = 196 IDs.
- Every file was read in full; annotations were written per batch in `_annotations/B###.ann`, compiled by `stage_A/replica/_tools/build.py` (exact-quote verification, coverage/overlap checks, back-links) and checkpointed with `11_REPLICA_WORK_QUEUE_AND_PROGRESS.py` after each batch.
- Blindness: no file under stage_A/primary, stage_A/independent, stage_A/reconciled, work/, 5.3 or any other run was opened. CANDIDATE.md was read for provenance only.

## Counts

- Files inventoried: 63; completed batches: 13/13
- Coverage segments: 1717 — DUPLICATE 37, EXTRA 73, IMPLEMENTATION 94, MIXED 32, NON_NORMATIVE 888, ORACLE_LINKED 593
- Uncovered nonblank lines: 0 (enforced by build.py and validator 12)
- Policies: 196 — MATCHED 196, PARTIAL 0, NOT_EVIDENCED 0, UNCERTAIN 0
- Constraints: 389 — ORACLE_LINKED 346, EXTRA 41, LINK_UNCERTAIN 2
- Orphan ledger: 66 rows — DUPLICATE 3, EXTRA_REGISTERED 41, LINK_UNCERTAIN 2, NON_NORMATIVE 11, POLICY_LINKED 9

## Policy status detail

- PARTIAL: none
- NOT_EVIDENCED: none
- UNCERTAIN: none

## EXTRA constraints (summary)

- EXTRA-K0-0001 (EXTRA; closest DEP-001, DEP-003): Dependency-removal commands (npm uninstall|remove|rm|r|un|unlink, pnpm/yarn remove, dotnet remove package, dotnet package remove, Uninstall-Package) are likewise denied until the add-dependency workflow has been completed and the command ca
- EXTRA-K0-0002 (EXTRA; closest ARC-001, ARC-020, ARC-028, GOV-017): Changing the project reference graph (dotnet add|remove reference, dotnet reference add|remove, or a .csproj ProjectReference change) is Reserved unless an accepted decision already requires the reference, even when the new reference would 
- EXTRA-K0-0003 (EXTRA; closest none): When instruction files change (CLAUDE.md, the decision register, .claude/** except .hook-state and settings.local.json), check-instructions runs and its errors are fed back to the agent.
- EXTRA-K0-0004 (EXTRA; closest none): Instruction artifacts are organized by two questions: the Kind (OP, DEC, STD, KNW, WF, ENF, IN) decides mechanism, location and loading; the Scope (common, backend, backend-tests, frontend, delivery, repo/meta) decides the directory and pat
- EXTRA-K0-0005 (EXTRA; closest none): Conformance dependencies point WF -> KNW -> STD -> DEC -> OP and ENF -> STD/DEC (declared in the header and Conforms to: lines); routing pointers (See also/Workflow/Technique/Procedure/Enforced by, workflow invocations, CLAUDE.md routing ta
- EXTRA-K0-0006 (EXTRA; closest none): The maintainer map lists every artifact with its owner, loading, enforcement and 'Extend here' routing; the Decision -> Affects view is generated from the register and must match it (verified by check-instructions).
- EXTRA-K0-0007 (EXTRA; closest ARC-002, DEP-011): Domain stays independent of mapping-library concerns (in addition to EF Core, ASP.NET Core, HTTP, persistence and external-service concerns).
- EXTRA-K0-0008 (EXTRA; closest RUN-009, RUN-024): Backend C# style rules: prefer primary constructors for simple DI/initialization (regular constructors when validation is non-trivial or the codebase uses them) and records where value semantics are intended (not every DTO/Domain type); kee
- UNCERTAIN-K0-0001 (LINK_UNCERTAIN; closest GOV-015, DEP-007): 'Commit package.json and package-lock.json, and keep the lockfile consistent with every dependency change.'
- EXTRA-K0-0009 (EXTRA; closest DEP-004, DEP-020, DEP-010): The NuGet packages Microsoft.Extensions.Http.Polly, Polly.Extensions.Http, Serilog.Sinks.Elasticsearch and FluentValidation.AspNetCore are reported as errors (deprecated; use Microsoft.Extensions.Http.Resilience, Elastic.Serilog.Sinks, Flue
- EXTRA-K0-0010 (EXTRA; closest none): Every instruction artifact carries the first-line header 'Kind
- EXTRA-K0-0011 (EXTRA; closest none): Standards live directly in .claude/rules/<scope>/<topic>.md for scopes common, backend, backend-tests, frontend, delivery; the header Scope equals the directory; STD loads path-scoped with non-empty paths whose globs stay inside the scope t
- EXTRA-K0-0012 (EXTRA; closest none): Skill and agent structure: skill frontmatter name equals the directory and has a concrete description (20+ characters); KNW skills load on demand and stay model-invocable; WF skills load as workflows; the required workflows (development-wor
- EXTRA-K0-0013 (EXTRA; closest none): Knowledge skills and their private references must not contain normative wording (must, never, requires approval) on a line without an owner reference (rules/, CLAUDE.md or a D-xx decision ID); the rule must be moved to its standard and poi
- EXTRA-K0-0014 (EXTRA; closest GOV-017): Exactly one decision register (docs/architecture/decision-register.md) carries Kind DEC and CLAUDE.md imports exactly it; register rows are 'D-xx
- EXTRA-K0-0015 (EXTRA; closest none): References must resolve: backticked file/skill/agent references and '§ section' references must point to existing targets and headings; unknown hyphenated skill/agent names in skill contexts are errors; skill-private references are used onl
- EXTRA-K0-0016 (EXTRA; closest none): Manual tool invocations in instruction files must be root-aware: node "$(git rev-parse --show-toplevel)/.claude/..." instead of a command relative to the current directory.
- EXTRA-K0-0017 (EXTRA; closest none): Hook configuration: every hook is a command hook in exec form (executable-only command, args [${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>, <event>] with the script present and handling the event), no variable expansion in arguments, a posi
- EXTRA-K0-0018 (EXTRA; closest DEP-010, DEP-004): Register FluentValidation validators with FluentValidation.DependencyInjectionExtensions; do not add a deprecated or legacy ASP.NET automatic-validation integration package without a concrete requirement.
- EXTRA-K0-0019 (EXTRA; closest DEP-001, GOV-014): Remove a dependency that is no longer used when that is part of the current change and safe to verify; do not leave dead references behind.
- EXTRA-K0-0020 (EXTRA; closest DEP-004, DEP-005, WF-009): The add-dependency output reports package, selected version and why, license, deprecation and vulnerability status, approval obtained (if needed), files changed and the verification result.
- EXTRA-K0-0021 (EXTRA; closest API-013, DEP-017, ARC-020): Adopting API versioning is Reserved (D-15).
- EXTRA-K0-0022 (EXTRA; closest GOV-017): Decision propagation: find everything a decision touches via its register entry and Affects list; after approval edit every artifact in Affects so each keeps only its own responsibility (standards cite the ID, knowledge adjusts technique, w
- EXTRA-K0-0023 (EXTRA; closest GOV-017, GOV-007): When rationale, alternatives or consequences need more than the register sentence add an ADR docs/decisions/NNNN-<slug>.md (Status, Date, Register, Context, Decision, Alternatives considered, Consequences) cited in Details in; superseding m
- EXTRA-K0-0024 (EXTRA; closest none): Changes to .claude/ instruction files are instruction-system maintenance: ask the user to run /template-maintenance for structural changes and run check-instructions after any instruction edit.
- EXTRA-K0-0025 (EXTRA; closest GOV-017, WF-009): The architecture-decision output is the Decision Request (when pending) or the recorded outcome: register entry, ADR path if any, artifacts updated, checker result.
- EXTRA-K0-0026 (EXTRA; closest RUN-021, ARC-017): Caching EF tracked entities across Unit of Work boundaries is listed as a mistake to avoid.
- EXTRA-K0-0027 (EXTRA; closest WF-009): The delivery-pipeline output lists files changed, stages and the commands they run, what was verified and any hosting-platform assumption still needing confirmation.
- EXTRA-K0-0028 (EXTRA; closest WF-009, GOV-017): The development-workflow output states what changed and why, the Delegated decisions taken, Decision Requests raised or still unresolved, and the verification report.
- EXTRA-K0-0029 (EXTRA; closest RUN-002, ARC-022): Fire-and-forget EF Core asynchronous operations are listed as a mistake to avoid.
- EXTRA-K0-0030 (EXTRA; closest GOV-015): Treat main, master and other protected or shared branches as non-rewritable.
- EXTRA-K0-0031 (EXTRA; closest WF-009): A PR describes what changed, why, how it was verified and any compatibility or migration notes.
- UNCERTAIN-K0-0002 (LINK_UNCERTAIN; closest GOV-015): High-risk Git operations may run when 'required by an approved workflow', not only when explicitly requested.
- EXTRA-K0-0032 (EXTRA; closest RUN-016, DEP-020): Do not wrap normal EF Core operations in a generic application-level retry pipeline; prefer the provider's EF Core execution strategy for transient retry and handle transaction/retry interaction per provider guidance; HTTP retry policies ar
- EXTRA-K0-0033 (EXTRA; closest RUN-005): Per-request values such as dynamic access tokens go on the request or through a handler; mutating a shared client's DefaultRequestHeaders concurrently for request-specific values is a race (stable media-type headers may be configured on the
- EXTRA-K0-0034 (EXTRA; closest DEP-008, DEP-022, DEP-023): Scaffolding creates the repository-wide files global.json (pinning the intended supported .NET SDK line: current stable SDK of the target release with a chosen rollForward servicing policy), .editorconfig, .gitignore and README.md alongside
- EXTRA-K0-0035 (EXTRA; closest none): Keep the always-loaded surface (CLAUDE.md, the register, skill descriptions) compact and move detail to the owner it belongs to.
- EXTRA-K0-0036 (EXTRA; closest none): When hooks or scripts change, exercise them with a sample payload (e.g. a pre-tool-use JSON for 'npm install lodash').
- EXTRA-K0-0037 (EXTRA; closest WF-009): Template maintenance summarizes what moved, the new owners and the checker result.
- EXTRA-K0-0038 (EXTRA; closest none): Instruction precedence: CLAUDE.md and the decision register govern every task; standards govern the files they cover; workflows own procedures; knowledge skills supply technique and never override a standard.
- EXTRA-K0-0039 (EXTRA; closest none): Vocabulary: must / must not — a violation is a defect; default — deviation needs a concrete reason and must be reported; prefer / avoid — guidance; requires approval — a Reserved decision.
- EXTRA-K0-0040 (EXTRA; closest GOV-017, ARC-020): Unclear decisions are Reserved if any answer is yes: adds, removes or replaces a dependency, framework or infrastructure capability; changes a project, layer or reference boundary; establishes a convention other code must follow; changes ob
- EXTRA-K0-0041 (EXTRA; closest DEP-023, RUN-009): Shared build configuration enables Nullable reference types, ImplicitUsings and AnalysisLevel latest for every .NET project below the root.

## Unsupported file types

None: all template files are UTF-8 text.

## Check results

```
K0: 13/13 claimed complete batches; 63 file rows, 1717 coverage spans, 389 constraints
PASS: claimed completed batches have structural coverage (not semantic proof).
{
  "candidate": "K0",
  "template_files": 63,
  "text_files": 63,
  "nonblank_lines": 5183,
  "unclassified_nonblank_lines": 0,
  "oracle_policies": 196,
  "constraints": 389,
  "extra_constraints": 41,
  "uncertain_constraints": 2,
  "coverage_segments": 1717,
  "error_count": 0
}
PASS (STRUCTURE ONLY): K0. This is not semantic completeness proof.
{
  "candidate": "K0",
  "orphan_candidates": 66,
  "resolution_counts": {
    "DUPLICATE": 3,
    "EXTRA_REGISTERED": 41,
    "LINK_UNCERTAIN": 2,
    "NON_NORMATIVE": 11,
    "POLICY_LINKED": 9
  },
  "extra_constraints": 41,
  "uncertain_constraints": 2,
  "error_count": 0
}
PASS (STRUCTURE ONLY): K0. NOT a semantic exhaustion guarantee.
```

## Limitations

- Structural PASS (validators 11/12/13) is not semantic proof.
- All 196 policies are MATCHED; tightened modalities and extra gates are noted in search_notes instead of downgrading status.
- Hooks were analyzed statically, not executed.
- Two relations remain open (UNCERTAIN-K0-0001 'Commit package.json and package-lock.json'; UNCERTAIN-K0-0002 'required by an approved workflow').
- Identifier numbering has gaps only where constraints were merged during annotation; IDs are local to this run.

