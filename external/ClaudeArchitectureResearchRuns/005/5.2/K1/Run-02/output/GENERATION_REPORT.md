# Generation Report — K1 (Kinds × Scopes + Replaceable Capabilities)

## Final acceptance

| Item | Result |
|---|---|
| Final acceptance result | **PASS** |
| Trigger-role delta count | 0 (194/194 inventory policies keep their `trigger_class`) |
| Minimum-scope coverage failures | 0 (every path policy sits in `rules/<its scope>/` with the scope's canonical glob) |
| Shared research invariants with runtime owner | 2/2 (decision control, challenge obligation — both in `CLAUDE.md`) |
| Unresolved broken-reference count | 0 |
| Known Windows-hook compatibility defects | 0 |
| Directly observed experimental isolation violations | 0 |
| Confirmation-audit result | 0 concrete template defects |

## Implemented candidate model

- **Capability → Kind → Scope** classification. Four static slots, each with `CONTRACT.md`, one selected implementation with `MODULE.md` (facets, `Names:` leak tokens, `Binds:`, contract coverage), runtime facets, an always-loaded selection row, and checker-enforced leak/conformance: architecture → clean-architecture (frame); persistence → ef-core, variant sqlserver (binds architecture); backend-testing → nunit (binds architecture); frontend → angular (optional).
- **Kinds:** OP `CLAUDE.md`; DEC `docs/architecture/decision-register.md` (single always-loaded register, `@`-imported; slot selection block + platform/stack, conditional technologies, defaults, accepted-decision log); STD `.claude/rules/<scope>/` (21 files, scope-first, no stability hierarchy); KNW 17 shared-name skills (+2 private references); WF 13 workflow skills (+5 private references) and a thin `code-reviewer` agent; ENF hooks, scripts, root build/editor config; IN `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`.
- **Neutral standard + facet** pairs: `architecture.md`/`architecture-style.md`, `persistence.md`/`persistence-technology.md`, `testing.md`/`test-framework.md` (+ frame facet `test-projects.md`), `frontend.md`/`frontend-framework.md`. Placement rules sit in the frame; technology technique in leaves.
- **Dependency direction** WF → KNW → STD → DEC → OP, ENF → STD/DEC, skill references are routing pointers; enforced (including cycles, private-reference ownership, STD scope reliability) by `.claude/scripts/check-instructions.cjs`.
- **Human map** `.claude/MAP.md` (not loaded): Kind × Scope view with file/owner/scope/capability/loading/enforcement/extension per artifact, Capability view per slot, topic → owner index.

## Runtime file count and tree

85 files under `output/template/`.

```text
template/
├── CLAUDE.md, SPECIFICATION.md (empty by design), CUSTOM_SETTINGS.md
├── .editorconfig, Directory.Build.props, Directory.Packages.props
├── docs/architecture/decision-register.md
└── .claude/
    ├── MAP.md, settings.json
    ├── agents/code-reviewer.md
    ├── capabilities/{architecture,persistence,backend-testing,frontend}/CONTRACT.md
    │   └── clean-architecture | ef-core | nunit | angular /MODULE.md
    ├── rules/common/{security,structure,dependencies}.md
    ├── rules/backend/{architecture,architecture-style,persistence,persistence-technology,api,api-contracts,operations,security,runtime,coding-style,dependencies}.md
    ├── rules/backend-tests/{testing,test-framework,test-projects}.md
    ├── rules/frontend/{frontend,frontend-framework,security,dependencies}.md
    ├── skills/ WF: development-workflow, verify, code-review, build-fix, custom-settings, git-workflow,
    │          security-scan (+references/scan-layers.md), add-dependency, architecture-decision,
    │          template-maintenance (user-only), project-structure (+references/solution-layout.md,
    │          backend-layout.md, test-setup.md, frontend-setup.md), delivery-change, persistence-change
    │   KNW: ef-core, http-api, aspnet-error-handling, dotnet-testing, logging (+references/serilog.md),
    │        httpclient-factory (+references/resilience.md), configuration, dependency-injection, caching,
    │        swagger, api-versioning, health-check, docker, ci-cd, angular, modern-csharp, authentication
    ├── hooks/dispatch.cjs
    └── scripts/{lib,check-instructions,check-manifests,check-cochange}.cjs
        └── facets/{architecture-style,persistence-technology,test-framework,frontend-framework}.cjs
```

## Structural choices where the candidate allowed freedom

- **No `rules/delivery/` and no `rules/repo/meta`:** the inventory has no path-triggered delivery or repo/meta policy; delivery obligations are workflow-triggered (`delivery-change`), Git policy is always-loaded.
- **Additional workflows** beyond the shared set, each owning workflow-triggered inventory policy: `development-workflow` (V2 Development Workflow; kept out of `CLAUDE.md`), `delivery-change` (CI and production-migration obligations; `ci-cd` stays a knowledge skill), `persistence-change` (module-owned WF facet: migration review, seed co-change, setup).
- **WF facets of the other slots** are private references of `project-structure` (`backend-layout.md`, `test-setup.md`, `frontend-setup.md`), since only scaffolding reaches them.
- **Knowledge-facet routing:** non-slot workflows name facet roles ("persistence knowledge facet named in the decision register"); the register's selection table resolves them to `ef-core`, `dotnet-testing`, `angular`.
- **Stable role vocabulary** (Domain, Application, Infrastructure, Api, Application Service, repository contract, `IUnitOfWork`) is defined by the architecture contract and usable by non-slot content; the implementation names are leak-checked.
- **ENF facets** are role-named scripts loaded through a static list in `check-manifests.cjs`; the frame exports `roleOf()` so leaves classify projects through the frame (declared `Binds:`). No NUnit-based architecture-test adapter was generated: the neutral reference check already runs in hooks and `verify`, and the .NET 10 toolchain needed to compile such an adapter is not available offline.
- **Hooks:** shell-neutral `node -e` bootstrap resolving `CLAUDE_PROJECT_DIR` inside Node; dispatcher derives the root from its own location. PreToolUse blocks unversioned dependency installs and npm force flags (routes to `add-dependency`); PostToolUse feeds manifest findings, product-input reminders, and instruction-structure errors back; Stop reports seed/migration/test co-change reminders once per change set (fingerprint in the Git directory, `stop_hook_active` respected).
- **Headers:** the one-line `Kind | Scope | Capability | Loading` header is the first content line, after the frontmatter that rules, skills, and the agent require. `SPECIFICATION.md` stays empty (no header) so "non-empty" keeps its V2 meaning; `.claude/settings.json` (JSON) has no header and is documented in the map. Maintenance metadata (MAP, CONTRACT, MODULE) uses `Kind: —`.
- **Project-owned files** (`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, root build/editor config, the register's accepted-decision log) are exempt from the leak rule and only warn on header loss, because product inputs and package manifests legitimately name technologies.

## Policy-preservation notes and permitted deltas

- **Leak-rule wording deltas** (semantics preserved; the implementation-specific facet states the concrete names): ARC-002, ARC-008, ARC-011, ARC-014 ("persistence technology", "database context", "entity sets"), TST-006 ("the persistence technology"), PST-009 ("persistence mapping"), SEC-011 ("the SPA framework" instead of the framework name).
- **Placement by capability:** implementation-specific policies moved to facets of their slot with unchanged trigger role and scope (ARC-018/019, PST-002/003/005, DEP-026 → persistence facet; ARC-001…008/012/016/017/023/029 → frame facet; ARC-028 → frame facet in backend-tests; TST-001 → test-framework facet; FE-001/004/008/010/011/012 → frontend facet; ARC-009, DEP-009, DEP-013, DEP-014, DEP-015 → register selection rows).
- **Vocabulary normalization:** "normally"/"should" in MUST policies expressed as must/never; DEFAULT policies prefixed "Default:"; strength unchanged.
- **Inherent inventory overlaps** kept with one owner each and phrased from distinct angles: DEP-012/API-017, DEP-013/DEP-024, PST-004/TST-008, ARC-008/ARC-019, ARC-009/ARC-020, DEP-010/API-010, FE-001/FE-007, WF-019/PST-004.
- **V2 material:** retained as technique in knowledge skills and references; normative V2 restatements in skills were converted to pointers or check-by-reference items. Framework-specific security and build-fix technique moved from non-slot artifacts into the owning module skills (`angular`, `ef-core`).

## Unresolved ambiguity

None blocking. Decision Request field names live in `architecture-decision` (output shape), while `CLAUDE.md` owns the protocol.

## Broken references

Found and fixed during generation and audit: ambiguous bare `MODULE.md`/`security.md` references, an STD→STD cycle risk (frame ↔ persistence facet), a DEC→STD dependency in the register, a private-reference cycle in `project-structure` references, a Claude Code local-settings mention resolved as a path. Unresolved: 0.

## Audit summary

**Primary substantive audit** (scripted evidence under `output/.work/`, now removed): owner/trigger/scope map of all 194 policies + 2 invariants; side-by-side fidelity review of every owner statement; unit-level V2 preservation matching of all 41 baseline files (2,853 units) with manual review of the 231 low matches; cross-file duplicate and per-owner restatement sweeps; independent structure/leak/hygiene audit; 74 hook/checker tests launching the exact `settings.json` commands through cmd.exe, Windows PowerShell 5.1, and Git Bash (including subdirectory cwd, missing `CLAUDE_PROJECT_DIR`, invalid input, scratch Git repository with `GIT_CEILING_DIRECTORIES`); 25 checker mutation tests; CRLF robustness check; always-loaded estimate ≈ 4.85k tokens.

**Primary-audit repairs that materially changed the template:**
1. Fidelity: GOV-003 lost an added weakening condition; GOV-008 now states settings never override the specification; PST-004 restored "tests own their own setup"; SEC-007 redirection nuance narrowed to V2 wording; WF-004 "remove" and WF-022 "clean" restored; DEP-006 keeps the `VersionOverride` exception.
2. V2 preservation: restored Aggregate-Root repository boundaries, Infrastructure validation of external assumptions, caching reasons, public-API CORS nuance, options custom-validation example, Mapster DI package, CPM example, resilience-handler registration and controller/Infrastructure note.
3. Restatements removed from `authentication`, `dependency-injection`/`architecture.md`, `delivery-change`/`ci-cd`, `http-api`, `angular`, `dotnet-testing`, `scan-layers.md`.
4. Checker defect: the leak/header check treated project-owned product and build files as instruction layers and would have failed once a project added packages; fixed and regression-tested.
5. Knowledge-skill descriptions rewritten trigger-first; MAP extended to all required fields; explicit owner reads added to `project-structure` and `delivery-change`; a hook message reduced to a pointer.

**Confirmation audit:** all gates rerun on the repaired template — mapping (0 deltas), fidelity of every repaired owner, V2 preservation (225 low matches: 223 from the manually reviewed primary-audit set; the 2 that newly dropped below the threshold were reviewed and are preserved — V2 http-api "406 concerns the response representation" by `http-api` "406 Not Acceptable — no representation acceptable to the client's content negotiation (response format); not 415", and V2 authentication "Do not commit signing secrets" by `.claude/rules/common/security.md` "Never hardcode or commit real secrets, credentials, private keys…" plus the `authentication` anti-pattern "Hardcoded signing keys"), duplicate sweeps, structure checker (0 errors, 0 warnings), independent audit, 74/74 hook tests, 25/25 mutations. Result: 0 concrete template defects.

**V2 low-match adjudication (documented):** each of the 225 remaining low-match units was listed with its closest template text and dispositioned: preserved paraphrase or merge (160); list-intro or heading fragments whose items are preserved (11); "detailed guidance belongs to skill X" lines replaced by `Technique:`/`Policy:` pointers (12); normative restatements now owned once by a standard or `CLAUDE.md` (37); implementation names neutralized with technique moved into the owning module (3); deliberately not carried (2: an ARC-025 exception absent from the unconditional inventory policy, and a Layer-7 intro sentence whose section is retained). Remaining preservation losses: 0. The six genuine losses found earlier were restored in the primary-audit repairs.

## Workspace events (directly observed)

- Experimental isolation violations: 0. No network, sibling, parent, or external-repository access; construction and audit material stayed in `output/.work/` and was removed.
- Recoverable workspace-process incidents: none.
- Platform-managed persistence events: the tool runtime saved two oversized command outputs to its own tool-results storage outside the workspace (not read back; the content was re-read from in-workspace files); Claude Desktop changed the session working directory after in-workspace `cd` commands and auto-loaded the in-workspace `CLAUDE.md` files of the baseline and the generated template as context. No forbidden information was consumed and the result does not depend on these events.
