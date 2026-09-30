# 001 — CleanArchitectureTemplate V3: Instruction Architecture Analysis and Design Proposal

| | |
|---|---|
| Status | Draft for human review. No template files were changed. |
| Date | 2026-09-30 |
| Produced by | `prompts/001-v3-design-goal.md` |
| Inputs | `research/hypothesis.md`, `research/requirements.md`, `templates/v2-baseline/` (all 41 files read in full) |
| State of `templates/v3/` | Identical to `templates/v2-baseline/` (41 files, verified by content hash) |
| Next step | Human review → answer the questions in §14 → Phase 0 of §11 |

---

## 0. Conventions, evidence standard and requirement classification

### 0.1 Path conventions

V2 file references are relative to `templates/v2-baseline/`, with the `.claude/` prefix left out for rules, skills and agents. For example, `rules/architecture.md:152` means `templates/v2-baseline/.claude/rules/architecture.md`, line 152. Root files (`CLAUDE.md`, `CUSTOM_SETTINGS.md`) are written as they are. Proposed V3 paths are relative to the template root.

### 0.2 Evidence labels

- **Observed**: read directly in a V2 file.
- **Expected**: predicted from Claude Code's loading mechanics, not tested.
- **Needs test**: plausible but uncertain. Must be tested before anything relies on it.

This document does not claim that any trigger is empirically reliable. One loading behavior was observed during the analysis: Claude Code found the nested skills under `templates/v2-baseline/.claude/skills/` and offered them as "scoped to" that directory, even though the session ran from the research repo root. §12 explains why this matters for benchmarks.

### 0.3 Claude Code mechanics assumed

| Mechanism | Assumed behavior | Confidence |
|---|---|---|
| `CLAUDE.md` at the project root | Loaded into every session. | High |
| `@path` imports in `CLAUDE.md` | Expanded when `CLAUDE.md` loads. Imports are eager, not lazy, so they do not save context. | High |
| `.claude/rules/**/*.md` without `paths` | Loaded into every session, like `CLAUDE.md`. | High |
| `.claude/rules/**/*.md` with `paths` | Loaded when Claude works with a matching file. The exact trigger is unknown: Read only, Edit/Write, a Write that creates a new file, or Glob/Grep hits. | Needs test |
| Other frontmatter on rules (e.g. `description`) | Not a documented rule field, so expected to have no loading effect. | Expected |
| Skill descriptions | Listed in context every session, subject to a listing budget. The body loads only when the skill is invoked. | High (budget size: needs test) |
| `disable-model-invocation: true` on a skill | Runs only when a user invokes it. The description is not offered to the model. | Medium-high |
| `allowed-tools`, `context: fork`, `model` on skills | Restrict tools, run in a forked context, or pick a model. | Medium (verify against the current version) |
| Subagents (`.claude/agents`) | Own context window and tool restrictions. May preload named skills via a `skills:` field. | Medium (verify `skills:` preload) |
| Hooks (`.claude/settings.json`) | Deterministic scripts that run on events such as PreToolUse, PostToolUse, UserPromptSubmit, Stop and SessionStart. They can block, ask, or send text back to Claude. | High (exact JSON output fields: verify) |
| Permissions (`settings.json`) | Deterministic allow / ask / deny on tool patterns such as `Bash(git push:*)`. | High |

### 0.4 Classification of the requirements

The prompt asks for invariants, goals, hypotheses and non-goals to be told apart. This is how I read `research/requirements.md`, and how each class is treated here.

| Class | Items | Treatment in this proposal |
|---|---|---|
| Mandatory invariants | 3.1 preserve useful V2 behavior; 3.2 no normative duplication; 3.3 no silent architectural overrides; 3.4 identifiable scope; 3.5 intentional loading, with no critical content behind unreliable triggers; 3.6 understandable to humans; 3.7 challenge questionable requirements | Hard constraints. Where an invariant is under-specified (what counts as "duplication" in 3.2), I propose an operational definition (§5.1) rather than weakening it. |
| Goals | 2.1 modularity; 2.3 stable dependencies; 2.4 separation of concerns; 2.5 single source of truth; 2.6 explicit scope; 2.7 selective loading; 2.8 reliable triggering; 2.9 decision control; 2.10 policy vs enforcement; 2.11 maintainability; 2.12 efficiency; 2.13 dogfooding | Optimized together. When goals conflict, reliability and decision control win over token count, as non-goal 5.5 allows. |
| Design hypotheses | 2.2 and 4.1 layered hierarchy; 4.2 smaller modules; 4.3 skills as orchestration; 4.4 backend/frontend split; 4.5 manifest; 4.6 task-specific execution strategy | Evaluated, not assumed. 2.2/4.1 and 4.3 are substantially modified. 4.6 is mostly rejected (§13). |
| Non-goals | 5.1 agent-agnostic; 5.2 universal architectures; 5.3 React; 5.4 maximum automation; 5.5 minimum tokens at any cost; 5.6 perfect V3 in one pass | Respected. 5.2 is also an argument against a separate, swappable "Architecture layer" (§4.2). |

Requirement 2.2 is filed under Goals but says itself that "This is a design hypothesis". I treat the goal as "distinguish levels of abstraction and stability", and the concrete hierarchy as a hypothesis.

---

## 1. Executive summary

**V2 has strong content and a weak structure.** Its policies are thoughtful and deliberately guard against over-engineering: a simple domain model by default, an approval gate for consequential decisions, strict product-spec governance, the rule that verified behavior must become a test, and license checks for dependencies. None of that should be lost. The weaknesses are about *where* each policy lives, *when* it loads and *who* owns it.

**Diagnosis**

1. **Critical policy sits behind triggers that may not fire.**
   - The Development-seeding policy, including the obligation to update `DbSeeder` when the model changes, lives in the `ef-core` skill. That skill loads only if Claude decides to invoke it.
   - The always-loaded error rule hands HTTP status semantics to the `http-api` skill (`rules/error-handling.md:65`).
   - All Angular policy lives in a skill that the model must choose to invoke.
   - The architecture rule is path-scoped to `backend/**/*.cs`. It is therefore expected to be absent during planning and greenfield scaffolding, which is exactly when architecture decisions are made.
2. **The duplication is compensatory, not careless.**
   - The rule "manually verified behavior must become a maintained test" appears in 7 artifacts.
   - The list of patterns that need approval appears in 7 artifacts, with different contents.
   - The `DbSeeder` sync obligation appears in 6 artifacts.
   - The pattern is consistent: the author copied each rule to every place it might be needed, because nothing guaranteed the owner would be loaded. **If V3 does not fix loading, deduplication will fail and the copies will come back.**
3. **There is no single register of decisions.**
   - Adopted and rejected patterns are spread across `CLAUDE.md`, `rules/architecture.md`, `skills/project-structure`, `backend-layout.md`, `code-review`, `code-reviewer` and `technology-stack.md`.
   - The lists disagree, and several boundaries are unclear: a local `Result<T>` versus a project-wide Result model, Minimal APIs, custom exception hierarchies, API versioning.
4. **There is no deterministic enforcement.**
   - V2 has no `settings.json`, hooks, permissions, `.editorconfig`, analyzers, architecture tests or scripts.
   - Mechanical constraints (unused usings, Central Package Management, project reference direction, forbidden packages, destructive Git operations) are enforced only by prose.
5. **Different kinds of content are mixed in one file.**
   - Single files combine project decisions, normative policy, technique and procedure. `skills/ef-core` (657 lines) mixes architecture policy, EF technique, data-lifecycle policy and co-change obligations.
   - `technology-stack.md` holds the approved stack, arguably the most important project decision. It sits in a scaffolding skill's `references/` folder, yet `rules/dependencies.md:17-19` depends on it.

**V3 in one sentence:** decide once, in an always-loaded decision register; state each rule once, with one owner per policy; load each rule by the trigger that matches its obligation (path, always, hook, or an explicit workflow step); enforce what is mechanical; and never put normative content behind a trigger the model must choose to fire.

**Proposed shape**

```text
CLAUDE.md                                always     operating policy, decision control, product governance, workflow map, precedence
docs/architecture/decision-register.md   always     (@import) adopted decisions, approved stack, reserved decision classes
.claude/rules/{common,backend,frontend}/ path       normative constraints; one owner per policy; every file path-scoped
.claude/skills/<workflow>/               invoked    procedures: verify, code-review, build-fix, scaffold, add-dependency, ...
.claude/skills/<knowledge>/              model      technique and examples only; never originates policy
.claude/agents/code-reviewer.md          delegated  thin execution wrapper that preloads the code-review skill
.claude/settings.json + hooks/           events     permissions and deterministic triggers (co-change reminders, dependency gate)
.claude/MANIFEST.md                      humans     ownership, scope, loading and enforcement map; checked by a script, never loaded
```

**Top recommendations, in priority order**

1. **Add an always-loaded decision register.** It replaces the 7 disagreeing pattern lists and closes the gap where architecture policy is missing during planning.
2. **Keep normative content out of model-invoked skills.** Move policy into path-scoped rules. Skills keep technique and procedure only.
3. **Define decision control.** Three classes (Decided, Delegated, Reserved), a five-question classification test, and an escalation protocol that also covers headless runs.
4. **Add a small deterministic layer:**
   - Git permissions.
   - Hooks that remind Claude of the right workflow when specific files change or specific commands run.
   - Shipped config files: `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props`.
   - An architecture test that needs no new dependency.
5. **Give every policy one owner**, and use an explicit reference discipline ("check-by-reference", §5.1). Turn the review agent into a thin wrapper over the review skill.
6. **Add a path-scoped Angular rule**, so frontend policy no longer depends on a model-invoked skill.
7. **Before migrating, build a V2 policy inventory and a trigger test suite.** The inventory proves behavior is preserved. The test suite measures whether the loading assumptions hold.

**What I recommend not doing**

- Do not turn `Core → Architecture → Technology → Project → Feature → Task` into a directory hierarchy. It mixes up stability, ownership and loading mechanism. It also puts the line between technology *selection* (a project decision) and technology *knowledge* in the wrong place (§4.2).
- Do not break the system into many micro-files. Split only when triggers, owners or rate of change differ (§4.1, P7).
- Do not hardcode model IDs or effort levels into the template (§13, H-8).

---

## 2. Current V2 architecture

### 2.1 Inventory

Token counts are estimated as characters / 4.

| Artifact | Kind | Lines | ~Tokens | Loading | Primary responsibility |
|---|---|---:|---:|---|---|
| `CLAUDE.md` | Core | 123 | 1.2k | Always | Spec governance, custom settings policy, core defaults, workflow, Git |
| `SPECIFICATION.md` | Product input | 0 | 0 | Read when instructed | Product behavior (intentionally empty) |
| `CUSTOM_SETTINGS.md` | Product input | 19 | 0.2k | Read when instructed | Empty table of approved tunable values, plus a restatement of the policy |
| `rules/architecture.md` | Rule | 192 | 1.9k | `backend/**/*.cs`, `backend/**/*.csproj` | Layers, domain style, repositories, UoW, EF boundary, decision gate |
| `rules/coding-style.md` | Rule | 121 | 0.9k | `backend/**/*.cs` | C# conventions |
| `rules/error-handling.md` | Rule | 92 | 0.7k | `backend/**/*.cs` | Exceptions, outcomes, validation boundaries, cancellation |
| `rules/performance.md` | Rule | 99 | 0.8k | `backend/**/*.cs` | Async, time, HttpClient, DB efficiency, caching, optimizations |
| `rules/security.md` | Rule | 153 | 1.1k | `backend/**/*`, `frontend/**/*`, `**/*.json`, `**/*.yml`, ... | Secrets, input, SQL, authz, TLS, CORS, logging, errors |
| `rules/testing.md` | Rule | 112 | 0.8k | `backend/**/*Tests/**` | NUnit, test levels, doubles, DB tests, isolation, probes |
| `rules/dependencies.md` | Rule | 242 | 1.5k | `**/*.csproj`, `Directory.Packages.props`, `package*.json` | Version and license procedure, CPM, npm, audits |
| 26 skills (`SKILL.md`) | Skills | 7,702 | ~54k | Invoked by the model based on the description. Descriptions total ~9.7k chars (~2.4k tokens) and are always listed. | 7 workflows and 19 technology guides |
| 4 skill references | References | 1,701 | 9.4k | Read when the owning skill says so | Solution and backend layout, technology stack, security scan layers |
| `agents/code-reviewer.md` | Subagent | 166 | 1.1k | Delegated | Read-only review; restates the review skill |
| Settings, hooks, commands, `.editorconfig`, analyzers, architecture tests | — | 0 | — | — | **None exist** |

The whole V2 instruction corpus is about 296k characters (about 74k tokens).

### 2.2 How V2 works

```text
Session start ─► CLAUDE.md (always) + 26 skill descriptions (always)
                  │ pointers: architecture.md, dependencies.md, custom-settings, code-review, verify
                  ▼
Claude reads a file ─► path rules for that file
                  │ (~5.3k tokens for any backend .cs: architecture + coding-style + error-handling + performance + security)
                  │ pointers inside rules: logging, http-api, ef-core, error-handling, testing skills
                  ▼
Claude judges a skill relevant ─► skill body ─► skill references (when the skill says so)
                  ▼
Completion ─► code-review (substantial work) ─► verify   (both named in CLAUDE.md)
```

In short:

- `CLAUDE.md` is a thin router plus product governance.
- Path rules carry most backend policy.
- Skills carry everything else, including policy.
- The completion workflows re-check a hand-picked subset of policies, which is why they restate them.

### 2.3 Implicit dependencies (notable edges)

| From | To | Nature | Issue |
|---|---|---|---|
| `rules/dependencies.md:17-19` | `skills/project-structure/references/technology-stack.md` | A rule depends on a skill-internal reference for the approved stack. | Inverted dependency: a stable, path-loaded rule depends on a hidden file inside a skill. |
| `rules/error-handling.md:53,65,92` | `logging`, `http-api` and `error-handling` skills | The rule names skills as the canonical owners of logging policy and HTTP semantics. | Canonical policy depends on a model-invoked skill. |
| `rules/performance.md:37,49` | `httpclient-factory`, `resilience`, `ef-core` skills | Hands off detail. | Acceptable as guidance pointers. |
| `skills/project-structure:245-252` → `technology-stack.md:79-86` → `skills/ef-core:343-552` | — | A three-step chain behind "every project gets a Development seeder". | A template default depends on two separate model decisions. |
| `agents/code-reviewer.md:40-54` | 12 skills | Routing table. | Useful, but the agent also restates the review criteria. |
| `skills/verify:86`, `skills/build-fix:255` | `angular` skill, for "frontend testing conventions" | Points to an owner that barely covers the topic (`skills/angular:310-327`). The runner choice actually lives in `technology-stack.md:237-241`. | The pointer leads to the wrong place. |
| `rules/security.md:52-53` | FluentValidation | A technology choice inside a security rule. | Stable policy tied to a changeable technology choice. |
| `CLAUDE.md:78,110-111` | `custom-settings`, `code-review`, `verify` | Explicit workflow pointers from always-loaded context. | Good pattern; keep it. |

### 2.4 What V2 does well (must be preserved)

- **A stance against over-engineering, stated with reasons.** Simple domain by default (`rules/architecture.md:26-42`). "A service becoming too large is a signal ... not an automatic reason to introduce another architectural pattern" (`:56`).
- **An approval gate for consequential decisions**, balanced by an explicit "do not ask for approval for routine local implementation decisions" (`rules/architecture.md:152-178`). The balancing clause protects Claude's autonomy.
- **Product governance.** Claude must not invent observable behavior, and string-comparison semantics count as product behavior (`CLAUDE.md:25-38`). This rule is unusually precise and valuable.
- **A clear split between the spec and the settings file.** The spec owns behavioral intent; `CUSTOM_SETTINGS.md` owns approved values (`CLAUDE.md:45-82`).
- **Honest verification.** Report NOT RUN rather than pretend (`skills/verify:222-237`). Build-fix iterations are bounded (`skills/build-fix:369-385`).
- **Behavioral probes become maintained tests** (`skills/testing:344-376`).
- **Dependency hygiene.** Stable versions only, license checks, and explicit handling of commercial packages (`rules/dependencies.md:21-113`).
- **Separated workflows.** code-review, verify and build-fix each say what they are not.
- **Context-aware security guidance**, including false-positive lists (`skills/security-scan:194-213`).
- **Progressive disclosure is already in use.** `project-structure` says "Do not load every reference merely because this skill was triggered" (`skills/project-structure:56`); `security-scan` follows the same pattern.

---

## 3. V2 problems and risks

### 3.1 Semantic duplication of policy

This table lists only duplication of normative content or responsibility. Similar wording that serves a different purpose is excluded.

| # | Policy | V2 locations | Do the copies disagree? |
|---|---|---|---|
| D1 | Patterns and infrastructure that need approval | `CLAUDE.md:89-93`; `rules/architecture.md:41-42,54,152-178,190-192` (the gate is stated again at 190-192 in the same file); `skills/project-structure:301-328`; `references/backend-layout.md:28-32,86,239`; `skills/code-review:120-130`; `agents/code-reviewer.md:56-60` | **Yes.** `project-structure` adds SharedKernel, BuildingBlocks, EventBus, Kubernetes and state-management frameworks. The gate adds multiple DbContexts, distributed caching and auth architecture. The agent adds Minimal APIs and "generic repositories", although an Infrastructure-internal generic repository is explicitly allowed (`rules/architecture.md:108-117`). |
| D2 | Manually verified behavior must become a maintained test | `rules/testing.md:95-103`; `skills/testing:20,344-376,417,431`; `skills/verify:34-35,115-117,119-131,208`; `skills/build-fix:419-431`; `skills/code-review:192-193`; `agents/code-reviewer.md:101-102` | Mostly consistent; 7 artifacts. |
| D3 | `DbSeeder` must follow Domain and persistence changes | `skills/ef-core:512-552,567-571,634,654` (owner); `skills/verify:146-150`; `skills/code-review:164-169`; `agents/code-reviewer.md:90-91`; `skills/custom-settings:92`; `references/technology-stack.md:79-86` | Consistent; 6 artifacts. |
| D4 | Clean Architecture boundary checklist | `rules/architecture.md:9-19` (owner); `references/backend-layout.md:298-327`; `skills/code-review:109-118`; `agents/code-reviewer.md:79-88`; `skills/verify:133-146`; `skills/build-fix:400-417`; `skills/ef-core:17-33`; `skills/project-structure:158-169` | Consistent; 8 artifacts. |
| D5 | Repository, UoW and generic repository policy | `rules/architecture.md:77-150`; `skills/ef-core:98-169,619-634,636-657` | Nearly a full copy. |
| D6 | Spec conformance and string-comparison semantics | `CLAUDE.md:6-43,107-108`; `skills/code-review:56-90`; `skills/verify:204` | Consistent. The comparison list is copied almost word for word. |
| D7 | `CUSTOM_SETTINGS.md` policy and "what does not belong here" | `CLAUDE.md:45-82`; `CUSTOM_SETTINGS.md:3-19`; `skills/custom-settings:13-45` | Consistent; three copies of the exclusion list. |
| D8 | Conditional dependencies (Mapster, resilience, Testcontainers, Playwright) | `rules/dependencies.md:209-232`; `references/technology-stack.md:335-364` | Identical. |
| D9 | What the dependency policy covers | `rules/dependencies.md` (owner); `references/technology-stack.md:312-333` (re-lists what the rule owns); `skills/build-fix:257-307` | Consistent. |
| D10 | Never log sensitive data | `rules/security.md:124-139`; `skills/logging:127-141`; `references/scan-layers.md:479-495`; `skills/serilog:272-282`; `skills/authentication:218-220` | The lists differ slightly (`logging` adds authorization headers and full bodies). |
| D11 | No internal details in error responses | `rules/security.md:141-146`; `rules/error-handling.md:62-63`; `skills/error-handling:94-98`; `skills/http-api:355-361`; `skills/swagger:123-125`; `skills/health-check:139-144` | Consistent. |
| D12 | Log an exception once, where it is handled | `rules/error-handling.md:45-53`; `skills/error-handling:284-296`; `skills/logging:82-91` | Consistent. |
| D13 | Propagate CancellationToken; client cancellation is not a failure | `rules/performance.md:19-20`; `rules/error-handling.md:67-78`; `skills/error-handling:298-305`; `skills/httpclient-factory:117-128`; `skills/resilience:213-219` | Consistent. The two rules share a path scope, so they always load together and say the same thing twice. |
| D14 | Validation boundaries; "don't move Domain invariants into FluentValidation" | `rules/error-handling.md:80-92`; `skills/error-handling:196-258`; `rules/security.md:50-56`; `references/technology-stack.md:88-108`; `references/backend-layout.md:127-133` | Consistent. |
| D15 | Technology choices (NUnit, FluentValidation, Swagger, no NgRx by default, Vitest) | `rules/testing.md:9-16`, `skills/testing:15`, `technology-stack.md:212-217`; `rules/security.md:52`; `skills/swagger:15-28,62-63` and `technology-stack.md:189-210`; `skills/angular:256-270` and `technology-stack.md:292-303`; `skills/build-fix:109-111` | Consistent, but no owner. |
| D16 | Backend test placement; Domain.Tests only when needed | `skills/project-structure:189-223`; `references/solution-layout.md:96-163`; `references/backend-layout.md:273-296`; `references/technology-stack.md:219-235` | Consistent; 4 copies. |
| D17 | No automatic production migrations | `skills/ef-core:581-587`; `skills/docker:224-232`; `skills/ci-cd:219-233` | Consistent. |
| D18 | Frontend guards and hidden UI are not security | `skills/angular:24-25,194-210`; `skills/authentication:148-150`; `rules/security.md:82-83`; `skills/build-fix:413`; `skills/code-review:142`; `references/scan-layers.md:378-382` | Consistent. |
| D19 | C# style: primary constructors, records, `var` | `rules/coding-style.md:28-83`; `skills/modern-csharp:21-63,156-163` | Consistent. The skill says "follow coding-style.md" and then restates it. |
| D20 | Options registration | `skills/configuration:40-63`; `skills/dependency-injection:200-214` | Consistent. |
| D21 | Timeouts, 429/Retry-After, retries of unsafe methods | `skills/httpclient-factory:130-206`; `skills/resilience:68-130` | Consistent, with heavy overlap. |
| D22 | 401 vs 403 | `skills/http-api:163-193`; `skills/authentication:152-172` | Consistent. |
| D23 | Review criteria, priorities and output format | `skills/code-review` and `agents/code-reviewer.md:62-166`. The agent says it will not redefine the methodology (`:19-20`), then does. | **Yes**, see C1. |
| D24 | Git safety | `CLAUDE.md:116-123`; `skills/git-workflow:12-30,62-73` | Consistent. |

### 3.2 Conflicts and ambiguities

| # | Issue | Evidence | How it can go wrong |
|---|---|---|---|
| C1 | The review priority order differs between the agent and the skill. | `agents/code-reviewer.md:64-73` puts security second. `skills/code-review:16-24` puts architecture second, and security third next to data integrity. | Inline and delegated reviews order severity differently. |
| C2 | Unclear whether a Result type needs approval. | The gate lists a "project-wide Result/railway-oriented programming model" (`rules/architecture.md:166`). The rule lists "a deliberately adopted `Result<T>` pattern" as an allowed option (`rules/error-handling.md:20`). The skill says "Consider it when…" and "If introduced, prefer typed errors" (`skills/error-handling:342-368`). | Claude adds a shared `Result<T>` "for one service", which becomes a project convention without approval. |
| C3 | Unclear whether Minimal APIs need approval. | Controllers are the "default" (`rules/architecture.md:60`). "Do not create Minimal API endpoint groups unless explicitly requested" (`references/backend-layout.md:239`) loads only during scaffolding. The gate only covers "replacing an approved baseline framework". | Nobody can tell whether one Minimal API endpoint "for one small thing" needs approval. |
| C4 | Custom business exceptions have no decision owner. | "A project may deliberately use typed exceptions … consistent project-level decision" (`skills/error-handling:260-268`). Who decides is not stated, and the gate does not mention it. | Nobody owns the decision. |
| C5 | Serilog sink advice conflicts with keeping the stack minimal. | `skills/serilog:319-325` suggests Seq, Elasticsearch and `AuditTo` in its decision table. `technology-stack.md:125-127` says "Add sinks only when they are required". `skills/logging:190` says logs are not an audit store unless an audit design has been adopted. | A table row reads as a recommendation, leading to unrequested sinks or auditing through logs. |
| C6 | The reviewer lists generic repositories among patterns it must not require. | `agents/code-reviewer.md:59-60` lists "generic repositories" next to MediatR. `rules/architecture.md:108-117` allows one inside Infrastructure. | The reviewer may treat an allowed pattern as suspicious. |
| C7 | No one decides which cross-stack contract wins. | "Determine which contract is authoritative" (`skills/build-fix:208`) is never answered anywhere. | Frontend and backend get patched into shapes that disagree. |
| C8 | Two versions of the test naming convention. | `MethodOrScenario_Condition_ExpectedBehavior` (`rules/testing.md:111`) versus `MethodOrScenario_StateOrCondition_ExpectedBehavior` (`skills/testing:321`). | Trivial, but it shows how independent copies drift apart. |
| C9 | Unclear how existing code relates to template policy. | "Follow the repository's existing conventions" (`rules/coding-style.md:10`). "Do not force an established project to match this template" (`skills/project-structure:298-299`). Nothing says how existing code relates to architecture decisions. | In an existing project, Claude may spread a legacy pattern that contradicts policy, or refactor without being asked. |

### 3.3 Unclear or inverted ownership

- **The approved technology stack** is a project decision. It lives in `skills/project-structure/references/technology-stack.md`, which loads only during scaffolding, and a rule depends on it (§2.3).
- **Everyday naming policy** ("Supporting Type Roles", `references/backend-layout.md:88-119`) applies to every feature: `Service`, `Rules`, `Policy` and `Validator` suffixes, and no `Helpers` or `Utils` folders. It is hidden in a scaffolding reference that is expected to load almost never during feature work.
- **The Development data lifecycle** is template-wide project policy stored in a technology skill (`skills/ef-core:343-587`). It covers seeding by default, seeding in Development only, and never migrating Production automatically.
- **Logging policy has two declared owners.** `rules/error-handling.md:53` says the `logging` skill owns it; `rules/security.md:124-139` owns the sensitive-data part.
- **Application outcome naming** (no HTTP-named categories, `skills/error-handling:131-140`) is an architecture boundary rule stored in a technique skill.
- **Frontend policy has no rule at all.** `skills/angular` is its only carrier.
- **Rules and skills share names** (`rules/error-handling.md` and `skills/error-handling`; `rules/testing.md` and `skills/testing`). A pointer such as "follow error-handling" is ambiguous.

### 3.4 Poor cohesion and mixing of policy with procedure

| Artifact | Mixed concerns | Evidence |
|---|---|---|
| `CLAUDE.md` | Product governance, settings policy, architecture principles, workflow, Git | Sections at lines 6, 45, 84, 100, 116 |
| `rules/architecture.md` | Layer rules, persistence patterns, governance gate | `:77-150` persistence; `:152-192` gate |
| `rules/performance.md` | Performance, async correctness, testability (TimeProvider), resource lifetime (HttpClient), policy on when to adopt caching | `:15-65` |
| `rules/security.md` | Security, a technology choice, authorization style | `:52`, `:67-83` |
| `skills/ef-core` (657 lines) | Architecture policy, EF technique, data-lifecycle policy, co-change rules | `:17-33`, `:35-341`, `:343-587` |
| `skills/verify` | Procedure, plus restated policy (seeding, settings drift, usings, probes) | `:133-153`, `:192-208` |
| `skills/build-fix` (479 lines) | Repair loop, plus restated dependency, architecture, testing and frontend policy | `:186-193`, `:257-307`, `:400-431` |
| `skills/project-structure` and its references | Scaffolding procedure, project decisions (stack, layout), everyday naming policy | See §3.3 |
| `technology-stack.md` | Decisions, dev database configuration, seeding summary, test placement, restated dependency rule | `:48-86`, `:212-254`, `:312-333` |

### 3.5 Missing deterministic enforcement

V2 relies on prose for rules that tooling could check. The full mapping is in §10.2. Examples:

- Project reference direction.
- EF Core or ASP.NET Core types in Application or Domain.
- Central Package Management.
- Floating or prerelease versions.
- Forbidden packages: MediatR, deprecated Polly integrations, EF InMemory in tests.
- Unused usings; file-scoped namespaces and naming.
- CancellationToken forwarding (CA2016).
- Misused log templates (CA2254, CA2017).
- SQL built from strings (CA2100, and EF Core's warning for interpolated raw SQL).
- Destructive Git operations.

`references/solution-layout.md:235-240` already says "Prefer enforceable tooling configuration over duplicating mechanical formatting rules in Claude instructions". The template ships no such configuration.

### 3.6 Defects found along the way

- `rules/testing.md:109-112` ends with an unclosed code fence.
- `rules/security.md:15-18` has a `description` frontmatter field, which is expected to have no effect on rule loading.
- The `skills/swagger` description has no "use when" trigger clause; every other skill's description does.
- `skills/verify:86` and `skills/build-fix:255` point to the `angular` skill for frontend testing conventions it barely contains.
- "normally" appears 54 times across 28 files. Each time, it is unclear whether Claude may deviate on its own judgment (§5.4).

### 3.7 Root cause

Most of these problems come from one gap. **V2 has no model of which mechanism should carry which kind of instruction**, so there is no confidence that an owner will be loaded when it is needed. The author responded sensibly by duplicating. V3 has to fix the choice of mechanism first (§6.4). Deduplication follows from that.

---

## 4. Proposed V3 architecture

### 4.1 Design principles

| # | Principle | Rationale |
|---|---|---|
| P1 | **Decide once.** Each adopted or rejected architecture or technology choice has exactly one entry in the decision register. | Removes D1 and D15, and makes deviations detectable. |
| P2 | **Load decisions up front, details on demand.** The compact register is always loaded. Implementation constraints load by path. Technique loads when needed. | Decisions are made during planning, before any file is touched. |
| P3 | **Keep normative content out of model-invoked skills.** Must / must-not rules live in always-loaded or path-scoped files. A knowledge skill can improve quality, but if it fails to load, no rule may be lost. | Invariant 3.5. |
| P4 | **Match the trigger to the obligation.** Code rules load by file path. Obligations not tied to a file load always. Obligations tied to a detectable event (a file changed, a command ran, the session is ending) use a hook. Everything else uses an explicit workflow step. | Removes the reason for compensatory copies like D2 and D3. |
| P5 | **One owner; everything else points to it.** Other files may point to the owner and may carry a one-line check (§5.1). They never restate the policy with conditions of their own. | Makes invariant 3.2 workable. |
| P6 | **Enforce what is mechanical; keep in the prompt what improves generation.** | Goal 2.10, with the prompt's caveat. |
| P7 | **Split by trigger, owner and rate of change, not by size.** Merge modules that load together and change together. | Guards against over-fragmentation. |
| P8 | **A human can see the whole system from two files.** `CLAUDE.md` shows everything that is always loaded (through explicit imports); `.claude/MANIFEST.md` maps the rest. | Invariant 3.6. |

### 4.2 Evaluating `Core → Architecture → Technology → Project → Feature → Task`

**Ideas worth keeping:** ordering by stability; the rule that more changeable instructions depend on more stable ones; the insistence that feature and task inputs must not silently override architecture.

**Problems if this becomes *the* structure:**

1. **It mixes three independent properties:** level of abstraction, who may change it (template author, project team, product owner) and how it loads. One piece of architecture policy needs two mechanisms: the decision always loaded, the implementation details loaded by path. A single "Architecture layer" cannot express that.
2. **"Technology" hides two different things.** Technology *selection* ("use EF Core + SQL Server", "use Serilog") is a project decision; it belongs with the decisions and changes only with approval. Technology *knowledge* ("how to write a good EF projection") is reusable technique. V2's worst ownership bugs come from mixing the two: `technology-stack.md` inside a skill, FluentValidation inside `security.md`. Putting "Technology" below "Architecture" and above "Project" also means the project can no longer choose its own technology.
3. **A separate, swappable "Architecture" layer serves a non-goal.** Supporting other architectures is non-goal 5.2. In a template, Clean Architecture is itself a project-level default.
4. **"Feature" and "Task" are inputs, not instruction layers.** The template does not ship feature or task instructions. It ships the rules for how those inputs interact with policy: they may define behavior; they may not change decisions without approval. Treating them as layers invites ceremony, such as a mandatory spec file per feature.
5. **A linear chain ignores cross-cutting concerns.** Workflows (verify, review) and security cut across every level. Backend versus frontend scope is independent of abstraction level.

**Verdict:** keep the stability ordering as a dependency rule (§4.4). Replace the linear hierarchy with **instruction kinds × scopes** (§4.3).

### 4.3 The V3 model: instruction kinds × scopes

**Kinds.** The kind says what an artifact is, and that decides where it lives, how it loads and who may change it.

| Kind | Responsibility | Mechanism | Who may change it | Stability |
|---|---|---|---|---|
| K1 Operating policy | How Claude works: precedence, scope discipline, decision control, product governance, completion contract | `CLAUDE.md` (always) | Template maintainers | Most stable |
| K2 Project decisions | What the project has decided: architectural style, adopted and non-adopted patterns, approved stack, decisions that need approval | `docs/architecture/decision-register.md` (always, via `@import`), plus ADRs (not loaded) | Humans, through an ADR | Stable |
| K3 Standards | Normative constraints for work in one scope; they implement K2 | `.claude/rules/<scope>/*.md` (by path) | Template maintainers; a project may add `project-*.md` rules | Stable to medium |
| K4 Knowledge | Technique, examples and trade-offs *within* the adopted decisions | Knowledge skills, plus references | Template maintainers | Medium |
| K5 Workflows | Procedures with steps, checks, outputs and stop conditions | Workflow skills, plus agents | Template maintainers | Medium |
| K6 Enforcement | Deterministic triggers and checks | `settings.json` permissions, hooks, scripts, analyzers, architecture tests | Template maintainers and the project | Medium |
| K7 Product inputs | Behavior, values, feature specs, tasks | `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, optional `docs/features/*.md`, prompts | Product owner or user | Most changeable |

**Scopes.** The scope says where an artifact applies (details in §8):

- `common`
- `backend` (C#/.NET)
- `backend-tests`
- `frontend` (Angular, including its tests)
- `delivery` (containers, CI/CD, health checks)
- `repo/meta` (the instruction system itself)

Every artifact has exactly one kind and one scope. Together they decide its directory and loading mechanism. That answers requirement 2.11: "where does a rule belong, and when is it loaded?"

### 4.4 Dependency direction

"A → B" means A may reference B and must conform to it. B must not reference A.

```text
K7 Product inputs ──(may request changes to)──► K2 Decisions   (never override them)

K5 Workflows ──► K4 Knowledge ──► K3 Standards ──► K2 Decisions ──► K1 Operating policy
     │                                  ▲
     └────(explicit "read rule X" steps)─┘

K6 Enforcement ──(implements / checks)──► K3, K2   (its messages point to the owning file)
Agents ──► K5 / K4   (they preload skills and contain no criteria of their own)
Skill references ──► owned by exactly one skill; no other artifact may depend on them
```

V2 breaks this direction in three places, and V3 fixes all three:

- A rule depends on a skill reference (`dependencies.md` → `technology-stack.md`).
- A rule names skills as the owners of its policy (`error-handling.md` → `http-api`, `logging`).
- A standard depends on a technology choice (`security.md` → FluentValidation).

### 4.5 Proposed layout

```text
<template root>/
├── CLAUDE.md                          K1  always   ~110 lines
├── SPECIFICATION.md                   K7           unchanged (empty in the template)
├── CUSTOM_SETTINGS.md                 K7           table + format note + pointer (policy moves to CLAUDE.md)
├── .editorconfig                      K6  asset    style, naming, IDE0005 severities            [new]
├── Directory.Build.props              K6  asset    Nullable, analyzers, EnforceCodeStyleInBuild [new]
├── Directory.Packages.props           K6  asset    ManagePackageVersionsCentrally=true          [new]
├── docs/
│   └── architecture/
│       ├── decision-register.md       K2  always   imported by CLAUDE.md                        [new]
│       └── decisions/                              ADRs, created when the first decision is recorded
└── .claude/
    ├── MANIFEST.md                    meta  not loaded: ownership, scopes, loading, enforcement, extension guide [new]
    ├── settings.json                  K6    permissions + hook registration                     [new]
    ├── hooks/                         K6    small, fast scripts (§10.4)                          [new]
    ├── rules/                               every file MUST declare `paths`
    │   ├── common/
    │   │   ├── security.md                  secrets, sensitive data in logs, error exposure, TLS validation
    │   │   └── dependencies.md              CPM, pinned stable versions, lockfile, narrow references
    │   ├── backend/
    │   │   ├── architecture.md              layers, project refs, layer responsibilities, composition root, code organization
    │   │   ├── persistence.md               repositories, UoW, EF boundary, migrations, dev seeding + seed co-change
    │   │   ├── api.md                       thin controllers, default status-code table, ProblemDetails, contract authority
    │   │   ├── error-handling.md            outcomes vs exceptions, central handling, log once, validation boundaries
    │   │   ├── csharp.md                    conventions + async / cancellation / TimeProvider / HttpClient lifetime + optimization discipline
    │   │   ├── security.md                  input trust, SQL, server-side authz, CORS, transport, data protection
    │   │   └── testing.md                   NUnit policy, test levels, doubles, DB tests, isolation, naming
    │   └── frontend/
    │       └── angular.md                   standalone, feature structure, data-access boundary, state, guards ≠ security, tests [new]
    ├── skills/
    │   │   ── workflows ──
    │   ├── scaffold/                        (was project-structure) + references/{solution-layout,backend-layout,dev-environment}.md + assets/
    │   ├── verify/
    │   ├── code-review/
    │   ├── build-fix/
    │   ├── add-dependency/                  procedure from dependencies.md: version, license, commercial options   [new]
    │   ├── change-settings/                 (was custom-settings)
    │   ├── architecture-decision/           decision request + ADR recording + register update               [new]
    │   ├── security-scan/                   + references/scan-layers.md
    │   ├── git-workflow/
    │   ├── template-maintenance/            optional; user-invoked only                                     [new, optional]
    │   │   ── knowledge ──
    │   ├── ef-core/                         technique only; + references/dev-seeding.md (example code)
    │   ├── http-api/                        edge cases: conditional requests, idempotency, 202/406/415, 5xx roles
    │   ├── aspnet-error-handling/           (was error-handling) IExceptionHandler, outcome mapping, FluentValidation wiring
    │   ├── dotnet-testing/                  (was testing) NUnit, WebApplicationFactory, DB strategy technique
    │   ├── authentication/
    │   ├── logging/                         + references/serilog.md (serilog skill merged in)
    │   ├── configuration/
    │   ├── dependency-injection/
    │   ├── outbound-http/                   (httpclient-factory + references/resilience.md)
    │   └── caching/  swagger/  api-versioning/  health-check/  docker/  ci-cd/  angular/  modern-csharp/
    └── agents/
        └── code-reviewer.md                 read-only; preloads code-review; no criteria of its own
```

Counts:

- Rules go from 7 to 10. Each has a single trigger and a single owner.
- Skills stay at 26 (plus 1 optional): two merges, two new workflows.

The gain comes from ownership and from choosing the right mechanism, not from the file count.

### 4.6 Precedence and conflict resolution (stated once, in `CLAUDE.md`)

1. **Deterministic controls** (permissions, hooks, failing checks) are never bypassed. If one blocks something legitimate, Claude surfaces it.
2. **An explicit user instruction in the current task.**
   - For a Reserved decision (§9), an explicit instruction counts as approval, and Claude records it (§9.5).
   - If the instruction contradicts `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`, those files get updated; they are not bypassed.
3. **Human-approved project sources, each authoritative in its own area:** `SPECIFICATION.md` for behavior, `CUSTOM_SETTINGS.md` for values, the decision register and ADRs for architecture and stack.
4. **Standards** (`.claude/rules`).
5. **Guidance** (knowledge skills, references, examples). If guidance contradicts levels 3–4, the rule wins and the contradiction is reported as a template defect.
6. **Existing code conventions** override the template's *style* guidance, never its decisions. Where existing code contradicts a decision, Claude surfaces it and does not spread either version.

**If two sources at the same level conflict, stop and ask.** This generalizes V2's spec-versus-settings rule (`CLAUDE.md:53-56`). Feature specs and tasks can *request* a decision change. They never silently override one (invariant 3.3).

### 4.7 Extension points

| To add… | Files touched | Files left alone |
|---|---|---|
| A technology (e.g. a Redis cache) | ADR and register entry; one knowledge skill (new or existing); a rule section only if new must-rules arise; a MANIFEST row | `CLAUDE.md`, workflows |
| A project decision (e.g. approve CQRS) | The `architecture-decision` workflow: ADR, register update, and the rules listed in the entry's "Affects" column | Unrelated rules and skills |
| A project-specific coding rule | `.claude/rules/<scope>/project-<topic>.md` with `paths`, plus a MANIFEST row | Template rules |
| Product behavior or tunable values | `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`, plus an optional `docs/features/<feature>.md` linked from the spec | Instruction files |
| A workflow | A new workflow skill; one line in the `CLAUDE.md` workflow map (only if it must be invoked automatically); a MANIFEST row | Rules |
| A frontend concern | A section in `rules/frontend/angular.md`, or a new `rules/frontend/<topic>.md` | Backend rules |

This meets requirement 2.11 in a measurable form: adding a technology touches at most three instruction files, by a documented procedure.

### 4.8 Illustrative `CLAUDE.md` skeleton (not final wording)

```markdown
# Project Instructions
ASP.NET Core + Angular Clean Architecture template. Backend first.

@docs/architecture/decision-register.md

## Precedence
<the six levels from §4.6, ~10 lines>

## Working agreement
1. Inspect relevant code before non-trivial changes. Keep changes in scope; preserve behavior.
2. Plan against the decision register. If the plan needs a Reserved decision, follow Decision control.
3. Implement following the rules for the files you touch.
4. Completion contract: behavior you verified manually must be covered by maintained automated tests
   (or by existing tests you confirmed). Substantial work: run `code-review` (via the code-reviewer agent).
   Always: run `verify`.

## Decision control
<Decided / Delegated / Reserved definitions, the five-question test, the Decision Request format, headless behavior (~30 lines)>

## Product governance
<spec authority, no invented observable behavior, string-comparison semantics, CUSTOM_SETTINGS ownership
 and approval steps; consolidated from V2 CLAUDE.md:6-82 (~35 lines)>

## Workflow map
dependency change → add-dependency · CUSTOM_SETTINGS change → change-settings · new solution/projects → scaffold
build/test broken → build-fix · reserved decision → architecture-decision · Git operations → git-workflow

## Git
Repository-changing Git operations only when explicitly requested (also enforced by permissions).
```

### 4.9 Scope rules

- **Every rule file declares `paths`.** There are no always-loaded rules. Always-loaded content is only what `CLAUDE.md` contains or imports. This keeps the always-loaded set visible in one file, and stops a forgotten `paths` field from silently making a rule global.
- **A rule contains only content that applies to every file its `paths` match.** Content for a narrower set of files moves to a narrower rule. For example, controller rules move to `api.md`.
- **Scope is expressed twice:** by directory (`rules/backend/…`) and by `paths`. The MANIFEST lists both, and the check script confirms each rule's paths fit its scope directory.
- **Path globs rely on the template's naming convention** (`backend/<Name>.Domain/…`). This coupling is explicit: it is documented in the MANIFEST and checked by the scaffold workflow.

---

## 5. Instruction ownership model

### 5.1 What counts as duplication

Invariant 3.2 only works with a precise definition.

| Form | Allowed? | Example |
|---|---|---|
| **Owner statement:** the rule with its conditions, exceptions and rationale | Exactly once | `rules/backend/persistence.md`: "Update DbSeeder in the same change when a model change affects seeded entities…" |
| **Pointer:** "see X" | Yes | "Status-code defaults: `rules/backend/api.md`." |
| **Check-by-reference:** a one-line yes/no check plus the owner's path, with no conditions, exceptions or rationale of its own | Yes, but only in workflows and review criteria | In verify: "☐ Seed data still valid for changed entities? (persistence.md §Seeding)" |
| **Decision summary:** a register entry naming the choice, with details left to the rule | Yes, in the register only | "D-04 Persistence: specific repositories + IUnitOfWork (details: persistence.md)" |
| **Restatement:** the policy with its own wording, conditions or examples, outside the owner | **No** | V2's `ef-core` restating the repository and UoW policy |

Check-by-reference deliberately accepts a small amount of repetition in exchange for reliability when work is being completed. It is safe because the check carries no nuance that could drift; all nuance stays with the owner. The check script (§10.4) can confirm that each check points to an existing section of its owner.

### 5.2 Ownership table

| Policy category | V3 owner | V2 locations consolidated | How others refer to it |
|---|---|---|---|
| Precedence and conflict handling | `CLAUDE.md` §Precedence | Implicit, scattered | — |
| Product behavior authority, no invented behavior, string semantics | `CLAUDE.md` §Product governance | `CLAUDE.md:6-43`, `code-review:56-90`, `verify:204` | code-review: check-by-reference |
| Tunable values policy | `CLAUDE.md` §Product governance | `CLAUDE.md:45-82`, `CUSTOM_SETTINGS.md:3-19`, `custom-settings:13-45` | `CUSTOM_SETTINGS.md` header: format + pointer. `change-settings`: procedure only. |
| Decision classes and escalation | `CLAUDE.md` §Decision control | `CLAUDE.md:91-93,113-114`, `architecture.md:152-192` | code-review checks against the register |
| Adopted and non-adopted patterns, approved stack, conditional technologies | Decision register | D1, D8, D15, D16, `technology-stack.md` | Rules cite IDs, e.g. "(D-03)" |
| Layer boundaries, project reference graph, code organization, naming by type role | `rules/backend/architecture.md` | `architecture.md:9-75`, `backend-layout.md:88-133,298-327`, the D4 copies | Architecture tests implement it; review checks it |
| Repository, UoW, EF boundary, migrations, dev seeding, seed co-change | `rules/backend/persistence.md` | `architecture.md:77-150`, `ef-core:17-169,343-587`, the D3 and D17 copies | ef-core skill: technique only. Hook H4: reminder. |
| Controller responsibilities, default status codes, contract authority | `rules/backend/api.md` | `architecture.md:58-75`, `http-api:487-511`, `authentication:152-172`, `build-fix:208` | http-api skill: edge cases only |
| Exceptions vs outcomes, central handling, log once, validation boundaries, outcome naming | `rules/backend/error-handling.md` | The rule, plus the policy parts of the `error-handling` skill, `logging:82-91`, `security.md:50-56` | — |
| C# conventions, async and cancellation, TimeProvider, HttpClient lifetime, optimization discipline | `rules/backend/csharp.md` | `coding-style.md`, `performance.md`, overlaps in `modern-csharp` | modern-csharp: C# 14 feature reference and modernization procedure |
| Secrets, sensitive logging, error exposure, TLS validation | `rules/common/security.md` | `security.md:23-36,124-146`, D10, D11 | logging, configuration, docker, ci-cd, scan-layers: pointers |
| Server-side security (input, SQL, authz, CORS, data protection) | `rules/backend/security.md` | `security.md:38-122` | authentication skill: technique |
| Backend test policy | `rules/backend/testing.md` | The `testing.md` rule, plus the policy parts of the `testing` skill | dotnet-testing: technique |
| Manually verified behavior must become a test | `CLAUDE.md` §Completion contract | D2 (7 copies) | verify, code-review, build-fix: check-by-reference |
| Dependency hygiene (normative) | `rules/common/dependencies.md` | `dependencies.md:115-242`, `build-fix:283-307` | — |
| Dependency selection procedure | `skills/add-dependency` | `dependencies.md:21-113` | `CLAUDE.md` workflow map; hook H1 |
| Angular policy | `rules/frontend/angular.md` | Principles in the `angular` skill, the frontend side of D18 | angular skill: technique |
| Git safety | `CLAUDE.md` §Git, plus permissions | D24 | git-workflow: conventions only |
| Review criteria and output format | `skills/code-review` | D23 | The agent preloads it |
| Verification procedure | `skills/verify` | — | — |

### 5.3 What each artifact may and may not contain

| Artifact | May contain | Must not contain |
|---|---|---|
| `CLAUDE.md` | Operating policy whose trigger is not a file path; precedence; the decision protocol; product governance; the workflow map; the register import | Technology details; architecture specifics (those go in the register or rules); long procedures |
| Decision register | The decision, its status, who may change it, "details in", and "affects" (dependent rules and skills) | How-to content; long rationale (that goes in ADRs) |
| Rules | Must / default / prefer statements with a one-line rationale; compact decision tables; a "Related skills" footer | Procedures; long examples; adopt or reject decisions (cite register IDs instead); content for files outside its `paths` |
| Workflow skills | Steps, stop conditions, output formats, check-by-reference items, explicit "read `rules/…` if not loaded" steps | New normative policy; restatements |
| Knowledge skills | Technique, examples, and trade-offs among options the register *allows* | Must-rules not owned elsewhere; decisions; restated policy |
| Skill references | Depth for their own skill | Anything another artifact depends on. Such content moves up to a rule or the register. |
| Assets | Literal files that workflows copy (configs, test skeletons, ADR template) | Prose policy |
| Agents | Role, tool limits, how to determine scope, return format, preloaded skills | Criteria (those live in skills) |
| Hooks and scripts | Detection logic; messages that name the owning file | Judgment |
| `SPECIFICATION.md`, feature specs | Product behavior | Engineering policy or architecture choices (they may *request* them) |
| `CUSTOM_SETTINGS.md` | The table of approved values; a format note; a pointer to the policy | Restated policy |
| `MANIFEST.md` | Inventory, ownership, loading, enforcement, extension guide | Policy text |

### 5.4 Normative vocabulary

V2 mixes "must", "do not", "normally", "prefer", "may" and "should". "Normally" (54 times in 28 files) causes the most ambiguity: it never says whether Claude may deviate on its own judgment. V3 defines the following terms in the MANIFEST and uses them consistently:

- **must / must not.** A violation is a defect. Enforced deterministically where possible.
- **default:** Do this unless the context gives a concrete reason not to, and mention any deviation in the summary. Deviating is a Delegated decision.
- **prefer / avoid.** Guidance; Claude uses judgment.
- **requires approval.** Reserved; follow Decision control.

### 5.5 Policy IDs

**Recommendation:** give stable IDs to register entries (`D-01…`) and reserved classes (`R-1…`), because rules, reviews and ADRs cite them. Do *not* number every rule statement: it hurts readability, and heading anchors are enough. Benchmarks can classify violations by `file#section` (Q3).

---

## 6. Loading and triggering model

### 6.1 Mechanisms and expected reliability

| Mechanism | Expected reliability | Best for | Weakness |
|---|---|---|---|
| Always loaded (`CLAUDE.md` and its imports) | Highest | Decisions; obligations not tied to a file | Permanent context cost; diluted if it grows too large |
| Path-scoped rule | High once a matching file is touched (exact trigger needs testing) | Constraints for code in a scope | Absent during planning, greenfield work, CLI-only actions and Q&A |
| Explicit pointer to a workflow, from always-loaded or path-loaded content | Medium to high | Completion workflows | Depends on Claude following the instruction |
| Reminder injected by a hook | The trigger is deterministic; whether Claude acts on it depends on instruction-following | Co-change obligations; gates on commands | Depends on platform and runtime; adds latency; can misfire |
| Explicit "read rule X" step inside an active workflow | High | Greenfield (no files yet); subagents | Extra tool calls |
| Skill preloaded by a subagent | Deterministic, if `skills:` preload is supported (verify) | Review | Depends on the Claude Code version |
| Skill invoked by the model (description match) | Variable and untested. Plausibly lower for routine work where Claude feels competent: editing a repository class does not feel like an "EF Core task". | Technique, depth | Must not carry policy |

### 6.2 V2: expected loading by task type

| Task | Always | Path rules (expected) | Skills (expected) | Gaps and excess |
|---|---|---|---|---|
| T1 Greenfield app from the spec | `CLAUDE.md`, descriptions | None until backend files exist and are touched. Whether writing a new file triggers a rule is untested. | `project-structure` is likely; its references follow when it says so | **`architecture.md` is absent during planning.** Only the duplicates cover the gap (core defaults in `CLAUDE.md`, the `project-structure` list). Seeding depends on the three-step chain. `dotnet new` and `dotnet add package` run from the CLI without touching manifest files, so **`dependencies.md` may never load**. |
| T2 Backend feature in existing code | same | architecture, coding-style, error-handling, performance, security (~5.3k tokens) on the first backend `.cs` read | http-api, ef-core, error-handling, testing: at the model's discretion. verify and code-review via the `CLAUDE.md` pointer. | Not guaranteed: HTTP status semantics, seeding obligations, naming by type role. Excess: persistence sections while editing controllers; caching and optimization lists everywhere. |
| T3 Domain entity change plus migration | same | the same 5 rules | ef-core only if invoked | **The seed obligation lives only in skills.** A stale `DbSeeder` is likely unless verify or code-review runs and is followed (hence the 6 copies). |
| T4 Frontend-only feature | same | `security.md` (mostly backend content) | angular (model-invoked) | **All Angular policy depends on a model-invoked skill.** Excess: backend security content. |
| T5 Writing tests | same | The 5 backend rules plus testing (~6.2k tokens), because test `.cs` files also match `backend/**/*.cs` | testing is likely | Excess: persistence and performance content for simple tests |
| T6 Build broken after an upgrade | same | `dependencies.md` once the manifests are read (likely) | build-fix is likely | OK |
| T7 Add a package from the CLI | same | None (no manifest is read) | — | The version and license procedure depends on Claude following the `CLAUDE.md` pointer and reading the rule by hand. |
| T8 Design question, no files touched | same | None | Possibly none | **Architecture policy is absent.** Claude may recommend MediatR or Redis from general knowledge. |
| T9 Code review | same | Rules for whatever files the reviewer reads | The code-review skill **or** the code-reviewer agent (they compete) | The criteria disagree (C1) |
| T10 Change a tunable value | same | None (`CUSTOM_SETTINGS.md` is not path-scoped) | custom-settings, via the `CLAUDE.md` pointer | OK when Claude starts the change; weaker when the user edited the file |
| T11 Docker or CI | same | `security.md` | docker, ci-cd (explicit task) | OK |
| T12 Security audit | same | As files are read | security-scan (explicit) | OK |

### 6.3 V2 failure situations

**A required instruction may fail to load:**

- Architecture policy during planning and greenfield work (T1, T8).
- The dependency procedure when packages are added from the CLI (T7).
- The seed co-change obligation (T3).
- The obligation to turn manual probes into tests. It sits in `rules/testing.md`, which loads when test files are touched. But the obligation arises when Claude runs a manual `curl` against production code, which is the wrong trigger.
- Angular policy (T4).
- HTTP status semantics: the always-loaded rule hands them to a skill (`rules/error-handling.md:65`).
- Naming by type role (`backend-layout.md:88-119`) during feature work.

**Too much unrelated context may load:**

- `rules/security.md` matches almost any file (`**/*.json` includes lockfiles and `tsconfig`), and most of its content is backend-only.
- Reading any backend `.cs` file loads 5 rules at once (~5.3k tokens), including repository and UoW detail while Claude edits a Domain enum.
- The 26 skill descriptions are always listed, and several are stuffed with keywords (`configuration` 475 characters, `dependency-injection` 463, `serilog` 514, `security-scan` 537).

**Several artifacts compete for one responsibility:**

- The `code-review` skill and the `code-reviewer` agent.
- `logging` and `serilog` (both claim "structured logging").
- `configuration` and `dependency-injection` (Options registration).
- `httpclient-factory` and `resilience`.
- Rules and skills with the same name (testing, error-handling).
- `coding-style` and `modern-csharp`.
- `security.md`, `security-scan` and `authentication`.

**A skill may be hard to trigger:**

- `swagger` has no "use when" clause.
- `ef-core`, `http-api` and `testing` during routine edits, where Claude may not see a task as being "about EF Core".
- `custom-settings`, when the change starts from an edit to the spec.
- The description listing budget with 26 skills (size not verified).

### 6.4 V3: choosing a mechanism

For each piece of content, ask these questions in order:

1. **Is it a project choice or an approval boundary?** → **Register** (always loaded).
2. **Is it agent behavior whose obligation is not triggered by a file path?** (spec governance, decision escalation, completion contract, scope, Git) → **`CLAUDE.md`** (always loaded).
3. **Is it normative for work on certain files?** → **Path-scoped rule** in the matching scope, with a *Related skills* footer pointing to the relevant knowledge skills.
4. **Is it a multi-step procedure?** → **Workflow skill**.
   - If the moment it is needed can be detected by a machine (a file changed, a command ran, the session is ending), add a **hook** that names the workflow.
   - If it must work in greenfield projects or inside a subagent, give the workflow explicit "read rule X" steps.
5. **Is it technique or depth?** → **Knowledge skill**, plus references.
6. **Is it mechanically checkable?** → **Enforcement**. Keep it in the prompt only if knowing it improves generation (§10).
7. **Is it for humans** (map, history, rationale)? → **MANIFEST or ADRs** (not loaded).

### 6.5 V3: expected loading by task type

| Task | Always (~4.6k tokens) | Path | Hook or explicit step | Skills (quality only, not critical) |
|---|---|---|---|---|
| T1 Greenfield | `CLAUDE.md` + register | None until files exist | `scaffold` explicitly reads `backend/architecture.md` and `persistence.md` before generating code, and copies the assets | scaffold, ef-core |
| T2 Backend feature | same | architecture, csharp, error-handling, both security rules; plus persistence (Domain, Application, Infrastructure) or api (Api) | verify and code-review, via the completion contract | http-api, ef-core, dotnet-testing |
| T3 Domain change | same | `persistence.md` (owns the seed co-change rule) | H4 at Stop: "Domain or migrations changed, DbSeeder untouched" | ef-core |
| T4 Frontend feature | same | `frontend/angular.md` + common security | — | angular |
| T7 Package from the CLI | same | — | H1 on `dotnet add package` or `npm install` → add-dependency | add-dependency |
| T8 Design question | same (register present) | — | architecture-decision, if a Reserved change is proposed | — |
| T9 Review | same | Inside the subagent, as files are read | The agent preloads code-review | — |
| T10 Settings change | same | — | H3 on an edit to `CUSTOM_SETTINGS.md` → change-settings | change-settings |

**Rough context comparison** (estimates, to be measured):

| Situation | V2 | V3 | Note |
|---|---|---|---|
| Always loaded | ~3.7k tokens (`CLAUDE.md` 1.2k + descriptions 2.4k) | ~4.6k (`CLAUDE.md` ~1.4k + register ~1.6k + shorter descriptions ~1.5k) | Slightly more |
| Editing an Application-layer file | ~5.3k path tokens | ~5k | More relevant content: seeding and naming rules now load; duplicates are gone |
| Editing an Angular file | 1.1k, mostly irrelevant backend security | ~1.2k of relevant frontend policy | Now relevant |

Net: slightly more always-loaded context, in exchange for closing the planning-time gap. Non-goal 5.5 allows this trade.

### 6.6 Making triggering testable

Build a **trigger test suite** in Phase 0 and run it against both V2 and V3.

- **Fixtures.** One repo per scenario: a greenfield copy of the template, or a small seeded solution that follows the layout.
- **Headless runs** (`claude -p`) with scripted prompts, for example:
  - "Add a Priority property to TaskItem"
  - "What caching approach should we use?"
  - "Install Mapster"
  - "Change max title length to 120"
- **Assertions.** From the session transcripts (JSONL): which rule and skill files loaded, and which hooks fired. From the repository state: `DbSeeder` updated, a test added, no MediatR package.
- **Settle the open mechanics first** (the "Needs test" items in §0.3):
  - Does a path rule trigger on Read, Edit, or a Write that creates a new file?
  - Do path rules load inside subagents?
  - How large is the description listing budget?
  - Does `skills:` preload in agents work?
  - How does nested `.claude` discovery behave?
- **Repeat** each scenario several times, because runs are non-deterministic, and record the Claude Code version with the results.

---

## 7. Skills, rules and references: who is responsible for what

### 7.1 Definitions

- **Rule:** *what must be true* of work in a scope. Short, normative, loaded by path, reliable.
- **Workflow skill:** *how to carry out a procedure*: steps, checks, outputs, stop conditions. Invoked explicitly, by the user, by a `CLAUDE.md` pointer, or by a hook reminder.
- **Knowledge skill:** *how to do something well* within the adopted decisions: technique, examples, trade-offs. Invoked by the model. It improves quality; it never carries policy.
- **Reference:** depth owned by one skill, loaded when that skill says so.
- **Agent:** an execution context (isolation, tool limits, preloaded skills), not a container for knowledge.

### 7.2 What should skills represent?

| Candidate role | Verdict | Reason |
|---|---|---|
| Workflows | **Yes** (workflow skills) | Procedures are what skills do best: they load when needed, with steps and references. |
| Capabilities and technique | **Yes** (knowledge skills) | Technique is too large to load by path and too valuable to drop. Pushing it all into rules, just so skills "only orchestrate", would bloat path-loaded context. |
| Policy | **No** | Model-invoked loading is not reliable enough for must-rules (P3). |
| Orchestration | **Yes, inside workflows** | For example, verify orchestrates checks and code-review delegates to the agent. A skill that only loads policies is unnecessary once policies load by path. |
| References | **Yes, as files owned by one skill** | A reference belongs to a skill. A reference that other artifacts depend on is in the wrong place. |

So skills should come in **two kinds, workflows and knowledge, and neither kind originates policy**. This modifies hypothesis 4.3 (§13, H-4).

### 7.3 Where V2 mixes responsibilities, and what V3 does with each skill

| V2 skill | Contains | V3 |
|---|---|---|
| `ef-core` | Architecture policy, technique, data-lifecycle policy, co-change rules | Policy → `persistence.md`. Technique stays. Seeder code → `references/dev-seeding.md`. |
| `error-handling` | Policy (principles, validation boundaries, outcome naming, stance on Result) and technique | Policy → `rules/backend/error-handling.md` and register D-08/D-09. Technique → `aspnet-error-handling`. |
| `testing` | Policy (NUnit, probes, stance on InMemory) and technique | Policy → `rules/backend/testing.md`, register D-15 and the `CLAUDE.md` completion contract. Technique → `dotnet-testing`. |
| `angular` | Policy (principles, anti-patterns) and technique | Policy → `rules/frontend/angular.md`. Technique stays. |
| `http-api` | A normative table of defaults and an edge-case reference | Table → `api.md`. Edge cases stay. |
| `project-structure` | Procedure, decisions (stack, layout), everyday naming policy | Procedure → `scaffold`. Decisions → register. Naming → `architecture.md`. |
| `verify`, `code-review`, `build-fix` | Procedure and restated policy | Procedure stays. Restatements become check-by-reference items. |
| `custom-settings` | Procedure and restated policy | Procedure → `change-settings`. Policy → `CLAUDE.md`. |
| `git-workflow` | Conventions and restated safety rules | Conventions stay. Safety → `CLAUDE.md` and permissions. |
| `serilog` | Provider technique, plus suggestions that conflict with a minimal stack | → `logging/references/serilog.md`. Reword the C5 rows as conditional options. |
| `httpclient-factory` + `resilience` | Overlapping technique | → `outbound-http` with `references/resilience.md`. Database resilience → ef-core. Inbound rate limiting → http-api. |
| `configuration`, `dependency-injection` | Technique; the D20 overlap | Keep both. Only configuration owns the Options section. |
| `modern-csharp` | Overlaps coding-style | Keep the C# 14 reference and the modernization procedure. Policy → `csharp.md`. |
| `security-scan` (and its reference), `docker`, `ci-cd`, `health-check`, `caching`, `swagger`, `api-versioning`, `authentication`, `logging` | Mostly technique | Keep. Replace restated policy with pointers. Add a "use when" clause to swagger. |

### 7.4 V3 skill catalog

| Skill | Kind | Invocation | Notes |
|---|---|---|---|
| scaffold | Workflow | Model and user | Reads the architecture and persistence rules explicitly; copies the assets |
| verify | Workflow | Model (completion contract) | Checklist of check-by-reference items; runs the check scripts |
| code-review | Workflow | Model or user; normally through the agent | The single owner of review criteria |
| build-fix | Workflow | Model | Bounded repair loop |
| add-dependency | Workflow | Model (workflow map and hook H1) | Version, license, commercial options |
| change-settings | Workflow | Model (workflow map and hook H3) | Sync procedure |
| architecture-decision | Workflow | Model (Decision control) | Decision Request, ADR, register update, updates to dependent rules |
| security-scan | Workflow | User, or model with a narrow description; `context: fork` if supported | Keeps its 711-line reference out of the main context |
| git-workflow | Workflow | Model or user | Conventions only |
| template-maintenance | Workflow | User only (`disable-model-invocation`) | Optional; costs no model context |
| ef-core, http-api, aspnet-error-handling, dotnet-testing, authentication, logging, configuration, dependency-injection, outbound-http, caching, swagger, api-versioning, health-check, docker, ci-cd, angular, modern-csharp | Knowledge | Model; linked from the rules' "Related skills" footers | Descriptions of about 250 characters or less |

### 7.5 Rules for writing skills

- **Description.** Put the trigger first ("Use when…"). Give concrete cues: file names such as `*Repository.cs`, `DbContext` or `Migrations/`, and commands. Keep it to about 250 characters. No keyword lists.
- **Body.** About 200 lines at most. Put depth in `references/`, with "read reference X when…" guidance (as V2's `project-structure` already does).
- **No new policy.** A skill must not contain a must-rule unless `CLAUDE.md`, the register or a rule owns it. The check script flags imperative lines ("must", "never", "do not") in knowledge skills for human review. This is a heuristic, not a hard failure.
- **Coupling to policy.** Cite register IDs and rule paths instead of restating them.
- **Workflows.** Declare inputs, steps, stop conditions and output format. Add explicit rule-read steps wherever path loading can't be relied on.
- **Names.** A skill never shares a name with a rule.

### 7.6 Subagents

- **`code-reviewer`.** Its frontmatter restricts it to read-only tools and preloads `code-review`. Verify that `skills:` is supported; if it is not, the agent's first step is "invoke the code-review skill". The body contains only the role, how to determine scope, and the instruction to return findings in the skill's format. This removes D23 and C1.
- **Later, if benchmarks show value:** a read-only `architecture-auditor` that checks large diffs against the decision register. Not proposed now, to avoid speculative agents.

---

## 8. Backend, frontend and common scopes

### 8.1 Scopes

| Scope | Paths (proposed; to validate) | Rules | Skills |
|---|---|---|---|
| common | Code, config, container and CI files (manifests only, for dependencies) | `common/security.md`, `common/dependencies.md` | verify, code-review, build-fix, add-dependency, git-workflow |
| backend | `backend/**/*.cs`, `backend/**/*.csproj` | architecture, csharp, error-handling, security | .NET knowledge skills |
| backend, per layer | persistence: `backend/*.Domain/**`, `backend/*.Application/**`, `backend/*.Infrastructure/**`, `backend/*.Api/Program.cs`. api: `backend/*.Api/**/*.cs` | persistence, api | ef-core, http-api, aspnet-error-handling |
| backend-tests | `backend/**/*Tests/**` | testing | dotnet-testing |
| frontend | `frontend/**/*.ts`, `frontend/**/*.html`, `frontend/**/angular.json` | `frontend/angular.md` (includes frontend test policy) | angular |
| delivery | `**/Dockerfile*`, `**/*.yml`, `**/*.yaml` | `common/security.md` applies | docker, ci-cd, health-check |
| repo/meta | `.claude/**`, `CLAUDE.md`, the register | — | template-maintenance |

### 8.2 How content is placed

- **Common is small and truly shared.** It covers secrets, sensitive data, error exposure, TLS validation, dependency hygiene, Git, the completion contract and the workflows. The test for "common": would the statement be correct and useful both when editing an Angular component and when editing a C# repository?
- **Backend is primary.** It gets finer rules that know about layers (persistence, api), because the template's value and risk are concentrated there.
- **Frontend gets one rule.** It carries the normative core that V2 left in a model-invoked skill:
  - standalone components;
  - feature-based structure;
  - HTTP only in data-access services;
  - no backend Domain types;
  - when to escalate to a state-management library;
  - route guards are UX only;
  - test placement and runner (from D-16).

  Technique stays in the `angular` skill. There is no React content.
- **Cross-stack contract.** `api.md` states that the backend HTTP contract (Controllers plus Swagger/OpenAPI) is authoritative: the frontend adapts, and generated clients are regenerated, not patched. This resolves C7 and is recorded as D-07 in the draft register.

### 8.3 Testing scope

- **Backend test policy** → `rules/backend/testing.md` (paths: test projects).
- **Frontend test policy** → a section of `rules/frontend/angular.md`.
- **Completion obligations** (tests for manually verified behavior, regression tests for bugs) → the `CLAUDE.md` completion contract. They are triggered by *verifying behavior*, not by file paths.
- **Test technique** → the `dotnet-testing` and `angular` skills.

### 8.4 Delivery scope

Docker, CI and health checks are skills triggered by explicit tasks. Their shared policies are owned elsewhere and only referenced:

- The production-migration and seeding policy: D-05, `persistence.md`.
- Secrets: `common/security.md`.

This removes D17.

### 8.5 Risks with globs

- **The per-layer globs depend on the `<Name>.<Layer>` project naming convention.** That is acceptable, because the scaffold workflow enforces the convention and the register records it (D-19). For an existing project adopting the template, the MANIFEST documents which globs to adjust.
- **Brace expansion in `paths` is unverified.** List patterns separately.

---

## 9. Architectural decision control

### 9.1 Three classes of decision

| Class | Definition | What Claude does | Examples |
|---|---|---|---|
| **Decided** | Already settled by the register, a rule, `SPECIFICATION.md` or `CUSTOM_SETTINGS.md` | Follows it. Does not ask and does not reopen it. | Controllers; specific repositories; FluentValidation; NUnit; Swagger in Development |
| **Delegated** | Local, reversible choices *inside* the decided architecture that change no contract, boundary, dependency or observable behavior | Decides on its own, and mentions notable choices in the final summary | See the list below |
| **Reserved** | A change to anything Decided, or anything that matches a reserved class | Stops the affected part, produces a Decision Request, and implements only after approval | R-1 to R-10 below |

Examples of Delegated decisions:

- how to split classes and methods;
- internal naming, within the naming rules;
- query shape, projection and tracking;
- test level and test data;
- outcome records specific to one use case;
- indexes for query performance;
- log statements;
- Options classes;
- adding an *approved conditional* dependency once its condition holds (through add-dependency).

**Reserved classes.** These consolidate the V2 gate (`rules/architecture.md:152-178`), requirement 2.9, and the disagreeing lists.

| Class | Covers |
|---|---|
| R-1 | Changing any register entry |
| R-2 | A new architectural pattern or style: DDD tactical patterns, CQRS, mediators, Vertical Slice Architecture, event sourcing, microservices, modular restructuring |
| R-3 | A new production project, layer or assembly, or a change to the project reference graph |
| R-4 | Persistence boundaries or technology: another DbContext, another database, Dapper or raw SQL as a general pattern, changes to repository or UoW policy |
| R-5 | New infrastructure: messaging, background processing, distributed cache, search, external storage, external identity provider |
| R-6 | A new major library or framework, replacing a baseline technology, or any dependency with a commercial, copyleft or unclear license |
| R-7 | Conventions other code must follow: a shared Result type, an exception hierarchy, universal base classes, global filters or interceptors that change behavior |
| R-8 | Authentication or authorization architecture |
| R-9 | Breaking changes to a public API contract; adopting API versioning |
| R-10 | Product behavior or tunable values not defined by the product sources. Owned by `CLAUDE.md` §Product governance; the same protocol applies. |

### 9.2 Classification test for unclear cases

Answer five questions. **Any "yes" makes it Reserved; all "no" makes it Delegated.**

1. Does it add, remove or replace a dependency, framework or piece of infrastructure?
2. Does it change a project or layer boundary, a reference, or an assembly?
3. Does it set a convention that other code is expected to follow?
4. Does it change observable product behavior or a public contract?
5. Would it be costly to reverse later, once other code builds on it?

This resolves V2's ambiguities:

| Case | Class | Why |
|---|---|---|
| A `CreateOrderOutcome` record specific to one use case | Delegated | All five answers are "no" |
| A shared `Result<T>` type (C2) | Reserved | Question 3 |
| One Minimal API endpoint (C3) | Reserved | Question 3: it sets up a second HTTP style |
| A custom exception hierarchy (C4) | Reserved | Question 3 |
| A generic repository base inside Infrastructure (C6) | Delegated | The persistence rule already allows it |
| Adding Seq (C5) | Reserved | Question 1 |

### 9.3 Draft decision register (derived from V2; no new policy)

| ID | Area | Decision | Details in | Affects |
|---|---|---|---|---|
| D-01 | Style | Clean Architecture with four projects: Domain, Application, Infrastructure, Api. Dependencies point inward. | architecture.md | architecture.md, architecture tests |
| D-02 | Domain model | Simple entities; use-case and workflow rules live in Application Services. Not adopted: Rich Domain Model, aggregates, domain events, specifications, domain services, systematic value objects. | architecture.md §Domain | architecture.md, scaffold |
| D-03 | Orchestration | Application Services. Not adopted: CQRS, MediatR or other mediators, Vertical Slice Architecture. | architecture.md §Application | architecture.md |
| D-04 | Persistence | EF Core with SQL Server; a single DbContext; specific repository interfaces in Application; `IUnitOfWork` as the commit boundary; a generic repository only as an Infrastructure-internal base class. | persistence.md | persistence.md, ef-core |
| D-05 | Data lifecycle | Migrations are source code and are never applied automatically in Production. Seeding runs in Development only, through `DbSeeder`, when the database is empty. | persistence.md §Seeding | persistence.md, docker, ci-cd |
| D-06 | HTTP | ASP.NET Core Controllers. Not adopted: Minimal APIs. | api.md | api.md |
| D-07 | Contract authority | The backend HTTP contract is authoritative. Generated clients are regenerated, not patched. | api.md | angular.md, build-fix |
| D-08 | Errors | ProblemDetails / ValidationProblemDetails; a central `IExceptionHandler`; expected outcomes expressed as null, bool, or types specific to one use case. Not adopted: a project-wide Result model, a business-exception hierarchy. | error-handling.md | error-handling.md |
| D-09 | Validation | FluentValidation (with its DI extensions). No deprecated auto-validation packages. | error-handling.md | — |
| D-10 | Logging | `ILogger<T>` in code; Serilog (Serilog.AspNetCore) as the provider; a Console sink as the baseline; other sinks only on requirement. | logging skill | logging |
| D-11 | Mapping | Manual mapping; Mapster (with its DI package) once mapping becomes repetitive [conditional]. No other mapper. | — | — |
| D-12 | Outbound HTTP | `IHttpClientFactory`; Microsoft.Extensions.Http.Resilience or Microsoft.Extensions.Resilience when needed [conditional]. Not adopted: deprecated Polly integrations, direct Polly. | outbound-http skill | — |
| D-13 | API docs | Swashbuckle Swagger UI, in Development only by default. `AddOpenApi`/`MapOpenApi` is not the default. | swagger skill | api.md |
| D-14 | Configuration | Options pattern with validation at startup; user-secrets locally; the platform's secret injection when deployed. | configuration skill | common/security.md |
| D-15 | Backend tests | NUnit; `WebApplicationFactory<Program>`; the real database provider when fidelity matters; Testcontainers [conditional]; no EF InMemory for relational behavior. | testing.md | testing.md |
| D-16 | Frontend | Latest stable Angular: standalone, strict, routing, zoneless when supported, SCSS, RxJS and Signals, Material/CDK; Vitest; Playwright for E2E [conditional]. Not adopted by default: NgRx, Axios, Lodash, Bootstrap, Tailwind, extra form, component or state libraries. | angular.md | angular.md |
| D-17 | Platform | .NET 10 LTS, C# 14; stable releases only. | — | scaffold |
| D-18 | Packages | NuGet Central Package Management; npm with a committed lockfile. | dependencies.md | assets |
| D-19 | Repository layout | `backend/` (production and test projects), `frontend/<Name>.Web`, `docs/`; `.slnx`; no top-level `tests/`; a Domain.Tests project only for non-trivial domain behavior. | scaffold references | path globs |
| D-20 | Caching | Not adopted by default. In-process caching or HybridCache is Delegated when the caching skill's criteria are met. A distributed cache is Reserved (R-5). | caching skill | — |
| D-21 | API versioning | Not adopted. Adopting it is Reserved (R-9). | api-versioning skill | — |
| D-22 | Containers / CI | Not adopted by default. Added when a task requires it. | docker, ci-cd | — |
| D-23 | Authentication / authorization | None by default. Choosing a scheme is Reserved (R-8). | authentication skill | — |

The **Affects** column is what keeps this maintainable: when a decision changes, the ADR workflow updates exactly those files.

### 9.4 Escalation protocol

When a task needs a decision that policy does not settle, or a Reserved decision:

1. **Detect it early.** Ideally during planning, since the register is always loaded; otherwise as soon as the need appears during implementation.
2. **Never resolve it silently**, not even "temporarily".
3. **Separate the work.** Continue the parts of the task that don't depend on the decision; stop the parts that do.
4. **Request a decision** in this format:

   ```text
   DECISION REQUIRED — <title>   (R-<n>)
   Context:   what the task needs; which register entry or rule doesn't cover it
   Options:   A. <option that complies with current policy> — consequences   (always include one)
              B. <alternative> — consequences, reversibility, new dependencies
   Recommendation: <option> — why
   Blocked:   <what>   Proceeding with: <what>
   ```

5. **After approval, record it** with `architecture-decision`:
   - an ADR in `docs/architecture/decisions/NNNN-<slug>.md`;
   - the register entry added or updated;
   - the files in its "Affects" column updated;
   - the check script run.
6. **If the request is rejected**, implement option A.
7. **If no option that complies with policy is feasible**, stop and report. Do not improvise.

### 9.5 An explicit user instruction counts as approval

"Use Redis for this cache" approves a Reserved decision (R-5). Claude proceeds, says that this sets a project-level decision, and records it with an ADR and a register entry. If the instruction looks like a one-off experiment, Claude asks whether to record it. This keeps Claude autonomous without letting decisions pile up unseen.

### 9.6 Headless and autonomous runs

When no human can answer (for example `claude -p` benchmarks or CI agents), Claude:

- chooses option A, the one that complies with policy;
- completes whatever can be completed;
- puts every Decision Request at the top of the final report.

This keeps autonomous runs safe, and it makes "unrequested architectural decisions" (one of the evaluation metrics) directly visible.

### 9.7 Feature specs and decisions

A feature spec may define behavior, and may *state a need* ("imports must be processed asynchronously"). If meeting that need requires a Reserved decision (background processing is R-5), the spec does not grant approval; the protocol applies. Once approved, the decision lives in the register, not in the feature spec.

### 9.8 Review as a backstop

`code-review` includes this check: "Any change that matches a Reserved class, without a register or ADR entry and without explicit approval in the task, is a High finding." It catches decisions that slipped through during implementation.

---

## 10. Policy versus deterministic enforcement

### 10.1 Classes of rules

| Class | Nature | Treatment |
|---|---|---|
| A. Judgment | Proportionality, invented product behavior, how rich the domain model is, choice of status code, retry safety | LLM only; review as a backstop |
| B. Critical for generation and checkable | Layer boundaries, forbidden packages, cancellation forwarding, sync-over-async | Keep a concise statement in the prompt, **and** enforce it |
| C. Mechanical and cheap to fix afterwards | Formatting, unused usings, naming style, file-scoped namespaces | Tooling only, plus one line in verify |
| D. Co-change and process obligations | Seed sync, settings sync, probe-to-test, dependency procedure | A hook detects the moment and names the workflow; the LLM decides what to change |
| E. Safety and irreversible actions | Destructive Git operations, force push | Permissions (`ask`) plus one line |

### 10.2 V2 rules mapped to mechanisms

| Policy (V2 source) | Mechanism | In the prompt after V3 |
|---|---|---|
| Project reference direction (`architecture.md:9-19`) | Project references (compile errors); an architecture test on referenced assemblies; the H2 check on `.csproj` edits | Keep, short (B) |
| No EF Core or ASP.NET Core in Domain or Application (`architecture.md:28-29,52`) | Missing package → compile error; architecture test | Keep, short (B) |
| Controllers don't take `DbContext` or concrete repositories (`architecture.md:68-73`) | Architecture test: reflect over controller constructor parameter types | Keep (B) |
| Repository interfaces don't expose `IQueryable` or `DbSet` (`architecture.md:90`) | Architecture test: reflect over the return types of Application interfaces | Keep (B) |
| `IUnitOfWork` is not a repository container (`architecture.md:136-137`) | Architecture test: no members typed as repositories | Keep (B) |
| Forbidden packages: MediatR, deprecated Polly integrations, EF InMemory in tests, non-adopted mappers | Deny-list check (H2, verify and CI) against a machine-readable list derived from the register | Register only (B) |
| Central Package Management (`dependencies.md:115-149`) | `ManagePackageVersionsCentrally=true`, which makes versioned references fail with NU1008 | One line (C) |
| No floating or prerelease versions (`dependencies.md:29-48`) | Check script | One line (C) |
| Unused usings (`coding-style.md:103-114`) | IDE0005 with `EnforceCodeStyleInBuild` (plus `GenerateDocumentationFile`, so IDE0005 runs during the build); `dotnet format --verify-no-changes` | One line in verify (C) |
| File-scoped namespaces, `var`, naming, async suffix (`coding-style.md:20,78-101`) | `.editorconfig` rules (IDE0161, IDE0007/0008, naming rules including the async suffix) | "Follow .editorconfig" (C) |
| CancellationToken forwarding (`performance.md:19`) | CA2016 | Keep, short (B) |
| Structured log templates (`logging:22-38`) | CA2254, CA2017 | Keep one line (B) |
| Sync-over-async (`performance.md:18`) | Optional BannedApiAnalyzers (a new dependency, see Q7), or a grep in the check script | Keep (B) |
| `DateTime.Now` in time-dependent logic (`performance.md:22-28`) | Optional BannedApiAnalyzers | Keep (A/B) |
| A new `HttpClient()` per request (`performance.md:32`) | Optionally ban the parameterless constructor | Keep (B) |
| SQL built from input (`security.md:58-65`) | CA2100; EF Core's analyzer for interpolated raw SQL | Keep (B) |
| Committed secrets (`security.md:23-36`) | Scan written files for secret patterns in H2/H4; an optional secret scanner in CI | Keep (B) |
| Automatic production migration (`ef-core:581`) | Check script: `Database.Migrate(` or `EnsureCreated(` outside a Development guard | Keep (B) |
| Swagger in Development only (`swagger:20-21`) | Integration test: `/swagger` is not served in the Production environment | Keep (B) |
| Unhandled errors leak no details (`security.md:141-146`) | Integration test that forces a 500 | Keep (B) |
| Destructive Git operations (`CLAUDE.md:118-120`) | Permissions set to `ask` | One line (E) |
| Seed co-change (`ef-core:512-552`) | The persistence rule, plus detection by H4 | Keep (D) |
| Settings sync (`CLAUDE.md:78`) | H3 trigger | Keep the workflow (D) |
| Dependency procedure (`dependencies.md:21-113`) | H1 trigger | Keep the workflow (D) |
| Probe to test (D2) | The completion contract; an optional, experimental H4 heuristic: a localhost `curl` or `Invoke-WebRequest` ran during the session and no test files changed | Keep (D) |
| No top-level `tests/` directory (D16) | Check script | Register only (C) |
| Spec conformance, domain proportionality, status semantics, retry safety | — | LLM (A) |

### 10.3 Ship enforcement as files, not prose

Enforcement lives in the *generated* project, and Claude is the one who creates that project. Prose that asks Claude to write the enforcement brings back the same reliability problem. V3 should ship enforcement as **literal files**:

- **At the template root from day one:** `.editorconfig`; `Directory.Build.props` (Nullable, `AnalysisLevel`, `EnforceCodeStyleInBuild`); `Directory.Packages.props` (CPM on); `.claude/settings.json`; the hook scripts; the check script.
- **Copied by `scaffold` from `assets/`**, with placeholders filled in: an architecture test file, and optionally integration-test skeletons for "Swagger in Development only" and "no error details leak".

### 10.4 Proposed hooks and scripts

| ID | Event / matcher | Detects | Action | Class |
|---|---|---|---|---|
| H1 | PreToolUse on Bash | `dotnet add … package`, `dotnet remove … package`, `npm install\|i\|add\|uninstall`, `ng add`, `ng update` | Ask or inform: "Dependency change: follow add-dependency (version, license, register)" | D |
| H2 | PostToolUse on Edit/Write of `*.csproj`, `Directory.Packages.props`, `package.json` | CPM violations, prerelease or floating versions, deny-listed packages, forbidden `ProjectReference` edges | Report violations back to Claude (not blocking at first) | B/C |
| H3 | PostToolUse on Edit/Write of `CUSTOM_SETTINGS.md` or `SPECIFICATION.md` | A product source changed | Remind Claude to run change-settings, or to check the spec and settings agree | D |
| H4 | Stop | From `git diff --name-only`: Domain entities or `Migrations/` changed without `Seeding/`; C# changed without any test change (a weak signal); forbidden patterns in new files | Remind once, with a guard against loops; never runs builds | D |
| S1 | Script `check-architecture` (verify, CI) | Deny-list, CPM, prerelease versions, project references, no `tests/`, the production-migration guard | Pass/fail report | B/C |
| S2 | Script `check-instructions` (template-maintenance, CI) | Every rule has `paths`; every `.claude` file is listed in the MANIFEST; description length; broken file or ID references; unclosed code fences; imperative lines in knowledge skills (warning only) | Pass/fail report | meta |

Design constraints for hooks:

- They must be fast (under a second) and use narrow matchers.
- They inform before they block. Start non-blocking; make a hook blocking only after benchmarks show few false positives.
- They must be cross-platform. The template's current user works on Windows (Q4).
- Their messages always name the owning file or workflow and never restate policy.

### 10.5 Permissions

In `.claude/settings.json`, set `ask` for:

- `git commit`, `git push`, `git merge`, `git rebase`;
- `git reset --hard`, `git clean`;
- `git branch -D`, `git stash drop`, `git worktree remove`.

`ask` keeps V2's "only when explicitly requested" meaning: the user confirms, and the instruction in `CLAUDE.md` shrinks to one line. `deny` is kept for things that are never wanted (Q5).

### 10.6 Architecture tests with no new dependency

These use only reflection and NUnit, which is already approved:

- **Assemblies.**
  - `typeof(DomainMarker).Assembly.GetReferencedAssemblies()` contains no Application, Infrastructure, Api, EF Core or ASP.NET Core assemblies.
  - Application's referenced assemblies contain no Infrastructure, EF Core or ASP.NET Core assemblies.
- **Types.**
  - Controller constructor parameters are not `DbContext` or Infrastructure types.
  - Application interfaces don't return `IQueryable<>` or `DbSet<>`.
  - `IUnitOfWork` has no members typed as repositories.

This covers most D4 checks without adding NetArchTest or ArchUnitNET. Namespace-level rules can come later if needed (Q6).

### 10.7 What must stay in the prompt

Everything in class A stays. So do concise statements of the class B rules: knowing the layer boundaries while generating code avoids wasted build-and-fix cycles. The prompt's caveat applies here: having architecture tests is not a reason to take architecture rules out of context.

---

## 11. Proposed migration plan

### 11.1 Principles

- **Inventory first.** Every normative statement in V2 gets an ID and a V3 destination: an owner, or an explicit removal with a reason. This is the proof for invariant 3.1.
- **One concern per step.** The benchmark after each phase must not regress.
- **Mechanisms before content.** Build the register, the choice of mechanism and the checks first; then move content.
- **Nothing is deleted until its owner exists** and the trigger test for that owner passes.

### 11.2 Phases

| Phase | Scope | Exit criteria |
|---|---|---|
| 0. Baseline (research repo only) | V2 policy inventory (`research/observations/002-…`); trigger test suite; V2 benchmark baseline; settle the "Needs test" mechanics (§0.3) | Inventory complete; mechanics answered; baseline numbers recorded |
| 1. Skeleton | New `CLAUDE.md` (precedence, decision control, product governance, completion contract, workflow map); decision register; MANIFEST; the S2 check script. The rest of the V2 content stays as it is. | Trigger tests show the register is present in T1 and T8 |
| 2. Rules | Create the scoped rules and move policy out of skills (persistence, api, error-handling, testing, angular, the security split, csharp) | Every inventory item is mapped; no restatements (S2 heuristics plus review) |
| 3. Skills | Separate policy from technique; merges (logging, outbound-http); new workflows (add-dependency, architecture-decision); renames (scaffold, change-settings, aspnet-error-handling, dotnet-testing); the thin agent; check-by-reference checklists | Skill trigger tests pass; the description budget is met |
| 4. Enforcement | Permissions; H1–H4; S1; root assets; scaffold assets, including the architecture test | Hook tests on Windows and one POSIX environment; review of false positives |
| 5. Cleanup | Remove superseded duplicates; final MANIFEST; S2 passes | S2 passes; inventory reconciled |
| 6. Evaluation | Full V2 vs V3 benchmark: goal completion, interventions, violations, unrequested decisions, rework, tokens | Human review of the results |

### 11.3 What to move, consolidate, split, keep and remove

**Move**

| Content | From | To |
|---|---|---|
| Naming by type role; directory conventions | `backend-layout.md:88-133` | `rules/backend/architecture.md` §Code organization |
| Seeding policy, seed co-change, migration policy | `ef-core:343-587` | `rules/backend/persistence.md`. The seeder code goes to `ef-core/references/dev-seeding.md`. |
| Approved stack and conditional technologies | `technology-stack.md` | The decision register. Dev database and CLI specifics go to `scaffold/references/dev-environment.md`. |
| Dependency selection procedure | `dependencies.md:21-113` | `skills/add-dependency` |
| Controller rules | `architecture.md:58-75` | `rules/backend/api.md` |
| Default status-code table; 401 vs 403 | `http-api:487-511`; `authentication:152-172` | `rules/backend/api.md` |
| Repository, UoW and EF boundary | `architecture.md:77-150` | `rules/backend/persistence.md` |
| The decision gate and every pattern list | The D1 locations | The register (D-xx, R-x) |
| Async, cancellation, TimeProvider, HttpClient lifetime | `performance.md:15-37` | `rules/backend/csharp.md` |
| Outcome naming | `error-handling` skill, `:131-140` | `rules/backend/error-handling.md` |
| Probe to test | The D2 locations | The `CLAUDE.md` completion contract |
| Angular principles and anti-patterns | `angular:14-27,338-352` | `rules/frontend/angular.md` |

**Consolidate** (many copies into one owner). D1 to D24 from §3.1 each go to the owner listed in §5.2. The largest gains:

- D1: 7 copies → 1
- D2: 7 → 1
- D3: 6 → 1
- D4: 8 → 1
- D5: 2 → 1
- D23: 2 → 1

**Split**

| V2 file | V3 destinations |
|---|---|
| `CLAUDE.md` | Core `CLAUDE.md` + register |
| `architecture.md` | architecture / persistence / api / register |
| `ef-core` | Rule + skill + reference |
| `technology-stack.md` | Register + scaffold reference |
| `dependencies.md` | Rule + workflow |
| `security.md` | Common + backend (Angular parts to `angular.md`) |
| `performance.md` | `csharp.md` (DB → persistence/ef-core; caching → register/caching skill) |
| `angular` | Rule + skill |
| `http-api` | Rule table + skill |
| `error-handling` skill | Rule + skill |
| `testing` skill | Rule + skill |

**Keep largely unchanged**, once duplicates are replaced by pointers:

- security-scan and scan-layers, health-check, docker, ci-cd, api-versioning, caching;
- swagger (plus a "use when" clause), authentication, configuration, dependency-injection;
- build-fix's repair loop, verify's structure, git-workflow's conventions;
- `SPECIFICATION.md`.

**Remove or reword:**

- The inert `description` field in the `security.md` frontmatter.
- `serilog` and `resilience` as standalone skills (merged).
- Rows in the Serilog decision table that read as recommendations (C5); reword them as conditional options.
- The criteria sections of the `code-reviewer` agent.
- The restated policy in `CUSTOM_SETTINGS.md`.
- Every restatement listed in §3.1, once its owner exists.
- `testing.md`'s unclosed code fence (the content moves anyway).

**Needs behavioral testing after migration:**

1. **Greenfield from a sample spec.** No non-adopted patterns; `DbSeeder` created; test projects placed per D-19; Swagger in Development only; CPM active; the architecture test present and passing.
2. **Design question** ("should we add caching / CQRS?"). The answer cites the register; Reserved items are escalated.
3. **A tempting feature.** A complex workflow that invites a Rich Domain Model, `Result<T>` or MediatR produces an escalation or a compliant implementation, never silent adoption.
4. **A Domain property is added.** The migration and `DbSeeder` are updated in the same change.
5. **A `CUSTOM_SETTINGS.md` value changes.** Code, validation, frontend and tests are all synchronized.
6. **A package is added from the CLI.** The add-dependency procedure is followed (version, license).
7. **An endpoint is verified with curl.** A maintained integration test exists when the work is complete.
8. **An Angular feature.** The angular rule is loaded; HTTP calls stay in data-access services; no NgRx.
9. **Code review of a diff with a planted defect.** Findings follow the skill's format; no demands for non-adopted patterns; Reserved violations are flagged High.
10. **The spec says nothing about case sensitivity.** Claude asks, as in V2.
11. **A build fix that tempts an invalid project reference.** The architecture test or H2 catches it.
12. **The trigger suite** for every rule (Read vs Write), every hook, and the agent's skill preload.
13. **A token and cost comparison** for each scenario.

---

## 12. Risks and trade-offs

| Risk | Where it arises | Mitigation |
|---|---|---|
| Over-fragmentation | 10 rules, 26 skills, hooks, scripts | P7 split criteria; the MANIFEST; merges where triggers overlap; no micro-files |
| Larger always-loaded context | The register (~+1.6k tokens) | Keep the register under ~100 lines. Shorter skill descriptions save ~0.9k. Measure. |
| The register goes stale or drifts from the rules | A decision changes without the rules being updated | The "Affects" column; the architecture-decision workflow updates the listed files; S2 checks that referenced IDs exist |
| Path triggers don't behave as assumed | Rules may not load when a new file is written, or inside subagents | Phase 0 tests; explicit read steps in scaffold and in the agent; fall back to broader paths or imports for critical rules |
| Skills don't trigger reliably | Knowledge skills | By design they carry no policy (P3). "Related skills" footers make triggering more likely. The trigger suite measures it. |
| Too much indirection | Pointers and IDs | Point only to owners that load reliably. Check-by-reference keeps workflows able to run their checks on their own. |
| Too much file discovery | Explicit read steps | Limit them to greenfield work and agents; rules are short |
| Hidden dependencies | Hooks and scripts are invisible in prompts | The MANIFEST's enforcement table; hook messages name the owner |
| Brittle, slow or non-portable hooks | Windows/PowerShell vs bash; slow scripts; false positives; Stop-hook loops | Few hooks; narrow matchers; non-blocking first; loop guard; test on Windows and POSIX; choosing the runtime is Q4 |
| Harder for humans to navigate | Content split between `docs/` and `.claude/` | Two entry points: `CLAUDE.md` (always loaded) and the MANIFEST (everything else). `docs/` holds only project decisions. |
| Unnecessary complexity | Decision classes, IDs, ADRs | The register and ADRs are plain Markdown; ADRs are created only when a decision is made |
| Check-by-reference items drift | Verify and review checklists | One-line checks with no conditions; S2 checks that their targets exist |
| Claude asks too much (less autonomy) | Reserved classes drawn too broadly | An explicit Delegated list; the five-question test; V2's "don't ask for routine decisions" preserved; the benchmark measures interventions |
| Dependence on the model or Claude Code version | Loading behavior changes between versions | Pin the version in benchmarks; re-run the trigger suite on every upgrade |
| **Research validity: nested discovery** | Observed: Claude Code finds `templates/*/.claude/skills` from the research repo root, and V2 and V3 use the same skill names | Run benchmarks with a copy of the template as the project root (working directory), never from the research repo root |
| Benchmark overfitting | Scenario design | Keep some scenarios held out; use the failure taxonomy from requirements §6 |

**Trade-offs made deliberately:**

- About 0.9k more always-loaded tokens, in exchange for reliability during planning.
- One-line checks repeated in workflows, in exchange for reliability at completion.
- Three more rule files, in exchange for precise triggers.
- A small hook layer, with its runtime and maintenance cost, in exchange for deterministic co-change triggers.

---

## 13. Disagreements with the provided design hypotheses

| # | Requirement or hypothesis | Concern | How it could fail | Recommended alternative |
|---|---|---|---|---|
| H-1 | 4.1 / 2.2: the linear hierarchy `Core → Architecture → Technology → Project → Feature → Task` | It mixes abstraction level, who may change what, and how content loads. | Decisions get loaded by path (and are missing during planning), or details get loaded always (bloat). The directory tree mirrors a theory rather than the triggers. | Kinds × scopes (§4.3). Keep the stability order as a dependency rule (§4.4). |
| H-2 | "Technology" as a level between Architecture and Project | It merges technology *selection* (a decision) with technology *knowledge* (technique). | It recreates V2's problem of `technology-stack.md` living inside a skill, and projects can't change their stack cleanly. | Selection → register (K2); knowledge → skills (K4). |
| H-3 | "Feature" and "Task" as instruction layers | They are inputs, not instructions owned by the template. | Ceremony (mandatory feature files), and confusion over whether a feature file may change the architecture. | Treat them as product inputs (K7) with an explicit override protocol (§4.6, §9.7). Use optional `docs/features/` only for large specs. |
| H-4 | 4.3: skills as orchestration rather than policy | Right that skills shouldn't own policy; wrong if it means skills should only orchestrate. | All technique gets pushed into path rules (context bloat) or dropped (lower quality). | Two kinds of skill, workflows and knowledge; neither originates policy (§7.2). |
| H-5 | 3.2 / 2.5: no normative duplication, stated as absolute | Absolute deduplication ignores that the owner may not be loaded when a check runs. | Checks are silently skipped, and authors duplicate again (V2's history). | Define the allowed reference forms: pointer, check-by-reference, register summary (§5.1). |
| H-6 | 4.2: smaller modules | Size is the wrong axis to split on. | Fragmented rules that always load together: more discovery, same context. | Split by trigger, owner and rate of change (P7). Merge skills that trigger together (logging with serilog; HTTP clients with resilience). |
| H-7 | 4.5: manifest, if it were loaded or maintained by hand | Loading it costs context with no behavioral gain. Metadata maintained by hand drifts from the frontmatter. | A stale map misleads humans and wastes tokens. | A human-facing `.claude/MANIFEST.md` that is never loaded, checked against the files by S2. |
| H-8 | 4.6 / 2.12: encode effort, model and permission mode per task type | Model IDs and the meaning of effort levels are the most changeable part of the stack, and session settings are user preferences. | The template goes stale with each model release and overrides users' choices. | Encode only structural properties: read-only tools, forked context, plan-first steps in architecture-decision, bounded iteration in build-fix. Put recommended effort per task type in the MANIFEST, for humans. Use model aliases in agents only for a structural reason. |
| H-9 | 2.7: selective loading as a general aim | Right for technique; wrong for decisions. | Decisions are missing during planning, which is V2's biggest gap. | Load decisions up front and details on demand (P2). |
| H-10 | 2.10: prefer deterministic mechanisms | Deterministic checks exist only if the generated project contains them. Hooks cost latency and portability, and can misfire. | Prose asks Claude to create the enforcement, which brings back the same reliability problem. Noisy hooks get switched off. | Ship enforcement as files (§10.3). Few, fast hooks that inform. Make one blocking only after measuring it. |
| H-11 | 4.4: backend/frontend separation | It needs more than two scopes, and path scoping depends on naming conventions. | Test and delivery policy end up in the wrong scope; globs break in existing repos. | Scopes: common, backend (with per-layer rules), backend-tests, frontend, delivery, meta. Document the coupling to naming conventions. |
| H-12 | 2.11: adding a technology should not require editing many files | Some edits are unavoidable: the decision, the knowledge, sometimes a rule. | Chasing "one file" leads to technology knowledge being mixed with decisions again. | Aim for at most 3 files, by a documented procedure (§4.7). |
| H-13 | 2.13: dogfooding inside the template | Template users rarely evolve the instruction architecture, and an always-available meta skill costs context. | Noise in downstream projects. | Ship `template-maintenance` as user-invoked only (no model context) plus S2. Keep research prompts in the research repo. |

---

## 14. Open questions requiring human decisions

**Needed before Phase 1**

| # | Question | Recommendation |
|---|---|---|
| Q1 | Replace the six-level hierarchy with kinds × scopes? | Yes |
| Q2 | Where should the decision register live: `docs/architecture/decision-register.md` (project-owned, imported) or inside `.claude/`? | `docs/architecture/` |
| Q3 | Use IDs only for decisions (`D-xx`) and reserved classes (`R-x`)? | Yes; no IDs on individual rule statements |
| Q4 | What should hooks and scripts run on: PowerShell 7, bash (Git Bash on Windows), or .NET 10 file-based C# scripts (`dotnet run check.cs`; the SDK is already required, but startup time needs measuring)? | Measure in Phase 0. Lean towards .NET file-based scripts for S1/S2, and the lightest option for per-tool hooks. |
| Q5 | Git permissions: `ask` for every repository-changing operation, or `deny` some (such as force push to main)? | `ask` everywhere; no `deny` |
| Q6 | Architecture tests: a dedicated `<Name>.ArchitectureTests` project or inside `IntegrationTests`? Reflection only, or NetArchTest/ArchUnitNET? | A small dedicated project; reflection only at first |

**Needed before Phases 3–4**

| # | Question | Recommendation |
|---|---|---|
| Q7 | How strict should analyzers be? Use `TreatWarningsAsErrors`? Add BannedApiAnalyzers (a new dependency)? | Treat warnings as errors for nullable and selected CA rules. BannedApiAnalyzers is optional and goes through a decision. |
| Q8 | Ship `.editorconfig`, `Directory.Build.props` and `Directory.Packages.props` at the template root? | Yes |
| Q9 | Merge serilog into logging? Merge resilience and httpclient-factory into outbound-http? Keep configuration and DI separate? | Yes to all three |
| Q10 | Record Minimal APIs as "not adopted", with adoption Reserved? | Yes |
| Q11 | Where is the Result boundary: outcome types specific to one use case are Delegated, and a shared Result type is Reserved? | Yes |
| Q12 | Add `rules/frontend/angular.md`? | Yes |
| Q13 | Allow optional `docs/features/<feature>.md` files, linked from `SPECIFICATION.md`? | Yes, optional |
| Q14 | Should substantial work always be reviewed through the `code-reviewer` subagent? | Yes; small changes can be reviewed inline |
| Q15 | Accept a Stop hook (H4) that runs at the end of every turn, including Q&A? | As an experiment, non-blocking, adopted only on benchmark evidence |
| Q16 | Record Delegated decisions anywhere? | No; only in the task summary |
| Q17 | In headless runs, choose the compliant option A and report? | Yes |
| Q18 | Ship `template-maintenance` in the template? | Yes, user-invoked only |
| Q19 | Keep `git-workflow`? | Yes, for conventions only |
| Q20 | Benchmark protocol: a copy of the template as the project root, a pinned Claude Code version, several runs per scenario, and the trigger suite included? | Yes |
