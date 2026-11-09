# Generation Report — Candidate M (Minimal Modular)

## 1. Implemented model

M = V2 + the frozen V2 policy oracle + the shared construction contract +
defect-driven refactoring. The V2 mental model is kept: `CLAUDE.md` holds
planning-time policy, a flat topical `.claude/rules/` directory holds
path-loaded policy, workflow skills hold procedures, knowledge skills hold
technique, and one thin `code-reviewer` agent exists. Changes from V2 were made
only to fix concrete defects or to meet shared requirements:

- **Knowledge skills owned policy.** V2 knowledge skills were the only owners of
  many must/default rules (seeding, migrations, HTTP semantics, Swagger,
  versioning, health checks, caching, DI, configuration, resilience, auth,
  Angular, CI, Docker). These rules were moved into rules or always-loaded files.
  The skills now hold technique and pointers only.
- **Duplicated policy.** V2 stated many rules several times: cancellation in two
  rules, error exposure in two rules, validation in rule, skill, and security,
  probe-to-test in a rule, a skill, and `verify`, and review criteria in both the
  agent and the skill. Each rule now has one owner, chosen for the most reliable
  trigger. The other copies became pointers or check-by-reference items.
- **Workflows mixed policy and procedure.** `dependencies.md` held both
  dependency policy and the step-by-step version, license, and vulnerability
  procedure. It was split into the `dependencies.md` rule and a new
  `add-dependency` workflow.
- **Loading defects.**
  - The stack reference was private to `project-structure`. It moved to the
    always-loaded `docs/technology-stack.md`, imported by `CLAUDE.md`.
  - There was no path-loaded frontend policy. `angular.md` was added.
  - Workflows that run before files exist (greenfield work, review, verify) now
    read the rules they depend on explicitly.

No `Level:` or `Kind:` classification is used. There are no capability slots or
manifests, no rule subdirectories, and no single decision register.

## 2. Runtime file count and tree

58 files: 47 instruction Markdown files (including `.claude/MAP.md`), 2 product
inputs, `settings.json`, 3 hooks, 2 scripts, `.editorconfig`, and two
`Directory.*.props` files.

```text
template/
├── CLAUDE.md                     always; imports docs/technology-stack.md
├── SPECIFICATION.md              product input (empty by design)
├── CUSTOM_SETTINGS.md            product input
├── .editorconfig
├── Directory.Build.props
├── Directory.Packages.props
├── docs/
│   └── technology-stack.md       always (imported)
└── .claude/
    ├── MAP.md                    human map, not auto-loaded
    ├── settings.json
    ├── hooks/        guard-bash.mjs, post-edit.mjs, stop-check.mjs
    ├── scripts/      check-manifests.mjs, check-instructions.mjs
    ├── agents/       code-reviewer.md
    ├── rules/        angular, api, architecture, coding-style, delivery,
    │                 dependencies, error-handling, performance, persistence,
    │                 security, testing (.md; flat)
    └── skills/
        ├── workflows: add-dependency, architecture-decision, build-fix,
        │   code-review, custom-settings, git-workflow, project-structure
        │   (+references/solution-layout.md, backend-layout.md), security-scan
        │   (+references/scan-layers.md), template-maintenance (user-only), verify
        └── knowledge: angular, api-versioning, aspnet-error-handling,
            authentication, caching, ci-cd, configuration, dependency-injection,
            docker, dotnet-testing, ef-core, health-check, http-api,
            httpclient-factory (+references/resilience.md), logging
            (+references/serilog.md), modern-csharp, swagger
```

## 3. V2 lineage of the artifacts

| Change | Artifacts |
|---|---|
| Keep | `CUSTOM_SETTINGS.md` (policy text removed: it now holds a header and the table only), `SPECIFICATION.md`, `coding-style.md`, `testing.md`, `security.md`, `git-workflow`, `custom-settings`, `code-review`, `build-fix`, `security-scan` (+ reference), and all knowledge skills not listed below |
| Fix in place | `CLAUDE.md` (decision control, challenge duty, and workflow routing added; the merged approval gate), `architecture.md` (gained moved DI, configuration, cache, and remote-HTTP boundaries), `performance.md` (caching key/expiry/invalidation moved in), `error-handling.md` (logging and outbound-failure semantics moved in), `verify` (probe and regression ownership), `code-reviewer` (thin wrapper that preloads `code-review`) |
| Split | `dependencies.md` → rule + `add-dependency`; the `ef-core` skill → `persistence.md` (seeding/migration policy) + skill (technique); `project-structure` references → policy moved out, examples kept |
| Merge | `serilog` → `logging/references/serilog.md`; `resilience` → `httpclient-factory/references/resilience.md`; the V2 "Consequential Decision Gate" + "Architectural Simplicity" sections → `CLAUDE.md` (Core Defaults, Decision Control) |
| Move | `project-structure/references/technology-stack.md` → `docs/technology-stack.md`; HTTP, Swagger, versioning, and health policy from skills → `api.md`; CI and container policy from skills → `delivery.md`; Angular policy → `angular.md` |
| Rename (shared naming) | `error-handling` skill → `aspnet-error-handling`; `testing` skill → `dotnet-testing` (this also removes the rule/skill name clash) |
| New | `architecture-decision`, `add-dependency`, `template-maintenance`, `api.md`, `delivery.md`, `angular.md`, `MAP.md`, `settings.json`, hooks, scripts, `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props` |

## 4. Structural choices (where CANDIDATE.md allowed freedom)

- **Eleven flat rules.** The illustrative nine, plus `api.md` and
  `delivery.md`. Both are new owners for must-policy that V2 kept only in
  knowledge skills, and both have their own triggers and change drivers.
  - `api.md` covers the HTTP contract.
  - `delivery.md` is the only rule that loads on Dockerfiles and CI files.
  - Folding them into `architecture.md` or `security.md` would have mixed
    unrelated owners.
- **Logging rules live in `error-handling.md` (Logging).** V2 already had that
  section. Sensitive and payload logging live in `security.md`.
- **Outbound timeout/retry/fallback semantics live in `error-handling.md`.**
  `HttpClient` lifetime stays in `performance.md`, as in V2.
- **V2-like broad globs kept.** Most backend rules use `backend/**/*.cs`;
  `security.md` keeps the V2 path list.
- **Decision model.** `CLAUDE.md` holds:
  - the Architecture Defaults paragraph, marked as the single designated
    decision summary;
  - the not-adopted list and Decision Control, which merges the V2 approval-gate
    examples into the shared ten-item Reserved list.

  `docs/technology-stack.md` owns the stack and conditional technologies.
  `docs/decisions/` holds only ADR history; the folder is not pre-created.
  `architecture-decision` records accepted decisions there and updates the
  Decided source.
- **Header format.** One header line on every instruction file:
  `> Owns: … | Scope: … | Loads: …`. It carries no kind or level field.
- **Enforcement is written in Node.js** (`.mjs`). Node is already required by
  the Angular baseline, and it runs on Windows, macOS, and Linux.
  - The Bash guard blocks npm `--force` and `--legacy-peer-deps`. It also blocks
    dependency-changing commands until they carry the `# add-dependency` marker
    that the workflow's install step adds.
  - The post-edit hook gives sync reminders and runs the manifest check on the
    edited file.
  - The Stop hook gives seeder, migration, and test reminders once per distinct
    change set. It is guarded by `stop_hook_active`, so it cannot loop.
  - `Directory.Build.props` and `.editorconfig` enforce IDE0005 (unused usings)
    at build time.
  - `settings.json` asks for confirmation on destructive or remote Git commands.

## 5. Policy preservation, placement deltas, and wording deltas

- **Ownership.** All 194 inventory policies and both research invariants map to
  exactly one owner. Per-owner counts:
  - `CLAUDE.md` 26, `technology-stack.md` 17
  - rules: architecture 26, persistence 11, coding-style 4, performance 12,
    error-handling 13, api 16, security 19, testing 10, dependencies 4,
    angular 12, delivery 3
  - workflows: verify 8, code-review 2, build-fix 3, custom-settings 2,
    git-workflow 2, security-scan 2, add-dependency 3
  - agent: code-reviewer 1

  The owner of each topic is listed in `MAP.md`.
- **Trigger-placement deltas.** These are deliberate. Each places the policy on
  a surface that is loaded at least when the original trigger fires.
  - **path → always:** ARC-027, the common-scope structural restraint. It has no
    narrower path glob, and it is needed before any files exist. API-017
    (Swagger UI exposure) was merged into the always-loaded stack entry for
    DEP-012 to avoid stating the same rule twice.
  - **workflow → always:**
    - GOV-002, GOV-007, WF-001..003 keep their V2 owner, the `CLAUDE.md`
      Development Workflow.
    - GOV-019 (never destroy user work) and WF-015 (never weaken verification)
      are critical must-nots that apply outside any single workflow.
    - DEP-017 and DEP-020 are conditional technologies, which §6.9 requires to
      be visible at planning time.
  - **workflow → path:**
    - RUN-010, RUN-012, and DEP-025 keep their V2 rule owners. DEP-025 is also
      blocked by the Bash guard.
    - PST-008, PST-010, WF-019, API-022, WF-017, and WF-018 moved out of
      knowledge skills into the rule that loads when the activity's files are
      edited.
    - `verify`, `code-review`, and `add-dependency` read these rules explicitly.
- **Strengthening required by the shared contract.** §6.8 item 9 makes adopting
  API versioning Reserved. That is stricter than V2 API-013 alone.
  - `api.md` keeps API-013's need test and points to the Reserved list.
  - The V2 "Rich Domain requires approval" rule (ARC-004) now points to the same
    Reserved list.
- **Workflow-owned must-policies.** Policies with `trigger_class: workflow` and
  must strength (verify, review, build-fix, git, custom-settings, security-scan,
  add-dependency) are owned by their workflow step, as §6.5 requires. Their
  invocation is made reliable by:
  - the mandatory routing table in `CLAUDE.md`;
  - hooks: dependency commands are routed to `add-dependency`, `verify` is
    reinforced by the Stop reminders, and `custom-settings` is reinforced by the
    post-edit reminder.
- **Wording deltas.** Rules use the §6.15 vocabulary. DEFAULT-strength policies
  carry "by default" or "prefer". Rule text is condensed from V2 wording, with
  semantics preserved. Non-oracle V2 technique stayed in the knowledge skills
  and private references, rephrased so it does not restate rules.

## 6. Unresolved ambiguity and unverified mechanics

- **"Model-invoked skill" in §6.5.** This could mean every non-user-only skill.
  Read that strictly, it would contradict §6.5's own role for `workflow`
  policies (explicit workflow step). This report reads it as on-demand knowledge
  material. Workflow skills are reached through mandatory routing. Critical
  cross-cutting must-nots were placed in `CLAUDE.md`.
- **Product-input headers.** `SPECIFICATION.md` is left empty, with no header.
  Adding a header would make it "non-empty", which changes the trigger condition
  of GOV-001. `CUSTOM_SETTINGS.md` carries an HTML-comment header.
- **Scope of dependency rules.** Dependency policies scoped `backend` or
  `frontend` load on manifest files only (`*.csproj`, `Directory.Packages.props`,
  `package*.json`), as in V2. They are not loaded on all backend or frontend
  source files.
- **Runtime behaviors used but not verified.** Hook JSON outputs (PostToolUse
  `additionalContext` / `decision`, Stop `decision`), `$CLAUDE_PROJECT_DIR` in
  hook commands on Windows, the agent `skills:` preload field, and
  `disable-model-invocation`. The design does not depend on them for policy
  availability: rules and `CLAUDE.md` carry the policy, and the hooks are
  reminders or guards.

## 7. Broken references found and fixed

- V2 references to `references/technology-stack.md` now point to
  `docs/technology-stack.md`.
- References to the `testing`, `error-handling`, `serilog`, and `resilience`
  skills were renamed or redirected to the new skill names and private
  references.
- The truncated code fence at the end of V2 `testing.md` was removed.
- The `architecture.md` rule is now cited consistently as
  `.claude/rules/architecture.md` / `architecture.md`.
- Final `check-instructions.mjs` run: imports, backticked paths, private-reference
  ownership, hook paths, and MAP completeness all resolve, with 0 problems.

## 8. Process notes

- Early on, an inventory dump was written by mistake to the parent of the run
  directory. It was moved to the session scratchpad immediately and later
  deleted.
- That listing showed a sibling run folder's name. Its contents were not
  inspected.
- Hook and checker tests ran on throwaway copies in the session scratchpad. They
  were deleted afterwards.
- No network access was used.

## 9. Final self-check

| # | Check | Result |
|---|---|---|
| 1 | Template standalone | PASS — no references outside `output/template/` |
| 2 | V2 policy semantics preserved | PASS — 194/194 mapped, deltas in §5 |
| 3 | Shared requirements and invariants | PASS — GOV-017/018 in `CLAUDE.md`; workflows, agent, knowledge names, enforcement, MAP |
| 4 | CANDIDATE.md binding rules | PASS — V2 lineage per artifact, flat rules with `paths`, two-part decision model, no Level/Kind/slots |
| 5 | One owner, no accidental restatement | PASS — duplicate-phrase scan done; remaining copies are pointers or check items; one designated decision summary |
| 6 | Imports and references resolve | PASS — `check-instructions.mjs` |
| 7 | trigger_class and minimum scope | PASS, with the deltas listed in §5 |
| 8 | Critical must-rules not only in on-demand material | PASS — no knowledge skill or private reference owns policy |
| 9 | Product inputs stay inputs | PASS |
| 10 | Workflows, knowledge, enforcement, map present | PASS — 10 workflows, 17 knowledge skills, agent, hooks, scripts, MAP |
| 11 | No application or benchmark generated | PASS |
| 12 | No research metadata in runtime | PASS — scan for labels, IDs, and workspace terms is clean |
| 13 | No dependency on files outside the template | PASS |
| 14 | Understandable, no gratuitous layers | PASS — every new file is a required owner, enforcement, or the map |
| 15 | English only | PASS — the only non-ASCII characters are dashes, arrows, and tree-drawing glyphs |

Always-loaded estimate (`CLAUDE.md` + `technology-stack.md` + skill
descriptions, at about 4 characters per token): about 5.3k tokens, slightly over
the roughly 5k target. Planning-time policy was kept in place rather than moved
out to hit the target.
