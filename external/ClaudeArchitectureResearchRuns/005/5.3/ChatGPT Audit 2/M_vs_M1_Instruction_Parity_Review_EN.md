# M vs M1 — Instruction and Requirement Parity Review

**Research phase:** 5.3  
**Input:** `MandM1.zip`  
**Scope:** FINAL runtime templates only, at `M/output/template/` and `M1/output/template/`, with `CANDIDATE.md` and the frozen source invariant/inventory files consulted to establish intended design. The implementation reports and previous ChatGPT audits were not used as evidence of runtime equivalence.  
**Method:** Static inspection and cross-file tracing of always-loaded policy, path rules, skill routing, selected capability records, and build configurations. **No paired Claude code-generation run was performed.** Behavioral predictions are hypotheses to test, not observed model outcomes.

## Bottom line

The intended controlled factor is replacement support: M embeds the selected implementations; M1 introduces four statically selected capability slots. Their two copies of `source/inventory.json` and `source/shared-research-invariants.json` are byte-identical, but identical input policy inventories do **not** establish identical effective instructions. Several non-slot differences could change the generated code, the verification gates or the autonomy of the agent.

- M runtime template: **61 files**; M1: **80 files**. The extra file/indirection cost is partly intentional.
- **Highest-confidence non-slot differences:** actual .NET build/style enforcement; the instruction that triggers the end-to-end implementation workflow; the default frontend framing; narrower or broader path-trigger activation.
- **Other potentially behavior-changing differences:** an explicit M ban on Minimal API endpoint groups vs a Controller default in M1; different API-version-deprecation owners; stricter NUnit parametrization advice in M1; the wording of HTTP transport leakage across Application boundaries.
- **Mostly equivalent requirements with redistributed owners:** Clean Architecture graph, Application Services, specific repositories, UoW, EF Core as Infrastructure implementation, Development seeding, most test-isolation requirements, HTTP status conventions, and Git safety.

## I. Potentially material non-capability drift

### P1 — Actual compiler/analyzer and editor configuration differs (HIGH, observed)

- **M:** `Directory.Build.props` includes `<AnalysisLevel>latest</AnalysisLevel>` and `<EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>`. `.editorconfig` sets `dotnet_diagnostic.IDE0005.severity = warning` and also defines an async method naming preference.
- **M1:** `Directory.Build.props` includes `TargetFramework`, `Nullable`, `ImplicitUsings`, but neither of the two settings above. `.editorconfig` sets `IDE0005` to `suggestion` and includes additional braces, expression-body, and modern-syntax preferences.
- **Consequence:** The same C# solution may encounter different build diagnostics or formatting pressure. This is **not** a capability-slot effect. M1's `verify` skill can still invoke `dotnet format`; that does not make the build configurations identical.
- **Probe:** Generate identical code under both templates and compare `dotnet build`, `dotnet format --verify-no-changes`, and diagnostics with the same SDK/command.

### P2 — End-to-end workflow applies to different change sizes (HIGH, observed)

- **M:** `CLAUDE.md`, Workflow Routing, explicitly routes **any implementation change** to `development-workflow`. Its skill description repeats that scope.
- **M1:** `CLAUDE.md` and the skill description emphasize a new application, feature, bug fix, refactor, or another **non-trivial** implementation change.
- **Consequence:** For a one-line fix or small code/config modification, M directly requires the whole workflow while M1 leaves more room to bypass its preparation, specialized co-change steps, and review sequence. Both separately route `verify` before completion, so this does not prove M1 omits verification.
- **Probe:** Request the same very small production-code bug fix and inspect skill invocation, regression coverage and verification evidence.

### P3 — Generated-output, CI/CD and API deprecation duties are distributed differently (MEDIUM/HIGH, activation risk)

- **M:** `.claude/skills/development-workflow/SKILL.md` directly includes dedicated sections for **Generated output**, **API version deprecation**, and **CI/CD and deployment**.
- **M1:** `development-workflow` is shorter. Related obligations live in `build-fix`, `angular`, `persistence-change`, `verify`, `architecture-decision` and dedicated technology skills; `.claude/rules/api.md` routes published-version deprecation to `architecture-decision` instead of `development-workflow`.
- **Consequence:** Many obligations remain present, but an agent must follow more conditional skill links at exactly the right time. The same API contract change or generated-client issue might trigger a different procedure or a different number of skills. This is a discoverability concern, not proof that M1 lacks the policies.
- **Probe:** Make a backend contract change requiring client regeneration, and separately deprecate an externally used API version. Compare the actual co-change and approval steps.

### P4 — Frontend baseline is framed differently (HIGH for greenfield benchmark, partly intentional)

- **M:** `CLAUDE.md` describes a reusable **ASP.NET Core + Angular** application template. `docs/technology-stack.md` gives the Angular baseline.
- **M1:** `CLAUDE.md` describes an ASP.NET Core backend with an **optional** web frontend. `docs/capability-selection.md` currently selects the optional `frontend/angular` slot.
- **Consequence:** At the current selected state both prefer Angular when a frontend is required. But for a broad greenfield prompt that doesn't explicitly ask for frontend, the two introductions bias whether a frontend is scaffolded at all. Optional frontend selection and removal are intentional capability features; unsolicited frontend-generation bias is a potential experimental confounder.
- **Probe:** Use two task variants: backend-only explicitly, and backend+Angular explicitly. Do not leave frontend scope implicit when comparing ordinary code quality.

### P5 — Explicit restriction on Minimal API is less visible in M1 (MEDIUM/HIGH, wording/priority risk)

- **M:** `CLAUDE.md` lists Minimal API endpoints as a **not-adopted** HTTP model; `.claude/rules/architecture.md` explicitly says not to create Minimal API endpoint groups unless requested.
- **M1:** always-loaded `docs/capabilities/architecture.md` selects **ASP.NET Core Controller** as entry point, and `.claude/rules/architecture.md` calls Controllers the default. An explicit no-Minimal-API instruction remains in `project-structure/references/backend-layout.md` (loaded via that skill), but it is not as plainly present in the primary architecture rule.
- **Consequence:** A Controller-default instruction is weaker than a blanket ban unless the system consistently treats changing the selected entry-point model as Reserved. For an endpoint-only task, M1 may be more likely to interpret Minimal APIs as a permissible exception. This is a **predicted risk**, not a demonstrated generation difference.
- **Probe:** Ask for a new endpoint when neither Minimal APIs nor Controllers are named in the task and inspect generated route organization and Decision Requests.

### P6 — HTTP-specific boundary exception differs (MEDIUM, observed wording)

- **M:** `.claude/rules/architecture.md` says not to leak `HttpResponseMessage` or remote transport concerns into Application.
- **M1:** the corresponding rule says not to leak these concerns into Application contracts **unless the Application explicitly models HTTP**.
- **Consequence:** M1 exposes a conditional exception absent from M; the same HTTP integration can receive a different Application-facing contract. Some exceptions may be defensible, but this difference is outside the capability-selection variable.
- **Probe:** Ask for an outbound HTTP adapter with an Application-facing abstraction and inspect whether its interface returns transport-level HTTP types.

### P7 — NUnit parameterized test guidance is stronger in M1 (MEDIUM, observed)

- **M:** `.claude/rules/testing.md` **prefers** explicit declarative `[TestCase]` cases over generated-case machinery for small, finite domains.
- **M1:** `.claude/rules/testing.md` expresses the same general preference, but `.claude/rules/test-framework.md` adds that the case tables **are written as `[TestCase]` rows rather than `TestCaseSource` generators**.
- **Consequence:** On a task with sizable dynamic fixture sets or generated test cases, M1 might resist an otherwise sensible `TestCaseSource` approach more strongly than M. The latter's special cases should be reconciled, not silently treated as equivalent.
- **Probe:** Ask for parametric tests over a generated matrix with non-constant data and compare how both handle NUnit data sources.

### P8 — Path-scoped rule loading is not equivalent (MEDIUM, observed)

- **M Angular rule:** `.claude/rules/angular.md` matches `frontend/**/*.ts`, `frontend/**/*.html`, `frontend/**/*.scss`.
- **M1 frontend rules:** `.claude/rules/frontend.md` and `frontend-framework.md` match `frontend/**/*`.
- **M repository-structure rule:** includes root `Directory.Build.props` and `Directory.Packages.props`; **M1 physical-structure rule** does not list those files (though the M1 dependency rule does).
- **M security rule:** explicitly includes `.github/**` and hidden YAML naming variants; **M1 security rule** adds `**/.env*`, `**/*.targets`, `**/*.config` but does not explicitly list `.github/**`.
- **M1 API rule:** additionally matches `backend/**/launchSettings.json`; M API rule matches backend C# files.
- **Consequence:** Even identical substantive policy can be more or less likely to be loaded for `angular.json`, `.env.local`, CI files, project config or launch profiles. Coverage depends on the actual path matching semantics, and some of these rules may still be reached through explicit workflows.
- **Probe:** Present identical config-only editing tasks and capture which rule files are actually loaded before modification.

### P9 — HTTP 201 and 204 guidance differs in where and how explicitly it is given (LOW/MEDIUM)

- **M:** `.claude/rules/api.md` explicitly states **a 204 response has no body**. Its 201 description emphasizes creation of an API resource.
- **M1:** `.claude/rules/api.md` adds a `Location` header expectation when a stable resource URI exists, but does not repeat the 204 body prohibition in that primary rule.
- **Both:** the `http-api` knowledge skill covers detailed status semantics.
- **Consequence:** Common handler code could choose different response content/header behavior depending on whether the detailed skill was loaded. This is a **rule prominence** disparity, not complete absence of the HTTP policy.
- **Probe:** Request a create and a delete endpoint with no HTTP semantics specified and inspect headers and bodies.

## II. Semantically aligned policies that have different ownership or file locations

Do **not** classify the following as defects merely because the files and wording differ:

| Topic | M owner | M1 owner(s) | Finding |
|---|---|---|---|
| Inward Clean Architecture dependencies, Application Services, repository boundaries | `CLAUDE.md`; `.claude/rules/architecture.md` | `docs/capabilities/architecture.md`; `.claude/rules/architecture.md` | Broadly equivalent at selected `clean-architecture` frame |
| EF Core isolation and SQL Server baseline | `docs/technology-stack.md`; `architecture.md` | `docs/capabilities/persistence.md`; `persistence-technology.md` | Same selected implementation; deliberate slot split |
| `IUnitOfWork`, shared scoped persistence session, no repository commits | `architecture.md` | `architecture.md`; `persistence-technology.md` | Broadly equivalent, with more explicit sample signature in M1 |
| Deterministic Development seeding and no automatic Production seeding | `persistence.md`; `development-workflow` | `persistence-technology.md`; `persistence-change` | Same intended safety constraints, different workflow routing |
| NUnit, real-provider database testing, isolated test data | `testing.md`; `technology-stack.md` | `testing.md`; `test-framework.md`; `docs/capabilities/backend-testing.md` | Broadly equivalent; see narrower `TestCaseSource` point above |
| `ProblemDetails`, centralized exception handling, no exception leakage | `error-handling.md` | `error-handling.md` | Broadly equivalent |
| Structured `ILogger<T>` + Serilog, configuration/DI rules | `architecture.md`; `coding-style.md` | `composition.md` | Broadly equivalent, not missing from M1 |
| Approval boundary for Reserved choices, product-spec supremacy, Git safety | `CLAUDE.md` | `CLAUDE.md`; capability-selection record | Same underlying governance intent |

## III. Intentional experimental differences — DO NOT normalize them away

- Four M1 capability slots: required architecture **frame**, required persistence **leaf**, required backend-testing **leaf**, optional frontend **leaf**.
- Selection record, contracts/manifests, selected-implementation facets and static `Binds:`/leak governance.
- Capability-replacement and optional-frontend-removal workflows and structural checking.
- Additional always-loaded capability decision records and resulting context/maintenance costs.

These are the treatment variables of the M versus M1 experiment. A replacement or removal benchmark should deliberately expose them rather than artificially giving M equivalent machinery.

## IV. Recommendation for experimental validity

1. **Record these differences before benchmarks.** Do not present M↔M1 as differing *only* in capabilities at the level of their current full runtime artifacts.
2. **Use identical explicit task scopes:** specify backend-only versus backend+Angular; explicit Controller model; fixed .NET SDK and build/test command; exact acceptance tests. This reduces uncontrolled task-interpretation bias without rewriting templates.
3. **Measure procedural behavior separately:** which workflows/rules were loaded, Decision Requests, generated code, `dotnet build`, `dotnet format`, test outputs, generated-code regeneration, manual-review gates and token cost.
4. If a **strictly controlled capability-effect** comparison is required, consider a second, versioned and explicitly disclosed harmonization pass for non-slot policy/build/style differences. Preserve the raw frozen originals as a separate experimental arm; do not silently alter them.
5. Use a balanced paired-task set: tiny bug fix, backend scaffold, backend+Angular scaffold, CRUD+EF integration, API create/delete, API deprecation, dynamic NUnit data, generated client update, and a genuine capability replacement.
6. Do not infer behavioral divergence from prose alone. The above are **testable risk hypotheses**; only paired execution can establish that Claude actually produces different code or procedures.

## V. Examined source paths

- `M/CANDIDATE.md`; `M1/CANDIDATE.md`
- `M/source/inventory.json`; `M1/source/inventory.json`
- `M/source/shared-research-invariants.json`; `M1/source/shared-research-invariants.json`
- **Both:** `output/template/CLAUDE.md`, `CUSTOM_SETTINGS.md`, `SPECIFICATION.md`, `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props`, `docs/technology-stack.md`, `.claude/MAP.md`, `.claude/settings.json`.
- **Both:** `output/template/.claude/rules/` — all available `.md` rules, including corresponding M `angular.md`, `persistence.md`, `repository-structure.md` and M1 `frontend*.md`, `persistence-technology.md`, `composition.md`, `test-framework.md`, `physical-structure.md`.
- **Both:** relevant `output/template/.claude/skills/` entries, especially `development-workflow`, `verify`, `project-structure`, `angular`, `build-fix`, `add-dependency`, `aspnet-error-handling`, `api-versioning`, `http-api`, `persistence-change` (M1), and logging/configuration references.
- **M1 only:** `output/template/docs/capability-selection.md`, `docs/capabilities/*.md`, and selected capability contract/manifest file locations.

**Important limit:** This is a **static instruction-parity audit**, not an exhaustive machine-proven mapping of all 196 policies and not evidence from code generation. It identifies differences that *could* materially influence a paired experiment and supplies concrete tasks to test those hypotheses.
