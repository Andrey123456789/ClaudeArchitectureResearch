# L1 Run-2 notes

## Sweep notes

Reverse checks conducted after all 10 batches, judged from L1's own text (no judgment carried over from K1 or K0; only the classification method was reused):

1. **Keyword scan of all NON_NORMATIVE / IMPLEMENTATION / DUPLICATE spans** (`_tools/sweep.py`); every Markdown hit re-read in context. Six security-scan investigation prompts that restate rules were reclassified from NON_NORMATIVE to DUPLICATE (scan-layers lines 18, 50, 51, 58, 62). Imperative technique notes were recorded as NON_NORMATIVE orphans (EF Core bulk operations, 304/429/502 reference entries, Swagger launch profile and document partitioning, frontend and authorization test targeting, builders/fixtures, review scoping, example numbers, image optimization, ClockSkew heuristic, Result typed-error shape).
2. **Large-span review** (NN/IM/DU spans of 15+ lines): code samples, YAML/JSON examples, navigation tables of the instruction map, `.editorconfig` suggestion-level settings and hook registrations only.
3. **Script branch review**: `pre-shell-command.mjs` (fail-closed via `onFailure: block`; force flags and reference commands → `ask`; dependency changes including removals and the frontend CLI → deny once, identical retry allowed within 30 minutes), `post-change-checks.mjs` (actual manifest state after edits and shell calls, including failed calls; deny list, approval lists from project and module facets, CPM, floating/prerelease versions, removed/moved manifests, architecture check after project-file changes, product-source reminder; findings exit 2 after the tool ran, internal failures never block), `stop-cochange.mjs` (Git-only; seed, migration, test and product-source reminders; once per material state; outside Git a system message only), `check-architecture.mjs` (reference direction, test-reference warnings, ASP.NET Core and EF Core packages in inner roles, top-level tests directory), `check-instructions.mjs` (every predicate mapped to X1, X2, X3, X12, X13, X14, X15 or R1/R2), `lib/project.mjs` (helpers only).
4. **Branch findings recorded**: the deny-once dependency gate cannot verify that add-dependency ran (exception of R21/X10); the reference gate asks on every reference command, including layout-conformant ones (X11); the manifest hook escalates a second test framework and overlapping frontend libraries from 'concrete reason/need' to 'approval' (noted in R22, R28).
5. **Config defaults**: settings.json (critical PreToolUse fail-closed, advisory post/Stop hooks), `.editorconfig` (IDE0005 warning; other settings suggestions), Directory.Build.props (net10.0; Nullable and ImplicitUsings registered as EXTRA-L1-0035), Directory.Packages.props (CPM on, empty), `.gitignore` (local secrets ignored, Development contract files tracked).
6. **Mixed clauses** split into oracle and extra parts (e.g. CLAUDE.md Reserved list and approval/ADR line, decisions persistence row, git-workflow high-risk operations, add-dependency resilience and removal, security-scan report shape, contracts' replacement sections).
7. **Notable L1-specific structure**: the capability model (four slots, static composition, contracts, manifests, leak rule, frame/leaf ownership, binds:, replacement and removal procedures, declared persistence properties) and the level model (headers, conformance direction, Core/Architecture technology neutrality) are registered as template-structure extras (X1–X6, X12–X15, X33); none of them is entailed by an oracle policy.

Classification rule (same method as for K1 and K0): EXTRA when binding (must/never/do not/only, a named anti-pattern prohibition, or hook/checker-enforced), outcome-changing and not entailed by a stack-neutral reading of an oracle policy; technique classes excluded by the oracle (EXC-002..EXC-018) stay NON_NORMATIVE; workflow report-content mandates beyond WF-009 are EXTRA.

## Limitations

- Structural PASS (validators 11/12/13) is not semantic proof.
- All 196 policies are MATCHED; tightened modalities and extra gates are noted in search_notes instead of downgrading status.
- Hooks and checkers were analyzed statically, not executed.
- Two relations remain open (UNCERTAIN-L1-0001 'commit package.json and package-lock.json'; UNCERTAIN-L1-0002 'or required by an approved workflow').
- CANDIDATE.md was read as provenance only; classifications rest on the template text.
- Identifier numbers are local to this run.
