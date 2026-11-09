Kind: DEC | Scope: backend | Capability: architecture (slot contract) | Loading: on demand (workflows, maintainers)

# Capability Contract: architecture

Required **frame**. Exactly one implementation is selected in the decision register. The frame owns **placement**: layer roles, dependency direction, use-case orchestration, commit-boundary placement, HTTP entry points, the composition root, backend project placement and backend test-project placement. Technique belongs to the leaf capabilities: placement belongs to the frame, technique belongs to the leaf.

## Stable role vocabulary

Leaf capabilities and neutral standards use these role names, never the frame implementation's name.

| Role | Meaning |
|---|---|
| Domain | business concepts, independent of infrastructure and transport |
| Application | use-case orchestration; defines the ports its use cases need |
| Infrastructure | implementations of ports: persistence and external adapters |
| Api | ASP.NET Core host: HTTP entry points and composition root |
| persistence port | Application-defined repository contracts |
| commit boundary | Application-facing abstraction that decides when a use case commits |
| persistence area | the Infrastructure location that hosts the persistence leaf's implementation |
| test projects | per-layer backend unit-test projects and the integration-test project |

## Required facets

| Kind | Facet | Location |
|---|---|---|
| DEC | selection, declared properties, styles not adopted | decision register → Capability selection |
| STD | style standards | `.claude/rules/backend/architecture-style.md` |
| WF | backend layout, scaffolding, project references, test-project placement | `workflow-facet.md` in the module directory |
| ENF | role map and allowed project/package references for `.claude/scripts/check-architecture.mjs`, test co-change patterns | `.claude/scripts/facets/architecture/enforcement.json` |

## Required declared properties

Style name, layer roles and their project suffixes, use-case orchestration mechanism, commit-boundary abstraction, and the styles explicitly not adopted.

## Replacement

Replacing the frame is Reserved because it changes every layer boundary. After approval, follow the `template-maintenance` workflow: create the new module with every required facet, re-check the `binds:` declarations of the leaf modules, update the register, remove the old module and its facets, and run the instruction-structure checker.
