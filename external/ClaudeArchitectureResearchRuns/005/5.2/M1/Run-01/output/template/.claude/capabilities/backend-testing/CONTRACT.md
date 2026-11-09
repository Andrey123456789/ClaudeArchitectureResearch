> **Capability contract** · Slot: backend-testing (required leaf) · Owns: required facets and properties, replacement obligations · Scope: backend-tests · Loading: maintainer-only (read by `template-maintenance` and the checkers)

# Backend-Testing Slot Contract

The backend-testing slot supplies the .NET test framework. Framework-independent
test policy — test levels, behavior focus, determinism and isolation, provider
fidelity, probe-to-test preservation, coverage, naming — stays outside the module
(`testing.md`, `verify`, `development-workflow`). Test-project placement comes
from the frame's `test-project role`.

## Required Facets

- `test-framework-rule` — path-loaded rule for backend test projects: the default
  framework, its packages, and its binding of the neutral testing vocabulary.
- `test-framework-reference` — the `dotnet-testing` private reference with the
  framework's syntax, examples, scaffold and run commands.

## Required Properties

- `packages` — framework packages.
- `testProjectMarkers` — package names that identify a test project (used by the
  architecture check to apply test-reference limits).
- `commands` — scaffold and run commands.
- `vocabularyBinding` — framework forms of the neutral terms used by `testing.md`.

## Replacement Obligations

Replacing the framework (for example with xUnit) replaces the module's two facets
and properties; neutral test policy and workflows stay unchanged.

```json
{
  "slot": "backend-testing",
  "status": "required",
  "frame": false,
  "requiredFacets": ["test-framework-rule", "test-framework-reference"],
  "requiredProperties": ["packages", "testProjectMarkers", "commands", "vocabularyBinding"]
}
```
