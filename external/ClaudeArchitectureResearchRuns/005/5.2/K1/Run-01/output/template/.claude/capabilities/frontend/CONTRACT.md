Kind: DEC | Scope: frontend | Capability: frontend (slot contract) | Loading: on demand (workflows, maintainers)

# Capability Contract: frontend

Optional **leaf**: zero or one implementation. Provides the browser frontend in `frontend/<Name>.Web/`, which consumes the backend's published HTTP contract. binds: — (the HTTP API contract is non-slot).

## Role vocabulary

| Role | Meaning |
|---|---|
| frontend workspace | `frontend/<Name>.Web/` with its own package manifest, lockfile and tests |
| data-access service | the feature-level HTTP boundary to the backend |
| structured form mechanism | the framework's explicit form-state and validation model |
| HTTP pipeline configuration | the framework's cross-cutting request/response hooks |
| route-level lazy loading | the framework's per-feature code-splitting mechanism |

## When selected, an implementation must provide

| Kind | Facet | Location |
|---|---|---|
| DEC | stack, libraries not added by default, conditional E2E tool | decision register → Capability selection |
| STD | role bindings and framework-specific standards | `.claude/rules/frontend/frontend-framework.md` |
| KNW | framework technique | knowledge skill named in the register |
| WF | scaffolding, build/test/dev-server commands, build-fix diagnostics, API client generation, E2E placement, security review cues | `workflow-facet.md` in the module directory |
| ENF | dependency-command patterns, npm approval watch-list, co-change patterns | `.claude/scripts/facets/frontend/enforcement.json` |

Neutral frontend policy stays in `.claude/rules/frontend/frontend.md` and must keep holding after a replacement.

## Selecting "none" or replacing

Both are Reserved. For "none", remove the module, its facets and `.claude/scripts/facets/frontend/`, set the register row to `none`, and keep `.claude/rules/frontend/frontend.md` for a possible later selection. For a replacement, follow `template-maintenance` and provide every facet above.
