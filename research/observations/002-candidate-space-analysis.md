# 002 — Candidate Architecture Space: Definitions and Cross-Candidate Analysis

| | |
|---|---|
| Status | Draft for human review. Design only. No template files were changed. |
| Date | 2026-10-02 |
| Produced by | `prompts/002-candidate-design-goal.md` |
| Inputs | `research/hypothesis.md`, `research/requirements.md`, `prompts/001-v3-design-goal.md`, `research/observations/001-v3-design-proposal.md`, `templates/v2-baseline/` (re-checked for every V2 claim used here) |
| Companion files | `research/candidates/{V2,M,L0,L1,K0,K1}/CORE_FEATURES.md` (research passports), `research/candidates/{M,L0,L1,K0,K1}/DESIGN.md` (design notes) |
| State of templates | `templates/v2-baseline/` and `templates/v3/` unchanged. `templates/v3/` is still byte-identical to V2 (checked with `diff -rq`). |
| Next step | Human review → answer §13 → run the pre-generation tests in §14 → build the V2 policy inventory and content pool → generate candidates |

---

## 0. Conventions

- **Candidate IDs** are fixed: `V2`, `M`, `L0`, `L1`, `K0`, `K1`. Every research artifact uses them.
- **Shared invariants** `S-01`…`S-19` are defined in §2. DESIGN and CORE_FEATURES files cite them by ID and do not restate them.
- **Structural predicates** `P-01`…`P-14` (§3.4) are the tests that decide which candidate an implementation actually is.
- **Evidence labels** are the same as in 001. **Observed**: read in a V2 file. **Expected**: a prediction. **Needs test**: plausible but must be measured before anything relies on it.
- **V2 paths** follow 001 §0.1: relative to `templates/v2-baseline/`, with the `.claude/` prefix left out for rules, skills and agents.
- **Policy inventory item**: one normative statement from V2, with a stable ID. The inventory does not exist yet (§13 Q1).
- **Content pool**: the deduplicated text fragments (policy, technique, procedure) that every experimental candidate is built from (S-01).
- **Runtime layout** means the files Claude Code sees in a project copy. **Authoring layout** means how maintainers organize the source. In this document they are the same unless stated otherwise.
- **Kind codes.** 001 named its kinds K1–K7. Those labels now clash with candidate `K1`, so this document and the K0/K1 designs use letter codes instead: `OP` operating policy, `DEC` project decisions, `STD` standards, `KNW` knowledge, `WF` workflows, `ENF` enforcement, `IN` product inputs.

**Relationship to 001.** The Kinds × Scopes proposal from 001 is now candidate K0. But many of 001's recommendations have nothing to do with Kinds × Scopes:

- the decision-control protocol;
- decisions loaded at planning time;
- keeping policy out of model-invoked skills;
- the enforcement package;
- the reference forms;
- the instruction map.

§2 makes these **shared invariants**, so they cannot become a hidden advantage of K0. What remains distinctive about K0 is its organization: kinds and scopes as the primary axes.

---

## 1. Executive summary

**The space.** Two axes, plus two reference points.

| | Embedded capabilities (B0) | Replaceable capability modules (B1) |
|---|---|---|
| No new meta-architecture (V2 lineage) | **M** | — (no candidate; see §3.6) |
| Stability-first (A-L) | **L0** | **L1** |
| Kinds × Scopes (A-K) | **K0** | **K1** |
| Frozen control (no shared invariants) | **V2** | — |

**Findings that shape the experiment**

1. **The shared bundle is deliberately large.** Most behavior-relevant fixes from 001 are not properties of any meta-architecture, so every experimental candidate gets them (S-01…S-19). That makes the comparison fair, but it also means:
2. **Behavioral differences among M, L0, L1, K0 and K1 are expected to be small** compared with their shared gain over V2 (Expected). The candidates differ mainly in where content lives and how it changes. The behavioral benchmark from 001 §11.3 alone cannot tell them apart. **A change-impact suite of maintainer tasks is needed** (§5.3). Without it, L1 and K1 would only be measured on their overhead, never on their benefit.
3. **Each candidate is defined by testable structural predicates** (§3.4), not only by prose. A script or a reviewer can then tell whether an implementation leaked a feature of another candidate.
4. **Recommended construction order**, for confound control (§13 Q2):
   1. V2 policy inventory;
   2. shared content pool;
   3. M;
   4. L0 and K0, by re-placing the same fragments;
   5. L1 and K1, by applying one *capability transformation* to L0 and K0, restricted to the agreed slot set.

   After each step, any difference that is not on a logged list of permitted deltas is accidental.
5. **Capability boundaries** (§7):
   - Strong candidates: backend testing (NUnit) and persistence (EF Core).
   - Architecture (Clean Architecture) is a *frame*, not a leaf. It is questionable as a plug-in, but it is the most informative stress test, so it is included.
   - Frontend (Angular) is questionable: removal is realistic, replacement is not (React is a non-goal).
   - Weak candidates: logging/Serilog, validation, mapping, API docs, and the database as a standalone capability. The database is better modelled as a provider variant of persistence.
   - **L1 and K1 must use the same slot set, contract format and composition mechanism.**
6. **Main confounders** (§6):
   - V2 vs M bundles two factors: the enforcement package and the instruction cleanup.
   - Skill and file naming.
   - Drift of the content between candidates.
   - The composition mechanism in L1 and K1.
   - Whether a replacement implementation is available in advance.
   - Generation sessions of uneven quality.
7. **Convergence is expected** (§12). Claude Code's mechanisms constrain the physical layout: one `CLAUDE.md`, path-scoped rules, and a flat skill namespace. Several candidates will therefore produce very similar runtime files. Convergence should be recorded as a result, not hidden by forcing artificial differences, which would itself be a confound.
8. **Predictions, not a selection** (details in §8–§11):

   | Metric family | Expected order (best first) |
   |---|---|
   | Behavioral metrics on ordinary tasks | M ≈ K0 ≈ L0 ≥ K1 ≈ L1 ≫ V2 |
   | Leaf replacement blast radius | L1 ≈ K1 > L0 > K0 ≈ M > V2 |
   | Frame replacement blast radius (CA → VSA) | L1 ≈ K1 > L0 ≈ K0 ≈ M > V2, with smaller gaps than for leaves |
   | "Where does this rule live, and when does it load?" | K0 > K1 ≈ L0 > L1 ≈ M > V2 |
   | Structural complexity (least first) | V2 < M < L0 ≈ K0 < L1 < K1 |

   Interaction hypothesis: capabilities add more to Kinds × Scopes than to Stability-first, because K0 spreads each technology across kinds while L0 already groups it at the Technology level: (K1 − K0) > (L1 − L0) on replacement metrics.

No candidate is eliminated and no winner is selected.

---

## 2. Shared invariants

### 2.1 The listed principles: shared or distinguishing?

Every principle the prompt lists is shared by M, L0, L1, K0 and K1. None of them may be used as an argument for one candidate over another. For each principle, the table shows what is identical everywhere and what may legitimately differ.

| Principle | Invariants | Identical in every experimental candidate | May differ (by candidate definition only) |
|---|---|---|---|
| Modularity | S-04, S-12 | No file mixes responsibilities. No split produces two files with the same trigger, the same owner role and the same change driver. No micro-files. | The *primary criterion* for drawing module boundaries: V2 lineage (M), stability level (L), kind × scope (K), and also capability (L1, K1). |
| Single source of truth | S-01, S-02 | One owner per inventory item. The same allowed reference forms. Restatement is forbidden. | Which file is the owner. |
| Explicit ownership | S-03 | Every instruction file starts with a one-line classification header, and the owner of every inventory item is recorded. | The header fields (none, level, kind and scope, capability) and the rule that assigns owners. |
| Separation of concerns | S-04 | Policy, procedure, technique, product inputs and enforcement are never mixed in one artifact beyond pointers and check-by-reference. | Whether this separation is a declared classification (K) or only a writing rule (M, L). |
| Stable dependency direction | S-05 | Normative content depends only on owners that load reliably. Engineering policy never depends on product or task inputs. Skill-private references stay private. Conformance dependencies are acyclic. | L adds a strict, ordered level rule. K adds a kind dependency graph. B1 adds contract direction. |
| Selective loading | S-09, S-18 | The same mechanism catalog, the same trigger class for every inventory item, and the same ceiling on always-loaded context. | Path granularity *within* a scope, and how many files load per trigger. These are measured outcomes, not things to equalize. |
| Reliable triggering | S-07, S-09, S-11 | No must-rule is carried only by a model-invoked skill. Decisions are present at planning time. Co-change obligations are hooked. Workflows contain explicit read steps. | Nothing. Trigger reliability is an outcome to measure, not a design choice. |
| No silent overrides | S-06, S-08 | Identical precedence order, decision classes, reserved classes, classification test, Decision Request format and headless behavior. | Which file holds them (always loaded in every candidate). |
| Human-readable structure | S-14, S-15 | A map of the instruction system that is never loaded and has the same fields everywhere. The same normative vocabulary. | How the map is organized (by file, by level, by kind × scope, by capability). |
| Backend / frontend / testing scope | S-10 | The same scope taxonomy, path globs and minimum path coverage. Every candidate has a path-scoped Angular rule. | Whether scope is a primary directory axis (K) or is expressed only through `paths` and file names (M, L). |
| Measurable behavior | S-13, S-14, S-17 | The same trigger suite, benchmark, metrics and failure taxonomy. Stable, unique file names that show up in transcripts. | Nothing. |
| Deterministic enforcement | S-13 | The same permissions, hooks, scripts, configuration assets and scaffold assets. | Hook messages name the owning file, which differs by candidate. Each candidate's instruction-structure checker verifies its own structural predicates. |
| Preservation of useful V2 behavior | S-01 | Inventory mapping is complete. Removals and rewordings are decided once, for all candidates. | Nothing. |
| Claude challenges questionable decisions | S-16 | Identical operating-policy text. | Nothing. |

### 2.2 Catalogue of shared invariants

These hold for **M, L0, L1, K0 and K1**. V2 holds none of them by construction (§2.4).

| ID | Invariant | Identical across candidates | May vary |
|---|---|---|---|
| **S-01** | **Content equivalence.** All experimental candidates are built from one V2 policy inventory and one shared content pool. Every inventory item maps to exactly one owner, or to an explicit removal. Removals, rewordings and new policy are decided once and applied to every candidate. Each candidate keeps a **permitted-delta log** for wording its architecture forces, for example technology-neutral wording at L's lower levels, or slot references in B1. | The policy fragments, the decisions about them, and the removals | Placement, file boundaries, glue text, logged deltas |
| **S-02** | **Single source of truth with fixed reference forms**, as defined in 001 §5.1. An *owner statement* appears exactly once. A *routing pointer* ("run `verify`", "see X") is allowed anywhere. A *check-by-reference* (a one-line yes/no check plus the owner's path) is allowed in workflows and review criteria only. A *decision summary* is allowed only in the candidate's decision-summary artifacts. *Restatement* is forbidden. | The definitions | The owner chosen |
| **S-03** | **Ownership header.** Every instruction file begins with a one-line classification header, for example `Owner: … · Scope: … · Loaded: …`. The map records the owner of every inventory item. | That a header exists, and the field `Loaded:` | Extra fields: `Level:` (L), `Kind:` (K), `Capability:` (B1) |
| **S-04** | **Minimum separation of concerns.** No artifact mixes normative policy, multi-step procedure, technique and examples, product input, or deterministic enforcement, except through S-02 pointers and checks. Workflow skills and knowledge skills are separate artifacts. | The rule | Grouping of the separated artifacts |
| **S-05** | **Minimum stable dependency direction.** (a) Normative content depends only on owners that load reliably (always or by path). (b) Engineering policy never depends on product, feature or task inputs. (c) Feature and task inputs may request a decision change but never override one. (d) A skill-private reference is depended on only by its own skill. (e) The graph of *conformance dependencies* ("A must comply with B") is acyclic. *Routing pointers* are not dependencies and may point in any direction, provided the target is reliably invocable. | The rule, and the distinction between conformance dependency and routing pointer | Stricter, candidate-specific direction rules |
| **S-06** | **Decision control and precedence.** The content is identical everywhere: the precedence order (001 §4.6); the Decided / Delegated / Reserved classes; the reserved classes R-1…R-10; the five-question test; the Decision Request format; an explicit instruction counts as approval and is recorded; headless runs choose the compliant option and report. Always loaded. | The text | The file it lives in |
| **S-07** | **Decisions available at planning time.** The adopted architecture, the patterns that are not adopted, the approved stack and the conditional technologies are always loaded, with identical content. The decision IDs (D-xx, seeded from 001 §9.3) and reserved-class IDs (R-x) are the same in every candidate. ADRs live at `docs/decisions/`. | Content, IDs, ADR path | One file or several, and where they are |
| **S-08** | **Product governance and product inputs.** Identical text for spec authority, no invented observable behavior, string-comparison semantics, and the `CUSTOM_SETTINGS.md` protocol. `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, optional feature specs and task prompts are **inputs, never instruction layers**. | The text | The file it lives in |
| **S-09** | **Trigger assignment.** Every inventory item gets the same *trigger class* in every candidate: always, path (scope X), hook, explicit workflow step, or on-demand knowledge. No must-rule is carried only by a model-invoked skill or a skill reference. Always-loaded content is reachable from `CLAUDE.md` through explicit `@` imports, and every rule file declares `paths`. | The trigger class of each item | Path granularity within a scope; the number of files per trigger |
| **S-10** | **Scope taxonomy and path conventions.** Scopes are `common`, `backend`, `backend-tests`, `frontend`, `delivery` and `repo/meta`. The glob conventions are identical and rely on `backend/<Name>.<Layer>/…` and `frontend/<Name>.Web/…`. An item applies at least wherever its scope says it does. Every candidate has a path-scoped Angular rule. | The taxonomy, the globs, minimum coverage | Whether scope is a directory axis |
| **S-11** | **Workflow and agent set.** `verify`, `code-review`, `build-fix`, scaffolding, `add-dependency`, settings change, `architecture-decision`, `security-scan`, `git-workflow`, and an optional `template-maintenance` that only the user can invoke. A thin `code-reviewer` agent preloads `code-review`. Steps, stop conditions and output formats are identical. | The set and the procedures | References inside steps; B1 may refer to capability facets |
| **S-12** | **Knowledge content and skill naming.** One shared pool of technique text. The same description rules (trigger first, about 250 characters at most, concrete cues). **Identical skill names for identical content.** Names change only through a central rename (§13 Q8). | The text, the description cues, the names | How knowledge is split, where the primary axis forces it, recorded as a delta |
| **S-13** | **Enforcement package "E".** Identical `.claude/settings.json` permissions; hooks H1–H4 with identical detection logic; the check script S1; root assets (`.editorconfig`, `Directory.Build.props`, `Directory.Packages.props`); scaffold assets, including the architecture check. Hook messages differ only in the owner path they name. Each candidate gets an instruction-structure checker (S2) with the same check categories, applied to its own predicates. | Mechanisms, detection logic, strength | Owner paths in messages; the structure rules S2 checks |
| **S-14** | **Human-facing instruction map**, never loaded. Fields: file, owner, scope, loading, enforcement, extension guide, plus the candidate-specific classification fields. | The fields | How it is organized |
| **S-15** | **Normative vocabulary**: *must / must not*, *default*, *prefer / avoid*, *requires approval*, with the definitions from 001 §5.4. | The definitions | — |
| **S-16** | **Challenge obligation.** Identical operating-policy text. Claude names concerns (duplication, cohesion, triggering, context, conflicts, complexity) and proposes alternatives before implementing a questionable request. | The text | — |
| **S-17** | **Execution parity.** No candidate encodes model IDs or effort levels. Benchmarks pin the Claude Code version, model, effort and permission mode. Agents have identical tool restrictions. | All of these | — |
| **S-18** | **Ceiling on always-loaded context.** One budget for every candidate. The proposed starting point is about 5k tokens including the skill listing (calibrate in §14 E8). Actual usage below the ceiling is measured, not equalized. | The ceiling | The actual usage |
| **S-19** | **Research metadata stays out of runtime.** `research/**`, including CORE_FEATURES and DESIGN, is never copied into a benchmark project. Benchmarks run with a copy of the candidate as the project root (see 001 §12, nested discovery). | Protocol | — |

### 2.3 What is deliberately not shared

These are the only legitimate sources of difference between experimental candidates:

1. **The primary decomposition criterion** (Axis A): V2 lineage, stability level, or kind × scope.
2. **Composition of capabilities** (Axis B): embedded, or replaceable modules with contracts, a selection record and static composition.
3. What follows from 1–2:
   - directory structure;
   - file boundaries;
   - rules for assigning owners;
   - dependency rules beyond S-05;
   - classification metadata;
   - the rules the structure checker enforces;
   - how the map is organized;
   - wording deltas the architecture forces, each logged per S-01.

Any other difference is a defect of the implementation. §6 lists how such defects typically arise.

### 2.4 V2's position

V2 is frozen. It has no policy inventory, no decision-control protocol, no hooks or permissions, and no instruction map. It loads no architecture policy at planning time. Some of its policy lives only in model-invoked skills (001 §3, §6.3). Comparing V2 with any experimental candidate therefore measures **the shared bundle plus that candidate's organization**. §5 and §6 explain how to separate these.

---

## 3. The two experimental axes

### 3.1 Axis A: primary decomposition model

| Value | Candidates | Defining property | Rule that assigns an owner |
|---|---|---|---|
| **A-M: no meta-architecture** (V2 lineage) | M | The V2 mental model and file topology are kept. Every change is a *local* refactoring justified by a specific defect or invariant. | "Where did V2 put this?", then fix only the documented defect. |
| **A-L: stability-first** | L0, L1 | Every artifact has a **level** in a totally ordered hierarchy: **Core → Architecture → Technology → Project**. Inputs sit outside the hierarchy. An artifact may conform only to its own level or more stable ones. Levels below Technology name no technology except the fixed platform. | "How fundamental and stable is this statement?", and then the most volatile thing it depends on. |
| **A-K: Kinds × Scopes** | K0, K1 | Every artifact has exactly one **kind** (OP, DEC, STD, KNW, WF, ENF, IN) and one **scope** (S-10). The kind fixes the mechanism and the allowed content. The directory structure follows kind, then scope. | "What responsibility does this statement have, and where does it apply?" |

The levels are not fixed by the prompt. The L designs use four levels plus inputs (L0 DESIGN §1). The kind list follows 001 §4.3 with the letter codes from §0.

### 3.2 Axis B: capability composition model

| Value | Candidates | Defining property |
|---|---|---|
| **B0: embedded** | M, L0, K0 | Important choices (Clean Architecture, EF Core, NUnit, Angular, SQL Server, Serilog) may be well modularized, but no generic mechanism governs them. Any artifact may name them where the Axis A rules allow. Replacing one means coordinated edits wherever it is named. |
| **B1: replaceable modules** | L1, K1 | Choices in the agreed slot set (§7.5) are **implementations of slots**. Each slot has a **contract**. Each implementation is a **module** that owns all of its implementation-specific facets. A **selection record** names one implementation per slot. Composition is **static**. **Outside its module, nothing names the implementation.** Everything outside the slot set stays embedded. |

**Vocabulary for B1**, shared by L1 and K1:

| Term | Meaning in this instruction system |
|---|---|
| Slot | A named, independently replaceable concern, e.g. `backend-testing`. |
| Contract | A maintainer-facing Markdown document per slot (§3.5). It is not loaded at runtime. |
| Implementation | A concrete choice for a slot, e.g. `backend-testing/nunit`. |
| Facet | One artifact an implementation supplies, of a kind or level the contract requires: a must-rule, knowledge, workflow steps, scaffold assets, an enforcement fragment, or a decision summary. |
| Module manifest | The list of runtime files an implementation owns. |
| Selection record | The always-loaded statement "slot → implementation". It is part of the decision summary (S-07). |
| Frame / leaf | A frame slot defines vocabulary that other slots are written in (architecture). A leaf slot does not (backend-testing). |
| Binding | Content that is specific to two slots at once, e.g. EF Core inside Clean Architecture (§7.4). |
| Leak | An implementation name that appears outside its module and outside the allow-list (the selection record and the decision summary). |
| Conformance | Required facets exist, metadata is present, no leaks, and the module's trigger tests pass. |

### 3.3 Capability contracts in a Markdown / Claude Code system

No compiler checks a Markdown contract. A contract is therefore three things together: **a document**, **a structural check** and **a behavioral check**. The format is identical in L1 and K1.

```text
# Contract: <slot>
Purpose            one paragraph: what is replaceable, and why it is a slot (§7 criteria)
Kind of slot       frame | leaf;  required | optional
Required facets    for each facet: role, the trigger class it must have (S-09), the vocabulary it must cover
                   e.g. backend-testing:  conventions (must-rule, path: backend-tests) · technique (knowledge)
                        · commands (consumed by verify and build-fix) · scaffold assets · architecture-check adapter
Optional facets    e.g. enforcement fragment (package deny-list entries), delivery fragment
Stable vocabulary  names other artifacts may use: the slot name, facet roles and, for frames, role names
Independent policy pointers to where the implementation-independent policy of this concern lives
                   (e.g. test levels, probe-to-test, determinism). The contract never restates it.
Requires / binds   other slots this one depends on, and which side owns each binding (§7.4)
Must not           override Core or OP policy; introduce Reserved decisions; name another implementation;
                   hide product-behavior consequences (§7.6)
Declared properties facts every implementation must state explicitly
                   (e.g. persistence: default string-comparison semantics; migration mechanism)
Conformance        what the S2 checker verifies; which trigger tests must pass
Replacement steps  ADR → select → compose → S2 → trigger tests → behavioral smoke task
```

Contracts are **not loaded at runtime**. What Claude needs at runtime is:

- the implementation-independent policy, placed by the primary axis;
- the selected implementation's facets;
- the selection record.

Claude reads a contract only during template maintenance, through the `template-maintenance` workflow.

### 3.4 Structural predicates: how to tell the candidates apart

These are the conformance tests that decide which candidate an implementation is. A "yes" in a column that should say "no" means **the implementation leaked a feature from another candidate**. Each candidate's S2 checker implements its own column, together with the shared invariants.

| # | Predicate | V2 | M | L0 | L1 | K0 | K1 |
|---|---|---|---|---|---|---|---|
| P-01 | Every artifact declares a stability level, and the levels are totally ordered | no | no | yes | yes | no | no |
| P-02 | Conformance dependencies point only to the same or a more stable level (checked) | no | no | yes | yes | no | no |
| P-03 | Core and Architecture name no technology beyond the platform (.NET / C#, TypeScript) | no | no | yes | yes | no | no |
| P-04 | Every artifact declares exactly one kind and one scope, and the kind fixes the mechanism | no | no | no | no | yes | yes |
| P-05 | Runtime rule directories are organized kind first, then scope | no | no | no | no | yes | yes |
| P-06 | A single decision-summary artifact holds every always-loaded decision | no | no (two V2-lineage files) | no (summaries per level) | no (per level) | yes (register) | yes (register) |
| P-07 | Every file traces to a V2 file (same, split or merged), or carries the defect or S-ID that justifies it | trivially | yes | no | no | no | no |
| P-08 | Shared invariants S-01…S-19 hold | no | yes | yes | yes | yes | yes |
| P-09 | A contract exists for every slot in the agreed slot set | no | no | no | yes | no | yes |
| P-10 | Implementation-specific artifacts declare `Capability:` ownership and are listed in a module manifest | no | no | no | yes | no | yes |
| P-11 | Leak check: outside its module and the allow-list, no artifact names a slot implementation | n/a | n/a | n/a | yes | n/a | yes |
| P-12 | An always-loaded selection record names one implementation per required slot | no | no | no | yes | no | yes |
| P-13 | Workflows reach technology steps through slot facets rather than concrete commands | no | no | no | yes | no | yes |
| P-14 | Content outside the slot set is placed exactly as in its B0 sibling | — | — | — | = L0 | — | = K0 |

P-14 is the key control for the B-axis comparisons. **L1 is L0 plus the capability transformation applied to the slot set, and nothing else.** The same holds for K1 and K0.

### 3.5 Selection and composition (no file format committed yet)

**Semantics.** These are required in L1 and K1, and identical in both.

1. A required slot has exactly one implementation selected. An optional slot has zero or one (for example `frontend`).
2. The selection is a project decision. Changing it is Reserved (R-1 / R-6). It is recorded once, in the selection record, which is part of the always-loaded decision summary (S-07).
3. **Composition is static.** Unselected implementations contribute nothing to runtime context: no rules, no skill descriptions, no hook fragments. Selecting at runtime among several shipped implementations is ruled out. It would put skill descriptions for the wrong implementation into the listing, and Claude could load the wrong module.
4. Composition can be verified. S2 confirms that the runtime file set equals the core files plus the facets of the selected implementations, that declared `requires` relations are satisfied, and that the leak check passes.
5. A missing required facet is a conformance failure, never a silent gap. A missing *declared property* (§7.6) turns into a Decision Request.

**Physical strategies.** The choice is deferred to §13 Q5.

| Strategy | Description | For | Against |
|---|---|---|---|
| CS-1: in-place | The selected module's facets live directly in the runtime locations (`.claude/rules/…`, `.claude/skills/…`). A manifest at `.claude/capabilities/<slot>/<impl>/MODULE.md` lists them. Replacing means removing the listed files and adding the new module's files. | No generator. Runtime files are the source. | The module is only logical: its files are scattered across rules and skills, because Claude Code fixes where they live. |
| CS-2: library plus compose script | Modules live together at `.claude/capabilities/<slot>/<impl>/…`. A script installs the selected facets into runtime locations and marks them "generated". | Modules are physically cohesive for maintainers. | Two copies of each text (source and generated) need a drift check. The tooling adds complexity. |
| CS-3: library plus documented manual install | Like CS-2, but a person or Claude follows the replacement steps. | No tooling. | Error-prone. The result of a replacement depends on the operator. |

**Facet naming rule (B1).** Facet files are named by **slot and facet role**, not by implementation. For example, `rules/backend-tests/test-framework.md` is owned by `backend-testing/nunit`. References from outside therefore survive a replacement. The implementation identity is recorded in the header, the module manifest and the selection record.

The exception is knowledge skills. Their *descriptions* must contain concrete trigger cues ("NUnit", "[TestCase]"), because trigger quality depends on them. The description belongs to the module's facet. The skill *name* stays concern-based (S-12).

### 3.6 Factor design, missing cells and optional ablations

The four cells L0, L1, K0 and K1 form a full 2 × 2 design. Main effects of A and B, and their interaction, can be estimated from them.

M and V2 are reference points outside the 2 × 2:

- **There is no "M1"** (V2 lineage with replaceable capabilities). So the experiment cannot tell whether capabilities need a meta-architecture to pay off. That is acceptable for this iteration, and is noted as an open question.
- **V2 vs M confounds two sub-factors**: the enforcement package E (S-13), and the instruction cleanup (everything else). Optional ablation: run **M−E** (M without the E package), or **V2+E**. This adds a variant without removing any of the six (§13 Q4).

---

## 4. Candidate comparison matrix

| Property | V2 | M | L0 | L1 | K0 | K1 |
|---|---|---|---|---|---|---|
| Axis A | — (ad hoc, organized by topic) | A-M (V2 lineage) | A-L | A-L | A-K | A-K |
| Axis B | embedded | B0 | B0 | B1 | B0 | B1 |
| Shared invariants | none | S-01…S-19 | S-01…S-19 | S-01…S-19 | S-01…S-19 | S-01…S-19 |
| Primary runtime directory axis | topic files | topic files (V2 names) | `rules/<level>/` | `rules/<level>/`, plus facets placed at the level of their slot | `rules/<scope>/`, kind by mechanism | as K0, plus facets placed by kind and scope |
| Owner-assignment rule | none | V2 location, corrected per defect | stability level, then topic | as L0; slot content goes to the implementation module | kind, then scope, then topic | as K0; slot content goes to the implementation module |
| Dependency rule beyond S-05 | none | none | level order (P-02); lower levels are technology-neutral (P-03) | as L0, plus: leaves bind only to contract vocabulary | kind graph `WF→KNW→STD→DEC→OP` | as K0, plus: leaves bind only to contract vocabulary |
| Where always-loaded decisions live | `CLAUDE.md` core defaults only; the stack is in a skill reference | `CLAUDE.md` (architecture defaults, the gate, patterns not adopted) plus `docs/technology-stack.md` (imported) | Architecture-level overview, plus Project-level decisions (both imported) | as L0, plus the selection record inside the Project decisions | `docs/architecture/decision-register.md` (imported) | the register, with a slot-selection section |
| Where technology-specific must-rules live | rules and skills | topic rules (`testing.md`, `persistence.md`, …) | `rules/2-technology/<tech>.md` | embedded technologies: as L0; slot technologies: module facets at level 1 or 2 | `rules/<scope>/<topic>.md`, mixed with the technology-neutral rules of the same topic | embedded: as K0; slot: facet files in `rules/<scope>/` |
| How workflows name technologies | concretely | concretely | concretely; each workflow sits at the level of its most volatile content | slot facets (P-13) | concretely | slot facets (P-13) |
| Contracts and selection record | — | — | — | yes | — | yes |
| Classification metadata per file | `paths` / `name` / `description` | header (owner, scope, loaded) | header + `Level` | header + `Level` + `Capability` | header + `Kind` + `Scope` | header + `Kind` + `Scope` + `Capability` |
| Runtime instruction files (Expected) | 41 | about 45–50 | about 55–65 | about 60–75, plus contracts and manifests | about 50–55 | about 65–80, plus contracts and manifests |
| One-line distinguishing predicate | frozen V2 | P-07 | P-01 to P-03, no P-09 | P-01 to P-03 and P-09 to P-13 | P-04 to P-06, no P-09 | P-04 to P-06 and P-09 to P-13 |

### 4.1 Trace: where NUnit-related content lives

Observed in V2: the word NUnit appears in 4 files (`rules/testing.md`, `skills/testing`, `skills/project-structure`, `references/technology-stack.md`). NUnit syntax appears in the examples in `skills/testing` (`[TestFixture]`, `[TestCase]`, `[OneTimeSetUp]`, `Assert.That`).

| Candidate | Decision | Framework-specific must-rules | Framework-neutral test policy | Technique | Scaffolding | Architecture check |
|---|---|---|---|---|---|---|
| V2 | `technology-stack.md` (skill reference) | `rules/testing.md` | `rules/testing.md` plus `skills/testing` (mixed) | `skills/testing` | `project-structure` | none |
| M | `docs/technology-stack.md` | `rules/testing.md` | `rules/testing.md` (same file) | `dotnet-testing` skill | `project-structure` | asset written in NUnit |
| L0 | Project decisions | `rules/2-technology/nunit.md` | `rules/0-core/testing-principles.md` | `dotnet-testing` (Technology level) | scaffold workflow (Project level) | asset written in NUnit |
| L1 | Selection record `backend-testing → nunit` | facet `rules/2-technology/test-framework.md`, owned by `backend-testing/nunit` | `rules/0-core/testing-principles.md` | `dotnet-testing` (module facet) | scaffold reads the module's scaffold facet | neutral checks plus an NUnit adapter facet |
| K0 | Register D-15 | `rules/backend-tests/testing.md` | the same file | `dotnet-testing` (KNW) | scaffold (WF) | asset written in NUnit (ENF) |
| K1 | Register, slot section | facet `rules/backend-tests/test-framework.md` | `rules/backend-tests/testing.md` (neutral) | `dotnet-testing` (KNW facet) | scaffold reads the module's scaffold facet | neutral checks plus an NUnit adapter facet |

### 4.2 Trace: where Clean Architecture lives

Observed in V2: 28 of the 41 files use the layer vocabulary (Domain, Infrastructure, Application Service, Application layer).

| Candidate | Placement |
|---|---|
| V2 | `rules/architecture.md` (path-scoped), copies in 7 other artifacts (D1, D4), `CLAUDE.md` core defaults |
| M | `rules/architecture.md` and `rules/persistence.md`. The gate and the list of patterns not adopted move to `CLAUDE.md`. |
| L0 | **The whole Architecture level is Clean Architecture**: overview (always), layers, persistence boundary, entry points, outcomes, frontend structure. Technology modules may name its layers. |
| L1 | The Architecture level holds the **role vocabulary** and role-level invariants: use-case unit, persistence-access contract, commit boundary, entry point, composition root. The `architecture/clean-architecture` implementation (facets at level 1) maps roles to projects and types, owns the layout and the list of patterns not adopted, and provides the specification of the architecture checks. Leaves are written against roles only. |
| K0 | Register D-01 to D-06 and D-19; `STD` rules `backend/architecture.md`, `persistence.md`, `api.md`; references from KNW and WF |
| K1 | The register's slot section; a neutral `STD` with role-level rules; the `architecture/clean-architecture` module contributes the `DEC` summary, the `STD` facets (layers, mapping, patterns not adopted), the scaffold `WF` facet and the `ENF` check specification |

---

## 5. Controlled comparison matrix

### 5.1 Direct comparisons

| Comparison | Isolates | Held constant | Must differ **only** in | Primary metrics | Expected result |
|---|---|---|---|---|---|
| **V2 vs M** | Conventional cleanup **plus** the shared bundle | V2 file topology (P-07); embedded capabilities | Every S-invariant; changes driven by defect IDs | Behavioral suite; trigger suite; tokens | Large improvement. **Confounded** (E vs cleanup) unless the §3.6 ablation runs. |
| **M vs L0** | Adding a stability-first meta-architecture | S-bundle, content pool, B0 | Directories, file boundaries, level metadata, neutral wording (logged) | Change-impact suite; navigation; behavioral (non-inferiority) | Behavior: equal within noise. Maintainability: L0 better for technology changes, worse for learning cost. |
| **M vs K0** | Adding a Kinds × Scopes meta-architecture | S-bundle, content pool, B0 | Directories, kind and scope metadata, the register | Same | Behavior: equal within noise. K0 better at "where does X go". M lower learning cost. |
| **L0 vs K0** | Axis A, with capabilities embedded | S-bundle, content, B0 | Placement by level vs by kind × scope | Change-impact; navigation; loading precision; behavioral | K0 better at loading precision and finding owners; L0 better at keeping a technology in one place. Behavior: small differences. |
| **L1 vs K1** | Axis A, with capabilities replaceable | S-bundle, content, **identical slot set, contract format, composition strategy and module content** | Placement of non-slot content (= L0 vs K0) and where facets land | Same, plus the replacement suite | As L0 vs K0. Replacement metrics are close, because the modules are the same. |
| **L0 vs L1** | Axis B under stability-first | Level structure; placement of non-slot content (P-14) | The capability transformation on the slot set | Replacement suite; behavioral (non-inferiority); tokens; indirection | L1 has a smaller blast radius and fewer missed mentions; L1 adds slight overhead on ordinary tasks. |
| **K0 vs K1** | Axis B under Kinds × Scopes | Kind and scope placement of non-slot content (P-14) | Same transformation | Same | As L0 vs L1, but **with a larger replacement gain** (interaction hypothesis). |
| **(L1 − L0) vs (K1 − K0)** | A × B interaction | Everything above | — | Replacement suite | The gain is larger under K. |
| **M vs L1 / K1** | Full meta-architecture plus capabilities vs conventional cleanup | S-bundle, content | Everything that is not shared | All suites, plus complexity metrics | L1 and K1 win only on replacement tasks. Whether that justifies their complexity depends on how often replacements happen. |
| **V2 vs any** | Total effect | — | — | All | Every experimental candidate is better than V2 on behavioral metrics (Expected). |

### 5.2 Interpreting the results

- A behavioral difference between two experimental candidates is credible only if **(a)** P-14 or S-01 holds, so the content is equivalent, **(b)** the trigger suite shows which owner did or did not load, and **(c)** the difference exceeds run-to-run variance over several repeats.
- When two candidates converge physically (§12), record "no detectable difference: structurally equivalent", not "tie".

### 5.3 Two benchmark families

1. **Behavioral suite**: 001 §11.3, items 1–13, unchanged.
2. **Change-impact suite** (new; maintainer tasks done by a person or by Claude through `template-maintenance`, the same way for every candidate):

   | ID | Task | What it measures |
   |---|---|---|
   | CI-1 | Add a project rule ("public API DTOs are records") | Owner discovery; files touched |
   | CI-2 | Approve a decision (adopt Minimal APIs for health endpoints) | Decision propagation; missed mentions |
   | CI-3 | Add a technology (Redis distributed cache, after approval) | Extension cost |
   | CI-4 | Replace a leaf: NUnit → xUnit | Leaf blast radius |
   | CI-5 | Replace a provider variant: SQL Server → PostgreSQL | Variant handling; surfacing the collation consequence |
   | CI-6 | Replace a leaf that brings secondary decisions: EF Core → Dapper | Completeness of the contract (migration mechanism) |
   | CI-7 | Replace the frame: Clean Architecture → Vertical Slice Architecture | Frame blast radius; whether the contract must be revised |
   | CI-8 | Remove an optional concern: frontend | Optional-slot handling |
   | CI-9 | Change one rule's wording (the test-naming convention) | Single source of truth in practice |
   | CI-10 | Answer "where is the rule for X, and when does it load?" | Navigability |

   **Metrics**:
   - authoritative artifacts edited outside the replaced unit;
   - total lines changed;
   - missed mentions (a grep for the old implementation after the task, plus review);
   - S2 result;
   - trigger-suite result after the change;
   - a short behavioral smoke task under the new choice;
   - tokens and time;
   - human interventions.

   **Fairness rule:** replacement *content* (xUnit technique, VSA policy, Dapper technique, PostgreSQL specifics) comes from the shared content pool and is identical for every candidate. What is measured is the cost of integrating it, not of writing it (§6, CF-10).

---

## 6. Confounding factors to avoid

| ID | Confounder | Distorts | Prevention | Detection |
|---|---|---|---|---|
| CF-1 | **Content drift**: candidates carry different policy wording or completeness | Every comparison | S-01: one inventory and content pool; central decisions; a permitted-delta log | Diff the fragment multiset per candidate; any unlogged delta fails |
| CF-2 | **Enforcement asymmetry**: hooks, permissions, architecture tests or analyzers differ | Behavior | S-13: one package E; messages differ only in owner paths | Diff `settings.json`, hook scripts and assets across candidates |
| CF-3 | **Enforcement bundled with cleanup** in V2 vs M | V2 vs M | Optional M−E or V2+E ablation (§3.6) | — |
| CF-4 | **Model, effort or version differences** | Everything | S-17: pinned for every run | Run metadata |
| CF-5 | **Always-loaded budget asymmetry**: one candidate loads everything up front | Behavior, tokens | S-18 ceiling | Measure at session start |
| CF-6 | **Naming effects**: emphatic or level- or kind-prefixed skill names, or different names for the same content | Skill triggering | S-12: identical names for identical content; classification goes in headers and the map, not in names | Diff the skill name lists |
| CF-7 | **Unequal description quality** | Skill triggering | Descriptions come from the content pool; same length rules | Diff the descriptions |
| CF-8 | **Generator and author effects**: candidates written in different sessions, of different quality | Everything | The construction order in §1 item 4; mechanical re-placement where possible; the same review checklist; the same number of fix iterations for each candidate | Review log; count of iterations per candidate |
| CF-9 | **Implementation maturity**: one candidate gets more debugging rounds | Everything | A fixed iteration budget, applied equally | Iteration log |
| CF-10 | **Replacement content available in advance**: L1 or K1 ship an xUnit module and the others don't | Replacement metrics | Replacement content lives in the shared pool and is supplied identically at task time | Audit the task inputs |
| CF-11 | **Composition mechanism differs** between L1 and K1 | L1 vs K1 | The same strategy (CS-1/2/3) and the same contract format | Diff the composition tooling |
| CF-12 | **Different slot sets** in L1 and K1 | L1 vs K1; interaction | One agreed slot set (§7.5) | Diff the contracts |
| CF-13 | **Non-slot content changed** during the capability transformation | L0 vs L1, K0 vs K1 | P-14 | Diff L0 with L1 and K0 with K1, excluding slot content; must be empty apart from logged glue |
| CF-14 | **Nested discovery or research leakage**: skills of other templates are visible, or a passport is read | Everything | S-19: a copy of the candidate as project root; `research/` excluded | Inspect the loaded skill list and transcripts |
| CF-15 | **Biased task selection**: only greenfield tasks, or only replacement tasks | Rankings | Balanced suites (§5.3); some scenarios held out | Coverage table of scenarios × candidates |
| CF-16 | **Reviewer bias** when scoring | Violations, rework | Blind the scoring of output diffs where possible | Inter-rater agreement |
| CF-17 | **Path-granularity differences** presented as architecture effects | Tokens, adherence | S-09: the same trigger class; minimum coverage per S-10 | Trigger suite: loaded files per task |
| CF-18 | **Artificially forced divergence**, to make candidates look different | Every A comparison | Report convergence instead (§12) | Structural distance (§12.2) |
| CF-19 | **Order or position effects** in always-loaded content (for example, where the decision summary sits) | Planning behavior | The same order of sections in `CLAUDE.md` where the content is shared | Diff of the `CLAUDE.md` skeleton |

---

## 7. Capability-boundary analysis

### 7.1 Criteria

Score each concern **H / M / L** on six criteria, then apply three gates.

| # | Criterion | Question | Counts towards a capability when |
|---|---|---|---|
| C1 | Independent choice | Can the choice be made without forcing other choices, or does it force only declared ones? | High |
| C2 | Probability of replacement **or removal** | Within the template's realistic user base and this research | High |
| C3 | Policy and workflow consequences | Does replacing it change must-rules, workflows, assets or enforcement, not just a package name? | High |
| C4 | Spread of knowledge | How many authoritative artifacts must currently know the choice (V2 evidence)? | High |
| C5 | Cost of replacing it without isolation | Edits, plus the risk of missing a mention | High |
| C6 | Coupling to other capabilities | How tangled it is with other slots. **Inverse**: high coupling lowers isolatability. | Low |

| Gate | Condition | If the gate fails |
|---|---|---|
| G1 Contract can be expressed | Other artifacts can be written against the slot without losing concreteness that matters for generation, or the implementation's own facets make up for the loss | Questionable at best |
| G2 Not the platform | .NET / C#, the ASP.NET Core host and TypeScript are assumed, not slots | Not a capability |
| G3 Enough facets | The implementation would supply at least two facets of different kinds | Weak: a decision entry plus knowledge is enough |

**Classification:**

- **Strong**: C1–C5 mostly high, C6 low or medium, all gates pass.
- **Questionable**: high value, but G1 or C6 is in doubt, or C2 is uncertain. Include only as an experiment, or later.
- **Weak**: C3–C5 low, or G3 fails. Keep it embedded.

### 7.2 The five required examples

| Example | C1 | C2 | C3 | C4 (V2, Observed) | C5 | C6 | Gates | Class |
|---|---|---|---|---|---|---|---|---|
| NUnit → xUnit | H | M–H | M | 4 files name NUnit; NUnit syntax throughout the examples in `skills/testing` | M | L | pass | **Strong** |
| EF Core → Dapper | H | L–M | H | 17 files mention EF Core, `DbContext` or `DbSet` | H | M–H | G1 only if the contract declares the secondary facets | **Strong, with declared secondary decisions** |
| SQL Server → PostgreSQL | M | M | M (few consequences, but sharp ones) | 6 files, 11 lines | L–M | H | G3 fails on its own | **Weak as a standalone capability.** Model it as a provider variant of `persistence`. |
| Clean Architecture → VSA | H | L–M | very H | 28 of 41 files use the layer vocabulary | very H | very H | G1 doubtful | **Questionable as a leaf. Treat it as a frame.** Include it as the stress test. |
| Serilog → another logging setup | M–H | M | L | 3 files (`serilog`, `logging`, `technology-stack.md`) | L | L | G3 fails | **Weak** |

**NUnit → xUnit (Strong).**

- What changes: attributes, fixture lifecycle (`[OneTimeSetUp]` vs `IClassFixture`), parallelization, data-driven test syntax, assertion style, test project templates, and the architecture-check wrapper.
- What does not change: the policy that is independent of the framework. Test levels, determinism, isolation, probe-to-test, no EF InMemory for relational behavior, and test placement are all *core or standard* content and stay outside the module. That separation is what makes the slot clean.
- Coupling is low. It binds to the architecture only for the test project layout, which is a placement question (§7.4).

**EF Core → Dapper (Strong, with secondary decisions).**

- The replacement goes well beyond swapping a package:
  - the Unit of Work becomes explicit transactions;
  - EF migrations disappear, so a **migration mechanism must be chosen**, which is a new Reserved decision;
  - seeding loses `DbContext`;
  - raw-SQL security moves from an edge case to the center;
  - query technique and the test-database strategy change.
- The persistence contract must therefore declare facets for *commit boundary*, *migration mechanism* and *seeding mechanism*. A Dapper implementation that leaves one unfilled fails conformance, which raises a Decision Request. This is the clearest case for why a contract is more than a folder.

**SQL Server → PostgreSQL (Weak as a standalone capability).**

- What changes:
  - the provider package;
  - the LocalDB development default (Windows only, in `technology-stack.md`);
  - migrations, which must be regenerated;
  - the CI service container (`skills/ci-cd`, line 145 names SQL Server);
  - the Testcontainers image;
  - **default string-comparison semantics.**
- Each of these is either inside persistence or a delivery or testing binding, so a separate slot would mostly forward to them.
- One consequence must not be hidden. Changing the default comparison semantics (expected: SQL Server's common default collations compare case-insensitively, PostgreSQL compares case-sensitively by default) changes *observable product behavior*, which V2 governs explicitly (`CLAUDE.md:25-38`). See §7.6.

**Clean Architecture → VSA (a frame: questionable as a plug-in, included as the stress test).**

- The architecture is the vocabulary that the persistence, testing-layout, error-handling, DI, caching and scaffolding guidance is written in. It is not a leaf.
- Isolating it requires a **role vocabulary**: use-case unit, persistence-access contract, commit boundary, entry point, composition root. Leaves bind to the roles, and the frame implementation maps the roles to concrete forms.
- Expected:
  - the replacement shrinks, but stays medium to large;
  - VSA will probably force a **revision of the contract**: for example, "persistence-access contract" may not exist as a separate role in VSA;
  - role vocabulary may make generation less concrete (§14 E1).
- It is still the most informative test of the B axis, and the prompt names it explicitly.

**Serilog → another logging setup (Weak).**

- Application code already depends on `ILogger<T>` (`technology-stack.md`, lines 129–135).
- Logging *policy* (structured templates, levels, no sensitive data, log once) does not depend on the provider, and belongs to Core or common standards.
- What depends on Serilog is the bootstrap in `Program.cs`, the sink configuration and the enrichers. That is one knowledge reference and one decision entry. A capability boundary would cost more than it saves.
- Revisit this if observability grows (OpenTelemetry traces and metrics).

### 7.3 Other concerns

| Concern | Class | Reason |
|---|---|---|
| Frontend (Angular, Vitest, Material) | **Questionable**: strong for *optional presence*, weak for *replacement* | Removing it (an API-only service) is realistic. Replacing it is not, since React is a non-goal (requirements §5.3). It touches 16 V2 files, plus verify, scaffold and CI steps and the contract-authority rule. |
| API style (Controllers vs Minimal APIs) | Questionable; belongs to the architecture frame | 15 files mention Controllers. It is strongly coupled to the architecture (VSA often goes with Minimal APIs), to Swagger, to error-handling filters and to versioning. |
| Authentication scheme | Questionable now; a candidate for a *later* optional slot | Absent by default, and adopting it is Reserved (R-8). Once adopted it cuts across API, frontend, Swagger and tests. A good task for the extension test "add a slot". |
| Delivery (Docker, CI vendor) | Questionable; later | Switching CI vendor is realistic (V2 shapes CI as GitHub Actions, `skills/ci-cd`, line 86). The consequences are modest and the coupling low to medium. |
| Validation (FluentValidation) | Weak | The validation-boundary policy belongs to the architecture or core. The library-specific technique is small. |
| API docs (Swashbuckle → built-in OpenAPI) | Weak | Platform drift makes it likely, but the consequences are small: packages and `Program.cs`. The Development-only policy stays. |
| Mapping (Mapster) | Weak | Conditional and trivial. |
| Outbound HTTP and resilience | Weak | Technique only. The decision is already Microsoft resilience. |
| Caching | Weak | Absent by default. A distributed cache is an infrastructure decision (R-5), not a slot. |
| Platform (.NET 10, C# 14) | Not a capability (fails G2) | A version bump is a parameter, not a replacement. |

### 7.4 Frames, leaves and bindings

The capability models only stay maintainable with a rule for content that belongs to two slots at once. Shared rule for L1 and K1:

> **Placement belongs to the frame; technique belongs to the leaf.**
> - Anything that says *where* code lives, or *which role* carries a responsibility, is owned by the frame implementation (`architecture/*`).
> - Anything that says *how* to do it with a technology is owned by the leaf implementation, and is written against **role names**, never against the frame implementation's terms.
> - When a binding cannot be phrased in role terms, it is owned by the **dependent** slot and declared as `binds: <slot>/<impl>`. That declaration is accepted coupling, and it is counted in the replacement metrics.

Examples:

| Content | Owner |
|---|---|
| "`IUnitOfWork` is the commit boundary of a use case and lives in Application" | `architecture/clean-architecture` (placement) |
| "Implement the commit boundary with `SaveChangesAsync` on the scoped `DbContext`" | `persistence/ef-core` (technique, phrased against the *commit boundary* role) |
| Test projects `<Name>.Application.Tests` and `<Name>.IntegrationTests` under `backend/` | `architecture/clean-architecture` (placement of the test-project roles) |
| Architecture checks | The frame provides a **neutral check specification**: reflection-based assertions in a plain class. `backend-testing/*` provides a **thin adapter** that exposes the checks as tests in its own framework. This avoids a frame × leaf cross-product. |

**Risk.** Each frame implementation multiplies the bindings. With one frame implementation, the risk stays latent. Adding VSA (CI-7) is exactly when it shows up.

### 7.5 Recommended slot set (identical for L1 and K1)

| Slot | Type | Implementation shipped | Why it is in the set |
|---|---|---|---|
| `architecture` | frame, required | `clean-architecture` | Stress test of the B axis; CI-7 |
| `persistence` | leaf, required; provider variants | `ef-core` (provider `sqlserver`) | Strong; secondary decisions; CI-5 and CI-6 |
| `backend-testing` | leaf, required | `nunit` | The cleanest strong leaf; CI-4 |
| `frontend` | leaf, **optional** | `angular` | Optional presence; CI-8 |

Everything else stays embedded in L1 and K1 exactly as in L0 and K0 (P-14).

Optional, if the researchers want a negative control: add `logging/serilog` as a *weak* slot to measure the overhead of turning a weak candidate into a capability. This is not recommended by default (§13 Q6).

### 7.6 Contracts must surface consequences for product behavior

A capability boundary must never hide a change in observable behavior. Contracts therefore carry **declared properties**, and every implementation must state them explicitly. For example, `persistence` requires "default string-comparison semantics", "case sensitivity of uniqueness" and "migration mechanism".

Core product-governance policy (S-08) treats a change to a declared property as a product decision. So SQL Server → PostgreSQL produces a Decision Request about case sensitivity instead of a silent behavior change. This keeps B1 from undermining invariant 3.3 (no silent overrides).

---

## 8. Expected complexity of each candidate

All figures are Expected and approximate. They should be re-measured after generation.

| Metric | V2 | M | L0 | L1 | K0 | K1 |
|---|---|---|---|---|---|---|
| Runtime instruction files | 41 | 45–50 | 55–65 | 60–75 | 50–55 | 65–80 |
| Maintainer-only files (map, contracts, manifests) | 0 | 1 | 1 | 1 + 4 contracts + 4 manifests | 1 | 1 + 4 + 4 |
| Concepts a maintainer must learn beyond Claude Code mechanisms | 0 (implicit) | about 6 shared (reference forms, decision classes, IDs, completion contract, map, vocabulary) | shared + 4 levels + level rule + neutral-wording rule ≈ 9 | L0 + slot, contract, implementation, facet, selection, binding, conformance, composition ≈ 17 | shared + 7 kinds + 6 scopes + kind graph ≈ 10 | K0 + the 8 capability concepts ≈ 18 |
| Classification decisions per new artifact | 0 | 1 (which V2 file) | 1 (level) + topic | 2 (level, slot or none) | 2 (kind, scope) | 3 (kind, scope, slot or none) |
| Structural rules checked by S2 | 0 | about 8 (shared) | about 12 | about 18 | about 12 | about 20 |
| Maximum hops from trigger to owner | 3 (rule → skill → reference) | 2 | 2 | 3 (slot → facet) | 2 | 3 |
| Always-loaded tokens | about 3.7k (001) | ≤ ceiling | ≤ ceiling | ≤ ceiling, plus the selection record | ≤ ceiling | ≤ ceiling, plus the slot section |

**The complexity cost of K1, analyzed explicitly** (the prompt asks for this):

1. **Three primary coordinates per artifact.** Kind fixes the mechanism, scope fixes the paths, capability fixes the replacement unit. Each new artifact takes three classification decisions. Each decision is a chance for disagreement, and for metadata drifting away from the physical location.
2. **The cell space is sparse but large.** 7 kinds × 6 scopes × (1 + 4 slots) = 210 cells, of which perhaps 30–40 are used. A maintainer must know which cells are legal.
3. **Facets are spread out.** One technology (NUnit) supplies up to five facets across four kind locations. At runtime, a missing facet is harder to notice in K1 than in L1, because in L1 the facets of a leaf sit together at its slot's level.
4. **Ownership conflicts across axes.** "Test projects under `backend/`" is a standard (`STD`) for scope backend-tests, owned by the architecture frame and used by the testing leaf. The rule in §7.4 resolves this, but only by adding another rule to learn.
5. **The map becomes three-dimensional.** It needs views by kind × scope *and* by capability.

**Prediction:** K1 is the most expensive to learn and to maintain day to day. Its payoff is confined to the change-impact suite, mainly CI-4 to CI-8. Whether the payoff exceeds the cost depends on how often replacements happen, which the template's real users would have to estimate (§13 Q14).

---

## 9. Expected loading and triggering risks

| Candidate | Risk | Why | Mitigation or test |
|---|---|---|---|
| V2 | Policy missing at planning time; seed, settings and Angular policy behind skills; excess backend context | 001 §6.3 | — (control) |
| M | Defect fixes miss cases that no defect ID names; V2-lineage files keep mixed triggers (for example, `performance.md` loads on every backend `.cs` file) | Fixes are local, with no global placement rule | Trigger suite; the inventory proves coverage |
| L0 | **More files load per path trigger** (Core, Architecture and Technology files for one backend edit) | Splitting by level separates content with the same trigger | Measure files and tokens per task |
| L0 | **Technology-neutral wording at lower levels** may weaken generation ("persistence-framework types" vs "EF Core types") | P-03 | §14 E2. The technology rule that binds an architecture constraint must be path-scoped at least as broadly as that constraint. |
| L0 | Decisions are split across two always-loaded files (Architecture overview, Project decisions) | Stratification | Both imported; trigger test T1 / T8 (001) |
| L1 | All of L0's risks, plus **slot indirection**: workflows reach commands through facets; more hops | P-13 | §14 E1; or substitution at composition time (§13 Q5) |
| L1 | **Role vocabulary** from the frame makes rule text less concrete | §7.4 | §14 E1 |
| L1, K1 | **A replacement silently drops a facet** (for example, the xUnit module forgets the test-placement rule) | Static composition | Conformance (S2) plus the trigger tests of the replacement procedure |
| K0 | Unclear kind boundaries ("Development-only seeding": decision or standard?) put content under the wrong trigger | Classification | Placement table in the map; review |
| K0 | The register grows and pushes the always-loaded budget | One decision file | S-18 ceiling; details stay in `STD` |
| K0 | Per-layer globs depend on project naming | S-10 | Same in every candidate (shared) |
| K1 | All of K0's risks, plus L1's indirection and facet risks, plus **facets of one capability spread across kind directories**, so a gap is less visible | Three axes | Module manifests; S2 |
| All | The mechanics are still unverified: whether path rules trigger on Read or Write, how rule subdirectories and skill directories are discovered, the skill listing budget, `skills:` preload in agents | 001 §0.3 | §14 E0, before generation |

---

## 10. Expected maintainability risks

| Candidate | Main risk | Failure mode | Early indicator |
|---|---|---|---|
| V2 | Compensating duplication | Copies drift (C8: two test-naming conventions) | Already observed |
| M | **There is no placement rule for new content** | Over time content goes "where it looks similar", and duplication creeps back | CI-1 / CI-3: inconsistent placement by different maintainers |
| L0 | **Arguments about which level something belongs to** (is seeding Technology or Project? is "no automatic production migrations" Core or Project?) | The same statement ends up at different levels in different edits; neutral wording erodes | CI-1: level-assignment disagreements; drift in P-03 |
| L0 | Over-abstraction | Authors write neutral text "for the future" that no one consumes | Neutral sentences with no binding technology statement |
| L1 | **Contracts drift away from their implementations**; contracts change whenever a new implementation does not fit (VSA) | The contract becomes a formality; "stable" artifacts change often | Contract revisions per replacement (CI-7) |
| L1, K1 | Binding growth (§7.4) | Frames × leaves cross-products | Number of `binds:` declarations |
| L1, K1 | Composition tooling (CS-2) | The generator and the source drift; manual edits to generated files | Drift check failures |
| K0 | **Learning cost of the taxonomy** (7 kinds × 6 scopes); the register's "Affects" column must be maintained | Content is misclassified; "Affects" goes stale | CI-2: missed entries in "Affects" |
| K0 | A technology is spread across kinds (embedded) | A replacement needs edits in 4–5 kind locations | CI-4 metrics |
| K1 | Highest concept count; three coordinates; ownership disputes across axes | Maintainers bypass the structure | CI-1 time and errors; S2 overrides |

---

## 11. Expected flexibility and replacement risks

Predicted number of **authoritative artifacts edited outside the replaced unit**. The selection record and the decision summary count as one edit. These are rough, Expected figures, to be measured by the change-impact suite.

| Task | V2 | M | L0 | L1 | K0 | K1 |
|---|---|---|---|---|---|---|
| CI-4 NUnit → xUnit | 4, plus heavy example rewrites; missed mentions likely | about 5 | about 5, mostly at one level | **1** (selection) + module swap | about 5, across 4 kind locations | **1** + module swap |
| CI-5 SQL Server → PostgreSQL | about 6 | about 5 | about 4 | 1 + variant swap + 1–2 bindings | about 5 | 1 + variant + 1–2 bindings |
| CI-6 EF Core → Dapper | 12+ | about 10 | about 8 | 1 + module swap + **a new decision** (migration mechanism) | about 10 | 1 + module + new decision |
| CI-7 CA → VSA | 20+ | about 15 | about 12–15 (the whole Architecture level, plus technology modules that use layer names) | about 3–6, **plus a likely contract revision** | about 12–15 | about 3–6, plus a contract revision |
| CI-8 Remove frontend | about 10 | about 8 | about 6 | 1 + module removal + conditional text in shared workflows | about 7 | 1 + module removal + conditional text |

**Risks by candidate:**

- **M, V2**: replacement means grep and edit. The blast radius is unknown in advance, and missed mentions are the main failure.
- **L0**: replacing a leaf is mostly local to the Technology and Project levels, *if* the neutral wording held. Replacing the frame rewrites the Architecture level and every technology module that uses its terms.
- **L1, K1**:
  - leaf replacements are small;
  - secondary decisions appear (Dapper) and must turn into Decision Requests, not gaps;
  - the frame replacement is the real test, and a contract revision is likely;
  - the risk of false confidence: "the module was swapped" is not the same as "the behavior is correct". The behavioral smoke task after each replacement is required.
- **K0**: a replacement touches every kind where the technology appears. The register's "Affects" column makes this traceable, but not small.

---

## 12. Where candidates may converge physically

### 12.1 Expected convergence cases

| # | Candidates | What converges | Why | Consequence |
|---|---|---|---|---|
| CV-1 | All five | `CLAUDE.md` (operating policy, decision control, product governance, completion contract, workflow map) | S-06, S-08, S-11 and S-16 fix the content; there is one always-loaded entry point | Differences in planning behavior cannot come from `CLAUDE.md` |
| CV-2 | M, L0, K0 (and L1, K1) | The always-loaded decision content | S-07 fixes the content. M's `technology-stack.md`, L0's overview plus Project decisions, and K0's register hold the same text | Only the number of files and their position differ. Test CF-19. |
| CV-3 | All five | The skill set: names, descriptions, bodies | S-11 and S-12, plus Claude Code's flat skill namespace | The skill layer differs only in the header and metadata, and in slot facets for B1 |
| CV-4 | All five | `angular.md` and the frontend rule | S-10; one frontend scope | Identical except for the directory |
| CV-5 | L0 ↔ K0 | The split of persistence policy (the neutral pattern vs the EF Core specifics) | K0 splits by "rate of change" (001 P7), which is the stability criterion again | L0 and K0 may end up with the same files in different directories |
| CV-6 | M ↔ K0 | Most of the file set | K0 (001) was derived from fixing V2's defects, and M fixes the same defects | Behavioral differences may disappear. That would be a significant result (the meta-architecture adds no behavior). |
| CV-7 | L1 ↔ L0, K1 ↔ K0 | The runtime layout when only one implementation per slot exists | Static composition; facets keep the trigger classes they had in B0 | Runtime differences shrink to slot wording, role vocabulary and facet splits. The B effect appears mainly in the change-impact suite. |
| CV-8 | L1 ↔ K1 | The modules themselves | Same slot set, contracts and content (CF-11, CF-12) | Differences come only from where non-slot content and facets land |
| CV-9 | All | Enforcement | S-13 | By design |

### 12.2 What to do about it

1. **Do not force divergence** (CF-18). Making two candidates artificially different adds a confound.
2. **Measure structural distance before benchmarking.** Suggested measures:
   - the share of inventory items whose owner file *role* differs between two candidates;
   - the Jaccard distance between their sets of runtime files, by content hash;
   - the difference between the sets of files loaded per benchmark task.
3. **Report convergence as a finding**, for example: "On the runtime layer, A-K and A-M produced structurally equivalent systems; the architectural principle only showed up in maintenance artifacts."

---

## 13. Questions that must be decided before implementation

| # | Question | Recommendation |
|---|---|---|
| Q1 | Build the **V2 policy inventory** with stable IDs first, as a separate research artifact (001 called it "002"; that number is now taken, so use the next free observation number) | Yes. It is the precondition for S-01 and for every confound check. |
| Q2 | Use the construction order inventory → content pool → M → L0 and K0 → L1 and K1 (§1, item 4)? | Yes |
| Q3 | Is the shared bundle S-01…S-19 accepted as is? In particular S-09 (the same trigger class per item) and S-12 (identical skill names). | Yes. If S-09 is relaxed, loading differences can no longer be attributed to architecture. |
| Q4 | Run the ablation **M−E** (or **V2+E**) to separate enforcement from cleanup? | Yes, as an optional seventh run. None of the six is removed. |
| Q5 | Composition strategy for L1 and K1 (CS-1 / CS-2 / CS-3), and **indirection at runtime vs substitution at composition time** for slot references | CS-1 (in place, with manifests) for the first experiment. Decide indirection vs substitution after §14 E1. |
| Q6 | Slot set: the four in §7.5? Add `logging` as a negative control? | The four; no `logging` |
| Q7 | Is `architecture` a replaceable frame in L1 and K1, or embedded even in B1? | A replaceable frame (the prompt names CA → VSA). Re-evaluate if E1 shows that role vocabulary degrades generation. |
| Q8 | Shared skill names: keep V2's names except where a collision defect forces a rename (`testing` → `dotnet-testing`, the `error-handling` skill → `aspnet-error-handling`)? Or use 001's verb names (`scaffold`, `change-settings`)? | V2 names plus the renames forced by collisions. This favors no candidate and keeps M faithful to V2. |
| Q9 | The L level set: Core → Architecture → Technology → Project, with inputs outside? | Yes (L0 DESIGN §1). Confirm that Project sits *above* Technology in volatility. |
| Q10 | The K kind set: OP, DEC, STD, KNW, WF, ENF, IN, plus the scopes in S-10? | Yes (001 §4.3, re-coded) |
| Q11 | Ceiling on always-loaded context (S-18)? | Start at about 5k tokens including the skill listing. Calibrate in E8. |
| Q12 | Where candidate implementations will live: `templates/candidates/<ID>/`? What happens to `templates/v3/`? | `templates/candidates/<ID>/`. Keep `templates/v3/` frozen as it is until the humans decide. Its name no longer matches the six-candidate design. |
| Q13 | Second implementations for the change-impact suite (xUnit, PostgreSQL, Dapper, VSA): written once in the content pool, before or during the benchmark? | Before, in the pool, available identically to every candidate (CF-10) |
| Q14 | How to weigh the change-impact metrics against the behavioral metrics in the final comparison? This needs an assumption about how often replacements happen. | Decide the weighting before any results are seen, to avoid fitting it afterwards. |
| Q15 | Fixed iteration budget per candidate (generation plus fix rounds)? | Yes. The same number of review and fix rounds for each. |
| Q16 | Does any candidate get rule subdirectories if E0 shows they are not discovered? | If subdirectories don't work, all candidates use a flat layout with prefixed names. L and K lose a visible axis equally. |

---

## 14. Empirical tests recommended before generation

These are cheap, targeted experiments. Each one decides a design question, so it must run **before** candidates are generated.

| # | Question | Affects | Protocol (sketch) | Feeds |
|---|---|---|---|---|
| E0 | **Mechanics**: do path rules trigger on Read, Edit, or a Write that creates a file? Are rules in subdirectories discovered? Are nested skill directories discovered? How large is the skill listing budget? Does `skills:` preload work in agents? Do `@import`s nest? Do hooks run on Windows? | All | 001 §6.6, run on one minimal fixture | Q16, S-09, every DESIGN |
| E1 | **Indirection and role vocabulary**: does slot or role wording ("the commit boundary", "the backend-testing conventions") degrade generation compared with concrete wording ("IUnitOfWork", "NUnit")? | L1, K1 | A/B on one rule pair with 3 to 5 small tasks, several runs each; measure violations and wrong placements | Q5, Q7 |
| E2 | **Technology-neutral wording at lower levels**: "persistence-framework types must not appear in Domain" plus a separate EF Core binding rule, vs one concrete rule | L0, L1 | A/B on Domain and Application edits | The neutral-wording rule in the L designs |
| E3 | **One decision file vs stratified files**: does Claude find Reserved items at planning time equally well? | L vs K vs M | Design-question tasks (001 T8) with both layouts | Confirms CV-2 is harmless or reveals CF-19 |
| E4 | **Several small rules vs one merged rule** with the same trigger: any effect on adherence? | L vs K | The same content, split vs merged | Expected size of L0 vs K0 differences |
| E5 | **Paper replacement**: sketch where NUnit → xUnit and CA → VSA would land in each candidate's DESIGN tree, and count the edits | All | Desk exercise using the DESIGN files | Recalibrates §11; may change Q7 |
| E6 | **Header and metadata visibility**: do classification headers (`Level:`, `Kind:`, `Capability:`) change behavior when the rule loads? | All | The same rule with and without the header line | Whether headers stay in runtime files or move to the map only (CF-6) |
| E7 | **A missing facet after replacement**: does Claude notice when a required rule is gone (e.g., test placement)? | L1, K1 | Remove one facet; run CI-4 | Strictness of conformance checks |
| E8 | **Calibrate the always-loaded budget** | All | Measure V2, then a rough skeleton of each candidate | Q11 |

**Order:**

1. E0 first; everything depends on it.
2. E1, E2 and E5 next. They decide the most consequential design questions for L1, K1 and L0.
3. E3, E4, E6, E7 and E8 can run in parallel with building the inventory.
