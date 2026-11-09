# Generation Report

## Result

| Item | Value |
|---|---|
| Final acceptance result | **PASS** |
| Trigger-role delta count | 0 (194 inventory policies + 2 shared invariants: always→always 32, path→path 123, workflow→workflow 41) |
| Minimum-scope failures | 0 |
| Unresolved broken references | 0 |
| Known Windows hook compatibility defects | 0 |
| Directly observed experimental isolation violations | 0 |
| Confirmation audit | 0 concrete template defects |

## Implemented Candidate Model

K0 — Kinds × Scopes with embedded technologies. Every instruction artifact carries one Kind (OP, DEC, STD, KNW, WF, ENF, IN) and one Scope (common, backend, backend-tests, frontend, delivery, repo/meta) in a one-line header; Kind determines mechanism:

- OP → `CLAUDE.md` (always loaded); DEC → one decision register `docs/architecture/decision-register.md` (imported by `@`; stable IDs, summary, `Details in`, `Affects`);
- STD → `.claude/rules/<scope>/<responsibility>.md` with the scope's canonical `paths:`; STD cites DEC IDs instead of restating decisions; no procedures;
- KNW → model-invoked skills (technique only; no "must" statements); WF → workflow skills and the thin `code-reviewer` agent;
- ENF → `settings.json`, Node hooks, two checkers, `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props`;
- IN → `SPECIFICATION.md` (empty by design), `CUSTOM_SETTINGS.md`.

Conformance direction WF → KNW → STD → DEC → OP, ENF → STD/DEC; `Technique:`/`Workflow:` lines, the routing table and register `Details in`/`Affects` are routing pointers. No levels, capability contracts, manifests or slots. Human map: `.claude/MAP.md` (Kind × Scope view, catalog with owner/loading/enforcement/extension, decision → Affects, policy locator), not auto-loaded.

## Runtime File Count and Tree

66 files.

```text
template/
├── CLAUDE.md                                  OP
├── SPECIFICATION.md                           IN (empty)
├── CUSTOM_SETTINGS.md                         IN
├── .editorconfig  Directory.Build.props  Directory.Packages.props        ENF
├── docs/architecture/decision-register.md     DEC
└── .claude/
    ├── MAP.md                                 human map (not loaded)
    ├── settings.json                          ENF
    ├── hooks/      hook-io.mjs  pre-command-guard.mjs  post-edit-checks.mjs  stop-co-change-check.mjs
    ├── scripts/    check-instructions.mjs  check-manifests.mjs
    ├── agents/     code-reviewer.md           WF
    ├── rules/                                 STD
    │   ├── common/        security.md  dependencies.md  structure.md
    │   ├── backend/       architecture.md  persistence.md  api.md  error-handling.md  security.md
    │   │                  csharp.md  outbound-http.md  caching.md  operations.md
    │   ├── backend-tests/ testing.md
    │   └── frontend/      angular.md  security.md
    └── skills/
        ├── WF:  development-workflow  project-structure (+references: solution-layout, backend-layout, scaffold-stack)
        │        verify  code-review  build-fix  custom-settings  git-workflow  security-scan (+references: scan-layers)
        │        add-dependency  architecture-decision  delivery-pipeline  template-maintenance (user-only)
        └── KNW: ef-core  http-api  aspnet-error-handling  dotnet-testing  logging (+references: serilog)
                 httpclient-factory (+references: resilience)  configuration  dependency-injection  caching
                 swagger  api-versioning  health-check  docker  ci-cd  angular  modern-csharp  authentication
```

## Structural Choices (where CANDIDATE.md allowed freedom)

1. **Two workflows beyond the shared set.** `development-workflow` holds the implementation procedure that must not live in `CLAUDE.md` (spec reading, code inspection, co-change obligations, review and verify gates). `delivery-pipeline` owns the workflow-triggered CI/CD and production-migration obligations; `ci-cd` stays knowledge.
2. **Standards split by scope, then responsibility** (3 common, 9 backend, 1 backend-tests, 2 frontend). No `delivery/` or repo/meta standards: no path-triggered policy has those scopes.
3. **Canonical scope globs** (`backend/**`, `backend/**/*Tests/**`, `frontend/**`; common = backend + frontend + root build, YAML, Dockerfile and `.env` files). Common rules deliberately exclude instruction/doc files so they do not become de-facto always-loaded.
4. **Package-manifest conventions** (backend CPM, frontend npm) share one common dependencies standard — one manifest responsibility whose paths cover both scopes.
5. **Decision IDs** are semantic (`DEC-AREA-NN`); `Affects` tokens are Kind-prefixed (`STD x`, `WF x`, `KNW x`, `ENF x`) and checked for existence and Kind; DEFAULT-strength entries are marked **Default**.
6. **Low-level C# style guidance** stays path-loaded as prefer/avoid guidance in `rules/backend/csharp.md`; `modern-csharp` holds examples.
7. **Hooks** are `node .claude/hooks/<file>.mjs` (no shell expansion); the project root is resolved inside Node from `CLAUDE_PROJECT_DIR`, the hook input `cwd`, or the process cwd. Package and repository-changing Git commands pause until re-run with an acknowledgment comment (`# add-dependency: done`, `# git: user-requested`). The Stop hook blocks at most once per change set (`stop_hook_active` + fingerprint kept inside `.git`). Hooks exit 1 with a clear message when they cannot run.
8. **Manifest gates** read the register: a gated package is accepted once an Adopted/Conditional row names it.
9. **`code-reviewer`** is read-only via `disallowedTools` and reads `code-review` explicitly; the `skills:` preload field is included but the design does not depend on it.

## Intentional Wording/Placement Deltas

- Workflow-triggered policies from the V2 `CLAUDE.md` (read specification, inspect code, review before verify, verify before completion, record approved behavior) moved to `development-workflow`; `CLAUDE.md` keeps routing pointers.
- The consequential-decision gate and the shared decision protocol form one Reserved list in `CLAUDE.md` § Decisions; "routine internal choices need no approval" is the Delegated class.
- "Approved technology is not silently replaced" is the register preamble (applies to every entry).
- Seeder co-change and migration review sit in `development-workflow`; production-migration policy in `delivery-pipeline`; API version deprecation in `architecture-decision`; versioning/resilience package choices in `add-dependency`.
- Overlapping policies are split by owner with pointers: Swagger exposure (register summary + operations standard); token logging in the frontend security standard points to the common logging rule; standards cite DEC IDs for NUnit, Angular baseline, EF Core, FluentValidation, Serilog.
- V2 conditions kept beyond the normalized wording: Rich Domain needs no extra approval when the approved specification already requires it; "Decided" includes choices required by the specification or established project structure; `VersionOverride` is allowed with a reported reason ("normally versionless").
- The V2 empty specification stays empty (no header) so "when non-empty" keeps its meaning.

## Policy-Preservation Concerns

None blocking. All 196 owners were reviewed against the normalized policy for strength and conditions.

## Unresolved Ambiguity

- The PowerShell tool's hook payload is assumed to carry `tool_input.command` like Bash; if it does not, the guard exits 1 with a visible message instead of silently passing.
- Always-loaded estimate ≈ 5.4k tokens (`CLAUDE.md` + register + skill descriptions) against the ~5k target; kept because the planning-time policy and decision summaries are required there.

## Broken References Found / Fixed

First-draft checker run: 13 errors — 2 knowledge "must" statements, 2 placeholder paths in the register preamble, 1 non-existent rules directory path in the map (fixed in the template); 8 checker false positives (map catalog of private references, numeric status codes read as workflow names; fixed in the checker). Final: 0 unresolved.

## Audit Summary

Primary substantive audit covered: owner + trigger-role + minimum-scope mapping (scripted), semantic-fidelity review of every owner text, V2 preservation (scripted heading/code-block coverage, 553/652 headings and 181/299 blocks verbatim, all unmatched items reviewed manually), duplicate/restatement sweep (shingles + normative-phrase scan), K0 structure and dependency direction (shipped checker), reference resolution (427 references), 64 deterministic hook/checker tests in an in-workspace sandbox (Git with `GIT_CEILING_DIRECTORIES`; exact hook commands launched through cmd.exe, PowerShell and bash), research-metadata/language hygiene, and the always-loaded budget.

Primary-audit repairs that materially changed the template:

1. Fidelity: CPM "normally versionless" restored; DEFAULT-strength register entries marked **Default**; Swagger exposure condition added to DEC-DOCS-01; "stage or clean" and Playwright "default" restored.
2. Checker defects: `PackageVersion` versions were never parsed (floating/prerelease undetected); standard checks keyed on header Kind instead of location.
3. 13 restatements in knowledge/reference files replaced by pointers; V2 repository/Unit of Work interface examples and a test-readability sentence restored.
4. Ambiguous "normally" removed from workflow guidance; map catalog extended with Loading/Enforcement columns.

Confirmation audit: all tooling rerun and every repaired item rechecked — 0 concrete template defects.

## Workspace Events (directly observed)

- Experimental isolation violations: 0.
- Recoverable workspace-process incident: the first read of `TASK.md` used a mistyped absolute path outside the workspace; the file did not exist, nothing was read, and the read was repeated with the workspace path. Remediated.
- Platform-managed persistence events: two oversized command outputs (one with `TASK.md`, one with the V2 `ef-core` and `error-handling` skills) were saved by the tool runtime to its own tool-result storage outside the workspace; the `TASK.md` copy was read once during normal execution (content identical to the workspace input), the other was not read. When the shell's working directory was inside the V2 baseline, the runtime auto-loaded that `CLAUDE.md` and listed its skills; they were not invoked. None of these created an external dependency.
- All construction and audit material lived in `output/.work/` (sandbox included) and was removed before completion.
