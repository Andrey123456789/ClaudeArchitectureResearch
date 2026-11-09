# L1-Restart — Independent Audit of `iteration_after_audit_3`

**Review status:** ACCEPT / READY TO FREEZE for phase 5.3, within the documented acceptance and verification boundary.

**Source:** `L1-Restart_AA3.zip` — `L1-Restart/output/template/`, plus the root source manifest, original candidate materials and current report. **Comparison source:** final `L1-Restart_AA2.zip` template (file-hash comparison only for the change scope). **Reference implementation:** L0's final `TECHNOLOGY_TERMS` list (41 terms).

## 1. Scope and integrity

- Template files: **86** before and after AA3.
- Changed template file: **only** `.claude/scripts/check-instructions.mjs`, SHA-256 `d315eaba57aa...` → `8171ce3941aba33d75a0b609d9d0c8a3f8761ad574b8a709209be6c219c55663`.
- Exact checker change: insertion of `Scrutor` and `Jest` into `TECHNOLOGY_LEXICON`. The other 85 template files are byte-identical to AA2.
- `baseline/`: 88/88 identical; `source/`: 43/43 identical; `audit/`: 8/8 identical relative to AA2.
- Original root `MANIFEST.sha256`: **144/144** verified against the AA3 archive.
- `output/` contains only `template/` and `REFINEMENT_REPORT.md`, without `output/.work/`.
- Independently recomputed final tree hash (sorted binary `sha256sum` listing): `41084c6bab8399a7148d39b8c1d293dd52045b0c17083c9b8bd9aca7a1beb436`, matching the implementation report.

## 2. Independent functional verification

| Verification | Result |
| --- | ---: |
| Real instruction checker fixtures on isolated full template copies | **151/151 PASS** |
| Of these: expected failures required a relevant technology-neutrality diagnostic | **130/130** |
| Of these: expected passes (including clean template and Level-2/Level-3 controls) | **21/21** |
| Structural mutations and Git/hook/architecture integration checks | **17/17 PASS** |
| Clean instruction checker | **68 artifacts, 0 violations, 0 warnings** |
| JavaScript module syntax (`node --check`) | **PASS** |
| Original source manifest | **144/144 PASS** |

### Technology neutrality / P4

Independent cases injected into Level 0 `.claude/rules/0-core/engineering.md` and Level 1 `.claude/rules/1-architecture/frame/boundaries.md`. `Jest` and `Scrutor` were tested in prescriptions, pure `Technique:` references, headings, nested lists, tables, formatting, uppercase/lowercase, paragraph continuations, and PascalCase identifiers. All were rejected for the **right reason**. Pure pointers are intentionally forbidden when naming concrete technology at Levels 0/1 under the agreed conservative policy.

Additionally, **all 41 technology terms** in L0's defined forbidden technology list were exercised at **both** Level 0 and Level 1 in L1, with an explicit `Must use ...` negative fixture. All 82 produced the expected neutrality diagnostic, including RxJS, Vitest, HybridCache, SQL Server, Jest, and Scrutor.

Positive fixtures proved that genuinely neutral instructions do not fail, including a requirement to run unit tests, reference to selected technology **without naming a technology**, and allowed fixed-platform vocabulary. `Jest` and `Scrutor` remained permitted in Level 2 and Level 3. Ordinary words containing unrelated substrings were also accepted.

**Test-oracle correction:** The initial positive `Follow the backend-testing.framework capability.` fixture was invalid at Core/Architecture because it introduces a prohibited dependency from a more stable level to a less stable facet. It was replaced by a properly neutral phrase (`Follow the selected testing capability.`); the candidate template was not changed. This is a correction to the independently designed test, not an observed product regression.

### Capability, architecture and hook regression controls

Mutation tests confirmed that a fifth capability slot is rejected, an absent required persistence `binds:` is rejected even if the corresponding contract requirement is deleted, and a concrete technology cannot be legalized by adding it to the architecture frame vocabulary. Real `.csproj` tests confirmed allowed Application→Domain references, rejected Domain→Api links with single-quoted XML, rejected Web SDK and ASP.NET Core packages in Domain, and verified that `PostToolUseFailure` catches a newly introduced forbidden dependency in a temporary real Git repository. PreToolUse rejected malformed JSON (exit code 2), requested user approval for peer-dependency bypass flags (`permissionDecision: ask`), and permitted an ordinary safe command. Stop with `stop_hook_active: true` returned without starting a loop.

**Test-oracle correction:** A first binding mutation used invalid `binds: none — ...` rather than valid `binds: none` and therefore triggered a format diagnostic. Replacing the mutation with `binds: none` confirmed both required-binding checks. A PreToolUse bypass returns a permission decision rather than a nonzero exit code; the independent oracle was corrected to inspect the structured decision. The candidate was not changed.

## 3. Final disposition and evidence limits

**ACCEPT for phase-5.3 freeze.** The previously reported Jest/Scrutor omissions are resolved. No blocking regression was found in the independent matrix. No additional L1 corrective pass is warranted on the basis of the known P4 issue.

This is an engineering acceptance result, **not a proof of correctness for arbitrary natural language, unknown technologies, or every possible MSBuild file**. The `check-architecture.mjs` run on the unmodified template says `NOT APPLICABLE (no backend directory)`; actual project behavior was separately exercised in an isolated Git repository. Windows Claude Desktop live-hook execution was not performed. The 196 policy inventory was not independently re-read and semantically re-audited end-to-end during AA3; normative files are byte-identical to AA2 and the original candidate/source materials are unchanged.

For reproducibility, this audit used Node.js v22.16.0 and isolated copies of the final template. No user repository files were modified by the independent tests.
