# L1-Restart — independent audit of corrective pass 1

**Reviewed input:** `L1-Restart_1.zip`, 22 October 2026.  
**Decision:** **NOT READY TO FREEZE.** First restart pass materially improves Run-02, but two reproduced, in-scope enforcement defects remain. A narrowly scoped second pass is recommended. 

## 1. Verifiable baseline, change control and reports

- Immutable input manifest: 144/144 entries verified against `MANIFEST.sha256`.
- Original `baseline/template/`: 85 files, 298,925 bytes. Final `output/template/`: **86 files, 351,673 bytes**. `output/` contains only the template and `REFINEMENT_REPORT.md`; no `.work` folder.
- File-level diff: **3 added, 2 removed, 33 modified**. `CLAUDE.md` byte-identical to original.
- Recalculated final tree checksum: **`e11bcf8c00b884aabe8d4b6408f90f66c4ab2b67fab534fcc9dd66508702cc22`**, identical to the Claude report, using `find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum -b | sha256sum`. The `-b` flag matters: the plain default hash listing produces a different top-level checksum without any difference in file contents.
- JavaScript: all six `.mjs` files passed `node --check`.
- Clean instruction checker: **PASS (68 artifacts, 0 violations, 0 warnings)**.
- Clean architecture checker: **NOT APPLICABLE (no backend directory)**, which is not a build nor a project-graph acceptance test.
- Claude's `REFINEMENT_REPORT.md` claims **302/302** in its own now-deleted temporary test harness. This full suite **was not independently reproduced**; only a separate purpose-built suite was executed.

## 2. Independent tests and evidence

| Suite | Correct/total | What it tests |
|---|---:|---|
| Strict P4/P6 body, list and sibling test cases | **100/100** | L0 and L1, forbidden selection, valid clean references, neutral siblings, referential duties, forms, API and package vocabulary |
| Targeted instruction-checker negative mutations | **15/15** | `onFailure`, hook registration/paths, fifth slot, selected-only module, required `binds:` incl. both sides removed, reverse direction, framework-leak, references, facets |
| Git + Node process-level hooks | **27/28** | Pre routing, fail-closed, Post success/failure actual-state, single-quote XML, PowerShell-compatible encodings, linked worktree isolation, Stop dedup |
| .NET architecture checker sample projects | **10/15** | valid and invalid refs, tests isolation, package boundaries, SDK and ASP.NET Core packages |
| P4 heading-only and heading/governor cases | **6/20** | concrete technology in Markdown headings (existing P4 grammar, levels 0 and 1) |

**All independent results:** 158 / 178. These are targeted tests and some failure variants share one root cause; the ratio is not a statistical reliability score. Evidence JSON files accompany this report.

## 3. BLOCKER A — the P4 neutrality checker skips headings entirely

Source: `output/template/.claude/scripts/check-instructions.mjs`, `neutralityCheck(...)`:

```js
for (const block of blocks) {
  if (block.type === 'heading') continue;
  // technology vocabulary and API-shape checks only run for other blocks
}
```

In both Level 0 (`.claude/rules/0-core/engineering.md`) and Level 1 (`.claude/rules/1-architecture/frame/boundaries.md`), **each of the following headings is wrongly accepted (PASS, 0 violations)** when appended to a rule:

```markdown
## Docker is required for deployment
## Selected deployment technology: Docker
## Must use Swagger
## Default logging provider: Serilog
```

A heading on its own is already an instructional statement, and the agreed strict P4 contract does not exempt bare product names or explicit selections merely because they are headings. A heading plus an unrelated body line also remained falsely accepted. 14 negative tests (seven variants x two levels) failed for this single reason; the six remaining heading controls behaved as expected.

**Required correction:** apply the existing vocabulary/API/strict-reference checks to heading text as content, while still using headings as governing context for their descendants. A positively recognized pure, non-normative technique pointer may be exempt according to the frozen P4 grammar; plain named technologies, selected/default/required technologies and API types may not. Preserve all 100 passing body/list tests; do not add a new Markdown grammar or deny-list expansion.

## 4. BLOCKER B — Domain/Application may implicitly or explicitly take an ASP.NET Core dependency

Owner: `.claude/rules/1-architecture/frame/boundaries.md` (Domain section says **keep Domain free of ASP.NET Core**, and Application explicitly must not use ASP.NET Core transport types). `check.json` already declares `Microsoft.AspNetCore.App` forbidden in inner roles. Yet `check-architecture.mjs` only inspects *explicit* `<FrameworkReference>` and the separate persistence package prefixes. It never inspects the static `Project Sdk` attribute or ordinary `Microsoft.AspNetCore.*` package references for inner projects.

Proved with real .NET project files and also via `PostToolUse`:

```xml
<!-- All three are wrongly accepted in a Domain project: -->
<Project Sdk='Microsoft.NET.Sdk.Web'>
```

```xml
<PackageReference Include='Microsoft.AspNetCore.Mvc.Core' />
```

```xml
<PackageReference Include='Microsoft.AspNetCore.Authentication.JwtBearer' />
```

The Web SDK implicitly supplies ASP.NET Core framework references. `Application` with Web SDK likewise passed incorrectly. For comparison, an **explicit** `<FrameworkReference Include='Microsoft.AspNetCore.App'/>` and `Domain → Api` were correctly rejected, while ordinary Domain `Microsoft.NET.Sdk`, Api Web SDK and valid inward references passed. A post-shell event also returned 0 findings for Domain Web SDK.

**Required correction:** reject Web SDK and concrete ASP.NET Core transport/implementation package references in **Domain and Application** only, preserving allowed Api entry-point/IntegrationTests uses. Parse both XML quote styles. Do not implement full MSBuild evaluation; document static checking limitations as before. The post-change hook must observe the architecture checker violation without needing a new hook design.

## 5. Other verified gates and remaining limitations

- Critical PreToolUse fails closed on malformed/empty input. `dotnet add/remove reference` → ask. `npm --prefix`, `pnpm --dir`, `yarn --cwd` → deny once then identical retry allowed. Peer dependency bypass → ask; `npm ci` / restore / unrelated shell strings do not block.
- PostToolUse and PostToolUseFailure detect invalid project references and package mutations despite unrelated command text; UTF-16LE odd-length failure reported. Linked worktree test confirms active path detection and unchanged main checkout. Stop dedup works on material same-file change.
- Four slots and required frame/leaf binds enforced under independent mutation tests, including simultaneous removal from persistence contract and module.
- Strict P4/P6 body/list handling passed 100 independently authored cases. Valid genuine references in the pristine template also pass its checker.
- **196/196 policies** and zero owner/trigger/scope regressions are claimed in Claude's report; the deleted complete policy-to-owner oracle was not available. Immutable source integrity is independently verified, but I did **not** repeat a complete semantic crosswalk of all 196 policies. The remaining 302/302 Claude harness result likewise cannot be treated as an independently reproduced suite.
- Live Windows PowerShell 5.1 and Claude Desktop hook activation were not rerun here. Process-level tests with Node, Git and synthetic host input do not prove integration with the Desktop host.

## 6. Freeze decision and bounded next step

**Do not freeze at iteration 1.** There are two actual policy-enforcement gaps, not a failed protocol/oracle or a theoretical unbounded English edge case. They are independent, localizable and should be resolved together in one small corrective pass.

Restrict production file edits to `check-instructions.mjs`, `check-architecture.mjs`, and if necessary `scripts/lib/project.mjs` for reusable static XML attribute extraction. The architecture rule, source policies, slot selection and other instruction files remain unchanged. Update the existing `output/REFINEMENT_REPORT.md`. Build a finite tests-first matrix for these two roots and negative/positive counterparts; rerun known stable gates and one final confirmation, then stop. No L1 iteration 9/legacy checkout, no new speculative P4 grammar and no infinite self-audit.
