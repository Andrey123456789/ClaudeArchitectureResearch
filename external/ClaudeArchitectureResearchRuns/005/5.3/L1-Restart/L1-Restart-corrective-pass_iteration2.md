# L1-Restart — corrective iteration 2 (Phase 5.3)

## Purpose and authority

Continue **IN PLACE** from the completed **L1-Restart iteration 1** `output/template/` (86 files). Do not begin another restart, copy `baseline/template/`, restore L1 iterations 2–8, change the candidate identity or broaden the P4 natural-language grammar.

Read: this entire task; `L1-Restart-REFINEMENT_TASK.md` (frozen P4/P6, D1–D17, stopping protocol); `output/REFINEMENT_REPORT.md`; `audit/DEFECT_DOSSIER.md`; the current implementation of `.claude/scripts/check-instructions.mjs`, `check-architecture.mjs`, `scripts/lib/project.mjs` and the selected `architecture.check` JSON facet. Refer to the independent reproduction cases below. Do not treat the old `302/302` as proof about new negative cases; the temporary harness was removed as designed.

**Permitted persistent changes:**
- `output/template/.claude/scripts/check-instructions.mjs`;
- `output/template/.claude/scripts/check-architecture.mjs`;
- `output/template/.claude/scripts/lib/project.mjs` **only if needed** for reusable, bounded static XML extraction;
- append the accurate corrective-pass-2 evidence to `output/REFINEMENT_REPORT.md`.

All other template files must remain **byte-identical** to iteration 1. In particular: no rule prose/policy edits, no manifest/slot/facet/`binds:` changes, no hook/settings edits, no added permanent files, no source/baseline/audit/root task changes. Temp fixtures are permitted only in `output/.work/` and must be deleted last. Current tree hash from `find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum -b | sha256sum`: `e11bcf8c00b884aabe8d4b6408f90f66c4ab2b67fab534fcc9dd66508702cc22`. Verify and record it ONCE before editing.

## Defect A — heading content bypasses the technology-neutrality check

`neutralityCheck(...)` currently contains `if (block.type === 'heading') continue;`. Thus a heading that *itself* selects a Level-2 technology is never checked. This is directly inside the already-agreed P4 scope: same-line normative statement in one of the six supported Markdown structural forms, not a new syntax or new product vocabulary.

In **each** of `.claude/rules/0-core/engineering.md` and `.claude/rules/1-architecture/frame/boundaries.md`, inject into a fresh isolated test copy:

**Must FAIL with a concrete-technology neutrality diagnostic:**

```markdown
## Docker is required for deployment
```

```markdown
## Selected deployment technology: Docker
```

```markdown
## Must use Swagger
```

```markdown
## Default logging provider: Serilog
```

```markdown
## Use Docker for deployment
- Additional non-normative context.
```

```markdown
## Docker
```

The bare `Docker` heading is ambiguous/unproven as a pure reference, so strict P4 gives **NO EXEMPTION**. Heading-only or heading-with-neutral-sibling behavior must be the same. The current checker falsely accepts them all.

**Must PASS:** benign headings (`## Deployment technology` / `## HTTP API`), a genuinely recognized non-normative heading pointer (`## Technique: ` + backticked `docker`, if that is admitted by the established positive grammar), and the current real clean template. Keep meaningful platform/role vocabulary within its existing fixed boundary.

**Implementation requirement:** evaluate heading blocks' own technology tokens and API-shape identifiers via the same centralized check used for paragraphs/list items, while preserving their *separate* function as governing context for descendants. Explicitly preserve the earlier 100 passing real-checker body/list/sibling P4 cases: selected/required/default with neutral siblings FAIL, `Must use this technique` FAIL, neutral/unrelated `Must run unit tests` with pure pointer PASS, ambiguous generic `Engineering Discipline` route FAIL, legitimate reference-only pointers PASS. Do not add another growing deny-list, new NLP semantics, or reinterpret P6.

## Defect B — inner-role ASP.NET Core dependencies not detected when implicit or via packages

The authoritative `.claude/rules/1-architecture/frame/boundaries.md` says Domain is free of ASP.NET Core and Application must not use ASP.NET Core transport types. The selected `.claude/capabilities/architecture/clean-architecture/check.json` already forbids `Microsoft.AspNetCore.App` framework references in inner roles, but `.claude/scripts/check-architecture.mjs` only observes **explicit** `<FrameworkReference>` and persistence package prefixes. A `.csproj` can acquire ASP.NET Core via the Web SDK or ordinary framework packages.

In fresh test repositories with appropriately named `backend/App.Domain/App.Domain.csproj`, `backend/App.Application/App.Application.csproj`, `backend/App.Api/App.Api.csproj`, and supporting projects:

**Must FAIL in Domain and Application (no false PASS):**

```xml
<Project Sdk='Microsoft.NET.Sdk.Web'><PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup></Project>
```

```xml
<Project Sdk="Microsoft.NET.Sdk.Web"><PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup></Project>
```

```xml
<Project Sdk='Microsoft.NET.Sdk'><ItemGroup><PackageReference Include='Microsoft.AspNetCore.Mvc.Core' /></ItemGroup></Project>
```

```xml
<Project Sdk='Microsoft.NET.Sdk'><ItemGroup><PackageReference Include='Microsoft.AspNetCore.Authentication.JwtBearer' /></ItemGroup></Project>
```

**Must continue to FAIL:** explicit `<FrameworkReference Include='Microsoft.AspNetCore.App'/>`, outward Domain→Api `ProjectReference`, EF Core package in Domain/Application, and production→test reference.

**Must PASS:** `Microsoft.NET.Sdk` in Domain/Application without forbidden references; a Web SDK and ASP.NET Core packages in an `App.Api` entry-point project; permitted inward Api→Application/Domain and Infrastructure→Application references; appropriate integration-test projects. Both single and double XML quotes must be equivalent. Treat unknown MSBuild property evaluation as the already-documented limitation, not as permission to accept a known literal `Sdk` or package ID.

The existing `PostToolUse` / `PostToolUseFailure` route must surface the resulting `checkArchitecture(...)` finding after a real `.csproj` edit in an active Git worktree, including a failed shell invocation with partial side effects. **Do not rewrite hook dispatch or snapshots**: the checker runs from the post-change hook already. Confirm by a focused integration test.

Prefer a small, explicit rule under the selected architecture frame's inner-role check, not a global ban of ASP.NET Core: Api is intentionally an ASP.NET Core adapter. Do not change the selected frame JSON or policy text. If reusable XML extraction needs an addition in `lib/project.mjs`, implement it there in a bounded way with comments and tests.

## Focused preservation and acceptance

1. Build **one** finite, table-driven real-checker fixture harness in `output/.work/`; lock expected verdicts *before editing*. Do not create hundreds of variants, reconstruct deleted old 302-test machinery, or fuzz random natural-language phrases. Require the **correct diagnostic**, not merely nonzero exit, for FAIL cases. Confirm clean PASS has 0 violations/warnings.
2. Baseline checkers and all `.mjs` syntax; 86-file structure; original immutable source manifest; byte identity for all unmodified template files; known benign P4 pointers; four static slots, correct frame/leaf mapping, required `binds:` including both-sides-removal negative test, frontend optional clearing in a sandbox; hook event/onFailure settings unchanged. Run focused representative mutation checks, not the entire historic campaign.
3. Actual process-level Git scenario: `PostToolUseFailure` with changed Domain Web SDK or ASP.NET Core package produces an architecture diagnostic; unchanged shell event is quiet; original legitimate project/hook behavior unaffected. No need to rerun exhaustive Windows linked-worktree/encoding/Stop experiments because the hook implementations remain byte-identical and iteration 1 already documented that evidence. Never claim a live Claude Desktop run when only a controlled Node host was tested.
4. Policy preservation 194 + GOV-017/GOV-018: the non-code instructional files must all be byte-identical, so their text/owner/trigger/scope cannot regress in this pass. Do not claim an independent semantic proof of all 196 if only using the previous report; state the evidence chain accurately.
5. At most one final cumulative confirmation audit against **unchanged** fixture definitions and oracle hash. If a genuine implementation defect is found, make **one bounded repair** then reconfirm **once**, otherwise report `BLOCKED` with exact fixture results. A broken test oracle must be fixed **before** final confirmation and described honestly; never change it mid-audit to turn red into green. No repeated self-audits prompted by Stop hooks.
6. Append `Corrective pass — iteration 2` to the existing `output/REFINEMENT_REPORT.md`, recording starting/final tree hashes (`sha256sum -b` method), exact changed files, concrete causes, test verdicts, 86-file invariant, policy identity proof, independent/previous evidence labels, limitations and **truthful** status (`STRICTLY_BETTER`, `NOT_PROMOTED` or `BLOCKED`). Remove `output/.work/` **last**, confirm only `template/` and `REFINEMENT_REPORT.md`, then STOP.

Promotion requires both defects fixed, no loss of legitimate references and previously passing invariants, and no changed authoritative instruction content. A STOP hook objecting after genuine completion is not permission to enter another validation cycle. If the run cannot finish under this bounded scope, stop and request owner intervention; never fabricate success.
