# V2 — Frozen Baseline: Core Features

> **Research passport.** This is human-facing research metadata. It is not part of any candidate's Claude instruction context, and benchmarks must never rely on it (S-19).

| | |
|---|---|
| ID | **V2** |
| Role | Experimental control |
| Definition | The files in `templates/v2-baseline/`. **Frozen: never modify them.** |
| Axis A / Axis B | Neither: an ad hoc topic organization, with embedded capabilities |
| Shared invariants S-01…S-19 | **None** (by construction) |
| Note | As of 2026-10-02, `templates/v3/` is a byte-identical copy of V2. It is not one of the six candidates. |

## 1. Core idea

CleanArchitectureTemplate V2 exactly as it was used before this research. It is the reference point every other candidate is measured against.

## 2. Primary decomposition model

There is no explicit principle. Content is organized **by topic or technology**, on Claude Code's native mechanisms:

- `CLAUDE.md` (always loaded, 122 lines);
- 7 rules, **all path-scoped** (none always loaded);
- 26 skills (frontmatter: `name` and `description` only);
- 4 skill references;
- 1 agent.

## 3. Capability composition model

Embedded. Technologies are named wherever they are needed. The approved stack lives in a skill reference (`skills/project-structure/references/technology-stack.md`), which a rule depends on (`rules/dependencies.md:17-19`).

## 4. Distinguishing features (identification facts, Observed)

- 41 files, about 10.7k lines (about 74k tokens, 001 §2.1).
- The architecture rule is path-scoped to `backend/**/*.cs` and `*.csproj`, so it is absent during planning.
- The approval gate is in `rules/architecture.md:152-178`. Its pattern lists are repeated, and disagree, in 7 artifacts (001 D1).
- Normative policy also lives in model-invoked skills: `ef-core` (seeding), `angular` (all frontend policy), `error-handling` and `testing`.
- The `code-reviewer` agent has `disallowedTools: Write, Edit` and restates the review criteria (001 C1).
- **No** `settings.json`, hooks, permissions, commands, `.editorconfig`, analyzers or architecture tests.
- `SPECIFICATION.md` is empty; `CUSTOM_SETTINGS.md` has an empty table. Both are intentional.
- Stack: .NET 10 / C# 14, ASP.NET Core Controllers, EF Core with SQL Server, FluentValidation, Serilog, Swashbuckle, NUnit, Angular with Vitest and Material; Mapster, Microsoft resilience packages, Testcontainers and Playwright are conditional.

## 5. Main hypothesis

The control, with no hypothesis of its own. Every comparison tests: *"Does changing the instruction architecture improve on V2?"*

## 6. What this candidate intentionally does NOT contain

- Any shared invariant: no policy inventory, no decision-control protocol, no always-loaded decisions, no enforcement package, no instruction map, no reference-form rules.
- Any meta-architecture (levels, kinds, scopes) or capability mechanism.
- A path-scoped Angular rule.

## 7. Expected strengths

- Strong, carefully reasoned content: the stance against over-engineering, an approval gate with an autonomy clause, product governance (string-comparison semantics), honest verification ("NOT RUN"), and dependency hygiene.
- Low indirection; everything about a topic sits in one or two files.
- Proven in real use.

## 8. Expected weaknesses

- Critical policy sits behind triggers that may not fire (architecture during planning, seeding, Angular, HTTP status codes).
- Compensatory duplication that is already drifting (C1, C8).
- No deterministic enforcement.
- Mixed responsibilities in single files (`ef-core`, `build-fix`, `technology-stack.md`).

## 9. Closest comparison candidates

**M** (the direct comparison). Every other candidate, for the total effect.

## 10. Experimental factors isolated by those comparisons

- **V2 vs M:** the shared bundle plus conventional cleanup. These two are confounded unless the M−E or V2+E ablation runs (002 §3.6).
- **V2 vs any:** the total effect of that candidate.
