# K0 — Kinds × Scopes, Embedded Capabilities: Design Notes

> **Research metadata.** This file is not part of any candidate's instruction context (S-19). Never copy it into a template or a benchmark project.

| | |
|---|---|
| Candidate | **K0**: Kinds × Scopes with embedded capabilities |
| Axis A | A-K: Kinds × Scopes |
| Axis B | B0: embedded capabilities |
| Passport | `research/candidates/K0/CORE_FEATURES.md` |
| Shared invariants | S-01…S-19, defined in `research/observations/002-candidate-space-analysis.md` §2 (hereafter "002") |
| Origin | The organization proposed in `research/observations/001-v3-design-proposal.md` §4–§8. The parts of 001 that do not depend on Kinds × Scopes (decision control, planning-time decisions, enforcement, reference forms, the map) are now shared invariants and give K0 no advantage. |
| Distinguishing predicates (002 §3.4) | P-04, P-05, P-06 **yes**; P-08 yes; P-01…P-03, P-07, P-09…P-13 **no** |
| B1 sibling | K1 (= K0 plus the capability transformation on the slot set; P-14) |
| Status | Design only. Illustrative trees, not final files. |

**Notation.** 001 named its kinds K1–K7. Here they use letter codes, so they do not clash with candidate K1: `OP`, `DEC`, `STD`, `KNW`, `WF`, `ENF`, `IN`.

---

## 1. The kind and scope model

### 1.1 Kinds

The kind says what responsibility an artifact has. The kind decides its mechanism, its location and who may change it.

| Kind | Responsibility | Mechanism | Location | Changed by |
|---|---|---|---|---|
| **OP** Operating policy | How Claude works: precedence, decision control, product governance, completion contract, challenge obligation, Git | Always | `CLAUDE.md` | Template maintainers |
| **DEC** Project decisions | What the project decided: architecture style, patterns adopted and not adopted, approved stack, conditional technologies, reserved items | Always (imported) | `docs/architecture/decision-register.md` (+ ADRs in `docs/decisions/`) | Humans, via ADR |
| **STD** Standards | Normative constraints for work in one scope; they implement DEC | Path | `.claude/rules/<scope>/<topic>.md` | Template maintainers; a project adds `project-*.md` |
| **KNW** Knowledge | Technique, examples and trade-offs *within* adopted decisions; never originates policy | On demand (model-invoked) | Knowledge skills and their references | Template maintainers |
| **WF** Workflows | Procedures with steps, checks, outputs and stop conditions | Explicit, by user, pointer or hook | Workflow skills, plus the `code-reviewer` agent | Template maintainers |
| **ENF** Enforcement | Deterministic triggers and checks | Events and tooling | `settings.json`, hooks, scripts, root assets, scaffold assets | Template maintainers and the project |
| **IN** Product inputs | Behavior, values, feature specs, tasks | Read on instruction | `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, `docs/features/`, prompts | Product owner or user |
| *(meta)* | The map and the instruction-structure checker | Never loaded | `.claude/MAP.md`, scripts | Template maintainers |

In every candidate the *trigger class* of each inventory item is fixed by S-09. **In K0 the kind and the trigger class coincide by design.** Knowing the kind tells you how the artifact loads. This is K0's defining practical property, and what distinguishes it from L0, where one level contains several mechanisms.

### 1.2 Scopes

`common`, `backend`, `backend-tests`, `frontend`, `delivery`, `repo/meta`. These are the shared taxonomy and globs (S-10). **In K0, scope is a primary directory axis for STD**, and a declared field for every other kind.

### 1.3 Classifying content

001 §6.4, adapted. Apply the questions in order; the first "yes" decides.

1. Is it a project choice or an approval boundary? → **DEC**
2. Is it agent behavior whose obligation does not depend on a file path? → **OP**
3. Is it normative for work on certain files? → **STD**, in the matching scope
4. Is it a multi-step procedure? → **WF**. Add an ENF hook if the moment can be detected, and explicit read steps if it must work in greenfield projects or subagents.
5. Is it technique or depth? → **KNW**
6. Is it mechanically checkable? → **ENF**. Keep it in STD as well if knowing it improves generation.
7. Is it a product statement? → **IN**

**Mixed statements are split by kind.** Example: V2's `ef-core` skill becomes:

- DEC "D-04 persistence";
- DEC "D-05 data lifecycle";
- STD `backend/persistence.md`: repositories, Unit of Work, EF boundary, seeding obligation;
- KNW `ef-core`: technique;
- KNW reference `dev-seeding.md`: the seeder code.

**Unlike L0, K0 does not split a statement merely because it names a technology.** STD rules may name EF Core, NUnit or Angular directly. A split happens only when *responsibility* or *trigger* differs.

---

## 2. Expected directory and artifact organization

Illustrative tree. It follows 001 §4.5, with the kind codes and the shared skill names (002 §13 Q8).

```text
<template root>/
├── CLAUDE.md                              OP   always     precedence, decision control, product governance,
│                                                          completion contract, challenge, workflow map, Git;
│                                                          @docs/architecture/decision-register.md
├── SPECIFICATION.md, CUSTOM_SETTINGS.md   IN
├── .editorconfig, Directory.Build.props, Directory.Packages.props        ENF assets [S-13]
├── docs/
│   ├── architecture/decision-register.md  DEC  always (imported)   D-01…D-23, reserved items, "Details in", "Affects"
│   ├── decisions/                         DEC  not loaded          ADRs
│   └── features/                          IN   optional            feature specs, linked from SPECIFICATION.md
└── .claude/
    ├── MAP.md                             meta not loaded   organized as a kind × scope grid  [S-14]
    ├── settings.json, hooks/, scripts/    ENF  package E [S-13]
    ├── rules/                             STD  every file declares paths
    │   ├── common/
    │   │   ├── security.md                     secrets, sensitive data in logs, error exposure, TLS
    │   │   └── dependencies.md                 CPM, pinned stable versions, lockfiles, narrow references
    │   ├── backend/
    │   │   ├── architecture.md                 layers, references, responsibilities, composition root, naming by role
    │   │   ├── persistence.md                  repositories, Unit of Work, EF boundary, migrations, seeding + seed co-change
    │   │   ├── api.md                          thin Controllers, status-code defaults, ProblemDetails, contract authority
    │   │   ├── error-handling.md               outcomes vs exceptions, central handling, log once, validation boundaries
    │   │   ├── csharp.md                       conventions, async, cancellation, TimeProvider, HttpClient lifetime
    │   │   └── security.md                     input trust, SQL, server-side authorization, CORS, data protection
    │   ├── backend-tests/
    │   │   └── testing.md                      NUnit, test levels, test doubles, database tests, isolation, naming
    │   ├── frontend/
    │   │   └── angular.md                      standalone, feature structure, data-access boundary, state, guards ≠ security, tests
    │   └── delivery/                           (none planned; common/security applies to containers and CI)
    ├── skills/                            shared set (S-11, S-12); kind in header
    │   │  WF:  project-structure, verify, code-review, build-fix, add-dependency, custom-settings, architecture-decision,
    │   │       security-scan, git-workflow, template-maintenance (user only)
    │   │  KNW: ef-core, http-api, aspnet-error-handling, dotnet-testing, logging, httpclient-factory, configuration,
    │   │       dependency-injection, caching, swagger, api-versioning, health-check, docker, ci-cd, angular, modern-csharp,
    │   │       authentication
    └── agents/code-reviewer.md            WF   delegated   thin; preloads code-review
```

**Expected size:** about 50–55 runtime instruction files: 10 STD rules, about 27 skills, plus `CLAUDE.md`, the register, the map, ENF and IN files.

---

## 3. Dependency direction

```text
IN ──(may request changes to)──► DEC   (never overrides it)

WF ──► KNW ──► STD ──► DEC ──► OP
 │                ▲
 └─(explicit "read rule X" steps)─┘

ENF ──(implements / checks)──► STD, DEC     (hook messages name the owning file)
Agents ──► WF / KNW                         (they preload; they have no criteria of their own)
Skill references ──► private to one skill
```

- The kind graph is the conformance-dependency rule. STD conforms to DEC; KNW conforms to STD and DEC; WF conforms to all of them.
- Routing pointers in the reverse direction are allowed (S-05). Examples: OP's workflow map → WF, and an STD rule's "Related skills" → KNW.
- **K0 has no stability ordering of its own.** An STD rule may name a technology. A DEC entry may name a technology. Stability appears only indirectly, through the kind graph: DEC and OP are the stable end.

---

## 4. Ownership model

- **The owner is chosen by kind first, then scope, then topic.** One owner per inventory item (S-01).
- The detailed owner table is 001 §5.2. Rows that concern shared invariants (precedence, decision control, product governance, completion contract) are owned by OP in K0, just as they are owned by `CLAUDE.md` in every other candidate.
- **The register (DEC) owns every decision summary** (P-06). STD rules cite IDs such as "(D-04)" instead of restating choices.
- **An embedded technology is spread across kinds.** NUnit appears in DEC (D-15), STD (`backend-tests/testing.md`), KNW (`dotnet-testing`), WF (scaffold steps) and ENF (the architecture-check asset). No single unit owns "NUnit". This is the defining B0 property of K0.

---

## 5. Loading strategy

| Kind | Trigger class |
|---|---|
| OP, DEC | Always (`CLAUDE.md` plus an import) |
| STD | Path, by scope directory and `paths` |
| WF | Explicit: the user, a workflow-map pointer, a hook message (H1, H3, H4), or the agent preload |
| KNW | On demand; "Related skills" footers make triggering more likely; never carries policy |
| ENF | Events: permissions, hooks, tooling |
| IN | Read on instruction (OP tells Claude when) |

Expected loading by task type: 001 §6.5. Those figures depend on the shared invariants and apply to every candidate. K0's own contribution is the **scope-precise STD split**: `persistence.md` loads for the Domain, Application and Infrastructure projects, and `api.md` for the Api project. This gives the best expected loading precision among the candidates (002 §1, item 8).

---

## 6. Responsibilities of skills, rules and references

- **WF and KNW are distinct kinds** (prompt 002 §3, K0): different header, different rules for allowed content, different invocation expectations.
- **STD rules contain:** must, default and prefer statements, each with a one-line rationale; compact decision tables; a "Related skills" footer.
- **STD rules do not contain:** procedures; long examples; decisions (they cite DEC IDs).
- **References** are private to one skill. Content that other artifacts depend on is promoted to STD or DEC.

001 §5.3 and §7 give the full may-contain / must-not-contain table.

---

## 7. Project decisions

- **The register is the single decision artifact** (P-06), imported into `CLAUDE.md`. Each entry has: ID, area, decision, "Details in", "Affects".
- The **"Affects" column** lists the dependent STD, KNW, WF and ENF files. `architecture-decision` updates exactly those files.
  - The column is loaded with the register (always), so its cost counts against S-18.
  - If it improves how Claude propagates a decision at runtime, that is an effect of representing decisions as a kind, not a confound. It must not contain policy text.
- **Reserved classes** R-1…R-10 and the protocol: OP (S-06). Architecture-specific "not adopted" items: DEC.

---

## 8. How feature and task inputs interact with policy

- **IN is a kind, not a layer.** Inputs may define behavior and request decisions, but never grant them (S-08, S-06).
- Optional feature specs at `docs/features/*.md`, linked from `SPECIFICATION.md`.
- When a feature needs a Reserved decision, the DEC change goes through the protocol. Once approved, the decision lives in the register, not in the feature spec (001 §9.7).

---

## 9. Expected extension points

These follow 001 §4.7, restated in kind terms.

| To add or change | Expected edits in K0 |
|---|---|
| A technology | A DEC entry plus an ADR; KNW (new or existing); an STD section only if new must-rules arise; a map row |
| A decision | `architecture-decision`: ADR, DEC, plus the files in its "Affects" column |
| A project rule | A new STD `rules/<scope>/project-<topic>.md`, plus a map row |
| A workflow | A new WF skill, plus a workflow-map line in OP if it must be invoked automatically |
| A frontend concern | STD `frontend/angular.md` or a new `frontend/<topic>.md` |
| Replace a technology (embedded) | Every kind where it appears: DEC, STD, KNW, WF steps, ENF assets. About 5 for NUnit → xUnit, across 4 kind locations (002 §11). The "Affects" column lists them. |

---

## 10. Structural conformance (what S2 checks for K0)

- The shared checks (see M DESIGN §10).
- **P-04**: every file has `Kind:` and `Scope:` headers, and the kind matches the mechanism and location.
- **P-05**: STD files live in `rules/<scope>/`, and their `paths` fall within the scope's globs.
- **P-06**: decision summaries appear only in the register; STD rules cite IDs.
- **Kind-content heuristics**: imperative lines in KNW produce a warning; procedures in STD produce a warning.
- **The "Affects" column resolves**: every listed file exists, and every file that cites an ID appears in that entry's "Affects".
- **Absence checks**: no `Level:` headers or level directories (L); no contracts or selection record (B1).

---

## 11. Important risks

| Risk | Detail | Indicator or test |
|---|---|---|
| Fuzzy kind boundaries | "Development-only seeding": DEC or STD? "No auto-migration in Production": DEC, STD or OP? | Classification disagreements; CI-1 |
| Learning cost of the taxonomy | 7 kinds × 6 scopes | Time and errors in CI-1 and CI-10 |
| The register grows | Always-loaded cost rises with every decision | S-18; E8 |
| "Affects" goes stale | Dependents are added without updating the register | S2 check; CI-2 missed mentions |
| Technologies are spread across kinds | Embedded replacements touch 4–5 kind locations | CI-4…CI-7 |
| Per-layer globs | Depend on project naming (shared; S-10) | Same in all candidates |
| Convergence with M and L0 (002 CV-5, CV-6) | Fixing the same defects, or splitting by rate of change, yields similar files | Structural distance; report it |

---

## 12. Leakage watchlist: signs that an implementation is no longer K0

- **Toward K1:**
  - capability contracts, module manifests or a slot-selection section in the register;
  - facet files named by slot;
  - workflows reaching technology steps through slots.
- **Toward L:**
  - `Level:` headers;
  - technology-neutral rewording of STD rules (P-03 style) not forced by a responsibility split;
  - stratified decision files.
- **Toward M:** dropping the kind and scope metadata or directories, or keeping V2 topic files merely for lineage.
