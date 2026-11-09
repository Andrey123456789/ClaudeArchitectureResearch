> Capability contract: backend-testing · Leaf slot (required) · Maintainer metadata · Not auto-loaded; read during capability maintenance

# Capability Contract: backend-testing

## Purpose

The backend-testing leaf supplies the .NET test framework: framework-specific
rules, knowledge and technique, commands, scaffold notes, and the adapter data
that lets the neutral architecture and manifest checks recognize test projects.
Framework-independent test policy (levels, behavior focus, determinism,
isolation, probe preservation, provider fidelity, naming) stays in
`.claude/rules/testing.md` outside the module. Test-project placement belongs to
the architecture frame.

## Role Vocabulary Exposed to Other Instructions

| Role | Meaning |
|---|---|
| test framework | the selected framework and its conventions (`.claude/rules/test-framework.md`) |
| explicit case mechanism | the framework construct for explicit case tables |
| backend-testing knowledge skill | technique, examples, and test-project setup |

## Required Facets

| Facet | Location | Loading |
|---|---|---|
| planning | `docs/capabilities/backend-testing.md` | always (import in `CLAUDE.md`) |
| rules | `.claude/rules/test-framework.md` | path (backend tests) |
| knowledge | a knowledge skill of the implementation, including § Test Project Setup | on demand |

## Required Properties

Framework name, framework/adapter packages, explicit case mechanism, fixture
lifecycle, and the filtered test command.

```json
{
  "slot": "backend-testing",
  "slotType": "leaf",
  "required": true,
  "requiredFacets": {
    "planning": "docs/capabilities/backend-testing.md",
    "rules": ".claude/rules/test-framework.md",
    "knowledge": null
  },
  "requiredProperties": ["framework", "packages", "caseMechanism", "fixtureLifecycle", "filterCommand"],
  "requiredEnforcement": ["testFrameworkPackages", "competingFrameworkPackages"],
  "roles": ["test framework", "explicit case mechanism", "backend-testing knowledge skill"]
}
```
