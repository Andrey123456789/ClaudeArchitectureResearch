---
paths:
  - "backend/**/*"
---
> Level: 3-project | Capability: persistence/ef-core (persistence.decision) | Owns: selected persistence stack | Scope: backend | Loads: always (imported by CLAUDE.md)

# Persistence Stack

Default persistence is Entity Framework Core with Microsoft SQL Server
(provider package Microsoft.EntityFrameworkCore.SqlServer). Provider-specific
concerns stay out of the use-case and domain-model roles.
