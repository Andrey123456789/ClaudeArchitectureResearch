# K0 Run-2 notes

## Sweep notes

Reverse checks conducted after all 13 batches, judged from K0's own text (K1 judgments not carried over; only the classification method was reused):

1. **Keyword scan of all NON_NORMATIVE / IMPLEMENTATION / DUPLICATE spans** (`_tools/sweep.py`); every Markdown hit re-read in context. No reclassification was needed; imperative technique notes were recorded as NON_NORMATIVE orphans (EF Core bulk operations, 429 reference, Swagger launch profile, mock guidance, image optimization, .gitignore guidance).
2. **Large-span review** (NN/IM/DU spans of 15+ lines): code samples, directory trees, navigation/decision tables and script helpers only.
3. **Script branch review**: hook.cjs pre-tool-use (dependency gate incl. removals and ng/nuget/PowerShell cmdlets; reference gate; Git 'ask' classification with read-only table; fail-closed deny on any error; marker comments `# add-dependency: reviewed` / `# project-references: approved` are self-certified), post-tool-use (worktree snapshot, product-input reminders, removed/moved manifests, reference-graph findings, instruction checks; decision 'block' feedback), stop (Git-only, once per exact state, seed reminder only when DbSeeder.cs exists, frontend .ts included in the test reminder), check-dependencies.cjs (deny list incl. FluentValidation.AspNetCore and Serilog.Sinks.Elasticsearch, decision notices, floating/prerelease checks, layer/test reference checks), check-instructions.cjs (every predicate mapped to X3-X6, X10-X17, R2, R119), repo.cjs (helpers only).
4. **Branch finding recorded**: with the review marker present a `--force`/`--legacy-peer-deps` install passes the hook (only the marker-less path adds the force message) — DEP-025 then rests on the add-dependency text.
5. **Config defaults**: settings.json (fail-closed PreToolUse only), .editorconfig (IDE0005 at warning; other style values suggestions), Directory.Build.props (net10.0; Nullable, ImplicitUsings, AnalysisLevel latest registered as EXTRA-K0-0041), Directory.Packages.props (CPM on, empty).
6. **Mixed clauses** (32 MIXED segments) split into oracle and extra parts (e.g. CLAUDE.md Reserved items 3 and 9, register D-05 package naming, add-dependency deprecated Polly packages, project-structure reference gate).
7. **Notable K0-specific structure**: csharp.md promotes visibility/sealed/record/primary-constructor preferences into a loaded standard (EXTRA-K0-0008); architecture.md extends Domain independence to mapping libraries (EXTRA-K0-0007); 'Common mistakes' lists in knowledge skills carry two independent restrictions (fire-and-forget EF calls X29, caching tracked entities X26).

Classification rule (same method as for K1): EXTRA when binding (must/never/do not/only, a named mistake, or hook/checker-enforced), outcome-changing and not entailed by a stack-neutral reading of an oracle policy; technique classes excluded by the oracle (EXC-002..EXC-018) stay NON_NORMATIVE; workflow report-content mandates beyond WF-009 are EXTRA.

## Limitations

- Structural PASS (validators 11/12/13) is not semantic proof.
- All 196 policies are MATCHED; tightened modalities and extra gates are noted in search_notes instead of downgrading status.
- Hooks were analyzed statically, not executed.
- Two relations remain open (UNCERTAIN-K0-0001 'Commit package.json and package-lock.json'; UNCERTAIN-K0-0002 'required by an approved workflow').
- Identifier numbering has gaps only where constraints were merged during annotation; IDs are local to this run.
