# Audit A — Phase 5.3 freeze readiness

| Candidate | Verdict | Principal qualification |
|---|---|---|
| M | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | Finite enforcement evidence; U-01–U-07 remain. |
| M1 | BLOCKED | A-001: ARC-025 exception weakens mandatory boundary. |
| L0 | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | Strict P4 passed; host/replacement conditions remain untested. |
| L1-Restart | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | Strict P4 passed; PAR-003/006 assessed separately. |
| K0 | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | A-L01 comment-only XML false positive; nonblocking limitation. |
| K1 | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | A-L02 two stale input-manifest entries; current authority available. |

## Authority, coverage and integrity

The normalized local inventory and two invariants control the common contract, not the strictest candidate or a self-reported PASS. Actual counts are 194 distinct inventory IDs in 10 groups plus GOV-017/GOV-018 (MUST), totaling 196 unique IDs. All six 43-file source trees are byte-identical. Every current CANDIDATE.md equals baseline/CANDIDATE.md, and all baseline TASK.md copies agree. Essential local inputs exist. The unavailable historical research citation does not remove the locally embedded invariant authority.

The CSV is a static clause-level evidence map, not 196/196 executed passes. SAME means the cited current owner expresses an equivalent obligation under the recorded trigger/scope and chosen stack; it does not certify live delivery or generated behavior. DIFFERENT identifies an extra exception/constraint relative to the normalized rule. UNVERIFIED preserves unresolved force/exception wording. Conditional policies remain represented when dormant in an empty template. Comparison assumes identical specification, repository, .NET/C#/SQL Server/NUnit/Angular selection, acceptance tests and model. An optional frontend slot never licenses ignoring an explicit Angular product requirement.

Candidate specifications, phase tasks, provenance, final templates including hidden files, and selected refinement change explanations were inspected. Reports supplied claims, never independent PASS proof. Per-policy evidence is in report 03; before/after manifests and exact command records are in report 04. Lexical retrieval helped locate paragraphs; scores, filenames, counts and candidate coverage maps were not themselves semantic proof. Split neutral/technology rules were considered together with imported decisions and workflow context. Complete technique-example preservation and live delivery remain explicit limitations.

## Six independent candidate assessments

### M — FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS

The flat topical design is present: M/CANDIDATE.md; M/output/template/CLAUDE.md:150, .claude/rules/, and imported docs/technology-stack.md. No Levels, Kinds or capabilities are imposed on M. Current owner evidence represents the common contracts, including ARC-025 at architecture.md:158. Actual pristine instruction/manifest checkers passed. A quiet pinned-package/reference pre-hook is consistent with its stronger post-state validation, not proof due diligence is optional. PostToolUseFailure probes reported all tested invalid versions and outward references. PAR-002 is a parity-only extra eligibility condition; U-01–U-07 constrain certification.

### M1 — BLOCKED

Four static slots are present: architecture/clean-architecture, persistence/ef-core with sqlserver, backend-testing/nunit, optional frontend currently angular. docs/capability-selection.md, imported docs/capabilities/*.md, four CONTRACT/MODULE pairs and facet references expose current selections. Pristine structural and XML/hook tests pass, but do not detect A-001's normative exception. A-001 satisfies all five blocker criteria independently of parity analysis. PAR-002/PAR-005 are separately counted comparability observations. Replacement and exhaustive V2 preservation remain unverified.

### L0 — FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS

The 0-core -> 1-architecture -> 2-technology -> 3-project organization, imported overview/decisions and absence of capability slots match L0/CANDIDATE.md. The actual checker is L0/output/template/.claude/tools/check-instructions.mjs. Strict P4 forbids concrete technology names even in pointers. Every actual L0 lexicon representative and six named Architecture probes was rejected; neutral controls passed. Documented fixed-platform vocabulary does not authorize a Docker pointer exemption. XML/failure-event and legal-direction probes passed in their bounded sense. No confirmed hard violation; U-01–U-07 remain.

### L1-Restart — FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS

The current branch is L1-Restart; inherited L1 wording in README/provenance does not authorize auditing the abandoned sibling. Levels plus four static slots/facets, adopted-frame imports, project decisions and frontend selection are present. The final accepted strict P4 decision controls over older context-sensitive exemptions. All actual L0 prohibited vocabulary representatives were rejected. Technique: backend-testing.framework was rejected in Architecture for reverse conformance; the one reconfirmation using documented Framework binding syntax passed. This is fixture calibration, not a neutrality defect. PAR-003/PAR-006 are assessed separately; no independently confirmed hard violation.

### K0 — FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS

Seven Kinds, scope-first standards, one imported decision register and WF -> KNW -> STD -> DEC -> OP plus ENF -> STD/DEC match K0/CANDIDATE.md and current MAP/register. No capabilities or levels are demanded. Pristine structural/dependency checks passed; current owner/workflow evidence maps the normalized corpus. XML quote, direction and failure-event probes pass except A-L01's comment-only false positive. That known failure is preserved in the ledger. A governing hard requirement establishing this particular false rejection as a material freeze blocker was not demonstrated. PAR-002 and U-01–U-07 remain.

### K1 — FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS

Capability -> Kind -> Scope, seven Kinds, one decision register, four slots, required leaf-to-frame binds and current selected facets match K1/REFINEMENT_TASK.md:25 onward. K1/output/template/.claude/scripts/check-instructions.cjs:26–29 declares the slot model; :504 onward checks binds. Pristine checks and failure/XML/direction probes passed. Legal Application -> Domain still triggers an absent-recorded-approval diagnostic; that is governance, not an outward-direction error. A-L02's two stale root-input manifest entries do not change the available current canonical sources. Approval-date tampering and full replacement scenarios were not independently executed.

## A-001 / PAR-001 — M1 remote HTTP boundary exception

SHARED_CONTRACT_VIOLATION; severity HIGH; confidence HIGH. One confirmed blocker, M1 only.

1. **Hard requirement:** M1/source/inventory.json#policygroups[id=architecture].policies[id=ARC-025], MUST/path/backend, prohibits leaking HttpResponseMessage or remote transport concerns into Application. M1/REFINEMENT_TASK.md:203 requires policy preservation; :206 forbids weakened semantic strength/conditions.
2. **Exact current evidence:** M1/output/template/.claude/rules/architecture.md:135–137 adds “into Application contracts unless the Application explicitly models HTTP.” Canonical ARC-025 has no such exception.
3. **Minimal reproduction:** compare that path-rule clause to the normalized JSON field. An Application explicitly modeling HTTP activates a permission absent from the canonical prohibition. This static contradiction does not require code generation.
4. **Expected/actual:** unconditional translation to Application-facing abstractions versus conditional permission to expose the remote response type/transport concerns.
5. **Material impact:** an identical supplier-adapter task could expose HttpResponseMessage in an Application service under M1 while other candidates require a neutral abstraction, altering coupling and review acceptance. No generated-code effect was measured.

**Contrary evidence:** architecture.md:53–55 keeps infrastructure details out of Application; :56–57 excludes persistence and ASP.NET Core transport types; httpclient-factory/SKILL.md:185 warns against HttpResponseMessage leakage. The remote System.Net.Http response type is not limited to the ASP.NET Core types named earlier. A specific exception in the normative owner remains unresolved by general abstraction language or a technique warning. GOV-017 does not expressly reserve this already-written exception for a new approval. No accepted local source authorizing relaxation was located.

**Disposition:** M1 BLOCKED. Restore the mandatory boundary in separately authorized correction; do not defer it solely as 5.4 parity work. No correction was made here.

## Confirmed nonblocking limitations

**A-L01 — K0 commented package false positive.** Severity LOW; confidence HIGH. K0/output/template/.claude/scripts/check-dependencies.cjs:75 onward scans start tags without excluding XML comments. Fixture at backend/App.Application/App.Application.csproj in a temp copy:

```xml
<Project Sdk="Microsoft.NET.Sdk"><ItemGroup><!-- <PackageReference Include="Example" Version="1.2.3" /> --></ItemGroup></Project>
```

Expected: no active Example package. The initial failure-event hook reports an active inline version; the one direct-checker reconfirmation exits 1 with “PackageReference Example has a version”. This can obstruct validation of valid commented XML. It is FAIL in the ledger and NONBLOCKING_LIMITATION under the five-part threshold: no applicable explicit hard requirement plus material impact sufficient for BLOCKED was established. No silent acceptance of an active violation or resulting generated-code defect is claimed.

**A-L02 — K1 stale optional input manifest.** Severity LOW; mismatch confidence HIGH; historical cause UNVERIFIED. K1/MANIFEST.sha256 disagrees with current GOAL_PROMPT.txt and REFINEMENT_TASK.md; one direct rehash confirmed both. REFINEMENT_TASK.md:7 explicitly supersedes prior execution wording without relaxing research requirements. Current accepted authority is available, CANDIDATE equals baseline, and normalized sources agree. PROVENANCE task_sha256 matches baseline/TASK.md. No unauthorized authoring history can be inferred from a stale manifest. All checked template entries match. Exact recorded/current hashes are in report 04.

## A3/A4 finite enforcement results

The 264 recorded subprocess fixtures comprise: 40 syntax runs; 6 pristine instruction checkers; 6 other pristine diagnostics; 24 pre-hook cases; 24 inline-version/comment post-failure cases; 24 project-direction cases; 24 central-version cases; 102 P4 cases; 6 missing-failure-hook negatives; 6 BOM inputs; 2 reconfirmations. PASS means the relevant diagnostic/permission matched the candidate contract, not merely exit zero. A nonzero response or interactive ask can be correct.

P4 exercised 41 representatives of actual L0 prohibited patterns in Core against both L candidates, plus Docker, Swagger, Jest, Scrutor, NuGet and EF Core in Architecture. Controls included technology-neutral prose and a neutral facet reference in both locations. L1's single invalid control expectation was corrected using its documented binding form. No pointer exemption was revived. L0/CANDIDATE.md:51 and :119 explicitly allow fixed .NET/C#/TypeScript vocabulary. Literal Git/protocol handling by a checker is not accepted as independent authority to widen that exception. A finite lexicon is not exhaustive natural-language technology recognition.

Both quote styles, multiline/reordered attributes, active inline/floating versions and Domain -> Infrastructure references were detected after failure by all six. Application -> Domain was not classified outward. Pinned central versions were not called floating. Other legitimate workflow/approval reminders can remain. K0 alone falsely rejected the observed comment-only package fixture. Custom targets/import evaluation remains outside demonstrated parser coverage.

## Explicit verification limits

| ID | Disposition | Material boundary |
|---|---|---|
| U-01 | NOT_RUN | Live Claude host execution, settings-schema acceptance, automatic loading and approval UI. Scripts were invoked with discovered settings arguments; no host launched. |
| U-02 | NOT_RUN | Physical linked worktrees, wrong launcher versus active root, nested-cwd switching, HEAD/branch resets, UTF-16 input, full Stop state transitions. Temp copies used independent git-init repositories without commits. UTF-8 BOM was tested. |
| U-03 | NOT_RUN | Optional-frontend removal, implementation replacement, missing-binds negative suite, coordinated contract/manifest tampering. Current selected structures inspected and pristine checkers ran. |
| U-04 | NOT_RUN | Exhaustive Kind/Level conformance and private-reference negative permutations. P4 and a documented neutral-binding control tested; no complete relation proof. |
| U-05 | UNVERIFIED | Full historical V2 technique/example preservation and strict improvement over every frozen baseline behavior. Normalized policy mapping and current source equality established; exhaustive historical equivalence not proved. |
| U-06 | NOT_RUN | Paired generation, application builds/tests, real database/provider behavior, CI execution, measured code quality. No application generation, restore, network, or model invocation allowed. |
| U-07 | UNVERIFIED | Evaluated MSBuild imports/conditions, custom props/targets, malformed XML corpus, runtime resolution of every symbolic facet. Finite probes covered literal csproj and Directory.Packages.props; broad security globs do not imply parsing every extension. |

**Overall:** no unconditional six-candidate freeze. M1 requires resolution of A-001; the other five have provisional readiness with these limitations. Parity-only issues do not independently block 5.3. No candidate repair was performed.
