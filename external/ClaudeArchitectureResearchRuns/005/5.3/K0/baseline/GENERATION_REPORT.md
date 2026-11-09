# Generation Report

## Final acceptance result: PASS

| Gate | Result |
|---|---|
| Trigger-role delta count | **0** (196/196 policies: 123 path, 41 workflow, 32 always — identical to inventory + shared invariants) |
| Minimum-scope failures | 0 |
| Unresolved broken references | **0** |
| Known Windows-hook compatibility defects | **0** |
| Directly observed experimental isolation violations | **0** |
| Confirmation-audit result | **0 concrete template defects** |

## Implemented candidate model

Kinds × Scopes with embedded technologies:

- **OP** — `CLAUDE.md` (always): precedence and vocabulary, product sources, engineering defaults, challenge obligation, decision protocol (Decided/Delegated/Reserved, Reserved list, five-question test, Decision Request, headless rule), Git safety, workflow routing table. No multi-step procedure.
- **DEC** — one register, `docs/architecture/decision-register.md`, imported by `CLAUDE.md`: 18 entries `D-01`–`D-18` (architecture, not-adopted patterns, stack, conditional technologies, project defaults), each with Decision / Details in / Affects. ADRs go to `docs/decisions/` when created.
- **STD** — 14 path-scoped rules organized by scope: `common/` (security, dependencies, repository-layout), `backend/` (architecture, persistence, api, error-handling, csharp, integrations, caching, hosting, security), `backend-tests/testing.md`, `frontend/angular.md`. Standards cite `D-xx` IDs instead of restating decisions.
- **KNW** — the 17 shared knowledge skills (technique only); Serilog depth private to `logging`, resilience depth private to `httpclient-factory`.
- **WF** — 12 workflow skills (`development-workflow`, `verify`, `code-review`, `build-fix`, `project-structure`, `custom-settings`, `git-workflow`, `security-scan`, `add-dependency`, `architecture-decision`, `delivery-pipeline`, user-only `template-maintenance`) + thin `code-reviewer` agent preloading `code-review`.
- **ENF** — `.claude/settings.json` (hooks, Git `ask` permissions), `.claude/hooks/hook.cjs`, `.claude/scripts/check-dependencies.cjs`, `.claude/scripts/check-instructions.cjs` (K0 structural predicates), `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props`.
- **IN** — `SPECIFICATION.md` (empty, intentional), `CUSTOM_SETTINGS.md` (data table + pointer to OP).
- Human map `.claude/MAP.md` (not loaded): Kind table, scope territories, Kind × Scope view, per-artifact table (file, Kind, Scope, owner, loading, enforcement, extension point), topic → owner index, decision → Affects view, enforcement summary.

Always-loaded surface ≈ 19.7K characters ≈ 4.9k tokens including skill and agent listings.

## Runtime file count and tree

62 files in `output/template/`.

```text
template/
├── CLAUDE.md                      OP
├── SPECIFICATION.md               IN (empty)
├── CUSTOM_SETTINGS.md             IN
├── .editorconfig                  ENF
├── Directory.Build.props          ENF
├── Directory.Packages.props       ENF
├── docs/architecture/decision-register.md   DEC
└── .claude/
    ├── MAP.md
    ├── settings.json              ENF
    ├── hooks/hook.cjs             ENF
    ├── scripts/check-dependencies.cjs, check-instructions.cjs   ENF
    ├── agents/code-reviewer.md    WF
    ├── rules/                     STD
    │   ├── common/{security,dependencies,repository-layout}.md
    │   ├── backend/{architecture,persistence,api,error-handling,csharp,integrations,caching,hosting,security}.md
    │   ├── backend-tests/testing.md
    │   └── frontend/angular.md
    └── skills/
        ├── WF: development-workflow, verify, code-review, build-fix, custom-settings, git-workflow,
        │       add-dependency, architecture-decision, delivery-pipeline, template-maintenance,
        │       security-scan (+references/scan-layers.md),
        │       project-structure (+references/{solution-layout,backend-layout,baseline-setup}.md)
        └── KNW: ef-core, http-api, aspnet-error-handling, dotnet-testing, logging (+references/serilog.md),
                httpclient-factory (+references/resilience.md), configuration, dependency-injection, caching,
                swagger, api-versioning, health-check, docker, ci-cd, angular, modern-csharp, authentication
```

## Meaningful structural choices

- **Development Workflow as a workflow skill** (`development-workflow`): the V2 `CLAUDE.md` procedure (and the workflow-class obligations GOV-002, WF-001..003, seeder co-change, migration review, regression tests, performance changes, API deprecation) needs a workflow owner; `CLAUDE.md` keeps only a routing row.
- **`delivery-pipeline` workflow**: WF-017..019 are workflow-class, while `ci-cd`/`docker` are shared knowledge names; a dedicated workflow keeps the trigger role without turning knowledge into an owner.
- **Decision recording in `architecture-decision`**: product-behavior approvals (GOV-007) are recorded there alongside register/ADR updates, since the Reserved list includes undefined product behavior.
- **No `rules/delivery/` or repo/meta rules**: no path-class policy has those scopes; files are not created to fill taxonomy cells.
- **`rules/common/dependencies.md`** owns DEP-001 (common), DEP-006 (backend) and DEP-007 (frontend): one trigger (all dependency manifests); its common scope covers both declared scopes.
- **`rules/backend/hosting.md`** groups configuration, logging, health checks and container images (paths include backend Dockerfiles for DEP-019).
- **Scope territories** (enforced by the checker): backend globs under `backend/` or root .NET build files; backend-tests under `backend/` containing `Tests`; frontend under `frontend/`.
- **Routing-line convention**: `See also:` / `Workflow:` / `Technique:` / `Enforced by:` lines are routing pointers; other references are conformance dependencies, checked for direction and acyclicity.
- **Dependency-command gate**: the pre-command hook denies package-changing commands until `add-dependency` has run; the workflow re-runs them with the marker comment `# add-dependency: reviewed`.
- **Shell-neutral hooks**: commands are `node -e "…"` resolving `CLAUDE_PROJECT_DIR` inside Node; findings are returned as Claude Code hook JSON with exit 0, so behavior does not depend on shell exit-code propagation; exit 1 only for clear hook failures.

## Policy-preservation concerns

None open. Workflow-class must-policies live in workflow skills (frozen trigger role) and are reachable from the always-loaded routing table plus hooks (dependency commands, manifests, product inputs, stop-time co-change reminders).

## Intentionally permitted wording/placement deltas

- "normally" (ambiguous under the shared vocabulary) is expressed as **default** (DEFAULT-strength policies) or folded into MUST wording where the inventory strength is MUST (API-012, API-014, API-019, TST-003).
- GOV-005 is expressed as "Delegated" with the Delegated class definition in the same OP file; ARC-020 and GOV-017 share one OP Reserved list (also carrying TASK §7.8 items).
- DEP-002 is part of the OP "Decided" class definition; DEP-012 / API-017 overlap: the register records the Swagger decision, `rules/backend/api.md` owns exposure.
- Split ownership via explicit owner references (semantics preserved): PST-004 → test setup clause references `rules/backend-tests/testing.md`; SEC-012 → token logging references `rules/common/security.md`; WF-019 → seeding clause references `rules/backend/persistence.md`; ARC-010 → "Controllers are the entry point" cites D-01.
- V2 material kept at its correct owner: mapping-library concerns added to the Domain-independence rule (V2 technology stack); C# style preferences (constructors, records, visibility, `var`, naming, member ordering) kept as prefer-guidance in `rules/backend/csharp.md`.
- V2 `CUSTOM_SETTINGS.md` policy text moved to OP; the file keeps data and a pointer.

## Unresolved ambiguity

None blocking. Hook output relies on Claude Code's documented hook JSON (PreToolUse `permissionDecision`, PostToolUse/Stop `decision: block`); the agent `skills:` preload is backed by an explicit "read `code-review` first" instruction.

## Broken references found and fixed

During generation and audit the checker found and the run fixed: one wrong section reference (`§ Test data` → `§ Isolation and data`), one malformed section phrase, stale self-references during the checker rename, and initial `Affects`/citation mismatches (Affects regenerated from citations). Final unresolved count: 0.

## Primary-audit repairs that materially changed the template

1. Semantic fidelity: removed added strength in GOV-007; restored inventory strength for RUN-020 ("avoid"), DEP-019 ("avoid"), DEP-020 ("prefer"); made TST-004 (wall-clock condition), TST-008 (execution order) and DEP-026 ("must come from user-secrets…") exact.
2. V2 preservation: restored review-discipline pattern list, `IOrderRepository`/`IUnitOfWork` examples, C# consistency and member-ordering guidance, test-readability principle, "compatible changes stay in the current version", mapping concerns out of Domain, sensitive-logging example.
3. Restatement sweep: 6 cross-artifact restatements and 15 knowledge paraphrases of standards converted to owner pointers.
4. Structure: `check-manifests.cjs` renamed `check-dependencies.cjs` (no "manifest" naming that could read as module manifests); baseline package table no longer repeats register content.
5. Enforcement: hook feedback switched from exit code 2 to JSON decisions after a test showed PowerShell 5.1 `-Command` collapses exit 2 to 1; checker no longer requires the template header in project-owned root build files.
6. A YAML-invalid `description` (`": "` in a plain scalar) fixed; skill descriptions shortened (always-loaded ≈ 5.7k → 4.9k tokens).

## Final self-check

- Structural checker: 59 artifacts, 0 errors (Kind/Scope headers, mechanism per Kind, scope globs, register IDs/Affects/citations, no decision restatement, no procedures in STD, no bare norms in KNW, references and sections resolve, skill privacy, acyclic conformance graph, hook commands without shell expansion, map coverage, no `Level:`/contracts/manifests).
- Owner map: 196/196 owners, 0 trigger-role deltas, 0 scope failures; manual fidelity review of all 196.
- V2 preservation: 41 files / 687 sections swept by term and code coverage; all low-coverage sections manually reviewed.
- Enforcement tests: 78/78 (hook launch via Git Bash, cmd.exe, PowerShell 5.1 and Node `spawn(shell)`; missing-environment failure; 17 command-detection cases; post-edit manifest/product/instruction checks; stop reminders with loop protection in a ceiling-capped scratch Git repository; dependency CLI; 20 checker mutation tests).
- Hygiene: English only; no research labels, policy IDs, run identifiers, model IDs or workspace references in `output/template/`.

## Workspace events (directly observed)

- Experimental isolation violations: 0.
- Recoverable workspace-process incident (remediated): one hook-launch test resolved `bash` to the system WSL launcher instead of Git Bash; it failed to start, read and wrote nothing outside the workspace; the harness was pinned to Git Bash.
- Platform-managed persistence events: the tool runtime stored two oversized command outputs in its own tool-results directory (not read back); when the shell working directory moved into `source/v2-baseline/`, the platform attached that directory's `CLAUDE.md` (an allowed input already read) to context. Neither created a dependency of the result on external data.
- Scratch material was kept in `output/.work/` and removed before completion.
