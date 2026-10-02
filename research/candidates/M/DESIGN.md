# M — Minimal Modular: Design Notes

> **Research metadata.** This file is not part of any candidate's instruction context (S-19). Never copy it into a template or a benchmark project.

| | |
|---|---|
| Candidate | **M**: Minimal Modular |
| Axis A | A-M: no meta-architecture; V2 lineage |
| Axis B | B0: embedded capabilities |
| Passport | `research/candidates/M/CORE_FEATURES.md` |
| Shared invariants | S-01…S-19, defined in `research/observations/002-candidate-space-analysis.md` §2 (hereafter "002") |
| Distinguishing predicates (002 §3.4) | P-07 **yes**; P-08 yes; P-01…P-06 and P-09…P-13 **no** |
| Status | Design only. Illustrative trees, not final files. |

---

## 1. Construction rule

M is **V2 plus the shared invariants plus defect-driven refactoring**. Nothing more.

Every M artifact must satisfy the **lineage rule** (P-07). Each file is one of:

| Change type | Meaning | Justification required |
|---|---|---|
| Keep | The same V2 file. Only restatements are replaced by pointers or checks (S-02). | None beyond S-02 |
| Fix in place | The same file; its content is corrected | A defect ID from 001 §3 (D-n, C-n, an inversion in §2.3, a defect in §3.6) |
| Split | One V2 file becomes two or more | A defect ID showing mixed responsibilities or triggers |
| Merge | Two or more V2 files become one | A defect ID showing competition (001 §6.3) |
| Move | Content moves to a file that loads more reliably | A defect ID showing a loading gap or an inverted dependency |
| New | No V2 predecessor | An S-ID (for example, S-13 enforcement, S-14 map) or a defect ID |

**M may not:**

- reorganize content for "architectural beauty";
- introduce a classification taxonomy;
- rename files without a reason (the renames in 002 §13 Q8 are central and apply to every candidate).

These limits are what make M a test of *conventional* cleanup.

**Placement heuristic** (local, not systemic): keep content in its V2 owner unless a defect forces a move. When moving it, choose the existing or V2-shaped file that (a) is loaded by the trigger the content needs (S-09) and (b) is closest in topic.

---

## 2. Expected directory and artifact organization

Illustrative tree. `[D…]`/`[C…]` refer to defects in 001 §3; `[S-…]` to shared invariants.

```text
<template root>/
├── CLAUDE.md                       always   V2 sections kept (Product Specification, Custom Settings, Core Defaults,
│                                            Development Workflow, Git), plus:
│                                            · Precedence                                        [S-06]
│                                            · Decision control: classes, R-1…R-10, five-question test, Decision Request,
│                                              headless behavior                                 [S-06; D1, C2–C4, C6]
│                                            · Adopted architecture (D-01…D-08) and patterns not adopted
│                                              (one consolidated list, moved from 7 places)      [S-07; D1]
│                                            · Completion contract (probe-to-test, review, verify) [D2]
│                                            · Workflow map                                       [S-11]
│                                            · @docs/technology-stack.md
├── SPECIFICATION.md                         unchanged (input)                                    [S-08]
├── CUSTOM_SETTINGS.md                       table + format note + pointer; restated policy removed [D7]
├── .editorconfig, Directory.Build.props, Directory.Packages.props                                [S-13]
├── docs/
│   ├── technology-stack.md         always (imported)  moved from skills/project-structure/references/;
│   │                                        approved stack and conditional technologies, D-09…D-23 [§2.3 inversion; D8, D15, D16]
│   └── decisions/                           ADRs                                                [S-07]
└── .claude/
    ├── MAP.md                      not loaded  flat table: one row per file                    [S-14]
    ├── settings.json, hooks/, scripts/      enforcement package E                               [S-13]
    ├── rules/                               flat; V2 names kept; every file declares paths      [S-09]
    │   ├── architecture.md         backend   layers, domain, application, API, composition root, simplicity;
    │   │                                     + naming by type role (from backend-layout.md)     [§3.3]
    │   │                                     − gate (→ CLAUDE.md) [D1]  − persistence (→ persistence.md) [D5]
    │   ├── persistence.md          Domain/Application/Infrastructure/Program.cs   NEW (split)
    │   │                                     repositories, UoW, EF boundary (from architecture.md);
    │   │                                     seeding policy, seed co-change, migration policy (from ef-core skill) [D3, D5, D17]
    │   ├── coding-style.md         backend .cs   + C# conventions restated in modern-csharp     [D19]
    │   ├── performance.md          backend .cs   cancellation owned here; duplicate removed from error-handling [D13]
    │   ├── error-handling.md       backend .cs   + outcome naming (from the skill); + default status codes and 401/403
    │   │                                     (from http-api / authentication) [§2.3 inversion, D22]; validation boundaries [D14];
    │   │                                     log-once owner [D12]
    │   ├── security.md             backend + config   narrower paths; Angular items → angular.md; FluentValidation
    │   │                                     mention → technology-stack [§2.3]; owner of D10 and D11; inert `description` removed
    │   ├── testing.md              backend tests   policy parts of the testing skill; one naming convention [C8];
    │   │                                     unclosed fence fixed [§3.6]
    │   ├── dependencies.md         manifests   normative hygiene only; procedure → add-dependency [D9]
    │   └── angular.md              frontend/**   NEW: principles, data-access boundary, state escalation, guards ≠ security,
    │                                     test placement and runner [S-10; D18]
    ├── skills/                              the shared skill set (S-11, S-12)
    │   │  workflows:  project-structure (+ explicit read steps for architecture.md and persistence.md), verify, code-review,
    │   │              build-fix, custom-settings, git-workflow, security-scan, add-dependency [NEW], architecture-decision [NEW],
    │   │              template-maintenance [NEW, user-only]
    │   │  knowledge:  ef-core (+ references/dev-seeding.md), http-api, aspnet-error-handling, dotnet-testing, logging
    │   │              (+ references/serilog.md), httpclient-factory (+ references/resilience.md), configuration,
    │   │              dependency-injection, caching, swagger, api-versioning, health-check, docker, ci-cd, angular,
    │   │              modern-csharp, authentication
    └── agents/code-reviewer.md     delegated   thin; preloads code-review                       [D23, C1]
```

The skill set, its names and its bodies are shared with every experimental candidate (S-11, S-12, 002 CV-3). The merges (serilog → logging, resilience → httpclient-factory) and the renames (002 §13 Q8) are central decisions. In M they are justified by competition and collision defects (001 §6.3, §3.3).

**Expected size:** about 45–50 runtime instruction files.

---

## 3. Dependency direction

M adopts only the shared minimum (S-05):

- Normative content depends only on owners that load reliably. A rule's "Related skills" footer is a routing pointer, never a source of policy.
- No engineering policy depends on product or task inputs.
- Skill references are private to their skill. `docs/technology-stack.md` is no longer a skill reference, which fixes 001 §2.3.
- Conformance dependencies are acyclic.

M has **no ordering among rules** and no rule about which file may cite which, beyond the above. This is intentional: M tests whether the minimum suffices.

---

## 4. Ownership model

- **One owner per inventory item** (S-01, S-02), assigned by lineage: the V2 owner, unless a defect required moving the item.
- **Tie-break** when V2 had several copies (D1–D24): the copy in the most reliably loaded file whose trigger matches the item becomes the owner. The others become pointers or check-by-reference items. For D2 and D3, that owner is the `CLAUDE.md` completion contract and `persistence.md`, respectively.
- The ownership table lives in `.claude/MAP.md` (S-14). It has one row per file and one column listing the inventory IDs that file owns.

---

## 5. Loading strategy

Loading follows the shared trigger assignment (S-09):

| Trigger class | M carrier |
|---|---|
| Always | `CLAUDE.md` and the imported `docs/technology-stack.md` |
| Path | The 9 rules above, each with `paths` (V2's 7 plus `persistence.md` and `angular.md`) |
| Hook | H1–H4 from the shared package (S-13) |
| Explicit workflow step | The read steps in `project-structure`, `verify` and `code-review` (for greenfield work and subagents) |
| On-demand knowledge | Knowledge skills and their references |

M keeps V2's coarse path scopes where no defect requires narrowing them. For example, `performance.md` and `error-handling.md` still match all of `backend/**/*.cs`. This is the expected reason M loads more context per backend edit than K0. It is a measured outcome, not a confound (002 CF-17).

---

## 6. Responsibilities of skills, rules and references

| Mechanism | Responsibility in M |
|---|---|
| `CLAUDE.md` | Operating policy and every always-loaded decision except the stack |
| `docs/technology-stack.md` | Approved stack and conditional technologies (imported) |
| Rules | Normative constraints for the files they match. No procedures. A "Related skills" footer. |
| Workflow skills | Procedures with check-by-reference items. No restated policy. |
| Knowledge skills | Technique only. Policy statements are removed or reduced to pointers. |
| References | Depth private to their skill |
| Agent | Execution context; preloads `code-review` |

M does **not** declare workflow and knowledge as formal categories. They are separate files because of S-04, but nothing in M's structure names the distinction.

---

## 7. Project decisions

- **Always loaded** (S-07):
  - the architecture decisions and the list of patterns not adopted, in `CLAUDE.md`;
  - the stack and conditional technologies, in `docs/technology-stack.md`.

  Both carry the shared IDs (D-xx, R-x).
- **Changing a decision** goes through `architecture-decision` (S-11): a Decision Request, then an ADR in `docs/decisions/`, then edits to the two always-loaded files and to the dependent rules. Dependents are found through the map, since M has no "Affects" column.
- **Project-specific additions** go into the most closely related existing rule, or into a new flat rule `rules/project-<topic>.md` with `paths`.

---

## 8. How feature and task inputs interact with policy

The text is identical to every other candidate (S-08, S-06). In M it lives where V2 put it: the `CLAUDE.md` sections Product Specification and Custom Settings, plus the new Precedence and Decision control sections.

Feature specs are optional, at `docs/features/*.md`, and linked from `SPECIFICATION.md`. They may request a decision change but never grant one.

---

## 9. Expected extension points

| To add or change | Expected edits in M |
|---|---|
| A project rule | The topically closest rule, or a new `rules/project-<topic>.md`, plus a map row |
| A technology | `docs/technology-stack.md`, plus a knowledge skill, plus a rule section if new must-rules arise, plus a map row |
| A decision | `architecture-decision`: ADR, `CLAUDE.md` or `technology-stack.md`, dependents found via the map |
| A workflow | A new skill, a line in the `CLAUDE.md` workflow map, a map row |
| Replace a technology | Grep and edit wherever it is named; expected about 5 files for NUnit → xUnit (002 §11) |

---

## 10. Structural conformance (what S2 checks for M)

- The shared checks:
  - every rule declares `paths`;
  - always-loaded content is reachable via imports;
  - every file is in the map;
  - references resolve;
  - every check-by-reference item points to an existing owner section;
  - skill descriptions are within length;
  - no unclosed fences;
  - imperative lines in knowledge skills produce a warning.
- **The lineage check** (P-07): every file maps to a V2 file, or carries a justification ID.
- **The absence checks**: no `Level:`, `Kind:` or `Capability:` headers; no rule subdirectories; no contracts or selection record.

---

## 11. Important risks

| Risk | Why it is specific to M | Consequence |
|---|---|---|
| Content drifts back into duplication | No systemic rule for placing new content | Long-term maintainability may decay toward V2 (002 §10) |
| Convergence with K0 (002 CV-6) | K0 was derived from fixing the same defects | Behavioral differences between M and K0 may disappear. This is a legitimate and important finding. |
| Keeping V2 lineage keeps some coarse triggers | `performance.md` and `error-handling.md` load on every backend `.cs` file | More context per edit than K0 or L0 |
| `CLAUDE.md` grows | Decision content added to an existing always-loaded file | It approaches the S-18 ceiling; check E8 |
| Under-fixing | Problems no defect ID names stay unfixed | Shown by the trigger suite and the inventory mapping |
| Over-fixing | An implementer "improves" M toward K0 or L0 | Breaks the purpose of M. Watch for the leakage signs below. |

---

## 12. Leakage watchlist: signs that an implementation is no longer M

- Rule subdirectories by scope (K), by level (L), or by capability (B1).
- Classification metadata beyond the shared ownership header.
- A separate decision-register file that merges the architecture decisions with the stack, or an "Affects" column. This is K's representation; M keeps V2's two locations.
- Technology-neutral rewording of rules "for stability". This is L's representation.
- Contracts, module manifests or a selection record (B1).
- Any file without lineage or justification.
