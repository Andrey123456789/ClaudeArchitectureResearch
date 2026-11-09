---
paths:
  - "backend/**/*Tests/**/*"
---

> Kind: STD | Scope: backend-tests | Capability: backend-testing/nunit | Loading: path-scoped (frontmatter paths)

# Test Framework — NUnit

- Default: NUnit is the .NET automated test framework. In an established project that deliberately uses another framework, follow that convention; do not introduce a second test framework without a concrete reason.

Technique: `dotnet-testing`. Enforced by: `.claude/scripts/facets/test-framework.cjs` (flags additional test frameworks).
