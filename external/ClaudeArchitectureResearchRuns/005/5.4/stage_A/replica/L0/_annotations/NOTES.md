# L0 Run-2 notes

## Sweep notes

Reverse checks conducted after all 12 batches, judged from L0's own text (no judgment carried over from K1, K0 or L1; only the classification method was reused):

1. **Keyword scan of all NON_NORMATIVE / IMPLEMENTATION / DUPLICATE spans** (`_tools/sweep.py`); every Markdown hit re-read in context. Imperative technique notes were recorded as NON_NORMATIVE orphans (EF Core bulk operations, 304/429/502 reference entries, Swagger launch profile and document partitioning, frontend/versioning/authorization test targeting, example numbers, image optimization, unsafe-deserialization and ClockSkew scan prompts, Result typed-error shape, review scoping). The dependency-removal suggestion in dependency-hygiene.md is marked '(prefer)', which the CLAUDE.md vocabulary defines as guidance, so it was not registered as EXTRA.
2. **Large-span review** (NN/IM/DU spans of 15+ lines): code samples, YAML/JSON examples, navigation tables of the instruction map, `.editorconfig` suggestion-level settings and hook registrations only.
3. **Script branch review**: `claude-hook.mjs` pre-bash (fails closed; blocks npm/pnpm/yarn force and legacy-peer flags including environment assignments, and every `dotnet add/remove … reference` / `dotnet reference add/remove`; does not gate package additions), post-bash (actual manifest state after successful and failed shell calls; per-worktree snapshot in the Git directory; routes dependency and reference changes; outside Git only after recognized dependency commands), post-edit (manifest checks, dependency/reference change routing against HEAD, product-input reminder, structure checker after instruction edits), stop (seed, migration review, tests, custom settings; repeated only on changed state; outside Git visible but non-blocking), `manifest-checks.mjs` (deny list, review list with exceptions read from '## Accepted' sections, CPM, versions, npm tooling category, `.npmrc` bypass, outward references), `check-instructions.mjs` (every predicate mapped to X3, X7, X25, X26 or R1/R2/R20).
4. **Branch findings recorded**: review-listed packages pass when their id appears anywhere in an 'Accepted' section (exception of R12–R15, X5); the reference gate blocks even approved or layout-mapped CLI reference commands (X1); the deny list has no approval path (X4).
5. **Config defaults**: settings.json (only PreToolUse fails closed), `.editorconfig` (IDE0005 warning; other settings suggestions), Directory.Build.props (net10.0; Nullable, ImplicitUsings and AnalysisLevel latest registered as EXTRA-L0-0030; EnforceCodeStyleInBuild/GenerateDocumentationFile implement RUN-010), Directory.Packages.props (CPM on, empty), `.gitignore` (local secrets ignored).
6. **Mixed clauses** split into oracle and extra parts (e.g. CLAUDE.md Reserved items 3 and 9, approval-and-recording line, git-workflow push and destructive operations, add-dependency resilience and report, development-workflow migrations and report, build-fix report, security-scan report shape).
7. **Notable L0-specific structure**: the level model (headers with Depends on, level directories, dependency direction and acyclicity, Level 0/1 technology neutrality, map completeness) and the placement/ownership rules are template-structure extras (X3, X6, X7, X25, X26); CLAUDE.md adds a normative vocabulary requiring deviations from defaults to be reported (X27) and an instruction-precedence rule (X29).

Classification rule (same method as for K1, K0 and L1): EXTRA when binding (must/never/do not/only, a named anti-pattern prohibition, or hook/checker-enforced), outcome-changing and not entailed by a stack-neutral reading of an oracle policy; technique classes excluded by the oracle (EXC-002..EXC-018) stay NON_NORMATIVE; workflow report-content mandates beyond WF-009 are EXTRA; statements the template itself marks as 'prefer/avoid' guidance are not registered as EXTRA.

## Limitations

- Structural PASS (validators 11/12/13) is not semantic proof.
- All 196 policies are MATCHED; tightened modalities and extra gates are noted in search_notes instead of downgrading status.
- Hooks and checkers were analyzed statically, not executed.
- Two relations remain open (UNCERTAIN-L0-0001 'commit package.json and package-lock.json'; UNCERTAIN-L0-0002 'clearly required by an approved workflow').
- CANDIDATE.md was read as provenance only; classifications rest on the template text.
- Identifier numbering has gaps where constraints were merged during annotation; IDs are local to this run.
