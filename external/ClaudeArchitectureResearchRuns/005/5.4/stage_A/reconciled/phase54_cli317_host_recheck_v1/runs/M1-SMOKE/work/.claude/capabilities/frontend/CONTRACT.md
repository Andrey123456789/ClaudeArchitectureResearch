> Capability contract: frontend · Leaf slot (optional) · Maintainer metadata · Not auto-loaded; read during capability maintenance

# Capability Contract: frontend

## Purpose

The optional frontend leaf supplies the web frontend framework:
framework-specific rules and role bindings, knowledge, scaffold and build/test
command notes, and selected-technology decisions. Framework-independent frontend
policy (feature structure, presentation focus, HTTP boundary, API errors, state,
routing, validation authority) stays in `.claude/rules/frontend.md` outside the
module. The workspace location belongs to the architecture frame.

Clearing the selection removes the module's facets and its planning import;
nothing outside the facets listed in the manifest needs to change.

## Role Vocabulary Exposed to Other Instructions

| Role | Meaning |
|---|---|
| feature data-access service | the framework's explicit HTTP boundary for a feature |
| explicit form model | the framework's form API for non-trivial forms |
| legacy framework constructs | constructs the framework rule restricts for new code |
| frontend knowledge skill | technique, examples, scaffolding, and security-review notes |

## Required Facets

| Facet | Location | Loading |
|---|---|---|
| planning | `docs/capabilities/frontend.md` | always (import in `CLAUDE.md`) |
| rules | `.claude/rules/frontend-framework.md`, including the bindings table | path (frontend) |
| knowledge | a knowledge skill of the implementation, including § Scaffolding | on demand |

## Required Properties

Test runner, E2E tool, scaffold command, and the bindings for the
framework-independent frontend rule.

```json
{
  "slot": "frontend",
  "slotType": "leaf",
  "required": false,
  "requiredFacets": {
    "planning": "docs/capabilities/frontend.md",
    "rules": ".claude/rules/frontend-framework.md",
    "knowledge": null
  },
  "requiredProperties": ["testRunner", "e2eTool", "scaffoldCommand", "bindings"],
  "requiredEnforcement": ["notByDefaultPackages", "devOnlyPackages"],
  "roles": ["feature data-access service", "explicit form model", "legacy framework constructs", "frontend knowledge skill"]
}
```
