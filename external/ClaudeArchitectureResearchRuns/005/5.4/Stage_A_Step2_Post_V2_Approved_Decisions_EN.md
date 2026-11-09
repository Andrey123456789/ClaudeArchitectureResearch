# Experiment 005 — Stage A / Step 2: Approved Post-v2 Parity Decisions

**Decision date:** 2026-11-04  
**Authority:** Direct user approvals in the research conversation.  
**Predecessor:** `stage_A/reconciled/step2_controlled_repair_v2/` (immutable).  
**Purpose:** Record decisions for a future controlled correction task. **This document is not an execution authorization to mutate the frozen source, the v2 predecessor, or Codex's search area.**

## Historical provenance: Codex macro-pass 0001

Codex `pass_0001` has **already been reviewed by a separate Claude session** on 2026-11-02 and must not be submitted for a second initial review. The review lives at `stage_A/reconciled/step1_union_augmented_pass1/` and is documented by `REVIEW_REPORT.md`. It adjudicated 152 Codex claim IDs: 26 distinct-unrepresented clause proposals, 29 existing-group facets, 71 non-independent details, 25 already represented claims, and 1 unresolved case. Its results are **provisional proposals and facets, not automatically adopted common policies**.

Both `step2_controlled_repair_v1` and `step2_controlled_repair_v2` account for this augmented Pass 1 union. The v2 final report explicitly states: "This work uses the Pass 1 augmented union. Codex Pass 2 was neither read nor used." Therefore the next integration should target **new evidence from Pass 2 and Pass 3**, cross-checked against the Pass 1-augmented union and v2. Preserve provenance and avoid double counting.

## Approved correction D-PV2-01: Git mutating-command hook parity

**Current discrepancy:** Only K0 has a `PreToolUse` hook specifically classifying repository-mutating Git commands and returning a `permissionDecision: ask` response. The other five candidates rely on normative Git text without that enforcement mechanism.

**Decision:** Introduce equivalent Git command classification and approval gating for M, M1, L0, L1, and K1, **using the native hook architecture and integration conventions of each candidate**; do not wholesale transplant K0's dispatcher or change candidate design identities.

**Required semantics:**
- Do not gate read-only Git commands such as ordinary `git status`, `git diff`, and `git log` merely for being Git commands.
- Identify repository-mutating Git commands, including relevant common command wrappers, multi-command lines, and supported Git global options. Return `ask` at the hook level rather than unconditional `deny` for otherwise-authorizable Git mutations.
- The hook's `ask` is **not** proof of user authorization. Retain HQ-01 / GOV-015: the action and scope must have been explicitly requested or specifically preapproved by the user; generic workflow approval is not sufficient.
- Preserve the original rules for a dirty tree before a modifying task, headless execution without a standing choice, scoped commits, and specifically authorized rewriting of `main` (unless another rule prohibits it).
- Preserve all pre-existing dependency, project-reference, and peer-bypass guards. An existing `deny` must not turn into `ask` merely because a command also contains Git.

**Acceptance:** Compare the six actual PreToolUse outputs for an equivalent fixture matrix of read-only Git, committing, staging, checkout/reset, force-push, Git global options, shell wrappers, combined commands, and malformed inputs. Verify the common user-authorization policy and full cumulative regression.

## Approved correction D-PV2-02: Fail-closed PreToolUse input in M and M1

**Current discrepancy:** M's critical hook accepts an empty or missing `tool_input.command` by exiting successfully. M1 routes the absent command to its classifier, which can also allow it. M reports malformed/empty JSON with exit 1 and relies on host-level `onFailure: block`; this does not demonstrate direct script-level blocking.

**Decision:** For shell-command `PreToolUse` events, M and M1 must reject malformed JSON, wrong payload shapes, missing or empty `tool_input.command`, and other truly invalid event inputs with an explicit blocking outcome. Preserve permissive behavior for valid, non-mutating commands and do not incorrectly require a command on unrelated hook event types.

**Acceptance:** Cover valid JSON with missing/empty/wrong-type commands, empty stdin, malformed JSON, non-object JSON, mismatched event/tool names when applicable, and valid read-only commands; test direct-script exit/decision semantics and separately document live-host `onFailure` behavior as `NOT_RUN` unless actually observed. Full cumulative regression required.

## Approved correction D-PV2-03: Remove K0-only root placement prohibition for CPM

**Current discrepancy:** K0 `.claude/scripts/check-dependencies.cjs` rejects a repository with a `.csproj` unless `Directory.Packages.props` exists **at the repository root** (decision D-17), even if each project inherits an effective, correct central-package configuration from a nested location. The other five candidates do not impose this blanket placement rule.

**Decision:** Remove the **mandatory root-only constraint** in K0, synchronizing checker behavior and authoritative D-17/rule language while retaining central-package-management obligations and MSBuild-based effective-state verification for every project. Root-level configuration may remain a **typical layout example**, not a universal gating requirement.

**Acceptance:** Positive fixtures with nested `Directory.Packages.props` that correctly manage all projects; negative fixtures where a project lacks effective CPM, has overridden/disabled CPM, or has invalid package metadata; mixed multi-project layouts. Do not weaken unrelated pinned-version, exception, or dependency-policy checks. Full cumulative regression required.

## Approved correction D-PV2-04: Frontend-test placement parity in M

**Current discrepancy:** M does not explicitly prohibit frontend tests beneath `backend/`, whereas M1, L0, L1, K0, and K1 do.

**Decision:** Add the same explicit ban to M in the appropriate existing normative owner (and update any necessary mirrors, references or classification entries) without imposing any unrelated additional repository-layout constraints.

**Acceptance:** Check exact normative scope and modality against the five candidate peers, test positive and negative repository layouts, re-evaluate affected findings/strength records, and run cumulative regression.

## Required execution discipline and scope limitations

1. Apply **one logical correction at a time**, with an immutable prechange checkpoint and an auditable change log.
2. After **each** correction, verify the whole affected candidate architecture, all linked oracle and candidate-specific policies, cross-candidate parity for the affected behavior, and the cumulative regression suites for **all prior corrections** (v1, v2, and the new series).
3. On a failing gate, repair or roll back the **current** correction before advancing.
4. After all corrections, perform a separate cold final audit of the final six trees; do not equate witness presence with semantic equivalence. Report `NOT_RUN` honestly.
5. Keep `inputs/`, original candidate trees, all v1/v2 artifacts, and Codex search artifacts untouched. Create a new versioned output folder. Do not start Step 3 or benchmark generation in this correction task.
6. Preserve differences integral to M/M1/L0/L1/K0/K1 instruction-delivery architectures; standardize only the explicitly approved behavior. Record changes that could affect comparative enforcement/strictness metrics and do not overwrite previously reported v2 results.
7. Integrate Codex Pass 2 and Pass 3 findings separately when available, first deduplicating against the Pass 1-augmented union and the v2 final state. Do not treat hypotheses as approved corrections automatically.

## Source anchors

- `step2_controlled_repair_v2/FINAL_PARITY_AND_CONSISTENCY_REPORT.md`, section 4 (four reported differences) and section 8 (Pass 1 augmentation and open limits).
- K0: `candidates/K0/template/.claude/hooks/hook.cjs` and `.claude/settings.json` (Git PreToolUse); `.claude/scripts/check-dependencies.cjs` (root-only D-17 check).
- M: `candidates/M/template/.claude/hooks/dependency-guard.mjs`, `hook-io.mjs` and `.claude/skills/project-structure/references/solution-layout.md`.
- M1: `candidates/M1/template/.claude/hooks/pre-tool-use.js`.
- Codex Pass 1: `stage_A/reconciled/step1_union_augmented_pass1/REVIEW_REPORT.md`.
