<!-- Kind: OP | Scope: common | Owns: operating policy — precedence, product governance, decisions, challenge, completion, Git safety, routing | Loads: always -->
# Operating Policy

Template for ASP.NET Core + Angular applications. This file and the imported decision register load at session start; standards in `.claude/rules/<scope>/` load when matching files are read; workflow and knowledge skills load when invoked. Human map of the instruction system: `.claude/MAP.md`.

@docs/architecture/decision-register.md

## Vocabulary

**must / must not** — violation is a defect. **default** — deviate only for a concrete reason and report the deviation. **prefer / avoid** — guidance. **requires approval** — Reserved decision (§ Decisions).

## Precedence

1. Explicit user instructions for the current task. An instruction that changes a Decided or Reserved matter counts as approval only when it is explicit; record it with `architecture-decision`.
2. This operating policy and the decision register.
3. Standards in `.claude/rules/` for the touched scope.
4. Workflow skills (procedure) and knowledge skills (technique); they never override 1–3.

Product inputs define product behavior and values. They may request an engineering decision change but never silently override engineering policy.

## Product Inputs

- `SPECIFICATION.md` — when non-empty, the authoritative source for project-specific functional requirements and observable product behavior. It is empty in the template by design.
- `CUSTOM_SETTINGS.md` — approved project-level tunable product limits and defaults (maximum lengths, page sizes, retention periods, thresholds) **must** be recorded here; `SPECIFICATION.md` owns behavioral intent, `CUSTOM_SETTINGS.md` the concrete values.
- Feature specifications and task prompts — inputs to the current work, not instruction layers.

Rules:

- **Must not** silently weaken, contradict or materially extend approved behavior, or invent user-visible behavior, limits, defaults, restrictions or workflows because they seem reasonable.
- An omitted detail that must be decided and materially affects observable behavior **requires approval**: propose the smallest reasonable option and ask.
- String semantics are product behavior when observable: case sensitivity, collation, culture vs ordinal comparison, normalization, trimming, uniqueness and lookup. When product sources are silent and the choice affects equality, uniqueness, lookup or accepted input, it **requires approval** — never choose silently, including through database collation or framework defaults.
- `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` **must not** contradict each other; on conflict, stop and ask which source to correct.
- A tunable value that materially changes accepted input or observable behavior and is not already defined by the specification, existing approved behavior or `CUSTOM_SETTINGS.md` **requires approval**: propose it with its reason, record it after approval, then run `custom-settings`.
- **Never** put secrets, environment-specific connection details, package versions, HTTP status codes, ports, migration identifiers or incidental implementation constants in `CUSTOM_SETTINGS.md`.

## Engineering Defaults

- **Default:** the simplest maintainable solution, with architectural complexity proportional to current requirements and no speculative abstractions.
- **Must not** introduce frameworks, libraries, infrastructure or architectural patterns without a concrete current need.
- **Must** keep changes focused on the requested scope and preserve existing behavior unless the task or approved specification requires a change.

## Decisions

- **Decided** — recorded in the decision register, required by the specification, or established by the existing project structure: follow it; reopening it requires approval.
- **Delegated** — routine, local, reversible choices that change no boundary, dependency, accepted convention, public contract or observable behavior: decide without approval.
- **Reserved** — **requires explicit approval** before implementation:
  1. changing an accepted project or architecture decision;
  2. a new architectural style or pattern — Rich Domain Model or DDD tactical patterns, CQRS, MediatR or another mediator, Vertical Slice Architecture, event sourcing, a project-wide Result model, microservices;
  3. a new production project, layer or assembly, or a change to the project reference graph;
  4. persistence boundaries or technology, including multiple `DbContext`s;
  5. a new infrastructure category — messaging, background processing, distributed cache, search, external storage, external identity;
  6. a major library or framework, or replacing an approved baseline technology;
  7. a project-wide convention or abstraction other code is expected to follow;
  8. authentication/authorization architecture;
  9. a breaking public API change or adopting API versioning;
  10. product behavior or tunable values not defined by product sources (§ Product Inputs).
- Unclear case — any "yes" makes it Reserved: (1) adds, removes or replaces a dependency, framework or infrastructure capability? (2) changes a project, layer or reference boundary? (3) establishes a convention other code is expected to follow? (4) changes observable behavior or a public contract? (5) expensive to reverse once other code depends on it?
- A Decision Request states **Context**, **Options**, **Recommendation**, **Blocked** and **Proceeding with**. Procedure and recording: `architecture-decision`.
- Autonomous or headless runs: take only a policy-compliant non-Reserved path, **never** make a Reserved decision silently, and report every unresolved Decision Request.

## Challenge Before Implementing

Before implementing a questionable request, **must** name the concrete concern — duplication, poor cohesion, trigger or loading problems, context cost, architecture conflict, unnecessary complexity — and propose an alternative. This never authorizes silently rewriting or ignoring the user's requirement.

## Completion

Implementation work runs `development-workflow`; it reads the product inputs, routes substantial work through `code-review`, and ends with `verify` before anything is declared complete. Report what was verified, what was not run, and any open Decision Requests.

## Git Safety

- **Must not** commit, push, merge, rebase, reset, force-push, delete branches or perform any other repository-changing Git operation unless explicitly requested; requested operations follow `git-workflow`.
- **Must** keep unrelated changes out of the current branch; parallel implementation work **must** use separate branches or worktrees.

## Routing

| Situation | Run |
|---|---|
| Feature, bug fix, refactor, performance change, new application | `development-workflow` |
| New solution or project, project references, structural reorganization | `project-structure` |
| Add, update or remove a NuGet or npm package | `add-dependency` |
| Reserved or unclear decision; recording an approved decision | `architecture-decision` |
| `CUSTOM_SETTINGS.md` value added, changed or removed | `custom-settings` |
| Failing build or tests | `build-fix` |
| Review of a diff, PR or completed work | `code-review` or agent `code-reviewer` |
| Before declaring work complete | `verify` |
| Security audit or security-sensitive review | `security-scan` |
| CI/CD pipeline, deployment, production migrations | `delivery-pipeline` |
| Requested Git operation | `git-workflow` |
| Changing the instruction system (user-invoked) | `template-maintenance` |
