# 005 — Generate one candidate runtime template

## Goal

Generate a **complete, standalone runtime instruction template** for the single assigned candidate in this isolated workspace.

This iteration is **template generation only**. Do not generate TaskBoard or any other application code, do not run a benchmark, and do not compare candidates.

## Assigned candidate

Read `ASSIGNED_CANDIDATE.txt` first.

It must contain exactly one candidate ID:

- `M`
- `L0`
- `L1`
- `K0`
- `K1`

If the file is missing or contains anything else, stop and report the problem. Do not guess the candidate.

## Required inputs

Read the relevant inputs before constructing the template.

Shared inputs:

1. `research/observations/001-v3-design-proposal.md`
2. `research/observations/002-candidate-space-analysis.md`
3. `research/policy/inventory.json`
4. `research/candidates/<assigned>/CORE_FEATURES.md`
5. `research/candidates/<assigned>/DESIGN.md`
6. the complete `templates/v2-baseline/` tree

Additional inputs:

- for `L1`, read `research/candidates/L0/DESIGN.md` before `research/candidates/L1/DESIGN.md`;
- for `K1`, read `research/candidates/K0/DESIGN.md` before `research/candidates/K1/DESIGN.md`;
- for `L1` and `K1`, also read `research/capabilities/capability-framework.md`.

The workspace is intentionally allowlisted. Missing benchmark, metrics, other-candidate, TaskBoard, result, or oracle material is intentional.

Do **not** inspect files outside the workspace root. Do not use the network or external repositories to recover excluded material.

## Established E0 mechanics

You may rely on these established Iteration-004 facts:

- nested directories under `.claude/rules/` are discovered recursively to at least two levels;
- direct and nested `@` imports work;
- a rule file explicitly loaded through `@` is effectively always-loaded; a `paths:` field on that imported copy does not make it conditional.

Do not treat unresolved E0 probes as established facts. Do not redesign the candidate merely to make an unresolved mechanic look proven.

## Construction rules

1. **V2 is the behavioral baseline, not the target layout.**
   Preserve the accepted normative intent represented by `research/policy/inventory.json`.

2. **The inventory is the normative oracle.**
   Do not independently strengthen, weaken, add, or remove policy. Organizational rewrites and technology-neutral wording are allowed only where the assigned candidate design requires them.

3. **The assigned design controls structure.**
   Implement the candidate described by its `DESIGN.md`, `CORE_FEATURES.md`, and the shared invariants/predicates in Iteration 002. Do not drift toward another candidate because it seems cleaner.

4. **Illustrative trees are not literal file-generation scripts.**
   Use engineering judgment where the design explicitly leaves implementation freedom, but choose the smallest solution that satisfies the assigned candidate.

5. **One normative owner.**
   Avoid semantic duplication of policy. Pointers, routing text, summaries that contain no independent normative content, and deterministic checks are allowed where the design permits them.

6. **No research metadata in the runtime template.**
   The generated template must not contain candidate labels (`M`, `L0`, `L1`, `K0`, `K1`) as research labels, experiment commentary, metric definitions, benchmark material, policy-inventory IDs used only for research bookkeeping, or references to the research repository.

7. **No product implementation.**
   `SPECIFICATION.md` and other input placeholders may exist as template artifacts, but do not fill them with TaskBoard or another concrete application.

8. **Do not modify inputs.**
   Write only under `output/`.

9. **Fresh-output requirement.**
   `output/` must be empty or absent at the start. If it already contains a prior generated template or report, stop rather than overwrite or learn from it.

10. **No candidate comparison or winner selection.**
    Generate the assigned template only. Do not score it against V2 or other candidates.

11. **Do not commit or push.**

## Deliverables

Create:

### `output/template/`

A complete standalone template ready to be copied into a future code-generation workspace. It must include all runtime instruction/configuration/reference/enforcement artifacts required by the assigned candidate.

It must not require the research repository to function.

### `output/GENERATION_REPORT.md`

Keep this concise. Record:

- assigned candidate;
- total generated runtime file count;
- major structural choices where the design allowed more than one valid implementation;
- any candidate-design ambiguity and the minimal interpretation chosen;
- any policy-preservation concern or unresolved item;
- any intentionally permitted wording/placement delta that is important for later audit;
- whether the final self-check found any broken internal references or known missing required artifact.

Do not include a quality score or comparison with another candidate.

## Final self-check

Before finishing:

1. verify that `output/template/` is standalone and contains no research-only files;
2. check the output against the assigned candidate's distinguishing predicates and shared invariants;
3. check that accepted V2 policy intent from `inventory.json` has not been silently lost or materially changed;
4. check internal file references/imports for broken paths;
5. check for accidental normative duplication;
6. check that no concrete application code or benchmark material was generated;
7. correct clear construction defects you find;
8. leave unresolved design ambiguities documented in `GENERATION_REPORT.md` rather than silently inventing a new architecture.

If a genuinely required input is missing and the candidate cannot be generated without inventing research material, stop and report the missing input rather than fabricating it.