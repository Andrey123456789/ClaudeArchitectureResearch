# K1 — Extraction report (Claude Run 2, blind replica)

## Scope and method

- Snapshot: `inputs/K1/output/template/` (87 files, 87 UTF-8 text, 0 binary/non-UTF-8, 5514 nonblank lines); queue `stage_A/_control/K1_WORK_QUEUE.json` (13 batches) used read-only.
- Oracle: `inputs/K1/source/inventory.json` (194) + `shared-research-invariants.json` (2) = 196 IDs.
- Every file was read in full; annotations were written per batch in `_annotations/B###.ann`, compiled by `stage_A/replica/_tools/build.py` (exact-quote verification, coverage/overlap checks, back-links) and checkpointed with `11_REPLICA_WORK_QUEUE_AND_PROGRESS.py` after each batch.
- Blindness: no file under stage_A/primary, stage_A/independent, stage_A/reconciled, work/, 5.3 or any other run was opened. CANDIDATE.md was read for provenance only.

## Counts

- Files inventoried: 87; completed batches: 13/13
- Coverage segments: 1730 — DUPLICATE 35, EXTRA 109, IMPLEMENTATION 141, MIXED 41, NON_NORMATIVE 807, ORACLE_LINKED 597
- Uncovered nonblank lines: 0 (enforced by build.py and validator 12)
- Policies: 196 — MATCHED 196, PARTIAL 0, NOT_EVIDENCED 0, UNCERTAIN 0
- Constraints: 386 — ORACLE_LINKED 338, EXTRA 45, LINK_UNCERTAIN 3
- Orphan ledger: 90 rows — DUPLICATE 6, EXTRA_REGISTERED 45, LINK_UNCERTAIN 3, NON_NORMATIVE 15, POLICY_LINKED 21

## Policy status detail

- PARTIAL: none
- NOT_EVIDENCED: none
- UNCERTAIN: none

## EXTRA constraints (summary)

- EXTRA-K1-0001 (EXTRA; closest ARC-020, DEP-009): Static capability composition: each required slot (architecture frame, persistence leaf, backend-testing leaf) has exactly one implementation (persistence with exactly one provider variant); the optional frontend slot has zero or one; selec
- EXTRA-K1-0002 (EXTRA; closest none): A slot implementation must provide every required item listed in its slot CONTRACT.md (architecture: role-map, dependency-direction, domain-modeling, use-case-orchestration, commit-boundary-placement, composition-root, transport-contracts, 
- EXTRA-K1-0003 (EXTRA; closest none): Non-slot artifacts refer to slot concerns through each slot's stable role vocabulary (architecture: Domain, Application, Infrastructure, Api, Application Service, repository contract, Unit of Work/IUnitOfWork, test projects) rather than thr
- EXTRA-K1-0004 (EXTRA; closest none): Frame/leaf ownership: placement (project roles, commit-boundary placement, composition, test-project placement and references) belongs to the architecture frame; technique belongs to the leaf slots (persistence, backend-testing), which decl
- EXTRA-K1-0005 (EXTRA; closest none): Facet locations are role-named and fixed: every implementation of a slot provides exactly the slot's listed facet locations (DEC row in the decision register, STD rule file, KNW facet, WF reference/skill, ENF facet script), file names never
- EXTRA-K1-0006 (EXTRA; closest none): Framework-neutral standards (rules/backend-tests/testing.md; rules/frontend/frontend.md, rules/frontend/security.md, rules/frontend/dependencies.md) stay unchanged when a slot implementation is replaced.
- EXTRA-K1-0007 (EXTRA; closest ARC-020, DEP-002, GOV-017): A persistence provider change is a variant change inside the persistence slot, not a new slot; replacing the persistence implementation requires every contract item, and an item the proposed implementation cannot provide (e.g. a migration m
- EXTRA-K1-0008 (EXTRA; closest DEP-001, DEP-003): Dependency-removal commands (npm/pnpm uninstall|remove|rm|r|un|unlink, yarn remove, dotnet remove package, dotnet package remove) are blocked before execution and routed to the add-dependency workflow (removal); deleting a frontend package.
- EXTRA-K1-0009 (EXTRA; closest ARC-001, ARC-020, ARC-028, GOV-017): Every .NET project-reference change (dotnet add|remove reference, dotnet reference add|remove, or a .csproj ProjectReference edit) is a Reserved decision: it is blocked or flagged as an error unless each edge appears as `From -> To` in a da
- EXTRA-K1-0010 (EXTRA; closest PST-009, PST-010): If the schema changes, a new migration is created (persistence-change); when persistence model files (Domain .cs, Infrastructure/Persistence/Configurations/*.cs, Infrastructure/Persistence/*DbContext.cs) change without any migration change,
- EXTRA-K1-0012 (EXTRA; closest none): Every instruction artifact is classified in the order Capability -> Kind -> Scope: capability-owned artifacts declare Capability: <slot>/<implementation> (others Capability: —); Kind (OP, DEC, STD, KNW, WF, ENF, IN) decides mechanism and lo
- EXTRA-K1-0013 (EXTRA; closest none): Instruction dependency direction is WF -> KNW -> STD -> DEC -> OP and ENF -> STD/DEC; each ENF artifact declares what it conforms to on a Conforms: line directly after its header.
- EXTRA-K1-0014 (EXTRA; closest none): Single owner per topic: each rule/topic lives in the artifact recorded as its owner in the map (Owns / Extend here when / Where does a topic live), new content is added at its owner, and the map is updated whenever an artifact is added, mov
- EXTRA-K1-0015 (EXTRA; closest GOV-017): Changes to the instruction system go through the user-invoked template-maintenance workflow, and changing a slot contract is a Reserved decision (rare).
- EXTRA-K1-0017 (EXTRA; closest API-013, DEP-017, ARC-020): Adopting API versioning is a Reserved decision (explicit approval required, per CLAUDE.md).
- EXTRA-K1-0016 (EXTRA; closest PST-003, ARC-019): EF Core persistence code is organised under backend/<Name>.Infrastructure/Persistence/: the DbSeeder in Persistence/Seeding/, migrations in Persistence/Migrations/, entity configurations in Persistence/Configurations/ and the DbContext file
- EXTRA-K1-0011 (EXTRA; closest none): When instruction files change (CLAUDE.md, docs/architecture/decision-register.md, .claude/** except settings.local.json), the instruction-structure checker runs and its errors are fed back to the agent for correction through the template-ma
- EXTRA-K1-0018 (EXTRA; closest none): Path-scoped standards live directly in .claude/rules/<scope>/ using only the scope directories common, backend, backend-tests, frontend, delivery (no deeper hierarchy); the header Scope equals the directory; every rule declares frontmatter 
- EXTRA-K1-0019 (EXTRA; closest none): CLAUDE.md must @-import the decision register; only OP/DEC artifacts may be @-imported into the always-loaded surface, every import must resolve, and no Markdown file other than CLAUDE.md may contain @ imports.
- EXTRA-K1-0020 (EXTRA; closest none): Skill inventory and structure: every skill directory has a SKILL.md whose frontmatter name equals the directory name and which has a description (warning above 450 characters: keep concise and trigger-first); required workflows (project-str
- EXTRA-K1-0021 (EXTRA; closest none): Instruction references must resolve: no references to unknown skills, no unresolved or ambiguous file references; skill-private references/ files are used only by their owning skill; conformance dependencies must not form cycles.
- EXTRA-K1-0022 (EXTRA; closest none): Hook configuration: settings.json registers only and all of PreToolUse, PostToolUse, PostToolUseFailure and Stop; each hook uses exec form (command node with args [${CLAUDE_PROJECT_DIR}/.claude/hooks/dispatch.cjs, <event>]) without shell-va
- EXTRA-K1-0023 (EXTRA; closest none): Normative text in OP, DEC and STD artifacts avoids the ambiguous word 'normally' and uses must/default/prefer vocabulary instead.
- EXTRA-K1-0024 (EXTRA; closest none): The always-loaded surface (CLAUDE.md, its imports, names/descriptions of model-invocable skills and agent descriptions) stays near a 5k-token target; above about 6000 estimated tokens a warning is raised.
- EXTRA-K1-0025 (EXTRA; closest DEP-020, DEP-004): The NuGet packages Microsoft.Extensions.Http.Polly and Polly.Extensions.Http are denied as deprecated resilience integration packages (error in project files and in Directory.Packages.props).
- UNCERTAIN-K1-0002 (LINK_UNCERTAIN; closest DEP-002, DEP-001, ARC-020): Before adding a dependency, the choice must match the decision register's approved stack; anything else goes through architecture-decision first.
- EXTRA-K1-0026 (EXTRA; closest DEP-011, ARC-002): Mapster (with Mapster.DependencyInjection) is never referenced from Domain.
- EXTRA-K1-0027 (EXTRA; closest DEP-001, GOV-014): Remove dependencies that are no longer used when doing so is part of the current change and safe to verify; do not leave dead package references behind.
- EXTRA-K1-0028 (EXTRA; closest DEP-004, DEP-005, WF-009): After a dependency change, build and run affected tests (verify) and report the package, version, license, due-diligence results and any approval obtained or pending.
- EXTRA-K1-0032 (EXTRA; closest GOV-017, GOV-007): For a consequential or non-obvious accepted decision, add a docs/decisions/NNNN-short-title.md record (context, decision, alternatives considered, consequences, date, approver).
- EXTRA-K1-0033 (EXTRA; closest GOV-017, WF-009): The architecture-decision workflow reports the decision, its class, the approval source, register/record updates and any request still unresolved.
- EXTRA-K1-0034 (EXTRA; closest DEP-010, DEP-004, API-010): Register FluentValidation validators with FluentValidation.DependencyInjectionExtensions and do not add deprecated/legacy ASP.NET automatic-validation integration packages.
- EXTRA-K1-0035 (EXTRA; closest RUN-021, ARC-017): Never cache tracked persistence entities across Unit of Work boundaries.
- EXTRA-K1-0036 (EXTRA; closest GOV-021, WF-009): The custom-settings report lists the setting, old -> new value, every updated surface, any migration created and the verify result.
- EXTRA-K1-0037 (EXTRA; closest WF-009, GOV-017): The development-workflow final report summarizes what changed and why, the verify report, approvals obtained and every unresolved Decision Request.
- EXTRA-K1-0038 (EXTRA; closest RUN-002, ARC-022): Never fire-and-forget EF Core asynchronous operations; a DbContext is not thread-safe.
- EXTRA-K1-0039 (EXTRA; closest RUN-016, DEP-020): Do not wrap normal database operations in a generic application-level retry pipeline or apply an HTTP retry policy to them; database transient faults use the persistence provider's execution strategy (EnableRetryOnFailure), with explicit tr
- UNCERTAIN-K1-0003 (LINK_UNCERTAIN; closest GOV-015): High-risk Git operations may be performed when 'clearly required by an approved workflow', not only when explicitly requested.
- EXTRA-K1-0040 (EXTRA; closest GOV-015): Treat main, master and other protected/shared branches as non-rewritable.
- EXTRA-K1-0041 (EXTRA; closest WF-009): A pull request description explains what changed, why, how it was verified and compatibility/migration notes.
- EXTRA-K1-0042 (EXTRA; closest RUN-005): Apply per-request values such as dynamic access tokens to the specific request or through a handler; never mutate a shared HttpClient's DefaultRequestHeaders concurrently.
- EXTRA-K1-0044 (EXTRA; closest TST-007, PST-009): Add or update persistence/integration tests when provider behavior, mappings, constraints or non-trivial queries changed.
- EXTRA-K1-0045 (EXTRA; closest PST-010, WF-009): The persistence-change report lists model changes, migration name and review notes (destructive operations called out), seeder updates and verification results.
- UNCERTAIN-K1-0004 (LINK_UNCERTAIN; closest GOV-015, DEP-007): Frontend scaffolding ends with 'Verify with the workspace's declared scripts ... and commit package-lock.json'.
- EXTRA-K1-0046 (EXTRA; closest DEP-008): The repository includes a global.json pinning the intended supported SDK line: the current stable SDK for the target .NET release (no RC/preview unless explicitly requested), with servicing allowed by the chosen rollForward policy.
- EXTRA-K1-0047 (EXTRA; closest none): Normative vocabulary: must / must not — a violation is a defect; Default — deviation needs a concrete reason and must be reported; Prefer / avoid — guidance; Requires approval — a Reserved decision.
- EXTRA-K1-0048 (EXTRA; closest GOV-017, ARC-020): Unclear decisions are Reserved if any answer is yes: (1) adds, removes or replaces a dependency, framework or infrastructure capability; (2) changes a project/layer/reference boundary; (3) establishes a convention other code is expected to 
- EXTRA-K1-0049 (EXTRA; closest DEP-023, RUN-009): Shared build configuration enables Nullable reference types and ImplicitUsings for every .NET project below the repository root.

## Unsupported file types

None: all template files are UTF-8 text.

## Check results

```
K1: 13/13 claimed complete batches; 87 file rows, 1730 coverage spans, 386 constraints
PASS: claimed completed batches have structural coverage (not semantic proof).
{
  "candidate": "K1",
  "template_files": 87,
  "text_files": 87,
  "nonblank_lines": 5514,
  "unclassified_nonblank_lines": 0,
  "oracle_policies": 196,
  "constraints": 386,
  "extra_constraints": 45,
  "uncertain_constraints": 3,
  "coverage_segments": 1730,
  "error_count": 0
}
PASS (STRUCTURE ONLY): K1. This is not semantic completeness proof.
{
  "candidate": "K1",
  "orphan_candidates": 90,
  "resolution_counts": {
    "DUPLICATE": 6,
    "EXTRA_REGISTERED": 45,
    "LINK_UNCERTAIN": 3,
    "NON_NORMATIVE": 15,
    "POLICY_LINKED": 21
  },
  "extra_constraints": 45,
  "uncertain_constraints": 3,
  "error_count": 0
}
PASS (STRUCTURE ONLY): K1. NOT a semantic exhaustion guarantee.
```

## Limitations

- Structural PASS from validators 11/12/13 proves coverage and referential integrity only, not semantic completeness.
- Policy statuses are judgments: all 196 policies are restated nearly verbatim in active surfaces, so all are MATCHED; strengthened modalities ('normally/should' -> 'must', e.g. API-012, API-019, TST-003) are noted in search_notes rather than downgraded.
- Hooks were analyzed statically; no candidate hook or script was executed.
- Three relations remain open (UNCERTAIN-K1-0002, -0003, -0004); they are not counted as EXTRA.
- Unused identifier gaps (EXTRA-K1-0029..0031, EXTRA-K1-0043, UNCERTAIN-K1-0001 converted to RULE-K1-0285) are intentional; IDs are local and not comparable across runs.
- Navigation-map and decision-guide tables were classified per table, not per row, after row-by-row reading.

