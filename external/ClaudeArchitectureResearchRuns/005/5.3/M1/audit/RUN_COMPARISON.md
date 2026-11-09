# M1 Run-01 vs Run-02 — independent comparison

## 1. Architectural identity

Both runs are recognizably **M1 = Minimal Modular + exactly four replaceable capabilities**.

Common invariant design point:

- `architecture/clean-architecture` is the required frame;
- `persistence/ef-core` is a required leaf with `sqlserver` provider;
- `backend-testing/nunit` is a required leaf;
- `frontend/angular` is the optional leaf;
- static composition; no dynamic plugin discovery;
- flat M-style rule organization;
- contracts + module manifests + role/facet boundaries;
- no Stability-first `Level:` taxonomy;
- no Kinds × Scopes `Kind:` taxonomy;
- non-capability content remains V2/M lineage rather than being globally neutralized.

Therefore the two runs do **not** represent contradictory interpretations of M1.

## 2. Structural variance

The implementations are nevertheless much less reproducible than M was:

- Run-01: 77 files, 397,827 bytes, 65 Markdown files / 347,952 Markdown bytes, 28 skills, 14 rules.
- Run-02: 80 files, 368,816 bytes, 67 Markdown files / 303,524 Markdown bytes, 29 skills, 14 rules.
- Common paths: 63; union: 94; path Jaccard: **0.6702**.
- Only `SPECIFICATION.md` is byte-identical among common paths; the runs rewrite most shared artifacts substantially.

Important shape differences:

- R1: `architecture-style.md`, `backend-runtime.md`, `repository-structure.md`; R2: `architecture.md`, `composition.md`, `physical-structure.md`.
- R1: two hooks (`PostToolUse`, `Stop`); R2: three hooks including `PreToolUse`.
- R1: monolithic-ish script helper + dependency policy JSON; R2: common/dependency/hook-output libraries and manifest checker.
- R1: capability planning imports only architecture/frontend planning facets plus selection; R2: four explicit `docs/capabilities/<slot>.md` planning facets.
- R2 adds `persistence-change` workflow.

This variance is a **generatability finding**: M1 leaves substantial implementation freedom. It does not by itself justify a third run because the defining architecture is consistent.

## 3. Policy and V2 preservation

Generated reports claim full 196-item coverage, zero trigger-role deltas, and zero scope gaps. Independent lexical diagnostics were also run instead of trusting those reports blindly.

Policy-oracle TF-IDF best-match against generated Markdown is essentially tied:

- R1 mean ~0.491, median ~0.469;
- R2 mean ~0.489, median ~0.463.

That diagnostic does **not** show material normative loss in R2.

Literal V2 preservation strongly favors R1:

- exact unique baseline headings retained: R1 ~92.0%, R2 ~71.6%;
- exact unique code blocks retained: R1 ~79.3%, R2 ~42.5%;
- broad source-chunk lexical similarity also strongly favors R1.

These are not correctness scores: R2 often paraphrases/condenses the same content. They do, however, create a mandatory 5.3 check: inspect every baseline section/example that R2 compressed, and restore only useful technique, examples, or constraints that are actually missing.

## 4. Enforcement quality

### Run-01

Strengths:
- role-token capability decoupling is clean;
- generated checkers pass;
- Windows PowerShell BOM handling was explicitly repaired.

Weaknesses:
- no `PreToolUse`, so package/dependency routing occurs only after mutation;
- settings launch hooks with `node .claude/hooks/...`, which fails from nested cwd;
- active-worktree detection is wrong when `CLAUDE_PROJECT_DIR` points to the main checkout;
- manual checker commands are root-relative.

### Run-02

Strengths:
- `PreToolUse` dependency routing;
- stronger manifest and architecture post-checks;
- more systematic hook/checker libraries;
- root-independent script bootstrap through `CLAUDE_PROJECT_DIR` for ordinary nested cwd;
- generated checkers pass.

Weaknesses confirmed independently:
- repository checks still operate on the **main checkout**, not the active worktree, after Claude enters a worktree;
- npm/pnpm/yarn global options before the subcommand bypass the normal dependency-change classifier;
- `dotnet add/remove ... reference` is not routed before mutation;
- settings use a complex shell-form Node launcher rather than current Claude Code exec form;
- the instruction checker assumes the old launcher shape and must evolve with the fix;
- root-relative manual checker commands remain cwd-sensitive;
- Stop-hook dedup fingerprints only file names + messages, not the actual changed state.

## 5. Overall assessment

Expert audit score (not a frozen experimental metric):

| Dimension | R1 | R2 |
|---|---:|---:|
| Policy/V2 preservation | 9.4 | 9.2 |
| M1 identity fidelity | 9.3 | 9.4 |
| Replaceability purity | 9.4 | 8.9 |
| Deterministic enforcement | 6.7 | 8.0 |
| Maintainability/conciseness | 8.2 | 8.8 |
| Overall starting quality | **8.5** | **8.9** |

R2 is selected because its enforcement foundation and maintainability are stronger. Its weaknesses are concrete and repairable without changing M1's architecture.
