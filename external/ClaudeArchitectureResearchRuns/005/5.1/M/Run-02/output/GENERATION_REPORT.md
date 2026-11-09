# Generation Report — Candidate M (Minimal Modular)

## 1. Implemented Model

M = the V2 baseline, the frozen V2 policy oracle, the shared construction
contract, and defect-driven refactoring. The V2 mental model is kept:
always-loaded `CLAUDE.md` with the imported `docs/technology-stack.md`, a flat
topical rule directory, workflow and knowledge skills, and a thin reviewer agent.
Changes were made only to fix concrete defects:

- **Path-class must-policy that lived only in knowledge skills or private
  references** (HTTP semantics, versioning, Swagger, health, DI, caching,
  outbound HTTP, seeding, Angular, CI/containers, auth) was **moved** into flat
  path rules.
- **Always-class stack decisions held in a skill-private reference**
  (`project-structure/references/technology-stack.md`) were **moved** to
  `docs/technology-stack.md`, imported by `CLAUDE.md`.
- **Duplicate owners** (V2 rules repeating skill content, competing
  `serilog`/`resilience` skills, a review checklist in both the skill and the
  agent) were **merged** into one owner each, with pointers elsewhere.
- **Mixed responsibilities** (normative policy plus multi-step procedure in
  `dependencies.md`) were **split**.
- **Shared requirements** were added as **new** artifacts: decision control, the
  challenge obligation, the `add-dependency`, `architecture-decision`, and
  `template-maintenance` workflows, hooks and checkers, and `.claude/MAP.md`.

No levels, kinds, capability slots, or decision registers were introduced.
Headers use only Owner / Scope / Loads / Enforced.

## 2. Runtime File Count and Final Tree

59 files in `output/template/`.

```text
template/
├── CLAUDE.md                         always; imports docs/technology-stack.md
├── SPECIFICATION.md                  product input (intentionally empty)
├── CUSTOM_SETTINGS.md                product input
├── .editorconfig
├── Directory.Build.props
├── Directory.Packages.props
├── docs/
│   └── technology-stack.md           always (imported)
└── .claude/
    ├── MAP.md                        human map, not auto-loaded
    ├── settings.json                 hook wiring
    ├── hooks/hooks.mjs               PreToolUse / PostToolUse / Stop dispatcher
    ├── scripts/                      lib.mjs, check-dependencies.mjs,
    │                                 check-architecture.mjs, check-instructions.mjs
    ├── agents/code-reviewer.md
    ├── rules/                        flat; every file declares paths
    │   ├── architecture.md   persistence.md   api.md   error-handling.md
    │   ├── coding-style.md   performance.md   security.md   testing.md
    │   └── dependencies.md   angular.md   delivery.md   repository-structure.md
    └── skills/
        ├── workflows: project-structure (+references/solution-layout.md,
        │   backend-layout.md), verify, code-review, build-fix, custom-settings,
        │   git-workflow, security-scan (+references/scan-layers.md),
        │   add-dependency, architecture-decision, template-maintenance (user-only)
        └── knowledge: ef-core, http-api, aspnet-error-handling, dotnet-testing,
            logging (+references/serilog.md), httpclient-factory
            (+references/resilience.md), configuration, dependency-injection,
            caching, swagger, api-versioning, health-check, docker, ci-cd,
            angular, modern-csharp, authentication
```

Always-loaded estimate from `check-instructions.mjs`: ~3.2k tokens
(`CLAUDE.md` plus the import) + ~1.6k tokens (skill listing) ≈ 4.8k.

## 3. V2 Lineage and Structural Choices

| Artifact | Change | Reason |
| --- | --- | --- |
| `CLAUDE.md` | Keep + fix | Added vocabulary, decision control, challenge obligation, and the architecture decision summary. Merged the V2 decision gate and simplicity text from `architecture.md` (one owner). Moved in the layout line (always-class) from project-structure references. |
| `docs/technology-stack.md` | Move | Always-class stack policy was skill-private; trimmed the dependency-policy restatements. |
| `CUSTOM_SETTINGS.md` | Fix | Restated rules replaced by a pointer to `CLAUDE.md`. |
| `architecture.md` | Keep + split | UoW and EF boundary → `persistence.md`; decision gate → `CLAUDE.md`. Moved in DI, cache and remote-HTTP boundaries, and DTO duplication from skills/references. |
| `persistence.md` | Split + move | Explicitly allowed by the candidate; holds seeding and migrations formerly only in `ef-core`. |
| `api.md` | New (move) | HTTP-contract must-policy lived only in four knowledge skills. Named `api.md` to avoid colliding with the `http-api` skill. |
| `error-handling.md` | Keep + move | Gained outbound failure semantics (timeouts, retries, Retry-After, fallback); V2 already owned the caller-cancellation retry clause. |
| `coding-style.md` | Keep + fix | Low-level style (constructors, records, `var`, naming) → `modern-csharp` + `.editorconfig` (non-oracle technique). Moved in typed options and logging-call style. |
| `performance.md` | Keep + move | Gained cache keys, lifetime, and invalidation; allocation technique → `modern-csharp`. |
| `security.md` | Keep + fix | Moved in auth, upload, fail-safe, and payload-logging policy; removed restatements (FluentValidation, error responses). |
| `testing.md` | Keep + move | Gained skill-only test policies and test-project references. |
| `dependencies.md` | Split | Procedure (version, license, vulnerability, removal) → `add-dependency`. |
| `angular.md` | New (move) | Shared requirement: path-scoped frontend must-policy. |
| `delivery.md` | New (move) | CI and container must-policy lived only in `ci-cd`/`docker`. |
| `repository-structure.md` | New (move) | A common-scope path policy (no speculative projects/dirs/buckets) had no common-path owner. Kept as one small rule rather than raising it to always. |
| `code-review` + agent | Merge | One review procedure; the agent is a thin wrapper that preloads it. The V2 priority-order conflict was resolved to the agent/oracle order. |
| `serilog`, `resilience` | Merge | Became private references of `logging` / `httpclient-factory`. |
| `error-handling`, `testing` skills | Rename | `aspnet-error-handling`, `dotnet-testing` (shared naming; avoids rule/skill name collisions). |
| Other skills | Keep | Policy sentences replaced by owner pointers; technique and examples preserved. |
| Hooks, scripts, settings, props, `.editorconfig`, `MAP.md` | New | Shared enforcement and navigation requirements. |

Other choices:

- Hooks are one Node.js dispatcher. Node is the only runtime guaranteed by the
  Angular stack and starts fast.
- Dependency and repository-changing Git commands are **paused once per command
  per session** (exit 2 with a pointer); re-running the same command proceeds.
  npm `--force` / `--legacy-peer-deps` is always blocked.
- Stop reminders: each trigger fires once, `stop_hook_active` prevents loops,
  and there is no reminder at all outside a Git repository.
- `docs/decisions/` is created by `architecture-decision` on first use, so no
  placeholder file ships.

## 4. Policy Ownership (Inventory + Shared)

All 196 policies (194 inventory + 2 shared) map to exactly one owner. A scratch
script checked existence, heading, trigger placement, and path coverage.

| Owner | Policies |
| --- | --- |
| `CLAUDE.md` | GOV-001–018 (017/018 shared), ARC-009, ARC-020, DEP-024, WF-001–003 |
| `docs/technology-stack.md` | DEP-002, 008–018, 020, 022, 023 |
| `architecture.md` | ARC-001–008, 010–015, 021–025, 029 |
| `persistence.md` | ARC-016–019, PST-001–008, PST-010, DEP-026, WF-019 |
| `api.md` | API-001, 003–006, 013–020, 022, ARC-026 |
| `error-handling.md` | API-002, 007–012, 021, RUN-015–019 |
| `coding-style.md` | RUN-009–011, 013, 022, 024, DEP-021 |
| `performance.md` | RUN-001–008, 012, 020, 021, 023 |
| `security.md` | SEC-001–018, RUN-014 |
| `testing.md` | TST-001–012, ARC-028 |
| `dependencies.md` | DEP-001, 006, 007 |
| `angular.md` | FE-001–012 |
| `delivery.md` | DEP-019, WF-017, WF-018 |
| `repository-structure.md` | ARC-027 |
| `add-dependency` | DEP-003, 004, 005, 025 |
| `verify` | WF-004–009 |
| `code-review` | WF-010–012 |
| `build-fix` | WF-013–016 |
| `security-scan` | WF-020, WF-021 |
| `git-workflow` | GOV-019, 020, WF-022 |
| `custom-settings` | GOV-021, PST-009 |

## 5. Intentional Wording and Placement Deltas

1. **Workflow-class policies not owned by a workflow skill** (17):
   - GOV-002, GOV-007, and WF-001–003 stay in the always-loaded `CLAUDE.md`
     workflow section (their V2 owner).
   - PST-008, PST-010, WF-019, TST-009, TST-010, RUN-010, and RUN-012 stay in
     the path rule that loads while the obligation arises (V2 rule or moved from
     a skill).
   - WF-017 and WF-018 go to `delivery.md`, because no shared CI workflow exists.
   - DEP-017 and DEP-020 go to `technology-stack.md` as conditional
     technologies.

   Each has an explicit workflow read step (`verify`, `code-review`,
   `add-dependency`, `architecture-decision`), and some also have a hook
   reminder.
2. **ARC-020 merged** into the Reserved list in `CLAUDE.md`, so one list covers
   the V2 gate and the shared Reserved categories; every V2 example remains.
   **GOV-005** is stated as the definition of Delegated.
3. **Overlapping inventory clauses** are stated once, with a pointer from the
   other owner:
   - DEP-012's non-Development exposure clause → API-017 (`api.md`).
   - DEP-009's provider-boundary clause → ARC-002/ARC-008.
   - SEC-012's "never log tokens" → the SEC-010 line in the same file.
   - PST-004's "tests own their setup" → TST-008.
   - WF-019's "no Development seeding in Production" → the PST-004 line in the
     same file.
4. **Vocabulary normalization** (6.15): "normally" or "should" in MUST/DEFAULT
   policies is rendered as must or default. For MUST items the original
   qualifiers are kept:
   - API-012: once, at the handling boundary.
   - API-014: a new version **or** an approved compatibility strategy.
   - API-019: dependencies that could cause restart loops.
   - WF-019: stated as "normal startup must not…".
5. **Removed V2 restatements**: knowledge-skill "Core Principles" and
   anti-pattern bullets that repeated rule text were replaced by pointers.
   Technique, examples, and decision guides were kept, with a few practical
   additions (CPM handling after `dotnet new`, the `webapi` OpenAPI replacement,
   `takeUntilDestroyed`, `ConfigureTestServices`).
6. **Agent tooling**: an allowlist (`Read, Grep, Glob, Bash`) replaces V2's
   `disallowedTools` for a reliable read-only boundary; Bash is read-only by
   instruction.

## 6. Policy-Preservation Concerns and Unresolved Ambiguity

- **Agent preload:** `skills: code-review` in agent front matter is not one of
  the established E0 mechanics. The agent body therefore also tells it to read
  `.claude/skills/code-review/SKILL.md`.
- **Hook mechanics:** the hooks rely on standard Claude Code exit-code-2
  semantics, `$CLAUDE_PROJECT_DIR`, and Node.js on `PATH`. Without Node they fail
  as non-blocking errors, and rules and workflows still carry the policy.
- **Pause-once friction:** pausing Git and dependency commands once adds one
  extra tool call to explicitly requested commits and installs. This is
  deliberate, so the routing is actually seen.
- **Common scope for ARC-027:** interpreted as `backend/**`, `frontend/**`,
  `docs/**`, and `*.slnx`. The `delivery` scope is used for `delivery.md`
  although no inventory policy declares it.
- **Mechanical checks are heuristics:**
  - IQueryable and namespace checks are text-based.
  - Prerelease and floating versions are warnings, because "explicitly
    requested" cannot be detected.
  - IntegrationTests → Infrastructure references are warnings, not errors.
- No contradiction among the inputs required stopping.

## 7. Broken References Found and Fixed

- V2 `dependencies.md` pointed into a skill-private reference
  (`project-structure/references/technology-stack.md`) → now
  `docs/technology-stack.md`.
- V2 `code-reviewer.md` and `security-scan` routed to `resilience`, `serilog`,
  `testing`, and `error-handling` skills → now `httpclient-factory`, `logging`,
  `dotnet-testing`, and `aspnet-error-handling`; no file outside a skill points
  into its references.
- V2 bare references (`architecture.md`, `performance.md`) → full paths with
  checked `§` headings.
- Found by the generated checker and fixed during this run:
  - pointers wrapped across lines (the checker now scans by paragraph);
  - a `.claude/settings.local.json` mention (marked local-only);
  - a bare `references/` mention in `template-maintenance`;
  - the `AppDbContext` pattern miss in the architecture check;
  - Windows short-path (8.3) relativity in the scripts (fixed with `realpath`).

## 8. Final Self-Check

| # | Check | Result |
| --- | --- | --- |
| 1 | Standalone template | PASS — no references to files outside `output/template/`; on-demand paths (`docs/decisions/`, `settings.local.json`) are documented. |
| 2 | V2 policy semantics preserved | PASS — 194/194 mapped and reviewed; deltas in §5. |
| 3 | Shared requirements (§6, invariants) | PASS — GOV-017/018 in `CLAUDE.md`; workflow, knowledge, and agent sets, enforcement, and map present. |
| 4 | Candidate M binding rules | PASS — flat rules with `paths`, V2 topical organization, `persistence.md` split, `angular.md`, two-part decision model, `MAP.md`, no L/K/B1 constructs. |
| 5 | One owner, no accidental duplication | PASS — scratch mapping plus a review of normative wording in skills (absolutes reworded to pointers or guidance). |
| 6 | Internal references resolve | PASS — `check-instructions.mjs`: no findings (paths, `§` headings, skills, imports, links, private references). |
| 7 | Trigger class and minimum scope | PASS — always → always-loaded; path → rule with covering `paths`; workflow → workflow step or explicitly read owner (§5.1). |
| 8 | Critical must-rules not only on demand | PASS — no must-policy is owned by a knowledge skill or private reference. |
| 9 | Product inputs remain inputs | PASS — stated in `CLAUDE.md`; `SPECIFICATION.md` empty; `CUSTOM_SETTINGS.md` holds data plus a pointer. |
| 10 | Workflows, knowledge, enforcement, map present | PASS — 10 workflows, 17 knowledge skills, agent, hooks, 3 checkers, config, `MAP.md`. |
| 11 | No application or benchmark generated | PASS — only fixtures in scratch space, outside `output/`. |
| 12 | No research metadata at runtime | PASS — scan found no IDs, labels, or research files; the only hit is "benchmark" in the RUN-012 rule text, which is domain wording. |
| 13 | No dependency outside the template | PASS. |
| 14 | Understandable, no gratuitous files | PASS — every new file is justified in §3; the map answers owner, scope, loading, enforcement, extension. |
| 15 | English only | PASS — no Cyrillic in any template file. |

Executed checks:

- `check-instructions.mjs`, `check-dependencies.mjs`, and
  `check-architecture.mjs` pass on the template.
- Negative tests on scratch copies detected:
  - missing headers and `paths`, a nested rule, and a competing skill;
  - broken paths and `§` headings, and a private-reference leak;
  - a missing user-only flag and a missing agent preload;
  - CPM version duplication and deprecated packages;
  - reversed project references, Domain/Application namespace leaks,
    `IQueryable` in repository contracts, and a controller using `DbContext`.
- Simulated hook inputs verified:
  - the npm bypass block;
  - dependency and Git pause-once, with immediate pass on re-run;
  - post-edit findings and the product-input reminder;
  - Stop reminders, the `stop_hook_active` guard, and no repeat for unchanged
    state.
