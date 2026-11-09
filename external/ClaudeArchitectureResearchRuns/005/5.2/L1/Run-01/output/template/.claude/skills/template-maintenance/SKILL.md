---
name: template-maintenance
description: >
  Maintain the instruction system itself: add or relocate a rule, add a workflow
  or knowledge skill, replace or clear a capability module, change a provider
  variant, update the instruction map, run the structure checker.
disable-model-invocation: true
---
> Level: 3-project | Owns: instruction-system maintenance procedure (user-invoked only) | Scope: repo/meta | Loads: user-invoked only (/template-maintenance)

# Template Maintenance

The maintainer map is `.claude/INSTRUCTION-MAP.md`. After every change run:

```bash
node .claude/scripts/check-instructions.cjs
```

## Placement principles

- **One owner.** Each normative rule has exactly one authoritative owner.
  Elsewhere use only a routing pointer ("run `verify`"), a short
  check-by-reference item, or — only in the capability selection record — a
  decision summary.
- **Level** (first match wins): project-specific selection, layout, or default
  → `3-project`; concrete non-platform technology → `2-technology`; adopted
  architecture, role, or boundary → `1-architecture`; otherwise `0-core`.
  Conformance dependencies point only to the same or a more stable level.
- **Platform vocabulary.** `0-core` and `1-architecture` artifacts name no
  concrete technology except the fixed platform vocabulary: .NET, C#, the
  `dotnet` CLI, NuGet/MSBuild, ASP.NET Core and its built-in primitives
  (Controllers, middleware, DI, options/configuration, `ILogger<T>`,
  `IHttpClientFactory`, `ProblemDetails`, `IExceptionHandler`, health checks,
  Data Protection, authentication/authorization/Identity,
  `WebApplicationFactory`), `TimeProvider`, HTTP/TLS/OIDC/OpenAPI standards, and
  Git.
- **Trigger.** Planning-time policy → a rule imported by `CLAUDE.md`;
  file-scoped policy → a path-scoped rule (every rule declares `paths`
  covering at least its scope); procedures → workflow skills; technique →
  knowledge skills (never the sole owner of a must-rule); mechanical checks →
  hooks/scripts, with the critical boundary still stated in a rule.
- **Leak rule.** Outside its module, nothing names a capability implementation
  (framework, library, provider) except the capability selection record and
  this map. Workflows reach implementation-specific steps through facet roles
  (`<slot>.<facet>`). Facet files are named by role, not implementation. Every
  module manifest declares `binds:` and `leak terms:` (the names the structure
  checker keeps inside the module).

## Add a rule

1. Choose the level and scope; pick the existing file whose concern matches
   (map: "Where new content goes") or create a narrowly named file.
2. Add YAML `paths` and the one-line header
   (`> Level: … | Owns: … | Scope: … | Loads: …`, plus `Capability:` for module
   facets).
3. Replace any duplicate wording elsewhere with a pointer; update the map.

## Add a skill

Workflow skills own procedures; knowledge skills own technique with
trigger-first descriptions and concrete cues. Add the header line after the
frontmatter and list the skill in the map.

## Replace a capability implementation

Changing a selection is Reserved: an accepted ADR must exist
(`architecture-decision`).

1. Read the slot `CONTRACT.md`; create `.claude/capabilities/<slot>/<new>/`
   with `MODULE.md` and every required facet (rules and skills in their normal
   locations, with `Capability: <slot>/<new>` headers; procedural and data
   facets in the module directory).
2. Update the capability selection record (selected implementation, knowledge
   skill, declared properties) and the decision import in `CLAUDE.md`.
3. Delete every facet listed in the old module's `MODULE.md`, then the old
   module directory — only one implementation per slot may ship — and update
   the slot's rows in the capability view of `.claude/INSTRUCTION-MAP.md`.
4. Run the checker; fix leaks or missing facets.

## Clear the optional frontend

Follow "Clearing the selection" in `.claude/capabilities/frontend/CONTRACT.md`.

## Change the persistence provider variant

Record the ADR, then update the persistence module's decision, rules, workflow,
scaffold, and declared properties (string-comparison semantics and relational
test fidelity included) and the selection record. Observable string-semantics
changes need product approval.

## Hooks and scripts

Hook commands in `.claude/settings.json` start Node through a shell-neutral
bootstrap that resolves the project directory inside Node; never use shell
variable expansion in hook commands. Exercise a changed hook by piping a sample
JSON payload into it, for example
`node .claude/hooks/dependency-guard.cjs < sample.json`.
