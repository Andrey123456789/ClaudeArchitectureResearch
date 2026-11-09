# M — 5.3 controlled refinement task

## 1. Goal

Produce a **demonstrably better** implementation of Candidate M than the selected 5.2 Run-02 baseline.

This is not a redesign exercise. It is a controlled defect-removal/refinement stage. Preserve M's architecture and all binding policy semantics while eliminating every confirmed defect in `audit/DEFECT_DOSSIER.md`.

A change is accepted only when it is demonstrably better than the baseline. Neutral, subjective, cosmetic, or regressive changes must be omitted or reverted.

## 2. Workspace and evidence

The current `5.3/M` directory is the complete refinement workspace.

Read completely before editing:

1. `CANDIDATE.md`;
2. `source/inventory.json`;
3. `source/shared-research-invariants.json`;
4. the complete `source/v2-baseline/` tree;
5. `baseline/TASK.md` as historical 5.2 acceptance context;
6. `baseline/GENERATION_REPORT.md` as evidence, not authority;
7. `audit/BASELINE_SELECTION.md`;
8. `audit/RUN_COMPARISON.md`;
9. `audit/DEFECT_DOSSIER.md`;
10. `audit/EXTERNAL_MECHANICS_NOTES.md`;
11. the complete `baseline/template/` tree.

Do not read parent/sibling candidate directories, 5.2, network resources, external repositories, or other research material. Everything needed for M refinement is supplied here.

`baseline/` and `source/` are immutable. Do not modify them.

Write only under `output/`.

## 3. Starting point

First create an exact working copy:

`baseline/template/` → `output/template/`

Then modify only `output/template/`.

The selected baseline is already strong. Prefer the smallest reliable patch set that fixes confirmed defects. Do not rewrite large portions merely to make them stylistically different.

## 4. Binding architecture identity

The result must remain Candidate M:

- recognizable V2 lineage;
- flat topical `.claude/rules/` organization;
- no Stability-first levels or `Level:` classification;
- no Kinds × Scopes taxonomy or `Kind:` classification;
- no capability slots, contracts, manifests, selection record, or formal replacement layer;
- no level/kind/capability rule trees;
- normal M decision model remains intact;
- workflow skill = procedure, knowledge skill = technique;
- private references remain private to their owning skill;
- every new artifact must have a concrete reliability purpose.

Do not solve a defect by turning M into L, K, M1, or another meta-architecture.

## 5. Binding policy preservation

Treat `source/inventory.json` and `source/shared-research-invariants.json` as policy oracles.

The refined template must preserve:

- exactly one normative owner for every applicable policy/invariant;
- **zero trigger-role deltas**;
- every minimum-scope requirement;
- policy strength and conditions (`must`, defaults, exceptions, approval gates, qualifiers);
- useful V2 technique and operational detail;
- explicit rule `paths`;
- critical must-rules outside purely on-demand material;
- acyclic instruction/reference dependencies;
- zero broken internal references;
- English-only technical/programming output;
- no research-only metadata in runtime artifacts.

Do not improve a hook by weakening or moving a policy.

## 6. Mandatory defect repairs

Every confirmed defect D1–D6 in `audit/DEFECT_DOSSIER.md` is binding and must be fixed.

In particular, the final implementation must:

1. use a current cross-platform **exec-form** hook launcher for project-installed Node hooks rather than CWD-dependent shell command strings;
2. use `${CLAUDE_PROJECT_DIR}` only to locate the installed hook script, not as the unquestioned active worktree/repository state root;
3. derive the active repo/worktree root from hook input `cwd` deterministically and use it for file/manifests/Git-state checks;
4. detect project-reference add/remove operations and validate architecture/project-reference constraints;
5. make npm dependency/force detection robust to global options such as `--prefix` and `--workspace`;
6. update `check-instructions.mjs` so the correct exec-form hook configuration passes while unsafe shell-dependent launchers fail;
7. make manual checker invocations reliable after directory changes by establishing the active repo/worktree root or using an equally robust cross-platform strategy.

Do not merely document these defects away. Implement and test the fixes.

## 7. Hook design requirements

Keep hook logic deterministic and bounded.

Separate:

- **launcher root** — stable path used to find the hook script itself;
- **active repository/worktree root** — state being inspected and modified during the current tool event.

Read hook JSON stdin before selecting the active repository root. Validate paths before operating on them. Do not silently skip a required check because a path falls outside the main checkout when the active cwd belongs to a valid worktree.

Avoid POSIX-only syntax. Windows PowerShell 5.1 BOM-prefixed stdin must remain accepted.

Do not build a general shell parser. Implement the minimum deterministic command parsing needed for supported dependency/project-reference commands and cover it with table-driven tests.

## 8. Required regression test matrix

Before promotion, test the actual generated files in an in-workspace sandbox. At minimum cover all twelve cases listed in `audit/DEFECT_DOSSIER.md`, including:

- root and nested cwd hook launch;
- worktree/active-cwd root selection;
- PowerShell BOM stdin;
- dotnet project-reference add/remove;
- npm `--prefix` + `--force` bypass attempt;
- npm `--workspace` + `--legacy-peer-deps` bypass attempt;
- active-worktree manifest/reference validation;
- static instruction-checker acceptance of safe exec form and rejection of unsafe launcher regressions.

Also rerun all existing generated checkers and candidate-specific structural checks.

Temporary test material belongs under `output/.work/` and must be removed before completion.

## 9. Optional improvements from Run-01

The optional ideas listed in the dossier are not requirements.

For each considered optional improvement, explicitly decide one of:

- `ADOPT` — concrete benefit proven and no meaningful regression;
- `REJECT` — not enough benefit, too noisy, too complex, or outside M's minimal philosophy;
- `DEFER` — evidence is insufficient and adding it would violate the promotion rule.

Do not adopt an optional feature merely to combine both runs.

## 10. Promotion gate — STRICTLY_BETTER

The refined result may be approved only if **all** of the following hold:

1. every D1–D6 confirmed defect is fixed;
2. all original 5.2 acceptance gates still pass;
3. zero new policy/scope/trigger regressions;
4. zero broken internal references;
5. Candidate M identity is unchanged;
6. Windows and worktree behavior is demonstrably stronger than baseline;
7. no known bypass remains in the dependency/project-reference command cases tested;
8. no new accidental semantic duplication;
9. useful V2 content is not lost;
10. always-loaded context is no worse without a concrete reliability justification; the rough target remains ~5k tokens;
11. file/layer/metadata complexity does not increase without a concrete reliability purpose;
12. every changed file has a documented reason tied to a defect or an approved net-positive optional improvement.

A tie is **not** an improvement. Cosmetic churn is **not** an improvement. “Cleaner” without measurable benefit is **not** an improvement.

If a proposed change fails this gate, revert that change and retain the baseline behavior instead.

## 11. Audit protocol

After the first repaired implementation is complete:

1. run a primary substantive audit against the actual `output/template/`;
2. repair every concrete binding defect found;
3. run a complete confirmation audit;
4. if the confirmation audit finds a concrete template defect, repair and repeat confirmation;
5. once confirmation finds zero concrete defects, stop additional audit cycles.

Do not reopen the audit merely for stronger narrative evidence, repeated hashing, independent verification of verification, or session-log archaeology.

## 12. Required report

Write `output/REFINEMENT_REPORT.md` containing:

- selected baseline: `M/Run-02`;
- final status: `STRICTLY_BETTER` or `NOT_PROMOTED`;
- complete list of changed files and why each changed;
- D1–D6 repair evidence;
- regression-test matrix and results;
- policy owner/trigger/scope audit result;
- broken-reference count;
- Windows/worktree hook result;
- always-loaded context estimate before and after;
- runtime file count before and after;
- optional Run-01 ideas: ADOPT/REJECT/DEFER with rationale;
- any rejected/reverted proposed changes and why;
- confirmation-audit result.

If every confirmed defect cannot be fixed without a regression, do not fake PASS. Preserve the best non-regressive baseline behavior and report `NOT_PROMOTED` with the exact blocker.

## 13. Completion condition

Success requires both:

- all confirmed defects are eliminated; and
- the resulting template passes the promotion gate as **STRICTLY_BETTER** than the immutable baseline.

When this is established, remove `output/.work/`, ensure `output/` contains only `template/` and `REFINEMENT_REPORT.md`, and stop.
