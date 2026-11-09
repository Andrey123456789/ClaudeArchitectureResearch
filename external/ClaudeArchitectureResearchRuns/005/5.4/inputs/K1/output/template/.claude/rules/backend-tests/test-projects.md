---
paths:
  - "backend/**/*Tests/**/*"
---

> Kind: STD | Scope: backend-tests | Capability: architecture/clean-architecture | Loading: path-scoped (frontmatter paths)

# Test Projects — Clean Architecture Frame

- Backend test projects must not have broader production-project references than their test scope requires; they follow the same inward dependency discipline as production projects. Typical references:

  | Test project | References |
  |---|---|
  | `<Name>.Domain.Tests` (optional) | Domain |
  | `<Name>.Application.Tests` | Application, Domain as needed |
  | `<Name>.IntegrationTests` | Api (other layers are exercised through the host) |
  | `<Name>.Infrastructure.Tests` (optional) | Infrastructure, narrower references as required |

Placement: decision register (Project defaults). Enforced by: `.claude/scripts/facets/architecture-style.cjs`.
