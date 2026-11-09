---
paths:
  - "backend/**"
  - "frontend/**"
---

> Level: 1 Architecture · Owns: physical structure by responsibility and role-revealing names · Scope: common · Loads: path; read explicitly by `project-structure`

# Code Organization

- **Must not** create speculative projects, infrastructure, empty directory trees or generic `Common`, `Helpers` or `Utils` buckets merely to make the repository look architectural. Create a project or directory when it contains real code with a cohesive responsibility.

## Role-revealing names (guidance)

- Prefer type names and immediate directories that reveal each type's role: `Service` (use-case orchestration), `Dto` (data transfer), `Request`/`Response` (Application operation contracts; HTTP contracts belong to Api), `Result`/`Outcome`, `Validator`, `Rules`/`Policy` (decision or workflow rules), `Factory`, `Mapper`, `Adapter`.
- Avoid ambiguous names whose role cannot be inferred without opening the file — prefer `TaskWorkflowRules`, `TaskWorkflowPolicy` or `TaskWorkflowService` over `TaskWorkflow`.
- Prefer responsibility-specific subdirectories only when a flat feature directory becomes hard to navigate; avoid subdirectories that classify one or two obvious files.
- Avoid generic `Models` buckets when a more specific responsibility can be named.
